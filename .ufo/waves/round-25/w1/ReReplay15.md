# ReReplay15 — re-attack of round-23 wave-2 Replay15 (row `context-capture-mapping-suffix`)

## Verdict

FINDING: there is a field-level false acceptance. The row's `expect` is `{"exit": 1}` with no `stdout_contains`. For `tools/context-capture.py`, exit 1 is shared by all 14 "failed" finding IDs. It also covers `expected_verdict_mismatch`, the error the tool raises when the row's own `expected.json` pin is violated, and any uncaught Python import error. Five concrete regressions of the mapping/suffix check in the tool each produced exit 1. Under the frozen expectation, the pristine `tools/command-binding.py` accepted every one of them (`exit 0, finding_ids []`). The static, recorded binding itself is exact: the frozen receipt is byte-consistent and CLEAN. However, the row does not bind the claim its name makes, which is that the suffix swap is detected as `mapping_mismatch`.

The finding still applies at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df. The row is byte-identical, `active`, and has no `superseded_by` link and no successor row. `context-capture.py`, `registry-check.py` and the fixture are unchanged between 496d212 and c9ff09f. The only change to `command-binding.py` is in the selftest fixture loader, and its `evaluate()` logic is unchanged.

## What was checked (static binding — holds)

All checks ran read-only against the lane, or inside my own clone `/tmp/rereplay15-d45FS8/lane` at c9ff09f.

- Row identity across the frozen artifacts: the requirement in `round-23/requirements.json`, `replay/bundle.json` (requirements[] and receipts[]) and `replay/observations.json` row `requirement` are equal (`req==bundle req True`, `obs.requirement==req True`). Receipt and observation `argv`, `cwd` (`/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`) and `revision` (`496d212bc46789cdf8cafab72978bdb7f4182963`) are all equal. Exit is 1 in both, and stderr is `''` in both.
- Full output, not tails: the receipt `stdout` (924 bytes) equals the observation `runner_result.stdout`, which equals `stdout_tail` (the output is short enough that the tail is the full text). Observations header: `capture: "complete decoded stdout/stderr; original runner tails retained separately"`.
- Bundle pin: `sha256sum replay/bundle.json` = `3d6c99b7…a50b9` = `replay/expected.json.bundle_sha256`. Running `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json` in the clone gave `{"exit": 0, "finding_ids": [] …}`.
- Runner and registry identity: observations `runner_sha256` `cba16646…944ad` = `sha256sum tools/registry-check.py` at c9ff09f. Observations `registry_sha256` `ebd2e69a…ec92a` = `git show 496d212:tools/registry.json | sha256sum`.
- Fixture pin: `round-15/frozen/mapping-suffix/expected.json` = `{"exit": 1, "id": "mapping_mismatch", "receipt_sha256": "02204ef8…8fe5e"}`, and `sha256sum receipt.json` = `02204ef8…8fe5e`.
- Re-execution of the row's argv in the clone with the pristine tool reproduced the retained stdout byte for byte (`CONTEXT: MISMATCH (id=mapping_mismatch … findings=2)`, then `FINDING mapping_mismatch leg 'js-kimi-census' declared_variable_suffix 'BASH' is not the canonical 'JS'; …` and `FINDING receipt_verdict_mismatch …`), with exit 1.

## Counterexample (field-level false acceptance on `expect`)

### Why exit 1 alone carries no row-specific meaning

`tools/context-capture.py:61-77` lists 14 stable IDs that all exit 1. The exit map (`:91-96`) says exit 1 means "a re-derived fact disagrees, the stored verdict disagrees, **or the recomputed verdict does not match the expected id/exit pin**". `apply_expected` (`:1308-1329`) turns a mismatch against the pin into exit 1: a clean exit 0 becomes `expected_verdict_mismatch`/1, and an exit-1 result with the wrong ID keeps exit 1. So the row's own `expected.json` pin cannot make a wrong verdict leave exit 1. Exit 1 is the result whether the pin holds or is violated.

The runner applies the same weak predicate. At `tools/registry-check.py` (`run_row`, `:718-720`), `held = got == expected_exit and not missing and cleanup_ok`, where `missing` is computed over `stdout_contains` needles. This row has no needles. Its `runner_result` in observations records `"expect": 1, "got": 1, "held": true`.

### Executed mutants

Each mutant changed only `tools/context-capture.py` in the `/tmp` clone, and the original was restored afterwards (sha256 confirmed and `git status` clean). The row's exact argv was run from the clone root. Each receipt was then bound with the pristine `command-binding.py` (fresh `bundle_sha256` pin, revision c9ff09f, cwd = clone root) under three expectations:

1. **Frozen**: `{"exit": 1}`.
2. **Sibling idiom**: `stdout_contains ["mapping_mismatch"]`, the bare-ID style used by row `context-capture-missing-env`.
3. **Correction**: `stdout_contains ["CONTEXT: MISMATCH (id=mapping_mismatch ", "FINDING mapping_mismatch leg 'js-kimi-census' declared_variable_suffix 'BASH' is not the canonical 'JS'"]`.

| Mutant | Tool output (first line) | Exit | Frozen | Bare-ID idiom | Correction |
|---|---|---|---|---|---|
| pristine | `CONTEXT: MISMATCH (id=mapping_mismatch … findings=2)` | 1 | CLEAN | CLEAN | CLEAN |
| M1: `recompute_mapping` returns immediately (`:1066`) | `(id=expected_verdict_mismatch … findings=1)`; detail `expected id=mapping_mismatch exit=1 but recomputed id=context_consistent exit=0` | 1 | **CLEAN (false accept)** | **CLEAN (false accept)** | STDOUT_MISMATCH |
| M2: trust the stored suffix (`suffix = stored_suffix`, suffix problem removed, `:1078-1082`) | same as M1 | 1 | **CLEAN (false accept)** | **CLEAN (false accept)** | STDOUT_MISMATCH |
| M3: import crash before `main()` (`import tameshi_nonexistent_module`) | stdout empty; `ModuleNotFoundError` traceback on stderr | 1 | **CLEAN (false accept)** | STDOUT_MISMATCH | STDOUT_MISMATCH |
| M4: emit `comparison_mismatch` instead of `mapping_mismatch` (`:1138`) | `(id=comparison_mismatch … findings=3)` | 1 | **CLEAN (false accept)** | **CLEAN (false accept)** | STDOUT_MISMATCH |
| M5: only the suffix-canonical problem removed (`elif stored_suffix != canonical_suffix` → `elif False`) | `(id=mapping_mismatch … findings=2)`, with no `declared_variable_suffix 'BASH'` clause | 1 | **CLEAN (false accept)** | **CLEAN (false accept)** | STDOUT_MISMATCH |

M2 is the strongest counterexample, because it is exactly the regression this fixture is named for: the tool stops treating a swapped `declared_variable_suffix` as a mismatch and accepts the forged `BASH` suffix on the `js-kimi-census` leg. The tool then decides the forged receipt is `context_consistent`. Only the pin turns that into exit 1, and the row accepts it.

### Adversarial delta: the bare finding-ID idiom is not a sufficient fix

When the pin is violated, `expected_verdict_mismatch`'s detail repeats the pinned ID (`expected id=mapping_mismatch exit=1 but recomputed …`, `:1317-1319`). So a bare `mapping_mismatch` needle is satisfied by the very output that reports the pin failure (M1, M2, M4 above). The same pattern probably exists in the sibling row `context-capture-missing-env` (bare `missing_injected_environment` needle) `[INFERENCE — not executed for that row; out of scope]`. M5 shows that pinning only the header ID is also not enough to bind the suffix check: the other leg checks still produce `mapping_mismatch`. So a needle naming the suffix clause is required.

## Evidence present versus inferred

- Present and observed: every equality, digest and command output above was observed in this run. The round-23 artifacts retain the full stdout for this row (924 bytes), not just tails.
- Provenance gap: the row's `source` is `SKILL.md@98bea7d:1680`. That line (read with `git show 98bea7d:SKILL.md | sed -n 1680p`) is the generic round-15 context-gate registry row. It names `--check --receipt FILE --expected FILE`, exit class "1 failed stable finding ID", and only the `context-missing-env.json` negative fixture. `git show 98bea7d:SKILL.md | grep -n mapping-suffix` returns nothing. So the specific fixture operands and `exit: 1` are taken from the generic template plus `round-15/frozen/mapping-suffix/expected.json` (added in b255055). They are not quoted from the cited line, and the row first appears in the registry at 2a22ade (round 17). This is a citation-granularity gap, not fabrication: `exit: 1` is consistent with the cited verdict map.
- Not claimed: no producer authentication of the round-23 replay or of the round-15 fixture, and no retrofill of historical metadata. The observations carry measurement intervals for the 2026-10-21 replay execution only.

## Impacted axes

- Calibration: this negative fixture's row cannot tell "detected the suffix swap" from "lost the detector and the pin fired" or "crashed". As a guard, its kill power against mapping-check regressions is zero under `exit` alone.
- C1 R23-ROUTED-1 (multi-token stdout): this row is a direct instance where a single token is too weak and two tokens (header ID plus suffix clause) are needed.

## Smallest safe correction (fixable defect, not a tradeoff)

Supersede the registry row with an identical row, changing only `expect`. This is integrator-owned and was not done here.

```json
"expect": {"exit": 1, "stdout_contains": [
  "CONTEXT: MISMATCH (id=mapping_mismatch ",
  "FINDING mapping_mismatch leg 'js-kimi-census' declared_variable_suffix 'BASH' is not the canonical 'JS'"
]}
```

Observed effect in the clone: the pristine tool stays CLEAN, and M1–M5 all become `STDOUT_MISMATCH` under `command-binding.py`. The bare `mapping_mismatch` needle must not be used, because the pin-failure detail echoes it.

Observation, out of scope: two other round-23 requirements also have no stdout needle (`repeat-control-snapshot-clean`, `repeat-control-snapshot-mismatch`). I did not attack them.

## Bounds and tooling

Writes: this report only, plus scratch under `/tmp/rereplay15-d45FS8`. No git or jj write commands were run in the lane, and no gate, suite or registry sweep was run in the lane. The original registry command ran only inside the `/tmp` clone (the assignment allowed read-only checks there). No tools were installed or upgraded.

R23-REATTACK Replay15: FINDING
