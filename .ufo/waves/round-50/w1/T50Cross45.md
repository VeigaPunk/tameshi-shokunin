# T50Cross45 — C1 independent cross-coder, spot-check round 45

Seat: T50Cross45. Base: `e3729de862f73ae080d98fcf522a7081ce16e40a` (lane tip at round start).
Scratch clone: `git clone --shared` of the lane at `/fast/scratch/hyaku/tameshi-r50/T50Cross45/lane`; every verdict was read from `git show e3729de:path` in that clone (read-only, no git/jj mutation). No tools were installed (no pacman/uv/npx action needed). No T50Disp* file was read.

Item texts read from `corpus/lessons/round-45-verifier-spotcheck.md:85-88` (their line numbers match the frozen defect lines in `.ufo/evidence/round-50/c1/defects.json`).

## R45.1 — No-harm monitor false red → **open**

Ask: fix the round-44 record-agreement counter (exempt pinned external hashes like `cd8e73f0…`; be round-parametric) before it is named in another contract's `no_harm`.

Tree check:
- `.ufo/evidence/round-44/calibration/measure.py` last changed at `ba01973` (round-44 freeze) — pre-routing (`routed_at` 683eedde). `git log --follow e3729de -- .ufo/evidence/round-44/calibration/measure.py` shows no post-routing commit.
- The counter's m11 class still treats every 40-hex token as a lane object without exemption: `measure.py:87` (`HEX40 = re.compile(...)`) and `measure.py:348-358` (`m11_revisions` → `git cat-file -e token`).
- I ran the counter at base (read-only): `python3 lane/.ufo/evidence/round-44/calibration/measure.py --lane $S/lane --rev e3729de --freeze ba01973c…` → `C2_R44: self_pin=1 classes=7 m6=1 m7=0 m8=0 m10=0 m11=0 m12=1 m13=1 total=3 ... C2_R44_PASS=false first=m6:standing=None_actual=130` (exit 1). The false-red state persists; the class still misfires.
- Mitigation exists but is not the fix: QUALITY 88 / `.ufo/evidence/round-46/quality/no-harm-gate.py` refuse the r44 counter as a monitor (`c88-90-falsifiers.stdout`: `WHY r44-record-agreement exit 1; missing token 'C2_R44_PASS=true'`), and rounds 46–50 `no_harm` scripts/contracts never name it. That satisfies the "before it is named…" clause only; the counter itself was never amended.

Doubt resolved: exclusion ≠ fix; the requested counter behavior does not exist in the tree → open.

## R45.2 — Selftest receipts → **fixed** (commit `745a583181648cfc7f9c1b476cd1be7dc68f7433`)

Ask: commit `--selftest` stdout (tally) for both `measure.py` counters; kill the 12 (C1) and 8 (C2) selftest survivors routed in SCORECARD Planned (round 46).

Tree check:
- `.ufo/evidence/round-46/selftest/c1-selftest.stdout:19-20` → `C1_R46_SELFTEST: cases=18 failed=0` / `VERDICT: PASS`; `c2-selftest.stdout:9-10` → `C2_R46_SELFTEST: cases=8 failed=0` / `VERDICT: PASS`; exit files 0. Both files are added by round-46 freeze commit `745a583` (post-routing; `git diff-tree 745a583` lists them).
- Survivors killed: `.ufo/evidence/round-46/after/c2.stdout:36` → `targets=hardened declared=25 killed=25 survived=0 inapplicable=0 neutral_killed=0 pristine=1 equivalence=1 C2_R46_PASS=true` — the hardening harness over both round-45 counters (freshness 12 survivors + coverage 8 survivors among the 25 declared) kills everything. SCORECARD round-45 Planned(round 46) names this exact ask.
- Keyed evidence: path ends with `selftest.stdout` (key); lines carry no acknowledgement words.

Doubt resolved: receipts are for the round-46 successor labels, but they are the committed `--selftest` stdout tallies the item demands, and the kill receipt covers the routed survivors → fixed.

## R45.3 — Freshness score definitional jump → **fixed** (commit `745a583181648cfc7f9c1b476cd1be7dc68f7433`)

Ask: cite the 0 → 71 count as the comparable measure; keep the old unit as monitor.

Tree check:
- `.ufo/evidence/round-46/before/no-harm-at-base.stdout:3` (added by `745a583`) → `NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok` — the committed no-harm monitor runs the old unit (the count) at base, with `fresh=71` as the keyed excerpt. The same count-based expectation persists in rounds 46–49 `no-harm.sh` and the round-50 contract's monitor list.
- `corpus/lessons/round-46.md:129` records the adopted rule: the count is the comparable measure and the definitional score is "cited only beside that count".
- Keyed evidence (`fresh=71`) is absent at `routed_at` (file created round 46); lines carry no acknowledgement words.

Doubt resolved: the counter line format predates routing (the "(already done)" note), but the post-routing committed monitor receipt is the old-unit monitor actually run on the count — the thing exists in the tree → fixed.

## R45.4 — Anchor refresh → **open**

Ask: work the five anchor-refresh candidates of `.ufo/waves/round-45/w2/ConnDriftAnchors.md` (S100, S153, S154, S157, S159; S089 already done via S160); pin S026/S093/S108 by quote, not whole-page hash.

Tree check:
- The five candidates remain unpinned: `corpus/SOURCES.md:108` (S100 pins the round-33 committed snapshot "2026-10-23"), `:123` (S153 pins `ast.html` 183a4f8c), `:124` (S154 pins `pathlib.html` 0044cae6), `:127` (S157 pins `python-argparse.html` 3158c439), `:129` (S159 pins `wikipedia-mutation-testing.html` 6e4a06c0). `git show e3729de:corpus/SOURCES.md | grep -E 'supersedes S(100|153|154|157|159)\b'` → no hits (no supersede row exists).
- Partial completion: S026/S093/S108 were re-anchored by `50545328e7ac4ba1703d70030e37dacec9362e68` (round 48): rows S265/S267/S268 (`SOURCES.md:140/142/143`) with quote-located anchors (raw line spans), per-snapshot fetch receipts under `.ufo/evidence/round-48/freshness/sources/`, and re-pointed entries (`corpus/knowledge/repeated-control-precondition.md:1`, `regression-tally-completeness.md:1`, `r8-golden-update-flag.md:1`). The round-48 spot-check confirms "four held rows re-anchored, with snapshots, receipts and quotes located live".

Doubt resolved: compound item — the "pin by quote" clause landed, but the five named candidates are still open in the tree; not every ask exists → open.

## Method notes
- All verdicts are judgments of the tree at base; no counter was run in deciding mode (only the read-only r44 probe above, which is an observation, not a verdict).
- Evidence excerpts are verbatim from the cited lines at e3729de; line spans ≤ 30; no spot-check / ledger / HARD paths used.

## Summary
- R45.1 open: r44 record-agreement counter byte-unchanged since freeze, still false-red at base (run shows `m6=1 m12=1 m13=1`, `C2_R44_PASS=false`); only exclusion via QUALITY 88/no-harm-gate.py exists.
- R45.2 fixed @ 745a583: committed `--selftest` tallies (`c1/c2-selftest.stdout`, cases=18/8, failed=0) + kill receipt `killed=25 survived=0`.
- R45.3 fixed @ 745a583: old-unit monitor run on the count (`no-harm-at-base.stdout:3`, key `fresh=71`); lesson records count-as-comparable rule.
- R45.4 open: S265/S267/S268 re-anchor S026/S093/S108 by quote, but the five ConnDrift candidates (S100/S153/S154/S157/S159) have no supersede rows at base.
- No tools installed; no lane mutations; deliverables only.
