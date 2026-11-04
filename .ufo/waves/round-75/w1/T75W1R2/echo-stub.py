#!/usr/bin/env python3
"""Echo-stub control (plan control 2, verified by T75W1R2): copies the doc's
own figure as the 'measurement'. Reads stale=0 — the count alone is not
self-authenticating."""
import re, sys
SPECS = [
 ('receipt-existence sweep', r'RECEIPT_EXISTS_SELFTEST: \d+/\d+ pass'),
 ('commit-message receipt binding sweep', r'RECEIPT_COMMIT_BIND_SELFTEST: \d+/\d+ pass'),
 ('quoted-line receipt backability', r'QUOTED_LINE_EXISTS_SELFTEST: \d+/\d+ pass'),
 ('counter-arm liveness check', r'ARM_LIVENESS_SELFTEST: \d+/\d+ pass'),
 ('counter-arm liveness check', r'rows=\d+ live=\d+ dead=\d+'),
 ('figure-attribution check', r'FIGURE_ATTRIBUTION_SELFTEST: \d+/\d+ pass'),
 ('figure-attribution check', r'FIGURE_ATTRIBUTION: rows=\d+ met=\d+ unexpected=\d+'),
 ('anchor-drift sweep', r'ANCHOR_DRIFT_SELFTEST: \d+/\d+ pass'),
 ('anchor-drift sweep', r'ANCHOR_DRIFT: rows=\d+ met=\d+ unexpected=\d+'),
 ('printed-count recheck', r'COUNT_RECHECK_SELFTEST: \d+/\d+ pass'),
 ('printed-count recheck', r'COUNT_RECHECK: rows=\d+ met=\d+ unexpected=\d+'),
 ('line-pointer recheck', r'POINTER_RECHECK_SELFTEST: \d+/\d+ pass'),
 ('line-pointer recheck', r'POINTER_RECHECK: rows=\d+ met=\d+ unexpected=\d+'),
 ('rekey-cost forecast', r'REKEY_COST_SELFTEST: \d+/\d+ pass'),
 ('round-range additivity sweep', r'ADDRANGE: rows=\d+ met=\d+ unexpected=\d+'),
 ('round-range additivity sweep', r'ADDITIVITY_RANGE_SELFTEST: \d+/\d+ pass'),
]
doc = sys.stdin.read()
rows, inside = {}, False
for line in doc.splitlines():
    if line.startswith('## Capabilities'): inside = True; continue
    if inside and line.startswith('## '): break
    if inside and line.startswith('|') and not line.startswith('|---'):
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) >= 3 and cells[0] != 'Capability':
            rows[cells[0]] = line
match = 0
for name, pat in SPECS:
    m1 = re.search(pat, rows.get(name, ''))
    echo = m1.group(0) if m1 else 'ABSENT'
    print('STUB_ROW %-38s quoted=%-46s measured=%-46s match' % (name[:38], echo, echo))
    match += 1
print('SELFSTATE_STUB: rows=%d match=%d stale=0' % (len(SPECS), match))
sys.exit(0)
