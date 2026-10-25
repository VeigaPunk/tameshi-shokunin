# CriticAxis — stagnation-nudge waiver (round 40, contract @ 5641ed84)

## Verdict: attack FAILS — the waiver stands. No difference found on the assigned surface.

The nudge arithmetic in `contract.json` `stagnation` matches the lane's declared
saturation line and window exactly; every frozen predicate was checked against the
canonical SCORECARD and an executed counting command.

## Assigned attack surface: saturation line / window — CONSISTENT

- Rule text: `/home/vgpnk/Projects/shokunin/AXES.md:66-70` — "When every axis the lane
  owns sits at or above the lane's saturation line and no capability has entered the
  table within the lane's stagnation window (both recorded in `SCORECARD.md`), the
  lowest-axis obligation is waived".
- Declaration: `SCORECARD.md:257-261` — "**saturation line 8/10** on each owned axis …
  **Stagnation window N = 2** completed rounds without a capability entering the table."
- Re-affirmed unchanged through the arc: `SCORECARD.md:330` ("Saturation 8 and
  stagnation window 2 remain"), `:393`, `:454`, `:549` ("Saturation8/window2
  unchanged"), and the round-32 invocation `:1557-1558` ("saturation line 8 … window 2").
- Contract: `"saturation_line": 8`, `"window_n": 2` — identical. No difference.

## Supporting predicates — all confirmed

- `depth_score: 9` — executed command D on the pinned base:
  `git show 304e3355705640af2879c772fc9a5c2902c61763:tools/mutate-and-run.sh | python3 -c '…'`
  → `recorded_cases=9 depth_score=9`; identical at HEAD (`5641ed84`).
- `calibration_score: 8` — `SCORECARD.md:1536-1537` (restored 6→8 at round 29, held 30);
  the 8→6 monitor drift at round 35 (`SCORECARD.md:1703-1706`) was restored 6→8 by a
  verified non-author spot-check at round 36 (`:1731-1789`, measured `b455001e`), then
  held 8→8 through rounds 38 (`:1835-1836`) and 39 (`:1864`). Contract value 8 matches
  the last measured statement.
- `last_capability_round: 37` — `SCORECARD.md:1805-1809` admits "bounded ANSI-C
  code_view" with "First-working round | round 37"; the next admitted row before it is
  tally-audit-v3 at round 35 (`:1696-1698`).
- `completed_rounds_without_capability: [38,39]` — `SCORECARD.md:1840-1841` ("no new
  row this round … golden-verdict fixture is a verification instrument, not a new
  repertoire capability") and `:1866` ("Capabilities table: no new row").
- Window semantics consistent with the established test — at round R the nudge is
  suppressed iff any of the last N=2 completed rounds admitted a capability
  (r38/r39 suppressed by r37's capability; r32 fired with last-capability r25).
  For round 40 the last two completed rounds are 38–39 with no capability →
  `nudge: fires` and `lowest_axis_obligation: waived` are correctly encoded.
  (Round 37's own invocation is a separate defect — finding 1 below.)
- Freeze integrity: `sha256 .ufo/evidence/round-40/contract.json` ==
  `sha256(git show 5641ed84:…/contract.json)` == `8a8dd141e16deeae237142821123552c9aabaac17dab45469a7945923cf7047d`; HEAD `5641ed84` is the freeze commit itself.

## Non-blocking findings on the same axis (record, do not rewrite predicates)

1. `SCORECARD.md:1795-1796` — round-37 preamble states "no capability added in rounds
   35–36", but round 35 admitted `tally-audit-v3` (`:1696-1698`). Under the lane's own
   suppression convention used at r38/r39 (capability at R suppresses through R+2),
   round 37's nudge fired one round early — round 36 was the only completed round
   inside its window. Harmless: round 37's C1 worked the lowest axis (calibration)
   anyway, so the obligation was satisfied without needing the waiver. Does not affect
   round 40 (`last_capability_round: 37` is still correct).
2. Rule-wording gap: `AXES.md:68` says "every axis the lane owns", while the lane
   convention applies it to the two *pinned numeric* axes only (depth, calibration —
   cf. `SCORECARD.md` round-21's "Both owned numeric axes"). Coverage, operability,
   freshness, adjacency are owned but unpinned/unscored, so literally their relation to
   the saturation line is unprovable. Settled by precedent since round 21; this
   contract follows the same convention. Smallest safe correction (outside this
   round's frozen claims): amend the AXES.md sentence to "every *pinned numeric* axis"
   — or pin the remaining axes — so future nudges are falsifiable rather than
   conventional.

## Result

- Counterexample: none found on the assigned surface; saturation line 8/10 and window
  N=2 in the contract equal the SCORECARD declaration verbatim.
- Impacted axes: calibration (the axis this seat is judged on) — the frozen
  `calibration_score: 8` is provenance-clean; note 1 is a historical misstatement in
  round 37's preamble, not a round-40 predicate defect.
- Smallest safe correction: none required to the round-40 contract; the r37 preamble
  erratum and the AXES.md "every axis" wording are the only residual fixes, both
  append-only documentation changes.
