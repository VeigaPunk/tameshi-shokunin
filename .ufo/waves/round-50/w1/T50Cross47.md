# T50Cross47 — C1 independent cross-coder, spot-check round 47

Seat: T50Cross47. Judged against the lane tree at base `e3729de862f73ae080d98fcf522a7081ce16e40a` (round-50 spot, read-only; no T50Disp* files read). Items R47.1–R47.7 from `.ufo/evidence/round-50/c1/defects.json` (routed_at `473336d9d789f6081195e7376d17836a24666bc3`), coded independently from `corpus/lessons/round-47-verifier-spotcheck.md` lines 103–109.

Disposition: 4 fixed (R47.1, R47.3, R47.4, R47.6), 3 declined (R47.2, R47.5, R47.7). No R47.x id is named in the newest `**Planned (round` paragraph of SCORECARD.md at base (line 2410, `**Planned (round 50):**`), so `open` is unavailable to any of them under the counter's rule.

## R47.1 — fixed

Ask: superseding row for `six-leg regression ledger` stating the stable observation (or declared-unstable form the counter can score); C1 counter observation repeatable N≥3 per profile or declared nondeterministic class; `hermetic env-differential probe` same treatment.

Findings (all `git show e3729de8:SCORECARD.md`):
- Line 2334: round-48 superseding table row `six-leg regression ledger` → `REGRESSION: PASS (cases=9 passed=9`, exit 0, deps `fleet-root,node`, **runs 3 stable**.
- Line 2340: `hermetic env-differential probe` row now carries **runs 3 stable** (same emit protocol as the other 21 rows).
- Line 2328: declared nondeterministic class for the six-leg row: "`six-leg regression ledger` is known to be nondeterministic under concurrency", with the observed class `stable` stated from three observation rounds of profiles P0–P5 (line 2326, `--emit` receipt `.ufo/evidence/round-48/calibration/emit-15b1521.stdout` committed at base).
- The `runs 3 stable` text is absent at routed_at (`git show 473336d9:SCORECARD.md | grep -c 'runs 3'` → 0). Introduced by commit `c7586b9a` (round-48 content revision; touches SCORECARD.md; ancestor of REV, not of routed_at).
- Counter only: CTL_B refusal of relabelled rows without re-observation (line 2376) confirms the N≥3 ask is enforced, not cosmetic.

Doubt resolved: the rows are not a relabel of old observations — the counter refuses relabelled rows and the receipt of the three-round/six-profile emit is committed.

## R47.2 — declined

Ask: commit selftest receipts for the three round-47 counters, `addition-lint.py`, and the criterion-93 falsifier block.

Findings (`git ls-tree -r --name-only e3729de8`):
- Only committed selftest receipts: `.ufo/evidence/round-48/selftest/c1-r48-selftest.{stdout,exit}`, `c2-r48-selftest.{stdout,exit}` (round-48 counters, content `C1_R48…`/`SELFTEST 01…`) and `.ufo/evidence/round-49/control/c1-selftest.{stdout,exit}`, `c2-selftest.{stdout,exit}` (round-49 counters).
- No round-47 C1/C2/C3 counter receipt exists (full round-47 evidence tree has none; grep for `r47.*selftest|c3.*r47` → empty).
- `.ufo/evidence/round-47/quality/c91-92-falsifiers.stdout` stops at `CRITERION-91/-92-FALSIFIER-OK`; criterion-93 output is uncommitted (conformance defect 4). `.ufo/evidence/round-48/quality/c94-96-falsifiers.*` covers 94–96 only.
- `addition-lint.py` selftest tally exists only as a wave copy (`.ufo/waves/round-48/w1/selftest/addition-lint.*`), which cannot satisfy the evidence path rules.
- `.ufo/evidence/round-47/after/addition-lint.stdout` is the deciding-run lint (`ADDITION_LINT: files=6 findings=0`), not a selftest receipt.

## R47.3 — fixed

Ask: append a named correction for `corpus/lessons/round-47.md:117-118` dependence sets.

Findings (`git show e3729de8:corpus/lessons/round-48.md`):
- Line 108: `## Correction C1-R48-1 — the round-47 dependence sets (unreceipted freeze-time observation)`.
- Lines 114–117: quotes `corpus/lessons/round-47.md` lines 117–118 verbatim (the `observed dependence sets` paragraph).
- Line 178: `**C1-R48-1 (corrects `corpus/lessons/round-47.md:117-118`; the file is never rewritten).**`; the bounds section states round-47.md is not rewritten (append-only correction, QUALITY 4).
- Round-48.md is absent at routed_at (`git show 473336d9:corpus/lessons/round-48.md` → absent); introduced by commit `50545328e` (lesson draft; ancestor of REV, not of routed_at).

## R47.4 — fixed

Ask: when refusing `r8-predictive-test-selection-cost.md` again, cite the unopened-row reason (QUALITY 10) rather than `PROVINCE.md:14-18`.

Findings (`git show e3729de8:corpus/lessons/round-48.md`):
- Line 270 (Correction C1-R48-2, appended): the refused row now reads `unopened row: its source: cites S205 / arXiv 1810.05286 and the lane has no such row (grep -c '1810.05286' corpus/SOURCES.md → 0, S205 → 0) … — **QUALITY 10** (decisive) and **QUALITY 2**`, and "The round-47 `PROVINCE.md:14-18` cite is withdrawn as the decisive reason".
- The old weak-cite rows survive only as quoted history being corrected (lines 218, 224). Same commit `50545328e`.

## R47.5 — declined

Ask (compound carried list): round-45 per-snapshot fetch receipt and S026/S093/S108 anchor refresh; delete/re-pin dead `brace_depth_at` helpers; selftest cases for the round-47 C1 (8) and C3 (10) counter survivors; a located-name (entry-author) check.

Findings: the fetch receipts landed (`.ufo/evidence/round-48/freshness/sources/S026/S093/S108.receipt.json` + snapshot files), but:
- `brace_depth_at` still exists at base in both helpers (`git grep -n 'brace_depth_at' e3729de8 -- tools/` → `tools/tally-audit-v2.py:135`, `tools/tally-audit-v3.py:234`).
- No selftest cases were added for the round-47 C1/C3 survivors (no round-47 counter receipt at all; Planned round 49/50 still list them).
- Located-name check is unbuilt (Planned round-50 paragraph line 2410 lists "carried items from round 48's list").
Not every ask is met → not fixed; not named in the newest Planned paragraph → not open; declined.

## R47.6 — fixed

Ask: run the falsification wave in the round that lands the entries (the round-47 40-seat round below the floor left additions/restated rows unattacked).

Findings:
- Round 49 landed S269/S270 and the F10 pilot entry at content `9b9b2a0`/`f181a961`, then dispatched the wave-2 falsify spec in the same round (`5f597fa8` "wave-2 falsify spec and dispatch (33 seats) against candidate f181a961") and integrated its results before deciding (`54a523654`).
- Committed artifacts: `.ufo/waves/round-49/spec-w2.json`, `w2-dispatch.json`, `w2-results.json`, `w2.ready.dispatched`, `w2/` seat reports.
- `corpus/lessons/round-49.md` line 118 records the wave-2 re-reads (`…/round-49/w2/T49W2Reread*.json`); line 91 records wave-2 precheck runs on the candidate; line 99 records the wave-2 access-trace/oracle-mutation checks. Line 118 is the evidenced row (carries key `w2`); introduced by commit `54a523654` (touches round-49.md; ancestor of REV, not of routed_at; file absent at routed_at).

Doubt resolved: the literal phrase "falsification wave" is not in citable non-wave files, but the dispatch/result artifacts and lesson records show the wave ran in the landing round.

## R47.7 — declined

Ask: SHONEN boxes all `[~]`; none fully checkable by a non-author; promotion stays operator-owned.

Findings: `git show e3729de8:SHONEN.md` → all four boxes `[~]` (lines 5, 7, 9, 11). This is an observation of state; promotion is operator-owned, so no post-routing lane commit can fix it. Declined.

## Evidence-rule compliance (checked mechanically)

For every fixed row: path resolves at REV and is not a spot-check/ledger/C1 instrument; lines single `a-b` with b-a ≤ 30; whitespace-normalised excerpt (15–400 chars) occurs within the cited lines; ≥1 key (case-insensitive) in the excerpt; excerpt absent from that path at routed_at; commit is full 40-hex, ancestor of REV, not ancestor of routed_at, and touches the cited path; no ACK_WORDS on cited lines. Verified with a Python harness over `git show` blobs (all rows printed `ok=True`).

## Summary

- R47.1 fixed: round-48 superseding table gives six-leg regression ledger and hermetic env-differential probe rows with `runs 3 stable` and a declared nondeterministic class (SCORECARD.md:2328/2334/2340; commit c7586b9a).
- R47.2 declined: no committed selftest receipts for the three round-47 counters, addition-lint.py, or the criterion-93 falsifier block.
- R47.3 fixed: round-48 lesson Correction C1-R48-1 appended for round-47.md:117-118 dependence sets (lines 108/178; commit 50545328e).
- R47.4 fixed: Correction C1-R48-2 re-refuses r8 with QUALITY 10 decisive, PROVINCE cite withdrawn (line 270; commit 50545328e).
- R47.5 declined: compound carried item partially landed (fetch receipts yes; brace_depth_at helpers, survivor cases, located-name check no).
- R47.6 fixed: round-49 wave-2 falsify ran in the landing round (lesson line 118; dispatch artifacts; commit 54a523654).
- R47.7 declined: SHONEN boxes remain [~]; promotion operator-owned; observation, not fixable.
