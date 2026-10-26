#!/usr/bin/env python3
"""Seat T50ExecShrinker: public round-49 panel harness for tools/shrink-case.py.

Replicates the frozen counter's (round-50 c2/measure.py) per-mutant procedure exactly:
find a counterexample with the frozen round-49 generator at seed 4949 / 400 cases, instrument the
pristine and mutant guards with the same run logger, run the shrinker under test, and judge the
result with the generator's own oracle (subset, kills, 1-minimality, cost, reduction).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
S = '/fast/scratch/hyaku/tameshi-r50/T50ExecShrinker'
WORK = os.path.join(S, 'panelwork')
DELIVERABLE = os.path.join(LANE, '.ufo', 'waves', 'round-50', 'w1', 'T50ExecShrinker.shrink-case.py')
GUARD = os.path.join(LANE, 'tools', 'staged-id-guard.py')
GEN = os.path.join(LANE, 'tools', 'pbt-staged-id.py')
PANEL = os.path.join(LANE, '.ufo', 'evidence', 'round-49', 'c2', 'panel.json')
GUARD_SHA = '03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8'
GEN_SHA = '0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05'
PANEL_SHA = 'd6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1'
SEED, CASES = '4949', '400'
INSTRUMENT = ("import os as _r50_os\n"
              "with open(_r50_os.path.join(_r50_os.path.dirname(_r50_os.path.abspath(__file__)), '.runs'), 'a') "
              "as _r50_fh:\n    _r50_fh.write('%s\\n')\n")


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def instrument(source, tag):
    lines = source.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            return '\n'.join(lines[:i]) + '\n' + (INSTRUMENT % tag) + '\n'.join(lines[i:])
    raise SystemExit('no import anchor')


def map_entries(case):
    m = case.get('map')
    if isinstance(m, dict) and isinstance(m.get('map'), dict):
        return m['map']
    return None


def units(case):
    n = len(case['registry'].splitlines(True)) + len(case['staged'].splitlines(True))
    entries = map_entries(case)
    return n + (len(entries) if entries is not None else 0)


def removals(case):
    for field in ('registry', 'staged'):
        lines = case[field].splitlines(True)
        for i in range(len(lines)):
            yield dict(case, **{field: ''.join(lines[:i] + lines[i + 1:])})
    entries = map_entries(case)
    if entries is not None:
        for key in list(entries):
            m = dict(case['map'])
            m['map'] = {k: v for k, v in entries.items() if k != key}
            yield dict(case, map=m)


def subsequence(small, big):
    it = iter(big)
    return all(any(x == y for y in it) for x in small)


def is_subcase(s, c):
    for field in ('registry', 'staged'):
        if not subsequence(s[field].splitlines(), c[field].splitlines()):
            return False
    if c.get('map') is None:
        return s.get('map') is None
    if not isinstance(s.get('map'), dict):
        return False
    ce, se = map_entries(c), map_entries(s)
    if ce is None:
        return s['map'] == c['map']
    if se is None:
        return False
    if {k: v for k, v in s['map'].items() if k != 'map'} != {k: v for k, v in c['map'].items() if k != 'map'}:
        return False
    return all(k in ce and ce[k] == v for k, v in se.items())


def valid_case(case):
    return (isinstance(case, dict) and isinstance(case.get('registry'), str)
            and isinstance(case.get('staged'), str) and (case.get('map') is None or isinstance(case['map'], dict)))


def load_generator(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location('frozen_pbt_r49', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    gen_bytes = open(GEN, 'rb').read()
    guard_bytes = open(GUARD, 'rb').read()
    panel_bytes = open(PANEL, 'rb').read()
    assert sha_bytes(gen_bytes) == GEN_SHA, 'generator digest'
    assert sha_bytes(guard_bytes) == GUARD_SHA, 'guard digest'
    assert sha_bytes(panel_bytes) == PANEL_SHA, 'panel digest'
    deliverable = open(DELIVERABLE, 'rb').read()
    guard_src = guard_bytes.decode('utf-8')
    panel = json.loads(panel_bytes.decode('utf-8'))
    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    os.makedirs(WORK)
    gen = load_generator(GEN)
    tool_src = os.path.join(WORK, 'tool')
    os.makedirs(tool_src)
    with open(os.path.join(tool_src, 'shrink-case.py'), 'wb') as fh:
        fh.write(deliverable)
    shutil.copyfile(GEN, os.path.join(tool_src, 'pbt-staged-id.py'))
    rows = []
    started_all = time.monotonic()
    for n, mutant in enumerate(panel['mutants']):
        mid = mutant.get('id', '?%d' % n)
        row = {'id': mid, 'name': mutant.get('name')}
        t0 = time.monotonic()
        msrc = (guard_src.replace(mutant['old'], mutant['new'])
                if guard_src.count(mutant['old']) == 1 else None)
        if msrc is None:
            row['error'] = 'edit does not apply once'
            rows.append(row)
            continue
        d = os.path.join(WORK, 'm%02d' % n)
        ver, shr, casedir = (os.path.join(d, x) for x in ('ver', 'shr', 'case'))
        for x in (ver, shr, casedir, os.path.join(shr, 'tmp')):
            os.makedirs(x)
        vp, vm = os.path.join(ver, 'pristine.py'), os.path.join(ver, 'mutant.py')
        open(vp, 'w', encoding='utf-8').write(guard_src)
        open(vm, 'w', encoding='utf-8').write(msrc)
        env = dict(os.environ, TMPDIR=os.path.join(shr, 'tmp'))
        dump = os.path.join(d, 'dump.jsonl')
        proc = subprocess.run([sys.executable, '-I', GEN, '--guard', vm, '--seed', SEED,
                               '--cases', CASES, '--dump', dump],
                              capture_output=True, env=env, timeout=3600)
        last = proc.stdout.decode('utf-8', 'replace').strip().split('\n')[-1]
        row['generator_last_line'] = last
        m = re.search(r'counterexample=(\d+)', last)
        if proc.returncode != 1 or not m:
            row['error'] = 'counterexample not found (exit %d)' % proc.returncode
            rows.append(row)
            continue
        index = int(m.group(1))
        row['counterexample_index'] = index
        case = None
        for raw in open(dump, encoding='utf-8'):
            rec = json.loads(raw)
            if rec.get('index') == index:
                case = {'registry': rec['registry'], 'staged': rec['staged'], 'map': rec['map']}
                break
        if case is None:
            row['error'] = 'dump row missing'
            rows.append(row)
            continue
        sp, sm = os.path.join(shr, 'pristine.py'), os.path.join(shr, 'mutant.py')
        open(sp, 'w', encoding='utf-8').write(instrument(guard_src, 'p'))
        open(sm, 'w', encoding='utf-8').write(instrument(msrc, 'm'))
        cpath, opath = os.path.join(shr, 'case.json'), os.path.join(shr, 'out.json')
        json.dump(case, open(cpath, 'w', encoding='utf-8'))
        shrink_started = time.monotonic()
        try:
            sproc = subprocess.run([sys.executable, '-I', os.path.join(tool_src, 'shrink-case.py'),
                                    '--pristine', sp, '--mutant', sm, '--case', cpath,
                                    '--out', opath],
                                   capture_output=True, cwd=shr,
                                   env=dict(env, TMPDIR=os.path.join(shr, 'tmp')), timeout=900)
            rc = sproc.returncode
        except subprocess.TimeoutExpired:
            rc = 124
            sproc = None
        row['shrink_seconds'] = round(time.monotonic() - shrink_started, 2)
        row['shrink_exit'] = rc
        if sproc is not None:
            row['shrink_stdout'] = sproc.stdout.decode('utf-8', 'replace').strip()
            row['shrink_stderr'] = sproc.stderr.decode('utf-8', 'replace').strip()[:400]
        logged = 0
        runlog = os.path.join(shr, '.runs')
        if os.path.exists(runlog):
            logged = sum(1 for _ in open(runlog))
        row['logged'] = logged
        try:
            out = json.load(open(opath, encoding='utf-8'))
        except (OSError, ValueError):
            out = None
        judge = type('J', (), {})()
        judge.gen, judge.pristine, judge.mutant, judge.casedir = gen, vp, vm, casedir

        def kills(candidate):
            if gen.check(candidate, gen.run_guard(vm, casedir, candidate)) is None:
                return False
            return gen.check(candidate, gen.run_guard(vp, casedir, candidate)) is None

        flags = {'exit0': rc == 0, 'valid': False, 'subset': False, 'kills': False,
                 'minimal': False, 'cost': False, 'reduced': False}
        ub, ua = units(case), None
        row['units_before'] = ub
        if isinstance(out, dict) and valid_case(out.get('case')):
            s = {'registry': out['case']['registry'], 'staged': out['case']['staged'],
                 'map': out['case'].get('map')}
            flags['valid'] = True
            ua = units(s)
            row['units_after'] = ua
            row['reported_runs'] = out.get('runs')
            row['reported_units'] = [out.get('units_before'), out.get('units_after')]
            flags['subset'] = is_subcase(s, case)
            flags['kills'] = kills(s)
            flags['minimal'] = flags['kills'] and not any(kills(r) for r in removals(s))
            flags['cost'] = (out.get('runs') == logged and isinstance(out.get('runs'), int)
                             and out.get('units_before') == ub and out.get('units_after') == ua)
            flags['reduced'] = ua <= ub
            row['shrunk'] = s
        row['flags'] = flags
        row['ok'] = all(flags.values())
        row['total_seconds'] = round(time.monotonic() - t0, 2)
        rows.append(row)
        print(mid, row.get('counterexample_index'), '%s->%s' % (ub, ua), 'runs=%s' % row.get('reported_runs'),
              'logged=%d' % logged, 'ok=%s' % row['ok'], 'flags=%s' % flags, flush=True)
    report = {
        'seat': 'T50ExecShrinker',
        'lane': LANE,
        'deliverable': DELIVERABLE,
        'deliverable_sha256': sha_bytes(deliverable),
        'panel': PANEL,
        'panel_sha256': PANEL_SHA,
        'guard_sha256': GUARD_SHA,
        'generator_sha256': GEN_SHA,
        'seed': SEED, 'cases': CASES,
        'mutants': rows,
        'total': len(rows),
        'ok': sum(1 for r in rows if r.get('ok')),
        'units_before_sum': sum(r.get('units_before', 0) for r in rows if r.get('ok')),
        'units_after_sum': sum(r.get('units_after', 0) for r in rows if r.get('ok')),
        'runs_sum': sum(r.get('reported_runs', 0) for r in rows if r.get('ok')),
        'wall_seconds': round(time.monotonic() - started_all, 1),
    }
    json.dump(report, open(os.path.join(S, 'public-runs.json'), 'w'), indent=1)
    print('TOTAL %d ok=%d units %d -> %d runs=%d wall=%ss' % (
        report['total'], report['ok'], report['units_before_sum'],
        report['units_after_sum'], report['runs_sum'], report['wall_seconds']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
