#!/usr/bin/env bash
# T90SN1 probe — hostile-path behaviour of the round-90 drivers.
# Every write happens inside $S; the fleet and every lane are only read.
# Re-run: bash T90SN1-probe.sh
set -u
S=/fast/scratch/hyaku/tameshi-r90/T90SN1
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
EV=$LANE/.ufo/evidence/round-90
trap 'rm -rf -- "$S"' EXIT
mkdir -p -- "$S" || { echo "scratch unavailable"; exit 3; }
say() { printf '\n===== %s\n' "$*"; }
files() { ( cd "$1" && find . -type f -not -path './.git/*' | sort | xargs -r sha256sum ); }

say "D0 the 2026-11-06 incident class: empty path resolves to cwd"
( cd /home/vgpnk/Projects/shokunin && git -C "" rev-parse --show-toplevel; echo "rc=$?" )
python3 -c 'import os; print("python realpath(empty)=" + os.path.realpath(""))'

say "D1 measure.py --repo '' (empty repo arg is not refused; it becomes cwd)"
mkdir -p "$S/d1/w"
( cd "$S/d1" && python3 -I "$EV/c1/measure.py" --repo "" --rev HEAD --work "$S/d1/w"; echo "rc=$?" )

say "D2 measure.py --work '' from an empty cwd (empty work passes the emptiness check)"
mkdir -p "$S/d2"
( cd "$S/d2" && python3 -I "$EV/c1/measure.py" --repo "$LANE" --rev 0000000000000000000000000000000000000000 --work ""; echo "rc=$?" )

say "D3 fixes.py --target '' from a lane-shaped cwd (all five writes land in cwd, rc 0)"
FL="$S/d3/fake-lane"
mkdir -p "$FL/corpus/knowledge" "$FL/corpus/lessons" "$FL/tools"
printf 'orig readme\n'  > "$FL/corpus/README.md"
printf 'orig ledger entry\n' > "$FL/corpus/knowledge/kernel-witnessed-ledger.md"
printf 'orig lesson\n'  > "$FL/corpus/lessons/round-89.md"
printf 'orig skill\n'   > "$FL/SKILL.md"
printf '{"rows": []}\n' > "$FL/tools/registry.json"
files "$FL" > "$S/d3-before.txt"
( cd "$FL" && python3 -I "$EV/c2/fixes.py" --target ""; echo "rc=$?" )
files "$FL" > "$S/d3-after.txt"
echo "--- files changed by --target '':"
diff "$S/d3-before.txt" "$S/d3-after.txt" | sed -n 's/^> //p' | awk '{print $2}'
echo "--- is the target a git worktree? (fixes.py never asks)"
( cd "$FL" && git rev-parse --show-toplevel; echo "rc=$?" )

say "D4 fixes.py --target on a sibling-lane shape (4 appends, then no rollback)"
SL="$S/d4/sibling-lane"
mkdir -p "$SL/corpus/knowledge" "$SL/corpus/lessons"
printf 'orig readme\n'  > "$SL/corpus/README.md"
printf 'orig lesson\n'  > "$SL/corpus/lessons/round-89.md"
printf 'orig skill\n'   > "$SL/SKILL.md"
files "$SL" > "$S/d4-before.txt"
python3 -I "$EV/c2/fixes.py" --target "$SL"; echo "rc=$?"
files "$SL" > "$S/d4-after.txt"
echo "--- files changed before the registry.json crash:"
diff "$S/d4-before.txt" "$S/d4-after.txt" | sed -n 's/^> //p' | awk '{print $2}'

say "D5 fixes.py --target on a fleet-root shape (no corpus/: fails before writing)"
FR="$S/d5/fleet-root-shape"; mkdir -p "$FR"
python3 -I "$EV/c2/fixes.py" --target "$FR" 2>&1 | tail -3; echo "rc=${PIPESTATUS[0]}"
echo "--- files created under the target:"; find "$FR" -mindepth 1 | wc -l

say "D6 shell counters refuse empty path arguments (contrast with D1-D3)"
bash "$EV/c2/measure-c2.sh" "$LANE" "" "$S/d6-w" >/dev/null 2>"$S/d6a.err"; echo "measure-c2 empty REV rc=$?"; sed -n 1p "$S/d6a.err"
bash "$EV/c2/measure-c2.sh" "$LANE" "$(git -C "$LANE" rev-parse HEAD)" "" >/dev/null 2>"$S/d6b.err"; echo "measure-c2 empty WORK rc=$?"; sed -n 1p "$S/d6b.err"
bash "$EV/c2/controls-c2.sh" "$LANE" "" >/dev/null 2>"$S/d6c.err"; echo "controls-c2 empty SC rc=$?"; sed -n 1p "$S/d6c.err"

say "D7 fixes.py exit status ignores both of its own receipts"
echo "(D3 printed rc=0 although registry_exit/selftest_exit were non-zero: no sys.exit) "

say "done"
