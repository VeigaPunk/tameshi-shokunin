# TameshiR15.ReviewTimestamp — C1 `observed_at` volatile exclusion review (round 15, w1)

Scope: only the top-level `observed_at` exclusion inside planned C1. Out of scope: scalar, registry text, exit-64 mapping (except where it touches the exclusion), other probe fields, sibling lanes.
Execution: none. No gate, selftest, probe, or context harness was run. Reads only: `read`, `grep`, `sha256sum`, `python3` JSON parsing of spec text, read-only `git rev-parse`/`status`.

## 0. Read revision

- Lane HEAD: `a9cf4da78f2514c7bedd91a850a88590009d7df0`.
- `tools/context-capture.py`: **absent at read time**. Findings about it are design-level and conditional on promotion.
- Historical `.ufo/evidence/round-14/capture-context.py`: sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, equal to the retained receipt's `tool_sha256`.
- `tools/pin-disposition.py`: sha256 `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11` (equal to the receipt's declared probe digest).
- `tools/mutate-and-run.sh`: sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`.
- `.ufo/evidence/round-13/pin-manifest.json`: sha256 `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6` (equal to the receipt's `sources.manifest`).
- Other dirty paths belong to peers and were not read or relied on: `M corpus/QUALITY.md`, `M corpus/SOURCES.md`, `?? corpus/lessons/round-15.md`.

## 1. Observable behavior (source and retained evidence)

Probe, `tools/pin-disposition.py`:
- L578: the only clock read in the probe. `payload["observed_at"]` is set in `run_mode` (L565–589) after all legs are evaluated (L573). It is an end-of-read-window stamp at one-second resolution (`%Y-%m-%dT%H:%M:%SZ`).
- No other time-derived output. `os.stat` uses (L248–389) read only mode, device, and inode. Grep for `mtime|ctime|atime|getmtime|time.time|monotonic` returns nothing.
- `invalid_input` documents (L184–194) carry no `observed_at`.
- `observed_at` appears only at top level.

Historical comparison, `.ufo/evidence/round-14/capture-context.py`:
- L350–392 `comparison_block`.
  - L352–361: baseline must parse as a six-leg `ok` `pin-disposition-v1` document with `observed_at` present and every leg verified and not unavailable. Otherwise `InvalidContext("probe_baseline_unusable")`, which is exit 2.
  - L364 `"exclusions": ["observed_at"]`; L365 normalization string.
  - L376–379: injected `observed_at` is recorded. If absent, `error` is set and the function returns (no raise), which later yields exit 1.
  - L384–386: `dict(base)` / `dict(injected)` shallow copies, then `pop("observed_at")`. Top level only.
  - L387–391: `json.dumps(sort_keys=True, separators=(",", ":"))`, then text equality → `equal`.
  - L367 `raw_stdout_equal` is recorded but is **not** an input to `equal` or to `decide`.
- L340–347 `parse_probe_document` returns None whenever `exit != 0`. An injected run that exits 2 with a valid `invalid_input` JSON is therefore reported as "produced no JSON document (exit=2)". The diagnostic is inaccurate; the exit is not affected.
- L553–580 `decide`: only `comparison.equal is not True` contributes the reason `"injected observation differs from baseline after excluding observed_at: {error or 'normalized JSON mismatch'}"`. This is free text with no stable ID; only the prefix and the two fixed suffixes are literal.
- L414–436 `base_receipt`: receipt top-level `observed_at` is taken at L419 **before** `evaluate` runs the probes. It is a start instant, not the probe's end-of-window instant. It is never compared.
- Exit map (L26–29, L605–643): 0 ok, 1 mismatch, 2 could-not-evaluate / invalid input, 64 usage. Exit 64 is not part of this review.

Retained evidence, `.ufo/evidence/round-14/context-receipt.json`:
- L5: receipt `observed_at` `2026-10-20T06:35:01Z`.
- L100–107: `exclusions` `["observed_at"]`; `observed_at.baseline` and `observed_at.injected` both `2026-10-20T06:35:01Z`.
- L108–112: `raw_stdout_equal: true`; both comparable SHA-256 `22e79150fb56beb74902b1c9056e930db9bd76321488a39e7e82f3bc1d1261f9`; `payload_tool_sha256_matches_disk: true`; `equal: true`.
- `.ufo/evidence/round-14/context-missing-env.json` shows the same `06:35:01Z` pair.

Lesson, `corpus/lessons/round-14-verifier-spotcheck.md`:
- L104 says "equal raw stdout including timestamp" and "Only top-level observed_at is excluded".
- L127 already rejects "infer broad environment independence … from one GIT_DIR injection".
- L160 is routed defect 5: register as gate, standalone isolated self-invocation with literal exits and stable IDs, map exit 64.

## 2. Observable versus inferred

Observable (source or retained bytes):
- One clock-derived key in the probe output; the comparison removes exactly that key at top level and compares the rest canonically.
- One retained pair of runs compared equal. Both observed-at values fall in the same UTC second.

Inferred (not observed here, not executed):
- That no other probe field can differ between two runs at a fixed root. Sibling-state fields (`head.commit`, `worktree.sha256`, `status`, `counts`) are derived from live repos. `.ufo/waves/round-14/w1/EnvSentinel.md:51` (ES-8) records sibling HEAD moving between legs as a genuine mismatch source.
- That the retained pair was produced back-to-back with no sibling motion. Not verified.

## 3. Exact acceptance criterion (for the planned tool)

A1. Two probe documents that differ only in top-level `observed_at` → `comparison.equal == true`, `comparison.exclusions == ["observed_at"]`, and no reason beginning `injected observation differs` is emitted.
A2. Documents differing in any other key, including nested keys → `comparison.equal == false` and reason exactly `injected observation differs from baseline after excluding observed_at: normalized JSON mismatch`.
A3. A nested key named `observed_at` that differs must still be a mismatch. This is the strictness boundary; it is recommended, not required, and it is the thing a regex-based strip would violate.
A4. Injected document lacks top-level `observed_at` while baseline has it → `equal == false`, error `injected document has no top-level observed_at`, exit 1. Baseline lacks it → exit 2 with `error.kind == "probe_baseline_unusable"`. The asymmetry is existing behavior; pin both, do not "fix" it silently.
A5. `raw_stdout_equal` is informational only. It must not be asserted by the selftest and must not feed `decide`.

## 4. Isolated fixture recipe (public CLI, temp roots only)

Pre-condition: the promoted tool must derive `LANE_ROOT` from two `dirname` calls on `realpath(__file__)` (`tools/context-capture.py` → lane root). See FP-1.

One fresh temp tree per case, under `tempfile.mkdtemp()`:
1. `fleet/tameshi-shokunin/tools/context-capture.py` = promoted tool. `fleet/` is `FLEET_ROOT`.
2. `tools/pin-disposition.py` = fixture stub that prints a six-leg `ok` `pin-disposition-v1` document with `tool_sha256` read from a sidecar file the fixture writes after hashing the stub. Stub emits `observed_at` = `T1` when `GIT_DIR` is absent (baseline) and `T2` when present (injected). Per-case mutation is in the stub text: `positive` (identical otherwise), `nonobserved` (injected changes `counts.legs`), `missing_injected_observed_at`, `missing_baseline_observed_at`.
3. `.ufo/evidence/round-13/pin-manifest.json`: `schema: pin-manifest-v1`, six legs with names matching `EXPECTED_SUFFIX` keys, 40-hex `pinned_commit`, 64-hex `expected_sha256`, and `derived_from: {path: "tools/mutate-and-run.sh", sha256: <fixture runner digest>}`.
4. `tools/mutate-and-run.sh`: synthetic runner that satisfies `parse_runner_mapping` exactly: six `#   <leg> <repo>/<path> n/n (p%)` header rows; six `PIN_<SUFFIX>=` and `REV_<SUFFIX>=` constants with values equal to manifest `expected_sha256` and `pinned_commit`; `run_regression()` body with six `regression_case_git <leg> '<repo>/<path>' "$PIN_<SUFFIX>" "$REV_<SUFFIX>" ... "$TABLE_<SUFFIX>"` calls, where `leg`, `path`, and the three suffixes are consistent with the manifest and `EXPECTED_SUFFIX`.
5. `.ufo/evidence/round-13/expected.json`: `{"inputs": {"tools/pin-disposition.py": <stub sha256>, ...}}` (only the probe key is consumed here).
6. `git init` inside the temp lane, with every `GIT_*` variable removed from the fixture subprocess environment. This makes the positive control meaningful (baseline `rev-parse --git-dir` succeeds; injected `GIT_DIR=/nonexistent/...` fails and names the path).
7. Run `python3 tools/context-capture.py` with cwd = temp lane root and `GIT_*` removed from the selftest environment. Read the emitted receipt from the temp lane.

Expected, per case (pins to use; literal reason strings copied from source):

| Case | Stub mode | Exit | Stdout head | Receipt assertions |
|---|---|---|---|---|
| P | `positive` | 0 | `CONTEXT: OK` | `status=ok`, `reasons=[]`, `comparison.equal=true`, `comparison.exclusions=["observed_at"]`, `comparison.observed_at` baseline `T1` ≠ injected `T2` |
| N | `nonobserved` | 1 | `CONTEXT: MISMATCH` | `comparison.equal=false`, `reasons==["injected observation differs from baseline after excluding observed_at: normalized JSON mismatch"]` |
| M | `missing_injected_observed_at` | 1 | `CONTEXT: MISMATCH` | `reasons==["injected observation differs from baseline after excluding observed_at: injected document has no top-level observed_at"]` |
| B | `missing_baseline_observed_at` | 2 | `CONTEXT: INVALID (kind=probe_baseline_unusable` | `error.kind=="probe_baseline_unusable"`, `status=invalid_input` |

Expected exit 0 in case P depends on the synthetic chain satisfying every other `decide` check (sidecar/digest match, env delta, positive control, mapping). Those are fixture-controlled. If a check fails, the reason list will show it, so the fixture is self-diagnosing. ContextGate must derive the exact stdout line text from the implemented source and must not invent it.

Stable IDs: none exist in the historical source beyond `error.kind` values and the literal reason strings. Map registry IDs to these literals. Do not introduce a new ID scheme under this criterion.

Mechanism-only limit: these fixtures prove the exclusion mechanics through the CLI. They do not prove the real six-leg pin chain, real sibling repos, or any environment independence.

## 5. Likely false positives (gate would be wrong)

FP-1 (highest): `LANE_ROOT` depth on promotion. Historical L45–47 uses four `dirname` calls because the file lives at `.ufo/evidence/round-14/`. A verbatim copy into `tools/context-capture.py` resolves to `/home/vgpnk/Projects`; `read_lane_bytes("tools/pin-disposition.py")` then fails with `missing_input` → exit 2, a false could-not-evaluate. Fix: two `dirname` calls. The fixture layout above (tool under `<lane>/tools/`) makes this visible in selftest.

FP-2: Positive-control false ineffective. A temp lane that is not a git repository makes `git -C LANE rev-parse --git-dir` fail at baseline → `positive_control.effective=false` → reason "git poison positive control is ineffective" → exit 1 for a case that should be P. Fix: `git init` in the fixture (step 6).

FP-3 (write-outside-temp risk): selftest fixture git commands inherit `GIT_DIR` if the selftest is launched with it set. The tool's own children are scrubbed (`safe_env`), but fixture setup is not. Unscrubbed `git init` / `git commit` could write to a live repository. Fix: scrub `GIT_*` for every fixture subprocess and assert the temp path is the only repo touched.

FP-4: Asserting `raw_stdout_equal == true` flakes whenever a second boundary falls between runs. Do not assert it (A5).

FP-5: Asserting order between receipt `observed_at` and probe `observed_at` is wrong by construction (start versus end) and is flaky at second resolution. Do not assert.

FP-6 (live-run caveat, not fixture-testable): a real mismatch can come from sibling HEAD or worktree motion between the two probe runs (EnvSentinel ES-8). The reason text "injected observation differs" must not be presented as proof of an environment cause. Record the differing JSON pointers if the promoted tool is extended, but do not add retries or A-B-A reruns under this criterion.

FP-7 (diagnostic only): an injected `invalid_input` JSON with exit 2 is reported as "produced no JSON document (exit=2)". Correct the wording in the promoted source or document it; exit semantics are unaffected.

## 6. Unearned claims to reject

U-1 "`observed_at` is the only volatile field." Earned only as "the only clock-derived field" (one `now()` call, L578). Unearned as a claim about field-set stability across runs (sibling-derived fields can change).
U-2 "Equal raw stdout including timestamp" (lesson L104; receipt `raw_stdout_equal`) as evidence that timestamps are stable. Reject: both retained stamps are `06:35:01Z`, a same-second coincidence.
U-3 "The exclusion shows environment injection is harmless / environment-independent." Reject. Lesson L127 already rejects this for one GIT_DIR injection.
U-4 "The round-14 receipt validates the promoted tool." Reject. Different file and digest (`7313e9a2…` versus the new tool); the receipt is retained evidence for the historical source only.
U-5 "Synthetic-fixture exit 0 proves C1 capability." Reject. The fixture proves exclusion mechanics only; it does not prove the real pin chain or repos.
U-6 "Exit 1 on missing injected `observed_at` shows the injection broke the probe." Reject. It is a shape difference with unknown cause.

Acceptable bounded wording: "The context gate removes only the top-level `observed_at` clock stamp from the probe document before canonical comparison; every other key is compared exactly. The exclusion does not establish timestamp stability, sibling-state stability, or environment independence."

## 7. Recommendations (bounded)

R1. Keep comparison semantics unchanged: top-level `pop("observed_at")` on shallow copies, canonical JSON, text equality. Change only path derivation (FP-1), output path (round15 only), and the selftest.
R2. Implement the four-case fixture matrix in section 4 (P/N/M/B) with exits 0/1/1/2, literal reason strings, and `error.kind`. Run it as CLI subprocesses against temp roots only.
R3. Do not add a regex, text-level, or nested `observed_at` strip. Do not add retry or A-B-A logic for this criterion.
R4. Keep `raw_stdout_equal` informational. Document it as such in the receipt schema comment.
R5. Document the two timestamps: receipt top-level `observed_at` is the start instant (`base_receipt`, before probes); probe `observed_at` is the end-of-read-window stamp (probe L578).
R6. Fixture git work: `git init` inside the temp lane with `GIT_*` scrubbed (FP-2, FP-3).
R7. Exit classes exercised by this criterion: 0, 1, 2. Exit 64 belongs to a separate usage case.
R8. Do not run any of this in this wave. L1 runs the selftest and the read-only retained-receipt check once after seats return.

## 8. Blockers

None. Implementation-critical items FP-1 (LANE_ROOT depth) and FP-3 (fixture `GIT_DIR` scrub) are being sent to TameshiR15 by message.
