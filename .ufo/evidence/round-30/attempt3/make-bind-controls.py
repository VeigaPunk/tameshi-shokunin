#!/usr/bin/env python3
"""Round 30 attempt 3: build the binding controls (synthetic session stores) for the round-29 pilot
assembly. Usage: make-bind-controls.py OUTDIR (run from a lane clone). Each control dir holds one
transcript per registry Read* member; none of them reads anything."""
import json, os, re, sys
S = sys.argv[1]
a = json.load(open('.ufo/evidence/round-29/coldread/assembled-w1.json'))
tr = {}
for e in a['entries']:
    for t in e['traces']:
        b = os.path.basename(t)
        tr.setdefault(re.sub(r'-\d+$', '', os.path.splitext(b)[0].split('.')[-1]), []).append(b)
reg = json.load(open('.ufo/waves/round-29/w1/swarm-registry.json'))
def w(d, k, msgs):
    os.makedirs(f'{S}/{d}', exist_ok=True)
    open(f'{S}/{d}/TameshiR29.{k}.jsonl', 'w').write(''.join(json.dumps(m) + '\n' for m in msgs))
def msg(role, content, **kw):
    return {'type': 'message', 'message': dict(role=role, content=content, **kw)}
for k in reg['members']:
    if not k.startswith('Read'):
        continue
    u = msg('user', [{'type': 'text', 'text': f'Last line exactly `COLDREAD {k}: <verdicts>`'}])
    fin = msg('assistant', [{'type': 'text', 'text': f'COLDREAD {k}: executed-ok'}])
    names = ' '.join(tr.get(k, []))
    call = msg('assistant', [{'type': 'toolCall', 'id': 'x1', 'name': 'bash', 'arguments': {'command': f'echo trace-inputs.py {names}'}}])
    w('promptonly', k, [u])                                   # no assistant line at all
    w('donothing', k, [u, fin])                               # the COLDREAD line, nothing else
    w('textmention', k, [u, msg('assistant', [{'type': 'text', 'text': f'ran trace-inputs.py --out {names}'}]), fin])  # keyed on trace labels, in prose
    w('noresult', k, [u, call, fin])                          # tool call naming the traces, never executed
    w('forged', k, [u, call, msg('toolResult', [], toolCallId='x1'), fin])  # hand-forged call + result: the residual limit
