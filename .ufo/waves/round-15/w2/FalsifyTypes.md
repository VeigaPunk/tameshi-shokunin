# FalsifyTypes — round-15 w2 critic (static review only)

Seat: `TameshiR15.FalsifyTypes`. Leaf seat. I executed nothing: no selftest, no `--check`, no build, no lint. Tool installs/updates: none.

## Source read (exact)
- `tools/context-capture.py` (snapshot tag `#472A`):
  - lines 1–1345: docstring, constants, coercers, validators, recompute functions, verdict, `run_check`;
  - lines 1570–2116: selftest harness, cases and CLI `main`.
  - I did not open the fixture builder body (1388–1569).
- Historical producer `.ufo/evidence/round-14/capture-context.py`:
  - lines 340–392: `parse_probe_document`, `comparison_block`;
  - lines 540–600: `evaluate` tail, `decide`.
- `corpus/lessons/round-14-verifier-spotcheck.md`, lines 154–162 (Routed defects).
- Sibling w2 reports, grep only: none covers this field.

## Bounded agreement on the assigned type attacks
Each item below is a static path trace, not an executed result.
- **Bool exits are rejected.**
  - `require_int` (395) uses `type(value) is not int`, so `true`/`false` raise `receipt_structure_invalid`/2.
  - This applies to `receipt.exit` (510), both run exits (443), `call.line` (736) and the expected-pin exit (1206, mapped to `expected_invalid`).
  - The selftest pins this with `bool-exit` (1871–1872).
- **Truthy strings and ints are rejected.**
  - Every stored flag goes through `require_bool` (388, `type is not bool`).
  - Every recompute comparison uses `is not` against a real bool (827, 859, 867, 933, 952, 965, 991–999, 1023, 1032, 1072, 1077, 1085–1096).
  - The selftest pins `truthy-matches-declared` (1858) and `truthy-all-match` (1865).
- **Wrong nested containers are rejected.**
  - `require_object`/`require_list` check exact types and key sets at every nesting level (363–413, 439–453, 559–750).
  - Embedded probe documents are type-checked (766–790, 912).
  - The selftest pins `comparison-container` (1881).
- **Deep nesting does not traceback.**
  - `json.loads` raises `RecursionError`, which is not a `ValueError`, so it escapes 324/759.
  - `main` catches it at 2106 and returns `internal_error`/2.

I found no false-clean (exit 0) path on these three attacks.

## Falsifiable hole: the validator rejects the producer's own `null` type for `payload_tool_sha256_matches_disk`

**Counterexample.** This is the producer-faithful receipt for the very failure the experiment probes: the poisoned `GIT_DIR` breaks the injected probe run. Build it from the selftest base receipt:
- `runs.injected.exit = 128`, `runs.injected.stdout = ""` (any `stderr`);
- `comparison` exactly as historical `comparison_block` writes it (round-14 lines 363–375):
  - `observed_at.injected = null`, `raw_stdout_equal = false`;
  - `baseline_comparable_sha256 = null`, `injected_comparable_sha256 = null`;
  - `payload_tool_sha256_matches_disk = null`, `equal = false`;
  - `error = "injected probe run produced no JSON document (exit=128)"`;
- `status = "mismatch"`, `exit = 1`, one non-empty reason (historical `decide` 560–565, 578–579 returns `mismatch`/1).
- The expected pin is `{receipt_sha256: sha256(R), id: "comparison_mismatch", exit: 1}`.

**Evidence (static trace).**
1. `validate_comparison` accepts the null `observed_at.injected` (583) and the null comparable digests, because `error` is non-null (590–595).
2. It then runs `require_bool(comparison["payload_tool_sha256_matches_disk"], ...)` at 598 unconditionally. `null` is not a bool, so it raises `receipt_structure_invalid`.
3. `run_check` 1337–1339 → `result_from_exception` → `apply_expected` 1283–1285. The output is `id=receipt_structure_invalid`, `exit=2`, with `expected_verdict_mismatch` added to the findings.
4. The recompute side expects this shape:
   - `recompute_comparison` sets `recomputed["payload_tool_sha256_matches_disk"] = None` on the error path (904, 912–917);
   - it compares with `recorded is not recomputed` (933).
   - A recorded `null` would match there, and the receipt would resolve to `comparison_mismatch`/1 (975–978).
   - The 933 branch is unreachable for the only value the producer writes.
5. A writer cannot satisfy both sides. If they record a bool to get past 598, then `True/False is not None` always files `comparison_tool_digest_mismatch` (933–940), and that becomes the primary id ahead of `comparison_mismatch`.
   - So no type-valid encoding of an injected-run failure can ever be pinned as `comparison_mismatch`.
   - The same applies to the producer's "no top-level observed_at" error path (round-14 377–379).
6. The selftest has no injected-failure or error-path comparison case (1736–1994). `comparison-raw-mismatch` keeps a parseable injected document, so this path is unpinned.

**Impacted axes.**
- C1 exit-class mapping: a genuine re-derivable failure (exit 1) is downgraded to could-not-evaluate (exit 2).
- Fidelity of reuse of the historical comparison semantics, which the integration interface requires.
- Stable-ID pinning: `comparison_mismatch` cannot be pinned for this class.

The gate still fails closed: nothing reaches exit 0. This is a fixable defect, not a tradeoff.

**Smallest safe correction.**
- At line 598, accept `None` only when `comparison["error"] is not None`, mirroring 590–595. Otherwise keep `require_bool`.
- Add one selftest case, `injected-run-failed`, with the producer-shaped fields above. Pin `comparison_mismatch`/1.

## Not routed (observations only, outside the one-hole bound)
In text mode with a UTF-8 strict stdout, a lone-surrogate JSON string in `mapping.legs[i].leg` reaches the unescaped `"leg {} ..."` detail (1074, 1079).
- `emit`'s `FINDING` write raises `UnicodeEncodeError` after the header line has already been written. The handler at 2106 then emits a second `INVALID … exit=2` line.
- The result is two contradictory verdict lines and exit 2, while `--json` gives exit 1.
- It is still fail-closed and has no traceback. Locale-dependent `[INFERENCE]`.

Message sent to `TameshiR15`: yes. The hole above is implementation-critical for C1 exit-class fidelity.
