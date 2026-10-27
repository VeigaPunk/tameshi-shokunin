# T52W1CritC2 — C2 predicate/control critique

## Counterexample: frozen pass does not mean every statement is calibrated

On a scratch clone, I started at BASE `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`, applied the documented positive corrections, committed them, then added a still-false claim in an unrelated SKILL section: `### Round-26 unrelated notes` / `The nine ledger legs remain unchanged in this sibling section.` Revision `724f8bb6143ad5e4b716b2dffba0e0913e592568` returned `total=0 C2_R52_PASS=true`. Observed command:

`python3 .ufo/evidence/round-52/c2/measure.py --lane "$D" --rev 724f8bb6143ad5e4b716b2dffba0e0913e592568 --explain`

The output reported `m1=0 ... total=0 ... true`; m1's implementation only extracts `### Round-26 gate/probe registry — report interop` at `measure.py:109-115`, so the inaccurate sibling statement is invisible. This limitation is acknowledged by contract `claims.C2.cannot_see` (stale statements outside frozen set), so it is a real boundary of the claim, not a counter to the declared bounded predicate. The predicate is measured at a tree, but its criterion is narrow lexical agreement, not holistic calibration of lane records.

## Additional critique/evidence

- **C2's evidence is self-attested, not semantic.** `m4` checks quoted substrings, reader identity, and `wrong_expectations == len(findings)` in `measure.py:151-165`; `check_findings` at `:82-95` checks verbatim substring/minimum length and frozen floors, not that the quote reports a *finding* rather than a reader's “holds”/non-error statement. `m6` uses the same validator (`:166-176`). Thus a quote can be provenance-valid but classified dishonestly; wrong_expectations can be set to the fabricated count and still satisfy its arithmetic. This is a calibration weakness and can create a false pass if all other checks pass.
- The m3 pointer counter is stronger than a mere token-search allegation: `range_has` at `measure.py:77-79` verifies the quoted numeric range in `tools/mutate-and-run.sh` actually contains the respective required token. I changed the pointer to `:1` in an otherwise positive scratch fixture; observed output was `m3a MISMATCH ... pointer=tools/mutate-and-run.sh:1` and nonzero total. So the proposed “unrelated line merely contains token” attack did **not** pass via this mechanism. It still does not verify that the cited range supports the surrounding explanatory statement beyond its one required token.
- m2/m3 scope predicates accept presence co-occurrence: m2 `:117-120` passes a row containing both `/tmp` and `TMPDIR`; m3c `:129-138` similarly accepts both strings in the bullet. These do not establish TMPDIR behavior or correct caveat semantics; wording can negate or qualify the variable while still passing. No control specifically exercises this semantic distinction.
- **Control coverage:** frozen controls specify `C2_CTL_0`, `DELETE`, `ZERO`, `FORGE` false and `POSITIVE` true (`contract.json:50-65`; implementation `control/controls.py:170-175`). There is no no-op case expected true: C2_CTL_0 is explicitly the BASE/failing control, and the positive case changes the frozen defects. Therefore a do-nothing control is excluded as a passing control, appropriately. The positive control's zero-finding weakness is explicitly documented in `contract.json:39` and exercised by C2_CTL_ZERO, but does not test semantically misclassified *nonzero* findings.

## Axes and smallest safe correction

- **Calibration:** the bounded predicate genuinely measures whether selected recorded assertions and correction records match selected evidence; it does not establish calibration beyond those statements, nor whether every cited quote is actually a finding. This is relevant to calibration (axis 8), but the acknowledged frozen-set blind spot should not be expanded into a different claim mid-round.
- **Operability/depth:** no impact demonstrated. The fixture attack concerns statement scope and interpretation, not registry operability or runnable case count.
- **Smallest safe correction:** keep this run's frozen predicate/claim unchanged. For a future calibration predicate, validate correction quotes against explicit finding markers or a frozen classification rubric (and test a quote that is verbatim but reports “holds”); tighten TMPDIR clauses to assert the actual fallback/override behavior, rather than co-occurrence. Expand frozen statement coverage only via a separately registered claim/control, not an after-the-fact change.

## Evidence locations / commands

- Counter and clause implementation: `.ufo/evidence/round-52/c2/measure.py` (especially lines 77-95, 109-138, 141-176); inspect with `nl -ba .ufo/evidence/round-52/c2/measure.py`.
- Claim boundary and expected controls: `.ufo/evidence/round-52/contract.json`; inspect with `python3 -m json.tool .ufo/evidence/round-52/contract.json`.
- Control definitions: `.ufo/evidence/round-52/control/controls.py:170-175`; inspect with `nl -ba .ufo/evidence/round-52/control/controls.py`.
- Scratch fixture commits and commands were confined to `/fast/scratch/hyaku/tameshi-r52/T52W1CritC2`; that directory was removed before reporting. No lane counter verdict or frozen contract was changed.

## Summary
- False pass demonstrated: unrelated stale nine-leg statement coexists with `C2_R52_PASS=true`.
- This is within the predicate's explicitly acknowledged frozen-statement limitation.
- The correction-record validator proves quote provenance, not that quoted text is a finding.
- The unrelated-range pointer attack was rejected by the counter.
- C2_CTL_0 is a failing base control; no no-op passing control exists.
- Preserve frozen claim; tighten semantic validation in a future registered calibration predicate.
