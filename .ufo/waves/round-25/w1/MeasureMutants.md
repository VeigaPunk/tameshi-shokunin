# Round-25 w1 — MeasureMutants (calibration probe of the C1 counter)

**Item:** mutate `.ufo/evidence/round-25/c1-measure.py` itself (drop the witness check; accept
runner exit 1; skip set equality in R3; skip the negative controls) and run each mutant with
`--repo` against a private clone of the lane at the frozen revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`.
**Verdict:** **no mutant changes the result at this revision.** All four runs are byte-identical to the
pristine run (exit 1, `C1_ROUTED: dispositioned=0/3`). All four therefore mark a check this revision
cannot exercise. Two further probes (private synthetic copies) show which of the four checks become
discriminating once the round-25 artifacts land: **M3 and M1 do; M2 provably cannot; M4 only in a
degenerate fixture.**

---

## 1. Method (all work in private copies; the lane was never written)

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/MeasureMutants-r25
git -C /tmp/MeasureMutants-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df
```

Pristine counter bytes (matches the frozen contract's `measure_sha256`):
`b18460c7ca559c18c354ce29ea4cfe60d78be3ad7c7e41abd321ba74eb1ee8b2` (8213 bytes).

Four mutants, each one exact string replacement, each anchor asserted to occur exactly once
(`/tmp/measuremutants/make-mutants.py`):

| id | disabled check | mutant bytes (sha256) |
|---|---|---|
| M1 | witness check — `c1-measure.py:69` `sorted(witnessed) == sorted(ids)` → `sorted(killed) == sorted(ids)` | `0426d266060826c68877c9ce88cf7479f46ae67cfcd4a4082794a9612f72dd82` |
| M2 | runner exit — `c1-measure.py:68` `run.returncode == 0` → `run.returncode in (0, 1)` | `413063efa3a01db2fc7d093b3da8b8907d5f5079764f051f4e7b6175e3f4a2ab` |
| M3 | R3 row-set equality — `c1-measure.py:76-77` block deleted | `870be8163849611e7a2eb4b872906e57d1f6eb17e5dac0e5be5481aafa16dcf7` |
| M4 | R3 negative controls — `c1-measure.py:112-113` → both `True` | `932a99cf4478a1fa2b9f67464238802efd140803da19da256e7bf1cec1410111` |

Each mutant was written **in place** over the clone's own
`.ufo/evidence/round-25/c1-measure.py`, run, then the pristine bytes were restored and the hash
re-checked after every run (`FINAL_SHA=b18460c7…`, `git status --porcelain` empty). The lane's copy of
the file was read only and is still `b18460c7…`. No git/jj write command was run; no tool was
installed (none was needed).

---

## 2. Evidence — Scenario A: frozen revision `c9ff09fb`, `--repo /tmp/MeasureMutants-r25`

Pristine:

```
$ python3 .ufo/evidence/round-25/c1-measure.py --repo /tmp/MeasureMutants-r25   # 16.4 s
exit=1   C1_ROUTED: dispositioned=0/3
  R23-ROUTED-1  holds=true  runner_exit=0  killed=[M1..M6]  witnessed=[M1..M6]  scorecard_row=false
  R23-ROUTED-2  holds=true  runner_exit=0  killed=[G1..G8]  witnessed=[G1..G8]  scorecard_row=false
  R23-ROUTED-3  holds=false reason="disposition file absent"  scorecard_row=false
```

Mutants (each run: mutate in place → run → restore → hash re-checked):

| mutant | mutated sha | exit | summary line | stdout vs pristine |
|---|---|---|---|---|
| M1 | `0426d266…` | 1 | `C1_ROUTED: dispositioned=0/3` | **byte-identical** |
| M2 | `413063ef…` | 1 | `C1_ROUTED: dispositioned=0/3` | **byte-identical** |
| M3 | `870be816…` | 1 | `C1_ROUTED: dispositioned=0/3` | **byte-identical** |
| M4 | `932a99cf…` | 1 | `C1_ROUTED: dispositioned=0/3` | **byte-identical** |

(`diff -q` of every mutant's stdout against the pristine stdout: identical; stderr 0 bytes for all.)

**Mutants that change the result at this revision: none.**

**Checks this revision cannot exercise (the answer to "list them"):**

1. **witness check** (M1) — every kill at this revision already carries its witness, so
   `sorted(witnessed) == sorted(ids)` is true before and after the mutation. It only bites when a
   defect is killed *without* an explicit `FIXTURE … FAIL` / `CASE … FAIL` line (see §3, scenC).
2. **runner-exit check** (M2) — the runner exits 0 at this revision; and the check is dominated in
   every state (see §3, scenD). It never decides the verdict.
3. **R3 row-set equality** (M3) — never reached: `r3()` returns at `c1-measure.py:102-103` because
   `.ufo/evidence/round-25/dead-falsifier-disposition.json` does not exist at this revision, so
   `disposition_failures()` is never called.
4. **R3 negative controls** (M4) — same short-circuit; the two doctored copies are never built.

**Why the counter reads 0/3 here (two independent masks, both fixable):**

* R1/R2 compute `holds=true` (control green, restore OK, all 14 defects killed and witnessed) but
  `dispositioned = holds AND recorded` (`c1-measure.py:144-148`), and `recorded` is false:
  `SCORECARD.md` at `c9ff09fb` carries **no** `R23-ROUTED-1/2/3` row (`grep -c "R23-ROUTED" SCORECARD.md`
  → 0). The sweeps are green and still count 0.
* R3 has no input file at this revision.

So the counter's *measurement* machinery works at this revision; its *record* side is empty.

---

## 3. Which of the four checks are load-bearing once the artifacts exist

To separate "check is dead code" from "revision lacks artifacts", the same four mutants were run
against four private synthetic copies of the clone (never in the lane). Each copy carries the
round-25 artifacts the counter needs: three `| R23-ROUTED-n |` SCORECARD rows, a
`dead-falsifier-disposition.json` with exactly the 34 dead round-23 wave-2 seats, and one report per
re-attacked seat holding `R23-REATTACK <name>: AGREE|FINDING`.

| scenario | repo state | pristine | M1 | M2 | M3 | M4 | verdict |
|---|---|---|---|---|---|---|---|
| scenB | artifacts present, mixed statuses (20 agree / 5 finding / 9 died) | **3/3** exit 0 | 3/3 | 3/3 | **2/3** | 3/3 | M3 **kills**; M1, M2, M4 inert |
| scenC | scenB + one multitoken defect killed without a witness (mutant hangs at import → suite dies, no `FIXTURE … FAIL` line) | **2/3** | **3/3** | – | – | – | M1 **kills** (witnessed `[M1..M6]` vs killed `[M1..M7]`) |
| scenD | scenB + suite exits 127 on mutant runs → INCONCLUSIVE → runner DEGRADED, **exit 1** | **2/3** | – | **2/3** | – | – | M2 **cannot** kill (runner_exit=1, killed=`[]` ⇒ `witnessed != ids` already) |
| scenE | artifacts present, every one of the 34 seats marked `reattack-seat-died` | **2/3** | – | – | – | **3/3** | M4 **kills** (`flip-one-status` control is False) |

Key readings:

* **M3 / row-set equality — load-bearing.** With the disposition file present, deleting the
  row-set check turns the `drop-one-row` doctored copy into a *passing* copy
  (`negative_controls_fail_as_required: {'drop-one-row': false, …}`), so R3 stops holding:
  3/3 → 2/3. The check is real; it is only unreachable today.
* **M1 / witness check — load-bearing, but only for unwitnessed kills.** On every real fixture state
  measured (frozen revision, live in-flight fixture, scenB) all kills carry a witness, so the check
  is a no-op. It fires exactly on the class it was written for: a mutant that dies the suite without
  printing a FAIL line (scenC, killed `M7`, no witness → pristine 2/3, M1 3/3).
* **M2 / runner exit — provably unable to decide the verdict.** `tools/mutate-and-run.sh:563-566`
  exits 1 **only** when `inconclusive > 0` (DEGRADED). An INCONCLUSIVE defect is never recorded as
  `DEFECT <id>: KILLED`, so it is absent from `killed` and from `witnessed`, hence
  `sorted(witnessed) == sorted(ids)` already fails. The exit gate is therefore *dominated* by the
  witness/kill-set equality: whenever it fails, the witness check fails too. Measured in scenD:
  pristine 2/3 and M2 2/3, byte-identical.
* **M4 / negative controls — load-bearing only in a degenerate fixture.** In a mixed, valid
  disposition both doctored copies fail as required, so forcing them to `True` changes nothing
  (scenB). It fires when the fixture is degenerate: if every row is `reattack-seat-died` there is no
  `reattacked-agree`/`reattacked-finding` row to flip, the `flip-one-status` control cannot fail,
  and R3 can never hold (scenE: pristine 2/3 with
  `negative_controls_fail_as_required: {'drop-one-row': true, 'flip-one-status': false}`, M4 → 3/3).

---

## 4. Live in-flight lane state (read-only snapshot, supplementary)

A read-only snapshot of the lane working tree as of this probe (`/tmp/measuremutants/lane-snap`,
sha256 of the snapshot's own files: `multitoken-mutants.spec 8ec3f56b…`, `guard-mutants.spec
af5b6f6e…`, `multitoken-cases.json f0a4ac80…`, `c1-suite.py ae33a04b…`, `c1-measure.py b18460c7…`,
`SCORECARD.md db139bf3…`) reads:

```
pristine : exit=1  C1_ROUTED: dispositioned=0/3
  R1 holds=true runner_exit=0 killed=[M1..M10] witnessed=[M1..M10] scorecard_row=false
  R2 holds=true runner_exit=0 killed=[G1..G14] witnessed=[G1..G14] scorecard_row=false
  R3 holds=false reason="disposition file absent"
M1/M2/M3/M4: exit=1, stdout byte-identical to the pristine stdout (all four inert)
```

The in-flight fixtures sweep clean (24/24 defects killed, every kill witnessed), so the witness
check does not bite on the real fixture either. The two masks of §2 are still in place: no
`R23-ROUTED-n` SCORECARD row and no disposition file.

---

## 5. Smallest safe corrections (for the L1 integrator)

1. **Land the SCORECARD rows in the pinned shape.** The counter accepts `^\|\s*R23-ROUTED-1\b`
   (`c1-measure.py:144`), but the lane's own pin script requires the stricter
   `^\| R23-ROUTED-%d \|[^\n]*\|$` (`.ufo/evidence/round-25/c1-pins.py:72`) and that the row says
   `dispositioned`. A row written exactly as
   `| R23-ROUTED-1 | dispositioned | <evidence> |` satisfies both. Without it the counter reads 0/3
   even when every sweep is green.
2. **Land `.ufo/evidence/round-25/dead-falsifier-disposition.json`** with exactly the 34 dead
   round-23 wave-2 seats (names taken from `.ufo/waves/round-23/original-outcomes2.json`, status
   `!= 'completed'`); R3 short-circuits without it and never evaluates the row-set or negative-control
   checks.
3. **Keep at least one row in status `reattacked-agree` or `reattacked-finding`.** If all 34 seats
   are recorded as `reattack-seat-died`, the `flip-one-status` negative control cannot fail and R3 can
   never hold — the 3/3 target becomes unreachable (scenE evidence above).
4. **Optional, counter-side:** the runner-exit gate (`c1-measure.py:68`) is dominated by the
   witness/kill-set equality and therefore never decides the verdict. If a discriminating exit
   condition is wanted, assert on the verdict line (`MUTATE: DONE` and `inconclusive=0`) rather than
   on `run.returncode == 0`; no change to the C1 target is implied either way.

Nothing in the counter, the suite, the specs or the lane was changed by this probe; the four mutants
exist only in `/tmp/measuremutants/mutants/` and in the private scenario copies.

---

## 6. Reproduction

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/MeasureMutants-r25
git -C /tmp/MeasureMutants-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df
python3 /tmp/measuremutants/make-mutants.py          # writes the four mutants
bash   /tmp/measuremutants/scenarioA.sh              # scenario A: mutate in place, run, restore
python3 /tmp/measuremutants/build-scenarios.py       # scenB..scenE synthetic copies
bash   /tmp/measuremutants/run-scen.sh /tmp/measuremutants/scenB scenB PRISTINE M1 M2 M3 M4
```

Logs: `/tmp/measuremutants/logs/{A,scenB,scenC,scenD,scenE,lane}-*.json`.
No tool was installed or upgraded for this item (none was needed).
