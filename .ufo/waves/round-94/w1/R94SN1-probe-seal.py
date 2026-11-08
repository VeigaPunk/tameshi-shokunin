#!/usr/bin/env python3
"""R94SN1 probe: git-seal bypass and revision-pinning of the C2 checker.

Builds scratch fixture repos under <scratch>/ and exercises the COMMITTED
instruments (.ufo/evidence/round-94/c1/measure-v94.py and
.ufo/evidence/round-94/conjunct-disposition-v94.py) against them.

Sections:
  F1  replace-ref substitution of the manifest the C2 checker grades
  F1  ambient GIT_DIR redirect of the C2 checker's git reads
  F2  receipts read from the working tree, not from --rev
  F3  a fully hand-written receipt set satisfies the C2 checker
  F6  make-pins94.py follows a symlink at pins.json
  F6  make-pins94.py --lane '' resolves to the CWD (the fleet root)
  F7  measure-v94.py --rev '' reads the git index

Nothing outside <scratch> is written.

Usage: python3 -I R94SN1-probe-seal.py <scratch-dir>
"""
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
C1 = LANE + "/.ufo/evidence/round-94/c1/measure-v94.py"
C2 = LANE + "/.ufo/evidence/round-94/conjunct-disposition-v94.py"
PINS = LANE + "/.ufo/evidence/round-94/c1/make-pins94.py"
MANIFEST = LANE + "/.ufo/evidence/round-94/conjunct-disposition.json"

KEYS = ["selfpin", "pins", "spec", "pin", "green", "canary", "valid0", "trivial0",
        "inconclusive0", "unstable0", "note", "verdict_tables", "ids", "mismatched0",
        "figure", "witnessed", "source", "coverage", "n_min"]


def sh(*a, cwd=None, env=None):
    return subprocess.run(list(a), cwd=cwd, capture_output=True, text=True, env=env)


def git(repo, *a):
    return sh("git", "-C", repo, *a)


def new_repo(path):
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)
    sh("git", "init", "-q", path)
    git(path, "config", "user.name", "ctl")
    git(path, "config", "user.email", "ctl@fixture.invalid")
    return path


def forged_manifest(dst):
    """Every conjunct declared falsifiable by one receipt -- the A4 cheat shape."""
    d = json.load(open(MANIFEST))
    for k in list(d["rows"]):
        d["rows"][k] = {"state": "pos-real", "mode": "conjunct-false"}
    open(dst, "w").write(json.dumps(d, indent=1))
    return dst


def build_fixture_lane(root, with_receipts=True):
    fx = new_repo(os.path.join(root, "lane"))
    os.makedirs(os.path.join(fx, ".ufo/evidence/round-94/c1"))
    os.makedirs(os.path.join(fx, ".ufo/evidence/round-94/pre-freeze/controls"))
    shutil.copy(C1, os.path.join(fx, ".ufo/evidence/round-94/c1/measure-v94.py"))
    shutil.copy(MANIFEST, os.path.join(fx, ".ufo/evidence/round-94/conjunct-disposition.json"))
    if with_receipts:
        man = json.load(open(MANIFEST))
        rd = os.path.join(fx, ".ufo/evidence/round-94/pre-freeze/controls")
        for k, row in man["rows"].items():
            st = row.get("state")
            if not st:
                continue
            if row.get("mode") == "setup-refusal":
                body = "exit=2\nC1_SETUP %s\nC1_R94_PASS=false\n" % row["token"]
            else:
                body = ("exit=1\nC1_CONJUNCTS "
                        + " ".join("%s=false" % x for x in KEYS) + "\n")
            open(os.path.join(rd, st + ".out"), "w").write(body)
        # the forged manifest (F1a/F1b) points EVERY row at pos-real, so that
        # receipt must exist for the forgery to reach a green findings=0.
        open(os.path.join(rd, "pos-real.out"), "w").write(
            "exit=1\nC1_CONJUNCTS "
            + " ".join("%s=false" % x for x in KEYS) + "\n")
    git(fx, "add", "-A")
    git(fx, "commit", "-q", "-m", "fixture")
    return fx


def c2(lane, rev, env=None, extra=()):
    return sh(sys.executable, "-I", C2, "--lane", lane, "--rev", rev,
              "--min-falsifiable", "17", *extra, env=env)


def main():
    root = os.path.abspath(sys.argv[1])
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    print("LANE:", LANE)
    print("C1 sha256:", sh("sha256sum", C1).stdout.split()[0])
    print("C2 sha256:", sh("sha256sum", C2).stdout.split()[0])
    print()

    print("== F1a: replace-ref substitutes the manifest the C2 checker grades ==")
    fx = build_fixture_lane(root)
    rev = git(fx, "rev-parse", "HEAD").stdout.strip()
    real = git(fx, "rev-parse", "HEAD:.ufo/evidence/round-94/conjunct-disposition.json").stdout.strip()
    forged_path = forged_manifest(os.path.join(root, "forged.json"))
    forged = git(fx, "hash-object", "-w", forged_path).stdout.strip()
    git(fx, "replace", real, forged)
    print("  --- checker, ambient env (no seal) ---")
    print("   ", c2(fx, rev).stdout.strip().splitlines()[-1])
    print("  --- checker, GIT_NO_REPLACE_OBJECTS=1 (the C1 seal) ---")
    e = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
    print("   ", c2(fx, rev, env=e).stdout.strip().splitlines()[-1])
    git(fx, "replace", "-d", real)
    print()

    print("== F1b: ambient GIT_DIR redirects the C2 checker's git reads ==")
    evil = new_repo(os.path.join(root, "evil"))
    os.makedirs(os.path.join(evil, ".ufo/evidence/round-94/c1"))
    shutil.copy(C1, os.path.join(evil, ".ufo/evidence/round-94/c1/measure-v94.py"))
    forged_manifest(os.path.join(evil, ".ufo/evidence/round-94/conjunct-disposition.json"))
    git(evil, "add", "-A")
    git(evil, "commit", "-q", "-m", "evil")
    erev = git(evil, "rev-parse", "HEAD").stdout.strip()
    fx2 = build_fixture_lane(os.path.join(root, "g2"))
    rev2 = git(fx2, "rev-parse", "HEAD").stdout.strip()
    env = dict(os.environ, GIT_DIR=evil + "/.git", GIT_WORK_TREE=evil)
    print("  --- checker with GIT_DIR=<attacker repo> ---")
    print("   ", c2(fx2, erev, env=env).stdout.strip().splitlines()[-1])
    print()

    print("== F2: receipts are read from the WORKING TREE, not from --rev ==")
    fx3 = build_fixture_lane(root)
    rev3 = git(fx3, "rev-parse", "HEAD").stdout.strip()
    print("  --- baseline ---")
    print("   ", c2(fx3, rev3).stdout.strip().splitlines()[-1])
    pm = os.path.join(fx3, ".ufo/evidence/round-94/pre-freeze/controls/pins-mutated.out")
    body = open(pm).read()
    open(pm, "w").write(body.replace("pins=false", "pins=true"))
    print("  --- after an UNCOMMITTED one-byte-class edit of one receipt ---")
    print("   ", c2(fx3, rev3).stdout.strip().splitlines()[-1])
    print("   ", [l for l in c2(fx3, rev3).stdout.splitlines()
                  if "no-flip" in l])
    open(pm, "w").write(body)
    print("  receipts committed at rev3:",
          len(git(fx3, "ls-tree", "-r", "--name-only", rev3,
                  ".ufo/evidence/round-94/pre-freeze/").stdout.split()))
    print("  -> the frozen rev has no receipts; the green verdict needs the live tree")
    print()

    print("== F3: a fully hand-written receipt set satisfies the C2 checker ==")
    fx4 = build_fixture_lane(root, with_receipts=False)
    man = json.load(open(MANIFEST))
    rd = os.path.join(fx4, ".ufo/evidence/round-94/pre-freeze/controls")
    for k, row in man["rows"].items():
        st = row.get("state")
        if not st:
            continue
        if row.get("mode") == "setup-refusal":
            b = "exit=2\nC1_SETUP %s\nC1_R94_PASS=false\n" % row["token"]
        else:
            b = ("exit=1\nC1_CONJUNCTS "
                 + " ".join("%s=false" % x for x in KEYS) + "\n")
        open(os.path.join(rd, st + ".out"), "w").write(b)
    open(os.path.join(rd, "pos-real.out"), "w").write(
        "exit=1\nC1_CONJUNCTS " + " ".join("%s=false" % x for x in KEYS) + "\n")
    git(fx4, "add", "-A")
    git(fx4, "commit", "-q", "-m", "hand-written receipts")
    rev4 = git(fx4, "rev-parse", "HEAD").stdout.strip()
    print("  receipts written by hand:", len(os.listdir(rd)),
          "(no clone, no counter run, no counter bytes)")
    print("  ", c2(fx4, rev4).stdout.strip().splitlines()[-1])
    print()

    print("== F6a: make-pins94.py follows a symlink at pins.json ==")
    fx5 = new_repo(os.path.join(root, "pins"))
    os.makedirs(os.path.join(fx5, ".ufo/evidence/round-94/c1"))
    shutil.copy(LANE + "/.ufo/evidence/round-94/c1/census-mutants.json",
                os.path.join(fx5, ".ufo/evidence/round-94/c1/"))
    shutil.copy(PINS, fx5)
    git(fx5, "add", "-A")
    git(fx5, "commit", "-q", "-m", "s")
    r5 = git(fx5, "rev-parse", "HEAD").stdout.strip()
    outside = os.path.join(root, "outside.txt")
    open(outside, "w").write("ORIGINAL-OUTSIDE-CONTENT\n")
    os.symlink(outside, os.path.join(fx5, ".ufo/evidence/round-94/c1/pins.json"))
    sh(sys.executable, "-I", os.path.join(fx5, "make-pins94.py"),
       "--lane", fx5, "--rev", r5)
    print("  outside file now contains:",
          open(outside).read().strip().splitlines()[0][:60])
    print("  -> the symlink was FOLLOWED and OVERWRITTEN")
    print()

    print("== F6b: make-pins94.py --lane '' resolves to the CWD ==")
    # The host guard pins the process cwd to the fleet root. This only computes
    # the path (cwd=FLEET); it does not write.
    FLEET = "/home/vgpnk/Projects/shokunin"
    r = sh(sys.executable, "-c",
           "import os;print(os.path.realpath(''));"
           "print(os.path.join(os.path.realpath(''),"
           "'.ufo/evidence/round-94/c1/pins.json'))", cwd=FLEET)
    lines = r.stdout.strip().splitlines()
    print("  os.path.realpath('') with cwd = fleet root:", lines[0])
    print("  -> write target would be:", lines[1])
    print("  fleet root is a git repo:",
          sh("git", "-C", FLEET, "rev-parse", "--is-inside-work-tree").stdout.strip())
    print("  (the write would land in the fleet root -- the 2026-11-06 incident shape)")
    print()

    print("== F2b: the REAL lane -- receipts are absent at the frozen rev ==")
    FROZEN = "7084358c732ebe1334c2eb9a352c3ed96b547f7c"
    at_frozen = git(LANE, "ls-tree", "-r", "--name-only", FROZEN,
                    ".ufo/evidence/round-94/pre-freeze/").stdout.split()
    at_head = git(LANE, "ls-tree", "-r", "--name-only", "HEAD",
                  ".ufo/evidence/round-94/pre-freeze/").stdout.split()
    print("  receipts at frozen rev %s: %d files" % (FROZEN[:8], len(at_frozen)))
    print("  receipts at HEAD          : %d files" % len(at_head))
    print("  -> the frozen predicate is not reproducible from the frozen rev;")
    print("     the green verdict is reachable only against the live working tree")
    print()

    print("== F7: measure-v94.py --rev '' reads the git INDEX ==")
    fx6 = os.path.join(root, "idx")
    shutil.rmtree(fx6, ignore_errors=True)
    sh("git", "clone", "-q", "--shared", "--no-checkout", LANE, fx6)
    git(fx6, "checkout", "-q", "--detach", "HEAD")
    np_ = os.path.join(fx6, "corpus/knowledge/mutation-case-fleet-sources-census.md")
    lines = []
    for line in open(np_).read().split("\n"):
        if line.startswith("| C0") or line.startswith("| C1"):
            lines.append(line.replace("KILLED", "SURVIVED").replace("SURVIVED", "KILLED"))
        else:
            lines.append(line)
    open(np_, "w").write("\n".join(lines))
    git(fx6, "add", "corpus/knowledge/mutation-case-fleet-sources-census.md")
    print("  index blob:", git(fx6, "rev-parse",
                               ":corpus/knowledge/mutation-case-fleet-sources-census.md").stdout.strip())
    print("  HEAD  blob:", git(fx6, "rev-parse",
                               "HEAD:corpus/knowledge/mutation-case-fleet-sources-census.md").stdout.strip())
    cnt = os.path.join(root, "cnt.py")
    open(cnt, "wb").write(sh("git", "-C", fx6, "cat-file", "blob",
                              "HEAD:.ufo/evidence/round-94/c1/measure-v94.py").stdout.encode())
    for revarg in ("", "HEAD"):
        w = os.path.join(root, "w" + (revarg or "empty"))
        shutil.rmtree(w, ignore_errors=True)
        os.makedirs(w)
        p = sh(sys.executable, "-I", cnt, "--repo", fx6, "--rev", revarg, "--work", w)
        summ = [l for l in p.stdout.splitlines()
                if l.startswith("C1_SUMMARY") or l.startswith("C1_R94_PASS")]
        print("  --rev %-5r ->" % revarg, " | ".join(summ))


if __name__ == "__main__":
    main()
