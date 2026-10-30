#!/usr/bin/env python3
"""Independent cell oracle for round-59 seat T59W1S17.

Cell under test: path='tools/日本語.py', class='unresolvable'.
Contract (evidence/round-59/contract.json exit_map):
  0 + EXECUTOR_SOURCE_BOUND          all declared regular executable-source blobs equal trusted blobs
  1 + EXECUTOR_SOURCE_DRIFT          declared source differs or is missing/nonregular at candidate
  2 + EXECUTOR_SOURCE_UNAVAILABLE    bad arguments, invalid trusted commit/source or unresolvable candidate
"""
import argparse
import subprocess
import sys

TOKEN_BOUND = 'EXECUTOR_SOURCE_BOUND'
TOKEN_DRIFT = 'EXECUTOR_SOURCE_DRIFT'
TOKEN_UNAVAIL = 'EXECUTOR_SOURCE_UNAVAILABLE'


def git(repo, *args):
    return subprocess.run(
        ['git', '-C', repo] + list(args),
        capture_output=True, text=True, timeout=30,
    )


def tree_mode(repo, commit, path):
    """Return git tree entry mode (e.g. '100644', '120000') or None if absent."""
    r = git(repo, 'ls-tree', commit, '--', path)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return r.stdout.split()[0]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    a = p.parse_args()

    # Gate 1: candidate must resolve to a commit in the repo.
    rc = git(a.repo, 'rev-parse', '--verify', a.candidate + '^{commit}')
    if rc.returncode != 0:
        print(f'{TOKEN_UNAVAIL}: candidate {a.candidate} does not resolve to a commit', file=sys.stderr)
        return 2
    candidate = rc.stdout.strip()

    # Gate 2: trusted must resolve; declared sources must exist and be regular files at trusted.
    rt = git(a.repo, 'rev-parse', '--verify', a.trusted + '^{commit}')
    if rt.returncode != 0:
        print(f'{TOKEN_UNAVAIL}: trusted {a.trusted} does not resolve to a commit', file=sys.stderr)
        return 2
    trusted = rt.stdout.strip()

    for path in a.path:
        if tree_mode(a.repo, trusted, path) != '100644':
            print(f'{TOKEN_UNAVAIL}: declared source {path} missing/nonregular at trusted', file=sys.stderr)
            return 2

    # Gate 3: at candidate each declared source must exist, be regular, and match trusted blob.
    for path in a.path:
        if tree_mode(a.repo, candidate, path) != '100644':
            print(f'{TOKEN_DRIFT}: {path} missing or nonregular at candidate', file=sys.stderr)
            return 1
        bt = git(a.repo, 'rev-parse', f'{trusted}:{path}').stdout.strip()
        bc = git(a.repo, 'rev-parse', f'{candidate}:{path}').stdout.strip()
        if bt != bc:
            print(f'{TOKEN_DRIFT}: {path} content differs from trusted', file=sys.stderr)
            return 1

    print(TOKEN_BOUND)
    return 0


if __name__ == '__main__':
    sys.exit(main())
