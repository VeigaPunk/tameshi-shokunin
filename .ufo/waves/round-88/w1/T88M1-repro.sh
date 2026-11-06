#!/usr/bin/env bash
# T88M1 — rebuild every fixture this probe used, from committed bytes only.
#
#   bash T88M1-repro.sh --build-only     # ~20 s: regenerate mutants/controls, print the matrix
#   bash T88M1-repro.sh                  # build, then run the whole counter matrix (~12 min, 13+11 runs)
#
# Read-only on the lane and on every sibling repo: the only git writes happen in the
# throwaway clone under $S. Frozen artifacts (measure.py, the spec, controls/make-runner.py,
# pre-freeze/) are read, never written.
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
W=$LANE/.ufo/waves/round-88/w1
EV=$LANE/.ufo/evidence/round-88
SPEC=$EV/c1/py-kake-ledger-guard.defects.spec
BASE_REV=f256302b394ae3253df014fe1131e2c20e2c16b6
CAND_REV=28ec58858a084bc193a89ca5b0a751942694ccfb
S=${S:-/fast/scratch/hyaku/tameshi-r88/T88M1-repro}
rm -rf "$S"; mkdir -p "$S/ctrl" "$S/mut" "$S/out" "$S/work"
trap 'echo "scratch: $S"' EXIT

# ---- frozen inputs, by hash -------------------------------------------------
cp "$EV/measure.py" "$S/measure.py"
test "$(sha256sum "$S/measure.py" | cut -d' ' -f1)" = cbb19f09af451d86ddfe8456caa9781575441a1fa31c2c5b29dc5ba2ecf900e9
test "$(sha256sum "$SPEC" | cut -d' ' -f1)" = 724beed385222b6342dc6d3af5ad19ae605bca8101f983f3ce58da905492689e

# ---- throwaway fixture clone at the base revision ---------------------------
git clone --shared -q "$LANE" "$S/ctrl/lane"
L=$S/ctrl/lane
test "$(git -C "$L" rev-parse --show-toplevel)" = "$L"
git -C "$L" -c advice.detachedHead=false checkout -q --detach "$BASE_REV"
git -C "$L" config user.name ctl
git -C "$L" config user.email ctl@fixture.invalid
git -C "$L" config commit.gpgsign false
git -C "$L" show HEAD:tools/mutate-and-run.sh > "$S/base-runner.sh"
git -C "$L" show "$CAND_REV:tools/mutate-and-run.sh" > "$S/cand-runner.sh"
test "$(sha256sum "$S/base-runner.sh" | cut -d' ' -f1)" = 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
git -C "$FLEET/kagi-shokunin" show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh > "$S/driftpins.sh"

# ---- mutants + controls (all sources committed next to T88M1.md) ------------
python3 "$W/T88M1-make-mutants.py" "$S/measure.py" "$S/mut" > "$S/mutants.log"
for i in 1 2 3 4 5 6 7 8; do
  cmp -s "$S/mut/T88M1-M$i.py" "$W/T88M1-M$i.py" || { echo "M$i differs from committed bytes"; exit 1; }
done
for v in lanetarget cmp dup unprereg doctored trivial forged; do
  python3 "$EV/controls/make-runner.py" "$S/base-runner.sh" "$S/ctrl/runner-$v.sh" "$v" --spec "$SPEC"
done
for v in badpin forged-badpin lie-badpin; do
  python3 "$W/T88M1-make-extra.py" "$S/base-runner.sh" "$S/ctrl/runner-$v.sh" "$v" --spec "$SPEC"
done
python3 "$W/T88M1-make-round88-shape.py" "$S/cand-runner.sh" "$S/ctrl/runner-dup11.sh" dup11
python3 "$W/T88M1-make-round88-shape.py" "$S/cand-runner.sh" "$S/ctrl/runner-inert.sh" inert "$S/driftpins.sh"

# control bytes are the identity that matters (fixture commit ids are per-run)
sha256sum "$S"/ctrl/runner-*.sh | sed "s|$S/ctrl/||" | sort > "$S/controls.sha256"
cat "$S/controls.sha256"

# ---- one commit per variant, then run the matrix ----------------------------
: > "$S/revs.txt"
for v in lanetarget cmp dup unprereg doctored trivial badpin dup11 inert forged forged-badpin lie-badpin; do
  install -m 0755 "$S/ctrl/runner-$v.sh" "$L/tools/mutate-and-run.sh"
  want=$(sha256sum "$S/ctrl/runner-$v.sh" | cut -d' ' -f1)
  git -C "$L" add -- tools/mutate-and-run.sh
  git -C "$L" commit -q -m "t88m1 control: runner variant $v (sha256 $want)"
  rev=$(git -C "$L" rev-parse HEAD)
  test "$(git -C "$L" show "$rev:tools/mutate-and-run.sh" | sha256sum | cut -d' ' -f1)" = "$want"
  echo "$v $rev sha256=$want" >> "$S/revs.txt"
done
cat "$S/revs.txt"
if [[ ${1-} == --build-only ]]; then echo BUILD_ONLY_OK; exit 0; fi

rev() { awk -v v="$1" '$1==v{print $2}' "$S/revs.txt"; }
run() { # <tag> <counter> <rev>
  tag=$1; counter=$2; crev=$3; w="$S/work/$tag"
  rm -rf "$w"; mkdir -p "$w"
  ( python3 -I "$counter" --repo "$L" --rev "$crev" --fleet "$FLEET" --work "$w" \
      >"$S/out/$tag.out" 2>"$S/out/$tag.err"; echo "EXIT=$?" >>"$S/out/$tag.out" ) &
}
run M1               "$S/mut/T88M1-M1.py" "$(rev lanetarget)"
run M2               "$S/mut/T88M1-M2.py" "$(rev cmp)"
run M3               "$S/mut/T88M1-M3.py" "$(rev dup)"
run M3-dup11         "$S/mut/T88M1-M3.py" "$(rev dup11)"
run M4               "$S/mut/T88M1-M4.py" "$(rev unprereg)"
run M5               "$S/mut/T88M1-M5.py" "$(rev doctored)"
run M5-forged        "$S/mut/T88M1-M5.py" "$(rev forged)"
run M6               "$S/mut/T88M1-M6.py" "$(rev trivial)"
run M6-inert         "$S/mut/T88M1-M6.py" "$(rev inert)"
run M8-badpin        "$S/mut/T88M1-M8.py" "$(rev badpin)"
run M8-forgedbadpin  "$S/mut/T88M1-M8.py" "$(rev forged-badpin)"
run M8-liebadpin     "$S/mut/T88M1-M8.py" "$(rev lie-badpin)"
run FROZEN-cmp       "$S/measure.py"      "$(rev cmp)"
run FROZEN-dup11     "$S/measure.py"      "$(rev dup11)"
run FROZEN-inert     "$S/measure.py"      "$(rev inert)"
run FROZEN-forged    "$S/measure.py"      "$(rev forged)"
run FROZEN-badpin    "$S/measure.py"      "$(rev badpin)"
run FROZEN-forgedbadpin "$S/measure.py"   "$(rev forged-badpin)"
run FROZEN-liebadpin "$S/measure.py"      "$(rev lie-badpin)"
wait
grep -H '^C1_R88 ' "$S"/out/*.out | sed "s|$S/out/||;s/ rev=[0-9a-f]*//"
