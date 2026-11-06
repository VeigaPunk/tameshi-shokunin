#!/usr/bin/env bash
# T88E2 — commit each variant in its own shared fixture clone and run the frozen
# round-88 counter against it. Writes <variant>.out / <variant>.err / <variant>.rc.
set -uo pipefail

S=/fast/scratch/hyaku/tameshi-r88/T88E2
FLEET=/home/vgpnk/Projects/shokunin
LANE=$FLEET/tameshi-shokunin
MEASURE=$LANE/.ufo/evidence/round-88/measure.py

mkdir -p "$S/fixtures" "$S/work" "$S/logs"
declare -A PIDS
for v in "$@"; do
  (
    D=$S/fixtures/$v
    rm -rf -- "$D"
    git clone -q --shared "$LANE" "$D" || { echo "clone failed" >&2; exit 90; }
    top=$(git -C "$D" rev-parse --show-toplevel) || exit 91
    [ "$top" = "$D" ] || { echo "toplevel mismatch: $top != $D" >&2; exit 92; }
    cp "$S/out/$v.sh" "$D/tools/mutate-and-run.sh"
    chmod +x "$D/tools/mutate-and-run.sh"
    git -C "$D" add tools/mutate-and-run.sh
    git -C "$D" -c user.name=ctl -c user.email=ctl@fixture.invalid \
      commit -q -m "T88E2 variant $v" || { echo "commit failed" >&2; exit 93; }
    REV=$(git -C "$D" rev-parse HEAD)
    W=$S/work/$v
    rm -rf -- "$W"; mkdir -p "$W"
    echo "variant=$v repo=$D rev=$REV runner_sha256=$(sha256sum "$D/tools/mutate-and-run.sh" | cut -d' ' -f1)" > "$S/logs/$v.meta"
    start=$(date +%s)
    TMPDIR=$S/work python3 -I "$MEASURE" --repo "$D" --rev "$REV" --fleet "$FLEET" --work "$W" \
      > "$S/logs/$v.out" 2> "$S/logs/$v.err"
    rc=$?
    end=$(date +%s)
    echo "rc=$rc elapsed=$((end-start))s" >> "$S/logs/$v.meta"
    echo "$rc" > "$S/logs/$v.rc"
  ) &
  PIDS[$v]=$!
done
fail=0
for v in "${!PIDS[@]}"; do
  wait "${PIDS[$v]}" || fail=1
done
for v in "$@"; do
  echo "===== $v ====="
  cat "$S/logs/$v.meta" 2>/dev/null
  tail -3 "$S/logs/$v.out" 2>/dev/null
  [ -s "$S/logs/$v.err" ] && { echo '--- stderr'; tail -5 "$S/logs/$v.err"; }
done
exit $fail
