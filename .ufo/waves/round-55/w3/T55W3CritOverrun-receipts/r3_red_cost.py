#!/usr/bin/env python3
"""R3: what would the 'RED floor with a disclosed miss' alternative have cost?

Runs the frozen round-21 credit measure at C0 (the re-key entries do not exist yet at C0,
so this is the no-re-key state) and prints the two terms the round pre-registered.

Usage: python3 r3_red_cost.py LANE   (takes ~60 s; uses TMPDIR)
"""
import json
import os
import subprocess
import sys
import tempfile

LANE = sys.argv[1]
C0 = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
MEASURE = LANE + '/.ufo/evidence/round-21/coldread/measure.py'

with tempfile.TemporaryDirectory() as td:
    env = dict(os.environ, TMPDIR=td)
    out = subprocess.run([sys.executable, MEASURE, '--repo', LANE, '--rev', C0],
                         capture_output=True, text=True, env=env)
d = json.loads(out.stdout)
c = d['coldread']
miss = c['missing']
reasons = {}
for m in miss:
    k = m['reason'].split(':')[0]
    reasons[k] = reasons.get(k, 0) + 1
print('at C0, with no re-key entries: credited=%d/%d score=%d'
      % (c['sections_covered'], c['sections_total'], d['calibration_restraint_score']))
print('missing=%d reasons=%s' % (len(miss), json.dumps(reasons, sort_keys=True)))
print('first three missing:')
for m in miss[:3]:
    print('  - %s : %s' % (m['heading'], m['reason'][:150]))
print('\npre-registered floor (no-harm.sh):')
print(subprocess.run(['sed', '-n', '16,17p', LANE + '/.ufo/evidence/round-55/no-harm.sh'],
                     capture_output=True, text=True).stdout.rstrip())
print('\ndeciding gate on the same floor (deciding-run.sh):')
print(subprocess.run(['sed', '-n', '63p;70,71p', LANE + '/.ufo/evidence/round-55/deciding-run.sh'],
                     capture_output=True, text=True).stdout.rstrip())
ok = d['calibration_restraint_score'] >= 8 and c['sections_covered'] >= 64
print('\nNO_REKEY_MONITOR=%s' % ('ok' if ok else 'RED'))
