#!/usr/bin/env python3
"""T56W2MutGateOnC0 — re-run the wave-1 gate mutant set against the C0 gate.

One exact byte-edit per mutant, applied to a fresh scratch clone of the lane at
C0. Each mutant is then killed (or not) by the gate's own `--selftest`.
Pristine bytes are restored after every mutant and the hash re-asserted.

Nothing in the lane is written; the only writes are inside the scratch clones.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W2MutGateOnC0')
LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
C0 = 'c0137451f5b7f22d65f748fc69f1b181f55e1378'
GATE_REL = 'tools/receipt-revision-gate.py'

# The eight mutants, each a single exact string replacement against the C0 bytes.
MUTANTS = [
    ('M1', 'drop-RECEIPT_REV_ABSENT',
     "    if not revs:\n        codes.append('RECEIPT_REV_ABSENT')",
     "    if False and not revs:\n        codes.append('RECEIPT_REV_ABSENT')",
     'absent-refused'),
    ('M2', 'drifted_paths-returns-empty',
     "    return [p for p in r.stdout.decode().splitlines() if p] + gone",
     "    return []",
     'content-drift-refused'),
    ('M3', 'is_ancestor-always-true',
     "    return git(['-C', lane, 'merge-base', '--is-ancestor', older, newer]).returncode == 0",
     "    return True",
     'control-not-ancestor-refused'),
    ('M4', 'skip-digest-check',
     "        if want != got:\n            codes.append('RECEIPT_DIGEST_MISMATCH')",
     "        if False and want != got:\n            codes.append('RECEIPT_DIGEST_MISMATCH')",
     'digest-mismatch-refused'),
    ('M5', 'allow-multiple-revs-in-positive-role',
     "        if len(revs) > 1:\n            codes.append('RECEIPT_REV_AMBIGUOUS')",
     "        if False and len(revs) > 1:\n            codes.append('RECEIPT_REV_AMBIGUOUS')",
     'ambiguous-refused'),
    ('M6', 'skip-required-line-check',
     "    if regex is not None and not re.search(regex, text, re.M):",
     "    if False and regex is not None and not re.search(regex, text, re.M):",
     'required-line-refused'),
    ('M7', 'empty-file-treated-as-present',
     "    if not data.strip():\n        return ['RECEIPT_EMPTY'], 'path=%s' % path, None",
     "    if False and not data.strip():\n        return ['RECEIPT_EMPTY'], 'path=%s' % path, None",
     'empty-refused'),
    ('M8', 'drop-RECEIPT_CONTROL_NOT_ANCESTOR',
     "            codes.append('RECEIPT_CONTROL_NOT_ANCESTOR')",
     "            pass  # mutant: drop RECEIPT_CONTROL_NOT_ANCESTOR",
     'control-not-ancestor-refused'),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_selftest(gate):
    env = dict(os.environ)
    env.update(HOME='/tmp', GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               GIT_DIR='/nonexistent', GIT_WORK_TREE='/nonexistent')
    r = subprocess.run([sys.executable, str(gate), '--selftest'],
                       capture_output=True, text=True, env=env, timeout=600)
    return r


def parse(out):
    m = re.search(r'GATE_SELFTEST: (\d+)/(\d+) pass', out)
    tally = (int(m.group(1)), int(m.group(2))) if m else None
    failed = re.findall(r'^CASE (\S+) FAIL$', out, re.M)
    return tally, failed


results = []
baseline = None

for mid, name, old, new, expect_case in MUTANTS:
    clone = S / ('m' + mid[1:])
    gate = clone / GATE_REL
    assert clone.is_dir(), clone
    head = subprocess.run(['git', '-C', str(clone), 'rev-parse', 'HEAD'],
                          capture_output=True, text=True).stdout.strip()
    top = subprocess.run(['git', '-C', str(clone), 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    assert head == C0, (mid, head)
    assert top == str(clone), (mid, top)

    pristine = gate.read_bytes()
    ph = sha(pristine)
    if baseline is None:
        r = run_selftest(gate)
        baseline = parse(r.stdout)
        (S / 'baseline-selftest.stdout').write_text(r.stdout)
        (S / 'baseline-selftest.stderr').write_text(r.stderr)
        print('BASELINE %s exit=%d' % (baseline, r.returncode))
        if baseline[0][0] != baseline[0][1]:
            print('BASELINE FAILS — every mutant is inconclusive')
            sys.exit(3)

    count = pristine.count(old.encode())
    if count != 1:
        results.append({'id': mid, 'name': name, 'error': 'old string occurs %d times' % count})
        print('%-3s SKIP  old-string-count=%d' % (mid, count))
        continue

    mutated = pristine.replace(old.encode(), new.encode(), 1)
    gate.write_bytes(mutated)
    mh = sha(mutated)
    r = run_selftest(gate)
    tally, failed = parse(r.stdout)
    stderr_head = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''
    verdict = 'KILLED' if (tally and tally[0] < baseline[0][0]) else 'SURVIVED'
    print('%-3s %-8s %s failed=%s expect=%s' % (mid, verdict, tally, failed, expect_case))
    if stderr_head:
        print('      stderr-last: %s' % stderr_head[:200])
    (S / ('mutant-%s.stdout' % mid)).write_text(r.stdout)
    (S / ('mutant-%s.stderr' % mid)).write_text(r.stderr)
    (S / ('mutant-%s.diff' % mid)).write_text(
        '--- pristine %s\n+++ mutant %s\n@@ %s\n%s\n--> %s\n' % (mid, mid, mid, new, mid))

    # restore exact bytes
    gate.write_bytes(pristine)
    rh = sha(gate.read_bytes())
    assert rh == ph, (mid, rh, ph)

    results.append({
        'id': mid, 'name': name, 'expect_case': expect_case,
        'old': old, 'new': new,
        'old_occurrences': count,
        'pristine_sha256': ph, 'mutated_sha256': mh, 'restored_sha256': rh,
        'restored_exact': rh == ph,
        'selftest_tally': '%d/%d' % tally if tally else None,
        'selftest_exit': r.returncode,
        'failing_cases': failed,
        'expected_case_failed': expect_case in failed,
        'verdict': verdict,
        'stderr_last_line': stderr_head[:400],
    })

out = {
    'schema': 'tameshi-mutgate-c0-v1',
    'seat': 'T56W2MutGateOnC0',
    'cand': C0,
    'gate_rel': GATE_REL,
    'gate_sha256_at_c0': sha((S / 'm1' / GATE_REL).read_bytes()),
    'baseline_tally': '%d/%d' % baseline[0],
    'baseline_exit': 0,
    'mutants': results,
}
(S / 'mutants.json').write_text(json.dumps(out, indent=1))
print('WROTE %s' % (S / 'mutants.json'))
for r in results:
    print('%-3s %-8s %s' % (r.get('id'), r.get('verdict'), r.get('selftest_tally')))
