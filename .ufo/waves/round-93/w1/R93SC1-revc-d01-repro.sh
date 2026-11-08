#!/usr/bin/env bash
# R93SC1 probe: the round-93 D01 removal mutant at the PRE-A3 instrument revision.
#
# Claim under test (the round-93 lesson class): "a duplicated rule hides which
# removal is load-bearing". At the rev-C instrument (b34c929e) the reader carried
# the stray-verdict rule in TWO places -- inside the table loop (for a table whose
# header row carries no `verdict` cell) and in the block-line scan. The driver's
# D01 anchor removes only the block-line copy, so the in-table copy still fires:
# the `renamed-result` state is still refused and the mutant does NOT flip to
# C1_R93_PASS=true. The driver's expectation for D01 is (exit 0, PASS=true), so
# the run reports `D01 MISMATCH exit=1`.
#
# At the A3 instrument (855f0c1c) the same driver anchor removes the single
# remaining copy, the state passes, and the committed receipt
# `.ufo/evidence/round-93/pre-freeze/controls/D01.out` reads `exit=0` /
# `C1_R93_PASS=true`.
#
# Read-only on the lane: the driver and the counter are read with `git
# cat-file`; the clones and work dirs live under the scratch dir.
#
# Usage: R93SC1-revc-d01-repro.sh <scratch-dir>
set -euo pipefail

LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV_C=b34c929e
REV_A3=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
BASE=4a7e259b407d582d2010197f32d7524d6bed5370

S=${1:?scratch dir required}
mkdir -p "$S"

echo "== the two copies of the stray-verdict rule at $REV_C =="
git -C "$LANE" show "$REV_C:.ufo/evidence/round-93/c1/measure-v93.py" \
  | grep -n "stray-verdict" || true

echo "== the single copy at $REV_A3 =="
git -C "$LANE" show "$REV_A3:.ufo/evidence/round-93/c1/measure-v93.py" \
  | grep -n "stray-verdict" || true

echo "== D01 anchor in the driver (rev C) =="
git -C "$LANE" show "$REV_C:.ufo/evidence/round-93/c1/controls-v93.py" \
  | sed -n '/a = """/,/"""/p'

echo "== running the rev-C battery with --only D01 =="
git -C "$LANE" cat-file blob "$REV_C:.ufo/evidence/round-93/c1/controls-v93.py" \
  > "$S/controls-v93-revC.py"
rm -rf "$S/work" "$S/out"
mkdir -p "$S/work" "$S/out"
python3 -I "$S/controls-v93-revC.py" \
  --lane "$LANE" --rev "$REV_C" --base "$BASE" \
  --work "$S/work" --outdir "$S/out" --only D01 --jobs 1 || true

echo "== the rev-C D01 receipt =="
cat "$S/out/D01.out"

echo "== the committed A3 D01 receipt (for comparison) =="
cat "$LANE/.ufo/evidence/round-93/pre-freeze/controls/D01.out" | head -4
cat "$LANE/.ufo/evidence/round-93/pre-freeze/controls/D01.out" | tail -4
