#!/bin/bash
# Run the frozen deciding-run.sh against one fixture, time-boxed.
# Usage: probe.sh NAME S [TIMEOUT_SECONDS]
# Prints the exit code, any DECIDING_REFUSED lines, and which OUT artefacts exist.
set -u
NAME=$1; S=$2; T=${3:-8}
D=$S/fix-$NAME; OUT=$D/.ufo/evidence/round-55/after
REV=$(git -C "$D" rev-parse HEAD)
mkdir -p "$S/hyaku-$NAME"
echo "### fixture=$D rev=$REV freeze=e2979f277138da503af27b263b783f626f109be4 out=$OUT timeout=${T}s"
HYAKU_SCRATCH=$S/hyaku-$NAME TMPDIR=$S/hyaku-$NAME \
  timeout "$T" bash "$D/.ufo/evidence/round-55/deciding-run.sh" "$D" "$REV" \
  e2979f277138da503af27b263b783f626f109be4 "$OUT" > "$S/$NAME.run.stdout" 2> "$S/$NAME.run.stderr"
rc=$?
echo "rc=$rc  (124 = still running when the timeout fired, i.e. past every gate refusal; 3 = refused)"
echo "--- refusal lines:"; grep -h 'DECIDING_REFUSED' "$S/$NAME.run.stdout" "$S/$NAME.run.stderr" || echo "(none)"
echo "--- gate artefacts in OUT:"; ls -1 "$OUT" 2>/dev/null | sed 's/^/  /' || echo "  (outdir missing)"
echo "--- stdout head:"; head -4 "$S/$NAME.run.stdout"
