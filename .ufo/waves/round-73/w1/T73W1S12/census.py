#!/usr/bin/env python3
"""Read-only census of the fleet's wave artifacts (results.json / dispatch /
swarm-registry.json). Answers: does `seats` equal the dispatched roster, is a
dead seat a record, can output be empty / carry a note, and does the registry
match the wave. Never writes; every path is absolute and read-only.
"""
import collections
import glob
import json
import os
import re

ROOTS = sorted(glob.glob('/home/vgpnk/Projects/shokunin/*-shokunin'))
RES = sorted({p for r in ROOTS for p in glob.glob(
    os.path.join(r, '.ufo/waves/round-*/*results.json'))})
REGS = sorted({p for r in ROOTS for p in glob.glob(
    os.path.join(r, '.ufo/waves/**/swarm-registry.json'), recursive=True)})


def dispatch_for(results_path, doc):
    base = os.path.dirname(results_path)
    wave = doc.get('wave')
    names = {r.get('name') for r in doc.get('results') or []}
    cands = []
    ready = os.path.join(base, '%s.ready' % wave)
    if os.path.exists(ready):
        try:
            cands.append(json.load(open(ready)).get('dispatch'))
        except ValueError:
            pass
    cands.append(os.path.join(base, '%s-dispatch.json' % wave))
    cands.extend(sorted(glob.glob(os.path.join(base, '*dispatch*.json'))))
    fallback = None
    for c in cands:
        if not c or not os.path.exists(c):
            continue
        try:
            d = json.load(open(c))
        except ValueError:
            continue
        tasks = (d.get('taskCall') or {}).get('tasks') or []
        if not tasks:
            continue
        tn = {t.get('name') for t in tasks}
        if tn == names:
            return d
        if fallback is None and names <= tn:
            fallback = d
    return fallback


def main():
    docs = 0
    bad = 0
    joined = 0
    seats_ok = 0
    name_ok = 0
    agent_mismatch = 0
    resume_waves = 0
    empty_out = 0
    null_out = 0
    notes = 0
    note_with_output = 0
    trunc = 0
    unavailable = 0
    note_kinds = collections.Counter()
    for p in RES:
        try:
            d = json.load(open(p))
        except ValueError:
            bad += 1
            continue
        if not isinstance(d, dict) or not isinstance(d.get('results'), list):
            bad += 1
            continue
        docs += 1
        rs = d['results']
        disp = dispatch_for(p, d)
        if disp is not None:
            joined += 1
            tasks = (disp.get('taskCall') or {}).get('tasks') or []
            if d.get('seats') == len(tasks) == len(rs):
                seats_ok += 1
            if {t.get('name') for t in tasks} == {r.get('name') for r in rs}:
                name_ok += 1
            agents = {t.get('name'): t.get('agent') for t in tasks}
            agent_mismatch += sum(1 for r in rs
                                  if agents.get(r.get('name')) != r.get('agent'))
            if disp.get('resumeSends'):
                resume_waves += 1
        for r in rs:
            o, n = r.get('output'), r.get('note')
            if o is None:
                null_out += 1
            elif isinstance(o, str):
                if not o.strip():
                    empty_out += 1
                if len(o) == 20000:
                    trunc += 1
                if '<output unavailable' in o:
                    unavailable += 1
            if n is not None:
                notes += 1
                if o is not None:
                    note_with_output += 1
                text = str(n).lower()
                for key in ('kernel restarted', 'never spawned', 'killed',
                            'no output', 'died', 'dead', 'timed out'):
                    if key in text:
                        note_kinds[key] += 1
    print('RESULTS files=%d parsed=%d bad=%d joined_to_dispatch=%d'
          % (len(RES), docs, bad, joined))
    print('SEATS seats==len(tasks)==len(results): %d/%d' % (seats_ok, joined))
    print('NAMES results names == dispatch tasks: %d/%d' % (name_ok, joined))
    print('AGENT results.agent == dispatch.agent mismatches: %d' % agent_mismatch)
    print('RESUME waves with resumeSends observed: %d' % resume_waves)
    print('OUTPUT empty-string=%d null=%d truncated-at-20000=%d unavailable-string=%d'
          % (empty_out, null_out, trunc, unavailable))
    print('NOTES non-null=%d (with non-null output=%d)' % (notes, note_with_output))
    print('NOTE-KINDS %s' % dict(sorted(note_kinds.items())))

    rdocs = 0
    rbad = 0
    kinds = collections.Counter()
    filled_docs = 0
    members = 0
    for p in REGS:
        try:
            d = json.load(open(p))
        except ValueError:
            rbad += 1
            continue
        if not isinstance(d, dict) or not isinstance(d.get('members'), dict):
            rbad += 1
            continue
        rdocs += 1
        ms = [v for v in d['members'].values() if isinstance(v, dict)]
        members += len(ms)
        kinds.update(v.get('kind') for v in ms)
        if any(v.get('agentId') for v in ms):
            filled_docs += 1
    print('REGISTRY docs=%d bad=%d members=%d kinds=%s docs_with_any_agentId=%d'
          % (rdocs, rbad, members, dict(kinds), filled_docs))


if __name__ == '__main__':
    main()
