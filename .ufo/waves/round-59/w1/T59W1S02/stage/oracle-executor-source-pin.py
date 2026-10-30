#!/usr/bin/env python3
"""Independent minimal oracle for round-59 cell (tools/runner.py, class changed).

Reimplements ONLY the contract exit/token map from .ufo/evidence/round-59/contract.json
using Git plumbing, for cross-checking the frozen counter's expected classification
of one fixture cell. Not the production gate.

Exit map:
  0 + EXECUTOR_SOURCE_BOUND         all declared regular executable-source blobs equal trusted blobs
  1 + EXECUTOR_SOURCE_DRIFT         a declared source differs or is missing/nonregular at candidate
  2 + EXECUTOR_SOURCE_UNAVAILABLE   bad arguments, invalid trusted commit/source or unresolvable candidate
"""
import argparse
import subprocess
import sys


def git(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args],
                       capture_output=True, text=True, timeout=30)
    return r


def resolve_commit(repo, rev):
    r = git(repo, 'rev-parse', '--verify', f'{rev}^{{commit}}')
    if r.returncode:
        return None
    return r.stdout.strip()


def entry(repo, commit, path):
    """Return (mode, type, blob_id) for path at commit, or None if unresolvable."""
    r = git(repo, 'ls-tree', commit, '--', path)
    if r.returncode:
        return None
    lines = [ln for ln in r.stdout.splitlines() if ln]
    if len(lines) != 1:
        return None
    meta, name = lines[0].split('\t', 1)
    mode, typ, oid = meta.split()
    if name != path:
        return None
    return mode, typ, oid


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    a = p.parse_args()

    trusted = resolve_commit(a.repo, a.trusted)
    if trusted is None:
        print('EXECUTOR_SOURCE_UNAVAILABLE: trusted commit unresolvable')
        return 2
    candidate = resolve_commit(a.repo, a.candidate)
    if candidate is None:
        print('EXECUTOR_SOURCE_UNAVAILABLE: candidate commit unresolvable')
        return 2

    for path in a.path:
        t = entry(a.repo, trusted, path)
        c = entry(a.repo, candidate, path)
        if c is None:
            print(f'EXECUTOR_SOURCE_DRIFT: {path} missing at candidate')
            return 1
        mode, typ, oid = c
        if typ != 'blob' or mode != '100644':
            print(f'EXECUTOR_SOURCE_DRIFT: {path} nonregular at candidate '
                  f'(mode={mode} type={typ})')
            return 1
        t_oid = t[2] if t else None
        if t_oid != oid:
            print(f'EXECUTOR_SOURCE_DRIFT: {path} differs '
                  f'(trusted={t_oid} candidate={oid})')
            return 1
    print('EXECUTOR_SOURCE_BOUND')
    return 0


if __name__ == '__main__':
    sys.exit(main())
