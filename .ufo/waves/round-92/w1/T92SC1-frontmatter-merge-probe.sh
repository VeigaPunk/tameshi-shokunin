#!/usr/bin/env bash
# T92SC1 front-matter-merge probe — arm D of the source-line hazard.
#
# T92SC1-source-line-probe.sh measured arms A/B/C on the note BODY. But the
# integration instruction this seat gives the L1 (integration note 2) is not
# "drop the source: line" — it is "MERGE the S320 clause into the note's
# EXISTING single front-matter `source:` line". That is a different edit to
# the note, and it has to be measured too: the round-90 counter reads
#
#     src = [l for l in nt.split("\n") if l.startswith("source:")]
#     cited = set(re.findall(r"\bS(\d{3,})\b", src[0])) if len(src) == 1 else set()
#
# and then requires, for each cited sid above BASE_MAX_SID (315), a
# SOURCES.md row with status `mined` AND the note path in that row's used-by
# cell. S320's row names only the lesson, so merging S320 into the note's
# front-matter adds a cited sid whose row does not yet name the note.
#
# Arms:
#   D  front-matter `source:` line merged with the S320 clause; SOURCES.md
#      unchanged (S320's used-by still names only the lesson)
#   E  same merge, PLUS S320's used-by cell gains the note path (keeping the
#      lesson path, which the round-92 counter's `source` conjunct requires)
#
# Both arms are then read by BOTH counters: the round-90 one (the note's own
# documented reproduce path) and the round-92 sealed one (the certificate).
#
# Read-only on the lane: clones under the seat's scratch.

set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
SEAT=/fast/scratch/hyaku/tameshi-r92/T92SC1
ADDENDUM="$LANE/.ufo/waves/round-92/w1/T92SC1-addendum.md"
R90="$LANE/.ufo/evidence/round-90/c1/measure.py"
R92="$LANE/.ufo/evidence/round-92/c1/measure-v92.py"
REV="${1:-$(git -C "$LANE" rev-parse HEAD)}"
NOTE=corpus/knowledge/mutation-case-fleet-sources-census.md

mkdir -p "$SEAT"
D=$(mktemp -d -p "$SEAT" fm.XXXXXX) || exit 1
trap 'rm -rf -- "$D"' EXIT

echo "== probe: merging S320 into the note's single front-matter source: line =="
echo "rev=$REV"

S320_CLAUSE='S320 sha256sum(1) — Arch manual pages (GNU coreutils 9.12) (docs, tier A, mined, opened 2026-11-08) — https://man.archlinux.org/man/sha256sum.1.en, `.ufo/evidence/round-92/sources/s320.txt:19`: "Print or check SHA256 (256-bit) checksums." and `s320.txt:53`: "The sums are computed as described in FIPS-180-2." (grounds the counter'"'"'s `SELF_SHA256` self-pin)'

python3 - "$ADDENDUM" "$D" "$S320_CLAUSE" <<'PY'
import sys
src, d, clause = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(src, encoding="utf-8").read().split("\n")
a = next(i for i, l in enumerate(lines) if l.strip() == "=== BEGIN APPEND BLOCK ===")
b = next(i for i, l in enumerate(lines) if l.strip() == "=== END APPEND BLOCK ===")
block = "\n".join(lines[a + 1:b]).strip("\n")
open(d + "/block.md", "w", encoding="utf-8").write(block + "\n")
print("block_lines=%d" % (block.count("\n") + 1))
with open(d + "/clause.txt", "w", encoding="utf-8") as f:
    f.write(clause)
print("clause_bytes=%d" % len(clause))
PY

build_arm() {
    local tag="$1" fix_sources="$2"
    local W="$D/$tag"
    mkdir -p "$W"
    git clone --shared -q "$LANE" "$W/clone" || return 1
    local TOP
    TOP=$(git -C "$W/clone" rev-parse --show-toplevel)
    [ "$TOP" = "$W/clone" ] || { echo "FATAL toplevel $TOP"; return 1; }
    git -C "$W/clone" checkout -q "$REV" || return 1

    # merge the S320 clause into the single front-matter `source:` line
    python3 - "$W/clone/$NOTE" "$D/clause.txt" <<'PY'
import sys
p, clausef = sys.argv[1], sys.argv[2]
clause = open(clausef, encoding="utf-8").read().strip()
lines = open(p, encoding="utf-8").read().split("\n")
n = 0
for i, l in enumerate(lines):
    if l.startswith("source:"):
        lines[i] = l.rstrip() + "; " + clause
        n += 1
        break
assert n == 1, "expected exactly one source: line, found %d" % n
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("  merged_into_front_matter=1")
PY

    # optionally: S320's used-by cell gains the note path (lesson path kept)
    if [ "$fix_sources" = "yes" ]; then
        python3 - "$W/clone/corpus/SOURCES.md" <<'PY'
import re, sys
p = sys.argv[1]
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
LESSON = "corpus/lessons/round-92.md"
lines = open(p, encoding="utf-8").read().split("\n")
hit = 0
for i, l in enumerate(lines):
    raw = l.split("|")
    c = [x.strip() for x in raw]
    if len(c) >= 13 and c[1] == "S320" and c[8] == "mined":
        assert LESSON in c[11], "lesson path missing from S320 used-by"
        assert NOTE not in c[11]
        # rewrite ONLY the used-by cell, preserving every other cell verbatim
        j = 11
        raw[j] = raw[j].replace(c[11], NOTE + ", " + LESSON)
        lines[i] = "|".join(raw)
        hit += 1
assert hit == 1, "expected exactly one S320 row, found %d" % hit
open(p, "w", encoding="utf-8").write("\n".join(lines))
# re-read and assert the result is what the counter will see
back = [x.strip() for x in [l for l in open(p, encoding="utf-8").read().split("\n") if "| S320 |" in l][0].split("|")]
assert LESSON in back[11] and NOTE in back[11], back[11]
print("  sources_usedby_updated=1 used_by=%r" % back[11])
PY
    fi

    cat "$D/block.md" >> "$W/clone/$NOTE"
    git -C "$W/clone" add -- "$NOTE" corpus/SOURCES.md || return 1
    git -C "$W/clone" -c user.name=ctl -c user.email=ctl@fixture.invalid \
        commit -q -m "r92 fixture: arm $tag" || return 1
    local FREV
    FREV=$(git -C "$W/clone" rev-parse HEAD)

    echo "-- arm $tag: source: lines=$(grep -c '^source:' "$W/clone/$NOTE") --"
    mkdir -p "$W/w90" "$W/w92"
    python3 -I "$R90" --repo "$W/clone" --rev "$FREV" --work "$W/w90" > "$W/r90.out" 2>&1
    echo "  r90_exit=$? $(grep -E '^C1_R90_PASS' "$W/r90.out" | head -1)"
    grep -oE 'source=[a-z]+' "$W/r90.out" | head -1 | sed 's/^/  r90 /'
    python3 -I "$R92" --repo "$W/clone" --rev "$FREV" --work "$W/w92" > "$W/r92.out" 2>&1
    echo "  r92_exit=$? $(grep -E '^C1_R92_PASS' "$W/r92.out" | head -1)"
    grep -oE 'source=[a-z]+' "$W/r92.out" | head -1 | sed 's/^/  r92 /'
    grep -oE 'badrows=[0-9]+ headers=[0-9]+' "$W/r92.out" | head -1 | sed 's/^/  r92 /'
}

build_arm D no
build_arm E yes

echo "== summary =="
for t in D E; do
    printf "arm %s: r90=%s r92=%s\n" "$t" \
        "$(grep -E '^C1_R90_PASS' "$D/$t/r90.out" | head -1)" \
        "$(grep -E '^C1_R92_PASS' "$D/$t/r92.out" | head -1)"
done
