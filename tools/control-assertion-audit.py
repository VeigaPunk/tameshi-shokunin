#!/usr/bin/env python3
"""control-assertion-audit — static provenance audit of a control driver.

Round 97's pre-freeze driver registered one state whose graded code was the
literal 0 (`add("c2-nowork-absent", 0, ...)`), so that control could not fail
whatever the `git grep` it wrapped returned (round-97 spot-check D-2). This
tool classifies every `add(...)` call site in a driver by where its recorded
code expression comes from:

  measured    the expression derives from a runner call (`sh`, `git`, `run`,
              `subprocess.run`): `p.returncode`, or the first element of
              `code, out = run(...)`; a name chain is followed to its last
              assignment before the call.
  literal     a constant, directly or bound through a name.
  unresolved  any other expression (a non-runner `.returncode`, a plain call,
              arithmetic, a loop variable, a name with no prior assignment).

A driver is conforming only when every site is `measured`; an expectation
(`want_code`) is data and is not classified.

Usage:
  python3 -I tools/control-assertion-audit.py --repo LANE --rev <40 hex> \
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


def collect_assigns(tree):
    """name -> [(lineno, kind, payload)] in source order.

    kind: 'direct' (payload = expression), 'tuple' (payload = (index, call)),
          'loop' (payload = None), 'other' (payload = expression).
    """
    out = {}

    def rec(node):
        for child in ast.iter_child_nodes(node):
            rec(child)
        if isinstance(node, ast.Assign):
            val = node.value
            tuple_bind = isinstance(node.value, ast.Call) and isinstance(node.targets[0], ast.Tuple)
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    kind = "direct"
                    out.setdefault(tgt.id, []).append((node.lineno, kind, val))
                elif isinstance(tgt, ast.Tuple):
                    for i, el in enumerate(tgt.elts):
                        if isinstance(el, ast.Name):
                            if tuple_bind:
                                out.setdefault(el.id, []).append((node.lineno, "tuple", (i, val)))
                            else:
                                out.setdefault(el.id, []).append((node.lineno, "other", None))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.value is not None:
                out.setdefault(node.target.id, []).append((node.lineno, "direct", node.value))
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            for el in ast.walk(node.target):
                if isinstance(el, ast.Name):
                    out.setdefault(el.id, []).append((getattr(el, "lineno", 0), "loop", None))

    rec(tree)
    return out


def resolve(name, lineno, assigns, depth=0):
    """Returns (class, detail) for a name used as a recorded code."""
    if depth > 8:
        return "unresolved", "name-chain"
    cand = [row for row in assigns.get(name, []) if row[0] < lineno]
    if not cand:
        return "unresolved", "no-assignment-before-call"
    ln, kind, payload = max(cand, key=lambda r: r[0])
    if kind == "loop":
        return "unresolved", "loop-variable"
    if kind == "tuple":
        idx, call = payload
        if is_runner_call(call) and idx == 0:
            return "measured", "tuple-run@%d" % ln
        return "unresolved", "tuple-not-runner@%d" % ln
    if kind == "direct":
        return classify(payload, ln, assigns, depth + 1)
    return "unresolved", "other-assignment@%d" % ln


def classify(expr, lineno, assigns, depth=0):
    if isinstance(expr, ast.Constant):
        return "literal", "constant"
    if isinstance(expr, ast.Name):
        return resolve(expr.id, lineno, assigns, depth)
    if isinstance(expr, ast.Attribute):
        if expr.attr == "returncode":
            v = expr.value
            if is_runner_call(v):
                return "measured", "returncode-of-runner"
            if isinstance(v, ast.Name):
                cls, det = resolve(v.id, lineno, assigns, depth)
                if cls == "measured" and det.startswith("tuple-run"):
                    return "unresolved", "returncode-of-tuple"
                if cls == "unresolved":
                    nxt = [r for r in assigns.get(v.id, []) if r[0] < lineno]
                    if nxt and nxt[-1][1] == "direct" and is_runner_call(nxt[-1][2]):
                        return "measured", "returncode-of-runner-name"
                return "unresolved", "returncode-of-%s" % cls
            return "unresolved", "returncode-of-non-runner"
        return "unresolved", "attribute-" + expr.attr
    if isinstance(expr, ast.IfExp):
        a = classify(expr.body, lineno, assigns, depth + 1)
        b = classify(expr.orelse, lineno, assigns, depth + 1)
        if a[0] == "measured" and b[0] == "measured":
            return "measured", "both-branches"
        if a[0] == "literal" and b[0] == "literal":
            return "literal", "both-constant"
        return "unresolved", "mixed-ifexp"
    if isinstance(expr, ast.Call):
        return "unresolved", "plain-call"
    return "unresolved", type(expr).__name__


def audit_text(text):
    """Returns (sites, exit_code, lines)."""
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return None, 2, ["AUDIT_SETUP unparsable:%s" % exc]
    assigns = collect_assigns(tree)
    sites = []
    calls = sorted((n for n in ast.walk(tree)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                    and n.func.id == "add"), key=lambda n: n.lineno)
    for node in calls:
        code_expr = None
        if len(node.args) >= 2:
            code_expr = node.args[1]
        for kw in node.keywords:
            if kw.arg == "code":
                code_expr = kw.value
        label = "?"
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            label = node.args[0].value
        if code_expr is None:
            return None, 2, ["AUDIT_SETUP add-without-code:line=%d" % node.lineno]
        cls, det = classify(code_expr, node.lineno, assigns)
        sites.append((node.lineno, label, cls, det))
    measured = sum(1 for s in sites if s[2] == "measured")
    literal = sum(1 for s in sites if s[2] == "literal")
    unmeasured = len(sites) - measured
    lines = ["CONTROL_ASSERT_SITE line=%d name=%s measured=%s class=%s detail=%s"
             % (ln, name, "yes" if cls == "measured" else "no", cls, det)
             for ln, name, cls, det in sites]
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
    ("rebound-to-measured",
     'import subprocess\ndef main():\n    rc = 0\n    p = subprocess.run(["true"])\n    rc = p.returncode\n    add("x", rc, "b", 0)\n',
     "measured"),
    ("fake-returncode",
     'class X:\n    returncode = 0\ndef main():\n    x = X()\n    add("x", x.returncode, "b", 0)\n',
     "unresolved"),
    ("constant-ifexp", 'def main():\n    add("x", 0 if True else 0, "b", 0)\n', "literal"),
    ("loop-site", 'def run(a):\n    return 1, "o"\ndef main():\n    for n in ("a", "b"):\n        code, out = run(["x"])\n        add(n, code, "b", 0)\n',
     "measured"),
    ("no-assignment", 'def main():\n    add("x", rc, "b", 0)\n', "unresolved"),
]


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
    _, rc_ok, _ = audit_text(SELFTEST_CASES[2][1])
    _, rc_bad, _ = audit_text(SELFTEST_CASES[0][1])
    for name, got, want in (("exit-conforming", rc_ok, 0), ("exit-literal", rc_bad, 1)):
        ok = got == want
        passed += ok
        total += 1
        print("SELFTEST %s %s got=%s want=%s" % (name, "PASS" if ok else "FAIL", got, want))
    # loop site counts once, not twice (static call sites, not runtime calls)
    sites, _, _ = audit_text(SELFTEST_CASES[7][1])
    ok = len(sites) == 1
    passed += ok
    total += 1
    print("SELFTEST loop-site-count %s got=%d want=1" % ("PASS" if ok else "FAIL", len(sites)))
    print("CONTROL_ASSERT_SELFTEST: %d/%d pass" % (passed, total))
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
