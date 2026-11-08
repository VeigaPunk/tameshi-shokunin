#!/usr/bin/env bash
set -u
S=/fast/scratch/hyaku/tameshi-r93/R93C1
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
NOTE=corpus/knowledge/mutation-case-fleet-sources-census.md

run_one () {
  local name="$1"
  local dir="$S/clone-$name"
  rm -rf "$dir"; mkdir -p "$dir"
  git clone -q --shared "$LANE" "$dir" 2>"$S/$name-clone.err"
  git -C "$dir" checkout -q --detach "$REV" 2>>"$S/$name-clone.err"
  local top; top="$(git -C "$dir" rev-parse --show-toplevel)"
  if [ "$top" != "$dir" ]; then echo "$name TOPLEVEL-MISMATCH:$top" ; fi
  # edits applied by python snippet per attack
  python3 "$S/edit-$name.py" "$dir/$NOTE"
  git -C "$dir" add -A
  GIT_AUTHOR_NAME="ctl" GIT_AUTHOR_EMAIL="ctl@fixture.invalid" GIT_COMMITTER_NAME="ctl" GIT_COMMITTER_EMAIL="ctl@fixture.invalid" git -C "$dir" commit -q -m "R93C1 attack $name"
  local got; got="$(git -C "$dir" rev-parse HEAD)"
  # verify the amended note is what we committed
  git -C "$dir" show --stat HEAD | head -5
  mkdir -p "$S/work-$name"
  python3 -I "$LANE/.ufo/evidence/round-93/c1/measure-v93.py" --repo "$dir" --rev "$got" --work "$S/work-$name" > "$S/$name.out" 2>&1
  local rc=$?
  echo "$name exit=$rc rev=$got" >> "$S/results.tsv"
}
export -f run_one
echo -e "$(date +%H:%M:%S) A1-A3" 
run_one A1 &
run_one A2 &
run_one A3 &
wait
echo -e "$(date +%H:%M:%S) A4-A7"
run_one A4 &
run_one A5 &
run_one A6 &
run_one A7 &
wait
echo -e "$(date +%H:%M:%S) B1-B3"
run_one B1 &
run_one B2 &
run_one B3 &
wait
echo -e "$(date +%H:%M:%S) B4-B6"
run_one B4 &
run_one B5 &
run_one B6 &
wait
echo DONE
