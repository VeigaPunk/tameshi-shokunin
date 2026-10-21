# FTeachingSweep — falsification report

Date: 2026-10-21. Scope: `.ufo/waves/round-19/w1/TeachingSweep.md` and the cited runbook, QUALITY, round-19 lesson, correction ruler and receipts. Compared source evidence with delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c9`; no lane suites, selftests or receipt argv were run.

## Strongest assertion and verdict

**Assertion:** “No unreflected receipt-correction teaching found” (TeachingSweep §4.1, lines 55–60).

**Agree, narrowly for the five C1 defects.** The scoped runbook teachings map to the correction criteria and lesson. The path-scoped `corpus/lessons/operator-*.md` absence is also accurately distinguished from the existing knowledge runbook. I found no sixth C1 defect in this source sweep.

Read-only arithmetic over the ruler’s pinned `source-baseline.txt` and `source-round18-final.txt` reproduces the claimed comparison: hashes match `SOURCE_PINS`; 62→76 rows; changed IDs S001/S052/S056/S057 (`used-by`) and S008 (`status`,`used-by`) = 6 cells; 14 added IDs, none removed, and zero net non-row deletions. `sources-diff.txt` says 25 added / 5 deleted lines. This supports the row/cell distinction, not a 5/5 result at `55e1`.

The retained receipt metadata also matches the frozen `measure.py` predicates: witness argv is `python3 tools/bash-witness-study.py selftest`, revision `4b7c682…`, exit 0, with both stream digests and exact supersession entries; the final measurement argv names `round-18/measure.py --repo … --rev 4b7c682… --explain`, revision matches, exit 0, and the companion pins the instrument. The captured measurement stdout reports 60/60 and restraint 8; this is historical evidence, not C1’s current 5/5 receipt.

## Concrete stale statement

TeachingSweep §4.2 (lines 66–72) says any correction to its path-scope nuance belongs to a **future** round. That timing is falsified by the delivered round-19 lesson itself: its Build-wave findings already append that the lessons-glob absence is path-scoped and that `corpus/knowledge/operator-runbook.md` exists (round-19 lesson, “The lessons glob’s teaching absence is path-scoped…”). The report’s underlying path observation is accurate; its future-round disposition was stale by `55e1`. This is not a sixth C1 defect and earns no calibration credit.

## Receipt boundary / residual unknown

`before.json` records `0/5` at baseline `7243e7…`; `after-21e7932.json` records `5/5` at `21e7932…`. Both carry ruler SHA `c538c33…`, not the frozen `55e1` ruler (the `measure.py` blob at `55e1` is `d13dc4fb…`; its earlier observed file SHA was `bb651e…`). There is no `.ufo/evidence/round-19/after.json` in `55e1`. Thus the old 5/5 receipt does not verify the delivered revision under its ruler; final same-ruler before/after measurement remains L1’s task. No source/report conclusion here supplies that missing receipt or producer authentication.