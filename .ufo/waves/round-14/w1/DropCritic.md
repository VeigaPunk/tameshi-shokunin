# DropCritic — round 14 w1 (critic, leaf)

Target: arbitrary supersession that hides a genuine failure. I did not run any checker, selftest, receipt argv or target suite. Everything below comes from static reads of committed round-13 bytes plus Python `json`/`hashlib` parsing.

**Status of reviewed code:** `tools/evidence-disposition.py`, `.ufo/evidence/round-14/dispositions{,-before}.json` and `capture-context.py` were **absent** when I reviewed (`ls` → No such file). This review covers the retained contract (shared context, spec.json Gate/DispositionSpec items) and the actual historical data. It does not cover an implementation.

## Observed facts (static)

| Fact | Observation |
|---|---|
| `expected.json` `expected_checks` key count | **12**: pin_selftest, metadata_selftest, metadata_old_null, metadata_corrected, producer_before, producer_before_oracle, producer_after_oracle, producer_after, witness_check, witness_count, pin_live, source_census |
| `expected.inputs` count / current mismatches | 13 / `[]`; `git diff --quiet d6809df -- .ufo/evidence/round-13` exit 0 |
| `verification.json` check names (13) | the 10 expected names other than the two oracles, plus receipt-only `pin_env_scrub`, `metadata_emit`, `frozen_and_guardrail_unchanged` |
| `producer-oracle-repair.json` check names | `producer_before_oracle`, `producer_after_oracle`. Neither receipt has a name the other also has, and every expected name appears in exactly one receipt |
| raw `producer_before` | exit 1, receipt `exit_matches: true`, literal `summary preserves top-level exposed declaration kind` found in **neither** stdout nor stderr; stderr ends in `FileNotFoundError … .ufo/evidence/tools/mutate-and-run.sh` |
| `producer_before_oracle` | exit 1; the only FAIL lines are `check summary preserves top-level exposed declaration kind FAIL` and `VERDICT: FAIL`; `WITNESS_SELFTEST: 40/41 pass` |
| `producer_after_oracle` | exit 0; same assertion `ok`; 41/41. Before and after assertion-name sets are identical (symmetric difference ∅) |
| `pin_live` vs `pin_env_scrub` | identical argv **and** byte-identical stdout |
| `verification-verdict.json` | leaves `producer_before` out of `checks` and lists `baseline_final_count matched:true`, but **no raw receipt contains that check** (`git grep` finds the name only in the verdict file) |
| Timing / provenance | verification checks ran 04:59:24–27Z and the oracles at 05:00:00Z. `verification.json.measured_input_sha256` has 12 entries and lacks `producer-oracle.py`, while `expected.json` has 13. All four files landed in one commit, `4acc607` |
| SHA-256 now | expected.json `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336`; verification.json `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f`; producer-oracle-repair.json `df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d` |

## Counterexamples → smallest safe correction

**D1. The "13 rows" count in the contract is wrong (spec defect).** The shared context says "All13 expected rows", and DispositionSpec is told to "explain count13". `expected_checks` has **12** keys; 13 is the count of `expected.inputs` and of `verification.json` checks. A dispositions file with 13 rows would need an invented row, for example receipt-only `pin_env_scrub`, which has no original expectation.
*Correction:* rows must equal `set(expected_checks)` exactly (12). The gate rejects any row name outside `expected_checks` (`unknown_row`), even if the receipt has that name. The report and claims say "12 expected rows; 13 pinned inputs".

**D2. Identity swap hides a failure without any supersession.** Suppose effective rows are allowed to pick any receipt check. Then `pin_live` could bind `pin_env_scrub`: same argv, identical stdout, and a uniqueness rule does not catch it. Worse, if uniqueness is only per row, an effective `producer_before` could bind `producer-oracle-repair.json:producer_before_oracle`. That check satisfies the original producer_before expectation (exit 1 + literal), so the crash would turn green while every row still reads "effective".
*Correction:* an effective row requires `check == name`. The named receipt must contain exactly one check of that name, and no other pinned receipt may contain it (cross-receipt uniqueness). The current data meets this rule at no cost, because every expected name lives in exactly one receipt.

**D3. A superseded row that drops its raw observation.** The schema text lists superseded rows as `name/state/reason/superseded_by` with no `receipt/check`. The Gate interface, however, requires the raw producer_before to be kept. Without the pointer, the failing observation is not machine-bound and the gate output can omit it.
*Correction:* superseded rows must also carry `receipt`+`check` (with `check == name`). The gate **evaluates them anyway** and emits the observed exit and per-field mismatch (`contains` missing), alongside the disposition. A superseded row is never removed from the output.

**D4. Arbitrary replacement: superseding a real failure with unrelated green rows.** Example: supersede `witness_check` with `superseded_by: [witness_count]`. Every listed replacement passes, so "replacements pass their own expectations" accepts it.
*Correction (generic, data-derived, no bespoke list):*
- (a) Each replacement is an expected key, `state: effective`, not equal to the superseded name, and appears in no `superseded_by` chain. This makes cycles and chains impossible by construction.
- (b) Each replacement passes its own original expectation.
- (c) **At least one replacement's observed check satisfies the superseded row's original expectation.** `producer_before_oracle` meets this (exit 1 + literal present); `witness_count` cannot meet `witness_check`'s `WITNESS_CHECK: CLEAN`.
- (d) Subject continuity: every argv path in the superseded check that is pinned in `expected.inputs` (`.ufo/evidence/round-13/producer-before.py`) appears in some replacement's argv. The oracle's `--source` argument meets this.

Optionally, for this round, also allow only one supersession, `producer_before → {producer_before_oracle, producer_after_oracle}`, and report any other superseded row as a finding (exit 1).

**D5. Superseding a passing row.** If the raw observation already matches, supersession swaps authority while hiding nothing. That same move can later mask a regression.
*Correction:* emit `supersession_of_passing_observation` (exit 1). A superseded row is legal only where the gate's own evaluation shows a mismatch.

**D6. Exit-only and summary-verdict authority.**
- The receipt's `exit_matches:true` for raw producer_before is false proof, which is round-13 defect 1.
- `verification-verdict.json` claims `baseline_final_count` matched, with no raw check behind it.

*Correction:* the gate never reads `exit_matches`, `expected_exit` or any verdict file. It recomputes every predicate from raw `exit`/`stdout` (structured fields from `json.loads(stdout)`), and reports disagreement with a receipt's self-claim as informational. Contains semantics are **stdout-only**: every round-13 literal is in stdout, and for producer_before the result is the same either way. Record that choice in the output.

**D7. Duplicate JSON keys silently pick the last value.** For example, a row with `"state":"effective","state":"superseded"`, or duplicate `inputs` keys. A human reader sees one value and `json.load` uses another. The dispositions file is the one input nothing else pins.
*Correction:* add `object_pairs_hook` that rejects duplicate keys in the dispositions file, expected file and receipts → exit 2.

**D8. Reason that only looks explicit.** `reason: " "` or a non-string passes a truthiness check.
*Correction:* `reason` must be a non-empty, non-whitespace `str`. The gate prints its own computed mismatch next to the reason, so readers never depend on prose. Optionally cross-check that the replacement receipt's self-declared `supersedes` names the same `receipt check` (`producer-oracle-repair.json.supersedes` starts with `verification.json producer_before`).

**D9. Re-authored expectations under a fresh pin.** The disposition author controls both `expected_file` and its `inputs` digest, so an edited copy of expected.json can be pinned.
*Correction:* the gate (or at minimum L1) asserts `expected_file == .ufo/evidence/round-13/expected.json`. Each receipt's own `expected_file` (verification.json has one) must equal it. L1 runs `git diff --quiet d6809df -- .ufo/evidence/round-13` and records the three SHA-256 values above.

**D10. Pre-registration overclaim (tradeoff to disclose; a code fix cannot remove it).** The oracle expectations and the oracle input digest were added after the 04:59Z verification run [INFERENCE: 12-entry measured set vs 13 inputs; oracles ran at 05:00Z; single commit]. The replacement expectations are therefore a post-observation repair receipt, not a pre-registered prediction (QUALITY 6). Valid as checked mechanism evidence; must not be called pre-registered or blind.

**D11. "Sole disposition fix" claim (C1) needs the before-run to fail for the right reason only.** If `dispositions-before.json` failed with exit 2 (schema or digest) or with extra findings, the claimed rejection would not discriminate.
*Correction:* L1 asserts that the before-run exits **1, not 2**, with exactly one failing expectation, `producer_before`, field `contains`. The after-run exits 0. The two dispositions files differ only in the producer_before row (state, reason, superseded_by).

## Impacted axes

- calibration (C1): D1–D9 are defects to fix before admission; D10 is a disclosed tradeoff.
- depth: unchanged.
- No harm to frozen evidence if the corrections stay within the round-14 files.

## Checks for L1 (after all seats finish)

1. `git diff --quiet d6809df7775338f000e44c8a916067b8866867fb -- .ufo/evidence/round-13 tools/mutate-and-run.sh` → 0. Confirm the three SHA-256 values above.
2. `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json`: expect **exit 1**, a single failing finding `producer_before`/`contains`, and all other 11 rows matched.
3. The same command on `dispositions.json`: expect **exit 0**. The output still contains producer_before with observed exit 1 and `contains` mismatch, plus replacements `producer_before_oracle` (exit 1, literal+FAIL) and `producer_after_oracle` (exit 0, 41/41).
4. Static diff of the two dispositions files with `json.load` and a duplicate-key hook: same `expected_file`/`inputs`, same 12 row names (no `pin_env_scrub`/`metadata_emit`/`frozen_and_guardrail_unchanged`), with the producer_before row as the only difference.
5. `--selftest`: exit 0, and the fixtures must include these adversarial cases with stable IDs:
   - effective row binding a different check name (`pin_live→pin_env_scrub`; `producer_before→producer_before_oracle`)
   - unrelated replacement (`witness_check` superseded by `witness_count`)
   - superseded row missing receipt/check
   - superseding a passing row
   - replacement that is itself superseded, or a cycle
   - whitespace-only reason
   - duplicate JSON keys
   - unknown 13th row
   - receipt-only name as a replacement
   - `exit_matches:true` exit-only false positive
   - `expected_file` pointing at a non-historical copy
6. Report wording: "12 expected rows", and "post-observation repair receipt, not pre-registered".

Tool installs/updates: none.
