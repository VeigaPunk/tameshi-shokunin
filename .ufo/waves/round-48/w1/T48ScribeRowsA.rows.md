# T48ScribeRowsA — C2 superseding rows and entry re-points for S026 and S048

Round 48 (hyaku run 8, attempt 1), wave 1. Lane `tameshi-shokunin`, base
`473336d9d789f6081195e7376d17836a24666bc3`, contract
`.ufo/evidence/round-48/contract.json` incl. amendments 1-3 (read first, not edited).
Owner of this draft: seat T48ScribeRowsA. Deliverable only: the L1 applies it.

Nothing below was written into `corpus/SOURCES.md`, `corpus/knowledge/*` or
`corpus/lessons/round-48.md` in the lane. The rows and lines were proved by
staging them in a scratch clone under `/fast/scratch/hyaku/tameshi-r48/T48ScribeRowsA/`
and running the wave-1 C2 counter there (probe, `--no-live` and live; see §7).

## 1. Registry rows (paste both, in this order, immediately after the current last registry row — S264, `corpus/SOURCES.md:139`)

```
| S265 | Flaky Tests at Google and How We Mitigate Them (John Micco, Google Testing Blog, 2016) — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | docs | A | supersedes S026's anchor and quote only: Google's flakiness rates and mitigations, re-anchored to the 2026-10-26 bytes | Post body (h2 title; publishdate 2016-05-27; articleBody paragraph at raw line 1132); fetched 2026-10-26, sha256 a4c5c46b4af9, 236387 bytes | supersedes S026 — about 1.5% of test runs are flaky, about 84% of pass-to-fail transitions involve a flaky test, and a fail-3-in-a-row flaky mark cuts false positives but teaches people to ignore flakiness | mined | 2026-10-26 | 730d | corpus/knowledge/repeated-control-precondition.md |
| S266 | Incremental analysis (PIT docs), object-neutral precision — https://pitest.org/quickstart/incremental_analysis/ | docs | A | supersedes S048's anchor and quote only: PIT's item-4 prioritisation distinction, with the disputed consequent located on the 2026-10-26 bytes | §Incremental analysis, item 4 (raw line 86); page version unstated, Last-Modified 2026-06-03, fetched 2026-10-26; sha256 e9cbc3e1ab7c, 8892 bytes | supersedes S048 — item 4 is prioritisation rather than a reuse skip, its consequent is the located quote, no claim here resolves its pronoun to test versus mutation, item 5 is not yet implemented and the dependency assumption remains unproven | mined | 2026-10-26 | 90d | corpus/knowledge/incremental-pin-disposition.md |
```

Row shape check (census): 11 cells, 13 `|`-fields, no `|` inside any cell; ids S265/S266 are
the next free ids (S093/S108 owners take S267/S268); `opened 2026-10-26`, `status mined`,
`recheck` keeps each base cadence (730d, 90d); used-by is exactly the base used-by cell of
each target, one path each.

Scope cells differ from the base rows by design (`supersedes <T>'s anchor and quote only: ...`),
so the census sees a new URL+scope key; the `teaches` cell also opens `supersedes S026 —` /
`supersedes S048 —` (U+2014), which is the census E04 exemption and the counter's row selector.

### Anchor digest

`sha256 a4c5c46b4af9` (S265) and `sha256 e9cbc3e1ab7c` (S266) are the first 12 hex of the
committed wave-1 snapshots I re-hashed myself:

| target | snapshot to commit under `.ufo/evidence/round-48/freshness/sources/` | bytes | sha256 |
|---|---|---|---|
| S026 | `S026.html` (copy of `.ufo/waves/round-48/w1/sources/S026.html`) | 236387 | `a4c5c46b4af9d54baa215b9d76c91cb5b8e9855ad153103b0a34ff3e39869d25` |
| S048 | `S048.html` (copy of `.ufo/waves/round-48/w1/sources/S048.html`) | 8892 | `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db` |

Placeholders, if the L1's committed copy differs by a byte: `sha256 @SHA:S026@` /
`sha256 @SHA:S048@` — fill from the committed snapshot, and remember the receipt `sha256`
must equal it. The C2 counter requires **exactly one** `S026.*` / `S048.*` file under that
directory besides `<T>.receipt.json` (a `S026.headers` file there would read
`snapshot=ambiguous`). Copy the two wave-1 receipts unchanged: both already carry
`fetched_at` on 2026-10-26, `http_status 200`, the digest above and a `url` equal to the row's
source URL, which is in the row's URL set (contract amendment 1).

## 2. Gate lines (one per row, into `corpus/lessons/round-48.md`, `## Gate`)

```
- C2-QUOTE S265 S026: `about 84% of the transitions we observe from pass to fail involve a flaky test`
- C2-QUOTE S266 S048: `then it is likely that the last killing test will still kill it and it should therefore be prioritised above others`
```

Both were chosen by the fetch seats and independently re-checked by me against the wave-1
snapshot with the counter's own `extract()`: S026 quote 15 whitespace tokens, exactly one
occurrence, carrying `84%`; S048 quote 21 tokens, exactly one occurrence, carrying
`should therefore be prioritised`. Neither exceeds 25 words; neither uses case/punctuation
folding. I use the fetch seat's quote verbatim in both cases (neither needed replacement).

## 3. Entry edits

### 3.1 `corpus/knowledge/repeated-control-precondition.md` (base used-by cell of S026)

Old line 1:

```
source: S004 — https://mutants.rs/using-results.html — §§“Tests fail in an clean tree?”, “Mutant outcomes”; fetched 2026-10-20T02:13:47Z, sha256 5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334 (29,579 B); S026 — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html — post body by John Micco, published 2016-05-27; fetched 2026-10-20T02:13:47Z, sha256 ca1145fbe56de30b43b66baf7372206a38abe08a55b3db13f6c7a0114d7a6c8c (236,385 B). Located excerpts: `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv`
```

Replacement line 1 (paste as one line; only the S026 segment changed — S004 is untouched):

```
source: S004 — https://mutants.rs/using-results.html — §§“Tests fail in an clean tree?”, “Mutant outcomes”; fetched 2026-10-20T02:13:47Z, sha256 5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334 (29,579 B); S265 (supersedes S026) — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html — post body by John Micco, published 2016-05-27; re-fetched 2026-10-26T08:40:51Z, sha256 a4c5c46b4af9d54baa215b9d76c91cb5b8e9855ad153103b0a34ff3e39869d25 (236,387 B). Located excerpts: `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv`
```

Old line 2 → new line 2:

```
- verified-at: 2026-10-20
+ verified-at: 2026-10-26
```

What changed in the source line and why: the entry's own S026 receipt
(`fetched 2026-10-20T02:13:47Z, sha256 ca1145fb… (236,385 B)`) is no longer what the URL
serves and no longer what the committed snapshot is. Rather than delete the receipt, the
segment now cites the superseding row (`S265 (supersedes S026)`) and carries the 2026-10-26
fetch facts (`re-fetched 2026-10-26T08:40:51Z, sha256 a4c5c46b… (236,387 B)`). The old URL
is kept unchanged, as required. The `recheck:` line and the round-12 receipt pointer are
untouched; both were re-tested (§6.3).

### 3.2 `corpus/knowledge/incremental-pin-disposition.md` (base used-by cell of S048)

Old line 1:

```
source: S003 — https://stryker-mutator.io/docs/stryker-js/incremental/ — §Incremental mode, §Limitations, §Forcing reruns; fetched 2026-10-20T04:46:12Z, sha256 9054e311a0569231aa2a1427a4137729c8180d7f2687dfd450322e855cc9ad90 (33,898 B); S041 — https://pitest.org/quickstart/incremental_analysis/ — §Incremental analysis; fetched 2026-10-20T04:46:12Z, sha256 e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db (8,892 B); S047 — the same URL and the same fetched bytes as S041, cited as the round-13 precision-correction row that supersedes S041's teaches cell (numbered optimisations 1–5 and the dependency paragraphs; page version unstated); S031 — tools/mutate-and-run.sh:80-89, 540-553 @ 4eb4cf3, sha256 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5 (own-work: the six-leg pins and recorded tables). The quoted excerpts in §1 are the retained location; the full-page digests make each fetch reproducible.
```

Replacement line 1 (one line; the new S266 segment is inserted after the S031 segment, the
S003/S041/S047 cites and their digests are kept byte-for-byte, including S041's copy of the
same URL):

```
source: S003 — https://stryker-mutator.io/docs/stryker-js/incremental/ — §Incremental mode, §Limitations, §Forcing reruns; fetched 2026-10-20T04:46:12Z, sha256 9054e311a0569231aa2a1427a4137729c8180d7f2687dfd450322e855cc9ad90 (33,898 B); S041 — https://pitest.org/quickstart/incremental_analysis/ — §Incremental analysis; fetched 2026-10-20T04:46:12Z, sha256 e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db (8,892 B); S047 — the same URL and the same fetched bytes as S041, cited as the round-13 precision-correction row that supersedes S041's teaches cell (numbered optimisations 1–5 and the dependency paragraphs; page version unstated); S031 — tools/mutate-and-run.sh:80-89, 540-553 @ 4eb4cf3, sha256 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5 (own-work: the six-leg pins and recorded tables); S266 — https://pitest.org/quickstart/incremental_analysis/ — §Incremental analysis (numbered items 1–5 and the dependency paragraphs); re-fetched 2026-10-26T08:40:42Z, sha256 e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db (8,892 B). The quoted excerpts in §1 are the retained location; the full-page digests make each fetch reproducible.
```

Old line 2 → new line 2:

```
- verified-at: 2026-10-20
+ verified-at: 2026-10-26
```

Line 5 (`source-correction: S048 — https://pitest.org/quickstart/incremental_analysis/ — …`)
is **not** changed: it describes S048's teaching correction, which is still true, and the
frozen C2 statement only requires the `source:` line to cite R plus a `verified-at` carrying
2026-10-26. If the L1 prefers every S048 cite to point at the superseding row, the only edit
needed there is `source-correction: S048 → source-correction: S266 (supersedes S048)`; that is
optional and outside the predicate as frozen.

## 4. Gate block prose (CORPUS.md rule 1 — URL, access date, quote, location)

Paste under `## Gate` in `corpus/lessons/round-48.md`, next to the two `- C2-QUOTE` lines:

```markdown
- **S265 (S026)** — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html,
  opened 2026-10-26 (HTTP 200, 236387 bytes, sha256 `a4c5c46b4af9…`). Quote (15 words): “about
  84% of the transitions we observe from pass to fail involve a flaky test”. Location: post
  body, `div[itemprop='articleBody']` paragraph at raw line 1132 of the committed snapshot
  (publishdate 2016-05-27 at raw line 1082; the same sentence also appears in the page's
  `text/template` body copy at raw line 1097). Grounds `teaches`: the 84% pass-to-fail clause,
  which is the one the entry uses for the retry/rerun argument.
- **S266 (S048)** — https://pitest.org/quickstart/incremental_analysis/, opened 2026-10-26
  (HTTP 200, 8892 bytes, sha256 `e9cbc3e1ab7c…`, `Last-Modified: 2026-06-03`). Quote (21
  words): “then it is likely that the last killing test will still kill it and it should
  therefore be prioritised above others”. Location: `§Incremental analysis`, the fourth `<li>`
  of the optimisation list (raw line 86), immediately after “If a mutation was previously
  killed, but the class or killing test has changed”. Grounds `teaches`: item 4's consequent is
  a prioritisation, not a reuse skip, and the pronoun in “still kill it” is left unresolved.
  This is the consequence round-45's dispute said the old quote dropped.
```

## 5. What each row claims (consistency with the base teaches)

- S265 keeps S026's three clauses and re-anchors them: 1.5% flaky rate, 84% of pass→fail
  transitions involve a flaky test, fail-3-in-a-row cuts false positives while teaching people
  to ignore flakiness. All three were re-located in the live text (§6.3).
- S266 keeps S048's substance: item 4 is prioritisation, no pronoun resolution, item 5 not yet
  implemented, dependency assumption unproven. All four were re-located in the live text
  (§6.3). The only addition is that the disputed consequent is now the located quote.

## 6. Verification performed by this seat

### 6.1 Independent live fetch (my own, before reading the fetch reports' conclusions)

```
curl -sS -D h026.txt -o s026.html -w '%{http_code}\n' https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html  -> 200
curl -sS -D h048.txt -o s048.html -w '%{http_code}\n' https://pitest.org/quickstart/incremental_analysis/                              -> 200
sha256sum: s026.html a4c5c46b4af9d54baa215b9d76c91cb5b8e9855ad153103b0a34ff3e39869d25  (236387 B)
           s048.html e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db  (8892 B)
```

Both digests equal the wave-1 snapshots byte-for-byte, so the anchors in §1 describe exactly
what will be committed.

### 6.2 Quote location (counter `extract()` = amendment 2, no folding)

| target | quote | tokens | occurrences | char offset | raw line(s) |
|---|---|---|---|---|---|
| S026 | about 84% of the transitions we observe from pass to fail involve a flaky test | 15 | 1 | 2136 | 1132 (articleBody), 1097 (template copy) |
| S048 | then it is likely that the last killing test will still kill it and it should therefore be prioritised above others | 21 | 1 | 1013 | 86 |

Extracted-text length: S026 26246 chars, S048 3253 chars.

### 6.3 Entry claims checked against the live text (quoted; all still hold)

`corpus/knowledge/repeated-control-precondition.md`:

- definition — “We define a "flaky" test result as a test that exhibits both a passing and a failing result with the same code.” (raw line 1130) — holds.
- rate — “a continual rate of about 1.5% of all test runs reporting a "flaky" result”; “Almost 16% of our tests have some level of flakiness associated with them!” (raw line 1130) — holds.
- transitions — “about 84% of the transitions we observe from pass to fail involve a flaky test”; monitors “wait for additional CI cycles to run this test again” (raw line 1132) — holds.
- retry family — “the ability to re-run only failing tests, and an option to re-run tests automatically when they fail”; “causing it to report a failure only if it fails 3 times in a row. This reduces false positives, but encourages developers to ignore flakiness in their own tests unless their tests start failing 3 times in a row, which is hardly a perfect solution.” (raw line 1136) — holds in substance, see finding F2 for the bracketed spelling.
- cost — “The breakage will not be discovered until 3 executions of the test complete, or 45 minutes” (raw line 1137) — holds.
- line anchors — the entry's `S026.html:1130-1137` and template copy `:1095-1102` still address these sentences in the live file.
- `recheck:` command — `grep -c 'hardly a perfect solution'` on the live bytes → **2** (post body + template copy), the entry's healthy count; 0 would be drift.

`corpus/knowledge/incremental-pin-disposition.md`:

- rule 2 — “If a mutation was killed in the last run and neither the class under test or the killing test has changed, then it can be assumed that this mutation is still killed.” — holds.
- rule 3 — “If a mutation survived in the last run, no new tests cover it, and none of the covering tests have changed, then it must still survive.” — holds.
- item 4 — “If a mutation was previously killed, but the class or killing test has changed then it is likely that the last killing test will still kill it and it should therefore be prioritised above others. (since 1.14.4)” — holds.
- item 5 — “… (not yet implemented)” — holds.
- potential-error sentence — “With the exception of 4), all these optimisations introduce a degree of potential error into the analysis.” — holds.
- dependency paragraphs — “PIT will only consider the strongest of these dependencies - changes to super classes and outer classes, when deciding if a class's behaviour might have changed.” and “… Although this assumption seems reasonable, it is currently unproven.” — hold.
- history provenance — “you will need to implement some mechanism to swap the values between runs” — holds.

### 6.4 Byte drift since the base receipts

| target | 2026-10-20 (entry receipt) | round-45 snapshot | live 2026-10-26 | content |
|---|---|---|---|---|
| S026 | `ca1145fb…` 236385 B | `5d74dd1c…` 236387 B | `a4c5c46b…` 236387 B | identical under amendment-2 extraction (26246 chars, quote at offset 2136 in both) |
| S048 | `e9cbc3e1…` 8892 B | `e9cbc3e1…` 8892 B (`cmp` identical) | `e9cbc3e1…` 8892 B | unchanged |

S026's 14 changed bytes (offsets 232727-232742, same length) are the Blogger
`dynamicviews` asset id `fa12fcebe36ff135` → `2abac2b3aa987931`; no body text changed
(`extract(round-45) == extract(live)` is True). That is why the anchor digest must move to
`a4c5c46b4af9` while the teaches cell does not change.

## 7. Probe (scratch clone, not the lane, not a verdict)

Staged in `/fast/scratch/hyaku/tameshi-r48/T48ScribeRowsA/lane` (shared clone of the lane at
HEAD `f1cfaad`, scratch commit `fc30ca1`): the two rows, both entry edits, the two gate
lines, the two snapshots+receipts under `.ufo/evidence/round-48/freshness/sources/`, and the
counter copied byte-exact to `.ufo/evidence/round-48/freshness/measure.py`. Then:

```
python3 .ufo/evidence/round-48/freshness/measure.py --lane <clone> --rev HEAD --no-live
TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
TARGET S048 row=S266 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
TARGET S093 row=none ... NOT
TARGET S108 row=none ... NOT
C2_R48: self_pin=1 targets=4 refreshed=2 census_exit=0 live=off rev=HEAD C2_R48_PARTIAL=false
exit 1   (expected: the other two targets are other seats' deliverables)

same, live on:
TARGET S026 ... live=ok REFRESHED
TARGET S048 ... live=ok REFRESHED
C2_R48: self_pin=1 targets=4 refreshed=2 census_exit=0 live=on rev=HEAD C2_R48_PASS=false
exit 1
```

`census_exit=0` in both runs is the census verdict on these two rows (no E01/E03/E04/E05-E11;
the same URL under the new scope can only raise the non-fatal W04). Per-target fields for
S026 and S048 are `ok` through `entries`, and `live=ok` when live is on. The scratch clone and
directory were deleted after this measurement; the receipts are transcribed here.

## 8. Findings, limits, out of scope

- **F1 (drift, handled).** S026's page chrome churns (14 bytes between round-45 and today, all
  in a Blogger asset id). The anchor digest and the entry's fetch receipt are refreshed to the
  live bytes; the teaches content is unchanged. If the page churns again between this draft and
  the deciding run, the committed snapshot keeps the anchor honest but the `--live` check
  compares the quote, not the digest, so the target still holds unless the post text changes.
- **F2 (pre-existing, not edited).** `repeated-control-precondition.md` §1 renders the retry
  sentence as “report[s] a failure only if it fails 3 times in a row”; the live text is
  “causing it to report a failure only if it fails 3 times in a row” (no `s`). The claim holds
  and the bracketed form was the earlier writer's editorial mark, but it is not verbatim. Out
  of this seat's two-line edit scope — reported, not silently fixed.
- **F3 (out-of-cell cite, not required).** `corpus/knowledge/fleet-kill-rate-ledger.md:374`
  reads `source method: S003 and S048,` but that file is not in S048's base used-by cell, so
  the frozen C2 statement does not require re-pointing it, and R's used-by cell must not list
  it (the counter compares the used-by set exactly to the base cell). Flagged for the L1 if it
  wants the cite moved to S266 outside C2.
- **F4 (revision evidence for S048).** The PIT page states no in-body version or date; the
  row's revision evidence is the HTTP `Last-Modified: Wed, 03 Jun 2026 08:45:37 GMT` and the
  unchanged digest, with `page version unstated` kept honestly in the anchor.
- **Not measured here:** no deciding run, no control scoring, no census run outside the
  counter's own call, no C1 work. Tooling: nothing installed or upgraded (curl 8.23.0,
  python3, gzip already present; no pacman call).
- **Cleanup:** `/fast/scratch/hyaku/tameshi-r48/T48ScribeRowsA` removed; no scratch tree left.
