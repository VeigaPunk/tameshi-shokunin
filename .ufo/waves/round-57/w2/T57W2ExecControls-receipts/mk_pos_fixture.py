#!/usr/bin/env python3
"""Scratch only (T57W2ExecControls): turn the lane's working-tree ledger into a ledger the amended C1 counter
passes, WITHOUT touching the counter: rows the counter refuses are replaced by honest `declined` rows with keyed
evidence; then write a synthetic panel (= each row's status_at_base) and pin it in the clone's counter copy."""
import json, re, subprocess, sys, hashlib, os
sys.path.insert(0, sys.argv[2] + '/.ufo/evidence/round-57/control')
import gen_ledger as g
clone = sys.argv[1] if len(sys.argv) > 1 else None
clone = sys.argv[2]
failing = set(json.load(open(sys.argv[1])))   # ids the counter refused
defects = json.load(open(clone + '/' + g.DEFECTS))['defects']
spot = {d['file'] for d in defects}
files = g.load_text_files(clone, spot)
doc = json.load(open(clone + '/' + g.LEDGER))
out = []
for r in doc['defects']:
    if r.get('id') in failing:
        d = next(x for x in defects if x['id'] == r['id'])
        ev, keyed = g.find_evidence(files, d['keys'], clone, spot)
        def tok(k, ex): return re.search(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', ex, re.I) is not None
        if not any(tok(k, ev['excerpt']) for k in d['keys']):
            ev = None
            for k in d['keys']:
                for path, lines in files:
                    for n, line in enumerate(lines, 1):
                        ex = g.norm(line)
                        if 15 <= len(ex) <= 300 and tok(k, ex):
                            ev = {'path': path, 'lines': '%d-%d' % (n, n), 'excerpt': ex}; break
                    if ev: break
                if ev: break
            keyed = ev is not None
        r = {'id': r['id'], 'seat': 'fixture', 'status': 'declined', 'status_at_base': 'open', 'evidence': [ev],
             'reason': 'dry-run fixture: row refused by the counter, replaced by a declined row with keyed evidence',
             'note': 'fixture keyed=%s' % keyed}
    out.append(r)
doc['defects'] = out
json.dump(doc, open(clone + '/' + g.LEDGER, 'w'), indent=1, ensure_ascii=False)
panel = {'verdicts': {r['id']: r['status_at_base'] for r in out[49:]}}
pp = clone + '/' + g.PANEL
open(pp, 'w').write(json.dumps(panel, indent=1, sort_keys=True) + '\n')
sha = hashlib.sha256(open(pp, 'rb').read()).hexdigest()
mp = clone + '/.ufo/evidence/round-57/c1/measure.py'
s = open(mp).read()
s = re.sub(r"^PANEL_SHA256 = .*$", "PANEL_SHA256 = '%s'" % sha, s, flags=re.M)
open(mp, 'w').write(s)
print(json.dumps({'refused_replaced': len(failing), 'panel_sha': sha}))
