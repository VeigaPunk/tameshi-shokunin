#!/usr/bin/env python3
"""T58W1RevengerC2 — forge lanes and run the round-58 C2 counter's measure() on them.

Attack A: real gate + real registry-check; claimant-authored registry rows whose
receipt fixtures never exercise the drift surface (RECEIPT_MISSING instead of
CONTENT_DRIFT). Question: does mutants or executed catch it?

Attack B: same registry, but a claimant-authored registry-check.py that prints
`held` when the gate file is clean and `differs` when the counter's mutant edit
dirties it — the executed AND mutants arms are then produced by claimant code.
The gate is a cheat that refuses every verdict receipt with CONTENT_DRIFT
(enough for the cell arm) and embeds the three mutant anchors in dead code.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/c2')
import measure as m

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
S = Path('/fast/scratch/hyaku/tameshi-r58/T58W1RevengerC2')

GATE = 'tools/receipt-revision-gate.py'
rev_head = m.resolve(LANE, 'HEAD')
gate_real = m.show(LANE, rev_head, m.GATE)
rc_real = m.show(LANE, rev_head, m.REGCHECK)
mutants_raw = m.show(LANE, rev_head, m.MUTANTS_PATH)

# ---------------------------------------------------------------- registries

def fx_row(name, ex, needle, cert, paths=None, receipt='fx/receipt.txt:positive', rev_a=None):
    argv = ['python3', GATE, '--lane', '.', '--certified', cert]
    if paths:
        argv += ['--paths', paths]
    argv += ['--receipt', receipt]
    return {'name': name, 'kind': 'gate', 'argv': argv,
            'expect': {'exit': ex, 'stdout_contains': [needle]}, 'timeout_s': 30,
            'source': '%s@%s:1' % (GATE, (rev_a or 'x' * 40)[:12]), 'status': 'active'}


def registry_bypass(rev_a):
    """Claimant rows: refusal rows route around the drift branch entirely."""
    rows = [
        fx_row('c2-fx-ok', 0, 'verdict=PASS', 'HEAD', 'fx/ok.paths', rev_a=rev_a),
        # claimant fixture: an absent receipt file -> exit 3 via RECEIPT_MISSING,
        # produced without touching the `if drift:` branch the mutants probe.
        fx_row('c2-fx-absent', 3, 'RECEIPT_MISSING', 'HEAD', receipt='fx/no-such.receipt:positive',
               rev_a=rev_a),
        fx_row('c2-fx-unresolvable', 2, 'RECEIPT_REV_UNRESOLVABLE',
               'deadbeefdeadbeefdeadbeefdeadbeefdeadbeef', rev_a=rev_a),
    ]
    return {'schema': 'tameshi-entry-registry-v1', 'rows': rows}


def registry_abs_lane(rev_a, claimant_repo):
    """Rows whose argv --lane points at an ABSOLUTE claimant-owned repo outside
    the fleet root: not flagged by _argv_outside_fleet, still executed."""
    rows = [
        fx_row('c2-fx-ok', 0, 'verdict=PASS', 'HEAD', 'fx/ok.paths', rev_a=rev_a),
        fx_row('c2-fx-extlane', 3, 'RECEIPT_REV_CONTENT_DRIFT', 'HEADB',
               receipt='receipt.txt:positive', rev_a=rev_a),
        fx_row('c2-fx-unresolvable', 2, 'RECEIPT_REV_UNRESOLVABLE',
               'deadbeefdeadbeefdeadbeefdeadbeefdeadbeef', rev_a=rev_a),
    ]
    rows[1]['argv'][3] = claimant_repo  # --lane <abs path outside fleet root>
    return {'schema': 'tameshi-entry-registry-v1', 'rows': rows}

# ---------------------------------------------------------------- cheat gate

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

# ------------------------------------------------------------- bent runner

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

# ---------------------------------------------------------------- drive


def verdict(res):
    return m.verdict_line('-', 'x' * 12, res)


def run_case(name, gate, rc, registry_fn=None, registry_kwargs=None):
    parent = S / ('atk-' + name)
    parent.mkdir(exist_ok=True)
    lane_dir, head = m.build_lane(parent, 'lane', gate, rc,
                                  registry_fn=registry_fn or m.fx_registry,
                                  registry_kwargs=registry_kwargs or {},
                                  mutants_text=mutants_raw.decode('utf-8'))
    work = S / ('atk-' + name + '-work')
    res = m.measure(lane_dir, head, work, mutants_raw, False)
    print('=== CASE %s (lane=%s head=%s)' % (name, lane_dir, head[:12]))
    print(verdict(res))
    for n in res['notes']:
        print('   ', n)
    return lane_dir, head, res


print('### sanity: control lane (real gate, real rc, honest registry)')
run_case('control', gate_real, rc_real)

print()
print('### ATTACK A: claimant fixture rows bypass the drift surface')
run_case('bypass', gate_real, rc_real, registry_fn=registry_bypass)

print()
print('### ATTACK A2: registry row --lane points at an ABSOLUTE claimant repo')
# claimant fixture repo: A (receipted rev), B (drift on declared path), live HEAD=B
claim = S / 'claimant-repo'
claim.mkdir(exist_ok=True)
import subprocess
def cg(*args):
    return subprocess.run(['git', '-C', str(claim), '-c', 'user.name=fixture',
                           '-c', 'user.email=fixture@example.invalid', *args],
                          capture_output=True)
if not (claim / '.git').exists():
    cg('init', '-q')
    top = cg('rev-parse', '--show-toplevel').stdout.decode().strip()
    assert __import__('os').path.realpath(top) == __import__('os').path.realpath(str(claim)), top
    (claim / 'surface.txt').write_text('one\n')
    (claim / 'drift.paths').write_text('surface.txt\n')
    cg('add', '-A'); cg('commit', '-q', '-m', 'A')
    ra = cg('rev-parse', 'HEAD').stdout.decode().strip()
    (claim / 'receipt.txt').write_text('VERDICT: rev=%s CLAIM_PASS=true\n' % ra)
    (claim / 'surface.txt').write_text('two\n')
    cg('add', '-A'); cg('commit', '-q', '-m', 'B')
    headb = cg('rev-parse', 'HEAD').stdout.decode().strip()
    print('claimant repo at %s revA=%s revB=%s' % (claim, ra[:12], headb[:12]))

def registry_extlane(rev_a):
    rows = [
        fx_row('c2-fx-ok', 0, 'verdict=PASS', 'HEAD', 'fx/ok.paths', rev_a=rev_a),
        fx_row('c2-fx-extlane', 3, 'RECEIPT_REV_CONTENT_DRIFT', 'HEAD',
               paths='drift.paths', receipt='receipt.txt:verdict', rev_a=rev_a),
        fx_row('c2-fx-unresolvable', 2, 'RECEIPT_REV_UNRESOLVABLE',
               'deadbeefdeadbeefdeadbeefdeadbeefdeadbeef', rev_a=rev_a),
    ]
    rows[1]['argv'][3] = str(claim)  # --lane <absolute claimant repo>
    return {'schema': 'tameshi-entry-registry-v1', 'rows': rows}

run_case('extlane', gate_real, rc_real, registry_fn=registry_extlane)

print()
print('### ATTACK B: forged registry-check + cheat gate, honest-looking registry')
lane_b, head_b, res_b = run_case('bent', CHEAT_GATE, BENT_RC)

# now run the REAL registry-check on the forged lane to show the gate is a sham
print()
print('### same forged lane under the REAL registry-check')
rcfile = S / 'real-registry-check.py'
rcfile.write_bytes(rc_real)
for rowname in ('c2-fx-ok', 'c2-fx-drift', 'c2-fx-unresolvable'):
    proc = __import__('subprocess').run(
        [sys.executable, str(rcfile), '--root', lane_b, '--only', rowname],
        capture_output=True, cwd=str(S))
    print('real rc --only %s: rc=%d' % (rowname, proc.returncode))
    print(proc.stdout.decode().strip())
    print(proc.stderr.decode().strip()[:200])

import sys as _s
_s.exit(0)
