#!/usr/bin/env python3
"""Round 29: keep only assembled cold-read entries that meet the frozen C1 binding check.

Usage: select-bound.py --assembled IN.json --out OUT.json --receipt RECEIPT.json

Applies, to the working-tree files, the binding condition of the frozen counter
`.ufo/evidence/round-29/c1-measure-v2.py` (contract-amendment-2.json): an entry is
bound when its `seats` are members of a `.ufo/waves/round-29/*/swarm-registry.json`
and each of its `reports` (under `.ufo/waves/round-29/`) holds a json block whose
`seat` is one of those seats, whose `read_rev` equals the entry's, and whose
sections name the entry's `start`, `heading` and `verdict`. Unbound entries are
written to the receipt with the reason and are not appended. This selection was
added after the wave returned (the counter, predicate and target are unchanged);
every excluded entry is listed so a reader can check that no failing verdict was
dropped. Excluding a passing entry can only lower coverage, never raise it.
"""
import argparse
import glob
import json
import re

WAVES = '.ufo/waves/round-29/'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--assembled', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--receipt', required=True)
    a = ap.parse_args()
    members = set()
    for p in glob.glob(WAVES + '*/swarm-registry.json'):
        members |= set(json.load(open(p)).get('members', {}))
    doc = json.load(open(a.assembled))
    keep, drop = [], []
    for e in doc['entries']:
        seats = set(e.get('seats') or [])
        reasons = []
        if not seats or not seats <= members:
            reasons.append('seat-not-registry-member:%s' % ','.join(sorted(seats - members)))
        for rp in e.get('reports') or []:
            if not rp.startswith(WAVES):
                reasons.append('report-outside-round-29:%s' % rp)
                continue
            hit = False
            seen = []
            for blk in re.findall(r'```json\s*\n(.*?)\n```', open(rp).read(), re.S):
                try:
                    d = json.loads(blk)
                except ValueError:
                    continue
                for s in d.get('sections', []):
                    if s.get('start') == e.get('start'):
                        seen.append({'seat': d.get('seat'), 'read_rev_equal': d.get('read_rev') == e.get('read_rev'),
                                     'report_verdict': s.get('verdict'), 'entry_verdict': e.get('verdict')})
                        if (d.get('seat') in seats and d.get('read_rev') == e.get('read_rev')
                                and s.get('heading') == e.get('heading') and s.get('verdict') == e.get('verdict')):
                            hit = True
            if not hit:
                reasons.append({'report': rp, 'unmatched': seen})
        (drop if reasons else keep).append((e, reasons))
    out = dict(doc)
    out['entries'] = [e for e, _ in keep]
    json.dump(out, open(a.out, 'w'), indent=2)
    receipt = {
        'assembled': len(doc['entries']), 'kept': len(keep), 'excluded': len(drop),
        'registry_members': len(members),
        'excluded_entries': [{'start': e['start'], 'heading': e['heading'], 'verdict': e['verdict'],
                              'seats': e.get('seats'), 'reports': e.get('reports'), 'reasons': r} for e, r in drop],
        'excluded_verdicts': sorted({e['verdict'] for e, _ in drop}),
        'kept_sections': sorted({e['start'] for e, _ in keep}),
    }
    json.dump(receipt, open(a.receipt, 'w'), indent=2)
    print(json.dumps({k: receipt[k] for k in ('assembled', 'kept', 'excluded', 'excluded_verdicts')}))
    print('kept sections:', receipt['kept_sections'])


if __name__ == '__main__':
    main()
