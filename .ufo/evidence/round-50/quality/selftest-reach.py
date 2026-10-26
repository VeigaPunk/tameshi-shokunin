#!/usr/bin/env python3
"""QUALITY criterion 101 check: does a claim counter's selftest reach its deciding function?

Usage: selftest-reach.py COUNTER.py [COUNTER.py ...]
For each file, parse the module (ast), find the top-level `selftest` function and report whether its body
(including nested functions) calls `measure` by name. Prints `REACH <file> selftest=<0|1> calls_measure=<n> <ok|FAIL>`
per file and `SELFTEST_REACH: files=<n> failed=<m>`; exit 0 when every file reaches measure(), 1 otherwise,
2 when a file cannot be read or parsed.
"""
import ast
import sys


def reach(path):
    tree = ast.parse(open(path, encoding='utf-8').read(), filename=path)
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'selftest'), None)
    if fn is None:
        return 0, 0
    calls = sum(1 for n in ast.walk(fn) if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Name) and n.func.id == 'measure')
    return 1, calls


def main(argv):
    if not argv:
        print(__doc__.strip().split('\n')[2], file=sys.stderr)
        return 2
    failed = 0
    for path in argv:
        try:
            has, calls = reach(path)
        except (OSError, SyntaxError, UnicodeDecodeError) as exc:
            print('REACH %s error=%s' % (path, exc), file=sys.stderr)
            return 2
        ok = has and calls > 0
        failed += 0 if ok else 1
        print('REACH %s selftest=%d calls_measure=%d %s' % (path, has, calls, 'ok' if ok else 'FAIL'))
    print('SELFTEST_REACH: files=%d failed=%d' % (len(argv), failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
