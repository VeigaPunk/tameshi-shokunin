#!/usr/bin/env python3
"""Emission-site sweep: disable each real `codes.append`/`return [CODE]` line, one
exact edit per run. Killed => the named selftest case pins that code's emission."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W1MutGate')
PRISTINE = S / 'gate-pristine.py'
WORK = S / 'gate-sweep.py'
LANE_GATE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py')

SWEEP = [
    ('E01-receipt-missing',
     "        return ['RECEIPT_MISSING'], 'path=%s' % path, None\n",
     "        pass\n"),
    ('E02-receipt-empty',
     "        return ['RECEIPT_EMPTY'], 'path=%s' % path, None\n",
     "        pass\n"),
    ('E03-rev-absent',
     "        codes.append('RECEIPT_REV_ABSENT')\n",
     "        pass\n"),
    ('E04-rev-unresolvable',
     "            codes.append('RECEIPT_REV_UNRESOLVABLE')\n",
     "            pass\n"),
    ('E05-rev-ambiguous',
     "            codes.append('RECEIPT_REV_AMBIGUOUS')\n",
     "            pass\n"),
    ('E06-rev-mismatch',
     "                codes.append('RECEIPT_REV_MISMATCH')\n",
     "                pass\n"),
    ('E07-rev-content-drift',
     "                    codes.append('RECEIPT_REV_CONTENT_DRIFT')\n",
     "                    pass\n"),
    ('E08-control-not-ancestor',
     "            codes.append('RECEIPT_CONTROL_NOT_ANCESTOR')\n",
     "            pass\n"),
    ('E09-digest-mismatch',
     "            codes.append('RECEIPT_DIGEST_MISMATCH')\n",
     "            pass\n"),
    ('E10-required-line-missing',
     "        codes.append('RECEIPT_REQUIRED_LINE_MISSING')\n",
     "        pass\n"),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def selftest(path):
    r = subprocess.run([sys.executable, str(path), '--selftest'],
                       capture_output=True, text=True)
    cases = re.findall(r'^CASE (\S+) (PASS|FAIL)$', r.stdout, re.M)
    tally = re.search(r'GATE_SELFTEST: (\d+)/(\d+) pass', r.stdout)
    return {'exit': r.returncode,
            'tally': tally.group(0) if tally else None,
            'passed': int(tally.group(1)) if tally else None,
            'failed_cases': [n for n, v in cases if v == 'FAIL']}


def main():
    pristine_bytes = PRISTINE.read_bytes()
    pristine_sha = sha(PRISTINE)
    assert sha(LANE_GATE) == pristine_sha
    base = selftest(PRISTINE)
    out = {'pristine_sha256': pristine_sha, 'baseline': base, 'sweep': []}
    for name, old, new in SWEEP:
        src = pristine_bytes.decode()
        n = src.count(old)
        assert n == 1, '%s: old_string occurs %d times' % (name, n)
        WORK.write_bytes(src.replace(old, new, 1).encode())
        res = selftest(WORK)
        WORK.write_bytes(pristine_bytes)
        out['sweep'].append({
            'site': name, 'edit': {'old': old, 'new': new},
            'tally_after': res['tally'], 'exit_after': res['exit'],
            'failed_cases': res['failed_cases'],
            'verdict': 'KILLED' if res['passed'] < base['passed'] else 'SURVIVED',
            'restored_exact': sha(WORK) == pristine_sha})
    out['not_blob_site'] = 'NONE — RECEIPT_NOT_BLOB has no emission line in the gate'
    S.joinpath('sweep.json').write_text(json.dumps(out, indent=1) + '\n')
    for s in out['sweep']:
        print('%-30s %-9s after=%s failed=%s' % (s['site'], s['verdict'], s['tally_after'],
                                                 ','.join(s['failed_cases']) or 'none'))
    print('LANE_SHA_AFTER', sha(LANE_GATE))


if __name__ == '__main__':
    main()
