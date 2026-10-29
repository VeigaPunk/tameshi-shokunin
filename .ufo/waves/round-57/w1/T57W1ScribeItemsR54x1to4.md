# T57W1ScribeItemsR54x1to4 — ledger rows R54.1–R54.4

seat: T57W1ScribeItemsR54x1to4 (leaf, wave 1 of round 57, calibration)
lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin
base (lane HEAD, verified): `5e3569969b532310d2b8a3d130901757a3df356b`
routed_at (commit that added the round-54 spot-check, `git log --diff-filter=A`): `650987a0d6fc285b37f0f9e63a3aae864af9cd5a`
fix commit used for three rows: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (round-55 C0, "the round-54 record corrections")

## Dispositions

| id | status | commit | evidence (lane paths, base lines) | residual outside lane | fixable triage |
|---|---|---|---|---|---|
| R54.1 false positive-control claim | fixed | 9cf0146 | `corpus/QUALITY.md:1602-1604`; `corpus/lessons/round-54.md:105`; `SCORECARD.md:2636-2637` | fleet report `.ufo/reports/round-54/tameshi.md:162` still reads "proven live by the phase-B positive control" | n/a (fixed); residual not lane-fixable |
| R54.2 three freeze pointers | fixed | 9cf0146 | `SCORECARD.md:2568-2569`; `SCORECARD.md:2645-2646` | fleet report `:157` still names `097985c1` | n/a (fixed); residual not lane-fixable |
| R54.3 `total=14` quoted | fixed | 9cf0146 | `SCORECARD.md:2585`; `SCORECARD.md:2650` | none | n/a (fixed) |
| R54.4 stale c2 digest in the report | declined | — | `.ufo/evidence/round-54/freeze.json:9`; `SCORECARD.md:2655-2656` | fleet report `:122` still cites `49280fe5…` | not-fixable by a lane seat (fleet-owned file) |

No item is `open`, so no staged patch is needed and no cold-read input is touched. Nothing was staged under `stage/`.

### Basis per row

- **R54.1 — fixed.** At `650987a` the lesson said the control was "proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`)", QUALITY 105 quoted `rekeyed=7/7` as the control's result, and SCORECARD carried `CTL_POS_c1 true`. At base all three lane sites now record `CTL_MISMATCH … expected=true actual=false`, "never fired", and ER-R54-1. `9cf0146` touches all three paths. The three excerpts are absent at `650987a` (the ER-R54-1 block did not exist there) and present at base.
- **R54.2 — fixed.** `650987a` had no `one freeze pointer` text and no `ER-R54-` entries (both counted 0). At base the round standing text and ER-R54-2 name one pointer, `077d431e`. The fleet report line `:157` (`097985c1`) is outside the lane tree.
- **R54.3 — fixed.** `650987a` SCORECARD carried `sources=0 total=14` in the C2 claim row. At base the row reads `total=13`, and ER-R54-3 records "Old: `total=14` … Corrected: `total=13`." (The `total=14` in ER-R54-3 is the record of the old value, which is correct.)
- **R54.4 — declined.** The only surface still carrying the stale digest is the fleet report, `.ufo/reports/round-54/tameshi.md` at fleet `fcb8d8db`, line 122 (`49280fe5…` for c2). That file is not in the lane tree (`lane has no .ufo/reports/round-54/tameshi.md at base`) and the fleet file is unchanged to fleet HEAD. A lane seat cannot edit it. The lane's pinned value is `8528ee85…` in `freeze.json`, and the correction is ER-R54-4. Reason text in the row is ≥40 chars.

## Judgement calls for the L1

1. **R54.1 and R54.2 are `fixed` on lane-tree surfaces only.** Their fleet-report copies still hold the defective text (report `:162` and `:157`). I took the counter's rule that a row agrees with the lane tree. If the L1 wants the report residue to block `fixed`, both rows become `declined` with a reason, and the report would need an operator-owned fleet correction.
2. **R54.4 as `declined`** rests entirely on the fleet-ownership reason. The alternative would be `fixed` on the ER-R54-4 correction, but that would overstate what the lane changed, because the cited surface (the report) is unchanged.
3. **Floors.** All three `fixed` commits are ancestors of base, so `fixed_this_round` contributes 0 from these rows. The round-50 floors (`fixed >= 20`, `this_round >= 5`) must be met by other seats' rows.
4. **Line spans are at base `5e3569969b…`.** If the L1 lands a commit that moves lines of `SCORECARD.md`, `corpus/QUALITY.md` or `corpus/lessons/round-54.md` before the content commit, the `lines` fields must be re-derived with `verify-rows.py` (its `locate` resolver reruns at any `BASE`). Excerpts are resolved by content, so a line shift alone does not fail the row.
5. **Counter inheritance (observed, not exercised).** The round-50 `planned_ids` regex is `\bR4\d\.\d+\b`, so an `open` row for an `R5x` id can never be `planned` under the round-50 bytes. No row here is `open`, so the defect does not bite this seat. Any open R5x row from another seat would fail `open_unplanned` regardless of the Planned paragraph. The L1 should check the round-57 counter for this before scoring.

## Verification (executed, not inferred)

- `verify-rows.py` (receipts dir) imports `corpus`-independent resolver functions from `.ufo/evidence/round-50/c1/measure.py` (`check_evidence`, `has_key`, `is_ancestor`, `touched`, `show`, `norm`, `HEX40`, `ACK_WORDS`, `measure`); the round-50 file is not edited. Spot-check exclusion covers every `corpus/lessons/round-N-verifier-spotcheck.md` at base (rounds 40–56).
  - Per-row resolver checks: R54.1 ok (3 keyed items), R54.2 ok (2), R54.3 ok (2), R54.4 ok (2). `all_rows_resolver_ok: true`.
  - End-to-end: a scratch clone at base with a fixture ledger holding exactly these four rows, scored by `measure()` with `base=5e3569969b…`, the spot-check as the defect file, and `routed_at=650987a`: `counts` all 0, `stat fixed=3 declined=1 open=0 fixed_this_round=0`, `total=0`, `rows=4`, `notes=[]`.
  - Output: `.ufo/waves/round-57/w1/T57W1ScribeItemsR54x1to4-receipts/verify-rows.stdout`.
- Negative controls (same script, mutated rows, output in this session):
  - R54.3 with `commit=650987a` (ancestor of routed_at): `fixed_bad=1`, notes `fixed-commit` and `fixed-not-new`, `total=1`.
  - R54.4 with a 9-word reason: `declined_bad=1`, `total=1`.
  - Control with an excerpt that quotes the old wording: passes freshness because that text first appears at `9cf0146`. This shows freshness is judged against `routed_at` content, not against a semantic reading.
- Command receipts: `.ufo/waves/round-57/w1/T57W1ScribeItemsR54x1to4-receipts/command-receipts.txt` (base/tip hashes, routed_at, fix ancestry, fix commit file list, `grep -c` of stale phrases at `650987a` = 0, fleet report lines 122/157/162, lane record sites at base, R54 ids in Planned paragraphs = none).
- Ledger schema: every row has `id, status, evidence[{path,lines,excerpt}], commit (fixed) | reason (declined), seat, note`, plus `keys` and `verdict_basis` in `rows.json` only. The L1 drops `keys` and `verdict_basis` when merging into `corpus/routed-defects.json`.

## Files

- Rows: `.ufo/waves/round-57/w1/T57W1ScribeItemsR54x1to4/rows.json` (4 rows, with `keys` and `verdict_basis`).
- Machine-readable disposition: `.ufo/waves/round-57/w1/T57W1ScribeItemsR54x1to4.json`.
- Receipts: `.ufo/waves/round-57/w1/T57W1ScribeItemsR54x1to4-receipts/` (`verify-rows.py`, `verify-rows.stdout`, `command-receipts.txt`).
- No lane production file edited. No stage patch needed (no `open` row). No installs or upgrades; no PATH directory touched.
