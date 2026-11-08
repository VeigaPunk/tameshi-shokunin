#!/usr/bin/env python3
"""control-assertion-audit-v2 — the round-98 audit plus recorder-alias sites (round 99).

Round 98's audit (`tools/control-assertion-audit.py`, frozen and unchanged) counts
only bare-name `add(...)` calls as sites, so a driver that registers its states
through a renamed recorder (`rec = add; rec("x", 0, ...)`) is zero-site for those
states and passes vacuously (round-98 declared limit; SCORECARD round-98 Planned).
v2 keeps v1's classification rules byte-for-byte and widens the SITE set only:

  recorder    `add`, plus every name bound anywhere in the module by a plain
              assignment `name = <recorder>` (fixpoint over chains `r2 = r1 = add`).
  ambiguous   a recorder alias that has any other binding anywhere in the module
              (another assignment, a def, an argument, a loop/with/except target,
              an import, an augmented assignment): its call sites are counted and
              graded `unresolved` / `ambiguous-recorder`.
  partial     a name bound by `partial(<recorder>, ...)` or
              `functools.partial(<recorder>, ...)`: its call sites are counted and
              graded `unresolved` / `partial-recorder` (argument positions shift).

Not sites (declared limits): attribute calls (`c.add(...)`, `self.rec(...)`),
`getattr`/`globals()`/dict dispatch, wrappers that forward to `add` inside a def or
lambda body, and a recorder passed as an argument and called under another name.

v2 prints one extra line, `CONTROL_ASSERT_RECORDERS aliases=<n> ambiguous=<n>
partial=<n> names=<comma list>`, before the unchanged summary line.

--- v1 docstring (unchanged rules) ---
control-assertion-audit — static, scope-aware provenance audit of a control driver.

Round 97's pre-freeze driver registered one state whose graded code was the
literal 0 (`add("c2-nowork-absent", 0, ...)`), so that control could not fail
whatever the `git grep` it wrapped returned (round-97 spot-check D-2). This
tool classifies every `add(...)` call site in a driver by where its recorded
code expression comes from:

  measured    the expression derives from a runner call (`sh`, `git`, `run`,
              `subprocess.run`): `p.returncode`, or the first element of
              `code, out = run(...)`; a name chain is followed through the
              call's own scope chain (function locals, enclosing functions,
              module) to the last assignment before the call.
  literal     a constant, directly or bound through a name.
  unresolved  any other expression (a non-runner `.returncode`, a plain call,
              arithmetic, a loop variable, a name with no prior assignment).

A driver is conforming only when every site is `measured`; an expectation
(`want_code`) is data and is not classified.

Usage:
  python3 -I tools/control-assertion-audit-v2.py --repo LANE --rev <40 hex> \
      [--driver PATH] [--selftest]

The driver is read as a blob at --rev through `git cat-file`, never from the
worktree, so a worktree-only edit cannot change the audit.

Exit: 0 every site measured; 1 an unmeasured site (named); 2 setup (bad rev,
driver absent, unparsable, an `add` call without a classifiable code argument);
64 usage.
"""
import argparse
import ast
import hashlib
import os
import re
import subprocess
import sys

GIT = "/usr/bin/git"
DRIVER = ".ufo/evidence/round-98/controls98.py"
RUNNERS = {"run", "sh", "git", "subprocess.run"}


def sealed_env():
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def call_name(node):
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
        return f.value.id + "." + f.attr
    return None


def is_runner_call(node):
    return isinstance(node, ast.Call) and call_name(node) in RUNNERS


class Scope:
    __slots__ = ("idx", "parent")

    def __init__(self, idx, parent):
        self.idx = idx
        self.parent = parent


def collect_scopes(tree):
    """Returns (assigns, scopes_of, call_scope, scope_nodes).

    assigns: (scope_idx, name) -> [(lineno, kind, payload)]
    scopes_of: id(node) -> Scope for every node, so a call site knows its scope
    """
    assigns = {}
    scopes_of = {}
    counter = [0]

    def new_scope(parent):
        counter[0] += 1
        return Scope(counter[0], parent)

    def record(scope, name, lineno, kind, payload):
        assigns.setdefault((scope.idx, name), []).append((lineno, kind, payload))

    def visit(node, scope):
        scopes_of[id(node)] = scope
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            inner = new_scope(scope)
            if isinstance(node, ast.Lambda):
                visit(node.body, inner)
                return
            # defaults and decorators evaluate in the enclosing scope
            for d in list(node.decorator_list) + list(node.args.defaults) + \
                    [d for d in node.args.kw_defaults if d is not None]:
                visit(d, scope)
            for arg in list(node.args.posonlyargs) + list(node.args.args) + \
                    list(node.args.kwonlyargs) + [node.args.vararg, node.args.kwarg]:
                if arg is not None:
                    record(inner, arg.arg, node.lineno, "loop", None)
            for child in node.body:
                visit(child, inner)
            return
        if isinstance(node, ast.Assign):
            tuple_bind = isinstance(node.value, ast.Call) and isinstance(node.targets[0], ast.Tuple)
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    record(scope, tgt.id, node.lineno, "direct", node.value)
                elif isinstance(tgt, ast.Attribute):
                    base = tgt.value
                    if isinstance(base, ast.Name):
                        record(scope, base.id + "." + tgt.attr, node.lineno, "direct", node.value)
                elif isinstance(tgt, ast.Tuple):
                    for i, el in enumerate(tgt.elts):
                        if isinstance(el, ast.Name):
                            if tuple_bind:
                                record(scope, el.id, node.lineno, "tuple", (i, node.value))
                            else:
                                record(scope, el.id, node.lineno, "other", None)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            record(scope, node.target.id, node.lineno, "direct", node.value)
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            # an augmented assignment changes the value without a plain binding
            record(scope, node.target.id, node.lineno, "other", None)
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            for el in ast.walk(node.target):
                if isinstance(el, ast.Name):
                    record(scope, el.id, getattr(el, "lineno", 0), "loop", None)
        for child in ast.iter_child_nodes(node):
            if id(child) not in scopes_of:
                visit(child, scope)

    root = new_scope(None)
    visit(tree, root)
    return assigns, scopes_of


def resolve(name, lineno, scope, assigns, depth=0):
    """Resolve a name in the call's scope chain (locals -> enclosing -> module)."""
    if depth > 8:
        return "unresolved", "name-chain"
    s = scope
    while s is not None:
        cand = [row for row in assigns.get((s.idx, name), []) if row[0] < lineno]
        if cand:
            classes = []
            for ln, kind, payload in cand:
                if kind == "loop":
                    classes.append(("unresolved", "loop-variable@%d" % ln))
                elif kind == "tuple":
                    idx, call = payload
                    if is_runner_call(call) and idx == 0:
                        classes.append(("measured", "tuple-run@%d" % ln))
                    else:
                        classes.append(("unresolved", "tuple-not-runner@%d" % ln))
                elif kind == "direct":
                    classes.append(classify(payload, ln, s, assigns, depth + 1))
                else:
                    classes.append(("unresolved", "other-assignment@%d" % ln))
            if all(c[0] == "measured" for c in classes):
                return "measured", classes[-1][1]
            if any(c[0] == "literal" for c in classes):
                return "literal", classes[-1][1]
            return "unresolved", classes[-1][1]
        s = s.parent
    return "unresolved", "no-assignment-in-scope-chain"


def classify(expr, lineno, scope, assigns, depth=0):
    if isinstance(expr, ast.Constant):
        return "literal", "constant"
    if isinstance(expr, ast.Name):
        return resolve(expr.id, lineno, scope, assigns, depth)
    if isinstance(expr, ast.Attribute):
        if expr.attr == "returncode":
            v = expr.value
            if isinstance(v, ast.Name):
                key = v.id + ".returncode"
                s = scope
                while s is not None:
                    mut = [r for r in assigns.get((s.idx, key), []) if r[0] < lineno]
                    if mut:
                        return classify(mut[-1][2], mut[-1][0], s, assigns, depth + 1)
                    s = s.parent
            if is_runner_call(v):
                return "measured", "returncode-of-runner"
            if isinstance(v, ast.Name):
                cls, det = resolve(v.id, lineno, scope, assigns, depth)
                if cls == "measured" and det.startswith("tuple-run"):
                    return "unresolved", "returncode-of-tuple"
                if cls == "unresolved":
                    s = scope
                    while s is not None:
                        nxt = [r for r in assigns.get((s.idx, v.id), []) if r[0] < lineno]
                        if nxt:
                            if nxt[-1][1] == "direct" and is_runner_call(nxt[-1][2]):
                                return "measured", "returncode-of-runner-name"
                            break
                        s = s.parent
                return "unresolved", "returncode-of-%s" % cls
            return "unresolved", "returncode-of-non-runner"
        return "unresolved", "attribute-" + expr.attr
    if isinstance(expr, ast.IfExp):
        a = classify(expr.body, lineno, scope, assigns, depth + 1)
        b = classify(expr.orelse, lineno, scope, assigns, depth + 1)
        if a[0] == "measured" and b[0] == "measured":
            return "measured", "both-branches"
        if a[0] == "literal" and b[0] == "literal":
            return "literal", "both-constant"
        return "unresolved", "mixed-ifexp"
    if isinstance(expr, ast.Call):
        return "unresolved", "plain-call"
    return "unresolved", type(expr).__name__


PARTIALS = {"partial", "functools.partial"}


def _target_names(node):
    return [n.id for n in ast.walk(node) if isinstance(n, ast.Name)]


def recorder_names(tree):
    """Returns (aliases, ambiguous, partials): name sets beyond `add` that record states."""
    binds = {}

    def bind(name, kind):
        binds.setdefault(name, []).append(kind)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            for tgt in targets:
                if isinstance(tgt, ast.Name) and isinstance(value, ast.Name):
                    bind(tgt.id, ("alias", value.id))
                elif (isinstance(tgt, ast.Name) and isinstance(value, ast.Call)
                      and call_name(value) in PARTIALS and value.args
                      and isinstance(value.args[0], ast.Name)):
                    bind(tgt.id, ("partial", value.args[0].id))
                else:
                    for n in _target_names(tgt):
                        bind(n, ("other", None))
        elif isinstance(node, ast.AugAssign):
            for n in _target_names(node.target):
                bind(n, ("other", None))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bind(node.name, ("other", None))
        elif isinstance(node, ast.arg):
            bind(node.arg, ("other", None))
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            for n in _target_names(node.target):
                bind(n, ("other", None))
        elif isinstance(node, ast.withitem) and node.optional_vars is not None:
            for n in _target_names(node.optional_vars):
                bind(n, ("other", None))
        elif isinstance(node, ast.ExceptHandler) and node.name:
            bind(node.name, ("other", None))
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for al in node.names:
                bind((al.asname or al.name).split(".")[0], ("other", None))
        elif isinstance(node, ast.NamedExpr):
            bind(node.target.id, ("other", None))
    rec = {"add"}
    aliases, partials = set(), set()
    changed = True
    while changed:
        changed = False
        for name, kinds in binds.items():
            if name == "add":
                continue
            for kind, src in kinds:
                if kind == "alias" and src in rec and name not in aliases:
                    aliases.add(name)
                    rec.add(name)
                    changed = True
                elif kind == "partial" and src in rec and name not in partials:
                    partials.add(name)
                    changed = True
    ambiguous = set()
    for name in aliases | partials:
        kinds = binds.get(name, [])
        clean_alias = all(k == "alias" and s in rec for k, s in kinds)
        clean_partial = all(k == "partial" and s in rec for k, s in kinds)
        if name in aliases and name in partials or not (clean_alias or clean_partial):
            ambiguous.add(name)
    return aliases - ambiguous, ambiguous, partials - ambiguous


def audit_text(text):
    """Returns (sites, exit_code, lines)."""
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return None, 2, ["AUDIT_SETUP unparsable:%s" % exc]
    assigns, scopes_of = collect_scopes(tree)
    add_defs = [n for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "add"]
    aliases, ambiguous, partials = recorder_names(tree)
    recorders = {"add"} | aliases | ambiguous | partials
    sites = []
    calls = sorted((n for n in ast.walk(tree)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                    and n.func.id in recorders), key=lambda n: n.lineno)
    for node in calls:
        label = "?"
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            label = node.args[0].value
        if node.func.id in ambiguous:
            sites.append((node.lineno, label, "unresolved", "ambiguous-recorder:" + node.func.id))
            continue
        if node.func.id in partials:
            sites.append((node.lineno, label, "unresolved", "partial-recorder:" + node.func.id))
            continue
        code_expr = None
        if len(node.args) >= 2:
            code_expr = node.args[1]
        for kw in node.keywords:
            if kw.arg == "code":
                code_expr = kw.value
        if code_expr is None:
            return None, 2, ["AUDIT_SETUP add-without-code:line=%d" % node.lineno]
        if len(add_defs) > 1:
            cls, det = "unresolved", "duplicate-add-definition"
        else:
            cls, det = classify(code_expr, node.lineno, scopes_of[id(node)], assigns)
        sites.append((node.lineno, label, cls, det))
    measured = sum(1 for s in sites if s[2] == "measured")
    literal = sum(1 for s in sites if s[2] == "literal")
    unmeasured = len(sites) - measured
    lines = ["CONTROL_ASSERT_SITE line=%d name=%s measured=%s class=%s detail=%s"
             % (ln, name, "yes" if cls == "measured" else "no", cls, det)
             for ln, name, cls, det in sites]
    lines.append("CONTROL_ASSERT_RECORDERS aliases=%d ambiguous=%d partial=%d names=%s"
                 % (len(aliases), len(ambiguous), len(partials),
                    ",".join(sorted(recorders))))
    lines.append("CONTROL_ASSERT sites=%d measured=%d literal=%d unmeasured=%d"
                 % (len(sites), measured, literal, unmeasured))
    return sites, (0 if unmeasured == 0 else 1), lines


SELFTEST_CASES = [
    ("direct-literal", 'def main():\n    add("x", 0, "b", 0)\n', "literal"),
    ("literal-via-name", 'def main():\n    rc = 0\n    add("x", rc, "b", 0)\n', "literal"),
    ("measured-returncode",
     'import subprocess\ndef main():\n    p = subprocess.run(["true"])\n    add("x", p.returncode, "b", 0)\n',
     "measured"),
    ("measured-tuple-run",
     'def run(a):\n    return 1, "o"\ndef main():\n    code, out = run(["x"])\n    add("x", code, "b", 0)\n',
     "measured"),
    ("rebound-mixed", 'import subprocess\ndef main():\n    rc = 0\n    p = subprocess.run(["true"])\n    rc = p.returncode\n    add("x", rc, "b", 0)\n',
     "literal"),
    ("all-measured-multiple",
     'import subprocess\ndef main():\n    p = subprocess.run(["true"])\n    rc = p.returncode\n    q = subprocess.run(["false"])\n    rc = q.returncode\n    add("x", rc, "b", 0)\n',
     "measured"),
    ("attr-mutation",
     'import subprocess\ndef main():\n    p = subprocess.run(["true"])\n    p.returncode = 0\n    add("x", p.returncode, "b", 1)\n',
     "literal"),
    ("augassign", 'def run(a):\n    return 1, "o"\ndef main():\n    code, out = run(["x"])\n    code += 7\n    add("x", code, "b", 0)\n',
     "unresolved"),
    ("duplicate-add",
     'def add(a, b, c, d):\n    pass\ndef add(a, b, c, d):\n    pass\ndef main():\n    add("x", 0, "b", 0)\n',
     "unresolved"),
    ("fake-returncode",
     'class X:\n    returncode = 0\ndef main():\n    x = X()\n    add("x", x.returncode, "b", 0)\n',
     "unresolved"),
    ("constant-ifexp", 'def main():\n    add("x", 0 if True else 0, "b", 0)\n', "literal"),
    ("loop-site", 'def run(a):\n    return 1, "o"\ndef main():\n    for n in ("a", "b"):\n        code, out = run(["x"])\n        add(n, code, "b", 0)\n',
     "measured"),
    ("no-assignment", 'def main():\n    add("x", rc, "b", 0)\n', "unresolved"),
    ("scope-shadow-constant",
     'import subprocess\ndef main():\n    rc = 0\n    def helper():\n        p = subprocess.run(["true"])\n        rc = p.returncode\n        return rc\n    add("x", rc, "b", 1)\n',
     "literal"),
    ("scope-shadow-attr",
     'import subprocess\nclass R:\n    returncode = 0\ndef main():\n    p = R()\n    def helper():\n        p = subprocess.run(["true"])\n        return p\n    add("x", p.returncode, "b", 1)\n',
     "unresolved"),
    # round-99 recorder-alias sites (v1 counts none of these; each is a single site)
    ("alias-literal", 'def main():\n    rec = add\n    rec("x", 0, "b", 0)\n', "measured"),
    ("alias-chain-literal", 'rec = add\nr2 = rec\ndef main():\n    r2("x", 0, "b", 0)\n', "literal"),
    ("alias-measured",
     'import subprocess\nrec = add\ndef main():\n    p = subprocess.run(["true"])\n    rec("x", p.returncode, "b", 0)\n',
     "measured"),
    ("alias-ambiguous",
     'import subprocess\nrec = add\ndef main():\n    p = subprocess.run(["true"])\n    rec("x", p.returncode, "b", 0)\nrec = print\n',
     "unresolved"),
    ("alias-shadowed-by-arg",
     'import subprocess\nrec = add\ndef main(rec):\n    p = subprocess.run(["true"])\n    rec("x", p.returncode, "b", 0)\n',
     "unresolved"),
    ("partial-recorder", 'import functools\nrec = functools.partial(add, "x")\ndef main():\n    rec(0, "b", 0)\n',
     "unresolved"),
    ("annotated-alias-literal", 'rec: object = add\ndef main():\n    rec("x", 0, "b", 0)\n', "literal"),
    ("non-recorder-name-not-a-site", 'rec = print\ndef main():\n    rec("x", 0, "b", 0)\n    add("y", 0, "b", 0)\n',
     "literal"),
]

CASE = {name: text for name, text, _ in SELFTEST_CASES}


def selftest():
    passed = total = 0
    for name, text, want in SELFTEST_CASES:
        sites, rc, lines = audit_text(text)
        got = sites[0][2] if sites and len(sites) == 1 else "site-count"
        ok = got == want
        passed += ok
        total += 1
        print("SELFTEST %s %s got=%s want=%s" % (name, "PASS" if ok else "FAIL", got, want))
    # exit-code arms: a conforming driver exits 0, a literal-coded one exits 1.
    _, rc_ok, _ = audit_text(CASE["measured-returncode"])
    _, rc_bad, _ = audit_text(CASE["direct-literal"])
    for name, got, want in (("exit-conforming", rc_ok, 0), ("exit-literal", rc_bad, 1)):
        ok = got == want
        passed += ok
        total += 1
        print("SELFTEST %s %s got=%s want=%s" % (name, "PASS" if ok else "FAIL", got, want))
    # loop site counts once, not twice (static call sites, not runtime calls). v1 indexed
    # SELFTEST_CASES[7], which is `augassign` (no loop); v2 binds the arm by name.
    sites, _, _ = audit_text(CASE["loop-site"])
    ok = len(sites) == 1 and "for " in CASE["loop-site"]
    passed += ok
    total += 1
    print("SELFTEST loop-site-count %s got=%d want=1" % ("PASS" if ok else "FAIL", len(sites)))
    # an alias call and a bare call in one driver are two sites
    sites, rc, _ = audit_text('import subprocess\nrec = add\ndef main():\n'
                              '    p = subprocess.run(["true"])\n    add("a", p.returncode, "b", 0)\n'
                              '    rec("c", 0, "b", 0)\n')
    ok = len(sites) == 2 and rc == 1 and [s[2] for s in sites] == ["measured", "literal"]
    passed += ok
    total += 1
    print("SELFTEST alias-and-bare-two-sites %s got=%d rc=%d" % ("PASS" if ok else "FAIL", len(sites), rc))
    print("CONTROL_ASSERT_V2_SELFTEST: %d/%d pass" % (passed, total))
    return 0 if passed == total else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None)
    ap.add_argument("--rev", default=None)
    ap.add_argument("--driver", default=DRIVER)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.repo or not a.rev:
        print(__doc__)
        sys.exit(64)
    if not re.fullmatch(r"[0-9a-f]{40}", a.rev):
        print("AUDIT_SETUP rev-not-a-commit-id")
        sys.exit(2)
    env = sealed_env()
    repo = os.path.realpath(a.repo)
    r = subprocess.run([GIT, "-C", repo, "rev-parse", "--verify", "--quiet",
                        "--end-of-options", a.rev + "^{commit}"], capture_output=True, env=env)
    if r.returncode != 0:
        print("AUDIT_SETUP rev-unresolvable")
        sys.exit(2)
    rev = r.stdout.decode().strip()
    b = subprocess.run([GIT, "-C", repo, "cat-file", "blob", "%s:%s" % (rev, a.driver)],
                       capture_output=True, env=env)
    if b.returncode != 0:
        print("AUDIT_SETUP driver-absent-at-rev:%s" % a.driver)
        sys.exit(2)
    try:
        text = b.stdout.decode("utf-8")
    except UnicodeDecodeError:
        print("AUDIT_SETUP driver-not-utf8")
        sys.exit(2)
    sites, rc, lines = audit_text(text)
    print("CONTROL_ASSERT_DRIVER rev=%s driver=%s sha256=%s"
          % (rev, a.driver, hashlib.sha256(b.stdout).hexdigest()))
    for line in lines:
        print(line)
    sys.exit(rc)


if __name__ == "__main__":
    main()
