import importlib.util, json, os, subprocess, sys, hashlib
S = os.environ['S']; FIX = S + '/fix'; W = os.environ['W']
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'; ROUTED = 'c1d49d76be4028df2a68322e7117ff3aafaccd5c'
spec = importlib.util.spec_from_file_location('m50', FIX + '/.ufo/evidence/round-50/c1/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def git(*a): return subprocess.run(['git', '-C', FIX] + list(a), capture_output=True, text=True, check=True).stdout
def blob(rev, path): return git('show', '%s:%s' % (rev, path))
ledger_base = blob(BASE, '.ufo/evidence/round-21/coldread/ledger.json').split('\n')
ledger_spot = blob(ROUTED, '.ufo/evidence/round-21/coldread/ledger.json')
# R52.1: heading + sha256 line of entries whose (heading, sha) is absent at the spot-check commit
def block_for(heading):
    for i, line in enumerate(ledger_base):
        if line.strip() == '"heading": "%s",' % heading:
            sha = ledger_base[i + 1]
            if '"sha256"' in sha and sha.strip() not in ledger_spot:
                return i + 1, i + 2  # 1-based heading line, sha line
    raise SystemExit('no new block for ' + heading)
h1 = block_for('### The tick, executed'); h2 = block_for('### The receipt at this boundary')
def excerpt(lines, span):
    return ' '.join(ledger_base[span[0] - 1:span[1]]).strip()
e1 = excerpt(ledger_base, h1); e2 = excerpt(ledger_base, h2)
print('R52.1 blocks', h1, h2)
print('e1:', e1[:200]); print('e2:', e2[:200])
lesson = blob(BASE, 'corpus/lessons/round-52.md').decode() if False else blob(BASE, 'corpus/lessons/round-52.md').split('\n')
log = blob(BASE, 'LOG.md').split('\n')
assert 'Example: Corr12, where the reviewer found 0 of 14' in lesson[26], lesson[26]
assert log[2443] == '## 2026-10-27 — round 52 (honest stop, run wrap-up)', repr(log[2443])
c_tick = git('log', '--reverse', '--format=%H', '-S', '"sha256": "d58978b5611e65939b188704ce32de562ddce854885aee7a85cb24858707b2f0"', '--', '.ufo/evidence/round-21/coldread/ledger.json').split()[0]
c_log = git('log', '--format=%H', '-S', 'round 52 (honest stop, run wrap-up)', '--', 'LOG.md').split()[0]
print('commits', c_tick, c_log)
rows = [
 {'id': 'R52.1', 'status': 'fixed', 'commit': c_tick,
  'evidence': [{'path': '.ufo/evidence/round-21/coldread/ledger.json', 'lines': '%d-%d' % h1, 'excerpt': e1},
               {'path': '.ufo/evidence/round-21/coldread/ledger.json', 'lines': '%d-%d' % h2, 'excerpt': e2}],
  'keys': ['The tick, executed', 'The receipt at this boundary', 'R52.1'],
  'seat': 'T57W1ScribeItemsR52x1to3',
  'verdict_basis': 'Round-21 monitor at BASE credits 64/64 (cr-base.json); at spot-check commit c1d49d7 it credits 45/64 and the 19 headings named in R52.1 are uncredited there. Entries for "The tick, executed" (sha256 d58978b5...) and "The receipt at this boundary" are absent at c1d49d7 and first added by re-key commits (e98044a for the first block); the excerpts are verbatim at BASE.',
  'note': 'Restoring commit is the first re-key commit to bind a lost heading (e98044a); later commits 88afa94, 7fa9a5e and c1dd23b completed the credit set. Monitor measure at BASE is the closure-independent evidence.'},
 {'id': 'R52.2', 'status': 'fixed', 'commit': c_log,
  'evidence': [{'path': 'LOG.md', 'lines': '2444-2444', 'excerpt': '## 2026-10-27 — round 52 (honest stop, run wrap-up)'}],
  'keys': ['round 52 (honest stop', 'R52.2', 'LOG.md'],
  'seat': 'T57W1ScribeItemsR52x1to3',
  'verdict_basis': 'The round-52 LOG entry is absent at c1d49d7 (git show c1d49d7:LOG.md contains no "round 52 (honest stop") and is added at BASE line 2444 by a41195d (the only commit whose diff adds it; git log -S returns only a41195d).',
  'note': 'a41195d is the round-53 C* content commit that also carries the round-52 and round-53 LOG entries.'},
 {'id': 'R52.3', 'status': 'open', 'evidence': [{'path': 'corpus/lessons/round-52.md', 'lines': '27-27', 'excerpt': lesson[26].strip()}],
  'keys': ['Corr12', '0 of 14', 'R52.3', 'over-count'],
  'seat': 'T57W1ScribeItemsR52x1to3',
  'verdict_basis': 'Still true at BASE: corpus/lessons/round-52.md:27 keeps "Example: Corr12, where the reviewer found 0 of 14 findings..." while the Corr12 reader file T51W2Read12.md carries two strict **drift** rows (P2 at line 55, P10 at line 63), so the 0-of-14 example is contradicted. No commit after c1d49d7 touches round-52.md or names R52.3 except inherited copies (grep).',
  'note': 'Full re-derivation of records 01,02,06,09-13 is not done; it needs each of 51 findings mapped to reader rows in heterogeneous formats (tables, JSON, prose), so it is costly, not a cheap patch.'},
]
json.dump(rows, open(W + '/rows.json', 'w'), indent=1, ensure_ascii=False)
print('wrote', len(rows))
