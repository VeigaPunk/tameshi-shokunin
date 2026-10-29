#!/usr/bin/env python3
"""Step 3: key-specificity check X9 (fresh excerpt contains a key of >= 6 chars) and X1 AND X9 combined."""
import importlib.util
import json
import os
import re

S = os.environ['S']
CL = os.path.join(S, 'clone')
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
spec = importlib.util.spec_from_file_location('measure50', os.path.join(S, 'measure50.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
o = json.load(open(os.path.join(S, 'out.json')))
DEF_LIST = json.loads(m.show(CL, BASE, '.ufo/evidence/round-50/c1/defects.json').decode())['defects']
DEF = {d['id']: d for d in DEF_LIST}
RR = {r['id']: r for r in json.loads(m.show(CL, BASE, 'corpus/routed-defects.json').decode())['defects']}
STOP = set('that this with from have been were will into only when than also they them their there which '
           'about would could should does doing each being after before under over across other where while '
           'since until both very more most such some'.split())


def toks(s):
    return {t for t in re.findall(r'[a-z][a-z0-9_]{3,}', s.lower()) if t not in STOP}


def fresh_items(rid, row, ev_rev):
    d = DEF[rid]
    files = m.touched(CL, row['commit'])
    out = []
    for item in row['evidence']:
        if not isinstance(item, dict) or not m.has_key(item, d['keys']) or item.get('path') not in files:
            continue
        then = m.show(CL, d['routed_at'], item['path'])
        if then is not None and m.norm(item['excerpt']) in m.norm(then.decode('utf-8', 'replace')):
            continue
        a, b = (int(x) for x in item['lines'].split('-'))
        text = m.show(CL, ev_rev, item['path']).decode('utf-8', 'replace').split('\n')
        if any(w in ' '.join(text[a - 1:b]).lower() for w in m.ACK_WORDS):
            continue
        out.append(item)
    return out


def X1(rid, fr):
    return any(len(toks(i['excerpt']) & toks(DEF[rid]['text'])) >= 3 for i in fr)


def X9(rid, fr):
    return any(k.lower() in m.norm(i['excerpt']).lower() for i in fr for k in DEF[rid]['keys'] if len(k) >= 6)


res = {'real': {}, 'forged': {}}
for rid, row in RR.items():
    if row['status'] != 'fixed':
        continue
    fr = fresh_items(rid, row, BASE)
    res['real'][rid] = {'X1': X1(rid, fr), 'X9': X9(rid, fr), 'keys': DEF[rid]['keys']}
for name, row in ((k, v['row']) for k, v in o['forgery'].items()):
    fr = fresh_items(row['id'], row, o['rev_forge'])
    res['forged'][name] = {'X1': X1(row['id'], fr), 'X9': X9(row['id'], fr), 'keys': DEF[row['id']]['keys']}
for name in ('X1', 'X9'):
    print(name, 'real false-rejects:', [k for k, v in res['real'].items() if not v[name]])
    print(name, 'forged accepted:', [k for k, v in res['forged'].items() if v[name]])
both_fr = [k for k, v in res['real'].items() if not (v['X1'] and v['X9'])]
both_acc = [k for k, v in res['forged'].items() if v['X1'] and v['X9']]
print('X1&X9 real false-rejects:', both_fr)
print('X1&X9 forged accepted:', both_acc)
print('real fixed rows with keys len<6 only:', [k for k, v in res['real'].items() if not any(len(x) >= 6 for x in v['keys'])])
json.dump(res, open(os.path.join(S, 'out3.json'), 'w'), indent=1, ensure_ascii=False)
