#!/usr/bin/env bash
# R93SN1 probe 11: final evidence cleanup.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe11.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
BASE=4a7e259b407d582d2010197f32d7524d6bed5370
probe() { printf 'PROBE %-50s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "M1 fleet repo replace refs (why the H2 control saw exit=2)"
probe "M1.fleet-replace-l" "$(git -C "$FLEET" replace -l | tr '\n' ' ')"
probe "M1.lane-replace-l" "$(git -C "$LANE" replace -l | tr '\n' ' ')"

sec "M2 ambient GIT_DIR: the fixture commit lands in the WRONG repo, guard passes"
git clone -q --shared --no-checkout "$LANE" "$S/hij" 2>/dev/null
git -C "$S/hij" checkout -q --detach "$REV" 2>/dev/null
mkdir -p "$S/w"
( cd "$S" && GIT_DIR="$S/hij/.git" python3 -I "$CTRL" --lane "$LANE" --rev "$REV" \
   --base "$BASE" --work "$S/w" --outdir "$S/o" --only pos-real --jobs 1 ) >"$S/m2.log" 2>&1
probe "M2.driver-rc" "$?"
probe "M2.hijack-has-r93-control-commit" "$(git -C "$S/hij" log --oneline --all 2>/dev/null | grep -c 'r93 control pos-real')"
probe "M2.hijack-refs" "$(git -C "$S/hij" show-ref 2>&1 | head -3 | tr '\n' '|')"
probe "M2.intended-clone-has-commit" "$(find "$S/w" -maxdepth 3 -name .git -exec git -C {} log --oneline -1 \; 2>/dev/null | tr '\n' ' ')"
probe "M2.receipt-exit" "$(grep -m1 '^exit=' "$S/o/pos-real.out" 2>/dev/null)"
probe "M2.receipt-setup-line" "$(grep -m1 'C1_SETUP' "$S/o/pos-real.out" 2>/dev/null)"
probe "M2.LANE-unaffected" "HEAD=$(git -C "$LANE" rev-parse --short HEAD) replace-refs=$(git -C "$LANE" replace -l | wc -l)"

sec "M3 the driver's sh() inherits the ambient env (no GIT_* scrub) - code-level"
grep -n 'def sh(' -A4 "$CTRL" | sed 's/^/    /'
probe "M3.counter-git-helper-env" "$(grep -n 'sealed_env()' "$LANE/.ufo/evidence/round-93/c1/measure-v93.py" | head -2 | tr '\n' '|')"

sec "M4 --outdir / --work are not validated (relative + empty)"
mkdir -p "$S/cwdM4" "$S/abs"
( cd "$S/cwdM4" && python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
   --work relwork --outdir relout --only nowork-base --jobs 1 ) >"$S/m4.log" 2>&1
probe "M4.driver-rc" "$?"
probe "M4.written-into-process-cwd" "$(cd "$S/cwdM4" && find . -maxdepth 2 | head -8 | tr '\n' ' ')"

sec "M5 counter --rev '' : what blob semantics does it use?"
mkdir -p "$S/wM5"
python3 -I "$LANE/.ufo/evidence/round-93/c1/measure-v93.py" --repo "$LANE" --rev "" --work "$S/wM5" 2>&1 | grep -E '^C1_(SUMMARY|R93_PASS)' | cut -c1-120

sec "M6 summary-file overwrite vs M4 rerun protection"
probe "M6.receipt_path-protects" "per-state receipts: <name>.rerun-N.out"
probe "M6.summary-write" "C1-summary.txt written with plain open(...,'w') - NO rerun protection"
grep -n 'C1-summary.txt' "$CTRL" | sed 's/^/    /'

printf '\n===== done =====\n'
