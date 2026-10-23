# ReviewScorecardRows — round-31 SCORECARD block review (wave 2)

Seat: ReviewScorecardRows. Review object: appended round-31 block of `SCORECARD.md` at content revision
`2da841bd9913a2037d2bf612793382e572c9d205` (diff from base `36c1d3933f680125aeefc447f07db0f03004901a`).
All git operations ran in my own scratch clone (`/fast/scratch/hyaku/tameshi-r31-seats/ReviewScorecardRows/c`, detached
at `2da841b`); the frozen counter and every tool ran from that clone or its scratch workdir. No tools installed
(the tooling directive was read; nothing was needed).

## Verdict (first)

**C1 fails at the content revision: `C1_R31_PASS=false`, mismatches=1/12, exit 1.** The calibration axis row states
score **8**, but its own frozen command (the strict cold-read monitor) prints **6** at `2da841bd…`
(`calibration_restraint_score=6`, sections covered 55/64, `box3_full_page=false`, `box3_points=false`; two
independent runs, identical). Every other value and claim in the appended block checked out. The base
`SCORECARD.md` is a byte prefix of the revision (cmp exit 0). The block is well-intentioned but premature: it
re-states calibration as 8 at a revision whose monitor has not yet been restored to 8 (the round's own drift plan
anticipates this; the measured-result row is correctly not yet appended).

## Claim-by-claim table

| # | Claim | Check | Verdict |
|---|---|---|---|
| 1 | Base SCORECARD.md is byte prefix of REV's | `git show BASE:SCORECARD.md \| cmp - <(git show REV:SCORECARD.md \| head -c $(... \| wc -c))` → `PREFIX_OK` | true |
| 2 | C1 predicate sentence in the block matches contract | `contract.json` predicate bytes identical to block's sentence; counter docstring identical; counter sha256 at REV `657fcc1291…` matches contract `counter_sha256` | true |
| 3 | Contract frozen at `c111dab5` before data seats | `c111dab5` is an ancestor of REV (`merge-base --is-ancestor` → 0); `frozen_before_data: true`; kill rule present in contract | true |
| 4 | Before at base: `mismatches=7`/12, PASS=false, exit 1, receipt path | `before/c1-at-base.stdout` at REV prints exactly `C1_R31: statements=12 mismatches=7 …append_only=1 …C1_R31_PASS=false`; 7 MISMATCH lines | true |
| 5 | Target `mismatches=0`, PASS true | design target; not evaluable at REV (no after-measurement exists — `.ufo/evidence/round-31/` has only `before/`, `ctl/`, coldread, counter) | not evaluable now |
| 6 | Measurement protocol (after-value = first full counter run at measurement revision) | process stipulation, no bytes to check at REV | unverifiable |
| 7 | Erratum premise: round-30 row calls JudgeC1 "named non-author seat" | round-30 verdict cell: `` `unprovable-but-better` by named non-author seat JudgeC1 (reviewer) `` | true |
| 8 | Erratum: "JudgeC1 dispatched by L1 and is still the lane (LEARNING.md §Discernment; AXES.md)" | **Neither `LEARNING.md` nor `AXES.md` exists anywhere in the tree at REV** (case-insensitive scan of every path finds only `.ufo/waves/round-20/w1/E05ScorecardAxes.md`). The cited sources do not resolve. Separately, `JudgeC1.md` (round-30 wC) self-labels line 3 "Non-author review". | unverifiable (broken cite) |
| 9 | Erratum: non-author ruling is the hyaku closure's own, spotcheck :47-84 | `round-30-verifier-spotcheck.md:47` header: "Claim C1 … (ruled by this closure)"; line 78 "Ruling: `unprovable-but-better`"; evidence cites `wC/JudgeC1.md:14,22` under "CloseC1Judge path:line" — JudgeC1's report is the supporting source | true |
| 10 | Supersession: three `| capabilities addition |` rows of rounds 23–25 | rows exist at lines 1055 (23), 1148 (24), 1232 (25) | true |
| 11 | Supersession quote of round-17 line | line 632–636 contains "At round 17:", "95/95", "`cases=7`", "56/56" verbatim | true |
| 12 | Round-17 line "was itself stale at base" | at base the frozen receipt observed selftest 106/106 (vs line's 95/95), regression `PASS,9,9` (vs `cases=7`), evidence-disposition 66/66 (vs 56/56) — all three quoted fragments stale at base. (Nuance: the line's unquoted pin-disposition 19/19 was current at base.) | true (for the quoted values) |
| 13 | Saturation sentence exists as quoted | line 261–262: "the nudge does not fire now (depth 6 < 8; calibration pinned 0, candidate 8 pending)"; saturation line 8/10 declared at line 257 | true |
| 14 | "depth is 9 and calibration 8, both at or above the declared saturation line 8/10" | depth 9 ≥ 8 true; but calibration's stated 8 is false (monitor prints 6, see finding 1) — sentence as written does not hold | false |
| 15 | First-working rounds unchanged (all 13 rows) | new rows vs old `\| Capability \|` table (240–249) and additions rows (1055/1148/1232): sources 1, mutation 3, regression 7/10(+26 stated as leg count), repeat 12, pin-disposition 13, witness 13, evidence-disposition 14, verify 15, env-diff 21, wave-accounting 22, command-binding 23, registry-replay 24, interop 25 | true |
| 16 | 10 C1 capability statements = what their frozen commands print at REV | canonical counter run at REV: 10/10 MATCH (census 94 rows exit 0; selftest 106/106 exit 0; regression PASS cases=9 passed=9 exit 0; repeat-control PASS 29 cases; pin-disposition 19/19; witness 39/39; evidence-disposition 66/66; verify exit 0 + 49/49; env-diff 9/9; accounting 8/8). Independent manual runs reproduced every one including `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | true |
| 17 | Depth axis row: score 9, command D prints `recorded_cases=9 depth_score=9`; nine legs at `tools/mutate-and-run.sh:87-95` | command D prints exactly that; lines 87–95 contain exactly nine `#   js/bash-… N/M` leg comments; monitor also reports `recorded_cases=9`, `ledger_legs` = 9 | true |
| 18 | Calibration axis row: score 8 | frozen monitor at REV prints `calibration_restraint_score=6` (55/64 covered; box3_points false). Row states 8 | **false** |
| 19 | Non-C1 rows: command-binding 44/44 exit 0 | direct run: `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0 | true |
| 20 | Non-C1 rows: registry-replay 10/10 exit 0 | direct run: `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0 | true |
| 21 | Non-C1 row: mte-interop SETUP exit 2 on this host | direct run: `MTE_SELFTEST: SETUP (No module named 'jsonschema')`, exit 2; `import jsonschema` → ModuleNotFoundError | true |
| 22 | Hermetic row's receipt claim: f5 receipt classes eight invariant + one nondeterministic (js-round-gate) | receipt-initial.json surfaces: 8 `invariant` + `js-round-gate | nondeterministic` (only one); old row line 248's "one raw-output-variable" is indeed contradicted by the receipt | true |
| 23 | "Measured commit" cells reference the future measured-result row | placeholders; no after-measurement exists at REV — consistent with "appended below only after execution" | true (placeholder, consistent) |

## Findings by severity

1. **[HIGH] Calibration row value is false at the revision (SCORECARD.md ≈:1537).** Row states score 8; its own
   command `python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` prints
   `calibration_restraint_score=6` at `2da841bd…` (covered 55/64, `box3_full_page=false`, `box3_points=false`;
   two runs identical). Consequences: `C1_R31_PASS=false`, exit 1 (canonical counter: `STATEMENT calibration:
   claimed=8 observed=6 (exit=0) MISMATCH`); the Saturation sentence "depth is 9 and calibration 8, both at or
   above … 8/10" (lines 1531–1532) inherits the false value. This is the expected drift state for a content
   revision (fresh cold reads pending), not an error in the measurement machinery — the block simply cannot yet
   state calibration 8. Smallest safe correction: leave the row as the measured-value target and append the
   measured-result row only after the monitor returns 8 (or re-state the row as the pre-read candidate), per the
   block's own protocol.
2. **[MEDIUM] Erratum cites files that do not exist at REV (SCORECARD.md:1496).** "LEARNING.md §Discernment;
   AXES.md" resolve to nothing in the tree at `2da841bd…` (case-insensitive full-tree scan finds only
   `.ufo/waves/round-20/w1/E05ScorecardAxes.md`). The identity claims ("dispatched by L1", "is still the lane")
   cannot be checked against the cited sources; `JudgeC1.md` itself says "Non-author review". Smallest safe
   correction: cite the artifact that exists (`.ufo/waves/round-30/wC/JudgeC1.md`, round-30 spotcheck lines
   40 and 47–84) and state the identity claim without pointing at absent files.
3. **[LOW] Round-17 supersession quote is accurate but omits a nuance.** The quoted fragments (95/95, cases=7,
   56/56) were all stale at base per the base receipt's observations, so "was itself stale at base" holds for
   them; the line's unquoted "pin-disposition 19/19" was current at base. Not a defect; recorded for calibration.
4. **[LOW] Measurement-protocol sentence (lines 1487–1488) is a stipulation, not yet a verifiable claim.** No
   after-measurement exists at REV (consistent with it). No action.

## Residual risk and verification gaps

- The mutation-runner `--selftest` and `--regression` statements were verified through the frozen counter (its
  `obs-*.stdout` receipts are under my scratch `counter-work-1/`); I did not run those two slow tools a second
  time independently. Both returned MATCH with the stated values.
- The monitor (statement 18) was run directly twice from the clone; stable.
- The three non-C1 rows and command D were run directly.
- Not verifiable from repo bytes: "L1 TameshiR31, attempt 1" (identity), the protocol's "first full counter run"
  rule, and the erratum's JudgeC1 identity claim (finding 2).
- No other value in the appended block was found false; 11/12 frozen statements match, and the three non-C1 row
  claims match their commands.

Report: .ufo/waves/round-31/w2/ReviewScorecardRows.md
