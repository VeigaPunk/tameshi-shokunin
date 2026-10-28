#!/bin/bash
# Build one fixture clone at C0 with a fabricated round-55 control receipt set, and
# (optionally) an empty OUTDIR. Usage: build-fixture.sh NAME KIND S
#   KIND = stale-rev | no-tally | zero-zero | failed-tally | symlink | worktree
# Prints: FIXTURE=<dir> REV=<commit> OUT=<dir>
# Every git call names -C "$D"; the toplevel is asserted before the commit.
set -eu
NAME=$1; KIND=$2; S=$3
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
STALE=0a2010acd1e9
D=$S/fix-$NAME
rm -rf -- "$D"
git clone --shared --quiet "$LANE" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "not a standalone repo: $D"; exit 9; }
git -C "$D" -c advice.detachedHead=false checkout --quiet "$C0"
CTL=$D/.ufo/evidence/round-55/control
mkdir -p "$CTL"

# Phase-B receipt shape, copied from the real controls.sh echo: each CTL line
# carries the counter verdict line, whose `rev=` is the clone's HEAD in score().
ctl_b_line () { printf 'CTL %s C1_R55: rev=%s classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true\n' "$1" "$2"; }

case "$KIND" in
stale-rev)
  # A phase-B receipt produced at BASE (0a2010acd1e9), i.e. before any round-55 work,
  # pasted in as the phase-B receipt for the revision under test.
  { ctl_b_line CTL_POS_c1 "$STALE"; ctl_b_line CTL_POS_c2 "$STALE";
    ctl_b_line CTL_BREAK_c2 "$STALE"; ctl_b_line CTL_SKIP_c1 "$STALE";
    ctl_b_line CTL_FAB_c1 "$STALE"; echo "CONTROLS_B: 5/5 as pre-registered"; } > "$CTL/controls-b.stdout"
  { ctl_b_line CTL_0_c1 "$STALE"; ctl_b_line CTL_0_c2 "$STALE";
    ctl_b_line CTL_SKIP_c2 "$STALE"; echo "CONTROLS_A: 3/3 as pre-registered"; } > "$CTL/controls-a.stdout"
  ;;
no-tally)
  # Control for the corroborating arm: same bytes without the tally line.
  { ctl_b_line CTL_POS_c1 "$STALE"; ctl_b_line CTL_POS_c2 "$STALE"; } > "$CTL/controls-b.stdout"
  { ctl_b_line CTL_0_c1 "$STALE"; } > "$CTL/controls-a.stdout"
  ;;
zero-zero)
  # Zero controls pre-registered.
  echo "CONTROLS_A: 0/0 as pre-registered" > "$CTL/controls-a.stdout"
  echo "CONTROLS_B: 0/0 as pre-registered" > "$CTL/controls-b.stdout"
  ;;
failed-tally)
  # A phase run that failed: controls.sh prints the tally before `exit 1`, and this
  # tally is 3/5 -- numerator != denominator -- with the exit receipt carrying 1.
  { ctl_b_line CTL_POS_c1 "$STALE"; echo "CTL_MISMATCH CTL_POS_c2 expected=true actual=false"; echo "CONTROLS_B: 3/5 as pre-registered"; } > "$CTL/controls-b.stdout"
  { ctl_b_line CTL_0_c1 "$STALE"; echo "CONTROLS_A: 1/2 as pre-registered"; } > "$CTL/controls-a.stdout"
  echo 1 > "$CTL/controls-a.exit"; echo 1 > "$CTL/controls-b.exit"
  ;;
symlink)
  # A symlink blob (mode 120000) is a blob to `git cat-file -t`, and the gate's grep
  # follows it in the worktree.
  printf 'CONTROLS_A: 5/5 as pre-registered\nCONTROLS_B: 5/5 as pre-registered\n' > "$S/outside-$NAME.txt"
  ln -s "$S/outside-$NAME.txt" "$CTL/controls-a.stdout"
  ln -s "$S/outside-$NAME.txt" "$CTL/controls-b.stdout"
  ;;
worktree)
  # The blob at REV carries no tally line; the worktree does, and the index bit makes
  # `git status --porcelain` blind to the difference.
  echo "CONTROLS_A: not scored (phase A interrupted)" > "$CTL/controls-a.stdout"
  echo "CONTROLS_B: not scored (phase B interrupted)" > "$CTL/controls-b.stdout"
  ;;
*) echo "unknown KIND $KIND"; exit 2;;
esac
echo 0 > "$CTL/controls-a.exit"; echo 0 > "$CTL/controls-b.exit"
[ "$KIND" = failed-tally ] || { echo 0 > "$CTL/controls-a.exit"; echo 0 > "$CTL/controls-b.exit"; }

git -C "$D" add -A
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git -C "$D" -c user.name=fixture -c user.email=fixture@invalid \
  commit --quiet -m "fixture $NAME: control receipts ($KIND)"
REV=$(git -C "$D" rev-parse HEAD)
git -C "$D" status --porcelain > "$S/fix-$NAME.status"

if [ "$KIND" = worktree ]; then
  for f in controls-a.stdout controls-b.stdout; do
    git -C "$D" update-index --assume-unchanged ".ufo/evidence/round-55/control/$f"
  done
  printf 'CONTROLS_A: 5/5 as pre-registered\n' > "$CTL/controls-a.stdout"
  printf 'CONTROLS_B: 5/5 as pre-registered\n' > "$CTL/controls-b.stdout"
fi
OUT=$D/.ufo/evidence/round-55/after
mkdir -p "$OUT"
echo "FIXTURE=$D REV=$REV OUT=$OUT"
