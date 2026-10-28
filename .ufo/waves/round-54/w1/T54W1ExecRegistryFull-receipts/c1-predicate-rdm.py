#!/usr/bin/env python3
"""Feed this seat's full-check stdout to the FROZEN round-52 C1 predicate.

Runs only the R (registry replay), D (dropped active rows) and M (mte row)
components of .ufo/evidence/round-52/c1/measure.py, from git objects at C0.
C and G are other tools' subjects and are not evaluated here.
"""
import importlib.util
import json
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
C0 = "59c38109bf119d0e9d4f878644a82babc937bc1e"
OUT = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ExecRegistryFull-receipts/full-check-c0.out"

spec = importlib.util.spec_from_file_location(
    "m52", LANE + "/.ufo/evidence/round-52/c1/measure.py")
m52 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m52)

out = open(OUT).read()
held, n, not_held, extra = m52.parse_registry_check(out)
print("R: held=%s n=%s not_held=%r extra=%s" % (held, n, not_held, extra))

base = json.load(open(LANE + "/.ufo/evidence/round-52/c1/base-active.json"))["active"]
reg = json.loads(subprocess.run(
    ["git", "-C", LANE, "show", C0 + ":tools/registry.json"],
    capture_output=True).stdout)
active = {r["name"] for r in reg["rows"] if r["status"] == "active"}
print("D: dropped=%r" % (sorted(set(base) - active),))

mte = subprocess.run(
    ["git", "-C", LANE, "show", C0 + ":tools/mte-interop.py"],
    capture_output=True).stdout.decode()
print("M: mte_row_ok=%r" % (m52.mte_row_ok(reg, mte),))
