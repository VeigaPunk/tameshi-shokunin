"""Negative controls and routed-absence check for the R50.1-4 rows (reads git objects only)."""
import json
import sys

sys.argv = sys.argv[:1]
import importlib.util

sys.dont_write_bytecode = True
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
ROUTED = '9962033fd7a75aa2f2847e979dd687a5d28505a1'
STAGED57 = LANE + '/.ufo/waves/round-57/w1/T57W1ExecC1Counter/stage/.ufo/evidence/round-57/c1/measure.py'
MEASURE50 = LANE + '/.ufo/evidence/round-50/c1/measure.py'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m50 = load('m50', MEASURE50)
m57 = load('m57', STAGED57)
rows = json.load(open(LANE + '/.ufo/waves/round-57/w1/T57W1ScribeItemsR50x1to4/rows.json', encoding='utf-8'))
byid = {r['id']: r for r in rows}

print('== A. every evidence excerpt absent at routing commit', ROUTED[:12])
for rid in sorted(byid):
    if byid[rid]['status'] != 'fixed':
        continue
    for e in byid[rid]['evidence']:
        then = m50.show(LANE, ROUTED, e['path'])
        present = then is not None and m50.norm(e['excerpt']) in m50.norm(then.decode('utf-8', 'replace'))
        print('ABSENT_AT_ROUTED', rid, e['path'], 'present=%s' % present)


def judge(rid, row_patch=None, keys=None, planned=frozenset()):
    row = {k: v for k, v in byid[rid].items() if k in ('id', 'status', 'evidence', 'commit', 'reason')}
    if row_patch:
        row.update(row_patch)
    d = {'id': rid, 'keys': keys or byid[rid]['keys'], 'routed_at': ROUTED, 'file': 'corpus/lessons/round-50-verifier-spotcheck.md'}
    stat = {'fixed': 0, 'open': 0, 'declined': 0, 'fixed_this_round': 0}
    notes = []
    cache = {}
    spot = {}
    fault = m57.judge(LANE, BASE, d, row, set(planned), cache, spot, BASE, stat, lambda *a: notes.append(a))
    return fault, notes


print('== B. negative controls (each must be refused)')
controls = [
    ('N1 fix commit equals routing commit', judge('R50.1', {'commit': ROUTED}), 'fixed_bad'),
    ('N2 excerpt already present at routing', judge('R50.1', {'evidence': [{'path': 'corpus/SOURCES.md', 'lines': '33-33',
                                                                             'excerpt': 'corpus/knowledge/fixture-shrinking-pilot.md'}]}), 'fixed_bad'),
    ('N3 wrong keys', judge('R50.3', keys=['zzz-no-such-key']), 'key_miss'),
    ('N4 open without planned naming', judge('R50.4'), 'open_unplanned'),
    ('N5 open with planned naming', judge('R50.4', planned={'R50.4'}), None),
    ('N6 short decline reason is not used', judge('R50.2', {'status': 'declined', 'reason': 'short'}), 'declined_bad'),
    ('N7 R50.2 fix commit not touching SKILL', judge('R50.2', {'commit': '5e3569969b532310d2b8a3d130901757a3df356b'}), 'fixed_bad'),
]
ok = True
for name, (fault, notes), want in controls:
    good = fault == want
    ok = ok and good
    print('CTL %-42s fault=%-16s want=%-16s %s %s' % (name, fault, want, 'ok' if good else 'MISMATCH', notes[:2]))
print('CONTROLS_OK' if ok else 'CONTROLS_FAIL')
sys.exit(0 if ok else 1)
