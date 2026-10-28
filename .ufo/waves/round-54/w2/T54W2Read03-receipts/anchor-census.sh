#!/usr/bin/env bash
# Resolve every anchor named inside
#   ### The boundaries — what a service run is not   (SKILL.md 869-893 @ 99c3bc8)
# against the artifacts as they exist at C1. Read-only: git show only.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C=99c3bc88d704566197783f66b211ee0a830e0330
r() { git -C "$LANE" show "$C:$1" | awk -v a="$2" -v b="$3" 'NR>=a&&NR<=b{printf "%4d| %s\n",NR,$0}'; }
echo "== A1 fleet-suite-census.md:288-291 =="; r corpus/knowledge/fleet-suite-census.md 288 291
echo "== A2 SKILL.md:819-820 (porcelain-clean precondition) =="; r SKILL.md 819 820
echo "== A3 tools/mutate-and-run.sh:36-38 =="; r tools/mutate-and-run.sh 36 38
echo "== A3b verbatim quote probe: 'The target is never written' =="
git -C "$LANE" show "$C:tools/mutate-and-run.sh" | grep -cF 'The target is never written'; echo "contiguous-occurrences(0=wrapped only)"
echo "== A4 heading '## Restore discipline' =="; git -C "$LANE" show "$C:SKILL.md" | grep -n '^## Restore discipline'
echo "== A5 mutation-case-mado-verify.md:57-59 =="; r corpus/knowledge/mutation-case-mado-verify.md 57 59
echo "== A6 SKILL.md:346-347 =="; r SKILL.md 346 347
echo "== A7 mado:175-176 =="; r corpus/knowledge/mutation-case-mado-verify.md 175 176
echo "== A8 mado:66-72 =="; r corpus/knowledge/mutation-case-mado-verify.md 66 72
echo "== A9 mado:237-238 =="; r corpus/knowledge/mutation-case-mado-verify.md 237 238
echo "== A9b mado:240-260 =="; r corpus/knowledge/mutation-case-mado-verify.md 240 260
echo "== A10 mado:17-23 =="; r corpus/knowledge/mutation-case-mado-verify.md 17 23
echo "== A11 mado:229-230 (cited for 'sensitivity, not truth') =="; r corpus/knowledge/mutation-case-mado-verify.md 229 230
echo "== A11b control: mado:228-229 (where the clause actually sits) =="; r corpus/knowledge/mutation-case-mado-verify.md 228 229
echo "== A12 matrix row F =="; git -C "$LANE" show "$C:SKILL.md" | grep -n '^| F coordinated edits'
echo "== A11c was this off-by-one introduced this round? (note untouched since round 6) =="
git -C "$LANE" log --oneline -1 -- corpus/knowledge/mutation-case-mado-verify.md
git -C "$LANE" show 59c38109bf11:corpus/knowledge/mutation-case-mado-verify.md | awk 'NR==228||NR==229||NR==230{printf "%4d| %s\n",NR,$0}'
