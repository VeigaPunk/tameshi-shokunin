#!/usr/bin/env python3
"""Merge the 25 wave-2 blind-panel seat files into .ufo/evidence/round-57/c1/panel.json (schema tameshi-c1-panel-v1)."""
import glob, hashlib, json, os
L = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
ids = [d['id'] for d in json.load(open(L + '/.ufo/evidence/round-57/c1/defects.json'))['defects']]
verdicts, detail, files = {}, {}, {}
for f in sorted(glob.glob(L + '/.ufo/waves/round-57/w2/T57W2Panel*.json')):
    d = json.load(open(f)); seat = os.path.basename(f)[:-5]
    files[seat] = hashlib.sha256(open(f, 'rb').read()).hexdigest()
    for k, v in d['verdicts'].items():
        verdicts[k] = v['verdict']; detail[k] = {'seat': seat, 'commit': v.get('commit')}
assert sorted(verdicts) == sorted(ids), set(ids) ^ set(verdicts)
out = {'schema': 'tameshi-c1-panel-v1', 'base': '5e3569969b532310d2b8a3d130901757a3df356b', 'verdicts': {i: verdicts[i] for i in ids},
       'detail': {i: detail[i] for i in ids}, 'files': files}
open(L + '/.ufo/evidence/round-57/c1/panel.json', 'w').write(json.dumps(out, indent=1) + '\n')
print(len(ids), 'seats', len(files), {v: list(verdicts.values()).count(v) for v in set(verdicts.values())})
