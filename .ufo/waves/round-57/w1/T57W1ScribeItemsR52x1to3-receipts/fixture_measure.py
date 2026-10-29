import importlib.util, json, os, subprocess, sys, hashlib
S = os.environ['S']; FIX = S + '/fix'; W = os.environ['W']
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'; ROUTED = 'c1d49d76be4028df2a68322e7117ff3aafaccd5c'
SPOT = 'corpus/lessons/round-52-verifier-spotcheck.md'
spec = importlib.util.spec_from_file_location('m50', FIX + '/.ufo/evidence/round-50/c1/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows = json.load(open(W + '/rows.json'))
ledger = {'schema': 'tameshi-routed-defects-v1', 'round': 52, 'note': 'R52.1-3 triage fixture',
          'defects': [{k: v for k, v in r.items() if k not in ('keys', 'verdict_basis')} for r in rows]}
open(FIX + '/corpus/routed-defects.json', 'w').write(json.dumps(ledger, indent=1, ensure_ascii=False) + '\n')
os.makedirs(FIX + '/.ufo/fixture', exist_ok=True)
open(FIX + '/SCORECARD.md', 'w').write('x\n\n**Planned (round 57):** R52.3 the Corr12 lesson row.\n')
def g(*a): return subprocess.run(['git', '-C', FIX] + list(a), capture_output=True, text=True, check=True)
g('add', 'corpus/routed-defects.json', 'SCORECARD.md')
g('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-q', '-m', 'fixture: R52.1-3 ledger rows + planned line')
rev = g('rev-parse', 'HEAD').stdout.strip()
sha = hashlib.sha256(subprocess.run(['git', '-C', FIX, 'show', BASE + ':' + SPOT], capture_output=True).stdout).hexdigest()
defects = [{'id': r['id'], 'file': SPOT, 'file_sha256': sha, 'routed_at': ROUTED, 'keys': r['keys']} for r in rows]
notes = []
rev_, counts, stat, total, nrows = m.measure(FIX, rev, defects, True, fixed_floor=0, declined_cap=99,
    explain=lambda *a: notes.append(' '.join(str(x) for x in a)), this_round_floor=0, base=BASE)
print('fixture rev', rev, 'rows', nrows)
print('stat', stat)
print('counts', {k: v for k, v in counts.items() if v})
print('total', total)
for n in notes: print('EXPLAIN', n)
print('planned_ids at fixture rev:', m.planned_ids(FIX, rev))
