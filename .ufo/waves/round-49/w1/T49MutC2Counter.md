# T49MutC2Counter — mutation probe of the frozen C2 counter's `--selftest`

Seat: T49MutC2Counter (wave 1, round 49). Item: 12+ single-edit mutants of
`.ufo/evidence/round-49/c2/measure.py`, run against `--selftest` only, in scratch; report
survivors and the selftest case each would need. The lane counter was **never edited**: all
mutants are fresh scratch copies; restoration is proven by sha256 before/after.

## Method and baseline gate

- Scratch root `S=/fast/scratch/hyaku/tameshi-r49/T49MutC2Counter` (deleted before yield;
  raw outputs preserved in `T49MutC2Counter.receipts.txt` beside this report).
- `cp .ufo/evidence/round-49/c2/measure.py $S/measure.py`; `sha256sum` both:
  `f4971d02b8b1af40363f331ae2fadfffeec8ddf2fcbe0c4bc514ec25d8d0fde5` — identical.
- Baseline: `python3 -I $S/measure.py --selftest` → all 11 cases PASS,
  `C2_R49_SELFTEST: cases=11 failed=0`, exit 0. Every verdict below is conditional on this pass.
- Each mutant: one string replacement in a fresh copy (old string verified to occur exactly
  once — held for all 15); detector `python3 -I $S/mut/<id>.py --selftest`.
- Restoration: after all runs, `sha256sum` lane + scratch copy again — both unchanged
  (`…f4971d02…` before == after). No tooling was installed (system python 3.14.8 only).

## Results — 15 mutants: 6 killed, 9 survived

Command showing any row: `python3 -I $S/mut/<id>.py --selftest` (raw stdout in receipts file).

| id | measure.py:line | single edit | verdict | detector (failing case) |
|---|---|---|---|---|
| census-loose | :57 | `ROW_CENSUS` `^ {0,3}` → `^ *` | KILLED | `oracle-indent4-not-row` |
| census-digits | :57 | `ROW_CENSUS` `\d{3,}` → `\d{4,}` | KILLED | `oracle-collision`, `oracle-indent4-not-row`, `oracle-duplicate-refusal`, `oracle-short-row-refusal`, `oracle-numeric-sort` |
| shortrow-4 | :101 | `len(cells) < 5` → `< 4` | KILLED | `oracle-short-row-refusal` |
| dup-drop | :101 | drop ` or m.group(1) in ids` | KILLED | `oracle-duplicate-refusal` |
| sort-lex | :106 | drop `, key=lambda s: int(s[1:])` (numeric sort → lexicographic) | **SURVIVED** | — (exit 0, 11/11 PASS) |
| class-idlen | :131 | id-digit predicate `>= 5` → `>= 6` | KILLED | `classes-basic` |
| class-collcount | :135 | `collision_count', 0) > 0` → `> 1` | KILLED | `classes-basic` |
| classmin-9 | :50 | `CLASS_MIN = 10` → `9` | **SURVIVED** | — |
| killtarget-10 | :51 | `KILL_TARGET = 11` → `10` | **SURVIVED** | — |
| killtarget-arith | :360 | `max(0, KILL_TARGET - res['confirmed'])` → `… - confirmed - 1)` | **SURVIVED** | — |
| comparable-staged | :191 | drop `'staged_sha256'` from comparable() exclusion tuple | **SURVIVED** | — |
| cx-index-ne | :340 | counterexample lookup `c['index'] == k` → `!= k` | **SURVIVED** | — |
| records-status | :285 | `cells[7] != 'mined'` → `!= 'opened'` | **SURVIVED** | — |
| records-opened | :285 | `cells[8] != '2026-10-26'` → `!= '2026-10-27'` | **SURVIVED** | — |
| dumplen-ge1 | :311 | pristine gate `dumpn == CASES` → `dumpn >= 1` | **SURVIVED** | — |

All 6 kills exited 1 with the named CASE lines FAIL; no syntax-level kills (every mutant was
valid Python), so every kill is a genuine behavioral detection.

## Survivors and the selftest case each would need

1. **sort-lex** (:106) — true detection gap in tested code. The frozen `oracle-numeric-sort`
   case intersects {S010, S100}, which co-sort identically under lexicographic and numeric
   order, so the numeric key is invisible to it. Needed case:
   `case('oracle-numeric-sort-disagree', oracle(H + row('S9','a') + row('S100','b'), H + row('S9','c') + row('S100','d'))[1] == ['S9','S100'])`
   — numeric orders S9 before S100 (9 < 100); lexicographic puts `S100` first, killing the mutant.
2. **comparable-staged** (:191) — true detection gap in tested code. `comparable-ignores-shas`
   varies only `registry_sha256`; the mutant stops ignoring `staged_sha256`. Needed case:
   `case('comparable-ignores-staged-sha', comparable((0, {'a':1,'staged_sha256':'x'}, b'')) == comparable((0, {'a':1,'staged_sha256':'y'}, b'')))`.
3. **classmin-9** (:50) and **killtarget-10** (:51) — constants read only inside `measure()`
   (:352, :360), which `selftest()` never calls. Needed case (one line covers both):
   `case('frozen-constants', (CLASS_MIN, KILL_TARGET, SEED, CASES) == (10, 11, 4949, 400))`.
4. **killtarget-arith** (:360) — the shortfall term is inline in `measure()`. Needed: factor it
   into a pure `shortfall(confirmed, target)` and assert `shortfall(10,11) == 1` (the `-1`
   mutant returns 0 there) plus `shortfall(11,11) == shortfall(12,11) == 0`.
5. **cx-index-ne** (:340) — counterexample confirmation is inline in `measure()`. Needed: a pure
   `pick_case(dump, k)` with cases asserting exactly-one hit for `index==k` and no hit for
   `index!=k` (the inverted lookup confirms the wrong case).
6. **records-status** (:285) — needed: factor the SOURCES-row check into pure `row_ok(cells)`
   and assert `row_ok` true for `cells[7]=='mined'` and false for `'opened'`.
7. **records-opened** (:285) — same helper: true for `cells[8]=='2026-10-26'`, false for
   `'2026-10-27'`.
8. **dumplen-ge1** (:311) — needed: a pure `pristine_ok(exit, cases, viol, dumpn, indices)`
   with `pristine_ok(0,400,0,399,…)` required to be False (the mutant accepts the short dump).

## Findings

- **Structural blind spot:** `selftest()` exercises only the pure helpers (`oracle`,
  `case_classes`, `comparable`, `LAST_RE`); `materialize`, `load_panel`, `write_mutant`,
  `run_guard`, `run_generator`, `load_dump`, `records`, `measure`, `witness` and the frozen
  constants are `--selftest`-invisible, so 7 of the 9 survivors fall there by construction.
  Only **sort-lex** and **comparable-staged** are gaps inside code the selftest claims to test.
- Deciding-run exposure [INFERENCE from source reading]: `killtarget-arith` (:360),
  `dumplen-ge1` (:311), `cx-index-ne` (:340) and the `records()` checks (:285) are load-bearing
  in the deciding invocation and their mutation survival means `--selftest` alone cannot
  certify them; the panel/witness/controls runs, not the selftest, are what would notice.
- Per the seat contract these survivors are coverage findings about the counter's selftest;
  they are not permission to change the frozen counter or the C2 contract, and no lane file
  was modified (hashes above).

## Summary

- Probed the frozen C2 counter `.ufo/evidence/round-49/c2/measure.py` (sha256 `f4971d02…`) in scratch with 15 single-edit mutants, detector `--selftest` only; lane file untouched (before/after hashes identical).
- Baseline passed (11/11 cases, exit 0); all 15 mutants applied cleanly (old string unique in each).
- 6 killed: both census-regex edits, short-row refusal, duplicate refusal, both class-predicate edits.
- 9 survived: numeric sort, CLASS_MIN, KILL_TARGET const + arithmetic, comparable() staged-sha drop, counterexample index lookup, records() status/opened, pristine dump length.
- Two survivors are true gaps in tested code (sort case's collision set co-sorts both ways; sha-ignores case never varies `staged_sha256`); the other 7 sit in regions `selftest()` cannot reach.
- Per-survivor selftest case specified above; receipts in `T49MutC2Counter.receipts.txt`; scratch deleted.
