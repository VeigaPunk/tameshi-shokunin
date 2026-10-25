#!/usr/bin/env python3
"""Round-47 C2 (operability) counter: a deterministic single-site mutant pool scored against the
two hardened counters' own selftests.

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C2_R47_PASS=true iff self_pin=1, pool_pin=1, for BOTH targets (freshness, coverage) the pristine
  selftest of the target passes (exit 0, `VERDICT: PASS`, no `FAIL` line), the neutral mutants all
  survive (neutral_killed=0), the v2 target prints byte-identical stdout to the round-46 hardened
  counter over the round-45 data revision (equivalence=1), and the pool's killed total over both
  targets is >= TARGET_KILLED.
A pool mutant is one single-site AST edit named `<function>:<kind>:<ordinal>` in pool.json (the
enumeration of the round-46 hardened counters' rule code: every top-level function except
`selftest`, `main`, `extra_*` and `_x*`; kinds `cmp` comparison-operator swap, `bool` and<->or,
`not` deletion, `int` constant+1, `const` True<->False). It is applied to the target by the same
address (function qualname + kind + ordinal in `ast.walk` order) and the module is re-emitted with
`ast.unparse`; a site absent from the target is `inapplicable` and counts as not killed.
A mutant is `killed` iff `python3 <mutated copy> --selftest` exits nonzero AND prints at least one
line starting `FAIL ` (a named rule case failed); a nonzero exit with no such line is `crashed`, a
run over the timeout is `timeout`; neither counts as killed. Neutral mutants (kind `commute`) are
semantics-preserving operand swaps of a pure comparison: an AST-different, behaviour-equal edit
that a selftest pinning its own source (text or AST) would kill and a rule case cannot.
Modes:
  --lane L --rev R --targets v2     deciding run (targets read from REV)
  --lane L --rev R --targets base   the do-nothing baseline: the round-46 hardened counters
  --enumerate FILE                  seat helper: list the pool sites of any counter file
  --try FILE --group G [--ids a,b]  seat helper: score selected pool ids on a working copy
  --selftest
"""
import argparse
import ast
import concurrent.futures
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
SELF_PATH = '.ufo/evidence/round-47/hardening/pool.py'
POOL_PATH = '.ufo/evidence/round-47/hardening/pool.json'
POOL_SHA256 = 'b4f0d0758bfc3e8a8057b4e80a3b038ea228c0879fdfaf4a4f669b8c63af4483'
TARGET_KILLED = 150
DATA_REV = 'ea25e0224fc81060414b27301c27bd1344669165'
GROUPS = {
    'freshness': dict(base='.ufo/evidence/round-46/hardening/freshness-counter.py',
                      v2='.ufo/evidence/round-47/hardening/freshness-counter.py'),
    'coverage': dict(base='.ufo/evidence/round-46/hardening/coverage-counter.py',
                     v2='.ufo/evidence/round-47/hardening/coverage-counter.py'),
}
EXCLUDE = re.compile(r'^(selftest|main|extra_\w+|_x\w+)$')
CMP_SWAP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
            ast.In: ast.NotIn, ast.NotIn: ast.In, ast.Is: ast.IsNot, ast.IsNot: ast.Is}
COMMUTE = {ast.Eq: ast.Eq, ast.NotEq: ast.NotEq, ast.Lt: ast.Gt, ast.LtE: ast.GtE, ast.Gt: ast.Lt, ast.GtE: ast.LtE}
TIMEOUT = 90


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    e['GIT_CONFIG_GLOBAL'] = '/dev/null'
    e['GIT_CONFIG_NOSYSTEM'] = '1'
    return e


def git_show(lane, rev, path):
    out = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True, env=env())
    return out.stdout if out.returncode == 0 else None


def pure(node):
    if isinstance(node, (ast.Name, ast.Constant)):
        return True
    if isinstance(node, ast.Attribute):
        return pure(node.value)
    return False


def sites_of(tree):
    """Yield (qualname, kind, ordinal, node, parent-agnostic desc) in a stable order."""
    funcs = []

    def collect(body, prefix):
        for n in body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                funcs.append((prefix + n.name, n))
            elif isinstance(n, ast.ClassDef):
                collect(n.body, prefix + n.name + '.')
    collect(tree.body, '')
    for qual, fn in funcs:
        if EXCLUDE.match(fn.name):
            continue
        counts = {}
        for node in ast.walk(fn):
            kind = None
            if isinstance(node, ast.Compare) and len(node.ops) == 1:
                if type(node.ops[0]) in CMP_SWAP:
                    yield qual, 'cmp', counts.setdefault('cmp', 0), node, type(node.ops[0]).__name__
                    counts['cmp'] += 1
                if type(node.ops[0]) in COMMUTE and pure(node.left) and pure(node.comparators[0]):
                    yield qual, 'commute', counts.setdefault('commute', 0), node, type(node.ops[0]).__name__
                    counts['commute'] += 1
            elif isinstance(node, ast.BoolOp):
                yield qual, 'bool', counts.setdefault('bool', 0), node, type(node.op).__name__
                counts['bool'] += 1
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
                yield qual, 'not', counts.setdefault('not', 0), node, 'Not'
                counts['not'] += 1
            elif isinstance(node, ast.Constant) and type(node.value) is int:
                yield qual, 'int', counts.setdefault('int', 0), node, str(node.value)
                counts['int'] += 1
            elif isinstance(node, ast.Constant) and type(node.value) is bool:
                yield qual, 'const', counts.setdefault('const', 0), node, str(node.value)
                counts['const'] += 1


def mid_of(qual, kind, k):
    return '%s:%s:%d' % (qual, kind, k)


def enumerate_pool(source):
    tree = ast.parse(source)
    out = []
    for qual, kind, k, node, desc in sites_of(tree):
        out.append(dict(id=mid_of(qual, kind, k), kind=kind, neutral=(kind == 'commute'), line=getattr(node, 'lineno', 0), desc=desc))
    return out


def replace_node(tree, old, new):
    for parent in ast.walk(tree):
        for field, value in ast.iter_fields(parent):
            if value is old:
                setattr(parent, field, new)
                return
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if item is old:
                        value[i] = new
                        return
    raise ValueError('node has no parent')


def apply_mutant(source, mid):
    """Return the mutated module text, or None when the address does not resolve."""
    tree = ast.parse(source)
    for qual, kind, k, node, desc in sites_of(tree):
        if mid_of(qual, kind, k) != mid:
            continue
        if kind == 'cmp':
            node.ops[0] = CMP_SWAP[type(node.ops[0])]()
        elif kind == 'commute':
            node.left, node.comparators[0] = node.comparators[0], node.left
            node.ops[0] = COMMUTE[type(node.ops[0])]()
        elif kind == 'bool':
            node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
        elif kind == 'not':
            replace_node(tree, node, node.operand)
        elif kind == 'int':
            node.value = node.value + 1
        elif kind == 'const':
            node.value = not node.value
        return ast.unparse(tree) + '\n'
    return None


def run_selftest(text):
    with tempfile.TemporaryDirectory(prefix='tameshi-r47-pool-') as d:
        path = os.path.join(d, 'counter.py')
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)
        try:
            p = subprocess.run([sys.executable, path, '--selftest'], capture_output=True, text=True, timeout=TIMEOUT,
                               env=env(), cwd=d)
        except subprocess.TimeoutExpired:
            return 'timeout', ''
    out = p.stdout + p.stderr
    named = any(l.startswith('FAIL ') for l in p.stdout.splitlines())
    if p.returncode == 0 and 'VERDICT: PASS' in p.stdout and not named:
        return 'pass', out[-300:]
    if p.returncode != 0 and named:
        return 'killed', next(l for l in p.stdout.splitlines() if l.startswith('FAIL '))[:200]
    return 'crashed', out[-300:]


def judge(source_text, mid):
    mutated = apply_mutant(source_text, mid)
    if mutated is None:
        return 'inapplicable', ''
    state, tail = run_selftest(mutated)
    return ('survived' if state == 'pass' else state), tail


def stdout_at_data(lane, path_bytes):
    with tempfile.TemporaryDirectory(prefix='tameshi-r47-eq-') as d:
        p = os.path.join(d, 'counter.py')
        with open(p, 'wb') as fh:
            fh.write(path_bytes)
        out = subprocess.run([sys.executable, p, '--lane', lane, '--rev', DATA_REV], capture_output=True, text=True,
                             env=env(), cwd=d)
    return out.returncode, out.stdout


def stdout_equal(a, b):
    """Equal exit code and stdout, and both runs reached a verdict line (two identical failures prove nothing)."""
    return a == b and '_PASS=' in a[1]


def measure(lane, rev, targets, jobs=12):
    me = open(os.path.abspath(__file__), 'rb').read()
    blob = git_show(lane, rev, SELF_PATH)
    self_pin = int(blob is not None and hashlib.sha256(blob).digest() == hashlib.sha256(me).digest())
    raw = git_show(lane, rev, POOL_PATH)
    pool_pin = int(raw is not None and hashlib.sha256(raw).hexdigest() == POOL_SHA256)
    if raw is None:
        print('C2_R47: pool.json absent at rev', file=sys.stderr)
        return 2
    pool = json.loads(raw)
    tot_killed = tot_app = 0
    pristine_ok = neutral_bad = 0
    equiv_ok = 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        for group in sorted(GROUPS):
            path = GROUPS[group]['v2' if targets == 'v2' else 'base']
            src = git_show(lane, rev, path)
            if src is None:
                print('C2_R47: target absent %s' % path, file=sys.stderr)
                return 2
            text = src.decode('utf-8')
            state, tail = run_selftest(ast.unparse(ast.parse(text)) + '\n')
            pr = int(state == 'pass')
            pristine_ok += pr
            muts = pool['groups'][group]
            futs = [(m, ex.submit(judge, text, m['id'])) for m in muts]
            counts = dict(killed=0, survived=0, crashed=0, timeout=0, inapplicable=0)
            nk = n_neut = 0
            for m, f in futs:
                v, tail = f.result()
                if m['neutral']:
                    n_neut += 1
                    nk += v == 'killed'
                    print('NEUTRAL %s/%s %s' % (group, m['id'], v))
                    continue
                counts[v] += 1
                print('MUT %s/%s %s%s' % (group, m['id'], v, (' | ' + tail) if v == 'killed' else ''))
            real = len(muts) - n_neut
            neutral_bad += nk
            tot_killed += counts['killed']
            tot_app += real - counts['inapplicable']
            print('GROUP %s: pool=%d killed=%d survived=%d crashed=%d timeout=%d inapplicable=%d neutral=%d neutral_killed=%d pristine=%d' % (
                group, real, counts['killed'], counts['survived'], counts['crashed'], counts['timeout'],
                counts['inapplicable'], n_neut, nk, pr))
            if targets == 'v2':
                base = git_show(lane, rev, GROUPS[group]['base'])
                eq = int(base is not None and stdout_equal(stdout_at_data(lane, base), stdout_at_data(lane, src)))
                equiv_ok &= eq
                print('EQUIVALENCE %s %d' % (group, eq))
    passed = (self_pin == 1 and pool_pin == 1 and pristine_ok == len(GROUPS) and neutral_bad == 0
              and (targets != 'v2' or equiv_ok == 1) and tot_killed >= TARGET_KILLED)
    print('C2_R47: self_pin=%d pool_pin=%d targets=%s killed=%d applicable=%d neutral_killed=%d pristine=%d equivalence=%s '
          'target=%d rev=%s C2_R47_PASS=%s' % (self_pin, pool_pin, targets, tot_killed, tot_app, neutral_bad, pristine_ok,
                                               equiv_ok if targets == 'v2' else 'na', TARGET_KILLED, rev,
                                               'true' if passed else 'false'))
    return 0 if passed else 1


def selftest():
    cases = []

    def check(name, ok, detail=''):
        cases.append(ok)
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))

    src = ('def f(a, b):\n    if a == b and a < 3:\n        return not b\n    return 5\n\n'
           'def selftest():\n    return a == b\n\ndef extra_x():\n    return 1 == 1\n')
    pool = enumerate_pool(src)
    ids = [m['id'] for m in pool]
    check('P01_enumerates_rule_code_only', all(i.startswith('f:') for i in ids), str(ids))
    check('P02_kinds', {m['kind'] for m in pool} == {'cmp', 'commute', 'bool', 'not', 'int'}, str(sorted({m['kind'] for m in pool})))
    check('P03_cmp_swap', 'a != b' in (apply_mutant(src, 'f:cmp:0') or ''), '')
    check('P04_bool_swap', 'a == b or a < 3' in (apply_mutant(src, 'f:bool:0') or ''), '')
    check('P05_not_deleted', 'return b' in (apply_mutant(src, 'f:not:0') or ''), '')
    check('P06_int_bump', 'return 6' in (apply_mutant(src, 'f:int:0') or ''), '')
    commuted = apply_mutant(src, 'f:commute:0') or ''
    check('P07_commute_preserves_value', 'b == a' in commuted and run_ev(commuted) == run_ev(src), '')
    check('P08_missing_site_inapplicable', apply_mutant(src, 'f:cmp:99') is None, '')
    check('P09_excluded_selftest_never_mutated', apply_mutant(src, 'selftest:cmp:0') is None, '')
    # kill rule: a toy counter whose selftest fails with a named case vs one that only crashes
    toy_ok = ('import sys\ndef rule(x):\n    return x > 2\ndef selftest():\n    ok = rule(3) and not rule(2)\n'
              '    print("PASS r" if ok else "FAIL r")\n    print("VERDICT: PASS" if ok else "VERDICT: FAIL")\n    return 0 if ok else 1\n'
              'if __name__ == "__main__":\n    sys.exit(selftest())\n')
    check('P10_pristine_passes', run_selftest(toy_ok)[0] == 'pass')
    check('P11_named_fail_is_killed', judge(toy_ok, 'rule:cmp:0')[0] == 'killed')
    toy_crash = toy_ok.replace('print("PASS r" if ok else "FAIL r")', 'assert ok')
    check('P12_crash_without_named_case_not_killed', judge(toy_crash, 'rule:cmp:0')[0] == 'crashed')
    toy_weak2 = toy_ok.replace('rule(3) and not rule(2)', 'rule(10)')
    check('P14_survivor_survives', judge(toy_weak2, 'rule:cmp:0')[0] == 'survived', judge(toy_weak2, 'rule:cmp:0')[0])
    # an AST-pin selftest kills the neutral commute mutant: the control the neutral set exists for
    toy_pin = toy_ok.replace('ok = rule(3) and not rule(2)', 'import ast, hashlib\n    ok = hashlib.sha256(ast.dump(ast.parse(open(__file__).read())).encode()).hexdigest() == "x"')
    check('P15_ast_pin_kills_neutral_commute', judge(toy_pin, 'rule:commute:0')[0] in ('killed',), judge(toy_pin, 'rule:commute:0')[0])
    failed = cases.count(False)
    print('C2_R47_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    print('VERDICT: %s' % ('PASS' if failed == 0 else 'FAIL'))
    return 0 if failed == 0 else 1


def run_ev(src):
    ns = {}
    exec(compile(src, '<m>', 'exec'), ns)
    return [ns['f'](a, b) for a in range(5) for b in range(5)]


def build_pool(lane, rev):
    groups = {}
    shas = {}
    for g, paths in GROUPS.items():
        raw = git_show(lane, rev, paths['base'])
        shas[g] = hashlib.sha256(raw).hexdigest()
        groups[g] = enumerate_pool(raw.decode('utf-8'))
    return dict(base_rev=rev, base_sha256=shas, groups=groups)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--targets', choices=('v2', 'base'))
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--enumerate')
    ap.add_argument('--build-pool', action='store_true')
    ap.add_argument('--try', dest='try_file')
    ap.add_argument('--group')
    ap.add_argument('--ids')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.enumerate:
        for m in enumerate_pool(open(a.enumerate, encoding='utf-8').read()):
            print(json.dumps(m))
        return 0
    if a.build_pool:
        print(json.dumps(build_pool(a.lane, a.rev), indent=1, sort_keys=True))
        return 0
    if a.try_file:
        text = open(a.try_file, encoding='utf-8').read()
        pool = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pool.json')))
        want = set(a.ids.split(',')) if a.ids else None
        st, _ = run_selftest(ast.unparse(ast.parse(text)) + '\n')
        print('PRISTINE %s' % st)
        for m in pool['groups'][a.group]:
            if want and m['id'] not in want:
                continue
            v, tail = judge(text, m['id'])
            print('%s %s %s' % ('NEUTRAL' if m['neutral'] else 'MUT', m['id'], v))
        return 0
    if not (a.lane and a.rev and a.targets):
        ap.error('--lane, --rev and --targets are required')
    return measure(a.lane, a.rev, a.targets)


if __name__ == '__main__':
    sys.exit(main())
