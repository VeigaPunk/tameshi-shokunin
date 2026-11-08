#!/usr/bin/env python3
"""T92SN1 probe 3 — does the counter honour the SPEC pin as a *precondition*?

Evidence chain, all against the committed bytes of
.ufo/evidence/round-92/c1/measure-v92.py (sha256 be5a9221…):

  H2a: the SPEC_SHA check is computed but never gates use of the spec.
       The spec's own fields (gate.repo / gate.path / gate.fixtures, and each
       mutant's witness dict) are consumed to build filesystem paths and to
       build a shell argv.  A spec whose sha256 does not equal SPEC_SHA is
       still executed.
  H2b: build_witness() joins an *unpinned* witness path onto the lane dir with
       os.path.join and no confinement check, so an absolute or ../-bearing
       path lands OUTSIDE the --work dir.
  H2c: the driver derives the mutant/state fixtures from the lane's *mutable
       working tree* (states(lane) -> spec_edit(lane, …)), not from the pinned
       rev, so the committed receipts are not fully rev-pinned.

Every write of this probe stays under the scratch dir except the two
deliberate escape targets, which are named under the scratch dir itself so the
escape is visible without touching anything outside scratch.
"""
import importlib.util, json, os, sys, tempfile, shutil, subprocess

S = "/fast/scratch/hyaku/tameshi-r92/T92SN1"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
COUNTER = os.path.join(LANE, ".ufo/evidence/round-92/c1/measure-v92.py")

spec = importlib.util.spec_from_file_location("m92", COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

print("== H2a: is the SPEC pin a precondition? ==")
src = open(COUNTER, encoding="utf-8").read()
i = src.index("spec_pinned =")
print(src[i:i+420])

print("\n== H2b: build_witness() with an unpinned witness path ==")
esc_dir = os.path.join(S, "specescape", "ESCAPED_DIR")
esc_file = os.path.join(S, "specescape", "ESCAPED_FILE.txt")
os.makedirs(os.path.dirname(esc_dir), exist_ok=True)
d = tempfile.mkdtemp(dir=os.path.join(S, "specescape") if os.path.isdir(os.path.join(S, "specescape")) else None,
                     prefix="w-")
shutil.rmtree(d, ignore_errors=True)
os.makedirs(d, exist_ok=True)
w = {"sources": None, "dirs": [esc_dir], "files": [esc_file]}
lane_dir = m.build_witness(d, w)
print("build_witness returned lane dir:", lane_dir)
print("ESCAPED_DIR created outside the witness dir? ", os.path.isdir(esc_dir))
print("ESCAPED_FILE created outside the witness dir?", os.path.isfile(esc_file))
print("witness dir contents:", sorted(os.listdir(lane_dir)))

print("\n== H2c: does the driver derive fixtures from the working tree? ==")
drv = open(os.path.join(LANE, ".ufo/evidence/round-92/c1/controls-v92.py"), encoding="utf-8").read()
for ln, line in enumerate(drv.split("\n"), 1):
    if "spec_edit(lane" in line or "def spec_edit" in line or "os.path.join(lane, SPEC)" in line:
        print("  driver:%d: %s" % (ln, line.rstrip()))
print("  driver reads the lane worktree spec, and the counter reads the spec at --rev:",
      "blob(repo, rev, SPEC_PATH)" in src)

print("\n== H2d: does the counter refuse a spec that fails the pin? (dry, no run) ==")
print("  spec_pinned is assigned, then spec is used unconditionally;")
print("  'die(' occurrences after the assignment:",
      src[i:i+3000].count("die("))
