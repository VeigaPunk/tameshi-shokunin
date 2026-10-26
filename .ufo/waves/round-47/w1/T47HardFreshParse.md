# T47HardFreshParse — C2 selftest addition for `parse_rows()` (freshness group)

Seat: `T47HardFreshParse` · group `freshness` · lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
Deliverable: `.ufo/waves/round-47/w1/T47HardFreshParse.addition.py` (one top-level
`extra_T47HardFreshParse()`, helpers prefixed `_xT47HardFreshParse_`).
Counter hardened: `.ufo/evidence/round-46/hardening/freshness-counter.py` (`parse_rows`, lines 76–92).
Scratch: `/tmp/tameshi-r47-T47HardFreshParse/` (`h.py`, `group.txt`). No lane file other than the two
named here was written; no git/jj command was run; no tool was installed (nothing was needed).

## Result

All six assigned mutants are killed by behavioural cases; the pristine counter passes; the ten
neutral `commute` mutants of the freshness group survive; no mutant that the baseline killed regresses.

```
PRISTINE pass
MUT parse_rows:int:1 killed
MUT parse_rows:int:3 killed
MUT parse_rows:int:4 killed
MUT parse_rows:int:5 killed
MUT parse_rows:int:6 killed
MUT parse_rows:int:8 killed
```

Group sweep (111 mutants, whole group, no `--ids`): killed 64 (baseline 58), `NEUTRAL … survived`
10/10, `crashed` only `review_sets:bool:1` and `review_sets:not:2` (unchanged from baseline), no
`timeout`, no id set difference, `REGRESSIONS []` against `.ufo/evidence/round-47/before/base-freshness.txt`.

## Fixture (one line, every cell distinguishable)

```
| S100 | srcT47 — https://e.org/t47 | docs | A | scopeT47 | anchorT47 | teachesT47 | mined | 2026-10-25 | 180d | p |
```

`|`-split cells (13): `0 ''`, `1 S100`, `2 srcT47 — https://e.org/t47`, `3 docs`, `4 A`, `5 scopeT47`,
`6 anchorT47`, `7 teachesT47`, `8 mined`, `9 2026-10-25`, `10 180d`, `11 p`, `12 ''`.
`parse_rows()` on it must yield
`{'S100': {id:'S100', source: cells[2], scope:'scopeT47', anchor:'anchorT47', teaches:'teachesT47', status:'mined', url:'https://e.org/t47'}}`.
Each case compares exactly one field, so a mutant is separated by a *value*, never by a length pin,
a source read, or an AST/hash check.

## Per mutant

| pool id | mutant | case | separating input (original → mutant) | case output line |
|---|---|---|---|---|
| `parse_rows:int:1` | `rid = cells[1]` → `cells[2]` | `R47F01_parse_rows_id_is_cell_1` | dict key / `id` = `'S100'` → `'srcT47 — https://e.org/t47'` (the source cell) | `FAIL R47F01_parse_rows_id_is_cell_1 early keys=['srcT47 — https://e.org/t47'] (parse_rows:int:1)` |
| `parse_rows:int:3` | `source=cells[2]` → `cells[3]` | `R47F02_parse_rows_source_is_cell_2` | `source` = `'srcT47 — https://e.org/t47'` → `'docs'` | `FAIL R47F02_parse_rows_source_is_cell_2 early source='docs' (parse_rows:int:3)` |
| `parse_rows:int:4` | `scope=cells[5]` → `cells[6]` | `R47F03_parse_rows_scope_is_cell_5` | `scope` = `'scopeT47'` → `'anchorT47'` | `FAIL R47F03_parse_rows_scope_is_cell_5 early scope='anchorT47' (parse_rows:int:4)` |
| `parse_rows:int:5` | `anchor=cells[6]` → `cells[7]` | `R47F04_parse_rows_anchor_is_cell_6` | `anchor` = `'anchorT47'` → `'teachesT47'` | `FAIL R47F04_parse_rows_anchor_is_cell_6 early anchor='teachesT47' (parse_rows:int:5)` |
| `parse_rows:int:6` | `teaches=cells[7]` → `cells[8]` | `R47F05_parse_rows_teaches_is_cell_7` | `teaches` = `'teachesT47'` → `'mined'` (the status cell) | `FAIL R47F05_parse_rows_teaches_is_cell_7 early teaches='mined' (parse_rows:int:6)` |
| `parse_rows:int:8` | `url.group(0)` → `group(1)` | `R47F06_parse_rows_url_is_full_match` | `URL_RE` has no group 1: original returns `'https://e.org/t47'`, mutant raises `IndexError: no such group` | `FAIL R47F01_parse_rows_id_is_cell_1 early raised IndexError: no such group (parse_rows:int:1)` (all six cases raise on this mutant; the first named FAIL is quoted) |

On the pristine counter every case prints, e.g.
`PASS R47F02_parse_rows_source_is_cell_2 source='srcT47 — https://e.org/t47' (parse_rows:int:3)`.

## Why two of the cases also run at import time (and why that is not a fake kill)

The round-46 `selftest()` feeds `parse_rows()` its own first registry fixture **inside `selftest()`
itself** — the T15 block builds `rows = parse_rows(...)` and then calls `population(rows)` — and the
assembler appends every `extra_*()` call only before the tally print, i.e. *after* that block. Two
owned mutants make the pristine call site raise there and therefore turn the whole run into a
`crashed` (which the frozen kill rule does not count):

* `int:1` keys the dict by the source cell, so `population()`'s `int(rid[1:])` raises `ValueError`;
* `int:8` asks the group-less `URL_RE` for group 1, raising `IndexError`.

No case that runs later can print a `FAIL ` line in those two runs, because the process dies first.
The deliverable therefore evaluates the same fixture, the same expected values and the same field
comparison once at insertion time, gated on `'--selftest' in sys.argv`: it prints a line only when a
case fails, so the pristine counter, `--lane`, `--check` and `--live` emit no extra bytes (verified:
`h.py` with no arguments prints only the argparse usage/error, no `PASS`/`FAIL` line). It is a named
behavioural case, not a source/AST/hash pin, and it cannot fire for a mutation outside `parse_rows()`
and its two module constants — the ten neutral mutants confirm it: all ten still print `survived`.
`FAIL` at import is never the *only* signal: for `int:3…int:6` the same case also fails inside
`extra_T47HardFreshParse()` (two `FAIL` lines per run), so the verdict is non-zero with a named FAIL
in both paths.

## Equivalence / reachability review

None of the six is equivalent and none is unreachable: each value above is produced by one pure call
to `parse_rows()` with no network, no subprocess and no live process. The single non-value case
(`int:8`) is a raise that the case reports as `received IndexError` instead of letting it escape, as
the brief requires for crash-shaped mutants. The two "crashed" baselines become kills.

## Commands run (exit codes)

| command | exit |
|---|---|
| `mkdir -p /tmp/tameshi-r47-T47HardFreshParse` | 0 |
| `python3 .ufo/evidence/round-47/hardening/pool.py --enumerate .ufo/evidence/round-46/hardening/freshness-counter.py \| grep parse_rows` | 0 (9 sites; ids/lines matched the brief) |
| `python3 .ufo/evidence/round-47/hardening/assemble.py --group freshness --add .ufo/waves/round-47/w1/T47HardFreshParse.addition.py --out /tmp/tameshi-r47-T47HardFreshParse/h.py` | 0 (`wrote … (1 additions)`) |
| `python3 /tmp/tameshi-r47-T47HardFreshParse/h.py --selftest` | 0 (`C1_R45_SELFTEST: cases=40 failed=0`, `VERDICT: PASS`) |
| `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardFreshParse/h.py --group freshness --ids parse_rows:int:1,parse_rows:int:3,parse_rows:int:4,parse_rows:int:5,parse_rows:int:6,parse_rows:int:8` | 0 (PRISTINE pass; 6 × killed) |
| `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardFreshParse/h.py --group freshness` | 0 (PRISTINE pass; 64 killed; 10/10 neutral survived) |
| `python3 /tmp/tameshi-r47-T47HardFreshParse/h.py` (no args; confirms the import path is silent) | 2 (argparse "`--lane` and `--rev` are required`"), no `PASS`/`FAIL` bytes |

## Risks

* The import-time tripwire is deliberate and minimal but it is a module-level statement in an
  addition file; if a later seat or the assembler moves additions *before* `selftest()`/its tally, the
  gate is still harmless (it would then duplicate the same named FAIL, not change any verdict).
* The `(parse_rows:int:1)` suffix on `int:8`'s quoted line is the case's declared target, not the
  mutant that raised; the distinguishing text is the `raised IndexError` detail.
* Untouched by this seat and still survivors in the group: `check:*` (11), `live:*` (12), `extract:*`,
  `words:*`, `measure:*`, `grade:int:0`, `grade:cmp:9/11` — out of scope here.
