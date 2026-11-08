#!/usr/bin/env python3
"""R93SC1 probe: the drafted round-93 status block does not break the reader.

Takes the committed note at the instrument revision, appends the drafted status
block (read from R93SC1-note-status-block.md between the BEGIN/END INTEGRATION
TEXT markers), commits it in a scratch clone, and runs the FROZEN counter blob
from that revision against the clone.

Read-only on the lane: the clone lives under the scratch dir, the lane is only
read with `git cat-file` / `git clone --shared`.

Usage: R93SC1-note-block-fixture.py <scratch-dir> <draft-md>
Exit: 0 when the counter prints C1_R93_PASS=true with verdict_tables=1 and
      badrows=0; 1 otherwise.
"""
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "855f0c1c59ee2af7f184d8de62d02cdd576eb94e"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
COUNTER = ".ufo/evidence/round-93/c1/measure-v93.py"


def sh(*a, cwd=None, check=True):
    p = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(a), p.stderr))
    return p.stdout


def extract_block(path):
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"--- BEGIN INTEGRATION TEXT ---\n(.*?)\n--- END INTEGRATION TEXT ---",
                  txt, re.S)
    if not m:
        raise SystemExit("no integration block in " + path)
    return m.group(1) + "\n"


def main():
    scratch = sys.argv[1]
    draft = sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else "replace"
    block = extract_block(draft)

    os.makedirs(scratch, exist_ok=True)
    repo = os.path.join(scratch, "repo")
    if not os.path.isdir(repo):
        sh("git", "clone", "-q", "--shared", "--no-checkout", LANE, repo)
        top = sh("git", "-C", repo, "rev-parse", "--show-toplevel").strip()
        if os.path.realpath(top) != os.path.realpath(repo):
            raise SystemExit("toplevel mismatch for " + repo)
        sh("git", "-C", repo, "checkout", "-q", "--detach", REV)
    note = os.path.join(repo, NOTE)
    original = open(note, encoding="utf-8").read()
    if mode == "append":
        new = original.rstrip("\n") + "\n\n" + block
    elif "## Certification attempt (appended round 93)" in original:
        # replace the existing round-93 section with the drafted one
        head, _, _ = original.partition("## Certification attempt (appended round 93)")
        new = head + block
    else:
        new = original + "\n" + block
    open(note, "w", encoding="utf-8").write(new)
    sh("git", "-C", repo, "add", "-A")
    sh("git", "-C", repo, "-c", "user.name=r93-fixture",
       "-c", "user.email=r93-fixture@invalid", "commit", "-q", "--allow-empty",
       "-m", "r93 R93SC1 note-block fixture")
    crev = sh("git", "-C", repo, "rev-parse", "HEAD").strip()

    blob = subprocess.run(["git", "-C", LANE, "cat-file", "blob", "%s:%s" % (REV, COUNTER)],
                          capture_output=True).stdout
    cp = os.path.join(scratch, "counter.py")
    open(cp, "wb").write(blob)
    work = os.path.join(scratch, "work")
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-I", cp, "--repo", repo, "--rev", crev,
                        "--work", work], capture_output=True, text=True)
    print("clone_rev=%s exit=%d" % (crev, p.returncode))
    print(p.stdout)
    if p.stderr:
        print("STDERR " + p.stderr)
    ok = (p.returncode == 0 and "C1_R93_PASS=true" in p.stdout
          and "verdict_tables=1" in p.stdout and "badrows=0" in p.stdout
          and "mismatched=0" in p.stdout)
    print("NOTE_BLOCK_FIXTURE " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
