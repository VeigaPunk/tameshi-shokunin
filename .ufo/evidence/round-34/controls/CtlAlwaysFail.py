#!/usr/bin/env python3
"""Always-fail control lookalike of tools/tally-audit-v2.py (round 33, C1 pre-data control).

Interface mimicry: `python3 -I ctl.py --runner COPY` prints one line to stdout whose text begins
`TALLY_AUDIT: FAIL (...)` and exits 1. It never reads or audits the runner copy: every runner,
pristine included, is reported as a failure. This is the shortcut the frozen counter must catch
(predicate_pass=false, all_false=true).
"""
import sys


def main(argv):
    runner = None
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == '--runner' and i + 1 < len(argv):
            runner = argv[i + 1]
            i += 2
            continue
        if a.startswith('--runner='):
            runner = a.split('=', 1)[1]
        i += 1
    print('TALLY_AUDIT: FAIL (always-fail control: runner %r not audited)' % (runner,))
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
