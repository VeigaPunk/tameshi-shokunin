#!/usr/bin/env python3
"""Merge wave-2 blind-panel seats + wave-3 clean re-seats into .ufo/evidence/round-57/c1/panel.json
(schema tameshi-c1-panel-v1). The three re-seat seats govern their six ids (contract, consolidation rule):
T57W3ReseatR515R516 -> R51.5 R51.6; T57W3ReseatR525R526 -> R52.5 R52.6; T57W3ReseatR542R543 -> R54.2 R54.3."""
import glob, hashlib, json, os
L = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
ids = [d['id'] for d in json.load(open(L + '/.ufo/evidence/round-57/c1/defects.json'))['defects']]
verdicts, detail, files = {}, {}, {}
for f in sorted(glob.glob(L + '/.ufo/waves/round-57/w2/T57W2Panel*.json')):
    d = json.load(open(f)); seat = os.path.basename(f)[:-5]
    files[seat] = hashlib.sha256(open(f, 'rb').read()).hexdigest()
    for k, v in d['verdicts'].items():
        verdicts[k] = v['verdict']; detail[k] = {'seat': seat, 'commit': v.get('commit')}
reseated = {}
for f in sorted(glob.glob(L + '/.ufo/waves/round-57/w3/T57W3Reseat*.json')):
    d = json.load(open(f)); seat = os.path.basename(f)[:-5]
    files[seat] = hashlib.sha256(open(f, 'rb').read()).hexdigest()
    for k, v in d['verdicts'].items():
        reseated[k] = (seat, v)
verdicts.update({k: v[1]['verdict'] for k, v in reseated.items()})
detail.update({k: {'seat': v[0], 'commit': v[1].get('commit')} for k, v in reseated.items()})
assert sorted(verdicts) == sorted(ids), set(ids) ^ set(verdicts)
assert len(reseated) == 6, sorted(reseated)
out = {'schema': 'tameshi-c1-panel-v1', 'base': '5e3569969b532310d2b8a3d130901757a3df356b',
       'verdicts': {i: verdicts[i] for i in ids}, 'detail': {i: detail[i] for i in ids}, 'files': files}
open(L + '/.ufo/evidence/round-57/c1/panel.json', 'w').write(json.dumps(out, indent=1) + '\n')
print(len(ids), 'seats', len(files), 'reseated', len(reseated), sorted(reseated),
      {v: list(verdicts.values()).count(v) for v in set(verdicts.values())})
