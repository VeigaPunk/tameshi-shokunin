#!/usr/bin/env python3
"""s4c/s4d: `findings` as a string, WITH the L1's adjudication allowance in
force (round-56 resolutions.json). The binder counts the string's CHARACTERS
as findings, so a malformed field consumes (or understates) the allowance."""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, '/fast/scratch/hyaku/tameshi-r56/T56W2SentReaders')
import harness as H  # noqa: E402

_work = H.S / 'sec'
_work.mkdir(parents=True, exist_ok=True)
_mod, _d = H.load_sectionize(H.LANE, H.C0, _work)
_raw = H.show(H.LANE, H.C0, 'SKILL.md').encode('utf-8', 'surrogateescape')
for _s in _mod.sectionize(_raw):
    H.SECTIONS[_s['heading']] = _s

RES = H.LANE / '.ufo/evidence/round-56/integrate/resolutions.json'
TARGET = '## Standing rules'          # allowance n=3 in the L1's resolutions
out = []

for tag, value in (('s4c-findings-3char-string', 'abc'), ('s4d-findings-1char-string', 'x')):
    repo = H.clone(tag)
    d = H.wave_dir(repo)
    d.mkdir(parents=True, exist_ok=True)
    for i, h in enumerate(H.HEADINGS):
        sha = H.SECTIONS[h]['sha256']
        data = H.report_for(i, h, sha)
        if h == TARGET:
            data['findings'] = value
        H.write_report(d, H.seat_name(i), data, H.md_for(h))
    rev = H.commit(repo, tag)
    v = H.run_validator(repo, rev, H.S / ('work-' + tag))
    out_dir = H.S / ('out-' + tag)
    if out_dir.exists():
        import shutil
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    tmp = H.S / ('tmp-' + tag)
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(H.ENV, TMPDIR=str(tmp))
    b = subprocess.run([sys.executable, str(H.BINDER), str(repo), H.C0, H.C0, str(out_dir),
                        '--headings', str(H.HEADINGS_FILE),
                        '--waves', '.ufo/waves/round-56/w2',
                        '--resolutions', str(RES),
                        '--label', 'L1 TameshiR56 re-key (round 56)'],
                       env=env, capture_output=True, text=True)
    ledger = json.loads((repo / '.ufo/evidence/round-21/coldread/ledger.json').read_text('utf-8'))
    ent = [e for e in ledger['entries'] if isinstance(e, dict) and e.get('heading') == TARGET
           and str(e.get('read_rev')) == H.C0]
    rec = {
        'tag': tag, 'findings_value': value,
        'allowance_from_resolutions': 3,
        'validator_rc': v.returncode,
        'validator_refusals': [l for l in v.stdout.splitlines() if l.startswith('REFUSE')],
        'validator_verdict': v.stdout.splitlines()[-1] if v.stdout else '',
        'binder_rc': b.returncode,
        'binder_skips': [l for l in b.stdout.splitlines() if l.startswith('SKIP ')],
        'binder_tail': [l for l in b.stdout.splitlines() if l.startswith('REFRESH ')],
        'ledger_entry': [{'verdict': e.get('verdict'), 'minor_gaps': e.get('minor_gaps'),
                          'reports': e.get('reports'), 'seats': e.get('seats')} for e in ent],
    }
    out.append(rec)
    print('== %s findings=%r' % (tag, value))
    print('   validator rc=%d %s' % (rec['validator_rc'], rec['validator_refusals'][:1]))
    print('   binder rc=%d %s %s' % (rec['binder_rc'], rec['binder_tail'], rec['binder_skips'][:2]))
    print('   ledger %s' % rec['ledger_entry'])

(H.S / 's4c-s4d.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n',
                                   encoding='utf-8')
