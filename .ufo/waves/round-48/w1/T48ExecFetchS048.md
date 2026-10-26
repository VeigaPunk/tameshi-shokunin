# T48ExecFetchS048 — C2 fetch for target S048

Seat: T48ExecFetchS048 (leaf). Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin at base
`473336d9d789f6081195e7376d17836a24666bc3`. Contract read first, including amendments 1–3
(amendment 1: receipt url must be in the set of https URLs of R's source and anchor cells;
amendment 2: extraction/quote-freezing rules; amendment 3: C1 grammar only). I edited no
registry row, no knowledge entry, no counter, no Git/jj state. Only the two C2 deliverables
below plus this report were written, plus scratch under
`/fast/scratch/hyaku/tameshi-r48/T48ExecFetchS048/` (deleted before finishing).

## Deliverables written

- `.ufo/waves/round-48/w1/sources/S048.html` — fetched bytes, byte-exact; sha256
  `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db`, 8,892 B
  (`cmp` against the fetched scratch file → identical).
- `.ufo/waves/round-48/w1/sources/S048.receipt.json` — url `https://pitest.org/quickstart/incremental_analysis/`,
  fetched_at `2026-10-26T08:40:42Z`, http_status `200`, bytes `8892`, sha256 as above, tool
  `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5 zlib/1.3.2 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.70.0 ngtcp2/1.25.0 nghttp3/1.18.0 mit-krb5/1.22.2`.

Fetch facts (from `S048.headers`): `HTTP/2 200`, `content-type: text/html; charset=utf-8`,
`content-length: 8892`, `last-modified: Wed, 03 Jun 2026 08:45:37 GMT`,
`etag: "6a1fe9b1-22bc"` (0x22bc = 8,892), server `GitHub.com` via Fastly (`date: Mon, 26 Oct 2026 08:40:42 GMT`).

## Base row read

`corpus/SOURCES.md:57`:

| S048 | Incremental analysis (PIT docs), object-neutral precision — https://pitest.org/quickstart/incremental_analysis/ | docs | A | PIT's item-4 prioritisation distinction without resolving an ambiguous pronoun | §Incremental analysis, numbered items 4–5 and dependency paragraphs; accessed 2026-10-20, page version unstated | supersedes S047 — item 4 is prioritisation rather than a reuse skip; no claim here resolves its pronoun to test versus mutation; item 5 is explicitly not yet implemented and the dependency assumption remains unproven | mined | 2026-10-20 | 90d | corpus/knowledge/incremental-pin-disposition.md |

Source-cell URL and receipt url are identical, so amendment 1's URL-set condition holds.
Base anchor carries no sha256 and only `accessed 2026-10-20, page version unstated`.

Round-45 ledger entry (`.ufo/evidence/round-45/freshness/ledger.json`, id S048): verdict
`holds`, raw_sha256 `e9cbc3e1…0db`, quote `If a mutation was previously killed, but the class
or killing test has changed` (14 tokens). Round-45 review (`reviews.json`, id S048,
reviewer `CritJudge02`) is a **dispute**: that quote is item 4's antecedent only, cut at
`has changed`, and drops the consequent `…then it is likely that the last killing test will
still kill it and it should therefore be prioritised above others` that carries the
prioritisation-vs-reuse-skip claim, "so it asserts nothing".

## Quote delivered (exact, whitespace-collapsed per amendment 2)

```
then it is likely that the last killing test will still kill it and it should therefore be prioritised above others
```

- Token count: **21** whitespace tokens (≤ 25).
- Contains the required phrase `should therefore be prioritised` (the phrase occurs exactly
  once in the extracted text).
- Verbatim: occurs once in the extracted text (substring of the amendment-2 normalized text),
  and also once in the raw HTML bytes; no case/punctuation folding used.
- Location: body `<h1 id="incremental-analysis">Incremental analysis</h1>` (raw HTML line 74),
  then the `<ol>` list of optimisations — the **fourth `<li>`** (item 4), raw byte span
  3786–4000, raw HTML line 86; the phrase itself starts at raw offset 3940 and at normalized-
  text offset 1104. The `<li>` is verbatim:
  `<li>If a mutation was previously killed, but the class or killing test has changed then it
  is likely that the last killing test will still kill it and it should therefore be
  prioritised above others. (since 1.14.4)</li>`.
- Dispute answer: this quote is item 4's **consequent** — the span round-45 found missing — so
  it states the prioritisation claim (`prioritised above others`) rather than a reuse skip,
  while the pronoun in `still kill it` remains unresolved (test vs mutation), matching the
  base row's teaches cell and `corpus/knowledge/incremental-pin-disposition.md:346-349`
  ("item4 prioritisation, not a reuse skip; no pronoun referent is resolved here").
  The full item-4 sentence including its antecedent is 35 tokens, over the 25-token cap, so
  the antecedent cannot be carried by the Gate quote.

## Proposed anchor cell text for the new superseding row

```
§Incremental analysis, item 4 (raw line 86); fetched 2026-10-26, Last-Modified 2026-06-03, page version unstated; sha256 e9cbc3e1ab7c, 8,892 B
```

(sha256 first 12 hex = `e9cbc3e1ab7c`; bytes 8,892; date is the 2026-10-26 fetch date, with the
server's `last-modified` as the revision evidence; the body itself states no version/date, so
"page version unstated" is retained. This anchor cell must also keep the source URL so that
amendment 1's URL set still contains the receipt url — the row's source cell carries it.)

## Drift verdict

**No drift; the teaches cell holds.**

- Live sha256 `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db` equals the
  round-45 ledger `raw_sha256` for S048 and equals the gunzipped round-45 snapshot
  `.ufo/evidence/round-45/freshness/sources/S048.raw.gz` (sha256 re-derived; `cmp` of live bytes
  vs snapshot → **byte-identical**, not merely same hash).
- It also equals the 2026-10-20 fetch recorded for S041 in
  `corpus/knowledge/incremental-pin-disposition.md:1` (`sha256 e9cbc3e1…0db (8,892 B)`), so the
  bytes have been stable from 2026-10-20 through 2026-10-26.
- What changed: nothing in the document. The base row's anchor is the weak part — it has no
  sha256 and says "page version unstated"; the new anchor pins sha256 + bytes + fetch date.
  The round-45 quote problem, not the document, is what the new row fixes.
- Item 4's consequent (prioritisation above others) is present; item 5's `(not yet implemented)`
  tag and the dependency paragraphs (`the assumption that it will be relatively rare … it is
  currently unproven`) are still present, so the base teaches cell's substance survives.

## Entry cites that the new row must re-point (owner action, not done here)

Base used-by cell is `corpus/knowledge/incremental-pin-disposition.md` only:

- line 5: `source-correction: S048 — https://pitest.org/quickstart/incremental_analysis/ …`
- lines 346-349: `Source guidance correction: **S048 supersedes S047's object-specific
  paraphrase** …`

These must become the new registry id (next free `S265`) with `verified-at: 2026-10-26` per the
C2 statement. Out-of-cell observation for L1: `corpus/knowledge/fleet-kill-rate-ledger.md:374`
also says `source method: S003 and S048`, but that file is not in S048's base used-by cell, so
the C2 statement as frozen does not require re-pointing it; flagging it rather than acting.

## Evidence commands actually run (scratch only)

- `curl -sS -L -D S048.headers -o S048.html -w '%{http_code} %{size_download}\n' 'https://pitest.org/quickstart/incremental_analysis/'` → `200 8892`.
- `sha256sum` on live file and on `gunzip -c` of the round-45 snapshot → both `e9cbc3e1…0db`;
  `cmp` → identical.
- Python extraction exactly per amendment 2 (UTF-8 decode, drop `<script>`/`<style>`, strip tags,
  `html.unescape`, collapse whitespace) → quote substring present once, 21 tokens.
- `curl --version` first line → receipt `tool` value.

No counter was built or run (not this seat's item); no deciding/control scoring performed.
No SOURCES.md, entry, ledger, jj or Git index change. No repository file other than the two
deliverables and this report was written.

## Risks / caveats

- The page has no in-body version/date; the anchor's revision evidence is the HTTP
  `last-modified: 2026-06-03` header (server-side, GitHub Pages). If L1 prefers a body-only
  revision marker, the honest value is still "page version unstated".
- The 25-token cap makes antecedent + consequent impossible (full sentence 35 tokens); the
  Gate quote is the consequent alone, which is exactly the span round-45 disputed as missing.
  It states prioritisation, not a reuse skip.
- Fetched from `pitest.org` with `-L`; no redirects were needed for the final 200 (the header
  dump shows a single HTTP/2 200 block), so the receipt url is the canonical page URL.
- Scratch dir `/fast/scratch/hyaku/tameshi-r48/T48ExecFetchS048` removed at completion; no
  fixture repos were created, so no throwaway commit identity was used.
- Tooling: nothing installed or upgraded (curl 8.23.0 and python3 already present), so no
  tool/version/channel record is due.
