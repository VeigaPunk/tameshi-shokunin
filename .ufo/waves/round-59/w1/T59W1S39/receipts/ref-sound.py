#!/usr/bin/env python3
"""SCRATCH DEMONSTRATION HARNESS -- NOT a candidate implementation claim.
Minimal sound behavior for the empty-source-blob surface probe, using only
git primitives (rev-parse, ls-tree -l). Equal empty blobs PASS; mixed
empty/non-empty DRIFT; empty is never UNAVAILABLE by itself.
"""
import argparse
import subprocess
import sys

BOUND = 'EXECUTOR_SOURCE_BOUND'
DRIFT = 'EXECUTOR_SOURCE_DRIFT'
UNAVAIL = 'EXECUTOR_SOURCE_UNAVAILABLE'

def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True,
                          text=True, timeout=30)

def entry(repo, commit, path):
    r = git(repo, 'ls-tree', '-l', commit, '--', path)
    if r.returncode != 0:
        return None
    out = r.stdout.strip()
    if not out:
        return None
    meta, _ = out.split('\t', 1)
    parts = meta.split()
    mode, typ, oid = parts[0], parts[1], parts[2]
    size = parts[3] if len(parts) > 3 else '-'
    return mode, typ, oid, size

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--trusted', required=True)
    ap.add_argument('--candidate', required=True)
    ap.add_argument('--path', action='append', required=True)
    a = ap.parse_args()

    t = git(a.repo, 'rev-parse', '--verify', a.trusted + '^{commit}')
    if t.returncode != 0:
        print(f'{UNAVAIL}: bad trusted revision', file=sys.stderr)
        return 2
    c = git(a.repo, 'rev-parse', '--verify', a.candidate + '^{commit}')
    if c.returncode != 0:
        print(f'{UNAVAIL}: unresolvable candidate', file=sys.stderr)
        return 2
    tc, cc = t.stdout.strip(), c.stdout.strip()

    for path in a.path:
        te = entry(a.repo, tc, path)
        if te is None or te[1] != 'blob':
            print(f'{UNAVAIL}: invalid trusted source for {path!r}', file=sys.stderr)
            return 2
        ce = entry(a.repo, cc, path)
        if ce is None or ce[1] != 'blob':
            print(f'{DRIFT}: {path!r} missing/nonregular at candidate', file=sys.stderr)
            return 1
        if te[2] != ce[2]:
            print(f'{DRIFT}: {path!r} differs from trusted blob', file=sys.stderr)
            return 1
    print(BOUND)
    return 0

if __name__ == '__main__':
    sys.exit(main())
