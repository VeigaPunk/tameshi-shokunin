#!/usr/bin/env python3
"""Build and verify ledger rows R54.8-10 with the round-50 C1 resolver (imported, not copied)."""
import sys, os, json, subprocess, importlib.util, hashlib, shutil
sys.dont_write_bytecode = True
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
RA = '650987a0d6fc285b37f0f9e63a3aae864af9cd5a'      # commit that added the round-54 spot-check (routed_at)
FIX = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'     # round-55 C0: the lane commit that changed the surfaces
SPOT = 'corpus/lessons/round-54-verifier-spotcheck.md'
S = os.environ['S']
OUT = '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeItemsR54x8to10'
STAGE = OUT + '/stage'
SEAT = 'T57W1ScribeItemsR54x8to10'

spec = importlib.util.spec_from_file_location('m50', LANE + '/.ufo/evidence/round-50/c1/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def lines_of(rev, path):
    b = m.show(LANE, rev, path)
    return b.decode('utf-8').split('\n')

def span(rev, path, a, b):
    return m.norm('\n'.join(lines_of(rev, path)[a - 1:b]))

spot_sha = hashlib.sha256(m.show(LANE, BASE, SPOT)).hexdigest()

# ---- base-anchored evidence (open/fixed) -------------------------------------------------
ev = {
 'R54.8': [('corpus/lessons/round-54.md', 98, 98),
           ('.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md', 343, 343)],
 'R54.9': [('corpus/lessons/round-54.md', 51, 52),
           ('SCORECARD.md', 2694, 2696)],
 'R54.10': [('SCORECARD.md', 2700, 2702),
            ('.ufo/evidence/round-54/control/controls-a.stdout', 3, 3)],
}
KEYS = {
 'R54.8': ['round-54.md', 'T54W1ExecStraceNoise.md', 'config.yml', 'm_glm53'],
 'R54.9': ['merge/tameshi', 'w1-registry.json', 'staged=81', 'reviewers=5'],
 'R54.10': ['controls-a.stdout', 'CTL_R53', 'r53-counter-at-88afa941'],
}
ROWS = []
ROWS.append({
  'id': 'R54.8', 'status': 'open',
  'evidence': [{'path': p, 'lines': '%d-%d' % (a, b), 'excerpt': span(BASE, p, a, b)} for p, a, b in ev['R54.8']],
  'keys': KEYS['R54.8'],
  'seat': SEAT,
  'note': ('(a) fixed in the lane: the seat file carries the SUPERSEDED block (round 55, ER-R54-8, commit 9cf0146). '
           '(b) still true at base: corpus/lessons/round-54.md has no config.yml record (its routed section stops at round 53); '
           'the record lives in round-55.md and SCORECARD ER-R54-8. Staged patch appends the correction to round-54.md; '
           'after it lands the row becomes fixed (see after_patch). Under the inherited planned-id rule an open R5x row fails '
           'open_unplanned, because planned_ids matches only R4x ids.'),
  'verdict_basis': ('Still true at base: round-54.md contains no config.yml or host-write record, and the seat file records the '
                    'incident only as a pointer to round-55.md; the part (a) of the item is closed by 9cf0146, part (b) is not.'),
  'after_patch': {
     'status': 'fixed', 'commit': '<full hash of the commit that lands the staged round-54.md patch>',
     'evidence_path': 'corpus/lessons/round-54.md', 'excerpt': '- **R54.8** — the `~/.omp/agent/config.yml` write is recorded in this lesson:',
     'note': 'L1 fills commit with the content commit; verified by fixture B2 in the report'},
})
ROWS.append({
  'id': 'R54.9', 'status': 'fixed', 'commit': FIX,
  'evidence': [{'path': p, 'lines': '%d-%d' % (a, b), 'excerpt': span(BASE, p, a, b)} for p, a, b in ev['R54.9']],
  'keys': KEYS['R54.9'], 'seat': SEAT,
  'note': ('Lesson line 51 said "the other 84 staged"; 9cf0146 corrects it to 80 (81 staged .md minus the refused delta-debugging entry). '
           'SCORECARD ER-R54-9 records the derived numbers from w1-registry.json and the package count. The fleet report '
           '(.ufo/reports/round-54/tameshi.md, outside the lane) still prints 4 reviewers and 26.3 %; not a lane-tree surface.'),
  'verdict_basis': ('Fixed by 9cf0146: the 84 excerpt is gone from lesson line 51 and the corrected numbers are present in SCORECARD; '
                    'excerpt absent at routed_at 650987a.'),
})
ROWS.append({
  'id': 'R54.10', 'status': 'fixed', 'commit': FIX,
  'evidence': [{'path': p, 'lines': '%d-%d' % (a, b), 'excerpt': span(BASE, p, a, b)} for p, a, b in ev['R54.10']],
  'keys': KEYS['R54.10'], 'seat': SEAT,
  'note': ('The lane never carried the misquote in a lane file (no lane file at routed_at pairs CTL_R53 with controls-a); the misquote '
           'is in the fleet report only. 9cf0146 adds ER-R54-10 to SCORECARD naming the correct pairing: controls-a.stdout prints rekeyed=0/7, '
           '0/30 belongs to r53-counter-at-88afa941.stdout. Fleet report copy untouched by the lane.'),
  'verdict_basis': ('The lane record states the correct receipt pairing from 9cf0146 on; the excerpt is absent at routed_at and the receipt line '
                    'controls-a.stdout:3 prints rekeyed=0/7 at base. Judgement call: the fleet report copy persists.'),
})

# ---- staged patch for R54.8(b) --------------------------------------------------------
base_lines = lines_of(BASE, 'corpus/lessons/round-54.md')
if base_lines and base_lines[-1] == '':
    base_lines = base_lines[:-1]
block = [
 '',
 '## Round-54 routed defects — corrections (round 55)',
 '',
 '- **R54.8** — the `~/.omp/agent/config.yml` write is recorded in this lesson:',
 '  seat `T54W1ExecStraceNoise` changed `scout` from `@m_grok` to `@m_glm53` outside',
 '  its write scope, and the change was reverted. The report\'s word *fabricated* is',
 '  withdrawn. The full record is `corpus/lessons/round-55.md` (R54.8 row) and SCORECARD',
 '  `ER-R54-8`; the seat file is marked superseded.',
]
patched_lines = base_lines + block
patched_text = '\n'.join(patched_lines) + '\n'
first_block_line = len(base_lines) + 4   # line of the "- **R54.8**" bullet (1-based)
ROWS[0]['after_patch']['lines'] = '%d-%d' % (first_block_line, first_block_line)

json.dump({'patched_round54_lesson': patched_text}, open(S + '/patched.json', 'w'))
open(S + '/round-54.base.md', 'wb').write(m.show(LANE, BASE, 'corpus/lessons/round-54.md'))
open(S + '/round-54.patched.md', 'w', encoding='utf-8').write(patched_text)

# ---- fixtures ----------------------------------------------------------------------------
clone = S + '/clone'
if os.path.exists(clone):
    shutil.rmtree(clone)
subprocess.run(['git', 'clone', '-q', '--shared', LANE, clone], check=True)
top = subprocess.run(['git', '-C', clone, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
assert top == clone, top
def git(*a, check=True):
    return subprocess.run(['git', '-C', clone] + list(a), capture_output=True, check=check)
IDENT = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid']
git('checkout', '-q', '--detach', BASE)
ledger_rows = [dict((k, v) for k, v in r.items() if k in ('id', 'status', 'evidence', 'commit', 'reason', 'seat', 'note')) for r in ROWS]
def write_ledger(rows):
    open(clone + '/corpus/routed-defects.json', 'w', encoding='utf-8').write(json.dumps({'schema': 'tameshi-routed-defects-v1', 'round': 57, 'defects': rows}, indent=1, ensure_ascii=False) + '\n')

# fixture A: base + ledger rows (R54.8 open)
write_ledger(ledger_rows)
git('add', 'corpus/routed-defects.json')
subprocess.run(['git', '-C', clone] + IDENT + ['commit', '-q', '-m', 'fixture A: ledger rows R54.8-10'], check=True)
REV_A = git('rev-parse', 'HEAD').stdout.decode().strip()
# fixture B1: base + staged lesson patch
git('checkout', '-q', '--detach', BASE)
open(clone + '/corpus/lessons/round-54.md', 'w', encoding='utf-8').write(patched_text)
git('add', 'corpus/lessons/round-54.md')
subprocess.run(['git', '-C', clone] + IDENT + ['commit', '-q', '-m', 'fixture B1: round-54 lesson correction'], check=True)
REV_B1 = git('rev-parse', 'HEAD').stdout.decode().strip()
# fixture B2: B1 + ledger with R54.8 fixed at B1
rowsB = json.loads(json.dumps(ledger_rows))
rowsB[0] = {'id': 'R54.8', 'status': 'fixed', 'commit': REV_B1,
            'evidence': [{'path': 'corpus/lessons/round-54.md', 'lines': ROWS[0]['after_patch']['lines'],
                          'excerpt': ROWS[0]['after_patch']['excerpt']}],
            'seat': SEAT, 'note': 'post-patch template verified by fixture B2'}
write_ledger(rowsB)
git('add', 'corpus/routed-defects.json')
subprocess.run(['git', '-C', clone] + IDENT + ['commit', '-q', '-m', 'fixture B2: ledger'], check=True)
REV_B2 = git('rev-parse', 'HEAD').stdout.decode().strip()

def defect(i):
    return {'id': i, 'round': 54, 'file': SPOT, 'line': 0, 'end': 0, 'routed_at': RA,
            'file_sha256': spot_sha, 'keys': KEYS[i], 'text': ''}

results = {}
def run(rev, label, patch_planned=False):
    out = {}
    orig = m.planned_ids
    if patch_planned:
        m.planned_ids = lambda lane, rev_: {'R54.8'}
    try:
        for i in ('R54.8', 'R54.9', 'R54.10'):
            notes = []
            _, counts, stat, total, nrows = m.measure(clone, rev, [defect(i)], True, fixed_floor=0, declined_cap=99,
                                                       explain=lambda *a: notes.append(' '.join(str(x) for x in a)),
                                                       this_round_floor=0, base=BASE)
            real = total - counts['extra']
            out[i] = {'total': real, 'stat': stat, 'bad_terms': {k: v for k, v in counts.items() if v and k != 'extra'}, 'notes': notes}
    finally:
        m.planned_ids = orig
    results[label] = out
    return out

run(REV_A, 'A_base_ledger_stock_planned_rule')
run(REV_A, 'A_base_ledger_planned_R54.8_named', patch_planned=True)
run(REV_B2, 'B2_patch_landed_stock_rule')
print(json.dumps({'REV_A': REV_A, 'REV_B1': REV_B1, 'REV_B2': REV_B2, 'results': results}, indent=1, ensure_ascii=False))

# per-evidence resolver check at base (what the counter's check_evidence says for each item)
cache = {}
for r in ROWS:
    for e in r['evidence']:
        why = m.check_evidence(clone, REV_A, e, r['keys'], {SPOT: spot_sha}, cache)
        print('CHECK_EVIDENCE', r['id'], e['path'], e['lines'], 'ok' if why is None else why)
json.dump({'rows': ROWS, 'fixture': {'REV_A': REV_A, 'REV_B1': REV_B1, 'REV_B2': REV_B2}, 'results': results,
           'patched_block_lines': block}, open(S + '/build-out.json', 'w'), indent=1, ensure_ascii=False)
