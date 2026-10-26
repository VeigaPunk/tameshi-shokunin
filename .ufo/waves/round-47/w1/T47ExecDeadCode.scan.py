#!/usr/bin/env python3
"""Dead-code debt scanner for the tameshi lane (round 47, idea 3 of considerthese/2026-10-25.md).

Read-only, stdlib-only (``ast``).  Lists three classes of unreachable or
unreferenced code in every ``*.py`` under the given roots (default: ``tools``
and the round-44..round-47 evidence trees):

  after-terminator  statements following an unconditional
                    ``return`` / ``raise`` / ``continue`` / ``break`` in the
                    same block (module, function, class, if/else, loop, with,
                    try body/handler/else/finally, match case).
  constant-test     branches guarded by a falsy constant test: ``if False``,
                    ``if 0``, ``while False`` (``not True`` included).
  unreferenced      function/method definitions never referenced anywhere in
                    the same file (Name loads, attribute names, or a
                    word-boundary mention inside a non-docstring string
                    constant) and never imported by another scanned file.
                    Dunder methods are skipped: the interpreter references
                    them, not a name.

The scanner errs toward under-reporting, never toward inventing dead code: a
name string counts as a reference, so CLI argv dispatch and selftest helpers
are not listed; an explicit ``from mod import name`` counts as a reference; an
``import mod`` of a scanned file marks that module's top-level functions live.

Exit code: 0 when the scanned tree is clean, 1 when any finding exists, 2 on a
missing root.  This makes it usable as a gate, but it is *not* a verdict
instrument -- it is a debt list.

Usage:
  python3 T47ExecDeadCode.scan.py                     # default roots, table
  python3 T47ExecDeadCode.scan.py ROOT [ROOT ...]
  python3 T47ExecDeadCode.scan.py --class after-terminator,constant-test
  python3 T47ExecDeadCode.scan.py --json
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

DEFAULT_ROOTS = ('tools', '.ufo/evidence/round-44', '.ufo/evidence/round-45',
                 '.ufo/evidence/round-46', '.ufo/evidence/round-47')

CLASSES = ('after-terminator', 'constant-test', 'unreferenced')
TERMINATORS = (ast.Return, ast.Raise, ast.Continue, ast.Break)
FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)
IDENT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')


def blocks(node):
    """Yield every statement list owned by ``node`` that executes in order.

    ``ExceptHandler.body`` and ``match_case.body`` are reached through their
    generic ``body`` field, so handler/case bodies are not yielded twice.
    """
    for field in ('body', 'orelse', 'finalbody'):
        block = getattr(node, field, None)
        if isinstance(block, list) and block and isinstance(block[0], ast.stmt):
            yield field, block


def excerpt(lines, lineno, limit=110):
    if not 1 <= lineno <= len(lines):
        return ''
    text = lines[lineno - 1].strip()
    return text[:limit] + ('...' if len(text) > limit else '')


def constant_falsy(test):
    """True for a test the compiler folds to a never-taken branch."""
    if isinstance(test, ast.Constant):
        if test.value is False:
            return True
        return (isinstance(test.value, (int, float))
                and not isinstance(test.value, bool) and test.value == 0)
    if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
        inner = test.operand
        return isinstance(inner, ast.Constant) and (
            inner.value is True or (isinstance(inner.value, int)
                                    and not isinstance(inner.value, bool)
                                    and inner.value == 1))
    return False


def docstring_nodes(tree):
    """Constant nodes that are docstrings: prose, not a dispatch name table."""
    nodes = set()
    for node in ast.walk(tree):
        body = getattr(node, 'body', None)
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                 ast.AsyncFunctionDef)):
            continue
        if body and isinstance(body[0], ast.Expr) \
                and isinstance(body[0].value, ast.Constant) \
                and isinstance(body[0].value.value, str):
            nodes.add(id(body[0].value))
    return nodes


def referenced_names(tree):
    """Names a file refers to: loads, attribute names, non-docstring strings."""
    names = set()
    prose = docstring_nodes(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and id(node) not in prose:
            names.update(IDENT.findall(node.value))
    return names


def defs(tree):
    """Yield (node, parents, kind): function | method | nested-function."""
    stack = []

    def walk(node):
        for child in ast.iter_child_nodes(node):
            kind = None
            if isinstance(child, FUNCTION_TYPES):
                if any(isinstance(p, FUNCTION_TYPES) for p in stack):
                    kind = 'nested-function'
                elif any(isinstance(p, ast.ClassDef) for p in stack):
                    kind = 'method'
                else:
                    kind = 'function'
            stack.append(node)
            if kind:
                yield child, tuple(stack), kind
            yield from walk(child)
            stack.pop()

    yield from walk(tree)


def qualified(node, parents):
    parts = [p.name for p in parents
             if isinstance(p, (ast.FunctionDef, ast.AsyncFunctionDef,
                               ast.ClassDef))]
    return '.'.join(parts + [node.name])


def module_stem(path):
    return path.stem.replace('-', '_')


def scan_file(path, rel, imported, wanted):
    try:
        source = path.read_text(encoding='utf-8')
        tree = ast.parse(source, filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError) as exc:
        return [], {'file': rel, 'error': '%s: %s' % (type(exc).__name__, exc)}

    lines = source.splitlines()
    findings = []

    def add(lineno, cls, text, name=None):
        if cls in wanted:
            findings.append({'file': rel, 'line': lineno, 'class': cls,
                             'excerpt': text, 'name': name})

    for node in ast.walk(tree):
        for _field, block in blocks(node):
            for index, stmt in enumerate(block):
                if not isinstance(stmt, TERMINATORS):
                    continue
                for dead in block[index + 1:]:
                    add(dead.lineno, 'after-terminator',
                        '%s  # unreachable after %s at line %d'
                        % (excerpt(lines, dead.lineno),
                           type(stmt).__name__.lower(), stmt.lineno))
                break
        if isinstance(node, (ast.If, ast.While)) and constant_falsy(node.test):
            add(node.lineno, 'constant-test',
                '%s  # %s guarded by a constant-false test'
                % (excerpt(lines, node.lineno),
                   'if' if isinstance(node, ast.If) else 'while'))

    if 'unreferenced' not in wanted:
        return findings, None

    referenced = referenced_names(tree)
    for node, parents, kind in defs(tree):
        name = node.name
        if name.startswith('__') and name.endswith('__'):
            continue
        if name in referenced:
            continue
        key = qualified(node, parents)
        if name in imported or key in imported:
            continue
        if kind == 'function' and ('%s.%s' % (module_stem(path), name)
                                   in imported):
            continue
        add(node.lineno, 'unreferenced',
            '%s  # %s never referenced in-file, never imported'
            % (excerpt(lines, node.lineno), kind), name=key)

    return findings, None


def collect_imports(modules):
    """Cross-file references: explicit from-imports and whole-module imports."""
    stems = {module_stem(Path(module)) for module in modules}
    imported = set()
    for module, tree in modules.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                target = (node.module or '').split('.')[-1].replace('-', '_')
                if not target and node.level:
                    target = module_stem(Path(module))
                if target not in stems:
                    continue
                for alias in node.names:
                    if alias.name != '*':
                        imported.add(alias.name)
                        imported.add('%s.%s' % (target, alias.name))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    stem = alias.name.split('.')[-1].replace('-', '_')
                    if stem in stems:
                        imported.add(stem)
    return imported


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Dead-code debt list (ast-only) for tools/ and evidence roots.')
    parser.add_argument('roots', nargs='*', default=None,
                        help='roots to scan (default: tools + round-44..47 evidence)')
    parser.add_argument('--class', dest='classes', default=','.join(CLASSES),
                        help='comma-separated subset of %s' % ','.join(CLASSES))
    parser.add_argument('--json', action='store_true', help='machine-readable output')
    parser.add_argument('--base', default=None,
                        help='directory that printed paths are relative to')
    args = parser.parse_args(argv)

    wanted = [c.strip() for c in args.classes.split(',') if c.strip()]
    unknown = [c for c in wanted if c not in CLASSES]
    if unknown:
        parser.error('unknown class(es): %s' % ', '.join(unknown))

    roots = [Path(r).resolve() for r in (args.roots or DEFAULT_ROOTS)]
    missing = [str(r) for r in roots if not r.is_dir()]
    if missing:
        print('missing root(s): %s' % ', '.join(missing), file=sys.stderr)
        return 2

    files = sorted({p.resolve() for root in roots
                    for p in root.rglob('*.py')
                    if '__pycache__' not in p.parts and p.is_file()})
    if not files:
        print('no python files under: %s' % ', '.join(str(r) for r in roots),
              file=sys.stderr)
        return 0

    base = Path(args.base).resolve() if args.base else Path.cwd().resolve()

    def display(path):
        return str(path.relative_to(base)) if path.is_relative_to(base) else str(path)

    parsed, parse_errors, findings = {}, [], []
    for path in files:
        try:
            parsed[path] = ast.parse(path.read_text(encoding='utf-8'),
                                     filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            parse_errors.append({'file': display(path),
                                 'error': '%s: %s' % (type(exc).__name__, exc)})

    imported = collect_imports({display(path): tree for path, tree in parsed.items()})
    for path in files:
        found, error = scan_file(path, display(path), imported, wanted)
        findings.extend(found)
        if error:
            parse_errors.append(error)

    findings.sort(key=lambda f: (CLASSES.index(f['class']), f['file'], f['line']))
    counts = {cls: sum(1 for f in findings if f['class'] == cls) for cls in wanted}

    if args.json:
        print(json.dumps({'files': len(files), 'counts': counts,
                          'findings': findings, 'parse_errors': parse_errors},
                         indent=2, sort_keys=True))
        return 1 if findings else 0

    width = max((len(f['file']) for f in findings), default=4)
    for cls in wanted:
        rows = [f for f in findings if f['class'] == cls]
        print('[%s] %d finding(s)' % (cls, len(rows)))
        for f in rows:
            print('  %-*s:%-5d %s' % (width, f['file'], f['line'], f['excerpt']))
        print()
    print('scanned_files=%d findings=%d %s parse_errors=%d'
          % (len(files), len(findings),
             ' '.join('%s=%d' % (c, counts[c]) for c in wanted),
             len(parse_errors)))
    for err in parse_errors:
        print('PARSE-ERROR %s: %s' % (err['file'], err['error']))
    print('caveats: non-docstring name strings and explicit imports count as '
          'references, so CLI argv dispatch and selftest helpers are not '
          'reported; a whole-module import of a scanned file keeps its '
          'top-level functions live.')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
