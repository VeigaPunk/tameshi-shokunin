# T48ScribeMistakes — `## Mistakes` draft for `corpus/lessons/round-48.md`

Seat: T48ScribeMistakes, leaf member, no dispatch. Item: draft the round-48 lesson `## Mistakes` section,
mining at least three mistakes from round 47 and earlier, first row the round-47 C1 miss.

## Behavior

Wrote one deliverable, 11,239 bytes, 56 lines, sha256
`38fd3b57eff21a5508aa8dedbbfafe2d49d7fb1e2ffec6507d1f5cc91e457b52`:

- `.ufo/waves/round-48/w1/T48ScribeMistakes.draft.md` — the section verbatim (`## Mistakes`, a seven-row
  table with the four corpus columns, seven tagged red-state command blocks, a sweep paragraph and a
  provenance/limits paragraph), ready to be inserted into the lesson.

Nothing else in the lane was touched: no contract, SCORECARD, lesson, counter, gate or jj/Git state. No git or
jj command that writes was run; no fixture repo; no clone; no tool installed or upgraded (none needed, and the
pacman guard was irrelevant because nothing was installed). No scratch directory was created — every reading
below is a read-only command against the lane tree, so there is nothing to delete under
`/fast/scratch/hyaku/tameshi-r48/T48ScribeMistakes/` and that path does not exist (`ls` → `No such file or
directory`).

## The seven rows, as landed in the draft

| # | class | evidence | captured-by |
|---|---|---|---|
| 1 | `stale-premise` (the round-47 C1 miss) | `.ufo/evidence/round-47/after/c1.stdout:5` claimed `FAIL (cases=9 passed=7` vs observed `PASS (cases=9 passed=9`; `SCORECARD.md:2318`, `663e0682`; instability disclosed at `SCORECARD.md:2314` | `none` — QUALITY 92 (`QUALITY.md:1365-1369`) requires value/exit/sha256/deps but no repeat count; round-47 C1 statement asked for one P0 observation |
| 2 | `scope` (wave 2 built, never dispatched; below the floor) | `.ufo/waves/round-47/spec-w2.json` 32 items, `.ufo/waves/round-47/w2/` = `swarm-registry.json` only; report `:52` | `none` — QUALITY 78 settles a dispatched wave and states "Prepared specs are not dispatched seats" |
| 3 | `landing` (selftest tallies cited, no receipt) | `.ufo/evidence/round-47/selftest/` 0 files vs report `:12` (35/35, 14/14, 24/24) and `SCORECARD.md:2308-2310` (`cases=7 failed=0`); round-46 committed 6 files | `none` — criterion 88 mandates a receipt for the no-harm script only; 92/93 name a `--selftest` without requiring its output |
| 4 | `landing` (criterion 93's falsifier has no receipt; receipt contradicts the report's chronology) | `quality/c91-92-falsifiers.stdout` 7 lines, ends `CRITERION-92-FALSIFIER-OK`; block 93 at `quality/falsifiers.sh:26-36` | `none` — criterion 93 names the block and requires no output; round-46 precedent `QUALITY.md:1312-1315` |
| 5 | `reference-drift` (lesson restates a superseded unstable observation) | `corpus/lessons/round-47.md:118` {env, node} vs `after/c1.stdout:17` `observed_deps=bwrap,node`; `SCORECARD.md:2314` | `none` — criterion 91 binds quotes only; criterion 92 binds SCORECARD rows, not a lesson restatement |
| 6 | `provider` (scratch on shared `/tmp` filled it; no counter could see it) | report `:17`; `w1/T47ExecObsD.md:30,199` (`clone/checkout failed` at P2 on ENOSPC) | `none` — QUALITY 9 (`QUALITY.md:24`) puts scratch in `/tmp`; QUALITY 92 (`:1367`) states free disk in `/tmp` stays unobserved; QUALITY 67 binds `--regression` workdirs only |
| 7 | `landing` (report's lane HEAD is one commit behind; that commit rewrites a landed seat report) | report `:5` HEAD `663e0682` vs `03facb22`; `git rev-list --count 663e0682..03facb22` → 1; diff touches `w1/T47ConnCross.md` only (+228/−214) | `none` — QUALITY 86 binds a deciding receipt to its measured revision, not a report's HEAD line; QUALITY 77 binds a report to the lane repo, not to the revision |

The five round-47 conformance defects map onto rows 2, 3, 4, 5 and 7 (defect 2 = row 7); the scratch incident
is row 6, with misroot explicitly ruled out (no seat file at the fleet root, QUALITY 77 clean).

## Readings (seat-level, none is a verdict)

All against `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at `f1cfaad3` (round-48 base `473336d9`):

```
git show edd4ca44:.ufo/evidence/round-47/after/c1.stdout | sed -n '5,6p'
# claimed=REGRESSION: FAIL (cases=9 passed=7|1|a7d3f2dd7d47 observed=REGRESSION: PASS (cases=9 passed=9|0|…
# P0=REGRESSION: PASS (cases=9 passed=9|0 … P4=SETUP passed=4|2 P5=SETUP passed=0|2
jq '.items|length' .ufo/waves/round-47/spec-w2.json → 32 ; ls .ufo/waves/round-47/w2/*.md | wc -l → 0
find .ufo/evidence/round-47/selftest -type f | wc -l → 0 ; round-46 → 6
grep -c '^CRITERION-' .ufo/evidence/round-47/quality/c91-92-falsifiers.stdout → 2 (91, 92; block 93 unrun)
diff <(lesson hermetic set) <(receipt observed_deps) → 1c1 / < env,node / --- / > bwrap,node ; exit 1
git rev-list --count 663e0682..03facb22 → 1 ; git diff --name-only 663e0682 03facb22 → w1/T47ConnCross.md
find /fast/scratch/hyaku/tameshi-r48 -mindepth 1 -maxdepth 1 -type d | wc -l → 18 ; du -sh → 13G
```

Qualitative checks: `git show --name-only 663e0682` → `SCORECARD.md` (the errata commit); the round-47
`## Mistakes` table has five data rows (`grep -n '^| '` → `:105-109`), so the three rounds-46 rows (quote fold,
embedded oracle, self-referential pins) are not restated as duplicates. Table integrity of the draft: 8 lines
match `^| ` = one header + seven data rows, each four columns.

## Findings for the L1

1. **Row 1's fix is pre-registered, not built, at this reading.** `.ufo/evidence/round-48/calibration/` and
   `.ufo/evidence/round-48/control/` were both empty (`ls` printed nothing) and
   `.ufo/evidence/round-48/selftest/` was empty. Peer deliverables `w1/T48ExecC1Counter.measure.py` (945 lines,
   carries the `runs 3 (stable|nondeterministic)` grammar and a `--selftest`) and
   `w1/T48ExecC1Controls.run-controls.py` exist in the wave directory but are not the frozen paths, so the draft
   claims no CTL_B result and names CTL_B only as the pre-registered control (`contract.json:33`). The counter's
   freeze-step-2 commit and the CTL_B receipt are what make row 1's fix scored rather than declared.
2. **Three defects in the round-47 spot-check are confirmed by direct reading**, not by citation: the empty
   `selftest/` tree against three cited tallies, the missing criterion-93 falsifier output, and the lesson's
   `hermetic env-differential probe` set disagreeing with its own deciding receipt (the only drift of the five
   dependent statements — `six-leg`, `effective expectation reconciliation`, `retained invocation-context gate`
   and `mutation report interop` all match).
3. **The round-47 lesson's own row 1 fix (`lesson-quote-check.py`) did not generalise to numbers**: it checks a
   located quote against a snapshot, and row 5's drift is a restated dependence set, which no checker reads.
   That is the gap the draft's row 5 names.
4. **Scratch footprint at this reading**: 18 seat directories, 13 GB under `/fast/scratch/hyaku/tameshi-r48`
   (live peers, left untouched), `/tmp` at 3 % and `/fast` at 28 %. Those are the quantities row 6's detector
   reads; they are not a claim about this seat, which created no scratch.
5. **No misroot of mine.** `.ufo/waves/round-48/w1/T48ScribeMistakes.draft.md` is the only file this seat wrote
   before this report; the fleet root's `git status --porcelain` shows pre-existing staged `.scratch/` and
   `.tower/` entries that no seat of this round wrote and that I did not touch.

## Out of scope (deliberately untouched)

The contract and `amendments`; `SCORECARD.md`; `corpus/lessons/round-48.md` (it does not exist yet — the draft is
the section, not the lesson); both round-48 counters and their selftests; every control; all gate lines (no
`C2-QUOTE` line is in the draft); the round-47 tree, `corpus/lessons/round-47.md`, and the round-47 receipts; jj
and Git state; `/home/vgpnk/Projects/shokuknow`. No claim is scored and no verdict is offered.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-48/w1/T48ScribeMistakes.draft.md` (deliverable,
  sha256 `38fd3b57eff21a5508aa8dedbbfafe2d49d7fb1e2ffec6507d1f5cc91e457b52`)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-48/w1/T48ScribeMistakes.md` (this report)
- Tools installed/updated: none (channel: n/a; reason: no install was needed).
