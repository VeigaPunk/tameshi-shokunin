#!/usr/bin/env bash
# Round-56 knowledge-entry fixture: the gate's content-identity exception, its
# control-role ancestor rule, and its stated blind spot (a copied `rev=` token).
# Read-only against the lane; every commit happens inside $D.
set -u
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
GATE=$L/tools/receipt-revision-gate.py
BASE=${HYAKU_SCRATCH:?}/tameshi-r56/T56W1ScribeKnowledge
mkdir -p "$BASE"
D=$(mktemp -d "$BASE/fixture.XXXXXX") || exit 1
trap 'rm -rf -- "$D"' EXIT
# scrub inherited git environment before any git call
for v in $(env | grep -o '^GIT_[A-Z_]*' ); do unset "$v"; done
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=f@example.invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=f@example.invalid

git clone --shared --quiet "$L" "$D/clone" || exit 1
C=$D/clone
test "$(git -C "$C" rev-parse --show-toplevel)" = "$C" || { echo "TOPLEVEL MISMATCH"; exit 1; }
git -C "$C" checkout --quiet --detach 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 || exit 1

# two synthetic commits: A1 changes only b.txt
printf 'alpha\n' > "$C/a.txt"; printf 'beta-1\n' > "$C/b.txt"
git -C "$C" add -f a.txt b.txt >/dev/null
git -C "$C" commit -q -m 'fixture: A0' >/dev/null
A0=$(git -C "$C" rev-parse HEAD)
printf 'beta-2\n' > "$C/b.txt"
git -C "$C" add -f b.txt >/dev/null
git -C "$C" commit -q -m 'fixture: A1 (b.txt only)' >/dev/null
A1=$(git -C "$C" rev-parse HEAD)
# a side commit that is not an ancestor of A1
git -C "$C" checkout -q --detach "$A0"
printf 'side\n' > "$C/c.txt"
git -C "$C" add -f c.txt >/dev/null
git -C "$C" commit -q -m 'fixture: SIDE' >/dev/null
SIDE=$(git -C "$C" rev-parse HEAD)
git -C "$C" checkout -q --detach "$A1"
echo "A0=$A0"; echo "A1=$A1"; echo "SIDE=$SIDE"

printf 'a.txt\n' > "$D/paths-a.txt"
printf 'a.txt\nb.txt\n' > "$D/paths-ab.txt"
printf 'CTL CTL_POS_fx VERDICT: rev=%s result=PASS\n' "$A0" > "$D/r-pos-a0.txt"
printf 'CTL CTL_POS_fx VERDICT: rev=%s result=PASS\n' "$A1" > "$D/r-pos-a1.txt"
printf 'CTL CTL_SET_fx rev=%s result=PASS\nCTL CTL_SET_fx rev=%s result=PASS\n' "$A0" "$A1" > "$D/r-ctl.txt"
printf 'CTL CTL_SET_fx rev=%s result=PASS\nCTL CTL_SET_fx rev=%s result=PASS\n' "$A0" "$SIDE" > "$D/r-ctl-side.txt"
# blind spot: a receipt that names the certified revision but was produced for
# nothing at all (no run, no claim) — the gate cannot tell.
printf 'FABRICATED VERDICT: rev=%s total=0 PASS=true (never run)\n' "$A1" > "$D/r-fab.txt"

run() { local label=$1; shift; echo "--- $label"; TMPDIR=$D python3 "$GATE" --lane "$C" "$@"; echo "rc=$?"; }

run "1 same rev, positive"        --certified "$A1" --receipt "$D/r-pos-a1.txt:positive"
run "2 other rev, no --paths"     --certified "$A1" --receipt "$D/r-pos-a0.txt:positive"
run "3 other rev, --paths a.txt (identical bytes) -> exception" --certified "$A1" --paths "$D/paths-a.txt" --receipt "$D/r-pos-a0.txt:positive"
run "4 other rev, --paths a.txt,b.txt (b.txt drifted)"          --certified "$A1" --paths "$D/paths-ab.txt" --receipt "$D/r-pos-a0.txt:positive"
run "5 control, both revs ancestors"   --certified "$A1" --receipt "$D/r-ctl.txt:control"
run "6 control, one rev not ancestor"  --certified "$A1" --receipt "$D/r-ctl-side.txt:control"
run "7 blind spot: fabricated receipt naming the certified rev" --certified "$A1" --receipt "$D/r-fab.txt:positive"
