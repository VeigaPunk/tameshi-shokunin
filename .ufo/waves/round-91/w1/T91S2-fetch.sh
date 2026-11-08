#!/usr/bin/env bash
# T91S2 — fetch git-replace(1) from git-scm.com and save the response headers
# next to the body, then produce the tag-stripped text the quote line numbers
# refer to.
#
# READ-ONLY with respect to the lane: writes only into the directory this
# script lives in (the seat's wave directory) or $OUTDIR. It touches no lane
# file, no fleet file, and runs no mutating git command.
#
# Usage:  bash T91S2-fetch.sh [OUTDIR]
# Default OUTDIR: the directory of this script.
#
# The tag-strip is exactly `sed 's/<[^>]*>//g'` — the same command the lane's
# row anchors quote line numbers against, so re-running this script reproduces
# the .txt byte-identically from the saved .html.
set -u

OUT="${1:-$(cd "$(dirname "$0")" && pwd)}"
URL='https://git-scm.com/docs/git-replace'
mkdir -p "$OUT"

echo "# fetch-start-utc $(date -u +'%Y-%m-%dT%H:%M:%SZ')" > "$OUT/T91S2-fetch.meta"
curl -sS -L --max-time 60 -D "$OUT/T91S2-git-replace.headers" \
     -o "$OUT/T91S2-git-replace.html" "$URL"
rc=$?
echo "curl_exit=$rc" >> "$OUT/T91S2-fetch.meta"
[ $rc -eq 0 ] || exit $rc

# The HTTP Date header is the access timestamp of record.
grep -i '^date:' "$OUT/T91S2-git-replace.headers" >> "$OUT/T91S2-fetch.meta"

sed 's/<[^>]*>//g' "$OUT/T91S2-git-replace.html" > "$OUT/T91S2-git-replace.txt"

{
  echo "url=$URL"
  echo "bytes=$(wc -c < "$OUT/T91S2-git-replace.html")"
  echo "sha256=$(sha256sum "$OUT/T91S2-git-replace.html" | cut -d' ' -f1)"
  echo "txt_bytes=$(wc -c < "$OUT/T91S2-git-replace.txt")"
  echo "quote_line_1661_wc_w=$(sed -n '1661p' "$OUT/T91S2-git-replace.txt" | wc -w)"
  echo "quote_line_1661=[$(sed -n '1661p' "$OUT/T91S2-git-replace.txt")]"
} >> "$OUT/T91S2-fetch.meta"

cat "$OUT/T91S2-fetch.meta"
