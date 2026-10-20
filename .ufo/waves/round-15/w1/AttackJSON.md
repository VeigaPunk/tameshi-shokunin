# AttackJSON — planned C1 vs malformed JSON and duplicate keys

Seat: `TameshiR15.AttackJSON` (critic, leaf). Mode: source read only. Nothing was executed: no gate, selftest, fixture or Python probe.
Read revision: lane HEAD `a9cf4da78f2514c7bedd91a850a88590009d7df0`.
Historical source: `.ufo/evidence/round-14/capture-context.py`, sha256 `7313e9a2…7d89`, which equals the retained receipt's `tool_sha256`.
Retained receipt: `.ufo/evidence/round-14/context-receipt.json`, sha256 `05cb55b8…9c1a`.
`tools/context-capture.py` **did not exist** at read time, so this is a contract and source-based attack, not a review of new code.
Host python3 reported `Python 3.14.7`. That was the only command run besides `sha256sum` and `git log -1`.
Tool installs/updates: none.

Axes: calibration (C1 claim honesty), operability (exit/finding classification), and preservation (historical bytes untouched). Effect on the scalar: none.

## Source facts (observed)

| Path | Duplicate-key policy | Malformed → | Lines |
|---|---|---|---|
| Manifest and `expected.json` via `parse_json` | rejected by `object_pairs_hook=_no_duplicate_keys`, which applies to nested objects too | `InvalidContext("invalid_json")` → `main` exit 2, prints `CONTEXT: INVALID (kind=invalid_json …)`, receipt written | 158-181, 497-498, 618-628 |
| Probe stdout via `parse_probe_document` | **accepted, last value wins** (plain `json.loads`) | baseline: `probe_baseline_unusable` exit 2; injected: `comparison.error` → `decide` mismatch exit 1 | 340-347, 350-366, 555-560 |
| Non-UTF-8 input | — | `invalid_utf8` (files) and `non_utf8_output` (probe streams), both exit 2 | 170-171, 203-207 |
| Valid JSON with wrong container types | — | **not guarded**: `.get` on a non-dict raises `AttributeError` | 354-356 (`row.get`, `row.get("pinned", {}).get`), 554-578 (`decide`: `(x or {}).get`, `reasons.extend`) |

`main` catches only `InvalidContext` (lines 617-628). Any other exception ends the process with a traceback, exit **1**, and no receipt and no `CONTEXT:` line. Under PROTOCOL's Gate standard (as quoted in `round-14/w1/VerdictContract.md:16-19`), `1` = failed. A crash therefore lands in the **mismatch/failed** class, not could-not-evaluate. The source's own docstring map (lines 26-29) says unparsable input is exit 2.

One duplicate-key path is not reachable today. The genuine probe serializes a dict with `json.dumps` (`tools/pin-disposition.py:171-172`), so it cannot emit duplicates. A substituted probe would also fail `sources.probe.matches_declared` and give exit 1 through `decide`. So accepting duplicates in probe stdout does not, today, produce a false clean.

## Counterexample (passes a nominal helper-only test, wrong CLI semantics)

The planned C1 promotes a **retained-receipt check CLI** that reuses `decide()`.

**Helper-only test (passes):**
- `parse_json(b'{"a":1,"a":2}', "x")` raises `invalid_json`.
- `parse_json(b'{', "x")` raises `invalid_json`.
- `decide({...well-typed mismatch...}) == ("mismatch", 1, …)`.

All three hold for the historical code.

**CLI counterexample A: crash disguised as a verdict.**
The fixture is a receipt that is valid, UTF-8, duplicate-free JSON with a non-dict section:

```json
{"schema":"tameshi-round14-context-receipt-v1","status":"ok","exit":0,"reasons":[],
 "comparison":[true],"positive_control":{"effective":true},"mapping":{"all_match":true},
 "sources":{"probe":{"matches_declared":true},"runner":{"matches_manifest_declaration":true}},
 "environment":{"env_delta_matches_declared":true,"baseline_has_GIT_DIR":false}}
```

Suppose check mode does `parse_json` then `decide(receipt)`, like the historical `decide`. Then `([true] or {}).get("equal")` raises `AttributeError` and the process exits **1** with a traceback.

Compare a correct mismatch case asserted only as `returncode == 1`: this crash cannot be told apart from it. The helper tests above never reach this path.

Same class, from historical code:
- `"sources":{"probe":"x"}` crashes in `decide`.
- `"mapping":{"all_match":false,"reasons":5}` crashes with `TypeError` in `reasons.extend`.
- In capture mode, a baseline probe document with `"legs":[1,2,3,4,5,6]` or `"pinned":null` crashes at line 355.

**CLI counterexample B: a digest gate hides the duplicate-key check.**
If check/snapshot mode verifies a pinned digest **before** parsing (as the round-15 admit criterion requires: "persisted snapshot bytes are digest-checked before interpreting", `corpus/lessons/round-15.md:31-33`), a duplicate-key fixture without its own matching pin exits **2** as `snapshot_tampered`.

An exit-only test (`2`) for "duplicate keys rejected" would still pass if `_no_duplicate_keys` were deleted. The parser is never reached.

The reverse is also a trap: a fixture that is both duplicated **and** syntactically broken (for example, truncated) yields `invalid_json` with or without the hook. Kind and exit alone cannot detect removal of the hook.

## Bounded recommendations

### Required (inside routed defect 5: public-CLI selftest with literal exit + stable finding ID; correct exit classes)

1. **Pin the exit together with the stable finding ID for every JSON case, and reject crashes.**
   - Each selftest JSON case asserts the literal exit **and** the stable kind token from the CLI's stdout line or report.
   - A case also fails if stderr contains `Traceback` or the expected finding line is missing.
   - Without this, counterexample A passes as "mismatch exit 1".
2. **The check mode must classify unusable receipt JSON as exit 2, never exit 1.**
   - Parse with the existing duplicate-rejecting `parse_json`. Do not use plain `json.loads`.
   - Before calling `decide()`, verify the container types it dereferences: top-level object; `comparison`, `positive_control`, `mapping`, `sources`, `environment`, `sources.probe` and `sources.runner` are objects; `mapping.reasons` is a list of strings when present.
   - Any violation is exit 2 with one stable kind (reuse the existing family, for example `invalid_json`, or a single new receipt-shape kind declared in the registry).
   - This is the minimum needed for the declared map "2 = unparsable input" to hold in new code. It is not a broad validation framework.
3. **The duplicate-key selftest fixture must be able to tell whether the hook is present.**
   - The fixture is otherwise valid JSON.
   - Under last-wins it would evaluate **clean** (for example, a first `"comparison":{"equal":false,…}` followed later by a clean `"comparison"`). Removing the hook then becomes a visible false-clean regression (exit 0 instead of 2).
   - If digest binding is active, the fixture's own pinned digest must match its bytes, so parsing is actually reached.
   - Assert `exit 2` plus kind `invalid_json` plus message substring `duplicate JSON key`. The message is needed because `invalid_json` also covers syntax errors and a non-object root (lines 160-181).
4. **Keep a separate digest-mismatch case:** `exit 2` plus `snapshot_tampered`. The two exit-2 classes are then pinned by different IDs, not merged into one.
5. **Hermetic ordering.** In capture mode, `evaluate` checks the live host `os.path.lexists(POISON_PATH)` and `FLEET_ROOT` (lines 468-473), and reads all four lane inputs (476-479) **before** any JSON parse.
   - Any capture-mode JSON fixture must run under a temporary lane root holding all four inputs, with the poison path/root and the receipt output path resolved inside that temporary root.
   - Otherwise the finding is `poison_path_exists`, `missing_input` or a live write instead of `invalid_json`.
   - Simpler: exercise JSON cases through check mode only.

### Optional hardening (not routed; do not claim as C1 evidence)

- Catch `RecursionError` in `parse_json` and map it to `invalid_json`. [INFERENCE: CPython's `json` raises `RecursionError`, not `JSONDecodeError`, for very deep nesting; not executed here.] Digest-pinned inputs make this unreachable in snapshot mode.
- Reject `NaN`/`Infinity` through `parse_constant` (strict RFC 8259). Python's `json` accepts them by default.
- Apply duplicate rejection to probe stdout in `parse_probe_document`. This is unreachable from the genuine probe (`pin-disposition.py:172`), and doing it changes the reused comparison semantics: a duplicate in the baseline becomes exit 2 instead of the current last-wins value. If adopted, declare it as a semantics change.
- Type-guard `comparison_block` baseline leg rows at line 355 so they raise `probe_baseline_unusable` instead of `AttributeError`. This is a latent capture-mode crash, reachable only through a substituted probe.

## Unearned claims to reject

- "Duplicate keys are rejected" stated without scope. It is true only for inputs parsed by `parse_json` (manifest, expected, and the check-mode receipt if wired to it). It is false for probe stdout.
- A JSON selftest that asserts only exit codes, or only calls helpers, presented as satisfying routed defect 5.
- Any claim that a malformed-JSON case shows correctness of the historical round-14 run. The retained receipt has `equal:true`, `raw_stdout_equal:true` and `status:"ok"`, but that is round-14 evidence only and is not re-executed.

## Confidence

High for the observed source behavior above: it rests on exact lines and Python's documented behavior for exceptions in `object_pairs_hook` and for uncaught exceptions (exit 1). Recommendation 2's exact kind name is left to ContextGate. The RecursionError item is inference.
