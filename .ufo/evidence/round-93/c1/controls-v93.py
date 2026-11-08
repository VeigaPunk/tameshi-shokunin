#!/usr/bin/env python3
"""Round-93 C1 control battery: committed scratch-clone states read by the frozen
counter .ufo/evidence/round-93/c1/measure-v93.py.

Every control clones the lane (--shared) at --rev into a scratch dir, asserts
`git rev-parse --show-toplevel` equals that directory before any commit, writes
ONE change on top of the honest state, commits it under a fixture identity
inside the clone only, and runs the frozen counter (extracted from --rev's
object store, never the working tree) with --rev HEAD there.

Two properties round 92's driver lacked, both from its own `## Mistakes`:

  * M4 (receipt overwrite): a re-run writes `<name>.rerun-<n>.out` and never
    overwrites a receipt that already exists in --outdir.
  * M1 (selection vs declaration): the summary is derived from the receipts on
    disk, and every pre-registered control name must have a receipt; a missing
    receipt is a MISSING row and fails the run, it is never silently dropped.

Mutant controls (D01-D05) are counter copies whose SELF_SHA256 line is
recomputed for the edited bytes (a mutation study, declared in the plan); the
frozen bytes stay pinned and are never modified.

Usage: python3 -I controls-v93.py --lane LANE --rev A_REV --base BASE_REV \
         --work EMPTY_DIR --outdir DIR [--only NAME ...] [--jobs N]
Exit: 0 every pre-registered control has a receipt matching its expectation;
      1 a mismatch or a missing receipt.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

COUNTER_PATH = ".ufo/evidence/round-93/c1/measure-v93.py"
SPEC = ".ufo/evidence/round-93/c1/census-mutants.json"
PINS = ".ufo/evidence/round-93/c1/pins.json"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
LESSON = "corpus/lessons/round-93.md"
READY = "corpus/README.md"
SRC = "corpus/SOURCES.md"
DERIVED = {"C01": "KILLED", "C02": "SURVIVED", "C03": "SURVIVED", "C04": "KILLED", "C05": "KILLED",
           "C06": "SURVIVED", "C07": "KILLED", "C08": "SURVIVED", "C09": "SURVIVED",
           "C10": "SURVIVED", "C11": "KILLED", "C12": "SURVIVED"}
SELF_LINE = re.compile(rb'^SELF_SHA256 = "[0-9a-f]{64}"\n', re.M)


def sh(*a, cwd=None, check=True):
    p = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(a), p.stderr))
    return p.stdout


def recompute_pin(path):
    b = open(path, "rb").read()
    norm = SELF_LINE.sub(b"", b)
    h = hashlib.sha256(norm).hexdigest()
    open(path, "wb").write(SELF_LINE.sub(('SELF_SHA256 = "%s"\n' % h).encode(), b, count=1))
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def note_text(rows=None, measured="5/12", drop=None, extra="", header=None, base=None):
    rows = dict(DERIVED if rows is None else rows)
    if base is not None:
        out = base
        if drop:
            out = "\n".join(l for l in out.split("\n") if not l.startswith("| %s " % drop))
        return out + extra
    out = ["source: S316/S321 fixture note (positive control only)", "",
           "# fixture note", "", "measured: %s killed" % measured, "",
           header or "| id | arm | verdict | witness |", "|---|---|---|---|"]
    for k, v in rows.items():
        if k == drop:
            continue
        out.append("| %s | fixture arm | %s | differs |" % (k, v))
    return "\n".join(out) + "\n" + extra


def spec_edit(lane, fn):
    s = json.load(open(os.path.join(lane, SPEC), encoding="utf-8"))
    fn(s)
    return json.dumps(s, indent=1, ensure_ascii=False) + "\n"


def mut(s, mid):
    return [m for m in s["mutants"] if m["id"] == mid][0]


HIDDEN3 = ("\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n" + "".join(
    "| C%03d | fixture arm | fixture edit | %s | differs |\n"
    % (i, "SURVIVED" if DERIVED["C%02d" % i] == "KILLED" else "KILLED") for i in range(1, 13)))
HIDDENX = ("\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n" + "".join(
    "| X%d | fixture arm | fixture edit | KILLED | differs |\n" % i for i in range(1, 13)))
RENAMED = ("\n| id | arm | result | witness |\n|---|---|---|---|\n"
           "| C01 | fixture arm | SURVIVED | differs |\n| C02 | fixture arm | KILLED | differs |\n")


def edit_readme_denial(lane):
    p = os.path.join(lane, READY)
    txt = open(p, encoding="utf-8").read()
    return txt + "\n| `knowledge/mutation-case-fleet-sources-census.md` | row appended by the " \
                 "control battery: not admitted | fixture |\n"


def edit_readme_absent(lane):
    p = os.path.join(lane, READY)
    kept = [l for l in open(p, encoding="utf-8").read().split("\n")
            if "knowledge/mutation-case-fleet-sources-census.md" not in l]
    return "\n".join(kept)


def states(lane):
    """name -> dict(files, expect, mutations). expect=(exit, {conj: bool}|{'__pass':True}|{'__setup':tok})"""
    real_note = open(os.path.join(lane, NOTE), encoding="utf-8").read()
    a13 = real_note.replace(
        "| survivor | lanes hit | effect on live registries |\n|---|---|---|\n| C12 used-by trim |",
        "| id | survivor | lanes hit | effect on live registries |\n|---|---|---|---|\n"
        "| C12 |  used-by trim |")
    for old, new in (("| C03 supersedes width |", "| C03 | supersedes width |"),
                     ("| C09 fragment strip |", "| C09 | fragment strip |"),
                     ("| C10 spaced cadence |", "| C10 | spaced cadence |"),
                     ("| C02, C06, C08 |", "| C02 | C06, C08 |")):
        a13 = a13.replace(old, new, 1)
    vcell = real_note + ("\n| survivor | witness | note |\n|---|---|---|\n"
                         "| C02 | differs | verdict |\n| **C03** | differs | bold id |\n")
    C = {}
    C["pos-real"] = dict(files={}, expect=(0, {"__pass": True}))
    C["pos-fixture"] = dict(files={NOTE: note_text()}, expect=(0, {"__pass": True}))
    C["pos-honest-a13"] = dict(files={NOTE: a13}, expect=(0, {"__pass": True}))
    C["pos-honest-verdict-cell"] = dict(files={NOTE: vcell}, expect=(0, {"__pass": True}))
    C["hidden-c001"] = dict(files={NOTE: real_note + HIDDEN3},
                            expect=(1, {"verdict_tables": False}))
    C["hidden-x"] = dict(files={NOTE: real_note + HIDDENX},
                         expect=(1, {"verdict_tables": False}))
    C["renamed-result"] = dict(files={NOTE: real_note + RENAMED}, expect=(1, {"ids": False}))
    C["pseudo-row"] = dict(files={NOTE: real_note + "| C02 | fixture arm | KILLED | differs |\n"},
                           expect=(1, {"ids": False}))
    C["position"] = dict(files={NOTE: note_text(
        header="| id | arm | witness | verdict |",
        extra="| C12 | fixture arm | KILLED | MAYBE |\n")}, expect=(1, {"ids": False}))
    C["drop-c12"] = dict(files={NOTE: note_text(drop="C12")}, expect=(1, {"ids": False}))
    C["dup-row"] = dict(files={NOTE: note_text(
        extra="| C02 | fixture arm | KILLED | differs |\n")}, expect=(1, {"ids": False}))
    C["inverted"] = dict(files={NOTE: note_text(
        rows={k: ("SURVIVED" if v == "KILLED" else "KILLED") for k, v in DERIVED.items()})},
        expect=(1, {"mismatched0": False}))
    C["note-absent"] = dict(files={}, drop_note=True, expect=(1, {"note": False}))
    C["pins-mutated"] = dict(files={PINS: json.dumps(
        {"fixtures": "scripts/fixtures/sources-census",
         "gate_commit": "f47ad6ba8d306f8125597401cb2ce45c1297a593",
         "gate_path": "scripts/sources-census.sh", "gate_sha256": "0" * 64,
         "spec_sha256": "ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290"},
        indent=1) + "\n"}, expect=(1, {"pins": False}))
    C["spec-shape"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C07").update(id="C06"))},
                           expect=(1, {"spec": False}))
    C["short-spec"] = dict(files={SPEC: spec_edit(
        lane, lambda s: s.__setitem__("mutants", [m for m in s["mutants"] if m["id"] != "C12"]))},
        expect=(1, {"n_min": False}))
    C["pin-mismatch"] = dict(files={SPEC: spec_edit(lane, lambda s: s["gate"].update(
        sha256="0" * 64))}, expect=(1, {"pin": False}))
    C["noop-mutant"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C02").update(
        new=mut(s, "C02")["old"]))}, expect=(1, {"valid0": False}))
    C["syntax-mutant"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C11").update(
        new='[ "$missing_error" = 1 ] && exit 2 ('))}, expect=(1, {"valid0": False}))
    C["trivial-mutant"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C10").update(
        new='function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ '))},
        expect=(1, {"trivial0": False}))
    C["timeout"] = dict(files={SPEC: spec_edit(lane, lambda s: s.update(timeout_s=0.001))},
                        expect=(1, {"inconclusive0": False}))
    C["figure"] = dict(files={NOTE: note_text(measured="6/12")}, expect=(1, {"figure": False}))
    C["witness-same"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C02")["witness"].update(
        sources=mut(s, "C02")["witness"]["sources"].replace("| 1234567 |", "| no |")))},
        expect=(1, {"witnessed": False}))
    C["source-noquote"] = dict(files={LESSON: "\n".join(
        l for l in open(os.path.join(lane, LESSON), encoding="utf-8").read().split("\n")
        if "A fenced code block begins with a code fence" not in l)},
        expect=(1, {"source": False}))
    C["source-status"] = dict(files={SRC: "\n".join(
        l.replace("| S321 |", "| S321 |", 1).replace("| mined |", "| queued |", 1)
        if l.startswith("| S321 |") else l
        for l in open(os.path.join(lane, SRC), encoding="utf-8").read().split("\n"))},
        expect=(1, {"source": False}))
    C["coverage-denial"] = dict(files={READY: edit_readme_denial(lane)},
                                expect=(1, {"coverage": False}))
    C["coverage-absent"] = dict(files={READY: edit_readme_absent(lane)},
                                expect=(1, {"coverage": False}))
    return C


def mutant_edits(counter_text):
    """D01-D05: single-rule removals (D05 removes a named pair, stated as such)."""
    out = {}
    a = """        toks = [c for c in split_cells(raw) if c in VERDICTS]
        if toks:
            bad.append("stray-verdict:%d:%s" % (oi + 1, raw.strip()[:24]))
"""
    assert a in counter_text, "D01 anchor"
    out["D01"] = (counter_text.replace(a, "        pass  # D01: stray-verdict scan removed\n", 1),
                  "renamed-result")
    b = """DENIAL_TOKENS = ("not admitted", "not-admitted", "uncertified", "withdrawn", "refused",
                 "rejected")"""
    assert b in counter_text, "D02 anchor"
    out["D02"] = (counter_text.replace(b, "DENIAL_TOKENS = ()  # D02: denial list emptied", 1),
                  "coverage-denial")
    c = "            pins_ok = all(pins.get(k) == v for k, v in derived.items())"
    assert c in counter_text, "D03 anchor"
    out["D03"] = (counter_text.replace(c, "            pins_ok = True  # D03: pins conjunct removed", 1),
                  "pins-mutated")
    d = "        figure_ok = len(heads) == 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n"
    assert d in counter_text, "D04 anchor"
    out["D04"] = (counter_text.replace(d, "        figure_ok = True  # D04: figure check removed", 1),
                  "figure")
    e1 = '    vtables_ok = info["verdict_tables"] == 1'
    e2 = """            if first not in spec_ids:
                bad.append("out-of-set:%d:%s" % (ln + 1, first[:24]))
                continue
"""
    e3 = "    ids_ok = (note is not None and not bad and set(note_rows) == spec_ids)"
    assert e1 in counter_text and e2 in counter_text and e3 in counter_text, "D05 anchors"
    d05 = (counter_text.replace(e1, "    vtables_ok = True  # D05: table-count rule removed", 1)
           .replace(e2, "            pass  # D05: out-of-set rule removed\n", 1)
           .replace(e3, "    ids_ok = (note is not None and not bad)  # D05: id-set equality removed", 1))
    out["D05"] = (d05, "hidden-c001")
    return out


def materialize_state(repo, spec):
    for p, text in spec.get("files", {}).items():
        fp = os.path.join(repo, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(text)
    if spec.get("drop_note"):
        np_ = os.path.join(repo, NOTE)
        if os.path.exists(np_):
            os.unlink(np_)


def clone_at(lane, rev, dest):
    sh("git", "clone", "-q", "--shared", "--no-checkout", lane, dest)
    top = sh("git", "-C", dest, "rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(dest):
        raise SystemExit("toplevel mismatch for " + dest)
    sh("git", "-C", dest, "checkout", "-q", "--detach", rev)
    return dest


def receipt_path(outdir, name):
    """M4: never overwrite a receipt; a re-run lands as <name>.rerun-<n>.out."""
    p = os.path.join(outdir, name + ".out")
    if not os.path.exists(p):
        return p
    n = 1
    while os.path.exists(os.path.join(outdir, "%s.rerun-%d.out" % (name, n))):
        n += 1
    return os.path.join(outdir, "%s.rerun-%d.out" % (name, n))


def run_ctl(name, spec, lane, rev, counter, scratch, outdir):
    d = tempfile.mkdtemp(dir=scratch, prefix="ctl-" + name + "-")
    try:
        repo = clone_at(lane, rev, os.path.join(d, "repo"))
        materialize_state(repo, spec)
        sh("git", "-C", repo, "add", "-A")
        sh("git", "-C", repo, "-c", "user.name=r93-fixture", "-c", "user.email=r93-fixture@invalid",
           "commit", "-q", "--allow-empty", "-m", "r93 control " + name)
        crev = sh("git", "-C", repo, "rev-parse", "HEAD").strip()
        work = os.path.join(d, "work")
        os.makedirs(work)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", crev,
                            "--work", work], capture_output=True, text=True)
        body = ("control=%s clone_rev=%s parent=%s\nexit=%d\n"
                % (name, crev, rev, p.returncode) + p.stdout + p.stderr)
        with open(receipt_path(outdir, name), "w", encoding="utf-8") as f:
            f.write(body)
        return name, p.returncode, p.stdout
    finally:
        shutil.rmtree(d, ignore_errors=True)


EXPECT_EXTRA = {
    "nowork-base": (2, {"__setup": "spec-absent-at-rev"}),
    "selfpin-edit": (2, {"__setup": "self-pin-mismatch"}),
    "replace-honest": (2, {"__setup": "replace-refs-present"}),
    "D01": (0, {"__pass": True}),
    "D02": (0, {"__pass": True}),
    "D03": (0, {"__pass": True}),
    "D04": (0, {"__pass": True}),
    "D05": (0, {"__pass": True}),
}


def conj_of(out):
    conj = {}
    for line in out.split("\n"):
        if line.startswith("C1_CONJUNCTS "):
            for kv in line.split()[1:]:
                k, v = kv.split("=", 1)
                conj[k] = (v == "true")
    return conj


def grade(name, code, out, want):
    ok = code == want[0]
    if ok and "__pass" in want[1]:
        ok = "C1_R93_PASS=true" in out
    if ok and "__setup" in want[1]:
        ok = ("C1_SETUP " + want[1]["__setup"]) in out
    if ok and "__pass" not in want[1] and "__setup" not in want[1]:
        conj = conj_of(out)
        for k, v in want[1].items():
            if conj.get(k) != v:
                ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--jobs", type=int, default=5)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    os.makedirs(a.outdir, exist_ok=True)
    work = os.path.realpath(a.work)
    if os.path.isdir(work) and os.listdir(work):
        raise SystemExit("work-not-empty")
    os.makedirs(work, exist_ok=True)
    blob = subprocess.run(["git", "-C", lane, "cat-file", "blob", a.rev + ":" + COUNTER_PATH],
                          capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("counter absent at rev")
    counter = os.path.join(work, "counter.py")
    open(counter, "wb").write(blob.stdout)
    print("CONTROL_INSTRUMENT sha256=" + hashlib.sha256(blob.stdout).hexdigest())
    C = states(lane)
    expectations = {n: C[n]["expect"] for n in C}
    expectations.update(EXPECT_EXTRA)
    sel = list(a.only) if a.only else None
    state_names = [n for n in C if sel is None or n in sel]
    with ThreadPoolExecutor(max_workers=min(a.jobs, max(1, len(state_names)))) as ex:
        futs = [ex.submit(run_ctl, n, C[n], lane, a.rev, counter, work, a.outdir)
                for n in state_names]
        for f in futs:
            f.result()
    if sel is None or "nowork-base" in sel:
        w2 = os.path.join(work, "base-work")
        os.makedirs(w2, exist_ok=True)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", lane, "--rev", a.base,
                            "--work", w2], capture_output=True, text=True)
        with open(receipt_path(a.outdir, "nowork-base"), "w", encoding="utf-8") as f:
            f.write("control=nowork-base rev=%s\nexit=%d\n" % (a.base, p.returncode)
                    + p.stdout + p.stderr)
    if sel is None or "selfpin-edit" in sel:
        pe = os.path.join(work, "counter-selfpin-edit.py")
        open(pe, "w").write(blob.stdout.decode() + "\n# post-freeze edit (never committed)\n")
        pw = os.path.join(work, "w-selfpin-edit")
        os.makedirs(pw, exist_ok=True)
        p = subprocess.run([sys.executable, "-I", pe, "--repo", lane, "--rev", a.rev,
                            "--work", pw], capture_output=True, text=True)
        with open(receipt_path(a.outdir, "selfpin-edit"), "w", encoding="utf-8") as f:
            f.write("control=selfpin-edit edit=appended-comment exit-bound-to-the-pin\nexit=%d\n"
                    % p.returncode + p.stdout + p.stderr)
    if sel is None or "replace-honest" in sel:
        st = clone_at(lane, a.rev, os.path.join(work, "st-replace-honest"))
        false_note = note_text(rows={k: ("SURVIVED" if v == "KILLED" else "KILLED")
                                    for k, v in DERIVED.items()})
        false_oid = subprocess.run(["git", "-C", st, "hash-object", "-w", "--stdin"],
                                   input=false_note, capture_output=True, text=True).stdout.strip()
        true_oid = sh("git", "-C", st, "rev-parse", "HEAD:" + NOTE).strip()
        subprocess.run(["git", "-C", st, "replace", true_oid, false_oid], check=True)
        w = os.path.join(work, "w-replace-honest")
        os.makedirs(w, exist_ok=True)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", st, "--rev", "HEAD",
                            "--work", w], capture_output=True, text=True)
        with open(receipt_path(a.outdir, "replace-honest"), "w", encoding="utf-8") as f:
            f.write("control=replace-honest exit=%d\n" % p.returncode + p.stdout + p.stderr)
        shutil.rmtree(st, ignore_errors=True)
    if sel is None or any(n.startswith("D0") for n in (sel or ["D01"])):
        mts = mutant_edits(blob.stdout.decode())
        st = clone_at(lane, a.rev, os.path.join(work, "st-hidden"))
        materialize_state(st, C["hidden-c001"])
        sh("git", "-C", st, "add", "-A")
        sh("git", "-C", st, "-c", "user.name=r93-fixture", "-c", "user.email=r93-fixture@invalid",
           "commit", "-q", "--allow-empty", "-m", "r93 D05 state")
        for n in sorted(mts):
            if sel is not None and n not in sel:
                continue
            text, state_name = mts[n]
            mp = os.path.join(work, "counter-" + n + ".py")
            open(mp, "w").write(text)
            recompute_pin(mp)
            if state_name == "hidden-c001":
                repo = st
            else:
                sd = tempfile.mkdtemp(dir=work, prefix="mstate-" + state_name + "-")
                repo = clone_at(lane, a.rev, os.path.join(sd, "repo"))
                materialize_state(repo, C[state_name])
                sh("git", "-C", repo, "add", "-A")
                sh("git", "-C", repo, "-c", "user.name=r93-fixture", "-c",
                   "user.email=r93-fixture@invalid", "commit", "-q", "--allow-empty",
                   "-m", "r93 mutant state " + state_name)
            mw = os.path.join(work, "mwork-" + n)
            os.makedirs(mw, exist_ok=True)
            p = subprocess.run([sys.executable, "-I", mp, "--repo", repo, "--rev", "HEAD",
                                "--work", mw], capture_output=True, text=True)
            with open(receipt_path(a.outdir, n), "w", encoding="utf-8") as f:
                f.write("mutant=%s state=%s\ncounter_sha=%s\nexit=%d\n" % (
                    n, state_name, hashlib.sha256(open(mp, "rb").read()).hexdigest(),
                    p.returncode) + p.stdout + p.stderr)
        shutil.rmtree(st, ignore_errors=True)

    # summary derived from the receipts on disk; every pre-registered control must
    # have a receipt (M1) - a missing receipt is a MISSING row and fails the run.
    lines, matched, mism, missing = [], 0, [], []
    for n in sorted(expectations):
        if sel is not None and n not in sel:
            continue
        found = None
        for cand in [n + ".out"] + ["%s.rerun-%d.out" % (n, i) for i in range(1, 50)]:
            p = os.path.join(a.outdir, cand)
            if os.path.exists(p):
                found = p
        if found is None:
            missing.append(n)
            lines.append("%s MISSING" % n)
            continue
        body = open(found, encoding="utf-8", errors="replace").read()
        m = re.search(r"exit=(\d+)", body)
        code = int(m.group(1)) if m else -1
        ok = grade(n, code, body, expectations[n])
        matched += 1 if ok else 0
        if not ok:
            mism.append(n)
        lines.append("%s %s exit=%d" % (n, "MATCH" if ok else "MISMATCH", code))
    print("\n".join(lines))
    print("C1_CONTROLS states=%d matched=%d mismatches=%d missing=%d%s%s" % (
        len(lines), matched, len(mism), len(missing),
        (" [" + ",".join(mism) + "]") if mism else "",
        (" missing=" + ",".join(missing)) if missing else ""))
    with open(os.path.join(a.outdir, "C1-summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    sys.exit(0 if not mism and not missing else 1)


if __name__ == "__main__":
    main()
