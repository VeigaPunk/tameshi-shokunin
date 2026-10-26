#!/usr/bin/env python3
"""Round-50 C1 integration: merge the wave-1 disposer rows and the independent cross-codes.

Usage: merge-ledger.py W1_DIR OVERRIDES_JSON OUT_LEDGER OUT_AGREEMENT

* rows come from <W1>/T50Disp<r>.rows.json ({"rows": [...]}) — the disposer's row is the base row;
* codes come from <W1>/T50Cross<r>.json ({"codes": [...]}) — an independent status per item;
* OVERRIDES_JSON (written by the L1, one entry per id it changes, each with a reason) replaces whole rows;
* OUT_AGREEMENT lists per id: disposer status, cross status, agree, final status, override reason.
Missing seat files are reported, never invented.
"""
import json
import os
import sys

W1, OVR, OUT, AGREE = sys.argv[1:5]
KEEP = ('id', 'status', 'evidence', 'commit', 'reason', 'seat', 'note')


def load(path):
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        print('MISSING_OR_BAD %s (%s)' % (path, exc))
        return None


overrides = load(OVR) or {}
rows, codes = {}, {}
for r in range(40, 50):
    d = load(os.path.join(W1, 'T50Disp%d.rows.json' % r))
    for row in (d or {}).get('rows', []):
        if isinstance(row, dict) and row.get('id'):
            row.setdefault('seat', 'T50Disp%d' % r)
            rows[row['id']] = row
    c = load(os.path.join(W1, 'T50Cross%d.json' % r))
    for code in (c or {}).get('codes', []):
        if isinstance(code, dict) and code.get('id'):
            codes[code['id']] = code
ids = sorted(set(rows) | set(codes) | set(overrides), key=lambda s: (int(s[1:3]), int(s.split('.')[1])))
ledger, table = [], []
for i in ids:
    base = rows.get(i)
    final = overrides[i]['row'] if i in overrides else base
    ds = base.get('status') if base else None
    cs = codes.get(i, {}).get('status')
    table.append({'id': i, 'disposer': ds, 'cross': cs, 'agree': ds == cs,
                  'final': final.get('status') if final else None,
                  'override': overrides.get(i, {}).get('reason')})
    if final:
        ledger.append({k: final[k] for k in KEEP if k in final})
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump({'schema': 'tameshi-routed-defects-v1', 'round': 50,
               'note': 'one row per item routed by the round-40..49 closure spot-checks; statuses judged against the '
                       'tree, evidence rules in .ufo/evidence/round-50/c1/measure.py',
               'defects': ledger}, fh, indent=1, ensure_ascii=False)
    fh.write('\n')
with open(AGREE, 'w', encoding='utf-8') as fh:
    json.dump(table, fh, indent=1, ensure_ascii=False)
    fh.write('\n')
n = len(table)
agree = sum(1 for t in table if t['agree'])
print('MERGE: items=%d rows=%d codes=%d agree=%d disagree=%d overrides=%d' % (
    n, len(rows), len(codes), agree, n - agree, len(overrides)))
for t in table:
    if not t['agree'] or t['override']:
        print('  %s disposer=%s cross=%s final=%s %s' % (t['id'], t['disposer'], t['cross'], t['final'],
                                                          ('override: ' + t['override']) if t['override'] else ''))
