#!/usr/bin/env python3
"""R94SC1 fixture: does the drafted case-note status block break the certificate?

Read-only on the lane. The block is appended to a SCRATCH CLONE of the lane
(the clone lives under the seat's scratch dir), the clone commits the edit
under the fixture identity `ctl <ctl@fixture.invalid>`, and the FROZEN counter
blob (extracted with `git cat-file` from the named revision) is run against the
clone's new commit. Nothing in the lane is written and no mutating git command
runs there.

The counter's predicates that the block can move:
  * `verdict_tables` — a second table whose HEADER ROW carries a `verdict` cell
    would be keyed and refuse the note (QUALITY 154/155).
  * `ids` / `mismatched0` — a stray KILLED/SURVIVED token outside the verdict
    table is a badrow (the one-rule stray-verdict scan).
  * `figure` — the block-level `measured: N/M killed` figure must appear exactly
    once.
  * `coverage` — graded on corpus/README.md, which the block does not touch.

Usage: R94SC1-note-block-fixture.py <block-file> [rev]
"""
import os
import re
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
SCRATCH = "/fast/scratch/hyaku/tameshi-r94/R94SC1"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
COUNTER = ".ufo/evidence/round-94/c1/measure-v94.py"

BLOCK = sys.argv[1]
REV = sys.argv[2] if len(sys.argv) > 2 else "6b19eb92cd9f37f79eb6632e356ad216e37cbb35"
BASE_REV = sys.argv[3] if len(sys.argv) > 3 else "a8f0e14bd400002324793d82030431696435d9a7"


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)


def main():
    block = open(BLOCK, encoding="utf-8").read()
    fx = os.path.join(SCRATCH, "fx-note")
    if os.path.exists(fx):
        subprocess.run(["rm", "-rf", fx])
    r = sh(["git", "clone", "--shared", "-q", LANE, fx])
    if r.returncode != 0:
        print("CLONE_FAILED", r.stderr)
        return 1
    # assert the clone is its own toplevel before any commit
    top = sh(["git", "-C", fx, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert top == fx, "fixture is not its own toplevel: %s" % top
    sh(["git", "-C", fx, "config", "user.name", "ctl"])
    sh(["git", "-C", fx, "config", "user.email", "ctl@fixture.invalid"])
    r = sh(["git", "-C", fx, "checkout", "-q", REV])
    if r.returncode != 0:
        print("CHECKOUT_FAILED", r.stderr)
        return 1

    # extract the FROZEN counter blob (never the working tree)
    counter_blob = sh(["git", "-C", fx, "cat-file", "blob", "%s:%s" % (REV, COUNTER)]).stdout
    cpath = os.path.join(SCRATCH, "counter-fixture.py")
    open(cpath, "w", encoding="utf-8").write(counter_blob)

    # CONTROL: the unmodified note at this rev
    work_c = os.path.join(SCRATCH, "work-control")
    subprocess.run(["rm", "-rf", work_c])
    os.makedirs(work_c)
    p = sh([sys.executable, "-I", cpath, "--repo", fx, "--rev", "HEAD", "--work", work_c])
    control = p.stdout
    print("== CONTROL (note unmodified at %s) ==" % REV[:8])
    for line in control.split("\n"):
        if line.startswith(("C1_SUMMARY", "C1_CONJUNCTS", "C1_R94_PASS", "C1_BADROWS")):
            print("  " + line)
    print("  exit=%d" % p.returncode)

    # apply the drafted block to the note in the CLONE
    # mode "append"   -> the block is appended after the existing text
    # mode "replace"  -> the block REPLACES the existing round-94 status section
    #                    (from its "## Certification attempt (appended round 94)" heading
    #                    to the end of the file)
    mode = sys.argv[4] if len(sys.argv) > 4 else "append"
    note_path = os.path.join(fx, NOTE)
    note = open(note_path, encoding="utf-8").read()
    if mode == "replace":
        marker = "## Certification attempt (appended round 94)"
        i = note.index(marker)
        note = note[:i].rstrip("\n") + "\n\n" + block.rstrip("\n") + "\n"
    else:
        note = note.rstrip("\n") + "\n\n" + block
    with open(note_path, "w", encoding="utf-8") as fh:
        fh.write(note)
    a = sh(["git", "-C", fx, "add", NOTE])
    st = sh(["git", "-C", fx, "status", "--porcelain"])
    dc = sh(["git", "-C", fx, "diff", "--cached", "--stat"])
    print("FIXTURE_ADD rc=%d stdout=%s stderr=%s" % (a.returncode, a.stdout.strip()[:200], a.stderr.strip()[:200]))
    print("FIXTURE_STATUS %s" % st.stdout.strip()[:200])
    print("FIXTURE_DIFF_CACHED %s" % dc.stdout.strip()[:200])
    c = sh(["git", "-C", fx, "commit", "-q", "-m", "fixture: apply drafted status block"])
    if c.returncode != 0:
        print("FIXTURE_COMMIT_FAILED rc=%d stdout=%s stderr=%s" % (c.returncode, c.stdout.strip()[:400], c.stderr.strip()[:400]))
        return 1
    new_rev = sh(["git", "-C", fx, "rev-parse", "HEAD"]).stdout.strip()
    base_rev = sh(["git", "-C", fx, "rev-parse", "HEAD~1"]).stdout.strip()
    print("FIXTURE_COMMIT %s (parent %s)" % (new_rev[:8], base_rev[:8]))
    if new_rev == base_rev:
        print("FIXTURE_COMMIT_NOOP")
        return 1
    # the block must actually be in the committed note
    committed = sh(["git", "-C", fx, "show", "HEAD:" + NOTE]).stdout
    if block.strip()[:200] not in committed:
        print("FIXTURE_BLOCK_NOT_IN_COMMIT")
        return 1
    print("FIXTURE_BLOCK_PRESENT_IN_COMMIT true")

    # run the frozen counter against the fixture commit
    work_t = os.path.join(SCRATCH, "work-blocked")
    subprocess.run(["rm", "-rf", work_t])
    os.makedirs(work_t)
    p = sh([sys.executable, "-I", cpath, "--repo", fx, "--rev", new_rev, "--work", work_t])
    print("== WITH DRAFTED BLOCK (fixture commit %s) ==" % new_rev[:8])
    for line in p.stdout.split("\n"):
        if line.startswith(("C1_SUMMARY", "C1_CONJUNCTS", "C1_R94_PASS", "C1_BADROWS")):
            print("  " + line)
    print("  exit=%d" % p.returncode)

    # verdict: the block must not move any conjunct
    def conj(text):
        for line in text.split("\n"):
            if line.startswith("C1_CONJUNCTS "):
                return dict(kv.split("=", 1) for kv in line.split()[1:])
        return {}

    c, t = conj(control), conj(p.stdout)
    moved = [k for k in c if c[k] != t.get(k)]
    print("CONJUNCTS_MOVED %s" % (",".join(moved) if moved else "none"))
    ok = (p.returncode == 0 and not moved and "C1_R94_PASS=true" in p.stdout)
    print("BLOCK_PRESERVES_CERTIFICATE %s" % ("true" if ok else "false"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
