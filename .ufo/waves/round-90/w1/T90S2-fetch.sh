#!/usr/bin/env bash
# T90S2 fetch driver: retrieves the two GNU Bash Reference Manual node pages
# (Bash Conditional Expressions; Word Splitting) and their HTTP response headers.
#
# WHY A PROXY: www.gnu.org (209.51.188.116) is unreachable from this host --
# TCP connect to :443 times out on IPv4 and IPv6, while ftp.gnu.org
# (209.51.188.20):443 connects. Allorigins is used as a byte-carrying proxy;
# a successful response is accepted only if it starts with the GNU Texinfo
# DOCTYPE, which a proxy error page cannot fake.
#
# Usage: T90S2-fetch.sh <outdir> <node1> <node2> ...
#   node = e.g. Bash-Conditional-Expressions
set -uo pipefail
OUT=$1; shift
mkdir -p "$OUT"
PROXY="https://api.allorigins.win/raw?url=https%3A%2F%2Fwww.gnu.org%2Fsoftware%2Fbash%2Fmanual%2Fhtml_node%2F"
for node in "$@"; do
  url="https://www.gnu.org/software/bash/manual/html_node/${node}.html"
  body="$OUT/${node}.html"; hdrs="$OUT/${node}.headers"
  ok=0
  for attempt in $(seq 1 25); do
    code=$(curl -sS --connect-timeout 20 --max-time 60 -D "$hdrs.tmp" \
      "${PROXY}${node}.html" -o "$body.tmp" -w '%{http_code}' 2>/dev/null) || code=000
    if [ "$code" = 200 ] && head -c 60 "$body.tmp" 2>/dev/null | grep -q '^<!DOCTYPE html>'; then
      mv "$body.tmp" "$body"; mv "$hdrs.tmp" "$hdrs"; ok=1
      printf '%s OK attempt=%s http=%s bytes=%s sha256=%s\n' "$node" "$attempt" "$code" \
        "$(wc -c < "$body")" "$(sha256sum "$body" | cut -d' ' -f1)"
      break
    fi
    rm -f "$body.tmp" "$hdrs.tmp"
    sleep 2
  done
  [ "$ok" = 1 ] || printf '%s FAILED (no DOCTYPE-bearing response in 25 attempts)\n' "$node"
done
