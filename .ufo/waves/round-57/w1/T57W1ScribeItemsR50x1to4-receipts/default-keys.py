import json, sys
sys.dont_write_bytecode = True
CTL, EXTRACT = sys.argv[1], sys.argv[2]
exec(open(CTL).read().split("print('== A.")[0])
d50 = json.load(open(EXTRACT))['defects']
dd = {x['id']: x for x in d50 if x['id'].startswith('R50.')}
ok = True
for rid in ['R50.1', 'R50.2', 'R50.3', 'R50.4']:
    row = byid[rid]
    d = {'id': rid, 'keys': dd[rid]['keys'], 'routed_at': dd[rid]['routed_at'], 'file': dd[rid]['file']}
    r = {k: row[k] for k in ('id', 'status', 'evidence') if k in row}
    if 'commit' in row:
        r['commit'] = row['commit']
    stat = {'fixed': 0, 'open': 0, 'declined': 0, 'fixed_this_round': 0}
    notes = []
    f = m57.judge(LANE, BASE, d, r, {'R50.4'}, {}, {}, BASE, stat, lambda *a: notes.append(a))
    print('DEFAULT-KEYS', rid, 'fault=', f, notes)
    ok = ok and f is None
print('DEFAULT_KEYS_OK' if ok else 'DEFAULT_KEYS_FAIL')
sys.exit(0 if ok else 1)
