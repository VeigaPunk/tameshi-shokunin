#!/bin/bash
# T89C1 driver: score the counterfeit witness with the FROZEN R89-C1 counter.
# Nothing in the lane repo is written; the fixture repo lives under scratch and is
# removed on exit. Usage (no args): bash T89C1-counterfeit-witness-measure.sh
set -uo pipefail
S=/fast/scratch/hyaku/tameshi-r89/T89C1
trap 'rm -rf -- "$S"' EXIT
rm -rf -- "$S"; mkdir -p "$S"
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
BASE=61990f3d8cd99932bfb0575e1c292e03d310b436
D=$S/fx
mkdir -p "$D" || exit 2
git -C "$D" init -q || exit 2
TOP=$(git -C "$D" rev-parse --show-toplevel) || exit 2
[[ "$TOP" == "$D" ]] || { echo "toplevel mismatch: $TOP != $D"; exit 2; }
mkdir -p "$D/tools" "$D/.ufo/evidence/round-89/controls" "$D/.ufo/waves/round-88/w1"
WIT=${WIT:-$(dirname "$0")/T89C1-counterfeit-witness.py}
cp "$WIT" "$D/tools/ledger-witness.py" || exit 2
git -C "$LANE" show "$BASE:tools/mutate-and-run.sh" > "$D/tools/mutate-and-run.sh" || exit 2
cp "$LANE/.ufo/evidence/round-89/controls/make-forgeries.py" "$D/.ufo/evidence/round-89/controls/" || exit 2
cp "$LANE/.ufo/waves/round-88/w1/T88E2-make-variants.py" "$D/.ufo/waves/round-88/w1/" || exit 2
printf '%s\n' '# fixture SCORECARD (capability row only)' '' \
  '| Capability | State | Evidence |' '|---|---|---|' \
  '| ledger witness | claimed | C1_R89 |' > "$D/SCORECARD.md"
git -C "$D" add -A || exit 2
git -C "$D" -c user.name=ctl -c user.email=ctl@fixture.invalid commit -q -m "ctl" || exit 2
REV=$(git -C "$D" rev-parse HEAD) || exit 2
W=$S/w; mkdir -p "$W"
echo "== fixture rev=$REV witness_sha256=$(sha256sum "$D/tools/ledger-witness.py" | cut -c1-64)"
echo "== command: bash $LANE/.ufo/evidence/round-89/measure.sh $D $REV $FLEET $W"
bash "$LANE/.ufo/evidence/round-89/measure.sh" "$D" "$REV" "$FLEET" "$W"
echo "C1_R89_COUNTER_EXIT=$?"
