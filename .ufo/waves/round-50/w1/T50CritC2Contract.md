# T50CritC2Contract — C2 (F6 shrinker) design falsification

Seat: `T50CritC2Contract` (UFO-FSD critic). Item: falsify C2's design; findings disclosed; no verdict on the claim. The frozen counter is used only as an instrument in scratch trees (never deciding). Report targets the counter/controls design, not the task owner.

## Sources read
- `contract.json:46-67` (claim C2), `contract.json:54` (shrinker interface), `contract.json:56` (hidden panel selection), `contract.json:59` (cannot_see).
- `.ufo/evidence/round-50/c2/measure.py` (frozen counter; self=`c3da7e59abf2` matches control receipts).
- `.ufo/evidence/round-50/control/c2-controls.py`, receipts `c2-CTL_ABSENT/IDENTITY/REF.stdout`, `c2-selftest.stdout`, `c2-controls.stdout`.
- `tools/staged-id-guard.py`, `tools/pbt-staged-id.py`, `.ufo/evidence/round-49/c2/panel.json`.

## Method (scratch evidence; commands that show it)
- Scratch: `S=/fast/scratch/hyaku/tameshi-r50/T50CritC2Contract`; lane cloned at freeze `cdbf24c07f9be3a991997c25b1f1d4bb375014ae` (`git clone -q --shared --no-checkout … "$S/lane"`; `git -C "$S/lane" checkout -q --detach cdbf24c0`; `git -C "$S/lane" rev-parse --show-toplevel` prints `$S/lane`).
- Counter exercised end-to-end through `measure()` (as the selftest does) on scratch clones, in scratch work dirs; public panel = frozen round-49 panel (sha256 `d6dd2cf3…` = frozen default pin). Hidden side uses a **synthetic** 8-mutant panel built by me (each mutant verified found by the frozen generator at seed 4949; sha256 `04905f9f…`); the real hidden panel was not read (`/home/vgpnk/.local/state/` untouched).
- Scripts: `prep.py`, `prep2.py` (synthetic panel construction), `exp.py` (experiments; receipts below are its `python3 "$S/exp.py"` output). The frozen counter was driven through `measure()` (as its own selftest does) on scratch clones into scratch work dirs.

---

## Finding 1 — SEVERE — the "stated cost in guard runs" is not enforced; the run log is controlled by the audited party

**Where:** `measure.py:62-64` (INSTRUMENT snippet), `measure.py:82-88` (injected before first top-level import), `measure.py:275-277` (shrinker subprocess, cwd=`shr/`), `measure.py:281-284` (`logged` = line count of `.runs` in `shr/`), `measure.py:300-301` (`cost` requires `out['runs'] == logged`, plus recomputed unit counts).
The run logger appends to `.runs` next to the guard copy — but the **shrinker process itself owns that directory**, so both sides of the equality are under its control:

- It can invoke the guard without logging: the `--pristine/--mutant` files are the only instrumented copies, and the instrumentation is three predictable lines (`import os as _r50_os` + a `with open(…,'a')` block). A shrinker can copy the file, drop those three lines, and run the stripped copy. It can also read the counter's own uninstrumented originals at `../ver/pristine.py` (created at `measure.py:250-258`, reachable from `cwd=shr`).
- It can fabricate `.runs` lines to match any claimed number; nothing checks who wrote the file.

**Demonstration (frozen counter, PASS):** `SILENT` = the counter's own reference greedy shrinker (`REF_SHRINKER` in `measure.py:375-418`), but every guard invocation routed through an instrumentation-stripped copy, reporting `runs=0`. Counter receipt (my run, `exp.py`):
```
MUTANT M01 panel=public … units=8->1 runs=0 logged=0 … kills=1 minimal=1 cost=1 reduced=1 OK
… (M01..M12, H02..H13 all OK) …
C2_R50: self=c3da7e59abf2 … mutants=20 ok=20 units_before=166 units_after=35 …
 total=0 C2_R50_PASS=true
```

Sidecar `true_runs.txt` (written by the shrinker, not the counter) recorded **15 real guard subprocess invocations for m00 alone** — real greedy search ran, the certified statement said zero runs, and the counter passed. Symmetrically, padding `.runs` with fake lines is trivially accepted (equality holds by construction).

**Impact:** the predicate's "stated run count equal to the logged guard invocations" is vacuous; the F6 entry's cost claim is unverifiable; a buggy or adversarial shrinker can report anything. This does not weaken the kill/minimality gates (Finding 6), only the cost claim.

## Finding 2 — SEVERE — "reduces by search" is not enforced; mutant identification makes offline precomputation sufficient for 12/20

**Where:** `measure.py:130-145` (`is_subcase`), `measure.py:157-160` (judge kills), `measure.py:299` (minimality), `measure.py:171-184` (`find_case`: deterministic — same frozen generator bytes, seed 4949, 400 cases). The shrinker receives the full mutant source (`--mutant`) and pristine (`--pristine`), so it can identify exactly which of the 20 mutants it faces (hash or diff) and answer from a table precomputed offline; the counter re-derives each input case deterministically, so a precomputed answer is always a valid sub-case.

The sub-case rule only constrains **output provenance** (subsequence / map-subset / unchanged other fields) — it cannot tell whether the output was found by search, by analysis, or by lookup. Verified directly (`python3` in scratch): a freshly synthesized semantically-equivalent case fails `is_subcase` (`False`), while any extracted subsequence or map-subset passes (`True`).

**Demonstration (frozen counter, PASS):** `LOOKUP` = a shrinker that, for the 12 public mutants, prints a precomputed 1-minimal case keyed by `md5(mutant source)` (computed with the same greedy method offline) with `runs=0`, and falls back to the reference search for unknown (hidden) mutants. Counter receipt (my run, `exp.py`):

```
MUTANT M01 panel=public … units=8->1 runs=0 logged=0 … kills=1 minimal=1 cost=1 reduced=1 OK
… M01..M12 all OK (table hits), H02..H13 OK (fallback) …
C2_R50: … mutants=20 ok=20 … total=0 C2_R50_PASS=true
```

**Impact:** 12 of 20 certified mutants are reduced with zero runtime search and the counter cannot distinguish this from genuine delta-debugging. The claim surface (a shrinker that "reduces … and states its cost") holds for a table lookup. Smallest safe correction: require the shrinker to emit a trace of evaluated candidates (units removed, verdicts) so the method is observable; or scope the claim to "a 1-minimal sub-case exists and is produced" without asserting search.

## Finding 3 — MEDIUM — unit model: line-level 1-minimality is coherent but coarse; empty-fixture minima occur

**Where:** `measure.py:105-108` (units = registry/staged lines + map entries), `measure.py:111-122` (removals = one unit).

- Header/separator lines are parse-inert (guard `parse_rows` only matches `ROW_RE` rows, `staged-id-guard.py:80-84`), and none survive in any of the 12 public minimal outputs — except M01's single retained line, which *is* the row only the mutant's weakened regex recognizes (a 4-space-indented row): it is semantic, not decorative. So "header/separator as unit" is not a practical defect in this gate.
- The real granularity gap is intra-row: a row's 11 cells are inseparable, so a 1-minimal "fixture" can still carry superfluous columns.
- Degenerate minima exist: two synthetic hidden mutants minimized to `units_after=0` (empty registry/staged/map) and still passed `kills=1 minimal=1` — the kill is then a behavioral difference on empty input, and the "fixture" is nothing. The README/interface should state the unit definition and that empty minima are possible.
- Note: greedy order-dependence means several distinct 1-minimal subsets of different composition can exist; "the minimal" is not canonical (fine for the claim, but wording should say "a 1-minimal sub-case").

## Finding 4 — LOW — CTL_REF positive control and F6 "held" wording

**Evidence:** `control/c2-CTL_REF.stdout:22` shows `C2_R50_PASS=true` for the counter's own ~25-line greedy-to-fixpoint loop (`REF_SHRINKER`, `measure.py:375-418`). This is exactly what the contract scopes (`contract.json:59`: "A plain greedy-to-fixpoint loop meets the bar … the claim is the capability and the method with its cost, not a search-efficiency result"). So F6 `held` is calibrated and justified *for the scoped claim*. The only mismatch is presentation: `records()` requires a README line containing "held (round 50)" (`measure.py:329-330`), which will read as generic frontier completion; the README should keep a scope qualifier (e.g., "for the staged-id-guard panel"), as the controls themselves do ("control fixture").

## Finding 5 — LOW/MEDIUM — generality: the hidden panel is 8 mutants from the same gate

**Evidence:** `contract.json:56`: hidden mutants are those found by the **same** frozen generator at seed 4949 ("of 12 candidates, the 9 found, minus one whose counterexample duplicated another's"); public 12 come from the same generator/gate. All 20 share generator bytes, seed, 400-case stream, oracle, and guard. Selection was by "found", not by difficulty or diversity, so there is no cross-gate, adversarial, or out-of-distribution probe. F6's theme ("fixture minimization for survivors") overstates what one guard×one generator can certify. Acceptable if the claim stays scoped; not enough to motivate a general F6-`held` claim.

## What the counter does enforce well
- Kill, subset and 1-minimality are re-verified independently by the judge against the frozen generator (`measure.py:157-160,299`): identity (CTL_IDENTITY false), fabricated content (selftest non-subset), missing/absent shrinker, bad selftest rc, missing F6 records, panel digest mismatch, and misreported unit counts all fail (`c2-selftest.stdout:1-9`).
- `units_before/units_after` are recomputed, not trusted (`measure.py:300-301`).

## Smallest safe corrections
1. Make the run log counter-owned: materialize the uninstrumented originals only after the shrink phase (or remove them), pre-create `.runs` read-only to the shrinker, and snapshot before/after; at minimum, change the `cost` check from equality to a monotone counter verified against process-level execution of the guard copies the counter itself handed over.
2. Require a shrink trace (list of candidates with verdicts) so the method is observable; otherwise downgrade the claim to "produces a verified 1-minimal sub-case" without asserting search or stated cost.
3. Document unit granularity and degenerate-empty minima in the interface/README.
4. Add a scope qualifier to the README F6 line.
5. Broaden future hidden panels across generators/seeds and select adversarially.

## Summary
- Cost reporting is unverifiable: the audited shrinker owns the log (SILENT: real search, runs=0, PASS).
- "Reduces by search" is unobservable: hashing/diff + precomputed table passes 12/20 with zero runs (LOOKUP: PASS).
- Sub-case rule blocks fabricated content but not extraction/lookup; kills/minimality are genuinely judge-enforced.
- Line units behave (headers dropped; only semantic non-data line kept), but cells are inseparable and empty-fixture minima occur.
- F6 `held` is justified only as calibrated by CTL_REF and scoped to one gate; README should say so.
- Hidden panel (8, same seed/generator/gate) is not a generality probe.
- No verdict on C2; these are design findings with the smallest safe corrections above.
