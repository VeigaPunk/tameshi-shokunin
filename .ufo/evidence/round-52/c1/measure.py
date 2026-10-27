#!/usr/bin/env python3
"""Round-52 C1 counter (operability): the lane's two registry homes return their registered outcomes at REV.

Usage: measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain]      measure.py --selftest

Components, all read from git objects (never the working tree):
  R  the entry-command monitor: tools/registry-check.py as committed at BASE (frozen bytes, materialised into WORK)
     run as `python3 -I WORK/registry-check.py --root LANE --rev REV`, stdin /dev/null, TMPDIR=WORK/tmp.
     not_held = active rows whose line ends `differs` (or any row line the monitor does not mark held) + 1 when the
     summary line `REGISTRY_CHECK: held=H/N` is missing or H != N.
  D  dropped = BASE active row names (frozen in c1/base-active.json) that are not active at REV.
  M  mte_row = 1 unless the REV registry row `mte-interop-check` is active, kind gate, argv carries
     tools/mte-interop.py and --check, expects exit 0, and its stdout_contains holds exactly
     `MTE_INTEROP: PASS legs_conforming=K/K` with K = len(LEG_TABLE) in tools/mte-interop.py at REV.
  C  c3 = the `total=` value of the frozen round-51 C3 counter (.ufo/evidence/round-51/c3/measure.py, bytes checked
     against its round-51 freeze digest) run at REV with --work WORK/c3 (a fresh clone outside the fleet root:
     a self-test that reads sibling repos through ROOT.parent fails there). Missing/garbled output counts 30.
  G  r21_cases_missing = how many of the 11 self-test case literals of tools/round21-measure.py at BASE
     (R21_CASES below) are absent from the file at REV (a stub that only prints a pass line keeps none of them).
total = not_held + dropped + mte_row + c3 + r21_cases_missing; prints `C1_R52: rev=… held=H/N not_held=… dropped=…
mte_row=… c3_covered=… c3_total=… r21_cases_missing=… total=… C1_R52_PASS=<true|false>`; exit 0 iff total == 0.
"""
import argparse, ast, hashlib, json, os, re, subprocess, sys

BASE = 'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4'
C3_PATH = '.ufo/evidence/round-51/c3/measure.py'
C3_SHA = 'a3abbd3b7888432919a999b1de357d4b71fa7262d55ae2f5ff97be4dddb3fd3a'
HERE = os.path.dirname(os.path.abspath(__file__))
ROW = re.compile(r'^ROW (\S+)( superseded)? expect=(\S+) got=(\S+)(?: (held|differs))?\s*$', re.M)
SUMMARY = re.compile(r'^REGISTRY_CHECK: held=(\d+)/(\d+)', re.M)
R21_CASES = ['check("c1-killed"', 'check("c1-missing-anchor"', 'check("c1-pristine-red"', 'check("c1-survived"',
             'check("c2-complete"', 'check("c2-missing-profile"', 'check("c2-unmined-source"',
             'check("c2-wrong-classification"', 'check("c2-wrong-pin"', 'check(claim + "-unknown-rev"',
             'check(claim + "-usage"']


def git(lane, *args):
    return subprocess.run(['git', '-C', lane] + list(args), capture_output=True)


def show(lane, rev, path):
    r = git(lane, 'show', '%s:%s' % (rev, path))
    return r.stdout if r.returncode == 0 else None


def leg_count(src):
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == 'LEG_TABLE' for t in node.targets):
            return len(node.value.keys)
    return None


def mte_row_ok(registry, mte_src):
    try:
        k = leg_count(mte_src)
    except SyntaxError:
        return False, 'mte-interop.py unparsable'
    rows = [r for r in registry.get('rows', []) if r.get('name') == 'mte-interop-check']
    if len(rows) != 1:
        return False, 'rows=%d' % len(rows)
    r = rows[0]
    argv = r.get('argv') or []
    exp = r.get('expect') or {}
    want = 'MTE_INTEROP: PASS legs_conforming=%s/%s' % (k, k)
    ok = (r.get('status') == 'active' and r.get('kind') == 'gate' and 'tools/mte-interop.py' in argv
          and '--check' in argv and exp.get('exit') == 0 and want in (exp.get('stdout_contains') or []))
    return ok, 'legs=%s want=%r status=%s needles=%s' % (k, want, r.get('status'), exp.get('stdout_contains'))


def parse_registry_check(out):
    rows = ROW.findall(out)
    not_held = [name for name, sup, _e, _g, verdict in rows if not sup and verdict != 'held']
    m = SUMMARY.search(out)
    held, n = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    extra = 0 if (m and held == n) else 1
    return held, n, not_held, extra


def parse_c3(out):
    line = next((ln for ln in out.split('\n') if ln.startswith('C3_R51:') and 'C3_R51_PASS=' in ln), '')
    m = re.search(r' covered=(\d+) .*? total=(\d+) ', line)
    return (int(m.group(1)), int(m.group(2))) if m else (None, 30)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--lane'); p.add_argument('--rev'); p.add_argument('--work')
    p.add_argument('--explain', action='store_true'); p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not (a.lane and a.rev and a.work):
        p.error('--lane, --rev and --work are required')
    if not os.path.isdir(a.work) or os.listdir(a.work):
        print('C1_R52: SETUP work dir must exist and be empty'); return 2
    rev = git(a.lane, 'rev-parse', '--verify', a.rev + '^{commit}').stdout.decode().strip()
    if not rev:
        print('C1_R52: SETUP rev unresolvable'); return 2
    tmp = os.path.join(a.work, 'tmp'); os.makedirs(tmp)
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': os.environ.get('HOME', '/'), 'TMPDIR': tmp,
           'LANG': 'C.UTF-8', 'HYAKU_SCRATCH': os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')}
    # R
    rc_src = show(a.lane, BASE, 'tools/registry-check.py')
    rc_path = os.path.join(a.work, 'registry-check.py')
    open(rc_path, 'wb').write(rc_src)
    r = subprocess.run([sys.executable, '-I', rc_path, '--root', a.lane, '--rev', rev], env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=3600)
    open(os.path.join(a.work, 'registry-check.stdout'), 'w').write(r.stdout + r.stderr)
    held, n, not_held, extra = parse_registry_check(r.stdout)
    # D
    base_active = json.load(open(os.path.join(HERE, 'base-active.json')))['active']
    try:
        registry = json.loads(show(a.lane, rev, 'tools/registry.json') or b'{}')
    except ValueError:
        registry = {}
    active = {x.get('name') for x in registry.get('rows', []) if x.get('status') == 'active'}
    dropped = sorted(set(base_active) - active)
    # M
    ok, why = mte_row_ok(registry, (show(a.lane, rev, 'tools/mte-interop.py') or b'').decode('utf-8', 'replace'))
    # C
    c3_src = show(a.lane, rev, C3_PATH) or b''
    c3_out = ''
    if hashlib.sha256(c3_src).hexdigest() == C3_SHA:
        c3_file = os.path.join(a.work, 'c3-measure.py'); open(c3_file, 'wb').write(c3_src)
        c3w = os.path.join(a.work, 'c3'); os.makedirs(c3w)
        c = subprocess.run([sys.executable, c3_file, '--lane', a.lane, '--rev', rev, '--work', c3w, '--explain'],
                           env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=3600)
        c3_out = c.stdout + c.stderr
        open(os.path.join(a.work, 'c3.stdout'), 'w').write(c3_out)
    covered, c3_total = parse_c3(c3_out)
    # G
    r21 = (show(a.lane, rev, 'tools/round21-measure.py') or b'').decode('utf-8', 'replace')
    gone = cases_missing(r21)
    if a.explain:
        print('C1_REGISTRY_CHECK exit=%d summary=%s/%s not_held=%s' % (r.returncode, held, n, not_held))
        print('C1_DROPPED %s' % (dropped or 'none'))
        print('C1_MTE_ROW %s %s' % ('ok' if ok else 'BAD', why))
        print('C1_R21_CASES missing=%s' % (gone or 'none'))
        for ln in c3_out.split('\n'):
            if ln.startswith('C3_TOOL') and ': OK' not in ln:
                print('C1_' + ln)
    total = len(not_held) + extra + len(dropped) + (0 if ok else 1) + c3_total + len(gone)
    print('C1_R52: rev=%s held=%s/%s not_held=%d dropped=%d mte_row=%d c3_covered=%s c3_total=%d r21_cases_missing=%d total=%d C1_R52_PASS=%s'
          % (rev, held, n, len(not_held) + extra, len(dropped), 0 if ok else 1, covered, c3_total, len(gone), total,
             'true' if total == 0 else 'false'))
    return 0 if total == 0 else 1


def cases_missing(src):
    return [c for c in R21_CASES if c not in src]


def selftest():
    fails = 0
    def t(name, cond):
        nonlocal fails
        print('SELFTEST %s %s' % (name, 'ok' if cond else 'FAIL')); fails += 0 if cond else 1
    out = 'ROW a expect=0 got=0 held\nROW b superseded expect=0 got=0\nROW c expect=0 got=0 differs\nREGISTRY_CHECK: held=1/2 superseded=1\n'
    t('rc-differs', parse_registry_check(out)[2:] == (['c'], 1))
    t('rc-clean', parse_registry_check('ROW a expect=0 got=0 held\nREGISTRY_CHECK: held=1/1 superseded=0\n')[2:] == ([], 0))
    t('rc-nosummary', parse_registry_check('ROW a expect=0 got=0 held\n')[3] == 1)
    mte = "LEG_TABLE = {'a': 1, 'b': 2}\n"
    row = {'name': 'mte-interop-check', 'kind': 'gate', 'status': 'active',
           'argv': ['python3', 'tools/mte-interop.py', '--check'],
           'expect': {'exit': 0, 'stdout_contains': ['MTE_INTEROP: PASS legs_conforming=2/2']}}
    t('mte-ok', mte_row_ok({'rows': [row]}, mte)[0])
    t('mte-stale', not mte_row_ok({'rows': [dict(row, expect={'exit': 0, 'stdout_contains': ['MTE_INTEROP: PASS legs_conforming=1/1']})]}, mte)[0])
    t('mte-superseded', not mte_row_ok({'rows': [dict(row, status='superseded')]}, mte)[0])
    t('mte-argv', not mte_row_ok({'rows': [dict(row, argv=['true'])]}, mte)[0])
    t('c3-parse', parse_c3('x\nC3_R51: tools=30 rows=32 covered=29 missing=1 total=1 C3_R51_PASS=false\n') == (29, 1))
    t('c3-garbled', parse_c3('') == (None, 30))
    print('C1_SELFTEST: cases=9 failed=%d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
