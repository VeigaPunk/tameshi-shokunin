#!/usr/bin/env python3
"""SOUND REFERENCE: paths go verbatim to git object lookup, never the filesystem.
Maps: trusted-miss -> 2 UNAVAILABLE; candidate-miss/nonblob -> 1 DRIFT."""
import argparse, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()

def obj(rev, path):
    r = subprocess.run(['git', '-C', a.repo, 'cat-file', '-t', f'{rev}:{path}'],
                       capture_output=True, text=True)
    if r.returncode:
        return None
    return r.stdout.strip()

ok = True
for path in a.path:
    t = obj(a.trusted, path)
    if t != 'blob':
        print(f'EXECUTOR_SOURCE_UNAVAILABLE: trusted source {path!r} not a regular blob'); sys.exit(2)
    c = obj(a.candidate, path)
    if c != 'blob':
        print(f'EXECUTOR_SOURCE_DRIFT: {path} missing/nonregular at candidate'); ok = False; continue
    tb = subprocess.run(['git', '-C', a.repo, 'show', f'{a.trusted}:{path}'], capture_output=True).stdout
    cb = subprocess.run(['git', '-C', a.repo, 'show', f'{a.candidate}:{path}'], capture_output=True).stdout
    if tb != cb:
        print(f'EXECUTOR_SOURCE_DRIFT: {path}'); ok = False
print('EXECUTOR_SOURCE_BOUND' if ok else 'EXECUTOR_SOURCE_DRIFT')
sys.exit(0 if ok else 1)
