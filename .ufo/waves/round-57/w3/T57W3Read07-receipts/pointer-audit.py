#!/usr/bin/env python3
"""Read-only audit of the assigned artifact map at a supplied scratch clone."""
import glob
import hashlib
import pathlib
import re
import subprocess
import sys
p = pathlib.Path(sys.argv[1]).resolve()
rev = 'adf87899c70d616140a81185a8f9acbbdfb30392'
assert subprocess.check_output(['git', '-C', str(p), 'rev-parse', 'HEAD'], text=True).strip() == rev
paths = ['corpus/knowledge/' + x + '.md' for x in ['operator-runbook', 'fleet-kill-rate-ledger', 'service-limits', 'service-optin-protocol', 'fleet-suite-census', 'service-standing-state', 'mutation-case-kumitate-cite-check', 'closeout-r11']]
paths += ['tools/mutate-and-run.sh', 'corpus/README.md', 'plans/round-11.plan.md', 'plans/completion-evidence.md', 'LOG.md', 'SCORECARD.md']
for name in paths:
    data = (p / name).read_bytes()
    print('POINTER OK', name, 'sha256=' + hashlib.sha256(data).hexdigest())
cases = sorted((p / 'corpus/knowledge').glob('mutation-case-*.md'))
assert len(cases) == 10
print('CASE NOTES', len(cases), ', '.join(x.name for x in cases))
plans = sorted(x.name for x in (p / 'plans').glob('round-*.plan.md'))
assert set(plans) == {'round-%d.plan.md' % n for n in range(2, 12)}
records = sorted(x.name for x in (p / 'plans').glob('round-*-record-draft.md'))
assert set(records) == {'round-%d-record-draft.md' % n for n in range(4, 11)}
assert not (p / 'plans/round-11-record-draft.md').exists()
print('PLANS', ', '.join(plans)); print('RECORD DRAFTS', ', '.join(records))
anchors = {'corpus/README.md': [125, 326, 614], 'corpus/knowledge/operator-runbook.md': [349, 350, 351], 'tools/mutate-and-run.sh': [149, 150], 'corpus/knowledge/fleet-kill-rate-ledger.md': [439, 441], 'LOG.md': [316, 317]}
for name, nums in anchors.items():
    lines = (p / name).read_text().splitlines()
    for n in nums:
        print('ANCHOR', name + ':' + str(n), lines[n - 1])
runbook = (p / 'corpus/knowledge/operator-runbook.md').read_text()
for n in [0, 2, 3, 4, 5, 6, 7, 10]:
    h = re.search(r'^## ' + str(n) + r'\. .+$', runbook, re.M)
    assert h
    print('RUNBOOK', h.group())
assert len(re.findall(r'^\| [1-6] \|', runbook, re.M)) == 12  # six ledger rows plus six tick rows
assert 'anchored source governs' in runbook
assert 'Pointer, not a second home' in (p / 'SKILL.md').read_text()
print('RUNBOOK six-case ledger, six-case tick, and source-precedence rule present; named bullet resolves in SKILL runbook section')
ledger = (p / 'corpus/knowledge/fleet-kill-rate-ledger.md').read_text()
measured = [x for x in ledger.splitlines() if (re.match(r'^\| [1-6] \|', x) and '%' in x) or re.match(r'^\| (?:kumitate `scripts/(?:round-gate|sources-check)\.mjs`)', x)]
print('LEDGER MEASURED ROWS', len(measured))
for row in measured: print(row)
assert len(measured) == 8
assert not re.search(r'^\|.*(?:cite-check|drift-pins).*\|.*(?:2/10|5/10)', ledger, re.M)
print('LEDGER no ninth/tenth measured table row; tenth supersession at line 439')
standing = (p / 'corpus/knowledge/service-standing-state.md').read_text()
assert all('SC' + str(n) in standing for n in [1, 2, 3])
print('STANDING SC1-SC3 present')
print('SWEEP PASS: all mapped pointers resolve and enumerated claims hold')
