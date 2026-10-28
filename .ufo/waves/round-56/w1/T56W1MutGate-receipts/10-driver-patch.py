#!/usr/bin/env python3
"""Build a patched scratch copy of the gate (proposed diff, never applied to the lane),
then re-run the 8 required mutants and the 5 surviving probes against it.

Expectation: patched selftest 19/19; every previously-surviving probe now KILLED;
every required mutant still KILLED."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W1MutGate')
PRISTINE = S / 'gate-pristine.py'
PATCHED = S / 'gate-patched.py'
WORK = S / 'gate-patched-mutant.py'
LANE_GATE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py')

PATCH = [
    # (label, old, new) — each an exact single edit
    ('P1-emit-not-blob',
     "    if not p.exists():\n        return ['RECEIPT_MISSING'], 'path=%s' % path, None\n",
     "    if not p.exists():\n        return ['RECEIPT_MISSING'], 'path=%s' % path, None\n"
     "    if not p.is_file():\n        return ['RECEIPT_NOT_BLOB'], 'path=%s' % path, None\n"),
    ('P2-codes-closed-distinct',
     "        cases.append(('codes-closed', len(CODES) == 11))\n",
     "        cases.append(('codes-closed', len(CODES) == len(set(CODES)) == 11))\n"),
    ('P3-new-cases',
     "        # 14 the codes list is closed\n",
     "        # 15 a non-regular-file receipt is a named refusal, not a traceback\n"
     "        r = call(str(Path(tmp)) + ':positive')\n"
     "        cases.append(('not-blob-refused',\n"
     "                      r.returncode == 3 and b'RECEIPT_NOT_BLOB' in r.stdout))\n"
     "        # 16 a JSON receipt's \"rev\" token is parsed\n"
     "        r = call(write_receipt('json.txt', '{\"rev\": \"%s\"}\\n' % c2) + ':verdict', certified=c2)\n"
     "        cases.append(('json-rev-parsed', r.returncode == 0))\n"
     "        # 17 an unknown role is a usage error, not silently a control\n"
     "        r = call(write_receipt('role.txt', SELFTEST_RECEIPT_OK % c2) + ':bogus')\n"
     "        cases.append(('unknown-role-refused',\n"
     "                      r.returncode == 1 and b'usage:' in r.stderr))\n"
     "        # 18 zero receipts is a usage error, never a PASS\n"
     "        r = call()\n"
     "        cases.append(('zero-receipts-refused',\n"
     "                      r.returncode == 1 and b'usage:' in r.stderr))\n"
     "        # 19 an unresolvable --certified is exit 2 with a named code\n"
     "        r = call(write_receipt('ok2.txt', SELFTEST_RECEIPT_OK % c2) + ':positive',\n"
     "                 certified='deadbeefdeaddead')\n"
     "        cases.append(('unresolvable-certified-refused',\n"
     "                      r.returncode == 2 and b'RECEIPT_REV_UNRESOLVABLE' in r.stdout))\n"
     "        # 14 the codes list is closed\n"),
]

MUTANTS = [
    ('M1-drop-rev-absent',
     "    if not revs:\n        codes.append('RECEIPT_REV_ABSENT')\n        return codes, detail, None\n",
     "    if False and not revs:\n        codes.append('RECEIPT_REV_ABSENT')\n        return codes, detail, None\n"),
    ('M2-drifted-paths-empty',
     "    return [p for p in r.stdout.decode().splitlines() if p]\n", "    return []\n"),
    ('M3-is-ancestor-true',
     "    return git(['-C', lane, 'merge-base', '--is-ancestor', older, newer]).returncode == 0\n",
     "    return True\n"),
    ('M4-skip-digest-check', "        if want != got:\n", "        if False and want != got:\n"),
    ('M5-accept-multi-rev-positive', "        if len(revs) > 1:\n", "        if False and len(revs) > 1:\n"),
    ('M6-skip-required-line',
     "    if regex is not None and not re.search(regex, text, re.M):\n",
     "    if False and regex is not None and not re.search(regex, text, re.M):\n"),
    ('M7-empty-file-present',
     "    if not data.strip():\n        return ['RECEIPT_EMPTY'], 'path=%s' % path, None\n",
     "    if False and not data.strip():\n        return ['RECEIPT_EMPTY'], 'path=%s' % path, None\n"),
    ('M8-drop-control-not-ancestor',
     "            codes.append('RECEIPT_CONTROL_NOT_ANCESTOR')\n", "            pass\n"),
]

HOLES = [
    ('X1-codes-closed-length-only',
     "    'RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_NOT_BLOB', 'RECEIPT_REV_ABSENT',",
     "    'RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_MISSING', 'RECEIPT_REV_ABSENT',"),
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
    r = subprocess.run([sys.executable, str(path), '--selftest'], capture_output=True, text=True)
    cases = re.findall(r'^CASE (\S+) (PASS|FAIL)$', r.stdout, re.M)
    tally = re.search(r'GATE_SELFTEST: (\d+)/(\d+) pass', r.stdout)
    return {'exit': r.returncode, 'tally': tally.group(0) if tally else None,
            'passed': int(tally.group(1)) if tally else None,
            'failed_cases': [n for n, v in cases if v == 'FAIL'],
            'stderr_tail': r.stderr.strip().splitlines()[-2:] if r.stderr.strip() else []}


def main():
    assert sha(LANE_GATE) == sha(PRISTINE)
    src = PRISTINE.read_text()
    for label, old, new in PATCH:
        assert src.count(old) == 1, '%s occurs %d times' % (label, src.count(old))
        src = src.replace(old, new, 1)
    PATCHED.write_text(src)
    patched_sha = sha(PATCHED)
    base = selftest(PATCHED)
    out = {'patched_sha256': patched_sha, 'patched_baseline': base,
           'mutants_on_patched': [], 'holes_on_patched': []}
    for group, items, key in (('mutants_on_patched', MUTANTS, 'mutant'),
                              ('holes_on_patched', HOLES, 'probe')):
        for name, old, new in items:
            s = PATCHED.read_text()
            assert s.count(old) == 1, '%s on patched occurs %d times' % (name, s.count(old))
            WORK.write_text(s.replace(old, new, 1))
            res = selftest(WORK)
            out[group].append({key: name, 'tally_after': res['tally'],
                               'failed_cases': res['failed_cases'],
                               'stderr_tail': res['stderr_tail'],
                               'verdict': 'KILLED' if res['passed'] < base['passed'] else 'SURVIVED'})
    S.joinpath('patched.json').write_text(json.dumps(out, indent=1) + '\n')
    print('PATCHED_BASELINE', base['tally'], 'exit', base['exit'])
    for g in ('mutants_on_patched', 'holes_on_patched'):
        for m in out[g]:
            n = m.get('mutant') or m.get('probe')
            print('%-30s %-9s after=%s failed=%s' % (n, m['verdict'], m['tally_after'],
                                                     ','.join(m['failed_cases']) or 'none'))
    print('PATCHED_SHA', patched_sha)
    print('LANE_SHA_AFTER', sha(LANE_GATE))


if __name__ == '__main__':
    main()
