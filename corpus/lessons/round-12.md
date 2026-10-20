# Round 12 — pristine controls and bash witness attribution

Baseline: `18ad5d050ef4bcd830fe513825baed878f025024`, clean at round start. Declared claims: `.ufo/evidence/round-12/claims.json`. C1 calibration acquires a repeated-control capability; C2 depth deepens attribution on an existing bash leg. Both scalar scores stay 6: the historical case-count and promotion-restraint rubrics do not count these improvements as new points.

## Gate

Source access recorded from this round, using observed UTC date 2026-10-20 rather than the dispatch prompt's calendar date. Existing rows are re-opened, not re-created. No new registry rows, no tier changes. These primary sources support their scoped semantics, not the truth of this lane's run results.

| Row | URL opened | Access | Located quote (at most 25 words) | Scope |
|---|---|---|---|---|
| S004 | https://mutants.rs/using-results.html | 2026-10-20 | “cargo-mutants can’t do anything until you have a tree where `cargo test` passes reliably when copied to a temporary directory.” — Tests fail in an clean tree? | Reliable copied-tree baseline is a precondition; does not prescribe three runs. |
| S006 | https://raw.githubusercontent.com/BWBama85/shmutant/7eefc73010ad6342b80e3ed43915503e02c90618/README.md | 2026-10-20 | “The suite went red, but not on its witness.” — The three verdicts, accidental row | Intended witness vs accidental red; tameshi's full-suite/exact-line adapter is not shmutant selector equivalence. |
| S026 | https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | 2026-10-20 | Opened by L1; reader omitted the article body. No article quotation is credited from that partial view. | Source body support is assessed by the source-opening executor; no statistical claim is inferred from the comments. |

Mutable-field ledger (all other registry cells unchanged):
- S004 `used-by`: `corpus/knowledge/mutation-score-semantics.md` → same plus `corpus/knowledge/repeated-control-precondition.md`; status `mined` → `mined`, recheck `on-release` → `on-release`.
- S006 `used-by`: `corpus/knowledge/witness-scoped-kill-verdict.md, corpus/knowledge/mutation-score-semantics.md` → same plus `corpus/lessons/round-12.md`; status `mined` → `mined`, recheck `90d` → `90d`.
- S026 `status`: `queued` → `mined`; `used-by`: `—` → `corpus/knowledge/repeated-control-precondition.md`; recheck `730d` → `730d`.

Gate decisions:
- Admit scoped source facts: S004 reliable baselines; S006 witness distinction. Runtime acquisition and measured attribution depend on retained observed receipts, not source authority.
- Reject “three matches prove determinism.” A finite sample establishes only no observed tuple mismatch; changing time/path output is intentionally rejected, even for a healthy program. Flip: evidence sufficient for an explicitly stated statistical/model claim, not a larger arbitrary run count.
- Reject “a bash witness reanalysis is a seventh independent gate.” Same artifact/spec remains the same leg. Flip: a genuinely new independently recorded case, not another analysis dimension.
- Reject treating lane-dispatched reviewers as outside admission or promotion authority. Outside round-12 admit/reject spot-check remains the external closure duty; no `[x]` is earned here.

### Source completion (continuation; supersedes incomplete S026 access row)

S026's article body was subsequently opened by ControlKnowledge and the
continuation source seat, not inferred from the comments omitted by the
reader view. URL: https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html;
access 2026-10-20; post body, definition paragraph:
“a test that exhibits both a passing and a failing result with the same code.”
Located served-byte anchor: `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv`,
Q4, HTML line 1130; digest and access time in that row. Word-count notes
in the inherited TSV are not credited as measurements. This is the
definition, not a claim that matching three executions excludes flakiness.

S011 and S028 source quotes and mutable transitions are recorded in the
source-review addendum below; that addendum is part of this Gate record.
S040 was also opened by SourceSurvey
(`.ufo/waves/round-12/w1/SourceSurvey.md`); status remains queued,
recheck and used-by unchanged. No S040 admission or new row is claimed.
The registry's old opened dates remain original access dates, not this
round's re-open dates; append-only source metadata is not rewritten.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix and failure requirement |
|---|---|---|---|
| vacuous | `.ufo/evidence/kaika-round-1/capability-demo/README.md`, H2: one pristine observation per sweep cannot detect changing subsequent controls | QUALITY 1–3; no previous repeated-control gate | Add standalone exact-tuple repeated-control gate; a deterministic changing fixture must defeat the single-control baseline and be refused by the new gate. Runtime receipts appended below. |
| attribution | `corpus/lessons/round-1-verifier-spotcheck.md:17`: box-3 increment rejected; `corpus/knowledge/witness-scoped-kill-verdict.md`, E1: declaration partly contaminated | QUALITY 3 and 6 | Preserve scalar scores and `[~]` marks, disclose prior exposure, freeze declaration before execution. Declaration integrity must reject changed evidence rather than silently re-register witnesses. |
| reference-drift | `.ufo/waves/round-12/w1/WitnessSourceReview.md`: abbreviated baseline grammar and passing alternative witness | QUALITY 2–4 | Historical knowledge E2/E3 append the omissions and exact-line/whole-token distinction; original declaration remains unchanged. No fresh replay credited by this correction. |

## Authority and dispatch

One validated 32-seat batch: `.ufo/waves/round-12/spec.json`, `dispatch.json`, `w1/swarm-registry.json`. Three executors; connector, scout, scribe, reviewer, critic and additional roles are present. The validator forbids planner taxonomy, so ClaimSkeleton uses reviewer taxonomy while performing the planner function. This is a disclosed exact-role-floor deviation, not a claim that the requested planner route ran. No routing/configuration edit or model override.

Previous outside review found a scope-overclaim, not authority to promote this round: box 3 remains unscored, and SHONEN remains lane assertions. No `round-11-verifier-spotcheck.md` or operator lesson exists in the complete starting lesson-directory listing (`corpus/lessons` contained round-1-verifier-spotcheck.md, round-1.md, round-10.md). No inherited uncommitted work was present.

### Host planner ruling, opened after dispatch

The initial “exact-role-floor deviation” above is superseded by the current binding host ruling: `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:33-36` assigns the canonical planner seat to L1 and forbids a swarm planner. L1 held scope, decomposition, and contracts; ClaimSkeleton supplied supplemental reviewer analysis, and MistakeMining supplied the revenger data walk. No validator bypass or extra dispatch is needed. The L0 answers to kama round 11 and tsukuroi round 12 also assign independent round admission to the fresh hyaku closure session; that future check is not claimed as already run.

### Source-review limits

S028's normative test-runner contract decides success by exit status, not repeated stream equality (`.ufo/waves/round-12/w1/SourceBazel.md`). C1's N≥3 and exact-byte requirements are lane policy. They intentionally reject volatile output without claiming a Bazel violation. S011 Discussion, p.9, says “some flaky tests may continue to show the same coverage even on our repeated executions, only to appear flaky another day.” The source-opening seat retained the primary PDF and excerpt under `.ufo/evidence/round-12/SourceFlakyPaper/`; no statistical power claim is made from three runs.

Additional source mining in this round:
- S011 `status`: `queued` → `mined`; `used-by`: `—` → `corpus/lessons/round-12.md`; recheck `730d` → `730d`. Opened primary PDF by SourceFlakyPaper; source report gives access date 2026-10-19, while parent UTC clock is 2026-10-20. Digest and located excerpt, not a fabricated reconciled timestamp, identify the source.
- S028 `status`: `queued` → `mined`; `used-by`: `—` → `corpus/lessons/round-12.md`; recheck `365d` → `365d`. Opened https://bazel.build/reference/test-encyclopedia on 2026-10-20; §Role of the test runner: “writing any of the strings PASS or FAIL to stdout has no significance to the test runner.” This grounds the rejected source-attribution claim, not C1's stricter lane policy.

## In-session inheritance resolution

The baseline/clean-at-start statements above describe the earlier headless
attempt, not this continuation. Durable dispatch digest:
`2026-10-19T23:10:59-03:00 launch tameshi round=12 pgid=13129 driver=hyaku slot=3 attempt=1`;
termination digest:
`2026-10-19T23:24:27-03:00 lane-dead-no-report tameshi round=12; retry same round (hyaku: headless attempt ended by operator directive to run in-session)`.
The current launch was
`2026-10-20T00:41:11-03:00 launch tameshi round=12 pgid=288438 driver=hyaku-inline attempt=1`.

Inherited lane work: modified LOG, SOURCES and witness knowledge; untracked
round-12 lesson, repeated-control knowledge, two tools, evidence and first
wave registry/reports. It is retained under this same round after source
review and integrated replay, not credited as newly produced by the current
wave. No aggregator/operator-owned file was changed. Existing evidence
scripts are reproducible retained experiments, not disposable scaffolding.
No historical recorded mutation case or runner code is changed.

The continuation validates and dispatches a second batch of 32 seats:
`.ufo/waves/round-12/spec-w2.json`, `dispatch-w2.json`,
`assignments-w2.json`, `record-w2.json`, `w2/swarm-registry.json`.
L1 is the canonical planner. The bounded revenger data walk is
`w2/IntentDataWalk.md`. Both batches together contain 64 seats,
not 64 newly spawned by this continuation. No models were passed.

Inherited claims.json's planner-deviation field is a superseded snapshot:
the host addendum already assigns planner to L1; no role-floor deviation
is newly claimed. The stale scorecard plan's “6 → 7” for a bash witness
analysis is rejected: one existing gate remains one existing gate.
The outside round-1 adjudication pins calibration 6 with box 3 excluded.
Command C is only an 8-point mark upper bound, not the pin; measure.py
implements the explicitly adjudicated exclusion, not an authority check.
Round-12 changes award neither new promotion points nor independent review.

Snapshot ruling: `--snapshot` reclassifies saved observations without
executing a command, against hand-recorded expected IDs and every input
digest. Run-mode `command.txt`/`finding.txt` directories are not automatically
frozen snapshots. Snapshot metadata's own history anchor is the repository;
coordinated edits to bytes and expected digests are outside accidental-drift
protection. Nested `mismatch/` is a separate snapshot, not stable-root input.
An intact expectation disagreement uses `controls_mismatch`/1; damaged
inputs use `snapshot_tampered`/2. These are deliberate scoped choices,
not adopted requests for a second live execution interface.

The existing `[~]` box-3 mark and older `[ ]` receipts are temporal evidence,
not permission to rewrite earlier reports. Criterion 13 now captures the
outside review's full-page sufficiency boundary. Criteria 11–12 capture the
finite-control and attribution mistakes above. All remain lane assertions;
round-12 outside admit/reject sampling is pending the separate closure.

### Internal review disposition

- W1's ClaimSkeleton item used reviewer taxonomy for a planner-function
  exercise; that was not the host's permitted data-walk carrier. L1 remained
  canonical planner. W2's IntentDataWalk revenger supplies the permitted
  bounded walk. The earlier MistakeMining item was mistake mining, not
  itself evidence that a full planning data walk ran.
- W2 ScopeConnector/ClaimsConnector proposals for a new receipt architecture
  and all-nonzero-first precedence are rejected as out-of-scope design
  expansion. The frozen command contract is unavailable → tuple mismatch
  → uniform nonzero → match. A `[1,2,1]` mismatch is an observation verdict,
  never admission of that baseline as suitable for mutation attribution.
- W2 FrontierConnector's “measured 8/0/2” prose preceded a complete experiment
  receipt and is not measurement evidence. Only the retained actual study
  summary and raw outputs determine C2. A docstring or predicted outcome
  never substitutes for runtime output.
- Temporal round-1 candidate tokens are superseded by the named outside
  adjudication, not silently rewritten. No new rule forcing a contested
  sample is invented here; the protocol's independent admit/reject sample
  remains the criterion and round-12 closure duty.
- An accidentally fleet-wide path reminder was intended only for this
  wave; Main was informed and instructed that future messages name only
  owned seats. Some seat reports initially used a relative fleet-root
  destination and were moved by their authors into the assigned absolute
  lane path. These were write-scope defects, not claimed domain work.

## Runtime results and failure-backed repairs

Final integrated receipt:
`.ufo/evidence/round-12/verification-final.json`.
`python3 tools/repeat-control.py --selftest` printed
`SELFTEST: PASS (29 cases)`, exit 0. Stable snapshot exited 0;
mismatch snapshot exited 1 with `controls_mismatch`. Three pristine
bash controls matched on raw streams and zero exits; this is finite
agreement, not a determinism proof. The retained raw files resolve
under `.ufo/evidence/round-12/replayed-controls/`.

The vacuous single-control repair is shown able to fail using the
same oracle, changing fixture and expected mismatch:
`.ufo/evidence/round-12/oracle-repair.json`. With only the repetition
loop reduced to one run, the oracle exits 1 (`controls_match`,
wrong expected finding); restoring the loop makes that same oracle
exit 0 (`controls_mismatch`, correct finding). Raw records and the
mutant are retained; no temp-only pointer carries this claim.

Failures were not erased: initial selftest exit 2 came from a wrong
saved-bytes path (`stable` vs generated `stable.sh`); integration
also used an ambiguous mutation anchor and then the restored stable
fixture instead of the changing fixture. Exact observed failures:
`integration-failure.txt`, `verification.json`. The final receipt
supersedes only the repaired oracle rows; other passing checks are
carried with their original outputs. These are reference-drift
mistakes captured by QUALITY 1–3 and repaired in the evidence recipe.

C2's canonical study classified ten declared defects:
8 killed-on-witness, 0 accidental, 2 survived, 0 inconclusive;
16 printed control slots = 14 exercised + 2 skipped. Six hits are
specific-case and two generic-only; B3 has an extra failure.
Declaration was not blind, NONE survivors are not out-of-sample,
and no assertion-level causality is claimed. The initial post-sweep
`KeyError: 'skip'` and pre-declare revision-parser refusal are named
in `w2/WitnessFinish.md`; raw crashed sweep is retained. Final
classifier selftest printed 40/40 pass; actual rerun agreed on ten
classifications without changing the canonical summary.
Main's integrated `check` and `count` exited 0 with no unresolved rows.
The summary's nested declaration.kind is null; its disclosure and
top-level kind remain explicit. That cosmetic defect is named, not
silently re-hashed after verification.

Unchanged-runner guardrails: main replay observed `MUTATE_SELFTEST:
80/80 pass` and six-leg `REGRESSION: PASS`, both exit 0.
End census command (same as start):
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
printed `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`,
exit 0 (`sources-after.txt`). Rows 44 → 44; A/B/C 37/5/2 unchanged;
mined/queued/rejected 12/29/3 → 15/26/3, measured by
`python3 .ufo/evidence/round-12/measure.py --rev REV` on the baseline
and the final content revision recorded in SCORECARD.

Self-verdicts: C1 capability and C2 bounded depth improved; scalar
depth/calibration both 6 → 6. Other axes unchanged. Expansion improved
as a sourced F3 entry and demonstrated capability; quality improved
through source corrections and failure-backed evidence repairs;
discernment improved only in the criterion-learning sense (outside
box-3 disagreement → criterion 13), not by a new outside spot-check.
Final claim admission still belongs to the separate non-author closure.
