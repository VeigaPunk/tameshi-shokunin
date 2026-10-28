#!/usr/bin/env bash
# Round-56 knowledge-entry fixture, part 2: an empty --paths file, a 7-hex
# prefix, a tag, and two distinct revs in one positive receipt.
set -u
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
GATE=$L/tools/receipt-revision-gate.py
BASE=${HYAKU_SCRATCH:?}/tameshi-r56/T56W1ScribeKnowledge
mkdir -p "$BASE"
D=$(mktemp -d "$BASE/fixture2.XXXXXX") || exit 1
trap 'rm -rf -- "$D"' EXIT
for v in $(env | grep -o '^GIT_[A-Z_]*' ); do unset "$v"; done
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=f@example.invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=f@example.invalid
git init -q -b master "$D/repo" || exit 1
C=$D/repo
test "$(git -C "$C" rev-parse --show-toplevel)" = "$C" || { echo "TOPLEVEL MISMATCH"; exit 1; }
printf 'alpha\n' > "$C/a.txt"; git -C "$C" add -f a.txt >/dev/null; git -C "$C" commit -q -m c0 >/dev/null
C0=$(git -C "$C" rev-parse HEAD)
printf 'beta\n' > "$C/b.txt"; git -C "$C" add -f b.txt >/dev/null; git -C "$C" commit -q -m c1 >/dev/null
C1=$(git -C "$C" rev-parse HEAD)
git -C "$C" tag -a v1 -m tag "$C1" >/dev/null 2>&1 || git -C "$C" tag v1 "$C1"
echo "C0=$C0"; echo "C1=$C1"
printf 'CTL CTL_POS_fx VERDICT: rev=%s result=PASS\n' "$C0" > "$D/r-c0.txt"
printf 'CTL CTL_POS_fx VERDICT: rev=%s result=PASS\n' "${C1:0:7}" > "$D/r-prefix.txt"
printf 'CTL CTL_POS_fx VERDICT: rev=v1 result=PASS\n' > "$D/r-tag.txt"
printf 'A rev=%s\nB rev=%s\n' "$C0" "$C1" > "$D/r-two.txt"
: > "$D/paths-empty.txt"
run() { local label=$1; shift; echo "--- $label"; TMPDIR=$D python3 "$GATE" --lane "$C" "$@"; echo "rc=$?"; }
run "8 other rev, EMPTY --paths file"  --certified "$C1" --paths "$D/paths-empty.txt" --receipt "$D/r-c0.txt:positive"
run "9 7-hex prefix of the certified rev" --certified "$C1" --receipt "$D/r-prefix.txt:positive"
run "10 rev names an annotated tag"    --certified "$C1" --receipt "$D/r-tag.txt:positive"
run "11 two distinct revs, positive"   --certified "$C1" --receipt "$D/r-two.txt:positive"
