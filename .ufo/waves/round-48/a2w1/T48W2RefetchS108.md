# T48W2RefetchS108 — independent re-open of C2 target S108

- Seat: `T48W2RefetchS108` (leaf; no dispatch). Item: re-open S108 at CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`, fetch the receipt URL live into scratch, test the quote (live + snapshot, <=25 tokens, required phrase, states the row's teaches claim), then test every S108-dependent claim in the used-by knowledge entry.
- Base `473336d9d789f6081195e7376d17836a24666bc3`; content rev `c7586b9a` is a commit; `git diff --stat c7586b9a HEAD` = 4 added files under `.ufo/waves/round-48/` only, `git diff --stat c7586b9a HEAD -- corpus` empty, so every corpus read below is content-rev content.
- Scratch: `S=/fast/scratch/hyaku/tameshi-r48/T48W2RefetchS108` (~1.6 MB of fetches), deleted before this report was finalized. No counter was run at the content revision (amendment 8): the frozen counter's pure functions (`parse_rows`, `check_row`, `check_snapshot`, `check_receipt`, `check_quote`, `check_phrases`, `check_entries`, `extract`) were imported read-only and driven by hand. Nothing is scored here; this is a probe report.
- No tool installed or upgraded; no pacman call.

**Verdict: no predicate-level defect in S108's C2 chain.** Row grammar, source URL, snapshot, receipt, Gate line, snapshot location, live location, phrase and citation all reproduce. Three minor documentation-accuracy findings (F1-F3) in the entry's and the lesson's *prose*, none of which touches a counter check, plus one live-stability risk (R1).

## 1. The superseding row

```
$ grep -c "supersedes S108 —" corpus/SOURCES.md      → 1      (SOURCES.md:143)
```

`parse_rows(show_text(lane, c7586b9a, SOURCES))` → 128 rows; candidate filter of `check_row('S108', …)` (= `teaches.startswith('supersedes S108 —')` and `id > S264`) returns exactly `S268`.

| field | value | check |
|---|---|---|
| id | S268 (above S264) | ok |
| teaches | `supersedes S108 — the zh-cn page still states that .expected files are updated by running the affected test with --test_arg=--update_goldens --test_strategy=local and that the resulting diff is checked; the sentence is re-located verbatim in the 2026-10-26 snapshot` | opens `supersedes S108 —` (U+2014) |
| source URL set | `https://www.tensorflow.org/federated/golden_tests?hl=zh-cn` | equals S108's base source+anchor URL set (amendment 1) |
| anchor | `§如何更新 .expected 文件？, … raw line 3611 (heading raw line 3609) … S108.html 111409 B sha256 04e4c091715a` | sha prefix present |
| opened / status / kind / tier | 2026-10-26 / mined / docs / B | ok |
| used-by | `corpus/knowledge/r8-golden-update-flag.md` | equals S108's base used-by set |

`check_row` → `ok S268`. (Note: an earlier `awk -F'|'` of mine mis-indexed the teaches cell because this registry row carries a `|` inside an earlier cell; the counter's own parser is authoritative and shows the prefix present. Not a defect.)

## 2. Snapshot and receipt (bytes and sha256)

| artifact | bytes | sha256 |
|---|---|---|
| `.ufo/evidence/round-48/freshness/sources/S108.html` | 111409 | `04e4c091715a9ee2258cb12f52af6c64aa3134c6afc3669501b14f20966d1af1` |
| `S108.receipt.json` | — | `…04e4c091715a…`, url = the row URL, `fetched_at 2026-10-26T08:41:18Z`, `http_status 200`, `bytes 111409` |
| (prior carrier) `.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` | 111405 | `f27cf274b5dd7c28122dcb5a137971b401dad7910f7702eb4cbd3c28cd782bf0` |

`ls .ufo/evidence/round-48/freshness/sources/` holds exactly one `S108.*` non-receipt file and one `S108.receipt.json` (no ambiguity). `check_snapshot` → `ok`, `check_receipt` → `ok`; the receipt sha equals the snapshot digest and the anchor carries its 12-hex prefix.

Snapshot structure backs the anchor cell: `S108.html:3609` is the `<h2 …>如何更新 <code>.expected</code> 文件？</h2>` and `S108.html:3611` is the section's only `<p>` (the section closes with `</div>` at `:3616`). Live response headers carry `last-modified: Tue, 07 Jun 2022 16:32:12 GMT`, matching the anchor text.

## 3. Gate line and the quote

`corpus/lessons/round-48.md:24`:

```
- C2-QUOTE S268 S108: `可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。`
```

| check | observed |
|---|---|
| matches `GATE_RE ^- C2-QUOTE (S\d{3,}) (S\d{3,}): \`([^\`]+)\`` | yes; names R=S268 then T=S108; exactly one Gate line names S108 |
| quote length | 106 chars / **6 whitespace tokens** (<= 25) |
| required phrase `--update_goldens` | present in the quote |
| located in snapshot (amendment-2 extraction, `extract()`) | **yes, exactly once**, 0-based offset 2513 of a 3496-char text |
| located live | **yes, exactly once at the same offset 2513**, in all 6 fetches, same 3496-char text |
| states the row's teaches claim (not boilerplate/navigation) | yes — article body, after the `path/ to/ some_test_goldens/` listing: `.expected` files are updated by running the affected test targets with `--test_arg=--update_goldens --test_strategy=local`, and the resulting diff should be checked for unexpected changes |

`check_quote` → `ok words 6`, `check_phrases` → `ok`.

## 4. Live re-fetch (mine, into scratch)

`curl -sS -L -o live.html -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective}' 'https://www.tensorflow.org/federated/golden_tests?hl=zh-cn'` → `http_code=200 size=111405`, effective url identical to the receipt url. Six variants, all HTTP 200, all extracting to **one** text (`sha256(text)[:16] = e83fc1baae0710f4`, 3496 chars), all containing the quote once at 2513:

| fetch variant | bytes | raw sha256 (first 16) |
|---|---|---|
| default (HTTP/2) | 111405 | `b514a6bcf0931918` |
| `Accept-Language: en` | 111409 | `9d941a02ba6ceac6` |
| `Accept-Language: ja` | 111409 | `36a50c404d2c8fb8` |
| `--compressed` | 111409 | `a7ab67ecd71ad3c0` |
| UA `tameshi-c2-r48/1.0 …` (the counter's own UA) | 111405 | `e555e5e91998a143` |
| `--http1.1` | 111409 | `80f8278695c66dc2` |

`snap.html` and the round-40 snapshot extract to the same text digest `e83fc1ba…`, so the entry's "extracted article text is identical" is independently confirmed against 6 live fetches plus both snapshots. The raw bytes differ from the snapshot only in per-request blocks; line diff of `snap.html` vs today's default fetch is 3 changed lines: `:4068` analytics JSON key order, `:4079` CSP `nonce`, `:4084` devsite flag list. The 21 `hreflang` lines are byte-identical.

## 5. The used-by entry, claim by claim

`corpus/knowledge/r8-golden-update-flag.md` is the only base used-by entry (`check_entries` → `ok`: `source:` line carries S268, `verified-at:` line starts 2026-10-26, R's used-by set equals the base set). `corpus/knowledge/r40-write-form-misses.md:14` also mentions S108 but states "S108 is not support for this entry", and its `source:` line is S152 — nothing there rests on S108.

| entry claim (line) | vs live text | verdict |
|---|---|---|
| §如何更新 .expected 文件？ heading and paragraph "are unchanged" (line 2) | round-40 snapshot, round-48 snapshot and 6 live fetches all extract to the identical 3496-char text | holds |
| "the paragraph is re-located in the 2026-10-26 snapshot" (line 2) | quote found once at 2513 in `S108.html`'s extraction | holds |
| "a line diff against today's live fetch (**104928 B**) finds only the head hreflang link block, the language-selector menu and the per-request script blocks" (line 2) | no 104928-byte response observed; today's live is 111405 or 111409 B. My diff has no hreflang or language-menu line, only the 3 script-block lines | **F1 + F2** (detail unreproducible; conclusion still holds) |
| "so the extracted article text is identical" (line 2) | 8/8 documents extract to `e83fc1ba…` | holds |
| "S107 … was not re-fetched" (line 2) | the URL is commit-pinned as stated; "not re-fetched" is a negative work claim no artifact can confirm | unverifiable, not contradicted |
| "The same page's official zh-cn localization restates that flag and the diff check" (line 10) | live: 可以通过使用参数 … --test_arg=--update_goldens … 来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。 | holds |
| "The note describes a documented flag. It is not a run …" (line 18) | boundary statement, not an S108 text claim | n/a |

No claim that rests on S108 has stopped holding while being re-pointed.

## Findings

**F1 — minor, documentation accuracy (not a counter check).** `corpus/knowledge/r8-golden-update-flag.md:2` names the live fetch it diffed as "(104928 B)". No response of that size exists in my observations: `for v in default al:en al:ja compressed ua h1; do curl …; done` → 111405 or 111409 B only; the snapshot's own fetch is 111409 B. The lesson's census names a different unreproduced figure (104924, `corpus/lessons/round-48.md:373`). Show: `wc -c live*.html` over the six fetches in the scratch dir reproduced per §4. Suggested fix (not applied — read-only lane): drop the parenthetical byte count or state the observed range.

**F2 — minor, documentation accuracy (not a counter check).** Same line: the diff enumeration claims the head hreflang link block and the language-selector menu changed. Show: `diff snap.html live.html` → 3 changed lines (`:4068` analytics JSON key order, `:4079` nonce, `:4084` devsite flag list); `grep -c hreflang snap.html live.html` → 21 and 21. The enumeration is a superset of what reproduces today; the sentence's conclusion ("extracted article text is identical") is true, so this weakens the evidence trail, not the claim.

**F3 — minor, lesson prose.** `corpus/lessons/round-48.md:78` says the quote was "found once, at offset 2 533 of 3 496 characters". Show: `python3 -c` driving the frozen `extract()` over `S108.html`, the round-40 snapshot and all six live fetches → offset **2513** (0-based code points) in a 3496-char text, 8/8. The character count reproduces; the offset does not (off by 20; 1-based would be 2514). The Gate line itself is unaffected.

**R1 — risk, not a defect.** `corpus/lessons/round-48.md:372-373` records that seven attempt-1 fetches produced two extracted text variants (3496 and 3148 chars) and sizes including 104924 B. My 8 documents show one text variant and two sizes. If the deciding run's single live fetch were served the alleged shorter variant and the quote were absent from it, the counter's live check would read `absent` for S108 (`corpus/…/freshness/measure.py:335-343`). Not observed today; named so the L1 knows the deciding run's live fetch is the only one that binds.

**Observation (no action).** S108's superseded teaches said `.expected` files "update **only** via --update_goldens"; the live zh-cn text offers a method (可以通过使用参数 … 来更新) and asserts no exclusivity (no 仅/只). S268's teaches and the entry both drop "only", so the refetch corrected the overclaim rather than propagating it. Separately, row/entry prose says "the affected test" where the page says 测试目标 (test targets); the Gate line quote is verbatim, so no gate is affected.

## Reproduced check tally (S108)

`row ok · snapshot ok (04e4c091715a…) · receipt ok · quote_in_snapshot ok (6 words) · phrases ok · entries ok · live quote in 6/6 fetches · receipt url = row url = base url · one snapshot file, one receipt`.
