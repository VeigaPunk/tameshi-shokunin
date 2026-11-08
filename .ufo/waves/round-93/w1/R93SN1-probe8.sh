#!/usr/bin/env bash
# R93SN1 probe 8: empty --rev, relative --work, and git-config/hook inheritance.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe8.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
probe() { printf 'PROBE %-48s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "J1 counter with --rev '' : index read, and does it PASS?"
mkdir -p "$S/wJ1"
python3 -I "$MEAS" --repo "$LANE" --rev "" --work "$S/wJ1" >"$S/j1.log" 2>&1
probe "J1.rc" "$?"
probe "J1.PASS-line" "$(grep '^C1_R93_PASS' "$S/j1.log")"
probe "J1.summary-rev-field" "$(grep '^C1_SUMMARY' "$S/j1.log" | cut -c1-40)"
probe "J1.rev-echoed" "$(grep -o 'rev=[^ ]*' "$S/j1.log" | head -1)"

sec "J2 counter with --repo '' (realpath -> process cwd)"
mkdir -p "$S/wJ2" "$S/cwdJ2"
( cd "$S/cwdJ2" && python3 -I "$MEAS" --repo "" --rev "$REV" --work "$S/wJ2" ) >"$S/j2.log" 2>&1
probe "J2.rc" "$?"
probe "J2.first-line" "$(head -1 "$S/j2.log")"

sec "J3 RELATIVE --work writes into the process cwd"
mkdir -p "$S/cwdJ3" "$S/absJ3"
( cd "$S/cwdJ3" && python3 -I "$MEAS" --repo "$LANE" --rev "$REV" --work relwork ) >"$S/j3.log" 2>&1
probe "J3.rc" "$?"
probe "J3.cwd-tree" "$(cd "$S/cwdJ3" && find . -maxdepth 2 | head -8 | tr '\n' ' ')"
( cd "$S/cwdJ3" && python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$REV" \
    --work relwork2 --outdir relout --only nowork-base --jobs 1 ) >"$S/j3b.log" 2>&1
probe "J3b.driver-rc" "$?"
probe "J3b.cwd-tree" "$(cd "$S/cwdJ3" && find . -maxdepth 2 | head -10 | tr '\n' ' ')"

sec "J4 git config inheritance: core.hooksPath from an ambient GIT_CONFIG_GLOBAL"
mkdir -p "$S/hooks" "$S/cfg" "$S/wJ4" "$S/oJ4"
cat > "$S/hooks/pre-commit" <<'EOF'
#!/bin/sh
echo "HOOK-EXECUTED pid=$$" >> "$HOOK_MARKER"
exit 0
EOF
chmod +x "$S/hooks/pre-commit"
cat > "$S/cfg/gitconfig" <<EOF
[core]
	hooksPath = $S/hooks
[user]
	name = envuser
	email = envuser@example.invalid
EOF
export HOOK_MARKER="$S/hook-marker.txt"
GIT_CONFIG_GLOBAL="$S/cfg/gitconfig" GIT_CONFIG_NOSYSTEM=1 \
  python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$REV" \
  --work "$S/wJ4" --outdir "$S/oJ4" --only pos-real --jobs 1 >"$S/j4.log" 2>&1
probe "J4.driver-rc" "$?"
probe "J4.hook-executed" "$( [ -f "$S/hook-marker.txt" ] && echo 'YES - ambient git config drove a hook during the fixture commit' || echo no )"
probe "J4.marker" "$(cat "$S/hook-marker.txt" 2>/dev/null | tr '\n' '|')"

sec "J5 the counter's own git calls are env-scrubbed (sealed_env) - verify"
mkdir -p "$S/wJ5"
GIT_CONFIG_GLOBAL="$S/cfg/gitconfig" GIT_DIR="$S/other-does-not-exist" \
  python3 -I "$MEAS" --repo "$LANE" --rev "$REV" --work "$S/wJ5" >"$S/j5.log" 2>&1
probe "J5.rc" "$?"
probe "J5.PASS" "$(grep '^C1_R93_PASS' "$S/j5.log")"
probe "J5.first-line" "$(head -1 "$S/j5.log")"

sec "J6 driver summary after a partial run: does C1-summary.txt describe the receipts on disk?"
cp -r "$LANE/.ufo/evidence/round-93/pre-freeze/controls" "$S/oJ6"
mkdir -p "$S/wJ6"
python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$REV" \
  --work "$S/wJ6" --outdir "$S/oJ6" --only nowork-base --jobs 1 >"$S/j6.log" 2>&1
probe "J6.receipts-on-disk" "$(ls "$S/oJ6"/*.out | wc -l)"
probe "J6.summary-rows" "$(wc -l < "$S/oJ6/C1-summary.txt")"
probe "J6.summary-content" "$(cat "$S/oJ6/C1-summary.txt" | tr '\n' '|')"
probe "J6.unmentioned-receipts" "$(for f in "$S/oJ6"/*.out; do b=$(basename "$f" .out); grep -q "^$b " "$S/oJ6/C1-summary.txt" || echo "$b"; done | tr '\n' ' ')"

printf '\n===== done =====\n'
