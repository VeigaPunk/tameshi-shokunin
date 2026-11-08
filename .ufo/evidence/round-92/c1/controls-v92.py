#!/usr/bin/env python3
"""Round-92 C1 control battery (QUALITY 145-149 class): committed scratch-clone
states read by the frozen counter .ufo/evidence/round-92/c1/measure-v92.py.

Every control clones the lane (--shared) at A_REV into a scratch dir, asserts
`git rev-parse --show-toplevel` equals that directory before any commit, writes
ONE change on top of the honest state, commits it under a fixture identity
inside the clone only, and runs the frozen counter (extracted from A_REV's
object store, never the working tree) with --rev HEAD there.

Receipts: <outdir>/<name>.out (stdout + stderr + exit). The summary printed at
the end is derived from those receipts, never hand-authored (QUALITY 147).

Mutant controls (D01/D02/D03) are counter copies with the self-pin line
recomputed for the edited bytes (a mutation study, documented in the plan);
the frozen bytes stay pinned and are never modified.

Usage: python3 -I controls-v92.py --lane LANE --rev A_REV --base BASE_REV \
         --work EMPTY_DIR --outdir DIR [--only NAME ...] [--jobs N]
Exit: 0 every control matches its pre-registered expectation; 1 otherwise.
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

COUNTER_PATH = ".ufo/evidence/round-92/c1/measure-v92.py"
SPEC = ".ufo/evidence/round-92/c1/census-mutants.json"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
READY_NOTE = "corpus/README.md"
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


def note_text(rows=None, measured="5/12", sid="S320", drop=None, extra="", header=None):
    rows = dict(DERIVED if rows is None else rows)
    out = ["source: %s fixture row (positive control only)" % sid, "", "# fixture note", "",
           "measured: %s killed" % measured, "",
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


def states(lane):
    """name -> dict(files, expect=(exit, {conjunct: bool} | {'__pass': True}))."""
    C = {}
    C["pos-real"] = dict(files={}, expect=(0, {"__pass": True}))
    C["pos-fixture"] = dict(files={NOTE: note_text()}, expect=(0, {"__pass": True}))
    C["nowork-note-absent"] = dict(files={}, drop_note=True,
                                   expect=(1, {"note": False, "ids": False}))
    hidden3 = "\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n" + "".join(
        "| C%03d | fixture arm | fixture edit | %s | differs |\n"
        % (i, "SURVIVED" if DERIVED["C%02d" % i] == "KILLED" else "KILLED")
        for i in range(1, 13))
    hiddenx = "\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n" + "".join(
        "| X%d | fixture arm | fixture edit | KILLED | differs |\n" % i for i in range(1, 13))
    C["out-of-set"] = dict(files={NOTE: note_text(extra=hidden3)}, expect=(1, {"ids": False}))
    C["out-of-set-letters"] = dict(files={NOTE: note_text(extra=hiddenx)},
                                   expect=(1, {"ids": False}))
    C["unkeyed-row"] = dict(files={NOTE: note_text(extra=(
        "\n| note row | arm | edit | verdict | witness |\n|---|---|---|---|---|\n"
        "| appended | fixture arm | fixture edit | KILLED | differs |\n"))},
        expect=(1, {"ids": False}))
    C["dup-row"] = dict(files={NOTE: note_text(extra="| C02 | fixture arm | KILLED | differs |\n")},
                        expect=(1, {"ids": False}))
    C["position"] = dict(files={NOTE: note_text(
        drop="C12", header="| id | arm | witness | verdict |", extra="| C12 | fixture arm | KILLED | MAYBE |\n")},
        expect=(1, {"ids": False}))
    C["inverted"] = dict(files={NOTE: note_text(
        rows={k: ("SURVIVED" if v == "KILLED" else "KILLED") for k, v in DERIVED.items()})},
        expect=(1, {"mismatched0": False}))
    C["figure"] = dict(files={NOTE: note_text(measured="6/12")}, expect=(1, {"figure": False}))
    C["source"] = dict(files={}, source_status="queued", expect=(1, {"source": False}))
    C["coverage"] = dict(files={}, drop_readme_row=True, expect=(1, {"coverage": False}))
    C["spec-mutated"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C03").update(
        new="teaches !~ /supersedes S[0-9]{5}/"))}, expect=(1, {"spec": False}))
    C["noop-mutant"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C02").update(
        new=mut(s, "C02")["old"]))}, expect=(1, {"invalid0": False}))
    C["syntax-mutant"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C11").update(
        new='[ "$missing_error" = 1 ] && exit 2 ('))}, expect=(1, {"invalid0": False}))
    C["trivial-mutant"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C10").update(
        new='function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ '
    ))}, expect=(1, {"trivial0": False}))
    C["witness-same"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C02")["witness"].update(
        sources=mut(s, "C02")["witness"]["sources"].replace("| 1234567 |", "| no |")))},
        expect=(1, {"witnessed": False}))
    C["pin-mismatch"] = dict(files={SPEC: spec_edit(lane, lambda s: s["gate"].update(
        sha256="0" * 64))}, expect=(1, {"pin": False}))
    return C


def mutant_edits(counter_text):
    base = counter_text
    lane_block = """    for r, label in ((repo, "lane"),):
        p = git(r, "replace", "-l", check=False)
        if p.returncode != 0:
            die("replace-list-failed:" + label)
        if p.stdout.strip():
            die("replace-refs-present:" + label)
"""
    assert lane_block in base, "D01 anchor missing"
    no_gate = "    pass  # D01: replace-list gate removed\n"
    env_frag = '"GIT_NO_REPLACE_OBJECTS": "1", '
    assert env_frag in base, "D02 anchor missing"
    d01 = base.replace(lane_block, no_gate, 1)
    d02 = base.replace(env_frag, "", 1)
    d01d02 = d01.replace(env_frag, "", 1)
    pin_assert = """    if not self_pin_ok():
        die("self-pin-mismatch")
"""
    assert pin_assert in base, "D03 pin anchor missing"
    shape = 'ID_SHAPE = re.compile(r"^[A-Za-z]{1,4}[_-]?[0-9]{1,4}$")'
    assert shape in base
    unkeyed = """        if not toks and not shaped:
            continue
        if not shaped:
            bad.append("unkeyed:" + first[:40])
            continue
"""
    assert unkeyed in base, "D03 unkeyed anchor missing"
    d03 = (base.replace(pin_assert, "", 1)
               .replace(shape, 'ID_SHAPE = re.compile(r"^C[0-9]{2}$")', 1)
               .replace(unkeyed, "        if not shaped:\n            continue\n", 1))
    return {
        "D01": (d01, "replace-honest"),
        "D01D02": (d01d02, "replace-false-committed"),
        "D03": (d03, "out-of-set"),
    }


def materialize_state(repo, spec):
    for p, text in spec.get("files", {}).items():
        fp = os.path.join(repo, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(text)
    if spec.get("drop_note"):
        npath = os.path.join(repo, NOTE)
        if os.path.exists(npath):
            os.unlink(npath)
    if spec.get("drop_readme_row"):
        rp = os.path.join(repo, READY_NOTE)
        lines = open(rp, encoding="utf-8").read().split("\n")
        kept = [l for l in lines if "knowledge/mutation-case-fleet-sources-census.md" not in l]
        open(rp, "w", encoding="utf-8").write("\n".join(kept))
    if spec.get("source_status"):
        sp = os.path.join(repo, "corpus/SOURCES.md")
        txt = open(sp, encoding="utf-8").read()
        out = []
        for line in txt.split("\n"):
            c = [x.strip() for x in re.sub(r"^ {0,3}", "", line).split("|")]
            if len(c) >= 13 and c[1] == "S320":
                line = line.replace("| mined |", "| %s |" % spec["source_status"], 1)
            out.append(line)
        open(sp, "w", encoding="utf-8").write("\n".join(out))


def clone_at(lane, rev, dest):
    sh("git", "clone", "-q", "--shared", "--no-checkout", lane, dest)
    top = sh("git", "-C", dest, "rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(dest):
        raise SystemExit("toplevel mismatch for " + dest)
    sh("git", "-C", dest, "checkout", "-q", "--detach", rev)
    return dest


def run_ctl(name, spec, lane, a_rev, counter, scratch, outdir):
    d = tempfile.mkdtemp(dir=scratch, prefix="ctl-" + name + "-")
    try:
        repo = clone_at(lane, a_rev, os.path.join(d, "repo"))
        materialize_state(repo, spec)
        sh("git", "-C", repo, "add", "-A")
        sh("git", "-C", repo, "-c", "user.name=r92-fixture", "-c", "user.email=r92-fixture@invalid",
           "commit", "-q", "--allow-empty", "-m", "r92 control " + name)
        rev = sh("git", "-C", repo, "rev-parse", "HEAD").strip()
        work = os.path.join(d, "work")
        os.makedirs(work)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev,
                            "--work", work], capture_output=True, text=True)
        open(os.path.join(outdir, name + ".out"), "w").write(
            "control=%s clone_rev=%s parent=%s\nexit=%d\n" % (name, rev, a_rev, p.returncode)
            + p.stdout + p.stderr)
        return name, p.returncode, p.stdout
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--mutants-only", action="store_true")
    ap.add_argument("--states-only", action="store_true")
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    os.makedirs(a.outdir, exist_ok=True)
    work = os.path.realpath(a.work)
    if os.path.isdir(work) and os.listdir(work):
        raise SystemExit("work-not-empty")
    os.makedirs(work, exist_ok=True)
    counter = os.path.join(work, "counter.py")
    blob = subprocess.run(["git", "-C", lane, "cat-file", "blob",
                           a.rev + ":" + COUNTER_PATH], capture_output=True)
    if blob.returncode != 0:
        raise SystemExit("counter absent at rev")
    open(counter, "wb").write(blob.stdout)
    print("CONTROL_INSTRUMENT sha256=" + hashlib.sha256(blob.stdout).hexdigest())
    C = states(lane)
    sel = a.only if a.only else list(C)
    results = {}
    expectations = {n: C[n]["expect"] for n in C}
    expectations.update({
        "nowork-base": (2, {"__setup": "spec-absent-at-rev"}),
        "replace-honest": (2, {"__setup": "replace-refs-present"}),
        "replace-false-sealed": (2, {"__setup": "replace-refs-present"}),
        "D01": (0, {"__pass": True}),
        "D01D02": (0, {"__pass": True}),
        "D03": (0, {"__pass": True}),
    })

    if not a.mutants_only:
        run_sel = [n for n in sel if n in C]
        with ThreadPoolExecutor(max_workers=min(a.jobs, max(1, len(run_sel)))) as ex:
            futs = [ex.submit(run_ctl, n, C[n], lane, a.rev, counter, work, a.outdir) for n in run_sel]
            for f in futs:
                n, code, out = f.result()
                results[n] = (code, out)
        if "nowork-base" in sel:
            w2 = os.path.join(work, "base-work")
            os.makedirs(w2, exist_ok=True)
            p = subprocess.run([sys.executable, "-I", counter, "--repo", lane, "--rev", a.base,
                                "--work", w2], capture_output=True, text=True)
            open(os.path.join(a.outdir, "nowork-base.out"), "w").write(
                "control=nowork-base rev=%s\nexit=%d\n" % (a.base, p.returncode) + p.stdout + p.stderr)
            results["nowork-base"] = (p.returncode, p.stdout)

    if not a.states_only:
        mts = mutant_edits(blob.stdout.decode())
        false_note = note_text(rows={k: ("SURVIVED" if v == "KILLED" else "KILLED")
                                     for k, v in DERIVED.items()})
        # state 1: honest note committed, replace ref maps the honest blob to the false note
        st1 = clone_at(lane, a.rev, os.path.join(work, "st-replace-honest"))
        false_oid = subprocess.run(["git", "-C", st1, "hash-object", "-w", "--stdin"],
                                   input=false_note, capture_output=True, text=True).stdout.strip()
        true_oid = sh("git", "-C", st1, "rev-parse", "HEAD:" + NOTE).strip()
        subprocess.run(["git", "-C", st1, "replace", true_oid, false_oid], check=True)
        # state 2: false note committed, replace ref maps the false blob to the honest note
        st2 = clone_at(lane, a.rev, os.path.join(work, "st-replace-false"))
        open(os.path.join(st2, NOTE), "w", encoding="utf-8").write(false_note)
        sh("git", "-C", st2, "add", "-A")
        sh("git", "-C", st2, "-c", "user.name=r92-fixture", "-c", "user.email=r92-fixture@invalid",
           "commit", "-q", "-m", "false note")
        false_blob = sh("git", "-C", st2, "rev-parse", "HEAD:" + NOTE).strip()
        true_blob = subprocess.run(["git", "-C", st2, "hash-object", "-w", "--stdin"],
                                   input=note_text(), capture_output=True, text=True).stdout.strip()
        subprocess.run(["git", "-C", st2, "replace", false_blob, true_blob], check=True)
        for n in sel:
            if n not in mts:
                continue
            text, state_name = mts[n]
            mp = os.path.join(work, "counter-" + n + ".py")
            open(mp, "w").write(text)
            recompute_pin(mp)
            repo = st1 if state_name == "replace-honest" else st2
            mw = os.path.join(work, "mwork-" + n)
            os.makedirs(mw, exist_ok=True)
            p = subprocess.run([sys.executable, "-I", mp, "--repo", repo, "--rev", "HEAD",
                                "--work", mw], capture_output=True, text=True)
            open(os.path.join(a.outdir, n + "-" + state_name + ".out"), "w").write(
                "mutant=%s state=%s\ncounter_sha=%s\nexit=%d\n" % (
                    n, state_name, hashlib.sha256(open(mp, "rb").read()).hexdigest(), p.returncode)
                + p.stdout + p.stderr)
            results[n] = (p.returncode, p.stdout)
        for nm, repo in (("replace-honest", st1), ("replace-false-sealed", st2)):
            w = os.path.join(work, "w-" + nm)
            os.makedirs(w, exist_ok=True)
            p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", "HEAD",
                                "--work", w], capture_output=True, text=True)
            open(os.path.join(a.outdir, nm + ".out"), "w").write(
                "control=%s exit=%d\n" % (nm, p.returncode) + p.stdout + p.stderr)
            results[nm] = (p.returncode, p.stdout)
        shutil.rmtree(st1, ignore_errors=True)
        shutil.rmtree(st2, ignore_errors=True)

    lines = []
    matched = 0
    mism = []
    for n in sorted(results):
        code, out = results[n]
        want = expectations.get(n)
        ok = want is not None and code == want[0]
        if ok and "__pass" in want[1]:
            ok = "C1_R92_PASS=true" in out
        if ok and "__setup" in want[1]:
            ok = ("C1_SETUP " + want[1]["__setup"]) in out
        if ok and "__pass" not in want[1] and "__setup" not in want[1]:
            conj = {}
            for line in out.split("\n"):
                if line.startswith("C1_CONJUNCTS "):
                    for kv in line.split()[1:]:
                        k, v = kv.split("=")
                        conj[k] = (v == "true")
            for k, v in want[1].items():
                if conj.get(k) != v:
                    ok = False
        if ok:
            matched += 1
        else:
            mism.append(n)
        lines.append("%s %s exit=%d" % (n, "MATCH" if ok else "MISMATCH", code))
    print("\n".join(lines))
    print("C1_CONTROLS states=%d matched=%d mismatches=%d%s" % (
        len(results), matched, len(mism), (" [" + ",".join(mism) + "]") if mism else ""))
    open(os.path.join(a.outdir, "C1-summary.txt"), "w").write("\n".join(lines) + "\n")
    sys.exit(0 if not mism else 1)


if __name__ == "__main__":
    main()
