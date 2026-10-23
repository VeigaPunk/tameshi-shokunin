# ReviewMistakes — review of ScribeMistakes31 mistake rows (round 31, wave 2)

Reviewed item: `.ufo/waves/round-31/w1/ScribeMistakes31.md` (draft rows 1-4, plus the
ColdA09 section-26 note). For each row: evidence pointer resolution and fidelity,
captured-by correctness, and fix-falsifiability ("shown able to fail"). All file reads
were done at the current lane worktree; git history queries were read-only
(`blame`, `log -S`, `show`).

## Verdict table

| Row | Class | Evidence resolves? | Evidence says what row claims? | Captured-by right? | Fix shown able to fail? | Row verdict |
|---|---|---|---|---|---|---|
| 1 | Reviewer authority from seat label | yes | yes | yes | partial (weak demonstration) | include, with minor note |
| 2 | Citation range extends beyond paragraph | yes | yes | yes | yes | include, clean |
| 3 | Process deaths misattributed to timeouts | yes | yes | yes | yes | include, clean |
| 4 | Stale self-assessment literals | yes | one sub-claim wrong (evidence-disposition suite) | yes | yes | include, but correct the round-17 receipt claim |

## Findings by severity

### Medium — Row 4 misstates the round-17 receipt for the evidence-disposition suite

- Row 4 claims: "The round-17 receipt `.ufo/evidence/round-17/c2-after-2a22ade.json:101-109,172-183`
  records those suites as 19/19 and 56/56."
- Verified: the pin-disposition-selftest entry (JSON lines ~101-113) ends with
  `SELFTEST: PASS (19/19)` — that half is accurate.
- The evidence-disposition-selftest entry (JSON lines ~171-187) ends with
  `SELFTEST: FAIL (2/56 failed: v2-historical-dangling, v2-historical-replace-ref; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.qeh1_gpg)`.
  The suite is 56 cases, not 56/56 passing; the two failures are setup/process errors
  (git identity unset in the environment), not assertion failures.
- Also, the base receipt's mismatched statement at `.ufo/evidence/round-31/before/c1-at-base.stdout:7`
  is named "effective expectation reconciliation" (claim 34 vs observed 66) — the
  SCORECARD capability row 246, whose command is `python3 tools/evidence-disposition.py --selftest`.
  The row's shorthand "evidence-disposition selftest 34 vs 66" is a defensible alias,
  but the cited receipt line is the authority.
- The row's conclusion still holds (claim 34 vs observed 66 exists; the literal is
  stale), so this does not invalidate the row.
- Smallest safe correction: replace "records those suites as 19/19 and 56/56" with
  "records pin-disposition 19/19 and the evidence-disposition suite at 56 cases
  (FAIL 2/56, setup errors)"; cite `c1-at-base.stdout:7` (34 vs 66) as the pairwise
  divergence evidence.

### Low — Row 1 "Shown able to fail" is a restatement, not a committed check path

- The fix (append erratum stating JudgeC1 was lane-dispatched/lane-authored) is correct
  and matches the routed defect at `round-30-verifier-spotcheck.md:208-209`.
- But the "Shown able to fail" text ("the same round-30 record contains both the
  dispatch fact and the 'non-author' label") documents the contradiction, not a
  committed path where the fix's own check would fail. The concrete falsifying pair
  exists: SCORECARD.md:1473 ("named non-author seat") vs `round-30-verifier-spotcheck.md:41`
  ("JudgeC1 was dispatched by the L1 and is still the lane"). Suggest pointing the
  sentence at that exact pair so the fix's check (label consistency) has a committed
  failing instance.

## Row-by-row verification detail

### Row 1 — reviewer authority from seat label

- `SCORECARD.md:1473` resolves; text: "...`unprovable-but-better` by named non-author
  seat JudgeC1 (reviewer), reasons on record". Claim accurate.
- `round-30-verifier-spotcheck.md:40-43` resolves; states JudgeC1 was dispatched by the
  L1, C1 ruling belongs to the closure, JudgeC1's report is supporting evidence only.
  Claim accurate.
- Routed correction at `round-30-verifier-spotcheck.md:208-209` resolves: "append an
  erratum naming this closure as the non-author C1 reviewer (append-only; do not edit
  the round-30 block)". Fix text matches.
- Captured-by correct: Conformance step-1 defects at `:39-43`.
- Shown able to fail: weak (see Low finding).

### Row 2 — citation range extends beyond paragraph

- `round-30-verifier-spotcheck.md:44-45` resolves: "The lesson cites the S094 paragraph
  of the knowledge entry as `:60-62`; the paragraph is line 60 only (61 blank, 62
  `## Limits`)". Accurate.
- Opened source `corpus/knowledge/regression-tally-completeness.md:60-62`: line 60 is
  the paragraph, 61 blank, 62 `## Limits`. Accurate.
- Captured-by correct: CloseSpotSources named at spotcheck line 45.
- Fix (cite erratum `:60-62` → `:60`) matches routed defect 5 at `:215`. Shown able to
  fail: yes — the committed lesson's `:60-62` includes the `## Limits` heading, so a
  paragraph-boundary check fails on the committed text; the one-line `:60` pointer is
  falsifiable against the opened source.

### Row 3 — process deaths misattributed to timeouts

- `wC/ColdA09.md:139-146` resolves: both replay attempts killed by ColdA09's own 300s /
  560s timeouts, no receipt exists, run not in commands_executed. Accurate.
- ColdA01 transcript `TameshiR30A3.ColdA01.jsonl:173-176` resolves: cleanup command at
  07:32:43.234Z; output at line 175 shows `killing 321391 bash /tmp/tameshi-r4-2-regression.1e5R9E/bash-checklist-run/mutant-D2.target.checklist-run.sh --selftest`
  and `killing 321402 bash ... --tsv ...` — both bash processes under
  `/tmp/tameshi-r4-2-regression.1e5R9E`. Accurate.
- `wC/ColdA01.md:100` erratum: "a broad pgrep/kill terminated two bash selftest
  processes belonging to a sibling seat's regression workdir
  (/tmp/tameshi-r4-2-regression.1e5R9E ...)". Accurate.
- Closure `round-30-verifier-spotcheck.md:181-186` confirms workdir ownership, the
  07:32:43Z kill, and the misattribution. Accurate.
- `wC/ColdB09.md:34` confirms the complete nine-leg replay (`REGRESSION: PASS (cases=9 passed=9)`). Accurate.
- Captured-by correct: Disclosed breaches `:181-186`.
- Fix: append section-26 note preserving the no-receipt limit and separating the two
  deaths from the incomplete replay attempts. The drafted note is consistent with both
  ColdA09.md section 26 and the closure; no invented facts.
- Shown able to fail: yes — the committed transcript kill lines are the falsifying
  record for ColdA09's timeout attribution.

### Row 4 — stale self-assessment literals

- `SCORECARD.md:64-67,240-249` resolves: two axis rows (depth 6, calibration 0) at
  `:66-67`; ten capability rows at `:240-249` whose literals are 44 rows, 80/80,
  6 legs, 29, 18/18, 39/39, 34/34, 49/49, 9/9, 8/8. Accurate.
- `before/c1-at-base.stdout:1-13` resolves: 7 MISMATCH / 5 MATCH,
  `append_only=1`, `C1_R31_PASS=false`; `before/c1-at-base.exit` contains `1`. All
  seven claimed pairs match lines 1 (44 vs 92), 2 (80 vs 106), 3 (6 vs 9), 5 (18 vs 19),
  7 (34 vs 66), 11 (depth 6 vs 9), 12 (calibration 0 vs 8). Accurate (except the row-7
  statement name, see Medium finding).
- `SCORECARD.md:632-636` resolves: "The rows stay as written; this line supersedes
  their counts". Accurate.
- History claims verified read-only:
  - `blame -L 64,67` → `cd31c6b` 2026-10-15 02:15:52 -0300. Accurate.
  - `blame -L 240,249` → sources-registry `121696b` 2026-10-19 19:22:35 -0300;
    mutation/six-leg `c7986cd` 2026-10-19 19:15:33 -0300. Accurate.
  - `log -S '| S047 |'` → `4acc607` 2026-10-20 02:02:45 -0300 (round 13). `log -S '| S045 |'` → `c7986cd`. Accurate.
  - `corpus/SOURCES.md:54-56`: S045 B, S046 C, S047 A. Accurate.
  - `show c699c8c -- tools/mutate-and-run.sh` adds `js-round-gate` leg and its
    check; ledger 6→7. Accurate. `runner-selftest.txt:84-87` records 83/83;
    `SCORECARD.md:633` records 95/95 vs literal 80. Accurate.
  - `show 2a22ade -- tools/pin-disposition.py` adds `detect_branch`
    (detached-HEAD branch-tip fallback); `tools/evidence-disposition.py` diff adds
    v2 historical-input cases. Accurate. `SCORECARD.md:625` records calibration 6→8;
    `SCORECARD.md:303-315` records round-12 calibration 6. Accurate.
  - Ninth leg `a08e85c` 2026-10-22 07:06:40 -0300; eighth `58e5d53` 2026-10-20
    17:20:09 -0300; both confirmed; base receipt observes nine. Accurate.
- Fix: use frozen contract counter with `append_only=1` and preserve base prefix —
  matches `contract.json` predicate/target (`.ufo/evidence/round-31/contract.json`).
  Shown able to fail: yes — stored base receipt exit 1, seven MISMATCH, `C1_R31_PASS=false`.
- The round-17 receipt sub-claim is wrong (see Medium finding).

## ColdA09 section-26 note cross-check

The draft's note (ScribeMistakes31.md line 15) was checked against `wC/ColdA09.md`
section 26 and the round-30 closure `round-30-verifier-spotcheck.md:181-186`:

- "ColdA01's cleanup at 07:32:43Z killed two bash selftest processes in my replay
  workdir /tmp/tameshi-r4-2-regression.1e5R9E" — matches transcript lines 173-176 and
  closure lines 181-183.
- "retract the attribution ... to my own 300s/560s timeouts" — matches ColdA09.md
  lines 140-141 (self-attribution) and closure lines 185-186 (misattribution flagged).
- "My section still has no complete --regression receipt" — matches ColdA09.md lines
  141-142.
- "complete nine-leg replay is ColdB09's (wC/ColdB09.md:34)" — confirmed.
- "separate no-harm run is RegressionReplayHead's (round-30-verifier-spotcheck.md:184-185)"
  — confirmed.
- No contradiction found between the note and either source.

## Other bounds compliance

- No files edited other than this report; no gates/selftests/counters run; read-only
  git queries only; no `jj`; no processes started or killed; no sibling scratch dirs
  touched. Tooling: no installs made.
