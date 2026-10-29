import importlib.util, json, sys, hashlib, subprocess
S, C, B, R, ROWS = sys.argv[1:6]
spec = importlib.util.spec_from_file_location('m50', C + '/.ufo/evidence/round-50/c1/measure.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows = json.load(open(ROWS))
ledger = json.dumps({'defects': rows}).encode()
orig = m.show
m.show = lambda lane, rev, path: ledger if path == m.LEDGER else orig(lane, rev, path)
spot = 'corpus/lessons/round-51-verifier-spotcheck.md'
def git(*a): return subprocess.run(['git', '-C', C] + list(a), capture_output=True, check=True).stdout
routed = git('log', '--diff-filter=A', '--format=%H', R, '--', spot).decode().split()[-1]
sha = hashlib.sha256(git('show', B + ':' + spot)).hexdigest()
defects = [{'id': r['id'], 'round': 51, 'file': spot, 'line': 0, 'end': 0, 'routed_at': routed, 'file_sha256': sha, 'text': '', 'keys': r['keys']} for r in rows]
notes = []
rev, counts, stat, total, nrows = m.measure(C, B, defects, True, explain=lambda *a: notes.append(a))
print('CHECK rows=%d stat=%s routed_at=%s spotcheck_changed=%d evidence_bad=%d key_miss=%d fixed_bad=%d missing=%d notes=%s' % (nrows, stat, routed[:9], counts['spotcheck_changed'], counts['evidence_bad'], counts['key_miss'], counts['fixed_bad'], counts['missing'], notes))
