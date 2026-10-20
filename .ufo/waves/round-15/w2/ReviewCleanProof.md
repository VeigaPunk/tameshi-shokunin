# ReviewCleanProof — C1 clean fixture vs. checked-receipt identity (round 15, wave 2)

Seat: `TameshiR15.ReviewCleanProof` (reviewer, leaf). Static review only. No gate, selftest, `--check`, probe, git, or hash computation was executed. Author-side advisory; not admission authority.

Tool installs/updates: none. No pacman transaction. Read `~/.omp/agent/RULES.md` only. Did not read `agent.db*`, credentials, or launch the omp CLI.

## Scope and exact source read

- `tools/context-capture.py` (live revision in the working tree, marker `#472A` at read time):
  - 1–123 (docstring, modes, stable IDs, exit map, constants, `DEFAULT_LANE_ROOT`)
  - 119–303, 299–603, 600–904, 899–1154 (utilities, structural validators, recompute functions, `verify_recorded_verdict`)
  - 1151–1349 (`check_receipt`, `validate_expected`, `make_result`, `emit`, `apply_expected`, `result_from_exception`, `run_check`)
  - 1348–1583 and 1578–1803, 1800–2116 (fixture builder, `SelftestHarness`, `check_case`, `usage_case`, `finish`, every selftest case, `parse_argv`, `main`)
  - Some structural lines are display-collapsed in range reads; the functions relied on below were re-read until visible.
- `SKILL.md:1609–1691`, specifically the context contract (1654–1674) and the round-15 registry row (1680).
- `corpus/lessons/round-14-verifier-spotcheck.md` routed defect 5 (line 160), read earlier.
- `.ufo/evidence/round-14/context-receipt.json`: `tool_sha256` (line 4), key structure via grep of 2- and 4-space keys, and lines 81 and 95 (baseline and injected stdout) read with `:raw`.

## Question

Does the selftest clean case, `run_selftest_cases` line 1737 `harness.check_case("clean", clean, "context_consistent", 0)`, positively identify a checked receipt, rather than help text or a constant-0 result?

## Bounded agreement (what the clean branch proves)

The clean case passes only if all of these hold, enforced in `check_case` (1645–1664):

1. Subprocess exit is 0 (`proc.returncode == expected_exit`, 1653–1655).
2. The final stdout line parses as JSON, is a dict, and has `id == "context_consistent"` and `exit == 0` (1645–1656).
3. `findings == []` (1660–1661).
4. `payload["receipt"]["sha256"]` equals the sha256 of the exact receipt bytes written (1662–1664).
5. Stderr contains no `Traceback` (1658).

Source-side reasoning:

- Exit 0 is reachable only through `run_check` → `emit` → `result["exit"]`. That value is set by `verify_recorded_verdict` (1108–1129), which sets `code = 0` only when `findings` is empty. `findings` comes from the six `recompute_*` calls in `check_receipt` (1169–1174), which re-derive every fact from raw fields. Every other path returns 1 or 2 (`result_from_exception`, `invalid_input`, `apply_expected` flips to 1). `main` returns 0 for `-h`/`--help` (2094–2096), and `usage_case` / the clean branch both reject that case.
- Clean-fixture internal consistency, checked by hand against the validators and recomputes: `build_fixture_receipt` (1388–1569) satisfies `validate_top` (459–512), `validate_environment`, `validate_runs`, `validate_comparison`, `validate_positive_control`, `validate_sources`, `validate_mapping` key sets and literal types (including `runs.env_delta` and `runner_call` line numbers), and all recompute equalities (`recompute_comparison` 878–978: canonical comparable sha, observed_at, raw_stdout_equal False because only observed_at differs, equal True; `recompute_positive_control` 981–1014: baseline_ok, reflects via POISON_PATH in stderr, effective; `recompute_mapping` 1038–1105). So the clean fixture reaches exit 0 by re-derivation, not by a stored-verdict shortcut.

Counterexample attempts (none succeed against the clean branch):

- `--help`/`-h` stub: exit 0 but no JSON. The last line of USAGE (`  "exit": 0 | 1 | 2}`) is not valid JSON, so `payload` is None and `observed_id = "<unparsed>"`. Fails at 1656.
- Constant-0 stub that prints `{"id":"context_consistent","exit":0,"findings":[]}` with no sha echo: fails at 1663–1664.
- Constant-0 stub that also echoes the correct sha256: passes the clean case alone. It fails the negative cases, which expect distinct IDs/exits. Examples: `missing-injected-env` (1739–1744, which keeps stored `status:"ok"` and removes `injected_env`, so a trust-stored-status shortcut would return clean); `comparison-raw-mismatch` (1751–1761); `control-ineffective` (1784–1794); `stored-verdict-lie` (1938–1944). The suite as a whole is the discriminator. The clean case by itself is not.

## Findings (none implementation-critical; no message sent to TameshiR15)

**F1 — low, test strength: clean branch under-asserts the result identity.** `check_case` (1660–1664) asserts id, exit, findings and sha echo. It does not assert fields the source emits to define the explicit-mode clean identity: `status == "ok"`, `mode == "explicit"`, `receipt.digest_matches is True` (make_result 1241), `verdict_matches_expected is True` (make_result 1247 / apply_expected 1274). No source path today makes these inconsistent with exit 0, so this is untested surface, not a live defect. Suggested: add those four literal assertions to the `expected_exit == 0` branch.

**F2 — medium, coverage residual: the registry's default entry command is not hermetically exercised.** SKILL.md:1680 names `python3 tools/context-capture.py --check` (frozen, no arguments) as the maintained clean replay. Frozen mode (1298–1310, literal pins 136–144, `full_path` from `DEFAULT_LANE_ROOT` at 1302) is never run by `--selftest`. `tool_declaration_mismatch` (1175–1179) has no selftest case. The only positive identity for the real frozen receipt is an L1 run against the lane file. This is a structural limit (selftest must not read the lane), so it is a residual to record, not a defect to fix. The L1 run should cite the frozen clean replay as its evidence, not the selftest clean case.

**F3 — low, naming and claim wording: `payload_tool_sha256_matches_disk` does not read disk.** Recomputed at 923–925 as `baseline.tool_sha256 == probe_sha and injected.tool_sha256 == probe_sha`, where `probe_sha = receipt["sources"]["probe"]["sha256"]` (881), a recorded field. `recompute_sources` (1017–1035) compares that field to its own `declared_sha256`. The gate never opens `tools/pin-disposition.py` (docstring line 11: "does not read live lane inputs"). The name, which is required by `COMPARISON_KEYS` (206) and retained in the historical receipt, implies a disk comparison that never happens. The docstring (99–101) and SKILL.md:1662 correctly bound the claim to recorded facts. Suggest documenting the name as "recorded probe digest" in the docstring; do not rename, because that breaks the frozen schema.

**F4 — low, scope wording: the frozen clean receipt contains three changed legs.** The retained baseline document (receipt lines 81 and 95, read raw) reports `content_status: "changed"` for `js-kimi-census`, `bash-tsukuroi-census` and `bash-mado-verify` (worktree sha differs from pin), and `unchanged` for the other three. `validate_baseline_document` (765–796) rejects only `content_status == "unavailable"` (782) and requires `pinned.status == "verified"` (787), so the clean verdict is accepted. That is consistent with the registry's stated scope, but the bare word "clean" / `context_consistent` can read as "all legs unchanged." Suggest the registry row (SKILL.md:1680 / 1662) state that the retained observation records three changed legs and that clean concerns receipt-internal consistency only.

**F5 — info: stdout parsing reads only the last line (1646).** Harmless under `--json`, which emits one line (1250). It would tolerate stray leading text, so pinning the whole stdout as a single JSON document would be stricter. Not a defect.

## Frozen artifact static agreement (not executed; not a hash check)

- `FROZEN_TOOL_SHA256` (tool line 140–142) equals the retained receipt's `tool_sha256` (receipt line 4): both `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`.
- Retained receipt top-level, environment, sources, runs, comparison, positive_control and mapping key sets match `RECEIPT_KEYS`, `ENVIRONMENT_KEYS`, `SOURCE_PATHS`, `RUNS_KEYS`, `COMPARISON_KEYS`, `POSITIVE_CONTROL_KEYS`, `MAPPING_KEYS`, `LEG_KEYS`, `CALL_KEYS` and `MANIFEST_ENTRY_KEYS` by grep of key structure.
- Lines 81 and 95 (baseline and injected stdout) read verbatim are identical in every displayed character. So `raw_stdout_equal: true` and `equal: true` agree with the recompute.
- Registry sha `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` (SKILL.md:1680, 1656) equals the literal at tool lines 137–139 by reading.
- NOT VERIFIED: the sha256 of the receipt file itself. Static-only rule; not computed. L1 must confirm `FROZEN_RECEIPT_SHA256` against the bytes.

## Residual risk and verification gaps

- The clean case is positive evidence only in combination with the negative suite; alone it would not reject a stub that echoes correct fields (F1, and the constant-0-with-sha counterexample above).
- Frozen clean replay of the real receipt is L1-only (F2).
- Naming and scope wording (F3, F4) can mislead readers; they do not change exit codes.
- Nothing was executed here; every "passes" statement above is a static inference from the source and retained bytes.

## Checks the main agent should run once after the wave

1. `python3 tools/context-capture.py --selftest` (expect `SELFTEST: PASS`, exit 0).
2. `python3 tools/context-capture.py --check --json` (frozen clean, exit 0, id `context_consistent`).
3. Confirm `sha256sum .ufo/evidence/round-14/context-receipt.json` equals `05cb55b8…99c1a` (F2 / NOT VERIFIED above).
4. `sha256sum .ufo/evidence/round-14/capture-context.py` remains `7313e9a2…7d89` (historical bytes unchanged).
