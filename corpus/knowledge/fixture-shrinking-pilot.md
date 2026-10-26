source: S271 — https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf — §I Introduction ("Simplification of test cases"), §III-A Definition 10, §IV-B Fig. 12 — Zeller & Hildebrandt, IEEE TSE 28(2), February 2002, DOI 10.1109/32.988498; course-mirror PDF opened 2026-10-26, 247,738 B, sha256 7ed0c812, snapshot `.ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf`
source: S022 — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 — Abstract — MacIver & Donaldson, "Test-Case Reduction via Test-Case Generation: Insights from the Hypothesis Reducer", ECOOP 2020, DOI 10.4230/LIPIcs.ECOOP.2020.13; abstract re-read 2026-10-26 (`.ufo/waves/round-50/w1/T50ScribeSrcHeld.md`)
source: S024 — https://www.fuzzingbook.org/html/Reducer.html — §Delta Debugging — The Fuzzing Book (Zeller et al.); snapshot `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html`, sha256 3abede35, re-read 2026-10-26
verified-at: 2026-10-26
recheck: 365d — `curl -fsSL 'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf' | pdftotext - - | tr -s ' \n' ' ' | grep -c 'removing any single input entity would cause the failure to disappear'` (expect 1); `sed 's/<[^>]*>//g' .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html | tr -s ' \n' ' ' | grep -c 'every character contained is required to produce the error'` (expect 1)
ground: F6 (fixture minimization for survivors)

# A fixture shrinker for a mutant's killing case: 1-minimal by single-unit removal, valid on the pristine gate, and costed in guard runs

Round 50 (claim C2) adds one shrinker, `tools/shrink-case.py`, for one gate pair: the round-43
pre-adoption id guard `tools/staged-id-guard.py` (sha256 `03a796c5…`, never edited) and the round-49
generator's oracle `tools/pbt-staged-id.py` (frozen at `7d3d977f`, sha256 `0cbee392…`). Its input is
the generator's counterexample — the first failing case — and its output is a sub-case of that case
from which no single unit can be removed without losing the kill, with every guard invocation it made
counted. It is the piece the round-49 entry named as missing: "No shrinking: a counterexample is the
first failing case, not a minimal one" (`corpus/knowledge/pbt-generator-pilot.md`, §What this does not
establish). Measured values live in the round's deciding receipt — `deciding-run.sh` writes each
counter's stdout into the `OUTDIR` it is handed — never in this text.

## What the sources state

- **1-minimality is a removal property, not a size.** S271, §I: "It stops when a minimal test case is
  reached, where removing any single input entity would cause the failure to disappear." S024 states
  the same result property for its own reducer: "Its result is 1-minimal, meaning that every character
  contained is required to produce the error". Neither source treats "reduced" as "small": the witness
  is that every remaining entity is load-bearing.
- **The cost is part of the result, and its unit is test runs.** S271, §I: "After 57 tests, the
  original 896-line HTML input is reduced to the minimal failing test case" — one reduction, one run count
  (the Abstract's 139 runs is the case study's two reductions summed, 82 + 57; see
  `corpus/knowledge/delta-debugging-minimization-contract.md`). A reduction reported without its run count
  cannot be compared with another reduction; runs are also the unit the lane counts everywhere else.
- **A reduced case must still be a valid input.** S022, Abstract: internal reduction works "internally,
  to the sequence of random choices made during generation", which "significantly mitigates the impact
  of the test-case validity problem, by ensuring that any reduced test case is one that could in
  principle have been generated". The lane's check is the same idea made operational without a
  generator on the other side: the shrunk case must still be answered by the pristine guard exactly as
  the round-49 oracle expects — otherwise it is not an input of this gate at all, and its effect on the
  mutant says nothing.
- **A reducer cannot manufacture an interesting input.** The lane's round-29 F6 attempt ran ddmin over
  a fixture for which no subset was interesting, and kept nothing: "ddmin made 171 oracle tests and
  kept nothing, because no subset kills" (`corpus/knowledge/survivor-fixture-minimization.md`, §What
  happened). Round 49 then supplied exactly what that attempt lacked: a case that violates, found by
  the frozen generator at seed 4949 over 400 cases and dumped with its index.

## What the lane built

- **One shrinker, one gate pair, one starting case per mutant.** `tools/shrink-case.py` takes a case in
  the generator's dump format (`{registry, staged, map}`), a pristine guard and a mutant guard, and
  writes `{case, runs, units_before, units_after}`. The interface is frozen in the round's contract
  (`claims.C2.shrinker_interface`): `--pristine P --mutant M --case CASE.json --out OUT.json`, plus
  `--selftest`; it may import `pbt-staged-id.py` from its own directory; standard library only;
  deterministic; exit 2 with a reason on a setup error. It edits neither guard.
- **Units are the generator's own granularity.** A unit is one registry line, one staged line, or one
  entry of `map['map']` when the case carries a map; every other field of the map document is held
  fixed. The counter counts units the same way and enumerates every single-unit removal from the
  emitted case, so the unit definition is not the shrinker's private choice.
- **Interestingness is the round-49 oracle, through the guards' CLI.** The generator's `check` compares
  a guard run with its own re-implementation of the guard's round-43 rules; `run_guard` writes the
  three inputs and calls the guard as a subprocess. A kill is: `check` returns None on the pristine
  guard (the case is answered as the oracle expects, including a setup refusal with its reason) and
  non-None on the mutant.
- **Method: delta debugging to a fixpoint, with verdict caching.** Drop chunks of decreasing size, try
  one chunk as the new set, refine the granularity, then a single-unit pass to a fixpoint — the last
  pass restates 1-minimality directly rather than relying on the search above it. Verdicts are cached
  by case content, so no case is run twice, and every guard invocation, pristine and mutant, is counted
  into `runs`.
- **Selftest.** `--selftest` runs the search on synthetic interestingness predicates (a sentinel that
  requires one unit, a size floor that leaves a 1-minimal set of three, an unsatisfiable predicate, an
  always-true predicate), a stub CLI end to end, and — when the guard and the generator sit beside the
  tool — the public round-49 panel's M02 edit against the real guard.

## How it is measured, and the control

The frozen counter `.ufo/evidence/round-50/c2/measure.py` (label `C2_R50_PASS`) takes nothing on the
shrinker's word. For each mutant of the 20-case panel — the 12 public round-49 mutants
(`.ufo/evidence/round-49/c2/panel.json`, sha256 `d6dd2cf3…`) and 8 hidden round-50 mutants, whose digest
the contract pins and which the deciding script reads from the revision under test — it finds the
counterexample with the frozen generator (rev `7d3d977f`, seed 4949, 400 cases), hands the case to the
shrinker at the revision under test, and then judges the emitted case itself:

- **sub-case**: registry and staged lines must be subsequences of the original, map entries a subset,
  every other map field equal;
- **kill and 1-minimality**: the counter re-runs the oracle on the pristine and the mutant guard for the
  emitted case, then for every case with exactly one unit removed — each such case must no longer kill.
  This is S271's stopping rule applied at the lane's unit granularity, checked by the measurer, not
  attested by the tool;
- **cost**: both guards are instrumented copies that log every invocation to a `.runs` file; the stated
  `runs` must equal the number of logged invocations, and `units_before`/`units_after` must equal the
  counter's own counts of the original and emitted cases;
- **records and selftest**: `corpus/README.md` carries a line naming F6 and `held (round 50)`, a
  knowledge entry new since base names F6 and cites a mined SOURCES row opened 2026-10-26, and the
  tool's `--selftest` exits 0.

PASS requires at least 19 of the 20 mutants to be ok on every check, with the ok mutants shrinking in
total. The counter's own 9-case selftest drives `measure()` end to end on a fixture repo with four
shrinkers — reference, cost-liar, identity, non-subset — plus an absent shrinker, a failing tool
selftest, missing records, a panel-digest mismatch and an instrumentation check
(`.ufo/evidence/round-50/control/c2-selftest.stdout`: `cases=9 failed=0`); that shape is deliberate,
because round 49's counter selftests never reached `measure()`. The positive control is the counter's own greedy-to-fixpoint reference shrinker: at freeze
bytes it meets the bar on the whole panel, 20/20, units 164 → 43 (`.ufo/evidence/round-50/control/c2-CTL_REF.stdout`,
last line). The panel is therefore reachable, and a plain greedy loop suffices; what this entry adds is
the capability with its stated cost, not a search result.

## What this does not establish

- Units are lines and map entries, not cells. A shrinker cannot cut inside a line — an id, a URL, one
  table cell — so the smallest reducible entity is a whole line or one map entry, and a case cannot be
  reduced to the single cell the mutant actually needs.
- The starting cases are the round-49 generator's tiny cases (small markdown registries and staged
  tables, two to eight rows across the pair). A reduction of a directory fixture, a long log or a
  compiled input is not measured here.
- A greedy-to-fixpoint loop meets the same bar (the positive control above). No claim is made that
  ddmin beats greedy; the logged run count makes such a comparison possible, not concluded.
- F6 names fixture minimization *for survivors*. These mutants are killed by the generator's case, not
  survivors of a fixture battery, and the round-29 B5 survivor stays masked
  (`corpus/knowledge/survivor-fixture-minimization.md:53,57`); the F6 move this entry carries is the
  method on killing cases, B5 is not discharged.
- One lane-owned gate and its 20 mutants. The hidden 8 probe generalisation over mutants found at one
  seed, not over other gates, other seeds, or other unit definitions.
- A kill is oracle agreement, not admission: the pristine side counts as passing when the guard's
  answer matches the oracle, which includes a setup refusal. The counter also cannot tell a 1-minimal
  sub-case a reader can interpret from one that is merely small and still interesting.
- The counter sees the search only through its logged cost and the resulting case; chunk order and
  cache reuse are outside the measurement.
- Under the counter's copy layout only the generator sits beside the shrinker, so the tool's
  real-guard selftest leg is skipped in the measured run (14 cases there, 21 when the guard sits beside
  it). The selftest the counter accepts is the synthetic and stub-CLI part; the real-guard leg is
  evidence outside the counter.
