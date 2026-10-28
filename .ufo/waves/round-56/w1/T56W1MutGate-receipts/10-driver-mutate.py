#!/usr/bin/env python3
"""Apply one exact single edit per mutant to a scratch copy of the gate, run its
--selftest, record the tally and the failing cases, then restore exact bytes."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W1MutGate')
PRISTINE = S / 'gate-pristine.py'
WORK = S / 'gate-mutant.py'
LANE_GATE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py')

MUTANTS = [
    ('M1-drop-rev-absent',
     "    if not revs:\n        codes.append('RECEIPT_REV_ABSENT')\n        return codes, detail, None\n",
     "    if False and not revs:\n        codes.append('RECEIPT_REV_ABSENT')\n        return codes, detail, None\n"),
    ('M2-drifted-paths-empty',
     "    return [p for p in r.stdout.decode().splitlines() if p]\n",
     "    return []\n"),
    ('M3-is-ancestor-true',
     "    return git(['-C', lane, 'merge-base', '--is-ancestor', older, newer]).returncode == 0\n",
     "    return True\n"),
    ('M4-skip-digest-check',
     "        if want != got:\n",
     "        if False and want != got:\n"),
    ('M5-accept-multi-rev-positive',
     "        if len(revs) > 1:\n",
     "        if False and len(revs) > 1:\n"),
    ('M6-skip-required-line',
     "    if regex is not None and not re.search(regex, text, re.M):\n",
     "    if False and regex is not None and not re.search(regex, text, re.M):\n"),
    ('M7-empty-file-present',
     "    if not data.strip():\n        return ['RECEIPT_EMPTY'], 'path=%s' % path, None\n",
     "    if False and not data.strip():\n        return ['RECEIPT_EMPTY'], 'path=%s' % path, None\n"),
    ('M8-drop-control-not-ancestor',
     "            codes.append('RECEIPT_CONTROL_NOT_ANCESTOR')\n",
     "            pass\n"),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def selftest(path):
    r = subprocess.run([sys.executable, str(path), '--selftest'],
                       capture_output=True, text=True)
    cases = re.findall(r'^CASE (\S+) (PASS|FAIL)$', r.stdout, re.M)
    tally = re.search(r'GATE_SELFTEST: (\d+)/(\d+) pass', r.stdout)
    return {
        'exit': r.returncode,
        'tally': tally.group(0) if tally else None,
        'passed': int(tally.group(1)) if tally else None,
        'total': int(tally.group(2)) if tally else None,
        'failed_cases': [n for n, v in cases if v == 'FAIL'],
        'stdout_tail': r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '',
        'stderr_tail': r.stderr.strip().splitlines()[-3:] if r.stderr.strip() else [],
    }


def main():
    pristine_bytes = PRISTINE.read_bytes()
    pristine_sha = sha(PRISTINE)
    assert sha(LANE_GATE) == pristine_sha, 'scratch copy must equal the lane gate'
    base = selftest(PRISTINE)
    out = {'pristine_sha256': pristine_sha, 'baseline': base, 'mutants': []}
    for name, old, new in MUTANTS:
        src = pristine_bytes.decode()
        n = src.count(old)
        assert n == 1, '%s: old_string occurs %d times' % (name, n)
        mutated = src.replace(old, new, 1)
        WORK.write_bytes(mutated.encode())
        mutated_sha = sha(WORK)
        res = selftest(WORK)
        # restore exact bytes
        WORK.write_bytes(pristine_bytes)
        restored_sha = sha(WORK)
        verdict = 'KILLED' if (res['passed'] is not None
                              and res['passed'] < base['passed']) else 'SURVIVED'
        out['mutants'].append({
            'mutant': name,
            'old': old,
            'new': new,
            'mutated_sha256': mutated_sha,
            'tally_before': base['tally'],
            'tally_after': res['tally'],
            'exit_after': res['exit'],
            'failed_cases_after': res['failed_cases'],
            'stderr_tail': res['stderr_tail'],
            'verdict': verdict,
            'restored_sha256': restored_sha,
            'restored_exact': restored_sha == pristine_sha,
        })
    S.joinpath('mutants.json').write_text(json.dumps(out, indent=1) + '\n')
    for m in out['mutants']:
        print('%-30s %-9s before=%s after=%s failed=%s restored=%s'
              % (m['mutant'], m['verdict'], m['tally_before'], m['tally_after'],
                 ','.join(m['failed_cases_after']) or 'none', m['restored_exact']))
    print('BASELINE', base['tally'], 'exit', base['exit'])
    print('PRISTINE_SHA', pristine_sha)
    print('LANE_SHA_AFTER', sha(LANE_GATE))


if __name__ == '__main__':
    main()
