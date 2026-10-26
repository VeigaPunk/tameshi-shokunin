# T48ExecFetchS026 — C2 fetch, target S026

Round 48 (hyaku run 8, attempt 1), wave 1. Lane `tameshi-shokunin`, base `473336d9d789f6081195e7376d17836a24666bc3`.
Scope: C2 freshness fetch for target **S026** only. No row, entry or lesson was edited.

## 1. Base state read

Base row (`corpus/SOURCES.md:37`):

```
| S026 | Flaky Tests at Google and How We Mitigate Them (John Micco, Google Testing Blog, 2016) — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | docs | A | Google's flakiness rates and mitigations | Post body, published 2016-05-27 (fetched 2026-10-19) | about 1.5% of test runs are flaky; about 84% of pass-to-fail transitions involve a flaky test; a fail-3-in-a-row flaky mark cuts false positives but teaches people to ignore flakiness | mined | 2026-10-19 | 730d | corpus/knowledge/repeated-control-precondition.md |
```

Used-by cell: `corpus/knowledge/repeated-control-precondition.md` (one entry; re-pointing is the integrator's step, not mine).

Round-45 ledger entry (`.ufo/evidence/round-45/freshness/ledger.json`, id `S026`): verdict `holds`,
`raw_sha256 5d74dd1c3c75d5ec1b8d53d6a518b4b01ae085f03006f1f44febbb8143e92296`, snapshot
`.ufo/evidence/round-45/freshness/sources/S026.raw.gz` (41326 B gz), opened 2026-10-25, author ExecRows04,
quote `about 84% of the transitions we observe from pass to fail involve a flaky test`.

Round-45 review (`.ufo/evidence/round-45/freshness/reviews.json`, id `S026`): reviewer CritJudge06, verdict
**`agree`** — not disputed, so there is no round-45 dispute to answer for this target (the disputed targets were
S048 and S093). Its stated location (articleBody paragraph at raw line 1132, same text at 1097 in the
Blogger text/template copy) is reproduced below from fresh bytes.

## 2. Live fetch

```
curl -sS -L -D "$S/S026.headers" -o "$S/S026.html" \
  -w '%{http_code} %{size_download}\n' 'https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html'
=> 200 236387
```

Response headers (`S026.headers`, copied from the live response): `HTTP/2 200`, `content-type: text/html;
charset=UTF-8`, `date: Mon, 26 Oct 2026 08:40:50 GMT`, `last-modified: Sat, 24 Oct 2026 06:42:39 GMT`,
`cache-control: private, max-age=0`, `server: GSE`. No redirect hop on the recorded URL.

Receipt (`.ufo/waves/round-48/w1/sources/S026.receipt.json`), every field verified against the delivered bytes:

```json
{"url": "https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html",
 "fetched_at": "2026-10-26T08:40:51Z", "http_status": 200, "bytes": 236387,
 "sha256": "a4c5c46b4af9d54baa215b9d76c91cb5b8e9855ad153103b0a34ff3e39869d25",
 "tool": "curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5 zlib/1.3.2 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.70.0 ngtcp2/1.25.0 nghttp3/1.18.0 mit-krb5/1.22.2"}
```

Checks run: receipt `sha256 == sha256(delivered S026.html)`, `bytes == 236387 == wc -c`, `http_status 200`,
`fetched_at` date `2026-10-26`. Receipt URL equals the base row URL (contract amendment 1: it is in R's set).

Snapshot delivered byte-exact at `.ufo/waves/round-48/w1/sources/S026.html`
(sha256 `a4c5c46b4af9d54baa215b9d76c91cb5b8e9855ad153103b0a34ff3e39869d25`, 236387 bytes; `cmp` against the
fetched file: identical). Nothing was re-encoded, decompressed or reformatted.

## 3. Extraction (contract amendment 2) and quote

Extraction: UTF-8 decode → drop `<script>`/`<style>` element contents → strip tags → `html.unescape` →
collapse whitespace. Round-45's counter `extract()` (`fold()`: NFKC plus quote/dash folding) was applied as the
compatible fold; the quote contains no character affected by folding, so the result is fold-independent.
Extracted text: **26246 chars**, sha256 `6e8b4d19dffde90b9fd88dd279096a2f4ebcd90541cfe580e853a2fc2343b95a`.

**Quote (exact, 15 whitespace tokens):**

```
about 84% of the transitions we observe from pass to fail involve a flaky test
```

- Required phrase `84%`: present (once in the quote).
- Located: substring of the extracted text, one occurrence, char offset **2136** (0-based) — the text reads
  `... What we find in practice is that about 84% ...`.
- Location in the raw file: post body, `/html/body//div[contains(@class,'post-content')][@itemprop='articleBody']`,
  the paragraph rendered inside its `<noscript>` fallback at **raw line 1132**; the same sentence also occurs
  verbatim at **raw line 1097** inside the preceding `<script type='text/template'>` body copy. Section heading:
  the post's own `<h2 class='title' itemprop='name'>` "Flaky Tests at Google and How We Mitigate Them"
  (raw line 1074) — the post body has no sub-heading above this paragraph. Publish date on the page:
  `Friday, May 27, 2016` (`<span class='publishdate' itemprop='datePublished'>`, raw line 1082).
- Teaches claim stated? The quote carries the 84% pass→fail clause. The row's other two clauses also still
  hold live in the same extracted text: `about 1.5% of all test runs reporting a "flaky" result` (raw line 1130)
  and `causing it to report a failure only if it fails 3 times in a row. This reduces false positives, but
  encourages developers to ignore flakiness in their own tests` (raw line 1136).

## 4. Drift: live vs round-45 snapshot vs base anchor

| | sha256 | bytes |
|---|---|---|
| live fetch 2026-10-26 | `a4c5c46b4af9d54baa215b9d76c91cb5b8e9855ad153103b0a34ff3e39869d25` | 236387 |
| round-45 snapshot (gunzipped `S026.raw.gz`) | `5d74dd1c3c75d5ec1b8d53d6a518b4b01ae085f03006f1f44febbb8143e92296` | 236387 |
| base row anchor | no digest in the anchor cell ("Post body, published 2016-05-27 (fetched 2026-10-19)") | — |

Raw-byte difference: **14 bytes**, all inside one same-length token at offsets 232727–232743: the Blogger page
config `'dynamicViewsScriptSrc': '//www.blogblog.com/dynamicviews/<hash>'` moved from `fa12fcebe36ff135`
(round-45) to `2abac2b3aa987931` (live). `cmp -l` reports no other difference; file length is unchanged.

Content difference: **none**. The amendment-2 extracted text of live and round-45 bytes is byte-identical
(26246 chars, same sha256 `6e8b4d19…`), the quote occurs once at the same offset 2136 in both, and the publish
date is unchanged. So the sha churn is page chrome (a versioned Dynamic Views asset id), not post content —
`last-modified: Sat, 24 Oct 2026 06:42:39 GMT` is consistent with the page template being re-served with a new
asset id.

**Verdict: holds (drifted bytes, stable content).** The teaches cell still holds in full; the anchor digest must
be refreshed to the live bytes because the round-45 anchor hash no longer matches what the URL serves.

## 5. Proposed anchor cell text (for the superseding row R)

```
Post body (h2 title, publishdate 2016-05-27; raw line 1132) @ fetched 2026-10-26, sha256 a4c5c46b4af9, 236387 bytes
```

Carries: section (`Post body`), revision/date (`publishdate 2016-05-27`, `fetched 2026-10-26`), the snapshot's
12-hex sha256 prefix (`a4c5c46b4af9`) and the byte count (`236387`), as C2 requires. The row's source cell keeps
the unchanged canonical URL above; the snapshot to commit is this file under
`.ufo/evidence/round-48/freshness/sources/` (suggested `S026.html`), and the receipt next to it.

## 6. Controls this fetch supports

- CTL_H (quote-without-phrase) does not bite here: the round-45 and live quotes both contain `84%`, so S026 is
  one of the ≤2 targets CTL_H can still credit, as the contract expects.
- CTL_G (rows-only) is unaffected by this delivery: a row pointing at the round-45 snapshot cannot carry the
  live 12-hex `a4c5c46b4af9`, so it stays unrefreshed.

## 7. Tooling, hygiene, risks

- No tool installed or upgraded (curl 8.23.0 and gzip were already present). No pacman call.
- Scratch: `/fast/scratch/hyaku/tameshi-r48/T48ExecFetchS026` (one shared clone not needed; only the fetch,
  gunzip of the round-45 snapshot for comparison, and extraction ran there). Removed before this report was
  finalised; nothing left under `/fast/scratch/hyaku/tameshi-r48/T48ExecFetchS026`.
- Read-only on the lane: no edit to `corpus/SOURCES.md`, `corpus/knowledge/*`, `corpus/lessons/*`, no git/jj
  state touched. Lane clone not created because the work needed only committed files plus the live fetch.
- Risk: the live document is CSP/dynamic-Views templated, so byte hashes churn while content is stable. The
  deciding run must re-fetch and compare the *quote/extracted text* rather than assume the delivered digest
  stays valid; if the bytes drift again, the C2 anchor digest will not match and that target would be
  unrefreshed at the deciding run. Reported as observed, not remediated.

## Deliverables

- `.ufo/waves/round-48/w1/sources/S026.html` — fetched bytes, 236387 B, sha256 `a4c5c46b4af9d54baa215b9d76c91cb5b8e9855ad153103b0a34ff3e39869d25`.
- `.ufo/waves/round-48/w1/sources/S026.receipt.json` — receipt as above.
- This report.
