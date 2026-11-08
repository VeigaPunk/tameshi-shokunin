#!/usr/bin/env bash
# T92S1 — independent re-fetch + tag-strip verification of the S320 source
# (https://man.archlinux.org/man/sha256sum.1.en) against the committed snapshot
# .ufo/evidence/round-92/sources/s320.html. Read-only on the lane; writes only
# beside this script.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
OUTDIR=$(cd "$(dirname "$0")" && pwd)
WORK=$(mktemp -d -p "${TMPDIR:-/fast/scratch/hyaku/tameshi-r92/T92S1}" t92s1.XXXXXX) || exit 1
trap 'rm -rf -- "$WORK"' EXIT
URL=https://man.archlinux.org/man/sha256sum.1.en
COMMITTED="$LANE/.ufo/evidence/round-92/sources/s320.html"
CHDR="$LANE/.ufo/evidence/round-92/sources/s320.headers"

echo "== fetch =="
curl -sS -D "$WORK/headers" -o "$WORK/body" "$URL"; echo "curl_exit=$?"
echo "http_date: $(grep -i '^date:' "$WORK/headers" | tr -d '\r')"
echo "content_length_hdr: $(grep -i '^content-length:' "$WORK/headers" | tr -d '\r')"
echo "body_bytes: $(wc -c < "$WORK/body")"
echo "body_sha256: $(sha256sum "$WORK/body" | cut -d' ' -f1)"
echo "committed_bytes: $(wc -c < "$COMMITTED")"
echo "committed_sha256: $(sha256sum "$COMMITTED" | cut -d' ' -f1)"
cmp -s "$WORK/body" "$COMMITTED" && echo "body_vs_committed: IDENTICAL" || echo "body_vs_committed: DIFFERS"
cp "$WORK/body" "$OUTDIR/T92S1-s320.html"
cp "$WORK/headers" "$OUTDIR/T92S1-s320.headers"
echo "saved_fetch_body_sha256: $(sha256sum "$OUTDIR/T92S1-s320.html" | cut -d' ' -f1)"
echo "== headers diff (committed vs fresh) =="
diff "$CHDR" "$WORK/headers" || true

echo "== tag-strip =="
python3 - "$WORK/body" "$OUTDIR/T92S1-stripped.txt" <<'PY'
import re, html, sys
b = open(sys.argv[1], 'rb').read().decode('utf-8')
t = re.sub(r'(?is)<(script|style)\b.*?</\1>', '', b)
t = re.sub(r'(?s)<!--.*?-->', '', t)
t = re.sub(r'(?i)<(br|/p|/div|/li|/tr|/h[1-6]|/pre)\b[^>]*>', '\n', t)
t = re.sub(r'(?s)<[^>]+>', ' ', t)
t = html.unescape(t)
lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in t.split('\n')]
lines = [l for l in lines if l]
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
PY

S="$OUTDIR/T92S1-stripped.txt"
echo "== quote locations in stripped text =="
grep -n -F 'Print or check SHA256 (256-bit) checksums.' "$S"
grep -n -F 'The sums are computed as described in FIPS-180-2.' "$S"
echo "== wc -w of the two quotes (quote text only) =="
printf '%s\n' 'Print or check SHA256 (256-bit) checksums.' | wc -w
printf '%s\n' 'The sums are computed as described in FIPS-180-2.' | wc -w
echo "== letter/digit word counts (second number only) =="
python3 - <<'PY'
import re
for q in ('Print or check SHA256 (256-bit) checksums.',
          'The sums are computed as described in FIPS-180-2.'):
    print('whitespace=%d letter_digit=%d %r' % (len(q.split()),
          len(re.findall(r'[A-Za-z0-9]+', q)), q))
PY
echo "== committed extract quote lines (cross-check) =="
grep -n -F 'Print or check SHA256' "$LANE/.ufo/evidence/round-92/sources/s320.txt"
grep -n -F 'The sums are computed as described in FIPS-180-2' "$LANE/.ufo/evidence/round-92/sources/s320.txt"

echo "== registry row S320 =="
awk -F'|' '/^\| S320 /{print "NF="NF; for(i=2;i<=NF-1;i++) printf "  col%d=%s\n", i-1, $i}' "$LANE/corpus/SOURCES.md"
