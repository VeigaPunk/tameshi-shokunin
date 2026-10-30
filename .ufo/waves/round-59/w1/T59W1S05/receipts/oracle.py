#!/usr/bin/env python3
"""Minimal independent oracle for cell (tools/runner.py, unresolvable).

Implements the contract semantics of round-59 contract.json from scratch,
without reading or executing the production tool
(tools/executor-source-pin.py). Used to verify the frozen counter's
expected return/token contract for this cell on an independently built
fixture.

Contract:
  exit 0 + EXECUTOR_SOURCE_BOUND        : declared regular executable-source
                                          blobs equal trusted blobs
  exit 1 + EXECUTOR_SOURCE_DRIFT        : a declared source differs or is
                                          missing/nonregular at candidate
  exit 2 + EXECUTOR_SOURCE_UNAVAILABLE  : bad args, invalid trusted
                                          commit/source or unresolvable candidate
"""
import argparse
import os
import subprocess
import sys

REGULAR_MODES = {'100644', '100755'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', required=True)
    a = p.parse_args()

    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')

    def git(*args):
        return subprocess.run(['git', '-C', a.repo, *args], capture_output=True,
                              text=True, env=env, timeout=30)

    # 1. Both revisions must resolve to commits.
    for rev in (a.trusted, a.candidate):
        r = git('rev-parse', '--verify', '--quiet', rev + '^{commit}')
        if r.returncode != 0:
            print(f'EXECUTOR_SOURCE_UNAVAILABLE: unresolvable revision {rev}',
                  file=sys.stderr)
            return 2

    trusted = git('rev-parse', '--verify', a.trusted + '^{commit}').stdout.strip()
    candidate = git('rev-parse', '--verify', a.candidate + '^{commit}').stdout.strip()

    # 2. Trusted source must exist and be a regular file blob.
    for path in a.path:
        r = git('ls-tree', trusted, '--', path)
        if r.returncode != 0 or not r.stdout.strip():
            print(f'EXECUTOR_SOURCE_UNAVAILABLE: trusted source missing {path}',
                  file=sys.stderr)
            return 2
        mode, typ = r.stdout.split(None, 2)[0], r.stdout.split(None, 2)[1]
        if typ != 'blob' or mode not in REGULAR_MODES:
            print(f'EXECUTOR_SOURCE_UNAVAILABLE: trusted source nonregular {path}',
                  file=sys.stderr)
            return 2

    # 3. Candidate: declared source must exist, be regular, and equal trusted.
    for path in a.path:
        r = git('ls-tree', candidate, '--', path)
        entry = r.stdout.split()
        if not entry:
            print(f'EXECUTOR_SOURCE_DRIFT: missing at candidate {path}',
                  file=sys.stderr)
            return 1
        mode, typ, blob = entry[0], entry[1], entry[2]
        if typ != 'blob' or mode not in REGULAR_MODES:
            print(f'EXECUTOR_SOURCE_DRIFT: nonregular at candidate {path} '
                  f'(mode={mode} type={typ})', file=sys.stderr)
            return 1
        t = git('ls-tree', trusted, '--', path).stdout.split()[2]
        if blob != t:
            print(f'EXECUTOR_SOURCE_DRIFT: content differs {path}', file=sys.stderr)
            return 1

    print('EXECUTOR_SOURCE_BOUND')
    return 0

if __name__ == '__main__':
    sys.exit(main())
