#!/usr/bin/env bash
# R93SN1 probe 5: decisive exploit demos.
#   (a) ambient GIT_DIR redirects the driver's MUTATING git calls
#   (b) a partial run clobbers the committed C1-summary.txt
#   (c) spec gate.repo='' -> 'git -C ""' reads the process CWD repo
#   (d) make-pins.py --lane '' write target
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe5.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
MPINS="$LANE/.ufo/evidence/round-93/c1/make-pins.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
BASE=4a7e259b407d582d2010197f32d7524d6bed5370
probe() { printf 'PROBE %-44s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "A ambient GIT_DIR pointing at a CLONE OF THE LANE: where does the fixture commit land?"
git clone -q --shared --no-checkout "$LANE" "$S/hijack" 2>/dev/null
git -C "$S/hijack" checkout -q --detach "$REV" 2>/dev/null
mkdir -p "$S/wA"
GIT_DIR="$S/hijack/.git" GIT_WORK_TREE="$S/hijack" \
  python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
  --work "$S/wA" --outdir "$S/oA" --only pos-real --jobs 1 >"$S/a.log" 2>&1
probe "A.driver-rc" "$?"
probe "A.log-tail" "$(tail -3 "$S/a.log" | tr '\n' '|')"
probe "A.hijack-commit-count" "$(git -C "$S/hijack" log --oneline 2>/dev/null | wc -l)"
probe "A.hijack-has-r93-control-commit" "$(git -C "$S/hijack" log --oneline --all 2>/dev/null | grep -c 'r93 control')"
probe "A.hijack-refs" "$(git -C "$S/hijack" show-ref 2>&1 | tr '\n' '|')"
probe "A.receipt-written" "$(ls -A "$S/oA" 2>/dev/null | tr '\n' ' ')"
probe "A.LANE-refs-replace-after" "$(git -C "$LANE" replace -l | tr '\n' ' ')"
probe "A.LANE-status-after" "$(git -C "$LANE" status --porcelain | wc -l) lines"

sec "B partial run clobbers the committed C1-summary.txt"
cp -r "$LANE/.ufo/evidence/round-93/pre-freeze/controls" "$S/oB"
probe "B.summary-before-lines" "$(wc -l < "$S/oB/C1-summary.txt")"
mkdir -p "$S/wB"
python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
  --work "$S/wB" --outdir "$S/oB" --only nowork-base --jobs 1 >"$S/b.log" 2>&1
probe "B.rc" "$?"
probe "B.summary-after-lines" "$(wc -l < "$S/oB/C1-summary.txt")"
probe "B.summary-after-content" "$(cat "$S/oB/C1-summary.txt" | tr '\n' '|')"
probe "B.receipt-count" "$(ls "$S/oB"/*.out | wc -l)"

sec "C spec gate.repo='' -> 'git -C \"\"' reads the PROCESS CWD repo"
git init -q "$S/cwdC"
git -C "$S/cwdC" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
printf 'x\n' > "$S/cwdC/f.txt"
git -C "$S/cwdC" add f.txt && git -C "$S/cwdC" -c user.name=t -c user.email=t@t commit -q -m f
FA=$(git -C "$S/cwdC" rev-parse HEAD:f.txt)
FA2=$(printf 'fake\n' | git -C "$S/cwdC" hash-object -w --stdin)
git -C "$S/cwdC" replace "$FA" "$FA2"
mkdir -p "$S/laneC" && git init -q "$S/laneC"
mkdir -p "$S/laneC/.ufo/evidence/round-93/c1"
python3 - "$S/laneC/.ufo/evidence/round-93/c1/census-mutants.json" <<'PY'
import json, sys
json.dump({"schema": 1, "gate": {"repo": "", "commit": "deadbeef", "path": "x", "sha256": "0"*64,
                                 "fixtures": "scripts/fixtures/sources-census"},
           "timeout_s": 1, "runs_per_verdict": 1, "mutants": []}, open(sys.argv[1], "w"))
PY
git -C "$S/laneC" add -A && git -C "$S/laneC" -c user.name=t -c user.email=t@t commit -q -m spec
REVC=$(git -C "$S/laneC" rev-parse HEAD)
mkdir -p "$S/wC"
( cd "$S/cwdC" && python3 -I "$MEAS" --repo "$S/laneC" --rev "$REVC" --work "$S/wC" ) >"$S/c.log" 2>&1
probe "C.counter-output" "$(head -2 "$S/c.log" | tr '\n' '|')"
probe "C.inspected-CWD-repo-not-spec-repo" "$(grep -q 'replace-refs-present:fleet' "$S/c.log" && echo 'YES - it read the CWD repo, not the repo named in the spec' || echo 'no')"

sec "D make-pins.py: --lane '' target, and whether it overwrites a committed pins.json"
mkdir -p "$S/cwdD" && cd "$S/cwdD" || exit 1
python3 -I "$MPINS" --lane "" --rev "$REV" >"$S/d1.log" 2>&1
probe "D.empty-lane.rc" "$?"
probe "D.empty-lane.out" "$(tail -1 "$S/d1.log")"
probe "D.cwdD-tree" "$(find "$S/cwdD" | head -5 | tr '\n' ' ')"
git clone -q --shared --no-checkout "$LANE" "$S/laneD" 2>/dev/null
git -C "$S/laneD" checkout -q --detach "$REV" 2>/dev/null
probe "D.pins-before" "$(sha256sum "$S/laneD/.ufo/evidence/round-93/c1/pins.json" | cut -c1-16)"
python3 -I "$MPINS" --lane "$S/laneD" --rev "$REV" >"$S/d2.log" 2>&1
probe "D.write-mode.rc" "$?"
probe "D.pins-after" "$(sha256sum "$S/laneD/.ufo/evidence/round-93/c1/pins.json" | cut -c1-16)"
probe "D.laneD-status" "$(git -C "$S/laneD" status --porcelain | tr '\n' ' ')"

printf '\n===== done =====\n'
