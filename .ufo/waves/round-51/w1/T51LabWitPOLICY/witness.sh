#!/usr/bin/env bash
# C2 S_POLICY survivor witness driver — seat T51LabWitPOLICY, round-51 w1.
# Witness: one no-hash baseline row (path registered via DRIFT_EXTRA_NOHASH)
# whose sha field is NOT `-` (off-suite; the selftest pins `-`). Plus one
# symbol row so the symbols file is non-empty.
# Pristine: POLICY refusal (exit 1). Mutant: guard flipped (sha=="-x" never
# true), so no POLICY line; falls through to sha compare -> DRIFT sha line.
set -u
S=${WIT_ROOT:-/fast/scratch/hyaku/tameshi-r51/T51LabWitPOLICY}
PRIS="$S/pristine.sh"; MUT="$S/mutant.sh"; W="$S/w/wit"
: > "$S/runs.tsv"
run() { # run <label> <gate>
  local label=$1 gate=$2 i rc
  for i in 1 2 3; do
    env -i HOME="$S/home" TMPDIR="$S/w" DRIFT_EXTRA_NOHASH="$W/secret.txt" \
      bash "$gate" --baseline "$W/base.tsv" --symbols "$W/sym.tsv" \
      > "$S/runs.$label.$i.out" 2>&1
    rc=$?
    printf '%s\t%s\t%s\n' "$label" "$i" "$rc" >> "$S/runs.tsv"
  done
}
run pristine "$PRIS"
run mutant "$MUT"
