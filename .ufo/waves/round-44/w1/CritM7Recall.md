# CritM7Recall — mask recall preservation

Axis: calibration. Evaluated `m7_citations` in `.ufo/evidence/round-44/calibration/measure.py` (lines 92–115) against registry rows S001 mined, S002 queued, S153 mined. The requested `/tmp/tameshi-r44-CritM7Recall-/` directory was absent, so the committed counter module was loaded directly; no lane files were changed.

Fixture outputs (exact):

```text
a: ['fixture unknown S777']
b: ['fixture unmined S002']
c: []
d: []
e: []
f: []
```

Verdict: PASS — unknown and unmined genuine citations remain detected, while a mined citation and staged, next-unused, and assignment-value IDs do not produce hits. This confirms the six specified cases only; it does not establish broader recall beyond these fixtures.

Evidence: counter applies the staged/next-unused masks and assignment-ID mask before scanning IDs (`measure.py:75-89,101-114`). No tools installed.
