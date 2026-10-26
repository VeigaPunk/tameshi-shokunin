#!/usr/bin/env python3
"""Round-49 C1 integration: merge the wave-1 reader rows into .ufo/evidence/round-49/c1/reads.json for CAND.

Usage: merge-reads.py LANE CAND ROWS_GLOB_DIR [EXTRA_ROWS.json]
For every pointer the frozen C1 extractor finds at CAND (`list_pointers`), the row is taken, in order, from:
  1. a reader row with the same heading, raw, file and ranges whose base_verdict is `holds` (the pointer is unchanged);
  2. a reader row whose proposed_fix names this pointer's file and ranges (`fixed_file`, `fixed_ranges`) and whose
     `skill_new` contains this raw text (the pointer is the correction) — excerpt = `fixed_excerpt`;
  3. a reader row with verdict `absent` for an unresolvable path pointer with the same raw text;
  4. EXTRA_ROWS (the L1's own reads, for pointers the integration introduced; each carries its reader).
Each row keeps the reader seat, the base verdict and the note. The result is checked with the frozen counter's own
check_reads() at CAND and the unmatched/failing pointers are printed; nothing is written when any remain.
"""
import glob
import importlib.util
import json
import os
import sys

LANE, CAND, ROWDIR = os.path.realpath(sys.argv[1]), sys.argv[2], sys.argv[3]
EXTRA = sys.argv[4] if len(sys.argv) > 4 else None
E = '.ufo/evidence/round-49'
spec = importlib.util.spec_from_file_location('c1m', os.path.join(LANE, E, 'c1/measure.py'))
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
cand = c1.git(LANE, 'rev-parse', '--verify', CAND + '^{commit}').stdout.decode().strip()
fleet = os.path.dirname(LANE)
fleet_head = c1.git(fleet, 'rev-parse', 'HEAD').stdout.decode().strip()

src = []
for f in sorted(glob.glob(os.path.join(ROWDIR, '*.rows.json'))):
    for r in json.load(open(f, encoding='utf-8')).get('rows', []):
        r['_from'] = os.path.basename(f)
        src.append(r)
extra = json.load(open(EXTRA, encoding='utf-8')).get('rows', []) if EXTRA else []

pointers, missing = c1.list_pointers(LANE, cand)
if missing:
    sys.exit('missing headings at CAND: %s' % missing)
rows, unmatched = [], []
for p in pointers:
    pick = None
    for r in src:
        if (r.get('heading') == p['heading'] and r.get('raw') == p['raw'] and r.get('file') == p['file']
                and r.get('ranges') == p['ranges'] and r.get('base_verdict') == 'holds'):
            pick = dict(verdict='holds', excerpt=r['excerpt'], reader=r.get('reader'), base_verdict='holds',
                        note=r.get('note', ''), fleet_commit=r.get('fleet_commit'))
            break
    if pick is None:
        for r in src:
            fx = r.get('proposed_fix') or {}
            if (r.get('heading') == p['heading'] and fx.get('fixed_file') == p['file']
                    and fx.get('fixed_ranges') == p['ranges'] and p['raw'] in (fx.get('skill_new') or '')
                    and fx.get('fixed_excerpt')):
                pick = dict(verdict='holds', excerpt=fx['fixed_excerpt'], reader=r.get('reader'),
                            base_verdict=r.get('base_verdict'), note='corrected: ' + fx.get('why', ''),
                            fleet_commit=fx.get('fleet_commit') or r.get('fleet_commit'))
                break
    if pick is None and p['file'] is None and p['pointer_kind'] == 'path':
        for r in src:
            if r.get('heading') == p['heading'] and r.get('raw') == p['raw'] and r.get('base_verdict') == 'absent':
                pick = dict(verdict='absent', excerpt='', reader=r.get('reader'), base_verdict='absent',
                            note=r.get('note', ''))
                break
    if pick is None:
        for r in extra:
            if r.get('heading') == p['heading'] and r.get('raw') == p['raw'] and r.get('file') == p['file'] \
                    and r.get('ranges') == p['ranges']:
                pick = {k: r.get(k) for k in ('verdict', 'excerpt', 'reader', 'base_verdict', 'note', 'fleet_commit')}
                break
    if pick is None:
        unmatched.append(p)
        continue
    row = {'heading': p['heading'], 'ordinal': p['ordinal'], 'raw': p['raw'], 'file': p['file'],
           'ranges': p['ranges']}
    row.update({k: v for k, v in pick.items() if v is not None})
    if p['kind'] in ('external', 'external-path') and not row.get('fleet_commit'):
        row['fleet_commit'] = fleet_head
    rows.append(row)
OVR = os.path.join(LANE, E, 'c1/l1-overrides.json')
if os.path.exists(OVR):  # L1 re-reads after the wave-2 semantic re-reads: re-chosen excerpt and/or note
    ov = json.load(open(OVR, encoding='utf-8'))
    for o in ov['overrides']:
        hit = [r for r in rows if r['heading'] == o['heading'] and r['raw'] == o['raw']]
        if len(hit) != 1:
            sys.exit('override matches %d rows: %s' % (len(hit), o['raw']))
        if o.get('excerpt'):
            hit[0]['excerpt'] = o['excerpt']
            hit[0]['reader'] = '%s; excerpt re-chosen by %s' % (hit[0].get('reader'), ov['reader'])
        hit[0]['note'] = (hit[0].get('note', '') + ' | L1 re-read: ' + o['note']).strip(' |')
doc = {'schema': 'tameshi-r49-reads-v1', 'candidate': cand, 'rows': rows}
res, detail = c1.check_reads(LANE, cand, fleet, pointers, doc)
for p in unmatched:
    print('UNMATCHED %s #%d %s -> %s %s' % (p['heading'][:40], p['ordinal'], p['raw'], p['file'], p['ranges']))
for p, st in detail:
    if st not in ('ok', 'absent'):
        print('CHECK %s #%d %s -> %s' % (p['heading'][:40], p['ordinal'], p['raw'], st))
print('MERGE pointers=%d rows=%d unmatched=%d %s' % (len(pointers), len(rows), len(unmatched), json.dumps(res)))
if unmatched or any(res[k] for k in ('unresolved', 'unverified', 'excerpt_miss', 'not_holds')):
    sys.exit(1)
with open(os.path.join(LANE, E, 'c1/reads.json'), 'w', encoding='utf-8') as fh:
    json.dump(doc, fh, indent=1, ensure_ascii=False)
    fh.write('\n')
print('WROTE %s/c1/reads.json' % E)
