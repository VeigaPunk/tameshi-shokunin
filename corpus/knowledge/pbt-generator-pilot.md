source: S269 — https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf — §Abstract (p. 268), §2.4 Monitoring Test Data (p. 270), §3.2 Generators for User-Defined Types (p. 271), §5.1.4 A False Sense of Security (p. 274) — Claessen & Hughes, ICFP 2000, DOI 10.1145/351240.351266; snapshot sha256 bfddcaa6, opened 2026-10-26
source: S270 — https://smallbone.se/papers/lic.pdf — §2.10 Generating Test Data, printed p. 34 — Smallbone, Chalmers TR 76L, 2011; snapshot sha256 eaee48f9, opened 2026-10-26
verified-at: 2026-10-26
recheck: 365d — `pdftotext .ufo/waves/round-49/w1/T49ScribeRows.src/smallbone.pdf - | tr -s ' \n' ' ' | grep -c 'that fit the program at hand'` (expect 1) and the same over `quick.pdf` for `print out a histogram of these values` (expect 1)
ground: F10 (PBT generators for gate fixtures)

# A property-based generator for a fixture gate: written to the gate's contract, observed by class, scored by mutants it never saw

Round 49 (claim C2) built one generator, `tools/pbt-staged-id.py`, against one named gate, `tools/staged-id-guard.py`
(the round-43 pre-adoption id guard, sha256 `03a796c5…`, never edited). This entry states what the two sources teach
about generators, what the lane built from it, how the build is measured, and what the measurement does not reach.
Measured values live in the deciding receipt `.ufo/evidence/round-49/after/c2.stdout`, never in this text.

## What the sources state

- **A property is an executable function over random input, and the generator is a separate artefact the tester writes.**
  S269, Abstract (p. 268): "Properties are described as Haskell functions, and can be automatically tested on random
  input". §2.4 (p. 270): "QuickCheck provides support for the programmer to define his or her own test data generators,
  with control over the distribution of test data".
- **The distribution must be observed, not assumed.** S269, §2.4 (p. 270): "The combinator collect will gather all values
  that are passed to it, and print out a histogram of these values." §5.1.4 (p. 274) names the failure this guards
  against: "the false sense of security that can be engendered when one's program passes a large number of tests in
  trivial cases".
- **Size is the tester's knob.** S269, §3.2 (p. 271): `sized` "generates an a by passing the current size bound to its
  parameter", and "It is then up to the programmer to interpret the size bound in some reasonable way during test data
  generation."
- **The generator must fit the program at hand.** S270, §2.10 (printed p. 34): "the quality of the test data determines
  the quality of the generated equations", and "it is important to provide good test data generators, that fit the
  program at hand"; the same page warns that "creating custom generators is sometimes necessary to get correct results".

## What the lane built

- **Written to the gate's documented contract, through its CLI only.** The generator never imports or execs the guard;
  it runs `python3 -I GUARD --registry R --staged G [--map M] --json` per case and checks the answer against its own
  oracle, written from the guard's docstrings: the CORPUS census row rule (0-3 leading spaces), collisions sorted by
  number, held/unmapped by form-insensitive document key, the naive map and its cascade, and the map-validation rules.
  The guard's exit semantics are taken as observed (0 answered/admitted, 1 analysis refused or map inadmissible,
  2 setup refusal); its module docstring names exit 1 only for an inadmissible map — a documentation imprecision recorded
  in `corpus/lessons/round-49.md`, not a guard edit.
- **Fit to the program at hand (S270).** Cases are small markdown registries and staged tables (0-8 rows) built from
  per-class recipes: indentation 0-6 spaces including 4+ (not a row under the census), ids of 3-5 digits, duplicate ids
  and short rows (must refuse), URL form variants (scheme, `www.`, case, trailing slash), undocumented rows, cascades,
  and admissible and inadmissible maps for each map rule.
- **Distribution printed, per class (S269 §2.4).** Every run prints the count of each of twelve classes (the frozen
  list in `.ufo/evidence/round-49/contract.json` `claims.C2.classes`); the round-49 counter recomputes the classes from
  the dump with its own predicates and requires at least 10 cases each at seed 4949, 400 cases.
- **Deterministic and replayable.** `random.Random(seed)`; the dump holds every case run; the first violation stops the
  run and names its index (the counterexample).

## How it is measured, and the control

The frozen counter `.ufo/evidence/round-49/c2/measure.py` runs the generator on the pristine guard (no violation
allowed, and its own oracle must agree with the guard on every analysis case), then on each mutant of a twelve-mutant
panel that was hidden from the generator's author until the deciding run (commit-reveal: the contract pins its sha256).
A mutant counts only when the generator's counterexample makes the pristine and the mutant guard print different
answers (differential confirmation). The fixture-replay control — the guard's own 14 selftest fixtures with golden
outputs, through the same interface — confirms 6 of the 12 (`.ufo/evidence/round-49/control/c2-controls.stdout`); a
hand-made witness set confirms all 12, so no panel mutant is equivalent.

## What this does not establish

- One generator against one lane-owned gate: F10's "one generator against a named fixture gate" move, not a method
  shown across the fleet's gates.
- No shrinking: a counterexample is the first failing case, not a minimal one.
- The counter cannot tell a property-based generator from a differential one that compares the mutant with a copy of
  the pristine guard (wave-1 critic, `.ufo/waves/round-49/w1/T49CritC2Contract.md` F1); the evidence that this one is
  property-based is outside the counter: its code (CLI calls only, its own oracle), an access trace and oracle-mutation
  results in the round-49 wave-2 reports.
- Twelve mutants are a small panel; a kill count is a measurement of this panel, not a mutation score of the guard.
