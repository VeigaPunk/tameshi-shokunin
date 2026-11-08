#!/usr/bin/env bash
# T91S2 — census-shape check for the proposed S319 row.
#
# READ-ONLY with respect to the lane and to fleet scripts/. It copies the
# lane's corpus/ and tools/ into a scratch dir, inserts the proposed S319 row
# into the COPY's registry table, creates the copy's corpus/lessons/round-91.md,
# and runs the real fleet gate
# (/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate) against
# the copy. The lane's own corpus/SOURCES.md is never touched.
#
# Usage:  bash T91S2-census-row-check.sh [SCRATCH]
# Output: the gate's findings for the S319 row, plus a baseline-vs-with-row
#         error diff.
set -u

SCRATCH="${1:-/fast/scratch/hyaku/tameshi-r91/T91S2}"
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
GATE=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
mkdir -p "$SCRATCH"
L="$SCRATCH/lanecopy"
rm -rf "$L"; mkdir -p "$L"
cp -r "$LANE/corpus" "$L/corpus"
cp -r "$LANE/tools" "$L/tools" 2>/dev/null
cp -r "$LANE/considerthese" "$L/considerthese" 2>/dev/null

echo "=== baseline: lane copy WITHOUT the proposed row ==="
bash "$GATE" validate --today 2026-11-08 --file "$L/corpus/SOURCES.md" > "$SCRATCH/base.out" 2>&1
echo "baseline_exit=$?"
grep -cE '	E[0-9]+	' "$SCRATCH/base.out" | sed 's/^/baseline_E_codes=/'

python3 - "$L/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]
row = ("| S319 | git-replace(1) — https://git-scm.com/docs/git-replace | docs | A | "
"the replacement-ref mechanics the sealed C1 counter's read path depends on: `git replace` writes a ref under the `refs/replace/` namespace and `git replace -l` lists those refs, so a non-empty list means a git object read may be served a substitute | "
"§DESCRIPTION, the \"Adds a replace reference in refs/replace/ namespace.\" sentence, tag-stripped line 1661 of `sed 's/<[^>]*>//g'` over the saved page @ page fetched 2026-11-08 03:29:24 GMT (HTTP 200, 38351 B, sha256 70ca75f4…); snapshot .ufo/waves/round-91/w1/T91S2-git-replace.html, text .ufo/waves/round-91/w1/T91S2-git-replace.txt | "
"a replace ref is named for the replaced object and holds the replacement object, so `git replace -l` is the read that reveals substitution and the counter refuses on a non-empty list rather than trusting it | "
"mined | 2026-11-08 | 365d | corpus/lessons/round-91.md |\n")
cells = [c for c in row.split("|")]
assert all("|" not in c for c in cells[1:-1]), "a cell contains a pipe"
lines = open(p).read().split("\n")
idx = max(i for i, l in enumerate(lines) if l.startswith("| S"))
lines.insert(idx + 1, row)
open(p, "w").write("\n".join(lines))
print("inserted S319 after registry line", idx + 1)
PY

echo "=== with the row, lesson corpus/lessons/round-91.md ABSENT ==="
bash "$GATE" validate --today 2026-11-08 --file "$L/corpus/SOURCES.md" 2>&1 | grep -E 'S319' || true

echo "=== with the row, lesson PRESENT ==="
printf '# round 91 lesson (placeholder)\n' > "$L/corpus/lessons/round-91.md"
bash "$GATE" validate --today 2026-11-08 --file "$L/corpus/SOURCES.md" > "$SCRATCH/with-s319.out" 2>&1
echo "with_row_exit=$?"
grep -E 'S319' "$SCRATCH/with-s319.out" || echo "(no S319 finding)"
grep -E '	E[0-9]+	' "$SCRATCH/with-s319.out" | sort > "$SCRATCH/e2"
grep -E '	E[0-9]+	' "$SCRATCH/base.out" | sort > "$SCRATCH/e1"
if diff -q "$SCRATCH/e1" "$SCRATCH/e2" >/dev/null; then echo "NO_NEW_ERRORS"; else
  echo "NEW ERRORS:"; diff "$SCRATCH/e1" "$SCRATCH/e2"; fi
