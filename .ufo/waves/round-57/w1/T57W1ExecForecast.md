# T57W1ExecForecast — cold-read cost forecast (considerthese 2026-10-28 proposal 3)

Staged: `.ufo/waves/round-57/w1/T57W1ExecForecast/stage/tools/cold-read-forecast.py` (stdlib only, sha256 `29d43bba390a88c7be58a48b6a09e71c2aec59d68943e056f950f04c1db8bc76`, 0755). Nothing in the lane was edited. Receipts: `T57W1ExecForecast-receipts/`. Machine-readable: `T57W1ExecForecast.json`.

## Answer for this round's planned edit set (base 5e35699)

`FORECAST: paths=10 headings=18 readers=18 of 64` (exit 0). Command (receipt `plan.stdout`, `plan.json`):

```
python3 tools/cold-read-forecast.py --lane LANE --rev 5e3569969b53… --paths corpus/SOURCES.md corpus/QUALITY.md corpus/README.md corpus/routed-defects.json tools/registry.json SKILL.md corpus/knowledge/receipt-revision-binding.md corpus/knowledge/cold-read-cost-forecast.md SCORECARD.md LOG.md --skill-section '## Standing rules' --skill-section '### Gate/probe registry'
```

Expected re-readers: **18** (one fresh reader per lost heading). Headings (SKILL.md line starts at base):

| L | heading | cost cause |
|---|---|---|
| 17 | `## Standing rules` | section-sha-void (planned edit) |
| 159 | `## Mutation-sweep recipe…` | QUALITY, README, SOURCES, registry.json |
| 949 | `## The leg ledger…` | README, SOURCES |
| 1100 | `### Triggers T1–T3 and the re-pin rule` | QUALITY, README, SOURCES, registry.json |
| 1282 | `### The service's limits…` | registry.json |
| 1312 | `## The operator's runbook and the six-leg regression…` | registry.json |
| 1421 | `### The map — where a reader enters…` | README |
| 1521 | `## Repeated controls and gate registry — round 12` | SOURCES |
| 1541 | `### Gate/probe registry` | section-sha-void (planned edit) |
| 1559 | `## Pin disposition and provenance correction — round 13` | SOURCES |
| 1590 | `### Round-13 gate/probe registry` | SOURCES |
| 1606 | `## Effective expectation reconciliation — round 14` | SOURCES |
| 1652 | `## Context gate classification…— round 15` | SOURCES, registry.json |
| 1857 | `## Live-tree re-pin and entry-command monitor — round 17` | QUALITY, README, SOURCES, registry.json |
| 1889 | `### Round-17 gate/probe registry — re-pin and monitor` | SOURCES, registry.json |
| 1968 | `### Round-18 gate/probe registry — routed-defect closure` | QUALITY, SOURCES, registry.json |
| 2007 | `### Round-21 gate/probe registry — finite environment differential` | QUALITY, SOURCES, registry.json |
| 2175 | `### Round-26 gate/probe registry — report interop` | registry.json |

Per-path marginal cost alone (receipt `marginal.tsv`): SOURCES 13, registry.json 11, QUALITY 6, README 6, SKILL `## Standing rules` 1, SKILL `### Gate/probe registry` 1, routed-defects.json 0, receipt-revision-binding.md 0 (UNPINNED), SCORECARD 0, LOG 0 (pinned, but every pinning heading has a second clean reader). The union is 18, not the sum 38: the overlap is almost total, so dropping any one of QUALITY/README/registry.json while keeping SOURCES saves at most a handful (SOURCES+QUALITY+README+registry only = 17; the two SKILL section edits add one: `## Standing rules` is already lost to QUALITY/README/SOURCES drift, only `### Gate/probe registry` is new). The new knowledge entry and `routed-defects.json` cost 0 (no entry pins them). SKILL.md edits shift every later `:NNN` anchor if the line count changes: not priced (the monitor keys on section bytes).

## Calibration (forecast vs monitor, same revs, real runs of the round-21 monitor)

| measured fact | forecast | monitor | headings identical |
|---|---|---|---|
| base 5e35699 + one appended line each to QUALITY/SOURCES/README + one new knowledge file (clone commit 4182777, monitor `--explain` run here: 64 → 50) | 14 | 14 lost (50/64) | yes, all 14 starts+headings |
| round-55 edits `0a2010a → 21eb3c6` (monitor at 21eb3c6: 46/64) | 18 | 18 uncovered | yes, 18/18 heading texts (symmetric difference empty) |
| round-56 C0 edits `21eb3c6 → c013745` (monitor at c013745: 46/64) | base 46 − 0 new = 46 | 46 | n/a |

Correction for the L1 (stated in the assignment): the **18-heading cost belongs to round 55's edits**, not to the round-56 C0 edits. At `21eb3c6`, before C0, the monitor already reads 46/64 (18 uncovered); the C0 edits (registry.json, SKILL `## Standing rules`, QUALITY, SOURCES) touch only headings that were already uncovered, so C0 itself cost 0 further sections (monitor at c013745 = 46, forecast 46). Receipts: `monitor-summaries.json`, `calibration.json`, `r55-edits.stdout`, `r56-c0.stdout`, `appends.stdout`.

Reason strings differ from the monitor's: the monitor lists every entry's first failure per section (entries already stale at base add noise); the forecast lists only the failures of entries that credited at base, i.e. the causes of the *new* loss. Counts and heading sets are what is validated.

Runtime: 1.6 s per forecast (one `ls-tree`, one `cat-file --batch`); the monitor takes ~4 min and ~29 CPU-min per run.

## Behavior

- Reads only git blobs at REV (SKILL.md, the round-21 ledger, pins, traces); re-implements the frozen round-18 credit rule (class/verdict gate, commands, inputs sha, trace validation incl. live-lane reads, veto aggregation) and evaluates each heading twice: base and "planned paths changed". Lost = covered at base, not after. Already-uncovered headings are reported separately, never counted.
- SKILL.md is DROPPED from input drift (as the monitor ignores it); only `--skill-section "<exact heading>"` / `--skill-lines A-B` price it, voiding that section's own sha (`section-sha-void`).
- `--diff-to REV2` prices the retrospective set (changed paths + changed SKILL sections) for calibration.
- Path classes: PRICED / STALE-ONLY / UNPINNED / NEW / UNPRICED. **Exit 2 (loud, forecast still printed)** when a planned path is read directly by the monitor yet pinned by no entry: SKILL.md without a section, the round-21 ledger, the round-18/21 monitor scripts (`FORECAST_UNPRICED`); also unknown/ambiguous SKILL section, unresolvable REV, unusable `TMPDIR`. `--strict` also exits 2 on UNPINNED/STALE-ONLY paths. Exit 64: option-like REV, non-canonical path.
- `--json` output; `--selftest` 16 cases in a `mkdtemp` fixture repo under `TMPDIR` (set-but-unusable `TMPDIR` is exit 2, never a `/tmp` fallback). `| head` no longer raises BrokenPipe.

**Interpretation to confirm** (assignment sentence "absent from every ledger entry but in the monitor's input universe"): I defined the monitor's input universe as the paths it reads directly (SKILL.md, the ledger, `tools/mutate-and-run.sh`, `SHONEN.md`, `corpus/SOURCES.md`, the round-18/21 measure scripts). Under that definition the planned set exits 0 (SOURCES/SHONEN/mutate-and-run are pinned by entries, so priced). If the L1 meant "every tracked path no entry pins", `--strict` gives that: the planned set then exits 2 for `corpus/routed-defects.json` and `corpus/knowledge/receipt-revision-binding.md` (both UNPINNED, cost 0).

## Controls and mutants

`--selftest`: `FORECAST_SELFTEST: 16/16 pass` (`selftest.stdout`). Seven single-edit mutants of the tool (`mutants.txt`): ignore-changed-set, veto-never, UNPRICED exit 0, SKILL void dropped, any-reader-loses, TMPDIR silent fallback, no base-uncovered skip → **7/7 killed** (the veto mutant survived the first fixture; a vetoed-clean-reader entry was added to the fixture and it then died 13/16).

## Limits (cannot see)

- Whether a re-keyed ledger (wave 3) changes the pins: forecast is for the ledger at REV. After the L1 re-keys, rerun at the re-key rev.
- Readers who fail their re-read (the lessons of rounds 48/52/53) are not forecast; only the credit loss.
- Line-anchor shifts in SKILL.md, SKILL edits that change sha but whose edited heading was never matched (already uncovered: cost 0, reported as already-uncovered).
- A vetoing entry that becomes stale after the edit (a possible *gain*) is simulated in the covered state but only losses are reported.
- Trace parsing uses the monitor's `LIVE_LANE_ROOT` constant verbatim; in a different lane path, live-lane reads under the old root are evaluated as the monitor evaluates them.

## Tooling / environment

No installs. Scratch under `/fast/scratch/hyaku/tameshi-r57/T57W1ExecForecast` (removed). Two shared clones (read-only monitor runs, one fixture commit with `-C` and fixture identity after asserting `rev-parse --show-toplevel`); no mutating git in the lane. Monitor runs: 4 (base, mutated clone, 21eb3c6, c013745), ~4 min each, `nice -n 10`.

## For wave 3 / L1

Validation command: rerun `cold-read-forecast.py --lane LANE --rev <rev before C0> --paths <files C0 actually changed> --skill-section …` (or `--diff-to C0`) and compare `headings` with the monitor's uncovered count at C0; the three calibration rows above were exact (14=14, 18=18, 46=46).
