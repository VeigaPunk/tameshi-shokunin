#!/usr/bin/env python3
"""Round-50 C2 counter (coverage, frontier F6): a 1-minimal fixture shrinker with a stated cost.

Usage:
  python3 measure.py --lane LANE --rev REV --work EMPTY_DIR --panel PUBLIC_PANEL --hidden HIDDEN_PANEL
  python3 measure.py --selftest --lane LANE --work DIR

For every mutant of the two panels (the 12 public round-49 mutants and the hidden round-50 set) of the
pinned gate tools/staged-id-guard.py, the counter
  1. finds a killing case with the FROZEN round-49 generator (tools/pbt-staged-id.py at 7d3d977f,
     sha256 pinned; seed 4949, 400 cases): the dumped counterexample case C;
  2. runs the shrinker under test, tools/shrink-case.py at REV (copied into the work dir next to a copy of
     the REV generator, `pbt-staged-id.py`, which it may import):
       python3 -I shrink-case.py --pristine P --mutant M --case C.json --out OUT.json
     P and M are instrumented copies of the pristine and mutant guard that log every invocation;
  3. checks OUT.json = {"case": {registry, staged, map}, "runs": int, "units_before": int,
     "units_after": int} with the frozen generator's oracle (`check`):
       subset    the shrunk registry/staged lines are subsequences of C's, its map entries a subset of C's
                 (every other map field equal);
       kills     the shrunk case passes the pristine guard and violates on the mutant;
       minimal   removing any single unit (one registry line, one staged line, one map entry) no longer
                 kills (S167's 1-minimality: "removing any single input entity would cause the failure
                 to disappear");
       cost      `runs` equals the invocations the instrumented guards logged, and units_before/after
                 equal the counter's own unit counts of C and of the shrunk case.
Records: corpus/README.md carries a line naming F6 and `held (round 50)`; a corpus/knowledge/ file new
since BASE names F6 and its `source:` lines cite an S-id whose SOURCES row is `mined`, opened 2026-10-26;
`tools/shrink-case.py --selftest` exits 0.

PASS iff the shrinker is present, both panels are valid and pinned, the generator finds every mutant,
at least N-1 of N mutants are ok on every check, the ok mutants shrink in total (sum after < sum before),
the records hold and the selftest exits 0. Last stdout line `C2_R50: ... total=<n> C2_R50_PASS=<bool>`;
exit 0 iff PASS, 1 otherwise, 2 on setup error.

What it cannot see: how the shrinker searches (ddmin, greedy, or otherwise) beyond its logged cost, and
whether a shrinker that only meets 1-minimality on these 20 cases generalises; the hidden panel is the
generalisation probe.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

BASE = 'e3729de862f73ae080d98fcf522a7081ce16e40a'
GEN_REV = '7d3d977f39acaa5723a696dff85ab183c80ddc8b'
GEN_SHA256 = '0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05'
GUARD = 'tools/staged-id-guard.py'
GUARD_SHA256 = '03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8'
SHRINKER = 'tools/shrink-case.py'
GENERATOR = 'tools/pbt-staged-id.py'
PUBLIC_SHA256 = 'd6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1'
HIDDEN_SHA256 = '5c14e9a6843b3aae99abb7ffbd92bb3aa1e594391776edcfbf65d941fe8b0cc6'
SEED, CASES = '4949', '400'
SHRINK_TIMEOUT = 900
SELFTEST_TIMEOUT = 300
OPENED = '2026-10-26'
INSTRUMENT = ("import os as _r50_os\n"
              "with open(_r50_os.path.join(_r50_os.path.dirname(_r50_os.path.abspath(__file__)), '.runs'), 'a') "
              "as _r50_fh:\n    _r50_fh.write('%s\\n')\n")
TERMS = ('shrinker_absent', 'gen_pin', 'guard_pin', 'panel_invalid', 'unfound', 'ok_short', 'no_reduction',
         'records_bad', 'selftest_bad')


class Setup(Exception):
    pass


def git_show(lane, rev, path):
    proc = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def sha(data):
    return hashlib.sha256(data).hexdigest()


def instrument(src, tag):
    """Insert the run logger before the guard's first top-level import (after its docstring)."""
    lines = src.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            return '\n'.join(lines[:i]) + '\n' + (INSTRUMENT % tag) + '\n'.join(lines[i:])
    raise Setup('guard has no top-level import to anchor the run logger')


def load_generator(path):
    spec = importlib.util.spec_from_file_location('frozen_pbt_r49', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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
    """Every case with exactly one unit removed."""
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


class Judge:
    def __init__(self, gen, pristine, mutant, casedir):
        self.gen, self.pristine, self.mutant, self.casedir = gen, pristine, mutant, casedir

    def kills(self, case):
        if self.gen.check(case, self.gen.run_guard(self.mutant, self.casedir, case)) is None:
            return False
        return self.gen.check(case, self.gen.run_guard(self.pristine, self.casedir, case)) is None


def apply_mutant(src, mutant):
    if not isinstance(mutant, dict) or not isinstance(mutant.get('old'), str) or not isinstance(mutant.get('new'), str):
        return None
    if src.count(mutant['old']) != 1:
        return None
    return src.replace(mutant['old'], mutant['new'])


def find_case(gen_path, guard_path, dump, env):
    proc = subprocess.run([sys.executable, '-I', gen_path, '--guard', guard_path, '--seed', SEED, '--cases', CASES,
                           '--dump', dump], capture_output=True, env=env, timeout=3600)
    last = proc.stdout.decode('utf-8', 'replace').strip().split('\n')[-1]
    m = re.search(r'counterexample=(\d+)', last)
    if proc.returncode != 1 or not m:
        return None
    index = int(m.group(1))
    with open(dump, encoding='utf-8') as fh:
        for raw in fh:
            row = json.loads(raw)
            if row.get('index') == index:
                return {'registry': row['registry'], 'staged': row['staged'], 'map': row['map']}
    return None


def measure(lane, rev, work, public, hidden, public_sha=PUBLIC_SHA256, hidden_sha=HIDDEN_SHA256, base=BASE,
            log=print, gen_lane=None):
    counts = {t: 0 for t in TERMS}
    os.makedirs(work, exist_ok=True)
    if os.listdir(work):
        raise Setup('work dir is not empty: ' + work)
    env = dict(os.environ, TMPDIR=work)
    gen_bytes = git_show(gen_lane or lane, GEN_REV, GENERATOR)
    if gen_bytes is None or sha(gen_bytes) != GEN_SHA256:
        counts['gen_pin'] = 1
        raise Setup('frozen generator unavailable or digest mismatch')
    frozen_gen = os.path.join(work, 'frozen-pbt.py')
    with open(frozen_gen, 'wb') as fh:
        fh.write(gen_bytes)
    gen = load_generator(frozen_gen)
    guard_bytes = git_show(lane, rev, GUARD)
    if guard_bytes is None or sha(guard_bytes) != GUARD_SHA256:
        counts['guard_pin'] = 1
        guard_bytes = git_show(lane, BASE, GUARD) or b''
    guard_src = guard_bytes.decode('utf-8')
    panel = []
    for label, path, pin in (('public', public, public_sha), ('hidden', hidden, hidden_sha)):
        try:
            raw = open(path, 'rb').read()
            doc = json.loads(raw.decode('utf-8'))
        except (OSError, ValueError):
            counts['panel_invalid'] += 1
            continue
        if sha(raw) != pin or not isinstance(doc.get('mutants'), list):
            counts['panel_invalid'] += 1
            continue
        panel += [(label, m) for m in doc['mutants']]
    shrinker = git_show(lane, rev, SHRINKER)
    tooldir = os.path.join(work, 'tool')
    os.makedirs(tooldir)
    if shrinker is None:
        counts['shrinker_absent'] = 1
    else:
        with open(os.path.join(tooldir, 'shrink-case.py'), 'wb') as fh:
            fh.write(shrinker)
        rev_gen = git_show(lane, rev, GENERATOR)
        if rev_gen is not None:
            with open(os.path.join(tooldir, 'pbt-staged-id.py'), 'wb') as fh:
                fh.write(rev_gen)
        try:
            st = subprocess.run([sys.executable, '-I', os.path.join(tooldir, 'shrink-case.py'), '--selftest'],
                                capture_output=True, cwd=tooldir, env=env, timeout=SELFTEST_TIMEOUT)
            st_rc = st.returncode
            log('SELFTEST exit=%d last=%s' % (st_rc, st.stdout.decode('utf-8', 'replace').strip().split('\n')[-1][:200]))
        except subprocess.TimeoutExpired:
            st_rc = 124
            log('SELFTEST timeout')
        if st_rc != 0:
            counts['selftest_bad'] = 1
    ok = 0
    before_sum = after_sum = 0
    for n, (label, mutant) in enumerate(panel):
        mid = mutant.get('id', '?%d' % n) if isinstance(mutant, dict) else '?%d' % n
        msrc = apply_mutant(guard_src, mutant)
        if msrc is None:
            counts['panel_invalid'] += 1
            log('MUTANT %s panel=%s invalid' % (mid, label))
            continue
        d = os.path.join(work, 'm%02d' % n)
        ver, shr, casedir = os.path.join(d, 'ver'), os.path.join(d, 'shr'), os.path.join(d, 'case')
        for x in (ver, shr, casedir, os.path.join(shr, 'tmp')):
            os.makedirs(x)
        vp, vm = os.path.join(ver, 'pristine.py'), os.path.join(ver, 'mutant.py')
        with open(vp, 'w', encoding='utf-8') as fh:
            fh.write(guard_src)
        with open(vm, 'w', encoding='utf-8') as fh:
            fh.write(msrc)
        case = find_case(frozen_gen, vm, os.path.join(d, 'dump.jsonl'), env)
        if case is None:
            counts['unfound'] += 1
            log('MUTANT %s panel=%s unfound' % (mid, label))
            continue
        if shrinker is None:
            continue
        sp, sm = os.path.join(shr, 'pristine.py'), os.path.join(shr, 'mutant.py')
        with open(sp, 'w', encoding='utf-8') as fh:
            fh.write(instrument(guard_src, 'p'))
        with open(sm, 'w', encoding='utf-8') as fh:
            fh.write(instrument(msrc, 'm'))
        cpath, opath = os.path.join(shr, 'case.json'), os.path.join(shr, 'out.json')
        with open(cpath, 'w', encoding='utf-8') as fh:
            json.dump(case, fh)
        try:
            proc = subprocess.run([sys.executable, '-I', os.path.join(tooldir, 'shrink-case.py'), '--pristine', sp,
                                   '--mutant', sm, '--case', cpath, '--out', opath], capture_output=True, cwd=shr,
                                  env=dict(env, TMPDIR=os.path.join(shr, 'tmp')), timeout=SHRINK_TIMEOUT)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            rc = 124
        logged = 0
        if os.path.exists(os.path.join(shr, '.runs')):
            with open(os.path.join(shr, '.runs')) as fh:
                logged = sum(1 for _ in fh)
        try:
            out = json.load(open(opath, encoding='utf-8'))
        except (OSError, ValueError):
            out = None
        judge = Judge(gen, vp, vm, casedir)
        flags = {'exit0': rc == 0, 'valid': False, 'subset': False, 'kills': False, 'minimal': False,
                 'cost': False, 'reduced': False}
        ub, ua = units(case), None
        if isinstance(out, dict) and valid_case(out.get('case')):
            s = {'registry': out['case']['registry'], 'staged': out['case']['staged'], 'map': out['case'].get('map')}
            flags['valid'] = True
            ua = units(s)
            flags['subset'] = is_subcase(s, case)
            flags['kills'] = judge.kills(s)
            flags['minimal'] = flags['kills'] and not any(judge.kills(r) for r in removals(s))
            flags['cost'] = (out.get('runs') == logged and isinstance(out.get('runs'), int)
                             and out.get('units_before') == ub and out.get('units_after') == ua)
            flags['reduced'] = ua <= ub
        good = all(flags.values())
        if good:
            ok += 1
            before_sum += ub
            after_sum += ua
        log('MUTANT %s panel=%s exit=%d units=%s->%s runs=%s logged=%d %s %s' % (
            mid, label, rc, ub, ua, out.get('runs') if isinstance(out, dict) else None, logged,
            ' '.join('%s=%d' % (k, v) for k, v in flags.items()), 'OK' if good else 'FAIL'))
    total_mutants = len(panel)
    if shrinker is not None:
        counts['ok_short'] = max(0, (total_mutants - 1) - ok)
        counts['no_reduction'] = 0 if (ok and after_sum < before_sum) else 1
    else:
        counts['ok_short'] = max(0, total_mutants - 1)
        counts['no_reduction'] = 1
    rec = records(lane, rev, base)
    counts['records_bad'] = sum(1 for v in rec.values() if not v)
    total = sum(counts.values())
    return counts, {'mutants': total_mutants, 'ok': ok, 'units_before': before_sum, 'units_after': after_sum,
                    'records': rec}, total


def records(lane, rev, base):
    out = {'readme_f6': False, 'entry': False}
    readme = git_show(lane, rev, 'corpus/README.md')
    if readme is not None:
        out['readme_f6'] = any(re.search(r'\bF6\b', l) and 'held (round 50)' in l
                               for l in readme.decode('utf-8', 'replace').split('\n'))
    reg = git_show(lane, rev, 'corpus/SOURCES.md')
    rows = {}
    if reg is not None:
        for l in reg.decode('utf-8', 'replace').split('\n'):
            m = re.match(r'^ {0,3}\|\s*(S\d{3,})\s*\|', l)
            if m:
                cells = [c.strip() for c in l.strip().strip('|').split('|')]
                rows[m.group(1)] = cells
    proc = subprocess.run(['git', '-C', lane, 'diff', '--name-only', '--diff-filter=A', base, rev, '--',
                           'corpus/knowledge'], capture_output=True)
    for path in proc.stdout.decode('utf-8', 'replace').split('\n'):
        if not path.endswith('.md'):
            continue
        text = (git_show(lane, rev, path) or b'').decode('utf-8', 'replace')
        if not re.search(r'\bF6\b', text):
            continue
        for l in text.split('\n'):
            if not l.startswith('source:'):
                continue
            for sid in re.findall(r'\bS\d{3,}\b', l):
                cells = rows.get(sid)
                if cells and len(cells) >= 11 and cells[7] == 'mined' and cells[8] == OPENED:
                    out['entry'] = True
    return out


def self_sha():
    with open(os.path.abspath(__file__), 'rb') as fh:
        return sha(fh.read())


def line(rev, counts, stat, total):
    parts = ['C2_R50: self=%s rev=%s mutants=%d ok=%d units_before=%d units_after=%d' % (
        self_sha()[:12], rev, stat['mutants'], stat['ok'], stat['units_before'], stat['units_after'])]
    parts += ['%s=%d' % (k, int(v)) for k, v in sorted(stat['records'].items())]
    parts += ['%s=%d' % (t, counts[t]) for t in TERMS]
    parts.append('total=%d C2_R50_PASS=%s' % (total, 'true' if total == 0 else 'false'))
    return ' '.join(parts)


# ------------------------------------------------------------------------------------------------
# selftest: a fixture lane (real guard, frozen generator) and four fixture shrinkers, measured end to
# end through measure() (round-49 mutation finding: its selftests never reached measure()).
# ------------------------------------------------------------------------------------------------
REF_SHRINKER = r'''
import argparse, importlib.util, json, os, sys
def load():
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location('g', os.path.join(here, 'pbt-staged-id.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def entries(c):
    m = c.get('map')
    return m['map'] if isinstance(m, dict) and isinstance(m.get('map'), dict) else None
def units(c):
    out = []
    for f in ('registry', 'staged'):
        for i in range(len(c[f].splitlines(True))): out.append((f, i))
    e = entries(c)
    if e is not None:
        out += [('map', k) for k in e]
    return out
def drop(c, u):
    f, i = u
    if f == 'map':
        m = dict(c['map']); m['map'] = {k: v for k, v in c['map']['map'].items() if k != i}; return dict(c, map=m)
    l = c[f].splitlines(True); return dict(c, **{f: ''.join(l[:i] + l[i+1:])})
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--pristine'); ap.add_argument('--mutant')
    ap.add_argument('--case'); ap.add_argument('--out'); ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest: print('REF_SELFTEST ok'); return 0
    g = load(); c = json.load(open(a.case)); runs = [0]; d = os.environ.get('TMPDIR', '.')
    def run(guard, x):
        runs[0] += 1
        return g.run_guard(guard, d, x)
    def kills(x):
        return g.check(x, run(a.mutant, x)) is not None and g.check(x, run(a.pristine, x)) is None
    before = len(units(c)); MODE
    changed = True
    while changed:
        changed = False
        for u in units(c):
            t = drop(c, u)
            if kills(t): c = t; changed = True; break
    json.dump({'case': c, 'runs': runs[0] + LIE, 'units_before': before, 'units_after': len(units(c))}, open(a.out, 'w'))
    return 0
sys.exit(main())
'''


def selftest(lane, work):
    results = []

    logs = []

    def case(name, ok):
        results.append((name, bool(ok)))
        print('SELFTEST %-40s %s' % (name, 'ok' if ok else 'FAIL'))
        if not ok:
            for entry in logs:
                print('  LOG ' + entry)
        del logs[:]

    root = os.path.join(work, 'c2r50-selftest')
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    try:
        repo = os.path.join(root, 'lane')
        os.makedirs(repo)
        env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t',
                   GIT_COMMITTER_EMAIL='t@t')

        def g(*args):
            return subprocess.run(['git', '-C', repo] + list(args), check=True, capture_output=True, env=env)
        g('init', '-q')
        if os.path.realpath(g('rev-parse', '--show-toplevel').stdout.decode().strip()) != os.path.realpath(repo):
            raise Setup('fixture toplevel mismatch')

        def write(path, data):
            full = os.path.join(repo, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'wb') as fh:
                fh.write(data if isinstance(data, bytes) else data.encode('utf-8'))

        def commit(msg):
            g('add', '-A')
            g('commit', '-q', '--allow-empty', '-m', msg)
            return g('rev-parse', 'HEAD').stdout.decode().strip()
        gen = git_show(lane, GEN_REV, GENERATOR)
        guard = git_show(lane, BASE, GUARD)
        if gen is None or guard is None:
            raise Setup('selftest needs the lane generator and guard')
        write(GUARD, guard)
        write(GENERATOR, gen)
        write('corpus/README.md', '| F6 | fixture minimization | open |\n')
        write('corpus/SOURCES.md', '| S001 | doc — https://e.x/a | paper | A | s | a | t | mined | 2026-10-26 | 365d | x |\n')
        fbase = commit('base')
        write('corpus/README.md', '| F6 | fixture minimization | held (round 50) |\n')
        write('corpus/knowledge/shrink.md', 'source: S001 — https://e.x/a\nground: F6\n')
        records_rev = commit('records')
        mut = {'id': 'T01', 'old': "ROW_RE = re.compile(r'^ {0,3}\\|", 'new': "ROW_RE = re.compile(r'^\\|"}
        pub = os.path.join(root, 'public.json')
        hid = os.path.join(root, 'hidden.json')
        with open(pub, 'w') as fh:
            json.dump({'mutants': [mut]}, fh)
        with open(hid, 'w') as fh:
            json.dump({'mutants': [dict(mut, id='T02')]}, fh)
        psha, hsha = sha(open(pub, 'rb').read()), sha(open(hid, 'rb').read())
        n = [0]

        def run(shrinker_src, rev=None, public_sha=psha):
            if shrinker_src is None:
                g('rm', '-q', '--ignore-unmatch', SHRINKER)
            else:
                write(SHRINKER, shrinker_src)
            r = commit('shrinker') if rev is None else rev
            n[0] += 1
            w = os.path.join(root, 'w%d' % n[0])
            counts, stat, total = measure(repo, r, w, pub, hid, public_sha, hsha, fbase, log=lambda *a: logs.append(' '.join(map(str, a))),
                                          gen_lane=lane)
            logs.append('counts=%r stat=%r total=%d' % (counts, stat, total))
            shutil.rmtree(w, ignore_errors=True)
            return counts, stat, total
        ref = REF_SHRINKER.replace('MODE', 'pass').replace('LIE', '0')
        counts, stat, total = run(ref)
        case('reference shrinker passes', total == 0 and stat['ok'] == 2 and stat['units_after'] < stat['units_before'])
        counts, stat, total = run(REF_SHRINKER.replace('MODE', 'pass').replace('LIE', '3'))
        case('misreported cost fails', counts['ok_short'] == 1 and stat['ok'] == 0)
        ident = REF_SHRINKER.replace('MODE', "json.dump({'case': c, 'runs': 0, 'units_before': before, "
                                             "'units_after': before}, open(a.out, 'w')); return 0").replace('LIE', '0')
        counts, stat, total = run(ident)
        case('identity shrinker fails minimality', counts['ok_short'] == 1 and stat['ok'] == 0)
        fresh = ref.replace("json.dump({'case': c,", "c = dict(c, registry=c['registry'] + '| S999 | z | a | b | c |\\n'); "
                                                    "json.dump({'case': c,")
        counts, stat, total = run(fresh)
        case('non-subset case fails', counts['ok_short'] == 1)
        counts, stat, total = run(None)
        case('absent shrinker fails', counts['shrinker_absent'] == 1 and total > 1)
        st_bad = ref.replace("print('REF_SELFTEST ok'); return 0", "return 1")
        counts, stat, total = run(st_bad)
        case('failing tool selftest counted', counts['selftest_bad'] == 1 and total == 1)
        g('checkout', '-q', fbase)
        write(SHRINKER, ref)
        rev_no_records = commit('no records')
        counts, stat, total = run(None, rev=rev_no_records)
        case('missing F6 records counted', counts['records_bad'] == 2 and total == 2)
        counts, stat, total = run(None, rev=records_rev, public_sha='0' * 64)
        case('panel digest mismatch counted', counts['panel_invalid'] == 1)
        case('instrumentation keeps the docstring', instrument(guard.decode(), 'p').startswith(guard.decode()[:40]))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    failed = [n for n, ok in results if not ok]
    print('C2_R50_SELFTEST: cases=%d failed=%d' % (len(results), len(failed)))
    return 0 if not failed else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--work')
    ap.add_argument('--panel')
    ap.add_argument('--hidden')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    try:
        if not a.lane or not a.work:
            raise Setup('--lane and --work are required')
        if a.selftest:
            os.makedirs(a.work, exist_ok=True)
            return selftest(a.lane, a.work)
        if not a.rev or not a.panel or not a.hidden:
            raise Setup('--rev, --panel and --hidden are required')
        rev = subprocess.run(['git', '-C', a.lane, 'rev-parse', '--verify', a.rev + '^{commit}'],
                             capture_output=True).stdout.decode().strip()
        if not rev:
            raise Setup('unknown revision ' + a.rev)
        counts, stat, total = measure(a.lane, rev, a.work, a.panel, a.hidden)
        print(line(rev, counts, stat, total))
        return 0 if total == 0 else 1
    except Setup as exc:
        print('C2_R50: setup error: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
