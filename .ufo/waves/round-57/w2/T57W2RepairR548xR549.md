# T57W2RepairR548xR549 — ledger rows R54.8 and R54.9 (round 57, wave 2, C1 calibration)

Lane base `5e3569969b532310d2b8a3d130901757a3df356b`; master at run time `06e9849787c8f92951a146935df2812485142f7d` (adds C0 `ca75c26` and wave-1 evidence `06e9849`; neither touches the cited evidence paths). Ledger source: working tree `corpus/routed-defects.json` (uncommitted). Nothing was committed in the lane; no lane file was edited in place.

## Verdict

| id | result | status | status_at_base | change |
|---|---|---|---|---|
| R54.8 | **repaired** (dry run: no fault line) | open (unchanged) | open (unchanged) | evidence replaced |
| R54.9 | **unrepairable** under the amended counter (dry run still `fixed-not-new`) | fixed (unchanged) | fixed (unchanged) | none; note refreshed |

No status was changed. Neither status was proven wrong by a command (see sweeps below), so no status change is proposed.

## R54.8 — repaired

Old evidence: `corpus/lessons/round-54.md:98-98` (heading, unkeyed) and `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md:343-343`. The seat-file item is `soft-excluded-path`: a `.ufo/waves/` path is admitted only when it ends with one of the item's keys, and `.../T54W1ExecStraceNoise.md` does not end with `T54W1ExecStraceNoise`. The seat file cannot be evidence under the amended rule, and no key may be weakened.

New evidence (one item, keyed):
- `SCORECARD.md` lines `2683-2685`, excerpt `The incident is now recorded in \`corpus/lessons/round-55.md\` and \`.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md\` is marked superseded.` It carries the keys `T54W1ExecStraceNoise` and `superseded` as whole tokens, resolves at master, and states where the record lives (round-55.md, not the round-54 lesson).

Why the row stays `open`: the item has two parts. (a) the seat file's own text is fixed at `9cf0146` (SUPERSEDED block present at base: `grep -n "SUPERSEDED (round 55"` → line 332). (b) `corpus/lessons/round-54.md` still has no config.yml record: `git show 06e9849:corpus/lessons/round-54.md | grep -c config.yml` → `0`. Part (b) is open, so `open` is the truthful status. Status unchanged.

Note for the L1: the row's `after_patch` is kept verbatim. When the staged `round-54.md` patch lands and the row flips to `fixed`, the landing commit must (1) name `R54.8` in its message (`names_id`), or (2) the evidence path must be named in the item text. `corpus/lessons/round-54.md` is named in neither, so a commit whose message does not name R54.8 gives `fixed-not-new`.

## R54.9 — unrepairable (no admissible evidence for `fixed`)

Lane-side figures are true (status `fixed` not proven wrong):
- `.ufo/waves/round-54/w1-registry.json` at base: `seats 76, attack_seats 21, role_mix.reviewer 5`; 21/76 = 27.6 %.
- `find /home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge -name '*.md' | wc -l` → `81`.
- SCORECARD `ER-R54-9` (`2692-2696`) and `corpus/lessons/round-54.md:51-52` carry the corrected numbers.
- The round-54 report that prints "4 reviewers / 26.3 %" is outside the lane (`.ufo/reports/` holds only `round-1`), as the row's note already says.

Why no admissible `fixed` evidence exists: the only commit that introduced the keyed excerpt is `9cf0146` (`git log -S'27.6' -- SCORECARD.md` → 9cf0146 only). The counter requires the commit to name the id or the evidence path to be named in the item text:
- `9cf0146` message names R54.9: **no** (`grep -c "R54\.9"` → 0).
- Any commit in `650987a..master` naming R54.9: **none** (`git log --grep='R54\.9'` → 0 lines).
- Item text names `SCORECARD.md`: **no**; names `corpus/lessons/round-54.md`: **no** (`SCORECARD.md` and `round-54.md` are not substrings of the item text; only `w1-registry.json`, `role_mix`, `attack_seats`, `27.6`, `81`, `84` appear).
- `.ufo/waves/round-54/w1-registry.json` (the only path named in the text) was last touched at `19c7558`, before routed_at; no commit after routed_at touches it.
- Other `role_mix` / `27.6` / `attack_seats` carriers after routed_at (`9cf0146`, `631cd64`, `51d1f0e`, `6efd2a1`, `0a2010a`) are either spot-check files (excluded), frozen counters (`.ufo/evidence/round-55/c1/measure.py`, path basename not in the item text, commit names no R-id), or do not name R54.9.

I did not weaken a key, invent a commit, or add a line to the lane. Options left to the L1 (decision, not a repair here): (a) land a commit whose message names `R54.9` and whose diff introduces a keyed excerpt into a lane file (a content change; not made by this seat); (b) accept the row as `fixed-not-new` and disclose it; (c) reclassify as `open` (a status change, which is a finding and not proposed here, because the lane-side record is in fact corrected).

## Dry runs (verbatim fault/verdict lines)

Patched ledger (`LEDGER=$S/ledger.json bash .ufo/waves/round-57/dry-c1.sh 80`, receipt `T57W2RepairR548xR549-receipts/dry-patched.out`):

```
EXPLAIN fixed-not-new R54.9
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=3 key_miss=8 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=31dcded5ebbc rows=51/51 agree=32/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=20 C1_R57_PASS=false
```

Baseline, working-tree ledger with no override (receipt `dry-base.out`):

```
EXPLAIN evidence-bad R54.8 soft-excluded-path .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md
EXPLAIN fixed-not-new R54.9
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=4 key_miss=8 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=068e11ab51b4 rows=51/51 agree=31/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=21 C1_R57_PASS=false
```

Delta: R54.8's `evidence-bad` line is gone (evidence_bad 4→3, agree 31→32, total 21→20). R54.9's `fixed-not-new` remains. The `panel_pin=1` term and the `panel-pin` EXPLAIN line come from the unpinned `panel.json` (PANEL_SHA256 pending the L1), not from these rows; they are outside this seat's item.

The `key_miss` (8) and `fixed_bad` (8) counts in the TERMS line are other rows' faults, reported as found; this seat did not touch them.

## Artifacts

- `.ufo/waves/round-57/w2/T57W2RepairR548xR549/rows.json` — the two full replacement rows (all fields; R54.8 keeps `after_patch`).
- `.ufo/waves/round-57/w2/T57W2RepairR548xR549-receipts/` — `dry-patched.out`, `dry-base.out`, `ledger-patched.json`, `sweep.txt` (the R54.8 and R54.9 sweep outputs above).
- `.ufo/waves/round-57/w2/T57W2RepairR548xR549.json` — machine-readable summary.

## Tooling

No installs or upgrades. No pacman, no `~/.local/bin` writes.

## Out of scope / residual

- Lane git was read-only throughout (`log`, `show`, `grep`, `diff-tree`, `status`, `merge-base` via the counter). The scratch clone was removed.
- The `dry-c1.sh` run rewrites `$HYAKU_SCRATCH/tameshi-r57/L1-dry` (its own fixed path); this seat's scratch is `$HYAKU_SCRATCH/tameshi-r57/T57W2RepairR548xR549`, removed of its clone.
