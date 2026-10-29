#!/usr/bin/env python3
"""Build and verify ledger rows R50.1-4 against the lane tree at base (no lane writes; no bytecode)."""
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
ROUTED = '9962033fd7a75aa2f2847e979dd687a5d28505a1'
SPOT = 'corpus/lessons/round-50-verifier-spotcheck.md'
EXPECTED_SPOTS = ['corpus/lessons/round-%d-verifier-spotcheck.md' % r for r in range(50, 57)]
STAGED57 = LANE + '/.ufo/waves/round-57/w1/T57W1ExecC1Counter/stage/.ufo/evidence/round-57/c1/measure.py'
EXTRACT50 = LANE + '/.ufo/evidence/round-50/c1/extract-defects.py'
MEASURE50 = LANE + '/.ufo/evidence/round-50/c1/measure.py'
COMMIT_FIX = '6d8c11e378aa90b12650808e1b79270742935f15'
OUT = LANE + '/.ufo/waves/round-57/w1/T57W1ScribeItemsR50x1to4/rows.json'
SEAT = 'T57W1ScribeItemsR50x1to4'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m50 = load('m50', MEASURE50)
m57 = load('m57', STAGED57)
ex50 = load('ex50', EXTRACT50)


def text_of(path, rev=BASE):
    return m50.show(LANE, rev, path).decode('utf-8', 'replace')


def line_of(path, needle):
    hits = [i + 1 for i, ln in enumerate(text_of(path).split('\n')) if m50.norm(needle) in m50.norm(ln)]
    assert len(hits) == 1, (path, needle[:60], hits)
    return hits[0]


def ev(path, needle):
    n = line_of(path, needle)
    return {'path': path, 'lines': '%d-%d' % (n, n), 'excerpt': needle}


spot_blob = m50.show(LANE, BASE, SPOT)
items = ex50.items_of(spot_blob.decode('utf-8'))
assert len(items) == 4, len(items)
for i, it in enumerate(items, 1):
    print('ITEM R50.%d line %d: %s' % (i, it['line'], it['text'][:110]))

spotchecks = {}
for p in [SPOT] + EXPECTED_SPOTS:
    if p not in spotchecks:
        spotchecks[p] = hashlib.sha256(m50.show(LANE, BASE, p)).hexdigest()
spotchecks = {p: spotchecks[p] for p in EXPECTED_SPOTS}  # SPOT is round-50, included in EXPECTED_SPOTS

ROWS = {
    'R50.1': {
        'status': 'fixed',
        'keys': ['S022', 'fixture-shrinking-pilot.md', 'mined'],
        'commit': COMMIT_FIX,
        'evidence': [
            ev('corpus/SOURCES.md', '| mined | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |'),
            ev('corpus/lessons/round-51.md', 'Rows touched: S022 status `queued` → `mined`'),
        ],
        'verdict_basis': ('The routed contradiction (S022 status queued while used-by names an existing entry) no longer holds at base: '
                          'corpus/SOURCES.md:33 reads mined with used-by corpus/knowledge/fixture-shrinking-pilot.md, '
                          'and the excerpt is absent at the routing commit 9962033 (that row read queued). '
                          'The status change came in 6d8c11e, round-51 integration; corpus/lessons/round-51.md logs old -> new.'),
        'note': ('Fixed before base (6d8c11e is an ancestor of 5e35699), so it does not count toward a this-round fix floor. '
                 'The spot-check also asked to re-base or record the round-45 freshness monitor exception; this seat did not verify that part.'),
    },
    'R50.2': {
        'status': 'fixed',
        'keys': ['shrink-case', 'pbt-staged-id', 'Gate/probe registry'],
        'commit': COMMIT_FIX,
        'evidence': [
            ev('SKILL.md', '| shrink-case | probe | `python3 tools/shrink-case.py --pristine PRISTINE.py --mutant MUTANT.py --case CASE.json --out OUT.json`'),
            ev('SKILL.md', '| pbt staged-id generator | gate | `python3 tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 1 --cases 400 --dump OUT.jsonl`'),
        ],
        'verdict_basis': ('The routed defect (no registry row for tools/shrink-case.py or tools/pbt-staged-id.py) no longer holds: '
                          'the round-51 registry block "#### Gate/probe registry — round 51" at SKILL.md:2181 carries one row per tool with '
                          'kind, entry command, verdict map (exit 2 included), selftest spelling, pinned values and write scope. '
                          'Neither row text is present at routing commit 9962033; both were added in 6d8c11e.'),
        'note': ('Residual, disclosed not fixed: the round-12 block scope sentence at SKILL.md:1548 still reads '
                 '"Registry scope is these round-12 instruments". The lane registers later instruments in per-round blocks, so the sentence '
                 'is accurate for the block it sits in; rewriting it is a costly SKILL.md edit (see report). Pre-round-51 registry-home '
                 'corrections are not this seat\'s scope.'),
    },
    'R50.3': {
        'status': 'fixed',
        'keys': ['F6', 'F10', 'README.md:608', 'README.md:599'],
        'commit': COMMIT_FIX,
        'evidence': [
            ev('corpus/README.md', '| F6 | fixture minimization for survivors | S022, S023, S024, S271 | held (round 50) — README.md:608'),
            ev('corpus/README.md', '| F10 | PBT generators for gate fixtures | S018, S019, S020, S021, S269, S270 | held (round 49) — README.md:599'),
        ],
        'verdict_basis': ('The routed defect (table at corpus/README.md:83 and :87 still reads open while the sections at :599 and :608 declare held) '
                          'is answered by a superseding table appended in 6d8c11e: corpus/README.md:621 and :625 state F6 held (round 50) and '
                          'F10 held (round 49), and the round-51 text says the table at :76-87 is superseded as a whole. '
                          'Neither superseding row is present at routing commit 9962033.'),
        'note': ('The original table cells at README:83 and :87 still say open; the spot-check accepted a superseding table or note as the fix. '
                 'Rewriting those cells would be a costly README edit (every README-pinned cold-read entry loses credit), so it is not proposed.'),
    },
    'R50.4': {
        'status': 'open',
        'keys': ['Planned (round 51)', 'forgery routes', 'successor C1/C2', 'R45.1'],
        'evidence': [
            ev('SCORECARD.md', '**Planned (round 51):** the seven routed items the round-50 ledger leaves open'),
            ev('SCORECARD.md', 'successor C1/C2 counters that close the forgery routes disclosed in round 50'),
            ev('corpus/lessons/round-50.md', 'both round-50 frozen counters admit forgeries a mechanical check cannot see'),
        ],
        'verdict_basis': ('Still true at base. The seven open rows (R45.1, R45.4, R46.2, R47.5, R48.4, R49.3, R49.5) remain status open in the base ledger, '
                          'and no lesson 51-56 or SCORECARD section at base records any of them closed (receipts grep). The successor C1/C2 '
                          'counters for the forgery routes named in the round-51 plan are not present at base (ls-tree receipt). '
                          'Status open requires the id in the newest "**Planned (round" paragraph at REV: the L1 must name R50.4 there.'),
        'note': ('Carry-forward pointer, not a separable defect: its substance is the seven open rows plus the successor counters, '
                 'which keep their own rows and work. Not fixable in this seat.'),
    },
}


def run(rows_by_id, planned):
    results = {}
    cache = {}
    for i, it in enumerate(items, 1):
        rid = 'R50.%d' % i
        spec = rows_by_id[rid]
        d = {'id': rid, 'keys': spec['keys'], 'routed_at': ROUTED, 'file': SPOT}
        row = {'id': rid, 'status': spec['status'], 'evidence': spec['evidence']}
        if 'commit' in spec:
            row['commit'] = spec['commit']
        if 'reason' in spec:
            row['reason'] = spec['reason']
        stat = {'fixed': 0, 'open': 0, 'declined': 0, 'fixed_this_round': 0}
        notes = []
        note = lambda *a: notes.append(' '.join(str(x) for x in a))
        fault = m57.judge(LANE, BASE, d, row, planned, cache, spotchecks, BASE, stat, note)
        results[rid] = {'fault': fault, 'notes': notes, 'stat': stat}
    return results


res = run(ROWS, {'R50.4'})
for rid in sorted(res):
    print('JUDGE(planned=R50.4)', rid, 'fault=%s' % res[rid]['fault'], res[rid]['notes'], res[rid]['stat'])
res_unplanned = run(ROWS, set())
print('JUDGE(planned=none) R50.4 fault=%s' % res_unplanned['R50.4']['fault'])

# every excerpt resolves via the round-50 resolver (the counter's own check_evidence)
for rid, spec in ROWS.items():
    for e in spec['evidence']:
        why = m50.check_evidence(LANE, BASE, e, spec['keys'], spotchecks, {})
        print('EXCERPT', rid, e['path'], e['lines'], 'ok' if why is None else why)

if any(res[r]['fault'] for r in res if r != 'R50.4') or res['R50.4']['fault'] not in (None, 'open_unplanned'):
    print('VERIFY_FAIL')
    sys.exit(1)

out = []
for i, it in enumerate(items, 1):
    rid = 'R50.%d' % i
    spec = ROWS[rid]
    row = {'id': rid, 'status': spec['status'], 'evidence': spec['evidence']}
    if 'commit' in spec:
        row['commit'] = spec['commit']
    row['seat'] = SEAT
    row['note'] = spec['note']
    row['keys'] = spec['keys']
    row['verdict_basis'] = spec['verdict_basis']
    out.append(row)
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
    fh.write('\n')
print('WROTE', OUT, len(out))
