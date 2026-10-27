#!/usr/bin/env python3
"""Round-53 controls, phase A — scored at the freeze bytes before any seat runs.

Usage: controls.py LANE FREEZE WORKDIR
Prints one 'CONTROL <name> <observed> expected=false <pass|FAIL>' line per control;
exit 0 iff every control behaved as pre-registered.

Pre-registered expectations (contract.json):
  CTL_C1_BASE — c1 counter at BASE 6db1d220 must print C1_R53_PASS=false
                (do-nothing control: precheck RED, no rekey-r53 directory)
  CTL_C2_BASE — c2 counter at BASE must print C2_R53_PASS=false
                (do-nothing control: the two inherited dir="/tmp" hardcodes)

The planted-mutant controls for the candidate's break-one arms (rekey trace
removal, reader-sha corruption, read_rev mismatch, planted /tmp, defeated
CR47) are phase B: they run against scratch fixtures built from the POST-FIX
candidate bytes in integrate/break-fixtures.py, before wave 2.  This harness
never writes to the lane; scratch lives under WORKDIR (TMPDIR-honouring).
"""
import os
from pathlib import Path
import re
import subprocess
import sys
import shutil

LANE = sys.argv[1]
FREEZE = sys.argv[2]
WORK = Path(sys.argv[3])
WORK.mkdir(parents=True, exist_ok=True)
BASE = '6db1d220b337c35ff1e25bf9cfd74abc9db1498d'
SCR = WORK / 'controls'
if SCR.exists():
    shutil.rmtree(SCR)
SCR.mkdir(parents=True)
os.environ['TMPDIR'] = str(SCR / 'tmp')
(SCR / 'tmp').mkdir()


def git(args, cwd=LANE, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git'] + args, cwd=cwd, env=env,
                          capture_output=True, text=True)


def show(rev, path):
    return git(['show', '%s:%s' % (rev, path)]).stdout


results = []


def record(name, ok, observed):
    print('CONTROL %s %s expected=false %s' % (name, observed[:110],
                                               'pass' if ok else 'FAIL'))
    results.append(ok)


def run_counter(kind, lane_path, rev, workdir):
    src = show(FREEZE, '.ufo/evidence/round-53/%s/measure.py' % kind)
    p = SCR / ('%s-measure.py' % kind)
    p.write_text(src)
    extra = []
    if kind == 'c1':
        lh = SCR / 'lost-headings.json'
        lh.write_text(show(FREEZE, '.ufo/evidence/round-53/c1/lost-headings.json'))
        extra = ['--explain']
    r = subprocess.run([sys.executable, str(p), '--lane', lane_path,
                        '--rev', rev, '--work', str(workdir)] + extra,
                       capture_output=True, text=True, timeout=3600)
    m = re.search(r'%s_R53_PASS=(true|false)' % kind.upper(),
                  r.stdout or '')
    return (m.group(1) if m else 'none'), (r.stdout or '').strip().split('\n')[-1]


for kind in ('c1', 'c2'):
    verdict, last = run_counter(kind, LANE, BASE, SCR / ('base-%s' % kind))
    record('CTL_%s_BASE' % kind.upper(), verdict == 'false',
           'verdict=%s %s' % (verdict, last[-70:]))

ok = all(results)
print('CONTROLS: total=%d pass=%d' % (len(results), sum(results)))
sys.exit(0 if ok else 1)
