#!/bin/bash
# Round-55 critic attack driver (scratch only). Builds fixtures from a --shared clone of the lane
# at the freeze commit, then runs the FROZEN deciding-run.sh unmodified against them.
set -u
S=/fast/scratch/hyaku/tameshi-r55/T55W1CritGate
LN=/home/vgpnk/Projects/shokunin/tameshi-shokunin
DR=$LN/.ufo/evidence/round-55/deciding-run.sh
FREEZE=631cd6455e58dce969310b4c0466c3383d9f5108
E=.ufo/evidence/round-55
mk () {  # mk DIR
  rm -rf "$1"
  git clone --shared --quiet "$LN" "$1" || return 1
  git -C "$1" -c advice.detachedHead=false checkout --quiet --detach "$FREEZE" || return 1
  [ "$(git -C "$1" rev-parse --show-toplevel)" = "$1" ] || { echo "TOPLEVEL-BAD $1"; return 1; }
}
commit () {  # commit DIR MSG
  git -C "$1" add -A >/dev/null
  git -C "$1" -c user.name=crit -c user.email=crit@invalid commit --quiet -m "$2"
}
run () {  # run TAG LANE REV FREEZE OUT [TIMEOUT]
  local tag=$1 lane=$2 rev=$3 frz=$4 out=$5 t=${6:-90}
  mkdir -p "$out"
  HYAKU_SCRATCH=$S/hs-$tag timeout "$t" bash "$DR" "$lane" "$rev" "$frz" "$out" \
      > "$S/receipts/$tag.out" 2>&1
  echo $? > "$S/receipts/$tag.rc"
  echo "== $tag rc=$(cat "$S/receipts/$tag.rc")"
  grep -E 'DECIDING_REFUSED|FREEZE_INTEGRITY|FROZEN_UNCHANGED|C[12]_R55_PASS|DECIDING_RUN_EXIT' "$S/receipts/$tag.out" || true
}
# a receipt file with the pre-registered verdict line the gate greps for
receipt () {  # receipt PATH PHASE
  printf 'CTL CTL_0_c1 C1_R55_PASS=false\nCTL CTL_0_c2 C2_R55_PASS=false\nCONTROLS_%s: 4/4 as pre-registered\n' "$2" > "$1"
}
