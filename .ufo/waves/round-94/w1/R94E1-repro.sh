#!/usr/bin/env bash
# R94E1 independent reproduction of the 12 fleet-gate census mutants,
# OUTSIDE the frozen counter (measure-v94.py is never imported or run for the
# mutant execution). Each mutant's exact old->new edit is applied to a pristine
# copy of scripts/sources-census.sh @ f47ad6ba, then `selftest` is run twice
# in the ordinary shell environment (no env -i). Verdict: rc 0 = SURVIVED,
# rc != 0 = KILLED. Finally the frozen counter is run once at the instrument
# revision and its stdout is saved for the deliverable table.
set -u
S=/fast/scratch/hyaku/tameshi-r94/R94E1
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
SPEC=$LANE/.ufo/evidence/round-94/c1/census-mutants.json
GATE_COMMIT=f47ad6ba8d306f8125597401cb2ce45c1297a593
INSTRUMENT=7084358c732ebe1334c2eb9a352c3ed96b547f7c
COUNTER=$LANE/.ufo/evidence/round-94/c1/measure-v94.py

  W=$(mktemp -d -p "$S" cw.XXXXXX)
  mkdir -p "$S/runs"
  cd "$S"

# --- pristine copy (exact materialization mandated by the seat spec) ---
D=$S/g
rm -rf "$D"; mkdir -p "$D/scripts"
git -C "$FLEET" archive --format=tar "$GATE_COMMIT" scripts/fixtures/sources-census | tar -x -C "$D"
git -C "$FLEET" show "$GATE_COMMIT:scripts/sources-census.sh" > "$D/scripts/sources-census.sh"
chmod 755 "$D/scripts/sources-census.sh"

# --- pristine baseline selftest ---
bash "$D/scripts/sources-census.sh" selftest > "$S/runs/pristine.out" 2>&1
PRISTINE_RC=$?
echo "pristine rc=$PRISTINE_RC" | tee "$S/runs/pristine.rc"
if [ "$PRISTINE_RC" -ne 0 ]; then echo "FATAL: pristine selftest not green"; exit 1; fi
grep -q '^selftest ok$' "$S/runs/pristine.out" || { echo "FATAL: pristine output lacks 'selftest ok'"; exit 1; }

RESULTS=$S/repro-results.tsv
printf 'id\trc_run1\trc_run2\tverdict\tarmline\n' > "$RESULTS"

for ID in C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12; do
  # apply the mutant's exact old->new edit with our own code; assert exactly once
  python3 -I - "$SPEC" "$ID" "$S/g" "$S" <<'PY'
import json, sys, shutil, os
spec_path, mid, pristine_root, S = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
spec = json.load(open(spec_path))
m = next(x for x in spec["mutants"] if x["id"] == mid)
case = os.path.join(S, "case-" + mid)
if os.path.exists(case): shutil.rmtree(case)
shutil.copytree(pristine_root, case)
gate = os.path.join(case, "scripts", "sources-census.sh")
text = open(gate, encoding="utf-8").read()
n = text.count(m["old"])
if n != 1:
    print(f"{mid}: FATAL old occurs {n} times (expected 1)", file=sys.stderr); sys.exit(1)
open(gate, "w", encoding="utf-8").write(text.replace(m["old"], m["new"]))
print(f"{mid}: edit applied exactly once")
PY
  if [ "$?" -ne 0 ]; then echo "$ID EDIT-FAILED"; printf '%s\tEDITFAIL\tEDITFAIL\t-\t-\n' "$ID" >> "$RESULTS"; continue; fi
  CASE=$S/case-$ID
  bash "$CASE/scripts/sources-census.sh" selftest > "$S/runs/$ID-run1.out" 2>&1; RC1=$?
  bash "$CASE/scripts/sources-census.sh" selftest > "$S/runs/$ID-run2.out" 2>&1; RC2=$?
  if [ "$RC1" -eq 0 ]; then V1=SURVIVED; else V1=KILLED; fi
  VERDICT=$V1
  if [ "$RC1" -ne "$RC2" ]; then VERDICT="UNSTABLE($RC1/$RC2)"; fi
  # arm lines that differ from pristine output (run1)
  DIFF=$(diff "$S/runs/pristine.out" "$S/runs/$ID-run1.out" | grep -E '^[<>]' | sed 's/^[<>] //' | tr '\n' '|' | sed 's/|$//') || true
  [ -z "$DIFF" ] && DIFF="(no output difference)"
  printf '%s\t%s\t%s\t%s\t%s\n' "$ID" "$RC1" "$RC2" "$VERDICT" "$DIFF" >> "$RESULTS"
  echo "$ID rc1=$RC1 rc2=$RC2 verdict=$VERDICT"
  echo "  differing arm lines vs pristine: $DIFF"
done

echo "=== results ==="; cat "$RESULTS"

# --- frozen counter, once, at the instrument revision ---
  python3 -I "$COUNTER" --repo "$LANE" --rev "$INSTRUMENT" --work "$W" > "$S/counter.out" 2>&1
CRC=$?
echo "counter exit=$CRC" | tee "$S/counter.rc"
cat "$S/counter.out"
echo "DONE results=$RESULTS counter_out=$S/counter.out"
