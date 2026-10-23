# Round 31 — six-axis no-harm forecast

**Verdict: no-harm is conditional, not yet demonstrated.** The plan can preserve all six axes, but calibration has a concrete, already observed drift hazard. Passing C1 is not a substitute for its separate no-harm monitor. The smallest safe correction is to finish the content inputs before the fresh reads, bind the resulting entries with frozen v4, and measure both C1 and the strict no-harm monitor at the revision carrying the final rows and ledger append. Do not change either frozen instrument.

This is a scoped forecast, not a claim ruling. Method: static source and receipt reads only. All observed outputs below are quoted retained evidence, not executions by this reviewer. Forecasts and unexecuted counterexamples are labelled **[INFERENCE]**. The proposed content and dead-seat checker were not supplied as completed artifacts, so their behavior is not asserted.

## Strongest counterexample and observed evidence

**[INFERENCE] Accurate self-assessment can coexist with harm.** Append a source change that invalidates existing cold-read credit, then append SCORECARD rows that accurately state the resulting observations, including the lower calibration observation. The frozen C1 equality property can hold while the separate no-harm predicate fails. This is not a defect to repair by changing C1: the contract measures equality, not preservation of the prior state (`.ufo/evidence/round-31/contract.json:14-26,45-49`). The counter extracts only the calibration observation for that statement and ultimately requires equality plus append-only preservation (`.ufo/evidence/round-31/c1-measure.py:151-155,201-224`).

The observed premise is stronger than a hypothetical large rewrite: **one comment line is sufficient**. The recorded drift experiment reports:

| Input perturbation | Exact retained output, omitting only its revision field | Receipt |
|---|---|---|
| Append one comment to SOURCES | `C1_MONITOR: covered=60/64 restraint=6 box3_mismatch=1 depth_score=9` | `.ufo/evidence/round-31/before/drift-sim.txt:1-6` |
| Append one comment to QUALITY | `C1_MONITOR: covered=63/64 restraint=6 box3_mismatch=1 depth_score=9` | same file, `:11-13` |
| Append one comment to README | `C1_MONITOR: covered=61/64 restraint=6 box3_mismatch=1 depth_score=9` | same file, `:14-18` |
| Append one comment to SCORECARD, LOG, or the lesson, separately | `C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9` | same file, `:7-10,19-20` |

There are eight distinct uncovered headings across the first three experiments. They are **not a measured combined-edit result**: the receipt runs separate perturbations and does not perturb the new knowledge entry. Do not forecast an exact union tally from it. Use the actual combined content revision to select the re-reads.

The command that produces these monitor fields is:

```sh
python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev REV
```

Its exact contract is exit zero only for full coverage, the required restraint observation, and no box-3 mismatch (`.ufo/evidence/round-27/c1-measure.py:12-14,45-54`). The historical scratch arguments for the drift runs are not preserved in `drift-sim.txt`; this report does not invent them.

**Additional trap:** the experiments showing no drift from SCORECARD/LOG/lesson apply to the old crediting entries. **[INFERENCE]** A fresh reader can record one of those files as a new input; a subsequent append can then stale its new entry. The input gate checks every recorded non-ignored input against the measured revision, not a permanent whitelist of safe filenames (`.ufo/evidence/round-18/measure.py:47-55,321-349`). A final-head reading is therefore necessary even after a successful restoration reading.

## Forecast by axis

The six axes are **depth, coverage, operability, freshness, calibration, adjacency**, as already enumerated in `SCORECARD.md:105-112,181-188`. The following are risks to prevent, not newly awarded axis moves.

### Calibration — exposed; restoration is necessary

- **What could drop:** source/index/quality edits stale full-page evidence; a later traced-input append stales the replacement reads. Separately, append-only tables can become competing authorities if the new block does not explicitly supersede the standing values. A fresh tally can also conceal the still-open tally-guard limitations if the prose calls the whole surface complete.
- **Receipt that would show it:** strict monitor at the final measured revision, including uncovered headings; frozen C1 stdout and exit; v4 selection receipt and excluded-entry reasons; ledger append comparison. The existing baseline C1 receipt has seven mismatches, not a clean starting point (`.ufo/evidence/round-31/before/c1-at-base.stdout:1-13`).
- **Cheapest check:** run the strict monitor first at the combined content revision and again at the revision containing the rows and ledger append. Use its actual uncovered sections, not an assumed fixed list. Apply v4 to the fresh assembly before appending, and inspect every exclusion needed for coverage. Reuse the eventual frozen C1 run for the twelve statement observations; do not add a second measurement authority.
- **Smallest correction:** label the appended tables as the current superseding observations while preserving old bytes, frozen statement identities, and historical first-working facts. Keep the eight routed selftest survivors and per-leg tally limitation visible. A calibration-equality pass does not resolve those operability debts. The contract explicitly leaves them routed (`contract.json:41-43`).

V4 is a separate necessary binding check, not something the strict monitor evaluates. The prior closure expressly identifies this separation (`corpus/lessons/round-30-verifier-spotcheck.md:105-109`). V4 checks report `read_rev`, section identity, a matching executed trace call and receipt revision (`bind-select-v4.py:294-336`, under the round-31 coldread directory). Its pilot kept 63 historical entries with no exclusions (`coldread/pilot/v4-on-r30-real-receipt.json:5-8`); that is compatibility evidence, not a fresh round-31 read. Also, the selector returns zero when **any** entry survives, not only when every needed entry survives (`bind-select-v4.py:343-359`). Do not use its exit alone as full restoration evidence.

### Depth — stable if the recorded-case surface stays unchanged

- **What could drop:** the new lesson, source rows, checker, or remeasured capability tables are counted as another recorded case, or the runner's pinned ledger is changed while the plan says it is untouched. **[INFERENCE]** Documentation can overstate depth even without altering runnable behavior.
- **Receipt that would show it:** command D at the measured revision and the runner blob comparison. The recorded base observation is `observed=9 (exit=0)` for depth (`before/c1-at-base.stdout:11`); the contract says no tenth recorded case (`contract.json:41-47`).
- **Cheapest check:** compare `tools/mutate-and-run.sh` between base and the final revision, then reuse command D's observation from C1. The exact standalone command is retained below.
- **Smallest correction:** describe the work as correcting the standing observation, not adding a case. Leave the runner unchanged for this round as planned; do not spend the calibration repair on a deferred runtime edit.

### Coverage — no new-surface conclusion follows from extra rows

- **What could drop:** the new knowledge entry is missing from the index, a source citation/backlink does not resolve, or the README silently closes frontier ground on the strength of extra source rows or same-ground record repair. **[INFERENCE]** A correct row count alone cannot establish a broader governed surface.
- **Receipt that would show it:** the content diff linking the entry, README row, source headers and used-by paths; census validation; an explicit unchanged frontier status or a separately justified surface change. The previous round's README deliberately calls its addition Core ground and leaves frontier status unchanged (`corpus/README.md:449-456`). QUALITY requires the entry/index pairing and source headers (`corpus/QUALITY.md:18-30`).
- **Cheapest check:** one joint read of the new entry, its README row, and S095–S097, plus the required census. Confirm cited rows are opened and usable for the stated scope; do not equate adding three rows with acquiring three surfaces.
- **Smallest correction:** give the README row the entry's bounded scope and retain existing frontier limits unless this round actually supplies a separate boundary-changing witness.

### Operability — new checker must not become a second status authority

- **What could drop:** the dead-seat check treats a partial report as completion; relies only on a seat name to identify repeated work; or treats a dead control's recorded absence as evidence that the required control class was exercised. A renamed identical task can evade a name-only comparison, while an old name can refer to a different measured object. **[INFERENCE]** These are prospective checker defects, not observed behavior of an implemented checker.
- **Receipt that would show it:** a committed pre-dispatch comparison, the exact dead/outcome list, proposed task descriptions and measured revisions, final report-path checks, and a scored receipt for each required control class. Local evidence already distinguishes reused names from genuinely repeated work: round 30's dead-seat overlap review found distinct measured objects and identified the omitted pre-dispatch comparison as the lapse (`round-30-verifier-spotcheck.md:175-180`, under corpus/lessons).
- **Cheapest check:** exercise the checker against one same-task/renamed-seat fixture and one same-name/different-revision fixture; inspect its output against the actual registry. Check separately that a failed seat's partial artifact does not become a completed outcome, and that a required dead control class still has a scored replacement. No full mutation sweep is needed to inspect these boundaries.
- **Smallest correction:** keep the script a read-only, explicit comparison of names **and task/target/revision evidence**, with reported ambiguities rather than inferred lifecycle decisions. Preserve the existing callback-accounting authority. Keep report presence, terminal status, and control-class sufficiency separate: QUALITY 58 requires a scored class replacement; QUALITY 59's final path check does not waive it (`corpus/QUALITY.md:653-675`). Do not resend a dead seat's task.

The green runner tally is not proof that the routed holes disappeared: round 30 records the duplicate/drop limitation and eight surviving mutations (`round-30-verifier-spotcheck.md:78-84`). Likewise the prefreeze regression reconnaissance returned `REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)` in the wrong sibling layout, while the frozen base counter observed `PASS,9,9,0` (`before/prefreeze-format-recon.txt:11-15`; `before/c1-at-base.stdout:3`). A new setup error is not itself evidence of a product regression; preserve it and use the frozen counter's intended layout rather than silently changing the expectation.

### Freshness — current bindings and source opens must refer to current inputs

- **What could drop:** S095–S097 are rows without actual round-local opens/located anchors, a census-clean row is mistaken for a verified teaching, an old receipt is labelled current, or a late content edit invalidates the fresh reads. **[INFERENCE]** An old successful v4 pilot cannot establish any of these current facts.
- **Receipt that would show it:** bounded source-open receipts with URLs, timestamps, retained bytes/digests and located anchors; matching entry headers; the final monitor and v4 receipt. Census validation checks structure, enums, dates and paths, not source truth (`scripts/sources-census.sh:24-37`, at fleet root). Current SOURCE allocation already ends at S095 as the next unused id (`corpus/SOURCES.md:364`); older stale allocation sentences are history, not permission to reuse IDs.
- **Cheapest check:** validate the registry, then locate each new row's quoted anchor in its ordinary-fetch receipt and compare its digest. Inspect new `read_rev` and input hashes against the frozen content revision; use the final monitor to detect later drift. Do not reopen unrelated historical sources for this forecast.
- **Smallest correction:** retain actual open evidence before citing it, append the new allocation state, and mark anything not rechecked as unverified rather than carrying an old result forward without qualification. QUALITY 62 already requires inferred carry-forwards to be labelled (`corpus/QUALITY.md:701-709`).

### Adjacency — keep lifecycle execution and sibling products outside the method

- **What could drop:** a dead-seat checker grows into a scheduler, kills/retries peers, writes fleet or sibling state, or the new knowledge entry generalizes one lane's behavior into a cross-domain rule. **[INFERENCE]** Such ownership expansion is not required by this plan.
- **Receipt that would show it:** final changed-path list, checker code/argv review, and the report's contested-scope routing. PROVINCE explicitly owns reusable verification craft, keeps sibling gate code read-only, and requires two independent lane examples before a pattern is called general (`PROVINCE.md:3-20,44-47`).
- **Cheapest check:** inspect the final changed paths and the new checker's file-write/process-control paths; compare the entry's claimed scope with PROVINCE. This is a focused read, not another runtime or fleet scan.
- **Smallest correction:** make the checker report-only, scoped to retained inputs; route lifecycle or sibling-product remediation to its owner. Do not relabel a lane-dispatched review as outside authority. The prior closure names that exact attribution error (`round-30-verifier-spotcheck.md:39-43`).

## Exact checks for the integration owner

These are **recommended, not run here**. Run code only in the owner's permitted scratch clone, with Git redirection variables unset; use fresh bounded work paths and timeouts. `REV` must name the commit containing both the rows and the ledger append, not merely the earlier content commit. Re-measure if a later round commit changes SCORECARD or any frozen-command input (`contract.json:25`).

```sh
# From the scratch clone, strict no-harm predicate.
timeout 300s python3 .ufo/evidence/round-27/c1-measure.py --repo "$CLONE" --rev "$REV"

# Inspect the precise credit failures when restoration is incomplete.
timeout 300s python3 .ufo/evidence/round-21/coldread/measure.py --repo "$CLONE" --rev "$REV" --explain

# Exact command D from SCORECARD.md:73; REV is the measured commit.
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'

# Read-only scope checks; no output for the runner comparison means unchanged.
git diff --exit-code 36c1d3933f680125aeefc447f07db0f03004901a "$REV" -- tools/mutate-and-run.sh
git diff --name-only 36c1d3933f680125aeefc447f07db0f03004901a "$REV"

# Structural census, targeting the scratch clone explicitly.
timeout 60s bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate "$CLONE"

# Frozen C1, in addition to—not instead of—the no-harm monitor.
# WORK is an absent/empty directory under the integration owner's scratch.
timeout 3300s python3 .ufo/evidence/round-31/c1-measure.py --lane "$CLONE" --rev "$REV" --work "$WORK"
```

The retained census baseline is exit `0` with eight duplicate-URL warnings and `tameshi ok` (`before/census-start.stdout:1-9`, `before/census-start.exit:1`). Those warnings do not imply new failure or new coverage. The pre-data exact frozen C1 command template is recorded in `contract.json:18`; its observed base output is `C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=36c1d3933f680125aeefc447f07db0f03004901a C1_R31_PASS=false` (`before/c1-at-base.stdout:13`). No after output is claimed here.

**Decision boundary:** missing re-reads, weak checker cases, unclear supersession, or missing source receipts are fixable implementation/evidence defects. A final calibration loss offered in exchange for cleaner standing rows is a cross-axis tradeoff, not a no-harm result; leave that decision to the canonical judge. Do not amend the frozen predicate or target to hide either finding.

Tools installed or updated: none. Commands/gates/selftests executed: none. Processes started: none. Production files changed: none; only this assigned report was written.
