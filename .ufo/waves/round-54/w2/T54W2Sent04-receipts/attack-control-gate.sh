#!/bin/bash
# T54W2Sent04 — control-gate abuse receipts for tameshi round 54.
# The lane and every lane object are READ-ONLY here: all git mutation happens inside
# `git clone --shared` copies under $TMP, and every git call names its -C target.
# Usage: bash attack-control-gate.sh   (prints every command's exact output)
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C1=99c3bc88d704566197783f66b211ee0a830e0330
FREEZE=441c26bec5e4c1cc31bc2a840f311cb8d1965259
TIP=097985c18b9a186c310bd35890b95b733cbb7f5b
REFRZ=19c7558
C=.ufo/evidence/round-54/control
E=.ufo/evidence/round-54
FROZEN="$E/contract.json $E/freeze.json $E/c1/measure.py $E/c1/lost-headings-at-base.json $E/c2/measure.py $E/no-harm.sh $E/deciding-run.sh $E/control/controls.sh .ufo/evidence/round-48/quality/coldread-precheck.sh .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-18/measure.py"
TMP=$(mktemp -d) || exit 2
trap 'rm -rf -- "$TMP"' EXIT
step() { printf '\n########## %s\n' "$*"; }
run()  { printf '+ %s\n' "$*"; "$@"; }
lane_run() { # lane_run LANE HYAKU_SCRATCH OUT REV FREEZE
  ( cd "$1" && HYAKU_SCRATCH="$2" bash .ufo/evidence/round-54/deciding-run.sh "$1" "$4" "$5" "$3" > "$3.log" 2>&1 )
  printf 'rc=%s\n' "$?"
  cat "$3.log"
  printf 'outdir-files=%s\n' "$(find "$3" -type f 2>/dev/null | wc -l)"
  printf 'scratch-root-exists=%s\n' "$(test -e "$2" && echo YES || echo NO)"
}
clone_at() { # clone_at DEST REV -> echoes lane path
  rm -rf "$1"; git clone --shared --quiet "$LANE" "$1/lane" >/dev/null 2>&1 \
    && git -C "$1/lane" checkout --detach --quiet "$2" >/dev/null 2>&1 || return 1
  local L=$1/lane
  [ "$(git -C "$L" rev-parse --show-toplevel)" = "$L" ] || return 1
  printf '%s' "$L"
}
add_receipts() { # add_receipts LANE MODE(real|empty) -> fixture commit with the four receipt paths
  local L=$1 mode=$2 empty=e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
  local b_a_out b_a_exit b_b_out b_b_exit idx
  b_a_out=$(git -C "$L" cat-file -p "$TIP:$C/controls-a.stdout" | git -C "$L" hash-object -w --stdin)
  b_a_exit=$(git -C "$L" cat-file -p "$TIP:$C/controls-a.exit" | git -C "$L" hash-object -w --stdin)
  b_b_out=$(printf 'FIXTURE controls-b.stdout: no committed bytes exist at any rev\n' | git -C "$L" hash-object -w --stdin)
  b_b_exit=$(printf '0\n' | git -C "$L" hash-object -w --stdin)
  [ "$mode" = empty ] && { b_a_out=$empty; b_a_exit=$empty; b_b_out=$empty; b_b_exit=$empty; }
  idx=$TMP/idx.$$; rm -f "$idx"
  GIT_INDEX_FILE=$idx git -C "$L" read-tree HEAD
  GIT_INDEX_FILE=$idx git -C "$L" update-index --add --cacheinfo 100644,$b_a_out,$C/controls-a.stdout
  GIT_INDEX_FILE=$idx git -C "$L" update-index --add --cacheinfo 100644,$b_a_exit,$C/controls-a.exit
  GIT_INDEX_FILE=$idx git -C "$L" update-index --add --cacheinfo 100644,$b_b_out,$C/controls-b.stdout
  GIT_INDEX_FILE=$idx git -C "$L" update-index --add --cacheinfo 100644,$b_b_exit,$C/controls-b.exit
  local tr; tr=$(GIT_INDEX_FILE=$idx git -C "$L" write-tree)
  local c; c=$(printf 'fixture: %s control receipts\n' "$mode" | \
    GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=f@l GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=f@l \
    git -C "$L" commit-tree "$tr" -p HEAD)
  git -C "$L" update-ref --no-deref HEAD "$c"
  git -C "$L" read-tree HEAD
  for f in controls-a.stdout controls-a.exit controls-b.stdout controls-b.exit; do
    if [ "$mode" = empty ]; then : > "$L/$C/$f"; else
      git -C "$L" cat-file -p "HEAD:$C/$f" > "$L/$C/$f"; fi
  done
}
status_of() { git -C "$1" status --porcelain | head -5; }

step "0. object census: does ANY commit carry the four pre-registered receipts?"
run git -C "$LANE" log --all --oneline -- "$C/controls-a.stdout" "$C/controls-b.stdout"
printf 'revs carrying controls-b.stdout: '
( for r in $(git -C "$LANE" rev-list --all); do
    git -C "$LANE" cat-file -e "$r:$C/controls-b.stdout" 2>/dev/null && echo "$r"; done ) | wc -l

step "1. C1 (no receipts at all), HEAD==REV, empty outdir: refuse, nothing executed"
L=$(clone_at "$TMP/c1" "$C1") || { echo CLONE-FAIL; exit 2; }
mkdir -p "$TMP/c1/out"; lane_run "$L" "$TMP/hk1" "$TMP/c1/out" "$C1" "$FREEZE"
printf 'clean-tree-after: [%s]\n' "$(status_of "$L")"

step "2. same state, invoked a second time: same refusal (no marker was ever written)"
lane_run "$L" "$TMP/hk2" "$TMP/c1/out" "$C1" "$FREEZE"

step "3. receipts present (a bytes from the tip, b fabricated), clean tree, witness file -> control gate OPENS"
add_receipts "$L" real
printf 'fixture HEAD=%s\n' "$(git -C "$L" rev-parse HEAD)"
for f in controls-a.stdout controls-a.exit controls-b.stdout controls-b.exit; do
  printf '  %s type=%s sha=%s\n' "$f" "$(git -C "$L" cat-file -t HEAD:$C/$f)" "$(git -C "$L" rev-parse "HEAD:$C/$f")"; done
: > "$L/FIXTURE_DIRTY"; mkdir -p "$TMP/c1/out3"
lane_run "$L" "$TMP/hk3" "$TMP/c1/out3" "$(git -C "$L" rev-parse HEAD)" "$FREEZE"
rm -f "$L/FIXTURE_DIRTY"; printf 'clean-tree-after: [%s]\n' "$(status_of "$L")"

step "4. the SAME invocation after a prior c1 start marker: second-invocation refusal"
mkdir -p "$TMP/c1/out4"; printf '2026-10-28T00:00:00Z\n' > "$TMP/c1/out4/c1.start"
lane_run "$L" "$TMP/hk4" "$TMP/c1/out4" "$(git -C "$L" rev-parse HEAD)" "$FREEZE"
printf 'outdir: %s\n' "$(ls -A "$TMP/c1/out4")"

step "5. and with the marker at c2.start: second-invocation c2 refusal"
mkdir -p "$TMP/c1/out5"; printf '2026-10-28T00:00:00Z\n' > "$TMP/c1/out5/c2.start"
lane_run "$L" "$TMP/hk5" "$TMP/c1/out5" "$(git -C "$L" rev-parse HEAD)" "$FREEZE"

step "6. existence-only receipt check: four ZERO-BYTE blobs satisfy the control gate"
L2=$(clone_at "$TMP/c1b" "$C1") || exit 2
add_receipts "$L2" empty
for f in controls-a.stdout controls-a.exit controls-b.stdout controls-b.exit; do
  printf '  %s type=%s size=%s\n' "$f" "$(git -C "$L2" cat-file -t "HEAD:$C/$f")" "$(git -C "$L2" cat-file -s "HEAD:$C/$f")"; done
: > "$L2/FIXTURE_DIRTY"; mkdir -p "$TMP/c1b/out"
lane_run "$L2" "$TMP/hk6" "$TMP/c1b/out" "$(git -C "$L2" rev-parse HEAD)" "$FREEZE"
rm -f "$L2/FIXTURE_DIRTY"

step "6b. non-blob receipts: four TREE objects at the receipt paths also satisfy the gate"
L2b=$(clone_at "$TMP/c1c" "$C1") || exit 2
empty_tree=4b825dc642cb6eb9a060e54bf8d69288fbee4904
idx=$TMP/idx.t; rm -f "$idx"
GIT_INDEX_FILE=$idx git -C "$L2b" read-tree HEAD
for f in controls-a.stdout controls-a.exit controls-b.stdout controls-b.exit; do
  GIT_INDEX_FILE=$idx git -C "$L2b" update-index --add --cacheinfo 100644,$empty_tree,$C/$f; done
tr=$(GIT_INDEX_FILE=$idx git -C "$L2b" write-tree)
c=$(printf 'fixture: tree objects at the receipt paths\n' | \
  GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=f@l GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=f@l \
  git -C "$L2b" commit-tree "$tr" -p HEAD)
git -C "$L2b" update-ref --no-deref HEAD "$c"; git -C "$L2b" read-tree HEAD
for f in controls-a.stdout controls-a.exit controls-b.stdout controls-b.exit; do
  printf '  %s type=%s cat-file-exit=' "$f" "$(git -C "$L2b" cat-file -t "HEAD:$C/$f")"
  git -C "$L2b" cat-file -e "HEAD:$C/$f"; echo $?; done
mkdir -p "$TMP/c1c/out"
lane_run "$L2b" "$TMP/hk6b" "$TMP/c1c/out" "$(git -C "$L2b" rev-parse HEAD)" "$FREEZE"

step "7. shipped tip (097985c), FREEZE=the round's recorded freeze 441c26be: stale manifest, then refusal"
L3=$(clone_at "$TMP/tip" "$TIP") || exit 2
mkdir -p "$TMP/tip/out"; lane_run "$L3" "$TMP/hk7" "$TMP/tip/out" "$TIP" "$FREEZE"

step "8. shipped tip as its own FREEZE: the phase-A receipt predates it"
mkdir -p "$TMP/tip/out8"; lane_run "$L3" "$TMP/hk8" "$TMP/tip/out8" "$TIP" "$TIP"

step "9. the script's own frozen-diff predicate, over the 11 frozen paths"
for pair in "441c26bec5e4 $C1" "441c26bec5e4 $TIP" "$REFRZ $TIP" "$TIP $TIP"; do
  set -- $pair; git -C "$LANE" diff --quiet "$1" "$2" -- $FROZEN; rc=$?
  printf 'git diff --quiet %s..%s -> rc=%s (FROZEN_UNCHANGED=%s)\n' "$1" "$2" "$rc" "$([ "$rc" = 0 ] && echo 1 || echo 0)"
done
run git -C "$LANE" diff --stat 441c26bec5e4 "$TIP" -- $FROZEN
