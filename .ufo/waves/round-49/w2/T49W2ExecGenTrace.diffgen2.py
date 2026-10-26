#!/usr/bin/env python3
"""Positive control for the trace method: a DIFFERENTIAL generator with no property.

No oracle, no expectation: for each case it runs `--guard` and `./staged-id-guard.py`
(the guard sitting in the generator's own cwd) and reports the first difference.
Every case is built so the collapse mutant (refused = bool(unmapped), cascade dropped)
differs from the pristine guard, so this control reproduces the wave-1 F1 cheat shape.
Used only to prove that the strace filter of the deliverable would have caught a read
of the pristine guard.
"""
import argparse
import json
import os
import random
import subprocess
import sys
import tempfile

HEAD = '| id | source | kind | tier | scope |\n|---|---|---|---|---|\n'


def rows(ids):
    return ''.join('| S%03d | https://d%d.test/x | doc | t | s |\n' % (n, n) for n in ids)


def shape(rnd):
    ids = sorted(rnd.sample(range(2, 40), rnd.randint(1, 3)))
    top = ids[-1]
    reg = HEAD + rows(ids)
    st = HEAD + rows([ids[0], top + 1])     # collision on ids[0]; naive target top+1 staged
    return {'registry': reg, 'staged': st, 'map': None}


def run(guard, d, case):
    rp = os.path.join(d, 'r.md')
    sp = os.path.join(d, 's.md')
    open(rp, 'w').write(case['registry'])
    open(sp, 'w').write(case['staged'])
    p = subprocess.run([sys.executable, '-I', guard, '--registry', rp, '--staged', sp,
                        '--json'], capture_output=True, cwd=d)
    return p.returncode, p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--guard')
    ap.add_argument('--seed', type=int)
    ap.add_argument('--cases', type=int)
    ap.add_argument('--dump')
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    work = tempfile.mkdtemp(prefix='diffgen-')
    d = os.path.join(work, 'case')
    os.makedirs(d)
    violations = 0
    dump = open(a.dump, 'w')
    ran = 0
    for i in range(a.cases):
        case = shape(rnd)
        dump.write(json.dumps({'index': i, 'registry': case['registry'],
                               'staged': case['staged'], 'map': None}) + '\n')
        ran += 1
        mine = run(a.guard, d, case)
        ref = run(os.path.join(os.getcwd(), 'staged-id-guard.py'), d, case)
        if mine != ref:
            violations += 1
            break
    dump.close()
    print('PBT_STAGED_ID: cases=%d violations=%d counterexample=%s'
          % (ran, violations, 'none' if violations == 0 else '0'))
    return 0 if violations == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
