# PredK10 — falsification of frozen predicate K10 `live-dependent-listed`

Revision attacked: c8c5b88c8e961a929cdc351b95a7074c76958909 (repo HEAD). Base: 6a1821a8897eea6e7d9669292160ec9593669409.
Mode: static read-only inspection. This item has no "Run" clause, so I did not execute the ruler, the selftest or any mutant. The counterexamples below are derived deterministically from the code; the outcomes I did not execute are marked [INFERENCE].
Tools installed or updated: none.

## Verdict

**K10 can be passed by a weaker implementation (defect in ruler calibration).** It is not vacuous, and the base result in `before.json` is honest. For the delivered tool, K10 passes for the right reason [INFERENCE]. However, the predicate does not discriminate the weakening that the knowledge entry names: "the list omits such a row". The cause is a single fixture that sets **both** disjuncts (`external=True` **and** `non_hermetic_argv`) on one row. K10 also checks neither `revision_pinned` nor the persisted `live-dependent.json` file.

## Evidence

### What K10 checks
- `.ufo/evidence/round-24/measure.py:181` defines the fixture as `obs(external=True, non_hermetic_argv=['/live/root'])`. Here `obs` (lines 147-157) routes every key except `external` into `runner_result`. As a result, one row carries both live-dependence signals at once.
- `.ufo/evidence/round-24/measure.py:183-184` passes K10 when all of the following hold:
  - `control_ok`
  - `exit == 0`
  - `report.live_dependent == ['one']`
  - `creport.live_dependent == []`
  - `bundle.json` exists

  K10 does not read `revision_pinned`, `live-dependent.json`, or per-branch attribution.

### Delivered implementation
- `tools/registry-replay.py:99` is `if row.get('external') is True or result.get('non_hermetic_argv'): live.append(name)`.
- `tools/registry-replay.py:105-107` builds the report with `revision_pinned = len(receipts) - len(set(live))`.
- `tools/registry-replay.py:125-127` writes `live-dependent.json`.
- On the K10 fixture, the delivered tool lists `['one']` and publishes with exit 0. The control fixture yields `[]` [INFERENCE, static].

### Runner semantics
- `tools/registry-check.py:663-671`: when argv names a live-fleet path and the row is **not** `external`, the runner sets `got="non-hermetic"`, `held=False` and `non_hermetic_argv`. When the row **is** `external`, it sets `non_hermetic_argv` and continues to execute.
- So with the real runner, a published (held) row with `non_hermetic_argv` is always also `external`. However, an `external` row does **not** always have `non_hermetic_argv`.

### Actual replay
`.ufo/evidence/round-24/replay/observations.json`, inspected read-only with `python3`:
- `pin-disposition-read`: `external=True`, `non_hermetic_argv=['/home/vgpnk/Projects/shokunin']`, `held=True`.
- `verify-round15`: `external=True`, `non_hermetic_argv=None`, `held=True`.

`.ufo/evidence/round-24/replay/live-dependent.json` contains `{"live_dependent": ["pin-disposition-read","verify-round15"], "revision_pinned": 41, "rows": 43}`.

### Tool selftest vs ruler
`tools/registry-replay.py:203-204` (cases `external` and `non-hermetic`) and `:221-222` (which asserts `revision_pinned == 0`) test each branch separately. The registry row `registry-replay-selftest` (`tools/registry.json:991-998`, expecting `10/10 pass`) therefore guards some of these weakenings. The frozen ruler K10 does not.

### Ruler integrity
- `sha256(measure.py) = 0a7f6daa…57daa64`, which equals `before.json.instrument_sha256`.
- `git diff --stat e338f1b HEAD -- measure.py contract.json before.json` returns empty, so nothing changed after the freeze.

## Counterexamples (weaker implementations that pass K10)

| # | Weakening applied to `tools/registry-replay.py` | K10 at frozen ruler | Production consequence | Caught elsewhere? |
|---|---|---|---|---|
| W1 | Line 99 becomes `if result.get('non_hermetic_argv'):`, dropping the `external` disjunct | **passes**: the fixture still has `non_hermetic_argv` [INFERENCE] | On the actual observations, `verify-round15` (external, no `non_hermetic_argv`) is omitted. The result is `live_dependent=['pin-disposition-read']`, `revision_pinned=42`. This is exactly the defect "live-dependent rows reported as revision-pinned" (`corpus/knowledge/replay-projection-hardening.md:19`) | the tool selftest `external` case fails (9/10); **K10 does not** |
| W2 | Line 105 becomes `'revision_pinned': len(receipts)` | **passes**: `revision_pinned` is never read [INFERENCE] | `live-dependent.json` would claim 43 pinned + 2 live out of 43 rows, which double-counts live rows as pinned | the selftest asserts `revision_pinned == 0`; **K10 does not** |
| W3 | Delete the `live-dependent.json` write (lines 125-127) | **passes**: only stdout and `bundle.json` are checked [INFERENCE] | The persisted replay directory (`bundle.json` + `expected.json`) no longer lists any live row. A reader of the retained evidence sees an all-pinned bundle | **neither** K10 **nor** the tool selftest checks the file |
| W4 | `live = [all row names] if any(external) else []` | **passes**: the single-row fixture cannot test per-row attribution [INFERENCE] | All 43 actual rows would be marked live-dependent | the selftest is also single-row; **not caught** |
| W5 | Line 99 becomes `if row.get('external') is True:`, dropping the `non_hermetic_argv` disjunct | passes [INFERENCE] | None under the real runner, because held `non_hermetic_argv` implies `external` (`registry-check.py:666-671`). This is a non-discriminated tradeoff, not a material defect | selftest `non-hermetic` case |

Of these, W1 is the strongest. It is plausible because `registry-check.py:38` and the replay docstring (lines 10-12) both present `non_hermetic_argv` as *the* hermeticity signal. It also shows up concretely on the retained real replay, through `verify-round15`.

## Vacuity / wrong-reason checks (none found)
- **Tool missing:** `measure.py:143-144` reports `tool-absent`, giving `discriminated=False`.
- **Tool crash or non-JSON stdout:** `report={}`, so `live_dependent` is `None`, not `['one']`, and the check fails.
- **Implementation that lists every row unconditionally:** the control requires `creport.live_dependent == []` (line 184). The key must be present, because `.get()` returning `None` does not equal `[]`.
- **Implementation that refuses to publish live rows:** fails K10, which requires `exit == 0` and `bundle`.
- **Other findings:** `control_ok` (line 170) requires exit 0, `finding_ids == []` and a bundle, so it cannot be satisfied by an erroring tool.

## Base honesty (`before.json`)
The base value for K10 is honest: `discriminated=false`, `reason="tool-absent"`.
- `git cat-file -e 6a1821a:tools/registry-replay.py` reports that the file does not exist in the base revision.
- The retained before clone `/tmp/tameshi-r24-before-YdP3/lane` has HEAD `6a1821a…` and has no `tools/registry-replay.py`.
- Base absence is also substantive, not only structural. The predecessor `.ufo/evidence/round-23/replay.py@6a1821a` has no `external`, `hermetic` or `pinned` handling; lines 65 and 82-84 only count `held`. The base registry already had the same two active external rows. So the base replay did report every row as pinned, and that is the defect K10 targets.
- `before.json` records `revision=6a1821a`, the matching `instrument_sha256`, `exit=1` and `1/11`. Its K10 row shape matches `measure.py:144`.

## Impacted axes
- **Calibration (primary).** K10's pass does not exclude W1, W2, W3 or W4, so `target 11/11` overstates what K10 discriminates.
- **Provenance (secondary, implementation).** `expected.json` pins only `bundle.json`. `bundle.json` has no live marker, and `command-binding.py` rejects unknown bundle keys. As a result, the "listed" claim lives only in an unpinned side file (`live-dependent.json`) and on stdout. `replay-gate.json` verifies the bundle without awareness of live rows. This is a tradeoff to disclose, not a K10 failure.

## Smallest safe correction
The ruler is frozen (contract `e338f1b`), so editing K10 now would be a new contract. Two corrections follow.

1. **Successor ruler.** Change K10 in the next contract only, splitting the fixture by disjunct and adding a mixed row:
   - (a) `obs(external=True)` with no `non_hermetic_argv`;
   - (b) `obs(non_hermetic_argv=['/live/root'])` with `external=False` and `held=True`;
   - (c) a two-row observation set with one hermetic row and one external row.

   For each case, require:
   - exact `live_dependent`;
   - `revision_pinned == rows - len(live_dependent)`;
   - `out/live-dependent.json` content equal to the report's `live_dependent`, `revision_pinned` and `rows`.

   This kills W1 through W4 without touching the tool.
2. **This round, without moving the frozen numbers.** Record in the round24 lesson or bounds that K10 checks one combined fixture. Per-branch, count and side-file coverage currently rest on `registry-replay-selftest`, which itself does not cover W3 or W4.

Not claimed: producer authentication, promotion, historical R17-CMD-BIND closure, or numeric score uplift.
