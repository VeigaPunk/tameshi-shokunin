#!/usr/bin/env python3
"""Differential harness: independent oracle vs tools/rekey-cost.py.

Runs both over deterministic arms drawn from the committed ledger's own
input keys (plus paths no entry pins), comparing at_risk and the exact
at-risk heading set.  Output is one ARm line per case plus AGREED/MISMATCH.
"""

import json
import os
import random
import re
import subprocess
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(SEAT, '..', '..', '..', '..', '..'))
LEDGER = os.path.join(REPO, '.ufo', 'evidence', 'round-21', 'coldread', 'ledger.json')
IGNORED = {'SKILL.md', '.ufo/evidence/round-17/coldread/ledger.json',
           '.ufo/evidence/round-21/coldread/ledger.json'}
ORACLE = os.path.join(SEAT, 'oracle.py')
TOOL = os.path.join(REPO, 'tools', 'rekey-cost.py')
RISK_RE = re.compile(r'^RISK (.*?)(?: \| pins=.*)?$')


def run(cmd):
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True,
                       encoding='utf-8', env={'PATH': os.environ['PATH'],
                                              'LC_ALL': 'C.UTF-8'})
    return p.returncode, p.stdout, p.stderr


def oracle(paths):
    args = [sys.executable, '-I', ORACLE, '--repo', REPO, '--detail']
    for p in paths:
        args += ['--edit', p]
    rc, out, err = run(args)
    at = None
    heads = set()
    for line in out.splitlines():
        m = RISK_RE.match(line)
        if m and line.startswith('RISK '):
            heads.add(m.group(1))
        m2 = re.match(r'^ORACLE at_risk=(\d+) sections=(\d+)$', line)
        if m2:
            at, secs = int(m2.group(1)), int(m2.group(2))
    assert at is not None, (rc, out, err)
    return at, secs, heads


def tool(paths):
    args = [sys.executable, '-I', TOOL]
    for p in paths:
        args += ['--edit', p]
    rc, out, err = run(args)
    at = None
    secs = None
    heads = set()
    for line in out.splitlines():
        m = re.match(r'^RISK (.*?) \| pins=.*$', line)
        if m:
            heads.add(m.group(1))
        m2 = re.match(r'^REKEY_COST sections=(\d+) planned=(\d+) at_risk=(\d+) predicted_lost=(\d+)$', line)
        if m2:
            secs, at = int(m2.group(1)), int(m2.group(3))
    assert at is not None, (rc, out, err)
    return at, secs, heads


def arms():
    led = json.load(open(LEDGER, encoding='utf-8'))
    keys = set()
    for e in led['entries']:
        keys |= set(e.get('inputs') or {})
    keys -= IGNORED
    keys = sorted(keys)
    rnd = random.Random(72)
    picks = ['corpus/SOURCES.md', 'PROVINCE.md', 'corpus/QUALITY.md',
             'SCORECARD.md', 'tools/pointer-recheck.json',
             'LOG.md', 'tools/rekey-cost.py',
             '.ufo/evidence/round-72/w1/T72W1S01/oracle.py']
    picks += rnd.sample(keys, 22)
    singles = [[p] for p in picks]
    multis = [['corpus/SOURCES.md', 'PROVINCE.md'],
              ['corpus/QUALITY.md', 'SCORECARD.md'],
              ['PROVINCE.md', 'LOG.md'],
              ['corpus/SOURCES.md', 'corpus/QUALITY.md', 'PROVINCE.md'],
              ['tools/pointer-recheck.json', 'LOG.md']]
    for m in multis:
        picks += m
    return singles + multis, sorted(set(picks))


def main():
    cases, picks = arms()
    bad = 0
    for paths in cases:
        oa, osecs, oheads = oracle(paths)
        ta, tsecs, theads = tool(paths)
        ok = (oa == ta) and (oheads == theads)
        if not ok:
            bad += 1
        label = '+'.join(paths)
        print('%s %-80s oracle=%d tool=%d sections=%d/%d'
              % ('AGREE' if ok else 'MISMATCH', label, oa, ta, osecs, tsecs))
        if not ok:
            print('  oracle-only: %s' % sorted(oheads - theads))
            print('  tool-only:   %s' % sorted(theads - oheads))
    print('DIFFERENTIAL cases=%d agree=%d mismatch=%d distinct_paths=%d'
          % (len(cases), len(cases) - bad, bad, len(picks)))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
