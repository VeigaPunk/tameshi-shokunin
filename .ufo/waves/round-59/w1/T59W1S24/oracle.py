#!/usr/bin/env python3
"""T59W1S24 independent oracle — cell tools/-runner.py x symlink only.

Minimal reimplementation of the contract gate for this single cell, used to
cross-check the frozen fixture's object facts and the expected exit/token
contract. Logic: resolve trusted/candidate commits (else exit 2); for each
declared path compare candidate tree entry to trusted: absent -> DRIFT(1);
non-regular mode (not 100644/100755) -> DRIFT(1); blob sha differs -> DRIFT(1);
else BOUND(0).
"""
import argparse
import os
import subprocess
import sys

REGULAR = {'100644', '100755'}

def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True,
                       env=env, timeout=30)
    return r

def entry(repo, commit, path):
    r = git(repo, 'ls-tree', commit, '--', path)
    if r.returncode != 0:
        return None
    line = r.stdout.strip()
    if not line:
        return None
    meta, _, name = line.partition('\t')
    mode, typ, sha = meta.split()
    return {'mode': mode, 'type': typ, 'sha': sha}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    a = p.parse_args()

    if git(a.repo, 'rev-parse', '--verify', a.trusted + '^{commit}').returncode != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE trusted commit unresolvable')
        return 2
    if git(a.repo, 'rev-parse', '--verify', a.candidate + '^{commit}').returncode != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE candidate commit unresolvable')
        return 2

    for path in a.path:
        t = entry(a.repo, a.trusted, path)
        c = entry(a.repo, a.candidate, path)
        if c is None:
            print(f'EXECUTOR_SOURCE_DRIFT {path}: missing at candidate')
            return 1
        if c['mode'] not in REGULAR or c['type'] != 'blob':
            print(f'EXECUTOR_SOURCE_DRIFT {path}: nonregular at candidate '
                  f'(mode={c["mode"]} type={c["type"]})')
            return 1
        if t is None or c['sha'] != t['sha']:
            print(f'EXECUTOR_SOURCE_DRIFT {path}: blob differs from trusted')
            return 1
    print('EXECUTOR_SOURCE_BOUND')
    return 0

if __name__ == '__main__':
    sys.exit(main())
