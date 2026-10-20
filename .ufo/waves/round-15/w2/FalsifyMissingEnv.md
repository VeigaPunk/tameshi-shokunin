# FalsifyMissingEnv — round-15 wave2 critic report

Seat: TameshiR15.FalsifyMissingEnv (critic, leaf, static review only). I executed nothing under review: no gate, no selftest, no `--check`, no sibling instrument. Tools installed: none.

## Target
Check whether `tools/context-capture.py` (snapshot read tag `#472A`, 2116 lines) can false-clean the negative historical receipt `.ufo/evidence/round-14/context-missing-env.json` when compared with the clean `.ufo/evidence/round-14/context-receipt.json`. The negative receipt differs from the clean one only by the removed `environment.injected_env`.

## Source read (exact)
- `tools/context-capture.py`: lines 1–123 (docstring, exit map, IDs), 145–255 (constants and key sets), 438–1185 (structure validation, raw re-derivation, `check_receipt`), 1185–1349 (expected pin, `make_result`, `apply_expected`, `run_check`), 1571–1753 (`SelftestHarness`, start of `run_selftest_cases`). I also grepped every `injected_env` / `missing_injected` occurrence, which includes fixture line 1451 and the invalid-input fixture at line 1957.
- Historical data (data read only):
  - The two receipts as sorted-key JSON, compared with `diff`. The only difference is that `context-missing-env.json` lacks `"injected_env": {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`.
  - `sha256`: clean `05cb55b8…899c1a`, which equals `FROZEN_RECEIPT_SHA256`; missing-env `1ee9d09b…2aa208`.
  - Both receipts store `status: "ok"`, `exit: 0`, `reasons: []`, the same `tool_sha256` (`7313e9a2…`), and `runs.env_delta == {"baseline": [], "injected": ["GIT_DIR"]}`. So the negative receipt itself *claims* to be clean.
- `.ufo/evidence/round-14/guardrails.json` lines 10/25–32: the historical literal pair for missing-env is stdout `missing_injected_environment`, `expected_exit` 1.
- `.ufo/evidence/round-15/measure.py`: it counts structure only and does not replay missing-env.

## Static trace for the historical missing-env bytes
These are code-path facts, not an executed result.
1. `validate_top`: status `ok` is accepted, all `RECEIPT_KEYS` are present, schema matches, and `result_reuse`/`not_compared` are the same as in the clean receipt.
2. `validate_environment` (l.519–526): `injected_env` is deliberately excluded from the required set (`allowed - {"injected_env"}`). The absent key therefore does **not** become exit 2 and reaches the classifier.
3. `validate_runs`, `validate_comparison`, `validate_positive_control`, `validate_sources`, `validate_mapping`: their inputs are byte-identical to the frozen-clean receipt, so they behave the same as for that receipt.
4. `recompute_environment` (l.807–811): `environment.get("injected_env", "<absent>") == "<absent>"`, so the finding `missing_injected_environment` is collected first. Any receipt without that key gets this finding unconditionally. No other branch can drop it, and `collect_finding` only de-duplicates.
5. Recompute of the other blocks: their inputs are the same as in the clean receipt, so they add no further findings `[INFERENCE from identical bytes; not executed]`.
6. `verify_recorded_verdict` (l.1108–1129): the computed status is `mismatch` with exit 1, but the stored values are `ok`/0. This appends `receipt_verdict_mismatch`. The final result is `("mismatch", 1, [missing_injected_environment, receipt_verdict_mismatch])`.
7. `run_check` (l.1340): primary id is `findings[0]` = `missing_injected_environment`, exit 1.

## Paths that could false-clean
Each was checked against the code; none returns exit 0.
- **Pin claims clean:** an `--expected` pin `{sha 1ee9d09b…, id context_consistent, exit 0}` gives `apply_expected` → no match. Because the result exit is not 0, `collect_finding(expected_verdict_mismatch)` runs and the result stays exit 1 (l.1283–1285).
- **Correct literal pin:** a pin `{…, id missing_injected_environment, exit 1}` sets `verdict_matches_expected=true`, and the exit stays 1. A matched negative pin never turns into clean, as the docstring states at l.91–93.
- **Frozen mode fed missing-env bytes:** the digest `1ee9…` differs from `FROZEN_RECEIPT_SHA256`, so the result is `snapshot_tampered` exit 2 before any parsing.
- **Key-level evasions:**
  - Duplicate `injected_env` keys → `_no_duplicate_keys` → `receipt_json_invalid` exit 2.
  - A case-variant or misplaced key → extra-key check → `receipt_structure_invalid` exit 2.
  - A literal string `"<absent>"` as the value → not a dict and not null → exit 2.
  - `null` → `missing_injected_environment` exit 1.
  - `{}` or a wrong value → `environment_delta_mismatch` exit 1.
- **No exit-0 path exists** while `injected_env` is absent: exit 0 requires `findings == []` (l.1109, 1127), and step 4 makes that impossible.

## Selftest coverage of this pair
`run_selftest_cases` l.1739–1744 builds `missing_env` by `pop("injected_env")` from the clean synthetic fixture. The fixture keeps stored `ok`/0, which matches the historical shape. The case pins the literal pair `missing_injected_environment`/1 and requires both `missing_injected_environment` and `receipt_verdict_mismatch` in the findings. It runs through the public CLI as a subprocess (`sys.executable -I SELF --check --receipt … --expected … --json`, l.1637–1640) under `mkdtemp`. The pair `clean` → `context_consistent`/0 at l.1736–1737 uses the same base, so the only difference between the two cases is the removed field, as in the historical pair. `null-injected-env` (l.1746–1749) also pins `missing_injected_environment`/1.

## Verdict
**Bounded agreement: no falsifiable false-clean hole on this axis.** Static code paths make `context-missing-env.json` unable to reach exit 0 in explicit, pinned or frozen mode. Its classification is `missing_injected_environment`/1, which matches the round-14 guardrail literal pair. I am not claiming an executed pass; L1 owns the runtime replay.

## Non-blocking observations
These are tradeoffs, not defects, and require no correction for C1.
1. **`expected_ids` is a subset check, not an exact list** (`all(item in ids …)`, l.1668). A regression that *added* a spurious extra finding to the missing-env case (for example `environment_delta_mismatch`) would still pass the selftest. It cannot cause a false-clean: the primary id and exit stay pinned.
   - Smallest correction if the integration owner wants it: compare `ids == expected_ids` for cases that pass `expected_ids`.
2. **The gate's IDs differ from the guardrail's for some other inputs.** The historical guardrail one-liner maps *every* non-matching environment to `missing_injected_environment`, including `{}`, `env_delta_keys` drift and `baseline_has_GIT_DIR` true. The gate splits these into `environment_delta_mismatch` and `environment_baseline_git_dir`, all exit 1. The exit class is the same, and the literal pair still holds for the historical missing-env bytes. Only a claim that the gate reproduces the guardrail *id* for those other inputs would be false, and the docstring (l.60) makes no such claim.
3. **No retained expected pin for `context-missing-env.json` exists yet.** Nothing under `.ufo/evidence/round-15/` binds sha `1ee9d09b…` to `missing_injected_environment`/1, so a replay of the historical negative depends on L1 supplying that pin at check time. This is outside this seat's write scope and is not a code defect.

## Impacted axes
None regressed. The false-clean resistance of the retained-replay C1 gate holds on the injected_env-removal axis.

No implementation-critical defect was found, so I sent no message to TameshiR15.
