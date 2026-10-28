#!/bin/bash
# T55W2RevDocsArms receipt driver: clone the lane at C0 in scratch, then run every
# documentation-arm check. Read-only against the lane; the clone and all outputs of
# the probes live under $HYAKU_SCRATCH.
set -u
export HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
HERE=$(cd "$(dirname "$0")" && pwd)
S=$HYAKU_SCRATCH/tameshi-r55/T55W2RevDocsArms
mkdir -p "$S"
rm -rf "$S/clone"
git clone --shared --no-checkout "$LANE" "$S/clone" -q || exit 1
git -C "$S/clone" checkout -q -B probe "$REV" || exit 1
test "$(git -C "$S/clone" rev-parse HEAD)" = "$REV" || { echo "clone not at $REV"; exit 1; }

for sect in cells diff grammar lazy arms classes; do
  CLONE="$S/clone" python3 "$HERE/arms.py" "$sect" > "$HERE/$sect.txt" 2>&1
  echo "== $sect: exit $?"
done
