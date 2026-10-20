# RetainedVsLive — round-15 w2 static review

Lane: tameshi-shokunin. Seat: `TameshiR15.RetainedVsLive` (leaf; no subagents).
Scope: connect the promoted retained-receipt gate `tools/context-capture.py` to the original round-14 experiment `.ufo/evidence/round-14/capture-context.py` and its retained outputs. Static review only. No gate, selftest, probe, runner, or replay argv was executed. No digest was computed.

## Source read (exact)

| Source | Snapshot tag | Ranges read |
|---|---|---|
| `tools/context-capture.py` | `472A` (start), `6F31`, `5BA8` (end) | 1–281, 296–360, 363–460, 456–615, 620–1113, 1108–1353, 1299–1353, 1731–2005, 2020–2116 (grep for I/O, subprocess, and key predicates at `5BA8`) |
| `.ufo/evidence/round-14/capture-context.py` | `096B` | 1–647 (full; partly via 1–125, 126–260, 259–650 windows) |
| `.ufo/evidence/round-14/context-receipt.json` | `D7EE` | 1–424 (full; line 81 raw) |
| `.ufo/evidence/round-14/context-missing-env.json` | `970E` | 1–421 (structure only) |
| `.ufo/evidence/round-14/guardrails.json` | `FE14` | 1–76 |
| `corpus/lessons/round-14-verifier-spotcheck.md` | `1267` | 1–173, esp. Routed defects item 5 |
| `AGENTS.md` | `A117` | 1–6 |

**Snapshot instability.** `tools/context-capture.py` changed during this review (`472A` → `6F31` → `5BA8`; a 3-line shift before `validate_top`, plus added selftest case `expected-verdict-mismatch`). Every finding below was re-checked at `5BA8` by grep or re-read. Line numbers are `5BA8` unless marked as historical (`capture-context.py`, tag `096B`).

## Tooling record

No install or update was performed. No pacman, uv, npm, or cargo transaction. No `~/.omp` credential or DB was read.

## 1. Predicate transfer map (historical → promoted)

Historical `decide()` (capture-context.py 553–580) emitted `mismatch`/1 from exactly seven reason classes. Each is re-derived in check mode from retained raw fields. The mapping is:

| Historical reason / capture predicate | Promoted finding id | Re-derivation in check mode | Status |
|---|---|---|---|
| `comparison.equal` / canonical JSON compare after dropping top-level `observed_at` (hist. 387–391) | `comparison_mismatch` | `recompute_comparison` (~878–978) re-parses `runs.{baseline,injected}.stdout` strictly and recomputes both sha256 digests and `equal`. The canonical text is byte-identical: `json.dumps(sort_keys=True, separators=(",", ":"))` after `pop("observed_at")`. | Transfers exactly |
| `payload_tool_sha256_matches_disk` (hist. 380–383) | `comparison_tool_digest_mismatch` | Compares the payload `tool_sha256` against **`sources.probe.sha256` as retained**, not the disk file. | Transfers only as retained-record self-consistency (see §3) |
| `environment.env_delta_matches_declared`, `injected_env` (hist. 531–534) | `environment_delta_mismatch`, `missing_injected_environment` | `recompute_environment` (~805–846) requires `injected_env == {"GIT_DIR": POISON}`, `env_delta_keys == ["GIT_DIR"]`, `poison_path_exists` literal False. | Transfers as a declared-value check (see §3) |
| `baseline_has_GIT_DIR is False` (hist. 535, 568) | `environment_baseline_git_dir` | Literal False check. | Transfers exactly |
| `positive_control.effective` (hist. 403–411, 570) | `positive_control_ineffective` | `recompute_positive_control` (~981–1014) recomputes `baseline_ok`, `reflects` (POISON in stdout/stderr or exit change), and `effective` from raw runs with the same formulas. | Transfers exactly |
| `sources.probe.matches_declared` (hist. 496–503, 572) | `probe_source_digest_mismatch` | `sha256 == declared_sha256`. `declared` is itself retained, not re-read from `.ufo/evidence/round-13/expected.json`. | Partial (see §3) |
| `sources.runner.matches_manifest_declaration` (hist. 504–509, 574) | `runner_source_digest_mismatch` | `sha256 == manifest_declared_sha256`. Same limit. | Partial (see §3) |
| `mapping.all_match` (hist. 260–337, 576) | `mapping_mismatch` | `recompute_mapping` (~1038–1105) recomputes the five per-leg checks, per-leg match, set and order equality, and `all_match` from the retained header, call, and manifest copies. Formulas match `mapping_block` (hist. 279–294) exactly. | Transfers as receipt-internal consistency only (see §3) |
| `status` / `exit` / `reasons` vs. verdict (hist. 629–630) | `receipt_verdict_mismatch` | `verify_recorded_verdict` (~1108–1129). | Promoted (new) |

Predicates in the promoted gate with **no historical `decide()` analog** (added, not transferred):
- `run_argv_mismatch`, `run_cwd_mismatch`, `run_env_delta_mismatch` (historical recorded `argv_equal`/`cwd_equal` but never decided on them).
- `tool_declaration_mismatch` (frozen mode only).
- `receipt_records_invalid_input`.
- Strict JSON (duplicate keys rejected), observed_at regex, and tightened structural validators.

Historical could-not-evaluate kinds (hist. 150–209, 340–348, 439–461, 471–472, 490–501) are **not** individually reproduced. Every retained `invalid_input` receipt collapses to `receipt_records_invalid_input`/2. The historical kind survives only in `error.kind`. `poison_path_exists` (historical exit-2 class) becomes `environment_delta_mismatch`/1 for a retained `ok` receipt that records `true`.

## 2. Exit and id concordance

- Usage 64, could-not-evaluate 2, mismatch 1, clean 0: the classes agree with the lesson's Routed defect 5 requirement. Usage 64 is documented as "usage / could-not-evaluate invocation" (`USAGE`, lines 266–270).
- Frozen replay, static trace: `FROZEN_RECEIPT_SHA256` = `05cb55…c1a`, `FROZEN_TOOL_SHA256` = `7313e9…d89`, expected `context_consistent`/0. The retained receipt declares `tool_sha256` `7313e9…d89` (textually equal to the pinned constant). Every key set in `context-receipt.json` matches `RECEIPT_KEYS` (19), `ENVIRONMENT_KEYS` (10), `RUNS_KEYS` (7), `COMPARISON_KEYS` (9), `POSITIVE_CONTROL_KEYS` (8), `SOURCE_ENTRY_KEYS`, `MAPPING_KEYS` (12), `LEG_KEYS` (9), and `CALL_KEYS` (7). `not_compared` contains all three `NOT_COMPARED_LIMITS`. The baseline stdout (line 81, raw) is a six-leg `pin-disposition-v1` `ok` document with `observed_at` `2026-10-20T06:35:01Z` (passes `OBSERVED_AT`). Static result: `ok`, exit 0, primary `context_consistent`.
  - [UNVERIFIED]: the on-disk SHA-256 of `.ufo/evidence/round-14/capture-context.py` (must equal `7313e9…`) and of `context-receipt.json` (must equal `05cb55…`). Neither was computed, per the no-execution scope.
- Retained guardrail `context-missing-env.json`: static trace → `missing_injected_environment`/1. This matches the historical literal pair in `guardrails.json` `context_setup_missing_field` (exit 1, stdout `missing_injected_environment`).

## 3. Limits and boundary (transfer boundary)

1. **Check mode re-derives only retained-record consistency.** It never reads `tools/pin-disposition.py`, `tools/mutate-and-run.sh`, `.ufo/evidence/round-13/pin-manifest.json`, or `.ufo/evidence/round-13/expected.json`. Consequently:
   - `sources.{probe,runner,manifest,expected_r13}.sha256` are never recomputed against bytes.
   - `probe.declared_sha256` and `runner.manifest_declared_sha256` are self-declared; the historical source was `expected.json`'s `inputs` and the manifest's `derived_from`, neither re-read.
   - Leg pins, rev values, and `runner_call` constant names are checked only against the copies stored inside the receipt.
   - **The historical runner-swap discriminator** (`runner_variable_swap_discriminator`, guardrails.json) parses live runner text. It has **no check-mode analog**. It transfers only as the receipt-level fixture `mapping-constant-swap` (see §4).
   - Authentication rests entirely on the `--expected` receipt_sha256 pin (or the built-in frozen pin). This matches the documented "digest pin is the integrity authority" (docstring 99–101).
2. **Injection is inferred, not observed per run.** The probe's injected run env is never recorded. `runs.env_delta` and `environment.injected_env` are declared. The only raw discriminator is the separate `git rev-parse` positive control. The retained positive control shows the GIT_DIR poison is effective for git; it does not prove the probe's injected run executed under that env. Same limit as historical (capture-context.py 399–411, 547–550).
3. **No replay argv executed.** Confirmed by grep: `subprocess` appears only in the selftest harness (`SelftestHarness.run`), which invokes `sys.executable -I SELF` on synthetic fixtures. Check mode never executes `runs.*.argv`, `positive_control.argv`, or the probe. `runs.*.stdout` is parsed as stored.
4. **Stricter than the historical writer (validator narrower than capture):**
   - `payload_tool_sha256_matches_disk` must be a literal bool (line 601), but the historical writer records `null` on every injected-failure path (hist. 369, 371–375). **Defect D1 below.**
   - `sources.probe.declared_sha256` and `runner.manifest_declared_sha256` must be hex (lines 636, 641). The historical writer records `null` when `expected.json` lacks the key or the manifest lacks `derived_from.sha256`, and that case decides as `mismatch`/1. The promoted gate returns `receipt_structure_invalid`/2. **Defect D2 below.**
   - Probe stdout parsed with duplicate-key rejection (`_no_duplicate_keys`, 311–317) and an `observed_at` regex. Historical used plain `json.loads` and accepted any string. Pin-disposition output is well-formed, so no honest receipt is affected, but this is a boundary.
5. **Poison-path class differs.** Historical treats `poison_path_exists` as could-not-evaluate (exit 2, hist. 469–472). Promoted treats a retained `ok` receipt recording `true` as `environment_delta_mismatch`/1 (`recompute_environment`). Historical could never write such an `ok` receipt, so this is a stricter disagreement, not a transfer.
6. **Expected-pin semantics (see D3).**
7. **Frozen pin is a built-in constant.** Frozen mode does not check the on-disk tool digest; it checks only the receipt's self-declared `tool_sha256`. Documented (docstring 99–101).

## 4. Selftest pinning vs. historical controls

- Pinned (`check_case` / `usage_case`, invoking the real CLI via `subprocess` with `-I`, exit + JSON id checked): clean, missing-injected-env (`missing_injected_environment`/1, plus `receipt_verdict_mismatch` as secondary), null-injected-env, comparison-raw-mismatch, comparison-observed-at-lie, payload-digest-lie, control-ineffective, control-flag-lie, mapping-check-lie, mapping-constant-swap, mapping-order-lie, probe-source-lie, runner-source-lie, truthy-matches-declared, truthy-all-match, bool-exit, exclusions-widened, comparison-container, duplicate-key, malformed-json, non-object-json, invalid-utf8, receipt-missing, snapshot-tampered, expected-missing, expected-invalid, expected-verdict-mismatch (clean receipt only), stored-verdict-lie, retained-invalid-input, expected-digest-invalid, baseline-unusable, five usage cases. Hermetic checks: `hermetic-no-lane-path`, `hermetic-temp-only`.
- **Not pinned:** the injected-run failure path (D1), null declared digests (D2), pin mismatch with retained exit 1 or 2 (D3), and the equal-valued variable swap (D4).

## 5. Defects (counterexamples are static traces, not executed)

### D1 — implementation-critical: honest injected-failure mismatch receipts exit 2
- Historical writer (`capture-context.py` 350–375): on injected exit≠0 it returns with `payload_tool_sha256_matches_disk = None`, `baseline_comparable_sha256 = None`, `injected_comparable_sha256 = None`, `equal = False`, `error = "injected probe run produced no JSON document (exit=N)"`, and `observed_at.injected = None`. `decide` then returns `mismatch`/1.
- Promoted `validate_comparison` (line 601) calls `require_bool(payload_tool_sha256_matches_disk)`. `None` raises `receipt_structure_invalid`.
- Counterexample: `context-receipt.json` with `runs.injected = {exit: 128, stdout: "", stderr: "fatal: …", …}` and the comparison block above, `status: "mismatch"`, `exit: 1`, reasons `["injected observation differs …"]`. Trace: `check_receipt` → `validate_comparison` raises → `run_check` → `result_from_exception` → **exit 2, id `receipt_structure_invalid`**. Expected from the design: exit 1, `comparison_mismatch` (the recompute branch at ~955–978 is designed for this path, and its error strings are byte-identical to the historical strings).
- The `recompute_comparison` error branch (`type(injected) is not dict`) is therefore unreachable for any honest receipt.
- Fix: accept `None` for `payload_tool_sha256_matches_disk` iff `comparison.error` is non-null. Add a selftest case pinning `comparison_mismatch`/1 for an injected exit-128 receipt.

### D2 — same class, lower severity: null declared digests exit 2 instead of mismatch/1
- Historical: `probe_declared = inputs.get(PROBE_REL)` and `derived.get("sha256")` may be `None`; `matches_declared` then False (hist. 499–509), and `decide` returns mismatch/1.
- Promoted: `require_hex(declared_sha256)` (line 636) and `require_hex(manifest_declared_sha256)` (line 641) reject `None` → exit 2.
- Fix: allow `None` iff the corresponding `matches_*` is literal False. The recompute at ~1022/1031 already handles `None` correctly.

### D3 — contract divergence: pin-mismatch id/exit disagrees with documentation
- Docstring (lines 74, 88–93) lists `expected_verdict_mismatch` as exit 1, and says a pin mismatch exits 1. Implementation (`apply_expected`, ~1268–1289): `expected_verdict_mismatch` becomes the primary id and exit 1 **only when the recomputed exit is 0**.
- Counterexample A (retained exit 1): `context-missing-env.json` with expected `{id: comparison_mismatch, exit: 1}` → exit 1, primary id `missing_injected_environment`, `verdict_matches_expected: false`, and `expected_verdict_mismatch` appears only as a secondary finding. A CI consumer reading exit codes cannot tell this from a matched pin when the pinned exit is 1.
- Counterexample B (retained exit 2): `receipt-missing` with expected `{id: context_consistent, exit: 0}` → **exit 2** (documented: pin mismatch → 1).
- Selftest covers only the clean-receipt case (`expected-verdict-mismatch`).
- Fix: when `matches` is False, set exit 1 and primary id `expected_verdict_mismatch` in all cases, or document the precedence explicitly and pin both counterexamples.

### D4 — selftest fixture does not exercise the equal-valued discriminator it is labelled for
- `mapping-constant-swap` (~1814–1835) changes only `leg[0].runner_call.rev_constant` (JS leg, `rev_value` 175de…) to `REV_BASH`. The values differ (BASH's commit is fecee…). The historical guardrail `runner_variable_swap_discriminator` used `REV_BASH→REV_CHECKLIST` on the bash-surface leg, where both values are `fecee…`, precisely to show name-binding matters when values are equal.
- The promoted recompute is name-based (`call["rev_constant"] == "REV_"+suffix`), so an equal-valued swap would still be caught. It is not pinned by any case, and the fixture comment ("equal-valued") is inaccurate.
- Fix: add the equal-value case (bash-surface → `REV_CHECKLIST`) and pin `mapping_mismatch`/1.

## 6. Bounded agreement (static, explicit)

Agreement is claimed only where historical and promoted formulas were compared line-by-line:
- Canonical comparison: identical `json.dumps` arguments, identical `observed_at` pop, identical sha256 (hist. 387–390 ↔ 923–929). Agreement.
- Positive control `baseline_ok` / `reflects` / `effective`: identical formulas (hist. 403–409 ↔ 984–989). Agreement.
- Environment: `injected_env == {GIT_DIR: POISON}`, `env_delta_keys == [GIT_DIR]`, `baseline_has_GIT_DIR is False` (hist. 531–535 ↔ 817–838). Agreement.
- Mapping per-leg five checks (hist. 279–299 ↔ 1054–1068), set/order equality, `all_match` (hist. 313–335 ↔ 1083–1095). Agreement.
- Verdict: historical `ok` iff no reasons; promoted `ok` iff no findings. Agreement modulo id naming.
- Excluding D1–D3, every retained `ok` receipt the historical writer can produce is accepted and reproduced by the promoted gate with exit 0 (static trace over the frozen receipt's key sets and values). Not executed.

## 7. Verification for main agent (not run here)

- `python3 tools/context-capture.py --selftest` — expect `SELFTEST: PASS` after D1–D3 fixes; currently expected to pass the pinned cases only.
- `python3 tools/context-capture.py --check` — frozen replay, expected exit 0 (static trace; unverified).
- Hash checks: `sha256sum .ufo/evidence/round-14/capture-context.py` (expect `7313e9…d89`) and `sha256sum .ufo/evidence/round-14/context-receipt.json` (expect `05cb55…1a`).
- After D1: `context-capture.py --check --receipt <synthetic injected-exit-128 receipt> --expected <pin>` → exit 1, `comparison_mismatch`.

## Messages sent

- To `TameshiR15`: D1 (implementation-critical) and D3 (exit contract). D2 and D4 are in this report only.

## Report-path note

The Target assignment says to write only this report. The Report: trailer is relative to the tameshi root; written there.
