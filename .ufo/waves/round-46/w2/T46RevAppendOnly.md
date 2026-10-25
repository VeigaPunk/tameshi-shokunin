seat: T46RevAppendOnly
item: verify the SCORECARD.md edit (and LOG/QUALITY/SOURCES/README/PROVINCE edits) at content rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 is append-only over base 683eedde3a50441c34d85a22f5fd5346f8b1ec6d and that the appended SCORECARD tables are real multi-row tables the C1 counter parses.

## Findings

### F1 — SCORECARD.md is a byte-prefix append; zero old lines changed (INFO)

Command (run for each of the six files):
`python3 -c 'new.startswith(base)'` over `git show <base>:<f>` vs `git show <rev>:<f>`:

- `SCORECARD.md`: base_len=207916 new_len=225496 prefix=True (+17580 appended bytes)
- `LOG.md`: base_len=176694 new_len=179671 prefix=True
- `corpus/QUALITY.md`: base_len=80492 new_len=84800 prefix=True
- `corpus/README.md`: base_len=55700 new_len=58069 prefix=True
- `PROVINCE.md`: base_len=6334 new_len=7728 prefix=True
- `corpus/SOURCES.md`: prefix=False — see F4.

`git -C LANE diff --stat <base> <rev> -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md corpus/README.md PROVINCE.md` → `192 insertions(+)` and no deletions line; `git diff -U0 ... | grep -c '^-[^-]'` → `0` for the five prefix files and `0` for SOURCES.md. No earlier line changed anywhere in the six files.

Boundary safety: base SCORECARD.md ends with `... | 45 |\n` (last line of a table block ending at line 2164); the appended bytes begin with `\n## Round 46 — ...`, so the base's final table is not extended by the appended header. No pipe-block straddles the boundary (verified by block enumeration).

### F2 — All four appended SCORECARD pipe-blocks are real multi-row tables (INFO)

Using the counter's own `strip_hidden`/`tables`/`cells_of` (`measure.py` loaded via importlib) on `git show <rev>:SCORECARD.md` (69 pipe-blocks total, 65 at base):

- lines 2174–2194 (21 lines): `Capability` table — header 4 cells, sep `|---|---|---|---|`, 19 data rows, every row 4 cells.
- lines 2196–2200 (5 lines): `axis` table (`Axis | Score (0–10) | ...`) — header 5 cells, sep 5 cols, 3 data rows (depth, calibration, freshness), every row 5 cells.
- lines 2204–2208 (5 lines): `Claim | Axis | Before | After`-family table — header 8 cells, sep 8 cols, 3 data rows, every row 8 cells; classified `skipped` by `last_rows` (header[0]≠Capability, header[1] not 'Score…') — it does not feed any statement.
- lines 2222–2226 (5 lines): `Capability` table — header 4 cells, sep 4 cols, 3 data rows (standing-statement counter; declared-mutant driver with neutral controls; no-harm-at-base gate and seat-name collision gate), every row 4 cells.

All separators contain only `|-: ` characters. None of the appended blocks is a single-line pipe block of the kind CritC1Control flagged at base lines 1851, 1993, 2020, 2081, 2146, 2164 — those six are still single-line blocks in rev (verified: each is a `sources-registry`-first-cell 1-line block, classified `skipped`, parser ignores them) and none lies in the appended region (2165+).

### F3 — last_rows / statement resolution (INFO)

`last_rows` over rev yields 25 keys (21 at base). New keys: `('axis','freshness')`, `('cap','standing-statement counter')`, `('cap','declared-mutant driver with neutral controls')`, `('cap','no-harm-at-base gate and seat-name collision gate')`. Restated keys (expected re-statement): `('axis','depth')`, `('axis','calibration')` cells differ from base. All 22 frozen statements (sha256 of statements.json at rev = `a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9`, matches the contract pin) resolve: `rows.get((kind,id))` non-None for 22/22 and `claim_of` non-None for 22/22 — zero unparsed at the structural level.

### F4 — corpus/SOURCES.md is a pure mid-file insertion, not a byte prefix (INFO)

`git show` comparison: base 468 lines, new 471 lines, common prefix 132 lines, common suffix 336 lines, inserted 3 lines at new-file lines 133–135 (the S258/S259/S260 rows), placed contiguously after the `| S257 |` row inside the existing registry table and before the blank line + `## Paths`. `git diff -U0` shows zero `-` lines: no old line was edited or deleted, and no re-ordering occurred. The item's prefix check listed SOURCES.md among "each must be a byte prefix, or list the edited old lines": there are no edited old lines — this is a clean insertion (the only structurally correct way to add contiguous registry rows). It does not affect C1's `append_only`, which pins SCORECARD.md only, and the re-run counter (F6) agrees: append_only=1.

### F5 — No unescaped `|` inside data cells (INFO)

Every data row in all four appended tables has cell count == header count (F2), so no cell was split by a stray `|`. `\|` (escaped pipe) count in the appended region: 0. A `|` character outside a table line would also be harmless to this parser (`tables()` only accepts lines starting with `|`), but none was found misplaced: all appended `|`-leading lines belong to the four enumerated blocks.

### F6 — Ground truth: counter re-run at the content rev (observed, not a verdict)

`python3 .ufo/evidence/round-46/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 --base 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --work /tmp/tameshi-r46-T46RevAppendOnly/c1work` (empty scratch dir; ~697s):

```
C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=0 unobservable=0 append_only=1 total=0 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C1_R46_PASS=true
```

All 22 statements MATCH (19 cap rows incl. sha-pinned claims, axis/depth=9, axis/calibration=6, axis/freshness=9). Reported as observed; the deciding run is the L1's.

## Residual risk

None identified in scope. The appended section is byte-appended, parse-clean, and every statement row resolves and matches; SOURCES.md's mid-file insertion is correct behavior, not a defect. Unrun: `--selftest` of the counter (not this item); other waves' counters not run.
