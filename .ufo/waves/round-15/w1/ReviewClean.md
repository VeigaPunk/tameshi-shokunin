# Round 15 — ReviewClean (C1 clean retained receipt, exit 0, stable ID)

Seat: TameshiR15.ReviewClean (reviewer, leaf). Read-only. No gate, selftest, build, or receipt command was executed. No sibling tree was read beyond the lane and fleet metadata listed below.

## Read revision and state

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, branch `master`, commit `a9cf4da78f2514c7bedd91a850a88590009d7df0` (from `.git/refs/heads/master`; working-tree cleanliness not read).
- `tools/context-capture.py` does **not** exist at this read. `tools/` holds only `evidence-disposition.py`, `pin-disposition.py`, `witness-metadata.py`, `bash-witness-study.py`, `repeat-control.py`, `mutate-and-run.sh`. The clean-check design below is therefore a review of the planned contract, not of implemented source.
- Historical source read in full: `.ufo/evidence/round-14/capture-context.py` (647 lines; `VERSION` r14). Its on-disk digest was **not** computed, so the `tool_sha256` value `7313e9a2…7fe89` recorded in the retained receipts is unverified against bytes.
- Retained clean evidence read: `.ufo/evidence/round-14/context-receipt.json` (status ok, exit 0, reasons []) and `.ufo/evidence/round-14/context-missing-env.json` (status ok, exit 0, reasons []; derived control with `injected_env` removed).
- Routed defect 5 read in full: `corpus/lessons/round-14-verifier-spotcheck.md:160`.
- Registry context: `SKILL.md:1601-1602` (round-14 row: "no standalone selftest", verdict map has no exit 64). Precedents for exit 64 in the same registry: `SKILL.md:1503-1504` (repeat-control, bash-witness: "64 usage/could-not-evaluate"), `SKILL.md:1553` (witness-metadata: "2 … including usage"), `SKILL.md:1601` (evidence-disposition: "64 usage").
- The "§Gate standard" the lesson cites was **not located** in lane docs (`SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `tools`, `corpus`, `.ufo/reports`, `.ufo/continuation`), nor in `~/Projects/ufo-fsd-alpha/skills/ufo`. Do not cite it as an authority; criteria below rest on the lesson's own characterization and on the registry columns.

## 1. Exact acceptance criterion for the clean path

A retained-receipt check run on a receipt file `R` with a pinned digest `D` must exit **0** and print one stable clean ID **only if all of the following hold**. Any single failure is a finding, not a silent pass.

1. **Pinned bytes.** `sha256(bytes of R) == D`, where `D` is a literal digest supplied by the caller or pinned in the tool. It must be computed from committed bytes at the merge revision (L1 action; not computed here).
2. **Parse.** UTF-8 JSON object, no duplicate keys (the historical `_no_duplicate_keys` hook must be kept), root is an object.
3. **Schema and tool identity.** `schema` equals the schema of its round (`tameshi-round14-context-receipt-v1` for round-14 files). `tool_sha256` equals the pinned digest of the tool that produced it. For round-14 this is the historical script digest, not the new tool digest.
4. **Status and exit, strict types.** `status == "ok"`, `type(exit) is int and exit == 0`, `reasons == []`.
5. **Decide predicates, strict.** Re-derive `decide(receipt)` on the stored dict and require `("ok", 0, [])`, with every predicate compared by `is True` / `is False`, not truthiness (see FP-2).
6. **Structural predicates that `decide()` does not check (required additions).**
   - `environment.injected_env == {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}` exactly.
   - `environment.env_delta_keys == ["GIT_DIR"]`.
   - `environment.baseline_has_GIT_DIR is False`.
   - `comparison.error is None` and `comparison.equal is True`.
   - `positive_control.effective is True`.
   - `mapping.all_match is True` and `len(mapping.legs) == 6`.
7. **Output.** Exactly one line that names the clean ID, for example `CTX-CHECK-CLEAN` (proposed literal; L1 fixes the final string and pins it in selftest). Exit 0.

Exit-code classes for this check (recommended, to match the lattice in `SKILL.md:63`): 0 clean (all of 1–7); 1 retained receipt fails a predicate in 2–6 (one stable ID per predicate); 2 could-not-evaluate (file missing, digest unreadable, non-UTF-8, invalid JSON, schema unknown, `status` not in {ok, mismatch}, `status == invalid_input`); 64 usage (bad argument, no output file written).

Note: a receipt whose own `status` is `invalid_input` must exit 2 (could-not-evaluate), not 1, not 0.

## 2. Verified outcomes on retained inputs (static reasoning, not executed)

- `context-receipt.json`: satisfies 1–7 provided the digests in 1 and 3 are pinned to the bytes read at merge. Expected CLEAN.
- `context-missing-env.json`: passes steps 4–5 and fails step 6 (no `injected_env` key, lines 14–26 of the file; `decide()` never reads `injected_env`). **Must exit 1** with a predicate ID such as `CTX-STRUCT-INJECTED-ENV`. Its own guardrail (`guardrails.json`, check `context_setup_missing_field`) expects `missing_injected_environment`, which is exactly this result. A decide-only check would call it clean.

## 3. Likely false positives (reject)

**FP-1 — decide-only clean on `context-missing-env.json`.** `decide()` (capture-context.py:553–580) reads only the stored booleans `environment.env_delta_matches_declared` and `baseline_has_GIT_DIR`. It never checks the injected value. The derived file has every predicate true (`comparison.equal` line 109, `positive_control.effective` 148, `mapping.all_match` 408, `status`/`exit` 418–419) and no `injected_env`. Reject any clean criterion satisfied by `decide()` alone. Step 6 is required.

**FP-2 — truthiness in `decide()`.** Three predicates use truthiness: `if not mapping.get("all_match")`, `if not (sources.get("probe") or {}).get("matches_declared")`, and `if not (sources.get("runner") or {}).get("matches_manifest_declaration")`. A retained receipt with `"all_match": "yes"` or `1` passes as clean. Reject reuse without changing these to `is True`. Changing them does not alter any real round-14 outcome, because those fields are real bools there.

**FP-3 — bool-as-int exit.** `exit == 0` accepts `false` (and `0.0`). Use `type(x) is int`. The same applies to any exit in the stored `runs` and `positive_control` blocks if re-checked.

**FP-4 — wrong root at the new path (implementation-critical).** The historical script derives `LANE_ROOT` as `dirname` four times from its own path (capture-context.py:46). That is correct at `.ufo/evidence/round-14/` but at `tools/context-capture.py` it resolves to `/home/vgpnk/Projects`, and `FLEET_ROOT` to `/home/vgpnk`. Every normal capture would then fail `missing_input` for `tools/pin-disposition.py` (exit 2), and the git positive control would run in the wrong directory. The new file needs two `dirname` calls, or an explicit `--root`. The selftest must assert the derived root equals its fixture.

**FP-5 — digest pinned to the wrong tool.** Retained round-14 receipts carry `tool_sha256 = 7313e9a2…` (the historical script). A check that requires `tool_sha256 == sha256(tools/context-capture.py)` will falsely mismatch every round-14 receipt. Pin per receipt, not per the live tool. (Also not verified: whether the on-disk historical script still hashes to `7313e9a2…`.)

**FP-6 — stable ID derived from free-text reasons.** Historical reasons embed leg names, error strings and exit codes (`"injected observation differs … {error}"`, `"leg {}: {}"`, `"runner mapping …"`). Mapping by string prefix or substring is unstable. Assign IDs by predicate key (the same keys as `CHECKS` and the `decide()` branches), and emit the free text only as detail.

**FP-7 — overwrite of round-14 evidence.** Historical `write_receipt()` uses unconditional `os.replace` to `OUTPUT_REL = .ufo/evidence/round-14/context-receipt.json` and runs on exit 0, 1 and 2. Running the archived script would overwrite the retained receipt. The registry must mark it archived, and the new tool must default to round-15 and refuse an existing target (`O_EXCL` or pre-check). A clean-check run must never write.

**FP-8 — selftest that reads the real lane.** Historical `main()` takes no fixture root; all inputs are lane-fixed. A selftest that uses the default root is a live read and violates the contract. A `--root` override is needed, and fixtures must stub `tools/pin-disposition.py` (the probe reads six sibling repos at pinned commits, which a hermetic fixture cannot reproduce). The stub makes the selftest a test of the wrapper, not of the probe. State that in the registry.

## 4. Unearned claims to reject

- **UC-1: "clean receipt shows the context is hermetic or environment-independent."** The receipt records one `GIT_DIR` injection and `result_reuse: not_established`, and its `not_compared` list names leg execution, suite environment and dependencies, and sibling movement. Stryker and PIT limitations (S003, S041–S048) say the same. Reject.
- **UC-2: "the retained-receipt check re-verifies the live environment or probe output."** It re-derives predicates from stored fields only. It runs no probe and checks no live state. Its clean ID must say "retained receipt self-consistent".
- **UC-3: "`guardrails.json` satisfies the standalone-selftest clause."** Routed defect 5 says the helper-only controls do not. Reject.
- **UC-4: "the round-14 receipt now carries a stable finding ID."** Historical bytes have none. The ID is assigned by the new check's output, not written into the receipt.
- **UC-5: "exit 64 means could-not-evaluate of evidence."** Exit 64 is a usage refusal that writes no receipt. The registry precedents disagree (`SKILL.md:1504` "64 usage/could-not-evaluate"; `SKILL.md:1601` "64 usage"; `SKILL.md:1553` puts usage under 2). Recommended exact wording: "64 usage — no receipt written; no verdict; reported at gate level as could-not-evaluate", matching the one precedent that names both. L1 must pick one and use it identically in the tool, selftest and `SKILL.md`.
- **UC-6: "C1 scalar moves."** Scalar stays 6; C1 is the lowest tied axis, and this check is calibration evidence only.
- **UC-7: "selftest passes / gate verified."** Nothing here was executed. Only L1's post-seat run can support those words.

## 5. Implementation-critical details for the implementer

1. Two-level root derivation (FP-4), or explicit `--root`, with a selftest assertion that the derived root equals the fixture.
2. `decide()` predicates compared with `is True` (FP-2); reuse the function, do not copy it.
3. Structural checks in step 6, computed from the stored dict only (FP-1).
4. Predicate-keyed stable IDs; reasons remain detail text (FP-6).
5. Round-scoped output path, refusal to overwrite, and a check mode that never writes (FP-7).
6. Historical `tool_sha256` pinned per receipt; new tool digest pinned only for round-15 receipts (FP-5).
7. Selftest: isolated temp root with `git init`, stub `tools/pin-disposition.py` and synthetic six-leg runner/manifest/expected; literal expected exit and ID pairs. Minimum cases: clean → 0; missing `injected_env` → 1; `all_match: "yes"` → 1; `exit: false` → 1; missing input → 2; `status: invalid_input` → 2; unknown argument → 64.
8. Keep the poison constant `/nonexistent/tameshi-round14-poison` unchanged, since the retained receipts depend on it.

## 6. Residual risk and verification gaps

- Not executed: any gate, selftest, receipt check or probe. Not verified: historical script digest, retained-receipt digests, working-tree cleanliness.
- Unlocated: the "§Gate standard" text. If it differs from the lesson's characterization, the gate-classification finding needs re-review.
- Unknown: whether the stub-probe selftest satisfies the lesson's "isolated standalone self-invocation" wording. L1 decides.
- The ID strings in this report are proposals; they are not authoritative until the implementer fixes and pins them.

## Tooling

No installs or updates performed by this seat. Reads only.
