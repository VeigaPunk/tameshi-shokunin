#!/usr/bin/env bash
# T91S1 — S318 source-fetch verification probe (round 91, seat T91S1).
#
# Re-runnable from committed bytes. Writes ONLY inside:
#   - $W1   (the seat's deliverable directory, default .ufo/waves/round-91/w1)
#   - $S    (a scratch dir under /fast/scratch/hyaku/tameshi-r91/T91S1)
# and touches nothing in the lane repo, the fleet repo, or any sibling lane.
#
# Usage:  bash T91S1-fetch.sh [W1_DIR]
# Output: prints a receipt block (URL, UTC access timestamp, HTTP status,
#         byte size, sha256, cmp result against the frozen snapshot, quote
#         line numbers and wc -w counts).

set -euo pipefail

LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
W1="${1:-$LANE/.ufo/waves/round-91/w1}"
S="${T91S1_SCRATCH:-/fast/scratch/hyaku/tameshi-r91/T91S1}"
FROZEN="$LANE/.ufo/evidence/round-91/sources/git-env.html"
FROZEN_TXT="$LANE/.ufo/evidence/round-91/sources/git-env.txt"

mkdir -p "$W1" "$S"
trap 'rm -rf -- "$S"' EXIT

STRIP="$W1/T91S1-strip.py"
test -f "$STRIP" || { echo "missing $STRIP" >&2; exit 1; }

echo "=== fetch https://git-scm.com/docs/git ==="
curl -sS -D "$S/git-env.headers" -o "$S/git-env.html" \
     -w 'http_code=%{http_code} size_download=%{size_download} url_effective=%{url_effective}\n' \
     https://git-scm.com/docs/git
echo "accessed_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "bytes=$(stat -c %s "$S/git-env.html")"
echo "sha256=$(sha256sum "$S/git-env.html" | cut -d' ' -f1)"
if cmp "$S/git-env.html" "$FROZEN"; then
  echo "cmp_vs_frozen_snapshot=IDENTICAL"
else
  echo "cmp_vs_frozen_snapshot=DIFFERENT"
fi

python3 "$STRIP" "$S/git-env.html" "$S/git-env.txt"

echo "--- GIT_NO_REPLACE_OBJECTS quote, ENVIRONMENT VARIABLES entry (my tag-stripped text) ---"
grep -n '^GIT_NO_REPLACE_OBJECTS$' "$S/git-env.txt"
echo "quote_lines=1432-1433  wc_w=$(sed -n '1432,1433p' "$S/git-env.txt" | wc -w)"

echo "--- same entry in the frozen committed .txt (line numbers differ by the stripper) ---"
grep -n 'GIT_NO_REPLACE_OBJECTS' "$FROZEN_TXT"
echo "committed_quote_lines=1414-1415  wc_w=$(sed -n '1414,1415p' "$FROZEN_TXT" | wc -w)"

echo "=== fetch https://git-scm.com/docs/git-replace ==="
curl -sS -D "$S/replace.headers" -o "$S/replace.html" \
     -w 'http_code=%{http_code} size_download=%{size_download} url_effective=%{url_effective}\n' \
     https://git-scm.com/docs/git-replace
echo "accessed_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "bytes=$(stat -c %s "$S/replace.html")"
echo "sha256=$(sha256sum "$S/replace.html" | cut -d' ' -f1)"
python3 "$STRIP" "$S/replace.html" "$S/replace.txt"
echo "--- replacement-ref quote ---"
sed -n '215,217p' "$S/replace.txt"
echo "replace_quote_lines=215-217  wc_w=$(sed -n '215,217p' "$S/replace.txt" | wc -w)"

cp "$S/git-env.html"    "$W1/T91S1-git-env.html"
cp "$S/git-env.headers" "$W1/T91S1-git-env.headers"
cp "$S/git-env.txt"     "$W1/T91S1-git-env.txt"
cp "$S/replace.html"    "$W1/T91S1-replace.html"
cp "$S/replace.headers" "$W1/T91S1-replace.headers"
cp "$S/replace.txt"     "$W1/T91S1-replace.txt"
echo "deliverables written under $W1"
