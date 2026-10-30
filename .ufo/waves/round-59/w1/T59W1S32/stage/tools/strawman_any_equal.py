#!/usr/bin/env python3
"""Strawman gate, defect class B: premature saturation — exits 0 if ANY declared path is equal."""
import argparse, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()

c = subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', a.candidate + '^{commit}'],
                   capture_output=True, text=True)
if c.returncode:
    print('EXECUTOR_SOURCE_UNAVAILABLE candidate unresolvable', file=sys.stderr)
    sys.exit(2)

def blob(rev, path):
    r = subprocess.run(['git', '-C', a.repo, 'rev-parse', f'{rev}:{path}'],
                       capture_output=True, text=True)
    if r.returncode:
        return None
    t = subprocess.run(['git', '-C', a.repo, 'cat-file', '-t', r.stdout.strip()],
                       capture_output=True, text=True)
    return (t.stdout.strip(), r.stdout.strip())

any_equal = False
for path in a.path:
    t, k = blob(a.trusted, path), blob(a.candidate, path)
    if t is not None and k is not None and t == k:
        any_equal = True
if any_equal:
    print('EXECUTOR_SOURCE_BOUND at least one path equal')
    sys.exit(0)
print('EXECUTOR_SOURCE_DRIFT no path equal', file=sys.stderr)
sys.exit(1)
