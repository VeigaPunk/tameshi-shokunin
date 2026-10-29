#!/usr/bin/env python3
"""Verify R53.7-9 ledger rows against the lane at base, reusing the round-50 counter's resolver by import."""
import importlib.util
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '5e3569969b532310d2b8a3d130901757a3df356b'
M50 = LANE + '/.ufo/evidence/round-50/c1/measure.py'
WAVE = LANE + '/.ufo/waves/round-57/w1/T57W1ScribeItemsR53x7to9'
SEAT = 'T57W1ScribeItemsR53x7to9'
ROWS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rows-spec.py')

spec = importlib.util.spec_from_file_location('m50', M50)
m50 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m50)

rows_ns = {}
exec(open(ROWS, encoding='utf-8').read(), rows_ns)
ROWS_SPEC = rows_ns['ROWS']

SPOT = {'corpus/lessons/round-%d-verifier-spotcheck.md' % r for r in range(40, 57)}
cache = {}
ok_all = True


def git(*a):
    return subprocess.run(['git', '-C', LANE] + list(a), capture_output=True, check=False)


routed_at = git('log', '--diff-filter=A', '--format=%H', REV, '--',
                'corpus/lessons/round-53-verifier-spotcheck.md').stdout.decode().split()[-1]
print('routed_at', routed_at)
planned = m50.planned_ids(LANE, REV)
print('planned_ids at base (round-50 rule):', sorted(planned))

for row in ROWS_SPEC:
    rid = row['id']
    errs = []
    if not (1 <= len(row['keys']) <= 5):
        errs.append('keys count')
    keyed = []
    for ev in row['evidence']:
        why = m50.check_evidence(LANE, REV, ev, row['keys'], SPOT, cache)
        if why:
            errs.append('evidence %s: %s' % (ev['path'], why))
            continue
        if m50.has_key(ev, row['keys']):
            keyed.append(ev)
    if not keyed:
        errs.append('no keyed evidence')
    if row['status'] == 'fixed':
        c = row['commit']
        full = git('rev-parse', '--verify', c + '^{commit}').stdout.decode().strip()
        if full != c or not m50.HEX40.match(c):
            errs.append('commit not full hex: %s' % c)
        if not m50.is_ancestor(LANE, c, REV):
            errs.append('commit not ancestor of base')
        if m50.is_ancestor(LANE, c, routed_at):
            errs.append('commit ancestor of routed_at')
        files = m50.touched(LANE, c)
        fresh = False
        for ev in keyed:
            if ev['path'] not in files:
                continue
            then = m50.show(LANE, routed_at, ev["path"])
            if then is not None and m50.norm(ev['excerpt']) in m50.norm(then.decode('utf-8', 'replace')):
                continue
            a, b = (int(x) for x in ev['lines'].split('-'))
            span = ' '.join(cache[(REV, ev['path'])][a - 1:b]).lower()
            if any(w in span for w in m50.ACK_WORDS):
                continue
            fresh = True
            print('  fresh via', ev['path'], ev['lines'])
            break
        if not fresh:
            errs.append('fixed-not-new')
    elif row['status'] == 'open':
        if rid not in planned:
            print('  NOTE open row not yet in newest Planned paragraph (L1 must plant it)')
    else:
        errs.append('status')
    verdict = 'PASS' if not errs else 'FAIL'
    ok_all = ok_all and not errs
    print(rid, row['status'], verdict, errs)

print('ALL_ROWS_PASS' if ok_all else 'ROWS_FAIL')
if ok_all and '--write' in sys.argv:
    out = []
    for row in ROWS_SPEC:
        r = {'id': row['id'], 'status': row['status'], 'evidence': row['evidence'], 'keys': row['keys'],
             'seat': SEAT, 'note': row['note'], 'verdict_basis': row['verdict_basis']}
        if row['status'] == 'fixed':
            r['commit'] = row['commit']
        out.append(r)
    os.makedirs(WAVE, exist_ok=True)
    with open(os.path.join(WAVE, 'rows.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print('wrote', os.path.join(WAVE, 'rows.json'))
sys.exit(0 if ok_all else 1)
