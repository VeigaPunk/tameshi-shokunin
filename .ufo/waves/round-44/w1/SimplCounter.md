# SimplCounter findings

Axes: calibration (primary); freshness unaffected. Lane counter was not edited.

Source: `.ufo/evidence/round-44/calibration/measure.py` (frozen counter). Baseline scratch copy selftest: `C2_R44_SELFTEST: cases=16 failed=0`, `VERDICT: PASS`.

## Safe deletion candidates

- Lines 73–74: `SKIP_SUFFIXES` is never read (its sole AST name occurrence is its own definition). Delete the constant. On scratch copy with this deletion, `C2_R44_SELFTEST: cases=16 failed=0`, `VERDICT: PASS`.
- Line 503: `stated_round` receives the second result of `row_count_claim` but is never read. Replace the binding with `_` (or delete the unused binding by extracting only the first tuple member). Scratch selftest after this change: `C2_R44_SELFTEST: cases=16 failed=0`, `VERDICT: PASS`.

## Reviewed; preserve

- Lines 103–105 in `m7_citations`: the label skips are not tautological overall. `next-free-phrase` and `safe-floor` are skipped because the corresponding broad phrase patterns are handled by `VALUE_ID_AFTER`, while concrete MASK_IDS patterns (staged/next-free declaration/register) are applied. Do not delete the loop or skip logic without replacing semantics; round-44 assignment masking is critical to the frozen m7 contract and T6 coverage.
- Lines 107–109 use three distinct pattern closures and are reachable; each removes only the matched S-id from the matched text, preserving surrounding prose for citation scanning.
- No branch identified as constant-truth from source inspection. In particular PASS depends on frozen self-pin, seven declared classes and measured total; round mismatch checks are data-dependent.

No tools installed. Contract preserved by proposed deletions; only `--selftest` was exercised as requested.
