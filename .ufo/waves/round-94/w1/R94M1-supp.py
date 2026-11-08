#!/usr/bin/env python3
"""R94M1 supplementary probes (post-matrix, not counted in killed:n/m).

S1  hidden-c001 + ONLY the table-count arm of D05 removed  -> does the flip
    belong to that arm alone?
S2  hidden-c001 + ONLY the id-set-equality arm removed      -> does that arm
    contribute anything observable on this state?
S3  sharp-source-wrongquote + the quote-occurrence rule removed (E22) -> is the
    occurrence half graded by the committed sharp state the round added for it?

Reuses R94M1-driver.py's module-level helpers (instrument extraction, controls
import, REV tree). Scratch-only clones, committed with identity ctl.
Usage: python3 -I R94M1-supp.py
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

W1 = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-94/w1"
SCRATCH = os.environ.get("R94M1_SCRATCH", "/fast/scratch/hyaku/tameshi-r94/R94M1/study")
_s = importlib.util.spec_from_file_location("drv", os.path.join(W1, "R94M1-driver.py"))
drv = importlib.util.module_from_spec(_s)
_s.loader.exec_module(drv)

TABLE_ONLY = {"old": "    vtables_ok = info[\"verdict_tables\"] == 1",
              "new": "    vtables_ok = True  # S1: table-count arm only"}
IDSET_ONLY = {"old": "    ids_ok = (note is not None and not bad and set(note_rows) == spec_ids)",
              "new": "    ids_ok = (note is not None and not bad)  # S2: id-set arm only"}
QUOTE_ONLY = {"old": "        quote_ok = any(norm_text(q) in text for q in quotes.get(sid, []))",
              "new": "        quote_ok = True  # S3: quote-occurrence rule removed"}
OUT_OF_SET = {"old": "            if first not in spec_ids:\n                bad.append(\"out-of-set:%d:%s\" % (ln + 1, first[:24]))\n                continue\n",
              "new": "            pass  # out-of-set arm only\n"}


PROBES = [("S1", "hidden-c001", [TABLE_ONLY]), ("S2", "hidden-c001", [IDSET_ONLY]),
          ("S3", "sharp-source-wrongquote", [QUOTE_ONLY]),
          ("S4", "hidden-c001", [TABLE_ONLY, IDSET_ONLY]),
          ("S5", "hidden-c001", [TABLE_ONLY, OUT_OF_SET]),
          ("S6", "hidden-c001", [IDSET_ONLY, OUT_OF_SET])]


def main():
    for sub in ("states", "supp", "work"):
        os.makedirs(os.path.join(SCRATCH, sub), exist_ok=True)
    ctl = drv.load_controls()
    pristine = drv.sealed_git_out(["-C", drv.LANE, "cat-file", "blob",
                                   drv.REV + ":" + drv.COUNTER_PATH])
    assert drv.sha_bytes(pristine) == drv.COUNTER_SHA
    pristine_path = os.path.join(SCRATCH, "pristine-counter.py")
    with open(pristine_path, "wb") as f:
        f.write(pristine)
    tree = drv.extract_revtree(os.path.join(SCRATCH, "revtree"))
    C = ctl.states(tree)
    built = {}
    for name in sorted({p[1] for p in PROBES}):
        dest = os.path.join(SCRATCH, "states", "supp-" + name)
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        repo = ctl.clone_at(drv.LANE, drv.REV, dest)
        ctl.materialize_state(repo, C[name])
        ctl.sh("git", "-C", repo, "add", "-A")
        ctl.sh("git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
               "commit", "-q", "--allow-empty", "-m", "r94m1 supp " + name)
        top = ctl.sh("git", "-C", repo, "rev-parse", "--show-toplevel").strip()
        assert os.path.realpath(top) == os.path.realpath(repo)
        built[name] = (repo, ctl.sh("git", "-C", repo, "rev-parse", "HEAD").strip())

    def run(counter, repo, rev):
        work = tempfile.mkdtemp(dir=os.path.join(SCRATCH, "work"), prefix="w-")
        try:
            p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev,
                                "--work", work], capture_output=True, text=True, timeout=1800,
                               stdin=subprocess.DEVNULL)
            return p.returncode, p.stdout + p.stderr
        finally:
            shutil.rmtree(work, ignore_errors=True)

    lines = []
    only = set(sys.argv[1:])
    for pid, state, edits in PROBES:
        if only and pid not in only:
            continue
        repo, rev = built[state]
        text = pristine.decode()
        for e in edits:
            assert text.count(e["old"]) == 1, (pid, e["old"][:40])
            text = text.replace(e["old"], e["new"], 1)
        mpath = os.path.join(SCRATCH, "supp", pid + ".py")
        with open(mpath, "w") as f:
            f.write(text)
        ctl.recompute_pin(mpath)
        msha = drv.sha_file(mpath)
        brc, bout = run(pristine_path, repo, rev)
        mrc, mout = run(mpath, repo, rev)
        with open(mpath, "wb") as f:
            f.write(pristine)
        rsha = drv.sha_file(mpath)
        rrc, rout = run(pristine_path, repo, rev)
        bconj, mconj = ctl.conj_of(bout), ctl.conj_of(mout)
        moved = {k: [bconj.get(k), mconj.get(k)] for k in sorted(bconj) if bconj.get(k) != mconj.get(k)}
        body = ("probe=%s state=%s edits=%s\nmutant_sha=%s restored_sha=%s pristine_sha=%s\n"
                "baseline_exit=%d mutant_exit=%d restored_exit=%d restored_identical=%s\n"
                "moved=%r\n--- baseline ---\n%s\n--- mutant ---\n%s\n--- restored ---\n%s\n") % (
                    pid, state, " + ".join(e["new"].strip() for e in edits), msha, rsha, drv.sha_bytes(pristine),
                    brc, mrc, rrc, drv.sha_bytes(rout.encode()) == drv.sha_bytes(bout.encode()),
                    moved, bout, mout, rout)
        with open(os.path.join(SCRATCH, "supp", pid + ".out"), "w") as f:
            f.write(body)
        lines.append("%s state=%s baseline_exit=%d mutant_exit=%d PASS=%s moved=%r" % (
            pid, state, brc, mrc, "C1_R94_PASS=true" in mout, moved))
        print(lines[-1])
    shutil.copytree(os.path.join(SCRATCH, "supp"), os.path.join(W1, "R94M1-supp-receipts"),
                    dirs_exist_ok=True)
    summary = os.path.join(W1, "R94M1-supp.out")
    keep = []
    if os.path.exists(summary) and only:
        keep = [l for l in open(summary) if l.split()[0] not in {p[0] for p in PROBES if p[0] in only}]
    with open(summary, "w") as f:
        f.write("".join(l if l.endswith("\n") else l + "\n" for l in keep + lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
