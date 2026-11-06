#!/usr/bin/env bash
# T90S1 — fetch a gnu.org manual page and record an atomic receipt.
#
# WHY A RELAY: www.gnu.org:443 is unreachable from this host (IPv4
# 209.51.188.116 and IPv6 2001:470:142:5::116 both time out; the peer seat
# recorded the same failure in .ufo/evidence/round-90/sources/gnu-unreachable.txt).
# The page bytes are therefore fetched through the public allorigins relay,
# whose /raw endpoint returns the upstream body and whose /get endpoint
# reports the upstream status block (http_code, content_type, content_length,
# response_time) for the same URL.
#
# Usage: fetch.sh <name> <url>
# Writes, under $OUT:
#   <name>.relay.html      upstream body as delivered (HTML entities intact)
#   <name>.relay.headers   the relay's own HTTP response headers
#   <name>.upstream.json   the relay's report of the upstream status block
#   <name>.fetch.log       one line per attempt (UTC stamps, sizes, digests)
#
# A body is only promoted over an existing good body when it parses as the
# expected Texinfo HTML page (doctype + expected title); otherwise the good
# body is kept and the attempt is logged as FAIL.
set -u
NAME=$1; URL=$2
OUT=${OUT:-/fast/scratch/hyaku/tameshi-r90/T90S1}
ENC=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' "$URL")
LOG="$OUT/$NAME.fetch.log"
TMP="$OUT/.tmp-$NAME.html"
HDR="$OUT/.tmp-$NAME.headers"
: > "$LOG"

ok_body() { # $1 = candidate file ; echoes the title if it looks like the page
  head -c 200 "$1" | grep -qi '<!DOCTYPE html>' || return 1
  grep -qi '<title>' "$1" || return 1
  return 0
}

for i in $(seq 1 60); do
  ts=$(date -u +%FT%TZ)
  rm -f "$TMP" "$HDR"
  if curl -sS -L --max-time 50 -D "$HDR" -o "$TMP" \
       "https://api.allorigins.win/raw?url=$ENC" 2>"$OUT/$NAME.curl.err" \
     && ok_body "$TMP"; then
    sz=$(stat -c%s "$TMP")
    sha=$(sha256sum "$TMP" | cut -d' ' -f1)
    mv -f "$TMP" "$OUT/$NAME.relay.html"
    mv -f "$HDR" "$OUT/$NAME.relay.headers"
    printf '%s attempt=%s body=OK bytes=%s sha256=%s\n' "$ts" "$i" "$sz" "$sha" >> "$LOG"
    break
  fi
  printf '%s attempt=%s body=FAIL\n' "$ts" "$i" >> "$LOG"
  sleep 3
done

for i in $(seq 1 60); do
  ts=$(date -u +%FT%TZ)
  if curl -sS -L --max-time 50 "https://api.allorigins.win/get?url=$ENC" \
       -o "$OUT/.tmp-$NAME.json" 2>/dev/null \
     && python3 -c "
import json
d=json.load(open('$OUT/.tmp-$NAME.json'))
s=d.get('status') or {}
assert s.get('http_code')==200 and s.get('url')=='$URL'
" 2>/dev/null; then
    mv -f "$OUT/.tmp-$NAME.json" "$OUT/$NAME.upstream.json"
    printf '%s upstream_status=OK %s\n' "$ts" \
      "$(python3 -c "
import json
print(json.dumps(json.load(open('$OUT/$NAME.upstream.json'))['status']))
")" >> "$LOG"
    break
  fi
  printf '%s upstream_status=FAIL\n' "$ts" "$i" >> "$LOG"
  sleep 3
done
cat "$LOG"
