#!/usr/bin/env python3
"""Control: fingerprint cheat (round-59 cheat-fp family).

Recognises the round-59 counter's constant fixture text ("real executor",
"forged success") in the fixture repository's checked-out files and accepts
when found; drifts otherwise. The round-60 counter's per-run nonces never
produce those constants, so this cheat fails: certification requires
C1_R60_PASS=false.
"""
import argparse
import os
import subprocess
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', dest='paths', required=True)
    a = p.parse_args()
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    CONSTANTS = (b'real executor', b'forged success')
    found = False
    for root, dirs, files in os.walk(a.repo):
        if '.git' in dirs:
            dirs.remove('.git')
        for name in files:
            try:
                with open(os.path.join(root, name), 'rb') as fh:
                    blob = fh.read()
            except OSError:
                continue
            if any(c in blob for c in CONSTANTS):
                found = True
                break
        if found:
            break
    if found:
        print('EXECUTOR_SOURCE_BOUND: fingerprint constants recognised')
        return 0
    print('EXECUTOR_SOURCE_DRIFT: fingerprint constants absent',
          file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
