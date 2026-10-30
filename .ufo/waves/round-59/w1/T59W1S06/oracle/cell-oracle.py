#!/usr/bin/env python3
"""Independent cell oracle: T59W1S06 probe for path 'tools/runner.py', class 'symlink'.

Implements the frozen round-59 contract exit/token semantics for ONE declared path
by reading Git objects only (never the worktree, so symlinks are not resolved):

  exit 0 + EXECUTOR_SOURCE_BOUND        candidate entry == trusted entry (regular blob)
  exit 1 + EXECUTOR_SOURCE_DRIFT        candidate entry missing, nonregular, or differs
  exit 2 + EXECUTOR_SOURCE_UNAVAILABLE  bad args, unresolvable trusted/candidate commit,
                                        or trusted source not a regular blob

Usage: oracle.py --repo REPO --trusted COMMIT --candidate COMMIT --path PATH
"""
import argparse
import subprocess
import sys

REGULAR_MODES = {"100644", "100755"}


def git(repo, *args):
    r = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True, timeout=30,
        env={"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
             "PATH": "/usr/bin:/bin"},
    )
    return r


def resolve(repo, rev):
    r = git(repo, "rev-parse", "--verify", f"{rev}^{{commit}}")
    if r.returncode:
        return None
    return r.stdout.strip()


def entry(repo, commit, path):
    """Return (mode, type, blob_hex) or None if the path is absent."""
    r = git(repo, "ls-tree", commit, "--", path)
    if r.returncode:
        return "error"
    line = r.stdout.strip()
    if not line:
        return None
    # ls-tree -r not used; a tree/gitlink entry occupies one line per path.
    meta, _, name = line.partition("\t")
    mode, typ, blob = meta.split()
    return (mode, typ, blob)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--trusted", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--path", action="append", required=True)
    a = p.parse_args()

    tc = resolve(a.repo, a.trusted)
    if not tc:
        print("EXECUTOR_SOURCE_UNAVAILABLE: trusted commit unresolvable")
        return 2
    cc = resolve(a.repo, a.candidate)
    if not cc:
        print("EXECUTOR_SOURCE_UNAVAILABLE: candidate commit unresolvable")
        return 2

    # Trusted source validity: every declared path must exist as a regular blob.
    for path in a.path:
        e = entry(a.repo, tc, path)
        if e is None or e == "error" or e[1] != "blob" or e[0] not in REGULAR_MODES:
            print(f"EXECUTOR_SOURCE_UNAVAILABLE: trusted source for {path!r} "
                  f"is not a regular executable-source blob")
            return 2

    # Candidate comparison.
    for path in a.path:
        e = entry(a.repo, cc, path)
        t = entry(a.repo, tc, path)
        if e is None:
            print(f"EXECUTOR_SOURCE_DRIFT: {path!r} missing at candidate")
            return 1
        if e == "error":
            print(f"EXECUTOR_SOURCE_UNAVAILABLE: candidate tree unreadable for {path!r}")
            return 2
        mode, typ, blob = e
        if typ != "blob" or mode not in REGULAR_MODES:
            print(f"EXECUTOR_SOURCE_DRIFT: {path!r} nonregular at candidate "
                  f"(mode={mode} type={typ})")
            return 1
        if blob != t[2]:
            print(f"EXECUTOR_SOURCE_DRIFT: {path!r} differs from trusted blob")
            return 1
    print("EXECUTOR_SOURCE_BOUND: all declared sources equal trusted blobs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
