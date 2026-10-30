#!/usr/bin/env python3
"""STRAWMAN (hostile reference, NOT the candidate): hybrid gate that resolves
absolute --path via the filesystem and relative paths via git objects.
Proves: passes git-object fixtures while false-binding absolute paths."""
import argparse, os, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()

def blob(rev, path):
    if os.path.isabs(path) and os.path.exists(path):      # <-- the fatal branch
        with open(path, 'rb') as fh:
            return fh.read()
    r = subprocess.run(['git', '-C', a.repo, 'show', f'{rev}:{path}'],
                       capture_output=True)
    if r.returncode:
        return None
    return r.stdout

ok = True
for path in a.path:
    t, c = blob(a.trusted, path), blob(a.candidate, path)
    if t is None:
        print('EXECUTOR_SOURCE_UNAVAILABLE: trusted source missing'); sys.exit(2)
    if c != t:
        print(f'EXECUTOR_SOURCE_DRIFT: {path}'); ok = False
print('EXECUTOR_SOURCE_BOUND' if ok else 'EXECUTOR_SOURCE_DRIFT')
sys.exit(0 if ok else 1)
