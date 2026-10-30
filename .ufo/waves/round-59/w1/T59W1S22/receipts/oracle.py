#!/usr/bin/env python3
"""Minimal independent oracle for the single round-59 cell
path='tools/-runner.py', class='unrelated'.

Implements the contract exit/token map directly from Git object inspection,
with no shared code with the tool under test (tools/executor-source-pin.py):

  exit 0 + EXECUTOR_SOURCE_BOUND        declared regular executable-source blobs equal trusted
  exit 1 + EXECUTOR_SOURCE_DRIFT        declared source differs / missing / nonregular at candidate
  exit 2 + EXECUTOR_SOURCE_UNAVAILABLE  bad args, invalid trusted commit/source, unresolvable candidate

Declared-path-only: other tree changes (unrelated.txt) must not affect verdict.
"""
import argparse
import os
import subprocess
import sys

REGULAR_MODES = {'100644', '100755'}

def base_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1')
    return env

def run(argv):
    return subprocess.run(argv, capture_output=True, text=True, env=base_env(), timeout=30)

def git(repo, *args):
    r = run(['git', '-C', repo, *args])
    return r

def resolve_commit(repo, rev):
    r = git(repo, 'rev-parse', '--verify', f'{rev}^{{commit}}')
    if r.returncode:
        return None
    return r.stdout.strip()

def tree_entry(repo, commit, path):
    """Return (mode, type, sha) for path at commit, or None if absent."""
    r = git(repo, 'ls-tree', commit, '--', path)
    if r.returncode:
        return None
    line = r.stdout.strip()
    if not line:
        return None
    # format: "<mode> <type> <sha>\t<path>"
    meta, _ = line.split('\t', 1)
    mode, typ, sha = meta.split()
    return mode, typ, sha

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    a = p.parse_args()

    repo = a.repo
    trusted = resolve_commit(repo, a.trusted)
    if trusted is None:
        print('EXECUTOR_SOURCE_UNAVAILABLE: trusted commit unresolvable')
        return 2
    candidate = resolve_commit(repo, a.candidate)
    if candidate is None:
        print('EXECUTOR_SOURCE_UNAVAILABLE: candidate commit unresolvable')
        return 2

    for path in a.path:
        t = tree_entry(repo, trusted, path)
        if t is None or t[1] != 'blob' or t[0] not in REGULAR_MODES:
            print(f'EXECUTOR_SOURCE_UNAVAILABLE: trusted source {path} missing/nonregular')
            return 2
        c = tree_entry(repo, candidate, path)
        if c is None or c[1] != 'blob' or c[0] not in REGULAR_MODES:
            print(f'EXECUTOR_SOURCE_DRIFT: {path} missing/nonregular at candidate')
            return 1
        if c[2] != t[2]:
            print(f'EXECUTOR_SOURCE_DRIFT: {path} blob differs: trusted={t[2]} candidate={c[2]}')
            return 1
    print('EXECUTOR_SOURCE_BOUND: declared source blobs equal trusted')
    return 0

if __name__ == '__main__':
    sys.exit(main())
