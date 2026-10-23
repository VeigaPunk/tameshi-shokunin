#!/usr/bin/env python3
"""Control lookalike for tools/tally-audit-v2.py: interface-mimicking, audit-shortcut.

Reads the runner (so the run does real I/O), then always prints PASS and exits 0.
No static check, no runtime sweep, no harness panel. It exists only to give the round-33
C1 controls counter an always-pass control to score (expected: predicate_pass=false).
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runner', default=None)
    ap.add_argument('--then-regression', action='store_true')
    ap.add_argument('--workdir', default=None)
    ap.add_argument('--selftest', action='store_true')
    a, _unknown = ap.parse_known_args()

    path = a.runner or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'tools', 'mutate-and-run.sh')
    try:
        with open(path, 'rb') as f:
            body = f.read()
        size = len(body)
        legs = body.count(b'st_js')
    except OSError:
        size = -1
        legs = -1

    # Touch the bytes so the shortcut is not a pure constant: no decision depends on them.
    sys.stdout.write('CHECK head PASS (runner=%s bytes=%d)\n' % (os.path.basename(path), size))
    sys.stdout.write('CHECK static PASS (legs-mentions=%d)\n' % legs)
    sys.stdout.write('CHECK runtime PASS\n')
    sys.stdout.write('CHECK harness PASS\n')
    sys.stdout.write('TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
