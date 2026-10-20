# ReviewExitMap — round-15 C1 exit map vs active SKILL registry (static, author-side advisory)

Scope: `tools/context-capture.py` r15 (delivered wave-1 source, unexecuted) against the active registry wording in `SKILL.md`. Static reading only. No gate, selftest, `--check`, `--help`, hashing, or git validation was run by this seat. Every "counterexample" below is a trace of the source path, not an observed run; each needs L1 confirmation.

Tool installs/updates: none. Writes: this report only.

## Source and registry read

- `tools/context-capture.py`: docstring 1-106 (exit map 88-97, stable IDs 58-86); constants 125-153 (frozen pin 136-144); USAGE 252-277; `validate_top`/`validate_environment` 459-555; `validate_runs`..`validate_mapping` 558-750; `recompute_environment` 805-846; `recompute_runs` 849-875; `recompute_comparison` 878-978; `recompute_positive_control` 981-1014; `recompute_sources` 1017-1035; `recompute_mapping` 1038-1105; `verify_recorded_verdict` 1108-1129; `validate_invalid_blocks` 1132-1149; `check_receipt` 1152-1180; `validate_expected`/`load_expected` 1186-1216; `make_result`/`emit` 1222-1262; `apply_expected` 1265-1286; `result_from_exception` 1289-1295; `run_check` 1298-1344; selftest harness 1579-1725; selftest cases 1728-2003; CLI `parse_argv`/`main` 2023-2116.
- `SKILL.md`: 1609-1675 (classification and exit-class prose), 1677-1681 (round-15 registry row, read raw at 1680).
- `corpus/lessons/round-14-verifier-spotcheck.md` routed defect 5, line 160 (exit-64 mapping, registry 64 path, standalone selftest).
- `corpus/lessons/round-15.md` lines 36-38 (admit criteria: "maps name every nonzero class") and 50-51 (mistakes table).

Registry pins cross-checked by text only: frozen receipt sha `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` (tool 137-139 = SKILL 1680). Frozen historical tool sha `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` appears at tool 141 and SKILL 1634. The negative fixture sha `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` appears only in SKILL 1652-1653 and is not checked in the tool. The fixture digests were not computed against bytes.

## Literal exit returns (agreement)

| Exit | Return site | Reachable only through | Agreement |
|---|---|---|---|
| 0 | `SELFTEST PASS` 1725; `main` help 2094-2096; `emit` of recomputed 0 | clean check, selftest pass, `-h`/`--help` | Docs say 0 = clean-only (see Finding 3) |
| 1 | `finish` 1723; `emit` of recomputed 1 | findings; `apply_expected` for recomputed 0 (1277-1282) | Agrees with docstring 89-93 and registry 1680 for the listed IDs |
| 2 | `run_selftest` setup error 2014; `emit` of recomputed 2 | every `CouldNotEvaluate` and `invalid_input` path | Agrees for every ID listed as exit 2 (checked 1 by 1) |
| 64 | `main` 2093 on `UsageError` | `parse_argv` only (2025-2079) | Agrees; no retained-data path returns 64; no receipt written; registry 1680 agrees |

No undeclared nonzero code is reachable from `main`. The generic `except Exception` at 2106-2112 maps to `internal_error` and exit 2.

## Findings

### F1 (medium-high): exit 1 is documented for expected-pin mismatch, but a could-not-evaluate verdict exits 2

Documentation says `expected_verdict_mismatch` is exit 1 (docstring 74 table; registry 1680 says only "1 failed stable finding ID", and docstring 90-93 says 1 = "the recomputed verdict does not match the expected id/exit pin").

Code path: `apply_expected` (1265-1286) only converts to exit 1 when `result["exit"] == 0` (1277). For any recomputed exit 2, it appends `expected_verdict_mismatch` as a secondary finding (1284-1285) and leaves `id`, `status`, and `exit` unchanged.

Counterexample trace: `--check --receipt R --expected E` where R is missing and E pins `{"id":"context_consistent","exit":0}`:
- `run_check` 1318-1322 raises `receipt_missing` and calls `result_from_exception(..., expected, None)`.
- `result_from_exception` 1289-1295 calls `apply_expected`.
- `matches` is False; `result["exit"]` is 2, so the 1283-1285 else branch runs and exit stays 2.
- Output: `id=receipt_missing`, `exit=2`, `status=invalid_input`, `verdict_matches_expected=false`, with `expected_verdict_mismatch` present only in `findings`.
- `main` 2099-2105 returns 2.

So the stable-ID table entry `expected_verdict_mismatch exit 1` (docstring 74) is not the exit for this emission path, and the docstring 90-93 rule "1 = ... does not match the expected pin" is contradicted for recomputed 2.

The selftest pins the code behaviour, not the docstring: `snapshot-tampered` (1906-1913) uses an expected pin `{id: context_consistent, exit: 0}` against a tampered receipt, and asserts `snapshot_tampered`/2. That agrees with registry 1680 ("tampered → 2") but contradicts the literal docstring 90-93.

Required fix (either direction): state explicitly in docstring 89-97, USAGE 266-270, and registry 1680 that a could-not-evaluate verdict outranks an expected-pin mismatch (exit 2, with `expected_verdict_mismatch` as a secondary finding), or change `apply_expected` to exit 1 and add a selftest case pinning exit 1 for it. Right now the only pinned behaviour (snapshot-tampered) sits on the other side of the documented rule.

### F2 (medium): nine stable IDs have no CLI selftest pin

Stable IDs that appear in the docstring table (58-86) and code, with zero selftest pins (zero quoted occurrences in 1728-2003):
- `environment_delta_mismatch` (exit 1): reachable only via `injected_env != INJECTED_ENV` (817-826) or `poison_path` mismatch (839-846)
- `environment_baseline_git_dir` (exit 1): 835-838
- `run_argv_mismatch` (exit 1): 853-862
- `run_cwd_mismatch` (exit 1): 863-870
- `run_env_delta_mismatch` (exit 1): 871-875
- `receipt_unreadable` (exit 2): 330-349
- `expected_unreadable` (exit 2): 1212-1214 via `read_regular`
- `internal_error` (exit 2): 2106-2112
- `tool_declaration_mismatch` (exit 1, frozen only): 1175-1179, not reachable via `--receipt` mode, so not CLI-selftestable without a frozen fixture

No selftest case mutates `runs.argv`, `runs.cwd`, `runs.env_delta`, `environment.baseline_has_GIT_DIR`, `environment.poison_path`, or `injected_env` to a non-null wrong value. The registry (1680) says "literal selftest exit/finding pairs in tool". That is true for the pairs that exist, but the lesson admit criterion (round-15.md:36-38, "public CLI selftest asserts literal exit and stable finding pairs") is only partly met for the exit-1 and exit-2 classes above.

### F3 (low-medium): `-h`/`--help` exits 0 without evaluating a receipt

`parse_argv` 2026-2027 returns `{"help": True}` for `["-h"]` or `["--help"]`. `main` 2094-2096 writes USAGE and returns 0. USAGE 266 (`exit 0   clean retained receipt`), docstring 89, and registry 1680 (`0 clean (context_consistent)`) all read 0 as a clean verdict.

Counterexample: `context-capture.py -h` returns 0 with no `CONTEXT:` line, no receipt, and no `context_consistent`. A caller that tests only the exit status (for example `context-capture.py -h && echo clean`) reads a clean verdict. The selftest does not cover `-h` (no `usage_case` or `check_case` for help).

Fix options: make help exit 64 (usage) or document that exit 0 with no CONTEXT line means help-only; the selftest should pin whichever is chosen.

### F4 (low): missing or null `injected_env` exits 1, but the registry's missing-input rule says exit 2

Registry 1665 says `Missing, unreadable, wrongly typed ... input → could not evaluate, exit2`. Code:
- `validate_environment` 520 exempts `injected_env` from the missing-key check (`allowed - {"injected_env"}`).
- `recompute_environment` 805-815 turns absent or null `injected_env` into `missing_injected_environment`, exit 1.
- Every other missing environment key (for example `baseline_policy`) raises `receipt_structure_invalid` at 523-526, exit 2.

Counterexample pair: deleting `environment.injected_env` gives exit 1 (`missing_injected_environment`, selftest 1739-1744); deleting `environment.baseline_policy` gives exit 2. Registry 1664 names this exception ("the missing-environment case keeps `missing_injected_environment`"), but the exit-class prose at 1665 and 1669-1672 has no carve-out. The lesson records it as `missing-field1` (round-14 guardrails). Behaviour is deliberate. The defect is that the prose rule and the code disagree for "missing input" without a stated exception in the classification paragraph.

### F5 (low): selftest's own exit classes are undeclared; frozen path is not exercised

- Docstring 58-97, USAGE 252-277, and registry 1680 say nothing about `--selftest` exit codes. Code: 0 on all cases pass (1725), 1 on any case failure (1723), 2 on setup error (2014), 64 on bad selftest arguments (`usage-selftest-extra`, 2002).
- Frozen mode (`--check` alone, 1299-1315) is not exercised by any selftest case; only explicit `--receipt/--expected` is. Frozen-mode behaviour (built-in pin, `tool_declaration_mismatch`) is therefore verified only by L1 runs, which the registry's "selftest green" wording does not mention.

## Bounded agreement (what matches)

- 0/1/2/64 are the only exits `main` can return. 64 comes only from `parse_argv` (2025-2079): no `UsageError` is raised after parse, and no receipt is written on 64.
- Every retained-input failure ID in the docstring (receipt_missing, receipt_unreadable, receipt_json_invalid, receipt_structure_invalid, baseline_unusable, snapshot_tampered, receipt_records_invalid_input, expected_missing, expected_unreadable, expected_invalid, internal_error) is returned at exit 2 by the code path that emits it.
- Every re-derived predicate ID (missing_injected_environment, environment_*, run_*, comparison_*, positive_control_ineffective, probe/runner_source_digest_mismatch, mapping_mismatch, receipt_verdict_mismatch, tool_declaration_mismatch) returns exit 1 through `verify_recorded_verdict`/`check_receipt` (1127, 1180).
- The registry's pinned hashes (frozen receipt sha, frozen tool sha) match the tool constants (136-142) as text.
- Routed defect 5 (round-14 spot-check line 160): context gate kind is now `gate` (SKILL 1680), exit 64 is named (SKILL 1670-1672, 1680), and a `--selftest` command is registered (SKILL 1680). The defect's classification and exit-64 requirements are satisfied in wording. F1-F3 concern whether the exit map is exact.

## Residual risk and verification gaps

- Nothing was executed. F1 and F3 are source traces; they need one L1 run each (for example `--check --receipt <missing> --expected <valid pin>` and `--help`) to confirm.
- I did not hash the frozen receipt, the negative fixture, or the historical script; the digest agreement is text-only.
- The evidence-disposition gate's exit wording (SKILL 1682 "2 and 64 ... 64 usage") was not reviewed; the shared-lattice claim (SKILL 1669-1672) is asserted for both gates without verification here.

Recommended remediation order: F1 (contract vs code), then F2 (pin the nine uncovered exit classes), then F3, F4, F5 as wording or selftest additions.
