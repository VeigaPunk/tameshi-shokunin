# ReviewRedProof — C1 missing-env negative (round 15, wave 2)

Author-side advisory. Static review only. No check, selftest, build, test, formatter, hash, or CLI run was executed by this seat. No tools installed or updated. No implementation-critical defect found, so nothing was sent to TameshiR15.

## Scope and exact source read

- `tools/context-capture.py`
  - L11–30 docstring (`--check`, `--selftest`, usage)
  - L44–48 environment contract (`injected_env` must be exactly `{"GIT_DIR": POISON_PATH}`)
  - L58–97 stable finding IDs and exit map
  - L121–123 `VERSION`, `SELF`, `DEFAULT_LANE_ROOT`
  - L515–555 `validate_environment` (required-key check at L519–526)
  - L805–846 `recompute_environment` (absent branch L807–811)
  - L1108–1129 `verify_recorded_verdict`
  - L1152–1180 `check_receipt` (ordering L1162–1180)
  - L1186–1216 `validate_expected`
  - L1298–1344 `run_check` (snapshot digest L1323–1333; `primary = findings[0]` L1340)
  - L1265–1286 `apply_expected`
  - L1388–1569 `build_fixture_receipt` (verdict block L1566–1568)
  - L1572–1576 `SELFTEST_ENV`
  - L1611–1682 `SelftestHarness.check_case` (CLI argv L1637–1640; expected pin L1625–1630; id/exit/subset match L1653–1668)
  - L1728–1749 `run_selftest_cases` (clean L1737; `missing-injected-env` L1739–1744; `null-injected-env` L1746–1749)
  - L2005–2017 `run_selftest`
  - L2083–2110 `main` (internal exception to exit 2 at L2106–2110)
- `.ufo/evidence/round-14/context-missing-env.json` (retained negative; read via `?q=` projections only)
- `.ufo/evidence/round-14/context-receipt.json` (retained clean; read via `?q=` projections only)
- `SKILL.md` L1643–1675 (retained-check semantics, discriminating counterpart), L1681 (round-15 registry row)
- `corpus/lessons/round-14-verifier-spotcheck.md` L96, L104, L160 (routed item 5 requiring a standalone selftest for the context gate)

Digest of `context-missing-env.json` (SKILL.md L1653 claims `1ee9d09b…aa208`) was **not** computed by this seat.

## Finding F1 — the negative is one field at the environment level, but two findings at the receipt level (non-blocking, precision)

Severity: low-medium. The primary ID still discriminates. The problem is that the case is not a single-cause negative, and the harness tolerates the second cause by subset matching.

Evidence:
1. The mutation at `run_selftest_cases` L1739–1740 pops only `environment["injected_env"]`. It does not regenerate the stored verdict. The fixture's `status`/`exit`/`reasons` stay at `ok`/`0`/`[]` (L1566–1568 in the builder; the same clean values appear in the retained negative, see below).
2. `check_receipt` runs `recompute_environment` (L1169) before `verify_recorded_verdict` (L1180). The absent branch emits `missing_injected_environment` (L807–811). `verify_recorded_verdict` then computes exit 1 against the stored exit 0 and emits `receipt_verdict_mismatch` (L1108–1126). The observed finding list is therefore **two** entries: `[missing_injected_environment, receipt_verdict_mismatch]`.
3. The harness compensates with `expected_ids=[missing_injected_environment, receipt_verdict_mismatch]` (L1743–1744) and checks `all(item in ids …)` (L1665–1668). That is a subset check, not an exact-set check. The case therefore pins the second finding as expected behavior without saying so.
4. The retained negative has the same shape. `context-missing-env.json?q=.environment` has 9 keys with no `injected_env`. `context-missing-env.json?q={status,exit,reasons}` returns `{"status":"ok","exit":0,"reasons":[],"keys":19}`, identical to the clean `context-receipt.json` top level. Its stored verdict is therefore also stale, and the gate yields the same two findings. SKILL.md L1652–1656 describes it only as "must fail at exit1" with `missing_injected_environment`, and does not disclose the second finding.

Counterexample to "one changed field" as the design intent: an exact-set pin `findings == ["missing_injected_environment"]` for the selftest negative would **fail** today, because `receipt_verdict_mismatch` is also emitted from L1126. A reviewer reading "one changed field, not construction error" would see that the second finding is a fixture-construction artifact (stale stored verdict), not an environment fact.

Bounded agreement: the second finding is not masked to the point of hiding a regression. Removing the absent branch makes the primary `receipt_verdict_mismatch` (L1169 → L1340), so `apply_expected` fails (L1269–1270) and the harness fails at L1656. Lowering the case to a subset check is only a tolerance; it does not let an unrelated spurious primary through.

Recommended correction, not applied here: in the selftest negative only, regenerate the stored verdict so it is honest (`status` `"mismatch"`, `exit` 1, non-empty `reasons`). Then `verify_recorded_verdict` should emit nothing extra and `missing_injected_environment` is the sole finding, which an exact-set pin can assert. [INFERENCE from code reading; not executed.] Do not edit the retained round-14 negative (read-only evidence). Instead, document in SKILL.md that the retained negative's expected finding set is two IDs.

## Finding F2 — null-value negative has the same stale-verdict second finding (low, same root cause as F1)

`run_selftest_cases` L1746–1749 (`null-injected-env`) is the cleaner value-change form. It also leaves the stored verdict clean, so it emits `missing_injected_environment` plus `receipt_verdict_mismatch`. The case checks only the primary ID and exit, so it passes while hiding the second finding. Same correction as F1.

## Documentation gap (low)

- SKILL.md L1652–1656 and L1681 name `missing_injected_environment` as the failing ID. Both are consistent with primary-ID semantics (`run_check` L1340). Neither mentions that the stored verdict is stale and that a second finding (`receipt_verdict_mismatch`) is emitted.

## Bounded agreement (what holds, from static reading)

- **Same CLI.** `check_case` runs `[sys.executable, "-I", SELF, "--check", "--receipt", …, "--expected", …, "--json"]` (L1637–1640), the same entry as production (`main` L2083–2100). The negative does not use a separate construction path.
- **No digest trap.** `check_case` writes `receipt_sha256` from the mutated bytes (L1619–1628), so `snapshot_tampered` (exit 2, L1325–1333) cannot be the path.
- **Structural validation does not pre-empt the case.** `validate_environment` excludes `injected_env` from the required-key set (L520), so an absent key reaches the semantic check. Other environment keys (`env_delta_keys`, `env_delta_matches_declared`, `baseline_has_GIT_DIR`, `poison_path`) are unchanged, so no `environment_delta_mismatch` is produced (L805–846; the `else` branch is skipped when the key is absent).
- **Sentinel collision blocked.** `recompute_environment` uses `environment.get("injected_env", "<absent>")` (L807). A receipt carrying the literal string `"<absent>"` is rejected earlier by L527–532 (`receipt_structure_invalid`, exit 2) before the sentinel is compared. No collision reachable.
- **Baseline is valid.** The base fixture is the clean builder output (L1388–1569). The clean case expects `context_consistent`/0 (L1737), so the negative begins from a valid receipt, not a broken construction.
- **Crashes fail, not pass.** Any `KeyError` on the negative path is caught by `main` (L2106–2110) and emitted as `internal_error` exit 2, which fails the case that expects 1.

## Verification gaps

- No execution performed: no selftest, no `--check`, no digest computation (`sha256` of the retained negative unverified), no `lsp` (no language-server device was used; text grep and reads only).
- Findings F1/F2 are derived from static trace; the reconstructed finding list is [INFERENCE] until a maintainer runs the selftest at the L1 integration step.
- Scope excludes the historical `capture-context.py`, the exit-64 mapping, and the other registry rows.
