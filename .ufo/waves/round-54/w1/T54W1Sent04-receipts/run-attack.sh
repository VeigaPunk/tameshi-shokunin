#!/bin/sh
# T54W1Sent04 attack driver (fixture; runs the FROZEN C2 counter unmodified).
#
# The counter clones --lane at --rev inside --work, so a patch held only in a scratch
# working tree never reaches the tree under test. `git` on PATH is therefore the shim
# in this directory, which applies PATCH to the counter's own fresh clone immediately
# after its checkout and passes every other git invocation through.
#
# Usage: S=<scratch tree> PATCH=<attack patch> WORK=<empty work dir> sh run-attack.sh
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=59c38109bf119d0e9d4f878644a82babc937bc1e
# The lane's c2/measure.py is editable by other seats while this runs, so pin the
# FROZEN counter bytes (blob at the freeze commit 441c26be, sha256 b4684a3f...).
COUNTER=${COUNTER:-$LANE/.ufo/evidence/round-54/c2/measure.py}
: "${S:?S must be the scratch tree}"
: "${PATCH:?PATCH must be the attack patch}"
: "${WORK:?WORK must be an empty work dir}"

mkdir -p "$S/tmp"
export TMPDIR="$S/tmp"
export SHIM_PATCH="$PATCH"
export SHIM_WORK="$WORK"
export PATH="$HERE:$PATH"

echo "== git resolved to: $(command -v git)"
echo "== patch: $(sha256sum "$PATCH")"
echo "== counter under test: $(sha256sum "$COUNTER")"
echo "== lane clean-state check (read-only): git -C LANE rev-parse = $(git -C "$LANE" rev-parse HEAD)"
echo "== RUN: python3 $COUNTER --lane LANE --rev $REV --work $WORK --explain"
python3 "$COUNTER" --lane "$LANE" --rev "$REV" --work "$WORK" --explain
echo "COUNTER_RC=$?"
echo "== tree the counter actually measured (its own clone) — diff against C0:"
git -C "$WORK/clone" diff
echo "== end"
