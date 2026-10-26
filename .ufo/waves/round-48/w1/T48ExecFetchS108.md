# T48ExecFetchS108 — C2 fetch for target S108

Seat: T48ExecFetchS108 (leaf). Contract: `.ufo/evidence/round-48/contract.json` (claims C2, amendments 1–2 read; contract not edited). Base rev `473336d9d789f6081195e7376d17836a24666bc3`. Lane checkout read-only; only my report and my two deliverables were written.

## Deliverables (written)

| path | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-48/w1/sources/S108.html` | 111409 | `04e4c091715a9ee2258cb12f52af6c64aa3134c6afc3669501b14f20966d1af1` |
| `.ufo/waves/round-48/w1/sources/S108.receipt.json` | 443 | receipt for the above |

Snapshot is byte-exact vs. the fetched file (`cmp` clean, same sha256 on both paths). Receipt fields: url `https://www.tensorflow.org/federated/golden_tests?hl=zh-cn`, fetched_at `2026-10-26T08:41:18Z` (the response `date:` header of the fetch — the fetch moment), http_status 200, bytes 111409, sha256 as above, tool `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5 zlib/1.3.2 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.70.0 ngtcp2/1.25.0 nghttp3/1.18.0 mit-krb5/1.22.2`.

Fetch command (run once, no retry): `curl -sS -L -D "$S/S108.headers" -o "$S/S108.html" -w '%{http_code} %{size_download}\n' 'https://www.tensorflow.org/federated/golden_tests?hl=zh-cn'` → `200 111409`.

Response headers of record (from `S108.headers`): `HTTP/2 200`, `last-modified: Tue, 07 Jun 2022 16:32:12 GMT`, `content-type: text/html; charset=utf-8`, `content-length: 111409`, `date: Mon, 26 Oct 2026 08:41:18 GMT`. No redirect hop (`-L` followed none).

## Quote

Exact (whitespace-collapsed, amendment 2 — decode UTF-8, drop `<script>`/`<style>` contents, strip tags, `html.unescape`, collapse whitespace runs):

```
可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。
```

- **Token count: 6** (whitespace-split; Unicode CJK runs count as single tokens, so well under the 25-word cap).
- **Required phrase `--update_goldens` present** — as its own token `--test_arg=--update_goldens`. It is the only occurrence of the phrase in the whole extracted text (`count == 1`), so the quote is not ambiguous.
- **Located verbatim** in the extracted text of the committed snapshot: substring hit at offset 2533 of the 3496-char extracted text. Confirmed twice with two independent extractors (regex tag-strip + `html.unescape`, and `html.parser` with `script`/`style` suppression) — both produce len 3496 and both locate the quote, so a counter implementing amendment 2 by either route finds it.
- **Location**: section heading `<h2 id="如何更新_expected_文件？" data-text="如何更新  .expected 文件？" tabindex="-1">如何更新  <code>.expected</code> 文件？</h2>` at **raw line 3609**; the quote is the single `<p>` of that section at **raw line 3611**, element `<p>` inside the `如何更新 .expected 文件？` section of the zh-cn rendered page (article body, after the `path/to/some_test_goldens/` example listing and before the CC-BY 4.0 footer).
- **Teaches claim**: the sentence states that affected test targets are run with `--test_arg=--update_goldens --test_strategy=local` to update `.expected` files, and that the resulting diff is inspected for unanticipated changes — i.e. the row's "update only via `--update_goldens`, and the diff is checked". Round-45 raised **no** dispute for S108 (`reviews.json` → `{"id":"S108","reviewer":"RevJudge02","verdict":"agree"}`, no review entry disputing it), so there was nothing to answer beyond locating the phrase.

Proposed Gate line (format per amendment 2 — for the L1/scribe to place in `corpus/lessons/round-48.md`; I did not write that file, it does not exist yet):

```
- C2-QUOTE S2xx S108: `可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。`
```

(`S2xx` = the superseding row id the registry assigns; next free id is S265 per contract, that assignment is not mine.)

## Drift comparison and verdict

| artefact | sha256 | bytes |
|---|---|---|
| live fetch (today) | `04e4c091715a9ee2258cb12f52af6c64aa3134c6afc3669501b14f20966d1af1` | 111409 |
| round-45 snapshot `S108.raw.gz` (decompressed) | `9056c530ca6cc9dfe036f2acd523aec7e9d7aa312fd4a5fcb2a94ad74740ff4c` | 111409 |
| base row S108 anchor cell | *(no hash — cell reads `如何更新 .expected 文件？ opened 2026-10-24`)* | — |

Raw bytes differ, **content does not**. Line-diff of the two raw files (both 4090 lines) shows exactly **3 changed lines, all outside the article body**:

1. raw line 4068 — `<script type="application/json" analytics>` dimension map: `dimension4/dimension12/dimension3…` reordered and `dimension1: "Signed out"`, `dimension6: "zh-cn"` added in the live copy.
2. raw line 4079 — CSP nonce: `nonce="yJfnByGELk+PJUEfPND5IzbJF69ljK"` (round 45) → `nonce="C6VL3Hf/oaT4wLB0w9u5qqwJM3A6HZ"` (this fetch; matches the `nonce-` in today's `content-security-policy` header).
3. raw line 4084 — devsite bootstrap JSON feature-flag list (`DevPro__…`, `Profiles__…` → `Search__enable_page_map`, `Concierge__enable_pushui`, …); same devsite build id `v5a0f9ff8b…` in both.

Every other line is identical, and after extraction the two documents are **byte-identical text** (both sha256 `e83fc1baae0710f41aa4d8a7a54439023644e038a88a6a5f0b786221152b1285`, 3496 chars).

**Verdict: no drift — teaches holds.** The `--update_goldens` statement, its section and its wording are unchanged since the round-45 snapshot; the only differences are per-request volatile markup (analytics JSON, CSP nonce, feature-flag array). The base row's anchor cell carried no sha256/bytes at all, so no hash comparison to base is possible; the comparable predecessor is the round-45 snapshot hash above.

Proposed anchor cell text (section + revision/date + `sha256 <first 12>` + bytes, in the house style of S153):

```
§如何更新 .expected 文件？ @ zh-cn page fetched 2026-10-26, last-modified 2022-06-07, snapshot .ufo/evidence/round-48/w1/sources/S108.html 111409 B sha256 04e4c091715a
```

## Evidence retained

- `S108.html` (the fetched bytes, byte-exact) and `S108.receipt.json` in the wave `sources/` dir — the only writable artefacts I touched in the lane.
- All comparisons (extraction, token count, quote location, three-line raw diff, extracted-text equality) were recomputed from the **committed deliverable copy**, not from the scratch file, so the report's numbers describe what is on disk in the lane.
- Scratch `/fast/scratch/hyaku/tameshi-r48/T48ExecFetchS108` removed (`rm -rf` on exit path). No clone was needed (this item is a single live fetch, not a repo experiment); no fixture repo created; no git or jj command run in the lane; nothing installed or upgraded (no tooling change to record).

## Risks / notes for the L1

1. **Live byte instability (design-relevant for C2 live mode).** This target is rendered by devsite with a per-request CSP nonce, an analytics JSON block and a feature-flag array; every refetch will produce a **different** raw sha256 at identical byte length (111409 both times, hashes differ). A `--live` deciding run that re-fetches and compares the *live bytes* to the committed snapshot hash will mismatch on this target for reasons unrelated to content. The contract as written only requires receipt.sha256 == snapshot.sha256 and http_status 200, which is stable — but if the C2 counter re-fetches live and requires byte equality, S108 is the target most likely to produce a spurious `refreshed<4`. Content-level equality holds (extracted text identical). Worth pinning in the counter freeze.
2. **Snapshot path.** My item's deliverable path is `.ufo/waves/round-48/w1/sources/`; the contract's C2 statement names `.ufo/evidence/round-48/freshness/sources/T.*` (that dir currently exists but is empty). The wave files must be relocated/pinned to the evidence path (or the counter taught the wave path) before the deciding run — my proposed anchor text uses the wave path, so adjust the cell if the pin moves the file.
3. **Citing entry untouched.** `corpus/knowledge/r8-golden-update-flag.md` line 1 cites both `S107` and `S108` on one `source:` line, `verified-at: 2026-10-24`. Per my item I edited nothing; the re-point must **keep S107** and replace only the S108 cite with the new id, and `verified-at` must move to 2026-10-26 while S107's round-45 re-anchor (S107 is not a round-48 target) stays valid — a shared-line edit is the easy way to break S107 inadvertently.
4. **Anchor wording.** `last-modified: Tue, 07 Jun 2022 16:32:12 GMT` is the page revision evidence available; there is no visible "last updated" string in the body, so the anchor's revision component rests on that header plus the fetch date.
