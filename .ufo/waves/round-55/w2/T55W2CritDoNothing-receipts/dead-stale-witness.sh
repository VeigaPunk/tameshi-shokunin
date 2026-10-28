#!/bin/bash
# T55W2CritDoNothing: does the pre-registered control set detect a DEAD stale scan?
# Builds C0 + one stale assertion reintroduced outside the corrections section, then scores it
# with (a) the frozen counter and (b) the same counter with scan() forced to return no hits.
# Then re-scores the three phase-A C1 controls with the dead-scan counter.
set -u
S=${1:?usage: dead-stale-witness.sh SCRATCHDIR}
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
FROZEN=$S/code-f5/c1/measure.py
MUT=$S/code-mutant/c1/measure.py
mkdir -p "$S/code-mutant/c1"
python3 - "$FROZEN" "$MUT" <<'PY'
import sys
src = open(sys.argv[1]).read()
# `rx = re.compile(pattern)` opens both scan() and scan_span(); deaden ONLY scan().
i = src.index("def scan(lane, rev, paths, pattern):")
j = src.index("def scan_span(")
head, mid, tail = src[:i], src[i:j], src[j:]
old = "    rx = re.compile(pattern)\n    hits = []"
assert mid.count(old) == 1, mid.count(old)
open(sys.argv[2], "w").write(
    head + mid.replace(old, old + "\n    return hits  # MUTANT: dead stale arm", 1) + tail)
PY

d=$S/clones/stale-back; rm -rf "$d"
git clone --shared --quiet "$L" "$d" || exit 2
git -C "$d" -c advice.detachedHead=false checkout --quiet "$C0" || exit 2
[ "$(git -C "$d" rev-parse --show-toplevel)" = "$(cd "$d" && pwd -P)" ] || { echo TOPLEVEL MISMATCH; exit 2; }
printf '\n## Round 55 stale reintroduction (fixture)\n\nThe phase-B positive control passes and prints `CTL_POS_c1 true`.\n' >> "$d/SCORECARD.md"
git -C "$d" add -A
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git -C "$d" -c user.name=ctl -c user.email=ctl@invalid \
  commit --quiet -m "fixture: one stale assertion back at C0" || exit 2
REV=$(git -C "$d" rev-parse HEAD)
score () { # score COUNTER TAG CLONE
  local w=$S/work-$2; rm -rf "$w"; mkdir -p "$w"
  python3 "$1" --lane "$3" --rev "$(git -C "$3" rev-parse HEAD)" --work "$w" ${4:-} 2>&1 | tail -1
}
echo "fixture rev=$REV"
echo "frozen counter      : $(score "$FROZEN" wit-real "$d")"
echo "dead-scan counter   : $(score "$MUT" wit-mut "$d")"
echo
echo "--- the three pre-registered phase-A C1 controls, re-scored with the DEAD-SCAN counter ---"
echo "CTL_0_c1 (base)     : $(score "$MUT" mut-base "$S/clone-base")"
echo "CTL_SKIP_c1 (skip1) : $(score "$MUT" mut-skip1 "$S/clones/skip1")"
echo "CTL_FAB_c1  (fab1)  : $(score "$MUT" mut-fab1 "$S/clones/fab1")"
echo
echo "expected with the frozen counter: CTL_0_c1 total=10 false, SKIP total=6 false, FAB total=10 false."
echo "If every line above still reads PASS=false, no phase-A C1 control distinguished the mutation."
