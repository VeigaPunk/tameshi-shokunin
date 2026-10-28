#!/usr/bin/env python3
"""Auxiliary single-edit probes: do the selftest's 14 cases pin the parts of the
gate the eight required mutants do not touch? A SURVIVED probe is a coverage hole."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W1MutGate')
PRISTINE = S / 'gate-pristine.py'
WORK = S / 'gate-probe.py'
LANE_GATE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py')

PROBES = [
    ('X1-codes-closed-length-only',
     "    'RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_NOT_BLOB', 'RECEIPT_REV_ABSENT',",
     "    'RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_MISSING', 'RECEIPT_REV_ABSENT',"),
    ('X2-rev-regex-40hex-only',
     "REV_RE = re.compile(r'\\brev=([0-9a-f]{7,40})\\b')",
     "REV_RE = re.compile(r'\\brev=([0-9a-f]{40})\\b')"),
    ('X3-drop-json-rev-tokens',
     "    revs = sorted(set(REV_RE.findall(text)) | set(JSON_REV_RE.findall(text)))",
     "    revs = sorted(set(REV_RE.findall(text)))"),
    ('X4-unknown-role-accepted',
     "        if len(parts) < 2 or parts[1] not in ('positive', 'verdict', 'control'):",
     "        if len(parts) < 2 or parts[1] not in ('positive', 'verdict', 'control', 'bogus'):"),
    ('X5-zero-receipts-is-pass',
     "    if not lane or not certified or not receipts:",
     "    if not lane or not certified:"),
    ('X6-unresolvable-certified-accepted',
     "    if full is None:\n        print('GATE: error=unresolvable-certified",
     "    if full is None and False:\n        print('GATE: error=unresolvable-certified"),
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
        'failed_cases': [n for n, v in cases if v == 'FAIL'],
    }


def main():
    pristine_bytes = PRISTINE.read_bytes()
    pristine_sha = sha(PRISTINE)
    assert sha(LANE_GATE) == pristine_sha
    base = selftest(PRISTINE)
    out = {'pristine_sha256': pristine_sha, 'baseline': base, 'probes': []}
    for name, old, new in PROBES:
        src = pristine_bytes.decode()
        n = src.count(old)
        assert n == 1, '%s: old_string occurs %d times' % (name, n)
        WORK.write_bytes(src.replace(old, new, 1).encode())
        res = selftest(WORK)
        WORK.write_bytes(pristine_bytes)
        verdict = 'SURVIVED' if res['passed'] == base['passed'] else 'KILLED'
        out['probes'].append({'probe': name, 'old': old, 'new': new,
                              'tally_after': res['tally'], 'exit_after': res['exit'],
                              'failed_cases_after': res['failed_cases'],
                              'verdict': verdict,
                              'restored_exact': sha(WORK) == pristine_sha})
    S.joinpath('probes.json').write_text(json.dumps(out, indent=1) + '\n')
    for p in out['probes']:
        print('%-34s %-9s after=%s failed=%s' % (p['probe'], p['verdict'], p['tally_after'],
                                                 ','.join(p['failed_cases_after']) or 'none'))
    print('LANE_SHA_AFTER', sha(LANE_GATE))


if __name__ == '__main__':
    main()
