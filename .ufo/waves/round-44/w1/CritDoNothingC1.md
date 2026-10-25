# CritDoNothingC1 — round-44 C1 controls

Axis: calibration. No tool installs.

## 1) Round-43 red-before at base

Command:
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-43/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 506e99c7b73c85711f066895984d501fcf7539cd --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685`

Output (verbatim):
`C2_R43: self_pin=1 classes=7 m6=0 m7=1 m8=0 m10=0 m11=0 m12=0 m13=0 total=1 records=4 sources_rows=114 standing=114 receipts=17 revisions=4 m13_probe=standing=7_column0=113_valid=114 rev=506e99c7b73c85711f066895984d501fcf7539cd freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=false first=m7:SCORECARD.md#round-43_unknown_S256`

Exit: 1. Independently checked the stored receipt `.ufo/evidence/round-44/before/c2-old-at-base.stdout`; its line contains the same m7/total/first/pass result for the same pinned base and freeze.

## 2) Assignment-mask deletion selftest

Copied `.ufo/evidence/round-44/calibration/measure.py` to `/tmp/tameshi-r44-CritDoNothingC1/measure.py` and removed the `ASSIGN_ID.sub(...)` application line in the scratch copy only. Ran:
`python3 /tmp/tameshi-r44-CritDoNothingC1/measure.py --selftest`

Output:
```
C2_R44_SELFTEST: cases=16 failed=2
FAIL T6_safe_floor_value_not_citation ['r unknown S256']
FAIL T6_assign_with_spaces_masked ['r unknown S256']
VERDICT: FAIL
EXIT=1
```

The requested `T6_safe_floor_value_not_citation` fails with the exact unknown S256 hit. The whitespace-assignment variant also fails for the same reason.

## 3) Cheapest alternate path without mask fix

The defect is in the newest round-43 SCORECARD history block, where the deciding-run field includes `safe_floor=S256`. At the pinned base, that block is present (`git show 506e99c7...:SCORECARD.md`), and the contract requires append-only records. Altering/removing the old field would be a historical rewrite, hence not a legal append-only move. Adding another appended record does not erase the `S256` token in the already-scanned SCORECARD block; the unchanged round-43 counter will still interpret it as an unknown citation. Therefore no legal append-only SCORECARD path can achieve C1's target total=0 without repairing the value-vs-citation mask. Editing the scorecard block in scratch could demonstrate suppression but is not an append-only/legal path and was not treated as a valid alternative.

Evidence anchors: contract `.ufo/evidence/round-44/contract.json:21-23,29,36`; round-43 counter `.ufo/evidence/round-43/calibration/measure.py:448-464` scans the newest block and applies value masks but has no assignment-form mask; round-44 counter `.ufo/evidence/round-44/calibration/measure.py:89-110` defines and applies `ASSIGN_ID`; base SCORECARD round-43 block includes `safe_floor=S256` (line 2091 in `git show` output).
