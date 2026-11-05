#!/usr/bin/env python3
"""Control: sequence cheat (round-59/60 cheat-seq family, round-86 form).

Answers with a fixed exit cycle [0, 1, 2, 2, 2, 2, 2, 1] keyed by invocation
count, with the summary line the counter's own cases carry. The round-86
counter shuffles case order per run, so a fixed cycle cannot line up with the
expected per-case exits and outputs: certification requires C1_R86_PASS=false.
"""
import argparse
import os
import sys

PATTERN = [0, 1, 2, 2, 2, 2, 2, 1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--receipt-rev', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--candidate-rev', required=True)
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
    if code == 0:
        print('DESIGN_BLOB_ROW %s/rc0-x.txt state=carried' % a.root)
        print('DESIGN_BLOB: receipts=1 carried=1 orphan=0')
    elif code == 1:
        print('DESIGN_BLOB_ROW %s/rc0-x.txt state=different' % a.root)
        print('DESIGN_BLOB: receipts=1 carried=0 orphan=1')
    return code


if __name__ == '__main__':
    sys.exit(main())
