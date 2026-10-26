#!/usr/bin/env python3
"""Round-47 addition lint: close the in-band cheat of the C2 target (T47CritC2Control (a), (d) residual).

The frozen C2 counter (`hardening/pool.py`) cannot tell a selftest addition that tests the rules from one that
embeds the pristine source as a free oracle: `extra_*` and `_x*` code is exempt from the pool by design, so a
differential oracle scored 160 of 183 with neutral_killed=0 in a scratch clone. The deciding run therefore also
requires every seat addition file to pass this lint (landing rule, disclosed beside the claim; it never changes
the frozen counter, predicate, pool or target).

  addition-lint.py --base COUNTER.py ADDITION.py [ADDITION.py ...]   exit 0 clean, 1 on any finding, 64 usage
  addition-lint.py --selftest

Findings (one line each: `LINT <rule> <file>:<line> <detail>`):
  EXEC     a call to the builtins exec, eval or compile
  IMPORT   an import of zlib, base64, marshal, pickle, gzip, bz2, lzma, binascii (a packed payload)
  BLOB     a str/bytes constant longer than 3000 characters that is not a docstring (an embedded source or a packed payload)
  COPY     a function whose body AST is at least 0.90 similar (difflib ratio of ast.dump) to a rule function of
           --base that has at least 6 statements: a verbatim or lightly renamed copy of rule code is an oracle
"""
import argparse
import ast
import difflib
import os
import sys
import tempfile

BAN_CALLS = {'exec', 'eval', 'compile'}
BAN_IMPORTS = {'zlib', 'base64', 'marshal', 'pickle', 'gzip', 'bz2', 'lzma', 'binascii'}
BLOB = 3000
COPY_RATIO = 0.90
MIN_STMTS = 6
EXCLUDE = ('selftest', 'main')


def rule_functions(base_src):
    tree = ast.parse(base_src)
    out = {}
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name not in EXCLUDE and not n.name.startswith(('extra_', '_x')):
            if len(n.body) >= MIN_STMTS:
                out[n.name] = ast.dump(ast.Module(body=n.body, type_ignores=[]))
    return out


def lint(base_src, path, src):
    findings = []
    rules = rule_functions(base_src)
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return ['LINT SYNTAX %s:%s %s' % (path, exc.lineno, exc.msg)]
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) \
                and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
            docstrings.add(id(node.body[0].value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in BAN_CALLS:
            findings.append('LINT EXEC %s:%d call to %s' % (path, node.lineno, node.func.id))
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split('.')[0] in BAN_IMPORTS:
                    findings.append('LINT IMPORT %s:%d import %s' % (path, node.lineno, a.name))
        elif isinstance(node, ast.ImportFrom) and (node.module or '').split('.')[0] in BAN_IMPORTS:
            findings.append('LINT IMPORT %s:%d from %s' % (path, node.lineno, node.module))
        elif isinstance(node, ast.Constant) and isinstance(node.value, (str, bytes)) and len(node.value) > BLOB and id(node) not in docstrings:
            findings.append('LINT BLOB %s:%d constant of %d characters' % (path, node.lineno, len(node.value)))
        elif isinstance(node, ast.FunctionDef) and len(node.body) >= MIN_STMTS:
            dump = ast.dump(ast.Module(body=node.body, type_ignores=[]))
            for name, rule in rules.items():
                if difflib.SequenceMatcher(None, dump, rule, autojunk=False).ratio() >= COPY_RATIO:
                    findings.append('LINT COPY %s:%d function %s is >= %.2f similar to rule function %s' % (
                        path, node.lineno, node.name, COPY_RATIO, name))
    return findings


def selftest():
    base = ('def rule(a, b, c):\n    x = a + 1\n    y = b + 2\n    z = x * y\n    if z > 10:\n        z = z - 1\n    w = [z, a, b]\n'
            '    return sorted(w)[0] if c else max(w)\n\ndef selftest():\n    return 0\n')
    clean = 'def extra_X():\n    print("PASS a")\n    return 1, 0\n'
    exec_bad = 'def extra_X():\n    exec("x = 1")\n    return 1, 0\n'
    zl = 'import zlib\n\ndef extra_X():\n    return 1, 0\n'
    blob = 'B = "%s"\n\ndef extra_X():\n    return 1, 0\n' % ('a' * 3100)
    copy = ('def _xX_rule(a, b, c):\n    x = a + 1\n    y = b + 2\n    z = x * y\n    if z > 10:\n        z = z - 1\n    w = [z, a, b]\n'
            '    return sorted(w)[0] if c else max(w)\n\ndef extra_X():\n    return 1, 0\n')
    renamed = copy.replace('x =', 'p =').replace('x *', 'p *').replace('_xX_rule', '_xX_other')
    doc = '"""%s"""\n\ndef extra_X():\n    return 1, 0\n' % ('d' * 3100)
    cases = [('L07_long_module_docstring_passes', doc, 0), ('L01_clean_passes', clean, 0), ('L02_exec_flagged', exec_bad, 1), ('L03_zlib_flagged', zl, 1),
             ('L04_blob_flagged', blob, 1), ('L05_verbatim_copy_flagged', copy, 1), ('L06_renamed_local_copy_flagged', renamed, 1)]
    failed = 0
    for name, src, want in cases:
        got = 1 if lint(base, name + '.py', src) else 0
        ok = got == want
        failed += not ok
        print('%s %s want=%d got=%d' % ('PASS' if ok else 'FAIL', name, want, got))
    print('ADDITION_LINT_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('files', nargs='*')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.base or not a.files:
        ap.error('--base and at least one addition file are required')
    base = open(a.base, encoding='utf-8').read()
    findings = []
    for f in a.files:
        findings += lint(base, f, open(f, encoding='utf-8').read())
    for line in findings:
        print(line)
    print('ADDITION_LINT: files=%d findings=%d' % (len(a.files), len(findings)))
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
