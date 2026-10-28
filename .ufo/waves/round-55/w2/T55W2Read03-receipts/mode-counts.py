#!/usr/bin/env python3
"""Mode enumeration of the C0 C2 counter, plus its own arithmetic.

Run from a C0 clone of the lane: prints the counter's own mode table and the
total a perfect tree would score, then the frozen contract's target string.
"""
import importlib.util
import json
import pathlib

CLONE = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W2Read03/clone")
p = CLONE / ".ufo/evidence/round-55/c2/measure.py"
spec = importlib.util.spec_from_file_location("c2", p)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

table = c2.modes(pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W2Read03/d2work"), CLONE)
alloc = [m for m in table if m[3]]
lazy = [m for m in table if not m[3]]
print("modes=%d allocating=%d lazy=%d" % (len(table), len(alloc), len(lazy)))
print("allocating:", [m[0] for m in alloc])
print("lazy:", [m[0] for m in lazy])
print("SKILL.md numeral sum: seven self-tests + env-diff --contract + registry-check --rev = %d" % (7 + 1 + 1))
print("perfect-tree total, code's (8 - note) term with note=%d: %d"
      % (len(alloc), (7 - 7) + (8 - len(alloc)) + (1 - 1)))
target = json.loads((CLONE / ".ufo/evidence/round-55/contract.json").read_text())["claims"]["C2"]["target"]
print("contract.json (C0) amendments:", len(json.loads((CLONE / ".ufo/evidence/round-55/contract.json").read_text())["amendments"]))
print("contract.json target:", target[:120] + "...")
print("contract says nine allocating modes:", "9/9 allocating modes" in target)
