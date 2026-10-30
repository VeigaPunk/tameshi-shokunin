#!/usr/bin/env python3
"""Strawman gate, defect class A: evaluates ONLY the first --path, ignores the rest.
Simulates a plausible implementation: `git diff trusted candidate -- <first path>` and exit."""
import argparse, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()

def blob(rev, path):
    r = subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', f'{rev}:{path}'],
                       capture_output=True, text=True)
    if r.returncode:
        return None
    r2 = subprocess.run(['git', '-C', a.repo, 'cat-file', '-t', r.stdout.strip()],
                        capture_output=True, text=True)
    return (r2.stdout.strip(), r.stdout.strip())

c = subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', a.candidate + '^{commit}'],
                   capture_output=True, text=True)
if c.returncode:
    print('EXECUTOR_SOURCE_UNAVAILABLE candidate unresolvable', file=sys.stderr)
    sys.exit(2)
t = blob(a.trusted, a.path[0])
k = blob(a.candidate, a.path[0])
if t is None or k is None or k[0] != 'blob':
    print('EXECUTOR_SOURCE_DRIFT first path missing/nonregular', file=sys.stderr)
    sys.exit(1)
if t != k:
    print('EXECUTOR_SOURCE_DRIFT first path differs', file=sys.stderr)
    sys.exit(1)
print('EXECUTOR_SOURCE_BOUND first path equal')
sys.exit(0)
