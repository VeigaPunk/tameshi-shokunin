# Round 14 w1 — EffectiveRows: historical expected_checks coverage audit

Lane: tameshi-shokunin. Seat: `TameshiR14.EffectiveRows` (leaf, read-only research).
Code status: `tools/evidence-disposition.py` is **absent** (contract-only for the gate); `.ufo/evidence/round-14/` holds only `claims.json`. Findings below are against the committed round-13 receipts and the round-14 gate contract in `spec.json`.
Checks run: none. Only JSON reads/parses and SHA-256 of committed bytes. No gate, selftest, runner or harness was executed. Tool installs/updates: none.

## 1. Cardinality: expected_checks has 12 rows, not 13 (HIGH)

`.ufo/evidence/round-13/expected.json` `expected_checks` keys (12):
`pin_selftest, metadata_selftest, metadata_old_null, metadata_corrected, producer_before, producer_before_oracle, producer_after_oracle, producer_after, witness_check, witness_count, pin_live, source_census`.

The "13" in the round-14 contract (`All13 expected rows effective except producer_before superseded`) matches neither:
- `expected.json` `inputs` has 13 entries (the "13 inputs" of the round-13 closure note);
- `verification.json` `checks` has 13 entries, but a different set (see §4).

Correct partition of the 12 expected rows: **11 effective + 1 superseded**.

| Row | Disposition | Receipt / check name | Original expectation |
|---|---|---|---|
| pin_selftest | effective | verification.json `pin_selftest` | exit 0, contains `SELFTEST: PASS (18/18)` — present |
| metadata_selftest | effective | verification.json `metadata_selftest` | exit 0, contains `SELFTEST: PASS 39/39` — present |
| metadata_old_null | effective | verification.json `metadata_old_null` | exit 1, id `metadata_inconsistent`, reason `normalized_kind_null` — both present as JSON fields |
| metadata_corrected | effective | verification.json `metadata_corrected` | exit 0, id `metadata_consistent` — present |
| producer_before | **superseded** | verification.json `producer_before` (raw, retained) | exit 1, contains `summary preserves top-level exposed declaration kind` — exit matches, **contains FAILS** |
| producer_before_oracle | effective | producer-oracle-repair.json `producer_before_oracle` | exit 1, contains `…kind FAIL` — present |
| producer_after_oracle | effective | producer-oracle-repair.json `producer_after_oracle` | exit 0, contains `WITNESS_SELFTEST: 41/41 pass` — present |
| producer_after | effective | verification.json `producer_after` | exit 0, contains `WITNESS_SELFTEST: 41/41 pass` — present |
| witness_check | effective | verification.json `witness_check` | exit 0, contains `WITNESS_CHECK: CLEAN` — present |
| witness_count | effective | verification.json `witness_count` | exit 0, contains `witness_classified=10` — present |
| pin_live | effective | verification.json `pin_live` | exit 0, rows 6, statuses, result_reuse — see §3 |
| source_census | effective | verification.json `source_census` | exit 0 only |

Silent-drop risk: `verification-verdict.json` `checks` lists 15 names and **omits `producer_before`**; the omission is explained only by the free-text field `excluded_initial_failure`. The gate must not derive rows from the verdict; `producer_before` must remain an explicit superseded row.

Required spec fix: change "All13" to "12 expected rows: 11 effective, producer_before superseded", or the DispositionSpec will either invent a row or fail its own count.

## 2. The stale row: producer_before is a real, not stale-able, failure (HIGH)

Raw `verification.json` `producer_before`:
- `exit` 1, `expected_exit` 1, `exit_matches` true — exit alone passes.
- `stdout` does **not** contain `summary preserves top-level exposed declaration kind` (checked: False). It contains only the earlier `check … ok` lines.
- `stderr` is a traceback: `producer-before.py` line 218 `sha256_file(RUNNER)` → `FileNotFoundError … .ufo/evidence/tools/mutate-and-run.sh` (path-layout error, before any target assertion).

Replacements (both in expected.json as their own rows, both pass their original expectations on their own receipts):
- `producer_before_oracle`: exit 1 (= expected), stdout contains `summary preserves top-level exposed declaration kind FAIL` (True), final line `WITNESS_SELFTEST: 40/41 pass`, `VERDICT: FAIL`. This is the red-before discriminator, against the **pre-fix** producer SHA `249d9dcd…` path/source `producer-before.py`.
- `producer_after_oracle`: exit 0, stdout contains `WITNESS_SELFTEST: 41/41 pass` (True), `VERDICT: PASS`. Source is `tools/bash-witness-study.py` (argv differs from the original `producer_after`, which runs `selftest` mode, so the replacement is not a re-run of the same argv).

Superseded-row requirements the gate must enforce (per contract):
1. `superseded_by` = exactly `[producer_before_oracle, producer_after_oracle]`, both effective and both passing their own original expectation.
2. The superseded row must **retain and bind** the raw observation: receipt path `verification.json`, check name `producer_before`, observed exit 1, stdout and stderr digests, and the presence of the `FileNotFoundError` in stderr. The gate must check the raw stdout does NOT contain the phrase; otherwise the supersession is hiding a different result.
3. `reason` should mirror the verdict's `excluded_initial_failure` text (`path-layout FileNotFoundError before target assertion`) as a literal string the gate compares, not a parsed prose field.
4. Exit-only success for producer_before is not mechanism proof; the gate must not treat `exit_matches` as sufficient for any row that declares `contains`.

Naive check of the stale row (the failure the contract wants visible): exit match true, `contains` predicate false. A before-state disposition with producer_before effective must exit 1 with that one row as the named mismatch.

## 3. pin_live predicates do not map literally onto the receipt (MEDIUM)

Expected: `{exit 0, rows 6, statuses {unchanged 3, changed 3, unavailable 0}, result_reuse not_established}`.

Receipt `pin_live.stdout` JSON has no `rows` or `statuses` key. It has top-level `counts` `{legs: 6, unchanged: 3, changed: 3, unavailable: 0}` and `legs[]` (6 entries) with `content_status` (`changed`×3, `unchanged`×3) and `result_reuse` (`not_established`×6); top-level `result_reuse` = `not_established`.

Gate must define explicitly:
- `rows` = `len(legs)` (6).
- `statuses` computed from `legs[].content_status`, with `unavailable` counted as **0 when absent** (no leg carries it). Requiring the key `unavailable` to exist in `counts` would be an artifact check, not a semantic one.
- `result_reuse` applied to each leg and the top-level field.

`pin_env_scrub` has identical argv to `pin_live` and is **not** an expected row; the gate must not merge or dedupe by argv.

## 4. Receipt checks with no expected row, and an unbacked verdict name (MEDIUM)

Receipt check names not in expected_checks:
- verification.json: `pin_env_scrub`, `metadata_emit`, `frozen_and_guardrail_unchanged` (3). All exit 0 with `exit_matches` true.
- verification-verdict.json only: `baseline_final_count` — no check row exists in `verification.json` or `producer-oracle-repair.json`; the string appears only in the verdict. It is an unbacked claim.

The contract says "no unexplained/drop/cycle/unknown/missing rows" but does not say what to do with **receipt** checks that have no expected row. Recommendation (decision for Gate/DispositionSpec): the gate must list these as `unmapped_receipt_check` findings, and the dispositions file must explicitly record them as `unmapped` with a reason, rather than silently ignoring them. Also: the gate must not accept `baseline_final_count` as a check at all; it should be reported as an unbacked verdict name.

## 5. Input pinning gap: the receipts are not pinned by expected.json (HIGH for the disposition contract)

`expected.json` `inputs` (13 entries) pins the round-12 bytes, the four tools, the round-13 manifest/companions/producer files and `producer-oracle.py`. It does **not** pin `verification.json`, `producer-oracle-repair.json` or `verification-verdict.json`.

The contract requires `dispositions.json` `inputs` to pin the expected file and every used receipt. Required inputs for the dispositions file:
- `.ufo/evidence/round-13/expected.json`
- `.ufo/evidence/round-13/verification.json` — observed sha256 `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f`
- `.ufo/evidence/round-13/producer-oracle-repair.json` — observed sha256 `df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d`
- `verification-verdict.json` only if the gate reads it (recommend it does **not**): observed sha256 `1d128a44e0417eb29ca75195bc7f97b8d0ceae246f520710faf67c397ef35a4c`

(Digests above are from my read of the committed working-tree files; L1 must recompute from the bytes before relying on them.)

All 13 `expected.inputs` digests currently match their worktree bytes (checked: 0 mismatches). The gate must verify every one of them before any predicate, per contract.

## 6. Minor observations (LOW)

- `metadata_old_null` / `metadata_corrected`: `id` and `reason` are JSON fields in stdout, not prose. The gate should parse stdout and compare the field for equality, not substring-match. Both values are present as fields today.
- `source_census` expects exit 0 only; this is honest but must be labeled exit-only in the output so it is not read as a content check. Its stdout contains two W04 warnings; those are not failures.
- `frozen_and_guardrail_unchanged` runs `git diff --quiet 546b371…`. This is a git-dependent historical check; the gate must not re-run git to replay it, and it has no expected row.
- `baseline` in expected.json is `546b371…`; the round-13 closure note records `before`=`546b371` and `delivered`=`7dd16d9`. Only the expected-file baseline matters to the gate; no mismatch found.

## 7. Historical bytes

`git status --short -- .ufo/evidence/round-13 corpus/lessons` returned no lines at audit time. Round-13 receipts are tracked and unchanged in the worktree. Round-14 is untracked (`?? .ufo/evidence/round-14/`, `?? .ufo/waves/round-14/`).

## Checks L1 should run (after all seats finish; not run here)

1. Recompute sha256 of all 13 `expected.json` inputs and of `verification.json`, `producer-oracle-repair.json`, `verification-verdict.json`; compare with §5.
2. Run `tools/evidence-disposition.py --root <lane> --dispositions .ufo/evidence/round-14/dispositions.json --json`; expect exit 0 and 12 per-expectation dispositions (11 effective, 1 superseded).
3. Negative cases (each must exit with the stated code, with a stable finding ID):
   - producer_before effective in a copy of dispositions → exit 1, mismatch on `contains`.
   - one expected row dropped → exit 1 (missing row finding).
   - one extra row or a duplicate name → exit 1.
   - a mutated `verification.json` byte or digest → exit 2 (could-not-evaluate, tampered input).
   - superseded_by pointing at a row that fails its own expectation → exit 1.
4. Confirm `git status --porcelain .ufo/evidence/round-13 corpus/lessons` is empty and round-12 runner/frozen paths are byte-unchanged vs `546b371`.
5. Confirm `baseline_final_count` appears in no receipt file (only in verdict), and that the gate reports it as unbacked rather than as passing.

## Acceptance against assignment

- Exact coverage: 12 expected keys enumerated; 11 effective and 1 superseded mapping is complete and unambiguous (§1).
- No silent stale-row drop: producer_before must stay as an explicit superseded row bound to its raw failure (§2); the verdict's omission is documented as a risk (§1).
- Code status: gate absent; findings are contract-only for `tools/evidence-disposition.py`.
- No checks executed; no tool installs or updates.
