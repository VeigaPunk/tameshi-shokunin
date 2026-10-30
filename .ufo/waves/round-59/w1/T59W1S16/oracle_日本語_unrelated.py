#!/usr/bin/env python3
"""Independent oracle for round-59 cell: path='tools/日本語.py', class='unrelated'.

Reference implementation of the frozen contract's expected verdict for this ONE
cell, derived independently from measure.py semantics:

  --repo, --trusted, --candidate, --path
  exit 0 + EXECUTOR_SOURCE_BOUND        declared path is a regular file whose
                                        mode+content at candidate equal trusted
  exit 1 + EXECUTOR_SOURCE_DRIFT        declared path differs, is absent, or is
                                        non-regular (symlink/dir/gitlink)
  exit 2 + EXECUTOR_SOURCE_UNAVAILABLE  candidate or trusted does not resolve

Reads only git objects (rev-parse/ls-tree), never the worktree, and passes the
path as raw bytes so non-ASCII spellings are not normalized.
"""
import argparse
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        text=False,
        env={
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "PATH": "/usr/bin:/bin",
        },
    )


def resolve(repo, rev):
    r = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    if r.returncode != 0:
        return None
    return r.stdout.decode().strip()


def entry(repo, commit, path):
    """Return (mode, type, blobhex) for path at commit, or None if absent."""
    r = git(repo, "ls-tree", "-z", commit, "--", path)
    if r.returncode != 0:
        return None
    out = r.stdout
    if not out:
        return None
    # ls-tree -z record: "<mode> <type> <hash>\t<path>\0"
    rec = out.split(b"\0")[0]
    meta, _, _p = rec.partition(b"\t")
    try:
        mode, typ, h = meta.split(b" ", 2)
    except ValueError:
        return None
    return mode.decode(), typ.decode(), h.decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--trusted", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--path", required=True)
    a = ap.parse_args()

    trusted = resolve(a.repo, a.trusted)
    if trusted is None:
        print("EXECUTOR_SOURCE_UNAVAILABLE: trusted revision does not resolve")
        return 2
    candidate = resolve(a.repo, a.candidate)
    if candidate is None:
        print("EXECUTOR_SOURCE_UNAVAILABLE: candidate revision does not resolve")
        return 2

    t = entry(a.repo, trusted, a.path)
    c = entry(a.repo, candidate, a.path)
    # Regular executable-source blob: git type blob, mode 100644/100755 only.
    def regular(e):
        return e is not None and e[1] == "blob" and e[0] in ("100644", "100755")

    if not regular(c):
        print("EXECUTOR_SOURCE_DRIFT: declared source missing or nonregular at candidate")
        return 1
    if not regular(t):
        print("EXECUTOR_SOURCE_UNAVAILABLE: declared source not a regular blob at trusted")
        return 2
    if c != t:
        print("EXECUTOR_SOURCE_DRIFT: declared source differs from trusted")
        return 1
    print("EXECUTOR_SOURCE_BOUND: declared source blob equals trusted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
