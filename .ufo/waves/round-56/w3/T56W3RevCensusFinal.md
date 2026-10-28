# T56W3RevCensusFinal — census at PIN (2f5512a8ab0771fb2eee463ec16db359174f5edd)

Scope: fleet census of `corpus/SOURCES.md` at PIN, comparison with base (981c5e8b), shape check of the two new rows, and the wave-1 shape harness run against synthetic rows. Read-only: no lane, frozen, or fleet-root file was written. Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W3RevCensusFinal` (fixtures kept there; scratch removed on exit).

Preconditions verified: `git rev-parse HEAD` = PIN; base is an ancestor of PIN; `corpus/SOURCES.md` in the worktree is byte-identical to `PIN:corpus/SOURCES.md` (`cmp`). Installs: none.

## 1. Census at PIN — exit 0

Command:
```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```
- exit: **0**
- trailer (last line): `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`
- E-codes: **none**
- W-lines: **16** = 15 × W04 (duplicate URL across scopes) + 1 × W01 (S101 tier-C mined). Warnings do not change status.

Census command:
```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi
```
- exit 0; `tameshi rows 142`; tier.A 127 · tier.B 12 · tier.C 3 · tier.invalid 0; status.mined 114 · status.queued 21 · status.rejected 7 · status.invalid 0; missing 0.

Row count at PIN: 142 (`grep -cE '^ {0,3}\| S[0-9]{3,} \|'` = 142). Base: 140.

## 2. Comparison with base (981c5e8b) — rows added

`git diff 981c5e8b..PIN -- corpus/SOURCES.md` adds exactly two registry rows and nothing else in the table:

| id | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|
| S281 | A | mined | 2026-10-28 | on-release | `corpus/knowledge/receipt-revision-binding.md` |
| S282 | A | rejected | 2026-10-28 | on-release | `—` |

Base census (`census --file <base registry>`): rows 140, tier.A 125, status.mined 113, status.rejected 6. Delta: +2 rows, +2 tier-A, +1 mined, +1 rejected — matches S281/S282 exactly. Warning set at base (file mode) and PIN is identical (16 W lines; `diff` shows no W-line change). No existing row was modified (`diff` shows only insertions at the registry tail and in the round notes).

Notes added in the same commit (outside the table, not counted by the census): a round-56 search note and a "Next unused id: S283" line.

## 3. New-row shape (S281, S282) — independently checked

Awk field split on `|` at PIN: S281 and S282 each have **11 cells** (NF=13) and **12 pipe characters** (leading, trailing, 10 interior separators), matching the harness's `pipes>12` threshold. No escaped `\|` (`grep -c '\\|'` over the registry = 0). No duplicate ids (`uniq -d` empty). Enums: status `mined` / `rejected` ∈ {queued, mined, rejected}; kind `spec`; tier `A`; recheck `on-release` (symbolic cadence, reported but never judged overdue). `opened` `2026-10-28` is a real ISO calendar date, not after today (2026-10-28, UTC). `used-by` for S281 is `corpus/knowledge/receipt-revision-binding.md` and exists at PIN (`git cat-file -e PIN:corpus/knowledge/receipt-revision-binding.md`; lane file present). S282 is rejected, so `—` is accepted (W02 thin-teaches not triggered).

Harness shape run at PIN:
```
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/census-after.sh --base 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 --label tameshi
```
- `CENSUS exit=0 rows=142`, `CENSUS_ROWS_SELFCHECK census=142 grep=142`, `CENSUS_SHAPE tameshi new_rows=2 findings=0`, `CENSUS_SHAPE_VERDICT pass=true new_rows=2 findings=0 rows_mismatch=false`.

## 4. Wave-1 shape harness against synthetic rows

Fixtures: copies of the PIN registry with one synthetic row inserted after S282. Each run:
```
bash .../round-56/census-after.sh --lane <lane> --root /home/vgpnk/Projects/shokunin --sources <fixture> --base 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 --label <n> --shape-only
```

| fixture | synthetic row | harness output | exit |
|---|---|---|---|
| syn10 | `| S283 | … | 2026-10-27 | 90d |` (10 cells) | `CENSUS_SHAPE S283 SHAPE_COLUMNS columns=10 want=11`; verdict `pass=false findings=1` | 1 — **refused** |
| esc | `… | cell a \| cell b | … | — |` (escaped pipe) | `CENSUS_SHAPE S284 SHAPE_PIPE escaped pipe (\|) in row`; `pass=false findings=1` | 1 — **refused** |
| pipe12 | 12 cells (extra literal pipe) | `CENSUS_SHAPE S286 SHAPE_PIPE literal pipes=13 want=12`; `pass=false findings=1` | 1 — **refused** |
| future | opened `2026-12-01` | `SHAPE_OPENED opened=2026-12-01 is in the future` | 1 — refused |
| watch | status `watch` | `SHAPE_STATUS status=watch` | 1 — refused |
| sect | row after `## Paths` | `SHAPE_SECTION row outside ## Registry section` | 1 — refused |
| ctrl | valid 11-cell row | `new_rows=3 findings=0`; `pass=true` | 0 — accepted (control) |

Verdict: the harness refuses both requested cases (10-column row and escaped-pipe row), with the cause named, and accepts a valid control row, so it is not refusing everything. Each other shape rule was exercised by one fixture. The `new_rows=3` in fixtures counts S281, S282 and the synthetic row; base ids are read from `base:corpus/SOURCES.md`.

## 5. Caveat found — `--file` mode resolves `used-by` against the fleet root

Running `sources-census.sh validate --root <fleet> --file <registry>` emits `E11 … missing used-by corpus/knowledge/...` for every row whose used-by lives in the lane (base file: many E11 lines, exit 1; PIN file: the same plus `S281 missing used-by corpus/knowledge/receipt-revision-binding.md`). This is a path-resolution artifact of `--file` (it checks paths under `--root`, the fleet root, not the lane). The canonical lane invocation (`validate … tameshi`) resolves used-by in the lane and returns exit 0 with zero E-codes. The deciding run should validate with the lane invocation, not `--file`. Census counts are unaffected (`--file` census gives the same 142 rows).

## 6. Findings

- No defect in the two added rows; 11 columns, enums, ISO date, used-by path all valid at PIN.
- The census gate (`validate tameshi`, exit 0, 142 rows) holds at PIN.
- Warnings are unchanged from base (16).
- Harness shape checks behave as specified on the two requested synthetic cases.
- Limitation: `--file` mode mis-resolves `used-by` (section 5); not a PIN defect.

## Reproduction

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi        # exit 0, trailer ok
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi          # tameshi rows 142
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/census-after.sh --base 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 --label tameshi   # CENSUS exit=0 rows=142; CENSUS_SHAPE_VERDICT pass=true
```
