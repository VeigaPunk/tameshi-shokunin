# ReviewCLIExamples — round-15 C1 CLI contract and selftest path (static review)

Seat: `TameshiR15.ReviewCLIExamples` (leaf reviewer, wave w2). Author-side advisory only. No checks, builds, tests, formatters, or gate executions were run. Every "traced" result below is a static trace of source; nothing was executed, and no pass is predicted.

Tools installed or updated: none. No pacman transactions (operator pause honored).

## Scope and bytes read

- `tools/context-capture.py` — the C1 gate. The file changed twice during this review: tag `#472A` (2116 lines) → `#6F31` (2123) → `#5BA8` (2129). Findings below cite the final `#5BA8` bytes. Validator bodies (`validate_environment` 518, `validate_runs` 561, `validate_comparison` 573, `validate_sources` 625, `validate_mapping` 648, `recompute_comparison` 881, `recompute_mapping` 1041, `verify_recorded_verdict` 1111, `check_receipt` 1155) were read at `#472A` and have shifted by exactly +3 lines in `#5BA8` (the `KNOWN_ARGUMENTS` insert); their bodies were not re-diffed line by line.
- `SKILL.md:1677-1692` — round-15 gate/probe registry row for `retained invocation-context gate` (line 1681) and its trailing note.
- `.ufo/evidence/round-14/context-receipt.json` — top-level fields only (grep: lines 4-7, 414-423). Its digest and recomputed verdict were not checked.
- `.ufo/waves/round-15/w2/swarm-registry.json` (wave membership), `AGENTS.md`, `corpus/lessons/round-14-verifier-spotcheck.md` (Routed defect 5).

## CLI contract — registry commands trace to source

| Registry entry command | Parse path (`#5BA8`) | Outcome traced |
|---|---|---|
| `python3 tools/context-capture.py --check` | `parse_argv` 2032-2093: mode=check, receipt=None, expected=None, `(receipt is None) != (expected is None)` False | frozen mode → `run_check` 1301-1347 → pinned sha/id/exit at 137-144 |
| `--check --receipt FILE --expected FILE` | 2059-2077 value consumed; both given | explicit mode; `load_expected` before receipt read (1316) |
| `python3 tools/context-capture.py --selftest` | 2049-2052 mode=selftest; 2082-2085 rejects other args | `run_selftest` 2014-2026 |
| usage 64 (`--check` alone with receipt only, no args, unknown flag, `--selftest --json`) | 2033-2034, 2080-2081, 2086-2087, 2079, 2082-2084 → `main` 2099-2106 prints `id=usage_error exit=64` | pinned by `usage_case` at 2005-2011 |

Registry-to-source pin agreement (SKILL.md:1681 vs source):
- Frozen sha `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` == `FROZEN_RECEIPT_SHA256` (137-139). Character-for-character match.
- Frozen id `context_consistent`, exit 0 == `FROZEN_EXPECTED_ID/EXIT` (143-144).
- Expected-pin schema `tameshi-context-expected-v1` with `receipt_sha256/id/exit` == `EXPECTED_KEYS` (250) and `validate_expected`.
- Exit 0/1/2/64 map == `USAGE` text (269-273) and the registry row. 64 is labelled could-not-evaluate in both.
- Frozen receipt `.ufo/evidence/round-14/context-receipt.json`: `tool_sha256` 7313e9a2…89 == `FROZEN_TOOL_SHA256` (140-142); `status` ok and `exit` 0 with `reasons` []; `lane_root` `/home/vgpnk/Projects/shokunin/tameshi-shokunin` is the child of `fleet_root` `/home/vgpnk/Projects/shokunin`, satisfying `validate_top` 487-491. Digest and full recompute NOT checked (static only).

Trace of selftest pins against recompute code (the 38 recorded checks = 31 `check_case` + 5 `usage_case` + 2 hermetic). Each pinned primary id is the first finding the code emits, traced statically:
- `payload-digest-lie` → `comparison_tool_digest_mismatch`: `recompute_comparison` 931-944 runs before `recompute_sources` 1017, so the comparison finding is primary. Consistent.
- `missing-injected-env` → `missing_injected_environment`: `validate_environment` 527-528 allows an absent `injected_env`; `recompute_environment` 808-811 emits the finding. Consistent.
- `mapping-constant-swap` → `mapping_mismatch` via the `elif all_match is False` branch (1102-1105); no `problems` raised because the recorded fields agree. Consistent.
- `expected-missing`, `receipt-missing`, `expected-invalid`, `expected-digest-invalid`, `snapshot-tampered`, `expected-verdict-mismatch`: traced through `run_check` 1316-1347, `load_expected`, `validate_expected`, `apply_expected` 1268-1289. Consistent.
- `usage-*` cases: stderr contains `id=usage_error` (`main` 2104-2105) and exit 64. Consistent.
- Remaining cases (structural, JSON, control, mapping and comparison mutations): primary id matches the first `collect_finding`/`CouldNotEvaluate` in the traced path. Consistent.

Bounded agreement: registry entry commands parse to the intended mode; pinned constants and frozen-receipt top-level fields agree; every literal selftest pair traces to its emitted primary id. None of this is an observed run.

## Findings (by severity)

### F1 — Medium — new `KNOWN_ARGUMENTS` guard changes an exit class with no pinned case
- Source: `tools/context-capture.py:251-253` (constant), `2065-2068` (guard in `parse_argv`).
- Change: a `--receipt`/`--expected` value that equals a recognized flag now raises `UsageError` → exit 64, instead of being consumed as a path.
- Coverage gap: the selftest table (`run_selftest_cases` 1737-2011) pins five usage cases (2005-2011) and none exercises this branch. Deleting lines 2065-2068 leaves the selftest unchanged.
- Counterexample (static trace, not executed): `--check --receipt --json --expected e.json`.
  - With the guard (`#5BA8`): exit 64 `usage_error`.
  - Without the guard: `receipt="--json"`, `expected="e.json"`, `json=False`. `run_check` loads `e.json` first (1316): absent → `expected_missing` exit 2; present → `receipt_missing` exit 2.
  - So the guard shifts the exit from 2 to 64 for this input, and the selftest cannot detect the shift.
- Recommendation: add `harness.usage_case("usage-flag-as-value", ["--check", "--receipt", "--json", "--expected", "expected.json"])` pinned to 64 / `usage_error`, and document the rule in `USAGE`. Changes no verdict semantics.

### F2 — Low — selftest setup failure can escape as a traceback with exit 1
- Source: `run_selftest` 2014-2026. `harness = SelftestHarness()` (2015) runs before the `try:` (2016). `SelftestHarness.__init__` (1583-1589) calls `tempfile.mkdtemp(..., dir="/tmp")`. `main` (2096-2125) only wraps `run_check`, not `run_selftest`.
- The `except Exception` at 2019 claims "setup failure is loud but never a traceback", but it covers only `run_selftest_cases`. `harness.finish()` (2024) is inside the outer `try`, so its exceptions propagate through `finally` as a traceback.
- Counterexample (static trace; [INFERENCE] on Python exit status): if `/tmp` is missing or unwritable, `mkdtemp` raises before the `try`, and the process exits 1 with a traceback. Exit 1 is the "failed verdict" class, not could-not-evaluate (2).
- Recommendation: move construction inside the guarded block and map to exit 2.

### F3 — Low — hard-coded `dir="/tmp"` ignores `TMPDIR`
- Source: `tools/context-capture.py:1584-1585`. Earlier snapshot used `tempfile.mkdtemp(prefix=...)` with the default directory. The docstring (line 27) still says "tempfile.mkdtemp()". Worsens F2 only on hosts without a writable `/tmp`. Recommendation: drop `dir="/tmp"` or document it.

### F4 — Low — dead parameter `expected_bytes`
- Source: `check_case` signature 1618 (`expected_bytes=None`), branches at 1628-1629 and 1640-1642.
- No call site in `run_selftest_cases` (1737-2011) passes `expected_bytes`. Dead code under AGENTS "delete dead weight".
- It also hints at an intended malformed-expected-bytes case (`parse_json_strict` on the expected file, `expected_invalid`). No such case exists, so the expected-file JSON parse path is unpinned. Either add the case or delete the parameter.

### F5 — Low (registry) — pinned negative-fixture digest is not enforced by the tool
- Registry `SKILL.md:1681` lists `negative fixture context-missing-env.json sha256 1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` under "Pinned values". The file exists at `.ufo/evidence/round-14/context-missing-env.json` (glob).
- Grep of `tools/context-capture.py` for `context-missing-env` and `1ee9d09` returns no match. The gate never reads or pins that digest. The registry row therefore documents a pin with no enforcing code. Digest not verified (no execution).
- Recommendation: either remove the digest from the Pinned-values column (it is documentation only) or add a selftest/frozen check that pins it.

### F6 — Low (registry) — `--selftest` exit classes undeclared
- Source: `finish` 1727-1734 returns 1 on any failed case and 0 on all-pass; `run_selftest` 2019-2023 returns 2 on setup error.
- Registry `SKILL.md:1681` "Self-test command" column names the command only and states no exit classes. The round-14 lesson asked for explicit exit classes. Recommendation: add "selftest 0 pass / 1 failed case / 2 setup error" to the row.

### Observation (scope, not a defect) — no prospective capture path
- The docstring (lines 9-12) states the tool "does not capture". The lane contract for this round mentions "normal prospective capture writes round15 only". The tool is check-only; the registry row (line 1681, "check reads receipt bytes only, writes nothing") agrees with the tool. If round 15 requires a capture, none exists in this file. [INFERENCE on scope; not a source defect.]

## Counterexamples with no execution

No command was executed. The counterexamples are static traces in F1 and F2 and rest on the source at the cited lines. Their observable behavior has not been demonstrated.

## Verification gaps (for L1, not run here)

- Run `python3 tools/context-capture.py --selftest` once after the wave returns and confirm all 38 recorded lines report OK. Static tracing does not prove this.
- Run `python3 tools/context-capture.py --check` and compare the output to the frozen pin. The receipt digest, the frozen `probe_sha` against `payload_tool_sha256_matches_disk`, and the mapping leg recompute were not traced.
- Re-hash `context-missing-env.json` against the registry digest (F5) and confirm the frozen receipt digest.
- Re-verify F1 by deleting lines 2065-2068 in a scratch copy and running `--selftest` (expected: still all green, which confirms the gap).

## Routing

- Message to `TameshiR15`: F1 only (implementation-critical: a new exit-class branch with no literal pinned pair violates the round's literal-pair requirement). F2-F6 are low and are carried in this report.
- No peer or main-agent message beyond that.
