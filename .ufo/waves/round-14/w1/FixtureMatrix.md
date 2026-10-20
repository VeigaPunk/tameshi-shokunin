# FixtureMatrix — round-14 w1 (contract + code-read only; no fixture run)

Scope: literal independent self-invocation fixture expectations for (a) same-command red/green, (b) setup crash vs assertion failure, (c) tampered snapshots. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

Status of the subject:
- `tools/evidence-disposition.py`: **absent** at review time (`tools/` lists pin-disposition.py, witness-metadata.py, bash-witness-study.py, repeat-control.py, mutate-and-run.sh). Gate expectations below are **contract-only**; finding IDs are PROPOSED and must be adopted or remapped by L1.
- Read as code: `tools/witness-metadata.py`, `tools/pin-disposition.py`, `.ufo/evidence/round-13/producer-before.py` (cmd_selftest), `.ufo/evidence/round-13/producer-oracle.py`.
- Read as recorded receipts: `round-13/expected.json`, `verification.json`, `producer-oracle-repair.json`, `verification-verdict.json`, `witness-metadata.json`.
- Nothing executed. Hashes of inputs were NOT recomputed here (would be a verification run); expected digests are taken from `expected.json` as recorded.
- Tooling: no installs or updates by this seat.

## 0. Axes

- A1 Literal fidelity: each expectation is checked against the frozen literal (exit, contains, id, reason, rows, statuses, result_reuse) on parsed stdout where structured.
- A2 Discrimination: a red must fail for the target reason; exit code alone must never carry a verdict.
- A3 Integrity-first: any tampered or unpinned snapshot yields exit 2 with zero semantic findings.
- A4 Immutability: historical round-12/round-13 bytes are read-only; no rewrite of `expected.json`, receipts, or `producer-before.py`.
- Scalar scores: unchanged (depth6 / calibration6). Nothing here is promotion evidence.

## 1. Frozen facts that constrain the matrix (observed in files)

F1. `round-13/expected.json` has **12** `expected_checks` keys: pin_selftest, metadata_selftest, metadata_old_null, metadata_corrected, producer_before, producer_before_oracle, producer_after_oracle, producer_after, witness_check, witness_count, pin_live, source_census. Its `inputs` map has **13** pinned paths. The spec phrase "All13 expected rows" is wrong for rows: the row count is **12** (11 effective + 1 superseded in the after file). Thirteen is the input count, and also the verification.json check count (13 names). DispositionSpec, Gate, and L1 must assert 12.

F2. `producer_before` raw receipt (verification.json, check `producer_before`): argv `python3 .ufo/evidence/round-13/producer-before.py selftest`, exit 1, `exit_matches: true`. Stdout ends at `check mutant digest mismatch refuses ok` and contains NO `summary preserves top-level exposed declaration kind` line, NO `WITNESS_SELFTEST:` line, NO `VERDICT:` line. Stderr is a Traceback: `FileNotFoundError ... .ufo/evidence/tools/mutate-and-run.sh` raised at `cmd_selftest` line 1478 (`sha256_file(RUNNER)`).

F3. Root cause of F2: `producer-before.py` sets `REPO = Path(__file__).resolve().parent.parent` (line 93) and `RUNNER = REPO/"tools"/"mutate-and-run.sh"` (line 95). Placed under `.ufo/evidence/round-13/`, REPO resolves to `.ufo/evidence`. The exception escapes `cmd_selftest` (no try around fixture construction, lines 1460-1488), so the process exits 1.

F4. Exit-code collision in the producer: `EXIT_FAIL = 1` for `VERDICT: FAIL`; an uncaught exception also exits 1. A crash and an assertion failure are indistinguishable by exit code. The only discriminators are stdout lines and stderr.

F5. Same-command pair that is actually valid: `producer_before_oracle` and `producer_after_oracle` have identical argv except one token. Before: `python3 .ufo/evidence/round-13/producer-oracle.py --source .ufo/evidence/round-13/producer-before.py --runner tools/mutate-and-run.sh`. After: same with `--source tools/bash-witness-study.py`. `producer-oracle.py` copies the source into a temp `tools/` layout, which removes the path confound from F3.

F6. Oracle stdout, recorded: before (exit 1, stderr empty) contains `  check summary preserves top-level exposed declaration kind FAIL`, `WITNESS_SELFTEST: 40/41 pass`, `VERDICT: FAIL`. After (exit 0, stderr empty) contains `  check summary preserves top-level exposed declaration kind ok`, `WITNESS_SELFTEST: 41/41 pass`, `VERDICT: PASS`.

F7. Substring traps in the frozen literals:
- `witness_count` contains `witness_classified=10`. The recorded row is `witness_classified=10` exactly, but `=100` also matches the substring.
- `producer_before` contains `summary preserves top-level exposed declaration kind` (no status token). This matches the `... kind ok` and `... kind FAIL` lines alike. Only the target name plus the status token is discriminating.
- `source_census` is exit-only (`{"exit": 0}`).

F8. `tools/witness-metadata.py`:
- `run_check` hashes all pinned inputs before any exit-1 comparison (lines 388-404). Integrity is first.
- `_fail` maps `*_digest_mismatch` with exit 2 to `snapshot_tampered`. Listed `companion_*` reasons with exit 2 also map to `snapshot_tampered`. Other exit-2 reasons map to `input_unavailable`.
- `main` catches `Exception` and returns exit 2 with reason `unexpected_exception`. Crashes in `--check` therefore do not exit 1.
- Selftest: 39 cases in `SELFTEST_CASES` (verified by enumeration). Each case passes only if returncode, JSON `exit`, `id`, `reason` all match and `Traceback` is absent from stderr. Good pattern.
- Selftest weakness: `_prepare_fixture` runs inside `try: ... finally: rmtree` with no except (lines 1124-1186). A fixture-construction crash propagates and exits 1 with no `SELFTEST:` summary. The `39/39` denominator is `len(SELFTEST_CASES)`, self-declared, not a count of observed OK lines.
- Selftest also copies live lane bytes and returns 2 `SETUP_FAIL` on digest drift (lines 1099-1120). It is coupled to live bytes.

F9. `tools/pin-disposition.py` selftest catches `(OSError, RuntimeError, SubprocessError)` and prints `SELFTEST: COULD_NOT_EVALUATE` with exit 2 (lines 1174-1176). This is the model for a distinct setup-crash channel. Other exceptions still exit 1.

## 2. Same-command red/green matrix (gate self-invocation and disposition-level)

Rule: the argv is a single literal list, `[sys.executable, "-I", TOOL, "--root", ROOT, "--dispositions", FILE, "--json"]`, and it is identical across the red and green runs. Only fixture bytes change. The selftest records argv and cwd in each case and asserts they are equal across the pair.

| ID | Fixture delta (argv unchanged) | Expected exit | Expected findings (PROPOSED IDs) | Forbidden |
|---|---|---|---|---|
| FM-G1 green | round-13 snapshot + dispositions.json (producer_before superseded, 2 replacements pass) | 0 | none; 12 per-expectation rows: 11 effective pass, 1 superseded with raw observation retained | any finding |
| FM-R1 red (real before) | round-13 snapshot + dispositions-before.json (all 12 effective) | 1 | exactly `contains_unmet@producer_before` and `setup_crash_observed@producer_before`; zero findings on other 11 rows | exit 0; exit-only pass for producer_before |
| FM-R2 red (fixture delta) | dispositions.json, but fixture expected copy changes producer_before_oracle contains to `... kind ok`, digest re-pinned | 1 | exactly `contains_unmet@producer_before_oracle` | exit 2 (digest must be re-pinned so the semantic red is not masked) |
| FM-R3 red (exit only) | dispositions.json, fixture expected copy sets witness_check exit 1, digest re-pinned | 1 | exactly `exit_mismatch@witness_check` | exit 2 |
| FM-R4 pair identity | FM-G1 vs FM-R1 | n/a | argv lists byte-equal; cwd equal; only fixture bytes differ | any argv difference |

Mandatory follow-up for L1 after the Gate lands: run the live gate once on `dispositions-before.json` (expect exit 1, only producer_before findings) and once on `dispositions.json` (expect exit 0). Same argv, different file.

## 3. Setup crash vs assertion failure matrix

Discriminator table. Exit 1 alone never classifies a row.

| Observation | Setup crash (producer_before raw) | Assertion failure (oracle before) | Pass (oracle after) |
|---|---|---|---|
| exit | 1 | 1 | 0 |
| stdout `WITNESS_SELFTEST: N/41 pass` | absent | `40/41 pass` | `41/41 pass` |
| stdout `VERDICT:` line | absent | `VERDICT: FAIL` | `VERDICT: PASS` |
| target check line `summary preserves ... kind <status>` | absent | `FAIL` | `ok` |
| stderr | `Traceback` + `FileNotFoundError` | empty | empty |

| ID | Fixture | Expected exit | Expected findings (PROPOSED) | Notes |
|---|---|---|---|---|
| FM-C1 crash as effective | producer_before effective, raw receipt | 1 | `contains_unmet@producer_before`, `setup_crash_observed@producer_before` | Crash must never count as mechanism proof |
| FM-C2 assertion red as effective | producer_before_oracle effective, oracle receipt | 0 for that row | none | Expected red: exit 1 + contains FAIL line + VERDICT FAIL + empty stderr |
| FM-C3 crash that prints the target string | producer_before_oracle receipt where the FAIL line is present but stderr contains `Traceback` | 1 | `setup_crash_observed@producer_before_oracle` | Contains alone is insufficient when a Traceback is recorded |
| FM-C4 exit-only trap | producer_before receipt with empty stdout, exit 1 | 1 | `contains_unmet@producer_before` | exit_matches alone must not pass |
| FM-C5 ok-line trap | producer_before_oracle stdout has `... kind ok` and `40/41 pass` | 1 | `contains_unmet@producer_before_oracle` | Substring `kind` must not satisfy `kind FAIL` |
| FM-C6 bool exit | receipt `exit: true` for expected 1 | 2 | `schema_invalid@<row>` | Python `True == 1`; use `type(x) is int` |
| FM-C7 unexpected exception path | expected.json nested ~2000 deep (RecursionError in parser) | 2 | `unexpected_exception` | Stderr must contain no `Traceback` |
| FM-C8 usage | `--dispositions` omitted | 64 | `usage` | argparse must not exit 2 |
| FM-C9 selftest crash channel (metadata/pin selftests) | none in current code | n/a | n/a | Recommendation only, see §6 R3 |

## 4. Tampered snapshot matrix (integrity first)

Every case here must emit zero semantic finding IDs (`contains_unmet`, `exit_mismatch`, `id_unmet`, `reason_unmet`, `rows_unmet`, `statuses_unmet`, `result_reuse_unmet`, `replacement_unmet`, `unexplained_supersession`). Asserted explicitly.

Fixture rule: to test a semantic or structural finding, the fixture must re-pin all digests. Otherwise the test is a digest test and proves nothing about the predicate.

| ID | Fixture | Expected exit | Expected findings (PROPOSED) |
|---|---|---|---|
| FM-T1 | +1 byte to a copy of expected.json | 2 | `expected_digest_mismatch` |
| FM-T2 | +1 byte to a copy of verification.json | 2 | `input_digest_mismatch@verification.json` |
| FM-T3 | +1 byte to producer-oracle-repair.json | 2 | `input_digest_mismatch@producer-oracle-repair.json` |
| FM-T4 | +1 byte to producer-before.py (an expected.inputs entry) | 2 | `input_digest_mismatch@.ufo/evidence/round-13/producer-before.py` |
| FM-T5 | FM-T2 plus FM-R1 semantic red, both present | 2 | `input_digest_mismatch@verification.json`; zero semantic IDs |
| FM-T6 | dispositions inputs map omits verification.json | 2 | `input_unpinned@verification.json` |
| FM-T7 | dispositions inputs pins verification.json to a wrong digest | 2 | `input_digest_mismatch@verification.json` |
| FM-T8 | expected_file `../expected.json` and absolute path | 2 each | `path_rejected` |
| FM-T9 | verification.json replaced by a symlink with identical bytes | 2 | `path_rejected` (symlink component, even though digest matches) |
| FM-T10 | verification.json missing | 2 | `input_missing@verification.json` |
| FM-T11 | producer_before_oracle name duplicated in oracle receipt (digest re-pinned) | 2 | `receipt_check_ambiguous@producer_before_oracle` |
| FM-T12 | receipt has no check named producer_after (digest re-pinned) | 2 | `receipt_check_missing@producer_after` |
| FM-T13 | superseded_by names `producer_after_oracl` (typo) | 2 | `supersession_unknown_ref@producer_before` |
| FM-T14 | cycle: producer_before superseded_by producer_before_oracle; producer_before_oracle superseded_by producer_before | 2 | `supersession_cycle` |
| FM-T15 | dispositions file is not valid JSON / contains NaN / duplicate key | 2 | `json_invalid` |
| FM-T16 | dispositions rows is a dict instead of a list | 2 | `schema_invalid` |

Residual that the Gate cannot close: the dispositions file is not self-authenticated. A forged dispositions file with a consistent set of digests passes integrity. This is configured authority, not adversarial authentication (same residual as the round-13 BaselineCritic note). State it in the report; do not claim otherwise.

## 5. Supersession and drop matrix (producer_before in the after file)

| ID | Fixture | Expected exit | Expected findings (PROPOSED) |
|---|---|---|---|
| FM-S1 green | producer_before superseded; reason non-empty; both replacements effective and pass | 0 | none; raw producer_before observation (exit 1, Traceback) reported as observed, not re-evaluated |
| FM-S2 one replacement | superseded_by lists only producer_before_oracle | 1 (DECISION, see §6 D2) | `supersession_replacement_unmet@producer_before` |
| FM-S3 replacement red | producer_after_oracle receipt exit changed to 1 (digest re-pinned) | 1 | `supersession_replacement_unmet@producer_before` |
| FM-S4 empty reason | reason "" | 2 | `schema_invalid@producer_before` |
| FM-S5 dropped row | producer_before row deleted (11 rows) | 2 | `row_missing@producer_before` |
| FM-S6 unexplained supersession | pin_live state superseded, no reason/replacements | 1 | `unexplained_supersession@pin_live` |
| FM-S7 raw observation erased | verification.json producer_before check removed (digest re-pinned) | 2 | `receipt_check_missing@producer_before` |
| FM-S8 duplicate row | producer_before listed twice | 2 | `row_duplicate@producer_before` |
| FM-S9 unknown row | extra row name `producer_before_v2` | 2 | `row_unknown@producer_before_v2` |

## 6. Frozen literal expectations (what L1 checks on the live run)

Per-row predicate, parsed as specified. Structured parse rules are required where noted.

| Row | Receipt : check | Exit | Predicate (literal) | Parse rule |
|---|---|---|---|---|
| pin_selftest | verification.json : pin_selftest | 0 | contains `SELFTEST: PASS (18/18)` | substring, full line |
| metadata_selftest | verification.json : metadata_selftest | 0 | contains `SELFTEST: PASS 39/39` | substring |
| metadata_old_null | verification.json : metadata_old_null | 1 | id `metadata_inconsistent`; reason `normalized_kind_null` | parse stdout JSON |
| metadata_corrected | verification.json : metadata_corrected | 0 | id `metadata_consistent` | parse stdout JSON |
| producer_before | verification.json : producer_before | 1 | contains `summary preserves top-level exposed declaration kind` | **FAILS on raw; superseded in after** |
| producer_before_oracle | producer-oracle-repair.json : producer_before_oracle | 1 | contains `summary preserves top-level exposed declaration kind FAIL` | line regex `^\s*check (.+?)\s+(ok\|FAIL)\s*$`, name exact, status FAIL |
| producer_after_oracle | producer-oracle-repair.json : producer_after_oracle | 0 | contains `WITNESS_SELFTEST: 41/41 pass` | substring |
| producer_after | verification.json : producer_after | 0 | contains `WITNESS_SELFTEST: 41/41 pass` | substring |
| witness_check | verification.json : witness_check | 0 | contains `WITNESS_CHECK: CLEAN` | substring |
| witness_count | verification.json : witness_count | 0 | contains `witness_classified=10` | **token boundary**: `witness_classified=10(?!\d)`, else `=100` passes |
| pin_live | verification.json : pin_live | 0 | rows 6; statuses unchanged 3 / changed 3 / unavailable 0; result_reuse `not_established` | parse stdout JSON: rows = len(legs); statuses from top-level `counts`; result_reuse top-level |
| source_census | verification.json : source_census | 0 | (exit only) | no stronger claim may be made for this row |

Mapping trap: `expected.json` key `rows` maps to JSON `legs`, and `statuses` maps to `counts`. The gate must encode this mapping literally, not infer it.

## 7. Risks and decisions

R1 (count error): "All13 expected rows" in the round-14 spec is 12. Expected after-state: 11 effective + 1 superseded. Before-state: 12 effective. L1 must assert 12.

R2 (exit-only acceptance): `producer_before` recorded `exit_matches: true` while its contains predicate failed. Any gate or report that treats exit match as pass reproduces the round-13 mistake. Required: a row with no contains/structured predicate is reported `exit_only`, never as mechanism proof.

R3 (crash channel): neither witness-metadata.py nor producer-before.py separates setup crash from assertion failure at the process level. Both can exit 1 from an unhandled exception. Recommendation for the owning lane (not this round, no edits here): add a `SELFTEST: COULD_NOT_EVALUATE` channel with exit 2, copying pin-disposition.py's pattern, and require the summary line in every selftest literal. For the new gate: `main` must map any uncaught exception to exit 2 `unexpected_exception` (witness-metadata's pattern, not the producer's).

R4 (self-declared denominator): `SELFTEST: PASS 39/39` derives from `len(SELFTEST_CASES)`. It does not prove that 39 cases ran. Stronger (recommended, not frozen): count unique `SELFTEST_CASE <name> ... OK` lines and require 39.

R5 (substring trap): `witness_classified=10` matches `=100`. Gate contains-matching must use token boundaries for `key=value` literals.

R6 (kind-line trap): substring `summary preserves top-level exposed declaration kind` matches the ok and FAIL lines alike. Structured check-line parse must be used for every `check ... ok|FAIL` literal.

R7 (location trap): any gate path must derive from `--root`, never `Path(__file__).parent`. The round-13 producer used `__file__`, and that caused F2/F3. The gate selftest must build its own layout under tempfile.

R8 (selftest live coupling): witness-metadata's selftest copies live lane bytes and fails with SETUP_FAIL when they drift. The new gate selftest must use synthetic fixtures only (as the contract requires: "isolated fixtures only"), so its result does not depend on the live round-13 bytes.

R9 (fixture digest masking): semantic/structural fixtures that do not re-pin digests will return exit 2 and prove nothing about the predicate. Every §2, §3 (C2-C5), and §5 fixture must re-pin.

R10 (decision points, proposed):
- D1 missing dispositions row, duplicate row, unknown row, missing receipt check, duplicate receipt check, unknown reference, cycle, unpinned input: exit 2 (structurally bad input). Predicate failures are exit 1.
- D2 superseded row with fewer than two replacements: exit 1 `supersession_replacement_unmet`. This is a judgment call; if the owner prefers exit 2 (malformed), change FM-S2 and state the change in the report.
- D3 effective-row receipt with recorded Traceback in stderr: exit 1 `setup_crash_observed`, even when the contains predicate passes (FM-C3). Owner must confirm.

R11 (residual): the Gate proves consistency with pinned digests. It does not authenticate the dispositions file or the historical producer. State this residual in any closure text; do not claim adversarial authentication.

## 8. Checks L1 should run (not run by this seat)

1. `python3 tools/witness-metadata.py --selftest` → exit 0, `SELFTEST: PASS 39/39`; count unique OK case lines = 39 (R4).
2. `python3 tools/pin-disposition.py --selftest` → exit 0, `SELFTEST: PASS (18/18)`.
3. `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata-old-null.json --json` → exit 1, `metadata_inconsistent` / `normalized_kind_null`.
4. `python3 tools/witness-metadata.py --check --json` → exit 0, `metadata_consistent`.
5. Same-command pair, oracle: `python3 .ufo/evidence/round-13/producer-oracle.py --source .ufo/evidence/round-13/producer-before.py --runner tools/mutate-and-run.sh` → exit 1 with `kind FAIL` line; then `--source tools/bash-witness-study.py` → exit 0 with `41/41 pass`. Compare argv: only the --source token differs.
6. Crash repro (optional, to confirm the mechanism): `python3 .ufo/evidence/round-13/producer-before.py selftest` → exit 1, stderr `FileNotFoundError` at `.ufo/evidence/tools/mutate-and-run.sh`, no `VERDICT:` line.
7. `python3 tools/bash-witness-study.py selftest` → exit 0, `WITNESS_SELFTEST: 41/41 pass`; `check` → `WITNESS_CHECK: CLEAN`; `count` → `witness_classified=10` as a token.
8. Sha256 of all 13 `expected.inputs` entries against recorded digests (L1 only; this seat did not run it).
9. Gate (once landed): `python3 tools/evidence-disposition.py --selftest` → exit 0; stable IDs for FM-G1, FM-R1..R4, FM-C1..C8, FM-T1..T16, FM-S1..S9 present and equal to the Gate's emitted IDs; any mismatch is a finding.
10. Gate live: `--root <lane> --dispositions .ufo/evidence/round-14/dispositions-before.json --json` → exit 1 (only producer_before findings); `--dispositions .ufo/evidence/round-14/dispositions.json --json` → exit 0. Same argv.
11. Tamper runs must use a `/tmp` copy of the lane evidence tree, never the historical files in place (FM-T1..T16).
12. Check that each expected row appears exactly once in the dispositions file (12 rows, R1).

## 9. Changes this seat recommends for the round-14 Gate/DispositionSpec contract (no file edits here)

- Replace "All13 expected rows" with 12 rows in the contract text (R1).
- Require `producer_before` in the after file to be `superseded` with the raw observation fields copied (receipt name, exit 1, stderr Traceback hash), not merely a reason string.
- Require token-boundary `key=value` matching and structured check-line parsing (R5, R6).
- Require uncaught-exception → exit 2 in the Gate `main`, and a `SELFTEST: COULD_NOT_EVALUATE` channel with exit 2 in the Gate selftest (R3).
- Require the Gate selftest to build synthetic fixtures under tempfile, invoke itself via `[sys.executable, "-I", TOOL, ...]`, and assert argv equality across red/green pairs (R7, R8).

Tools installed/updated by this seat: none.
