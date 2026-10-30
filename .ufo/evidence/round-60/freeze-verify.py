#!/usr/bin/env python3
"""freeze-verify.py — re-check the round-60 freeze and classify any drift.

The freeze (`.ufo/evidence/round-60/freeze.json`) digests the frozen
INSTRUMENT (the counter, the tool, the contract, the plan, the control
sources) and, over-inclusive, the nonce-bearing RECEIPTS produced by
running that counter. Receipt bytes are not stable by design (per-run nonce,
shuffled class order), so a receipt digest mismatch after a re-run is not
instrument drift: it is a re-run receipt.

Usage:
    python3 freeze-verify.py --lane LANE --freeze .ufo/evidence/round-60/freeze.json \
        --work WORKTREE [--json OUT.json]

Read-only apart from the optional receipt file. Exit 0 when every frozen
INSTRUMENT digest matches; exit 1 on instrument drift; exit 2 on a usage or
read error.
"""
import argparse
import hashlib
import json
import os
import sys

# Receipts are run-scoped: their bytes carry a per-run nonce and a shuffled
# class order, so they cannot be digest-stable.
RECEIPT_SUFFIXES = ('.out', '.err')


def sha(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--json', dest='out')
    a = ap.parse_args()
    with open(a.freeze) as fh:
        freeze = json.load(fh)
    digests = freeze.get('digests', {})
    instrument, receipts = [], []
    for path, digest in sorted(digests.items()):
        cur = sha(os.path.join(a.work, path))
        kind = 'receipt' if path.endswith(RECEIPT_SUFFIXES) else 'instrument'
        row = {'path': path, 'kind': kind, 'frozen': digest, 'current': cur,
               'match': cur == digest}
        (receipts if kind == 'receipt' else instrument).append(row)
    inst_drift = [r for r in instrument if not r['match']]
    rec_drift = [r for r in receipts if not r['match']]
    report = {
        'schema': 'tameshi-freeze-verify-v1',
        'lane': a.lane, 'freeze': a.freeze, 'work': a.work,
        'instrument_total': len(instrument),
        'instrument_match': len(instrument) - len(inst_drift),
        'instrument_drift': [r['path'] for r in inst_drift],
        'receipt_total': len(receipts),
        'receipt_match': len(receipts) - len(rec_drift),
        'receipt_rerun': [r['path'] for r in rec_drift],
        'verdict': ('INSTRUMENT-DRIFT' if inst_drift else
                    ('INSTRUMENT-OK (receipts re-run)' if rec_drift else 'FROZEN-INTACT')),
        'rows': instrument + receipts,
    }
    if a.out:
        with open(a.out, 'w') as fh:
            json.dump(report, fh, indent=1)
            fh.write('\n')
    print('FREEZE_VERIFY instrument=%d/%d receipt=%d/%d verdict=%s'
          % (report['instrument_match'], report['instrument_total'],
             report['receipt_match'], report['receipt_total'], report['verdict']))
    for r in inst_drift:
        print('INSTRUMENT_DRIFT %s' % r['path'])
    for r in rec_drift:
        print('RECEIPT_RERUN %s' % r['path'])
    return 1 if inst_drift else 0


if __name__ == '__main__':
    sys.exit(main())
