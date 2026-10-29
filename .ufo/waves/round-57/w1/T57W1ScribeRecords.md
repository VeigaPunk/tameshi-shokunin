# T57W1ScribeRecords — round 57 wave 1 skeletons (SCORECARD, LOG, lesson)

Seat `T57W1ScribeRecords`, L1 `TameshiR57`, lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `5e3569969b532310d2b8a3d130901757a3df356b` (lane HEAD at my start). Judged on calibration. All three drafts are SKELETONS: every unmeasured value is `<TBD:name>`. Nothing in them is a measured result, and no lane file was edited.

## Staged deliverables (not installed; the L1 copies them)

| Staged path | Kind | sha256 | Notes |
|---|---|---|---|
| `.ufo/waves/round-57/w1/T57W1ScribeRecords/stage/SCORECARD.md` | base bytes + appended `## Round 57` block (39 added lines, 0 removed) | `ef98839979458f26f253248567c36ec6b70c3c4c67dedb5e0cef9092ae6ce403` | base prefix byte-identical (`cmp -n`). Newest `**Planned (round` paragraph is the round-58 one (one contiguous line, names `R56.1`, `R56.4` and the seven carried R4x ids). |
| `.ufo/waves/round-57/w1/T57W1ScribeRecords/stage/LOG.md` | base bytes + appended round-57 entry (10 added lines, 0 removed) | `fb1e2e9f47c1f7d4d86e9fe79af5b8f7562ee3168ab9b5c998e59c6e0721c474` | base prefix byte-identical. Append-only. |
| `.ufo/waves/round-57/w1/T57W1ScribeRecords/stage/corpus/lessons/round-57.md` | new file, 45 lines: `## Gate`, `## Mistakes`, `## Round-56 dispositions` | `bec1149963760689615a41b6f1b594f7dcb5fd2661ce4f32994c0d0efd86c9d3` | new file; no existing lesson or SOURCES row touched. |

Full-file staging of SCORECARD.md and LOG.md is what the spec asked for; if another wave-1 seat also appends to either file, the L1 must merge the appended tail (the base prefix is the same in both), not overwrite.

## What each skeleton contains

1. **SCORECARD `## Round 57`**: standing axis table with calibration 8 unchanged (last-change round 56; measured-commit field `<TBD:REV>`); claims table for C1 and C2 with axis, before, target, counting command and frozen controls, taken from `.ufo/evidence/round-57/contract.json`; a results skeleton; no-harm and frontier lines; `**Planned (round 58):**` paragraph naming ledger rows left open by id (the C1 `open` rule reads this paragraph; the staged counter's `PLANNED_ID` regex is `\bR5[0-6]\.\d+\b`, so only the R5x ids are checked).
2. **LOG `round-57` entry**: skeleton, appended.
3. **`corpus/lessons/round-57.md`**:
   - `## Gate`: S283 row with `<TBD>` URL, quote and verdict; one rejected-candidate row in the reject-before-append form with a flip condition; the GNU grep "Exit Status" candidate is named as scout material only, not admitted; spot-check slot named; considerthese proposal 3 mining slot.
   - `## Mistakes`: one row for the round-56 Attempt-4 first Mistakes row (control design: a positive control read the round's own committed receipts), with this round's `controls.sh` as the captured-by and fix (recomputed, never read; generation guard), plus a `<TBD>` mined-mistake row.
   - `## Round-56 dispositions`: R56.1–R56.7 each with what the round does, its ledger status (contract-stated where pinned, `<TBD>` otherwise) and the evidence slot, citing `routed_defects_from_round_56`.

## Facts I measured (receipts under `.ufo/waves/round-57/w1/T57W1ScribeRecords-receipts/`)

| Fact | Command | Result (file) |
|---|---|---|
| Lane HEAD at start is the base | `git -C <lane> rev-parse --short HEAD` | `5e35699`; lane `git status` shows only the untracked `.ufo/evidence/round-57/` and `.ufo/waves/round-57/` (pre-existing) |
| Round-21 monitor at base reads 64/64, score 8, box 3 full page | `python3 .ufo/evidence/round-21/coldread/measure.py --repo <scratch clone at 5e35699> --rev 5e35699` in `$HYAKU_SCRATCH/tameshi-r57/T57W1ScribeRecords/clone` | exit 0; `calibration_restraint_score": 8`, `sections_covered": 64`, `box3_full_page": true` (`coldread-base.stdout`) |
| Base ledger has 49 rows: 31 fixed, 7 open, 11 declined; open ids R45.1, R45.4, R46.2, R47.5, R48.4, R49.3, R49.5 | `git show 5e35699:corpus/routed-defects.json` + python Counter | `ledger-base-counts.txt`: `rows 49 {'fixed': 31, 'declined': 11, 'open': 7}` and the seven open ids |
| Base registry: 57 rows, `gate` 22, `selftest` 31, `probe` 4; one row mentions `receipt-revision-gate` | `git show 5e35699:tools/registry.json` (`registry-base.json`) | `registry-base-count.txt` |
| Base SKILL.md `## Standing rules` row 1 (line 53) names `RECEIPT_REV_MISMATCH` for a verdict receipt naming another revision | `git show 5e35699:SKILL.md \| grep -n RECEIPT_` | line 53 as quoted in the skeleton |
| Sources census at base: exit 0, 142 `S` rows | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` run in the lane; `grep -c "^| S[0-9]"` on `5e35699:corpus/SOURCES.md` | `census-now.stdout` (exit 0, 17 lines, W04 notices only); 142 rows |
| The ledger extension's routed-item count is 51 (expected) | not re-derived here; the dry run at a scratch REV prints `rows=0/51` for the staged C1 counter | `T57W1ExecControls-receipts/dry-real-counters.stdout` (other seat's receipt, cited not copied) |

## Sweeps and checks run on the drafts

- **Planned-paragraph parse** (mirrors the staged counter's `planned_ids`: newest line starting `**Planned (round`, contiguous until a blank line): one paragraph line; counter-visible ids `R56.1, R56.4`; carried R4x ids named but not counted by the regex (`planned-paragraph-parse.txt`). Consequence: the seven R4x rows are not checked by the counter at all (their rows are "old49" and only need identity), so naming them is a human record, not a gate.
- **Append-only check**: `cmp -n` on base byte length for SCORECARD and LOG (both identical prefix); `diff | grep -c '^<'` = 0 for both (`stage-append-check.txt`).
- **Counter-line transcription**: every counter line quoted in the drafts is either a base receipt I re-ran (coldread, census, registry) or a dry-run line in another seat's receipt (`dry-real-counters.stdout`, `CONTROLS_A: 8/8`, `CONTROLS_B: 0/2`, `rows=0/51`). Before values for C1 and C2 are NOT measured here; the contract's before text is cited and the committed before receipt is `<TBD>`.
- **Attack on the mistake row**: I checked the claim "controls.sh does not read a committed round-57 receipt". `grep -n "control/\|after/\|controls-a\|controls-b\|cat \|git show"` on the staged script (`controls-read-paths.txt`) finds no read of a committed control or `after/` receipt: the only receipt-shaped reference is the REV guard at line 54 (`ls-tree` for `control/controls-` or `after/` refuses with exit 2), and the generators at lines 126 and 132 are executed from the clone, not read as receipts. This is a grep, not a run: the read-mode mutant is not executed, so the row names it `<TBD: mutant>` and claims only that the fix is recomputed by construction and that the dry run shows the positive arms can fail.

## Findings for the L1

1. **`before/` is empty.** `.ufo/evidence/round-57/before/` exists but has no files, while the contract's `before` fields and the SCORECARD claim table cite `before/c1.stdout` and `before/c2.stdout`. This is the round-56 landing class ("before-receipts cited while untracked") recurring. C0 must commit them. Recorded as the candidate mined-mistake row in the lesson, not confirmed as a closed finding.
2. **The lesson's "first mistake" is ambiguous.** The round-56 lesson's `## Mistakes` opens with the landing class (R55.6, uncommitted round evidence). Its `## Attempt 4` opens with control design. `controls.sh` cites the Attempt-4 row by name, so I used that one. The landing row is addressed by `deciding-run.sh`'s clean-tree gates, not by `controls.sh`. L1 to confirm which row the task meant; if both, add one row.
3. **Planned paragraph is the C1 open gate.** The round-56 block has no `**Planned (round` paragraph, so at base the newest is round 55's. The round-57 block adds the round-58 one; it must stay the last such paragraph in the file and must not be split by a blank line.
4. **Open-row set is not known.** The `<TBD:open ids>` slot must be filled from the round-57 ledger after the 51 new rows exist; `R56.1` is open per the contract; `R56.4` depends on whether a referent record is written. Writing the paragraph before the ledger is final will make `CTL_OPEN` / `open-unplanned` the first thing to re-check.
5. **Not verified here:** SOURCES S283 (scout material only), QUALITY criterion numbers, the forecast receipt path, the `R56.x` status values, controls and deciding receipts, every `<TBD>`.

## Out of scope (not touched)

No lane file edited; no git mutation in the lane or fleet repo; no SKILL.md, QUALITY.md, SOURCES.md or README.md change (the no-harm drift risk); no sources row; no ledger row; no tool installed (none needed: `python3`, `git`, `sha256sum`, `diff` were already present). Tool record: none.

## Receipts

Directory `.ufo/waves/round-57/w1/T57W1ScribeRecords-receipts/`: `clone-head.txt`, `coldread-base.stdout`, `coldread-base.stderr`, `census-now.stdout`, `registry-base.json`, `registry-base-count.txt`, `ledger-base-counts.txt`, `controls-read-paths.txt`, `planned-paragraph-parse.txt`, `stage-append-check.txt`, `stage-sha256.txt`.

## Next (for the L1)

- Copy the three staged files into the lane at the freeze step; re-run `stage-sha256.txt` against the copies.
- Fill every `<TBD>`; the SCORECARD counter lines, LOG and lesson values must come from the committed receipts, not from this draft.
- Run the round-57 counters at REV only after the staged instruments are frozen (the L1's job, not this seat's).
