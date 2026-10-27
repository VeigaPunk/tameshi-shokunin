#!/usr/bin/env bash
# T51LabWitUSAGEEXIT — S_USAGE_EXIT survivor-witness probe (C2, round 51).
#
# Witness input: one unknown argument (--witness-unknown-arg).
# Prediction to falsify equivalence: pristine exits 2 with
#   stderr last line: drift-pins: unknown argument: --witness-unknown-arg
# mutant (exit 2 -> exit 0 at the `*)` catch-all) exits 0 with the same line.
#
# Hermetic: HOME and TMPDIR point inside the scratch root; the gate exits
# during argument parsing, so no baseline/symbols fixture is needed and no
# pinned real-HOME file is touched. cwd is the scratch work dir.
# Usage: witness.sh <pristine.sh> <mutant.sh> <scratch-root>
set -u
PRISTINE=$1
MUTANT=$2
S=$3
W=$S/w
mkdir -p "$W" "$S/home"
cd "$W" || exit 9

export HOME="$S/home"
export TMPDIR="$S"

printf 'witness input: bash <gate> --witness-unknown-arg  (no other args, empty scratch HOME)\n'
printf 'cwd=%s HOME=%s TMPDIR=%s\n\n' "$W" "$HOME" "$TMPDIR"

for variant in pristine mutant; do
  case "$variant" in
    pristine) script=$PRISTINE ;;
    mutant)   script=$MUTANT ;;
  esac
  printf '%s sha256=%s\n' "$variant" "$(sha256sum "$script" | cut -d' ' -f1)"
  for run in 1 2 3; do
    out="$W/${variant}.run${run}.out"
    err="$W/${variant}.run${run}.err"
    bash "$script" --witness-unknown-arg >"$out" 2>"$err"
    rc=$?
    printf '%s run%d exit=%d stdout_bytes=%d stderr_last_line=[%s]\n' \
      "$variant" "$run" "$rc" "$(wc -c <"$out")" "$(tail -n 1 "$err")"
  done
  printf '\n'
done

printf '%s\n' '--- cross-variant diff of captured streams (run 1) ---'
printf 'stdout diff: %s\n' "$(diff -u "$W/pristine.run1.out" "$W/mutant.run1.out" >/dev/null 2>&1 && echo identical || echo differs)"
printf 'stderr diff: %s\n' "$(diff -u "$W/pristine.run1.err" "$W/mutant.run1.err" >/dev/null 2>&1 && echo identical || echo differs)"
printf '%s\n' '--- exit codes across all runs ---'
for variant in pristine mutant; do
  for run in 1 2 3; do
    printf '%s run%d: see run.log lines above\n' "$variant" "$run"
  done
done
