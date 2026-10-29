import sys, json, hashlib, importlib.util, os
sys.dont_write_bytecode = True
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '5e3569969b532310d2b8a3d130901757a3df356b'
spec = importlib.util.spec_from_file_location('r50c1', LANE + '/.ufo/evidence/round-50/c1/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows = json.load(open(LANE + '/.ufo/waves/round-57/w1/T57W1ScribeItemsR55x1to4/rows.json'))
SPOT = 'corpus/lessons/round-55-verifier-spotcheck.md'
ROUTED = 'fa48c06c3669355fd80e8722eb733c1d6dfdd2f8'
spot_sha = hashlib.sha256(m.show(LANE, ROUTED, SPOT)).hexdigest()
ledger = {'schema': 'tameshi-routed-defects-v1', 'round': 50,
          'defects': [{k: v for k, v in r.items() if k not in ('keys', 'verdict_basis')} for r in rows]}
blob = json.dumps(ledger, ensure_ascii=False).encode()
orig_show = m.show
def fake_show(lane, rev, path):
    if path == m.LEDGER:
        return blob
    return orig_show(lane, rev, path)
m.show = fake_show
defects = [{'id': r['id'], 'file': SPOT, 'file_sha256': spot_sha, 'routed_at': ROUTED, 'keys': r['keys']} for r in rows]
# pass 1: the frozen rules as they stand (planned paragraph not yet written)
rev, counts, stat, total, nrows = m.measure(LANE, REV, defects, True, fixed_floor=0, declined_cap=12,
                                            explain=lambda *a: print('NOTE', *a), this_round_floor=0, base=REV)
print('PASS1 rev=%s stat=%s counts=%s total=%d rows=%d' % (rev[:12], stat, {k: v for k, v in counts.items() if v}, total, nrows))
# pass 2: same rows with the planned check satisfied for the two open ids (isolates the other arms)
m.planned_ids = lambda lane, rev: {'R55.2', 'R55.4'}
rev, counts, stat, total, nrows = m.measure(LANE, REV, defects, True, fixed_floor=0, declined_cap=12,
                                            explain=lambda *a: print('NOTE', *a), this_round_floor=0, base=REV)
print('PASS2 rev=%s stat=%s counts=%s total=%d rows=%d' % (rev[:12], stat, {k: v for k, v in counts.items() if v}, total, nrows))
# per-evidence resolution detail
cache = {}
for r, d in zip(rows, defects):
    for item in r['evidence']:
        print(r['id'], item['path'], item['lines'], 'resolves' if m.check_evidence(LANE, REV, item, d['keys'], {SPOT: spot_sha}, cache) is None else m.check_evidence(LANE, REV, item, d['keys'], {SPOT: spot_sha}, cache), 'keyed' if m.has_key(item, d['keys']) else 'unkeyed')
