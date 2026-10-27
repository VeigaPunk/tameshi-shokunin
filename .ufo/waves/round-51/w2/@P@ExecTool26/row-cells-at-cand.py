import importlib.util, json, sys, os
spec = importlib.util.spec_from_file_location("m", "/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool26/measure_c3.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LANE="/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV="6d8c11e378aa90b12650808e1b79270742935f15"
skill = m.show(LANE, REV, "SKILL.md").decode("utf-8","surrogateescape")
rows = m.registry_rows(skill)
print("total 8-cell rows parsed:", len(rows))
for n,c in rows:
    if "tools/witness-metadata.py" in c[2]:
        print("=== candidate row at SKILL.md line", n, "===")
        for k,v in zip(["name","kind","entry","vmap","selftest","pinned","scope","owner"], c):
            print(f"  [{k}] {v}")
        why, argv = m.row_reason(LANE, REV, "tools/witness-metadata.py", c)
        print("  row_reason ->", why, argv)
