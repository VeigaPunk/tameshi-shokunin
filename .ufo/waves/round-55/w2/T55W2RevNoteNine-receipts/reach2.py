"""Branch-scoped reachability: which documented mode reaches which scratch
allocation site, in the seven tools that call strict_scratch_root().

Entry points are the documented modes; `prune` removes the sibling mode's
subtree that a shared dispatcher also calls (e.g. main()'s --selftest branch),
so the closure is the mode's own path.
"""
import ast, sys
from pathlib import Path

def call_name(n):
    f = n.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None

def analyse(path):
    tree = ast.parse(path.read_text())
    funcs, class_init = {}, {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef):
                    funcs["%s.%s" % (node.name, sub.name)] = sub
                    if sub.name == "__init__":
                        class_init[node.name] = "%s.__init__" % node.name
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs[node.name] = node
    sites, edges = [], {n: set() for n in funcs}
    for name, node in funcs.items():
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                cn = call_name(sub)
                if cn == "strict_scratch_root":
                    sites.append((sub.lineno, "strict_scratch_root()", name))
                elif cn in ("mkdtemp", "TemporaryDirectory", "NamedTemporaryFile"):
                    kw = {k.arg for k in sub.keywords}
                    sites.append((sub.lineno, "tempfile.%s%s" % (cn, "" if "dir" in kw else " (NO dir=)"), name))
                elif cn in funcs and cn != name:
                    edges[name].add(cn)
                elif cn in class_init:
                    edges[name].add(class_init[cn])
    return sites, edges

def closure(starts, edges, prune):
    seen, stack = set(), [s for s in starts if s not in prune]
    while stack:
        n = stack.pop()
        if n in seen or n not in edges:
            continue
        seen.add(n)
        stack.extend(c for c in edges[n] if c not in prune)
    return seen

MODES = {
 "env-diff": [("--selftest", ["selftest"], ()), ("--contract", ["main"], ("selftest",))],
 "repeat-control": [("--selftest", ["selftest"], ()), ("--snapshot", ["snapshot_mode"], ("selftest",)),
                    ("--runs/--out", ["run_mode"], ("selftest",))],
 "registry-check": [("--selftest", ["selftest"], ()), ("--rev", ["main"], ("selftest",)),
                    ("--root live run", ["main"], ("selftest", "clone_lane_at_rev"))],
 "bash-witness-study": [("declare", ["cmd_declare"], ()), ("run", ["cmd_run"], ()),
                        ("rerun", ["cmd_rerun"], ()), ("count", ["cmd_count"], ()),
                        ("check", ["cmd_check"], ()), ("selftest", ["cmd_selftest"], ())],
 "pin-disposition": [("--manifest/--root", ["run_mode"], ()), ("--selftest", ["selftest"], ())],
 "evidence-disposition": [("--root/--dispositions", ["main"], ("selftest",)), ("--selftest", ["selftest"], ())],
 "context-capture": [("--check", ["main"], ("run_selftest",)), ("--selftest", ["run_selftest"], ())],
}
root = Path(sys.argv[1])
print("%-22s %-24s %-52s %s" % ("tool", "documented mode", "allocation site", "guarded"))
for tool, modes in MODES.items():
    sites, edges = analyse(root / "tools" / (tool + ".py"))
    for mode, entries, prune in modes:
        reach = closure(entries, edges, set(prune))
        hits = [(ln, k, fn) for ln, k, fn in sites if fn in reach]
        if not hits:
            print("%-22s %-24s %-52s %s" % (tool, mode, "- no allocation on this path -", "n/a"))
        for ln, kind, fn in sorted(hits):
            print("%-22s %-24s %-52s %s" % (tool, mode, "%s.py:%d %s in %s()" % (tool, ln, kind, fn),
                                             "NO" if "NO dir=" in kind else "yes"))
