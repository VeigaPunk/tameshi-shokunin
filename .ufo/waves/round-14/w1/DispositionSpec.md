# Round 14 w1 — DispositionSpec: effective/superseded expectation ledger

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Baseline
`d6809df7775338f000e44c8a916067b8866867fb`. Wrote only the two assigned files;
no checker, runner, probe, harness, git-history or test command was executed.
Tool installs/updates: none.

## Files written

1. `.ufo/evidence/round-14/dispositions-before.json`
2. `.ufo/evidence/round-14/dispositions.json`

Both are JSON object ledgers with schema `evidence-dispositions-v1`:

- `expected_file`: `.ufo/evidence/round-13/expected.json` (frozen historical file).
- `inputs`: exactly the three files the ledger reads — the expected file and both
  receipts — pinned by SHA-256 of the committed bytes (verified equal to the blob
  at the baseline commit):
  - `.ufo/evidence/round-13/expected.json` `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336`
  - `.ufo/evidence/round-13/verification.json` `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f`
  - `.ufo/evidence/round-13/producer-oracle-repair.json` `df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d`
  The 13 digests inside `expected.inputs` are not duplicated in this map; the gate
  is required to re-verify all of them from the pinned expected file before any
  predicate.
- `rows`: exactly the 12 `expected_checks` keys of the frozen expected file, once
  each, in expected-file order. No receipt-only check is promoted to a row.

Row shape used:

- effective: exactly `name`, `state=effective`, `receipt`, `check` (no extra keys).
  `receipt` is the repo-relative `.ufo/evidence/round-13/verification.json` or
  `.ufo/evidence/round-13/producer-oracle-repair.json`, matching the pinned
  `inputs` key; `check` is the receipt's unique check name (equals `name` for all
  11 effective rows).
- superseded (`producer_before`, after file only): exactly `name`,
  `state=superseded`, `reason`, `raw_receipt` (`.ufo/evidence/round-13/verification.json`),
  `raw_check` (`producer_before`), `superseded_by` = `[producer_before_oracle,
  producer_after_oracle]`. The raw setup crash is retained and bound to the pinned
  receipt/check so the gate re-evaluates it against the original expectation and
  reports its contains mismatch. Gate's final parser contract requires these two
  raw keys (an intermediate message had omitted them; the final lane-relative
  normalized form is used in both files).

## Row census and selected receipts

| # | Row | State (after) | Receipt | Check | Frozen expectation (observed on frozen bytes) |
|---|---|---|---|---|---|
| 1 | pin_selftest | effective | verification.json | pin_selftest | exit0, contains `SELFTEST: PASS (18/18)` — holds |
| 2 | metadata_selftest | effective | verification.json | metadata_selftest | exit0, contains `SELFTEST: PASS 39/39` — holds |
| 3 | metadata_old_null | effective | verification.json | metadata_old_null | exit1, id `metadata_inconsistent`, reason `normalized_kind_null` — holds |
| 4 | metadata_corrected | effective | verification.json | metadata_corrected | exit0, id `metadata_consistent` — holds |
| 5 | producer_before | **superseded** | raw: verification.json | producer_before | exit1 holds; contains marker **absent** (by design, see below) |
| 6 | producer_before_oracle | effective | producer-oracle-repair.json | producer_before_oracle | exit1, contains `… kind FAIL`, `WITNESS_SELFTEST: 40/41 pass` — holds |
| 7 | producer_after_oracle | effective | producer-oracle-repair.json | producer_after_oracle | exit0, contains `WITNESS_SELFTEST: 41/41 pass` — holds |
| 8 | producer_after | effective | verification.json | producer_after | exit0, contains `WITNESS_SELFTEST: 41/41 pass` — holds |
| 9 | witness_check | effective | verification.json | witness_check | exit0, contains `WITNESS_CHECK: CLEAN` — holds |
| 10 | witness_count | effective | verification.json | witness_count | exit0, contains `witness_classified=10` — holds |
| 11 | pin_live | effective | verification.json | pin_live | exit0, rows6, statuses unchanged3/changed3/unavailable0, result_reuse `not_established` — holds against `legs[]`/`counts` |
| 12 | source_census | effective | verification.json | source_census | exit0 only — holds |

Before file: all 12 rows effective. After file: the same 12 rows with only row 5
changed — `state effective→superseded`, plus `reason`, `raw_receipt`, `raw_check`,
`superseded_by`, and removal of its effective `receipt`/`check` selector. All other
row objects, order, inputs and digests are byte-identical between the files.

`producer_before` raw observation: exit 1, `expected_exit` 1, but stdout lacks
`summary preserves top-level exposed declaration kind`; stderr ends in
`FileNotFoundError … .ufo/evidence/tools/mutate-and-run.sh` from
`sha256_file(RUNNER)` before the kind assertion. Exit equality alone would pass
here; the `contains` predicate is the discriminator. The after ledger therefore
reports the raw row as superseded-by-checked-mechanism, not as passing and not as
dropped. The reason text states that the oracle pair proves the assertion
red/green on the pinned historical/current sources and does **not** re-prove the
original raw argv.

## Count 13 — honest reconciliation

The frozen `expected.json` has **12** `expected_checks` keys, not 13. Two other
13s exist and must not be conflated with row count:

- `expected.json` `inputs` has **13** entries (the round-13 closure's "13 inputs").
- `verification.json` `checks` has **13** entries, of which 10 are selected by
  expected rows; `pin_env_scrub`, `metadata_emit` and
  `frozen_and_guardrail_unchanged` have no expected row and are deliberately not
  rows here. `verification.json measured_input_sha256` has 12 entries (the oracle
  file was added after that measurement).

The shared-context phrase "All13 expected rows" was a count typo; the after ledger
is 11 effective + 1 superseded = 12. Adding a 13th row would invent an unknown
expectation.

## Injected-environment gap — honest statement

The round-13 raw receipt does not prove the claimed `GIT_DIR`-poisoning setup:
`verification.json` `pin_env_scrub` has the same argv as `pin_live` and no
`injected_env` field (keys: argv, exit, expected_exit, exit_matches, name,
started_at, stderr, stdout). Its `started_at`/timestamp is the only environment
provenance. This ledger neither grades nor repairs that experiment — `pin_env_scrub`
is not an expected row. A new prospective context receipt (owned by the
ReceiptHarness seat) is the correct place to record an explicit
`injected_env={GIT_DIR:/nonexistent/tameshi-round14-poison}`; it cannot be
retrospective proof of omitted round-13 setup, and it is not counted here as
discharge of the frozen expectation or as a new gate case.

## Retained evidence and non-rewrites

- Frozen round-13 `expected.json`, `verification.json` and
  `producer-oracle-repair.json` are byte-identical to baseline blobs
  (sha256 above; worktree equals `git show d6809df:<path>`). No historical file,
  runner, SHONEN, SKILL, SOURCES, QUALITY or sibling repository was touched.
- Static (not gate-executed) checks performed while authoring: JSON parses; 12
  unique row names equal the 12 `expected_checks` keys; each effective
  `(receipt, check)` exists exactly once in its receipt; all 11 effective rows
  satisfy their frozen exit/contains/id/reason fields on the retained stdout; the
  raw `producer_before` contains-predicate fails while its exit matches; both
  replacements satisfy their own expectations; the two files differ only in the
  `producer_before` row.
- Gate's final parser contract, received during authoring, fixed the exact shapes
  used here: effective `{name,state,receipt,check}` with `check == name`;
  superseded `{name,state,reason,raw_receipt,raw_check,superseded_by}`; every
  `receipt`/`raw_receipt` a lane-relative path equal to an `inputs` key; inputs
  pinned for expected.json and both receipts. Both files were normalized to that
  final contract. Gate's predicted results: before file exit 1 with
  `expected_contains_missing` on `producer_before`; after file exit 0.
  `tools/evidence-disposition.py` itself was still absent when this report was
  written, so those predictions are not executed here.

## Checks L1 should run (not run by this seat)

1. `python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions-before.json --json`
   — expect exit 1 with the single `producer_before` contains mismatch (exit matches,
   marker absent); all other rows satisfied.
2. Same command with `--dispositions .ufo/evidence/round-14/dispositions.json` —
   expect exit 0: 11 effective + 1 superseded, both replacements effective and passing.
3. `python3 tools/evidence-disposition.py --selftest` — expect exit 0 with the gate's
   own tally.
4. Tamper/negative mutants: drop or duplicate a row, point a replacement at a failing
   row, mutate a receipt byte (expect exit 2), substitute a 13th row (expect a finding).
5. `git diff --quiet d6809df7775338f000e44c8a916067b8866867fb -- .ufo/evidence/round-13 tools/mutate-and-run.sh`
   — expect clean; confirm the two ledger files differ only in the `producer_before` row.
