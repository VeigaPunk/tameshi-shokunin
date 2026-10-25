seat: ExecLiveSweep
axis: freshness — C1 informational live sweep (outside the frozen predicate; drift flag for the lesson)
rev: ad5942c6e9858af19d00000b58439b321ddfa62b (lane /home/vgpnk/Projects/shokunin/tameshi-shokunin)
read-only: no lane file, jj state or Git index touched; scratch in /tmp/tameshi-r45-ExecLiveSweep/

## 1. Command and full output

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 .ufo/evidence/round-45/freshness/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev ad5942c6e9858af19d00000b58439b321ddfa62b --live
LIVE S001 present
LIVE S002 present
LIVE S003 present
LIVE S004 present
LIVE S005 present
LIVE S006 present
LIVE S008 present
LIVE S011 present
LIVE S012 present
LIVE S024 present
LIVE S026 present
LIVE S028 present
LIVE S041 present
LIVE S047 present
LIVE S048 present
LIVE S049 present
LIVE S052 present
LIVE S054 present
LIVE S055 present
LIVE S056 present
LIVE S057 present
LIVE S058 absent
LIVE S059 present
LIVE S060 present
LIVE S061 present
LIVE S062 present
LIVE S063 present
LIVE S064 present
LIVE S065 present
LIVE S066 present
LIVE S068 present
LIVE S069 present
LIVE S070 present
LIVE S072 present
LIVE S073 present
LIVE S074 present
LIVE S075 present
LIVE S076 present
LIVE S077 present
LIVE S078 present
LIVE S079 present
LIVE S081 present
LIVE S084 present
LIVE S086 present
LIVE S087 present
LIVE S089 present
LIVE S090 present
LIVE S091 present
LIVE S093 present
LIVE S094 present
LIVE S095 present
LIVE S096 present
LIVE S097 present
LIVE S099 present
LIVE S100 present
LIVE S101 present
LIVE S102 present
LIVE S103 present
LIVE S104 present
LIVE S105 present
LIVE S106 present
LIVE S107 present
LIVE S108 present
LIVE S132 present
LIVE S152 present
LIVE S153 present
LIVE S154 present
LIVE S155 present
LIVE S156 present
LIVE S157 present
LIVE S158 present
LIVE S159 present
LIVE S160 present
C1_R45_LIVE: present=72 absent=1 rev=ad5942c6e9858af19d00000b58439b321ddfa62b
```

73 LIVE lines = 73 `holds` entries, all of them in the population (population 73, holds-in-pop 73 — computed from the REV registry `corpus/SOURCES.md` and REV `ledger.json`; all entries carry `verdict: holds`). Exit 0 (by construction: `live()` ends `return 0`, measure.py:322). Wall time 27.7 s. Log kept at `/tmp/tameshi-r45-ExecLiveSweep/live-run1.txt` (1391 B, 74 lines).

## 2. The single `absent` row — S058

Row: `https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf`
Ledger entry at REV (`.ufo/evidence/round-45/freshness/ledger.json`, id S058): `verdict holds`, `opened 2026-10-25`,
`raw_sha256 d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede`,
`quote "a trace which we can use to verify existing values"`, `snapshot .ufo/evidence/round-45/freshness/sources/S058.raw.gz`.

**Classification: transport (anti-bot), NOT content drift.**

Manual re-fetch #1, same flags the counter uses (`-A Mozilla/5.0`, `-f`):

```
$ curl -fsSL --max-time 60 -A 'Mozilla/5.0' -o /tmp/tameshi-r45-ExecLiveSweep/S058.bin \
    https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf
CURL_RC 22 META 403 0 text/html STDERR curl: (22) The requested URL returned error: 403
CLASS transport
```

Manual re-fetch #2, headers kept (`-sS -D`):

```
HTTP/2 403
server: AkamaiNetStorage
content-length: 4410
content-type: text/html
strict-transport-security: max-age=31536000; includeSubDomains
etag: "6d1c7b0dad0b83d59486e6231dc7bbe7:1762790445.270795"
cache-control: max-age=465
date: Sun, 25 Oct 2026 20:24:31 GMT
```

First 300 bytes of that 403 body (4410 B, `text/html`, no `%PDF` magic — a Microsoft anti-bot / error page, not the paper):

```
b'<!doctype html>\r\n<html lang="en">\r\n\r\n<head>\r\n    <meta charset="utf-8">\r\n    <title>Microsoft</title>\r\n    <meta name="viewport" content="width=device-width, initial-scale=1">\r\n    <meta name="robots" content="noindex, nofollow">\r\n\r\n    <link href="https://assets.onestore.ms/cdnfiles/external/mwf/lo'
```

Manual re-fetch #3, **default curl UA** (no `-A`) — same URL, same minute:

```
NOUA http=200 size=728559 type=application/pdf
```

and on those live bytes:

```
LIVE_SHA   d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede
LEDGER_SHA d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede
SHA_EQUAL True
MAGIC b'%PDF-'
QUOTE_PRESENT_IN_LIVE_PDF True
TEXT_LEN 101389
```

So today's bytes are **byte-identical** to the committed snapshot and the 6-token quote is still located in the live PDF. `HEAD` with `Mozilla/5.0` also returns 403, so the block is UA-keyed at the Akamai edge and is stable across the three attempts. Committed snapshot integrity re-checked at REV: gunzipped blob sha == ledger `raw_sha256`, quote present.

## 3. Drift flag for the lesson

- The only `absent` is a harness artifact: `measure.py:305-306` sends `-A Mozilla/5.0` and `-f`, so the edge answers 403 and `curl -f` discards the body; `present` stays False (`measure.py:307-313`). A `-A`-less retry gets the real 728559-byte PDF.
- Informational consequence for C1: live re-verification of the held corpus is 73/73 with zero content drift once the UA block is bypassed — 72/73 under the counter's own flags.
- It does not touch the frozen predicate: `--live` is explicitly outside `measure()` and always returns 0 (measure.py:300-322, docstring lines 26-28). No counter, ledger, snapshot, registry or review file was modified.

## 4. Retained evidence

- `/tmp/tameshi-r45-ExecLiveSweep/live-run1.txt` — full sweep output (74 lines).
- `/tmp/tameshi-r45-ExecLiveSweep/ledger.json` — `git show ad5942c6…:.ufo/evidence/round-45/freshness/ledger.json` (73 entries, all `holds`).
- `/tmp/tameshi-r45-ExecLiveSweep/s058.hdr`, `s058.pdf` (403 body, 4410 B), `s058-noua.bin` (200 PDF, 728559 B), `refetch.py` (manual classifier).

## 5. Tooling

None installed or upgraded. `curl` and `pdftotext` were already present at `/usr/bin/`.
