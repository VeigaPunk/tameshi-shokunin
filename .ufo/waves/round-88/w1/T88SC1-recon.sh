#!/usr/bin/env bash
# T88SC1-recon.sh — round-88 seat T88SC1 (scout) per-surface reconnaissance, READ-ONLY.
#
# Answers four questions about R88-C1 (coverage: the fleet mutation ledger governs an
# eleventh sibling gate, its first Python gate — kake scripts/ledger_append_guard.py):
#   (1) Has kake-shokunin or any other lane already mutation-tested that guard?
#   (2) Does any other lane hold a replayable mutation ledger leg on a Python gate?
#   (3) Is e8d3a924249983972e5163d160cf236487986c55 still the last commit touching the
#       guard on kake's origin/master, and is the guard byte-identical at kake's tip?
#   (4) Re-open S312 and check the two quotes the lane will cite (snapshot vs live page).
#
# READ-ONLY CONTRACT: this script writes ONLY under its own scratch dir ($S, default
# /fast/scratch/hyaku/tameshi-r88/T88SC1). It never runs a mutating git command, never
# touches a lane working tree, never writes into a lane repo. All git calls are
# read-only (show/log/ls-tree/cat-file/rev-parse/merge-base/for-each-ref/branch).
#
# Usage:  bash T88SC1-recon.sh
# Exit:   0 all probes ran (findings are in stdout), 2 a probe could not run.

set -u

F=/home/vgpnk/Projects/shokunin
L=$F/tameshi-shokunin
K=$F/kake-shokunin
S=${S:-/fast/scratch/hyaku/tameshi-r88/T88SC1}
mkdir -p "$S"

hr() { printf '\n===== %s =====\n' "$1"; }

hr "Q1a  kake lane: commits touching scripts/ledger_append_guard.py (all refs)"
git -C "$K" log --all --format='%H %ci %s' -- scripts/ledger_append_guard.py | head -10

hr "Q1b  kake lane: does any kill-rate / mutation figure exist FOR THE GUARD?"
grep -rn 'kill-rate\|kill_rate' "$K/corpus" "$K/LOG.md" "$K/SCORECARD.md" 2>/dev/null \
  | grep -i 'guard\|ledger_append' || echo "(none)"

hr "Q1c  kake round-80 mutation-tester seat (MutC): which file was its target?"
python3 - <<'PY'
import json
d = json.load(open('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/w1-spec.json'))
for it in d.get('items', []):
    if it.get('role') == 'mutation-tester':
        print('SEAT:', it.get('name'))
        print('ITEM:', it.get('item', '')[:400])
PY
echo "--- did MutC leave a report? ---"
ls -1 "$K/.ufo/waves/round-80/w1/" | grep -i '^MutC' || echo "(no MutC report file)"

hr "Q1d  kake round-80 'kills 3 mutants': what are the mutants of?"
grep -n 'def build_\|counter\b.*=\|run_counter' "$K/.ufo/waves/round-80/c80_ledger_fixtures.py" | head -12

hr "Q1e  fleet-wide: any mutant of the guard SOURCE (prefix_probe / rindex / startswith)?"
grep -rn 'prefix_probe\|base.rindex(b"]")\|carrier.startswith(head' \
  --include='*.py' --include='*.sh' --include='*.md' --include='*.json' --include='*.tsv' \
  --include='*.spec' --include='*.txt' \
  "$F" 2>/dev/null | grep -v '/.git/' | grep -v '/.jj/' | grep -v '/__pycache__/' \
  | grep -v 'prefix_probes' | head -20

hr "Q2a  every .defects.spec in the fleet (a leg needs one)"
find "$F" -maxdepth 6 -name '*.defects.spec' -not -path '*/.git/*' -not -path '*/.jj/*' 2>/dev/null | sort -u

hr "Q2b  lanes holding a COPY of the fleet mutation-ledger runner (REGRESSION_EXPECT)"
grep -rl 'REGRESSION_EXPECT: recorded kill-rates' --include='*.sh' "$F" 2>/dev/null \
  | grep -v '/.git/' | grep -v '/.ufo/waves/round-88/' | sort -u

hr "Q2c  leg list in each runner copy (any python leg before tameshi's leg 11?)"
for f in $(grep -rl 'REGRESSION_EXPECT: recorded kill-rates' --include='*.sh' "$F" 2>/dev/null \
           | grep -v '/.git/' | grep -v '/.ufo/waves/round-88/' | sort -u); do
  echo "--- $f"
  grep -o '^ *regression_case_git [a-z0-9-]*' "$f" | awk '{print "    "$2}'
done

hr "Q2d  other lanes' python mutation tools: do they reference a SIBLING lane repo?"
for f in "$F"/tsukuroi-shokunin/tools/mutation-kill-r8*.py \
         "$F"/kaidoku-shokunin/tools/round-8*/*.py \
         "$F"/souji-shokunin/census/round-6*/c2-mutate.py \
         "$F"/kotodama-shokunin/reports/round-72/accept-c.py; do
  [ -f "$f" ] || continue
  n=$(grep -c 'shokunin/' "$f" 2>/dev/null || echo 0)
  echo "  $f  sibling-repo-refs=$n"
done

hr "Q3a  kake: commits touching the guard ON origin/master"
git -C "$K" log --format='%H %ci %s' origin/master -- scripts/ledger_append_guard.py

hr "Q3b  guard blob at origin/master vs at the pin e8d3a924"
git -C "$K" ls-tree origin/master scripts/ledger_append_guard.py
git -C "$K" rev-parse origin/master:scripts/ledger_append_guard.py
git -C "$K" rev-parse e8d3a924249983972e5163d160cf236487986c55:scripts/ledger_append_guard.py
printf 'sha256(origin/master) '; git -C "$K" show origin/master:scripts/ledger_append_guard.py | sha256sum
printf 'sha256(pin)         '; git -C "$K" show e8d3a924249983972e5163d160cf236487986c55:scripts/ledger_append_guard.py | sha256sum
printf 'sha256(local master) '; git -C "$K" show master:scripts/ledger_append_guard.py | sha256sum
git -C "$K" merge-base --is-ancestor e8d3a924249983972e5163d160cf236487986c55 origin/master \
  && echo 'pin is an ancestor of origin/master: YES' || echo 'pin is an ancestor of origin/master: NO'
echo '--- guard blob at every remote-tracking ref ---'
for r in $(git -C "$K" for-each-ref --format='%(refname)' refs/remotes/); do
  b=$(git -C "$K" rev-parse "$r:scripts/ledger_append_guard.py" 2>/dev/null || echo '(absent)')
  echo "  $r $b"
done

hr "Q4a  S312 snapshot: sha256, size, anchor lines"
SNAP=$L/.ufo/evidence/round-88/sources/s312-stdtypes.html
sha256sum "$SNAP"
wc -c < "$SNAP"
grep -n 'id="bytes.startswith"' "$SNAP" | cut -c1-60
grep -n 'id="bytes.rindex"' "$SNAP" | cut -c1-60

hr "Q4b  S312 snapshot: the two located sentences (rendered text, tags dropped)"
python3 - <<'PY'
import re, html
p = '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-88/sources/s312-stdtypes.html'
s = open(p, encoding='utf-8', errors='replace').read()
lines = s.split('\n')

def rendered(a, b):
    t = re.sub(r'<[^>]+>', '', '\n'.join(lines[a - 1:b]))
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()

for anchor in ('bytes.startswith', 'bytes.rindex'):
    i = next(k for k, ln in enumerate(lines) if 'id="%s"' % anchor in ln)
    print('anchor %-16s at snapshot line %d' % (anchor, i + 1))
    txt = rendered(i + 1, i + 8)
    print('  RENDERED:', txt[:300])
    for q in ("Return True if the binary data starts with the specified prefix, otherwise return False.",
              "Like rfind() but raises ValueError when the subsequence sub is not found.",
              "raises ValueError when the subsequence sub is not found"):
        if q in txt:
            print('  QUOTE PRESENT (%d words): %s' % (len(q.split()), q))
    print()

print('--- line spans of the two bytes.* sentences (anchored at the bytes.* anchor) ---')
for name, needle in (('bytes.startswith', 'Return <code class="docutils literal notranslate"><span class="pre">True</span></code> if the binary data'),
                      ('bytes.rindex', 'but raises <a class="reference internal" href="exceptions.html#ValueError"')):
    start = next(k for k, ln in enumerate(lines) if 'id="%s"' % name in ln)
    for k in range(start, len(lines)):
        if needle in lines[k]:
            end = k + 1
            while '</p>' not in lines[end - 1] and end < len(lines):
                end += 1
            print('%s: anchor line %d; sentence spans snapshot lines %d-%d'
                  % (name, start + 1, k + 1, end))
            break
PY

hr "Q4c  live page fetch: does it agree with the snapshot?"
curl -sSL -o "$S/live-stdtypes.html" \
  -w 'http=%{http_code} final_url=%{url_effective} bytes=%{size_download}\n' \
  https://docs.python.org/3/library/stdtypes.html
sha256sum "$S/live-stdtypes.html"
if cmp -s "$SNAP" "$S/live-stdtypes.html"; then
  echo 'LIVE == SNAPSHOT (byte-identical)'
else
  echo 'LIVE != SNAPSHOT (differs)'
fi
grep -n 'id="bytes.startswith"' "$S/live-stdtypes.html" | cut -c1-60
grep -n 'id="bytes.rindex"' "$S/live-stdtypes.html" | cut -c1-60

hr "Q4d  S312 registry row as it currently stands (working tree, uncommitted)"
grep -n '^| S312 |' "$L/corpus/SOURCES.md" | cut -c1-200 || echo "(no S312 row in working tree)"
printf 'S312 row committed at 28ec5885? '
git -C "$L" show 28ec58858a084bc193a89ca5b0a751942694ccfb:corpus/SOURCES.md | grep -c '^| S312 |'
printf 'case note corpus/knowledge/mutation-case-kake-ledger-guard.md exists on disk? '
ls "$L/corpus/knowledge/mutation-case-kake-ledger-guard.md" >/dev/null 2>&1 && echo YES || echo NO

hr "Q4e  word counts of the two quotes the row cites"
python3 - <<'PY'
for q in ("Return True if the binary data starts with the specified prefix, otherwise return False.",
          "Like rfind() but raises ValueError when the subsequence sub is not found."):
    print('%2d words | %s' % (len(q.split()), q))
PY

hr "Q5  the sweep receipt leg 11 (tameshi's own measured table)"
sed -n '1,6p;/MUTATE: DONE/p' "$L/.ufo/evidence/round-88/c1/sweep.txt"

hr "Q6  the ledger row for leg 11 (working tree fleet-kill-rate-ledger.md)"
grep -n 'py-kake-ledger-guard' "$L/corpus/knowledge/fleet-kill-rate-ledger.md" | cut -c1-240

hr "DONE (read-only recon)"
