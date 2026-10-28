#!/usr/bin/env python3
"""R7: where the 18 re-key readers actually wrote, and what the wave can cash.

The w3 brief (spec-w3.json context) carries w2's reader-discipline line verbatim:
"only the three reader seats", the heading `## Standing rules`, and a write path under
round-55/w2/. This sweep counts the delivered reader JSONs per directory and checks
coverage of the 18 lost headings.

Usage: python3 r7_reader_coverage.py LANE
"""
import glob
import json
import os
import sys
from collections import Counter

LANE = sys.argv[1]
W = LANE + '/.ufo/waves/round-55'
lost = set(json.load(open(LANE + '/.ufo/evidence/round-55/c1/lost-headings-at-c0.json')))
C0 = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'

rows = []
for w in ('w2', 'w3'):
    for p in sorted(glob.glob('%s/%s/T55W3R*.json' % (W, w))):
        d = json.load(open(p))
        rows.append((w, os.path.basename(p), d.get('heading'), len(d.get('findings') or []),
                     d.get('cand') == C0))
print('reader JSONs per directory:', dict(Counter(r[0] for r in rows)), 'total', len(rows))
heads = {r[2] for r in rows}
print('distinct headings read: %d of %d lost' % (len(heads), len(lost)))
print('still unread:', sorted(lost - heads))
print('cand == C0 for every file:', all(r[4] for r in rows))
print('finding-bearing: %d of %d files' % (sum(1 for r in rows if r[3]), len(rows)))
print('binder accepts a finding-bearing reader only up to the resolutions allowance')
print('  (.ufo/evidence/round-55/integrate/binder.py:116-119 -> reader-has-findings:%d>%d)')
print('\nper-file:')
for w, f, h, n, ok in rows:
    print('  %s/%-12s findings=%d cand_c0=%s  %s' % (w, f, n, ok, h[:70]))
