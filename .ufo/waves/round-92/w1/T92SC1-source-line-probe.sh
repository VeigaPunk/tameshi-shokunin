#!/usr/bin/env bash
# T92SC1 source-line probe — the round-90 counter's `source:`-line conjunct
# vs the round-92 addendum draft.
#
# The round-92 sealed counter does NOT read the note's `source:` line (it
# reads the SOURCES.md row for S320 and the round-92 lesson). But the
# round-90 counter — the one the note's own §5 "Reproduce" section tells a
# reader to run — does read it:
#
#     measure.py:232  src = [l for l in nt.split("\n") if l.startswith("source:")]
#     measure.py:233  cited = set(re.findall(r"\bS(\d{3,})\b", src[0])) if len(src) == 1 else set()
#
# `len(src) == 1` — so a note carrying a SECOND line that starts with
# "source:" makes the round-90 counter cite nothing and drop its `source`
# conjunct. The note's documented reproduce path would stop printing
# C1_R90_PASS=true at the landing revision.
#
# Arms (all scratch clones of the lane; the lane itself is read-only):
#
#   A  the note as committed                              (baseline)
#   B  the note + a block carrying its own `source:` line  (the hazard)
#   C  the note + the actual addendum draft block         (the shipped shape)
#
# Arm B SYNTHESIZES the hazard rather than depending on the draft's current
# shape, so the probe measures the same thing whichever form the draft is
# in — and so its output stays valid after the draft is revised.
#
# Read-only on the lane: clones under the seat's scratch.

set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
SEAT=/fast/scratch/hyaku/tameshi-r92/T92SC1
ADDENDUM="$LANE/.ufo/waves/round-92/w1/T92SC1-addendum.md"
R90_COUNTER="$LANE/.ufo/evidence/round-90/c1/measure.py"
REV="${1:-$(git -C "$LANE" rev-parse HEAD)}"

mkdir -p "$SEAT"
D=$(mktemp -d -p "$SEAT" src.XXXXXX) || exit 1
trap 'rm -rf -- "$D"' EXIT

echo '== probe: the round-90 counter source-line conjunct vs the draft =='
echo "rev=$REV"
echo "r90_counter=$R90_COUNTER"

python3 - "$ADDENDUM" "$D" <<'PY'
import sys
src, d = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().split("\n")
a = next(i for i, l in enumerate(lines) if l.strip() == "=== BEGIN APPEND BLOCK ===")
b = next(i for i, l in enumerate(lines) if l.strip() == "=== END APPEND BLOCK ===")
block = "\n".join(lines[a + 1:b]).strip("\n")
open(d + "/block-draft.md", "w", encoding="utf-8").write(block + "\n")
# the hazard, synthesised: the same block but opening with its own
# `source:` line — the shape the draft had before it was revised
hazard = "source: S999 fabricated(1) (docs, tier A, mined, opened 2026-11-08) — https://example.invalid/x\n\n" + block
open(d + "/block-hazard.md", "w", encoding="utf-8").write(hazard + "\n")
print("draft_block_lines=%d source_lines=%d" % (
    block.count("\n") + 1, sum(1 for l in block.split("\n") if l.startswith("source:"))))
print("hazard_block_lines=%d source_lines=%d" % (
    hazard.count("\n") + 1, sum(1 for l in hazard.split("\n") if l.startswith("source:"))))
PY

NOTE=corpus/knowledge/mutation-case-fleet-sources-census.md

run_arm() {
    local tag="$1" blockfile="$2"
    local W="$D/$tag"
    mkdir -p "$W"
    git clone --shared -q "$LANE" "$W/clone" || return 1
    local TOP
    TOP=$(git -C "$W/clone" rev-parse --show-toplevel)
    if [ "$TOP" != "$W/clone" ]; then echo "FATAL: toplevel $TOP"; return 1; fi
    git -C "$W/clone" checkout -q "$REV" || return 1
    local FREV="$REV"
    if [ -n "$blockfile" ]; then
        cat "$blockfile" >> "$W/clone/$NOTE"
        git -C "$W/clone" add -- "$NOTE" || return 1
        git -C "$W/clone" -c user.name=ctl -c user.email=ctl@fixture.invalid \
            commit -q -m "r92 fixture: arm $tag" || return 1
        FREV=$(git -C "$W/clone" rev-parse HEAD)
    fi
    echo "-- arm $tag: source: lines in the note = $(grep -c '^source:' "$W/clone/$NOTE") --"
    mkdir -p "$W/work"
    python3 -I "$R90_COUNTER" --repo "$W/clone" --rev "$FREV" --work "$W/work" \
        > "$W/r90.out" 2>&1
    echo "arm=$tag r90_exit=$?"
    grep -E '^C1_CONJUNCTS' "$W/r90.out" | grep -oE 'source=[a-z]+' | sed 's/^/   /'
    grep -E '^C1_R90_PASS' "$W/r90.out" | sed 's/^/   /'
}

run_arm A ""
run_arm B "$D/block-hazard.md"
run_arm C "$D/block-draft.md"

echo '== summary =='
for t in A B C; do
    if [ -f "$D/$t/r90.out" ]; then
        printf 'arm %s: %s (source=%s)\n' "$t" \
            "$(grep -E '^C1_R90_PASS' "$D/$t/r90.out" | head -1)" \
            "$(grep -oE 'source=[a-z]+' "$D/$t/r90.out" | head -1)"
    fi
done
