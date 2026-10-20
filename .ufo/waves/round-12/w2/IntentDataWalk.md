# IntentDataWalk — round 12, wave 2

**Axes:** depth (count of independently recorded mutation cases in the pinned runner ledger) and calibration (what a pristine-control observation establishes). **Status:** bounded, lane-internal planning analysis; advisory only. No source or runner edits, score changes, builds, tests, or runtime experiments were made. Tool installations/updates: none.

## Reconciled claims

The round-12 claims ledger records a clean baseline revision `18ad5d050ef4bcd830fe513825baed878f025024` and two separate, score-neutral claims (`.ufo/evidence/round-12/claims.json:2-12`):

- **C1 / calibration:** acquire a *standalone repeated pristine-control capability*. The starting condition is no repeat-control gate while the existing mutation runner samples the pristine once. Acceptance is at least three exact runs, accepting matching zero-exit tuples, naming output/exit disagreement, and treating a nonzero baseline as unevaluable. The claim explicitly keeps calibration `6 → 6` because a capability acquisition does not alter the promotion-restraint rubric (`claims.json:6`).
- **C2 / depth:** add declared-witness attribution and captured failing labels for the ten defects of the existing `bash-surface-census` leg; preserve the aggregate or disclose any difference. It explicitly keeps depth `6 → 6` because reanalysis is not a seventh independently recorded mutation gate (`claims.json:7`).
- The ledger says the axes tie at the pinned 6, C1 is separable from C2, and the inherited “round2” plan is stale; the round-12 move is F3 repeated controls plus F2 bash attribution, not the freshness re-sweeps (`claims.json:9-12`).

These claims reconcile with the round-12 lesson, which says both scalar scores stay 6 (`corpus/lessons/round-12.md:1-3`). In particular, C2 deepens the evidence attached to one existing bash row; it does not create or execute a new mutation leg. C1 and C2 are independent measurements, not a combined score delta.

## Stale plan entry and the seventh-leg error

The current `SCORECARD.md` still has its earlier **“Round 2 (declared fleet round 1, kaika)”** plan at lines 261-272. Its third item proposes a bash witness split “recorded as a ledger case” and predicts “Before: command D 6 → after 7” (`SCORECARD.md:271-272`). The claims ledger itself labels that round-2 row stale (`claims.json:12`); it must not override the round-12 claim contract.

The scorecard defines depth as one point per recorded mutation case in the pinned replay ledger (`SCORECARD.md:64-66`) and command D counts matching ledger-comment lines (`SCORECARD.md:71-75`). The runner’s ledger already contains six cases, including `bash-surface-census` at 8/10 (`tools/mutate-and-run.sh:84-89`). A witness split on that same artifact/spec adds attribution, not an independent case. Thus the planned `+1` is unsupported even if the split is fully measured. The inherited `ClaimSkeleton` review makes the mechanical pitfall explicit: command D's regex would count a witness-shaped line added to the comment block, although that would not be a legitimate new mutation case (`.ufo/waves/round-12/w1/ClaimSkeleton.md:41,64`). Do not manufacture a ledger line to satisfy the stale prediction; retain the six-leg ledger and report the split separately. The round-12 knowledge note independently bounds repeat-control and reanalysis as not seventh gate legs (`corpus/knowledge/repeated-control-precondition.md:49,51-55`).

There is a second wording correction in the stale plan: “repeated-control determinism gate” (`SCORECARD.md:268-270`) overstates C1. The supported name is a repeated pristine-control **consistency precondition/capability**. The round-12 lesson rejects “three matches prove determinism” and says a finite sample supports only the runs observed (`corpus/lessons/round-12.md:20-23`); the knowledge contract says `N≥3` is the round’s policy, not a source-prescribed guarantee (`corpus/knowledge/repeated-control-precondition.md:26,48`).

Calibration also stays 6: the round-12 lesson records that value (`corpus/lessons/round-12.md:3`), and the scorecard’s adjudication pins 6 with box 3 excluded rather than awarding a mechanical command-C upper bound of 8 (`SCORECARD.md:209-225`). C1 is a new measured capability, not a SHONEN box promotion.

## Measured scope that preserves intent

1. **C1:** report only whether the standalone gate observed identical or differing `(exit, stdout, stderr)` tuples across its selected runs, with its named outcome. Do not say “deterministic,” “flake-free,” or that the mutation runner was integrated. The knowledge contract describes the separate command and exact tuple comparison (`corpus/knowledge/repeated-control-precondition.md:30-48`) and explicitly says the runner remains unchanged and the repeat-control observation is not a new mutation leg (`:49,53-55`).
2. **C2:** keep the unit of analysis to the pinned `bash-surface-census` experiment, whose pinned target is identified in the inherited denominator report (`.ufo/waves/round-12/w1/BashDenominator.md:5-6,25-35`). For each of the ten mutation defects in the claim, retain its declared witness, the full captured failing-label set, and the classification; distinguish declared matches from other failing labels, survivors, and inconclusive rows. Preserve the existing aggregate expectation only if the observations support it; otherwise state the discrepancy rather than converting it into another leg. The old case note records the historical 8/10 kill result and ten independent defect injections (`corpus/knowledge/mutation-case-kagi-census.md:40-53`); that historical aggregate is not a substitute for the new attribution evidence.
3. **Denominator wording:** keep defect count separate from the suite’s test-case denominator. The pinned bash selftest has 16 numbered case slots; on a host without `the-janitor`, cases 15–16 are `skip-case`, leaving 14 executed assertions (`.ufo/waves/round-12/w1/BashDenominator.md:41-51,133-136`; also `corpus/knowledge/mutation-case-kagi-census.md:27-35`). Report both `16 total (14 executed, 2 skipped)` when that is the observed host state. This reconciles the claim’s **10 mutation defects** with a **16-case/14-executed** selftest; neither count is a new gate leg.

## Why one pristine-control sample is limited

The implementation directly shows the limitation: after mutant preparation, the runner calls `run_one` once on the pristine (`tools/mutate-and-run.sh:465-468`), checks only whether that one exit is nonzero, aborts on a red control, and otherwise emits green (`:469-475`). This establishes one exit observation, not cross-run consistency; stdout/stderr are printed, not compared between repeated controls.

The inherited baseline experiment gives concrete consequences, not just a theoretical risk: scenario A observed a green first control followed by a spurious “killed” result when a harmless mutant’s second suite invocation flaked (`.ufo/waves/round-12/w1/BaselineControl.md:74-91`); scenario B observed a transient red first control abort the sweep before any mutant evaluation (`:93-102`); scenario C observed changing timestamp/PID/random output while the single zero-exit control still passed (`:104-119`). These examples show that one run can neither expose intermittent pass/fail variation nor establish output stability. They do **not** establish that any real suite is flaky.

Repeated controls address the sample-size gap only for the tuples actually taken: a later run can still diverge after `N` matching samples. The retained knowledge therefore frames C1 as observed stability, not determinism, and rejects retries as a cure (`corpus/knowledge/repeated-control-precondition.md:24-28,48,53-54`).

## Evidence limits and confidence

**Confidence: high** that the stale planned `6 → 7` prediction conflicts with the explicit round-12 claims, score rubric, and six-row runner ledger; high that the runner’s control path is a single exit-only sample. The C2 measurement proposal is scoped to the claim and pinned denominator evidence above; this report does not assert that C2’s final experiment has completed or passed.

The required `lsp` device was unavailable: requesting `xd://lsp` returned “No such tool.” I used direct file/line reads for these source and claim references; the literal search was discovery only, not semantic proof. No runtime or check was invoked by this seat. This report is advisory and carries no independent admission or promotion authority.

**Owned path:** `.ufo/waves/round-12/w2/IntentDataWalk.md`.