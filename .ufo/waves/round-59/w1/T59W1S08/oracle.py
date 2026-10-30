#!/usr/bin/env python3
"""Independent oracle for ONE cell of round-59 contract:
path='tools/space name.py', class in {equal (control), changed}.

Implements the frozen contract's declared semantics using only argv-list git
invocations (no shell), mirroring measure.py's sanitized environment.
Contract: exit 0 + EXECUTOR_SOURCE_BOUND   (candidate blob == trusted blob)
          exit 1 + EXECUTOR_SOURCE_DRIFT    (declared source differs or is
                                             missing/nonregular at candidate)
          exit 2 + EXECUTOR_SOURCE_UNAVAILABLE (bad args / invalid trusted
                                             commit/source / unresolvable candidate)
"""
import argparse
import subprocess
import sys

BOUND = "EXECUTOR_SOURCE_BOUND"
DRIFT = "EXECUTOR_SOURCE_DRIFT"
UNAVAIL = "EXECUTOR_SOURCE_UNAVAILABLE"


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, timeout=30)
    return r


def resolve_commit(repo, rev):
    r = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    if r.returncode != 0:
        return None
    return r.stdout.strip()


def blob_at(repo, commit, path):
    """Return (mode, sha) for path at commit, or None if absent/unresolvable."""
    r = git(repo, "ls-tree", commit, "--", path)
    if r.returncode != 0:
        return None
    lines = [ln for ln in r.stdout.splitlines() if ln]
    if not lines:
        return None
    # exactly one tree entry expected for a single pathspec
    meta = lines[0].split()
    if len(meta) < 3:
        return None
    return meta[0], meta[2]  # mode, sha


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--trusted", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--path", required=True)
    a = p.parse_args()

    trusted = resolve_commit(a.repo, a.trusted)
    if trusted is None:
        print(f"{UNAVAIL}: trusted revision unresolvable", file=sys.stderr)
        return 2
    candidate = resolve_commit(a.repo, a.candidate)
    if candidate is None:
        print(f"{UNAVAIL}: candidate revision unresolvable", file=sys.stderr)
        return 2

    tblob = blob_at(a.repo, trusted, a.path)
    if tblob is None or tblob[0] != "100644":
        print(f"{UNAVAIL}: declared trusted source absent or nonregular", file=sys.stderr)
        return 2
    cblob = blob_at(a.repo, candidate, a.path)
    if cblob is None:
        print(f"{DRIFT}: declared source missing at candidate", file=sys.stderr)
        return 1
    if cblob[0] != "100644":
        print(f"{DRIFT}: declared source nonregular at candidate (mode {cblob[0]})", file=sys.stderr)
        return 1
    if cblob[1] != tblob[1]:
        print(f"{DRIFT}: declared source blob differs from trusted", file=sys.stderr)
        return 1
    print(f"{BOUND}: {a.path} matches trusted revision")
    return 0


if __name__ == "__main__":
    sys.exit(main())
