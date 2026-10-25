seat: RevC2Entries

# Round 45 w2 — C2 entries claim-vs-source review (coverage)

Item: review `corpus/knowledge/r8-gtest-order-and-seed.md` and `corpus/knowledge/r8-gtest-primer-independence.md` plus rows S256/S257 (`corpus/SOURCES.md:131-132`) against the committed snapshots `.ufo/evidence/round-45/coverage/sources/googletest-{advanced,primer,testing}.md`. Every quoted sentence under "What was observed" was located in the snapshot at its cited line; every "What is inferred" bullet was checked for labelling and over-reach; every row check in the item was executed. Bounds held: read-only, scratch in `/tmp/tameshi-r45-RevC2Entries/`, no counter run of any kind (the deciding run is the L1's). No tool installs (curl/git/awk/python3 already present).

## Verdicts

- `r8-gtest-order-and-seed.md` (S256): **admit-with-errata** — E1, E2 below.
- `r8-gtest-primer-independence.md` (S257): **admit-with-errata** — E3, E4 below (E4 is a wording note, not a factual defect).
- Rows S256/S257: **admit** — all row checks pass (§4).

## 1. Snapshot identity (working tree, 2026-10-25)

`sha256sum` + `wc -l` on the three snapshots:

| snapshot | lines | sha256 (prefix) | prefix check | live check (my own run) |
|---|---|---|---|---|
| googletest-advanced.md | 2457 | `05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2` | row + entry `05546ed6` ✓ | curl pinned commit → 200, same sha; curl `master` alias → 200, same sha |
| googletest-primer.md | 482 | `03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e` | row + entry `03d756ab` ✓ | curl pinned commit → 200, same sha |
| googletest-testing.md | 1550 | `44c56c61…` | backs the REFUSED record | not re-fetched |

`git ls-remote --heads https://github.com/google/googletest` → 10 heads: `main`, `v1.8.x`, `v1.10.x`, `v1.12.x`–`v1.18.x`; `HEAD` = `cd8e73f06…` = `refs/heads/main` (pin valid; no `master` head). All three committed snapshots are accounted for: two admitted rows plus the snapshot of the REFUSED package entry (staged S204, `.ufo/waves/round-45/w1/ScribeGtestRows.md` §5) — `googletest-testing.md` is not an orphan.

## 2. Entry 1 `r8-gtest-order-and-seed.md` — observed vs snapshot (googletest-advanced.md)

Every quoted fragment is byte-exact at the cited line:

- :12 "Remember that the test order is undefined, so your code can't depend on a test" → `:896` ✓; "preceding or following another. Also, the tests must either not modify the state" → `:897` ✓; "state to its original value before passing control to the next test." → `:899` ✓ (the :897→:899 quote skips literal line :898, which the dual line cites disclose).
- :14 "This helps to reveal bad dependencies between tests." → `:1977` ✓; `--gtest_shuffle` flag introduced → `:1975` ✓; "By default, GoogleTest uses a random seed calculated from the current time." → `:1979` ✓; "the random seed value, such that you can reproduce an order-related test failure" → `:1981` ✓; "To specify the random seed explicitly, use the `--gtest_random_seed=SEED`" → `:1982` ✓ (fragment; line continues with the env-var form).
- :16 "GoogleTest creates a new test fixture object for each test in order to make" → `:872` ✓; "tests independent and easier to debug." → `:873` ✓; "one-copy-per-test model … prohibitively expensive" → `:874-875` ✓ (paraphrase, unquoted); static-member `SetUpTestSuite()`/`TearDownTestSuite()` sharing alternative → `:881-888` ✓ (the numbered list; the automatic calls are described at `:890-894`).
- Header: "2457 lines" ✓ (`wc -l`), sha ✓, commit ✓. Recheck phrase `grep -cF 'the random seed value, such that you can reproduce an order-related test failure'` → 1 ✓ (re-run by me).

No observed sentence is unsupported.

### Entry 1 — inference bullets

- :20 seed-as-run-identity — labelled ✓. Snapshot citations ✓ (`:896`, `:1979`, `:1981`, `:1982`). Lane-file claims verified: `corpus/knowledge/repeated-control-precondition.md:26` ("`controls_match` records … Determinism is a property of the program across runs, including runs not taken") ✓; `corpus/knowledge/hermetic-env-differential.md:56-57` ("Raw streams are SHA-256 hashed without replacing paths or times (`normalization: none`)") ✓. The "lane's instrument does neither today" clause is explicitly disclaimed as a lane limit, not a snapshot claim ✓. No over-reach.
- :21 shuffle-as-detection — labelled ✓. **E2 (errata, wording):** the quote "names the shared-resource problem" — the snapshot names "bad dependencies between tests" (`:1977`); shared-resource mutation is not named anywhere in the shuffle section. The same sentence argues the hazard-class mapping to `:897`/`:899`, so the substance is defensible, but "names" overstates; "is in the same hazard class as" is what the bytes support.
- :24 fixture complement — labelled ✓; `:872-873` + `:897-899` ✓; "framework-supported default, sharing an explicit opt-in" is supported by `:872` and `:878` ("in addition to per-test set-up/tear-down, GoogleTest also supports per-test-suite set-up/tear-down") ✓.
- :26 normative status — labelled ✓ and correctly finite; Limits bullet 2 (:29) explicitly disclaims any GoogleTest-enforcement claim (no statement of how order-independence is enforced, nothing on teardown mutation checks) ✓ — exactly the restraint this review checks for.

### Entry 1 — Limits

- **E1 (errata, factual wording):** :27 claims "`git ls-remote` lists only `refs/heads/main`". False as stated: `git ls-remote --heads` returns 10 heads (main plus v1.8.x, v1.10.x, v1.12.x–v1.18.x). The true and sufficient statement — used verbatim by the staged S202 package row — is that `refs/heads/master` no longer exists and raw serves `master` as an alias. The operative conclusion (pin to commit, not a branch name) is unaffected, and the same bullet's live-fetch/diff claims are confirmed by my own fetches (identical sha256s).
- :31 ("stated purpose, not a guarantee") and :33 (recheck grep run once, count 1) are accurate as written.

## 3. Entry 2 `r8-gtest-primer-independence.md` — observed vs snapshot (googletest-primer.md)

- :10 dead-name account: the staged S203 row (read-only package `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:57`) itself records the brief's named path `docs/gtest_for_dummies.md` as dead ✓; the 18/18 404 sweep and the live-fetch sha are committed in `.ufo/waves/round-45/w1/ScribeGtestPrimer.md` §2-3 (all 18 URLs pasted; live sha `03d756ab…` = snapshot) ✓. My own curl of the successor at the pinned commit → 200, sha `03d756ab…` ✓.
- :12 [snapshot:14-15] "Tests should be *independent* and *repeatable*. … as a result of other tests." → `:14-15` ✓; [snapshot:15-16] "GoogleTest isolates the tests by running each of them on a different object." → spans `:15-16` ✓.
- :14 [snapshot:251] "GoogleTest always deletes a test fixture before it creates the next one." ✓; [snapshot:252-253] "does **not** reuse … do not affect other tests." ✓; [snapshot:329-330] `QueueTest`/`t1` and `IsEmptyInitially` ✓. [snapshot:356-364] cycle ✓, with **E3 (errata, presentation):** the quoted arrow chain skips the intervening bullet `:360 "*   Deletes the fixture."` between `:358` and `:362`, so the chain reads as consecutive when it is not. Substance is covered by [snapshot:251] (deletion before the next fixture), so no factual error.
- :16 [snapshot:107-109] assertions-in-pairs + `ASSERT_*` fatal/abort ✓ (`:107-109`); [snapshot:109-110] `EXPECT_*` nonfatal ✓; [snapshot:110-111] `EXPECT_*` preferred ✓; [snapshot:83-84] general wording ✓.
- Header recheck `grep -c 'GoogleTest always deletes a test fixture before it creates the next one.'` → 1 ✓ (re-run by me).

### Entry 2 — inference bullets

- :20 fatal/nonfatal ↔ F2 — labelled ✓; snapshot facts exact (`:108-111`). **E4 (wording note):** "the verdict is scoped to the witness" — "witness" is the lane F2's vocabulary (`corpus/knowledge/witness-scoped-kill-verdict.md:12-13`, "red on its witness"); the snapshot says "abort the current function" and never says "witness". The bullet frames the mapping transparently as the lane's F2 lens and the gate-reporting remark is lane commentary, so the analogy is admissible as labelled inference; keep "the current function" primary.
- :22 dead-path-is-input-finding — labelled ✓; grounded in the committed 404 receipt; explicitly scoped to the input naming, not the source; no over-reach.
- Unknowns (:25): "does not describe how `SetUp()`/`TearDown()` failures are reported" — verified: primer mentions `TearDown` only at `:220`, `:222`, `:249`, `:291`, `:358`, `:425`, none about failure reporting ✓.
- Ground line :4: `corpus/README.md` F3 row exists (`:80`, "determinism precondition, flaky-aware verdicts") ✓; `corpus/QUALITY.md` criterion 62 exists (`:701`) but is the round-30 measured-revision/receipt rule — a loose pointer for "flaky-aware verdicts" (minor note; the primary F3 ground is exact). F2 file exists ✓.

## 4. Rows S256/S257 (`corpus/SOURCES.md:131-132`)

- 11 columns each: `awk -F'|' 'NR==131||NR==132{print NF-2}'` → 11, 11; all 117 registry rows are 11-wide (`awk … | sort | uniq -c` → `117 11`), so no embedded `|` and the schema matches pre-existing rows (e.g. S159/S160 at :129-130).
- Anchor carries snapshot path + sha prefix: S256 → `.ufo/evidence/round-45/coverage/sources/googletest-advanced.md sha256 05546ed6` (= `05546ed6db…` ✓); S257 → `…/googletest-primer.md sha256 03d756ab` (= `03d756ab11…` ✓).
- Anchor sections exist: advanced `## Sharing Resources Between Tests in the Same Test Suite` `:870`, `### Shuffling the Tests` `:1973`; primer `## Test Fixtures: Using the Same Data Configuration for Multiple Tests` `:205` ✓.
- used-by matches the citing entry, exclusively: S256 → `corpus/knowledge/r8-gtest-order-and-seed.md`, S257 → `…/r8-gtest-primer-independence.md`; `grep -rln 'S256\|S257' corpus/knowledge/` → exactly those two files; line 1 of each entry cites its row id back ✓. Both entries are indexed in `corpus/README.md:562-563` ✓.
- teaches grounded: S256 → order undefined `:896`, shuffle reveals bad dependencies `:1977`, seed printed so an order-related failure can be reproduced `:1980-1983` ✓; S257 → fresh fixture per test `:246-251`, deleted before the next `:251`, no reuse / changes do not affect other tests `:252-253` ✓. Titles match snapshot H1s (`# Advanced GoogleTest Topics` `:1`, `# GoogleTest Primer` `:1`) ✓. Status mined / 2026-10-25 / 365d consistent; each recheck phrase occurs exactly once in its snapshot ✓.
- Adoption: `.ufo/evidence/round-45/assimilation/adoption-map.json` maps staged S202→S256, S203→S257 (same document, same commit `cd8e73f`), matching the contract id_map; `guard-map.json` has `map_ok: true`, floor S256, and the identity/naive maps are refused (`refused-map-identity.json`, `refused-map-next.json`, cascade S161–S168) ✓. Package staged rows verified at `SOURCES.append.md:56-57` (S202 advanced.md, S203 primer.md with the dead `gtest_for_dummies.md` brief note); package accessed read-only.

## 5. Residual risk / verification gaps

- The 18/18 404 sweep is accepted on the committed w1 receipt (all 18 outputs pasted there); I re-verified only the successor URL live, not all 18.
- Entry 1's "diff exit 0" live-vs-snapshot claim is accepted via sha256 equality (my own fetches), not by re-running their diff.
- No counter was run (`measure.py --selftest` not exercised); entry-level quote locality was checked with raw line reads instead.
- `googletest-testing.md` bytes were not re-fetched; no admitted claim depends on it.
- Upstream drift after 2026-10-25 is inherently open; both entries state this and pin 365d rechecks.

All four errata are wording-level; every observed sentence in both entries is snapshot-backed at its cited line, so both entries are admissible with the errata above.
