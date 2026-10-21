# H03 — Calibration-cap review

## Finding and axes

**Agree: numeric calibration remains 8; no promotion or score increase is claimed.** The latest recorded owned numeric axes are tied at depth 8 and calibration 8 (SCORECARD.md, Round 19 §). The declared saturation line is 8/10 on each owned axis; calibration's lane-attainable cap is 8, while depth is capped at 10 recorded cases. The remaining two calibration points require independent promotion review of all boxes (SCORECARD.md:255–260; :571, :692–697). Thus closing more defects or a routed recurrence at the lane's 8-point ceiling does not, by itself, increase the scalar score.

- **Calibration:** remains 8/10; the last two points are outside the lane-attainable cap absent independent review of every box.
- **Depth:** 8/10, tied-lowest at Round 19; no depth score movement is claimed there.
- **Saturation:** declared line 8/10, stagnation window N=2 completed rounds without a capability entering the table. This review confirms the calibration cap; it does not independently recalculate the current nudge state.

## Evidence and recorded commands/results

The calibration score had already reached 8 in Round 16: the scorecard records a 6→8 move from the full-page SKILL cold-read evidence (54/54 buckets); box 3 remained a lane assertion (`[~]`), not an independent `[x]` (SCORECARD.md:571–576). Round 18 then records depth 8 and calibration unchanged at 8 (:647–677).

Round 19's recorded ruler command is:

```sh
python3 .ufo/evidence/round-19/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --check
```

SCORECARD.md:699–705 records baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190` as `corrected=0, open=5, total=5, exit1`; the delivered correction revision `32838a505fc9e15be5e7f6ad4335b0548d263dcd` is recorded as `corrected=5, open=0, total=5, exit0` (:745–754; `.ufo/evidence/round-19/final/c1-final.stdout`). The latter receipt also records `ruler_sha256=7af3e951bf67f7671954dee33aaa4dc183a642fce85cbc2d9d782085f856cf72`.

The scorecard adjudicates that Round 19 C1 as **improved** for five named defect corrections, but explicitly records numeric calibration `8→8`, with no independent-promotion re-score or current-page cold-read credit (:695–697, :725–727). The final monitor receipt records `calibration_restraint_score: 8`, strict input-keyed `60/60`, restraint `8`, and no overrides (`.ufo/evidence/round-19/final/monitor-final.stdout`; SCORECARD.md:756–760). Although that receipt has `coldread.box3_full_page: true`, the scorecard limits the evidence: these are not a blind/independent cold-read or required-command coverage. The final verdict states **no promotion**, no axis retirement, and no new capability-table claim; the 18 Round-18 guard survivors and source-anchor/backlink debts remain open (:767–769).

These are the command and outputs **recorded in the scorecard/receipts**, not a rerun by this seat. This was a read-only evidence review; no checker or suite was run.

## What is needed for 9–10; promotion status

The explicit scorecard condition for the last two points is an **independent promotion review of all boxes**. Lane-dispatched seats' `[~]` assertions do not satisfy that independent review; the scorecard says they earn lane-assertion points only (:573–576). Round 19 also expressly does not claim independent promotion or current-page cold-read credit. Therefore neither the full-page flag in the L1-authored monitor nor the five corrected defects can be treated as that missing independent review.

No promotion and no increase above 8 are claimed. Round 19's verdict is “improved” for its named-defect unit, with scalar calibration unchanged. The Round-20 contract's stated restraint (retain 8; no promotion) is consistent with this evidence.

## Counterexample / defect check and smallest safe correction

No defect found in the calibration cap or the Round-19 scalar verdict. One status-text caution: SCORECARD.md:255–260's “nudge does not fire now” parenthetical is paired with fleet-Round-1 values (`depth 6`, calibration pinned 0/candidate 8), not the later 8/8 state. The paragraph dates the declaration to fleet Round 1, and the later Round-1 correction explicitly supersedes its calibration-0 detail (:219–220), so it must not be reused as a current nudge judgment. Smallest safe correction, if that status is presented as current, is to label the parenthetical explicitly “as of fleet Round 1” and evaluate the N=2 window separately for the current round; do not change the 8-point calibration cap or imply promotion.