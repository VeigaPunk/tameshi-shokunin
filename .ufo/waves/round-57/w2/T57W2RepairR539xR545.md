# T57W2RepairR539xR545 — repair of ledger rows R53.9 and R54.5 (C1, wave 2)

Seat: T57W2RepairR539xR545 (leaf repair, calibration). Lane `tameshi-shokunin`, base `5e35699`, dry-run rev `24fd2af` (scratch clone of master + working-tree ledger). Tools installed: none. Lane and fleet not mutated (read-only git only; no commit, no edit in place).

## Result

| id | outcome | evidence after repair | fault left by the amended counter |
|---|---|---|---|
| R53.9 | **repaired** (status `fixed`, commit `d33053f` kept) | `.ufo/waves/round-53/w1-results.json` 188-188, `.ufo/waves/round-53/w2-results.json` 140-140 and 164-164 | none (EXPLAIN line gone) |
| R54.5 | **unrepairable** under the amended counter (status `fixed` kept, commit `9cf0146` kept, evidence unchanged) | none admissible (see sweep) | `key-miss R54.5` (dry run); the deeper blocker is the `fixed-not-new` naming arm, which the same commit would also fail |

Rows for the L1 to install: `.ufo/waves/round-57/w2/T57W2RepairR539xR545/rows.json` (list of two full row objects, all fields).

## R53.9 — what was wrong and the repair

- Old evidence: two `.ufo/waves/round-53/w2/...` and `w1/...` seat `.md` files (`T53W1ExecR523.md`, `T53W2RevW1Specialists.md`). The amended counter's soft rule admits `.ufo/waves/` paths only when the path ends with one of the item's keys; these paths end with `.md`, so both were `evidence-bad soft-excluded-path` (dry-c1-explain lines 9-10).
- Truth check: `d33053f` ("round-53: land wave receipts that were never committed") adds exactly the six named files (`git show --stat d33053f`); all six are tracked at master; `d33053f` is a non-ancestor of routed_at `2ef0a5a` and an ancestor of base; its parent `9b9cd57` and `2ef0a5a` both lack `w1-results.json` / `w2-results.json` (receipts/keyed-check.txt). So `fixed` with commit `d33053f` is true; status unchanged.
- Repair: cite the two results JSON files the same commit added. Paths end with the keys `w1-results.json` / `w2-results.json` (path-suffix key), the excerpts carry the seat keys as whole tokens (`"name": "T53W1ExecR523",`, `"name": "T53W2CritClaims",`, `"name": "T53W2RevW1Specialists",`), each verbatim, one line, span 1. The commit names the paths in the item text (`.ufo/waves/round-53/w1-results.json`, `…/w2-results.json`), so `fixed-not-new` admits them (excerpt absent at routed_at and at the parent; no ACK words).
- Honesty note: the excerpts are seat-name lines of the two results files, not the seats' findings. They establish that the files now exist tracked; the item is that they were untracked. That is what the item asks.

## R54.5 — why it cannot be repaired honestly

The item: the report's wave-1/wave-2 counts (25; 22 in 9) disagree with the committed readers (28; 25 in 12). Re-derived here with a command (base `.ufo/waves/round-54/w1` and `w2` `*Read*.json`, `-receipts/` excluded): w1 = 23 files, 28 findings; w2 = 23 files, 25 findings in 12 non-zero sections. The fix record in `9cf0146` (SCORECARD ER-R54-5, lesson round-55 row) states exactly these values, so the status `fixed` is consistent with the tree. The blocker is evidence admissibility under the amended counter:

1. **Fix commit `9cf0146` fails the naming arm.** Its message does not name R54.5 (`git log --grep 'R54\.5' --grep 'ER-R54-5'` over all history: no hit, receipts/msg-grep-R54.5.txt is empty). Its touched files (1273 paths, receipts/9cf0146-touched.txt) include `SCORECARD.md`, `corpus/lessons/round-54.md`, `corpus/lessons/round-55.md`, but none has a path or basename in the item text (`text` + `extended_text`); the sweep's `named` filter returns no file. `fixed-not-new` therefore refuses any excerpt the commit adds.
2. **No keyed, admissible excerpt introduced by `9cf0146`.** Its added lines containing a key (`minor_gaps`, `99c3bc8`, `25 findings in 12 sections`, `resolutions.json`) sit only in quoted-item receipts and seat reports under `.ufo/waves/round-55/w1/T55W1Connector2-receipts/r54-line-anchors.stdout`, `…/T55W1Connector2.md`, `…/T55W1Er01-receipts/…`, and in a build spec. Those paths are soft and do not end with a key (refused), or are spot-check/ledger/instrument paths (refused). Lane-authored, non-soft lines of `9cf0146` (SCORECARD ER-R54-5, lesson row) carry no key token; the "25 findings in 12 sections" phrase in `corpus/lessons/round-54-verifier-spotcheck.md` is a spot-check (excluded).
3. **Other commits that name the resolutions.json basename** (the sweep found the only commits after routed_at that touch a path the item names): `c31cdd92` (F4 contract C2 value), `51d1f0eb` (C1 fix pass; adds W1-* adjudication rows and receipts with `EXPLAIN R54.5 ... derived=w1=28 w2=25` lines), `63fb53a0` (round-56 gap-minor adjudications), `877eedee` (round-56 integrate). Each would satisfy the path-suffix key and the naming arm mechanically, but none fixes R54.5: their resolutions.json additions are about other items (W1-CCPATCH-REDUNDANT, W1-R54.8-PREMISE, W1-WRAPPED-CLAIM, round-56 adjudication headings). Attributing one of them as the fix would be inventing evidence. Not used.

Sweep run (receipts/sweep-R54.5.txt, `sweep.py`): 29 commits in `routed_at..base`; 4 name a file in the item text (all resolutions.json, all of the commits above); KEYLINE hits in those files at base: none. `git rev-list` ancestry checks: `9cf0146` is an ancestor of base and not of routed_at `650987a` (as the counter requires).

Consequence: the dry run keeps `key-miss R54.5` (the keyed-excerpt arm trips first), and even with a keyed excerpt the `fixed-not-new` arm would refuse `9cf0146`. R54.5 stays a fault in the dry run. The L1 decides; I did not weaken a key, did not name an unrelated commit, and did not invent an excerpt.

Status finding (not acted on; no proof of wrong status): `.ufo/waves/round-55/w1/T55W1CritC1.json:343` on master, and `51d1f0eb`'s diff, carry the text "R54.10 hard-coded literal and R54.5 steerable counts remain open". That is a round-55 critic's status claim about the counter's values, not a proof that the R54.5 record is wrong; `51d1f0eb`'s receipts also show `FAIL premise=ok corrected=miss` for R54.5 in `T55W1CritClaimShape-receipts/c1-base.stdout` and `c1-c2only.stdout` (then `ok` in `c1-head-133b2ce.stdout`). The L1 should read these before deciding whether `fixed` stands. Also: `.ufo/reports/round-54/tameshi.md` is not in the lane (absent at master), so the item's "Report :62" is outside the lane; the lane's correction does not change that report.

## Dry run (scratch clone, rev 24fd2af7cd73)

Command: `python3 .ufo/waves/round-57/patch-ledger.py corpus/routed-defects.json .ufo/waves/round-57/w2/T57W2RepairR539xR545/rows.json $S/ledger.json` → `patched 2`; then `LEDGER=$S/ledger.json bash .ufo/waves/round-57/dry-c1.sh 80`. Full output: receipts/dry-c1-repaired.txt. Relevant lines:

```
EXPLAIN key-miss R54.5
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=3 key_miss=8 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=24fd2af7cd73 rows=51/51 agree=32/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=20 C1_R57_PASS=false
```

Before the repair (the L1's dry run, dry-c1-explain.txt): `evidence-bad R53.9 soft-excluded-path` ×2, `key-miss R54.5`, and `agree=31/51 total=21`. After: R53.9 has no fault line; `agree=32/51 total=20`. The remaining R53.9/R54.5 fault: `key-miss R54.5` only. The other EXPLAIN lines are other seats' rows, unchanged by this repair (untouched: `key-miss R51.1` … `key-miss R56.1`, `panel-pin`).

## Rows (repaired; full objects in rows.json)

- R53.9: `status` fixed; `commit` d33053f7552db4bd290c99a36979760f544c41ad; `status_at_base` fixed; `seat` T57W2RepairR539xR545; `evidence` three items (above); `note` explains the repair.
- R54.5: `status` fixed; `commit` 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb; `status_at_base` fixed; `seat` T57W2RepairR539xR545; `evidence` unchanged (SCORECARD.md 2661-2662; corpus/lessons/round-55.md 59-59); `note` records the unrepairable verdict.

## Checks the main agent should run

- `bash .ufo/waves/round-57/dry-c1.sh` on the installed ledger (expect R53.9 clean, R54.5 still `key-miss`, `agree=32/51`, `total=20`).
- Decide on R54.5 with the L1 (naming arm; the status question in the finding above).

## Receipts

`.ufo/waves/round-57/w2/T57W2RepairR539xR545-receipts/`: `dry-c1-repaired.txt`, `sweep.py`, `sweep-R54.5.txt`, `sweep-R53.9.txt`, `9cf0146-touched.txt`, `msg-grep-R54.5.txt` (empty by design), `resolutions-commits.txt`, `keyed-check.txt`.
