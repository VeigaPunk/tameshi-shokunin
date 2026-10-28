#!/usr/bin/env python3
"""Extract, per scenario, what the binder actually wrote into the ledger for
heading[0] (the tampered heading), plus run one more scenario: a second report
for the same heading that sorts FIRST and carries findings, which the binder
`break`s on."""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, '/fast/scratch/hyaku/tameshi-r56/T56W2SentReaders')
import harness as H  # noqa: E402

HEADINGS = H.HEADINGS
H0 = HEADINGS[0]
_work = H.S / 'sec'
_work.mkdir(parents=True, exist_ok=True)
_mod, _digest = H.load_sectionize(H.LANE, H.C0, _work)
_raw = H.show(H.LANE, H.C0, 'SKILL.md').encode('utf-8', 'surrogateescape')
for _sec in _mod.sectionize(_raw):
    H.SECTIONS[_sec['heading']] = _sec
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else H.S / 'ledger-evidence.json')
res = json.loads((H.S / 'results.json').read_text('utf-8'))

ev = {}
for s in res['scenarios']:
    tag = s['tag']
    repo = H.S / ('clone-' + tag.split('-')[0])
    ledger = json.loads((repo / '.ufo/evidence/round-21/coldread/ledger.json').read_text('utf-8'))
    ent = [e for e in ledger['entries']
           if isinstance(e, dict) and e.get('heading') == H0]
    # the entry this binder wrote is the one whose read_rev is C0 and whose
    # traces point at the harness OUT dir
    written = [e for e in ent if str(e.get('read_rev')) == H.C0
               and any('section-' in str(t) for t in (e.get('traces') or []))]
    ev[tag] = {
        'validator_rc': s['validator_rc'],
        'validator_verdict': s['validator_verdict'],
        'validator_refusals': s['validator_refusals'],
        'binder_rc': s['binder_rc'],
        'binder_skips': s['binder_skips'],
        'binder_rekeys': s['binder_rekeys'],
        'heading0_entries': [
            {'read_rev': e.get('read_rev'), 'sha256': (e.get('sha256') or '')[:12],
             'verdict': e.get('verdict'), 'minor_gaps': e.get('minor_gaps'),
             'reports': e.get('reports'), 'seats': e.get('seats'),
             'traces': e.get('traces')} for e in ent],
        'heading0_bound': [
            {'read_rev': e.get('read_rev'), 'sha256': (e.get('sha256') or '')[:12],
             'verdict': e.get('verdict'), 'minor_gaps': e.get('minor_gaps'),
             'reports': e.get('reports'), 'seats': e.get('seats'),
             'traces': e.get('traces')} for e in written],
    }

# ---- extra scenario: a second report for the same heading, sorting FIRST ------
tag = 's5b-bad-first'
repo = H.clone('s5b')
d = H.wave_dir(repo)
d.mkdir(parents=True, exist_ok=True)
for i, h in enumerate(HEADINGS):
    sha = H.SECTIONS[h]['sha256']
    data = H.report_for(i, h, sha)
    H.write_report(d, H.seat_name(i), data, H.md_for(h))
alt = H.report_for(0, H0, H.SECTIONS[H0]['sha256'])
alt['findings'] = ['a finding the L1 never adjudicated']
alt['commands'] = ['grep -n -- "%s" SKILL.md' % H0]
H.write_report(d, H.seat_name(0) + '-alt', alt, H.md_for(H0))
rev = H.commit(repo, 'S5b alt report sorts first')
extra = H.summarize(tag, repo, rev,
                     'second report for heading[0] whose name sorts BEFORE the good one '
                     '(%s-alt.json) and carries one finding' % H.seat_name(0))
ledger = json.loads((repo / '.ufo/evidence/round-21/coldread/ledger.json').read_text('utf-8'))
ent = [e for e in ledger['entries'] if isinstance(e, dict) and e.get('heading') == H0
       and str(e.get('read_rev')) == H.C0]
ev[tag] = {
    'validator_rc': extra['validator_rc'],
    'validator_verdict': extra['validator_verdict'],
    'validator_refusals': extra['validator_refusals'],
    'binder_rc': extra['binder_rc'],
    'binder_skips': extra['binder_skips'],
    'binder_rekeys': extra['binder_rekeys'],
    'heading0_entries': [{'read_rev': e.get('read_rev'), 'verdict': e.get('verdict'),
                           'minor_gaps': e.get('minor_gaps'), 'reports': e.get('reports'),
                           'seats': e.get('seats')} for e in ent],
    'heading0_bound': [{'read_rev': e.get('read_rev'), 'verdict': e.get('verdict'),
                         'minor_gaps': e.get('minor_gaps'), 'reports': e.get('reports'),
                         'seats': e.get('seats')} for e in ent],
}
res['scenarios'].append(extra)
(H.S / 'results.json').write_text(json.dumps(res, indent=1, ensure_ascii=False) + '\n',
                                  encoding='utf-8')
OUT.write_text(json.dumps(ev, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
for tag, v in ev.items():
    print('== %s validator_rc=%s binder_rc=%s skips=%s' %
          (tag, v['validator_rc'], v['binder_rc'], v['binder_skips']))
    for e in v['heading0_entries']:
        print('   entry verdict=%s minor_gaps=%s reports=%s seats=%s'
              % (e.get('verdict'), e.get('minor_gaps'), e.get('reports'), e.get('seats')))
print('evidence -> %s' % OUT)
