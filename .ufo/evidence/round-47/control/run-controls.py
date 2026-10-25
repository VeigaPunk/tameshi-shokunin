#!/usr/bin/env python3
"""Round-47 do-nothing / cheapest-cheat controls, scored by the FROZEN counters on scratch clones.

Run from anywhere: LANE is the lane repo two levels above .ufo; every fixture is a `git clone` of the
lane into a mktemp dir (so the round-45 data revision exists there), every git call names -C, the
toplevel is verified before the first commit, and nothing is committed in the lane.

  CTL_A  C3 package entries copied byte-exact (rows with lane snapshots added)           -> entries=0
  CTL_B  C3 relabel: package entries with only the header rewritten                       -> entries=0
  CTL_C  C3 rows only, no entries                                                         -> entries=0
  CTL_D  C3 rows with a wrong snapshot digest and relabelled entries                      -> rows=0
  CTL_E  C2 selftest that pins the AST of its own rule code (kills every real mutant AND
         the AST-different, behaviour-equal neutral mutants)                              -> neutral_killed>0, PASS false
  CTL_F  C2 selftest that always fails                                                    -> pristine<2, PASS false
  CTL_G  C2 round-46 hardened counters unchanged (the do-nothing baseline)                -> killed<TARGET, PASS false
  CTL_H  C2 selftest that pins the AST with a bare assert (kills by crash, no FAIL line)  -> killed small, PASS false
Each control prints the counter's final line.
"""
import ast
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
E = '.ufo/evidence/round-47'
C3 = E + '/coverage/measure.py'
C2 = E + '/hardening/pool.py'
POOL = E + '/hardening/pool.json'
SNAP = E + '/coverage/sources/'
PKG = E + '/assimilation/package/'
BASE_F = '.ufo/evidence/round-46/hardening/freshness-counter.py'
BASE_C = '.ufo/evidence/round-46/hardening/coverage-counter.py'
V2_F = E + '/hardening/freshness-counter.py'
V2_C = E + '/hardening/coverage-counter.py'
DOCS = [
    ('S261', 'arxiv-2302.09330-abs.html', 'https://arxiv.org/abs/2302.09330', 'flaky-aware-verdict-evidence.md'),
    ('S263', 'arxiv-2607.09345-abs.html', 'https://arxiv.org/abs/2607.09345', 'r8-flakiness-not-static.md'),
    ('S264', 's2-icst24-cost-of-flaky.json',
     'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICST60714.2024.00037?fields=title%2Cabstract%2Cyear%2Cvenue%2Cauthors%2CexternalIds',
     'r8-flaky-cost-baseline.md'),
]


def git(d, *a):
    return subprocess.run(['git', '-C', d, *a], env=ENV, capture_output=True, check=True)


def scratch():
    d = tempfile.mkdtemp(prefix='tameshi-r47-ctl-')
    subprocess.run(['git', 'clone', '-q', '--no-hardlinks', LANE, d], env=ENV, capture_output=True, check=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], env=ENV, capture_output=True).stdout.decode().strip()
    assert top == os.path.realpath(d), (top, d)
    return d


def copy(d, rel, data=None):
    dst = os.path.join(d, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if data is None:
        shutil.copyfile(os.path.join(LANE, rel), dst)
    else:
        with open(dst, 'wb') as fh:
            fh.write(data if isinstance(data, bytes) else data.encode())


def commit(d):
    git(d, 'add', '-A')
    git(d, '-c', 'user.name=ctl', '-c', 'user.email=ctl@ctl', 'commit', '-qm', 'ctl')


def last(cmd):
    out = subprocess.run(cmd, env=ENV, capture_output=True, text=True)
    lines = [l for l in out.stdout.strip().splitlines() if l]
    return (lines[-1] if lines else 'NO-OUTPUT ' + out.stderr[-200:]), out.returncode


def c3_repo(entries, wrong_digest=False, rows=True):
    d = scratch()
    copy(d, C3)
    reg = open(os.path.join(d, 'corpus/SOURCES.md')).read() if os.path.exists(os.path.join(d, 'corpus/SOURCES.md')) else ''
    reg = ''
    for sid, snap, url, pkg in DOCS:
        copy(d, SNAP + snap)
        copy(d, PKG + pkg)
        digest = hashlib.sha256(open(os.path.join(LANE, SNAP + snap), 'rb').read()).hexdigest()[:8]
        if wrong_digest:
            digest = 'deadbeef'
        used = 'corpus/knowledge/%s' % pkg
        reg += ('| %s | t — %s | paper | A | s | %s%s %s | t | mined | 2026-10-25 | 365d | %s |\n'
                % (sid, url, SNAP, snap, digest, used))
    copy(d, 'corpus/SOURCES.md', reg if rows else '')
    readme = ''
    for sid, snap, url, pkg in DOCS:
        text = entries(sid, pkg)
        if text is not None:
            copy(d, 'corpus/knowledge/%s' % pkg, text)
            readme += '`corpus/knowledge/%s`\n' % pkg
    copy(d, 'corpus/README.md', readme)
    commit(d)
    return d


def package_text(pkg):
    return open(os.path.join(LANE, PKG + pkg), encoding='utf-8').read()


def relabel(sid, pkg):
    body = package_text(pkg).lstrip('\n').split('\n')
    head = ['source: %s — relabelled package entry' % sid, 'verified-at: 2026-10-25', 'recheck: 365d']
    return '\n'.join(head + body[3:]) + '\n'


def run_c3(name, d):
    line, rc = last([sys.executable, os.path.join(d, C3), '--lane', d, '--rev', 'HEAD'])
    print('%s rc=%d %s' % (name, rc, line))


def run_c2(name, d):
    line, rc = last([sys.executable, os.path.join(d, C2), '--lane', d, '--rev', 'HEAD', '--targets', 'v2'])
    print('%s rc=%d %s' % (name, rc, line))


def c2_repo(fresh_src, cover_src):
    d = scratch()
    copy(d, C2)
    copy(d, POOL)
    copy(d, V2_F, fresh_src)
    copy(d, V2_C, cover_src)
    commit(d)
    return d


def rule_hash(src):
    """sha256 of the AST dump of the rule functions (everything except selftest/main/extra_*/_x*)."""
    tree = ast.parse(src)
    keep = [n for n in tree.body if not (isinstance(n, ast.FunctionDef) and (n.name in ('selftest', 'main') or n.name.startswith('extra_') or n.name.startswith('_x')))]
    return hashlib.sha256(ast.dump(ast.Module(body=keep, type_ignores=[])).encode()).hexdigest()


PIN_BODY = '''
def _xPin_check():
    import ast as _a, hashlib as _h
    tree = _a.parse(open(__file__, encoding='utf-8').read())
    keep = [n for n in tree.body if not (isinstance(n, _a.FunctionDef) and (n.name in ('selftest', 'main') or n.name.startswith('extra_') or n.name.startswith('_x')))]
    return _h.sha256(_a.dump(_a.Module(body=keep, type_ignores=[])).encode()).hexdigest() == '{HASH}'
'''


def pin_variant(src, named):
    """Add a pin of the rule code's AST to the selftest; `named` prints a FAIL line, else a bare assert."""
    canon = ast.unparse(ast.parse(src)) + '\n'
    h = rule_hash(canon)
    body = PIN_BODY.replace('{HASH}', h)
    if named:
        hook = "    if not _xPin_check():\n        print('FAIL PIN_ast_of_rule_code')\n        print('VERDICT: FAIL')\n        return 1\n"
    else:
        hook = "    assert _xPin_check()\n"
    return (canon.replace('\ndef main():\n', body + '\n\ndef main():\n', 1)
            .replace('def selftest():\n', 'def selftest():\n' + hook, 1))


def always_fail(src):
    return src.replace('def selftest():\n', "def selftest():\n    print('FAIL ALWAYS')\n    print('VERDICT: FAIL')\n    return 1\n", 1)


def main():
    run_c3('CTL_A_package_byte_exact', c3_repo(lambda sid, pkg: package_text(pkg)))
    run_c3('CTL_B_relabel_header_only', c3_repo(relabel))
    run_c3('CTL_C_rows_only', c3_repo(lambda sid, pkg: None))
    run_c3('CTL_D_wrong_digest', c3_repo(relabel, wrong_digest=True))
    fresh = open(os.path.join(LANE, BASE_F), encoding='utf-8').read()
    cover = open(os.path.join(LANE, BASE_C), encoding='utf-8').read()
    base_f = fresh.replace('.ufo/evidence/round-46/hardening/freshness-counter.py', V2_F)
    base_c = cover.replace('.ufo/evidence/round-46/hardening/coverage-counter.py', V2_C)
    run_c2('CTL_E_selftest_pins_rule_ast', c2_repo(pin_variant(base_f, True), pin_variant(base_c, True)))
    run_c2('CTL_F_selftest_always_fails', c2_repo(always_fail(base_f), always_fail(base_c)))
    run_c2('CTL_G_round46_hardened_unchanged', c2_repo(base_f, base_c))
    run_c2('CTL_H_ast_pin_by_bare_assert', c2_repo(pin_variant(base_f, False), pin_variant(base_c, False)))


if __name__ == '__main__':
    main()
