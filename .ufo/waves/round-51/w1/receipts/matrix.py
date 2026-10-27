#!/usr/bin/env python3
"""Emit the observed mutant×detector matrix rows from receipts."""
import os
import re
import sys

S = '/fast/scratch/hyaku/tameshi-r51/T51MutC2Counter'
sys.path.insert(0, S)
import probe

RCPT = os.path.join(S, 'receipts')
MIDS = [m for m, *_ in probe.MUTANTS]


def last_line(fn):
    txt = open(os.path.join(RCPT, fn), encoding='utf-8', errors='replace').read()
    rc = int(re.search(r'^rc=(\d+)', txt, re.M).group(1))
    lines = [l for l in txt.split('\n') if l.startswith('C2_R51:')]
    return rc, lines[-1] if lines else '(no verdict line)'


def selftest_line(fn):
    txt = open(os.path.join(RCPT, fn), encoding='utf-8', errors='replace').read()
    rc = int(re.search(r'^rc=(\d+)', txt, re.M).group(1))
    tail = [l for l in txt.split('\n') if 'SELFTEST:' in l][-1]
    return rc, tail


rows = []
for mid in MIDS:
    rc1, l1 = selftest_line('selftest-%s.txt' % mid)
    d1ok = rc1 == 0 and 'cases=11 failed=0' in l1
    rc2, l2 = last_line('run-%s-ctl0.txt' % mid)
    rc3, l3 = last_line('run-%s-ctlcomment.txt' % mid)
    d2ok = rc2 == 1 and l2.endswith('C2_R51_PASS=false')
    d3ok = rc3 == 1 and l3.endswith('C2_R51_PASS=false')
    kills = []
    if not d1ok:
        kills.append('D1')
    if not d2ok:
        kills.append('D2')
    if not d3ok:
        kills.append('D3')
    verdict = 'KILLED-by-%s' % '/'.join(kills) if kills else 'SURVIVED' if mid != 'M16_recorded_clause_drop' else 'EQUIVALENT'
    print('%-28s D1 rc=%d %s | D2 rc=%d %s | D3 rc=%d %s | %s'
          % (mid, rc1, 'ok' if d1ok else 'FAIL', rc2, 'false' if d2ok else 'DEVIATES',
             rc3, 'false' if d3ok else 'DEVIATES', verdict))
