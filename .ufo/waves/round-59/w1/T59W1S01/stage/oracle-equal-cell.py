#!/usr/bin/env python3
"""Independent oracle for round-59 cell (path='tools/runner.py', class='equal').

Checks only the equal-cell contract:
  trusted and candidate commits resolve in --repo;
  tools/runner.py is a regular blob at both;
  equal blobs -> exit 0 + EXECUTOR_SOURCE_BOUND;
  drift/missing/nonregular -> exit 1 + EXECUTOR_SOURCE_DRIFT;
  unresolvable commit/path-arg problems -> exit 2 + EXECUTOR_SOURCE_UNAVAILABLE.
"""
import argparse
import subprocess
import sys

PATH = 'tools/runner.py'


def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args],
                       capture_output=True, text=True)
    return r


def blob_info(repo, rev):
    """Return (mode, type, blobhash) for PATH at rev, or None if absent."""
    r = git(repo, 'ls-tree', rev, '--', PATH)
    if r.returncode:
        return None
    out = r.stdout.strip()
    if not out:
        return None
    mode, typ, blobhash, _path = out.split(None, 3)
    return mode, typ, blobhash


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    a = p.parse_args()

    if a.path != [PATH]:
        print(f'EXECUTOR_SOURCE_UNAVAILABLE: oracle scoped to {PATH}, got {a.path}')
        return 2

    for rev in (a.trusted, a.candidate):
        if git(a.repo, 'rev-parse', '--verify', rev + '^{commit}').returncode:
            print(f'EXECUTOR_SOURCE_UNAVAILABLE: unresolvable commit {rev}')
            return 2

    t = blob_info(a.repo, a.trusted)
    c = blob_info(a.repo, a.candidate)
    for rev, info in ((a.trusted, t), (a.candidate, c)):
        if info is None:
            print(f'EXECUTOR_SOURCE_DRIFT: {PATH} missing at {rev}')
            return 1
        if info[1] != 'blob':
            print(f'EXECUTOR_SOURCE_DRIFT: {PATH} nonregular ({info[1]}) at {rev}')
            return 1

    if t[2] == c[2]:
        print('EXECUTOR_SOURCE_BOUND '
              f'{PATH} blob {t[2]} equal at trusted and candidate')
        return 0
    print(f'EXECUTOR_SOURCE_DRIFT: {PATH} blob {t[2]} != {c[2]}')
    return 1


if __name__ == '__main__':
    sys.exit(main())
