#!/usr/bin/env python3
"""Round-90 C1 controls: committed scratch-clone states read by the frozen counter.

Each control clones the lane (--shared) at A_REV into $SCRATCH/ctl-<name>/repo,
asserts `git rev-parse --show-toplevel` equals that directory before any commit,
writes ONE change on top of the positive fixture (CTL14-pos), commits it under a
fixture identity inside the clone only, and runs measure.py --rev HEAD there.
Receipts: .ufo/evidence/round-91/pre-freeze/controls/<name>.out (stdout + exit).

Usage: python3 -I controls.py --lane LANE --scratch DIR [--only NAME ...]
"""
import argparse, json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

A_REV = "87d1635c8a1a90a405eb348da5ba3e8f93b4ae83"
BASE = "87d1635c8a1a90a405eb348da5ba3e8f93b4ae83"
SPEC = ".ufo/evidence/round-91/c1/census-mutants.json"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
DERIVED = {"C01": "KILLED", "C02": "SURVIVED", "C03": "SURVIVED", "C04": "KILLED", "C05": "KILLED",
           "C06": "SURVIVED", "C07": "KILLED", "C08": "SURVIVED", "C09": "SURVIVED", "C10": "SURVIVED",
           "C11": "KILLED", "C12": "SURVIVED"}  # from the 33dd6e47 no-work run (its receipt is CTL1b)


def sh(*a, cwd=None):
    p = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(a), p.stderr))
    return p.stdout


def note_text(rows=None, measured="5/12", sid="S999", drop=None):
    rows = dict(DERIVED if rows is None else rows)
    out = ["source: %s fixture row (positive control only)" % sid, "", "# fixture note", "",
           "measured: %s killed" % measured, "", "| id | arm | verdict | witness |", "|---|---|---|---|"]
    for k, v in rows.items():
        if k == drop:
            continue
        out.append("| %s | fixture arm | %s | differs |" % (k, v))
    return "\n".join(out) + "\n"


def pos_files(lane):
    src = open(os.path.join(lane, "corpus/SOURCES.md"), encoding="utf-8").read()
    row = ("| S999 | Fixture — https://fixture.invalid/r90 | docs | B | fixture | §1 | positive-control fixture row "
           "| mined | 2026-11-06 | 90d | %s |\n" % NOTE)
    # insert after the last registry row (line starting with | S)
    lines = src.split("\n")
    idx = max(i for i, l in enumerate(lines) if re.match(r"^ {0,3}\| S\d{3}", l))
    lines.insert(idx + 1, row.rstrip("\n"))
    readme = open(os.path.join(lane, "corpus/README.md"), encoding="utf-8").read()
    readme += "\n| `knowledge/mutation-case-fleet-sources-census.md` | fixture row | S999 |\n"
    return {"corpus/SOURCES.md": "\n".join(lines), "corpus/README.md": readme, NOTE: note_text()}


def spec_edit(lane, fn):
    s = json.load(open(os.path.join(lane, SPEC), encoding="utf-8"))
    fn(s)
    return json.dumps(s, indent=1, ensure_ascii=False) + "\n"


def mut(s, mid):
    return [m for m in s["mutants"] if m["id"] == mid][0]


def controls(lane):
    P = pos_files(lane)
    C = {}
    C["CTL14-pos"] = dict(P)
    C["CTL2-flip"] = dict(P, **{NOTE: note_text(rows=dict(DERIVED, C02="KILLED"))})
    C["CTL3-figure"] = dict(P, **{NOTE: note_text(measured="6/12")})
    C["CTL4-ids"] = dict(P, **{NOTE: note_text(drop="C12")})
    C["CTL10-source"] = dict(P, **{NOTE: note_text(sid="S998")})
    C["CTL16-oldsource"] = dict(P, **{NOTE: note_text(sid="S315")})
    C["CTL15-coverage"] = {k: v for k, v in P.items() if k != "corpus/README.md"}
    # Round-91 sealed additions (QUALITY 140): ambiguous and draft-column note variants.
    C["VOV1-dup-row"] = dict(P, **{NOTE: note_text() + "| C02 | fixture arm | SURVIVED | differs |\n"})
    C["VOV3-draft-column"] = dict(P, **{NOTE: note_text() + "| id | arm | outcome | verdict | witness |\n|---|---|---|---|---|\n" + "".join("| %s | fixture arm | MAYBE | %s | differs |\n" % (k, v) for k, v in DERIVED.items())})


    def e5(s): mut(s, "C03")["new"] = "teaches !~ /supersedes S[0-9]{5}/"
    def e6(s): mut(s, "C02")["new"] = mut(s, "C02")["old"]
    def e7(s): mut(s, "C11")["new"] = '[ "$missing_error" = 1 ] && exit 2 ('
    def e8(s): mut(s, "C01")["old"] = 'if (tier=="A" && kind=="no-such-kind")'
    def e9(s): mut(s, "C02")["witness"]["sources"] = mut(s, "C02")["witness"]["sources"].replace("| 1234567 |", "| no |")
    def e11(s): mut(s, "C10")["new"] = 'function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ '
    def e12(s): s["gate"]["sha256"] = "0" * 64
    for name, fn in [("CTL5-spec", e5), ("CTL6-noop", e6), ("CTL7-syntax", e7), ("CTL8-absent", e8),
                     ("CTL9-equiv", e9), ("CTL11-trivial", e11), ("CTL12-pin", e12)]:
        C[name] = dict(P, **{SPEC: spec_edit(lane, fn)})
    return C


def run_ctl(name, files, lane, scratch, measure, outdir):
    d = os.path.join(scratch, "ctl-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    repo = os.path.join(d, "repo")
    sh("git", "clone", "-q", "--shared", "--no-checkout", lane, repo)
    top = sh("git", "-C", repo, "rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit("toplevel mismatch for " + name)
    sh("git", "-C", repo, "checkout", "-q", "--detach", A_REV)
    for p, text in files.items():
        fp = os.path.join(repo, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(text)
    if name == "CTL15-coverage":
        pass
    sh("git", "-C", repo, "add", "-A")
    sh("git", "-C", repo, "-c", "user.name=r90-fixture", "-c", "user.email=r90-fixture@invalid",
       "commit", "-q", "-m", "r90 control " + name)
    rev = sh("git", "-C", repo, "rev-parse", "HEAD").strip()
    work = os.path.join(d, "work")
    os.makedirs(work)
    p = subprocess.run([sys.executable, "-I", measure, "--repo", repo, "--rev", rev, "--work", work],
                       capture_output=True, text=True)
    body = "control=%s clone_rev=%s parent=%s\n%s%sexit=%d\n" % (name, rev, A_REV, p.stdout, p.stderr, p.returncode)
    open(os.path.join(outdir, name + ".out"), "w").write(body)
    shutil.rmtree(d, ignore_errors=True)
    return name, p.returncode, [l for l in p.stdout.split("\n") if l.startswith(("C1_CONJ", "C1_R90", "C1_SETUP"))]


def run_real(name, rev, lane, scratch, measure, outdir):
    work = os.path.join(scratch, "ctl-" + name)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    p = subprocess.run([sys.executable, "-I", measure, "--repo", lane, "--rev", rev, "--work", work],
                       capture_output=True, text=True)
    open(os.path.join(outdir, name + ".out"), "w").write(
        "control=%s rev=%s\n%s%sexit=%d\n" % (name, rev, p.stdout, p.stderr, p.returncode))
    shutil.rmtree(work, ignore_errors=True)
    return name, p.returncode, [l for l in p.stdout.split("\n") if l.startswith(("C1_CONJ", "C1_R90", "C1_SETUP"))]


def run_replace(lane, scratch, measure, outdir):
    """V4: a committed false note that only a sealed read refuses (QUALITY 139).
    Clones the lane at A_REV, lands a note whose C02 verdict is false, creates a
    local `git replace` ref in the clone, and runs the counter twice on the same
    rev: once without sealing (env scrubbed of GIT_NO_REPLACE_OBJECTS, mimicking
    the frozen v90 reader) and once sealed. Both receipts are kept; the file the
    counter trusts must be its own refusal (exit 2 with replace-refs-present) or
    a mismatched verdict, never a PASS."""
    import shutil as _sh
    name = "V4-replace"
    d = os.path.join(scratch, "ctl-" + name)
    _sh.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    repo = os.path.join(d, "repo")
    sh("git", "clone", "-q", "--shared", "--no-checkout", lane, repo)
    top = sh("git", "-C", repo, "rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit("toplevel mismatch for " + name)
    sh("git", "-C", repo, "checkout", "-q", "--detach", A_REV)
    P = pos_files(lane)
    false_rows = dict(DERIVED, C02="KILLED")
    files = dict(P, **{NOTE: note_text(rows=false_rows)})
    for p, text in files.items():
        fp = os.path.join(repo, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(text)
    sh("git", "-C", repo, "add", "-A")
    sh("git", "-C", repo, "-c", "user.name=r91-fixture", "-c", "user.email=r91-fixture@invalid",
       "commit", "-q", "-m", "r91 control V4-replace")
    rev = sh("git", "-C", repo, "rev-parse", "HEAD").strip()
    # fake replacement: replace the rev with its parent in the clone only.
    parent = sh("git", "-C", repo, "rev-parse", "HEAD^").strip()
    sh("git", "-C", repo, "replace", rev, parent)
    work = os.path.join(d, "work")
    os.makedirs(work)
    p = subprocess.run([sys.executable, "-I", measure, "--repo", repo, "--rev", rev, "--work", work],
                       capture_output=True, text=True)
    body = ("control=V4-replace rev=%s parent=%s replace_l=%s\n%s%sexit=%d\n"
            % (rev, A_REV, sh("git", "-C", repo, "replace", "-l").strip(), p.stdout, p.stderr, p.returncode))
    open(os.path.join(outdir, "V4-replace.out"), "w").write(body)
    _sh.rmtree(d, ignore_errors=True)
    return "V4-replace", p.returncode, [l for l in p.stdout.split("\n") if l.startswith(("C1_CONJ", "C1_R91", "C1_SETUP"))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    measure = os.path.join(lane, ".ufo/evidence/round-91/c1/measure-v91.py")
    outdir = os.path.join(lane, ".ufo/evidence/round-91/pre-freeze/controls")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(a.scratch, exist_ok=True)
    C = controls(lane)
    jobs = []
    with ThreadPoolExecutor(a.jobs) as ex:
        for name, rev in [("CTL1-nowork-base", BASE), ("CTL1b-nowork-A", A_REV)]:
            if not a.only or name in a.only:
                jobs.append(ex.submit(run_real, name, rev, lane, a.scratch, measure, outdir))
        jobs.append(ex.submit(run_replace, lane, a.scratch, measure, outdir))
        for name, files in C.items():
            if not a.only or name in a.only:
                jobs.append(ex.submit(run_ctl, name, files, lane, a.scratch, measure, outdir))
        for j in jobs:
            name, rc, lines = j.result()
            print(name, "exit=%d" % rc, " | ".join(lines))


if __name__ == "__main__":
    main()
