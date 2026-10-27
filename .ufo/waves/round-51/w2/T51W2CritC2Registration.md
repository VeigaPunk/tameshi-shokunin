# T51W2CritC2Registration — C2 receipt and suite binding

## Axes

- **Depth:** whether the tenth recorded/wired leg and its associated artifacts satisfy the frozen predicate.
- **Calibration:** whether the reported sweep/table is genuinely supported by the observed suite, rather than a self-confirming receipt.
- **Operability:** whether a later verifier can reproduce and audit that result from committed material.

Read-only review; no lane or fleet mutation and no new sweep run.

## F1 — The sweep is reproducible only after supplying an unregistered suite

The exact frozen spec is `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`; its header declares in prose: `env -i … bash "$MUTANT" --selftest` (13 cases), alternate-baseline harness, exit-status oracle. It does **not** freeze the actual command template, environment, sandbox naming, harness bytes, or a suite digest. The spec does freeze ten mutation substitutions and their KILLED/SURVIVED predictions; the spec SHA is compiled into the counter (`measure.py:38`), and the counter compares the embedded heredoc to the spec (`:250`). `T51CritPrereg.md` F1–F3 reports the spec added once in `fe335384`, byte-identical `sweep/spec.copy`, all ten `@old` strings uniquely present in pinned bytes, and seven of ten predictions matching the recorded sweep. These facts authenticate the mutation definitions and prediction text, not the test execution protocol.

Evidence: `T51CritPrereg.md` F1–F4; spec lines 1–7; `measure.py:38, 250`; contract C2 lines 33–43. The spec's single prose suite sentence is not machine-readable registration. A later verifier cannot derive the table solely from frozen spec bytes without guessing a suite implementation.

## F2 — Frozen counter checks receipt shape/consistency, not suite provenance or actual execution

The counter accepts a sweep if `sweep_check()` finds a green CONTROL with pin match, one verdict line per spec ID without `INCONCLUSIVE`, restore/done markers, and parseable date after the spec's first-add commit (`measure.py:134–159`, `:262–275`). It does not read `results.tsv` or `evidence/*.out`, nor bind `MUTATE_TOOL`, `MUTATE_SPEC`, a suite command, suite hash, path naming, or external timestamp. `TABLE_DRIFT` is compared against parsed sweep verdicts; the ledger table is therefore tied to the receipt text, not to independently verified test output. `MUTATE_DATE` is a receipt field, not an independently witnessed time (`T51CritPrereg.md` F7–F8).

Thus the committed record can establish that the chosen sweep text is internally acceptable under the counter's parsers and that the candidate's leg table agrees with it. It cannot establish that the recorded suite generated that text. `T51MutC2Counter.md` F/MUT-1 and B1–B15 adds a direct counterexample to stronger provenance claims: its scratch forged tree passes the pristine counter while supplying a synthetic sweep, synthetic dated receipt, and runner that prints the expected regression banner. The counter's result is receipt consistency, not proof of execution.

## F3 — Neutral-path falsifier breaks the claimed 2/10 as a suite-independent measurement

The committed sweep says 2/10 killed and identifies K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN as survivors (`c2/sweep/sweep.txt:7–18,31`). But `T51LabSandboxLeak.md` §2–§4 rebuilt all ten mutants with SHA matches to the sweep, then changed only sandbox naming: id-named A reproduces 2/10; neutral B yields 5/10, with precisely those three changing to KILLED; C verdict-word naming resurrects K_GONE_ARM. Three repeats matched. The pinned target's selftest uses an unanchored grep over captured output while output includes scratch paths (§4), so the defect ID in the path can satisfy the expected verdict word despite the expected diagnostic being absent.

This is not a counterexample to the ten recorded legs existing; it is a falsifier of treating 2/10 and the three SURVIVED labels as suite-independent defect outcomes. The original measured receipt is consistent with the historical/id-named suite, but cannot be derived from committed bytes alone because that suite is not registered or bound. The 5/10 neutral result is an independently reproduced diagnostic, not a replacement frozen receipt/table and not the claim's deciding predicate.

## F4 — Exactly what is pre-registered versus prose/self-stamped

**Frozen / machine-bound:** ten defect IDs and exact old/new substitutions; predictions (5 KILLED / 5 SURVIVED) as spec text; pinned target identity and hash in spec/leg; spec bytes by SHA and exact embedded-heredoc equality; counter's table-to-sweep-text comparison; the receipt's stated dates and verdict-line structure. See spec and `measure.py:38, 134–159, 250–265`.

**Only prose or self-stamped/unbound:** suite invocation/environment details, the `sandbox-$DEFECT_ID` path convention, actual 13 test cases, oracle semantics as an executable check, runner identity at sweep time, `results.tsv` and per-case output corroboration, uniqueness/ordering of runs, and trustworthy wall-clock provenance. The suite form is described in spec prose but neither parsed nor hashed. The sweep self-reports `MUTATE_DATE`; the counter compares that text to git commit time, without external attestation. `T51CritPrereg.md` F4–F8 documents these limits. The neutral-name and verdict-word probes in `T51LabSandboxLeak.md` show why the unbound detail is outcome-determinative, not clerical.

## F5 — Do not silently replace the suite or table after seeing outcomes

Changing the suite to neutral naming after observing the 2/10 result changes three outcomes; changing to verdict-word naming can make a killed mutant pass. Therefore neither the committed 2/10 table nor a post-hoc neutral 5/10 table can be presented as the pre-registered measured outcome. The spec predictions are immutable in the candidate history, but the counter merely counts and reports prediction matches outside its PASS predicate (`measure.py:22,264–265`). Editing predictions after data would be a visible artifact/history change, but even unchanged predictions do not validate the oracle or force the suite. Replacing the sweep/table after seeing neutral results is also visible as a candidate change, yet the frozen counter has no independent receipt signature or suite binding that would prove which run was original. The safe treatment is to preserve the original receipt/table unchanged, retain the neutral-path result as a separately labeled falsifier, and make no claim that the 2/10 is a robust suite-independent kill-rate.

Evidence: `T51CritPrereg.md` F9; `T51LabSandboxLeak.md` §§3–5; `T51MutC2Counter.md` F/MUT-1 and §6. Avoid “correcting” either record by substituting the neutral results into the original table without a new, pre-registered measurement protocol; that would be post-hoc suite selection.

## F6 — Tenth-leg depth is a separate predicate from kill-rate, but this report does not verify its final candidate truth

The frozen C2 predicate separates structural depth from kill rate: it requires 10 ledger matches and 10 wired legs, exactly one new target, true blob pin, spec/hash/embedding match, receipt conditions, table equality, `--regression` passing ten cases, and source/README linkage (`measure.py:5–21, 272–279`; contract C2). Prediction misses are expressly outside the predicate; contract says they are data, not a kill (`contract.json` C2 kill_rule), and the counter prints `predictions_held` without requiring a threshold. Consequently, neutral-path 5/10 does **not**, by itself, invalidate the tenth-leg depth increment. Conversely, an internally consistent 2/10 receipt cannot prove depth: it does not supply the leg, wiring, regression, or sourced entry.

The prior `T51CritPrereg.md` F10 observed that at freeze/base the runner remained at nine legs and C2 failed. This review has not run the deciding counter at candidate REV, so does not assert `C2_R51_PASS=true` or independently verify the final tenth leg. The calibrated statement is conditional: **if** the frozen counter passes at candidate REV, the depth predicate can verify independently of whether the kill rate is 2/10 or 5/10; the receipt/provenance weakness remains a measurement-quality limitation, not a kill-rate clause in the frozen rule. `T51MutC2Counter.md` shows a deeper caveat: 15 single-edit weakening mutants survive its D1/D2/D3 detectors, and forged positive trees can satisfy the pristine counter; those checks do not independently close provenance.

## F7 — Smallest safe correction

Do not amend the frozen suite, spec, sweep, or table based on these outcomes. Preserve both observations with explicit labels (original id-named recorded receipt; neutral-name falsifier), and qualify any prose that calls the 2/10 a measured kill-rate without stating the suite-binding limitation. For a future measurement, freeze a machine-readable suite command/environment and suite digest before mutation runs; record/verifiably bind per-mutant output and runner bytes, and make the oracle independent of scratch-path tokens. This is a future protocol correction, not a retroactive change to this round's predicate or receipt.

## Exact evidence commands / pointers

Commands cited from the prior read-only evidence reports (not rerun here):

```sh
git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh
sha256sum .ufo/evidence/round-51/c2/bash-drift-pins.defects.spec .ufo/evidence/round-51/c2/sweep/spec.copy
python3 .ufo/evidence/round-51/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain
```

Pointers: `T51CritPrereg.md` §§F1–F10; `T51LabSandboxLeak.md` §§1–5 and `T51LabSandboxLeak/README.md` table/raw receipts; `T51MutC2Counter.md` §§2–6 and `receipts/run-pristine-tall.txt`; candidate `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`, `sweep/sweep.txt`, `measure.py`; `.ufo/evidence/round-51/contract.json` C2 predicate and kill rule.
