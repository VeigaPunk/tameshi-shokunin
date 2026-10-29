#!/usr/bin/env bash
# Production-impact probe: does a mutant change the counter's REAL verdict at C0?
# Builds one clone at C0 + the round-57 evidence dir (like dry-c2.sh), then runs
# the pristine counter and each mutant against that rev, comparing verdict lines.
set -u
S=/fast/scratch/hyaku/tameshi-r57/T57W2MutC2Counter
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
P="$S/probe"
mkdir -p "$P" "$S/tmp"
rm -rf "$P/clone"
git clone -q --shared "$LANE" "$P/clone" || exit 2
git -C "$P/clone" rev-parse --show-toplevel >/dev/null || exit 2
git -C "$P/clone" checkout -q --detach ca75c2674645ab6bdadeecb8584007c74342bfa9 || exit 2
rm -rf "$P/clone/.ufo/evidence/round-57"
cp -r "$LANE/.ufo/evidence/round-57" "$P/clone/.ufo/evidence/round-57"
git -C "$P/clone" add -A
git -C "$P/clone" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m probe
REV=$(git -C "$P/clone" rev-parse HEAD)
echo "PROBE_REV=$REV" | tee "$P/probe-rev.txt"

run_one() {
  id="$1"
  w="$P/w/$id"; rm -rf "$w"; mkdir -p "$w/work"
  ( cd "$w" && TMPDIR="$S/tmp" python3 "$S/mut/$id/measure.py" --lane "$P/clone" --rev "$REV" \
      --work "$w/work" --explain >"$P/$id.stdout" 2>"$P/$id.stderr"; echo $? >"$P/$id.exit" )
}
export -f run_one
export S LANE P REV
printf '%s\n' BASELINE M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M11 M12 | xargs -P 4 -I{} bash -c 'run_one "$@"' _ {}
echo PROBE_DONE
for id in BASELINE M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M11 M12; do
  printf '%-9s exit=%-3s %s\n' "$id" "$(cat "$P/$id.exit" 2>/dev/null)" \
    "$(grep -h '^C2_R57:' "$P/$id.stdout" 2>/dev/null | tail -1)"
done
