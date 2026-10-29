# T57W1ScribeItemsR53x7to9 — ledger rows R53.7–R53.9

Seat: T57W1ScribeItemsR53x7to9 (leaf scribe, judged on calibration). Lane base `5e3569969b532310d2b8a3d130901757a3df356b`. Source: `corpus/lessons/round-53-verifier-spotcheck.md` lines 84–86 (routed items 7–9, id rule: unlabelled-by-position, here labelled `**R53.n`). Spot-check added at `2ef0a5ad429de7f204b0e8138b2f36dcbb32a626` (routed_at); the item R53.9 line was appended later at `abae0a0`, which does not change routed_at (the round-50 extractor takes the `--diff-filter=A` commit).

## Verdicts

| id | status | commit | evidence (lane paths, lines) | cheap fix |
|---|---|---|---|---|
| R53.7 | fixed | `19c75588b3c581a0dc84ea87e09d33d88a99ac8e` | `.ufo/evidence/round-54/integrate/binder.py` 166, 142, 183 | n/a |
| R53.8 | open | — | `corpus/lessons/round-53.md` 23, 31–32 | fixable-cheap (staged) |
| R53.9 | fixed | `d33053f7552db4bd290c99a36979760f544c41ad` | `.ufo/waves/round-53/w2/T53W2RevW1Specialists.md` 1, `.ufo/waves/round-53/w1/T53W1ExecR523.md` 1 | n/a |

No item is `declined`. No item is `unresolved`.

## R53.7 — "inputs pinned at C7" imprecise → fixed

- Claim as routed: 11 of 11 747 rekey input keys pin at read_rev / fix-pass-2 rather than C7 `8f474419`; the rekey-final commit (88afa94) says "inputs pinned at C7".
- Tree at base: the live rekey driver `.ufo/evidence/round-54/integrate/binder.py` reads every input blob at the PIN revision (`b = blob_at(pin, p)`, line 142) and records `read_rev` C0 separately (line 183) and the pin hash in `rev_reason` (line 166). The round-53 driver string `(the content-final revision)` survives only in the immutable `.ufo/evidence/round-53/integrate/rekey.py:160`.
- Commit: `19c75588b3c581a0dc84ea87e09d33d88a99ac8e` (round-54 re-freeze) is the first commit that adds this binder; the three cited lines exist in it at 136, 155 and 171 (the file moved by later edits, so base line numbers differ; excerpts are verified at base and the excerpt absence check is at routed_at, where the path did not exist).
- Judgement call for the L1: the round-55 disposition (`T55W1Connector2-receipts/round54-dispositions.stdout`) also records this as FIXED, citing the round-55 binder lineage; I chose the earliest commit that carries the corrected surface. The round-53 wording and commit 88afa94's message cannot be edited; if the L1 reads "fixed" as requiring the historical record to be retracted, R53.7 becomes `open` and not-fixable.

## R53.8 — S275 locator → open (partly fixed)

- Fixed at `99c3bc88d704566197783f66b211ee0a830e0330` (round-54 C1 fix pass): `corpus/SOURCES.md:150` and `corpus/knowledge/change-aware-resweep-cadence.md:2` now read `p. 3 (physical …)`. This half is not counted as open.
- Still true at base: `corpus/lessons/round-53.md:23` reads `quote (22 words, camera-ready p. 4, pdftotext lines 289–294)` and `:31–32` reads `Located quote (19 words, abstract)`. Both quotes count 20 words (python `str.split`: S275 = 20, S276 = 20). The item's word-count parenthetical defect therefore holds at base, so status is `open`.
- Staged correction (fixable-cheap): `stage/corpus/lessons/round-53.md` (full file, two replacements, asserted count 1 each). Patch: `T57W1ScribeItemsR53x7to9-receipts/lesson-round-53-R53.8.patch`. Result text: `(20 words, camera-ready p. 3 (physical; printed footer 1787), pdftotext lines 289–294)` and `(20 words, abstract)`.
- Cold-read cost: the lesson file is not in any cold-read input set (`grep -c "lessons/round-53.md" .ufo/evidence/round-21/coldread/ledger.json` → 0; the grep over all `lessons/round-53` path strings returns nothing). No SKILL.md or pinned section is touched.
- Alternative for the L1: if the page-cell half alone is taken as the item, R53.8 is `fixed` at 99c3bc8. The lesson parenthetical still disagrees with the tree, so I do not claim that.

## R53.9 — uncommitted round work → fixed

- Commit `d33053f7552db4bd290c99a36979760f544c41ad` ("round-53: land wave receipts that were never committed", 2026-10-27 11:43:51 −0300) adds all six named files. At base `git ls-tree` lists all six; `git status --porcelain` at the lane shows no round-53 untracked file (only the round-57 directories, which are this round's own work).
- d33053f is an ancestor of base and not of routed_at.

## Round-50 counter compatibility (flags for the L1)

1. `planned_ids` in `.ufo/evidence/round-50/c1/measure.py` matches only `\bR4\d\.\d+\b` (line 111). An `open` row for R53.8 therefore cannot satisfy the inherited rule as written; the round-57 counter must widen the pattern to R5x, or the row must become `fixed` after the L1 lands the lesson patch. I did not edit the round-50 counter. At base `planned_ids` returns `[]`.
2. The newest `**Planned (round` paragraph at base is round 55 (`SCORECARD.md:2598`) and does not name R53.8; the L1 must plant it in the round-57 Planned paragraph if R53.8 stays open.
3. Keys for each row are in `rows.json` (`keys`, 4 each). The rows' excerpts contain at least one key (R53.7: `inputs pinned at PIN`; R53.8: `camera-ready p. 4`, `22 words`, `19 words`; R53.9: `T53W2RevW1Specialists`, `T53W1ExecR523`). `has_key` also passes via path suffix for the `.ufo/waves/` paths, which are SOFT-excluded unless the path ends with a key.

## Sweep (commands and outputs)

- Row verification (reuses `check_evidence`, `has_key`, `touched`, `is_ancestor`, `show`, `norm`, `ACK_WORDS`, `planned_ids` imported from the round-50 counter, not copied): `T57W1ScribeItemsR53x7to9-receipts/verify-rows.stdout` → `R53.7 fixed PASS`, `R53.8 open PASS`, `R53.9 fixed PASS`, `ALL_ROWS_PASS`, exit 0. Spot-check set passed to `check_evidence` = round 40–56 spot-check paths.
- Ancestry, touched files, ls-tree, historical greps, word counts, ledger pin grep: `T57W1ScribeItemsR53x7to9-receipts/git-facts.stdout`.
- Commands used for the phrase history: `git log -S"(the content-final revision)" -- .ufo/evidence/`, `git log -S'p. 3 (physical'`, `git log -S'camera-ready p. 4'` (all read-only).
- No lane file was edited; the only writes are under `.ufo/waves/round-57/w1/` and the scratch directory (removed after the run).

## Outputs

- `rows.json` (this directory): three rows, schema `{id, status, evidence[{path,lines,excerpt}], commit (fixed), keys, seat, note, verdict_basis}`. Rows carry no `reason` (no declined rows).
- `T57W1ScribeItemsR53x7to9.json`: machine-readable summary (beside this file).
- `T57W1ScribeItemsR53x7to9-receipts/`: `verify-rows.stdout`, `git-facts.stdout`, `lesson-round-53-R53.8.patch`, `verify.py`, `rows-spec.py`.
- `stage/corpus/lessons/round-53.md` (R53.8 staged correction).

## Tools

None installed or upgraded. Verification used `git` and Python 3 already on the host.

## Not run

- The round-57 C1 counter and the round-21 cold-read monitor were not run (outside this seat's brief; the L1 freezes and scores after wave 1).
- The staged lesson patch was not re-run through the sources census (lesson text is not a census row); the L1 should run it with the other staged files.
