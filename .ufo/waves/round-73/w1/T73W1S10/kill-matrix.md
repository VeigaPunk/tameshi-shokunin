# Round 73 — mutation kill matrix (seat T73W1S10)

Mutation probe on the two instruments R73-C1/R73-C2 rest on. Every mutant lives in
`/fast/scratch/hyaku/tameshi-r73/T73W1S10/stage/`, never in the lane. This is evidence for the
L1's verdict, not a verdict.

## 0. Bytes tested (pristine and mutant, sha256)

| file | role | sha256 |
|---|---|---|
| `tools/rekey-cost.py` | pristine (copy of lane worktree byte-for-byte) | `85ca2b69d723871d41dfc17307131d81262c1a8404e140f6ab4b461543bd88f4` |
| `tools/rekey-cost.py` | mutant **M3** (`IGNORED = frozenset()`) | `7e0fdf623f6693b0414983c48c0fea62086618e63460e1c88f54ef63781db844` |
| `tools/wave-reconcile.py` | pristine (copy of lane) | `e68947bd7686ee9879998a4642147c87a1089dd0b866c501ae45066549ccc15f` |
| `tools/wave-reconcile.py` | mutant **W1** (`ok = True` in `sweep()`) | `81eb4ed6ebbdbf99b8040b4b8ed064fa7164e95dce2534beb8af78739e975e1c` |
| `tools/wave-reconcile.py` | mutant **W2** (seat_reports any depth) | `37703d42622ea962ee9e3c28c7090487781dece4b8034dbb793cff1acb9ec042` |

Pristine copies were made with `cp -p` from the lane and re-hashed in place: the copy hash equals
the lane hash for both files, so every mutant below is a one-line delta on the bytes the frozen
counters run. Each substitution asserted `old.count == 1` before writing (see `T73W1S10.md` §2).

## 1. Mutants

| id | instrument | exact substitution | line |
|---|---|---|---|
| M3 | `rekey-cost.py` | the three-line `IGNORED = frozenset((SKILL, '.ufo/evidence/round-17/coldread/ledger.json', LEDGER))` → `IGNORED = frozenset()` | 71-73 |
| W1 | `wave-reconcile.py` | `ok = measured == row['expect']` → `ok = True` | 284 |
| W2 | `wave-reconcile.py` | `if p.startswith(prefix) and '/' not in p[len(prefix):]` → `if p.startswith(prefix)` | 206 |

W1 and W2 were chosen from the three suggested classes: W1 attacks the verdict (the `expect`
comparison), W2 attacks the artifact re-derivation (the depth clause of `seat_reports`).

The mutants themselves never enter the lane (hard rule 1 deletes the scratch tree before this seat
yields), so their exact text is preserved here as reconstructible evidence:
`T73W1S10/mutants.diff` (unified diffs against the pinned pristine hashes) next to this file.

### Compact mutant × arm matrix

Rekey battery arms `B1..B7` = `sources, province, quality, scorecard, pointer, union, ignored-skill`;
rekey selftest arms `S1..S8` = `arm1…arm8` in printed order. Wave arms `A1..A12` = `arm1…arm12`.
`·` = identical to pristine, **K** = kill.

| mutant | B1 | B2 | B3 | B4 | B5 | B6 | B7 | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 | A11 | A12 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M3 | · | · | · | · | · | · | **K** | · | · | · | · | **K** | · | · | · | – | – | – | – | – | – | – | – | – | – | – | – | killed |
| W1 | – | – | – | – | – | – | – | – | – | – | – | – | – | – | – | · | **K** | · | · | · | **K** | · | · | · | · | · | · | killed (selftest only; standing sweep blind) |
| W2 | – | – | – | – | – | – | – | – | – | – | – | – | – | – | – | · | · | · | · | · | · | · | · | · | · | · | · | **SURVIVED** |

(`–` = not applicable: the rekey mutants were not run against wave arms and vice versa.)

## 2. Kill matrix — `rekey-cost.py` × M3

Battery invocation: `python3 -I <copy> --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --arms`.
Selftest invocation: same with `--selftest`. Every arm, both runs:

| arm | planned edit set | pristine measured | M3 measured | kill |
|---|---|---|---|---|
| `sources` | `corpus/SOURCES.md` | 13 ok | 13 ok | · |
| `province` | `PROVINCE.md` | 6 ok | 6 ok | · |
| `quality` | `corpus/QUALITY.md` | 6 ok | 6 ok | · |
| `scorecard` | `SCORECARD.md` | 0 ok | 0 ok | · |
| `pointer` | `tools/pointer-recheck.json` | 0 ok | 0 ok | · |
| `union` | `corpus/SOURCES.md` + `PROVINCE.md` | 17 ok | 17 ok | · |
| `ignored-skill` | `SKILL.md` | 0 ok | **9 UNEXPECTED** | **KILL** |

| selftest arm | pristine | M3 | kill |
|---|---|---|---|
| `arm1-shared-two-sections` | ok (got=2) | ok (got=2) | · |
| `arm2-unpinned-zero` | ok (got=0) | ok (got=0) | · |
| `arm3-oldest-only-not-risk` | ok (got=0) | ok (got=0) | · |
| `arm4-three` | ok (got=1) | ok (got=1) | · |
| `arm5-ignored-skill-zero` | ok (got=0) | **FAIL (got=1)** | **KILL** |
| `arm6-empty-set-setup` | ok (got=setup) | ok (got=setup) | · |
| `arm7-missing-ledger-setup` | ok (got=setup) | ok (got=setup) | · |
| `arm8-union-not-sum` | ok (got=2) | ok (got=2) | · |

```
pristine --arms     : REKEY_ARMS: arms=7 meet=7 unexpected=0   exit 0
M3      --arms      : REKEY_ARMS: arms=7 meet=6 unexpected=1   exit 1
pristine --selftest : REKEY_COST_SELFTEST: 8/8 pass            exit 0
M3      --selftest  : REKEY_COST_SELFTEST: 7/8 pass            exit 1
```

**M3 verdict: KILLED**, by 1/7 battery arms (`ignored-skill`) and 1/8 selftest arms
(`arm5-ignored-skill-zero`). The measured value `9` was re-derived independently of the tool
(§6), so the kill is on the correct value, not on any number the mutants happen to print.

## 3. Kill matrix — `wave-reconcile.py` × {W1, W2}

`python3 -I -X utf8 <copy> --selftest`:

| selftest arm | pristine | W1 | W2 |
|---|---|---|---|
| `arm1-seats-meet` | ok | ok | ok |
| `arm2-seats-mismatch-caught` | ok | **FAIL (got=0)** | ok |
| `arm3-seatreports-drift-measured` | ok | ok | ok |
| `arm4-roles-spec-meet` | ok | ok | ok |
| `arm5-roles-text-drift-measured` | ok | ok | ok |
| `arm6-attack-below-floor-caught` | ok | **FAIL (got=0)** | ok |
| `arm7-attack-at-floor-meet` | ok | ok | ok |
| `arm8-bom-refused` | ok | ok | ok |
| `arm9-invalid-utf8-refused` | ok | ok | ok |
| `arm10-zero-rows-refused` | ok | ok | ok |
| `arm11-unresolvable-rev-refused` | ok | ok | ok |
| `arm12-declaration-absent-refused` | ok | ok | ok |

```
pristine : WAVE_RECONCILE_SELFTEST: 12/12 pass   exit 0
W1       : WAVE_RECONCILE_SELFTEST: 10/12 pass   exit 1
W2       : WAVE_RECONCILE_SELFTEST: 12/12 pass   exit 0   <-- SURVIVOR
```

**W1 verdict: KILLED** by `arm2-seats-mismatch-caught` and `arm6-attack-below-floor-caught` (2/12).
Both are `sweep_exit` arms; `arm3` and `arm5` assert `measure()` alone and are structurally blind
to the verdict step.

**W2 verdict: SURVIVED** all 12 selftest arms.

## 4. Out-of-selftest behaviour: the standing six-row sweep

`python3 -I -X utf8 <copy> --repo <lane> --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json`
(the frozen C1 counter), against `tools/wave-reconcile.json`
sha256 `f09231ad69666beb3b081e296ee44702ccecec4aa411459574cd337f3a1ad4d4`:

| variant | `seat_reports` row detail | summary | exit | stdout sha256 |
|---|---|---|---|---|
| pristine | `printed=11 files=12` | `rows=6 met=6 unexpected=0` | 0 | `fca1143accc6f6543ce8d42deda50dd8b7139b98382318d56140cd425ed52aae` |
| W1 | `printed=11 files=12` | `rows=6 met=6 unexpected=0` | 0 | `fca1143a…` — **byte-identical to pristine** |
| W2 | `printed=11 files=17` | `rows=6 met=6 unexpected=0` | 0 | `150f272556e8f35d7abac1ba54a760585a74607e17f12abfed337edc94b3f5f9` |

Two findings the selftest cannot show:

* **W1 is invisible to the standing counter.** Dropping the `expect` comparison changes no byte of
  the six-row sweep, because all six standing rows already meet their expectation (the two red arms
  are `expect=drift measured=drift`). The standing manifest exercises the comparison zero times.
  W1's only detector in the committed instrument is selftest arms 2 and 6.
* **W2 changes the standing sweep's *detail* but not its *verdict*.** The round-72 wave dir at
  `a3dd3574` holds 12 top-level `*.md` seat reports and 5 nested ones (17 total); the depth clause
  is load-bearing on the number the red arm prints (`files=12` vs `files=17`) and on nothing else,
  because 17 is as far from 11 as 12 is. The row measures "not 11", not "exactly 12".

## 5. Survivor list

| mutant | survived selftest | survived standing sweep | witness required |
|---|---|---|---|
| W2 | 12/12 | yes (verdict unchanged) | §6 probe A |

## 6. Non-equivalence probes (outside the selftest fixtures)

Hermetic fixture repo, `D=$(mktemp -d) && git -C "$D" init -q`, toplevel asserted equal to `$D`
before the first commit (`D=/tmp/tmp.GEasQMIGab`, commits `0719db7f`, `b9c4d790`, `fd6771b1`).
Record `report.md` = `- **The wave**: 12 seats, 12 reports.`; manifest rows bind
`span: "12 reports", printed: 12, expect: meet`.

### Probe A — W2 survivor witness: one nested `*.md` inside the wave dir

12 top-level `wave/T1W1S01.md … T1W1S12.md` **plus** `wave/sub/notes.md`, at `0719db7f`.

```
$ python3 -I -X utf8 stage/pristine/tools/wave-reconcile.py --repo "$D" --manifest out/probe-nested.json
WAVE_ROW nested-md kind=seat_reports expect=meet measured=meet ok | printed=12 files=12
WAVE_RECONCILE: rows=1 met=1 unexpected=0                                     [exit 0]

$ python3 -I -X utf8 stage/w2/tools/wave-reconcile.py --repo "$D" --manifest out/probe-nested.json
WAVE_ROW nested-md kind=seat_reports expect=meet measured=drift MISMATCH | printed=12 files=13
WAVE_MISMATCH nested-md expect=meet measured=drift
WAVE_RECONCILE: rows=1 met=0 unexpected=1                                     [exit 1]
```

Disagreement on identical bytes: pristine `files=12`/exit 0, W2 `files=13`/exit 1. This is the
input class absent from the selftest (no fixture carries a nested `*.md`) **and** from the standing
manifest (its only `seat_reports` row expects `drift`, so any over-count still reads `drift ok`).

### Probe B — attribution control: same repo, nested file removed

`b9c4d790` deletes `wave/sub/notes.md`; 12 top-level `*.md`, nothing else changed.

```
$ python3 -I -X utf8 stage/pristine/tools/wave-reconcile.py --repo "$D" --manifest out/probe-flat.json
WAVE_ROW nested-md kind=seat_reports expect=meet measured=meet ok | printed=12 files=12
WAVE_RECONCILE: rows=1 met=1 unexpected=0                                     [exit 0]

$ python3 -I -X utf8 stage/w2/tools/wave-reconcile.py --repo "$D" --manifest out/probe-flat.json
WAVE_ROW nested-md kind=seat_reports expect=meet measured=meet ok | printed=12 files=12
WAVE_RECONCILE: rows=1 met=1 unexpected=0                                     [exit 0]
```

They agree once the nested file is gone, so probe A's disagreement is caused by the removed depth
clause and not by W2 being broken generally.

### Probe C — W1 delta outside the selftest harness (not required; recorded because W1's verdict kill is selftest-only)

`fd6771b1` deletes one seat report: 11 top-level `*.md`, record still prints 12, row `expect=meet`.

```
$ python3 -I -X utf8 stage/pristine/tools/wave-reconcile.py --repo "$D" --manifest out/probe-short.json
WAVE_ROW short-wave kind=seat_reports expect=meet measured=drift MISMATCH | printed=12 files=11
WAVE_MISMATCH short-wave expect=meet measured=drift
WAVE_RECONCILE: rows=1 met=0 unexpected=1                                     [exit 1]

$ python3 -I -X utf8 stage/w1/tools/wave-reconcile.py --repo "$D" --manifest out/probe-short.json
WAVE_ROW short-wave kind=seat_reports expect=meet measured=drift ok | printed=12 files=11
WAVE_RECONCILE: rows=1 met=1 unexpected=0                                     [exit 0]
```

W1 prints a drifting row as `ok`: that is the always-green cheat the plan's C1 control (i) targets,
reached by deleting the comparison instead of the measurement.

### Independent re-derivation of M3's `measured=9`

Not a tool run: 64 sections from `.ufo/evidence/round-18/measure.py`, newest-entry inputs from the
committed 820-entry ledger, `SKILL.md` membership with and without the three-key filter.

```
pristine IGNORED: SKILL.md-pinning sections = 0
M3 IGNORED=∅   : SKILL.md-pinning sections = 9
  ## Source notes / ## Defect-taxonomy templates and exact-string guidance /
  ## Appendix B — worked example: bash case / ## The cadence's first scheduled tick … /
  ### Boundary readings, executed by this lane / ### Where to enter — four readers /
  ### What stays open — named, never closed by prose /
  ## Promotion-evidence calibration — fleet round-1
```

The battery's `measured=9` under M3 is the correct value for this ledger, and `measured=0` under
pristine is correct (the filter is what makes the arm 0).

## 7. Findings

1. **M3 is killed, and only by the arm added for it.** 1/7 battery arms and 1/8 selftest arms are
   sensitive; the other six battery arms plan no path in the `IGNORED` set, so they are blind by
   construction. The C2 claim "the battery kills M3" is true and rests on a single arm — a
   deliberate single-point by design (`ignored-skill` exists precisely for it), not an accident.
2. **The `expect` comparison is exercised by exactly two arms.** Arms 3 and 5 assert `measure()`
   and never reach the verdict. W1 survives the standing six-row sweep byte-identically
   (stdout sha equal), so the selftest is the only committed detector of a dropped comparison.
3. **The `seat_reports` depth clause is unverified in both directions.** No fixture and no standing
   row pairs a *meet* expectation with a nested `*.md`; the standing red arm cannot tell 12 from 17.
   W2 is therefore a genuine coverage gap, not an equivalent mutant: probe A shows a real
   disagreeing input. Fixing it would be a fixture addition (one selftest arm with a nested report
   and `expect=meet`), which is the L1's contract decision, not mine.
4. Setup arms (BOM, invalid UTF-8, zero rows, unresolvable rev, absent declaration) are orthogonal
   to all three mutants and stay green — no cross-talk observed.

## 8. Lane byte-identity (no production byte touched by this seat)

```
BASELINE (HEAD 17cd1939)                    AFTER (HEAD 3e0ef1c8)
git status --porcelain -- tools/            git status --porcelain -- tools/
 M tools/pointer-recheck.json                (empty)
 M tools/rekey-cost.py
?? tools/wave-reconcile.json
?? tools/wave-reconcile.py

sha256 tools/rekey-cost.py      85ca2b69…  ==  85ca2b69…   (worktree AND HEAD blob)
sha256 tools/wave-reconcile.py  e68947bd…  ==  e68947bd…   (worktree AND HEAD blob)
sha256 tools/wave-reconcile.json f09231ad… ==  f09231ad…   (worktree AND HEAD blob)
```

The status delta is the L1's own commits landing mid-run (`7982619f` C2 battery, `fddbb667` C1
instrument, then record/receipt/erratum commits); HEAD advanced while the two hashes I
mutate-tested did not move, and at the final tip the committed blobs hash to exactly the tested
values with `tools/` clean. No mutation was ever written outside
`/fast/scratch/hyaku/tameshi-r73/T73W1S10/`; the scratch tree (staged pristine copies and mutants)
was deleted before yielding, and the probe fixture repo was deleted after its toplevel was
re-verified. `T73W1S10/mutants.diff` preserves the mutant text.

Restoration note: since the lane was never mutated, restoration is the hash equality above plus the
staged mutant→pristine diffs in `T73W1S10.md` §2, which are one line each in the opposite
direction.
