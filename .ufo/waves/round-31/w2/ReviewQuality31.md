# ReviewQuality31 — review of QUALITY criteria 66–71 and F1–F4 errata at 2da841bd9913a2037d2bf612793382e572c9d205

Reviewer: TameshiR31.ReviewQuality31 (quality axis). Scope: `corpus/QUALITY.md` diff
`36c1d393…→2da841bd…` (+98 lines), criteria 66–71, errata F1–F4. All paths below resolve at
REV = 2da841bd9913a2037d2bf612793382e572c9d205 unless stated.

## Verdict

No blocking defect. All falsifier pointers resolve at REV and the cited lines say what the
criteria claim; F1–F4's own line citations are accurate. Two routing/citation defects:

1. **Criterion 71 is unrouted** — its "Captured by" names the round-31 C1 counter, not an
   item in either listed round-30 lesson; the round-31 "Routed by" preamble covers only
   66–70. (Medium.)
2. **Criterion 69's "Captured by" line range misattributes Mistake 2** — `:69-73` holds the
   "Binding v3 limit" bullet, not Mistake 2 (which is at `:148-153`). (Low.)

Criterion 69 *against this round's own practice*: substance conforms (v4 frozen pre-data at
c111dab5, attacked by pre-data controls, redesigned to v5 pre-data at 87eb64e, re-scored
pre-data, assembler uses v5); one stale reference in the wave-2 dispatch context still names
v4. (Low/informational.)

## Findings by severity

### Medium

- **Criterion 71 has no routing anchor in `round-30-verifier-spotcheck.md` or `round-30.md`.**
  `corpus/QUALITY.md:833-844` (criterion 71) says "Captured by: the round-31 C1 counter
  (`.ufo/evidence/round-31/c1-measure.py`)" — an artifact of this round, not a routed lesson
  item. The preamble `corpus/QUALITY.md:750` ("Routed by … Conformance defects and routed
  defects 1–5 … Mistakes 2, 4 and 5") maps to: 66←conformance defect (a) + routed defect 1;
  67←Mistake 5; 68←Mistake 4; 69←Mistake 2 + routed defect 4; 70←conformance defect (b) +
  routed defect 5. No listed item covers 71. Smallest safe correction: either cite a lesson
  item (none exists for standing SCORECARD rows) or amend the preamble to "criteria 66–70 are
  routed by …; criterion 71 captures the round's own C1 measurement".

### Low

- **Criterion 69 "Captured by" mispoints Mistake 2.** `corpus/QUALITY.md:788-789` cites
  `lessons/round-30.md:69-73,213` for "(Mistake 2 and routed binding v4)". Numbered at REV:
  lines 69–73 are the "Binding v3 limit" bullet (captures the v4 routing, fine); Mistake 2's
  own body is at `:148-153`; line 213 is the "Routed to round 31" line "- Binding v4
  (Mistake 2): the post-data audit's conditions become the binding." ✓ Substance is captured;
  the range tag for "Mistake 2" is wrong. Smallest safe correction: cite `:69-73,148-153,213`
  or drop the Misake 2 parenthetical from the `:69-73` range.
- **Criterion 69 vs round-31 practice — stale binding reference in the dispatch context.**
  Practice conforms: v4 frozen as executable code before data at c111dab5
  (`.ufo/evidence/round-31/coldread/bind-select-v4.py`, sha256 dd8bb393…, contract.json
  `binding_v4`); attacked before data by wave-1 controls CtlBindV4Old (all 7 old shapes + 5
  controls killed, 0/32) and CtlBindV4New (5 of 9 NEW forged shapes kept 63/63 → v4 failed);
  redesigned before data into v5 (`.ufo/evidence/round-31/coldread/bind-select-v5.py`, sha256
  8760ddc9…, committed at 87eb64e, before the wave-2 dispatch record 3351738) with
  `contract-addendum-1.json` recording the supersession; v5 re-scored before data
  (`ctl/bind-v5-real-r30.stdout` 63/63, `bind-v5-new-shapes.stdout` all killed,
  `bind-v5-old-controls.stdout`/`bind-v5-old-shapes.stdout` 0/32); assembler
  (`.ufo/evidence/round-31/coldread/assemble-w2.sh`, worktree) keeps only entries meeting
  binding v5; no post-data audit supplies conditions. Inconsistency: the wave-2 context in
  `spec-w2.json` (commit 3351738, §context) still says "bound by the frozen binding v4 …
  bind-select-v4.py", while the operative binding is v5 (also the target of seats
  ReviewBindV5 / CtlBindV5Fresh). Smallest safe correction: update the dispatch context (or
  append a note next to the v4 mention) to name v5 before data lands.
- **Criterion 71's falsifier third item is corroborated indirectly.** The claim "all three
  stale at the same revision" for the round-17 supersession line (`SCORECARD.md:632-636`, at
  REV: "runner selftest 95/95 (row says 80/80); six-leg regression is seven legs, `cases=7`
  (row says 6); … evidence-disposition 56/56 (34/34)") is backed for runner/regression by
  `.ufo/evidence/round-31/before/c1-at-base.stdout` directly (`mutation sweep runner:
  claimed=80,80,0 observed=106,106,0`; `six-leg regression ledger: claimed=PASS,6,6,0
  observed=PASS,9,9,0`; `mismatches=7` at 36c1d393). Evidence-disposition 56/56 staleness
  is not one of the 12 statements; it is only indirectly corroborated by the
  "effective expectation reconciliation" statement (`tools/evidence-disposition.py
  --selftest`: claimed=34,34,0 observed=66,66,0). Note, not a defect.
- **Criterion 71's norm extends to prose "supersedes" lines, but the counter measures only
  table rows.** The c1-measure.py statement set is the 10 capability rows + depth/calibration
  axis rows; the supersession prose line is not checked by the instrument. Acceptable as a
  rule norm; "Captured by" slightly overstates instrument coverage.

## Verified — falsifier pointers resolve at REV and cited lines match

- 66: `.ufo/waves/round-30/wC/JudgeC1.md:3` = "Non-author review of exploratory claim C1…" ✓;
  `SCORECARD.md:1473` = round-30 table row ending "`unprovable-but-better` by named non-author
  seat JudgeC1 (reviewer), reasons on record" ✓; routing `round-30-verifier-spotcheck.md:40-43`
  = conformance defect with LEARNING.md §Discernment / AXES.md quotes ✓.
- 67: `ColdA01.md:45` = "timeout 240 bash tools/mutate-and-run.sh --regression --keep" with no
  `--workdir` ✓; `ColdA01.md:100` = Errata: broad pgrep/kill terminated two sibling seats'
  bash selftest processes ✓; routing `round-30.md:169-182` = Mistake 5 exactly ✓.
- 68: `attempt2-dead-seats.txt:7-10` = ConnectorOverlap (line 7), RegistryNoHarm, RegressionReplay,
  SelftestsNoHarm ✓; `spec-wC.json:279-284` = item "ConnectorOverlap" at 279 ✓;
  `round-30.md:164-168` = "the overlap was not checked before dispatch" ✓; routing
  `round-30.md:159-168` = Mistake 4 exactly ✓.
- 69: `bind-select-v3.py:2-10` = weaker selector (trace basename + tool call naming
  trace-inputs.py + tool result) ✓; `audit-bound-wC.py:2-9` = stricter post-data conditions
  (bash call with `--out`, later non-error result, trace rev = read_rev) ✓.
- 70: `round-30.md:59` = "The S094 paragraph (`:60-62`) stretches §1 …" exactly at line 59 ✓;
  paragraph-in-entry check: `corpus/knowledge/regression-tally-completeness.md:60` = paragraph,
  61 blank, 62 `## Limits` ✓; routing `round-30-verifier-spotcheck.md:44-45` ✓.
- 71: `c1-at-base.stdout` = `C1_R31: statements=12 mismatches=7 … rev=36c1d393…` with runner
  80/80 vs 106/106 and regression 6 legs vs 9 ✓; `SCORECARD.md:632-636` = round-17 supersession
  line as stated ✓.
- F1–F4 internal citations: F1 `QUALITY.md:683-688` (criterion 60 falsifier) ✓; F2
  `:649-651` (round-30 preamble) ✓; F3 `:705-709` (criterion 62 falsifier) ✓; F4 `:716-721`
  (criterion 63 falsifier) ✓; report refs `ReviewQualityR30.md:22-29 / 35-43 / 45-56 /
  58-71` ✓; F4's `contract.json:45` (round-30, four-file comment-line sandbox recipe) ✓ and
  `drift-sim-union4.txt` (`covered=33/64 … rev=daa11583…`) ✓; `daa11583` is not a lane object
  (as F4 states).
- Base SCORECARD.md is a byte prefix of REV's (`prefix True`; 59 lines added, 0 deleted).

## Residual risk / verification gaps

- C1's own correctness (statement parsing, `append_only`, controls) is handled by the wave-1/2
  control seats (Ctl*, MutCounter, DeterminismProbe, RerunC1Content); not re-run here.
- The v5 re-scoring receipts were produced with the seats' harnesses copied to L1 scratch
  (labels still say "v4_kept"); byte-identity of the executed binder with the committed
  `bind-select-v5.py` is not independently re-established here.
- The wave-2 assembly has not run yet (uncommitted `assemble-w2.sh`/`append-entries.py`);
  the dispatch-context v4 mention is worth fixing before it does.
