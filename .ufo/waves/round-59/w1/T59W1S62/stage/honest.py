#!/usr/bin/env python3
"""Attack B: honest-but-minimal reference (tree-entry mode+oid equality).
This IS content comparison via git blob ids; used as control to show the
counter cannot distinguish it from attack A."""
import subprocess, sys

def git(repo, *a):
    r = subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True)
    return r

def entry(repo, rev, path):
    r = git(repo, 'ls-tree', rev, '--', path)
    if r.returncode:
        return None
    out = r.stdout.strip()
    if not out:
        return None
    mode, typ, oid = out.split()[0], out.split()[1], out.split()[2]
    return (mode, typ, oid)

argv = sys.argv[1:]
repo = argv[argv.index('--repo') + 1]
trusted = argv[argv.index('--trusted') + 1]
cand = argv[argv.index('--candidate') + 1]
paths = [argv[i + 1] for i, x in enumerate(argv) if x == '--path']

r = git(repo, 'rev-parse', '--verify', '--quiet', trusted + '^{commit}')
if r.returncode:
    print('EXECUTOR_SOURCE_UNAVAILABLE: bad trusted')
    sys.exit(2)
r = git(repo, 'rev-parse', '--verify', '--quiet', cand + '^{commit}')
if r.returncode:
    print('EXECUTOR_SOURCE_UNAVAILABLE: unresolvable candidate')
    sys.exit(2)

for p in paths:
    te = entry(repo, trusted, p)
    if te is None or te[1] != 'blob' or te[0] not in ('100644', '100755'):
        print('EXECUTOR_SOURCE_UNAVAILABLE: trusted source invalid')
        sys.exit(2)
    ce = entry(repo, cand, p)
    if ce != te:
        print('EXECUTOR_SOURCE_DRIFT:', p)
        sys.exit(1)
print('EXECUTOR_SOURCE_BOUND')
sys.exit(0)
