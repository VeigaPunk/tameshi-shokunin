# T47HardFreshMeasure — C2 freshness selftest addition (round 47, wave 1)

Seat: `T47HardFreshMeasure`, group `freshness`, lane `tameshi-shokunin`.
Deliverable: `.ufo/waves/round-47/w1/T47HardFreshMeasure.addition.py` (one top-level
`extra_T47HardFreshMeasure()`, helpers prefixed `_xT47HardFreshMeasure_`).
Base being hardened: `.ufo/evidence/round-46/hardening/freshness-counter.py`.
No lane file other than this report and the addition file was written; all scratch
state is under `/tmp/tameshi-r47-T47HardFreshMeasure/`.

## Result

Five of five assigned mutants killed, each by a named `FAIL ` line; pristine
`--selftest` still `VERDICT: PASS`; no neutral killed; no baseline kill lost;
no `inapplicable` address.

Freshness-group sweep on the assembled `/tmp/tameshi-r47-T47HardFreshMeasure/h.py`:
111 addresses, killed **58 -> 63** (exactly the five below changed state), survived
unchanged otherwise, 0 neutral killed (10 NEUTRAL lines, all `survived`), 0
`inapplicable`, 0 new `crashed`/`timeout`.

## Per-mutant attribution

All three cases reuse the round-46 `_xHardMeasure_build/_run/_fields/_fixture`
helpers read-only (scratch git repo per case: `git init -q -b m`, toplevel asserted
equal to the scratch dir, one commit with `-c user.name=t -c user.email=t@t`,
`GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`).

### measure:cmp:2 — `if state == 'invalid':` -> `!=` (line 247)

- Case: `F20_invalid_reason_routing`
- Separating input: two population rows; S001 is a verified entry, S002 is an entry
  whose `url` is `https://e.org/other` while its row URL is `https://e.org/x002`
  (`grade` -> `('invalid', 'url mismatch')`).
- Original behaviour: the reason loop prints exactly one `INVALID S002 url mismatch`
  line (summary `population=2 entries=2 verified=1 invalid=1 fresh=0 score=0 pass=false`, exit 1).
- Mutant behaviour: the loop appends for the *verified* row instead (`'S001 ok'`) and
  drops the genuine invalid reason, so the parsed `INVALID` id set becomes `['S001']`.
- Output line:
  `FAIL F20_invalid_reason_routing INVALID ids=['S001'] want=['S002']`
- Original line: `PASS F20_invalid_reason_routing`

### measure:int:0 — `score = (10 * fresh) // len(pop) if pop else 0` -> `else 1` (line 255)

- Case: `F21_empty_population_score`
- Separating input: `_xHardMeasure_fixture(0, [], [])` — an empty `corpus/SOURCES.md`
  and an empty ledger, so `population(parse_rows(''))` is empty and the `else` branch
  of the score formula is the executed one.
- Original: `C1_R45: ... population=0 entries=0 verified=0 fresh=0 score=0 ... C1_R45_PASS=false`, exit 1.
- Mutant: `score=1` from the empty-population branch.
- Output line: `FAIL F21_empty_population_score score=1 want=0`
- Original line: `PASS F21_empty_population_score`

### measure:cmp:4 — `passed = self_pin == 1 and fresh >= TARGET` -> `>` (GtE->Gt, line 256)

- Case: `F22_target_equality_passes`
- Separating input: `TARGET` (50) population rows, all 50 entries verified, each with
  an `agree` review from seat `RevX` whose report names the id, and the counter bytes
  committed at `SELF_PATH` (`self_pin=1`): `fresh == TARGET` exactly, the one point
  where `>=` and `>` disagree.
- Original: `fresh=50 score=10 target=50 C1_R45_PASS=true`, exit 0.
- Mutant: `50 > 50` is false, so `C1_R45_PASS=false`, exit 1.
- Output line: `FAIL F22_target_equality_passes exit=1 want=0 C1_R45_PASS=false want=true`
- Original line: `PASS F22_target_equality_passes`

### measure:int:1 — `return 0 if passed else 1` -> returns 1 on both arms (line 268)

- Case: `F22_target_equality_passes` (same fixture, now read through the exit code)
- Separating input: a measurement that *passes* (`self_pin=1`, `fresh=50`); the
  original returns 0, the mutant returns 1 on the passing arm.
- Output line: `FAIL F22_target_equality_passes exit=1 want=0`
- Original line: `PASS F22_target_equality_passes` (exit 0)

### measure:int:5 — `self_pin == 1` -> `self_pin == 2` (line 256)

- Case: `F22_target_equality_passes`
- Separating input: a pinned fixture (`self_pin` is 0 or 1 by construction, never 2)
  with `fresh=50`; the mutated predicate is false for the observable self_pin=1 input.
- Mutant: `C1_R45_PASS=false`, exit 1.
- Output line: `FAIL F22_target_equality_passes exit=1 want=0 C1_R45_PASS=false want=true`
- Original line: `PASS F22_target_equality_passes`

No assigned mutant was equivalent or unreachable; nothing is reported as unkillable.

## Commands and exit codes (all run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`)

1. `python3 .ufo/evidence/round-47/hardening/pool.py --enumerate .ufo/evidence/round-46/hardening/freshness-counter.py` -> rc 0
   (`measure:cmp:2` line 247 Eq; `measure:int:0` line 255 `0`; `measure:cmp:4` line 256 GtE;
   `measure:int:1` line 268 `0`; `measure:int:5` line 256 `1`).
2. `python3 .ufo/evidence/round-47/hardening/assemble.py --group freshness --add .ufo/waves/round-47/w1/T47HardFreshMeasure.addition.py --out /tmp/tameshi-r47-T47HardFreshMeasure/h.py` -> rc 0
   (`wrote ... (1 additions)`).
3. `python3 /tmp/tameshi-r47-T47HardFreshMeasure/h.py --selftest` -> rc 0;
   `C1_R45_SELFTEST: cases=37 failed=0`; `VERDICT: PASS`; F20/F21/F22 all `PASS`.
4. `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardFreshMeasure/h.py --group freshness --ids measure:cmp:2,measure:int:0,measure:cmp:4,measure:int:1,measure:int:5` -> rc 0;
   `PRISTINE pass`; all five `MUT ... killed`.
5. `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardFreshMeasure/h.py --group freshness` (whole group, no `--ids`) -> rc 0;
   111 addresses; killed 63 (baseline `.ufo/evidence/round-47/before/base-freshness.txt` 58); NEUTRAL 10/10 `survived`; no `inapplicable`; set difference to baseline is exactly the five ids above, both directions, so no baseline kill regressed and no unintended kill was added.
6. `/tmp`-only attribution script (imports `pool.py` read-only, applies each of the five mutants to `h.py`, runs `--selftest`, prints the `FAIL ` lines): rc 0; results quoted per mutant above.

## Bounds honoured

No git or jj mutation in the lane; no write to `/home/vgpnk/Projects/shokuknow`, the
fleet repo, or a sibling lane; counters were run only as `--selftest`/`--try` probes
into `/tmp`, never as a verdict; no tool installs were needed (python3 + git present,
pacman untouched).
