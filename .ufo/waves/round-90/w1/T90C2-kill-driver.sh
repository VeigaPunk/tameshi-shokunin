#!/usr/bin/env bash
# T90C2 — attack R90-C2 under the frozen plan's kill rule (a).
#
# Builds committed states in scratch clones of the lane at the freeze rev and runs the
# frozen C2 counter on each. Every variant is two commits at most: `prep` (the frozen
# c2/fixes.py --variant pos, or nothing) then `attack` (one edit), so the attack edit
# is a one-commit diff against the honest construct.
#   honest         fixes only (control; expected C2_R90_PASS=true)
#   forge-registry fixes + registry.json row argv prints the needle instead of running
#                  the witness (routed item 4)
#   wrong-count    fixes + the appended correction states the routed defect's own wrong
#                  count ("four") while the token survives as a rejected quote (item 2)
#   tool-neuter    no fixes + shims in tools/defect-bind.py and tools/registry-check.py
#                  (additional, counter-authority class; none of items 1-4 repaired)
#
# Usage: bash T90C2-kill-driver.sh OUTDIR
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=3485ceb08df394edf5fbe26bd09b03985a04fba1
COUNTER=$LANE/.ufo/evidence/round-90/c2/measure-c2.sh
FIXES=$LANE/.ufo/evidence/round-90/c2/fixes.py
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=${1:?outdir}
SROOT=/fast/scratch/hyaku/tameshi-r90/T90C2
mkdir -p "$SROOT" "$OUT" || exit 2
S=$(mktemp -d -p "$SROOT" run.XXXXXX) || exit 2
trap 'rm -rf -- "$S"' EXIT

build() { # build NAME PREP(fixes|none) [MUTATOR]
  local name=$1 prep=$2 mut=${3:-}
  local repo=$S/$name/repo work=$S/$name/work rev rc
  mkdir -p "$work" || return 2
  git clone -q --shared "$LANE" "$repo" || return 2
  [ "$(git -C "$repo" rev-parse --show-toplevel)" = "$repo" ] \
    || { echo "$name C2_SETUP toplevel"; return 2; }
  git -C "$repo" checkout -q -B attack "$BASE" || return 2
  if [ "$prep" = fixes ]; then
    python3 -I "$FIXES" --target "$repo" || return 2
    git -C "$repo" add -A || return 2
    git -C "$repo" -c user.name=ctl -c user.email=ctl@fixture.invalid \
      commit -qm "T90C2 $name prep ($prep)" || return 2
  fi
  if [ -n "$mut" ]; then
    python3 -I "$mut" "$repo" || return 2
    git -C "$repo" add -A || return 2
    git -C "$repo" -c user.name=ctl -c user.email=ctl@fixture.invalid \
      commit -qm "T90C2 $name attack" || return 2
  fi
  rev=$(git -C "$repo" rev-parse HEAD) || return 2
  echo "== $name rev=$rev parent=$(git -C "$repo" rev-parse HEAD^)"
  echo "-- log:"; git -C "$repo" log --oneline -3
  echo "-- attack-commit stat:"; git -C "$repo" show --format='%h %s' --stat HEAD | head -14
  if git -C "$repo" diff --quiet "$BASE" -- tools/defect-bind.py tools/registry-check.py; then
    echo "-- checker-tools-unmodified-since-base=yes"
  else
    echo "-- checker-tools-unmodified-since-base=no"
  fi
  bash "$COUNTER" "$repo" "$rev" "$work" 2>&1 | tee "$OUT/T90C2-$name.out"
  rc=${PIPESTATUS[0]}
  echo "exit=$rc" | tee -a "$OUT/T90C2-$name.out"
  return 0
}

{
  echo "driver out=$OUT lane=$LANE base=$BASE"
  echo "counter-sha256=$(sha256sum "$COUNTER" | cut -d' ' -f1)"
  echo "fixes-sha256=$(sha256sum "$FIXES" | cut -d' ' -f1)"
  build honest fixes || exit 2
  build forge-registry fixes "$HERE/T90C2-forge-registry.py" || exit 2
  build wrong-count fixes "$HERE/T90C2-wrong-count.py" || exit 2
  build tool-neuter none "$HERE/T90C2-tool-neuter.py" || exit 2
  echo "DONE"
} 2>&1 | tee "$OUT/T90C2-driver.log"
