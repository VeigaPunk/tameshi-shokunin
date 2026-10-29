#!/bin/bash
# Round-57 controls. Usage: controls.sh LANE BASE REV OUTDIR
#
# ONE GENERATION. Controls are RECOMPUTED, never READ (round-56 lesson, Attempt 4, first
# Mistakes row; R56.5): round 56's C2 arm 5 read the round's committed controls-a/b.stdout, so
# the first controls run could never print CONTROLS_B 2/2 and the round needed a bootstrap
# generation plus a second one. Nothing here reads a committed receipt of this round. Every
# control is built from lane git objects at BASE or REV in a fresh `git clone --shared` under
# scratch, mutated by the generators in .ufo/evidence/round-57/control/ (gen_ledger.py,
# gen_registry.py), committed there under a fixture identity, and scored by the counter that
# the clone itself carries. REV is the content-final revision, chosen before this script runs;
# this round's control receipts are committed in a LATER commit, so REV cannot contain them -
# the script refuses (exit 2, CTL_GENERATION_ERROR) when REV already carries a controls receipt
# or an `after/` receipt, because a positive control scored there could be reading one.
#
# Phase A (all but POS): every control must reach its pre-registered verdict (false).
#   C1: CTL_0_c1   BASE tree with the round-57 instruments overlaid from REV (do-nothing)
#       CTL_SKIP_c1  REV; 51 new rows `declined`, 45-char reason: the declined cap must fire
#       CTL_FAB_c1   REV; new rows `fixed` with an invented excerpt
#       CTL_OPEN_c1  REV; new rows `open`, SCORECARD's newest Planned paragraph names none
#   C2: CTL_0_c2   BASE tree with the instruments overlaid (do-nothing)
#       CTL_SKIP_c2  REV; three gate rows whose expect.exit is rotated (wrong)
#       CTL_FAB_c2   REV; gate rows whose fixture receipts were never written
#       CTL_MUT_c2   REV; rows that hold but never run the drift branch (no mutant but M3 can
#                    turn a row red; any valid exit-2 row runs M3's branch)
# Phase B (POS): CTL_POS_c1 / CTL_POS_c2 are scored AT REV, the revision they certify, in a
#   fresh clone of REV (the round-54 lesson: a positive control scored at the freeze certified
#   nothing).
# Why the do-nothing control is not `--rev BASE` against the lane: the round-57 frozen
# statement set and counters are installed after BASE, so a literal BASE read ends in a setup
# error (exit 2, no verdict token) instead of the counter's own false; BASE + the instruments
# is the do-nothing tree the counters can actually grade.
#
# Every CTL line names the revision the counter printed. A revision that exists only inside a
# scratch clone (the fixtures commit there) is relabelled `clone_rev=` so the receipt gate,
# which binds `rev=` tokens to lane revisions, never reads it as a lane revision.
# CTL_MISMATCH means the counter did not reach the pre-registered boolean: the round stops.
# The committed receipts carry a `.sha256` sibling (the L1 computes it).
# Per-control full counter output (the --explain lines) goes to OUTDIR/ctl-<NAME>.full.
# Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r57/controls, removed on exit.
set -u
[ $# -eq 4 ] || { echo "usage: controls.sh LANE BASE REV OUTDIR"; exit 2; }
LANE=$1; BASE_IN=$2; REV_IN=$3; OUT=$4
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
case "$OUT" in /*) ;; *) echo "OUTDIR must be absolute"; exit 2;; esac
for v in $(env | grep -oE '^GIT_[A-Za-z_]+'); do unset "$v"; done
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 PYTHONDONTWRITEBYTECODE=1
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r57/controls
E=.ufo/evidence/round-57
G=(-c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false)
BASE=$(git -C "$LANE" rev-parse --verify --quiet "$BASE_IN^{commit}") || { echo "BASE unresolvable: $BASE_IN"; exit 2; }
REV=$(git -C "$LANE" rev-parse --verify --quiet "$REV_IN^{commit}") || { echo "REV unresolvable: $REV_IN"; exit 2; }
git -C "$LANE" merge-base --is-ancestor "$BASE" "$REV" || { echo "BASE is not an ancestor of REV"; exit 2; }
if git -C "$LANE" ls-tree -r --name-only "$REV" | grep -qE "^$E/(control/controls-|after/)"; then
  echo "CTL_GENERATION_ERROR: REV $REV already carries a round-57 controls/after receipt"; exit 2
fi
rm -rf "$SCR"; mkdir -p "$SCR" "$OUT" || exit 2
trap 'rm -rf -- "$SCR"' EXIT; export TMPDIR="$SCR"
C1="$E/c1/measure.py"; C2="$E/c2/measure.py"
A_ok=0; A_n=0; B_ok=0; B_n=0

emit() { # emit NAME EXPECTED ACTUAL VERDICT_LINE COUNTER_EXIT
  local name=$1 want=$2 got=$3 line=$4 ec=$5
  # A counter line that names a revision nothing in the lane resolves is
  # relabelled clone_rev= here: the receipt gate binds `rev=` tokens to lane
  # revisions, and a clone-local commit SHA (these fixtures commit inside
  # scratch clones) must not masquerade as a lane revision.
  local rest=$line out=
  while [[ $rest =~ (^|.*[^_[:alnum:]])rev=([0-9a-fA-F]+)(.*) ]]; do
    local sha=${BASH_REMATCH[2]}
    if git -C "$LANE" rev-parse --verify --quiet "$sha^{commit}" >/dev/null 2>&1; then
      out="rev=$sha${BASH_REMATCH[3]}$out"
    else
      out="clone_rev=$sha${BASH_REMATCH[3]}$out"
    fi
    rest=${BASH_REMATCH[1]}
  done
  line=$rest$out
  echo "CTL $name $line"
  if [ "$want" = "$got" ]; then echo "CTL_MATCH $name expected=$want actual=$got counter_exit=$ec"; RES=1
  else echo "CTL_MISMATCH $name expected=$want actual=$got counter_exit=$ec"; RES=0; fi
}

verdict_of() { grep -oE 'C[12]_R57_PASS=(true|false)' | tail -1 | cut -d= -f2; }

clone_at() { # clone_at DIR REV
  git -c advice.detachedHead=false clone --quiet --shared "$LANE" "$1" || return 2
  git -C "$1" -c advice.detachedHead=false checkout --quiet --detach "$2" || return 2
  [ "$(git -C "$1" rev-parse --show-toplevel)" = "$(cd "$1" && pwd -P)" ] || return 2
}

commit_all() { # commit_all DIR MESSAGE
  [ "$(git -C "$1" rev-parse --show-toplevel)" = "$(cd "$1" && pwd -P)" ] || return 2
  git -C "$1" "${G[@]}" add -A >/dev/null || return 2
  git -C "$1" "${G[@]}" commit --quiet --no-verify -m "$2" >/dev/null || return 2
}

score() { # score NAME COUNTER_REL DIR -> sets L V EC (counter run from DIR's own tree at DIR's HEAD)
  local name=$1 counter=$2 d=$3 work=$SCR/w-$1
  mkdir -p "$work"
  python3 "$d/$counter" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$work" --explain \
    > "$OUT/ctl-$name.full" 2>&1
  EC=$?
  L=$(tail -n 1 "$OUT/ctl-$name.full"); V=$(echo "$L" | verdict_of)
}

phase_a() { # phase_a NAME COUNTER_REL DIR
  A_n=$((A_n+1)); score "$1" "$2" "$3"; emit "$1" false "$V" "$L" "$EC"; A_ok=$((A_ok+RES))
}

echo "# controls: one generation; recomputed from lane git objects, no committed receipt read"
echo "# LANE=$LANE BASE=$BASE REV=$REV"
echo "# phase A: do-nothing and mutation controls (expected false)"

# CTL_0: BASE tree + the instruments from REV (the frozen set and counters do not exist at BASE)
D=$SCR/ctl0; clone_at "$D" "$BASE" || exit 2
OV=("$E/c1" "$E/c2")
git -C "$LANE" cat-file -e "$REV:$E/contract.json" 2>/dev/null && OV+=("$E/contract.json")
git -C "$D" checkout --quiet "$REV" -- "${OV[@]}" || { echo "overlay failed"; exit 2; }
commit_all "$D" 'control: BASE plus round-57 instruments' || exit 2
phase_a CTL_0_c1 "$C1" "$D"
phase_a CTL_0_c2 "$C2" "$D"

gen_c1() { # gen_c1 NAME MODE
  D=$SCR/$1; clone_at "$D" "$REV" || exit 2
  local g; g=$(python3 "$D/$E/control/gen_ledger.py" --clone "$D" --mode "$2") || { echo "gen_ledger failed ($1)"; exit 2; }
  echo "CTL_GEN $1 $g"
  commit_all "$D" "control: $1 ledger" || exit 2
}
gen_c2() { # gen_c2 NAME MODE
  D=$SCR/$1; clone_at "$D" "$REV" || exit 2
  local g; g=$(python3 "$D/$E/control/gen_registry.py" --clone "$D" --base "$BASE" --rev "$REV" --mode "$2") || { echo "gen_registry failed ($1)"; exit 2; }
  echo "CTL_GEN $1 $g"
  commit_all "$D" "control: $1 registry" || exit 2
}

gen_c1 CTL_SKIP_c1 skip; phase_a CTL_SKIP_c1 "$C1" "$D"
gen_c1 CTL_FAB_c1 fab;   phase_a CTL_FAB_c1 "$C1" "$D"
gen_c1 CTL_OPEN_c1 open; phase_a CTL_OPEN_c1 "$C1" "$D"
gen_c2 CTL_SKIP_c2 skip; phase_a CTL_SKIP_c2 "$C2" "$D"
gen_c2 CTL_FAB_c2 fab;   phase_a CTL_FAB_c2 "$C2" "$D"
gen_c2 CTL_MUT_c2 mut;   phase_a CTL_MUT_c2 "$C2" "$D"

echo "CONTROLS_A: $A_ok/$A_n as pre-registered"

echo "# phase B: the positive controls scored at the revision they certify (REV=$REV)"
D=$SCR/pos; clone_at "$D" "$REV" || exit 2
[ "$(git -C "$D" rev-parse HEAD)" = "$REV" ] || { echo "positive clone is not at REV"; exit 2; }
B_n=$((B_n+1)); score CTL_POS_c1 "$C1" "$D"; emit CTL_POS_c1 true "$V" "$L" "$EC"; B_ok=$((B_ok+RES))
B_n=$((B_n+1)); score CTL_POS_c2 "$C2" "$D"; emit CTL_POS_c2 true "$V" "$L" "$EC"; B_ok=$((B_ok+RES))
echo "CONTROLS_B: $B_ok/$B_n as pre-registered"
