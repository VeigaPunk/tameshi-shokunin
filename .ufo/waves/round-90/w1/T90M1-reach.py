#!/usr/bin/env python3
"""T90M1 reachability probe: for a surviving counter defect, build the forged committed
state it would accept and run BOTH counters on the SAME clone revision.

A defect is REACHABLE iff there exists a committed lane state (note / README / SOURCES /
spec) that the pristine counter rejects and the mutated counter accepts. Because the
pristine counter pins the spec bytes with SPEC_SHA, a forgery that edits the spec is only
reachable when the defect itself drops that pin (D14); note/README/SOURCES edits are
reachable for any defect that drops the corresponding check.

Usage:
  python3 T90M1-reach.py --lane LANE --scratch DIR --driver <patched controls.py> \
      --pristine <measure.py> --mutants DIR --out reach.json [--only D04 D06 ...]
"""
import argparse, importlib.util, json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

A_REV = "33dd6e474ec3660f72c3c1e1c30105269807fe12"


def load_driver(path):
    spec = importlib.util.spec_from_file_location("ctl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_repo(lane, scratch, name, files):
    d = os.path.join(scratch, "reach", name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    repo = os.path.join(d, "repo")
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", lane, repo], check=True)
    top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit("toplevel mismatch " + name)
    subprocess.run(["git", "-C", repo, "checkout", "-q", "--detach", A_REV], check=True)
    for p, text in files.items():
        fp = os.path.join(repo, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(text)
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=r90-fixture",
                    "-c", "user.email=r90-fixture@invalid", "commit", "-q", "-m", "r90 reach " + name],
                   check=True)
    rev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True,
                         text=True).stdout.strip()
    return d, repo, rev


def measure(measure_py, repo, rev, work):
    os.makedirs(work)
    p = subprocess.run([sys.executable, "-I", measure_py, "--repo", repo, "--rev", rev,
                        "--work", work], capture_output=True, text=True)
    lines = [l for l in p.stdout.split("\n") if l.startswith(("C1_CONJ", "C1_R90", "C1_SETUP"))]
    return p.returncode, lines, p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--driver", required=True)
    ap.add_argument("--pristine", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--par", type=int, default=4)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    scratch = os.path.realpath(a.scratch)
    C = load_driver(a.driver)
    P = C.pos_files(lane)
    NOTE = C.NOTE
    DERIVED = C.DERIVED

    def note_with_dup():
        t = C.note_text()
        return t + "| C02 | fixture arm | SURVIVED | differs |\n"

    def note_ambiguous():
        rows = dict(DERIVED)
        out = ["source: S999 fixture row (positive control only)", "", "# fixture note", "",
               "measured: 5/12 killed", "", "| id | arm | verdict | witness |", "|---|---|---|---|"]
        for k, v in rows.items():
            if k == "C02":
                out.append("| C02 | fixture arm | SURVIVED | KILLED |")
            else:
                out.append("| %s | fixture arm | %s | differs |" % (k, v))
        return "\n".join(out) + "\n"

    def sources_with_s315_usedby():
        src = P["corpus/SOURCES.md"]
        out = []
        for line in src.split("\n"):
            if re.match(r"^ {0,3}\| S315 \|", line):
                c = line.split("|")
                c[8] = " mined "
                c[11] = " " + NOTE + " "
                line = "|".join(c)
            out.append(line)
        return "\n".join(out)

    def spec_weakened_c01():
        """Replace C01's killed mutant with a copy of C02's survivor (same gate string,
        same witness) and let the note claim 4/12 killed: a coverage forgery that only
        the spec pin can reject."""
        s = json.load(open(os.path.join(lane, C.SPEC), encoding="utf-8"))
        c02 = [m for m in s["mutants"] if m["id"] == "C02"][0]
        c01 = [m for m in s["mutants"] if m["id"] == "C01"][0]
        c01.update({"old": c02["old"], "new": c02["new"], "witness": c02["witness"],
                    "arm": "swapped for a survivor"})
        return json.dumps(s, indent=1, ensure_ascii=False) + "\n"

    def note_four_killed():
        rows = dict(DERIVED, C01="SURVIVED")
        return C.note_text(rows=rows, measured="4/12")

    CASES = {
        "D04": ("note with a duplicated C02 row (same verdict)",
                dict(P, **{NOTE: note_with_dup()})),
        "D05": ("note cites S315 and SOURCES.md S315 used-by gains the note",
                dict(P, **{NOTE: C.note_text(sid="S315"), "corpus/SOURCES.md": sources_with_s315_usedby()})),
        "D06": ("note prints measured: 5/9 killed (right numerator, wrong denominator)",
                dict(P, **{NOTE: C.note_text(measured="5/9")})),
        "D11": ("note table says C02 KILLED while derived is SURVIVED, measured: 5/12",
                dict(P, **{NOTE: C.note_text(rows=dict(DERIVED, C02="KILLED"))})),
        "D12": ("corpus/README.md does not name the case note",
                {k: v for k, v in P.items() if k != "corpus/README.md"}),
        "D13": ("spec names a gate sha256 that does not match the gate blob",
                dict(P, **{C.SPEC: C.spec_edit(lane, lambda s: s["gate"].__setitem__("sha256", "0" * 64))})),
        "D14": ("spec swaps C01's killed mutant for a survivor; note claims 4/12 killed",
                dict(P, **{C.SPEC: spec_weakened_c01(), NOTE: note_four_killed()})),
        "D19": ("note row for C02 carries both SURVIVED and KILLED",
                dict(P, **{NOTE: note_ambiguous()})),
    }
    cases = {k: v for k, v in CASES.items() if not a.only or k in a.only}
    res = {}

    def one(did, desc, files):
        mut = os.path.join(a.mutants, did, "measure.py")
        if not os.path.exists(mut):
            return did, {"desc": desc, "error": "mutant missing"}
        d, repo, rev = build_repo(lane, scratch, did, files)
        prc, plines, pout = measure(a.pristine, repo, rev, os.path.join(d, "work-pristine"))
        mrc, mlines, mout = measure(mut, repo, rev, os.path.join(d, "work-mutant"))
        with open(os.path.join(d, "pristine.out"), "w") as f:
            f.write(pout)
        with open(os.path.join(d, "mutant.out"), "w") as f:
            f.write(mout)
        out = {"desc": desc, "rev": rev, "pristine_exit": prc, "mutant_exit": mrc,
               "pristine": plines, "mutant": mlines, "reachable": prc != 0 and mrc == 0}
        print("%s pristine_exit=%d mutant_exit=%d reachable=%s | %s" % (
            did, prc, mrc, out["reachable"], desc), flush=True)
        shutil.rmtree(d, ignore_errors=True)
        return did, out

    with ThreadPoolExecutor(a.par) as ex:
        futs = [ex.submit(one, did, desc, files) for did, (desc, files) in sorted(cases.items())]
        for f in futs:
            did, out = f.result()
            res[did] = out
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print("\nREACHABLE %d/%d" % (sum(1 for v in res.values() if v.get("reachable")), len(res)))


if __name__ == "__main__":
    main()
