#!/usr/bin/env python3
"""18-heading drift map at the round-56 base: section bytes, prior pinned inputs,
which pins drifted, and which headings have no matching ledger entry."""
import hashlib
import importlib.util
import json
import subprocess
import os

S = '/fast/scratch/hyaku/tameshi-r56/T56W1CritC1'
L = S + '/lane'
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
FROZEN = json.load(open(LANE + '/.ufo/evidence/round-56/c1/lost-headings-at-base.json'))


def blob(rev, path):
    r = subprocess.run(['git', '-C', L, 'show', '%s:%s' % (rev, path)], capture_output=True, env=ENV)
    return r.stdout if r.returncode == 0 else None


spec = importlib.util.spec_from_file_location('r18d', L + '/.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
secs = {s['heading']: s for s in m.sectionize(blob(BASE, 'SKILL.md'))}
led = json.loads(blob(BASE, '.ufo/evidence/round-21/coldread/ledger.json').decode('utf-8', 'surrogateescape'))
out = []
for head in FROZEN:
    sec = secs[head]
    prior = [e for e in led['entries'] if e.get('sha256') == sec['sha256']]
    pins = {}
    for e in prior:
        for p, sha in (e.get('inputs') or {}).items():
            data = blob(BASE, p)
            pins[p] = pins.get(p) or {'sha_recorded': sha,
                                      'at_base': 'missing' if data is None else hashlib.sha256(data).hexdigest()}
    drifted = sorted(p for p, v in pins.items() if v['at_base'] != v['sha_recorded'])
    out.append({'heading': head, 'start': sec['start'], 'end': sec['end'],
                'sha256_at_base': sec['sha256'], 'prior_entries': len(prior),
                'prior_inputs': len(pins), 'drifted_inputs': drifted,
                'stable_inputs': sorted(set(pins) - set(drifted))})
json.dump(out, open(S + '/out/drift.json', 'w'), indent=1)
for r in out:
    print('%-62s %3d-%-3d prior=%d pins=%d drifted=%d %s' % (
        r['heading'][:62], r['start'], r['end'], r['prior_entries'], r['prior_inputs'],
        len(r['drifted_inputs']), ','.join(r['drifted_inputs'])[:120]))
