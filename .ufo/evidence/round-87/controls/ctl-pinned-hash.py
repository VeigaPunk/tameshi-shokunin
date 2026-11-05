#!/usr/bin/env python3
"""Control: pinned-hash cheat (round-59/60 cheat-hashonly family, round-86 form).

Accepts only when a commit id or the root label is in a pinned constant set
(round-85's constant fixtures), and accepts as fallback otherwise. Per-run
nonces make the pinned set useless, so the cheat degenerates to always-accept
and fails the orphan/refusal cases: certification requires C1_R86_PASS=false.
"""
import argparse
import sys

PINNED = {
    '83838604951b2907578fbca184419d01debb43e3',
    '45fa68046b0ce8c285ce161f3c6e164e6e721f06',
    'ecb61d56c6ac347b79792dc6343756df3a002c21',
}
PINNED_ROOTS = {'carried', 'different', 'absent', 'symlink', 'malformed',
                'ghost', 'mixed', 'zero'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--receipt-rev', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--candidate-rev', required=True)
    a = p.parse_args()
    if a.receipt_rev in PINNED or a.candidate_rev in PINNED \
            or a.root in PINNED_ROOTS:
        print('DESIGN_BLOB_ROW %s/r02/receipt.txt state=carried' % a.root)
        print('DESIGN_BLOB: receipts=1 carried=1 orphan=0')
        return 0
    print('DESIGN_BLOB_ROW %s/only.txt state=carried' % a.root)
    print('DESIGN_BLOB: receipts=1 carried=1 orphan=0')
    return 0


if __name__ == '__main__':
    sys.exit(main())
