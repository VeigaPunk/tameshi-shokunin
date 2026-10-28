#!/bin/bash
# T55W2RevRound54Wording — read-only attack driver over corpus/lessons/round-54.md at C0.
# No lane writes, no git mutations: git show / ls-tree / log only.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
BASE=$(git -C "$LANE" rev-parse "$C0^")
PKG=/home/vgpnk/Projects/shokuknow/merge/tameshi
F=corpus/lessons/round-54.md

echo "### 0. revisions"
echo "C0=$C0 base=$BASE"
git -C "$LANE" log -1 --format='C0 %H %ad %s' --date=iso "$C0"
git -C "$LANE" log -1 --format='base %H %ad %s' --date=iso "$BASE"

echo
echo "### A. the three edits in $F between base and C0"
git -C "$LANE" diff "$BASE" "$C0" -- "$F"

echo
echo "### B1. staged-count edit: my count of the package"
python3 - "$PKG" <<'PY'
import json, os, sys, collections
pkg = sys.argv[1]
d = json.load(open(os.path.join(pkg, 'MERGE-REPORT.json')))
e = d['entries']
print('MERGE-REPORT.json entries =', len(e), ' accepted =', len(d['accepted']), ' refused =', len(d['refused']))
print('kinds =', dict(collections.Counter(x['kind'] for x in e)))
files = []
for r, _, fs in os.walk(os.path.join(pkg, 'knowledge')):
    files += [os.path.join(r, f) for f in fs if f.endswith('.md')]
print('*.md under merge/tameshi/knowledge (recursive) =', len(files))
print('*.md under merge/tameshi (recursive, all) =', sum(1 for r, _, fs in os.walk(pkg) for f in fs if f.endswith('.md')))
names = {os.path.basename(f): f for f in files}
print('adopted-by-round-53 entry still on disk: change-aware-resweep-cadence.md ->', 'change-aware-resweep-cadence.md' in names)
print('named rejected entry on disk: delta-debugging-minimization-contract.md ->', 'delta-debugging-minimization-contract.md' in names)
for x in e:
    if x['kind'] == 'amendment':
        print('amendment entry target', x['target'], '| payload present under knowledge/?', os.path.basename(x['target']) in names)
print('arithmetic:')
print('  entries 86 - 1 adopted in round 53            = ', 86 - 1, '(round-53 "other 85", SCORECARD Planned(round 54) "85 unadopted")')
print('  that set - 1 named in round 54 (delta)        = ', 85 - 1, '(the pre-edit value 84)')
print('  files under knowledge - 1 named in round 54   = ', len(files) - 1, '(the post-edit value 80)')
PY

echo
echo "### B2. round-53's own staged-set sentence and SCORECARD Planned(round 54)"
git -C "$LANE" show "$C0:corpus/lessons/round-53.md" | grep -n "other 85 staged"
git -C "$LANE" show "$C0:SCORECARD.md" | grep -n "85 unadopted"
echo "--- ER-R54-9 as committed ---"
git -C "$LANE" show "$C0:SCORECARD.md" | sed -n '/ER-R54-9/,/^$/p'
echo "--- MERGE-REPORT.md header claim ---"
grep -n "proposed knowledge entries" "$PKG/MERGE-REPORT.md"

echo
echo "### C1. R53.1 edit: the receipts the new sentences cite"
echo "--- control/controls-b.stdout (phase-B control) ---"
git -C "$LANE" show "$C0:.ufo/evidence/round-54/control/controls-b.stdout"
echo "--- after/c1.stdout (deciding revision) ---"
git -C "$LANE" show "$C0:.ufo/evidence/round-54/after/c1.stdout"
echo "--- after/frozen.stdout ---"
git -C "$LANE" show "$C0:.ufo/evidence/round-54/after/frozen.stdout"
echo "--- after/c1.start (deciding run opened) ---"
git -C "$LANE" show "$C0:.ufo/evidence/round-54/after/c1.start"
echo "--- commit that put controls-b in the tree ---"
git -C "$LANE" log -1 --format='%h %ad %s' --date=iso -- .ufo/evidence/round-54/control/controls-b.stdout

echo
echo "### C2. the dropped tokens, before and after"
echo "--- at $BASE ---"
git -C "$LANE" show "$BASE:$F" | grep -n -E "positive control|rekeyed=7/7|CTL_POS_c1"
echo "--- at $C0 ---"
git -C "$LANE" show "$C0:$F" | grep -n -E "positive control|rekeyed=7/7|CTL_POS_c1|rekeyed=3/7|7 of 7"

echo
echo "### D. untouched bullet R53.5 vs the round's own freeze"
echo "--- lesson R53.5 bullet at $C0 ---"
git -C "$LANE" show "$C0:$F" | sed -n '/R53.5/,+3p'
echo "--- freeze.json amendment count at each freeze commit ---"
for r in 441c26b 077d431; do
  printf '%s amendments=' "$r"
  git -C "$LANE" show "$r:.ufo/evidence/round-54/freeze.json" | python3 -c 'import json,sys; print(len(json.load(sys.stdin).get("amendments",[])))'
done
echo "--- commits touching freeze.json ---"
git -C "$LANE" log --format='%h %ad %s' --date=iso -- .ufo/evidence/round-54/freeze.json
echo "--- SCORECARD's corrected freeze sentence (same round) ---"
git -C "$LANE" show "$C0:SCORECARD.md" | grep -n "5 amendments" | head -3

echo
echo "### E. the Gate word counts vs the round's own census receipt"
git -C "$LANE" show "$C0:.ufo/waves/round-54/w1/T54W1ExecCensus-receipts/08-lesson-quote-wordcounts.txt"
echo "--- lesson Gate parentheticals ---"
git -C "$LANE" show "$C0:$F" | grep -n "words,"
echo "--- round-53 spot-check defect 8 (the routed count clause) ---"
git -C "$LANE" show "$C0:corpus/lessons/round-53-verifier-spotcheck.md" | sed -n '85p'
echo "--- S279's located sentence, from which 11 is countable ---"
git -C "$LANE" show "$C0:.ufo/evidence/round-54/assimilation/S279-tempfile-docs.html" | python3 -c '
import sys,re,html
t=sys.stdin.read(); t=re.sub(r"<script.*?</script>","",t,flags=re.S); t=re.sub(r"<[^>]+>"," ",t); t=html.unescape(t); t=re.sub(r"\s+"," ",t)
i=t.find("The list is: The directory named by the TMPDIR")
s=t[i:t.find(".",i)+1]
print(repr(s)); print("whitespace tokens in that sentence =", len(s.split()))
'

echo
echo "### F. QUALITY 105: the lesson's drafted block vs the landed criterion"
echo "--- lesson block at $C0 ---"
git -C "$LANE" show "$C0:$F" | sed -n '/## QUALITY criterion/,/^## The method/p'
echo "--- landed criterion at $C0 (falsifier sentence) ---"
git -C "$LANE" show "$C0:corpus/QUALITY.md" | grep -n "The check that can fail: a positive-control"

echo
echo "### G. Gate attribution of the mined considerthese proposal"
echo "--- committee: considerthese dir at $C0 ---"
git -C "$LANE" ls-tree --name-only "$C0" considerthese/
echo "--- 2026-10-28 proposal 1 and 2-5 (bytes at $C0) ---"
git -C "$LANE" show "$C0:considerthese/2026-10-28.md" | sed -n '/## Self-improvement ideas/,$p'
echo "--- where the contract-debt tracker actually lives ---"
grep -rn -i -E "contract-debt|contract sections still left as placeholders" "$LANE/considerthese/" | head -5
echo "--- the lesson's Gate sentence ---"
git -C "$LANE" show "$C0:$F" | grep -n -A4 "considerthese"

echo
echo "### H. control sweep: bullets the round did not touch that DO hold"
echo "--- R53.9 six files tracked at the base ---"
for p in .ufo/waves/round-53/w1-results.json .ufo/waves/round-53/w2-results.json .ufo/waves/round-53/w1/T53W1ExecR523.md .ufo/waves/round-53/w2/T53W2CritClaims.md .ufo/waves/round-53/w2/T53W2ExecR523B.md .ufo/waves/round-53/w2/T53W2RevW1Specialists.md; do
  printf '%s ' "$p"; git -C "$LANE" cat-file -e "$BASE:$p" 2>/dev/null && echo TRACKED-at-base || echo ABSENT-at-base
done
echo "--- R53.6 four-of-seven: before vs after C2 unusable lines ---"
git -C "$LANE" show "$C0:.ufo/evidence/round-54/before/c2.stdout" | grep -E "EXPLAIN unusable|C2_R54:" | sed -e 's/\(.\{150\}\).*/\1.../'
git -C "$LANE" show "$C0:.ufo/evidence/round-54/after/c2.stdout" | grep -E "EXPLAIN unusable|C2_R54:" | sed -e 's/\(.\{150\}\).*/\1.../'
echo "--- R53.1 dead-arm receipt (0/30) ---"
git -C "$LANE" show "$C0:.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout" | head -4
echo "--- Gate snapshot digests vs the lesson's sha prefixes ---"
for f in S277-posix-env.html S278-tempfile.py S279-tempfile-docs.html; do
  printf '%s ' "$f"
  git -C "$LANE" show "$C0:.ufo/evidence/round-54/assimilation/$f" | sha256sum
done
echo "--- text-extraction sizes: claim vs plain tag-strip of the committed snapshot ---"
for f in S277-posix-env.html S279-tempfile-docs.html; do
  git -C "$LANE" show "$C0:.ufo/evidence/round-54/assimilation/$f" | python3 -c '
import sys,re,html
n=sys.argv[1]; t=sys.stdin.read(); t=re.sub(r"<script.*?</script>","",t,flags=re.S); t=re.sub(r"<style.*?</style>","",t,flags=re.S)
t=re.sub(r"<[^>]+>"," ",t); t=html.unescape(t); t=re.sub(r"\s+"," ",t).strip()
print(n, "blob_bytes_len", len(sys.stdin.read()) if False else "n/a", "tagstrip_len", len(t))
' "$f"
done
echo "--- S278 anchor lines 163-165 of the committed snapshot ---"
git -C "$LANE" show "$C0:.ufo/evidence/round-54/assimilation/S278-tempfile.py" | sed -n '163,165p' | cat -A | sed -e 's/\$$//' | head -5
