#!/usr/bin/env python3
"""Do-nothing control for C2: a manifest of non-guard string edits that still
prints the frozen predicate. Uses the frozen guard-inertia.py as a module.
Writes only under this scratch dir; reads the lane read-only."""
import hashlib
import importlib.util
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
TOOL = os.path.join(LANE, ".ufo/evidence/round-97/c2/guard-inertia.py")
CHECKER = os.path.join(LANE, ".ufo/evidence/round-96/conjunct-disposition-v96.py")
SCRATCH = "/fast/scratch/hyaku/tameshi-r97/R97C1"

os.environ["HYAKU_SCRATCH"] = SCRATCH

spec = importlib.util.spec_from_file_location("guard_inertia", TOOL)
gi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gi)

checker = open(CHECKER, "rb").read()
print("checker_sha256=%s" % hashlib.sha256(checker).hexdigest())
print("checker_has_token=%s" % (b"DISPOSITION rows=" in checker))
print("checker_has_guard_anchor=%s" % (b"MIN_REASON = 40" in checker))

# 8 "killed" rows: the edit changes an UNRELATED printed token, never a guard.
kill_old = "DISPOSITION rows="
kill_new = "DISPOSITION rowz="
# 2 "limit" rows: a byte change with no behavioural effect.
limit_old = "MIN_REASON = 40"
limit_new = "MIN_REASON = 40 "

rows = []
for i in range(8):
    rows.append({
        "id": "trivial-kill-%d" % i,
        "guard": "NOT A GUARD: the summary-token print only",
        "edit": {"old": kill_old, "new": kill_new},
        "state": "clean",
        "pristine": {"exit": 0, "token": "DISPOSITION rows="},
        "expect": "killed",
    })
for i in range(2):
    rows.append({
        "id": "trivial-limit-%d" % i,
        "guard": "NOT A GUARD: an inert byte change",
        "edit": {"old": limit_old, "new": limit_new},
        "state": "clean",
        "pristine": {"exit": 0, "token": "DISPOSITION rows="},
        "expect": "limit",
        "limit_mechanism": "the edit only appends a space to an unprinted constant; exit and token are identical",
    })
manifest = {"rows": rows}
tag = os.path.join(SCRATCH, "c2-donothing-tree")
os.makedirs(tag, exist_ok=True)
rc = gi.run_matrix(checker, manifest, tag)
print("run_matrix rc=%d" % rc)
sys.exit(0)
