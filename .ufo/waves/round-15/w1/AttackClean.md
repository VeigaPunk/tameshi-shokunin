# AttackClean — critic, round15 w1

Target: falsify planned C1 on the **clean retained-receipt exit0 + stable ID** case. Show how a counterexample gets past a test that only checks the helper, and require exit/finding semantics from the real CLI.
Mode: read-only source/data inspection. **No gate, selftest, capture or decide() was executed.** Every predicted exit below is `[INFERENCE]` from static reading of `.ufo/evidence/round-14/capture-context.py` (sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, 647 lines). The only commands run were `sha256sum`, `diff` over `json.tool --sort-keys`, and `json.load` field reads of the retained receipts. Tool installs/updates: none.

## Primary counterexample (required routed fix)

**The retained negative fixture is classified clean by the historical decide().**

Evidence (observed):

- `diff <(json.tool --sort-keys context-receipt.json) <(json.tool --sort-keys context-missing-env.json)` shows that the **only** difference is the removal of `environment.injected_env = {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`.
- Both files keep the same stored values: `status "ok"`, `exit 0`, `reasons []`, `environment.env_delta_matches_declared true`, `environment.baseline_has_GIT_DIR false`, `comparison.equal true`, `positive_control.effective true`, `mapping.all_match true`, and the same `tool_sha256 7313e9a2…`.
- File digests: clean `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`; missing-env `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`.
- Round14 `guardrails.json` check `context_setup_missing_field` pins exit **1** and stdout `missing_injected_environment` for `context-missing-env.json`. That verdict came from an inline `python3 -c` helper, not from the tool.
- `decide()` (lines 553–580) reads only these values: `comparison.equal`, `comparison.payload_tool_sha256_matches_disk`, `environment.env_delta_matches_declared`, `environment.baseline_has_GIT_DIR`, `positive_control.effective`, `sources.probe.matches_declared`, `sources.runner.matches_manifest_declaration` and `mapping.all_match`. It never reads `injected_env`.

`[INFERENCE]`: `decide(json.load(context-missing-env.json))` returns `("ok", 0, [])`.

Suppose the promoted `--check RECEIPT` reuses `decide()` on the retained JSON as-is, which is what the integration interface asks for ("reuse decide/comparison/mapping semantics"). Then:

| Fixture | Nominal helper test | Actual CLI (naive reuse) | Required literal pair |
|---|---|---|---|
| `context-receipt.json` | `decide()` → ok/0 ✔ | exit0 ✔ | exit0, clean ID |
| `context-missing-env.json` | not exercised (selftest only feeds `decide()` the live-built dicts, so `injected_env` and `env_delta_matches_declared` always agree) | **exit0 clean** ✘ | exit1, `missing_injected_environment` (round14 precedent) |

A test of the clean case alone cannot reveal this, because both receipts produce exit0. **A clean exit0 counts as evidence only if a sibling fixture, one bounded mutation away, fails with its literal ID through the same CLI subprocess.** This is the same failure as round13 producer_before: the exit agreed, but the intended assertion was never evaluated.

The `tool_sha256` binding does not separate these two files either. Both carry `7313e9a2…`, yet `context-missing-env.json` was hand-derived in commit `4d409d7`, not emitted by the tool. A receipt's own `tool_sha256` is a claim the receipt makes about itself, not proof that the tool produced it.

## Secondary counterexamples (same root: the stored derived booleans are trusted)

1. **Truthy rather than strict checks (required).** `decide()` uses `is not True` / `is not False` for comparison and environment, but plain truthiness for `sources.probe.matches_declared`, `sources.runner.matches_manifest_declaration` and `mapping.all_match`. Live receipts always hold real bools, so live tests never reach this. A retained JSON with `"matches_declared": "false"`, `"all_match": 1` or `"all_match": "no"` → `[INFERENCE]` ok/0.
2. **Derived booleans contradict the raw fields (required).** Any of these would give `[INFERENCE]` ok/0 under decide-only checking:
   - `comparison.equal true` while `runs.baseline.stdout` and `runs.injected.stdout` canonicalize differently;
   - `positive_control.effective true` with `injected.exit 0`;
   - `sources.probe.sha256 != declared_sha256` while `matches_declared true`;
   - `mapping.all_match true` while some `legs[].checks` value is `false`.
3. **Duplicate keys (required in check mode).** A JSON object such as `{"equal": false, …, "equal": true}` is accepted by plain `json.load` (last value wins). Check mode must load through the existing `parse_json` / `_no_duplicate_keys` path. Expected result: exit2 `invalid_json`.
4. **Stored verdict fields (required).** If `--check` echoes the retained `status`/`exit`/`reasons`, both files report ok/0. Like `tools/evidence-disposition.py:61` ("Receipt `expected_exit`/`exit_matches` fields are never trusted"), the stored values must be recomputed. A mismatch between stored and recomputed values must itself be a finding.
5. **Path and depth errors when promoting to tools/ (required).** Historical `LANE_ROOT` is 4×`dirname(SELF)`. Copied to `tools/context-capture.py`, that gives `[INFERENCE]` `LANE_ROOT=/home/vgpnk/Projects` and `FLEET_ROOT=/home/vgpnk`. The probe input reads would then fail with exit2 `missing_input`, but `main()` writes the receipt even on `InvalidContext`. It would land at `/home/vgpnk/Projects/.ufo/evidence/round-14/context-receipt.json`: outside the lane, and at a round14 path. `OUTPUT_REL` is also hard-coded to round-14. Only a public CLI subprocess run against an isolated root can see this; a helper-only test cannot.
6. **Vacuous or misrouted clean result (required test shape).**
   - Historical `-h`/`--help` returns exit0.
   - The existing `case()` pattern (`evidence-disposition.py:1571`) checks `payload.get("findings", []) == []`. An empty expected-ID list is therefore satisfied by any exit0 JSON that has no `findings` key.
   - A check mode that ignores its argument and reads the default live round14 receipt also yields exit0 on a synthetic clean fixture, because it checked the live bytes. That is a hidden live read.

## Smallest safe correction (bounded)

### Required (routed fixes; C1 should not admit without them)

R1. Do not apply `decide()` to the stored booleans. Check mode first **re-derives** them from the raw retained fields, then calls the shared `decide()` on the re-derived values. At minimum:
- `injected_env == {"GIT_DIR": POISON_PATH}`;
- `env_delta_keys == ["GIT_DIR"]`;
- `baseline_has_GIT_DIR is False`;
- `runs.argv_equal` / `cwd_equal` recomputed from `runs.baseline` and `runs.injected`;
- the canonical comparable sha256 recomputed from both `runs.*.stdout` minus top-level `observed_at`, which must equal both stored `*_comparable_sha256` values;
- `positive_control` recomputed from the stored `baseline`/`injected` exits and output;
- `sources.*.sha256 == declared` recomputed as strings;
- `mapping.all_match == (six legs ∧ every legs[].checks value is True ∧ leg_set_equal ∧ leg_order_equal)`.

Each disagreement emits a distinct stable ID. The missing `injected_env` case keeps the round14 literal pair **exit1 `missing_injected_environment`**.

R2. Use strict types everywhere: `is True` / `is False`, and the expected `str`, `list` and `dict` shapes. Wrong type, missing required container, duplicate key or non-UTF-8 → exit **2** (could-not-evaluate) with a stable kind. Exit 1 is reserved for well-formed receipts whose recomputed facts disagree.

R3. Never trust the stored `status`/`exit`/`reasons`/`tool_sha256`. A stored-versus-recomputed exit disagreement is a finding. `tool_sha256` is compared to the pinned historical digest `7313e9a2…` and reported as a declaration, not as authentication.

R4. Promotion paths:
- `LANE_ROOT` is computed for `tools/` (2×dirname) or taken from an explicit `--root`.
- Capture output goes to round15 only.
- Check mode writes nothing.
- On exit2, capture mode must not write outside `--root`.

R5. The selftest invokes the real CLI by subprocess (`sys.executable SELF --check …`) under `mkdtemp` with `--root` in the temp dir. It pins literal pairs, **including a positive clean ID** rather than an empty list:

| Case | Fixture | Exit | Stable ID(s) |
|---|---|---|---|
| clean | synthetic copy of the clean receipt shape | 0 | positive clean ID (e.g. `context_receipt_consistent`), with the input sha256 echoed equal to the fixture bytes |
| missing-env | clean minus `environment.injected_env` | 1 | `missing_injected_environment` |
| truthy-string | `mapping.all_match: "false"` | 2 | type kind |
| contradicted-equal | `comparison.equal true`, `runs.injected.stdout` differs | 1 | comparison ID |
| stored-exit-lie | stored `exit 0`, recomputed failure | 1 | stored-exit ID |
| duplicate key | duplicate `equal` | 2 | `invalid_json` |
| usage | extra or unknown argv | 64 | usage |

In the clean case, `findings` must be present and of type `list` before it is compared, and stdout must carry the clean ID. This rules out acceptance through `--help` or a missing `findings` key. The clean and missing-env fixtures must sit in the same temp dir and give different exits, which shows the argument was actually read.

Live retained-receipt pairs for L1 to run once (non-selftest, read-only, no write) — `[INFERENCE]` expectations, not executed:
- `--check .ufo/evidence/round-14/context-receipt.json` → exit0, clean ID, input sha `05cb55b8…`
- `--check .ufo/evidence/round-14/context-missing-env.json` → exit1 `missing_injected_environment`, input sha `1ee9d09b…`

### Optional hardening (not admission-blocking)

- Run the selftest under env poisoning (`GIT_DIR=/nonexistent`, a cwd outside the lane), following SKILL.md:71's outside-hermeticity pattern.
- In snapshot mode, pin the receipt-file sha256 values above in a committed manifest. Re-derivation (R1) is the actual safeguard; the pin only adds integrity.
- Rehash `sources.*.path` against the disk in live check mode, labelled as a live read. Keep it out of the selftest.
- Make the clean ID independent of `observed_at` and absolute paths so it stays stable.

## Impacted axes

- **calibration:** affected. A clean exit0 without R1–R3 would replace the round14 negative guardrail with a contradicting tool verdict. That is false provenance and premature saturation.
- **operability:** at risk from R4, which would write outside the lane.
- **depth, coverage, freshness, adjacency:** unaffected.

Scalar is unchanged in either case. Without R1/R2/R5, the clean-exit0 claim gives no discriminating evidence and should be rejected as written.
