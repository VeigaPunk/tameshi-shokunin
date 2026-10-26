#!/bin/bash
# Round 50: commit the selftest receipts that routed items R45.2 and R47.2 asked for and that no round committed.
# Usage: run-receipts.sh LANE REV OUTDIR. Runs every command in a scratch clone at REV (the round-47 falsifiers
# write fixture repos), never in the lane; each receipt is <name>.selftest.stdout / .stderr / .exit.
set -u
LANE=$1; REV=$2; OUT=$3
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r50/routed-receipts
rm -rf "$S"; mkdir -p "$S" "$OUT"; trap 'rm -rf -- "$S"' EXIT
git clone -q --shared "$LANE" "$S/lane" && git -C "$S/lane" checkout -q --detach "$REV" || exit 2
[ "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane" ] || exit 2
echo "rev=$(git -C "$S/lane" rev-parse HEAD)" > "$OUT/revision.txt"
run() { name=$1; shift; (cd "$S/lane" && TMPDIR="$S" "$@") > "$OUT/$name.selftest.stdout" 2> "$OUT/$name.selftest.stderr"; echo $? > "$OUT/$name.selftest.exit"; echo "$name exit=$(cat "$OUT/$name.selftest.exit") $(tail -1 "$OUT/$name.selftest.stdout")"; }
# R45.2: both round-45 counters
run r45-c1-freshness python3 .ufo/evidence/round-45/freshness/measure.py --selftest
run r45-c2-coverage python3 .ufo/evidence/round-45/coverage/measure.py --selftest
# R47.2: the three round-47 counters, addition-lint.py and the criterion-93 falsifier block
run r47-c1-measure python3 .ufo/evidence/round-47/calibration/measure.py --selftest
run r47-c2-pool python3 .ufo/evidence/round-47/hardening/pool.py --selftest
run r47-c3-coverage python3 .ufo/evidence/round-47/coverage/measure.py --selftest
run r47-addition-lint python3 .ufo/evidence/round-47/quality/addition-lint.py --selftest
run r47-falsifiers bash .ufo/evidence/round-47/quality/falsifiers.sh
