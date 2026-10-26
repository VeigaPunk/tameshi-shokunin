#!/usr/bin/env python3
"""T49SentinelCounters repro: hostile inputs against the two frozen round-49 counters (read-only).

Usage: python3 -B T49SentinelCounters.probe.py SCRATCH_DIR
Writes only under SCRATCH_DIR. Imports the frozen counters from the lane without writing bytecode.
Each block prints a line `FINDING <id> ...` so the report's claims can be tied to output.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '8ca67421111fa354b47b803358391d0b07fc6db9'
C1 = os.path.join(LANE, '.ufo/evidence/round-49/c1/measure.py')
C2 = os.path.join(LANE, '.ufo/evidence/round-49/c2/measure.py')
S = os.path.realpath(sys.argv[1])
os.makedirs(S, exist_ok=True)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c1 = load(C1, 'c1m')
c2 = load(C2, 'c2m')
ENV = dict(c1.GIT_ENV)


def sh(*a, **kw):
    return subprocess.run(list(a), capture_output=True, env=ENV, **kw)


# ---------------------------------------------------------------- C1 probes
print('== C1 (measure.py %s)' % C1)

# F2: a reads.json row whose heading/ordinal/raw is a JSON array/object is unhashable; the
# counter builds a dict key from them and dies.
ptr = [{'heading': 'H', 'ordinal': 0, 'raw': 'x.md:1', 'pointer_kind': 'line', 'file': None,
        'kind': None, 'ranges': None}]
for label, row in (('raw=list', {'heading': 'H', 'ordinal': 0, 'raw': ['x.md:1']}),
                   ('heading=object', {'heading': {'a': 1}, 'ordinal': 0, 'raw': 'x'}),
                   ('ordinal=list', {'heading': 'H', 'ordinal': [0], 'raw': 'x'})):
    try:
        c1.check_reads(LANE, BASE, LANE, ptr, {'rows': [row]})
        print('FINDING F2 %s NO-CRASH' % label)
    except Exception as exc:  # noqa: BLE001 - the counter raises uncaught
        print('FINDING F2 %s -> %s: %s' % (label, type(exc).__name__, str(exc)[:70]))

# F3: a pointer range of more than 4300 digits dies in int(); extract() is unguarded.
for digits in (100, 5000):
    try:
        got = c1.extract('see n.md:' + '9' * digits + '\n')
        print('FINDING F3 digits=%d ok ranges=%s' % (digits, got[0]['ranges']))
    except Exception as exc:  # noqa: BLE001
        print('FINDING F3 digits=%d -> %s: %s' % (digits, type(exc).__name__, str(exc)[:60]))

# F9-positive: excerpts are substring-compared, never compiled as regex (metacharacters inert).
D = os.path.join(S, 'meta')
os.makedirs(D, exist_ok=True)
sh('git', '-C', D, 'init', '-q')
open(os.path.join(D, 'n.md'), 'w').write('alpha beta gamma delta epsilon zeta eta theta\n')
sh('git', '-C', D, 'add', '-A')
sh('git', '-C', D, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x')
rev = sh('git', '-C', D, 'rev-parse', 'HEAD').stdout.decode().strip()
P = [{'heading': 'H', 'ordinal': 0, 'raw': 'n.md:1', 'pointer_kind': 'line', 'file': 'n.md',
      'kind': 'line', 'ranges': [[1, 1]]}]
for ex in ('alpha.*beta gamma delta eps', '(alpha|beta) gamma delta epsilon',
           'alpha [a-z]+ gamma delta ep', 'alpha beta gamma delta epsilon zeta'):
    r, _ = c1.check_reads(D, rev, D, P, {'rows': [{'heading': 'H', 'ordinal': 0, 'raw': 'n.md:1',
                                                   'file': 'n.md', 'ranges': [[1, 1]],
                                                   'verdict': 'holds', 'excerpt': ex}]})
    print('OK metachar-excerpt %-34r excerpt_miss=%d' % (ex[:30], r['excerpt_miss']))

# Ranges are bounds-checked (fail-closed) and excerpt length is bounded.
for raw, rng in (('n.md:0', [[0, 0]]), ('n.md:5-3', [[5, 3]]), ('n.md:1', [[1, 1]])):
    r, _ = c1.check_reads(D, rev, D, [dict(P[0], raw=raw, ranges=rng)],
                          {'rows': [dict(P[0], raw=raw, ranges=rng, file='n.md',
                                         excerpt='alpha beta gamma delta epsilon zeta')]})
    print('OK range %-9s -> unresolved=%d' % (raw, r['unresolved']))

# Traversal: a '..' pointer token is handed to `git cat-file`, which refuses to leave the repo.
for tok in ('../../SKILL.md', 'corpus/../../../x.md'):
    print('OK traversal %-24s resolve=%s' % (tok, c1.resolve(D, rev, tok, 'line')))
r = sh('git', '-C', D, 'cat-file', 'blob', 'HEAD:../meta-secret.md')
print('OK git-traversal exit=%d msg=%s' % (r.returncode, r.stderr.decode().strip()[:80]))

# ---------------------------------------------------------------- C2 probes
print('== C2 (measure.py %s)' % C2)
W = os.path.join(S, 'c2w')
for d in ('tree/tools',):
    os.makedirs(os.path.join(W, d), exist_ok=True)
gbytes = sh('git', '-C', LANE, 'cat-file', 'blob', BASE + ':' + c2.GUARD).stdout
gp = os.path.join(W, 'tree', 'tools', 'staged-id-guard.py')
open(gp, 'wb').write(gbytes)
print('OK guard at REV sha matches pin:', hashlib.sha256(gbytes).hexdigest() == c2.GUARD_SHA)


def gen(name, body):
    p = os.path.join(W, 'tree', 'tools', name)
    open(p, 'w').write(body)
    return p


# F1: the generator is handed a writable path to the guard it is scored against; the sha pin is
# checked once, before the runs (measure.py:253), never again.
cheat = gen('cheat.py', '''
import json, os, sys
a = sys.argv
guard, dump = a[a.index("--guard") + 1], a[a.index("--dump") + 1]
orig = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orig-guard.py")
case = {"index": 0, "registry": "| S001 | x | d | A | x | y | z | mined | 2026-01-01 | 180d | - |\\n",
        "staged": "| S001 | x | d | A | x | y | z | mined | 2026-01-01 | 180d | - |\\n", "map": None}
open(dump, "w").write(json.dumps(case) + "\\n")
if not os.path.exists(orig):
    open(orig, "wb").write(open(guard, "rb").read())
    open(guard, "w").write('print("{\\\\"stubbed\\\\": true}")\\n')
print("PBT_STAGED_ID: cases=1 violations=1 counterexample=0")
sys.exit(1)
''')
r = c2.run_generator(cheat, gp, W, 'cheat')
post = hashlib.sha256(open(gp, 'rb').read()).hexdigest()
print('FINDING F1 generator exit=%s guard_sha_after_run_matches_pin=%s' % (r['exit'], post == c2.GUARD_SHA))
# a byte-identical "mutant" cannot be killed by construction; the kill branch still says confirmed
mp = os.path.join(W, 'mut', 'ident', 'staged-id-guard.py')
os.makedirs(os.path.dirname(mp), exist_ok=True)
open(mp, 'wb').write(gbytes)
case = [c for c in (r['dump'] or []) if c['index'] == 0][0]
a = c2.comparable(c2.run_guard(gp, case, W, 'cp'))
b = c2.comparable(c2.run_guard(mp, case, W, 'cm'))
print('FINDING F1 kill-branch verdict=%s pristine=%s identical_mutant=%s'
      % ('confirmed' if a != b else 'unconfirmed', str(a)[:40], str(b)[:40]))

# F3: the generator's summary line is parsed with unbounded int().
for tag, body in (('big-cases', 'print("PBT_STAGED_ID: cases=" + "9" * 5000 + " violations=0 counterexample=none")\n'),
                  ('big-ce', 'import sys\nprint("PBT_STAGED_ID: cases=400 violations=1 counterexample=" + "9" * 5000)\nsys.exit(1)\n')):
    g = gen(tag + '.py', body)
    res = c2.run_generator(g, gp, W, tag)
    expr = 'int(pr["last"].group(1))' if tag == 'big-cases' else 'int(mr["last"].group(3))'
    group = 1 if tag == 'big-cases' else 3
    try:
        int(res['last'].group(group))
        print('FINDING F3 %s NO-CRASH' % tag)
    except Exception as exc:  # noqa: BLE001
        print('FINDING F3 %s -> counter line %s raises %s: %s'
              % (tag, 'measure.py:308' if tag == 'big-cases' else 'measure.py:339',
                 type(exc).__name__, str(exc)[:50]))

# F5: TMPDIR is advisory; an absolute write escapes --work and the run still exits 0.
escape = os.path.join(S, 'abs-escape-pwn')
g = gen('abs_writer.py', 'open(%r, "w").write("x")\n'
        'print("PBT_STAGED_ID: cases=400 violations=0 counterexample=none")\n' % escape)
res = c2.run_generator(g, gp, W, 'abs')
print('FINDING F5 generator exit=%s wrote_outside_work=%s (work=%s)'
      % (res['exit'], os.path.exists(escape), W))

# F4: the mutant --selftest call (measure.py:332-333) sets no cwd and has no timeout handler.
mroot = os.path.join(S, 'cwdtest')
os.makedirs(mroot, exist_ok=True)
stub = os.path.join(mroot, 'mutant-selftest.py')
open(stub, 'w').write('open("relative-pwn", "w").write("x")\n')
cwd0 = os.getcwd()
os.chdir(mroot)
try:
    subprocess.run([sys.executable, '-I', stub, '--selftest'], capture_output=True,
                   env=c2.env_for(W), timeout=c2.GUARD_TIMEOUT)
    print('FINDING F4 relative write lands in the inherited cwd=%s file=%s'
          % (mroot, os.path.exists(os.path.join(mroot, 'relative-pwn'))))
finally:
    os.chdir(cwd0)
hang = os.path.join(mroot, 'hang-selftest.py')
open(hang, 'w').write('import time\ntime.sleep(30)\n')
try:
    subprocess.run([sys.executable, '-I', hang, '--selftest'], capture_output=True,
                   env=c2.env_for(W), timeout=3)  # frozen constant is GUARD_TIMEOUT=60
    print('FINDING F4 hang NO-CRASH')
except subprocess.TimeoutExpired:
    print('FINDING F4 an unguarded timeout raises TimeoutExpired (frozen timeout=%d s, reproduced at 3 s)'
          % c2.GUARD_TIMEOUT)
