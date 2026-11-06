#!/usr/bin/env bash
# Round-90 C2 controls. Each fixture is a --shared scratch clone of the lane at INSTR
# (the pre-freeze instrument commit), the fixes applied by fixes.py with one variant,
# committed under a fixture identity inside the clone only (toplevel asserted first).
#   controls-c2.sh LANE SCRATCH
set -u
LANE=$(realpath -- "${1:?lane}"); SC=${2:?scratch}
INSTR=a90218cc06665ddaa76a0e2f26b9ad7df506d1ec
BASE=4e1c10e0cfcc1e7533f1fc71a1b3b615aa60a7e0
M="$LANE/.ufo/evidence/round-90/c2/measure-c2.sh"
FX="$LANE/.ufo/evidence/round-90/c2/fixes.py"
OUT="$LANE/.ufo/evidence/round-90/pre-freeze/controls"
mkdir -p "$OUT" "$SC"
real() { # name rev msrc
  local w="$SC/c2-$1"; rm -rf -- "$w"; mkdir -p "$w"
  { echo "control=$1 rev=$2 manifest_src=$3"; bash "$M" "$LANE" "$2" "$w" "$3"; echo "exit=$?"; } > "$OUT/$1.out" 2>&1
  rm -rf -- "$w"
}
fixture() { # name variant
  local d="$SC/c2fx-$1"; rm -rf -- "$d"; mkdir -p "$d"
  local r="$d/repo"
  git clone -q --shared --no-checkout "$LANE" "$r" || exit 3
  [ "$(git -C "$r" rev-parse --show-toplevel)" = "$(realpath -- "$r")" ] || { echo "toplevel mismatch $1" >&2; exit 3; }
  git -C "$r" checkout -q --detach "$INSTR" || exit 3
  (cd "$r" && TMPDIR="$d" python3 -I "$FX" --target . --variant "$2") > "$d/fixes.log" 2>&1
  git -C "$r" add -A && git -C "$r" -c user.name=r90-fixture -c user.email=r90-fixture@invalid commit -q -m "r90 c2 control $1" || exit 3
  local rev; rev=$(git -C "$r" rev-parse HEAD)
  mkdir -p "$d/w"
  { echo "control=$1 variant=$2 clone_rev=$rev parent=$INSTR"; cat "$d/fixes.log"; bash "$M" "$r" "$rev" "$d/w" "$rev"; echo "exit=$?"; } > "$OUT/$1.out" 2>&1
  rm -rf -- "$d"
}
real C2-nowork-base "$BASE" "$INSTR"
real C2-nowork-instr "$INSTR" "$INSTR"
fixture C2-pos pos
fixture C2-wrongsection wrongsection
fixture C2-bogus-registry bogusregistry
for f in C2-nowork-base C2-nowork-instr C2-pos C2-wrongsection C2-bogus-registry; do
  printf '%s: ' "$f"; grep -E '^(C2_SUMMARY|C2_SETUP|exit=)' "$OUT/$f.out" | tr '\n' ' '; echo
done
