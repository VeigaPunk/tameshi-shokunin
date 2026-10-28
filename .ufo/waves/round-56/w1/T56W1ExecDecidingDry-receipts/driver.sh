#!/bin/bash
# Round-56 wave 1 / seat T56W1ExecDecidingDry
# Drive .ufo/evidence/round-56/deciding-run.sh through its pre-run refusal matrix
# in a scratch clone of the lane pinned at the round-56 freeze.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
S=/fast/scratch/hyaku/tameshi-r56/T56W1ExecDecidingDry
FREEZE=c3e2ca9f020776b3d66c7af854fb82c834674fcf
BASE=981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
C=$S/clone
R=$S/receipts
E=.ufo/evidence/round-56
GI=(-c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null)

rm -rf "$C" "$S"/hs-*; mkdir -p "$R"
git clone --shared --quiet "$LANE" "$C" || { echo "CLONE_FAIL"; exit 9; }
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "TOPLEVEL_MISMATCH"; exit 9; }
git -C "$C" checkout --detach --quiet "$FREEZE" || { echo "CHECKOUT_FAIL"; exit 9; }
{
  echo "CLONE=$C"
  echo "TOPLEVEL=$(git -C "$C" rev-parse --show-toplevel)"
  echo "HEAD=$(git -C "$C" rev-parse HEAD)"
  echo "FREEZE=$(git -C "$C" rev-parse $FREEZE)"
  echo "BASE=$(git -C "$C" rev-parse $BASE)"
  echo "SCRIPT_SHA256=$(sha256sum "$C/$E/deciding-run.sh" | cut -d' ' -f1)"
  echo "MANIFEST_DECIDING_DIGEST=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["files"]["deciding-run.sh"])' "$C/$E/freeze.json")"
} > "$R/00-clone.txt"

commit_fixture() { # message
  git -C "$C" add -A >/dev/null || return 9
  git -C "$C" "${GI[@]}" commit -q -m "$1" >/dev/null || return 9
  git -C "$C" rev-parse HEAD
}

# ---------------------------------------------------------------- fixtures
# a1: freeze.json with ONE digest changed (no-harm.sh)
git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-a1 "$FREEZE"
python3 - "$C/$E/freeze.json" <<'PY'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
d['files']['no-harm.sh'] = '0' * 64
open(p, 'w').write(json.dumps(d, indent=1) + '\n')
PY
FIX_A1=$(commit_fixture 'fixture a1: freeze.json digest for no-harm.sh replaced with zeros')

# a2: frozen file bytes changed at the freeze commit, manifest untouched
git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-a2 "$FREEZE"
printf '\n# fixture a2: one appended byte-run in a frozen file\n' >> "$C/$E/no-harm.sh"
FIX_A2=$(commit_fixture 'fixture a2: no-harm.sh bytes changed, freeze.json untouched')

# a3: one entry DELETED from the manifest's files map
git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-a3 "$FREEZE"
python3 - "$C/$E/freeze.json" <<'PY'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
del d['files']['deciding-run.sh']
open(p, 'w').write(json.dumps(d, indent=1) + '\n')
PY
FIX_A3=$(commit_fixture 'fixture a3: deciding-run.sh entry deleted from freeze.json files map')

# d: pre-registered control receipts that the binding gate accepts at REV
mk_clean_controls() { # rev-named
  mkdir -p "$C/$E/control"
  cat > "$C/$E/control/controls-a.stdout" <<EOF
CTL CTL_0_c1 C1_R56: rev=$1 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false
CTL CTL_0_c2 C2_R56: rev=$1 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false
CONTROLS_A: 2/2 as pre-registered
EOF
  cat > "$C/$E/control/controls-b.stdout" <<EOF
CTL CTL_POS_c1 C1_R56: rev=$1 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 total=5 C1_R56_PASS=false
CONTROLS_B: 1/1 as pre-registered
EOF
  echo 0 > "$C/$E/control/controls-a.exit"
  echo 0 > "$C/$E/control/controls-b.exit"
}

git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-d "$FREEZE"
mk_clean_controls "$FREEZE"
FIX_D=$(commit_fixture 'fixture d: control receipts naming the freeze, gate-acceptable at this rev')

# f: the same receipts committed on a branch from BASE (does not descend from FREEZE)
git -C "$C" checkout --detach --quiet "$BASE"
git -C "$C" checkout -q -B fix-f "$BASE"
mk_clean_controls "$BASE"
FIX_F=$(commit_fixture 'fixture f: control receipts committed from base, not descending from the freeze')

# g1: controls-b is the REAL round-54 control set (names an absent revision)
git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-g1 "$FREEZE"
mk_clean_controls "$FREEZE"
cp "$LANE/.ufo/evidence/round-54/control/controls-b.stdout" "$C/$E/control/controls-b.stdout"
FIX_G1=$(commit_fixture 'fixture g1: controls-b = real round-54 set (rev=7df0e0426c98 absent)')

# g2: controls-b is the REAL round-54 CTL_POS_c1 line (drifts from the certified rev)
git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-g2 "$FREEZE"
mk_clean_controls "$FREEZE"
{ cat "$LANE/$E/c2/red-before/round-54-ctl-pos-c1.stdout"; echo 'CONTROLS_B: 1/1 as pre-registered'; } > "$C/$E/control/controls-b.stdout"
FIX_G2=$(commit_fixture 'fixture g2: controls-b = real round-54 CTL_POS_c1 line (rev=077d431e6996)')

# g4: controls-a names a revision that is not an ancestor of the certified rev
git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-g4 "$FREEZE"
mk_clean_controls "$FREEZE"
sed -i "s/rev=$FREEZE c0=none credited=46/rev=$FIX_F c0=none credited=46/" "$C/$E/control/controls-a.stdout"
FIX_G4=$(commit_fixture 'fixture g4: controls-a names a sibling-branch revision')

# c2/c3: control receipt that is a tree, and one that is an empty blob
git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-c2 "$FREEZE"
mk_clean_controls "$FREEZE"
rm -f "$C/$E/control/controls-b.stdout"
mkdir -p "$C/$E/control/controls-b.stdout"
: > "$C/$E/control/controls-b.stdout/placeholder"
FIX_C2=$(commit_fixture 'fixture c2: controls-b.stdout is a tree')

git -C "$C" checkout --detach --quiet "$FREEZE"
git -C "$C" checkout -q -B fix-c3 "$FREEZE"
mk_clean_controls "$FREEZE"
: > "$C/$E/control/controls-b.stdout"
FIX_C3=$(commit_fixture 'fixture c3: controls-b.stdout is an empty blob')

{
  echo "FIX_A1=$FIX_A1"; echo "FIX_A2=$FIX_A2"; echo "FIX_A3=$FIX_A3"
  echo "FIX_D=$FIX_D"; echo "FIX_F=$FIX_F"; echo "FIX_G1=$FIX_G1"; echo "FIX_G2=$FIX_G2"
  echo "FIX_G4=$FIX_G4"; echo "FIX_C2=$FIX_C2"; echo "FIX_C3=$FIX_C3"
} > "$R/01-fixtures.txt"

# ---------------------------------------------------------------- arms
OUTREL=$E/dryout
OUT=$C/$OUTREL

reset_tree() {
  git -C "$C" checkout --quiet -- . 2>/dev/null
  rm -f "$C/$E/dirty-canary.txt" "$C/$E/dryout-extra.txt"
}

run_arm() { # name checkout rev freeze outpre dirty bound
  local name=$1 co=$2 rev=$3 frz=$4 pre=$5 dirty=$6 bound=${7:-}
  local hs=$S/hs-$name rf=$R/$name.txt raw=$R/$name.raw rc
  reset_tree
  git -C "$C" checkout --detach --quiet "$co" || { echo "ARM $name CHECKOUT_FAIL" > "$rf"; return; }
  rm -rf "$OUT"; mkdir -p "$OUT"
  case $pre in
    c1.start) : > "$OUT/c1.start";;
    c2.start) : > "$OUT/c2.start";;
    both) : > "$OUT/c1.start"; : > "$OUT/c2.start";;
  esac
  case $dirty in
    tracked) printf '\nfixture dirty-canary line\n' >> "$C/corpus/SOURCES.md";;
    untracked) : > "$C/$E/dirty-canary.txt";;
    outsuffix) : > "$C/$E/dryout-extra.txt";;
  esac
  rm -rf "$hs"; mkdir -p "$hs"
  {
    echo "ARM $name"
    echo "CMD: bash \$CLONE/$E/deciding-run.sh \$CLONE $rev $frz \$CLONE/$OUTREL"
    echo "HEAD=$(git -C "$C" rev-parse HEAD)  REV=$(git -C "$C" rev-parse "$rev")  FREEZE=$(git -C "$C" rev-parse "$frz")"
    echo "SCRIPT_SHA256=$(sha256sum "$C/$E/deciding-run.sh" | cut -d' ' -f1)"
    echo "OUT_PRE: $(ls -A "$OUT" | tr '\n' ' ')"
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
    else
      wait "$pid"; rc=$?
    fi
  else
    env HYAKU_SCRATCH="$hs" bash "$C/$E/deciding-run.sh" "$C" "$rev" "$frz" "$OUT" > "$raw" 2>&1
    rc=$?
  fi
  {
    echo "EXIT=$rc"
    echo "--- stdout+stderr ---"
    cat "$raw"
    echo "--- refusal lines ---"
    grep -E '^(DECIDING_REFUSED|FREEZE_INTEGRITY|GATE:)' "$raw" || echo '(none)'
    echo "--- OUT after ---"
    ls -A "$OUT" 2>/dev/null | sort | sed 's/^/  /'
    echo "--- OUT receipt-gate ---"
    if [ -f "$OUT/receipt-gate.stdout" ]; then echo "receipt-gate.exit=$(cat "$OUT/receipt-gate.exit" 2>/dev/null)"; cat "$OUT/receipt-gate.stdout"; else echo '(receipt-gate not reached)'; fi
    echo "--- SCR $hs/tameshi-r56/deciding ---"
    if [ -d "$hs/tameshi-r56/deciding" ]; then echo present; else echo absent; fi
    echo "--- ran-anything canary (OUT) ---"
    for f in c1.stdout c2.stdout c1.start c2.start no-harm.stdout no-harm.exit coldread-precheck.stdout census.stdout frozen.stdout; do
      if [ -e "$OUT/$f" ]; then echo "$f=PRESENT"; else echo "$f=absent"; fi
    done
    echo "--- TREE_AFTER ---"
    git -C "$C" status --porcelain
  } >> "$rf"
}

run_arm a1 "$FIX_A1" "$FIX_A1" "$FIX_A1" none none
run_arm a2 "$FIX_A2" "$FIX_A2" "$FIX_A2" none none
run_arm a3 "$FIX_A3" "$FIX_A3" "$FIX_A3" none none
run_arm b  "$FREEZE" "$BASE" "$FREEZE" none none
run_arm c1missing "$FREEZE" "$FREEZE" "$FREEZE" none none
run_arm c2tree "$FIX_C2" "$FIX_C2" "$FREEZE" none none
run_arm c3empty "$FIX_C3" "$FIX_C3" "$FREEZE" none none
run_arm d0 "$FIX_D" "$FIX_D" "$FREEZE" none none 45
run_arm d1 "$FIX_D" "$FIX_D" "$FREEZE" none tracked
run_arm d2 "$FIX_D" "$FIX_D" "$FREEZE" none untracked
run_arm d3 "$FIX_D" "$FIX_D" "$FREEZE" none outsuffix 25
run_arm e1 "$FIX_D" "$FIX_D" "$FREEZE" c1.start none
run_arm e2 "$FIX_D" "$FIX_D" "$FREEZE" c2.start none
run_arm e3 "$FIX_D" "$FIX_D" "$FREEZE" both none
run_arm f  "$FIX_F" "$FIX_F" "$FREEZE" none none
run_arm g1 "$FIX_G1" "$FIX_G1" "$FREEZE" none none
run_arm g2 "$FIX_G2" "$FIX_G2" "$FREEZE" none none
run_arm g4 "$FIX_G4" "$FIX_G4" "$FREEZE" none none
reset_tree
echo "DRIVER_DONE"
