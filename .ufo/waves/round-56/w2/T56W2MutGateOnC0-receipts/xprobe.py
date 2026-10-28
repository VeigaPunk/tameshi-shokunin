#!/usr/bin/env python3
"""Re-check the six wave-1 SURVIVING probes (X1-X6) against the C0 gate.

Wave 1 found six single-edit probes that survived the 14-case suite and
proposed five extra cases (15-19).  The C0 gate carries those cases, so the
same six probes are re-run here to record whether the amendment closed them.
This is supporting context for the required 8-mutant set, not a substitute.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W2MutGateOnC0')
LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
GATE_REL = 'tools/receipt-revision-gate.py'
SRC = (LANE / GATE_REL).read_bytes()

PROBES = [
    ('X1', 'CODES entry swapped for a duplicate (NOT_BLOB -> MISSING)',
     "    'RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_NOT_BLOB', 'RECEIPT_REV_ABSENT',",
     "    'RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_MISSING', 'RECEIPT_REV_ABSENT',"),
    ('X2', 'rev regex narrowed to {40}',
     "REV_RE = re.compile(r'\\brev=([0-9a-f]{7,40})\\b')",
     "REV_RE = re.compile(r'\\brev=([0-9a-f]{40})\\b')"),
    ('X3', 'JSON rev tokens dropped (JSON_REV_RE not consulted)',
     "    revs = sorted(set(REV_RE.findall(text)) | set(JSON_REV_RE.findall(text)))",
     "    revs = sorted(set(REV_RE.findall(text)))"),
    ('X4', 'unknown role accepted',
     "        if len(parts) < 2 or parts[1] not in ('positive', 'verdict', 'control'):",
     "        if len(parts) < 2:"),
    ('X5', 'zero --receipt accepted',
     "    if not lane or not certified or not receipts:",
     "    if not lane or not certified:"),
    ('X6', 'unresolvable --certified accepted',
     "    full = resolve(lane, certified)\n    if full is None:",
     "    full = resolve(lane, certified) or 'deadbeef'\n    if False:"),
]


def run(gate):
    env = dict(os.environ)
    env.update(HOME='/tmp', GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    r = subprocess.run([sys.executable, str(gate), '--selftest'],
                       capture_output=True, text=True, env=env, timeout=600)
    m = re.search(r'GATE_SELFTEST: (\d+)/(\d+) pass', r.stdout)
    failed = re.findall(r'^CASE (\S+) FAIL$', r.stdout, re.M)
    return (('%s/%s' % (m.group(1), m.group(2))) if m else None), failed, r.returncode, r.stderr


rows = []
base_tally, base_failed, base_exit, _ = run(LANE / GATE_REL)
print('C0 BASELINE %s exit=%d' % (base_tally, base_exit))
assert base_failed == [], base_failed

for pid, desc, old, new in PROBES:
    n = SRC.count(old.encode())
    if n != 1:
        rows.append({'id': pid, 'desc': desc, 'error': 'old occurs %d times' % n})
        print('%s SKIP count=%d' % (pid, n))
        continue
    g = S / ('x-%s-gate.py' % pid)
    g.write_bytes(SRC.replace(old.encode(), new.encode(), 1))
    tally, failed, exit_, err = run(g)
    verdict = 'KILLED' if (tally and int(tally.split('/')[0]) < int(base_tally.split('/')[0])) else 'SURVIVED'
    print('%s %-9s %s failed=%s' % (pid, verdict, tally, failed))
    rows.append({'id': pid, 'desc': desc, 'old': old, 'new': new,
                 'tally': tally, 'failed_cases': failed, 'exit': exit_,
                 'verdict': verdict,
                 'stderr_last': err.strip().splitlines()[-1:] or []})
    g.unlink()

(S / 'x-probes.json').write_text(json.dumps(rows, indent=1))
print('survived: %s' % [r['id'] for r in rows if r.get('verdict') == 'SURVIVED'])
