#!/bin/bash
# T54W2Sent04 — the literal "second run": a REAL first deciding invocation (it opens the
# control gate, runs no-harm + precheck + census + both counters, ~5 min) on a fixture
# clone, then the identical invocation again. The second one must be refused with
# DECIDING_REFUSED second-invocation c1 and must touch nothing.
# The lane is READ-ONLY: mutations happen only in a `git clone --shared` under $TMP.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C1=99c3bc88d704566197783f66b211ee0a830e0330
FREEZE=441c26bec5e4c1cc31bc2a840f311cb8d1965259
RECEIPT_SRC=097985c18b9a186c310bd35890b95b733cbb7f5b   # the only rev carrying controls-a.*
C=.ufo/evidence/round-54/control
TMP=$(mktemp -d) || exit 2
trap 'rm -rf -- "$TMP"' EXIT
export HYAKU_SCRATCH=$TMP/hyaku
git clone --shared --quiet "$LANE" "$TMP/lane" || exit 2
git -C "$TMP/lane" checkout --detach --quiet "$C1"       || exit 2
L=$TMP/lane
[ "$(git -C "$L" rev-parse --show-toplevel)" = "$L" ] || { echo "toplevel assert failed"; exit 2; }
echo "fixture toplevel: $L"; echo "REV=$C1 FREEZE=$FREEZE"

# the four receipt paths: a bytes from RECEIPT_SRC (the only committed ones), b fabricated
b_a_out=$(git -C "$L" cat-file -p "$RECEIPT_SRC:$C/controls-a.stdout" | git -C "$L" hash-object -w --stdin)
b_a_exit=$(git -C "$L" cat-file -p "$RECEIPT_SRC:$C/controls-a.exit" | git -C "$L" hash-object -w --stdin)
b_b_out=$(printf 'FIXTURE controls-b.stdout: no committed bytes exist at any rev\n' | git -C "$L" hash-object -w --stdin)
b_b_exit=$(printf '0\n' | git -C "$L" hash-object -w --stdin)
idx=$TMP/idx; rm -f "$idx"
GIT_INDEX_FILE=$idx git -C "$L" read-tree HEAD
GIT_INDEX_FILE=$idx git -C "$L" update-index --add --cacheinfo 100644,$b_a_out,$C/controls-a.stdout
GIT_INDEX_FILE=$idx git -C "$L" update-index --add --cacheinfo 100644,$b_a_exit,$C/controls-a.exit
GIT_INDEX_FILE=$idx git -C "$L" update-index --add --cacheinfo 100644,$b_b_out,$C/controls-b.stdout
GIT_INDEX_FILE=$idx git -C "$L" update-index --add --cacheinfo 100644,$b_b_exit,$C/controls-b.exit
tree=$(GIT_INDEX_FILE=$idx git -C "$L" write-tree)
newc=$(printf 'fixture: the four control receipts\n' | \
  GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=f@l GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=f@l \
  git -C "$L" commit-tree "$tree" -p HEAD)
git -C "$L" update-ref --no-deref HEAD "$newc"
git -C "$L" read-tree HEAD
for f in controls-a.stdout controls-a.exit controls-b.stdout controls-b.exit; do
  git -C "$L" cat-file -p "HEAD:$C/$f" > "$L/$C/$f"; done
echo "fixture HEAD=$newc"; echo "clean tree: [$(git -C "$L" status --porcelain)]"

OUT=$TMP/out; mkdir -p "$OUT"
echo "=== FIRST invocation (real; about five minutes)"
t0=$(date +%s)
( cd "$L" && bash .ufo/evidence/round-54/deciding-run.sh "$L" "$newc" "$FREEZE" "$OUT" > "$TMP/first.log" 2>&1 )
rc=$?; echo "first rc=$rc elapsed_s=$(( $(date +%s) - t0 ))"
tail -3 "$TMP/first.log"
for f in c1.start c1.end c2.start c2.end deciding-run.exit; do printf '  %s=%s\n' "$f" "$(cat "$OUT/$f" 2>/dev/null)"; done
echo "  frozen.stdout=$(cat "$OUT/frozen.stdout")"
sum_before=$(find "$OUT" -type f -printf '%f %s\n' | sort | sha256sum)

echo "=== SECOND invocation, identical command, same OUT"
t0=$(date +%s%N)
( cd "$L" && HYAKU_SCRATCH=$TMP/hyaku2 bash .ufo/evidence/round-54/deciding-run.sh "$L" "$newc" "$FREEZE" "$OUT" > "$TMP/second.log" 2>&1 )
rc=$?; echo "second rc=$rc elapsed_ms=$(( ( $(date +%s%N) - t0 ) / 1000000 ))"
cat "$TMP/second.log"
sum_after=$(find "$OUT" -type f -printf '%f %s\n' | sort | sha256sum)
echo "outdir file-set+size sha before: $sum_before"
echo "outdir file-set+size sha after : $sum_after"
echo "second-invocation scratch root created? $(test -e "$TMP/hyaku2" && echo YES || echo NO)"
