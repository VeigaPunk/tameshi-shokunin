# T49W2MutGenerator — oracle mutation probe of `tools/pbt-staged-id.py` (round 49, wave 2)

Axes (godspeed): the claim under attack is **C2 / coverage (F10)**; the probe's own axes are
**kill rate** (does the generated distribution exercise each oracle rule?) and **detector
boundary** (what can a `violations=0` oracle-run never see?). This seat attacks the
generator's oracle, never the guard: `tools/staged-id-guard.py` stayed byte-pristine
throughout (sha256 `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`,
verified before and after every run; equals contract `claims.C2.named_gate`).

## Method

Detector (same command for baseline and every mutant; run only in scratch, never a verdict):

```
git -C LANE show f181a961ae44061af486f600e5ea257d2baf78f8:tools/pbt-staged-id.py   # base copy
python3 -I <generator> --guard <pristine guard> --seed 4949 --cases 400 --dump <scratch>/dump.jsonl
```

- Verdict semantics (per item): **killed** = the mutant makes the generator report a false
  violation on the PRISTINE guard (`violations=1`, `counterexample=<index>`); **survived** =
  the generator still prints `violations=0` over seed 4949 / 400 cases — the mutated oracle
  rule is not exercised by any generated case.
- Baseline (pristine generator, pristine guard): exit 0,
  `PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31`,
  11.2 s. All 12 classes ≥ 30 (generator floor 20, contract floor 10). **Baseline conclusive.**
- 21 single-edit mutants (more than the required 10), each `old` occurring exactly once in
  the base source (asserted by the builder); mutated points cited as
  `tools/pbt-staged-id.py:<line>` at `f181a961` (scratch base copy sha-verified equal to the
  blob: `0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05`).
- Secondary column: `python3 -I <generator> --selftest` (31 internal cases, no guard
  subprocess) — shows which survivors/casualties the generator's own selftest covers.

## Results — 17 killed, 4 survived

| Mutant | Area | Base line | Verdict | Evidence (observed) | selftest |
|---|---|---|---|---|---|
| M01 | census regex upper bound `{0,3}`→`{0,4}` | 56 | KILLED | idx 20, `field staged_max: guard 'S000', oracle 'S007'` (4-space row admitted as a row) | failed=1 |
| M02 | census regex lower bound `{0,3}`→`{1,3}` | 56 | KILLED | idx 0, `exit 1, oracle expects 0` | failed=20 |
| M03 | census regex id width `S\d{3,}`→`S\d{4,}` | 56 | KILLED | idx 0, `exit 1, oracle expects 0` | failed=20 |
| M04 | numeric sort of collisions: `key=id_number` dropped | 127 | **SURVIVED** | `cases=400 violations=0 counterexample=none` | failed=1 |
| M05 | held normalisation: scheme strip removed | 96 | KILLED | idx 10, `field held: guard {'S023': 'S023'}, oracle {}` | failed=2 |
| M06 | held normalisation: `rstrip('/')` removed | 98 | KILLED | idx 8, `field held: guard {'S026': 'S015'}, oracle {}` | failed=3 |
| M07 | naive map off-by-one `top+index`→`top+index+1` | 146 | KILLED | idx 0, `field naive_map: guard {'S022': 'S023'}, oracle {'S022': 'S024'}` | failed=1 |
| M08 | cascade predicate `in staged`→`in registry` | 147 | KILLED | idx 5, `exit 1, oracle expects 0` | failed=1 |
| M09 | refusal prediction `or`→`and` | 158 | KILLED | idx 0, `exit 1, oracle expects 0` | failed=2 |
| M10 | map floor ignores staged ids | 182 | KILLED | idx 12, `field map_floor: guard 'S017', oracle 'S016'` | failed=1 |
| M11 | map dedupe: normalised→exact string compare | 192-194 | KILLED | idx 12, `exit 0, oracle expects 1` | failed=1 |
| M12 | held-moved rule removed (`held_moved = []`) | 207-208 | KILLED | idx 54, `field map_held_moved: guard ['S004'], oracle []` | failed=1 |
| M13 | selfmap rule removed (`selfmap = []`) | 205 | KILLED | idx 54, `field map_reasons: guard [... ('self', ('S004',)), ...], oracle [...]` (missing self) | failed=1 |
| M14 | injective rule removed | 212-213 | KILLED | idx 93, `exit 1, oracle expects 0` | failed=1 |
| M15 | reason projection phrase `'held document off'`→`'held-document-off'` | 289 | KILLED | idx 54, `field map_reasons: guard [... ('unknown', 'map moves a held document off ...')], oracle [... ('held', ('S004',))]` | **failed=0** |
| M16 | short-row threshold `< 5`→`< 6` | 118 | **SURVIVED** | `cases=400 violations=0 counterexample=none` | **failed=0** |
| M17 | duplicate-id refusal removed | 120-121 | KILLED | idx 50, `exit 2, oracle expects 0` (guard: `staged:5 duplicate id S006`) | failed=1 |
| M18 | class-logic predicate `other != url`→`other == url` | 365 | **SURVIVED** | `cases=400 violations=0` with `url_form_variant=0` (baseline 30) | failed=1 |
| M19 | document_key head length `> 8`→`> 80` | 90 | KILLED | idx 8, `exit 0, oracle expects 1` | **failed=0** |
| M20 | safe_floor off-by-one (drop `+1`) | 162 | KILLED | idx 0, `field safe_floor: guard 'S023', oracle 'S022'` | failed=1 |
| M21 | S-id length rule `> 12`→`> 99` | 104 | **SURVIVED** | `cases=400 violations=0 counterexample=none` | **failed=0** |

All four survivors produced class counts byte-identical to the baseline (determinism held;
the mutated code paths never fired).

## Findings (each survivor = an oracle rule no generated case exercises)

1. **M04 — numeric sort of `collisions` (line 127) is never exercised by generation.**
   From the baseline dump of all 400 cases: only 7 cases have ≥2 collisions, max
   `|collisions|` is 2, and in **0** cases does lexicographic order differ from numeric
   order (`S\d{3,}` ids with `S%03d` padding sort identically either way). The run cannot
   kill this mutant; only selftest case `numeric-sort` (`S999`+`S1000`, line 831) does.
   *Coverage gap:* no recipe ever puts two colliding ids across the 3/4-digit padding
   boundary (e.g. `S999` and `S1000` both colliding). Command that shows it: the scan over
   `dump.jsonl` (7 multi-collision cases, 0 order differences).
2. **M16 — the 5-cell boundary of the short-row rule (line 118) is never probed.**
   Cell-count histogram over all 1487 parsed rows in the 400 baseline cases:
   `{2: 6, 4: 12, 11: 1469}` — no row with exactly 5 cells is ever generated, so `< 5`
   vs `< 6` is indistinguishable to the whole run *and* to selftest (its short-row fixture
   has 4 cells). The refusal recipes (`rec_refusal`, line 451) emit only 2- and 4-cell rows;
   all normal rows have 11 cells.
3. **M21 — the `len(sid) > 12` refusal (line 104) is unexercised by construction.** The
   source comment itself says "not generated, kept for fidelity"; the longest id any recipe
   can emit is `S999999` (7 chars, `rec_id_4_plus_digits`, line 434). A documented,
   deliberate hole — listed here because it is precisely an oracle rule the generated
   distribution never touches (the hidden panel is the intended coverage for it).
4. **M18 — detector boundary: class-logic mutants are structurally invisible to
   `violations`.** `case_classes` (lines 337-365) feeds only the printed CLASS counts, never
   `check()` (line 303); the run exits 0 with `url_form_variant=0` while the baseline had
   30. A `violations=0` deciding run therefore cannot degrade-detect class-distribution
   collapse; the counter's `class_min >= 10` gate is the control that sees it (here the
   CLASS lines do expose `url_form_variant=0`). Recorded as a boundary fact, not a defect.

Corollary on the two coverage channels: M15 and M19 are killed by generated cases but pass
selftest (`failed=0`), while M04 is caught only by selftest — the generated run and the
selftest exercise disjoint subsets of the oracle, and both channels were needed to cover
this panel (selftest alone misses 2/17 kills; the run alone misses 4 mutants).

## Commands (reproduce any row)

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  f181a961ae44061af486f600e5ea257d2baf78f8:tools/pbt-staged-id.py > g.py   # sha 0cbee392…
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  f181a961ae44061af486f600e5ea257d2baf78f8:tools/staged-id-guard.py > guard.py  # sha 03a796c5…
# apply exactly one table edit at the cited line, then:
python3 -I g.py --guard guard.py --seed 4949 --cases 400 --dump d.jsonl   # observe PBT_STAGED_ID line
python3 -I g.py --selftest                                                # observe failed=…
```

Baseline output and every mutant's full `VIOLATION` / `PBT_STAGED_ID` /
`PBT_STAGED_ID_SELFTEST` lines are quoted above (verifiable without my scratch, which is
deleted by policy; the cited shas pin the inputs).

## Restoration evidence

- Scratch base copies re-hashed after all 22 runs (baseline + 21 mutants): generator
  `0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05`, guard
  `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` — identical to pre-run
  hashes; guard sha equals the contract's `named_gate` value.
- Lane checkout untouched by this seat: `git -C <lane> status --porcelain -- tools/` → empty;
  `git diff --stat -- tools/` → empty. Blobs re-read from `f181a961` match both shas above.
- No tools installed or upgraded (system `python3` only); no scratch path cited as evidence;
  no forbidden path read (`~/.local/state/`, `c2-WITNESS/CTL_*.stdout` untouched); no counter
  invoked; nothing under the lane modified except this report file.

## Summary

- Baseline (pristine generator vs pristine guard, seed 4949, 400 cases): violations=0, exit 0 — detector conclusive.
- 21 single-edit oracle/class mutants: 17 killed (false violation on the pristine guard), 4 survived.
- Survivors M04 (collisions numeric sort, line 127), M16 (5-cell row boundary, line 118), M21 (S-id >12 rule, line 104): oracle rules no generated case exercises; M04/M16 also pass selftest.
- M04 gap quantified: 7 multi-collision cases, 0 with lexicographic≠numeric order; max 2 collisions/case — no recipe crosses the 3/4-digit padding boundary.
- M16 gap quantified: row cell histogram {2:6, 4:12, 11:1469} — a 5-cell row is never generated.
- M18: class-logic mutant (url_form_variant 30→0) leaves violations=0 — class counts are invisible to the violations oracle; the counter's class gate is the seeing control.
- M15/M19 pass selftest but are killed by generated cases; M04 the reverse — run and selftest cover disjoint oracle subsets.
- Guard and generator base bytes unchanged pre/post (shas above); lane tools/ clean; report at .ufo/waves/round-49/w2/T49W2MutGenerator.md.
