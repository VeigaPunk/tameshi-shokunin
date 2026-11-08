#!/usr/bin/env bash
# R93SN1 probe 7: empty --rev, unwritable outdir, and an isolated GIT_DIR guard bypass.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe7.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
BASE=4a7e259b407d582d2010197f32d7524d6bed5370
probe() { printf 'PROBE %-46s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "I1 counter: --rev '' (empty) - refused, or does it read the INDEX?"
mkdir -p "$S/wI1"
python3 -I "$MEAS" --repo "$LANE" --rev "" --work "$S/wI1" >"$S/i1.log" 2>&1
probe "I1.rc" "$?"
probe "I1.first-line" "$(head -1 "$S/i1.log")"
probe "I1.setup-or-rows" "$(grep -c '^C1_ROW' "$S/i1.log")"

sec "I2 disposition checker: --rev '' "
python3 -I "$LANE/tools/conjunct-disposition.py" --lane "$LANE" --rev "" >"$S/i2.log" 2>&1
probe "I2.rc" "$?"
probe "I2.output" "$(tail -1 "$S/i2.log")"

sec "I3 driver: --rev '' "
mkdir -p "$S/wI3" "$S/oI3"
python3 -I "$CTRL" --lane "$LANE" --rev "" --base "$BASE" --work "$S/wI3" --outdir "$S/oI3" --only nowork-base --jobs 1 >"$S/i3.log" 2>&1
probe "I3.rc" "$?"
probe "I3.tail" "$(tail -2 "$S/i3.log" | tr '\n' '|')"

sec "I4 driver: unwritable --outdir"
mkdir -p "$S/oI4" "$S/wI4"
chmod 500 "$S/oI4"
python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" --work "$S/wI4" --outdir "$S/oI4" --only nowork-base --jobs 1 >"$S/i4.log" 2>&1
probe "I4.rc" "$?"
probe "I4.last-line" "$(tail -1 "$S/i4.log")"
probe "I4.traceback" "$(grep -c 'Traceback' "$S/i4.log")"
chmod 700 "$S/oI4"

sec "I5 isolated GIT_DIR bypass of the driver's toplevel guard"
# a scratch repo standing in for 'some other repo' that GIT_DIR points at
git init -q "$S/other"
git -C "$S/other" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
# a scratch lane clone the driver will clone FROM
git clone -q --shared --no-checkout "$LANE" "$S/laneI" 2>/dev/null
git -C "$S/laneI" checkout -q --detach "$REV" 2>/dev/null
mkdir -p "$S/wI5"
( cd "$S" && GIT_DIR="$S/other/.git" python3 -I "$CTRL" --lane "$S/laneI" --rev "$REV" \
   --base "$BASE" --work "$S/wI5" --outdir "$S/oI5" --only pos-real --jobs 1 ) >"$S/i5.log" 2>&1
probe "I5.driver-rc" "$?"
probe "I5.tail" "$(tail -2 "$S/i5.log" | tr '\n' '|')"
probe "I5.other-repo-commits" "$(git -C "$S/other" log --oneline --all 2>/dev/null | wc -l)"
probe "I5.other-has-r93-control-commit" "$(git -C "$S/other" log --oneline --all 2>/dev/null | grep -c 'r93 control')"
probe "I5.other-worktree-files" "$(ls -A "$S/other" | tr '\n' ' ')"
probe "I5.clone-in-work-has-commit" "$(find "$S/wI5" -maxdepth 3 -name '.git' -exec git -C {} rev-parse HEAD \; 2>/dev/null | tr '\n' ' ')"

sec "I6 same, but with GIT_WORK_TREE too (should be caught by the toplevel guard)"
git init -q "$S/other6"; git -C "$S/other6" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
mkdir -p "$S/wI6"
( cd "$S" && GIT_DIR="$S/other6/.git" GIT_WORK_TREE="$S/other6" python3 -I "$CTRL" --lane "$S/laneI" --rev "$REV" \
   --base "$BASE" --work "$S/wI6" --outdir "$S/oI6" --only pos-real --jobs 1 ) >"$S/i6.log" 2>&1
probe "I6.driver-rc" "$?"
probe "I6.tail" "$(tail -2 "$S/i6.log" | tr '\n' '|')"
probe "I6.other6-has-r93-commit" "$(git -C "$S/other6" log --oneline --all 2>/dev/null | grep -c 'r93 control')"

sec "I7 driver: is the lane's own .git touched by a normal run?"
before=$(git -C "$LANE" rev-parse HEAD)
mkdir -p "$S/wI7" "$S/oI7"
python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" --work "$S/wI7" --outdir "$S/oI7" --only pos-real --jobs 1 >"$S/i7.log" 2>&1
probe "I7.rc" "$?"
probe "I7.lane-head-unchanged" "$([ "$before" = "$(git -C "$LANE" rev-parse HEAD)" ] && echo yes || echo NO)"
probe "I7.lane-status" "$(git -C "$LANE" status --porcelain | wc -l) lines"
probe "I7.lane-refs-replace" "$(git -C "$LANE" replace -l | wc -l) refs"
probe "I7.lane-objects-count" "$(git -C "$LANE" count-objects -v | tr '\n' ' ')"

printf '\n===== done =====\n'
