#!/usr/bin/env bash
# SOURCES census v2 (fleet round 1, kaika) — run from the lane root.
# Part A = the frozen contract v1 census, verbatim; exit 1 on any violation.
# Part B = fleet critic H4 extensions (not contract v1), reported separately:
#   B1 strict: a mined row's used-by file contains the row id.
#   B2 id-or-path: ... contains the row id OR the row's repo-path source token
#      (own-work/code rows whose used-by entries predate the registry and cite
#      the source by path). Exit 1 on B2 violations; B1 is informational.
f=corpus/SOURCES.md; R='^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|'; bad=0
echo "== A rows"; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' $f
echo "== A malformed (must be 0)"; m=$(awk -F'|' "/$R/ && NF!=13 {n++} END{print n+0}" $f); echo $m; [ "$m" = 0 ] || bad=1
echo "== A tiers"; awk -F'|' "/$R/ {t=\$5; gsub(/[[:space:]]/,\"\",t); n[t]++} END{for(k in n) printf \"%s=%d \", k, n[k]; print \"\"}" $f
echo "== A status"; awk -F'|' "/$R/ {s=\$9; gsub(/[[:space:]]/,\"\",s); n[s]++} END{for(k in n) printf \"%s=%d \", k, n[k]; print \"\"}" $f
o=$(awk -F'|' "/$R/ {i=\$2; gsub(/[[:space:]]/,\"\",i); print i}" $f | sort | uniq -d); echo "== A dup ids (must print nothing)"; [ -z "$o" ] || { echo "$o"; bad=1; }
o=$(awk -F'|' "/$R/ && NF==13"' {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' $f); echo "== A enum/tier-inflation (must print nothing)"; [ -z "$o" ] || { echo "$o"; bad=1; }
pairs=$(awk -F'|' "/$R/ && NF==13"' {i=$2;s=$9;src=$3; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); sub(/.* — /,"",src); gsub(/[[:space:]]+$/,"",src); if (p!="" && p!="—") print i, p, src}}}' $f)
o=$(echo "$pairs" | while read -r i p s; do [ -e "$p" ] || echo "missing: $p"; done); echo "== A mined used-by missing (must print nothing)"; [ -z "$o" ] || { echo "$o"; bad=1; }
echo "== B1 strict id-cite (informational)"; echo "$pairs" | while read -r i p s; do grep -qF "$i" "$p" || echo "no-id-cite: $i $p"; done | awk '{print} END{print "count=" NR}'
o=$(echo "$pairs" | while read -r i p s; do b=${s##*/}; grep -qF "$i" "$p" || { [ -n "$b" ] && grep -qF "$b" "$p"; } || echo "no-id-or-path-cite: $i $p ($b)"; done); echo "== B2 id-or-path cite (must print nothing)"; [ -z "$o" ] || { echo "$o"; bad=1; }
echo "== VERDICT"; [ $bad = 0 ] && echo "SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)" || echo "SOURCES_CENSUS: VIOLATIONS"; exit $bad
