# CriticEquivalence — round 26, wave 1: attack on the js-cite-check 5/10 headline

Seat: TameshiR26.CriticEquivalence (critic, leaf). Date: 2026-10-22. Scratch: /tmp/crit-equiv-r26
(pinned blob, rebuilt mutants, fixtures, lane clone at a08e85c). Nothing in the lane was edited.
No tools were installed or upgraded.

## Verdict

1. **S_EMPTY_GUARD is an equivalent mutant.** This is a proof, not a probe: the two verdict expressions
   agree on every input. The other four survivors are real suite gaps; each has an off-suite witness below.
2. **The recorded table must not change.** Keep `TABLE_CITECHECK`, `results.tsv`, the spec, the predictions
   and the ledger row `5/10` as they are. SURVIVED is what was measured. "Equivalent" is an analysis
   label, and a recorded table holds measurements only.
3. **The entry text must change.** It should say that one of the five survivors is equivalent code (a
   calibration item, not a gap, per `SKILL.md:221-223`). It should also say that only 9 of the 10
   "held" predictions could have failed.
4. **PIT and Stryker would both report a higher number, and the two differ from each other.** PIT 1.25 or
   later counts EQUIVALENT as detected, giving 6/10. Stryker's Ignored drops the mutant from the score,
   giving 5/9. Re-scoring after the sweep is a favourable move made after the fact on a pre-registered
   5/10. It must stay a side note, never the headline.
5. **The real hole sits next to S_EMPTY_GUARD.** Dropping only the resolved-citations guard survives all
   62 cases and is not equivalent. It is a candidate for a later round, not for this frozen table.

## 1. Counterexample: S_EMPTY_GUARD is equivalent (proof)

The spec's mutation (`cite-check.defects.spec`, defect S_EMPTY_GUARD) applied to `cite-check.mjs:1590`:
`totals.filesScanned > 0 && totals.resolved > 0 && !drift` becomes `totals.resolved > 0 && !drift`.

The two are equal for every input exactly when `resolved > 0` implies `filesScanned > 0`. The pinned
bytes (rev 1205c66, sha256 4057344…0c9f, re-hashed this session) show:

- `totals` is a local of `runCheck`, created with both counters at 0 (`:1543-1550`). Nothing else
  writes either counter: `totals.` occurs only inside `runCheck` (`:1543-1590`). The later reads
  (`:1617`, `:1626`, `:2527-2528`) happen after the verdict is fixed.
- In one iteration of `for (const rel of docs)`, the order is: `readFileSync`, which on failure runs
  `continue` and skips both counters (`:1555`); then `totals.filesScanned++` (`:1556`); then, further
  down, `if (f.kind === 'OK') totals.resolved++` (`:1583`).
- So every increment of `resolved` comes after at least one increment of `filesScanned`. That makes the
  `filesScanned > 0` conjunct redundant in the verdict. The mutant changes no output byte and no exit
  code. This is stronger than the round-gate CKIND precedent, which was equivalent "for gate behaviour"
  only (`corpus/knowledge/mutation-case-kumitate-round-gate.md:91-96`).

The spec's own reason argues only about the empty-scan input: "an empty scan set also has zero
resolved citations… (co-extensive guard)" (`cite-check.defects.spec`, S_EMPTY_GUARD block). Under the
proof above, "co-extensive" really means "equivalent". The defect was labelled hole-aimed, but there is
no hole for it to aim at.

**Differential corroboration** (my harness `probe.sh`; output in `/tmp/crit-equiv-r26/probe.stdout`):

    DIFFERENTIAL S_EMPTY_GUARD runs=316 identical=316 differing=0 pristine_PASS=20 pristine_FAIL=296 filesScanned0=32 filesScanned0_with_resolved>0=0
    DIFFERENTIAL K_EMPTY_VERDICT runs=316 identical=275 differing=41 ...

The 316 runs are 158 fixtures (8 hand-built edge cases plus 150 seeded random documents), each run
with `--json` and with `--json --strict`. The edge cases are: empty self; unreadable `SKILL.md`
(mode 000); `SKILL.md` as a directory; no citations; only bogus citations; one good citation; corpus
only; and an unreadable corpus document. "Identical" means stdout, stderr and exit code all match. The
K_EMPTY_VERDICT control shows the harness does see verdict differences.

The rebuilt mutants match the sweep byte for byte: all ten sha256 values equal `results.tsv` column 5
(`MUTANT_SHA_MATCH`). The recorded evidence agrees: `sweep/evidence/S_EMPTY_GUARD.out:22`
`PASS fail-closed: empty scan set → exit-2 condition — filesScanned=0 verdict=FAIL`, and `:65`
`62/62 cases passed (hermetic)`.

## 2. The other four survivors are not equivalent (off-suite witnesses, observed)

| survivor | input | pristine | mutant |
|---|---|---|---|
| S_OOR_EDGE | cite `lib/a.txt:21` in a 20-line file | rc=1, `LINE_OOR` | rc=0, `VERDICT: PASS` |
| S_STRICT | one ownerless `:424242` (single `ORPHAN_REF` warning) plus one OK, with `--strict` | rc=1, `VERDICT: FAIL` | rc=0, `VERDICT: PASS` |
| S_PIN_INCLUDES | `sha256 <digest[1:13]>` after a cited file | rc=1, `PIN_MISMATCH` | rc=0, `VERDICT: PASS` |
| S_USAGE | `--bogus` | rc=64 | rc=65 |

So the survivors split into 4 suite gaps and 1 equivalent. The headline 5/10 stays; its reading
changes.

## 3. How PIT and Stryker treat equivalent mutants (all sources opened 2026-10-22 ~10:57Z with curl)

- PIT, https://pitest.org/quickstart/basic_concepts/ — "not all mutations will behave differently
  than the unmutated class. These mutants are referred to as equivalent mutations." Also: "PIT avoids
  generating this type of equivalent mutation by not generating mutations for lines that contain a call
  to common logging frameworks". That is filtering before generation, not relabelling after a run.
- PIT, https://raw.githubusercontent.com/hcoles/pitest/master/pitest/src/main/java/org/pitest/mutationtest/DetectionStatus.java
  — `EQUIVALENT(true)`, documented as "Mutation is equivalent to the un-mutated code. Treated as detected
  although by definition it cannot be." The status was added in 1.25.0: README changelog "#1471 introduce
  equivalent status" (https://raw.githubusercontent.com/hcoles/pitest/master/README.md); the GitHub API
  for https://github.com/hcoles/pitest/pull/1471 gives merged_at 2026-05-22T12:03:20Z.
- PIT score, https://raw.githubusercontent.com/hcoles/pitest/master/pitest-entry/src/main/java/org/pitest/mutationtest/statistics/MutationStatistics.java
  — "getPercentage(getTotalMutations(), getTotalDetectedMutations())", so EQUIVALENT lands in the
  numerator. https://pitest.org/quickstart/maven/ (mutationThreshold): "Please bear in mind that your
  build may contain equivalent mutations. Careful thought must therefore be given when selecting a threshold."
- Stryker, https://stryker-mutator.io/docs/stryker-js/disable-mutants/ — "Disabled mutants will remain
  in your report but will get the ignored status. Mutants with this status in your report don't influence
  your mutation score". Score: "Mutation score detected / valid * 100"
  (https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/), and Ignored is
  defined there as "The mutant wasn't tested because it is ignored."
- Stryker, https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ — "There is no
  definitive way for Stryker to find and ignore them. There is currently also no way yet to mark them to
  be ignored." This general page conflicts with the StrykerJS disable-comment page above. I treat the
  StrykerJS page as current for JavaScript; that choice is an inference.
- The report schema (https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/packages/report-schema/src/mutation-testing-report-schema.json)
  lists `["Killed","Survived","NoCoverage","CompileError","RuntimeError","Timeout","Ignored","Pending"]`.
  There is no Equivalent status.

What this means for this leg (arithmetic from the formulas above; not a lane score):

| convention | S_EMPTY_GUARD becomes | rate |
|---|---|---|
| tameshi `k/(k+s)` (`SKILL.md:210`) | Survived (measured) | 5/10 |
| PIT ≥ 1.25 EQUIVALENT | detected | 6/10 |
| Stryker disable comment | Ignored, removed from valid | 5/9 |

The two external conventions disagree with each other, and both raise the number. Neither maps onto a
mutant that was actually run and measured green. Stryker's Ignored means "wasn't tested", which would
be false provenance here. PIT's own docs say EQUIVALENT is counted as detected "although by definition
it cannot be".

## 4. Should the recorded table change? No. Counterfactuals run in the /tmp clone at a08e85c

| edit to `tools/mutate-and-run.sh` | C1 counter (frozen) | other effect |
|---|---|---|
| `S_EMPTY_GUARD:SURVIVED` → `:EQUIVALENT` | `WIRED`, `depth_score=9`, rc 0: the counter cannot see it | mte-interop `per_mutant=False {'S_EMPTY_GUARD': ('Survived', None)}` (judge rule `tools/mte-interop.py:257`, `STATUS` `:69`); replay would print `REGRESSION_DEFECT … measured=SURVIVED recorded=EQUIVALENT` (`:1284-1286`, read, not run) |
| drop the pair (9 entries) | `UNWIRED (table-counts)`, `depth_score=8`, rc 1: misses the frozen target | — |
| drop the pair, set leg-check to `9:5`, ledger comment to `5/9` | `WIRED`, 9, rc 0 | the embedded spec still has 10 `@defect` lines (counted); replay would flag `measured=SURVIVED recorded=ABSENT` (`:1281-1283`, read, not run). Removing it from the spec rewrites the pre-registered bytes of 622d31d. |

Every table edit either misses the frozen C1 target or fails a no-harm companion
(`contract.json` C1 `no_harm_companions`: regression PASS 9/9, interop 9/9). The relabel is the
dangerous one: the counter stays green, so only the companions catch it. The contract's own bound
already says this ("whether the recorded table equals a real sweep is checked by the regression
companion, not by the counter"). If a judge is ever shown a relabel, it must reject it as a
false-provenance tradeoff, not as a defect it can fix.

## 5. A second finding next to it: the hole the slot missed

The informative sibling drops only the resolved guard: `filesScanned > 0 && !drift` (my
`mut/X_RESOLVED_GUARD.mjs`). Run with the contract's hermetic `env -i … node … --selftest`:
`62/62 cases passed (hermetic)`, rc 0, so it survives. It is not equivalent. On a scanned document
with zero citations (`diff/e-nocite`), pristine prints `VERDICT: FAIL` and the mutant prints
`VERDICT: PASS`. The exit code is 2 for both, because `main()`'s fail-closed arm (`:2527-2533`)
masks it.

So K_EMPTY_VERDICT is killed only because the empty-scan case has both counters at zero. Neither
guard is pinned on its own, and only the resolved guard has behaviour of its own. The round-gate
precedent rejected a candidate that was "equivalent by unreachability" before the sweep
(`mutation-case-kumitate-round-gate.md:45-48`). Round 26 has no `rejected_candidates` field in
`predictions.json`.

## 6. Axes affected

- **Depth:** the leg still counts (the counter counts recorded and wired legs). The informative content
  is 4 gap-bearing survivors plus 1 calibration item, not 5 gaps.
- **Calibration:** "10/10 verdict predictions held" overstates what was tested. S_EMPTY_GUARD's
  SURVIVED prediction could not fail, so 9/10 were falsifiable and all 9 held.
- **Provenance:** any table relabel would assert a measurement that never happened.

## 7. Smallest safe correction (moves no frozen target)

Text only. Keep every committed table and spec byte, the counter and its target.

1. In the leg entry and the `SKILL.md` "Ninth recorded case" paragraph (`SKILL.md:2086-2095`), add:
   "5/10 killed. Of the 5 survivors, 4 are suite gaps with off-suite witnesses. S_EMPTY_GUARD is
   equivalent code: `totals.resolved` is incremented only after `totals.filesScanned` in the same loop
   iteration (`cite-check.mjs:1553-1583`), so the verdicts agree on every input. It is recorded
   SURVIVED as measured, and is a calibration item, not a gap (`SKILL.md:221-223`). 10/10 predictions
   held; 9 were falsifiable."
2. Optional side note in the same place: "PIT 1.25 or later would score this set 6/10 (EQUIVALENT
   counted as detected) and Stryker 5/9 (Ignored). The lane's rate stays 5/10." Cite the sources above.
3. Note: `SKILL.md:2095` names `corpus/knowledge/mutation-case-kumitate-cite-check.md`, but that path
   is not in the tree at a08e85c (`git ls-tree -r HEAD` shows no such file). The equivalence sentence
   belongs in that entry once it exists.
4. For later rounds only: carry X_RESOLVED_GUARD into a later spec. Also require a pre-sweep witness
   input (or a `rejected_candidates` entry) for every hole-aimed defect.

Checks for the L1 after any text edit: `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE`
should still give `depth_score=9` (text edits cannot move it); `bash tools/mutate-and-run.sh
--regression` should give `cases=9 passed=9`; the interop check should give `legs_conforming=9/9`.
