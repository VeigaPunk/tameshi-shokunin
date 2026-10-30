#!/usr/bin/env python3
"""T58W2MutC2: reproduce wave-1's decisive bent-runner forgery (ATTACK B of
T58W1RevengerC2) against the PRISTINE round-58 C2 counter, entirely inside this
scratch dir, as independent evidence. The frozen lane target is not touched:
the forged lane is a throwaway fixture built from the counter's own build_lane,
with the cheat gate and the bent registry-check committed as its tools.

BENT_RC never executes a row: on a clean gate worktree it prints
`ROW <name> expect=E got=E held` for whatever the registry expects; only when
the counter dirties the gate (mutants arm) does it print a fabricated
`differs` with an integer got, which the counter credits as mutant kills.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r58/T58W2MutC2')
C0 = '8063d0a551fc5b3cb5a2d397da7353af53444534'

spec = importlib.util.spec_from_file_location('m', S / 'cnt' / 'measure.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

mutants_raw = (S / 'cnt' / 'mutants.json').read_bytes()
assert len(m.load_mutants(mutants_raw)) == 3

CHEAT_GATE = b'''#!/usr/bin/env python3
"""claimant gate: resolves --certified but never reads receipts or diffs paths."""
import re
import subprocess
import sys

CODES = (
    'RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_NOT_BLOB', 'RECEIPT_REV_ABSENT',
    'RECEIPT_REV_AMBIGUOUS', 'RECEIPT_REV_UNRESOLVABLE', 'RECEIPT_REV_MISMATCH',
    'RECEIPT_REV_CONTENT_DRIFT', 'RECEIPT_CONTROL_NOT_ANCESTOR',
    'RECEIPT_DIGEST_MISMATCH', 'RECEIPT_REQUIRED_LINE_MISSING',
)

_ANCHORS = """
                if drift:
                    codes.append('RECEIPT_REV_CONTENT_DRIFT')
"""


def main(argv):
    args = {}
    i = 0
    while i < len(argv):
        if argv[i].startswith('--'):
            args[argv[i]] = argv[i + 1]
            i += 2
        else:
            i += 1
    lane, certified = args['--lane'], args['--certified']


    receipts = [v for k, v in args.items() if k == '--receipt']
    proc = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', '--quiet',
                           certified + '^{commit}'], capture_output=True)
    if proc.returncode != 0:
        print('GATE: error=unresolvable-certified receipts=%d verdict=REFUSED codes=RECEIPT_REV_UNRESOLVABLE'
              % len(receipts))
        return 2
    for tok in receipts:
        path, role = tok.split(':')[:2]
        if role == 'verdict':
            print('GATE REFUSED %s role=%s revs=%s code=RECEIPT_REV_CONTENT_DRIFT detail=sham'
                  % (path, role, certified[:12]))
            print('GATE: receipts=%d ok=0 refused=%d codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED'
                  % (len(receipts), len(receipts)))
            return 3
        print('GATE OK %s role=%s revs=%s' % (path, role, certified[:12]))
    print('GATE: receipts=%d ok=%d refused=0 codes=none verdict=PASS'
          % (len(receipts), len(receipts)))
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        sys.exit(0)
    sys.exit(main(sys.argv[1:]))
'''

BENT_RC = b'''#!/usr/bin/env python3
"""claimant registry-check: reports rows held on a clean worktree and differs
when tools/receipt-revision-gate.py is dirty (i.e. the counter wrote a mutant).
Never executes a row."""
import json
import os
import subprocess
import sys


def main(argv):
    root = only = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--root':
            i += 1
            root = argv[i]
        elif a == '--only':
            i += 1
            only = argv[i]
        i += 1
    reg = json.load(open(os.path.join(root, 'tools', 'registry.json')))
    row = next(r for r in reg['rows'] if r['name'] == only)
    expect = row['expect']['exit']
    dirty = subprocess.run(
        ['git', '-C', root, 'status', '--porcelain', '--',
         'tools/receipt-revision-gate.py'],
        capture_output=True).stdout.strip()
    if dirty:
        got = (expect + 1) if isinstance(expect, int) else 1
        print('ROW %s expect=%s got=%s differs' % (only, expect, got))
        print('REGISTRY_CHECK: held=0/1 superseded=0')
        return 1
    print('ROW %s expect=%s got=%s held' % (only, expect, expect))
    print('REGISTRY_CHECK: held=1/1 superseded=0')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
'''

parent = S / 'atk-bent'
parent.mkdir(exist_ok=True)
lane_dir, head = m.build_lane(parent, 'lane', CHEAT_GATE, BENT_RC,
                              mutants_text=mutants_raw.decode('utf-8'))
work = S / 'atk-bent-work'
res = m.measure(lane_dir, head, work, mutants_raw, False)
print('=== forged lane (cheat gate + bent registry-check committed) head=%s' % head[:12])
print(m.verdict_line('-', 'x' * 12, res))
for n in res['notes']:
    print('    ' + n)
print()
print('### the same forged lane under the REAL registry-check (bytes from clone@C0)')
rc_real = m.show(str(S / 'clone'), C0, m.REGCHECK)
assert rc_real is not None
rcfile = S / 'real-registry-check.py'
rcfile.write_bytes(rc_real)
for rowname in ('c2-fx-ok', 'c2-fx-drift', 'c2-fx-unresolvable'):
    proc = subprocess.run([sys.executable, str(rcfile), '--root', lane_dir, '--only', rowname],
                          capture_output=True)
    print('real rc --only %s: rc=%d' % (rowname, proc.returncode))
    print(proc.stdout.decode('utf-8', 'replace').strip())
