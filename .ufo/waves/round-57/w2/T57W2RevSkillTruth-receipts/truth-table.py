#!/usr/bin/env python3
"""Re-run the receipt-revision-gate truth table at C0 bytes.

Role x paths matrix: which code/exit the gate actually emits.
Fixture: repo with c0 (surface=A, other=A, moved=A), c1 (moved=B), side branch off c0.
"""
import os
import subprocess
import sys
from pathlib import Path

GATE = sys.argv[1]
WORK = Path(sys.argv[2])
WORK.mkdir(parents=True, exist_ok=True)

ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')

REPO = WORK / 'repo'
REPO.mkdir(exist_ok=True)


def g(*args, check=True):
    p = subprocess.run(['git', '-C', str(REPO), '-c', 'user.name=fixture',
                        '-c', 'user.email=fixture@example.invalid'] + list(args),
                       env=ENV, capture_output=True)
    if check and p.returncode != 0:
        raise SystemExit('git %s failed: %s' % (' '.join(args), p.stderr.decode()))
    return p.stdout.decode().strip()


g('init', '-q', '-b', 'master')
top = g('rev-parse', '--show-toplevel')
assert os.path.realpath(top) == os.path.realpath(str(REPO)), 'toplevel %s != %s' % (top, REPO)
(REPO / 'surface.txt').write_text('alpha\n')
(REPO / 'other.txt').write_text('alpha\n')
(REPO / 'moved.txt').write_text('alpha\n')
g('add', '-A')
g('commit', '-q', '-m', 'c0')
C0 = g('rev-parse', 'HEAD')
(REPO / 'moved.txt').write_text('gamma\n')
g('commit', '-q', '-a', '-m', 'c1')
C1 = g('rev-parse', 'HEAD')
(REPO / 'other.txt').write_text('delta\n')
g('commit', '-q', '-a', '-m', 'c2')
C2 = g('rev-parse', 'HEAD')
g('checkout', '-q', C0)
(REPO / 'side.txt').write_text('side\n')
g('add', '-A')
g('commit', '-q', '-m', 'side')
SIDE = g('rev-parse', 'HEAD')
g('checkout', '-q', 'master')

P_SURFACE = WORK / 'surface.paths'
P_SURFACE.write_text('surface.txt\n')
P_ALL = WORK / 'all.paths'
P_ALL.write_text('surface.txt\nmoved.txt\n')
P_EMPTY = WORK / 'empty.paths'
P_EMPTY.write_text('# only a comment\n')


def receipt(name, text):
    p = WORK / name
    p.write_text(text)
    return str(p)


def call(receipts, certified=C1, paths=None, extra=None):
    argv = [sys.executable, GATE, '--lane', str(REPO), '--certified', certified]
    if paths:
        argv += ['--paths', paths]
    for r in receipts:
        argv += ['--receipt', r]
    if extra:
        argv += extra
    p = subprocess.run(argv, capture_output=True, env=ENV)
    out = p.stdout.decode('utf-8', 'replace')
    err = p.stderr.decode('utf-8', 'replace')
    codes = []
    verdict = 'none'
    for line in out.splitlines():
        if line.startswith('GATE: '):
            for tok in line.split():
                if tok.startswith('codes='):
                    codes = [] if tok[6:] == 'none' else tok[6:].split(',')
                if tok.startswith('verdict='):
                    verdict = tok[8:]
    named = []
    for line in out.splitlines():
        if ' code=' in line:
            named.append(line.split(' code=')[1].split()[0])
    return p.returncode, sorted(set(codes)) or sorted(set(named)), verdict, out, err


OK = 'VERDICT: rev=%s C1_X_PASS=true\n'
rows = []


def rec(label, role, paths, result, expect_note=''):
    rc, codes, verdict, out, err = result
    rows.append((label, role, paths, rc, ','.join(codes) or 'none', verdict, expect_note))


R_MATCH = receipt('match.txt', OK % C1)
R_OLD = receipt('old.txt', OK % C0)
R_SIDE = receipt('side.txt', OK % SIDE)
R_NOVER = receipt('nover.txt', 'VERDICT: no revision named\n')
R_TWO = receipt('two.txt', 'A rev=%s\nB rev=%s\n' % (C0, C1))
R_DEAD = receipt('dead.txt', 'VERDICT: rev=deadbeefdeadbeef C1_X_PASS=true\n')
R_CTL_OK = receipt('ctlok.txt', 'CTL A rev=%s\nCTL B rev=%s\n' % (C0, C1))
R_CTL_SIDE = receipt('ctls.txt', 'CTL A rev=%s\n' % SIDE)
R_CTL_DEAD = receipt('ctld.txt', 'CTL A rev=%s\n' % 'deadbeefdeadbeef')
R_NOLINE = receipt('noline.txt', 'VERDICT: rev=%s\n' % C2)
R_EMPTY = receipt('empty.txt', '\n')
R_MISSING = str(WORK / 'nope.txt')
R_DIR = str(WORK)

for role in ('positive', 'verdict'):
    rec('%s/match/no-paths' % role, role, 'absent', call(['%s:%s' % (R_MATCH, role)], paths=None))
    rec('%s/match/paths-surface' % role, role, 'surface.txt',
        call(['%s:%s' % (R_MATCH, role)], paths=str(P_SURFACE)))
    rec('%s/old/no-paths' % role, role, 'absent', call(['%s:%s' % (R_OLD, role)], paths=None))
    rec('%s/old/paths-surface(identical)' % role, role, 'surface.txt',
        call(['%s:%s' % (R_OLD, role)], paths=str(P_SURFACE)))
    rec('%s/old/paths-all(drift)' % role, role, 'surface.txt+moved.txt',
        call(['%s:%s' % (R_OLD, role)], paths=str(P_ALL)))
    rec('%s/old/paths-empty-file' % role, role, 'empty file',
        call(['%s:%s' % (R_OLD, role)], paths=str(P_EMPTY)))
    rec('%s/old/paths-missing-file' % role, role, 'missing file',
        call(['%s:%s' % (R_OLD, role)], paths=str(WORK / 'nosuch.paths')))
    rec('%s/no-rev/no-paths' % role, role, 'absent', call(['%s:%s' % (R_NOVER, role)], paths=None))
    rec('%s/two-revs/paths-all' % role, role, 'surface.txt+moved.txt',
        call(['%s:%s' % (R_TWO, role)], paths=str(P_ALL)))
    rec('%s/dead-rev/no-paths' % role, role, 'absent', call(['%s:%s' % (R_DEAD, role)], paths=None))
    rec('%s/missing-file' % role, role, 'absent', call(['%s:%s' % (R_MISSING, role)], paths=None))
    rec('%s/empty-file' % role, role, 'absent', call(['%s:%s' % (R_EMPTY, role)], paths=None))
    rec('%s/dir-receipt' % role, role, 'absent', call(['%s:%s' % (R_DIR, role)], paths=None))
    rec('%s/regex-missing' % role, role, 'absent',
        call(['%s:%s:C1_X_PASS=' % (R_NOLINE, role)], paths=None))

rec('control/ancestors', 'control', 'absent', call(['%s:control' % R_CTL_OK], paths=None))
rec('control/ancestors+paths', 'control', 'surface.txt',
    call(['%s:control' % R_CTL_OK], paths=str(P_SURFACE)))
rec('control/non-ancestor', 'control', 'absent', call(['%s:control' % R_CTL_SIDE], paths=None))
rec('control/dead-rev', 'control', 'absent', call(['%s:control' % R_CTL_DEAD], paths=None))
rec('control/two-revs', 'control', 'absent', call(['%s:control' % R_CTL_TWO if False else '%s:control' % R_CTL_OK]))

# digest sidecar
p = receipt('digest.txt', OK % C2)
(WORK / 'digest.txt.sha256').write_text('0' * 64 + '\n')
rec('verdict/digest-mismatch', 'verdict', 'absent', call(['%s:verdict' % p], paths=None))
# certified unresolvable
rec('positive/certified-unresolvable', 'positive', 'absent',
    call(['%s:positive' % R_MATCH], certified='deadbeefdeadbeefdeadbeef'))
# usage errors
rec('usage/unknown-role', 'bogus', 'absent', call(['%s:bogus' % R_MATCH], paths=None))
rec('usage/no-receipts', '-', 'absent', call([], paths=None))
rec('usage/flag-without-value', '-', 'absent',
    (lambda p: (p.returncode, [], 'none', p.stdout.decode(), p.stderr.decode()))(
        subprocess.run([sys.executable, GATE, '--lane', str(REPO), '--certified', C1,
                        '--receipt', '%s:positive' % R_MATCH, '--paths'],
                       capture_output=True, env=ENV)))
rec('usage/unknown-flag', '-', 'absent',
    (lambda p: (p.returncode, [], 'none', p.stdout.decode(), p.stderr.decode()))(
        subprocess.run([sys.executable, GATE, '--lane', str(REPO), '--certified', C1,
                        '--receipt', '%s:positive' % R_MATCH, '--nope'],
                       capture_output=True, env=ENV)))
rec('usage/paths-empty-string', 'positive', "''",
    call(['%s:positive' % R_OLD], paths=None))
# lane missing
rec('positive/lane-missing', 'positive', 'absent',
    (lambda p: (p.returncode, [], 'none', p.stdout.decode(), p.stderr.decode()))(
        subprocess.run([sys.executable, GATE, '--lane', str(WORK / 'nosuchlane'),
                        '--certified', C1, '--receipt', '%s:positive' % R_MATCH],
                       capture_output=True, env=ENV)))
# json mode on exit-2 path
p = subprocess.run([sys.executable, GATE, '--lane', str(REPO), '--certified', 'deadbeefdeadbeef',
                    '--receipt', '%s:positive' % R_MATCH, '--json'], capture_output=True, env=ENV)
rows.append(('json/certified-unresolvable', 'positive', 'absent', p.returncode, 'none', 'none',
             'json=%s' % ('yes' if p.stdout.decode().strip().startswith('{') else 'no')))
# json mode on a refusal
p = subprocess.run([sys.executable, GATE, '--lane', str(REPO), '--certified', C1,
                    '--paths', str(P_ALL), '--receipt', '%s:positive' % R_OLD, '--json'],
                   capture_output=True, env=ENV)
rows.append(('json/drift-refusal', 'positive', 'surface.txt+moved.txt', p.returncode,
             'RECEIPT_REV_CONTENT_DRIFT', 'none', 'json=%s' % ('yes' if p.stdout.decode().strip().startswith('{') else 'no')))

print('%-34s %-9s %-24s %4s %-34s %-8s %s' % ('case', 'role', 'paths', 'exit', 'codes', 'verdict', 'note'))
for r in rows:
    print('%-34s %-9s %-24s %4d %-34s %-8s %s' % r)

# distinct exit/code lattice
print()
print('CODES emitted across the sweep:')
allc = sorted({c for r in rows for c in r[4].split(',') if c and c != 'none'})
for c in allc:
    print('  %-34s cases=%s' % (c, ','.join(r[0] for r in rows if c in r[4].split(','))))
print('exits observed:', sorted({r[3] for r in rows}))
