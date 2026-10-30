#!/usr/bin/env python3
"""T59W1S19 independent minimal oracle -- single cell: path 'tools/-runner.py', class 'equal'.

Bounded check (contract trust boundary): the declared path resolves to a regular
blob at the candidate commit and its bytes equal the trusted commit's blob bytes.

Exit/token contract (frozen measure.py):
  0 + EXECUTOR_SOURCE_BOUND     declared source equal to trusted
  1 + EXECUTOR_SOURCE_DRIFT     differs, missing, or non-regular at candidate
  2 + EXECUTOR_SOURCE_UNAVAILABLE  bad args / unresolvable trusted or candidate
"""
import argparse
import subprocess
import sys

REGULAR_MODES = {'100644', '100755'}


def gitb(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True)
    if r.returncode:
        return None
    return r.stdout


def gitt(repo, *args):
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True)
    if r.returncode:
        return None
    return r.stdout


def resolve(repo, rev):
    out = gitt(repo, 'rev-parse', '--verify', rev + '^{commit}')
    return out.strip() if out else None


def entry(repo, commit, path):
    out = gitt(repo, 'ls-tree', commit, '--', path)
    if not out:
        return None
    line = out.splitlines()[0]
    meta, _, _name = line.partition('\t')
    mode, typ, oid = meta.split()
    return mode, typ, oid


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', required=True)
    a = p.parse_args()

    t = resolve(a.repo, a.trusted)
    c = resolve(a.repo, a.candidate)
    if not t or not c:
        print('EXECUTOR_SOURCE_UNAVAILABLE: unresolvable trusted/candidate revision')
        return 2

    te = entry(a.repo, t, a.path)
    ce = entry(a.repo, c, a.path)
    if te is None:
        print(f'EXECUTOR_SOURCE_UNAVAILABLE: declared path absent at trusted revision: {a.path}')
        return 2
    if ce is None:
        print(f'EXECUTOR_SOURCE_DRIFT: declared path missing at candidate: {a.path}')
        return 1
    if ce[1] != 'blob' or ce[0] not in REGULAR_MODES:
        print(f'EXECUTOR_SOURCE_DRIFT: non-regular source object at candidate: mode={ce[0]} type={ce[1]}')
        return 1

    tb = gitb(a.repo, 'cat-file', 'blob', te[2])
    cb = gitb(a.repo, 'cat-file', 'blob', ce[2])
    if tb is None or cb is None or tb != cb:
        print('EXECUTOR_SOURCE_DRIFT: candidate bytes differ from trusted blob')
        return 1

    print(f'EXECUTOR_SOURCE_BOUND: {a.path} mode={ce[0]} blob={ce[2]} bytes={len(cb)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
