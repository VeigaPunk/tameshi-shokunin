#!/usr/bin/env python3
"""Independent oracle for the single cell: path='tools/-runner.py', frozen round59.

Contract under test (from .ufo/evidence/round-59/contract.json):
  exit 0 + EXECUTOR_SOURCE_BOUND      : declared blob at candidate equals trusted blob
  exit 1 + EXECUTOR_SOURCE_DRIFT      : differs, or missing/nonregular at candidate
  exit 2 + EXECUTOR_SOURCE_UNAVAILABLE: bad args / invalid trusted / unresolvable candidate

This oracle deliberately uses only Git plumbing (rev-parse, ls-tree, cat-file)
and string blob-identity comparison, independent of any production tool logic.
Usage: oracle.py --repo REPO --trusted COMMIT --candidate COMMIT --path PATH
"""
import argparse
import subprocess
import sys

def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args],
                       capture_output=True, text=True, timeout=30)
    return r

def blob_at(repo, rev, path):
    """Return (mode, type, blob) tuple for path at rev, or None if absent."""
    r = git(repo, 'ls-tree', rev, '--', path)
    if r.returncode != 0:
        return None
    lines = [l for l in r.stdout.splitlines() if l]
    if not lines:
        return None
    mode, typ, blob, _ = lines[0].split(None, 3)
    return (mode, typ, blob)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', required=True)
    a = p.parse_args()

    # Resolve trusted commit; invalid => UNAVAILABLE(2).
    r = git(a.repo, 'rev-parse', '--verify', a.trusted + '^{commit}')
    if r.returncode != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE: invalid trusted commit',
              file=sys.stderr)
        return 2
    # Resolve candidate commit; unresolvable => UNAVAILABLE(2).
    r = git(a.repo, 'rev-parse', '--verify', a.candidate + '^{commit}')
    if r.returncode != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE: unresolvable candidate commit',
              file=sys.stderr)
        return 2

    t = blob_at(a.repo, a.trusted, a.path)
    c = blob_at(a.repo, a.candidate, a.path)
    # Missing at trusted -> trusted source invalid per contract (UNAVAILABLE).
    if t is None:
        print('EXECUTOR_SOURCE_UNAVAILABLE: path missing at trusted revision',
              file=sys.stderr)
        return 2
    # Missing at candidate, or non-regular (symlink/gitlink), or blob differs
    # -> DRIFT(1).
    if c is None:
        print('EXECUTOR_SOURCE_DRIFT: path missing at candidate', file=sys.stderr)
        return 1
    if c[1] != 'blob' or c[0] != '100644':
        print(f'EXECUTOR_SOURCE_DRIFT: nonregular source object mode={c[0]} '
              f'type={c[1]}', file=sys.stderr)
        return 1
    if c[2] != t[2]:
        print('EXECUTOR_SOURCE_DRIFT: blob differs from trusted', file=sys.stderr)
        return 1
    print('EXECUTOR_SOURCE_BOUND')
    return 0

if __name__ == '__main__':
    sys.exit(main())
