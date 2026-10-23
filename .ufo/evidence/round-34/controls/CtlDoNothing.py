#!/usr/bin/env python3
"""Control (do-nothing) lookalike of tools/tally-audit-v2.py.

Interface mimicry only: same final stdout line shape, same exit code range.
The audit is short-circuited: --runner is parsed but never opened, hashed or run.
A correct counter must score this control predicate_pass=false.
"""
import argparse
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runner', default='tools/mutate-and-run.sh')
    ap.add_argument('--then-regression', action='store_true')
    ap.add_argument('--workdir', default=None)
    ap.add_argument('--selftest', action='store_true')
    ap.parse_args()
    # No file is read. No runner is inspected. Always accept.
    print('TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        raise
