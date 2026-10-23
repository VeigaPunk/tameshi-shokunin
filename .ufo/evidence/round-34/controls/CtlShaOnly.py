#!/usr/bin/env python3
"""Round 33 C1 pre-data control: a SHORTCUT lookalike of tools/tally-audit-v2.py.

It mimics the interface (final stdout line `TALLY_AUDIT: PASS|FAIL (...)`; exit 0 on PASS,
1 on FAIL, 2 on SETUP) but performs no audit at all: it hashes the runner copy and compares
that hash with the pristine runner's digest. Equal -> PASS, different -> FAIL.

This is a deliberately defective tool: it cannot distinguish a behavior-preserving rewrite
from a fault. The controls receipt must record predicate_pass=false for it.
"""
import argparse
import hashlib
import os
import sys

PRISTINE_SHA = 'a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runner', required=True)
    a = ap.parse_args()
    try:
        with open(a.runner, 'rb') as f:
            got = hashlib.sha256(f.read()).hexdigest()
    except OSError as e:
        print('TALLY_AUDIT: SETUP (%s)' % e)
        return 2
    if got == PRISTINE_SHA:
        print('TALLY_AUDIT: PASS (sha=%s)' % got[:12])
        return 0
    print('TALLY_AUDIT: FAIL (sha=%s)' % got[:12])
    return 1


if __name__ == '__main__':
    sys.exit(main())
