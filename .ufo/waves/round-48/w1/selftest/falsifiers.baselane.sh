#!/bin/bash
# Round-47 QUALITY criteria 91-93: each block must FAIL its bad input and pass its good input; prints CRITERION-NN-FALSIFIER-OK.
# Usage: falsifiers.sh [REV]   (run from any cwd; REV defaults to the round-47 freeze; needs the lane checkout at the paths below)
L=/fast/scratch/hyaku/tameshi-r48/T48ExecSelftestReceipts/lane
E=$L/.ufo/evidence/round-47
REV=${1:-9acfbe21435e1976636a276448dee1d5e7155915}
BASE=0b5b7cd2b2c15d23086e811a0f0348d84261277b
T=$(mktemp -d -p /fast/scratch/hyaku/tameshi-r48/T48ExecSelftestReceipts/tmp)
# ---- 91: a lesson quote printed with a folded dash is refused by the byte-fidelity checker; the one-character repair passes
Q=$E/quality
(cd "$L" && python3 "$Q/lesson-quote-check.py" corpus/lessons/round-46.md > "$T/lq-bad.out" 2>&1; echo $? > "$T/lq-bad.rc")
(cd "$L" && python3 "$Q/lesson-quote-check.py" "$Q/round46-lesson-dash-restored.md" > "$T/lq-good.out" 2>&1; echo $? > "$T/lq-good.rc")
tail -1 "$T/lq-bad.out"; tail -1 "$T/lq-good.out"
if [ "$(cat "$T/lq-bad.rc")" = 1 ] && grep -q 'LQ FAIL tum-portal' "$T/lq-bad.out" && [ "$(cat "$T/lq-good.rc")" = 0 ]; then echo CRITERION-91-FALSIFIER-OK; else echo CRITERION-91-FALSIFIER-VACUOUS; fi
# ---- 92: a standing row must state the dependence set the statement shows; `deps none` on a node-dependent statement is refused
D="$T/lane"; git clone -q --no-hardlinks "$L" "$D" && [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] && git -C "$D" checkout -q --detach "$REV" || { echo CRITERION-92-FALSIFIER-VACUOUS; exit 1; }
row=$(grep '^EMIT_CAP | mutation report interop |' "$E/control/emit-observed-pre-freeze.out" | sed 's/^EMIT_CAP //')
mk() { # $1 = deps value
  printf '%s\n\n| Capability | What | Evidence | First |\n|---|---|---|---|\n%s\n' "$(git -C "$D" show "$BASE:SCORECARD.md")" "$(echo "$row" | sed "s/deps \`[a-z,-]*\`/deps \`$1\`/")" > "$D/SCORECARD.md"
  git -C "$D" add -A && git -C "$D" -c user.name=f -c user.email=f@f commit -qm "rows deps=$1" && git -C "$D" rev-parse HEAD
}
bad=$(mk none); good=$(mk node)
python3 "$D/$(echo .ufo/evidence/round-47)/calibration/measure.py" --lane "$D" --rev "$bad" --base "$BASE" --work "$T/w-bad" --only "mutation report interop" | grep '^C1_R47_PARTIAL' | grep -oE 'dep_mismatch=[0-9]+' | tee "$T/bad.out"
python3 "$D/$(echo .ufo/evidence/round-47)/calibration/measure.py" --lane "$D" --rev "$good" --base "$BASE" --work "$T/w-good" --only "mutation report interop" | grep '^C1_R47_PARTIAL' | grep -oE 'dep_mismatch=[0-9]+' | tee "$T/good.out"
if [ "$(cat "$T/bad.out")" = dep_mismatch=1 ] && [ "$(cat "$T/good.out")" = dep_mismatch=0 ]; then echo CRITERION-92-FALSIFIER-OK; else echo CRITERION-92-FALSIFIER-VACUOUS; fi
# ---- 93: a kill count survives only if a rule case named the kill: the AST-pin control kills every real mutant AND the neutral ones (refused), a bare-assert pin kills none by name (refused), the unchanged v1 counters stay below target
(cd "$L" && python3 "$E/control/run-controls.py" 2>&1 | grep -E '^CTL_(E|G|H)' | cut -c1-260 | tee "$T/ctl")
# an embedded differential oracle (T47CritC2Control (a)) passes the frozen counter but not the addition lint
python3 - "$T/oracle.py" <<'P'
import sys
open(sys.argv[1], 'w').write('import zlib, base64\n\ndef extra_Oracle():\n    exec(compile("x = 1", "<o>", "exec"))\n    return 1, 0\n')
P
python3 "$Q/addition-lint.py" --base "$L/.ufo/evidence/round-46/hardening/freshness-counter.py" "$T/oracle.py" | tail -2; lint_bad=${PIPESTATUS[0]}
python3 "$Q/addition-lint.py" --base "$L/.ufo/evidence/round-46/hardening/freshness-counter.py" $(ls "$L/.ufo/waves/round-47/w1"/T47HardFresh*.addition.py) | tail -1; lint_good=${PIPESTATUS[0]}
echo "c93 oracle_lint_exit=$lint_bad real_additions_lint_exit=$lint_good"
if [ "$lint_bad" = 1 ] && [ "$lint_good" = 0 ] && grep '^CTL_E' "$T/ctl" | grep -q 'neutral_killed=[1-9]' && grep '^CTL_H' "$T/ctl" | grep -q 'killed=0 ' && grep '^CTL_G' "$T/ctl" | grep -q 'C2_R47_PASS=false'; then echo CRITERION-93-FALSIFIER-OK; else echo CRITERION-93-FALSIFIER-VACUOUS; fi
rm -rf "$T"
