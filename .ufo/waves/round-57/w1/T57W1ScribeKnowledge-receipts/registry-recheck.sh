#!/usr/bin/env bash
# T57W1ScribeKnowledge: execute the staged gate rows (T57W1ExecRegistryRows/stage) through
# registry-check.py --rev, in a scratch clone of base with the staged registry committed there.
# The lane is only read (git clone --shared); nothing is written to it.
set -u
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r57/T57W1ScribeKnowledge-recheck
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=5e3569969b532310d2b8a3d130901757a3df356b
STAGE=$LANE/.ufo/waves/round-57/w1/T57W1ExecRegistryRows/stage
git clone -q --shared "$LANE" "$S/clone" && git -C "$S/clone" checkout -q --detach "$BASE"
C="$S/clone"
echo "== before: base registry, tag new-r57 (expect could-not-evaluate: no such rows)"
python3 "$C/tools/registry-check.py" --rev "$BASE" --tag new-r57; echo "rc=$?"
cp "$STAGE/tools/registry.json" "$C/tools/registry.json"
mkdir -p "$C/tools/fixtures/receipt-gate" && cp "$STAGE/tools/fixtures/receipt-gate/"* "$C/tools/fixtures/receipt-gate/"
git -C "$C" add tools/registry.json tools/fixtures/receipt-gate
git -C "$C" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "staged gate rows (scratch)"
NEW=$(git -C "$C" rev-parse HEAD)
echo "== after: staged registry at scratch commit $NEW, tag new-r57 (expect held=3/3)"
python3 "$C/tools/registry-check.py" --rev "$NEW" --tag new-r57; echo "rc=$?"
echo "== per-row (--only takes one name)"
for n in receipt-gate-accept receipt-gate-content-drift receipt-gate-unresolvable-certified; do
  python3 "$C/tools/registry-check.py" --rev "$NEW" --only "$n"; echo "rc=$?"
done
echo "== registry-check selftest (scratch only)"
python3 "$C/tools/registry-check.py" --selftest | tail -1; echo "rc=${PIPESTATUS[0]}"
