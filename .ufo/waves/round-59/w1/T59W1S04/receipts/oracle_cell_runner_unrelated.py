#!/usr/bin/env python3
"""Minimal independent oracle for round-59 cell path=tools/runner.py, class=unrelated.

Decides the contract-mandated outcome from first principles using only git
plumbing, for ANY class on this single path. Contract (frozen):
  exit 0 + EXECUTOR_SOURCE_BOUND        all declared regular executable-source blobs equal trusted
  exit 1 + EXECUTOR_SOURCE_DRIFT        declared source differs or is missing/nonregular at candidate
  exit 2 + EXECUTOR_SOURCE_UNAVAILABLE  bad args / invalid trusted commit/source / unresolvable candidate

Usage: oracle.py --repo REPO --trusted COMMIT --candidate COMMIT --path PATH
Only checks the DECLARED path (trust boundary: declared Git blobs only).
"""
import argparse
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True,
        env={"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
             "PATH": "/usr/bin:/bin"},
    )


def resolve_commit(repo, rev):
    r = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    if r.returncode != 0:
        return None
    return r.stdout.strip()


def tree_entry(repo, commit, path):
    """Return (mode, type, blobhash) or None if path absent / not a single blob."""
    r = git(repo, "ls-tree", commit, "--", path)
    if r.returncode != 0:
        return "error"
    lines = [ln for ln in r.stdout.splitlines() if ln]
    if not lines:
        return None
    if len(lines) != 1:
        return "error"
    meta, _tab, _name = lines[0].partition("\t")
    mode, typ, blob = meta.split()
    return (mode, typ, blob)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--trusted", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--path", required=True)
    a = p.parse_args()

    trusted = resolve_commit(a.repo, a.trusted)
    if trusted is None:
        print("EXECUTOR_SOURCE_UNAVAILABLE: trusted not a commit")
        return 2
    candidate = resolve_commit(a.repo, a.candidate)
    if candidate is None:
        print("EXECUTOR_SOURCE_UNAVAILABLE: candidate unresolvable")
        return 2

    te_t = tree_entry(a.repo, trusted, a.path)
    if te_t in (None, "error"):
        print("EXECUTOR_SOURCE_UNAVAILABLE: declared source missing/nonregular at trusted")
        return 2
    mode_t, typ_t, blob_t = te_t
    if typ_t != "blob" or mode_t not in ("100644", "100755"):
        print("EXECUTOR_SOURCE_UNAVAILABLE: declared source not a regular file at trusted")
        return 2

    te_c = tree_entry(a.repo, candidate, a.path)
    if te_c in (None, "error"):
        print("EXECUTOR_SOURCE_DRIFT: declared source missing at candidate")
        return 1
    mode_c, typ_c, blob_c = te_c
    if typ_c != "blob" or mode_c not in ("100644", "100755"):
        print("EXECUTOR_SOURCE_DRIFT: declared source missing/nonregular at candidate")
        return 1
    if blob_c != blob_t:
        print("EXECUTOR_SOURCE_DRIFT: declared source content differs")
        return 1
    print("EXECUTOR_SOURCE_BOUND: declared source blob equals trusted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
