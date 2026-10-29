#!/usr/bin/env bash
# T57W1ScribeKnowledge: code-by-condition sweep of tools/receipt-revision-gate.py at base.
# Runs the gate's real CLI on a scratch fixture repo (never the lane) and prints, per case,
# the exit code and the verdict line. Read-only on the lane.
set -u
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r57/T57W1ScribeKnowledge
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=5e3569969b532310d2b8a3d130901757a3df356b
git clone -q --shared "$LANE" "$S/clone" && git -C "$S/clone" checkout -q --detach "$BASE"
GATE="$S/clone/tools/receipt-revision-gate.py"
echo "gate sha256: $(sha256sum "$GATE" | cut -c1-64)"

# fixture repo: c0 (surface.txt, moved.txt=alpha) -> c1 (moved.txt=gamma); side branch s from c0
D=$(mktemp -d -p "$S" fx.XXXX)
git -C "$D" init -q -b master
test "$(git -C "$D" rev-parse --show-toplevel)" = "$(realpath "$D")" || { echo "FIXTURE TOPLEVEL MISMATCH"; exit 9; }
G=(git -c user.name=fixture -c user.email=fixture@example.invalid -C "$D")
printf 'alpha\n' > "$D/surface.txt"; printf 'alpha\n' > "$D/moved.txt"
git -C "$D" add -A && "${G[@]}" commit -q -m c0
C0=$(git -C "$D" rev-parse HEAD)
printf 'gamma\n' > "$D/moved.txt"
git -C "$D" add -A && "${G[@]}" commit -q -m c1
C1=$(git -C "$D" rev-parse HEAD)
"${G[@]}" checkout -q -b side "$C0"
printf 'side\n' > "$D/side.txt"; git -C "$D" add -A && "${G[@]}" commit -q -m side
SIDE=$(git -C "$D" rev-parse HEAD)
"${G[@]}" checkout -q master
echo "fixture c0=$C0 c1=$C1 side=$SIDE"
printf 'surface.txt\n' > "$S/paths-surface.txt"
printf 'surface.txt\nmoved.txt\n' > "$S/paths-both.txt"
printf 'VERDICT: rev=%s C1_X_PASS=true\n' "$C0" > "$S/r-c0.txt"
printf 'VERDICT: rev=%s C1_X_PASS=true\n' "$C1" > "$S/r-c1.txt"
printf 'VERDICT: no revision named\n' > "$S/r-absent.txt"
printf 'A rev=%s\nB rev=%s\n' "$C0" "$C1" > "$S/r-ambig.txt"
printf 'VERDICT: rev=deadbeefdead C1_X_PASS=true\n' > "$S/r-unres.txt"
printf 'CTL A rev=%s\nCTL B rev=%s\n' "$C0" "$C1" > "$S/ctl-anc.txt"
printf 'CTL A rev=%s\n' "$SIDE" > "$S/ctl-side.txt"
printf 'VERDICT: rev=%s C1_X_PASS=true\n' "$C0" > "$S/r-digest.txt"; printf '%064d\n' 0 > "$S/r-digest.txt.sha256"
printf 'VERDICT: rev=%s\n' "$C1" > "$S/r-noline.txt"
printf '\n' > "$S/r-empty.txt"
mkdir -p "$S/r-dir"

run() {  # run NAME -- gate args...
  local name=$1; shift; [ "$1" = -- ] && shift
  local out rc
  out=$(python3 "$GATE" "$@" 2>&1); rc=$?
  local verdict codes
  verdict=$(printf '%s\n' "$out" | grep '^GATE: ' | tail -1)
  [ -z "$verdict" ] && verdict="(no GATE verdict line)"
  printf 'CASE %-28s rc=%s | %s\n' "$name" "$rc" "$verdict"
  if [ -z "$(printf '%s\n' "$out" | grep '^GATE: ')" ]; then
    printf '    stderr-tail: %s\n' "$(printf '%s\n' "$out" | tail -1)"
  fi
}

L="$D"; CERT_C1="$C1"
run accept-matched        -- --lane "$L" --certified "$C1" --receipt "$S/r-c1.txt:positive"
run identical-on-paths    -- --lane "$L" --certified "$C1" --paths "$S/paths-surface.txt" --receipt "$S/r-c0.txt:positive"
run drift-on-paths        -- --lane "$L" --certified "$C1" --paths "$S/paths-both.txt" --receipt "$S/r-c0.txt:positive"
run mismatch-no-paths     -- --lane "$L" --certified "$C1" --receipt "$S/r-c0.txt:positive"
run verdict-role-drift    -- --lane "$L" --certified "$C1" --paths "$S/paths-both.txt" --receipt "$S/r-c0.txt:verdict"
run absent                -- --lane "$L" --certified "$C1" --receipt "$S/r-absent.txt:positive"
run ambiguous             -- --lane "$L" --certified "$C1" --receipt "$S/r-ambig.txt:positive"
run unresolvable-receipt  -- --lane "$L" --certified "$C1" --receipt "$S/r-unres.txt:positive"
run control-ancestors     -- --lane "$L" --certified "$C1" --receipt "$S/ctl-anc.txt:control"
run control-not-ancestor  -- --lane "$L" --certified "$C1" --receipt "$S/ctl-side.txt:control"
run digest-mismatch       -- --lane "$L" --certified "$C1" --receipt "$S/r-digest.txt:verdict"
run required-line-missing -- --lane "$L" --certified "$C1" --receipt "$S/r-noline.txt:verdict:C1_X_PASS="
run receipt-missing       -- --lane "$L" --certified "$C1" --receipt "$S/nope.txt:positive"
run receipt-empty         -- --lane "$L" --certified "$C1" --receipt "$S/r-empty.txt:positive"
run receipt-not-blob      -- --lane "$L" --certified "$C1" --receipt "$S/r-dir:positive"
run certified-unresolvable -- --lane "$L" --certified deadbeefdeaddeadbeefdeadbeefdeadbeefdead --receipt "$S/r-c1.txt:positive"
run usage-no-receipt      -- --lane "$L" --certified "$C1"
run paths-file-missing    -- --lane "$L" --certified "$C1" --paths "$S/no-such-paths.txt" --receipt "$S/r-c0.txt:positive"
run json-drift            -- --lane "$L" --certified "$C1" --paths "$S/paths-both.txt" --receipt "$S/r-c0.txt:positive" --json

echo "--- lane-level (real receipts at base; certified as the entry in corpus/knowledge/receipt-revision-binding.md names it)"
LANEG="$GATE"
run lane-ER-R54-1-drift   -- --lane "$LANE" --certified c21081008adb --paths "$LANE/.ufo/evidence/round-56/c2/red-before/round-54-surface.paths" --receipt "$LANE/.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout:positive"
run lane-controls-b-unres -- --lane "$LANE" --certified c21081008adb --receipt "$LANE/.ufo/evidence/round-54/control/controls-b.stdout:positive"
run lane-r55-absent       -- --lane "$LANE" --certified 4c04c1d33377 --receipt "$LANE/.ufo/evidence/round-55/after/c2.stdout:verdict"

echo "--- staged rows (T57W1ExecRegistryRows) run as the registry does: cwd = clone, relative fixture paths"
cp -r "$LANE/.ufo/waves/round-57/w1/T57W1ExecRegistryRows/stage/tools/fixtures" "$S/clone/tools/" 2>/dev/null
mkdir -p "$S/clone/tools/fixtures/receipt-gate" && cp "$LANE/.ufo/waves/round-57/w1/T57W1ExecRegistryRows/stage/tools/fixtures/receipt-gate/"* "$S/clone/tools/fixtures/receipt-gate/"
( cd "$S/clone" && run staged-accept    -- --lane . --certified "$BASE" --receipt tools/fixtures/receipt-gate/accept.receipt:positive
  cd "$S/clone" && run staged-drift     -- --lane . --certified "$BASE" --paths tools/fixtures/receipt-gate/drift.paths --receipt tools/fixtures/receipt-gate/drift.receipt:positive
  cd "$S/clone" && run staged-unresolved -- --lane . --certified deadbeefdeadbeefdeadbeefdeadbeefdeadbeef --receipt tools/fixtures/receipt-gate/accept.receipt:positive )

echo "--- selftest at base bytes"
python3 "$GATE" --selftest | tail -1; echo "selftest rc=${PIPESTATUS[0]}"
