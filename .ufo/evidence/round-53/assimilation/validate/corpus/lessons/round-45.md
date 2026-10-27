# Round 45 lesson

author: tameshi L1 TameshiR45 (hyaku run 7, attempt 1); Gate drafted by wave-2 seat ScribeLesson, verified and edited by the L1
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

`considerthese/2026-10-25.md` proposal 1, **"Measured-to-landing drift check"**
(lines 66-68), is mined and lands as QUALITY criterion 86 (number 85 stays
reserved for `considerthese/2026-10-22.md` proposal 5, `corpus/lessons/round-43.md:110-114`).
Grounding opened what the reflection points at instead of trusting it: the
round-43 counter is green at measured `3c4003f6e97e5c787e7538b2eb35d62f49783aaf`
and red (`m7=1`) at landing `718a1e987febd32eb78ebc65adfe939f23b3de63`, and the
one commit between them carries `SCORECARD.md` and `LOG.md` edits beside the
receipts (`.ufo/waves/round-45/w1/ExecLiveDriftR43.md`); round 44 did not drift
(green at both `ef990aaea3f6546db20feccbff89ac9ab78c5405` and
`df000ab79a4c526bcb5cbf03a356c1a44fb32e27`). Wave-1 critic CritDriftClaim
showed the contract's literal `landing_rule` ("re-run at the final landing tip
and cite landing-tip receipts") is a fixed point a receipt cannot satisfy; the
criterion therefore binds the content revision C and requires the receipts-only
follow-up. Falsifier receipt: `.ufo/evidence/round-45/quality/c86-falsifier.stdout`
(`CRITERION-86-FALSIFIER-OK drift_paths=2`). This round applies it: the records
are committed at C before the deciding runs, and the commit after C carries
receipts only (see `## Census and quarantine`).

Proposal 2 ("cumulative mismatch-class regression run") was exercised as data,
not implemented: `.ufo/waves/round-45/w1/ExecRegressionSweep.md` re-ran the
round-41..44 calibration counters at base; the older counters still flag the
`safe_floor=S256` assignment value as an unknown citation (m7), a known false
positive superseded by the round-44 mask, not a regression of a fixed record.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| number-drift | `corpus/lessons/round-44.md:26` labels the Stryker line-15 quote "20 words"; measured `whitespace_tokens=28 letter_digit_words=22`, and the round-45 C1 counter grades that quote `('invalid', 'quote length 28')` (`.ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout`); the 20 was inherited from `corpus/lessons/round-43.md:52`, whose shorter quote is this one's suffix (`.ufo/waves/round-45/w2/ScribeQuality.md` gate 4) | none (routed by `corpus/lessons/round-44-verifier-spotcheck.md:73`, which itself wrote an unmeasured "24") | QUALITY criterion 87: a quote's length is printed by a command using the accepting counter's tokenizer. Shown able to fail: its falsifier prints `CRITERION-87-FALSIFIER-OK` on the round-44 label and `VACUOUS` when the label is rewritten to 28 (`.ufo/evidence/round-45/quality/c87-falsifier.stdout`). Every quote this round is measured. |
| landing | `.ufo/evidence/round-45/contract.json` `no_harm` names the round-44 record-agreement counter as a no-harm monitor "at the deciding revision"; that counter appends `BLOCK_ROUND_MISMATCH` whenever the newest SCORECARD block is not round 44, so it cannot be green at any round-45 tip (`.ufo/waves/round-45/w1/CritDriftClaim.md` D3; observed at the content revision, receipt `.ufo/evidence/round-45/after/c-r44-at-content.stdout`) | none | not rewritten (the contract is frozen): the monitor is reported as round-bound and its other classes are read off the same line; criterion 86's last clause forbids citing a round-bound monitor green. A future contract names a monitor that is valid at its own round's tip. |
| landing | the L1's persistent shell kept `set -e` from an earlier command; the guard-map receipt batch then aborted with no output and exit 1 after writing only `guard-map.*` and `refused-map-identity.json` (mtimes 16:26:51 vs 16:27:03 for the re-run batch) | none | re-ran the batch without `set -e` and checked every `*.exit` file and both refused verdicts before committing; receipts are read back, never assumed written. |
| scope | `.ufo/waves/round-45/w1/RevGtestProvince.md` HIGH-1: the adopted entry draft said the lane's `env-diff.py` "strips, but does not publish" run-identity artefacts; `corpus/knowledge/hermetic-env-differential.md:56-57` says raw streams are hashed with `normalization: none` | the per-entry QUALITY claim-vs-source bar, applied by the wave-1 reviewer | corrected before wave 2 (commit `ad5942c6e9858af19d00000b58439b321ddfa62b`); wave-2 RevC2Entries/CritC2Admission errata (ls-remote heads, "shared-resource" wording, held rows S013/S025 unreconciled, F2 continuation clause) applied in `f6a34f3900789dd3f693e824c4f874385a4177c3`. Shown able to fail: the reviewers' findings are the failing state. |
| vacuous | `.ufo/waves/round-45/w1/CritC1Control.md`: the C1 counter's per-row gate accepts title chrome, an unrelated section, different-URL bytes and a stale blob; a 5-file forged ledger with a forged results file passes the whole counter offline. Wave-2 judges then disputed two author-accepted entries (S048 truncated antecedent, S093 markup-only fragment) that the counter had verified | the counter itself (it cannot see provenance or topicality); the wave-2 non-author re-fetch is the decisive gate | disclosed, not repaired (frozen counter). The two disputes are the failing state of the review gate: `DISPUTED S048`, `DISPUTED S093` in the deciding run. Round 46 routes a provenance check (fetch receipt per snapshot) and the selftest survivors from `w1/MutC1Counter*.md` and `w2/MutC1Reviews.md`. |
| vacuous | `.ufo/waves/round-45/w1/MutC2Counter.md` (6 killed / 8 survived) and `MutC2Counter-2.md` (8/8): snapshot prefix, snapshot present, provenance-trio order, recheck line, README full-path form, count thresholds and self_pin conjunct have no killing selftest case | none | disclosed; the survivor list and each killing case are routed to round 46 (`SCORECARD.md` round-45 Planned field). |
| provider | wave-2 seat ScribeScorecard: `.ufo/waves/round-45/w2-results.json` carries, under that seat name, an output from mori round 47 (`"seat": "ScribeScorecard", "round": 47`); no tameshi report exists at `.ufo/waves/round-45/w2/ScribeScorecard.md` | none | counted as a dead seat; the L1 wrote the SCORECARD and LOG entries. Seat names are not unique across lanes in the orchestrator's results mapping; the C1 review gate keys on reviewer names, so a future round prefixes seat names with the lane and round. |

## Census and quarantine

Start: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, 115 rows, W04 ×9 and W01 ×1, no E-codes (`.ufo/evidence/round-45/census-start.{stdout,stderr,exit}`).
End: same command at the content revision → see `.ufo/evidence/round-45/census-end.{stdout,stderr,exit}` (committed after the content revision, receipts only).
Quarantine slice: 17 rows, 14 `payload-absent` and 3 could-not-be-fetched, byte-identical
to the round-40 lesson list, no new verdicts (`.ufo/waves/round-45/w1/ScoutQuarantine.md`,
`.ufo/evidence/round-45/assimilation/quarantine-slice`).
