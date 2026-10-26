"""Probes for T50W2RevShrinkCode: run-mode cost accounting, determinism, ddmin properties.

Fixture tree: S/fix (shrink-case.py, pbt-staged-id.py, staged-id-guard.py from 80ea77e9).
Everything runs inside S; no lane, no ~/.local/state, no counter execution.
"""
import importlib.util
import json
import os
import random
import subprocess
import sys

S = '/fast/scratch/hyaku/tameshi-r50/T50W2RevShrinkCode'
FIX = os.path.join(S, 'fix')
TOOL = os.path.join(FIX, 'shrink-case.py')
GEN = os.path.join(FIX, 'pbt-staged-id.py')
GUARD = os.path.join(FIX, 'staged-id-guard.py')
B = os.path.join(FIX, 'b')

RUN_LOGGER = ("import os as _shrink_os\n"
              "with open(_shrink_os.path.join(_shrink_os.path.dirname(_shrink_os.path.abspath(__file__)), "
              "'.runs'), 'a') as _shrink_log:\n    _shrink_log.write('%s\\n')\n")


def instrument(src, tag):
    lines = src.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            return '\n'.join(lines[:i]) + '\n' + (RUN_LOGGER % tag) + '\n'.join(lines[i:])
    raise SystemExit('no anchor')


WRAP = ("import os, sys\n"
        "with open(os.environ['COUNT_LOG'], 'a') as fh:\n"
        "    fh.write('sub\\n')\n"
        "os.execv(sys.executable, [sys.executable, '-I', os.environ['REAL_%s']] + sys.argv[1:])\n")

HEAD = ('| id | source | kind | tier | scope | anchor | teaches | status | opened '
        '| recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n')
BODY = ('| S%03d | Src S%03d \u2014 https://a%d.test/doc | docs | A | scope | anchor '
        '| teaches | queued | 2026-10-24 | 180d | -\n')

M02_OLD = "ROW_RE = re.compile(r'^ {0,3}\\|"
M02_NEW = "ROW_RE = re.compile(r'^\\|"


def setup():
    os.makedirs(B, exist_ok=True)
    src = open(GUARD, encoding='utf-8').read()
    assert src.count(M02_OLD) == 1, 'M02 edit does not apply exactly once'
    with open(os.path.join(B, 'real-p.py'), 'w', encoding='utf-8') as fh:
        fh.write(instrument(src, 'p'))
    with open(os.path.join(B, 'real-m.py'), 'w', encoding='utf-8') as fh:
        fh.write(instrument(src.replace(M02_OLD, M02_NEW), 'm'))
    for tag in ('P', 'M'):
        with open(os.path.join(B, 'wrap-%s.py' % tag.lower()), 'w', encoding='utf-8') as fh:
            fh.write(WRAP % tag)
    case = {'registry': HEAD + BODY % (1, 1, 1) + BODY % (2, 2, 2),
            'staged': HEAD + ' ' + BODY % (1, 1, 1), 'map': None}
    with open(os.path.join(B, 'case.json'), 'w', encoding='utf-8') as fh:
        json.dump(case, fh)
    return case


def run_case(outname, tmpdir, hashseed=None, wrappers=True):
    for stale in ('.runs', 'count.log'):
        p = os.path.join(B, stale)
        if os.path.exists(p):
            os.unlink(p)
    os.makedirs(tmpdir, exist_ok=True)
    env = dict(os.environ, TMPDIR=tmpdir,
               COUNT_LOG=os.path.join(B, 'count.log'),
               REAL_P=os.path.join(B, 'real-p.py'),
               REAL_M=os.path.join(B, 'real-m.py'))
    if hashseed is not None:
        env['PYTHONHASHSEED'] = hashseed
    if wrappers:
        pristine, mutant = os.path.join(B, 'wrap-p.py'), os.path.join(B, 'wrap-m.py')
    else:
        pristine, mutant = os.path.join(B, 'real-p.py'), os.path.join(B, 'real-m.py')
    os.makedirs(os.path.join(B, 'cwdrun'), exist_ok=True)
    return subprocess.run([sys.executable, '-I', TOOL, '--pristine', pristine,
                           '--mutant', mutant, '--case', os.path.join(B, 'case.json'),
                           '--out', os.path.join(B, outname)],
                          capture_output=True, env=env, cwd=os.path.join(B, 'cwdrun'))


def probe_cost_and_surface(case):
    print('== probe B: cost accounting and write surface ==')
    tmp = os.path.join(B, 'tmp-cost')
    p = run_case('out.json', tmp)
    print('rc=%d stdout=%r stderr=%r' % (p.returncode, p.stdout.decode()[-120:],
                                         p.stderr.decode()[-300:]))
    out = json.load(open(os.path.join(B, 'out.json'), encoding='utf-8'))
    runs = out['runs']
    logged = sum(1 for _ in open(os.path.join(B, '.runs'), encoding='utf-8'))
    subs = sum(1 for _ in open(os.path.join(B, 'count.log'), encoding='utf-8'))
    print('out.runs=%d .runs-lines=%d wrapper-subprocesses=%d equal=%s'
          % (runs, logged, subs, runs == logged == subs))
    print('units %s -> %s (input %d) subset-check via tool logic next' %
          (out['units_before'], out['units_after'],
           len(case['registry'].splitlines(True)) + len(case['staged'].splitlines(True))))
    print('tmp dir left behind: %s' % (os.listdir(tmp) if os.path.isdir(tmp) else 'absent'))
    print('b/ listing: %s' % sorted(os.listdir(B)))


def probe_determinism():
    print('== probe C: determinism across hash seeds and TMPDIRs ==')
    o1 = os.path.join(B, 'out-h1.json')
    o2 = os.path.join(B, 'out-h2.json')
    run_case(o1, os.path.join(B, 'tmp-d1'), hashseed='1')
    run_case(o2, os.path.join(B, 'tmp-d2'), hashseed='31337')
    b1 = open(o1, 'rb').read()
    b2 = open(o2, 'rb').read()
    print('byte-identical across PYTHONHASHSEED=1 vs 31337 and different TMPDIR: %s (%d bytes)'
          % (b1 == b2, len(b1)))
    print(open(o1, encoding='utf-8').read()[:400])


def probe_selftest():
    print('== probe A: --selftest ==')
    tmp = os.path.join(S, 'tmp-selftest')
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ, TMPDIR=tmp)
    p = subprocess.run([sys.executable, '-I', TOOL, '--selftest'],
                       capture_output=True, env=env, cwd=FIX)
    text = p.stdout.decode()
    print('rc=%d' % p.returncode)
    for line in text.splitlines():
        print('  ' + line)
    if p.stderr:
        print('  STDERR ' + p.stderr.decode()[-300:])


def probe_ddmin_fuzz():
    print('== probe F: ddmin property fuzz (soundness + 1-minimality) ==')
    spec = importlib.util.spec_from_file_location('shrink_case_probe', TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rng = random.Random(5050)
    bad = 0
    asks_total = dup_total = 0
    for trial in range(300):
        n = rng.randint(0, 25)
        items = tuple(range(n))
        core = frozenset(rng.sample(items, rng.randint(0, n))) if n else frozenset()
        floor = rng.randint(0, 4)
        monotone = rng.random() < 0.5
        seen = []

        def kills(keep):
            seen.append(frozenset(keep))
            if monotone:
                return core <= keep
            return core <= keep and len(keep) >= floor

        got = mod.ddmin(items, kills)
        asks_total += len(seen)
        dup_total += len(seen) - len(set(seen))
        if got is None:
            if kills(frozenset(items)):
                bad += 1
                print('  BAD trial %d: None but initial holds' % trial)
            continue
        got = frozenset(got)
        if not kills(got):
            bad += 1
            print('  BAD trial %d: result fails predicate' % trial)
        for unit in got:
            if kills(got - {unit}):
                bad += 1
                print('  BAD trial %d: unit %d removable (n=%d)' % (trial, unit, n))
                break
    print('trials=300 bad=%d asks=%d duplicate-asks=%d' % (bad, asks_total, dup_total))


if __name__ == '__main__':
    case = setup()
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if which in ('all', 'fuzz'):
        probe_ddmin_fuzz()
    if which in ('all', 'selftest'):
        probe_selftest()
    if which in ('all', 'cost'):
        probe_cost_and_surface(case)
    if which in ('all', 'determinism'):
        probe_determinism()
