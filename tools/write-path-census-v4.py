#!/usr/bin/env python3
"""F4 write-path census v4 — attribute-bound and output-flag destinations.

v3 resolves a destination through the assignments visible before the write.
Two destination shapes stay invisible to it, and both are live in this lane:

* an instance attribute: `self.root = tempfile.mkdtemp(...)` in `__init__`,
  read through a same-class helper `self.case_dir(name)` that returns
  `os.path.join(self.root, ...)` — v3 cannot see `mkdtemp`, so a scratch
  write reads as an unflagged expected-value write;
* an operator-chosen output directory: `p.add_argument('--out')`, then
  `publish(..., Path(args.out))` writing `out / 'expected.json'` — v3 sees a
  bare parameter and cannot tell an explicit destination from a hidden update.

v4 keeps v3's walk and adds three bounded resolution steps:

1. attribute binding — inside a class, every `self.<attr> = <expr>` in any
   method is collected; an attribute with exactly one distinct assigned
   expression resolves to it; two or more distinct expressions (or any
   augmented assignment) leave it unresolved, so it is never read as scratch;
2. method-return fold — `self.<m>(...)` for a same-class method with exactly
   one top-level `return <expr>` resolves to that expression, evaluated in the
   method's own top-level assignments;
3. output-flag trace — argparse options `--out`, `--output`, `--out-dir`,
   `--output-dir` (dest from the first long option, `-` to `_`, or `dest=`).
   A destination is `explicit_out` when its root resolves to `<ns>.<dest>` of
   such an option with `<ns>` bound to a `parse_args(...)` call, or when its
   root is a parameter of a module-level function and EVERY in-module call of
   that function passes, at that position, an expression that does.
   `explicit_out` implies not `unflagged`; the resolved text names the option.

Write forms (unchanged from v3): open(path, 'w'|'a'|...), Path.write_text /
.write_bytes, os.replace / os.rename (both arguments), os.symlink destination.

Scope, stated so it cannot be read as universal: resolution is bounded to a
depth of eight through assignment, `os.path.join`, `+`, `/`, f-strings,
attribute reads and the three steps above, inside one module. Aliases,
closures over reassigned names and attribute reassignment are not reliably
resolved: a name can bind by definition order or keep a stale binding, so a
reader must not treat an unresolved destination as proven safe. Control flow,
containers, indirect calls, calls into other modules and unrecognized
path-producing calls stay out of scope. This is a bounded recognizer, not a
dataflow analyser.

Output: text mode prints v3's line format; `--json` prints one object whose
`sites` list carries every write site with lineno, kind, expected, scratch,
explicit_out, flagged, unflagged and resolved.

Exit codes: 0 pass · 1 selftest fail · 2 usage.
"""
import argparse
import ast
import json
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
OUTPUT_FLAGS = ('--out', '--output', '--out-dir', '--output-dir')
PATH_WRAPPERS = frozenset(('Path', 'pathlib.Path', 'str', 'os.fspath', 'os.path.abspath',
                           'os.path.realpath', 'os.path.expanduser'))
MAX_DEPTH = 8


class Module:
    """Module-wide facts: output-flag dests, module functions, call sites."""

    def __init__(self, tree):
        self.out_dests = {}
        self.funcs = {}
        self.calls = {}
        for stmt in tree.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.funcs[stmt.name] = stmt
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                    and node.func.attr == 'add_argument':
                options = [a.value for a in node.args
                           if isinstance(a, ast.Constant) and isinstance(a.value, str)]
                flag = next((o for o in options if o in OUTPUT_FLAGS), None)
                if flag is None:
                    continue
                dest = None
                for kw in node.keywords:
                    if kw.arg == 'dest' and isinstance(kw.value, ast.Constant):
                        dest = kw.value.value
                if dest is None:
                    longs = [o for o in options if o.startswith('--')]
                    dest = (longs[0] if longs else options[0]).lstrip('-').replace('-', '_')
                self.out_dests[dest] = flag


class Ctx:
    """Where a statement sits: its module, enclosing class, module function."""

    def __init__(self, module, cls=None, func=None):
        self.module = module
        self.cls = cls
        self.func = func


class ClassInfo:
    def __init__(self, node):
        self.methods = {}
        assigned = {}
        for stmt in node.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.methods[stmt.name] = stmt
        for method in self.methods.values():
            for sub in ast.walk(method):
                targets, value = [], None
                if isinstance(sub, ast.Assign):
                    targets, value = sub.targets, sub.value
                elif isinstance(sub, ast.AnnAssign) and sub.value is not None:
                    targets, value = [sub.target], sub.value
                elif isinstance(sub, ast.AugAssign):
                    targets, value = [sub.target], sub
                for target in targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) \
                            and target.value.id == 'self':
                        assigned.setdefault(target.attr, {})[ast.dump(value)] = value
        self.attrs = {attr: list(vals.values())[0] for attr, vals in assigned.items()
                      if len(vals) == 1 and not isinstance(list(vals.values())[0], ast.AugAssign)}

    def method_return(self, name):
        method = self.methods.get(name)
        if method is None:
            return None, None
        returns = [s for s in method.body if isinstance(s, ast.Return) and s.value is not None]
        if len(returns) != 1:
            return None, None
        env = {}
        for stmt in method.body:
            if stmt is returns[0]:
                break
            _bind(stmt, env)
        return returns[0].value, env


def _src(node, text):
    """Source segment of a node, with an unparse fallback."""
    seg = ast.get_source_segment(text, node)
    if seg:
        return seg
    try:
        return ast.unparse(node)
    except Exception:  # pragma: no cover - defensive
        return ''


def _is_self_attr(node):
    return isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
        and node.value.id == 'self'


def _resolve(node, env, text, ctx, depth=0):
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
        sub, sub_trace = _resolve(bound, env, text, ctx, depth + 1)
        return sub, trace + ' ' + sub_trace
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(str(value.value))
            elif isinstance(value, ast.FormattedValue):
                parts.append(_resolve(value.value, env, text, ctx, depth + 1)[0])
        return ''.join(parts), trace
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Div)):
        left, left_trace = _resolve(node.left, env, text, ctx, depth + 1)
        right, right_trace = _resolve(node.right, env, text, ctx, depth + 1)
        return left + right, trace + ' ' + left_trace + ' ' + right_trace
    if isinstance(node, ast.Call):
        if ctx.cls is not None and _is_self_attr(node.func):
            value, method_env = ctx.cls.method_return(node.func.attr)
            if value is not None:
                sub, sub_trace = _resolve(value, method_env, text, ctx, depth + 1)
                return sub, trace + ' ' + sub_trace
        parts = [trace]
        for arg in list(node.args) + [kw.value for kw in node.keywords]:
            sub, sub_trace = _resolve(arg, env, text, ctx, depth + 1)
            parts.append(sub)
            parts.append(sub_trace)
        return ''.join(parts), ' '.join(parts)
    if isinstance(node, ast.Attribute):
        if ctx.cls is not None and _is_self_attr(node) and node.attr in ctx.cls.attrs:
            sub, sub_trace = _resolve(ctx.cls.attrs[node.attr], {}, text, ctx, depth + 1)
            return sub, trace + ' ' + sub_trace
        base, base_trace = _resolve(node.value, env, text, ctx, depth + 1)
        return (base + '/' + node.attr) if base else node.attr, trace + ' ' + base_trace
    if isinstance(node, ast.Subscript):
        base, base_trace = _resolve(node.value, env, text, ctx, depth + 1)
        return base, trace + ' ' + base_trace
    return '', trace


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return (base + '.' + node.attr) if base else node.attr
    return ''


def _param_args(name, ctx, seen):
    """Arguments passed for parameter `name` of the enclosing module function.

    Returns a list of (arg node, caller env, caller ctx), one per in-module
    call, or None when the name is not a parameter, a call omits or star-passes
    it, or the function has no in-module call.
    """
    func = ctx.func
    if func is None or func.name in seen:
        return None
    params = [a.arg for a in func.args.posonlyargs + func.args.args]
    kwonly = [a.arg for a in func.args.kwonlyargs]
    if name not in params and name not in kwonly:
        return None
    sites = ctx.module.calls.get(func.name, [])
    if not sites:
        return None
    out = []
    for call, call_env, call_ctx in sites:
        arg = None
        if name in params and params.index(name) < len(call.args):
            arg = call.args[params.index(name)]
            if isinstance(arg, ast.Starred):
                return None
        for kw in call.keywords:
            if kw.arg == name:
                arg = kw.value
        if arg is None:
            return None
        out.append((arg, call_env, call_ctx))
    return out


def _parse_args_ns(node, env, ctx, depth=0, seen=frozenset()):
    """True when `node` is a namespace returned by `<parser>.parse_args(...)`."""
    if depth > MAX_DEPTH:
        return False
    if isinstance(node, ast.Call):
        return isinstance(node.func, ast.Attribute) and node.func.attr == 'parse_args'
    if not isinstance(node, ast.Name):
        return False
    bound = env.get(node.id)
    if bound is not None:
        return _parse_args_ns(bound, env, ctx, depth + 1, seen)
    sites = _param_args(node.id, ctx, seen)
    if not sites:
        return False
    return all(_parse_args_ns(arg, call_env, call_ctx, depth + 1, seen | {ctx.func.name})
               for arg, call_env, call_ctx in sites)


def _out_flag(node, env, ctx, depth=0, seen=frozenset()):
    """Return the output option string a destination root is bound to, or None."""
    if node is None or depth > MAX_DEPTH:
        return None
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        flag = ctx.module.out_dests.get(node.attr)
        if flag and _parse_args_ns(node.value, env, ctx, depth + 1, seen):
            return flag
        return None
    if isinstance(node, ast.Call):
        dotted = _dotted(node.func)
        if dotted in PATH_WRAPPERS and len(node.args) == 1 and not node.keywords:
            return _out_flag(node.args[0], env, ctx, depth + 1, seen)
        if dotted == 'os.path.join' and node.args:
            return _out_flag(node.args[0], env, ctx, depth + 1, seen)
        return None
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Div)):
        return _out_flag(node.left, env, ctx, depth + 1, seen)
    if isinstance(node, ast.Name):
        if node.id in env:
            return _out_flag(env[node.id], env, ctx, depth + 1, seen)
        sites = _param_args(node.id, ctx, seen)
        if not sites:
            return None
        flags = set()
        for arg, call_env, call_ctx in sites:
            flag = _out_flag(arg, call_env, call_ctx, depth + 1, seen | {ctx.func.name})
            if flag is None:
                return None
            flags.add(flag)
        return ' '.join(sorted(flags))
    return None


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


def _record(node, kind, dests, env, text, flagged, records, ctx):
    resolved_parts = []
    traces = []
    flags = set()
    for dest in dests:
        resolved, trace = _resolve(dest, env, text, ctx)
        resolved_parts.append(resolved)
        traces.append(trace)
        flag = _out_flag(dest, env, ctx)
        if flag:
            flags.add(flag)
    explicit_out = bool(flags) and len(flags) == len(dests)
    if explicit_out:
        resolved_parts.append('argparse ' + ' '.join(sorted(flags)))
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
            'explicit_out': explicit_out,
            'flagged': flagged,
            'unflagged': expected and not scratch and not flagged and not explicit_out,
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


def _walk_stmts(stmts, env, text, flagged, records, ctx, collect):
    """Walk statements; record write sites, or (collect=True) module call sites."""
    for stmt in stmts:
        for node in _calls_in_stmt(stmt):
            if collect:
                if isinstance(node.func, ast.Name) and node.func.id in ctx.module.funcs:
                    ctx.module.calls.setdefault(node.func.id, []).append((node, dict(env), ctx))
                continue
            found = _write_call(node)
            if found is not None:
                _record(node, found[0], found[1], env, text, flagged, records, ctx)
        _bind(stmt, env)
        inner_ctx = ctx
        if isinstance(stmt, ast.ClassDef):
            inner_ctx = Ctx(ctx.module, ClassInfo(stmt), None)
        elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)) and ctx.cls is None \
                and ctx.func is None:
            inner_ctx = Ctx(ctx.module, None, stmt)
        for field in ('body', 'orelse', 'finalbody'):
            inner = getattr(stmt, field, None)
            if isinstance(inner, list) and inner and isinstance(inner[0], ast.stmt):
                _walk_stmts(inner, dict(env), text, flagged, records, inner_ctx, collect)
        for handler in getattr(stmt, 'handlers', None) or []:
            _walk_stmts(handler.body, dict(env), text, flagged, records, inner_ctx, collect)


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
                'explicit_out': False,
                'flagged': flagged,
                'unflagged': False,
            }
        )
        return records
    module = Module(tree)
    _walk_stmts(tree.body, {}, text, flagged, [], Ctx(module), True)
    _walk_stmts(tree.body, {}, text, flagged, records, Ctx(module), False)
    records.sort(key=lambda rec: (rec['lineno'], rec['kind']))
    return records


SELFTEST = {
    # name: (source, expected classification of its single expected-value site)
    'attr_bound_scratch': ('''import os
import tempfile


class Runner:
    def __init__(self):
        self.base = tempfile.mkdtemp(prefix="t-")

    def workdir(self, label):
        where = os.path.join(self.base, label)
        return where

    def go(self):
        golden = os.path.join(self.workdir("x"), "golden.txt")
        with open(golden, "w") as fh:
            fh.write("y")
''', {'scratch': True, 'explicit_out': False, 'unflagged': False}),
    'attr_bound_repo': ('''import os


class Runner:
    def __init__(self):
        self.base = "fixtures"

    def workdir(self, label):
        return os.path.join(self.base, label)

    def go(self):
        with open(os.path.join(self.workdir("x"), "expected.txt"), "w") as fh:
            fh.write("y")
''', {'scratch': False, 'explicit_out': False, 'unflagged': True}),
    'attr_two_assignments': ('''import os
import tempfile


class Runner:
    def __init__(self):
        self.base = tempfile.mkdtemp()

    def reset(self):
        self.base = "fixtures"

    def go(self):
        with open(os.path.join(self.base, "expected.json"), "w") as fh:
            fh.write("y")
''', {'scratch': False, 'explicit_out': False, 'unflagged': True}),
    'method_two_returns': ('''import os
import tempfile


class Runner:
    def __init__(self):
        self.base = tempfile.mkdtemp()

    def pick(self, fast):
        if fast:
            return self.base
        return "fixtures"

    def go(self):
        with open(os.path.join(self.pick(True), "expected.json"), "w") as fh:
            fh.write("y")
''', {'scratch': False, 'explicit_out': False, 'unflagged': True}),
    'output_dir_param': ('''import argparse
import os


def emit(blob, dest_dir):
    with open(os.path.join(dest_dir, "expected.json"), "w") as fh:
        fh.write(blob)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output-dir")
    ns = ap.parse_args()
    emit("{}", ns.output_dir)
''', {'scratch': False, 'explicit_out': True, 'unflagged': False}),
    'output_flag_direct': ('''import argparse
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--output", dest="target")
ns = ap.parse_args()
(Path(ns.target) / "snapshot.json").write_text("{}")
''', {'scratch': False, 'explicit_out': True, 'unflagged': False}),
    'output_namespace_param': ('''import argparse
from pathlib import Path


def run(opts):
    folder = Path(opts.output)
    (folder / "expected.txt").write_bytes(b"")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    run(ap.parse_args())
''', {'scratch': False, 'explicit_out': True, 'unflagged': False}),
    'output_namespace_bound_param': ('''import argparse
from pathlib import Path


def run(opts):
    folder = Path(opts.output)
    (folder / "expected.txt").write_bytes(b"")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    parsed = ap.parse_args()
    run(parsed)
''', {'scratch': False, 'explicit_out': True, 'unflagged': False}),
    'input_flag_param': ('''import argparse
import os


def emit(blob, dest_dir):
    with open(os.path.join(dest_dir, "expected.json"), "w") as fh:
        fh.write(blob)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source")
    ns = ap.parse_args()
    emit("{}", ns.source)
''', {'scratch': False, 'explicit_out': False, 'unflagged': True}),
    'output_param_one_constant_caller': ('''import argparse
import os


def emit(blob, dest_dir):
    with open(os.path.join(dest_dir, "expected.json"), "w") as fh:
        fh.write(blob)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ns = ap.parse_args()
    emit("{}", ns.out)
    emit("{}", "fixtures")
''', {'scratch': False, 'explicit_out': False, 'unflagged': True}),
    'output_attr_not_parse_args': ('''import os

class Cfg:
    out = "fixtures"

cfg = Cfg()
with open(os.path.join(cfg.out, "expected.json"), "w") as fh:
    fh.write("y")
''', {'scratch': False, 'explicit_out': False, 'unflagged': True}),
    'v3_variable_replace': ('''import os

root = os.environ.get("REPO", ".")
dest = os.path.join(root, "fixtures", "expected.json")
os.replace(dest, os.path.join(root, "actual.json"))
''', {'scratch': False, 'explicit_out': False, 'unflagged': True}),
    'v3_symlink': ('''import os

root = "tests/fixtures"
os.symlink(os.path.join(root, "actual.json"), os.path.join(root, "expected.json"))
''', {'scratch': False, 'explicit_out': False, 'unflagged': True}),
    'v3_scratch_var': ('''import os

base = os.path.join("/tmp", "census")
dest = os.path.join(base, "expected.json")
os.replace(dest, os.path.join(base, "actual.json"))
''', {'scratch': True, 'explicit_out': False, 'unflagged': False}),
    'update_flag': ('''import sys

if "--update-goldens" in sys.argv:
    with open("golden/expected.json", "w") as fh:
        fh.write("x")
''', {'scratch': False, 'explicit_out': False, 'unflagged': False}),
}


def selftest():
    failed = []
    for name, (source, want) in sorted(SELFTEST.items()):
        sites = [r for r in classify_source(source) if r['expected']]
        if len(sites) != 1:
            failed.append('%s: expected-value sites=%d, want 1' % (name, len(sites)))
            continue
        for key, value in want.items():
            if sites[0][key] != value:
                failed.append('%s: %s=%s, want %s' % (name, key, sites[0][key], value))
    for item in failed:
        print('FAIL %s' % item)
    print('WRITE_CENSUS_V4_SELFTEST: cases=%d failed=%d' % (len(SELFTEST), len(failed)))
    return 0 if not failed else 1


def main():
    parser = argparse.ArgumentParser(description='F4 write-path census v4')
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--file', default=None, help='source file to classify')
    parser.add_argument('--json', action='store_true', help='print every site as JSON')
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.file:
        with open(args.file, encoding='utf-8', errors='replace') as handle:
            records = classify_source(handle.read())
        if args.json:
            print(json.dumps({'file': args.file, 'sites': records}, sort_keys=True))
            return 0
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
        return 0
    parser.print_usage(sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
