#!/bin/bash
# T55W3Connector4 — recall check on the sweep: the mistake-class *vocabulary*
# each sibling lane uses in its round-5* lessons. A class recorded under a name
# my two regex families miss would show up here as an unexamined label.
set -u
cd /home/vgpnk/Projects/shokunin || exit 2
echo "## mistake-class labels in sibling round-5* lessons (label<TAB>count<TAB>lanes)"
{
  grep -hoE '^\- \*\*class: [^.]{3,80}' */corpus/lessons/round-5*.md 2>/dev/null |
    sed 's/^- \*\*class: //'
  grep -hE '^\| *[a-z][a-z0-9-]{2,30} *\|' */corpus/lessons/round-5*.md 2>/dev/null |
    awk -F'|' '{gsub(/^ +| +$/,"",$2); print $2}'
  grep -hoE '\*\*M[0-9]+[a-z]? — [a-zA-Z-]+' */corpus/lessons/round-5*.md 2>/dev/null |
    sed 's/^\*\*M[0-9]*[a-z]* — //'
} | grep -v '^tameshi' | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn | head -60
echo
echo "## labels whose name is in the neighbourhood of either class:"
{
  grep -hoE '^\- \*\*class: [^.]{3,90}' */corpus/lessons/round-5*.md 2>/dev/null | sed 's/^- \*\*class: //'
  grep -hE '^\| *[a-z][a-z0-9-]{2,30} *\|' */corpus/lessons/round-5*.md 2>/dev/null | awk -F'|' '{gsub(/^ +| +$/,"",$2); print $2}'
} | tr 'A-Z' 'a-z' | grep -E 'stale|predat|revision|shape|wrap|line|typograph|verbatim|reproduc|premise|vacuous|order' | sort | uniq -c | sort -rn
echo
echo "## lanes contributing labels (sanity: taxonomy is a fleet-wide practice)"
grep -lE '^\- \*\*class: |^\| *[a-z][a-z0-9-]{2,30} *\|' */corpus/lessons/round-5*.md 2>/dev/null |
  cut -d/ -f1 | sort | uniq -c | sort -rn
