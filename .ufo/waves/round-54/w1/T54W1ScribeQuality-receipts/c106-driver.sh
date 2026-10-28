#!/bin/bash
# Criterion-106 falsifier driver (seat T54W1ScribeQuality).
# Question: does the frozen C2 counter notice an eighth caller of
# strict_scratch_root() that violates the contract it claims to enforce?
# Usage: c106-driver.sh LANE REV SCRATCH
#   LANE     absolute lane path (read-only; we clone --shared out of it)
#   REV      the content revision (C0)
#   SCRATCH  an existing writable scratch dir; the fixture is mktemp -d under it
set -u
LANE=$1; REV=$2; SCRATCH=$3
FIXTURE_TOOL=$(dirname "$(readlink -f "$0")")/scratch-consumer.py
[ -r "$FIXTURE_TOOL" ] || { echo "DRIVER_ERROR fixture-tool-missing"; exit 2; }
D=$(mktemp -d "$SCRATCH/c106-fixture.XXXXXX") || exit 2
trap 'rm -rf -- "$D"' EXIT
export TMPDIR="$D/tmp"; mkdir -p "$TMPDIR"
git clone --shared --quiet "$LANE" "$D/lane" || { echo "DRIVER_ERROR clone"; exit 2; }
git -C "$D/lane" checkout --quiet "$REV" || { echo "DRIVER_ERROR checkout"; exit 2; }
TOP=$(git -C "$D/lane" rev-parse --show-toplevel) || exit 2
[ "$TOP" = "$D/lane" ] || { echo "DRIVER_ERROR not-fixture-toplevel $TOP"; exit 2; }
cp "$FIXTURE_TOOL" "$D/lane/tools/scratch-consumer.py"
chmod +x "$D/lane/tools/scratch-consumer.py"
GITENV="GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1"
env $GITENV git -C "$D/lane" add -A || exit 2
env $GITENV git -C "$D/lane" -c user.name=fixture -c user.email=fixture@invalid \
    commit --quiet -m "fixture: an eighth strict_scratch_root() caller with the pre-C0 mapping" || exit 2
FREV=$(git -C "$D/lane" rev-parse HEAD) || exit 2

echo "=== the eighth caller's own behaviour on a set-but-unusable TMPDIR"
UNUSABLE="$D/unusable-tmpdir"
( cd "$D/lane" && TMPDIR="$UNUSABLE" python3 tools/scratch-consumer.py --selftest ) > "$D/eighth.out" 2>&1
echo "eighth-caller rc=$? (contract requires 2, could-not-evaluate, no traceback)"; tail -3 "$D/eighth.out"

echo "=== population as the code carries it, at the fixture revision"
git -C "$D/lane" grep -l 'def strict_scratch_root()' "$FREV" -- 'tools/*.py' | sed 's/^/CALLER /'
N=$(git -C "$D/lane" grep -l 'def strict_scratch_root()' "$FREV" -- 'tools/*.py' | wc -l)
echo "grep-callers=$N"

echo "=== the frozen C2 counter at the fixture revision"
mkdir -p "$D/w"
python3 "$LANE/.ufo/evidence/round-54/c2/measure.py" --lane "$D/lane" --rev "$FREV" --work "$D/w" > "$D/c2.out" 2>&1
RC=$?
echo "c2-exit=$RC"
tail -1 "$D/c2.out"
echo "=== verdict: if the counter still prints tools=7 and C2_R54_PASS=true, the population is a hand-list and the eighth caller is outside the claim"
