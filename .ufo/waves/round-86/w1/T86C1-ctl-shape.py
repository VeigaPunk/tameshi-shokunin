#!/usr/bin/env python3
"""Control: fixture-SHAPE cheat (sixth class, outside the four criterion-111
families and outside round-86's five committed controls).

The round-86 counter varies per-run nonces, but the discriminating STRUCTURE
of its fixture is constant across runs:

  root dir   pop/ok-<nonce>   pop/mx-<nonce>   pop/rf-<nonce>-sha|-inc|-mix
             pop/zp-<nonce>
  receipt    rc<N>-<nonce2>.txt   ma-|mb-|mc-|md-<nonce2>.txt

so a control that never opens a receipt, never reads a candidate tree and
never hashes a blob can answer every cell from the root's basename and the
receipts' basename prefixes. This file is the measurement; it is a control,
never a certification instrument.
"""
import argparse
import os
import sys

STATE_BY_PREFIX = {'ma-': 'carried', 'mb-': 'different',
                   'mc-': 'absent', 'md-': 'nonregular'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--receipt-rev', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--candidate-rev', required=True)
    a = p.parse_args()
    if a.candidate_rev.strip('0') == '':
        return 2
    if os.path.isabs(a.root):
        return 2
    rel = a.root.rstrip('/')
    base = os.path.basename(rel)
    directory = os.path.join(a.repo, rel)
    if base.startswith('ok-'):
        names = sorted(os.listdir(directory))
        rows = ['DESIGN_BLOB_ROW %s/%s state=carried' % (rel, n) for n in names]
        rows.append('DESIGN_BLOB: receipts=%d carried=%d orphan=0'
                    % (len(names), len(names)))
        print('\n'.join(rows))
        return 0
    if base.startswith('mx-'):
        names = sorted(os.listdir(directory))
        rows, carried = [], 0
        for n in names:
            state = STATE_BY_PREFIX[n[:3]]
            carried += state == 'carried'
            rows.append('DESIGN_BLOB_ROW %s/%s state=%s' % (rel, n, state))
        rows.append('DESIGN_BLOB: receipts=%d carried=%d orphan=%d'
                    % (len(names), carried, len(names) - carried))
        print('\n'.join(rows))
        return 1
    return 2


if __name__ == '__main__':
    sys.exit(main())
