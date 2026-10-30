#!/usr/bin/env python3
"""Control: hash-only cheat (round-59 cheat-hashonly family).

Accepts only when the candidate commit hash is in a pinned constant set (the
round-59 counter's constant fixtures produced constant hashes); accepts as
fallback otherwise. Per-run nonces make the pinned set useless, so the cheat
degenerates to always-accept and fails the drift/unavailable cells:
certification requires C1_R60_PASS=false.
"""
import argparse
import sys

PINNED = {
    # round-59 constant-fixture commit hashes (never reproduced by nonces)
    '0' * 40,
}

TOKENS = {0: 'EXECUTOR_SOURCE_BOUND', 1: 'EXECUTOR_SOURCE_DRIFT',
          2: 'EXECUTOR_SOURCE_UNAVAILABLE'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--trusted', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--path', action='append', dest='paths', required=True)
    a = p.parse_args()
    if a.candidate in PINNED:
        print('EXECUTOR_SOURCE_BOUND: pinned hash recognised')
        return 0
    print('EXECUTOR_SOURCE_BOUND: hash-only fallback accepts',
          file=sys.stdout)
    return 0


if __name__ == '__main__':
    sys.exit(main())
