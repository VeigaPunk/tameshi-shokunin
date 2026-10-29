#!/usr/bin/env bash
# Run the counter's own selftest for BASELINE + each mutant, 4 at a time.
# Never touches the lane repo (read-only git via the counter's own clone/show).
set -u
S=/fast/scratch/hyaku/tameshi-r57/T57W2MutC2Counter
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=ca75c2674645ab6bdadeecb8584007c74342bfa9
MUT="$S/mut"
OUT="$S/out"
mkdir -p "$OUT" "$S/tmp"

run_one() {
  local id="$1"
  local dir="$MUT/$id"
  local w="$S/work/$id"
  rm -rf "$w"; mkdir -p "$w"
  ( cd "$w" && TMPDIR="$S/tmp" python3 "$dir/measure.py" --selftest --lane "$LANE" --rev "$REV" \
      >"$OUT/$id.stdout" 2>"$OUT/$id.stderr"; echo $? > "$OUT/$id.exit" )
}

export -f run_one
export S LANE REV MUT OUT

LIST=$(printf '%s\n' BASELINE M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M11 M12)
echo "$LIST" | xargs -P 4 -I{} bash -c 'run_one "$@"' _ {}
echo "ALL DONE"
for id in $LIST; do
  printf '%-9s exit=%s ' "$id" "$(cat "$OUT/$id.exit" 2>/dev/null)"
  grep -h 'C2_R57_SELFTEST' "$OUT/$id.stdout" 2>/dev/null | tail -1
done
