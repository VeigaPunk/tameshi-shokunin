#!/usr/bin/env python3
"""Independent oracle for the single round-59 cell:
      path='tools/-runner.py', class='missing'
Verdict derived directly from Git object store (ls-tree / cat-file), with no
reference to the production tool (tools/executor-source-pin.py) implementation.

Contract mapping (frozen measure.py / contract.json):
  exit 0 + EXECUTOR_SOURCE_BOUND         trusted blob == candidate blob (regular file)
  exit 1 + EXECUTOR_SOURCE_DRIFT         declared source differs / missing / nonregular at candidate
  exit 2 + EXECUTOR_SOURCE_UNAVAILABLE   bad args, invalid trusted commit/source, unresolvable candidate
"""
import argparse
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args],
                          capture_output=True, text=True, timeout=30)


def resolve_commit(repo, rev):
    r = git(repo, 'rev-parse', '--verify', rev + '^{commit}')
    return r.stdout.strip() if r.returncode == 0 else None


def entry(repo, commit, path):
    """Return (mode, type, objectid) for path at commit, or None if no tree entry."""
    r = git(repo, 'ls-tree', commit, '--', path)
    if r.returncode != 0:
        return None
    lines = [l for l in r.stdout.splitlines() if l]
    if not lines:
        return None
    mode, typ, rest = lines[0].split(None, 2)
    return mode, typ, rest.split('\t')[0]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', required=True)
    a = p.parse_args()

    tc = resolve_commit(a.repo, a.trusted)
    if tc is None:
        print('EXECUTOR_SOURCE_UNAVAILABLE: trusted commit unresolvable')
        return 2
    t = entry(a.repo, tc, a.path)
    if t is None or t[1] != 'blob' or t[0] not in ('100644', '100755'):
        print('EXECUTOR_SOURCE_UNAVAILABLE: trusted source not a regular blob')
        return 2

    cc = resolve_commit(a.repo, a.candidate)
    if cc is None:
        print('EXECUTOR_SOURCE_UNAVAILABLE: candidate commit unresolvable')
        return 2
    c = entry(a.repo, cc, a.path)
    if c is None or c[1] != 'blob' or c[0] not in ('100644', '100755'):
        print('EXECUTOR_SOURCE_DRIFT: declared source missing or nonregular at candidate')
        return 1
    if c[2] != t[2]:
        print('EXECUTOR_SOURCE_DRIFT: declared source differs from trusted blob')
        return 1
    print('EXECUTOR_SOURCE_BOUND: declared source equals trusted blob')
    return 0


if __name__ == '__main__':
    sys.exit(main())
