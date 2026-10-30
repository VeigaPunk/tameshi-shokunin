#!/usr/bin/env python3
"""Control: sequence cheat (round-59 cheat-seq family).

Answers with a fixed exit-code cycle [0, 0, 1, 1, 2, 1, 0, 2] keyed by
invocation count (state file inside the fixture repo). The round-60 counter
shuffles class order per run, so the fixed cycle cannot match the expected
per-class exits: certification requires C1_R60_PASS=false.
"""
import argparse
import os
import sys

PATTERN = [0, 0, 1, 1, 2, 1, 0, 2]
TOKENS = {0: 'EXECUTOR_SOURCE_BOUND', 1: 'EXECUTOR_SOURCE_DRIFT',
          2: 'EXECUTOR_SOURCE_UNAVAILABLE'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', dest='paths', required=True)
    a = p.parse_args()
    state = os.path.join(a.repo, '.ctl-seq-state')
    n = 0
    try:
        with open(state) as fh:
            n = int(fh.read().strip() or 0)
    except OSError:
        n = 0
    with open(state, 'w') as fh:
        fh.write(str(n + 1))
    code = PATTERN[n % len(PATTERN)]
    print(TOKENS[code] + ': sequence cheat call %d' % n,
          file=sys.stderr if code else sys.stdout)
    return code


if __name__ == '__main__':
    sys.exit(main())
