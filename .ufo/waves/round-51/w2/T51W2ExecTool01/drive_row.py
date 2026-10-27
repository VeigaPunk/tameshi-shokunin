#!/usr/bin/env python3
"""Run the frozen C3 counter's OWN row logic against the bash-witness-study row
at the candidate revision. Read-only on the lane; writes only into scratch."""
import importlib.util, json, os, subprocess, sys

CAND = "6d8c11e378aa90b12650808e1b79270742935f15"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
CLONE = "/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool01/cand"
WORK = "/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool01/work"
TOOL = "tools/bash-witness-study.py"

spec = importlib.util.spec_from_file_location(
    "c3", os.path.join(CLONE, ".ufo/evidence/round-51/c3/measure.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

skill = m.show(LANE, CAND, "SKILL.md").decode("utf-8", "surrogateescape")
rows = m.registry_rows(skill)
print("registry_rows found:", len(rows))
hits = [(n, c) for n, c in rows if TOOL in c[2]]
for n, c in hits:
    print("---- row at SKILL.md:%d" % n)
    for i, cell in enumerate(c):
        print("   cell%d: %s" % (i, cell[:300]))

os.makedirs(WORK, exist_ok=True)
for n, c in hits:
    why, spec_argv = m.row_reason(LANE, CAND, TOOL, c)
    print("row_reason(line %d) -> why=%r argv=%r" % (n, why, spec_argv))
    if why is None:
        rc, last = m.run_row(CLONE, WORK, spec_argv)
        print("run_row(line %d) -> rc=%r last=%r" % (n, rc, last))
