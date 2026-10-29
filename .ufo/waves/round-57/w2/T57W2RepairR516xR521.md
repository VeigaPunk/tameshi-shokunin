# T57W2RepairR516xR521 — repair of ledger rows R51.6 and R52.1 (C1 amended counter)

Base `5e3569969b532310d2b8a3d130901757a3df356b`. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Ledger edited only in scratch: the replacement rows are in `rows.json` beside this report; the L1 installs them with `patch-ledger.py`. No lane file was edited. No tool was installed or upgraded.

## Result

| id | status (base → repaired) | commit | evidence | dry-run fault line | repaired |
|---|---|---|---|---|---|
| R51.6 | open → open (kept) | none | round-51.md 5-7 (keyed `## Gate`), 12-12 (non-keyed) | none (was `key-miss`) | yes |
| R52.1 | fixed → fixed (kept) | e98044a → 441c26b | `.ufo/evidence/round-54/deciding-run.sh` 2-2 (keyed `deciding-run.sh`), `.ufo/evidence/round-54/after/c1.stdout` 5-5 (non-keyed) | none (was `key-miss`) | yes, with a commit-field change (below) |

Neither row is unrepairable. Neither status changed.

## R51.6 — `## Gate` completeness (open)

- Item (defects.json): list rejected candidates with reasons in the round-51 lesson's `## Gate` section, not only admits and touched rows.
- Why `key-miss` before: the old evidence (lines 7, 28, 62) carries none of `## Gate`, `rejected candidates`, `LEARNING` as a whole token.
- New evidence: `corpus/lessons/round-51.md` lines 5-7 (`## Gate` header plus the rows-opened sentence) carry the keyed token; lines 12-12 (rows touched) show the section's scope.
- Status check (kept `open`): the lane has no rejected-candidate list in the Gate section. Sweep run at base:
  - `git show 5e35699:corpus/lessons/round-51.md | grep -c -i reject` → `0`.
  - `git grep -c 'Candidates-rejected' 5e35699` → 0 hits.
  - The staged patch (stage/corpus/lessons/round-51.md, per the row's fix_note) is not landed.
- Note corrected: the old note said rejected candidates "sit in the C3 section and Attempt 3 section". The grep above contradicts that, so the claim is withdrawn in the replacement note. Status is not affected.
- Open planning check: the L1's dry-run regenerates `**Planned (round 58)**` from open rows, so R51.6 stays planned (`open_unplanned=0`).

## R52.1 — coldread re-key debt (fixed)

- Item: 19 sections lost credit at the tip; re-run the frozen re-key/deciding pipeline per `.ufo/evidence/round-52/deciding-run.sh`, or record an honest stop.
- Why `key-miss` before: the old evidence was two JSON lines from `.ufo/evidence/round-21/coldread/ledger.json` with none of `deciding-run.sh`, `Read18`, `re-key debt`, `honest stop` as a token.
- Sweep for a counter-admissible commit (command outputs in `T57W2RepairR516xR521-receipts/sweep.txt`):
  - `git log --grep=R52\.1 c1d49d76..5e35699` → no commit names the item.
  - Commits after routing (`c1d49d76`) that add or modify a `deciding-run.sh`: `cf87276`, `441c26b`, `19c7558`, `097985c`, `077d431`, `4f7a704`, `631cd64`, `c3e2ca9`, `21eb3c6`. The counter's tie route for this item is only through the basename `deciding-run.sh`, which is in the item text.
  - `e98044a` (the row's old commit): ancestor of base, not an ancestor of the routed commit, but touches only round-21 `ledger.json` and `rekey-r53-*` traces, which carry no key and no item id. The counter cannot admit it.
- Chosen: `441c26b` introduced `.ufo/evidence/round-54/deciding-run.sh`, the round-54 frozen re-key/deciding pipeline the item names. Keyed evidence is its header line 2: `# Round-54 deciding run. Usage: deciding-run.sh LANE REV FREEZE OUTDIR`.
- Restoring run: `4fe57df` (`after/c1.stdout` line 5: `credited=64 lost=0 ... C1_R54_PASS=true` at `c21081008adb`). Its paths carry no item key or id, so the counter cannot admit it. It is listed as non-keyed corroboration only.
- Status check (kept `fixed`), run at base `5e35699` in scratch:
  - `coldread-precheck.sh` floor `d33053f7` (credited 57) → cand `5e35699`: `COLDREAD_PRECHECK floor=d33053f7552d floor_credited=57 cand=5e3569969b53 cand_credited=64 lost=0 ok`, exit 0.
  - round-21 selector `measure.py --rev 5e35699`: `credited: 64`, `calibration_restraint_score: 8`.
  - Receipts: `T57W2RepairR516xR521-receipts/coldread-precheck-base.out`, `round21-measure-base.out`.

## Dry runs (scratch clone; L1 scratch path `…/tameshi-r57/L1-dry` as the driver writes it)

Before (L1's `dry-c1-explain.txt`, unpatched):
```
EXPLAIN key-miss R51.6
EXPLAIN key-miss R52.1
C1_R57_TERMS: … key_miss=8 … total=21 …
C1_R57: … rows=51/51 agree=31/51 … total=21 C1_R57_PASS=false
```

After, patched (`patch-ledger.py` then `LEDGER=… dry-c1.sh 200`), two runs at different scratch revs:
```
(no EXPLAIN line mentions R51.6 or R52.1)
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=4 key_miss=6 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=65b978ec712d rows=51/51 agree=33/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=19 C1_R57_PASS=false
C1_R57: self=63a88c257490 rev=8976d6cbc46c rows=51/51 agree=33/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=19 C1_R57_PASS=false
```

Net: `key_miss` 8 → 6, `agree` 31 → 33, `total` 21 → 19. The remaining 19 faults are other rows and the panel pin, outside this item. `C1_R57_PASS=false` is unchanged by this item.

## Findings for the L1

1. Counter limit (not repaired here): the tie rule admits a fix only through a commit whose path or message carries the item id or a basename in the item text. For R52.1 that makes a pipeline-introduction commit the only admissible carrier. The restoring receipts (`4fe57df`) cannot be cited as keyed evidence. Semantic support is not visible to the counter; the row's note says so.
2. Row change (not status): R52.1 `commit` moves `e98044a` → `441c26b`. Loud on purpose: a commit change is a row change, not a repair of the defect itself.
3. Note correction (not status): R51.6's note location claim for rejected candidates was unsupported; corrected.
4. Scratch: `dry-c1.sh` uses a fixed path `…/tameshi-r57/L1-dry` and removes it on exit. My two runs did not collide with any sibling that I could see, but a concurrent run would share that path.

## Checks the L1 should run

- `bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/dry-c1.sh 80` after installing `rows.json` through `patch-ledger.py`; expect no EXPLAIN line for R51.6 or R52.1.
- Nothing else. The status checks above are already run at base.

## Tools

None installed or upgraded. Scratch removed on exit.
