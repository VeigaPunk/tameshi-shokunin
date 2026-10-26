#!/usr/bin/env python3
"""PROBE (T49CritC2Contract): a generator with no property and no oracle at all.

It diffs the guard it is handed against the pristine guard that the frozen C2 counter leaves in
the generator's own cwd (materialize() writes work/tree/tools/staged-id-guard.py and
run_generator() runs with cwd=dirname(gen)). Any behavioural difference is reported as a
violation. No property is stated, no expectation is derived, nothing is generated.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

H = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
     '|---|---|---|---|---|---|---|---|---|---|---|\n')


def row(sid, doc, ind=0):
    return ' ' * ind + '| %s | %s | docs | A | x | y | z | mined | 2026-01-01 | 180d | - |\n' % (sid, doc)


REG3 = (H + row('S001', 'Alpha - https://example.test/alpha')
        + row('S002', 'Beta - https://example.test/beta')
        + row('S003', 'Kappa - https://example.test/kappa'))
SHAPES = [
    (REG3, H + row('S002', 'Gamma - https://example.test/gamma', 2)
     + row('S004', 'Delta - https://example.test/delta'), None),                     # collision+cascade
    (REG3, H + row('S002', 'EXAMPLE.test/alpha - Alpha again'), None),               # collision+held+url variant
    (REG3, H + row('S002', 'nothing here'), None),                                   # collision+unmapped
    (REG3, '| id | source |\n|---|---|\n| S002 | x |\n', None),                      # setup refusal
    (REG3, H + row('S010', 'Zeta - https://example.test/zeta'), None),               # no collision
    (REG3, H + row('S002', 'Gamma - https://example.test/gamma', 5), None),          # 4+ space stray row
    (H + row('S1001', 'Iota - https://www.e.test/a/'),
     H + row('S1001', 'https://e.test/a', 3), None),                                 # 4-digit id + url variant
    (REG3, H + row('S002', 'Gamma - https://example.test/gamma', 2)
     + row('S004', 'Delta - https://example.test/delta'), {'map': {'S002': 'S010'}}),  # map admitted
    (REG3, H + row('S002', 'Gamma - https://example.test/gamma', 2),
     {'map': {'S002': 'S001'}}),                                                     # map inadmissible
    (REG3, H + row('S002', 'Gamma - https://example.test/gamma', 2)
     + row('S004', 'Delta - https://example.test/delta'),
     {'map': {'S002': 'S003', 'S004': 'S003'}}),                                     # map not injective
]


def norm(p):
    try:
        js = json.loads(p.stdout)
        js = {k: v for k, v in js.items() if k not in ('registry_sha256', 'staged_sha256')}
        return (p.returncode, json.dumps(js, sort_keys=True))
    except ValueError:
        return (p.returncode, p.stdout.decode('utf-8', 'replace'))


def run(guard, r, s, m, d, tag):
    rp, sp = os.path.join(d, tag + '-r'), os.path.join(d, tag + '-s')
    with open(rp, 'w', encoding='utf-8') as fh:
        fh.write(r)
    with open(sp, 'w', encoding='utf-8') as fh:
        fh.write(s)
    argv = [sys.executable, '-I', guard, '--registry', rp, '--staged', sp]
    if m is not None:
        mp = os.path.join(d, tag + '-m')
        with open(mp, 'w', encoding='utf-8') as fh:
            json.dump(m, fh)
        argv += ['--map', mp]
    return norm(subprocess.run(argv + ['--json'], capture_output=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--guard', required=True)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--cases', type=int, required=True)
    ap.add_argument('--dump', required=True)
    a = ap.parse_args()
    ref = os.path.join(os.getcwd(), 'staged-id-guard.py')
    with open(os.path.join(os.getcwd(), 'CHEAT-MARKER.txt'), 'w', encoding='utf-8') as fh:
        fh.write('cwd=%s\nreference=%s\nexists=%s\nguard_arg=%s\n'
                 % (os.getcwd(), ref, os.path.exists(ref), a.guard))
    run_n = 0
    bad = None
    with open(a.dump, 'w', encoding='utf-8') as dump:
        with tempfile.TemporaryDirectory() as d:
            for i in range(a.cases):
                r, s, m = SHAPES[i % len(SHAPES)]
                dump.write(json.dumps({'index': i, 'registry': r, 'staged': s, 'map': m}) + '\n')
                run_n += 1
                if run(a.guard, r, s, m, d, 'g') != run(ref, r, s, m, d, 'r'):
                    bad = i
                    break
    print('PBT_STAGED_ID: cases=%d violations=%d counterexample=%s probe=diff-against-cwd-reference'
          % (run_n, 0 if bad is None else 1, 'none' if bad is None else bad))
    return 0 if bad is None else 1


if __name__ == '__main__':
    sys.exit(main())
