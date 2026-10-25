# ReviewBaselineAxes — round 42 wave 1

Scope: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md` (rounds 36–41 blocks)
and `/home/vgpnk/Projects/shokunin/AXES.md`. Read-only review; no counter was re-run
(deciding runs belong to the L1). All receipts cited exist in the tree and hold the quoted values.

## Findings

### F1. Non-retired axes and latest measured scores (only two axes carry numeric scores)

| Axis | Latest score | Measuring command | Latest measurement | Receipt / cite |
|---|---|---|---|---|
| depth | **9** | `git show "$REV:tools/mutate-and-run.sh" \| python3 -c '…'` (command D, `SCORECARD.md:73`) | round 41, deciding run at `baa18b7bdd637ff175255e82b6bee3c85df0881e`; last-change round 26 (`SCORECARD.md:1536`) | `.ufo/evidence/round-41/census/command-d.stdout` prints `D: recorded_cases=9 depth_score=9` at `a3d6c690`, `2ae00eb7`, `812ee0d1` |
| calibration | **6** | `python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev REV` (strict cold-read monitor, `SCORECARD.md:1537`; instrument exists, `.ufo/evidence/round-21/coldread/measure.py`) | round 41, both revisions print 6 | `.ufo/evidence/round-41/census/command-d.stdout:15-17` → `coldread at a3d6c690 = 6`, `coldread at 2ae00eb7 = 6`; `SCORECARD.md:1922-1927` supersedes the carried `8` as an upper bound (`command C`'s `asserted_mark_upper_bound=8` awards no credit) |

**Calibration (6) is the lowest non-retired axis** — the only other scored axis is depth 9
(`SCORECARD.md:1927`, round-42 `contract.json:10`). No retirement is recorded
(`SCORECARD.md:281-283`; every round 32–41 block restates "no retirement").

**coverage, operability, freshness, adjacency** are non-retired but **carry no numeric score
anywhere in the current record**: the round-31 re-stated current-axes table lists only depth and
calibration (`SCORECARD.md:1534-1537`), and every per-round row for these four is verdict language
("unchanged") without a number or a counting command. Therefore **no axis has a score asserted
without a command** — these four assert no score at all (they also have no command). If the
milestone expects every non-retired axis to carry a score, that expectation fails on these four,
not on missing command evidence.

### F2. Stagnation nudge does not fire for round 42 — confirmed, two independent reasons

1. **Capability within window N=2**: capability rows entered `## Capabilities` at round 40
   (write-path-census-v2, `SCORECARD.md:1889`) and round 41 (write-path census destination
   resolution, `SCORECARD.md:1920`). Window N=2 covers completed rounds 40–41, so the
   no-capability condition is false. Round-41 block: "the stagnation nudge does not fire because
   round 40 added a capability inside the window N=2" (`SCORECARD.md:1902`); round-42
   `contract.json:10` records the same ("a capability entered the table at round 41, inside the
   window N=2").
2. **Not all axes at/above saturation**: the nudge precondition ("every axis the lane owns sits at
   or above the lane's saturation line", `AXES.md` §The stagnation nudge) fails anyway —
   calibration 6 < saturation line 8 (declared `SCORECARD.md:257-262`).

### F3. Note on the round-36 8

Round 36 measured calibration 6 → 8 at `b455001e` (erratum-corrected evidence timing,
`SCORECARD.md:1788`), but round 41 re-measured the monitor at the base and round commits and got 6
at both; the carried 8 is explicitly superseded as an upper bound (`SCORECARD.md:1922-1927`,
receipt `command-d.stdout`). **The latest measured calibration score is 6**, not 8.

## Verification gaps

- Receipts were read, not regenerated; the deciding runs at `baa18b7b` (round 41) are the
  authority for the scores above.
- The cold-read monitor command was not re-run against `baa18b7b` itself; the round-41 receipt
  records 6 at `a3d6c690` (base) and `2ae00eb7` (round commit), which is what the round-41 record
  claims.
