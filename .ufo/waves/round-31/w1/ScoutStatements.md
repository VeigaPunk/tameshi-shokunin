# ScoutStatements — standing self-assessment outside the frozen 12

Verdict: at `c111dab58b0a8d55e991bbd2efe3aad56717b95a`, C1's 12 statements are the only numeric cells in the one `| Capability |` table and the one `| Axis | Score (0–10) |` table. They do not cover the standing sentences below. Four of those are stale against a command or a cited file at this revision: the Saturation nudge sentence, the `SHONEN.md:5-34` cite, the `tools/mutate-and-run.sh:84-89` cite read at this revision, and the env-diff class name `raw-output-variable`. The rest of the standing set still matches the check named here, or is a policy declaration with no later standing amendment. This seat changes nothing.

No tool was installed.

Clone: `/fast/scratch/hyaku/tameshi-r31-seats/ScoutStatements/repo`, detached at `c111dab`. `git show --stat -1` adds only `.ufo/evidence/round-31/` files (parent `36c1d393`). `SCORECARD.md` and `SHONEN.md` in that tree are the texts below. Line numbers are that tree.

## What was treated as standing

Standing means a sentence that is still the lane's current checklist or register, not a dated round section and not a row whose heading is a round. That is `SHONEN.md` (whole file), and in `SCORECARD.md`: the opening lines, `## Current axes` (other than the two score cells), `## Capabilities` (other than the numbers the frozen regex captures), `## Saturation`, and `## Retired`.

Excluded on purpose, after reading them:

- `## Move log`, the ten-round verdict table, `## Fleet round-1 interactive continuation`, `## Fleet round 1 — kaika continuation (2026-10-19)`, and every `## Round N` section. They carry many checkable numbers. They are round-scoped or dated, so they are outside this list even though C1 does not read them either.
- Three `| capabilities addition |` rows (SCORECARD.md:1057, :1150, :1234). The counter keeps a row only when the first header cell is exactly `Capability` (`.ufo/evidence/round-31/c1-measure.py:114`). These headers are not that, and they sit inside round sections.
- `## Planned` is a standing heading, but its three items are labeled `Round 2 (declared fleet round 1, kaika)` (SCORECARD.md:268-279). Round-scoped. The named count `grep -c 'stale' corpus/knowledge/fleet-kill-rate-ledger.md` printed `16`, not the plan's "2 stale". Not listed as a standing current claim.

The frozen 12, not repeated as findings: the ten capability-row patterns in `c1-measure.py:38-61`, plus the depth and calibration score cells (SCORECARD.md:66-67). The committed base receipt `.ufo/evidence/round-31/before/c1-at-base.stdout` already records 7 mismatches on those 12 at the parent. This sweep does not re-run that counter.

## Standing statements C1 does not cover

| Line | Statement | What would check it | At this revision |
|---|---|---|---|
| SHONEN.md:5 | Box 1 `[~]`: SKILL.md has real decision tables, error patterns, checklists, cited sources | Mark census (command C, below) plus structural presence in `SKILL.md` | Mark current. `grep -cE '^\| ' SKILL.md` → 217; `grep -c 'corpus/knowledge/' SKILL.md` → 38; `grep -c -i checklist SKILL.md` → 16. A decision table is at SKILL.md:58 and a fail-closed arm table at :501. "Real" was not re-judged. |
| SHONEN.md:7 | Box 2 `[~]`: at least one end-to-end domain task is logged in LOG.md | `grep -n -i 'end-to-end' LOG.md` | Mark current. A logged run is at LOG.md:229 (`reproduced one killed mutant end-to-end`). Not an independent promotion review. |
| SHONEN.md:9 | Box 3 `[~]`: instructions executable without oral context; cite `.ufo/evidence/round-21/coldread/ledger.json` | The cite resolves; the cold-read monitor is the substantive check | Cite current: the file loads, `entries` length 456. The `[~]` mark is still `[~]` (command C). This seat did not re-run the monitor. |
| SHONEN.md:11 | Box 4 `[~]`: no cross-domain bleed; PROVINCE.md still accurate | File exists; latest append vs command D's case count. Bleed itself needs a review this seat did not do | `wc -l PROVINCE.md` → 118. Latest append (PROVINCE.md:109-118) says nine recorded legs. Command D printed `recorded_cases=9`. The round-1 sentence "six" (PROVINCE.md:29) is kept and superseded in later appends. Cross-domain bleed: not re-judged. |
| SCORECARD.md:5 | "Axes will be pinned with their counting commands as rounds land." | Whether commands D and C are already in the score section | Stale as a forecast. Commands D and C are already written at SCORECARD.md:72-75. |
| SCORECARD.md:66 | Counting-rule cite `` `tools/mutate-and-run.sh:84-89` `` for the pinned replay ledger (not the score cell `6`) | `sed` that range at this rev, and the same range at the row's named commit `284ab0f` | Stale at this rev. Lines 84-86 are the ledger intro; 87-89 are 3 of 9 case lines; the nine cases run 87-95. At `284ab0f` the same range is all six case lines (file then ended the list at line 89). The cite was exact for the commit the row names, and it is not the ledger span now. |
| SCORECARD.md:66 | "capped at 10" | Command D uses `min(10, n)` | Current as a rule. Command D printed `recorded_cases=9 depth_score=9`. |
| SCORECARD.md:67 | Cite `` `SHONEN.md:5-34` `` (not the score cell `0`) | `wc -l SHONEN.md`, and the same file at `284ab0f` | Stale now. `wc -l` → 12, so lines 5-34 do not exist. At `284ab0f` the file had 36 lines, so the range existed then. |
| SCORECARD.md:67 | "Baseline has four `[x]` marks" | Command C at `284ab0f`, versus command C now | Accurate for the baseline it names, and not a live mark claim. At `284ab0f`: `checked=4 asserted=0`. Now: `checked=0 asserted=4`. |
| SCORECARD.md:67 | Lane cap 8, last 2 points need independent review of all boxes | Command C's upper bound and the absence of `[x]` | Current as a rubric. Command C printed `asserted_mark_upper_bound=8` and `checked=0`. |
| SCORECARD.md:240 | `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | Current. The script printed that CLEAN line and `EXIT:0`. The same run printed `== A rows` / `92`. The `44` in this row is one of the frozen 12, not this finding. |
| SCORECARD.md:242 | "historical round 7 (four legs) / round 10 (six)" | Move log and the runner comment, not the live case count | Current as history. Move log SCORECARD.md:20 says the round-7 ledger replays 4 recorded cases. `tools/mutate-and-run.sh:83` says `r10-2 six legs`. The live count is command D's 9; the row's `cases=6` is one of the frozen 12. |
| SCORECARD.md:243 | What-column `N≥3` | `python3 tools/repeat-control.py --runs 2 --out <scratch> -- true` | Current. Printed `repeat-control: --runs must be >= 3, got 2`, `REPEAT_CONTROL: invalid_usage`, exit 64. The `29` cases figure is one of the frozen 12. |
| SCORECARD.md:244 | `changed3/unchanged3/unavailable0` | Cited `.ufo/evidence/round-13/pin-dispositions.json` `counts` | Current as a citation. `counts` is `legs 6, unchanged 3, changed 3, unavailable 0`. Not re-run as a live probe. The `18/18` selftest figure is one of the frozen 12. |
| SCORECARD.md:245 | `40/41` then `41/41` on the producer oracle | Substring count in cited `.ufo/evidence/round-13/producer-oracle-repair.json` | Current as a citation: `40/41` once, `41/41` once, `WITNESS_SELFTEST` twice. The compressed tokens `FAIL1` and `PASS0` do not occur in that file (count 0). The `39/39` selftest figure is one of the frozen 12. |
| SCORECARD.md:246 | before `FAIL1` / `contains_missing`, after `CLEAN` with findings 0, eleven effective and one superseded; short hash `6431478` | Cited `.ufo/evidence/round-14/verification-final.json` stdout JSON, and `git rev-parse` | Current as a citation. Before: exit 1, status `failed`, counts `failed 1`, finding id `expected_contains_missing`. After: exit 0, status `clean`, counts `effective 11, superseded 1, failed 0, findings 0`. `git rev-parse --verify 6431478^{commit}` → `64314783836bb0d05ad06a774d7310fd3a23b5bd`, equal to that file's `measured_commit`. The `34/34` selftest figure is one of the frozen 12. |
| SCORECARD.md:247 | `registered frozen0`, `missing-env1`, `tamper2`, `usage64` | Cited `.ufo/evidence/round-15/verification-3.json` check exits | Current as a citation, not re-executed here. `gate-frozen-builtin` observed exit 0; `gate-missing-env` exit 1 id `missing_injected_environment`; `gate-tampered-snapshot` exit 2 id `snapshot_tampered`; `gate-usage` exit 64. `passed` is true and `failed_checks` is empty. `selftest-new-full-count` detail is `SELFTEST: PASS (49/49)`, which is the frozen statement, not this one. |
| SCORECARD.md:248 | seven profiles; classifies 9/9; eight invariant and one `raw-output-variable` | Cited `.ufo/evidence/round-21/f5/receipt-initial.json` | Mixed. Profile keys are 7: `clean`, `clean_repeat`, `columns`, `home`, `host`, `locale`, `tz`. Surfaces: 9, of which 8 are `invariant` and 1 is `nondeterministic` (`js-round-gate`). The string `raw-output-variable` occurs 0 times in `receipt-initial.json`, `receipt.json`, and `receipt-final-production.json`. The class name is stale. The `actual9/9` selftest figure is one of the frozen 12. |
| SCORECARD.md:249 | 146-seat replay, 66 completed, 80 failed, `wrong-count1` / `TOTAL_MISMATCH` | Cited `.ufo/evidence/round-22/final/verification.json` | Numbers current as a citation. `frozen-entry` total is `seats 146, completed 66, dead 80`. `wrong-count-entry` exit 1, finding id `TOTAL_MISMATCH`. The row's word "failed" is the receipt field `dead` (same number, different word). The `8/8` counter figure is one of the frozen 12. |
| SCORECARD.md:243-249 | Seven "admission pending" / "separate non-author admission pending" statuses | A later standing withdrawal, or an `[x]` on SHONEN | Current as unwithdrawn text. No standing section after the capability table withdraws them. Command C still prints `checked=0`. Not a fresh admission review. |
| SCORECARD.md:257-260 | Declared saturation line 8/10 on each owned axis; stagnation window N = 2 | The standing section itself, and whether a later standing section amends it | Current as policy text. Round sections still talk about that line and window; none of them is a standing amendment. These are not observations of the live depth or calibration cells. |
| SCORECARD.md:261-262 | "the nudge does not fire now (depth 6 < 8; calibration pinned 0, candidate 8 pending)" | Command D for the depth half. The calibration half is the monitor, which this seat did not re-run | Stale. Command D printed `recorded_cases=9 depth_score=9`, so "depth 6 < 8" does not hold, and the whole "does not fire now" sentence fails on that half alone. The parent receipt `.ufo/evidence/round-31/before/c1-at-base.stdout:12` records the monitor's calibration cell observation as 8 at `36c1d39`; this commit does not change `SCORECARD.md`, `SHONEN.md`, or `SKILL.md`. That parent line was not produced by this seat. |
| SCORECARD.md:283 | Retired: none | `grep -n -i retir SCORECARD.md` | Current. Every hit is a denial ("none", "no retirement"), including this standing bullet and later round sections. |

Commands, from the clone above, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset:

```text
REV=$(git rev-parse HEAD)   # c111dab58b0a8d55e991bbd2efe3aad56717b95a
git show "$REV:tools/mutate-and-run.sh" | python3 -c '...'   # command D
# recorded_cases=9 depth_score=9
git show "$REV:SHONEN.md" | python3 -c '...'                 # command C
# boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8
git show 284ab0f0b8b989ee73d9c00c0c0df0a59757af8d:SHONEN.md | python3 -c '...'
# lines=36 boxes=4 checked=4 asserted=0 untouched=0
wc -l SHONEN.md                                              # 12
bash .ufo/evidence/kaika-round-1/sources-census-v2.sh
# == A rows / 92 ; SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path) ; EXIT:0
grep -c 'stale' corpus/knowledge/fleet-kill-rate-ledger.md   # 16
python3 tools/repeat-control.py --runs 2 --out <scratch>/rc-out -- true
# --runs must be >= 3, got 2 ; REPEAT_CONTROL: invalid_usage ; EXIT:64
git rev-parse --verify '6431478^{commit}'
# 64314783836bb0d05ad06a774d7310fd3a23b5bd
```

The receipt reads were `json.load` of the paths in the table, in that same clone.

## Smallest safe correction

None in the tree. The frozen counter, the 12 statements, and the predicate stay as frozen. A later pass of those 12 would not make the four stale standing sentences true: the Saturation nudge sentence (SCORECARD.md:261-262), the `SHONEN.md:5-34` cite (SCORECARD.md:67), the ledger cite `tools/mutate-and-run.sh:84-89` read at this revision (SCORECARD.md:66), and `raw-output-variable` on the env-diff row (SCORECARD.md:248). Appending a correction, if anyone does that later, is how this file has been keeping old sentences.

## Not checked

- Live re-run of pin-disposition, verify.py, the witness producer, the round-14 disposition gate, env-diff, or wave-accounting. Side numbers above are citation checks of the files the rows name.
- The cold-read monitor at `c111dab`. Box 3's substantive credit and the calibration half of the nudge sentence are not freshly measured here.
- Whether PROVINCE.md is free of cross-domain bleed, beyond the nine-leg append matching command D.
- Whether "admission pending" was closed in a lesson or a fleet report outside this lane's standing sections.
