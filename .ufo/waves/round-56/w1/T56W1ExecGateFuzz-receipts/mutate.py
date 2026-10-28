#!/usr/bin/env python3
"""Round-56 W1 T56W1ExecGateFuzz: mutation test of the frozen gate's own suite.

Each mutant is a one-token edit of a scratch copy of tools/receipt-revision-gate.py
(sha256 1d80f8a6...).  The suite is `--selftest` (the C2 arm-1 instrument).  A mutant
is KILLED when the suite fails; SURVIVED when the suite still reports 14/14.

usage: mutate.py GATE OUTDIR
Writes OUTDIR/mutants.tsv and OUTDIR/mutants.log.  Never mutates the lane.
"""
import hashlib
import re
from pathlib import Path
import subprocess
import sys

GATE, OUTDIR = sys.argv[1], Path(sys.argv[2])
SRC = Path(GATE).read_text()

MUTANTS = [
    ('M01-mismatch-off', 'if full != certified:', 'if False:'),
    ('M02-ambiguous-off', 'if len(revs) > 1:', 'if False:'),
    ('M03-ancestor-off', 'if not is_ancestor(lane, full, certified):', 'if False:'),
    ('M04-digest-off', 'if want != got:', 'if False:'),
    ('M05-required-line-off',
     'if regex is not None and not re.search(regex, text, re.M):', 'if False:'),
    ('M06-empty-off', 'if not data.strip():', 'if False:'),
    ('M07-missing-off', 'if not p.exists():', 'if False:'),
    ('M08-drift-always-empty',
     'return [p for p in r.stdout.decode().splitlines() if p]', 'return []'),
    ('M09-drift-always-nonempty',
     'return [p for p in r.stdout.decode().splitlines() if p]', "return ['<mutant>']"),
    ('M10-rev-min-4', r"REV_RE = re.compile(r'\brev=([0-9a-f]{7,40})\b')",
     r"REV_RE = re.compile(r'\brev=([0-9a-f]{4,40})\b')"),
    ('M11-json-rev-off', '| set(JSON_REV_RE.findall(text))', ''),
    ('M12-exit0-always', "return 0 if verdict == 'PASS' else 3", 'return 0'),
    ('M13-rev-uppercase-ok', r"REV_RE = re.compile(r'\brev=([0-9a-f]{7,40})\b')",
     r"REV_RE = re.compile(r'\brev=([0-9a-fA-F]{7,40})\b')"),
    ('M14-resolve-always-none',
     'return r.stdout.decode().strip() if r.returncode == 0 else None', 'return None'),
    ('M15-sidecar-ignored', 'if sidecar.exists():', 'if False:'),
    ('M16-control-as-positive',
     "if role_name in ('positive', 'verdict'):",
     "if role_name in ('positive', 'verdict', 'control'):"),
    ('M17-rev-dedup-off', 'revs = sorted(set(REV_RE.findall(text)) | set(JSON_REV_RE.findall(text)))',
     'revs = sorted(list(REV_RE.findall(text)) + list(JSON_REV_RE.findall(text)))'),
    ('M18-unresolvable-continues', '    if codes:\n        return codes, detail, revs',
     '    if False:\n        return codes, detail, revs'),
    ('M19-role-check-off',
     "if len(parts) < 2 or parts[1] not in ('positive', 'verdict', 'control'):",
     'if len(parts) < 2:'),
    ('M20-path-check-off', 'if not paths:', 'if False:'),
]

out = OUTDIR / 'mutants'
out.mkdir(parents=True, exist_ok=True)
base_hash = hashlib.sha256(Path(GATE).read_bytes()).hexdigest()
lines = ['mutant\tapplied\tresult\texit\tselftest\tfailing_cases']
log = ['GATE_SHA256=%s' % base_hash]

base = subprocess.run([sys.executable, GATE, '--selftest'], capture_output=True, timeout=300)
base_out = base.stdout.decode()
m = re.search(r'GATE_SELFTEST: (\d+)/(\d+) pass', base_out)
lines.append('M00-baseline\t-\t%s\t%d\t%s\t-'
             % ('PASS' if base.returncode == 0 else 'FAIL', base.returncode,
                m.group(0) if m else 'none'))
log += ['=== M00-baseline', base_out.rstrip()]

for name, old, new in MUTANTS:
    n = SRC.count(old)
    path = out / (name + '.py')
    if n != 1:
        lines.append('%s\tCOUNT=%d\tSKIP\t-\t-\t-' % (name, n))
        log += ['=== %s SKIP: pattern count %d' % (name, n)]
        continue
    path.write_text(SRC.replace(old, new, 1))
    r = subprocess.run([sys.executable, str(path), '--selftest'],
                       capture_output=True, timeout=300)
    so = r.stdout.decode()
    m = re.search(r'GATE_SELFTEST: (\d+)/(\d+) pass', so)
    failing = [ln.split()[1] for ln in so.splitlines()
               if ln.startswith('CASE ') and ln.endswith(' FAIL')]
    killed = not (r.returncode == 0 and m and m.group(1) == m.group(2))
    lines.append('%s\tyes\t%s\t%d\t%s\t%s'
                 % (name, 'KILLED' if killed else 'SURVIVED', r.returncode,
                    m.group(0) if m else 'none', ','.join(failing) or '-'))
    log += ['=== %s KILLED=%s' % (name, killed), so.rstrip()]

(OUTDIR / 'mutants.tsv').write_text('\n'.join(lines) + '\n')
(OUTDIR / 'mutants.log').write_text('\n'.join(log) + '\n')
print('\n'.join(lines))
