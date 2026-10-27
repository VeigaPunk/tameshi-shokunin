#!/usr/bin/env python3
"""F4 write-path census v3 — destination resolution, not line matching.

v2 reads one line at a time and needs the expected-value token to be a string
literal on that same line. A destination held in a variable is invisible to it:
`dest = os.path.join(root, "expected.json")` followed by `os.replace(dest, x)`
is one write site to v2 and zero expected-value destinations.

v3 parses the source with `ast`, resolves a destination through the
assignments visible before the write, and classifies the resolved text.

Write forms: open(path, 'w'|'a'|...), Path.write_text / .write_bytes,
os.replace / os.rename (both arguments), os.symlink destination.

Scope, stated so it cannot be read as universal: one-hop-ish name resolution
inside a module, function or block, through assignment, `os.path.join`, `+`,
`/` and f-strings, to a depth of four. Aliases, closures over reassigned
names, attribute reassignment, conditional assignment, dictionary and list
elements, and any path computed by a function call that does not fold to a
literal are NOT resolved. This is a bounded recognizer, not a dataflow
analyser.

Exit codes: 0 pass · 1 selftest fail · 2 usage.
"""
import argparse
import ast
import json
import os
import re
import sys

EXPECTED_RE = re.compile(r'expected\.json|expected\.txt|\.expected\b|golden|snapshot')
SCRATCH_MARKERS = (
    '/tmp',
    'tempfile',
    'TemporaryDirectory',
    'NamedTemporaryFile',
    'mkdtemp',
    'scratch',
)
FLAG_RE = re.compile(r'--update_goldens|--update-goldens|--update\b|update_goldens')
WRITE_MODES = frozenset(('w', 'a', 'w+', 'a+', 'wb', 'ab', 'w+b', 'a+b', 'x', 'xb'))
MAX_DEPTH = 4
FIXTURE_REL = '.ufo/evidence/round-41/census/fixtures.json'


def _src(node, text):
    """Source segment of a node, with an unparse fallback."""
    seg = ast.get_source_segment(text, node)
    if seg:
        return seg
    try:
        return ast.unparse(node)
    except Exception:  # pragma: no cover - defensive
        return ''


def _resolve(node, env, text, depth=0):
    """Return (resolved_text, trace).

    `trace` is every source segment consulted while resolving, so a scratch
    marker that lives one assignment upstream stays visible.
    """
    trace = _src(node, text)
    if node is None or depth > MAX_DEPTH:
        return '', trace
    if isinstance(node, ast.Constant):
        return (node.value if isinstance(node.value, str) else ''), trace
    if isinstance(node, ast.Name):
        bound = env.get(node.id)
        if bound is None:
            return '', trace
        sub, sub_trace = _resolve(bound, env, text, depth + 1)
        return sub, trace + ' ' + sub_trace
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(str(value.value))
            elif isinstance(value, ast.FormattedValue):
                parts.append(_resolve(value.value, env, text, depth + 1)[0])
        return ''.join(parts), trace
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Div)):
        left, left_trace = _resolve(node.left, env, text, depth + 1)
        right, right_trace = _resolve(node.right, env, text, depth + 1)
        return left + right, trace + ' ' + left_trace + ' ' + right_trace
    if isinstance(node, ast.Call):
        parts = [trace]
        for arg in list(node.args) + [kw.value for kw in node.keywords]:
            sub, sub_trace = _resolve(arg, env, text, depth + 1)
            parts.append(sub)
            parts.append(sub_trace)
        return ''.join(parts), ' '.join(parts)
    if isinstance(node, ast.Attribute):
        base, base_trace = _resolve(node.value, env, text, depth + 1)
        return (base + '/' + node.attr) if base else node.attr, trace + ' ' + base_trace
    if isinstance(node, ast.Subscript):
        base, base_trace = _resolve(node.value, env, text, depth + 1)
        return base, trace + ' ' + base_trace
    return '', trace


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return (base + '.' + node.attr) if base else node.attr
    return ''


def _write_call(node):
    """Yield (kind, [destination nodes]) for a Call that writes."""
    func = node.func
    dotted = _dotted(func)
    attr = func.attr if isinstance(func, ast.Attribute) else None
    if dotted == 'open' or attr == 'open':
        mode = ''
        if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
            if isinstance(node.args[1].value, str):
                mode = node.args[1].value
        for kw in node.keywords:
            if kw.arg == 'mode' and isinstance(kw.value, ast.Constant):
                if isinstance(kw.value.value, str):
                    mode = kw.value.value
        if mode in WRITE_MODES and node.args:
            return 'open', [node.args[0]]
        return None
    if attr in ('write_text', 'write_bytes'):
        return attr, [func.value]
    if dotted in ('os.replace', 'os.rename'):
        if len(node.args) >= 2:
            return dotted, [node.args[1], node.args[0]]
        return None
    if dotted == 'os.symlink':
        if len(node.args) >= 2:
            return 'os.symlink', [node.args[1]]
        return None
    return None


def _bind(stmt, env):
    if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
        target = stmt.targets[0]
        if isinstance(target, ast.Name):
            env[target.id] = stmt.value
    elif isinstance(stmt, ast.AnnAssign) and stmt.value is not None:
        if isinstance(stmt.target, ast.Name):
            env[stmt.target.id] = stmt.value
    elif isinstance(stmt, ast.With):
        for item in stmt.items:
            if isinstance(item.optional_vars, ast.Name):
                env[item.optional_vars.id] = item.context_expr


def _record(node, kind, dests, env, text, flagged, records):
    resolved_parts = []
    traces = []
    for dest in dests:
        resolved, trace = _resolve(dest, env, text)
        resolved_parts.append(resolved)
        traces.append(trace)
    resolved = ' '.join(part for part in resolved_parts if part)
    trace = ' '.join(traces)
    expected = bool(EXPECTED_RE.search(resolved))
    scratch = any(marker in trace for marker in SCRATCH_MARKERS) or any(
        marker in resolved for marker in SCRATCH_MARKERS
    )
    records.append(
        {
            'lineno': getattr(node, 'lineno', 0),
            'kind': kind,
            'resolved': resolved,
            'expected': expected,
            'scratch': scratch,
            'flagged': flagged,
            'unflagged': expected and not scratch and not flagged,
        }
    )


def _calls_in_stmt(stmt):
    """Calls owned by one statement: expressions yes, nested statements no.

    Nested statements are visited by `_walk_stmts` itself, with their own
    environment; descending into them here would record every call twice.
    """
    calls = []
    stack = [stmt]
    while stack:
        node = stack.pop()
        if node is not stmt and isinstance(node, ast.stmt):
            continue
        if isinstance(node, ast.Call):
            calls.append(node)
        stack.extend(ast.iter_child_nodes(node))
    calls.sort(key=lambda call: getattr(call, 'lineno', 0))
    return calls


def _walk_stmts(stmts, env, text, flagged, records):
    for stmt in stmts:
        for node in _calls_in_stmt(stmt):
            found = _write_call(node)
            if found is not None:
                _record(node, found[0], found[1], env, text, flagged, records)
        _bind(stmt, env)
        for field in ('body', 'orelse', 'finalbody'):
            inner = getattr(stmt, field, None)
            if isinstance(inner, list) and inner and isinstance(inner[0], ast.stmt):
                _walk_stmts(inner, dict(env), text, flagged, records)
        for handler in getattr(stmt, 'handlers', None) or []:
            _walk_stmts(handler.body, dict(env), text, flagged, records)


def classify_source(text):
    """Classify every write call site in `text`. Returns a list of records."""
    flagged = FLAG_RE.search(text) is not None
    records = []
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        records.append(
            {
                'lineno': getattr(exc, 'lineno', 0) or 0,
                'kind': 'parse-error',
                'resolved': '',
                'expected': False,
                'scratch': False,
                'flagged': flagged,
                'unflagged': False,
            }
        )
        return records
    _walk_stmts(tree.body, {}, text, flagged, records)
    records.sort(key=lambda rec: (rec['lineno'], rec['kind']))
    return records


def summarize(records):
    """Aggregate a record list into the counters the fixtures assert."""
    out = {
        'sites': len(records),
        'expected_sites': 0,
        'unflagged': 0,
        'variable_expected': 0,
        'symlink_expected': 0,
        'scratch_expected': 0,
        'parse_errors': 0,
    }
    for rec in records:
        if rec['kind'] == 'parse-error':
            out['parse_errors'] += 1
            continue
        if rec['expected']:
            out['expected_sites'] += 1
            if rec['scratch']:
                out['scratch_expected'] += 1
            if rec['kind'] == 'os.symlink':
                out['symlink_expected'] += 1
            elif rec['kind'] in ('open', 'write_text', 'write_bytes', 'os.replace', 'os.rename'):
                out['variable_expected'] += 1
        if rec['unflagged']:
            out['unflagged'] += 1
    return out


EXPECT = {
    'var_unflagged': {'unflagged': 1, 'expected_sites': 1},
    'symlink_unflagged': {'unflagged': 1, 'expected_sites': 1},
    'literal_unflagged': {'unflagged': 1, 'expected_sites': 1},
    'scratch_var': {'unflagged': 0, 'expected_sites': 1},
}


def selftest(fixture_path):
    with open(fixture_path, encoding='utf-8') as handle:
        planted = json.load(handle)
    failed = []
    summary = {}
    for name, want in EXPECT.items():
        body = planted.get(name)
        if not isinstance(body, str):
            failed.append('missing fixture %s' % name)
            summary[name] = {'unflagged': -1, 'expected_sites': -1}
            continue
        got = summarize(classify_source(body))
        summary[name] = got
        for key, value in want.items():
            if got[key] != value:
                failed.append(
                    'planted %s: want %s=%d got %d' % (name, key, value, got[key])
                )
    print(
        'WRITE_CENSUS_V3_SELFTEST: var_unflagged=%d symlink_unflagged=%d '
        'literal_unflagged=%d scratch_var=%d'
        % (
            summary.get('var_unflagged', {}).get('unflagged', -1),
            summary.get('symlink_unflagged', {}).get('unflagged', -1),
            summary.get('literal_unflagged', {}).get('unflagged', -1),
            summary.get('scratch_var', {}).get('unflagged', -1),
        )
    )
    for item in failed:
        print('FAIL %s' % item)
    return 0 if not failed else 1


def main():
    parser = argparse.ArgumentParser(description='F4 write-path census v3')
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--fixtures', default=None, help='fixture JSON path')
    parser.add_argument('--file', default=None, help='source file to classify')
    args = parser.parse_args()
    if args.selftest:
        path = args.fixtures
        if path is None:
            here = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(os.path.dirname(here), FIXTURE_REL)
        return selftest(path)
    if args.file:
        with open(args.file, encoding='utf-8', errors='replace') as handle:
            records = classify_source(handle.read())
        totals = summarize(records)
        for rec in records:
            if rec['expected']:
                print(
                    '%s:%d %s expected=%d scratch=%d unflagged=%d %s'
                    % (
                        args.file,
                        rec['lineno'],
                        rec['kind'],
                        int(rec['expected']),
                        int(rec['scratch']),
                        int(rec['unflagged']),
                        rec['resolved'][:80],
                    )
                )
        print(' '.join('%s=%d' % (k, v) for k, v in sorted(totals.items())))
        return 0
    parser.print_usage(sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
