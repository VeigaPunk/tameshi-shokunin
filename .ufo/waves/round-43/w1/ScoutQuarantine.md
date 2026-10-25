# ScoutQuarantine — round 43 wave 1 findings

Access date: 2026-10-25. Lane: tameshi-shokunin. Read-only seat: the register and every
campaign file were read, never written; the only file created is this report.

Question: re-derive this lane's slice of
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(the header/summary totals are stale — the data rows are the evidence).

## 1. The filter returns 17 tameshi rows: 14 `payload-absent` + 3 could-not-be-fetched

Exact command (item text), run verbatim:

```
awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Output, 17 lines, in register order:

```
 S105   `payload-absent`
 S109   `payload-absent`
 S110   `payload-absent`
 S118   `payload-absent`
 S119   `payload-absent`
 S124   `payload-absent`
 S126   `payload-absent`
 S129   `payload-absent`
 S131   `payload-absent`
 S132   `payload-absent`
 S137   `payload-absent`
 S140   `payload-absent`
 S141   `payload-absent`
 S143   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S123`   the cited source could not be fetched, so no quote was checked
 S134`   the cited source could not be fetched, so no quote was checked
```

Row count: **17**. Ids: **S105 S109 S110 S118 S119 S124 S126 S129 S131 S132 S137 S140 S141
S143** (payload-absent) and **S113 S123 S134** (could-not-be-fetched).

## 2. Family of each row, with register coordinates

| id | round | family | register location | cited source |
|---|---|---|---|---|
| S105 | round1 | `payload-absent` | `absent-defect-register.md:215` | https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html |
| S109 | round1 | `payload-absent` | `:216` | https://doi.org/10.21105/joss.01891 |
| S110 | round1 | `payload-absent` | `:217` | https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf |
| S118 | round1 | `payload-absent` | `:218` | https://zenn.dev/seckeyjp/articles/j-six-mutation-testing |
| S119 | round2 | `payload-absent` | `:219` | https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf |
| S124 | round2 | `payload-absent` | `:220` | https://github.com/VeigaPunk/tameshi-shokunin |
| S126 | round2 | `payload-absent` | `:221` | https://github.com/VeigaPunk/tameshi-shokunin |
| S129 | round3 | `payload-absent` | `:222` | https://www.t.kyoto-u.ac.jp/lib/ja/support/ieice |
| S131 | round3 | `payload-absent` | `:223` | https://github.com/VeigaPunk/tameshi-shokunin |
| S132 | round3 | `payload-absent` | `:224` | https://github.com/VeigaPunk/tameshi-shokunin |
| S137 | round4 | `payload-absent` | `:225` | https://github.com/VeigaPunk/tameshi-shokunin |
| S140 | round5 | `payload-absent` | `:226` | https://github.com/VeigaPunk/tameshi-shokunin |
| S141 | round5 | `payload-absent` | `:227` | https://github.com/VeigaPunk/tameshi-shokunin |
| S143 | round5 | `payload-absent` | `:228` | https://github.com/VeigaPunk/tameshi-shokunin |
| S113 | round1 | could-not-be-fetched | `:363` | https://doi.org/10.1145/3540250.3558911 |
| S123 | round2 | could-not-be-fetched | `:364` | https://doi.org/10.1109/TSE.2026.3685588 |
| S134 | round4 | could-not-be-fetched | `:365` | https://doi.org/10.1145/351240.351266 |

Per round: round1 = 5 (S105, S109, S110, S118 + S113), round2 = 4 (S119, S124, S126 + S123),
round3 = 3 (S129, S131, S132), round4 = 2 (S137 + S134), round5 = 3 (S140, S141, S143).

The 3 could-not-be-fetched rows are not a class token: the never-checked table has no class
column, so the awk's `$5` is the why-string. All three tameshi rows carry "the cited source
could not be fetched, so no quote was checked". **Zero** tameshi rows carry the other
why-family ("the gate block named no locator").

## 3. Independent corroboration — four ways, same 17 ids, same families

1. **Column parse instead of awk offsets.** A regex parse of the leading
   `| lane | round | id |` columns (so quoted text containing `|` cannot shift fields) yields
   14 payload-absent rows at `:215–:228` and 3 never-checked rows at `:363–:365`. Every
   register line with `` `tameshi` `` in column 2 is `215–228`, `240` (the by-lane totals row,
   correctly rejected because its `$3` is ` 14 `), and `363–365`. No tameshi row is missed and
   none is spurious.
2. **Census v5 derivation** (`quote-lint-full-v5.json`, the file the register names as its
   source). Tameshi has 16 ABSENT findings → 14 distinct rows (S132 and S141 carry 2 ABSENT
   findings each) and 3 `fetch-failed` rows, 0 `no-locator`. Same ids, same families.
3. **Census v4 derivation.** Same 17 ids and families. This matters because the two censuses
   disagree on the corpus-wide ABSENT count (v4 `absent: 325` vs v5 `absent: 324`), so a
   re-derivation is not stable on the summary figures but *is* stable on this lane's slice.
4. **Frozen-slice byte identity.** The fresh output is byte-identical to
   `tameshi-shokunin/.ufo/waves/round-42/assimilation/quarantine-slice`
   (`diff` clean, md5 `9f897205525c58ddd64c876ef45baf1f`, 583 B, 17 lines). It also matches
   `round-41/w1/ExecQuarantine.md` (`:10` 17 rows, `:44–:60` the per-row list) and
   `round-42/w1/ScoutQuarantine.md` verbatim.

## 4. What is actually stale in the register (derived, not assumed)

Parsing both sections end to end:

- `## Rows` (line 25): **194** data rows — matches the header's `194` (line 18) and the class
  table's `payload-absent | 194` (line 23).
- `## By lane` (line 232): every lane count matches the section-1 rows exactly, including
  `tameshi | 14` (line 240) and `tsukuroi | 2`.
- `## Rows whose quotes were NEVER CHECKED` (line 256): **109** data rows — matches its own
  `rows: **109**` (line 263).

So the row totals are **not** stale. The one figure that cannot be reconstructed from the
printed table is the header's `ABSENT quotes: **324**` (line 19):

- the generator prints at most 3 quote spans per row (`absent-defect-register.py:143`,
  `r["quotes"][:3]`), so the table's ceiling is **303**;
- four rows are physically truncated mid-quote and print only one partial span each:
  `absent-defect-register.md:103` (kotoba S151), `:108` (S167), `:111` (S172), `:114` (S176).
  Those lines end inside a quote, with no closing backtick, no trailing pipe and no note
  column (byte lengths 162/182/127/148);
- visible spans therefore **301**, and 324 − 301 = 21 lost to the 3-span cap plus 2 lost to
  the four truncated rows.

Second register defect, quoting-only: `absent-defect-register.py:160` writes the never-checked
id as `{r['id']}` + a stray closing backtick (no opening one), so every row in that table reads
``S113` `` and the awk's `$4` prints `S113\``. This is the source of the backtick in the item's
expected output; the id is S113/S123/S134.

## 5. No coverage hole for this lane outside the slice

The census shows tameshi findings in rounds 6–9 (S145, S146, S153, S160, S165, S166, S167).
Every one of those findings' verdicts is `folded` (no ABSENT, no fetch-failed, no no-locator),
so their absence from the register is correct: the register has no tameshi row after round5,
and none is owed.

## What I did not check

- Verdict *correctness* for any of the 17 rows. The verdicts stay where they are:
  `corpus/lessons/round-40.md:49–73` carries one verdict per slice id (one adopted, seven
  refused, nine present-but-not-adopted), plus `round-41/w1/ExecQuarantine.md`. Not re-audited.
- Nothing was adopted; no campaign file, lane file, jj state or git index was touched.
- Tooling: no install or upgrade was needed (no tool recorded). Scratch file
  `/tmp/tameshi-r43-ScoutQuarantine-raw.txt` was deleted.
