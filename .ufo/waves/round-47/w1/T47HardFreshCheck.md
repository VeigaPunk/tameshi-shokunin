# T47HardFreshCheck — C2 selftest addition for the freshness `check()` lineage

- Seat: `T47HardFreshCheck` (leaf, godspeed). Group: `freshness`. Judged on: operability.
- Deliverable: `.ufo/waves/round-47/w1/T47HardFreshCheck.addition.py` — one top-level
  `extra_T47HardFreshCheck()` (helpers `_xT47HardFreshCheck_*`).
- Hardened counter under test: `.ufo/evidence/round-46/hardening/freshness-counter.py`.
- Scratch: `/tmp/tameshi-r47-T47HardFreshCheck/` (`h.py`, `group.txt`).

## Result

All nine assigned mutants killed, plus one collateral behavioural kill (`parse_rows:int:6`).
Freshness-group kills 58 -> 68 of 101 real mutants; all 10 freshness neutrals survive; no
baseline kill was lost; assembled `--selftest` ends `VERDICT: PASS` (39 cases, 0 failed).

## The gap

`check()` (`.ufo/evidence/round-46/hardening/freshness-counter.py:273-297`) is the
`--check FRAGMENT.json` seat helper. Neither the round-45 `selftest()` nor any round-46
addition calls it, so all sixteen of its sites (nine non-neutral) were unexercised and the
whole lineage survived. The cases below drive it directly: a scratch git lane whose
`corpus/SOURCES.md` at rev `m` carries one population row (S001), a snapshot directory, and
a fragment file written per case. Each case asserts the exact exit code and the `CHECK ...`
line that `check()` prints; no case reads the counter's own bytes.

Fixture (shared, built once per selftest via the existing `_xHardMeasure_build`/`_xHardMeasure_git`):

- row: `| S001 | x — https://example.org/a | docs | A | flaky failure reports | section Metrics | flaky failures cluster in the same job | mined | 2026-10-25 | 180d | p |`
- page: the `_xHardGrade_page()`-style HTML paragraph; quote `Flaky failures cluster inside
  the same job because the rerun` (10 tokens, verbatim in the page, not a substring of the
  row cells, 3 shared content words -> `verified`).
- Every `check()` call is wrapped (`contextlib.redirect_stdout` + `try/except Exception`) so a
  mutant that raises is reported as a named `FAIL <case> exit='raised <Exc>'` line instead of
  killing the selftest with a traceback (a traceback is `crashed`, not a kill).

## Per mutant

| pool id | mutation | case | separating input | FAIL line (mutant) |
|---|---|---|---|---|
| `check:cmp:0` | `if row is None:` -> `is not None` | `H01_row_in_population_verified` | fragment id S001 **is** in the rev population | `FAIL H01_... exit=1 want_exit=0 ... got='CHECK S001 invalid not in population'` |
| `check:bool:1` | `git(...) or ''` -> `and ''` | `H01_row_in_population_verified` | same; the rev registry read is non-empty, mutant discards it | `FAIL H01_... got='CHECK S001 invalid not in population'` |
| `check:bool:0` | `entry.get('snapshot') or ''` -> `and ''` | `H01_row_in_population_verified` | entry names `snap/page.txt`, snapdir holds `page.txt` | `FAIL H01_... got='CHECK S001 invalid snapshot absent'` |
| `check:cmp:1` | `state in ('verified',...)` -> `not in` | `H01_row_in_population_verified` | verified state must map to exit 0 | `FAIL H01_... exit=1 ... got='CHECK S001 verified ok'` |
| `check:int:1` | `return 0 if ...` -> `1 if ...` | `H01_row_in_population_verified` | verified state must map to exit 0 (mutant always exits 1) | `FAIL H01_... exit=1 ... got='CHECK S001 verified ok'` |
| `check:int:2` | final `else 1` -> `else 2` | `H05_invalid_state_exit_1` | present row, page present, `raw_sha256='0'*64` -> `invalid sha mismatch` | `FAIL H05_... exit=2 want_exit=1 ... got='CHECK S001 invalid sha mismatch'` |
| `check:int:0` | early `row is None` `return 1` -> `2` | `H02_row_absent_exit_1` | fragment id S999 is **not** in the population | `FAIL H02_... exit=2 want_exit=1 ...` |
| `check:int:3` | `name[:-3]` -> `name[:-4]` for `.gz` | `H03_gz_suffix_strip` | entry names `snap/page.txt.gz`, snapdir holds the raw page as `page.txt` only | `FAIL H03_... got='CHECK S001 invalid snapshot absent'` |
| `check:bool:2` | `name and os.path.isfile(full)` -> `or` | `H04_missing_snapshot_no_raise` | entry names `snap/absent.txt`, file absent | `FAIL H04_... exit='raised FileNotFoundError' want_exit=1 ...` (original grades `invalid snapshot absent`, exit 1) |

Collateral kill (not assigned, same lineage): `parse_rows:int:6` (`teaches=cells[7]` ->
`cells[8]`) — `H01`/`H03` grade the parsed row, whose `teaches` cell no longer contributes the
shared words, so the valid entry grades `CHECK S001 invalid overlap 1`, exit 1. Behavioural,
not a pin.

Per-mutant FAIL counts observed: cmp:0 5, bool:1 4, cmp:1 4, bool:0 3, int:1 2, int:2 2,
int:0 1, int:3 1, bool:2 1 (`H02` for cmp:0 is the fall-through `raised TypeError`, caught and
named). Each mutant's FAIL set contains at least one case whose expectation differs only
through the mutated site.

## Commands run (all absolute-path, lane read-only)

```
python3 .ufo/evidence/round-47/hardening/assemble.py --group freshness \
  --add .ufo/waves/round-47/w1/T47HardFreshCheck.addition.py \
  --out /tmp/tameshi-r47-T47HardFreshCheck/h.py          # exit 0, wrote h.py (1 additions)
python3 /tmp/tameshi-r47-T47HardFreshCheck/h.py --selftest # exit 0, VERDICT: PASS, cases=39 failed=0
python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardFreshCheck/h.py \
  --group freshness --ids check:cmp:0,check:bool:0,check:int:0,check:cmp:1,check:int:1,\
check:int:2,check:bool:1,check:bool:2,check:int:3                # exit 0: PRISTINE pass, 9/9 killed
python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardFreshCheck/h.py \
  --group freshness                                              # exit 0: all 10 NEUTRAL survived
```

Whole-group sweep (101 MUT + 10 NEUTRAL, stored at `/tmp/tameshi-r47-T47HardFreshCheck/group.txt`):
killed 58 (baseline `.ufo/evidence/round-47/before/base-freshness.txt`) -> 68; newly killed =
the nine ids above + `parse_rows:int:6`; no baseline kill regressed; neutrals
(`git:commute:0`, `grade:commute:0..4`, `measure:commute:0..2`, `live:commute:0`) all
`survived`.

Assembler sanity: diff of `h.py` against the round-46 counter removes exactly the `SELF_PATH`
line and adds only my block plus the four `extra_cases/failed` call lines — no rule code moved.

## Risks / notes

- The cases reuse `_xHardMeasure_build`/`_xHardMeasure_git`/`_xHardMeasure_env` (read-only);
  if a later seat changes those helpers, this addition follows them or fails loudly as
  `FAIL T47HardFreshCheck_harness`, which is visible on the pristine run (pristine must pass).
- Wall cost: five `check()` calls, each one `git show` in a fresh scratch repo (~1 s total),
  well inside the 90 s pool timeout.
- The output of `check()` is a seat-helper contract (exit 0 for verified/drifted/unreachable,
  1 otherwise), so pinning the exact 0/1/2 codes is a behavioural statement, not cosmetics.
- No tool installs or upgrades were needed; `pacman` untouched. No lane writes beyond this
  report and the one addition file; no git/jj mutation in the lane.
