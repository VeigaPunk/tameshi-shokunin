#!/usr/bin/env python3
"""Build corpus/routed-defects.json for round 57: the 49 base rows byte-identical + 51 new rows.
Usage: build-ledger.py LANE C0 [FREEZE_COMMIT]   (reads wave-1 rows; fixed-this-round overrides below)
Evidence line numbers are found by locating a needle in the file at the working tree (== the commit that carries it)."""
import glob, json, os, subprocess, sys
LANE, C0 = sys.argv[1], sys.argv[2]
FREEZE = sys.argv[3] if len(sys.argv) > 3 else None
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
W = os.path.join(LANE, '.ufo/waves/round-57/w1')
base = json.loads(subprocess.run(['git', '-C', LANE, 'show', BASE + ':corpus/routed-defects.json'], capture_output=True, check=True).stdout)
rows = {}
for f in sorted(glob.glob(W + '/T57W1ScribeItems*/rows.json')):
    for r in json.load(open(f)):
        r = dict(r)
        r.pop('verdict_basis', None); r.pop('keys', None)
        r['status_at_base'] = r['status']
        rows[r['id']] = r

def ev(path, needle, span=1):
    lines = open(os.path.join(LANE, path), encoding='utf-8').read().split('\n')
    hits = [i for i, l in enumerate(lines) if needle in l]
    assert len(hits) >= 1, (path, needle)
    i = hits[0]
    return {'path': path, 'lines': '%d-%d' % (i + 1, i + span), 'excerpt': ' '.join(' '.join(lines[i:i + span]).split())[:400]}

L = 'corpus/lessons/round-57.md'
fixes = {
 'R53.8': (C0, [ev(L, 'S275 quote "22 words"', 2)], 'corrected word counts (20 and 20) appended as a round-57 correction; round-53 lesson untouched'),
 'R55.2': (C0, [ev(L, 'c2-integrated.out', 1), ev(L, 'total=1 C2_R55_PASS=false', 1)], 'superseding record names the receipt line the report mis-quoted; report is fleet-side'),
 'R56.2': (C0, [ev('SKILL.md', 'a verdict receipt names another revision (a positive receipt gates identically)')], 'SKILL standing-rules cell now equals the code the gate emits on a --paths drift fixture (C2 standing_cell arm)'),
 'R56.3': (C0, [ev('corpus/knowledge/receipt-revision-binding.md', 'ER-R57-K1'), ev('corpus/README.md', 'knowledge/receipt-revision-binding.md` (round 56; errata ER-R57-K1')], 'errata names the 19/19 recheck; README coverage-map row indexes the entry'),
 'R56.4': (C0, [ev('.ufo/evidence/round-57/coldread-referent-r56.md', '- Referent: commit')], 'referent of the 13/6 mismatching external_inputs labels recorded (commit 877eede between C0 and the bind); labels not re-bound'),
 'R56.6': (C0, [ev('tools/registry.json', '"receipt-gate-unresolvable-certified"'), ev('SKILL.md', '| receipt-revision gate | gate |')], 'three executed gate rows (exits 0, 3, 2) and a SKILL gate/probe registry row with the 0/2/3 map'),
 'R56.7': (C0, [ev(L, 'R56.7 — "no byte changed after C0/PIN"')], 'phrasing corrected by a superseding record; round-56 lesson untouched'),
}
if FREEZE:
    fixes['R56.5'] = (FREEZE, [ev('.ufo/evidence/round-57/controls.sh', 'ONE GENERATION. Controls are RECOMPUTED, never READ')], 'controls.sh header pre-registers one generation and states controls are recomputed, never read; C2 kill_rule in the contract')
for rid, (commit, evidence, note) in fixes.items():
    r = rows[rid]
    r['status'] = 'fixed'; r['commit'] = commit; r['evidence'] = evidence; r['note'] = note
    r['seat'] = 'TameshiR57'; r.pop('reason', None)
d = {'schema': base['schema'], 'round': 57, 'note': base['note'] + '; round 57 appended the rows of the round-50..56 closures (status_at_base = the status judged against the tree at the round base)', 'defects': base['defects'] + [rows[k] for k in sorted(rows, key=lambda s: (int(s[1:3]), int(s.split('.')[1])))]}
with open(os.path.join(LANE, 'corpus/routed-defects.json'), 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(d, indent=1, ensure_ascii=False) + '\n')
print('rows', len(d['defects']), {s: sum(1 for r in d['defects'][49:] if r['status'] == s) for s in ('fixed', 'open', 'declined')})
