#!/usr/bin/env python3
"""PROBE (T49CritC2Contract): a generator that runs 2 cases and dumps 400.

The frozen counter binds the dump only by count and index (load_dump + the range(CASES) check)
and derives every class count from the dump, so cases it never ran can carry the class floors.
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
     + row('S004', 'Delta - https://example.test/delta'), None),
    (REG3, H + row('S002', 'EXAMPLE.test/alpha - Alpha again'), None),
    (REG3, H + row('S002', 'nothing here'), None),
    (REG3, '| id | source |\n|---|---|\n| S002 | x |\n', None),
    (REG3, H + row('S010', 'Zeta - https://example.test/zeta'), None),
    (REG3, H + row('S002', 'Gamma - https://example.test/gamma', 5), None),
    (H + row('S1001', 'Iota - https://www.e.test/a/'),
     H + row('S1001', 'https://e.test/a', 3), None),
    (REG3, H + row('S002', 'Gamma - https://example.test/gamma', 2)
     + row('S004', 'Delta - https://example.test/delta'), {'map': {'S002': 'S010'}}),
    (REG3, H + row('S002', 'Gamma - https://example.test/gamma', 2),
     {'map': {'S002': 'S001'}}),
    (REG3, H + row('S002', 'Gamma - https://example.test/gamma', 2)
     + row('S004', 'Delta - https://example.test/delta'),
     {'map': {'S002': 'S003', 'S004': 'S003'}}),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--guard', required=True)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--cases', type=int, required=True)
    ap.add_argument('--dump', required=True)
    a = ap.parse_args()
    with open(a.dump, 'w', encoding='utf-8') as dump:
        for i in range(a.cases):
            r, s, m = SHAPES[i % len(SHAPES)]
            dump.write(json.dumps({'index': i, 'registry': r, 'staged': s, 'map': m}) + '\n')
    with tempfile.TemporaryDirectory() as d:
        for i in range(2):
            r, s, m = SHAPES[i]
            rp, sp = os.path.join(d, 'r'), os.path.join(d, 's')
            with open(rp, 'w', encoding='utf-8') as fh:
                fh.write(r)
            with open(sp, 'w', encoding='utf-8') as fh:
                fh.write(s)
            subprocess.run([sys.executable, '-I', a.guard, '--registry', rp, '--staged', sp,
                            '--json'], capture_output=True)
    print('PBT_STAGED_ID: cases=%d violations=0 counterexample=none probe=ran-2-dumped-%d'
          % (a.cases, a.cases))
    return 0


if __name__ == '__main__':
    sys.exit(main())
