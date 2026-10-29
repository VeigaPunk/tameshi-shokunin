# T57W2RepairR5410xR551 — repair ledger rows R54.10, R55.1 (C1 calibration)

Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin · base 5e3569969b532310d2b8a3d130901757a3df356b · C0 ca75c2674645ab6bdadeecb8584007c74342bfa9.
Scratch: /fast/scratch/hyaku/tameshi-r57/T57W2RepairR5410xR551 (clone at C0; removed at exit). No tool installed or upgraded. No lane file edited; no lane git mutation.

## Outcome

| id | result | status | commit | dry-run line |
|---|---|---|---|---|
| R55.1 | REPAIRED (evidence and commit replaced; status unchanged) | fixed (unchanged) | c3e2ca9 → **18bbdab** | no EXPLAIN line for R55.1 |
| R54.10 | **UNREPAIRABLE** under the amended counter (row left verbatim; status unchanged) | fixed (unchanged, verified true) | 9cf0146 (unchanged) | `EXPLAIN fixed-not-new R54.10` |

`rows.json` holds both rows as full replacement objects. R54.10 is included verbatim except for an appended note stating the unrepairable result; its evidence and commit are unchanged.

## R55.1 — repaired

Why the row failed: the dry-run reason `fixed-not-new R55.1` is correct for the old commit. `c3e2ca9` (round-56 freeze) touches none of the keyed paths; its only excerpt-bearing file is the instrument set. The keyed evidence `.ufo/evidence/round-56/before/c2.stdout` line 4 was introduced by `c0137451`, not by `c3e2ca9`.

Sweep for an admissible fix commit (commands in the scratch clone):
- `git log -- .ufo/evidence/round-56/after/c2.stdout` → only `18bbdab` (round-56 attempt 4 "deciding-run receipts at 1b44bace … C2_R56_PASS=true"). `git show --stat 18bbdab -- …after/c2.stdout` → `7 +++++++` (new file). `1b44bace` does not touch it.
- `after/c2.stdout` line 7 at base: `C2_R56: rev=1b44bace0974 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=PASS docs=4/4 total=0 C2_R56_PASS=true`. Complete file (7 lines, ends with verdict).
- Ancestry: `18bbdab` ancestor of base; not ancestor of routed_at `fa48c06c` (round-55 spot-check). Parent lacks the file; routed_at lacks the file. No ACK words in the span.
- Tie: the commit message does not name R55.1; the path is tied by basename `c2.stdout`, which appears in the item text (`after/c2.stdout`).

What changed in the row: `commit` → `18bbdab73b26422e33186076be6be433b3358bc1`; new first evidence item `.ufo/evidence/round-56/after/c2.stdout` lines 7-7; the three original evidence items are kept (all resolve at base). `seat` → this seat (the original is recorded in the note). `status`, `status_at_base` unchanged (`fixed`, `fixed`).

Semantic check (not decided by the counter): the item asks for a C2 verdict at the measured revision, committed. `18bbdab` commits exactly that for round 56 (green, names its measured revision 1b44bace). The `before/c2.stdout` red arm was not the fix; it is retained only as supporting evidence. Caveat recorded in the note: the tie is by basename, not the item's literal round-55 path `after/c2.stdout` (which holds the truncated round-55 verdict in commit 875bb75).

Dry-run lines for R55.1 (from the patched run, receipts/dry-c1-patched.txt): no `EXPLAIN` line names R55.1. Before the patch the L1 dry run printed `EXPLAIN fixed-not-new R55.1`. Terms moved from `fixed_bad=8 agree=31/51` to `fixed_bad=7`, `agree=32/51`.

## R54.10 — unrepairable under the amended counter

Status verified true, not changed. Commands (receipts/r54-10-tie-sweep.txt):
- `9cf0146` adds `**ER-R54-10**` to SCORECARD (`SCORECARD.md` lines 2700-2702 at base). The excerpt is absent at `650987a` (routed_at) and at `9cf0146^`, present at `9cf0146` (grep count 0 / 0 / 1). `9cf0146` is an ancestor of base and not of routed_at. So the fix is real.
- Tie fails. `9cf0146` message (`round-55: C0 — … the round-54 record corrections (ten routed defects …)`) does not contain the id `R54.10` (regex `(?<![\w.])R54\.10(?!\d)` → False). The item text (`defects.json` `R54.10`) names neither `SCORECARD.md` nor its basename → the commit is never a candidate for the fresh-excerpt check.
- Sweep for any other commit that could tie: `git log --all -F --grep=R54.10` → only `0a2010a` (round-54 erratum that routes the defect; it is the routing record, not a fix). Basenames in the item text (`controls-a.stdout`, `r53-counter-at-88afa941.stdout`): tie-able files introduced after routed_at are the round-55/56 control receipts (`4c04c1d`, `caf6742`, `875bb75`, and waves fixtures); none contains a `CTL_R53` line (grep count 0 at base), so none carries the excerpt. The two keyed evidence files that predate routed_at (`19c7558`) are not fresh.
- Honest conclusion: the only commit that fixes the misquote is `9cf0146`, and the counter's tie rule (message names id, or item names the path) cannot see it. I did not borrow a control-receipt commit as the "fix" (it would relabel an unrelated commit), did not weaken a key, and did not change status.

Decision needed from the L1 (not mine to make): either amend the tie rule so a correction commit is accepted when its diff adds a keyed excerpt to a file the item's own evidence names, or accept R54.10 as a documented tie exception. Without one of these, R54.10 keeps the `fixed-not-new` fault and the counter stays at `fixed_bad=7`.

## Dry-run output (patched ledger; receipts/dry-c1-patched.txt)

Command: `python3 …/patch-ledger.py …/corpus/routed-defects.json …/rows.json $S/ledger.json` (prints `patched 2`), then `LEDGER=$S/ledger.json bash …/dry-c1.sh 80`.

```
EXPLAIN fixed-not-new R54.10
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=4 key_miss=8 fixed_bad=7 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=abceb61c99f6 rows=51/51 agree=32/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=20 C1_R57_PASS=false
```

The two ids must not appear in any fault line: R55.1 does not; R54.10 does (`fixed-not-new`, unrepairable as above). Rev differs between runs because each dry run creates a new fixture commit (first run `ae6e32de04eb`).

Other lines are unchanged from the L1 baseline and are outside this item (not touched). Notable for the L1: `panel_pin=1` — `panel.json` pin (`PANEL_SHA256 = 'PIN_PENDING_SET_BY_L1_AFTER_THE_BLIND_PANEL'`) is still unset, so the panel arm does not yet verify.

## Files

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2RepairR5410xR551/rows.json` — two replacement rows.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2RepairR5410xR551.json` — machine-readable outcome.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2RepairR5410xR551-receipts/` — `r54-10-tie-sweep.txt`, `dry-c1-patched.txt`.

## Checks the main agent should run

- `python3 …/patch-ledger.py …/corpus/routed-defects.json …/w2/T57W2RepairR5410xR551/rows.json <out>` then the dry run with `LEDGER=<out>`, expecting no `R55.1` fault.
- Decide the R54.10 tie question above before the C1 verdict can go PASS.
