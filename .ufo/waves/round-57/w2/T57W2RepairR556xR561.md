# T57W2RepairR556xR561 — repair ledger rows R55.6 and R56.1 (round 57, wave 2, C1 calibration)

Seat: T57W2RepairR556xR561. Lane base 5e3569969b532310d2b8a3d130901757a3df356b; master 06e9849 (C0 ca75c26 landed).
Outputs: `rows.json` (full replacement rows, in `T57W2RepairR556xR561/`), this report, `T57W2RepairR556xR561.json`,
receipts in `T57W2RepairR556xR561-receipts/` (`dry-c1-patched.txt`, `ledger-patched.json`, `sweep.txt`).
Ledger and counter were not edited in the lane; the patched ledger exists only in scratch and in receipts.

## Result
- R55.6: repaired. `status` fixed (kept), `status_at_base` fixed (kept). Two evidence items cited (was six, four rejected by
  the waves/ soft rule). Commit set to 981c5e8b (was already 981c5e8b). Note rewritten: it previously said "six are cited here".
- R56.1: repaired. `status` open (kept), `status_at_base` open (kept). Four existing evidence items kept (they resolve);
  one keyed item added: `SCORECARD.md:2753-2753`, excerpt `SKILL.md page-local anchors (57 of 61 distinct ranges`.
- No status change. Nothing is `unrepairable`.

## R55.6 — why the old row failed, and the sweep
Item (defects.json): seven uncommitted round-55 receipts; keys `T55W1ExecRekeyPrep-receipts`, `T55W1ExecNoHarm-receipts`,
`coldread-at-base.json`, `coldread-HEAD.json`, `T55W2ScoutColdread-receipts`.
EXPLAIN before: `evidence-bad R55.6 soft-excluded-path` x4 (base.json, cand.json, rekey.json, inputs.json).
Rule: a `.ufo/waves/` path is admitted only when it ENDS with one of the keys. `.../T55W1ExecRekeyPrep-receipts/base.json`
ends with `base.json` (no key); `inputs.json` ends with no key. Only the two `coldread-*.json` paths end with a key.

Sweep (command `git -C <lane> show --stat 981c5e8b` and `ls-tree` at base and parent, output in receipts/sweep.txt):
- 981c5e8b is an ancestor of base: yes. It is NOT an ancestor of routed_at fa48c06c: correct for `fixed`.
- 981c5e8b adds all seven item files (absent at parent 6efd2a1, present once at base). Its message names `(R55.6)`.
- The `coldread-at-base.json` and `coldread-HEAD.json` lines 1-2 are `{` and `  "calibration_restraint_score": 8,` / `6,`.
  The excerpt `{ "calibration_restraint_score": 8,` (whitespace-normalised) is in lines 1-2, has no ACK word, and the
  file is absent at routed_at and at the parent: the fixed-not-new check passes.
- The four excluded receipts cannot be cited under the amended rule, so the row cites the two it can. The truth is
  unchanged: the commit adds all seven.
- `floor.json` (same commit, not in the item) is not cited.

## R56.1 — why the old row failed, and the sweep
EXPLAIN before: `key-miss R56.1`. All four evidence items resolved; none of their excerpts contained a key.
Keys: `page-local`, `heading anchors`, `line anchors`, `QUALITY 34` (whole token, case-insensitive).
Sweep: `git -C <lane> grep -n -i -E 'page-local|heading anchors|line anchors|quality 34' master` (excluding spot-checks,
ledger, round-5x evidence, waves). Hits in admissible lane files:
- SCORECARD.md:2534 (`restore-discipline anchors...`), 2753 (`SKILL.md page-local anchors (57 of 61 distinct ranges`), and
  2753 is a current-state statement: the residual is "not claimed fixed". Chosen.
- corpus/lessons/round-56.md:92, :132, :208 (`page-local` line ranges, the routed origin), tools/cold-read-forecast.py:38,555.
- SKILL.md:1059 `line anchors` is the jj-lane helper, not the R56.1 subject: rejected.
The SCORECARD 2753 excerpt is at master, and SCORECARD.md has no working-tree diff against master (`git diff master -- SCORECARD.md` is empty).
R56.1 is open in the dry run, so the Planned line the dry script appends names it (open_unplanned did not fire).

## Dry runs (scratch, `dry-c1.sh 80`, LEDGER override)
Command: `python3 .../patch-ledger.py .../corpus/routed-defects.json .../w2/T57W2RepairR556xR561/rows.json $S/ledger.json`
then `LEDGER=$S/ledger.json bash .ufo/waves/round-57/dry-c1.sh 80`.
Patch output: `patched 2`. Dry run exit 0.

EXPLAIN lines containing R55.6 or R56.1: **none** (grep count 0). Remaining EXPLAIN lines (unchanged in kind, not mine):
```
EXPLAIN key-miss R51.1 / fixed-not-new R51.3 / key-miss R51.6 / key-miss R52.1 / key-miss R52.2 / key-miss R52.6
EXPLAIN fixed-not-new R53.6 / fixed-not-new R53.7 / evidence-bad R53.9 (x2, soft) / key-miss R54.5 / key-miss R54.6
EXPLAIN fixed-not-new R54.7 / evidence-bad R54.8 (soft) / fixed-not-new R54.9 / fixed-not-new R54.10
EXPLAIN fixed-not-new R55.1 / fixed-not-new R55.3 / evidence-bad R55.4 (x2, soft) / panel-pin .ufo/evidence/round-57/c1/panel.json
```
Verdict-side lines (dry run):
```
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=3 key_miss=7 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=6215431f7458 rows=51/51 agree=33/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=19 C1_R57_PASS=false
```
Before (ledger as in the lane): `evidence_bad=4 key_miss=8`, `agree=31/51`, `total=21`. After: `evidence_bad=3 key_miss=7`, `agree=33/51`, `total=19`.
Net: two rows now agree, and each removed term is one of my two ids. The verdict is still FAIL for reasons outside this item:
`fixed_bad=8`, `key_miss=7`, `evidence_bad=3` on other rows, and `panel_pin=1` (the blind panel is not pinned yet; L1 owns that).

## Notes for the L1
- The `panel` arm compares the blind-panel verdict on R55.6 and R56.1 with `status_at_base` (both kept). I did not
  read `panel.json` (not pinned, not in my scope).
- The R56.1 status `open` is consistent with the SCORECARD residual at 2753 (unchanged, not proven wrong).
- Tools installed: none. Scratch ($S) removed on exit.
