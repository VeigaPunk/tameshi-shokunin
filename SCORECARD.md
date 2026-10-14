# tameshi-shokunin — Scorecard

Lane axes per AXES.md (six-axis vocabulary; primary verdicts per
LEARNING.md trends). Probation rounds 1-3 build the initial measurements.
Axes will be pinned with their counting commands as rounds land.

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|
| 1 | depth | seed `SKILL.md`: 22 lines, 0 tables, 0 cited sources, corpus empty | 171 lines: gate-shape decision table (3 rows), fail-closed arm taxonomy (5 rows), 7 mutation-bar rules, 8-step no-permissiveness audit recipe — every rule citing a survey-note line; 3 source notes admitted under it (556+335+105 lines) | `git show 40f8e1f:SKILL.md \| wc -l` → 22; `wc -l SKILL.md corpus/knowledge/*.md` → 171 / 556 / 335 / 105; `grep -cE '^\| ' SKILL.md` → 10 (8 rule rows + 2 header rows); `grep -c 'corpus/knowledge/' SKILL.md` → 3. Re-run 2026-10-14 (TAMESHI-SCRIBE) |
| 1 | calibration | no observation/inference/unknown separation measured anywhere (corpus empty, no notes) | all three notes label every claim and keep the classes apart (kumitate O:33/I:7, kagi [OBS]28/[INF]18/[UNK]7, fleet OBSERVATION×11/INFERENCE×4); unknowns named as unknowns, never green (kumitate §9 ×4; kagi [UNK] ×7; fleet U1–U7); self-caught errors kept as append-only errata, not silently fixed (kagi ER-1 = 16 wrong-line cites + generator analysis); counts quoted from executed counters, never source greps (kumitate 62/42/60/102/39/43 executed vs 62/42/60/71/35/41 literal sites; kagi 250 from suite counters vs static 6/1/0/1/6/2) | `grep -oE '(^|[[:space:]])O:' corpus/knowledge/gates-survey-kumitate.md \| wc -l` → 33 (same for `I:` → 7); `grep -oE '\[OBS\]' corpus/knowledge/gates-survey-kagi.md \| wc -l` → 28 (`[INF]` → 18, `[UNK]` → 7); `grep -cE '^\| §' corpus/knowledge/gates-survey-kagi.md` → 16; `grep -cE '^- U[0-9]' corpus/knowledge/verification-patterns-fleet.md` → 9 (U1–U7 + 2 prediction bullets). Re-run 2026-10-14 (TAMESHI-SCRIBE) |---|
