#!/usr/bin/env python3
"""s6: does a receipts-directory .json (the shape every wave-2 seat's receipts
take) poison the wave-1 validator's report glob?

The validator's glob is the counter's:  /T56W\\d+.*Read.*\\.json$
A path such as .ufo/waves/round-56/w2/T56W2Read02-receipts/01-live-dispositions.json
matches it, so the receipts of a READER seat are read as reader reports.
"""
import json
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

out = []

CASES = [
    ('s6a-receipt-json-no-heading', 'T56W2Read02-receipts/01-live-dispositions.json',
     {'note': 'a receipt payload with no heading key'}),
    ('s6b-receipt-json-with-heading', 'T56W2Read03-receipts/02-dispositions.json',
     {'heading': H.HEADINGS[0], 'note': 'a receipt payload that happens to carry a heading'}),
    ('s6c-seat-md-json', 'T56W2MutGateOnC0-receipts/mutants.json',
     {'note': 'a receipt under a seat name with no "Read" in it'}),
]

for tag, rel, payload in CASES:
    repo = H.clone(tag)
    d = H.wave_dir(repo)
    d.mkdir(parents=True, exist_ok=True)
    for i, h in enumerate(H.HEADINGS):
        H.write_report(d, H.seat_name(i), H.report_for(i, h, H.SECTIONS[h]['sha256']),
                       H.md_for(h))
    p = repo / '.ufo/waves/round-56/w2' / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=1) + '\n', encoding='utf-8')
    rev = H.commit(repo, tag)
    v = H.run_validator(repo, rev, H.S / ('work-' + tag))
    rec = {'tag': tag, 'file': rel,
           'glob_match': bool(__import__('re').search(r'/T56W\d+.*Read.*\.json$', rel)),
           'validator_rc': v.returncode,
           'validator_refusals': [l for l in v.stdout.splitlines() if l.startswith('REFUSE')],
           'validator_verdict': v.stdout.splitlines()[-1] if v.stdout else ''}
    out.append(rec)
    print('== %s file=%s glob_match=%s' % (tag, rel, rec['glob_match']))
    print('   validator rc=%d %s' % (rec['validator_rc'], rec['validator_verdict']))
    for r in rec['validator_refusals']:
        print('   %s' % r[:170])

(H.S / 's6-receipt-poison.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n',
                                            encoding='utf-8')
