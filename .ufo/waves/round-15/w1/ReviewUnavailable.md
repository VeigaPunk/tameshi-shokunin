# ReviewUnavailable — planned C1 vs missing receipt / missing source input (exit 2)

Lane: tameshi · Wave: tameshi-r15-w1 · Seat: TameshiR15.ReviewUnavailable (leaf reviewer, no dispatch)

## Read revision and state

- Lane HEAD read: `a9cf4da78f2514c7bedd91a850a88590009d7df0` (baseline named by `.ufo/evidence/round-15/claims.json`).
- `tools/context-capture.py` **does not exist at the read revision** (`tools/` lists bash-witness-study.py, evidence-disposition.py, mutate-and-run.sh, pin-disposition.py, repeat-control.py, witness-metadata.py). Every finding below about the promoted tool is a pre-implementation requirement or a hazard inherited from the historical source. Re-check against the implemented file before admission.
- Historical source read: `.ufo/evidence/round-14/capture-context.py` (647 lines), sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`. Its digest equals the `tool_sha256` recorded in the retained `.ufo/evidence/round-14/context-receipt.json`, so the historical bytes are unchanged since that receipt.
- Retained receipt read: `.ufo/evidence/round-14/context-receipt.json` (status ok, exit 0, reasons []). Control: `.ufo/evidence/round-14/context-missing-env.json` (sha256 `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`).
- Working tree untracked at read: `.ufo/evidence/round-15/`, `.ufo/waves/round-15/`, `corpus/lessons/round-15.md`. No tracked file was modified by this seat.
- Execution: **none**. No gate, selftest, probe, runner, or sibling was run. Reads were `read`/`grep`/`ls`/`sha256sum`, and in-memory `json.load` of two retained JSON files for field inspection. Tool installs/updates: none.

Sources consulted: `AGENTS.md`; `corpus/lessons/round-14-verifier-spotcheck.md` (Routed defects, items 1–5, lines 154–162); `corpus/lessons/round-15.md` (Gate, Admit/Reject lines 31–39); `SKILL.md` lines 1479–1607 (round-12/13/14 registries and round-14 reconciliation); `.ufo/waves/round-14/w1/VerdictContract.md` (quotes the protocol Gate standard, `PROTOCOL.md:393-419`); `corpus/knowledge/repeated-control-precondition.md` lines 36–48; `tools/evidence-disposition.py` (1–63, 1066–1081, 1927–1956); `tools/repeat-control.py` (110–117, 855–895); `tools/mutate-and-run.sh` (84–89, 542–553, 1074–1137); `.ufo/waves/round-15/spec1.json` ContextGate and ReviewUnavailable targets.

## 1. Exact acceptance criterion (what "exit 2 for missing receipt or source input" must mean)

Pin these in the promoted tool's registry row and its `--selftest`, as literal exit/ID pairs:

| Condition | Exit | ID (reuse historical IDs; stable) | Side effect allowed |
|---|---|---|---|
| Any of the four source inputs (`tools/pin-disposition.py`, `tools/mutate-and-run.sh`, `.ufo/evidence/round-13/pin-manifest.json`, `.ufo/evidence/round-13/expected.json`) absent (incl. dangling symlink) | 2 | `missing_input` | none in capture mode except the round-15 invalid receipt (see §2) |
| Source present but a directory / unreadable | 2 | `unreadable_input` | same |
| Receipt path given to check mode is absent | 2 | `receipt_missing` (new; name it) | **none** |
| Receipt present, bytes differ from a pinned sha256 | 2 | `snapshot_tampered` (matches repeat-control's ID) | none |
| Receipt present, required structure absent (see §2 F5) | 2 | `receipt_structure_invalid` (new) | none |
| Expected/manifest pin for a source is absent | 2 | `expected_pin_missing` (new) | none |
| No receipt path supplied to check mode | 64 | `invalid_usage` | none — **no implicit default to the round-14 path** |

Stable-ID alignment: the protocol names are `snapshot_tampered`, `setup_error`, `invalid_usage` (repeated-control-precondition.md:41–45). Use the same spellings in the new registry row so one exit-2 vocabulary spans both instruments.

## 2. Findings, by severity

### F1 — CRITICAL: historical exit-2 path overwrites the retained round-14 receipt

Evidence: `capture-context.py:58` hardcodes `OUTPUT_REL = ".ufo/evidence/round-14/context-receipt.json"`. `main()` (lines 614–628) on `InvalidContext` builds a receipt with `status: invalid_input, exit: 2` and calls `write_receipt()` to that same path. The success branch (629–636) does the same. So running the historical script with any missing input **replaces** the retained round-14 receipt. The docstring line 23 claims "no other path is written," which is true only for the success branch.

Acceptance: the promoted tool writes only `.ufo/evidence/round-15/…` in capture mode. Check mode writes nothing. Selftest proves round-14 bytes are untouched (fixture copies only; selftest never opens the live round-14 file). Likely false positive if not fixed: a missing-input rerun reports exit 2 "correctly," while silently destroying the evidence the round is required to preserve.

### F2 — CRITICAL: LANE_ROOT derivation depth is wrong for `tools/`

Evidence: `capture-context.py:46-47` derives `LANE_ROOT = dirname×4(SELF)`, which is correct only for `.ufo/evidence/round-14/capture-context.py`. For `tools/context-capture.py`, four `dirname`s resolve to `/home/vgpnk/Projects` (FLEET_ROOT `/home/vgpnk`). In-tree precedent for the two-level form: `tools/repeat-control.py:113-115` uses `os.path.dirname(os.path.dirname(SELF))`.

Consequences if copied verbatim: every live input is "missing" → exit 2 `missing_input` for `tools/pin-disposition.py` that is actually present (a false could-not-evaluate); and `write_receipt` would `makedirs` and write under `/home/vgpnk/Projects/.ufo/evidence/round-15/`, outside the lane.

Acceptance: `LANE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))`, or an explicit `--root` with the same meaning. Selftest asserts the resolved root equals its fixture lane and that no write lands outside temp roots.

### F3 — HIGH: uncaught exceptions exit 1, colliding with "mismatch"

Evidence:
- `main()` has no catch-all (605–643). `base_receipt()` at line 614 is **outside** the `try` (615) and calls `open(SELF)` (415) and `os.getcwd()` (420). An OSError there exits with the interpreter's unhandled-exception status, which is 1 [INFERENCE from interpreter default; not executed].
- `comparison_block` 354–356: `row.get(...)` and `row.get("pinned", {}).get(...)` on unvalidated leg rows raise `AttributeError` for a non-object leg, or a non-object `pinned`. The documented class for that input is exit 2 ("baseline not a six-leg ok pin-disposition-v1 document", docstring 28–29), but the actual code path is exit 1.
- `parse_json` (167–181) catches only `UnicodeDecodeError` and `JSONDecodeError`; deeply nested JSON raises `RecursionError` → exit 1.

Precedent in the same lane: `tools/evidence-disposition.py:1948-1952` ("fail closed, never exit 1 on an internal error") and `tools/repeat-control.py:893-894` ("never let a traceback exit 1"), plus its selftest catch-all at 861.

Acceptance: top-level `except Exception` → exit 2 with one stable ID (`setup_error` to match repeat-control, or `internal_error` to match evidence-disposition; pick one and pin it). Selftest fixture: a probe stub whose baseline `legs` contains a string row → expect **2**, not 1. Likely false positive if not fixed: a malformed probe reads as a semantic failure.

### F4 — HIGH: absent declared pins exit 1; pin mismatch classification is unsettled

Evidence: `evaluate` 496–509 uses `inputs.get(PROBE_REL)` and `derived.get("sha256")`. If either key is absent, `matches_declared` / `matches_manifest_declaration` is `False`, and `decide()` (575, 572–573) returns exit 1 "does not match its declared digest." An absent pin is an unusable expectation document, not a semantic mismatch.

Second, adjacent boundary: a source whose digest differs from its pinned value is exit 1 under historical `decide()`. The round-14 table (SKILL.md:1574) and the protocol quoted in VerdictContract.md ("an edited input is `snapshot_tampered` (could-not-evaluate), never a compared verdict") place digest drift in exit 2.

Acceptance (recommended): absent pin → 2 `expected_pin_missing`. Pinned-input digest mismatch → 2 `snapshot_tampered`. Keep exit 1 only for live behavioral mismatches (comparison, env delta, control, mapping). **Decision required by L1**: this departs from historical `decide()` on digest drift. The registry row must state whichever is chosen; the selftest must pin it.

### F5 — HIGH: a retained-receipt check that reuses `decide()` passes structurally incomplete receipts

Evidence: `decide()` (553–580) reads only: `comparison.equal`, `comparison.payload_tool_sha256_matches_disk`, `environment.env_delta_matches_declared`, `environment.baseline_has_GIT_DIR`, `positive_control.effective`, `sources.*.matches_*`, `mapping.all_match`. It never reads `environment.injected_env`, `environment.env_delta_keys`, `runs.argv_equal`, `runs.cwd_equal`, `sources.*.sha256`, or the stored `status`/`exit`.

Retained control: `context-missing-env.json` is identical to `context-receipt.json` except that `environment.injected_env` is absent. Its stored `status` is `ok`, `exit` is `0`. [Static inference: `decide()` on that file returns ok/0, because every predicate it reads is still satisfied.] The round-14 guardrail labels the same file "missing_injected_environment" with **exit 1**, a helper-only check that the lesson explicitly says does not satisfy the standalone selftest clause.

Acceptance:
- Check mode validates required structure **before** `decide()`: `environment.injected_env == {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`, `environment.env_delta_keys == ["GIT_DIR"]`, `environment.baseline_has_GIT_DIR is False`, `runs.argv_equal is True`, `runs.cwd_equal is True`, plus the `sources`/`comparison`/`positive_control`/`mapping` keys decide reads. Missing → exit 2 `receipt_structure_invalid`.
- The round-14 guardrail's expected exit 1 for `context-missing-env.json` is a helper-only expectation. Under the §1 table it becomes **2**. Pin the new value and state that the old helper check is superseded for this file. Do not edit the historical file.
- Check mode recomputes `decide()` and compares to the stored `status`/`exit`. A contradiction is a finding (recommended exit 1, `stored_verdict_mismatch`), not a silent pass.

### F6 — HIGH: no receipt input exists in the historical script; the check-mode path must be explicit

Evidence: the historical `main()` has no receipt argument; it only writes one. A check mode is new design surface.

Acceptance: explicit receipt path required (§1 row, 64 if absent); absent → 2 `receipt_missing` with no write; symlink or non-regular file → 2; non-UTF-8, invalid JSON, duplicate keys, non-object root → 2 (reuse `parse_json`'s `_no_duplicate_keys` path, which already yields `invalid_json`/`invalid_utf8`). Optional, low: the sibling `evidence-disposition.py` reads pinned inputs with `O_NOFOLLOW` and lstat/fstat identity. Adopt only if "avoid needless new frameworks" is not violated.

### F7 — MEDIUM: injected-run failure boundary contradicts its own documentation

Evidence: the docstring (26–29) and USAGE (123) say "1 mismatch (including injected run unusable)". The code: `evaluate` line 540 calls `run_bounded(... injected_env ...)` **unguarded**. Timeout, exec failure, or non-UTF-8 output raises `InvalidContext` → exit **2**. A non-zero exit or non-JSON stdout yields `comparison.error` → decide → exit **1**. The same "unusable injected observation" therefore produces 1 or 2 depending on failure type.

Acceptance: choose one rule and pin it per failure kind. Recommended: any injected run that yields no usable document → 2 (`timeout`, `exec_failed`, `non_utf8_output`, and a new `injected_run_unusable` for non-zero/non-JSON), matching the baseline-unusable rule. Fix the docstring/USAGE accordingly. If the historical 1 is kept, say so explicitly in the registry.

### F8 — MEDIUM: poison-path check is not hermetically testable under the stated write rules

Evidence: `POISON_PATH` is the fixed literal `/nonexistent/tameshi-round14-poison` (line 60–61). `evaluate` 469–472 exits 2 `poison_path_exists` if it exists. Positive-testing that class requires creating a path outside temp roots, which the integration interface forbids.

Acceptance: either parameterize the poison path for selftest only (a fixed test-only constant, with the production value unchanged), or record `poison_path_exists` as **not selftested** in the registry row. Do not claim it is covered.

### F9 — MEDIUM: selftest happy-path fixture has non-obvious prerequisites; a naive fixture yields a false mismatch

- Positive control runs `git -C LANE_ROOT rev-parse --git-dir` (402) and requires baseline exit 0 with non-empty stdout (403). A fixture lane that is not a git repository yields `baseline_ok=False` → `effective=False` → **exit 1**, misreported as a mismatch. The fixture must `git init`.
- The real probe needs fleet sibling repos under `--root`. A fixture without them makes baseline unusable → exit 2 `probe_baseline_unusable`, which mimics a missing sibling. The happy-path selftest should use a stub probe whose stdout is a six-leg `pin-disposition-v1` document with correct `tool_sha256` (= the stub's sha) and a varying `observed_at` (excluded). [INFERENCE: real-probe feasibility in fixtures not measured.]
- `expected.json` `inputs` must pin the stub probe digest; `pin-manifest.json` `derived_from.sha256` must equal the fixture runner digest; the runner fixture must contain six header rows, six `PIN_`/`REV_` constants, and six `regression_case_git` calls matching the manifest.

### F10 — LOW (static only): runner grammar dependency

Static check, not executed: the runner's six header rows (`tools/mutate-and-run.sh:84-89`) match `HEADER_ROW_RE` shape; six `PIN_`/`REV_` constants (542–553) match `PIN_CONST_RE`/`REV_CONST_RE`; the six calls in `run_regression` (1112–1137) match `CALL_RE`'s `leg 'path' "$PIN_X" "$REV_X" "…" '…' "$TABLE_X"` shape. A future runner edit that changes this shape yields `runner_unparsed` → exit 2. That is correct could-not-evaluate behavior, but it should be called out as a maintenance coupling in the registry row.

## 3. Likely false positives to guard against

1. **`tool_sha256` of the retained receipt ≠ the new tool's digest.** The round-14 receipt was produced by the historical script; comparing to the new tool's bytes would falsely mismatch. Do not check it.
2. **`lane_root`/`fleet_root`/`invocation.argv` equality.** They are absolute or machine-specific. A check that compares them to the current checkout falsely fails on any other path.
3. **`observed_at`.** Excluded by design. Also: **do not require `comparison.raw_stdout_equal` to be true.** It includes the top-level `observed_at`, so two runs straddling a second boundary yield `false` while `equal` remains `true`. It is informational only.
4. **Digest drift of live sources in check mode.** Check mode must verify the retained receipt against its own pins; re-reading live sources in check mode falsely fails when any unrelated repo file moves. Live source comparison belongs to capture mode only.
5. **Missing `git` / `python3`** on PATH → exit 2 is correct; do not map to 1.
6. **Runner grammar drift** → exit 2 is correct, but do not read it as a probe failure.

## 4. Unearned claims to reject

1. "Exit 0 on the retained receipt proves the historical GIT_DIR injection was the historical setup." Reject: the lesson (round-14 item 1, line 156) says historical setup stays unproven.
2. "Exit 2 on missing inputs proves the sources are intact" or "exit 0 proves no drift." Reject: exit 2 means could-not-evaluate; exit 0 covers only the recorded predicates and pins.
3. "Selftest exit 0 proves environment independence, source authentication, or safe result reuse." Reject: `result_reuse` is `not_established` in the receipt (`context-receipt.json`), and the not-compared list names leg execution, suite/dependency identity, and sibling movement.
4. "Helper-only guardrails (`context_setup_positive`, `context_setup_missing_field`, `runner_variable_swap_discriminator`) satisfy the standalone self-invocation clause." Reject: lesson line 161 says they do not.
5. "A digest pin means authenticated authorship." Reject: SKILL.md:1604–1605 calls it configured authority only.
6. "The promoted gate re-verifies round 14, or changes round-14's verdict." Reject: check mode reads one retained receipt's predicates; it does not rerun probe/runner.
7. "Registry exit 2 covers every failure class." Reject without the F3 catch-all and the F4/F7 decisions pinned.
8. "A green selftest covers all finding IDs." Reject: the lesson says not every emitted ID needs its own fixture, but the registry must list which IDs are selftested and which (e.g., `poison_path_exists`, F8) are not.

## 5. Recommended bounded actions for the executor (L1 runs checks once, after seats return)

1. Promote `tools/context-capture.py` with `LANE_ROOT` = two `dirname`s (F2); `OUTPUT_REL` = round-15 only (F1); top-level catch-all → 2 (F3).
2. Implement the §1 table; reuse historical IDs (`missing_input`, `unreadable_input`, `invalid_json`, `invalid_utf8`, `duplicate_key`, `invalid_manifest`, `invalid_expected`, `runner_unparsed`, `probe_baseline_unusable`, `poison_path_exists`, `invalid_fleet_root`, `missing_executable`, `timeout`, `exec_failed`, `non_utf8_output`) plus the new ones named above.
3. Decide and pin: F4 (digest drift → 2 vs 1), F7 (injected unusable rule), F8 (poison-path testing). L1 must record each decision in the registry row.
4. Check mode: explicit path, structure validation before `decide()` (F5), no default path (F6), no writes.
5. Selftest (F9 fixtures, all under temp roots, literal exit + ID pairs). Minimum cases:
   - clean capture → 0 `context_clean` (git-init fixture, stub probe)
   - each of 4 sources missing → 2 `missing_input`
   - receipt path absent (check) → 2 `receipt_missing`, no file created
   - receipt digest pinned and differs → 2 `snapshot_tampered`
   - `environment.injected_env` absent (check) → 2 `receipt_structure_invalid`
   - expected pin key absent → 2 `expected_pin_missing`
   - probe baseline with string leg row → 2 (not 1) — F3 catch-all
   - probe baseline non-JSON → 2 `probe_baseline_unusable`
   - injected probe observation differs → 1 mismatch
   - stored status contradicts recomputation → 1 `stored_verdict_mismatch`
   - unknown argument, or `--selftest` with other args → 64 `invalid_usage`
   - round-14 bytes unchanged after selftest (fixture-only)
6. Registry row (SKILL.md, not edited by this seat): name, `gate`, entry command, exit map 0/1/2/64 with each class named, `--selftest` spelling, pinned values (round-13 pin manifest, expected.json digests, runner/probe digests), write scope = round-15 receipt only in capture mode, owner tameshi. Supersede the round-14 "probe / no standalone selftest" row explicitly rather than erasing it (round-15 lesson lines 45–46).
7. Verdict revision: the new capture receipt should record the lane HEAD it was measured against (PROTOCOL.md:406–407 per VerdictContract.md). The historical receipt does not record it; do not require it on the retained round-14 receipt.

## 6. Residual risk and verification gaps

- No file was executed. Every behavioral claim above is static reading of `capture-context.py` and the retained JSON; labelled [INFERENCE] where it depends on interpreter behavior or on fixture feasibility.
- Not inspected: any implemented `tools/context-capture.py` (absent at HEAD a9cf4da); the actual probe's behavior under fixtures; sibling reports under `.ufo/waves/round-15/w1/` written by other seats (not read, to keep this review independent).
- Round-14 `guardrails.json` expects exit 1 for `context-missing-env.json`; the new classification (2) conflicts with it. This is a deliberate reclassification that L1 must pin, not a regression to hide.
- Historical `-h`/`--help` exits 0 and writes nothing; any other argument exits 64 before writes. `--selftest` passed to the historical script therefore exits 64 without writing. This satisfies the round-15 "old unsupported invocation" distinction by reading only, not by execution.

## Blocking items for the executor

None that prevent starting work. F1 and F2 must be addressed in the first implementation pass; the rest are pins to decide and encode.
