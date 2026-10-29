import importlib.util, json, os, sys, hashlib, subprocess
S = os.environ['S']; C = S + '/clone'
B = '5e3569969b532310d2b8a3d130901757a3df356b'; R = 'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4'
FIX = 'bcba8924894216268afc4171f06eb8c28e912b46'
SEAT = 'T57W1ScribeItemsR51x1to4'
def load(name, p):
    spec = importlib.util.spec_from_file_location(name, p); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
m = load('m50', C + '/.ufo/evidence/round-50/c1/measure.py')
ext = load('ext50', C + '/.ufo/evidence/round-50/c1/extract-defects.py')
def git(*a): return subprocess.run(['git', '-C', C] + list(a), capture_output=True, check=True).stdout
def blob(rev, p): return git('show', '%s:%s' % (rev, p)).decode('utf-8', 'replace')
def norm(t): return ' '.join(t.split())
def locate(path, excerpt, maxspan=3):
    lines = blob(B, path).split('\n'); want = norm(excerpt)
    for span in range(1, maxspan + 1):
        for i in range(len(lines) - span + 1):
            if want in norm('\n'.join(lines[i:i + span])):
                return '%d-%d' % (i + 1, i + span)
    raise SystemExit('LOCATE_FAIL %s %r' % (path, excerpt))
def ev(path, excerpt, lines=None):
    return {'path': path, 'lines': lines or locate(path, excerpt), 'excerpt': norm(excerpt)}
spot = 'corpus/lessons/round-51-verifier-spotcheck.md'
items = ext.items_of(blob(R, spot))
assert [i['text'][:40] for i in items][:4] == [i['text'][:40] for i in items][:4]
rows_spec = {
 'R51.1': dict(status='fixed', commit=FIX, keys=['mte-interop-check', 'tools/registry.json', 'registry-check --only mte-interop-check'],
   evidence=[ev('tools/registry.json', 'MTE_INTEROP: PASS legs_conforming=10/10'),
             ev('tools/mte-interop.py', 'MTE_INTEROP: %s legs_conforming=%d/%d')],
   note='Row mte-interop-check now expects legs_conforming=10/10 (was 9/9) in bcba892; the round-52 no-harm.sh tools-scope allows M:tools/registry.json. A green registry-check receipt was not re-run in this seat.'),
 'R51.2': dict(status='fixed', commit=FIX, keys=[':2136', '/tmp', ':174', ':211', ':937-950'],
   evidence=[ev('SKILL.md', 'leg set not equal to the ten ledger legs'),
             ev('SKILL.md', 'caller-chosen --workdir (or auto mktemp under ${TMPDIR:-/tmp}) for run and --regression'),
             ev('SKILL.md', 'the maintained driver also prints the failing count: `tools/mutate-and-run.sh:434`'),
             ev('SKILL.md', 'PASS/FAIL/SETUP (`tools/mutate-and-run.sh:139-143,1519-1548`)')],
   note='Three of the four stale statements were corrected in bcba892 (ten ledger legs; runner row honours TMPDIR; pointers :434 and :579-583). The :937-950 regression pointer was re-anchored later, in 7ff81a5 (round 52, wave-2 fix-reads), to 139-143,1519-1548; the base text at 139-143 is the exit map.'),
 'R51.3': dict(status='fixed', commit=FIX, keys=['wrong_expectations', 'refresh.py', 'coldread/refresh.py'],
   evidence=[ev('.ufo/evidence/round-21/coldread/ledger.json', 'wrong_expectations 0 was written from code (round-51 refresh.py:227)', lines='112211-112211'),
             ev('.ufo/evidence/round-21/coldread/ledger.json', '"wrong_expectations": 3,', lines='112193-112193'),
             ev('.ufo/evidence/round-52/coldread/refresh.py', "'wrong_expectations': len(reader['findings'])")],
   note='bcba892 appends the top-level "corrections" list (20 records, append-only) to the round-21 ledger; each record names the round-51 refresh.py:227 zero and carries the recorded count. The refresh instrument itself was not changed by this fix.'),
 'R51.4': dict(status='fixed', commit=FIX, keys=['tools/round21-measure.py', '--selftest', 'hermetic', 'fleet-bound'],
   evidence=[ev('tools/round21-measure.py', 'so the selftest is fleet-bound, not hermetic'),
             ev('SKILL.md', 'fleet-bound, not hermetic (since round 52 it reads the sibling blobs at the fleet root')],
   note='bcba892 takes the second branch of the item: the selftest is declared fleet-bound, not hermetic, in the tool docstring and the SKILL gate row. The pre-registration is the SCORECARD round-52 section in the same commit; the R51.5 mutation attack is not part of this row.'),
}
defects = []
for it in items[:4]:
    pass
# id rule: labelled **R<round>.<n> else 1-based position in the item list
for pos, it in enumerate(items, 1):
    lab = it['text'].startswith('**R51.')
    did = 'R51.%s' % it['text'][len('**R51.'):].split('*')[0].split(',')[0].split('.')[0] if lab else 'R51.%d' % pos
    if did in rows_spec:
        defects.append({'id': did, 'round': 51, 'file': spot, 'line': it['line'], 'end': it.get('end', it['line']),
                        'routed_at': git('log', '--diff-filter=A', '--format=%H', R, '--', spot).decode().split()[-1],
                        'file_sha256': hashlib.sha256(git('show', '%s:%s' % (B, spot))).hexdigest(),
                        'text': it['text'][:600], 'keys': rows_spec[did]['keys']})
print('ITEM_IDS', [(d['id'], d['line'], d['text'][:50]) for d in defects])
rows = []
for d in defects:
    s = rows_spec[d['id']]
    row = {'id': d['id'], 'status': s['status'], 'evidence': [{k: e[k] for k in ('path', 'lines', 'excerpt')} for e in s['evidence']],
           'commit': s['commit'], 'seat': SEAT, 'note': s['note'], 'keys': s['keys'], 'verdict_basis': None}
    rows.append(row)
json.dump({'schema': 'tameshi-routed-defects-v1', 'round': 51, 'rows_for': 'R51.1-4', 'defects': rows}, open(S + '/rows_only.json', 'w'), indent=1, ensure_ascii=False)
# measure with a fixture ledger carrying only these rows (the lane ledger is replaced in memory, not on disk)
notes = []
orig_show = m.show
ledger_bytes = json.dumps({'defects': rows}).encode()
def fake_show(lane, rev, path):
    if path == m.LEDGER: return ledger_bytes
    return orig_show(lane, rev, path)
m.show = fake_show
rev, counts, stat, total, nrows = m.measure(C, B, defects, True, explain=lambda *a: notes.append(a))
print('MEASURE rev=%s counts_nonzero=%s stat=%s total=%d' % (rev[:8], {k: v for k, v in counts.items() if v}, stat, total))
print('NOTES', notes)
json.dump({'rev': rev, 'counts': counts, 'stat': stat, 'total': total, 'notes': [list(map(str, n)) for n in notes]}, open(S + '/measure.json', 'w'), indent=1)
