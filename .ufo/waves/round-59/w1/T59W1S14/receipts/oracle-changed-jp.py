#!/usr/bin/env python3
"""Independent minimal oracle for round-59 C1 cell: path 'tools/日本語.py', class 'changed'.

Decision rule (contract.json exit_map), implemented directly against committed Git
objects only -- never the worktree:
  trusted must resolve to a regular blob, candidate to a commit, else UNAVAILABLE(2).
  declared source missing/nonregular at candidate, or content/mode differing -> DRIFT(1).
  identical blob (and regular-file mode) -> BOUND(0).
"""
import argparse
import subprocess
import sys

BOUND, DRIFT, UNAVAILABLE = 0, 1, 2


def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args],
                       capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def entry(repo, rev, path):
    """(mode, type, object_id) for path at rev, or None if unresolvable/absent."""
    rc, out, _ = git(repo, 'ls-tree', rev, '--', path)
    if rc != 0 or not out:
        return None
    meta = out.split('\t', 1)[0]
    mode, typ, oid = meta.split()
    return mode, typ, oid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--trusted', required=True)
    ap.add_argument('--candidate', required=True)
    ap.add_argument('--path', required=True)
    a = ap.parse_args()

    t = entry(a.repo, a.trusted, a.path)
    if t is None or t[1] != 'blob':
        print('EXECUTOR_SOURCE_UNAVAILABLE trusted-source-not-regular-blob')
        return UNAVAILABLE
    rc, _, _ = git(a.repo, 'rev-parse', '--verify', a.candidate + '^{commit}')
    if rc != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE candidate-unresolvable')
        return UNAVAILABLE
    c = entry(a.repo, a.candidate, a.path)
    if c is None:
        print('EXECUTOR_SOURCE_DRIFT declared-source-missing-at-candidate')
        return DRIFT
    if c[1] != 'blob':
        print(f'EXECUTOR_SOURCE_DRIFT declared-source-nonregular-at-candidate mode={c[0]} type={c[1]}')
        return DRIFT
    if c != t:
        print(f'EXECUTOR_SOURCE_DRIFT candidate-blob={c[2]} trusted-blob={t[2]}')
        return DRIFT
    print('EXECUTOR_SOURCE_BOUND')
    return BOUND


if __name__ == '__main__':
    sys.exit(main())
