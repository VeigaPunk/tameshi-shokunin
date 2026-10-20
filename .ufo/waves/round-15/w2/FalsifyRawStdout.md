# FalsifyRawStdout — round-15 w2 critic

Seat: TameshiR15.FalsifyRawStdout (leaf critic). Static review only. I did not run the tool, its selftest, or any Python snippet. Nothing was installed.

## Target

Can a retained receipt whose stored `comparison.equal` is `True`, but whose raw `runs.*.stdout` diverges (including in a probe leg tuple), get past `tools/context-capture.py --check`?

## Exact source read

- `tools/context-capture.py`. I read it at snapshot #472A, 2116 lines. A concurrent edit moved it to #6F31, 2123 lines, and I re-anchored on that version. Ranges read:
  - 2–303: docstring, finding-ID and exit map, constants
  - 304–352: `_no_duplicate_keys`, `parse_json_strict`, `read_regular`
  - 459–1003: validators, `embedded_json`, `validate_baseline_document`, `canonical_payload`, `recompute_comparison`
  - 1107–1363: verdict, expected pin, `run_check`
  - 1364–1460, 1611–1680, 1728–2004: fixture and selftest cases
  - 2005–2116: `run_selftest`, `parse_argv`, `main`
- Historical `.ufo/evidence/round-14/capture-context.py` (#096B): `parse_probe_document`/`comparison_block` (340–392), `evaluate`/`decide` (465–580), `main` (605–643). These are the parity reference.
- `AGENTS.md`.

## Bounded agreement (the main attack fails)

- **Stored `equal` cannot override the raw data.** `recompute_comparison` (881–981 in #6F31) re-parses both stdouts and rebuilds the canonical text: `dict` copy, pop of the top-level `observed_at`, then `json.dumps(sort_keys, separators)`. It records a `comparison_mismatch` finding in each of these cases:
  - `recorded["equal"] is not recomputed["equal"]`
  - `recomputed["equal"] is False`, unconditionally
  - either comparable sha256 disagrees
- **A diverging leg tuple, or any non-`observed_at` field, cannot survive.** The comparison is whole-document canonical text, not a dict `==`. So the `True`/`1` and `1.0`/`1` collisions don't apply, and lists keep their order.
- **Duplicate-key smuggling is rejected.** Last-wins duplicate keys would have hidden divergence in the historical `json.loads`. Here `_no_duplicate_keys` rejects them: an injected duplicate gives `injected=None`, so `error` and `equal=False`, giving `comparison_mismatch` exit 1. A baseline duplicate gives `baseline_unusable` exit 2. This is stricter than the historical script and documented in the docstring (lines 39–40).
- **What the normalization still collapses:** whitespace, key order, string-escape spelling, number spelling (`1.00`/`1.0`, `-0`/`0`, floats beyond 17 significant digits) and a JSON `null` injected `observed_at`. The historical `comparison_block` (384–391) collapses exactly the same things. None of these can change a hex commit/digest/status string in a leg tuple. This is parity, not a defect.
- **Selftest coverage:** `comparison-raw-mismatch` (1763) keeps the stored `equal: True` and changes the injected raw `status`, pinned to `comparison_mismatch`/1. That matches the code path above.

## Counterexample: one falsifiable hole (classification, not a false pass)

**The bug.** `embedded_json` (759–765) catches only `ValueError`. CPython's json C scanner raises `RecursionError` on nesting past the recursion limit, and `RecursionError` is a `RuntimeError`, not a `ValueError` `[INFERENCE: CPython json behaviour, not executed here]`. So:

1. The injected-side `except CouldNotEvaluate:` at 900 does not catch it.
2. The exception passes through `check_receipt` and `run_check` and lands in `main`'s generic `except Exception` at 2113.
3. The result is `internal_error`, exit 2, built via `result_from_exception(..., None, None, None)`.

**Concrete receipt.** Start from the selftest fixture clean receipt and change three things:
- In `runs.injected.stdout`, replace `legs[0].pinned` with about 1100 nested arrays (`[[[…]]]`). The document is still valid JSON, still an object, and still has a top-level `observed_at`.
- Keep the stored `comparison.equal = true` and the baseline comparable digests.
- Set the stored `status`/`exit`/`reasons` to `mismatch`/1/non-empty.
- Pin `{"id":"comparison_mismatch","exit":1}` with the correct receipt sha256.

**Expected by the tool's own rule.** The 893–901 branch is meant to turn an unparseable injected stdout into "no JSON document". Together with the historical exit map ("1 mismatch (including injected run unusable)"), that should give `comparison_mismatch`, exit 1.

**What actually happens** `[INFERENCE, static]`:
- id `internal_error`, exit 2
- `receipt.sha256: null`, `expected: null`, `verdict_matches_expected: null`

So the `--expected` id/exit pin is silently never applied. The same bypass on the baseline side yields `internal_error` instead of `baseline_unusable`; the exit is the same (2) but the id is wrong. At receipt level, `parse_json_strict` (327) yields `internal_error` instead of `receipt_json_invalid`.

**Severity.** Fail-closed: the result is never exit 0, so stored `equal` is never accepted. It does break the literal stable id/exit classification and drops the pin binding for a raw-stdout divergence. That is a fixable defect, not a tradeoff the judge must reject.

## Impacted axes

- Literal expected exit/finding pairs: the stable ID map and the 64-class mapping.
- Faithful reuse of the historical comparison semantics (unusable injected run counts as a mismatch).
- Pin binding: the expected pin is lost on the internal-error path.

Not affected: clean-proof integrity, write scope, snapshot digest, no-false-pass.

## Smallest safe correction

1. In `embedded_json` and `parse_json_strict`, catch `(ValueError, RecursionError)` and route both to the existing `CouldNotEvaluate(finding_id, …)`. With that change, an injected-side failure becomes `comparison_mismatch` exit 1, a baseline-side failure becomes `baseline_unusable` exit 2, and a receipt-level failure becomes `receipt_json_invalid` exit 2.
2. Add one selftest `check_case`: injected stdout with a leg tuple nested past the recursion limit and stored `equal: True`, pinned to `comparison_mismatch`/1.

No other change. Keep `main`'s generic fallback as the last-resort net.
