#!/bin/bash
# Round-47 QUALITY criteria 91-92: each block must FAIL its bad input and pass its good input; prints CRITERION-NN-FALSIFIER-OK.
# Usage: falsifiers.sh [REV]   (run from any cwd; REV defaults to the round-47 freeze; needs the lane checkout at the paths below)
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
E=$L/.ufo/evidence/round-47
REV=${1:-9acfbe21435e1976636a276448dee1d5e7155915}
BASE=0b5b7cd2b2c15d23086e811a0f0348d84261277b
T=$(mktemp -d)
# ---- 91: a standing row must state the dependence set the statement shows; `deps none` on a node-dependent statement is refused
D="$T/lane"; git clone -q --no-hardlinks "$L" "$D" && [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] && git -C "$D" checkout -q --detach "$REV" || { echo CRITERION-91-FALSIFIER-VACUOUS; exit 1; }
row=$(grep '^EMIT_CAP | mutation report interop |' "$E/control/emit-observed-pre-freeze.out" | sed 's/^EMIT_CAP //')
mk() { # $1 = deps value
  printf '%s\n\n| Capability | What | Evidence | First |\n|---|---|---|---|\n%s\n' "$(git -C "$D" show "$BASE:SCORECARD.md")" "$(echo "$row" | sed "s/deps \`[a-z,-]*\`/deps \`$1\`/")" > "$D/SCORECARD.md"
  git -C "$D" add -A && git -C "$D" -c user.name=f -c user.email=f@f commit -qm "rows deps=$1" && git -C "$D" rev-parse HEAD
}
bad=$(mk none); good=$(mk node)
python3 "$D/$(echo .ufo/evidence/round-47)/calibration/measure.py" --lane "$D" --rev "$bad" --base "$BASE" --work "$T/w-bad" --only "mutation report interop" | grep '^C1_R47_PARTIAL' | grep -oE 'dep_mismatch=[0-9]+' | tee "$T/bad.out"
python3 "$D/$(echo .ufo/evidence/round-47)/calibration/measure.py" --lane "$D" --rev "$good" --base "$BASE" --work "$T/w-good" --only "mutation report interop" | grep '^C1_R47_PARTIAL' | grep -oE 'dep_mismatch=[0-9]+' | tee "$T/good.out"
if [ "$(cat "$T/bad.out")" = dep_mismatch=1 ] && [ "$(cat "$T/good.out")" = dep_mismatch=0 ]; then echo CRITERION-91-FALSIFIER-OK; else echo CRITERION-91-FALSIFIER-VACUOUS; fi
# ---- 92: a kill count survives only if a rule case named the kill: the AST-pin control kills every real mutant AND the neutral ones (refused), a bare-assert pin kills none by name (refused), the unchanged v1 counters stay below target
(cd "$L" && python3 "$E/control/run-controls.py" 2>&1 | grep -E '^CTL_(E|G|H)' | cut -c1-260 | tee "$T/ctl")
if grep '^CTL_E' "$T/ctl" | grep -q 'neutral_killed=[1-9]' && grep '^CTL_H' "$T/ctl" | grep -q 'killed=0 ' && grep '^CTL_G' "$T/ctl" | grep -q 'C2_R47_PASS=false'; then echo CRITERION-92-FALSIFIER-OK; else echo CRITERION-92-FALSIFIER-VACUOUS; fi
rm -rf "$T"
