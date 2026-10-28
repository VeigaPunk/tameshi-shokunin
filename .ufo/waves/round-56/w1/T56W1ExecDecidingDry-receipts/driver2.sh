#!/bin/bash
# Round-56 wave 1 / seat T56W1ExecDecidingDry - follow-up arms
# f2: receipts committed off-freeze and merged in (REV descends from FREEZE, so the
#     script exists in REV's tree) -> control-receipt-not-after-freeze
# outdir / va / vb: the three refusals the first driver did not exercise
# d3b: re-run the dirty-tree prefix escape with clean-tree-before.txt preserved
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
S=/fast/scratch/hyaku/tameshi-r56/T56W1ExecDecidingDry
FREEZE=c3e2ca9f020776b3d66c7af854fb82c834674fcf
BASE=981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
C=$S/clone
R=$S/receipts
E=.ufo/evidence/round-56
OUT=$C/$E/dryout
OUTREL=$E/dryout
GI=(-c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null)
. "$R/01-fixtures.txt"

[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "TOPLEVEL_MISMATCH"; exit 9; }

reset_tree() {
  git -C "$C" checkout --quiet -- . 2>/dev/null
  rm -f "$C/$E/dirty-canary.txt" "$C/$E/dryout-extra.txt"
  rm -rf "$C/$E/no-such-out"
}

run_arm() { # name checkout rev freeze outpre dirty bound
  local name=$1 co=$2 rev=$3 frz=$4 pre=$5 dirty=$6 bound=${7:-}
  local hs=$S/hs-$name rf=$R/$name.txt raw=$R/$name.raw rc
  reset_tree
  git -C "$C" checkout --detach --quiet "$co" || { echo "ARM $name CHECKOUT_FAIL" > "$rf"; return; }
  rm -rf "$OUT"; [ "$pre" = noout ] || mkdir -p "$OUT"
  case $pre in c1.start) : > "$OUT/c1.start";; c2.start) : > "$OUT/c2.start";; both) : > "$OUT/c1.start"; : > "$OUT/c2.start";; esac
  case $dirty in
    tracked) printf '\nfixture dirty-canary line\n' >> "$C/corpus/SOURCES.md";;
    untracked) : > "$C/$E/dirty-canary.txt";;
    outsuffix) : > "$C/$E/dryout-extra.txt";;
    strip-a) grep -v '^CONTROLS_A:' "$C/$E/control/controls-a.stdout" > "$S/x" && cat "$S/x" > "$C/$E/control/controls-a.stdout";;
    strip-b) grep -v '^CONTROLS_B:' "$C/$E/control/controls-b.stdout" > "$S/x" && cat "$S/x" > "$C/$E/control/controls-b.stdout";;
  esac
  rm -rf "$hs"; mkdir -p "$hs"
  {
    echo "ARM $name"
    echo "CMD: bash \$CLONE/$E/deciding-run.sh \$CLONE $rev $frz \$CLONE/$OUTREL"
    echo "HEAD=$(git -C "$C" rev-parse HEAD)  REV=$(git -C "$C" rev-parse "$rev")  FREEZE=$(git -C "$C" rev-parse "$frz")"
    echo "SCRIPT_SHA256=$(sha256sum "$C/$E/deciding-run.sh" | cut -d' ' -f1)"
    echo "OUT_PRE: $(ls -A "$OUT" 2>/dev/null | tr '\n' ' ')"
    echo "TREE_BEFORE:"; git -C "$C" status --porcelain
  } > "$rf"
  if [ -n "$bound" ]; then
    setsid env HYAKU_SCRATCH="$hs" bash "$C/$E/deciding-run.sh" "$C" "$rev" "$frz" "$OUT" > "$raw" 2>&1 &
    local pid=$!
    sleep "$bound"
    if kill -0 "$pid" 2>/dev/null; then
      echo "STILL_RUNNING_AFTER=${bound}s -> killed" >> "$rf"
      kill -TERM -"$pid" 2>/dev/null; sleep 2; kill -KILL -"$pid" 2>/dev/null
      wait "$pid" 2>/dev/null; rc="killed-after-${bound}s"
    else wait "$pid"; rc=$?; fi
  else
    env HYAKU_SCRATCH="$hs" bash "$C/$E/deciding-run.sh" "$C" "$rev" "$frz" "$OUT" > "$raw" 2>&1
    rc=$?
  fi
  {
    echo "EXIT=$rc"
    echo "--- stdout+stderr ---"; cat "$raw"
    echo "--- refusal lines ---"; grep -E '^(DECIDING_REFUSED|FREEZE_INTEGRITY|GATE:)' "$raw" || echo '(none)'
    echo "--- OUT after ---"; ls -A "$OUT" 2>/dev/null | sort | sed 's/^/  /'
    echo "--- clean-tree-before.txt ---"; cat "$OUT/clean-tree-before.txt" 2>/dev/null || echo '(not reached)'
    echo "--- OUT receipt-gate ---"
    if [ -f "$OUT/receipt-gate.stdout" ]; then echo "receipt-gate.exit=$(cat "$OUT/receipt-gate.exit" 2>/dev/null)"; cat "$OUT/receipt-gate.stdout"; else echo '(receipt-gate not reached)'; fi
    echo "--- SCR $hs/tameshi-r56/deciding ---"; if [ -d "$hs/tameshi-r56/deciding" ]; then echo present; else echo absent; fi
    echo "--- ran-anything canary (OUT) ---"
    for f in c1.stdout c2.stdout c1.start c2.start no-harm.stdout no-harm.exit coldread-precheck.stdout census.stdout frozen.stdout; do
      if [ -e "$OUT/$f" ]; then echo "$f=PRESENT"; else echo "$f=absent"; fi
    done
    echo "--- TREE_AFTER ---"; git -C "$C" status --porcelain
  } >> "$rf"
}

# ---- f2: merge a base-rooted receipts branch into a freeze-rooted commit
reset_tree
git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-f2 "$FREEZE"
git -C "$C" "${GI[@]}" merge --no-ff --no-edit fix-f > "$R/f2-merge.log" 2>&1 || { echo "MERGE_FAIL" >> "$R/f2-merge.log"; }
FIX_F2=$(git -C "$C" rev-parse HEAD)
{
  echo "FIX_F2=$FIX_F2  parents=$(git -C "$C" rev-list --parents -n1 $FIX_F2 | cut -d' ' -f2- | tr '\n' ' ')"
  echo "freeze-is-ancestor-of-FIX_F2: $(git -C "$C" merge-base --is-ancestor $FREEZE $FIX_F2 && echo yes || echo no)"
  echo "freeze-is-ancestor-of-FIX_F:  $(git -C "$C" merge-base --is-ancestor $FREEZE $FIX_F && echo yes || echo no)"
  echo "last-commit-touching-controls-a.stdout-at-FIX_F2: $(git -C "$C" log -1 --format=%H $FIX_F2 -- $E/control/controls-a.stdout)"
  echo "last-commit-touching-controls-b.stdout-at-FIX_F2: $(git -C "$C" log -1 --format=%H $FIX_F2 -- $E/control/controls-b.stdout)"
  echo "script-in-FIX_F2-tree: $(git -C "$C" cat-file -t $FIX_F2:$E/deciding-run.sh 2>&1)"
  echo "script-in-FIX_F-tree:  $(git -C "$C" cat-file -t $FIX_F:$E/deciding-run.sh 2>&1)"
} > "$R/02-f2-graph.txt"
echo "FIX_F2=$FIX_F2" >> "$R/01-fixtures.txt"

run_arm f2 "$FIX_F2" "$FIX_F2" "$FREEZE" none none
run_arm outdir "$FIX_D" "$FIX_D" "$FREEZE" noout none
run_arm va "$FIX_D" "$FIX_D" "$FREEZE" none strip-a
run_arm vb "$FIX_D" "$FIX_D" "$FREEZE" none strip-b
run_arm d3b "$FIX_D" "$FIX_D" "$FREEZE" none outsuffix 8
reset_tree
echo DRIVER2_DONE
