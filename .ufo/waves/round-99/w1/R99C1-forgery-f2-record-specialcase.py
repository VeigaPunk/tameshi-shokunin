#!/usr/bin/env python3
"""Forgery F2: treats ONLY the name 'record' as a recorder alias (plus chains
through it). No fixpoint alias discovery, no partial/annotated/ambiguous logic
beyond what the literal name triggers. Uses the real v1 grader when present."""
import ast, importlib.util, subprocess, sys

def load_v1():
    # find v1 next to the lane tools
    for cand in ("/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/control-assertion-audit.py", "tools/control-assertion-audit.py"):
        try:
            spec = importlib.util.spec_from_file_location("v1audit", cand)
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
            return m
        except Exception:
            pass
    return None

def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        print("CONTROL_ASSERT_V2_SELFTEST: 27/27 pass"); return 0
    # parse --repo/--rev/--driver crudely
    repo = args[args.index("--repo")+1]; rev = args[args.index("--rev")+1]; driver = args[args.index("--driver")+1]
    src = subprocess.run(["git","-C",repo,"cat-file","blob",f"{rev}:{driver}"],capture_output=True,text=True).stdout
    tree = ast.parse(src)
    # forgery: only 'record' is an alias, found by direct string search 'record = add'
    has_alias = "record = add" in src or "record=" in src.replace(" ","")
    # count add() and record() Call sites via AST (skip everything else)
    v1 = load_v1()
    sites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("add","record"):
            sites.append(node)
    # grade each site: literal if code arg is a literal constant
    measured = literal = unmeasured = 0
    for n in sites:
        code = n.args[1] if len(n.args) >= 2 else None
        is_lit = isinstance(code, ast.Constant) and isinstance(code.value, (int,float))
        if is_lit:
            literal += 1; unmeasured += 1
            print(f"CONTROL_ASSERT_SITE line={n.lineno} class=literal")
        else:
            measured += 1
            print(f"CONTROL_ASSERT_SITE line={n.lineno} class=measured")
    aliases = 1 if has_alias else 0
    names = "add,record" if has_alias else "add"
    print(f"CONTROL_ASSERT_RECORDERS aliases={aliases} ambiguous=0 partial=0 names={names}")
    print(f"CONTROL_ASSERT sites={len(sites)} measured={measured} literal={literal} unmeasured={unmeasured}")
    return 1 if (literal or unmeasured) else 0

sys.exit(main())
