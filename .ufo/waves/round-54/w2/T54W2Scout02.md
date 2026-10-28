# T54W2Scout02 — delta-debugging entry, round-55 planned list

Survey only. Nothing under the lane or `/home/vgpnk/Projects/shokuknow` was edited. No tool was installed. Registry and QUALITY lines below are the bytes at C1 `99c3bc88d704566197783f66b211ee0a830e0330` (`git diff --stat C1 HEAD` is empty for `corpus/SOURCES.md`, `corpus/QUALITY.md`, and `corpus/knowledge/delta-debugging-minimization-contract.md`).

Not a round-55 assimilation candidate. Round 50 already admitted an edited copy of this entry and refused the staged row.

## Staged row ids

One id. The staged file's only `source:` line is line 2:

`source: S167 — https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf — §I Introduction (ddmin definition and the 896-line HTML case study), p. 183-184`

The body cites only S167. `MERGE-REPORT.md:35` lists the file as `new-file`, round2. `MERGE-REPORT.json` sets `collides_with_existing: false` (packaging-time; stale — the lane now holds the path).

The package append row is the same id, one 11-cell row at `merge/tameshi/SOURCES.append.md:21`. Its `used-by` cell names two paths: this entry and `corpus/knowledge/repeat-control-measured-n3.md`. That second file also has `source: S167` (its line 3). Same staged row, not a second id. The "rows the lane already holds" table (`MERGE-REPORT.md:118-124`) does not list S167.

## Rows an adoption would append

None.

- C1 `corpus/SOURCES.md` has no `| S167 |` row (`grep -c` = 0) and one `| S271 |` row. S271 is this URL, mined 2026-10-26, used by `corpus/knowledge/delta-debugging-minimization-contract.md` and `corpus/knowledge/fixture-shrinking-pilot.md`. Round 50's note (`corpus/SOURCES.md:506`) records staged S167 as re-pointed by document to S271 and not reused.
- C1's last registry note: next unused id **S280**; staged ids S161–S255 stay reserved. Minting S167, or a second row at S280 for the same URL, is not an append this entry needs.
- The landed file is the round-50 edit (`source: S271` and `source: S024`, `verified-at: 2026-10-26`), not the staged bytes. Copying the staged file onto `corpus/knowledge/delta-debugging-minimization-contract.md` would overwrite that landing. `repeat-control-measured-n3.md` is not in the lane; it is a different entry that shares S167, not a row this adoption adds.

## First QUALITY-bar failure

**QUALITY 2** (`corpus/QUALITY.md:4-5` at C1): every claim carries a measured anchor. The staged text fails it before any later criterion.

QUALITY 1 passes: the statements are checkable against the PDF. The earliest failing claim is the header locator plus the cost sentence that an adoption would also append in S167's teaches cell.

Quoted staged teaches cell (`SOURCES.append.md:21`): "a failing test case is reduced by successive testing until removing any single input entity would make the failure disappear, and the reduction is itself a measured cost (139 automated test runs, 35 minutes on a 500 MHz PC)". Anchor on that row: "§I Introduction (ddmin definition and the 896-line HTML case study), p. 183-184".

Quoted staged entry (`delta-debugging-minimization-contract.md:15-17`): "it simplified 896 lines of HTML to the single line that caused the failure. The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC" (S167, §Abstract/§I).

What the carrier actually says (reading-order `pdftotext` of the pinned PDF, sha256 `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`, 247738 bytes, 17 pages):

- The 139 sentence occurs once, in the Abstract: "The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC." It is the case study's total, not §I's figure for the 896-line reduction.
- §I: "After 57 tests, the original 896-line HTML input is reduced to the minimal failing test case".
- §IV-B Fig. 12: "After 57 test runs, the ddmin algorithm minimizes the original 896 lines to a 1-line input".
- §IV-B Fig. 11: "After 82 test runs (or 21 minutes), only 3 out of 95 user actions are left".

`82 + 57 = 139` is an inference the paper does not state. The row's anchor does not contain 139. The entry's bullet places the Abstract's total in the same quotation as the 896-line reduction and cites §I for a sentence §I does not contain.

The same criterion fails the page anchor on line 2. `pdfinfo` reports 17 pages. `grep -c '183'` on the flattened extract is 0. Journal pages 183–184 are not on this carrier. The live URL fetched 2026-10-28 is byte-identical to the snapshot (`cmp`), so this is not snapshot drift.

The staged recheck is the same failure: `grep -c 'minimal test case'` on the PDF bytes prints 0 (live and snapshot). The string is in the text layer, not in the compressed file `grep` sees. Round 50 already recorded the refusal in `corpus/lessons/round-50.md:62-67` and in the landed entry's "Refused from the package" section (`corpus/knowledge/delta-debugging-minimization-contract.md:46-50`).

## Later failures, not first

- QUALITY 10 clause 2 (`corpus/QUALITY.md:27-30`): `source: S167` names no lane row. Fixable only by citing S271, which is why an adoption appends nothing. It is a later criterion than 2.
- QUALITY 9: the package ships no snapshot. The lane already holds one at `.ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf`.
- QUALITY 34: a bare page into a file the lane does not own. The section name §I does resolve; the page does not.
- Dangling `CANNOT-ANSWER.md` §2 (staged lines 43-45). No such file in the lane corpus or in `merge/tameshi/`.
- Witness direction (staged lines 26-28): "the entity whose removal restores the failure". The quoted §I sentence says removal makes the failure disappear. The landed entry corrects this. Not the first bar failure.

## Commands

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc88d704566197783f66b211ee0a830e0330:corpus/SOURCES.md | grep -c '| S167 |'   # 0
git -C ... show C1:corpus/SOURCES.md | grep -c '| S271 |'   # 1
git -C ... show C1:corpus/SOURCES.md | grep 'Next unused id:' | tail -1   # S280
pdfinfo <snapshot>    # Pages: 17; 247738 bytes
sha256sum <snapshot>  # 7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa
grep -c 'minimal test case' <snapshot>   # 0
curl -fsSL --max-time 25 -o live.pdf <url> && cmp live.pdf <snapshot>   # identical; live grep -c = 0
pdftotext <snapshot> - | tr -s ' \n' ' ' | grep -o '<sentence>'   # 139 sentence ×1, After 57 tests ×1, After 57 test runs…896 lines ×1, After 82 test runs ×1, '183' ×0
```

## Opened

- `/home/vgpnk/Projects/shokuknow/merge/tameshi/MERGE-REPORT.md` (line 35; already-held table 114-124; adopt checklist)
- `/home/vgpnk/Projects/shokuknow/merge/tameshi/MERGE-REPORT.json` (entry at lines 94-104)
- `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/delta-debugging-minimization-contract.md` (whole file, 47 lines)
- `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:21` (S167, verbatim)
- `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/repeat-control-measured-n3.md:2-3` (second `source: S167`)
- Lane at C1: `corpus/QUALITY.md:4-5` and `:27-30`, `corpus/SOURCES.md` S271 row and the S280 note, `corpus/knowledge/delta-debugging-minimization-contract.md:46-50`, `corpus/lessons/round-50.md:46-67`
- Carrier: `.ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf` and a fresh fetch of the same URL

## Unresolved

None that change the three answers. The 82+57 reading of 139 is an inference; the paper never states the sum. Confidence: high on the row id, the empty append, and the QUALITY 2 failure.
