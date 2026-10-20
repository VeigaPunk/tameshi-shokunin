# FalsifyMapping — round 15 wave 2 (critic, static review only)

Seat: TameshiR15.FalsifyMapping. Static source review only. I ran no selftest, check, build, or receipt. No tools were installed or updated. The only write is this report.

## Source read (exact)
- `tools/context-capture.py` (2116 lines, snapshot tag `#472A`): docstring lines 39-73; constants 155-169 and 237-249; `validate_mapping` 645-750; `recompute_mapping` 1038-1105; `verify_recorded_verdict` 1108-1129; `check_receipt` 1152-1180; `run_check` 1298-1344; fixture `build_fixture_receipt` rows 1406-1436; `SelftestHarness.check_case` 1611-1682; selftest cases `mapping_check_lie`, `mapping_constant_swap`, `mapping_order_lie`, and `truthy-all-match` 1806-1869.
- Historical producer `.ufo/evidence/round-14/capture-context.py` (tag `#096B`): mapping derivation lines 238-311, `all_match` at 335, and decide at 576.

## Axis 1 — stored `all_match` contradicted by a per-leg false: bounded agreement
- `recompute_mapping` recomputes every check from raw fields (1048-1068). It derives `match = all(checks)` (1069), then `all_match = leg_set_equal and leg_order_equal and len==6 and all(recomputed_matches)` (1093-1095). It compares the recomputed value with the stored literal bool using `is not` (1096). `validate_mapping:692` already rejects non-bool values with `receipt_structure_invalid`/2, and the `truthy-all-match` selftest pins that pair.
- **Case A:** stored `all_match: true` while any leg recomputes false. Line 1096 appends a problem, which produces `mapping_mismatch`. That finding comes first and becomes the primary id (1340). The stored ok/0 verdict also adds `receipt_verdict_mismatch` (1112-1126). The result is `mapping_mismatch`/1. No hole.
- **Case B:** stored `all_match: false` while every leg is clean. Only line 1096 catches this, and the result is `mapping_mismatch`/1. No hole.
- **Coverage note (not a hole):** in Case A, lines 1096 and 1102 emit the same id, so deleting 1096 would not change the selftest result. No selftest pins Case B, which is the only case where 1096 is the sole detector. This is a test-strength gap, not a behavioural defect.

## Axis 2 — equal-valued REV name swap: ONE falsifiable hole
**Defect:** the leg's suffix comes from the receipt row, not from the authoritative table.
- `recompute_mapping:1045` uses `suffix = leg["declared_variable_suffix"]`, which is a stored, self-declared field.
- `validate_mapping:716-721` only requires `suffix in EXPECTED_SUFFIX.values()`. It does not check that the suffix equals `EXPECTED_SUFFIX[leg["leg"]]`. It does not require suffixes to be unique, and it does not check that the leg name is a key of the table.
- The validated authority is already there: `declared_variable_table == EXPECTED_SUFFIX` (679). It is never used to bind each row.
- The historical producer derives the suffix as `suffix = EXPECTED_SUFFIX.get(leg)` (round-14 line 269). All four name checks require `suffix is not None` (284, 288, 292).
- So the maintained checker does not reuse the historical mapping semantics. Its name checks only compare each row against itself.

**Concrete counterexample** (built from the selftest fixture, `base = build_fixture_receipt()`):
```
leg = document["mapping"]["legs"][0]            # "js-kimi-census", table suffix "JS"
leg["declared_variable_suffix"] = "BASH"        # in EXPECTED_SUFFIX.values() -> passes 718
leg["runner_call"]["pin_constant"]   = "PIN_BASH"
leg["runner_call"]["rev_constant"]   = "REV_BASH"   # REV name swapped to bash-surface-census
leg["runner_call"]["table_constant"] = "TABLE_BASH"
# pin_value / rev_value unchanged == js-kimi manifest values (equal-valued swap)
# checks all True, match True, all_match True, status "ok", exit 0, reasons [] unchanged
```
Static trace through the source:
- Validation passes: the suffix is configured, the call strings are non-empty, and the leg order is unchanged.
- Recompute: `header_matches_manifest` is True. `leg_call_matches_manifest` is True. PIN check: `"PIN_BASH" == "PIN_"+"BASH"` and the values are equal, so True. REV check: `"REV_BASH" == "REV_"+"BASH"` and the values are equal, so True. Constant-names check: True. So `match` is True and `all_match` is True. Nothing is appended to `problems`, and the 1102 branch does not fire.
- No other block is touched, so `findings == []`. `verify_recorded_verdict` accepts ok/0/[].
- The traced result is `context_consistent`/0.

For the same runner state, the historical producer computes `rev_name REV_BASH != REV_JS`. That makes the REV, PIN, and constant-names checks False, so it records `match` False, `all_match` False, and mismatch/1.

This is the equal-valued REV name swap the round-14 design meant to catch. It passes as clean as long as the receipt's derived suffix field is changed to match. A variant with a renamed leg (`legs[i].leg = "x"`, plus a matching `manifest_leg_order` and `runner_leg_order`, and any configured suffix) also passes, because the historical `.get` → None → False path is never reproduced.

**Impacted axes:**
- mapping recompute fidelity: the "recomputed from raw fields" claim at docstring line 54 is false for constant names.
- reuse of historical decide/mapping semantics.
- C1 bounded retained-replay honesty: a forged-clean retained receipt is accepted as `context_consistent`.

**Smallest safe correction:**
- In `recompute_mapping`, set `suffix = EXPECTED_SUFFIX.get(name)` (or use the validated `mapping["declared_variable_table"].get(name)`).
- Prefix the PIN, REV, and constant-names checks with `suffix is not None and`, as in historical lines 284/288/292.
- Append a problem when `leg["declared_variable_suffix"] != suffix`, so a stored-derived lie becomes `mapping_mismatch`/1, consistent with docstring line 55.
- Add a selftest case `mapping-suffix-swap` using the counterexample above, with stored ok/0 and expected `mapping_mismatch`/1. Optionally add a Case B fixture (stored `all_match: false` with clean legs → `mapping_mismatch`/1) so line 1096 is pinned on its own.

**Classification:** a fixable defect, not a tradeoff. No new environment claim is needed.
