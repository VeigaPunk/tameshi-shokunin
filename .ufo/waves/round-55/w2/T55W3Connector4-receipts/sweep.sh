#!/bin/bash
# T55W3Connector4 — cross-lane lesson-overlap sweep.
# Read-only over sibling lanes. Writes nothing outside this receipts dir.
# Usage: bash sweep.sh <mode>   modes: inventory | classA | classB | all
set -u
FLEET=/home/vgpnk/Projects/shokunin
cd "$FLEET" || exit 2
MODE=${1:-all}

inventory() {
  echo "## corpus of sibling round-5* lesson files"
  echo "# selector: $FLEET/*/corpus/lessons/round-5*.md (tameshi's own excluded from the sweep, listed for scale)"
  total=$(ls */corpus/lessons/round-5*.md 2>/dev/null | wc -l)
  echo "files_total=$total"
  echo "files_other_lanes=$(ls */corpus/lessons/round-5*.md 2>/dev/null | grep -vc '^tameshi-shokunin/')"
  echo
  echo "## per-lane count (other lanes)"
  ls */corpus/lessons/round-5*.md 2>/dev/null | grep -v '^tameshi-shokunin/' | cut -d/ -f1 | sort | uniq -c | sort -rn
  echo
  echo "## same-calendar-week subset (week of 2026-10-26..2026-11-01; tameshi r55 is 2026-10-28, a Wednesday)"
  echo "# a file counts when its latest 2026 date is >= 2026-10-26"
  for f in */corpus/lessons/round-5*.md; do
    d=$(grep -ohE '2026-(10-2[6-9]|11-[0-9]{2})' "$f" 2>/dev/null | sort | tail -1)
    [ -n "$d" ] && echo "$d $f"
  done | grep -v ' tameshi-shokunin/' | sort
  echo
  echo "## date histogram of the whole corpus (top 8)"
  grep -ohE '2026-[0-9]{2}-[0-9]{2}' */corpus/lessons/round-5*.md 2>/dev/null | sort | uniq -c | sort -rn | head -8
}

classA() {
  echo "## CLASS A sweep — a control/check scored at a revision that cannot contain the work it certifies"
  echo "# patterns: predate | strict ancestor | revision it certifies | pre-receipt state | the measured revision | scored at a revision"
  echo "#           cannot represent its positive state | pre-data control freeze omitted | receipts did not name the revision"
  pat='predate|strict ancestor|revision it certifies|pre-receipt state|the measured revision|scored at a revision|cannot represent its positive state|pre-data control freeze omitted|receipts did not name the revision'
  hits=$(grep -nE "$pat" */corpus/lessons/round-5*.md 2>/dev/null | grep -v '^tameshi-shokunin/')
  echo "hits=$(printf '%s\n' "$hits" | grep -c . )"
  echo "files=$(printf '%s\n' "$hits" | cut -d: -f1 | sort -u | grep -c . )"
  echo
  printf '%s\n' "$hits" | cut -c1-240
}

classB() {
  echo "## CLASS B sweep — a predicate that reads a present fact as absent because of typography"
  echo "# patterns: line break | hard-wrapped | wrapped quote | 78 col | stripped[- ]line | exact ... line |"
  echo "#           whitespace-collaps | verbatim | folds line | substring test"
  pat='line ?break|hard-wrapped|wrapped quote|78 col|stripped[- ]line|exact [^|]{0,20}line|whitespace-collaps|verbatim|folds? (a |two |one )?line|substring test'
  hits=$(grep -nE "$pat" */corpus/lessons/round-5*.md 2>/dev/null | grep -v '^tameshi-shokunin/')
  echo "hits=$(printf '%s\n' "$hits" | grep -c . )"
  echo "files=$(printf '%s\n' "$hits" | cut -d: -f1 | sort -u | grep -c . )"
  echo
  printf '%s\n' "$hits" | cut -c1-240
}

case "$MODE" in
  inventory) inventory ;;
  classA)    classA ;;
  classB)    classB ;;
  all)       inventory; echo; classA; echo; classB ;;
  *) echo "unknown mode: $MODE"; exit 2 ;;
esac
