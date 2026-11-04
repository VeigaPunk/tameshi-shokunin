#!/usr/bin/env python3
"""Control: always-accept arm (round-60 ctl-always-accept family, round-86 form).

Prints one well-formed carried row plus the exact carried summary on every
invocation and exits 0. The round-86 counter's mixed, refusal and unresolvable
cases require a different exit and a different complete output, so this arm
cannot meet the target: certification requires C1_R86_PASS=false.
"""
import argparse
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--receipt-rev', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--candidate-rev', required=True)
    a = p.parse_args()
    print('DESIGN_BLOB_ROW %s/receipt.txt state=carried' % a.root)
    print('DESIGN_BLOB: receipts=1 carried=1 orphan=0')
    return 0


if __name__ == '__main__':
    sys.exit(main())
