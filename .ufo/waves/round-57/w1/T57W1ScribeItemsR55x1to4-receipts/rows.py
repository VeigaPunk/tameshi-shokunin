import sys, json, hashlib, subprocess, os
sys.dont_write_bytecode = True
import importlib.util
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '5e3569969b532310d2b8a3d130901757a3df356b'
ROUTED = 'fa48c06c3669355fd80e8722eb733c1d6dfdd2f8'
SPOT = 'corpus/lessons/round-55-verifier-spotcheck.md'
SEAT = 'T57W1ScribeItemsR55x1to4'
OUT_DIR = LANE + '/.ufo/waves/round-57/w1/T57W1ScribeItemsR55x1to4'
os.makedirs(OUT_DIR, exist_ok=True)

def git(*a):
    return subprocess.run(['git', '-C', LANE] + list(a), capture_output=True, check=True).stdout

def show(rev, path):
    return git('show', '%s:%s' % (rev, path))

def norm(t):
    return ' '.join(t.split())

def locate(rev, path, excerpt):
    lines = show(rev, path).decode('utf-8', 'replace').split('\n')
    ex = norm(excerpt)
    for span in (1, 2, 3):
        for a in range(1, len(lines) - span + 2):
            b = a + span - 1
            if ex in norm('\n'.join(lines[a - 1:b])):
                return '%d-%d' % (a, b)
    raise SystemExit('LOCATE-FAIL %s %r' % (path, excerpt[:60]))

ROWS = [
 dict(id='R55.1', status='fixed', commit='c3e2ca9f020776b3d66c7af854fb82c834674fcf',
      keys=['gate 0c', '--certified', 'receipt-gate-verdicts', 'deciding-run.sh', 'RECEIPT_REV_ABSENT'],
      ev=[('.ufo/evidence/round-56/deciding-run.sh', 'gate 0c: the verdicts this run just produced must name the certified revision.'),
          ('.ufo/evidence/round-56/after/receipt-gate-verdicts.stdout', 'GATE: receipts=2 ok=2 refused=0 codes=none verdict=PASS'),
          ('.ufo/evidence/round-56/before/c2.stdout', 'EXPLAIN arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT')],
      verdict_basis='Gate 0c (deciding-run.sh, added by freeze commit c3e2ca9f, which is not an ancestor of the spot-check fa48c06) runs receipt-revision-gate.py --certified on the verdict receipts the run produces, so a verdict that does not name the certified revision is refused; the gate refuses the round-55 truncated c2 receipt (RECEIPT_REV_ABSENT) and passes the round-56 verdicts at 1b44bace0974. Matches the round-56 lesson disposition FIXED.',
      note='Fix landed in round 56 (not this round); counts toward FIXED_FLOOR only, not the this-round floor. Caveat from wave-1 review: the verdict receipts are produced in the working tree, so committing them is an unenforced step.'),
 dict(id='R55.2', status='open',
      keys=['c2-integrated.out', 'total=1', 'T56W3ScribeRecords.md', 'total=6', 'R55.2'],
      ev=[('.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out', 'total=1 C2_R55_PASS=false'),
          ('.ufo/waves/round-56/w3/T56W3ScribeRecords.md', 'both quote **`total=6`** and cite `before/c2.stdout`')],
      verdict_basis='The committed receipt c2-integrated.out:44 still reads total=1 C2_R55_PASS=false, and the round-56 wave-3 record (T56W3ScribeRecords.md:30, V13) shows the same class recurring (a quoted total=6 against before/c2.stdout total=2). No lane instrument checks quoted bytes; round-56 lesson disposition CARRIED. Still true at base.',
      note='Carried. Needs a checker that compares quoted totals to the receipt line they name; no such instrument exists. The report that quoted total=0 is fleet-side (.ufo/reports/round-55/tameshi.md), outside lane evidence.'),
 dict(id='R55.3', status='fixed', commit='2f5512a8ab0771fb2eee463ec16db359174f5edd',
      keys=['calibration', 'c1dd23b', 'box3=true', 'R55.3', 'monitor=8/64'],
      ev=[('SCORECARD.md', 'calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; two points per restrained, evidence-linked `[~]` SHONEN box, with box 3 requiring the full page: `64/64`, `box3=true`')],
      verdict_basis='SCORECARD.md at base carries the restated standing calibration row (score 8, measured commit c1dd23b, last change round 56), added by 2f5512a, which is not an ancestor of the spot-check fa48c06. The 18 lost cold-read headings were re-keyed at C0 (round-56 lesson R55.3 FIXED); the round-21 monitor reading at base is verified separately in receipts (see report).',
      note='Fix landed in round 56 (not this round). The row is restated to the score the monitor reads at the commit the row names; the fix is verified only as far as the base monitor run goes.'),
 dict(id='R55.4', status='open',
      keys=['R55.4', 'still running at filing', 'T56W3ScribeRecords.md', 'T56W1RevRound55Dispositions.md'],
      ev=[('.ufo/waves/round-56/w3/T56W3ScribeRecords.md', 'R55.4 — stale control sentence ("still running at filing") | **carried**'),
          ('.ufo/waves/round-56/w1/T56W1RevRound55Dispositions.md', 'Correct disposition is `carried`')],
      verdict_basis='The round-56 wave-1 review (T56W1RevRound55Dispositions.md:12, F2) found the lesson claim FIXED by construction overclaimed: deciding-run.sh checks receipt existence and verdict-line presence, never report prose against a receipt; the round-56 wave-3 record (T56W3ScribeRecords.md:148) disposes R55.4 as carried. The round-55 sentence itself sits in the fleet-side report (.ufo/reports/round-55/tameshi.md:93), still unchanged. Still true at base.',
      note='Carried, not fixed. The lesson corpus/lessons/round-56.md row still says FIXED by construction and contradicts the wave-3 record; the L1 must align them. A fix needs a falsifier that reads status claims against receipts (new counter arm and a QUALITY criterion), not a patch.'),
]

m = None
spec = importlib.util.spec_from_file_location('r50c1', LANE + '/.ufo/evidence/round-50/c1/measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

spot_sha = hashlib.sha256(show(ROUTED, SPOT)).hexdigest()
rows_out = []
defects = []
for r in ROWS:
    row = {'id': r['id'], 'status': r['status']}
    ev = []
    for path, exc in r['ev']:
        p = path
        if p == 'SCORECARD.md':
            pass
        lines = locate(REV, p, exc)
        ev.append({'path': p, 'lines': lines, 'excerpt': exc})
    row['evidence'] = ev
    if 'commit' in r: row['commit'] = r['commit']
    if 'reason' in r: row['reason'] = r['reason']
    row['seat'] = SEAT
    row['note'] = r['note']
    rows_out.append(dict(row, keys=r['keys'], verdict_basis=r['verdict_basis']))
    defects.append({'id': r['id'], 'file': SPOT, 'file_sha256': spot_sha, 'routed_at': ROUTED, 'keys': r['keys']})

ledger = {'schema': 'tameshi-routed-defects-v1', 'round': 50, 'defects': [{k: v for k, v in x.items() if k not in ('keys', 'verdict_basis')} for x in rows_out]}
json.dump(rows_out, open(OUT_DIR + '/rows.json', 'w'), indent=2, ensure_ascii=False)
json.dump(ledger, open(os.environ['HYAKU_SCRATCH'] + '/tameshi-r57/T57W1ScribeItemsR55x1to4/ledger-candidate.json', 'w'), indent=2, ensure_ascii=False)
print('rows written', len(rows_out))
