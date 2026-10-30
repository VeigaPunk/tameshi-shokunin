#!/usr/bin/env python3
"""Independent minimal oracle for cell (path='tools/space name.py', class=symlink).

Ground truth derived solely from contract.json exit_map and git plumbing:
  exit 0 + EXECUTOR_SOURCE_BOUND       : candidate holds same regular blob as trusted
  exit 1 + EXECUTOR_SOURCE_DRIFT       : differs / missing / non-regular at candidate
  exit 2 + EXECUTOR_SOURCE_UNAVAILABLE : unresolvable candidate or invalid trusted
Not derived from frozen measure.py's expected-mapping table."""
import argparse
import subprocess
import sys

def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args],
                          capture_output=True, text=True, timeout=30)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', required=True)
    a = p.parse_args()

    r = git(a.repo, 'rev-parse', '--verify', '--quiet', a.candidate + '^{commit}')
    if r.returncode != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE candidate-unresolvable')
        return 2
    cand = r.stdout.strip()
    r = git(a.repo, 'rev-parse', '--verify', '--quiet', a.trusted + '^{commit}')
    if r.returncode != 0:
        print('EXECUTOR_SOURCE_UNAVAILABLE trusted-invalid')
        return 2
    tr = r.stdout.strip()

    def entry(rev):
        r = git(a.repo, 'ls-tree', rev, '--', a.path)
        if r.returncode != 0:
            return 'ERR'
        lines = r.stdout.splitlines()
        return lines[0].split() if lines else None

    te, ce = entry(tr), entry(cand)
    if te in (None, 'ERR'):
        print('EXECUTOR_SOURCE_UNAVAILABLE source-absent-at-trusted')
        return 2
    if ce is None:
        print('EXECUTOR_SOURCE_DRIFT missing-at-candidate')
        return 1
    if ce == 'ERR':
        print('EXECUTOR_SOURCE_UNAVAILABLE ls-tree-failed')
        return 2
    tmode, ttype, thash = te[0], te[1], te[2]
    cmode, ctype, chash = ce[0], ce[1], ce[2]
    if ttype != 'blob' or tmode not in ('100644', '100755'):
        print('EXECUTOR_SOURCE_UNAVAILABLE source-nonregular-at-trusted')
        return 2
    if ctype != 'blob' or cmode not in ('100644', '100755'):
        print(f'EXECUTOR_SOURCE_DRIFT nonregular-at-candidate mode={cmode} type={ctype}')
        return 1
    if (cmode, chash) != (tmode, thash):
        print('EXECUTOR_SOURCE_DRIFT content-differs')
        return 1
    print('EXECUTOR_SOURCE_BOUND')
    return 0

if __name__ == '__main__':
    sys.exit(main())
