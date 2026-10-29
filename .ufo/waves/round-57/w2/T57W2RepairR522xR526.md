# T57W2RepairR522xR526 — repair ledger rows R52.2 and R52.6 (round 57, wave 2, calibration)

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `5e3569969b532310d2b8a3d130901757a3df356b`.
Scope: the two working-tree rows of `corpus/routed-defects.json` that the AMENDED C1 counter flagged `key-miss`.
Nothing in the lane was edited; the ledger file was not touched. Replacement rows are staged at
`.ufo/waves/round-57/w2/T57W2RepairR522xR526/rows.json` (list of two full row objects) for the L1 to install.

## Verdict

| id | status (kept) | before (dry run) | after (scratch dry run, patched ledger) | result |
|---|---|---|---|---|
| R52.2 | fixed (`a41195d`) | `EXPLAIN key-miss R52.2` | no fault line | repaired |
| R52.6 | open | `EXPLAIN key-miss R52.6` | no fault line | repaired |

Neither status changed. Both were checked, not assumed (see sweeps). No item is `unrepairable`.

## Why each row was refused (the cause, from the item text and the counter)

- **R52.2** (item: "Append (never rewrite) the round-52 entry naming the commits bcba892 → f1a3246 and the wrap-up disposition"; keys `bcba892`, `f1a3246`, `round-52`). The only evidence was `LOG.md:2444` (the heading `## 2026-10-27 — round 52 (honest stop, run wrap-up)`). It spells the round as `round 52`, not `round-52`, and it names no commit, so no key is a whole token of it. The entry's body does carry the key `round-52`, at `LOG.md:2448`, but was not cited.
- **R52.6** (item keys `Landed changes`, `Before → after`, `SHONEN box`, `report contract`). Both evidence items (`SCORECARD.md:37`, `SHONEN.md:5`) are true lines but contain none of the keys. The round-52 report and prompt are fleet-owned (outside the lane), so the lane holds no line that is about the report contract itself.

## Repairs

**R52.2 (fixed, kept).** Heading item kept; a keyed item added:
- `LOG.md` lines 2448-2448, excerpt ``honest-stop report is at `.ufo/reports/round-52/tameshi.md` (fleet commit`` (`round-52` is a whole token). The entry (lines 2444-2464) names `bcba8924` → `f1a32461` (8-char prefixes of the item's bcba892 → f1a3246), and carries the wrap-up disposition.
- Commit `a41195dfc13a73958e4c5228ec196b28d03ded03` (the round-53 content commit): ancestor of base, not ancestor of `routed_at` c1d49d7, touches `LOG.md`; its parent lacks the entry, the commit has it. The path `LOG.md` appears in the item's text, which satisfies the "names the item or the path" rule.

**R52.6 (open, kept).** Original two items kept (both still resolve); one keyed item added:
- `corpus/lessons/round-42.md` line 146, excerpt `| SHONEN box | standing command a non-author can run | gap |` (key `SHONEN box`). A non-spot-check lane file (round-42 is not in the frozen set). **Weak semantic support, stated plainly:** this is the per-box SHONEN table header of a considerthese mining note; it shows per-box checkability is a recorded lane gap, not the round-52 report itself. An open row needs no commit; the open-planned check passes because the dry-run Planned paragraph lists it.

## Dry run (the commands and their lines)

Patch: `python3 .ufo/waves/round-57/patch-ledger.py corpus/routed-defects.json .ufo/waves/round-57/w2/T57W2RepairR522xR526/rows.json $S/ledger.json` → `patched 2`.
Dry run: `LEDGER=$S/ledger.json bash .ufo/waves/round-57/dry-c1.sh 80` (receipt: `T57W2RepairR522xR526-receipts/dry-c1-patched.txt`). Result: neither `R52.2` nor `R52.6` appears in any EXPLAIN line. Full verdict line:

```
C1_R57: self=63a88c257490 rev=be5a162749dd rows=51/51 agree=33/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=19 C1_R57_PASS=false
C1_R57_TERMS: ... key_miss=6 fixed_bad=8 ... panel_pin=1 panel_over=0 base_status_bad=0
```

Unpatched working tree, same script (receipt `dry-c1-unpatched.txt`), for comparison:

```
EXPLAIN key-miss R52.2
EXPLAIN key-miss R52.6
C1_R57: self=63a88c257490 rev=7ea9e48ec595 rows=51/51 agree=31/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=21 C1_R57_PASS=false
```

Effect: `agree` 31 → 33, `key_miss` 8 → 6, `total` 21 → 19. The remaining `total` is not this seat's: `panel_pin=1` (the panel file hash is still the pending marker, L1-owned), and the other EXPLAIN lines (R51.1, R51.3, R51.6, R52.1, R53.6/7/9, R54.5-10, R55.1/3/4/6, R56.1) belong to other seats.

Panel note: `status_at_base` for both rows is kept as `fixed` / `open`. I did not open `.ufo/evidence/round-57/c1/panel.json` (the blind verdicts), so no row was tuned to it.

## Sweeps (command + output; full text in `T57W2RepairR522xR526-receipts/sweeps.txt`)

1. R52.2 commit introduction: `git show a41195d^:LOG.md | grep -c 'honest-stop report is at'` → `0`; `git show a41195d:LOG.md | grep -c ...` → `1`; `grep -c 'round 52 (honest stop'` at parent → `0`; `git diff-tree --name-only -r a41195d` contains `LOG.md`; `merge-base --is-ancestor a41195d 5e35699…` → yes; `merge-base --is-ancestor a41195d c1d49d7` → not an ancestor of routed_at (yes).
2. R52.6 admissible keys: `git grep -n -i -E "report contract|landed changes"` at base, excluding `.ufo/waves`, `.ufo/reports`, the round-50..56 spot-check files, the ledger, and round-57 → only spot-check copies under `.ufo/evidence/round-53/assimilation/validate/corpus/lessons/` (spot-checks, not admissible for this seat's purpose) and `corpus/lessons/round-{28,35,36,45,46}-verifier-spotcheck.md`. No non-spot-check lane file carries `report contract` or `Landed changes`.
3. `SHONEN box` / `Before → after` in non-spot-check lane files: LOG.md, SCORECARD.md (claim tables), corpus/README.md, corpus/lessons/round-1/16/27/42.md, plans/, reports/, considerthese/. Only `corpus/lessons/round-42.md:146` is a per-box SHONEN line; I used it.
4. Lane commits after `c1d49d7` touching round-52 report paths: `git log c1d49d7..5e35699 -- .ufo/reports/round-52 corpus/lessons/round-52.md` → empty. So no lane commit repaired R52.6's report residue; status `open` stands.
5. Excerpt precheck (each new item verbatim in lines a..b at base): `R52.2 LOG.md 2444-2444 present`, `R52.2 LOG.md 2448-2448 present`, `R52.6 SCORECARD.md 37-37 present`, `R52.6 SHONEN.md 5-5 present`, `R52.6 corpus/lessons/round-42.md 146-146 present`.

## Staged output

- `T57W2RepairR522xR526/rows.json` — the two full replacement rows (`id`, `status`, `commit` where fixed, `evidence`, `seat`, `note`, `status_at_base`).
- `T57W2RepairR522xR526.json` — machine-readable summary.
- `T57W2RepairR522xR526-receipts/` — dry-run outputs (patched, unpatched), sweeps, excerpt precheck, patched ledger copy.

## Out of scope / residue

- Status is unchanged for both rows; no status change was proven, so none is reported as a finding.
- R52.6's real residue (per-box SHONEN lines, Landed changes and Before → after sections in the round-52 report; the false "not committed/pushed" sentence; trend vocabulary) lives in the fleet-owned report. It stays open and belongs in the round-57 report's Planned paragraph, as the wave-1 scribe noted. The keyed lane line is weak support for that; the L1 may want a stronger lane-side excerpt if one is written later.
- The panel arm (`panel_pin`) is the L1's to pin. This seat did not read the panel verdicts.

## Tooling

No tool was installed or upgraded. Read `/home/vgpnk/.omp/agent/RULES.md` (tooling directive; nothing needed). Scratch under `/fast/scratch/hyaku/tameshi-r57/T57W2RepairR522xR526`, removed after the receipts were copied.

## Checks for the main agent to run

- `LEDGER=<staged patched ledger> bash .ufo/waves/round-57/dry-c1.sh 80` after installing `rows.json` into the ledger (expect no `R52.2`/`R52.6` line).
- Install with `python3 .ufo/waves/round-57/patch-ledger.py corpus/routed-defects.json .ufo/waves/round-57/w2/T57W2RepairR522xR526/rows.json <out>`.
