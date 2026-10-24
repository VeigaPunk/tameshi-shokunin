# Round 36 claim-set / axis audit

## Attack
Looked for a hidden third or exploratory claim, conflation of the two claimed axes, and a lower non-retired numeric-axis pin that would invalidate calibration as the round-start target.

## Evidence
- `.ufo/evidence/round-36/contract.json` is frozen before data runs and its `claims` object has exactly `C1` and `C2`: C1 is `calibration`; C2 is `depth (surface: the tally-audit counter's predicate completeness)`. No exploratory claim or C3 is declared. The separate S103 source-row/frontier work is recorded as frontier activity, not a measured claim.
- `SCORECARD.md` Round 35, “Numeric axes, measured” (§ lines 1700–1713): depth is `9 → 9`; calibration is `8 → 6`, with the tip measurement `calibration_restraint_score: 6, sections_covered 60/64`. The standalone Retired section says none retired. The round-36 starting-revision monitor receipt independently reports score 6 and 60/64 at `796e08b888849308d0c4d5e932e56833600a139f`.
- Executed the SCORECARD command-D depth census at the exact round-36 starting revision:

  ```sh
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 796e08b:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\\S+\\s+\\S+\\s+\\d+/\\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
  ```

  Output: `recorded_cases=9 depth_score=9`.
- Monitor receipts at `796e08b` (start), `e423c41b` (content/do-nothing control), and `b455001e` (refresh) report respectively calibration 6, 6, and 8; the start and control have 60/64 covered, refresh has 64/64. This is consistent with a refresh effect and does not create another claim.
- `SCORECARD.md` Round 36 and `LOG.md` Round 36 each describe C1 and C2 on the same distinct axes. The historical use of “exploratory” elsewhere in SCORECARD (e.g. round 30) is not a round-36 claim.

## Counterexample tested
Potential counterexample: the S103 frontier/source addition is a third exploratory claim, or “depth surface” duplicates calibration. Contract and round-36 records reject both: S103 is a frontier row, while C1 and C2 have distinct axis labels and separate measured predicates.

## Impacted axes
Calibration and depth (counter predicate-completeness surface). Calibration is the lower round-start numeric pin: 6 < 9.

## Verdict
**VERDICT: PASS — exactly two measured claims (C1 calibration, C2 depth surface), no exploratory claim; axes are distinct; calibration was the lowest non-retired numeric axis at round start (6 vs depth 9).**

Commands/evidence revisions: depth census above at `796e08b`; committed monitor outputs at `796e08b888849308d0c4d5e932e56833600a139f`, `e423c41ba253357ab8c8513f0376dad9d38ab248`, and `b455001e2589b3f4f471d94a3de7e5e549b9f54c`. Read-only source review: `contract.json`, `SCORECARD.md` Round 35–36, `LOG.md` Round 36. No files other than this report were written.