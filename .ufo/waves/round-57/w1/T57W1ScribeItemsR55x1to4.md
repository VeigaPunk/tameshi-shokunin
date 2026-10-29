# T57W1ScribeItemsR55x1to4 — ledger rows R55.1–R55.4

seat: T57W1ScribeItemsR55x1to4 (leaf, scribe-triage) · milestone: ledger rows R55.1-4 · base `5e3569969b532310d2b8a3d130901757a3df356b` · spot-check `corpus/lessons/round-55-verifier-spotcheck.md` added at `fa48c06c3669355fd80e8722eb733c1d6dfdd2f8` (not an ancestor of the base's freeze/fix commits)

Machine-readable: `T57W1ScribeItemsR55x1to4.json`. Rows: `T57W1ScribeItemsR55x1to4/rows.json`. Receipts: `T57W1ScribeItemsR55x1to4-receipts/`.

## Verdicts

| id | status | basis at base (tree) | fixable |
|---|---|---|---|
| R55.1 | **fixed** (commit `c3e2ca9f020776b3d66c7af854fb82c834674fcf`, round 56) | `deciding-run.sh` gate 0c (`receipt-revision-gate.py --certified REV` on the verdict receipts) exists at base; red-before `before/c2.stdout:4` `RECEIPT_REV_ABSENT`; green `after/receipt-gate-verdicts.stdout:3` `verdict=PASS revs=1b44bace0974` | none needed |
| R55.2 | **open** | `T55W1ScribeSkill-receipts/c2-integrated.out:44` still reads `total=1 C2_R55_PASS=false`; wave-3 record `T56W3ScribeRecords.md:30` shows the class recurring (`total=6` quoted vs `total=2`). No instrument checks quoted bytes. Round-56 disposition: carried. | fixable-costly (see below) |
| R55.3 | **fixed** (commit `2f5512a8ab0771fb2eee463ec16db359174f5edd`, round 56) | `SCORECARD.md:2718` restated calibration row (score 8, measured commit `c1dd23b`, last change 56). Base monitor re-run (scratch clone): `calibration_restraint_score=8`, `sections_covered=64/64`, `box3_full_page=true`, exit 0 | none needed |
| R55.4 | **open** | Lane records say carried: `T56W1RevRound55Dispositions.md:12` (F2: "FIXED by construction" is an overclaim; "Correct disposition is `carried`") and `T56W3ScribeRecords.md:148` (`| **carried**`). No instrument compares a report's status sentence with the receipt it describes. The stale sentence itself is fleet-side (`.ufo/reports/round-55/tameshi.md:93`), not lane evidence. | fixable-cheap for the lane record; the defect is costly |

## Ledger rows

Each row is `{id, status, evidence[{path, lines, excerpt}], commit | reason, seat, note}` in the round-50 schema, plus `keys` and `verdict_basis` in `rows.json`. The L1 must **drop `keys` and `verdict_basis` from the ledger objects** (or move `keys` to a keys file); they are not ledger fields.

Evidence paths: `.ufo/evidence/round-56/deciding-run.sh`, `.ufo/evidence/round-56/after/receipt-gate-verdicts.stdout`, `.ufo/evidence/round-56/before/c2.stdout`, `SCORECARD.md`, `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out`, `.ufo/waves/round-56/w3/T56W3ScribeRecords.md`, `.ufo/waves/round-56/w1/T56W1RevRound55Dispositions.md`. None is a spot-check, the ledger, or a round-57 c1/control file. Every `lines` span is one line.

## Verification (sweep and output)

- Resolver reuse: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-50/c1/measure.py` imported by path (`sys.dont_write_bytecode=True`), not copied. `check_evidence` and `has_key` used per item; `measure()` run over the four rows with `show` stubbed only for the ledger path and, in pass 2, `planned_ids` stubbed. Output: `receipts/verify.out`, script `receipts/verify.py`.
- Per-item resolution: all 8 evidence items resolve at `5e35699` (`resolves`); keyed items present for every id.
- Pass 1 (frozen rules as they stand): `stat={fixed:2, open:2, declined:0, fixed_this_round:0} counts={open_unplanned:2} total=2`. The only failures are the two `open` ids, which are not yet named in a `**Planned (round` paragraph.
- Pass 2 (planned check stubbed to R55.2, R55.4): `total=0`. So the remaining arms (evidence, keys, fixed ancestry, touched-file freshness, ACK words, spot-check hash) all pass.
- Ancestry and excerpt-absence sweep: `receipts/sweep.txt`. `c3e2ca9f` and `2f5512a8` are ancestors of base and not of `fa48c06`. R55.1's excerpt is absent at `fa48c06` (file absent); R55.3's excerpt is absent at `fa48c06` and present at base.
- Base monitor (round-21, scratch clone at base): `receipts/monitor-base-summary.json`.

## Fixable classification

- **R55.1, R55.3**: fixed; no patch.
- **R55.2**: fixable-costly. A real fix is a quote-vs-receipt arm in the C2 counter (a freeze amendment) plus a QUALITY 107 scope edit. `corpus/QUALITY.md` is pinned by 73 cold-read entries across 13 headings: `### Round-20 gate/probe registry — frozen receipt instruments` (19), `# tameshi-shokunin` (13), `## Live-tree re-pin and entry-command monitor — round 17` (7), `### Round-21 gate/probe registry — finite environment differential` (7), `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (7), `### Triggers T1–T3 and the re-pin rule` (5), `### Round-18 gate/probe registry — routed-defect closure` (5), `## Standing rules` (4), `## Ninth recorded case — round 26` (2), `## No-permissiveness audit recipe` (1), `## The cadence's first scheduled tick, and the service's limits (round 9, measured)` (1), `## Gate-shape decision table — hermetic vs live vs audit-lane` (1), `### Where to enter — four readers` (1). Not staged.
- **R55.4**: the defect itself is costly (a falsifier for status prose needs a counter arm and a QUALITY criterion). The lane-record overclaim is cheap: `corpus/lessons/round-56.md` row R55.4 still says "FIXED by construction", contradicting the wave-1 F2 finding and the wave-3 record. That lesson file is pinned by **0** cold-read entries. Staged: `T57W1ScribeItemsR55x1to4/stage/corpus/lessons/round-56.md` (only line 105 changes; diff in `receipts/R55.4-lesson-row.diff`). R55.4 stays `open` in the ledger; the staged change does not fix the defect.
- No staged file touches `SKILL.md`, `SOURCES.md`, `README.md`, a knowledge entry, or a counter.

## Flags for the L1

1. **Planned paragraph.** `open` rows R55.2 and R55.4 need the round-57 `**Planned (round 57)` paragraph to name both ids. The round-50 `planned_ids` regex is `\bR4\d\.\d+\b`, which cannot match `R55.x`. The round-57 counter must use an R5x-aware pattern, or both rows fail `open_unplanned`. The current newest Planned paragraph (`SCORECARD.md:2598`, round 55) names neither.
2. **Floors.** R55.1 and R55.3 landed in round 56 (ancestors of base), so `fixed_this_round=0` for this item set. They count toward FIXED_FLOOR only.
3. **Lesson conflict.** `corpus/lessons/round-56.md:105` says R55.4 is FIXED. The ledger row says open. Either the staged correction goes in or the L1 accepts the conflict in the round-57 record.
4. **Monitor reads fleet inputs.** The round-21 monitor's external inputs are fleet paths (for example `/home/vgpnk/Projects/shokunin/SCORECARD.md`), so a fleet edit can change its reading even when the lane is unchanged.
5. **Counter not yet written.** `.ufo/evidence/round-57/c1/` is empty at this check; the verification above used the round-50 rules directly, as the assignment requires.

## Out of scope / not run

- Did not run the round-57 C1 or C2 counters, `deciding-run.sh`, or `controls.sh`.
- Did not edit any tracked lane file, the ledger, SKILL.md, or any frozen path under `.ufo/evidence/round-5[0-6]/`.
- No tools installed or upgraded (no `RULES.md` channel used).
- Pre-existing `.ufo/evidence/round-50/c1/__pycache__/` (not created by this seat; its `measure.cpython-314.pyc` predates this round) left untouched.
