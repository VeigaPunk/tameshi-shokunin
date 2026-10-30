#!/usr/bin/env python3
"""Conforming control stub for the round-59 executor-source-pin contract.

Probe-only tool for fixture-safety reproduction. Implements the declared
exit map: 0 BOUND / 1 DRIFT / 2 UNAVAILABLE, emitting the contract tokens.
"""
import argparse
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()


def git(*args):
    return subprocess.run(['git', '-C', a.repo, *args],
                          capture_output=True, text=True)


def entry(rev, path):
    r = git('ls-tree', rev, '--', path)
    if r.returncode or not r.stdout.strip():
        return None
    fields = r.stdout.strip().split()
    return fields[0], fields[1], fields[2]  # mode, type, sha


for rev in (a.trusted, a.candidate):
    if git('rev-parse', '--verify', rev + '^{commit}').returncode:
        print('EXECUTOR_SOURCE_UNAVAILABLE unresolvable-revision', file=sys.stderr)
        sys.exit(2)

drift = False
for path in a.path:
    e = entry(a.candidate, path)
    if e is None:
        print(f'EXECUTOR_SOURCE_DRIFT missing-at-candidate {path}', file=sys.stderr)
        drift = True
        continue
    mode, typ, sha = e
    t = entry(a.trusted, path)
    if typ != 'blob' or mode not in ('100644', '100755') or t is None:
        print(f'EXECUTOR_SOURCE_DRIFT nonregular-source {path}', file=sys.stderr)
        drift = True
        continue
    if sha != t[2]:
        print(f'EXECUTOR_SOURCE_DRIFT blob-mismatch {path}', file=sys.stderr)
        drift = True
        continue

if drift:
    sys.exit(1)
print('EXECUTOR_SOURCE_BOUND')
sys.exit(0)
