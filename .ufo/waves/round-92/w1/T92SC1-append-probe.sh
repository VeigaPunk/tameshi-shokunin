#!/usr/bin/env bash
# T92SC1 append-probe — verification-fixture craft for the round-92 case-note
# status addendum draft.
#
# Question this probe answers: if the L1 appends the drafted block
# (.ufo/waves/round-92/w1/T92SC1-addendum.md, between the BEGIN/END APPEND
# BLOCK markers) to corpus/knowledge/mutation-case-fleet-sources-census.md,
# does the sealed round-92 counter still certify the note?
#
# The addendum appends prose to the note, and the note is what the counter
# parses (QUALITY 143's id-set refusal keys on the note's table rows). So an
# appended block can, in principle, break the certificate: a stray table row
# carrying a verdict token, a second `verdict` header, or a second
# `measured:` line would each make the counter refuse an honest note.
# This probe runs the real counter over the real note plus the draft.
#
# Read-only on the lane: the clone is under the seat's scratch; nothing in
# /home/vgpnk/Projects/shokunin is written.
#
# Usage: T92SC1-append-probe.sh [rev]     (default rev = lane tip)

set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
SEAT=/fast/scratch/hyaku/tameshi-r92/T92SC1
ADDENDUM="$LANE/.ufo/waves/round-92/w1/T92SC1-addendum.md"
COUNTER="$LANE/.ufo/evidence/round-92/c1/measure-v92.py"
REV="${1:-$(git -C "$LANE" rev-parse HEAD)}"

mkdir -p "$SEAT"
D=$(mktemp -d -p "$SEAT" fx.XXXXXX) || exit 1
trap 'rm -rf -- "$D"' EXIT

echo "== probe: appending the drafted addendum to the case note =="
echo "lane=$LANE"
echo "rev=$REV"
echo "addendum=$ADDENDUM"
echo "fixture=$D"

# --- extract the append block ------------------------------------------------
python3 - "$ADDENDUM" "$D/block.md" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().split("\n")
try:
    a = next(i for i, l in enumerate(lines) if l.strip() == "=== BEGIN APPEND BLOCK ===")
    b = next(i for i, l in enumerate(lines) if l.strip() == "=== END APPEND BLOCK ===")
except StopIteration:
    sys.exit("FATAL: append-block markers not found in " + src)
block = "\n".join(lines[a + 1:b]).strip("\n")
open(dst, "w", encoding="utf-8").write(block + "\n")
print("block_lines=%d block_bytes=%d" % (block.count("\n") + 1, len(block)))
PY
[ -s "$D/block.md" ] || { echo "FATAL: empty block"; exit 1; }

# --- fixture clone -----------------------------------------------------------
git clone --shared -q "$LANE" "$D/clone" || exit 1
TOP=$(git -C "$D/clone" rev-parse --show-toplevel)
if [ "$TOP" != "$D/clone" ]; then
    echo "FATAL: toplevel $TOP != $D/clone"
    exit 1
fi
git -C "$D/clone" checkout -q "$REV" || exit 1

# --- append the block to the note, commit ------------------------------------
NOTE=corpus/knowledge/mutation-case-fleet-sources-census.md
cp "$D/clone/$NOTE" "$D/note.before"
cat "$D/block.md" >> "$D/clone/$NOTE"
git -C "$D/clone" add -- "$NOTE" || exit 1
git -C "$D/clone" -c user.name=ctl -c user.email=ctl@fixture.invalid \
    commit -q -m "r92 fixture: append the drafted addendum to the case note" || exit 1
FIXREV=$(git -C "$D/clone" rev-parse HEAD)
echo "fixture_rev=$FIXREV"
echo "note_bytes_before=$(wc -c < "$D/note.before") note_bytes_after=$(wc -c < "$D/clone/$NOTE")"

# --- static hazards the counter's parser would punish ------------------------
echo "-- static hazard scan of the appended block --"
python3 - "$D/block.md" <<'PY'
import re, sys
ID_SHAPE = re.compile(r"^[A-Za-z]{1,4}[_-]?[0-9]{1,4}$")
VERDICTS = ("KILLED", "SURVIVED")
nt = open(sys.argv[1], encoding="utf-8").read()
in_fence = False
hdr = 0
bad = []
rows = []
for raw in nt.split("\n"):
    line = raw.strip()
    if line.startswith("```"):
        in_fence = not in_fence
        continue
    if in_fence:
        continue
    cells = [c.strip() for c in raw.split("|")]
    if len(cells) < 3:
        continue
    low = [c.lower() for c in cells]
    if "verdict" in low:
        hdr += 1
        continue
    first = cells[1]
    toks = [c for c in cells if c in VERDICTS]
    shaped = bool(ID_SHAPE.match(first))
    if not toks and not shaped:
        continue
    bad.append("row would be keyed: first=%r toks=%r shaped=%r" % (first, toks, shaped))
print("verdict_headers_in_block=%d" % hdr)
print("measured_lines_in_block=%d" % len(re.findall(r"^measured: (\d+)/(\d+) killed\s*$", nt, re.M)))
print("keyed_rows_in_block=%d" % len(bad))
for b in bad:
    print("  HAZARD " + b)
print("VERDICT_STATIC " + ("clean" if not bad and hdr == 0 else "hazard"))
PY

# --- run the real sealed counter over the fixture ----------------------------
echo "-- sealed counter over the fixture (note + draft) --"
mkdir -p "$D/work"
python3 -I "$COUNTER" --repo "$D/clone" --rev "$FIXREV" --work "$D/work"
echo "counter_exit=$?"

# --- control: the same counter over the un-appended note at the same rev -----
echo "-- sealed counter over the un-appended note at the same rev (control) --"
mkdir -p "$D/work-control"
python3 -I "$COUNTER" --repo "$D/clone" --rev "$REV" --work "$D/work-control"
echo "counter_control_exit=$?"
