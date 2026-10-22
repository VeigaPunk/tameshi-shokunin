#!/usr/bin/env python3
"""Round-25 C1 input-pin check — closes the vacuity holes the wave seats
MeasureVacuity and C1Framing found in the frozen counter c1-measure.py, without
changing the frozen counter:

  python3 .ufo/evidence/round-25/c1-pins.py --repo CLONE_AT_REV

Checks, all over git-tracked bytes at the clone's HEAD:
  P1 every file the counter stages or reads has the sha256 recorded in
     contract-amendment-2.json (runner, gate, suite, fixtures, both specs,
     round-23/24 fixture files, round-23 outcomes file, the counter itself);
  P2 the specs carry exactly the defect ids M1-M10 and G1-G14;
  P3 the disposition population is exactly the 34 non-completed round-23 wave-2 seats;
  P4 every disposition row names its canonical seat TameshiR25.Re<name> (present in
     the committed wave dispatch) and, when re-attacked, the canonical git-tracked
     report path .ufo/waves/round-25/w1/Re<name>.md;
  P5 each label has exactly one SCORECARD table row, and it reads `| R23-ROUTED-n | dispositioned | ...`.
Exit 0 all hold · 1 any fails · 2 setup.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

E = '.ufo/evidence/round-25'


def tracked(repo, rel):
    return subprocess.run(['git', '-C', str(repo), 'ls-files', '--error-unmatch', rel],
                          capture_output=True).returncode == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True, type=Path)
    repo = parser.parse_args().repo.resolve()
    try:
        pins = json.loads((repo / E / 'contract-amendment-2.json').read_text())['c1_input_sha256']
        disp = json.loads((repo / E / 'dead-falsifier-disposition.json').read_text())['rows']
        outcomes = json.loads((repo / '.ufo/waves/round-23/original-outcomes2.json').read_text())
        seats = {t['name'] for t in json.loads((repo / '.ufo/waves/round-25/dispatch.json').read_text())['taskCall']['tasks']}
        scorecard = (repo / 'SCORECARD.md').read_text()
    except (OSError, ValueError, KeyError) as exc:
        print('C1_PINS: SETUP (%s)' % exc)
        return 2
    failures = []
    for rel, want in sorted(pins.items()):
        path = repo / rel
        got = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if got != want or not tracked(repo, rel):
            failures.append('P1 %s sha256 %s != %s or untracked' % (rel, got, want))
    ids = {spec: re.findall(r'^@defect (\S+)', (repo / E / spec).read_text(), re.M)
           for spec in ('multitoken-mutants.spec', 'guard-mutants.spec')}
    if ids['multitoken-mutants.spec'] != ['M%d' % i for i in range(1, 11)]:
        failures.append('P2 multitoken ids %s' % ids['multitoken-mutants.spec'])
    if ids['guard-mutants.spec'] != ['G%d' % i for i in range(1, 15)]:
        failures.append('P2 guard ids %s' % ids['guard-mutants.spec'])
    dead = sorted(r['name'] for r in outcomes['rows'] if r['status'] != 'completed')
    if len(dead) != 34 or sorted(r['name'] for r in disp) != dead:
        failures.append('P3 population %d dead, %d rows' % (len(dead), len(disp)))
    for r in disp:
        if r.get('seat') != 'TameshiR25.Re' + r['name'] or ('Re' + r['name']) not in seats:
            failures.append('P4 %s seat %s' % (r['name'], r.get('seat')))
        if r['status'] != 'reattack-seat-died':
            rel = '.ufo/waves/round-25/w1/Re%s.md' % r['name']
            if r.get('report') != rel or not tracked(repo, rel):
                failures.append('P4 %s report %s not canonical or untracked' % (r['name'], r.get('report')))
    for n in (1, 2, 3):
        rows = re.findall(r'^\| R23-ROUTED-%d \|[^\n]*$' % n, scorecard, re.M)
        if len(rows) != 1 or not rows[0].startswith('| R23-ROUTED-%d | dispositioned |' % n):
            failures.append('P5 SCORECARD row R23-ROUTED-%d: %d rows' % (n, len(rows)))
    counts = {}
    for r in disp:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    print(json.dumps({'failures': failures, 'pinned_files': len(pins), 'disposition_counts': counts},
                     indent=1, sort_keys=True))
    print('C1_PINS: %s (%d failures)' % ('HOLD' if not failures else 'FAIL', len(failures)))
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
