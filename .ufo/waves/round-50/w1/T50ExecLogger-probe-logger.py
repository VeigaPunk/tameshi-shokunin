#!/usr/bin/env python3
"""T50ExecLogger probe: does the C2 counter's run logger (c2/measure.py instrument) count exactly
one line per guard process and nothing else, without changing the guard's stdout/exit?"""
import ast
import hashlib
import importlib.util
import json
import os
import random
import shutil
import stat
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
S = '/fast/scratch/hyaku/tameshi-r50/T50ExecLogger'
W = os.path.join(S, 'w')
COUNTER = LANE + '/.ufo/evidence/round-50/c2/measure.py'
GUARD = LANE + '/tools/staged-id-guard.py'
GEN = LANE + '/tools/pbt-staged-id.py'
PANEL49 = LANE + '/.ufo/evidence/round-49/c2/panel.json'
RECEIPT = LANE + '/.ufo/waves/round-50/w1/T50ExecLogger-receipt-logger.txt'
OUT = []


def say(*a):
    line = ' '.join(str(x) for x in a)
    OUT.append(line)
    print(line)


def sha_of(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def nlines(p):
    if not os.path.exists(p):
        return 0
    with open(p) as fh:
        return sum(1 for _ in fh)


def read_lines(p):
    if not os.path.exists(p):
        return []
    with open(p) as fh:
        return [l.rstrip('\n') for l in fh]


def run(argv, **kw):
    kw.setdefault('capture_output', True)
    return subprocess.run(argv, **kw)


def digest(obs):
    return {'exit': obs['exit'], 'stdout': obs['stdout'], 'stderr': obs['stderr'],
            'json': obs['json']}


def cmp(label, a, b, extra=''):
    ok = a == b
    say('%-46s %s %s' % (label, 'IDENTICAL' if ok else 'DIFFERS', extra))
    if not ok:
        for k in ('exit', 'stdout', 'stderr'):
            if a[k] != b[k]:
                say('   %s: plain=%r inst=%r' % (k, a[k][:300], b[k][:300]))
        if a['json'] != b['json']:
            say('   json: plain=%r inst=%r' % (str(a['json'])[:200], str(b['json'])[:200]))
    return ok


def main():
    shutil.rmtree(W, ignore_errors=True)
    os.makedirs(W)
    c2 = load('r50_c2_measure', COUNTER)
    gen = load('gen49', GEN)
    say('SECTION 0 identity')
    say('counter %s sha=%s self_sha=%s' % (COUNTER, sha_of(COUNTER), c2.self_sha()))
    say('guard   %s sha=%s pin=%s match=%s' % (GUARD, sha_of(GUARD), c2.GUARD_SHA256,
                                               sha_of(GUARD) == c2.GUARD_SHA256))
    say('gen     %s sha=%s pin=%s match=%s' % (GEN, sha_of(GEN), c2.GEN_SHA256,
                                              sha_of(GEN) == c2.GEN_SHA256))
    say('INSTRUMENT literal = %r' % (c2.INSTRUMENT % '<TAG>'))

    guard_src = open(GUARD, encoding='utf-8').read()
    plain_src = guard_src
    inst_p = c2.instrument(guard_src, 'p')
    inst_m = c2.instrument(guard_src, 'm')
    pdir = os.path.join(W, 'plain')
    idir = os.path.join(W, 'inst')
    for d in (pdir, idir):
        os.makedirs(d)
    plain_path = os.path.join(pdir, 'guard.py')
    inst_path = os.path.join(idir, 'guard.py')
    instm_path = os.path.join(idir, 'guard-m.py')
    open(plain_path, 'w', encoding='utf-8').write(plain_src)
    open(inst_path, 'w', encoding='utf-8').write(inst_p)
    open(instm_path, 'w', encoding='utf-8').write(inst_m)

    say('SECTION 1 insertion point')
    src_lines = guard_src.split('\n')
    anchor = next(i for i, l in enumerate(src_lines)
                  if l.startswith('import ') or l.startswith('from '))
    say('first top-level import: line %d (1-based) %r' % (anchor + 1, src_lines[anchor]))
    added = len(inst_p.split('\n')) - len(src_lines)
    say('lines added by instrument = %d; logger occupies lines %d-%d (1-based)'
        % (added, anchor + 1, anchor + added))
    say('logger body line 1 = %r' % inst_p.split('\n')[anchor])
    say('logger body line 3 = %r' % inst_p.split('\n')[anchor + 2])
    say('docstring preserved (startswith first 40 chars) = %s' % inst_p.startswith(guard_src[:40]))
    say('ast docstring preserved = %s' % (ast.get_docstring(ast.parse(inst_p)) is not None))
    try:
        compile(inst_p, 'x', 'exec')
        say('compile(instrumented) = OK')
    except SyntaxError as exc:
        say('compile(instrumented) = SyntaxError %s' % exc)
    top = ast.parse(inst_p).body
    kinds = [type(n).__name__ for n in top[:4]]
    say('first 4 top-level AST nodes = %s' % kinds)
    say('logger at module top level (docstring, Import os, With, then guard imports; no '
        'FunctionDef among the first four) = %s'
        % (kinds[:3] == ['Expr', 'Import', 'With'] and 'FunctionDef' not in kinds))

    say('SECTION 2 behaviour parity through the round-49 generator run_guard')
    rnd = random.Random(4949)
    order = list(range(len(gen.RECIPES)))
    rnd.shuffle(order)
    cases = [gen.RECIPES[order[i % len(order)]](rnd) for i in range(len(gen.RECIPES))]
    say('cases = %d (one per RECIPES entry, seeded 4949 like run())' % len(cases))
    all_ok = True
    for i, case in enumerate(cases):
        d0 = os.path.join(W, 'c%02d' % i, 'base')
        d1 = os.path.join(W, 'c%02d' % i, 'inst')
        g1 = os.path.join(W, 'c%02d' % i, 'guard')
        for d in (d0, d1, g1):
            os.makedirs(d)
        gp, gm = os.path.join(g1, 'guard.py'), os.path.join(g1, 'guard-m.py')
        for dst, src in ((gp, inst_p), (gm, inst_m)):
            open(dst, 'w', encoding='utf-8').write(src)
        o0 = gen.run_guard(plain_path, d0, case)
        o1 = gen.run_guard(gp, d1, case)
        n1 = nlines(os.path.join(g1, '.runs'))
        m = case['map']
        mags = 'none' if m is None else '%s(len=%d)' % (type(m).__name__, len(m))
        name = 'case%02d units=%d map=%s' % (i, c2.units(case), mags)
        ok = cmp(name, digest(o0), digest(o1), '| .runs after run=%d (want 1)' % n1)
        all_ok = all_ok and ok and n1 == 1
        o1m = gen.run_guard(gm, d1, case)
        nm = nlines(os.path.join(g1, '.runs'))
        okm = cmp(name + ' [mutant-tagged]', digest(o0), digest(o1m),
                  '| .runs=%d (want 2)' % nm)
        all_ok = all_ok and okm and nm == 2
    say('parity + one-line-per-process over %d cases (pristine- and mutant-tagged copies): %s'
        % (len(cases), 'ALL OK' if all_ok else 'FAILURES ABOVE'))

    say('SECTION 3 tag lines / no partial lines / N runs -> N lines (one shared dir)')
    for i in range(7):
        kd = os.path.join(W, 'k%d' % i)
        os.makedirs(kd)
        gen.run_guard(inst_path, kd, cases[i])
    got = read_lines(os.path.join(idir, '.runs'))
    say('N=7 runs into one dir -> .runs lines=%d tags=%s partial_or_foreign=%s'
        % (len(got), sorted(set(got)), [l for l in got if l not in ('p', 'm')]))
    say('observed lines=%d, want N=7' % len(got))

    say('SECTION 4 python3 -I guard --selftest with and without the logger')
    sp = run([sys.executable, '-I', plain_path, '--selftest'], capture_output=True, cwd=pdir)
    before = nlines(os.path.join(idir, '.runs'))
    si = run([sys.executable, '-I', inst_path, '--selftest'], capture_output=True, cwd=idir)
    after = nlines(os.path.join(idir, '.runs'))
    say('plain selftest exit=%d stdout_sha=%s last=%r'
        % (sp.returncode, hashlib.sha256(sp.stdout).hexdigest(),
           sp.stdout.decode('utf-8', 'replace').strip().split('\n')[-1][:120]))
    say('inst  selftest exit=%d stdout_sha=%s last=%r'
        % (si.returncode, hashlib.sha256(si.stdout).hexdigest(),
           si.stdout.decode('utf-8', 'replace').strip().split('\n')[-1][:120]))
    say('selftest stdout byte-identical=%s exit-identical=%s stderr-identical=%s .runs delta=%d '
        '(want 1)' % (sp.stdout == si.stdout, sp.returncode == si.returncode,
                      sp.stderr == si.stderr, after - before))

    say('SECTION 5 --help and setup-refusal paths')
    hp = run([sys.executable, '-I', plain_path, '--help'], capture_output=True, cwd=pdir)
    b0 = nlines(os.path.join(idir, '.runs'))
    hi = run([sys.executable, '-I', inst_path, '--help'], capture_output=True, cwd=idir)
    b1 = nlines(os.path.join(idir, '.runs'))
    say('--help exit plain=%d inst=%d stdout_identical=%s delta=%d'
        % (hp.returncode, hi.returncode, hp.stdout == hi.stdout, b1 - b0))
    rp = run([sys.executable, '-I', plain_path, '--json'], capture_output=True, cwd=pdir)
    b0 = nlines(os.path.join(idir, '.runs'))
    ri = run([sys.executable, '-I', inst_path, '--json'], capture_output=True, cwd=idir)
    b1 = nlines(os.path.join(idir, '.runs'))
    say('missing-args exit plain=%d inst=%d stderr=%r identical=%s delta=%d'
        % (rp.returncode, ri.returncode, ri.stderr[-120:],
           (rp.returncode, rp.stdout, rp.stderr) == (ri.returncode, ri.stdout, ri.stderr),
           b1 - b0))

    say('SECTION 6 guard imported as a module, never run')
    b0 = nlines(os.path.join(idir, '.runs'))
    imp = run([sys.executable, '-I', '-c',
               'import importlib.util as u,sys;'
               's=u.spec_from_file_location("g",sys.argv[1]);m=u.module_from_spec(s);'
               's.loader.exec_module(m);print("exec_module ok")', inst_path],
              capture_output=True, cwd=W)
    b1 = nlines(os.path.join(idir, '.runs'))
    say('import-only exit=%d stdout=%r ; .runs delta=%d (1 means a bare import also logs)'
        % (imp.returncode, imp.stdout.decode('utf-8', 'replace').strip(), b1 - b0))

    say('SECTION 7 relative script path / cwd dependence')
    b0 = nlines(os.path.join(idir, '.runs'))
    rel = run([sys.executable, '-I', 'guard.py', '--selftest'], capture_output=True, cwd=idir)
    b1 = nlines(os.path.join(idir, '.runs'))
    say('cwd=guard dir, argv guard.py: exit=%d delta=%d' % (rel.returncode, b1 - b0))
    outside = os.path.join(W, 'elsewhere')
    os.makedirs(outside, exist_ok=True)
    b0 = nlines(os.path.join(idir, '.runs'))
    rel2 = run([sys.executable, '-I', '../inst/guard.py', '--selftest'], capture_output=True,
               cwd=outside)
    b1 = nlines(os.path.join(idir, '.runs'))
    say('cwd=elsewhere, argv ../inst/guard.py: exit=%d delta=%d (abspath(__file__) -> guard dir)'
        % (rel2.returncode, b1 - b0))
    tmpcopy = os.path.join(W, 'copied')
    os.makedirs(tmpcopy)
    shutil.copy2(inst_path, os.path.join(tmpcopy, 'guard.py'))
    b0 = nlines(os.path.join(idir, '.runs'))
    cp = run([sys.executable, '-I', os.path.join(tmpcopy, 'guard.py'), '--selftest'],
             capture_output=True, cwd=outside)
    say('guard copied to a scratch dir: exit=%d ; .runs of the ORIGINAL dir delta=%d ; '
        'copy dir .runs lines=%d' % (cp.returncode, nlines(os.path.join(idir, '.runs')) - b0,
                                     nlines(os.path.join(tmpcopy, '.runs'))))

    say('SECTION 8 read-only guard directory')
    ro = os.path.join(W, 'readonly')
    os.makedirs(ro)
    ro_guard = os.path.join(ro, 'guard.py')
    shutil.copy2(inst_path, ro_guard)
    pl = os.path.join(ro, 'plain-guard.py')
    shutil.copy2(plain_path, pl)
    case = cases[0]
    cd = os.path.join(W, 'rocase')
    os.makedirs(cd)
    o_plain = gen.run_guard(pl, cd, case)
    os.chmod(ro, stat.S_IRUSR | stat.S_IXUSR)
    try:
        o_ro = gen.run_guard(ro_guard, cd, case)
    finally:
        os.chmod(ro, stat.S_IRWXU)
    say('read-only dir: plain exit=%d ; instrumented exit=%d stdout_empty=%s stderr_head=%r'
        % (o_plain['exit'], o_ro['exit'], o_ro['stdout'] == b'', o_ro['stderr'][:200]))
    say('read-only dir parity = %s' % cmp('read-only dir', digest(o_plain), digest(o_ro)))

    say('SECTION 9 public round-49 panel mutants (12): anchor + parity + one line')
    panel = json.load(open(PANEL49, encoding='utf-8'))
    say('panel sha=%s mutants=%d (pin %s)' % (sha_of(PANEL49), len(panel['mutants']),
                                             c2.PUBLIC_SHA256))
    mok = 0
    mcount = 0
    for man in panel['mutants']:
        mid = man.get('id', '?')
        msrc = c2.apply_mutant(guard_src, man)
        if msrc is None:
            say('mutant %s invalid panel entry' % mid)
            continue
        mim = c2.instrument(msrc, 'm')
        mp = os.path.join(W, 'mut_%s.py' % mid)
        open(mp, 'w', encoding='utf-8').write(msrc)
        mdir = os.path.join(W, 'mi_%s' % mid)
        os.makedirs(mdir)
        mip = os.path.join(mdir, 'mutant.py')
        open(mip, 'w', encoding='utf-8').write(mim)
        try:
            compile(mim, 'x', 'exec')
            comp = True
        except SyntaxError:
            comp = False
        d0 = os.path.join(W, 'mp_%s' % mid)
        d1 = os.path.join(W, 'mi_%s' % mid, 'case')
        os.makedirs(d0)
        os.makedirs(d1)
        a = gen.run_guard(mp, d0, case)
        b = gen.run_guard(mip, d1, case)
        n = nlines(os.path.join(mdir, '.runs'))
        same = digest(a) == digest(b)
        ast_ok = [type(x).__name__ for x in ast.parse(mim).body[:3]] == ['Expr', 'Import', 'With']
        mok += 1 if (comp and same and n == 1 and ast_ok) else 0
        mcount += 1
        say('mutant %s compile=%s logger_top=%s parity=%s .runs=%d (want 1)'
            % (mid, comp, ast_ok, same, n))
    say('public mutants meeting compile+top-level-logger+parity+one-line: %d/%d' % (mok, mcount))

    say('SECTION 10 double instrumentation (counter never does this)')
    twice = c2.instrument(inst_p, 'p')
    open(os.path.join(W, 'twice.py'), 'w', encoding='utf-8').write(twice)
    b0 = nlines(os.path.join(W, '.runs'))
    tw = run([sys.executable, '-I', os.path.join(W, 'twice.py'), '--selftest'], capture_output=True,
             cwd=W)
    b1 = nlines(os.path.join(W, '.runs'))
    say('instrument(instrument(src)) exit=%d lines/process=%d' % (tw.returncode, b1 - b0))

    say('SECTION 11 timeout boundary')
    say('GUARD_TIMEOUT in generator = %s ; the logger writes at import, so a guard killed by the '
        'timeout still logs exactly one line (logged counts STARTED processes, not completed '
        'evaluations)' % gen.GUARD_TIMEOUT)

    say('SECTION 12 counter read side')
    say('measure.py:281-284 reads sum(1 for _ in open(<shr>/.runs)) where <shr> is the directory '
        'of the --pristine copy the counter writes; the logger writes into dirname(abspath(guard)), '
        'so parity holds only while the shrinker invokes the guard file in place from <shr>')

    say('SECTION 13 durability: line survives an os._exit right after import')
    b0 = nlines(os.path.join(idir, '.runs'))
    du = run([sys.executable, '-I', '-c',
              'import importlib.util as u,sys,os;'
              's=u.spec_from_file_location("g",sys.argv[1]);m=u.module_from_spec(s);'
              's.loader.exec_module(m);sys.stdout.write("imported\\n");sys.stdout.flush();'
              'os._exit(0)', inst_path], capture_output=True, cwd=W)
    b1 = nlines(os.path.join(idir, '.runs'))
    say('import + os._exit(0): exit=%d stdout=%r .runs delta=%d (with-close already flushed)'
        % (du.returncode, du.stdout.decode('utf-8', 'replace').strip(), b1 - b0))

    say('SECTION 14 judge/find legs do not write shr/.runs (directory disjointness)')
    m0 = os.path.join(W, 'm00')
    ver, shr, casedir = (os.path.join(m0, x) for x in ('ver', 'shr', 'case'))
    for x in (ver, shr, casedir):
        os.makedirs(x)
    vp, vm = os.path.join(ver, 'pristine.py'), os.path.join(ver, 'mutant.py')
    open(vp, 'w', encoding='utf-8').write(guard_src)
    open(vm, 'w', encoding='utf-8').write(guard_src)
    open(os.path.join(shr, 'pristine.py'), 'w', encoding='utf-8').write(inst_p)
    o = gen.run_guard(vp, casedir, case)
    gen.run_guard(vm, casedir, case)
    say('judge-style runs from ver/ (uninstrumented): exit=%d ; .runs in ver=%d case=%d shr=%d'
        % (o['exit'], nlines(os.path.join(ver, '.runs')), nlines(os.path.join(casedir, '.runs')),
           nlines(os.path.join(shr, '.runs'))))
    gen.run_guard(os.path.join(shr, 'pristine.py'), casedir, case)
    say('one shrinker-style run from shr/: shr/.runs=%d ver/.runs=%d case/.runs=%d'
        % (nlines(os.path.join(shr, '.runs')), nlines(os.path.join(ver, '.runs')),
           nlines(os.path.join(casedir, '.runs'))))

    os.makedirs(os.path.dirname(RECEIPT), exist_ok=True)
    with open(RECEIPT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(OUT) + '\n')
    say('receipt written to %s' % RECEIPT)


try:
    main()
finally:
    shutil.rmtree(W, ignore_errors=True)
    print('work dir removed:', not os.path.exists(W))
