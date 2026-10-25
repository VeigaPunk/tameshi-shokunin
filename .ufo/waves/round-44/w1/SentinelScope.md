# SentinelScope — round-44 scope audit (sentinel)

Seat: L1Tameshi44.SentinelScope. Item: list every file round-44 changes touch; confirm none lies outside the lane, in a sibling, in /home/vgpnk/Projects/shokuknow, or in /home/vgpnk/Projects/shokunin/.ufo/state.

## 1. Planned touch set (all verified in-lane)

| # | Path (rel. lane root) | Kind | State |
|---|---|---|---|
| 1 | corpus/SOURCES.md | append S160 row + used-by log | exists; `SOURCES.md:456` already declares "Next unused id: S160." (row absent — grep `^ {0,3}\| S160 ` = 0 at base, per contract C2) |
| 2 | corpus/knowledge/r44-anchor-refresh-rule.md | new | absent; `r43-survivor-resolution-rule.md` is the naming precedent (corpus/knowledge/) |
| 3 | corpus/lessons/round-44.md | new | absent; round-43.md etc. are the precedent (corpus/lessons/) |
| 4 | SCORECARD.md | append round-44 block | exists; newest block is "## Round 43" (`SCORECARD.md:2048`), carrying `**Planned (round 44):**` at :2076 |
| 5 | LOG.md | append | exists; latest entry round 43 (`LOG.md:2221-2263`) |
| 6 | .ufo/evidence/round-44/** | receipts | exists: contract.json, before/c2-old-at-base.stdout, before/c2-new-at-base.stdout, calibration/measure.py, census-start.{stdout,stderr}, sources/stryker-equivalent-mutants.html; `after/` and `control/` exist, empty — landing receipts go there |
| 7 | .ufo/waves/round-44/** | wave specs/reports | exists: spec-w1.json (reportDir=".ufo/waves/round-44/w1"), dispatch-w1.json, build-spec.py, w1/swarm-registry.json |
| 8 | .ufo/waves/round-43/w1/RevC2Classes.md | dirty — commit or revert | the only working-copy change in the lane (see §3) |
| 9 | .ufo/waves/round-44/w1/SentinelScope.md | this report (draft, authorized by item) | written |

## 2. Boundary verification

`realpath -m` of every planned path resolves under `/home/vgpnk/Projects/shokunin/tameshi-shokunin`:

```
corpus/SOURCES.md → …/tameshi-shokunin/corpus/SOURCES.md
corpus/knowledge/r44-anchor-refresh-rule.md → …/tameshi-shokunin/corpus/knowledge/r44-anchor-refresh-rule.md
corpus/lessons/round-44.md → …/tameshi-shokunin/corpus/lessons/round-44.md
SCORECARD.md → …/tameshi-shokunin/SCORECARD.md
LOG.md → …/tameshi-shokunin/LOG.md
.ufo/evidence/round-44 → …/tameshi-shokunin/.ufo/evidence/round-44
.ufo/waves/round-44 → …/tameshi-shokunin/.ufo/waves/round-44
.ufo/waves/round-43/w1/RevC2Classes.md → …/tameshi-shokunin/.ufo/waves/round-43/w1/RevC2Classes.md
.ufo/waves/round-44/w1/SentinelScope.md → …/tameshi-shokunin/.ufo/waves/round-44/w1/SentinelScope.md
```

- Siblings: fleet root `/home/vgpnk/Projects/shokunin/` contains the lane plus sibling lanes (kagi-shokunin, kumitate-shokunin, mado-shokunin, …). No planned path references a sibling or the fleet-level files (PROTOCOL.md, AXES.md, MANIFEST.json, m-rev-vs-rev.py, scripts/hyaku/…).
- `/home/vgpnk/Projects/shokuknow` (assimilation, read-only): top-level is MANIFEST.json, README.md, RUNBOOK.md, doctrine/, lanes/, merge/, etc. No planned path overlaps; no campaign file is written.
- `/home/vgpnk/Projects/shokunin/.ufo/state`: holds per-lane aggregator files (`tameshi.mission/.out/.round`, `tameshi.report-baseline`, …). No planned path overlaps; round-44 evidence/waves live under the lane's own `.ufo/`.

Conclusion: no planned path lies outside the allowed set. Zero exceptions to report.

## 3. Dirty `.ufo/waves/round-43/w1/RevC2Classes.md` — commit or revert

`jj status` (run in lane, read-only) shows exactly one working-copy change:

```
Working copy changes:
M .ufo/waves/round-43/w1/RevC2Classes.md
Working copy (@) : mknqtklt 2719aeab (no description set)
Parent commit (@-): plrnlsko 315453b8 master | round-44: base census receipt
```

Diff: `jj diff --git` / `--stat` → 61 insertions, 46 deletions. Content: the round-43 reviewer seat's report is updated to the newest counter pin — A13/A14 rework (m7 value-id masking via `VALUE_ID_AFTER`/`VALUE_ID_BEFORE` at `measure.py:81-82`, m8 glob-skip narrowing at `measure.py:221/223`, m10 supersede coverage at `measure.py:245-314`, shifted line refs). This is precisely the repair the round-44 C1 claim describes (S-id bound to an assignment is a value, not a citation; genuine unknown/unmined still flag).

Recommendation: **commit** (retain). It is in-lane, documents the actual round-43 C2 class text at the round-44 base, and is consistent with the round-44 contract's C1 before-state narrative. Reverting would drop that provenance and leave the working copy clean but the round-43 w1 record stale vs the committed counter. (Sentinel is read-only; the commit decision is the main agent's.)

## 4. Notes

- The round-44 evidence receipts already committed at the freeze: `contract.json`, `calibration/measure.py` (sha256 c0c6199f… per contract), `sources/stryker-equivalent-mutants.html` (sha256 79f6501a…). `after/` receipts (deciding-run stdouts) and `control/` receipt (`mask-removed.selftest.stdout`) are expected in-set additions at landing.
- No scratch artifacts left in /tmp (none created; this audit is read-only except this report).
