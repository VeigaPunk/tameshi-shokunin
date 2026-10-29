import importlib.util, json, os, subprocess, sys, hashlib
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
S = os.environ['S']; W = os.environ['W']; R = os.environ['R']
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
ROUTED = '650987a0d6fc285b37f0f9e63a3aae864af9cd5a'
FIX = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
SPOT = 'corpus/lessons/round-54-verifier-spotcheck.md'
SEAT = 'T57W1ScribeItemsR54x5to7'
spec = importlib.util.spec_from_file_location('m50', LANE + '/.ufo/evidence/round-50/c1/measure.py')
m50 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m50)
rows = [
 {'id': 'R54.5', 'status': 'fixed', 'commit': FIX,
  'evidence': [
    {'path': 'SCORECARD.md', 'lines': '2661-2662',
     'excerpt': '`w1=28 w2=25 sections=12` - 28 findings across 23 wave-1 reader reports, 25 across 12 of the 23 wave-2'},
    {'path': 'corpus/lessons/round-55.md', 'lines': '59-59',
     'excerpt': '| R54.5 | FIXED — `w1=28 w2=25 sections=12`, re-derived from the committed reader files |'}],
  'keys': ['w1=28 w2=25', 'sections=12', 'findings', 'R54.5'],
  'verdict_basis': 'The ER-R54-5 correction at 9cf0146 (added after routed_at 650987a) states w1=28 / w2=25 over 12 sections, which the sweep in receipts re-derives from the 46 committed Read JSONs (28 findings in 23 w1 files; 25 in 12 non-empty w2 files); the pre-correction text "25 wave-1 findings; 22 ... in 9 sections" is absent at 650987a.',
  'note': 'Lane record corrected; the fleet-side report .ufo/reports/round-54/tameshi.md (not a lane file) still reads 25/22. The 26 in the commit subject 99c3bc8 is immutable history and is not named in the correction block.'},
 {'id': 'R54.6', 'status': 'fixed', 'commit': FIX,
  'evidence': [
    {'path': 'SCORECARD.md', 'lines': '2669-2669',
     'excerpt': 'Corrected: they are committed; the sweep that committed them is `ff2a821`.'},
    {'path': 'corpus/lessons/round-55.md', 'lines': '60-60',
     'excerpt': '| R54.6 | FIXED — the three swept deliverables are committed at `ff2a821` |'}],
  'keys': ['ff2a821', 'R54.6', 'swept', 'uncommitted'],
  'verdict_basis': 'The three seat deliverables exist at base and were first added by ff2a821 (which predates routed_at, so it cannot itself be the ledger commit under the round-50 rule); the ledger credits the record correction at 9cf0146, which post-dates routing and introduces the "committed; ... ff2a821" text absent at 650987a.',
  'note': 'The repair itself (the closure durability sweep ff2a821) landed before the spot-check routed R54.6; the rule credits only a later commit, so the credited commit is the SCORECARD/lesson correction. Evidence cites lane records only; the seat files are not spot-check-excluded but carry no key-bearing excerpt that the rule requires.'},
 {'id': 'R54.7', 'status': 'fixed', 'commit': FIX,
  'evidence': [
    {'path': 'SCORECARD.md', 'lines': '2674-2675',
     'excerpt': 'Corrected: the file was **renamed** into `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` at `7fa9a5e`'},
    {'path': 'corpus/lessons/round-55.md', 'lines': '61-61',
     'excerpt': '| R54.7 | FIXED — "renamed into the receipts dir" at `7fa9a5e` |'}],
  'keys': ['renamed', 'forged-reader', '7fa9a5e', 'R54.7'],
  'verdict_basis': 'Base has the old path absent and the new path present; 7fa9a5e is a 100% rename (R100) into receipts/forged-reader.json; the corrected wording "renamed into ... at 7fa9a5e" first appears in the 9cf0146 SCORECARD correction, after routed_at, and the bare "the deletion lands in 7fa9a5e0" wording is no longer in the lane record.',
  'note': 'The fleet report line still says "the deletion lands in 7fa9a5e0" (fleet file, outside lane reach). Non-credit of the forged file was re-checked against the reader pattern and the section_sha256 sweep (see receipts).'},
]
json.dump(rows, open(W + '/rows.json', 'w'), indent=1, ensure_ascii=False)
# ledger doc as the lane would commit it (schema of round-50 rows, without verdict_basis)
doc = {'schema': 'tameshi-routed-defects-v1', 'round': 54, 'note': 'staged candidate rows R54.5-7 (T57W1ScribeItemsR54x5to7)',
       'defects': [{k: v for k, v in r.items() if k not in ('keys', 'verdict_basis')} | {'seat': SEAT} for r in rows]}
spot_sha = hashlib.sha256(subprocess.run(['git', '-C', LANE, 'show', f'{BASE}:{SPOT}'], capture_output=True).stdout).hexdigest()
defects = [{'id': r['id'], 'file': SPOT, 'file_sha256': spot_sha, 'routed_at': ROUTED, 'keys': r['keys']} for r in rows]
# fixture: scratch clone at base, candidate ledger committed there (never in the lane)
clone = S + '/clone'
open(clone + '/corpus/routed-defects.json', 'w').write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid', GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
subprocess.run(['git', '-C', clone, 'add', 'corpus/routed-defects.json'], check=True)
subprocess.run(['git', '-C', clone, 'commit', '-q', '-m', 'fixture ledger R54.5-7'], check=True, env=env)
newrev = subprocess.run(['git', '-C', clone, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
print('fixture rev', newrev, 'toplevel', subprocess.run(['git', '-C', clone, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip())
lines = []
for r in rows:
    for e in r['evidence']:
        why = m50.check_evidence(clone, newrev, e, r['keys'], {SPOT: spot_sha}, {})
        lines.append(f"EVIDENCE {r['id']} {e['path']}:{e['lines']} -> {'resolves' if why is None else 'REFUSED ' + why}")
counts_out = []
rev, counts, stat, total, nrows = m50.measure(clone, newrev, defects, True, 0, 12, explain=lambda *a: counts_out.append(' '.join(map(str, a))), this_round_floor=0, base=None)
lines += counts_out
lines.append('COUNTS ' + json.dumps({k: v for k, v in counts.items() if v}) + ' STAT ' + json.dumps(stat) + f' TOTAL {total} rows={nrows}')
txt = '\n'.join(lines) + '\n'
open(R + '/measure-fixture.txt', 'w').write(txt)
print(txt)
