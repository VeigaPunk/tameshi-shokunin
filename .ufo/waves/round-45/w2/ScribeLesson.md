seat: ScribeLesson

# Round 45 lesson draft (`corpus/lessons/round-45.md`) — not written

Item: draft the round-45 lesson in the shape of `corpus/lessons/round-44.md`; the lane
checkout stays read-only except this report. Nothing was written to
`corpus/lessons/round-45.md`. Scratch: `/tmp/tameshi-r45-ScribeLesson/` (empty; no scratch
file was needed — every value below is read or measured in place).

Bounds honored: contract read first and never edited
(`.ufo/evidence/round-45/contract.json`); no counter executed at all (not even
`--selftest`/`--check`/`--extract`) — the deciding run is the L1's; no git/jj command that
writes; the read-only package was not opened (its content reached me through the wave-1
reports and the committed receipts); no `agent://all` message.

---

## 1. Draft — verbatim content for `corpus/lessons/round-45.md`

````markdown
# Round 45 lesson

author: tameshi L1 (hyaku run 7, attempt 1)
date: 2026-10-25

## Gate

Theme: **GoogleTest test-order and fixture lifecycle** — adopt two GoogleTest upstream
documents from the read-only package `shokuknow/merge/tameshi` as new rows S256/S257, each
cited by a re-grounded knowledge entry. This is the round's coverage move (C2, sourced with
assimilation); the freshness move (C1) is measured in SCORECARD and contributes no row
here. Both documents are pinned to upstream commit
`cd8e73f067129f8489e35c7b51c7a68552b289d2`, so the admission is a document adoption, not a
"latest master" capture.

### Admit — S256 (new row): Advanced GoogleTest Topics, `docs/advanced.md`

- URL https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/advanced.md;
  access date 2026-10-25; 2457 lines. Snapshot
  `.ufo/evidence/round-45/coverage/sources/googletest-advanced.md`, SHA-256
  `05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2`.
- Located quotes (`grep -nF` against the snapshot; each found once, at the cited line;
  token counts measured as whitespace tokens, not estimated):
  - line 896, 15 tokens: “Remember that the test order is undefined, so your code can't depend on a test”
  - line 1977, 8 tokens: “This helps to reveal bad dependencies between tests.”
  - line 1980, 8 tokens: “Therefore you'll get a different order every time.”
- Scope: the upstream normative statement of the F3 determinism precondition — test order
  is undefined (§Sharing Resources Between Tests in the Same Test Suite, line 870);
  `--gtest_shuffle` reveals bad inter-test dependencies and the computed seed is printed so
  an order-related failure can be reproduced (§Shuffling the Tests, line 1973). The
  document does not say how order-independence is enforced beyond the per-test fixture
  object, and no such enforcement is claimed here.
- Row change: `corpus/SOURCES.md:131` appends S256 as `docs`/`A`/`mined`, opened
  2026-10-25, recheck 365d, anchor `§Sharing Resources … and §Shuffling the Tests @ commit
  cd8e73f067129f8489e35c7b51c7a68552b289d2, snapshot
  .ufo/evidence/round-45/coverage/sources/googletest-advanced.md sha256 05546ed6`,
  `used-by` `corpus/knowledge/r8-gtest-order-and-seed.md`.
- Cited by `corpus/knowledge/r8-gtest-order-and-seed.md` (`source:` S256 on line 1,
  `verified-at: 2026-10-25` on line 2, `recheck:` 365d on line 3 with a live count of 1
  run 2026-10-25), indexed at `corpus/README.md:562`.

### Admit — S257 (new row): GoogleTest Primer, `docs/primer.md`

- URL https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md;
  access date 2026-10-25; 482 lines. Snapshot
  `.ufo/evidence/round-45/coverage/sources/googletest-primer.md`, SHA-256
  `03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e`.
- Located quotes (`grep -nF`, each found once):
  - line 251, 12 tokens: “GoogleTest always deletes a test fixture before it creates the next one.”
  - line 253, 12 tokens: “changes one test makes to the fixture do not affect other tests.”
- Scope: the fixture lifecycle behind F3's determinism precondition — a fresh fixture
  object per test, deleted before the next is created, and no reuse across tests
  (§Test Fixtures: Using the Same Data Configuration for Multiple Tests, line 205). It
  states the mechanism; it does not claim that global-state hygiene is checked at teardown.
- Row change: `corpus/SOURCES.md:132` appends S257 as `docs`/`A`/`mined`, opened
  2026-10-25, recheck 365d, anchor `§Test Fixtures … @ commit
  cd8e73f067129f8489e35c7b51c7a68552b289d2, snapshot
  .ufo/evidence/round-45/coverage/sources/googletest-primer.md sha256 03d756ab`,
  `used-by` `corpus/knowledge/r8-gtest-primer-independence.md`.
- Cited by `corpus/knowledge/r8-gtest-primer-independence.md` (`source:` S257 line 1,
  `verified-at: 2026-10-25` line 2, `recheck:` 365d line 3, live count 1 with the live
  fetch byte-identical to the snapshot), indexed at `corpus/README.md:563`.

### Ids, collisions and the guard receipts

- Registry at the freeze: `reg-ids` **115** ids, max S160 (`registry_rows: 115`,
  `registry_max: "S160"`, `registry_sha256: d1a4004377cc1db5…`). Staged package:
  `staged-ids` **103** ids, S153–S255 (`staged_rows: 103`, `staged_max: "S255"`,
  `staged_sha256: 020fbeaa048fc672…`).
- `collisions` = **8** ids: S153 S154 S155 S156 S157 S158 S159 S160. `column0_collisions`
  is identical and `column0_miss` is empty, so no collision hides behind indentation.
- Four of the eight are the same document already held, and are deduped by URL rather than
  renumbered: `map_dedupe` {S153→S105, S154→S106, S159→S155, S160→S156}. The other four
  are different documents wearing held ids and move: S155→S258, S156→S259, S157→S260,
  S158→S261 (`adoption-map.json`, 10 entries, 10 distinct targets).
- This round's two documents are mapped **by document**: staged S202 → S256, staged S203 →
  S257 (`adoption-map.json`; package row text at `SOURCES.append.md:56-57`). No arithmetic
  map was used.
- Guard verdict `admitted`: `guard-map.json` `verdict: "admitted"`, `map_ok: true`,
  `map_floor: "S256"`, `safe_floor: "S256"`, `map_entries: 10`, `guard-map.exit` = 0.
  Both cheaper maps are refused with exit 1 and `inadmissible`: identity S202→S202 /
  S203→S203 ("map targets are still staged ids: S202,S203") and next-free S202→S161 /
  S203→S162 ("…S161,S162"); the map-free analysis is `refused` on the 8-row cascade
  S161–S168 (`refused-map-identity.*`, `refused-map-next.*`).
- The extractor that produces those 8 is load-bearing and the guard carries its own proof:
  `guard-proof-collisions` = `S002` against `guard-proof-column0-collisions` = empty
  (0 bytes) — the same row indented two spaces is caught by the 0–3-space pattern and is
  invisible to a column-0 pattern. Mutant proof: a column-0-only `ROW_RE` returns
  `collisions: []`, `registry_rows` 2→1, exit 0 — a silent false green, not an error.
- Stripped from the campaign rows when adapting: (a) the staged prose recheck cells
  ("365d — `curl -fsSL '…' | grep -c '…'` (expect a non-zero count …)") become the bare
  cadence 365d; (b) `**…**` emphasis becomes plain text; (c) the carrier notes in the
  source cell are dropped (S202's master-alias byte-identity note, S203's
  `gtest_for_dummies.md` 404/rename history), leaving title + pinned URL; (d) scope is
  trimmed to F3 only (S202's F10 mention and S203's F2 mention leave the scope cell) and
  `teaches` is condensed to one grounded sentence each.

### Refused / not adopted — `r8-gtest-generator-contract.md`

- Package entry `r8-gtest-generator-contract.md` (staged row S204, "Parameter generators",
  `docs/reference/testing.md` at the same commit; snapshot
  `.ufo/evidence/round-45/coverage/sources/googletest-testing.md`, SHA-256
  `44c56c6198c6736bf2dc27c47391e4d481be70b36839e3c0073f273894d52d2b`) is **refused**.
- Reason, two independent grounds. Content: the table at `googletest-testing.md:100-113`
  documents deterministic enumeration for value-parameterized `TEST_P` instantiation
  (Range, Values, ValuesIn, Bool, Combine, ConvertGenerator) — no randomness, no
  distribution, no shrinking — so it is not a property-based generator contract for F10;
  and the entry presents a paraphrased yield column as the upstream table and says "five
  generators" where upstream lists six. Standing: the contract's `id_map` declares only
  S202→S256 and S203→S257, so S204 has no admitted id, and a third row now would be a
  post-score population change; its only quote-shaped string is 4 tokens, below the
  counter's 6-token floor.
- Flip: admit only if upstream states randomized/property-semantic generation (sampling
  distributions, shrinking) for these generators — or re-scope the row to
  "value-parameterized deterministic enumeration as a test-repetition fixture practice"
  under a frontier other than F10, with its own guard-admitted row and a verbatim table.

### Quarantine slice

17 rows, unchanged, no new verdicts: 14 `payload-absent`
(S105 S109 S110 S118 S119 S124 S126 S129 S131 S132 S137 S140 S141 S143) and 3
could-not-be-fetched (S113 S123 S134). The re-derivation is byte-identical to the committed
slice (sha256 `cb8270615417d23454552f32edd0d3d57a0c4028b4a4180537d6c74fc7e796ad`, `cmp`
clean) and to the round-40 list. No slice id is S202/S203, and GoogleTest appears nowhere
in the register, so S256/S257 are un-quarantined by construction rather than by exemption.
Verdicts stay those recorded in the round-40 lesson.

### considerthese

`considerthese/2026-10-25.md` proposal 1, **"Measured-to-landing drift check,"** is mined,
not implemented, as criterion 85: it proposes listing the commits between a round's
measured commit and its landing tip that touch records (LOG, SCORECARD, lessons, SOURCES)
and re-running that round's frozen counter at the landing tip — exactly the round-43
failure, green at `3c4003f` and red at `718a1e9`. The round-45 contract's `landing_rule`
enacts one instance of it (both claim counters and the round-44 record-agreement counter
re-run at the final landing tip), but nothing yet lists the record-touching commits between
the two, so the criterion is not implemented. Note: criterion number 85 was pre-reserved by
`corpus/lessons/round-43.md:114` for `considerthese/2026-10-22.md` proposal 5 (survivor
reclassification / overturn rate), which has not landed; landing proposal 1 at 85 needs an
appended supersede note, otherwise proposal 1 takes 86. [L1 to resolve at landing.]

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| quote-label | `.ufo/evidence/round-44/mistakes/r44-quote-token-count.stdout`: the round-44 lesson labels the line-15 Stryker quote "20 words"; measured `whitespace_tokens=28`, `letter_digit_words=22`, and the C1 grade on that label is `('invalid', 'quote length 28')` | the round-45 C1 grading of round-44's own label; no round-44 criterion measured a label against the quote it describes | count whitespace tokens before writing a word count into a lesson. Every quote admitted this round is measured (15, 8, 8, 12, 12 tokens) and inside the 6–25 window. A label is a claim about a quote and is graded like one. |
| persistent-shell | L1's account: a `set -e` left set in the persistent shell aborted the guard-map receipt step silently — no output, exit 1; only `guard-map.*` and `refused-map-identity.json` existed until the step was re-run without it. Artifact corroboration: `.ufo/evidence/round-45/assimilation/guard-map.*` mtime 16:26:51, while `refused-map-*`, `reg-ids`, `staged-ids`, `collisions`, `guard-proof-*` all carry 16:27:03 — two batches, consistent with a re-run | the L1 (not witnessed by this seat; the timestamps are the corroboration) | re-ran the receipt batch without `set -e`, then verified by presence: 15 files under `assimilation/`, all in the freeze commit. A receipt step that prints nothing and exits 1 is a failure, not a quiet success — read the `.exit` file, never infer success from an empty stderr. |
| selftest-negative-space | `w1/MutC2Counter.md`: 6 killed / 8 survived of 14 mutations; `w1/MutC2Counter-2.md`: 8 killed / 8 survived of 16 probes, after correcting a driver that scored a crash as a survivor. Convergent survivors: snapshot path prefix (:36), snapshot present (:83), provenance-trio order (:100), recheck line (:103), README full-path index form (:129), count thresholds (:135), self_pin conjunct (:135) | two independent mutation instances | disclosed, not repaired — the counter is frozen and the deciding run is the L1's. The survivor list and the case that would kill each are recorded; the highest-value fix is boundary `want='C2_R45_PASS=false'` cases, because T2–T7 assert count substrings that the summary line prints whether or not the verdict flipped. |
| forgeable-evidence | `w1/CritC1Control.md`: all four attack classes accepted — title chrome (A1/A1b), an unrelated section of the right page (A2), different-URL bytes with `entry.url` unchanged (A3), a round-35 stale blob declared `opened: 2026-10-25` (A4); a 5-file shared-snapshot ledger scores `fresh=50 C1_R45_PASS=true` fully offline, cheaper than CTL_A's 74 files | wave-1 critic CritC1Control | disclosed, not repaired: the counter has no snapshot-provenance, age or topicality check beyond a 2-word lexical overlap. The decisive gate for C1 is therefore the wave-2 non-author re-fetch (own URL, sha256 against `raw_sha256` and the committed snapshot, the quote read in context inside the anchored section, and fetch-time evidence), not the counter's `verified` count. |

## Census and quarantine

Start: <START>
End: <END>
Quarantine slice: 17 rows, 14 `payload-absent` and 3 could-not-be-fetched, byte-identical
to the round-40 lesson list, no new verdicts — details in the Gate's quarantine block.
Evidence `.ufo/waves/round-45/w1/ScoutQuarantine.md`.
````

---

## 2. Every value in the draft, and the command that produced it

### 2.1 Quotes located afresh (`grep -nF`, run in `.ufo/evidence/round-45/coverage/sources/`)

```
$ grep -nF "Remember that the test order is undefined, so your code can't depend on a test" googletest-advanced.md
896:Remember that the test order is undefined, so your code can't depend on a test
$ grep -nF "This helps to reveal bad dependencies between tests." googletest-advanced.md
1977:This helps to reveal bad dependencies between tests.
$ grep -nF "Therefore you'll get a different order every time." googletest-advanced.md
1980:Therefore you'll get a different order every time. The console output includes
$ grep -nF "GoogleTest always deletes a test fixture before it creates the next one." googletest-primer.md
251:GoogleTest always deletes a test fixture before it creates the next one.
$ grep -nF "changes one test makes to the fixture do not affect other tests." googletest-primer.md
253:changes one test makes to the fixture do not affect other tests.
```

One hit each. Token counts measured, not copied from `ScribeGtestRows.md`:

```
advanced:896:  whitespace_tokens=15  words_alpha=15
advanced:1977: whitespace_tokens=8   words_alpha=8
advanced:1980: whitespace_tokens=8   words_alpha=8
primer:251:    whitespace_tokens=12  words_alpha=12
primer:253:    whitespace_tokens=12  words_alpha=12
```

All five are inside the counter's 6–25 window and inside the lesson's ≤25-word bar. The
label-vs-quote discipline of the first `## Mistakes` row is applied here: the counts are
`split()` lengths, the same measure the round-44 receipt used.

Context check (quotes are body prose, in the anchored sections, not chrome):
`googletest-advanced.md:888-900` shows line 896 inside the "Sharing Resources" prose
(`SetUpTestSuite()`/`TearDownTestSuite()` discussion, heading at line 870);
`googletest-advanced.md:1974-1982` shows 1977 and 1980 inside the `--gtest_shuffle`
paragraph (heading at line 1973); `googletest-primer.md:248-254` shows 251 and 253 in the
fixture-lifecycle paragraph (heading at line 205).

### 2.2 Snapshots

```
$ sha256sum googletest-advanced.md googletest-primer.md googletest-testing.md
05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2  googletest-advanced.md
03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e  googletest-primer.md
44c56c6198c6736bf2dc27c47391e4d481be70b36839e3c0073f273894d52d2b  googletest-testing.md
$ wc -l googletest-advanced.md googletest-primer.md googletest-testing.md
  2457 / 482 / 1550
```

### 2.3 Id sets, collisions, guard receipts (`.ufo/evidence/round-45/assimilation/`)

```
$ wc -l reg-ids staged-ids collisions guard-proof-collisions guard-proof-column0-collisions
 115 reg-ids
 103 staged-ids
   8 collisions
   1 guard-proof-collisions
   0 guard-proof-column0-collisions
$ cat collisions
S153 S154 S155 S156 S157 S158 S159 S160   (one per line)
$ cat guard-proof-collisions   → S002
$ cat guard-proof-column0-collisions → (empty, 0 bytes)
$ cat guard-map.exit → 0 ; cat refused-map-identity.exit → 1 ; cat refused-map-next.exit → 1
```

`guard-map.json` (pretty-printed, key fields): `verdict: "admitted"`, `map_ok: true`,
`map_floor: "S256"`, `safe_floor: "S256"`, `map_entries: 10`, `map_targets: 10`,
`registry_rows: 115`, `registry_max: "S160"`, `registry_docs: 100`,
`registry_sha256: d1a4004377cc1db5344a366706d2818e06fecbceecb7687355bd3080b078d63d`,
`staged_rows: 103`, `staged_max: "S255"`,
`staged_sha256: 020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807`,
`collision_count: 8`, `column0_miss: []`, `cascade_count: 8` (S161–S168),
`held`/`map_dedupe` = {S153:S105, S154:S106, S159:S155, S160:S156},
`naive_map` S153→S161 … S160→S168, `next_free: "S161"`, `analysis_refused: true`.
`adoption-map.json` = {S153:S105, S154:S106, S159:S155, S160:S156, S155:S258, S156:S259,
S157:S260, S158:S261, S202:S256, S203:S257}. Refused maps: `map_ok: false`,
`map_staged_clash ["S202","S203"]` / `["S161","S162"]`, reasons "map targets are still
staged ids: …".

Indent-proof cross-check: `w1/MutGuardIndent.md` RUN7/RUN8 shows the 0–3-space extractor
reporting `column0_miss: ["S202"]` on an indented staged row while the column-0 mutant
reports `collisions: []`, `staged_rows: 0`, exit 0 — the same shape as the committed
`S002`/empty proof pair, so the draft's claim that the extractor is load-bearing is
supported, not asserted.

### 2.4 Landed rows, entries, index (working tree, read-only)

```
$ grep -cE '^ {0,3}\| S25[67] ' corpus/SOURCES.md        → 2
$ grep -cE '^ {0,3}\| S[0-9]{3,} ' corpus/SOURCES.md     → 117
$ grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md           → 1   (contract no-harm monitor holds)
$ sed -n '131,132p' corpus/SOURCES.md | grep -o '| corpus/knowledge/[^|]*|'
| corpus/knowledge/r8-gtest-order-and-seed.md |
| corpus/knowledge/r8-gtest-primer-independence.md |
$ grep -n "r8-gtest-order-and-seed\|r8-gtest-primer-independence" corpus/README.md
562:| `knowledge/r8-gtest-order-and-seed.md` | … | S256 |
563:| `knowledge/r8-gtest-primer-independence.md` | … | S257 |
```

`corpus/SOURCES.md:131` anchor cell carries
`snapshot .ufo/evidence/round-45/coverage/sources/googletest-advanced.md sha256 05546ed6`
and `:132` the primer equivalent with `03d756ab` — the 8-hex prefixes the C2 counter's
`gt_rows` requires. `corpus/knowledge/r8-gtest-primer-independence.md:1-3` carries
`source: S257 — …primer.md — snapshot …`, `verified-at: 2026-10-25`, `recheck: 365d …`;
`r8-gtest-order-and-seed.md:1-3` the S256 equivalent.

### 2.5 Criterion numbering (for the considerthese block)

```
$ grep -n "Criterion 8[0-4]" corpus/QUALITY.md
967:### Criterion 80 …   1001:### Criterion 81 …   1023:### Criterion 82 …
1049:### Criterion 83 …   1083:### Criterion 84 …
1107:### Criterion 83/84 — falsifier correction (round 43, appended)
$ grep -rn "criterion 85" corpus/ 
corpus/lessons/round-43.md:114:overturn rate. A future round lands it as criterion 85.
```

QUALITY.md ends at criterion 84; no round-45 seat appends 85 (grep over
`.ufo/waves/round-45/` returns only dispatch/spec boilerplate quoting this item).

---

## 3. Findings for the L1 (decisions, not edits)

1. **Criterion 85 is double-booked.** `corpus/lessons/round-43.md:114` pre-reserved
   criterion 85 for `considerthese/2026-10-22.md` proposal 5 (survivor
   reclassification/overturn rate, not landed). This item directs that
   `considerthese/2026-10-25.md` proposal 1 be mined as criterion 85. The draft states both
   facts and leaves the resolution to the L1 — either append a supersede note naming
   proposal 5's reservation, or give proposal 1 the number 86. Landing 85 without either
   leaves two proposals claiming one criterion number, which is exactly the class of
   record-disagreement the lane's m-classes exist to catch.
2. **The draft's Gate is already satisfied by the tree, but the deciding run is still the
   L1's.** Both rows, both entries and both README index lines are present in the working
   tree; I did not run `.ufo/evidence/round-45/coverage/measure.py` (bounds), so
   `rows=2 entries=2 indexed=2` is an inference from the files, not a measurement. If the
   L1's deciding run disagrees with the draft's Gate, the run wins and the Gate paragraph
   must be corrected rather than the counter.
3. **`RevGtestProvince`'s MEDIUM-1 condition is met by the landed entries, by inspection.**
   That report warned that all of entry 1's staged double-quoted spans crossed a line break,
   which `measure.py:38`'s `QUOTE_RE` (`"([^"\n]{10,400})"`) cannot match. The landed
   `r8-gtest-order-and-seed.md` quotes several single-line spans, including the
   `:896` sentence (15 tokens) and the seed sentence `"the random seed value, such that you
   can reproduce an order-related test failure"` (13 tokens), so the entry now has
   counter-reachable located quotes. Verified by reading the entry; not by running the
   counter.
4. **The `## Census and quarantine` placeholders are the only unfilled values.** I did not
   run `scripts/sources-census.sh` (it writes nothing but is the L1's start/end receipt
   pair, and the item reserves both for the L1). For orientation only, the working tree
   now holds **117** census-pattern rows (115 at the freeze + S256 + S257).
5. **`assimilation/` receipts are internally consistent with the draft.** `guard-map.json`
   reproduces `adoption-map.json`'s ten entries with `map_ok: true` and both refused maps
   exit 1; `reg-ids`/`staged-ids`/`collisions` are 115/103/8 and the indent proof pair is
   `S002` vs empty. Nothing in the draft's id paragraph is taken from a wave report without
   an artifact behind it.
6. **The `set -e` mistake is L1-reported, and the draft says so.** No wave report records
   it; the only artifact-level corroboration is the two-batch mtime split in
   `.ufo/evidence/round-45/assimilation/` (16:26:51 for `guard-map.*`, 16:27:03 for the
   rest). The draft's row attributes the observation to the L1 and the timestamps to the
   evidence, rather than upgrading it to an independently witnessed event.

## 4. Out of scope / not done

- `corpus/lessons/round-45.md` was **not** written (the item says "do not write it").
- No counter was executed, in any mode.
- No census run, no `git`/`jj` write command, no package access, no commit, no
  `agent://all` message.
- The C1 (freshness) content is deliberately absent from the Gate: the lesson's Gate covers
  the assimilation theme, as the round-44 lesson did with `Assimilation: none`.

## 5. Tooling

No tool installed or upgraded. `/home/vgpnk/.omp/agent/RULES.md` read; pacman untouched
(host-wide pause respected); `grep`, `awk`, `sha256sum`, `wc`, `python3` were already
present and sufficient.

Scratch: `/tmp/tameshi-r45-ScribeLesson/` (created, unused — all measurements ran in place
against read-only paths).
