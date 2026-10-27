# Self-hardening — `mutate-and-run.sh` `--regression` comparator, r6 meta-sweep (TAMESHI-T6-4)

Run date 2026-10-14. Lane: tameshi (round 6, `plans/round-6.plan.md`; assignment
T6-4 — own-gate hardening). Scope: mutation-test tameshi's **own**
`tools/mutate-and-run.sh` `--regression` path at meta level — the mutants are
defects of the **regression comparator itself** — and harden the tool's own
`--selftest` so it kills them. Besides the tool's new selftest cases this is the
only file the lane wrote; every fleet tree was read-only throughout.

Anchors: **O** = observation (command output / file:line), **I** = inference,
**U** = unknown. Line refs without a revision note are R1 (below).

Revisions (O: `sha256sum`, `stat`, `git show HEAD:…`):

- **R1** (pre-hardening) `tools/mutate-and-run.sh` sha256
  `597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b`, 42291 B
  — the revision the round plan's PREP-T6 probe and the round's other kill-rate
  lanes cite; `git show HEAD:tools/mutate-and-run.sh` hashes identical.
- **R2** (post-hardening) sha256
  `b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb`, 46850 B.
  `git diff --stat` vs R1: **83 insertions, 4 deletions** in exactly three
  hunks — the channel note (`:4-7`), the `--selftest` coverage clause
  (`:98-106`), and one +74-line selftest block (rg5–rg9). Sweep, spec-parse and
  comparator code bytes are unchanged; §4 proves comparator behaviour identical
  (probe identity R1 ≡ R2).

## 0. Method and headline

- O: target = the tool itself; suite = `bash "$MUTANT" --selftest`; six defects,
  one exact edit each, all inside `regression_case` (the `--regression`
  comparator). Spec: `/tmp/w6-t6-4-meta/spec-meta-regression.spec` (§7). Every
  `@old` string occurs exactly once on both revisions — asserted by the tool
  before any suite run.
- O: prediction, from static reading of `regression_case` and the r4-2 fixture
  set **before sweep A ran** (the coverage-gap reading is in the lane's opening
  update): all six survive — the r4-2 fixtures exercise only all-match PASS,
  two-flip FAIL, pin-mismatch SETUP, missing-target SETUP; no band edges, no
  absent-row accounting, no rc=1 sweep, no asymmetric table.
- O headline, **sweep A (R1)**: `CONTROL: GREEN`; **0/6 killed — 6/6
  survived**; `MUTATE_RESTORE: OK`; `MUTATE: DONE (target=mutate-and-run-r1
  defects=6 killed=0 survived=6 inconclusive=0 kill-rate=0%)`, exit 0; full log
  `/tmp/w6-t6-4-meta/sweepA.log`, evidence `…/sweepA/evidence/`.
- O headline, **sweep B (R2)**: `CONTROL: GREEN`; **6/6 killed — kill-rate
  100%**; `MUTATE_RESTORE: OK`; exit 0; log `/tmp/w6-t6-4-meta/sweepB.log`.
  Every FAIL check in every kill is a **new** rg5–rg9 label (§3); the 37
  pre-r6 checks pass in all six mutant runs.
- O: tool selftest count 37/37 (R1) → **55/55** (R2), `VERDICT: PASS`, exit 0
  both (`/tmp/w6-t6-4-meta/selftest-R{1,2}.out`).
- O: `--regression` on R2 at the recorded fleet pins → `REGRESSION: PASS`
  (`cases=2 passed=2`; js `83016d45049b…`, bash `275d8294a94e…`; each case
  `match=10/10`, 80 %) — the r6 edit did not disturb the fleet gate.

## 1. Sweep A — kill-rate table (pre-hardening)

Each mutant = fresh copy of the pinned R1 pristine, one exact edit; verdicts
and shas from `…/sweepA/results.tsv`; all runs 2323–2335 ms, none inconclusive.

| # | defect class | injected edit (R1 site) | predicted | measured | exit | mutant sha256 (short) |
|---|---|---|---|---|---|---|
| M1 | band edge (flips) | `(( flips > BAND_FLIPS ))` → `>=` (:683) | survived | **SURVIVED** | 0 | `64b6683de371` |
| M2 | band edge (killed-delta) | `(( delta > BAND_KILLED ))` → `>=` (:682) | survived | **SURVIVED** | 0 | `073656399183` |
| M3 | dropped accounting arm | level-B loop deleted — recorded entries absent from the measurement stop counting (:663-672) | survived | **SURVIVED** | 0 | `8a9241612acb` |
| M4 | weakened count check | `(( total != exp_total ))` → `(( total < exp_total ))` (:685) | survived | **SURVIVED** | 0 | `027cc85a22d5` |
| M5 | rc-class handling | `if [[ $rc -ne 0 && $rc -ne 1 ]]` → `if [[ $rc -ne 0 ]]` (:628) | survived | **SURVIVED** | 0 | `7879bfa90b66` |
| M6 | wrong reference column | `exp_killed=$(table_count "$table" KILLED)` → `SURVIVED` (:676) | survived | **SURVIVED** | 0 | `4c55fff91e65` |

- O: prediction and measurement agree — first meta-sweep kill-rate 0 %; control
  ran the full selftest in 2342 ms; target bytes held (restore proof above).
- I: the r4-2 regression fixtures were written against the comparator's happy
  paths; the boundary and accounting arms of the stated band contract (R1
  header :78-83) were never themselves under test. §2 shows each survivor is a
  real verdict/accounting hole, not an equivalent mutant.
- I: `delta > BAND_KILLED` is subsumed by `flips > BAND_FLIPS` while
  `BAND_KILLED <= BAND_FLIPS` — every row that moves the killed count is also a
  flip, so `|Δkilled| <= flips`; with the shipped 1/1 bands the delta arm can
  only add a reason string, never change a verdict. M2's survival is consistent
  with this; the arm stays valid defense-in-depth if the bands are ever made
  asymmetric (U: not measured this round).

## 2. Survivor probes — non-equivalence, measured

Harness (O): probe copy of a revision = every line up to `# ---- main` plus a
driver that calls `regression_case` on the selftest's own fixture — fixtures
extracted byte-identically from the tool, sub-sweeps run through the intact
revision (`PROBE_SELF`). Outputs `/tmp/w6-t6-4-meta/probe/out-{R1,R2,M1..M6}.txt`,
diff summary `…/probe/summary-probes.txt`. (O: a first probe build reused one
shared head for all revisions and produced six identical outputs; discarded and
rebuilt per revision — recorded here so nobody re-uses that first pass.)

Five scenarios: `boundary` (recorded `K:KILLED,S:KILLED` — the at-band 1-flip
measurement), `recorded-absent` (recorded `Z` unmeasured), `measured-absent`
(table lacks measured `S`), `degraded` (hang suite → sweep rc=1), `all-killed`
(strict suite → fully-matching all-killed table). Measured R2 behaviour vs each
mutant (abridged to the differing lines):

- **M1** (flips `>=`): `boundary` R2 `PASS (band: …)` → M1 `FAIL (out of band:
  flips=1)`, exit 1. Reason strings also gain `flips=1` in `measured-absent`
  and `degraded`.
- **M2** (delta `>=`): `boundary` R2 `PASS` → M2 `FAIL (out of band:
  killed-delta=1)`; `degraded` reason gains `killed-delta=1`.
- **M3** (loop deleted): `recorded-absent` loses `REGRESSION_DEFECT fixture Z:
  measured=ABSENT recorded=KILLED`; TABLE `flips=2` → `flips=1`; FAIL reason
  loses `flips=2`.
- **M4** (count weakened): `measured-absent` R2 `FAIL (out of band:
  defects=2-recorded=1)`, exit 1 → M4 **`PASS (… defects=1)`, exit 0** — an
  over-count escapes entirely.
- **M5** (rc class): `degraded` R2 emits the inconclusive row + TABLE +
  `FAIL (out of band: inconclusive=1)` → M5 `FAIL (sweep exit=1, expected 0 or
  1)` with no table comparison — a DEGRADED sub-sweep is misreported as an
  engine error.
- **M6** (wrong column): `recorded-killed` reported as `0` in every scenario
  (`boundary`: `2` → `0`); `all-killed` R2 `PASS` → M6 `FAIL (out of band:
  killed-delta=2)`; `recorded-absent` reason loses `killed-delta=2`.

### 2.1 Supplementary probe A7 (outside the six-defect sweep)

- O: one extra mutation — `[[ $delta -lt 0 ]] && delta=$((0 - delta))` deleted
  (signed delta) — probed the same way: verdicts identical in all five
  scenarios; the only measured difference is the `recorded-absent` FAIL reason
  dropping `killed-delta=2`. Its own selftest exits 1, killed by exactly one
  check: `unmeasured-entry FAIL line exact` (rg6's exact-reason assertion).
- I: consistent with the §1 subsumption argument — under 1/1 bands the abs line
  is verdict-equivalent, observable only in reason strings, and rg6 covers it.
  A7 is **not** part of the six-defect sweep; no table row is claimed for it.

## 3. Hardening (R2) — the five new cases and the kill proof

Edit scope (O): one contiguous block in `selftest()` after the r4-2 regression
fixtures — fixtures + rg5–rg9 + one fixture-byte-identity assertion = **18 new
checks** (17 `st` assertions + 1 identity), 37 → 55. New fixture
`suite-strict.sh` (asserts both the add() result and the banner string). No
comparator, spec, or sweep code touched; `VERSION` left at r4-2 deliberately
(scope: selftest cases and their doc lines only).

Cases, each keyed to the survivor it closes (asserted lines are the ones
measured in §2):

| case | scenario | closes |
|---|---|---|
| rg5 `…/edge` | at-band 1-flip / killed-delta 1 must PASS; PASS + TABLE lines exact | M1, M2 (also M6: `recorded-killed=2` pinned) |
| rg6 `…/unmeasured` | recorded entry the measurement lacks → FAIL; `measured=ABSENT recorded=KILLED` line + exact FAIL reason | M3 (also A7) |
| rg7 `…/unrecorded` | measured row the table lacks → FAIL; `recorded=ABSENT` line + TABLE + exact FAIL reason | M4 |
| rg8 `…/degraded` | DEGRADED sub-sweep (rc=1) table-compared → FAIL; inconclusive row + TABLE + `inconclusive=1` | M5 |
| rg9 `…/all-killed` | fully-matching all-killed table → PASS; `recorded-killed=2` + PASS line exact | M6 |

- O sweep B (R2, same spec): `MUTATE: DONE (target=mutate-and-run-r2 defects=6
  killed=6 survived=0 inconclusive=0 kill-rate=100%)`, exit 0, control 4651 ms,
  per-defect runs 4630–4660 ms, restore OK.
- O per-defect kill attribution (`…/sweepB/evidence/<id>.out`, FAIL labels; run
  exits all 1; 49–53 of 55 checks still pass per run — M6 fires six new-case
  checks, the rest 2–4):

| # | FAIL checks that fired (all new labels) |
|---|---|
| M1 | band edge (1 flip / killed-delta 1) still PASSes; band-edge PASS line exact; unrecorded-row FAIL line exact; degraded-sweep FAIL line names inconclusive=1 |
| M2 | band edge (1 flip / killed-delta 1) still PASSes; band-edge PASS line exact; degraded-sweep FAIL line names inconclusive=1 |
| M3 | unmeasured recorded entry named (measured=ABSENT); unmeasured-entry FAIL line exact |
| M4 | measured row the table lacks FAILs; unrecorded-row FAIL line exact |
| M5 | degraded sweep names the inconclusive row; degraded-sweep FAIL line names inconclusive=1; degraded-sweep table line exact |
| M6 | band-edge table line exact; unmeasured-entry FAIL line exact; unrecorded-row table line exact; all-killed table (full match, zero flips) PASSes; all-killed table line exact (recorded-killed=2); all-killed PASS line exact |

- O: in every mutant run the 37 pre-r6 checks pass — the r4-2 fixtures never
  saw these defects and still do not; every kill is attributable to the new
  cases only.

## 4. Verification chain (re-run end-to-end)

- O: `bash -n` clean on R2; selftest runs exit 0 (37/37 and 55/55).
- O: **probe identity** — the same five scenarios through stripped R1 and R2
  give byte-identical output modulo workdir paths (`diff` empty). The edit
  changed the selftest only, not the comparator.
- O: `--regression` on R2 over the pinned fleet artifacts → `REGRESSION: PASS`,
  `match=10/10` per case at 80 % per case, exit 0, 18.8 s; kumitate/kagi
  porcelain-clean for the pinned paths; live sha256 == recorded pins
  (`83016d45…`, `275d8294…`). Evidence `…/regression-R2.log` + workdir.
- O: fixture byte-compare — the probe fixture set equals the tool's own
  extracted selftest fixtures (all five files; `suite-strict.sh` was re-synced
  from R2 after a comment-wording diff was found, then all probes re-run).

## 5. Findings and recommendations

- O: a gate's own selftest pinned only the happy path of its stated band; six
  single-edit comparator mutants survived, two of them verdict-changing (M4
  lets an over-count escape; M6 mis-reads the band's reference count).
- O: after hardening all six are killed, exclusively by the new cases, with
  per-defect sweep evidence (mutant sha, exit, FAIL labels).
- I: the same gap class is likely in sibling gate selftests — a gate's tests
  are typically written against the implementation's happy path. Recommendation
  for the round-6 service contract (`fleet-suite-census.md` queue): when a
  sibling gate is swept, the survivor-hardening step should add *boundary,
  absent-row, DEGRADED-rc and asymmetric-table* cases before a kill-rate is
  published. Kept a recommendation, not a general claim (PROVINCE two-lane bar).
- O for round coordination: the tool revision moved R1 → R2 mid-round
  (`597e1419…` → `b56c6e57…`). `REGRESSION_TOOL` records the tool sha, the
  `--regression` contract is unchanged (§4 probe identity, fleet `REGRESSION:
  PASS`); lanes citing the tool sha should cite R2 from here on.
- O: no sibling tree was written; tameshi's own porcelain shows only
  `tools/mutate-and-run.sh` modified plus this note.

## 6. Unknowns

- U: six defects sample the comparator's mutation space; no completeness claim.
  Static reading suggests the `control-not-green` / `restore-not-ok` reason
  arms are unreachable through the sweep (red control or restore drift exits 2
  → `regression_case` returns SETUP before the comparison), making their
  mutants equivalent-in-practice — **not probed this round**.
- U: band interiors beyond the edges (e.g. `BAND_FLIPS < BAND_KILLED`
  configurations) unmeasured; the shipped bands are 1/1.
- U: the new cases pin the fixture's 2-defect scale; fleet-scale (10-defect)
  band behaviour is covered by the fleet pins only at exact match.

## 7. Reproduce

```sh
# sweep A (R1) / sweep B (R2) — same spec, target = the tool itself
cd tameshi-shokunin
bash tools/mutate-and-run.sh --target tools/mutate-and-run.sh \
  --defects /tmp/w6-t6-4-meta/spec-meta-regression.spec \
  --suite 'bash "$MUTANT" --selftest' \
  --workdir /tmp/w6-t6-4-meta/sweepA --label mutate-and-run-r1 --timeout 120
bash tools/mutate-and-run.sh --target tools/mutate-and-run.sh \
  --defects /tmp/w6-t6-4-meta/spec-meta-regression.spec \
  --suite 'bash "$MUTANT" --selftest' \
  --workdir /tmp/w6-t6-4-meta/sweepB --label mutate-and-run-r2 --timeout 120

bash tools/mutate-and-run.sh --selftest                       # 37/37 (R1) · 55/55 (R2)
bash tools/mutate-and-run.sh --regression \
  --workdir /tmp/w6-t6-4-meta/regression-R2                   # REGRESSION: PASS
```

Spec `/tmp/w6-t6-4-meta/spec-meta-regression.spec` (the six defects; `@old`
strings cut from the pinned revision, count==1 asserted by the tool):

```
@defect M1 | band: flips boundary strict (>= instead of >) — an at-band 1-flip case must PASS
@old   (( flips > BAND_FLIPS )) && reasons="$reasons flips=$flips"
@new   (( flips >= BAND_FLIPS )) && reasons="$reasons flips=$flips"

@defect M2 | band: killed-delta boundary strict (>= instead of >) — a 1-off killed count must PASS
@old   (( delta > BAND_KILLED )) && reasons="$reasons killed-delta=$delta"
@new   (( delta >= BAND_KILLED )) && reasons="$reasons killed-delta=$delta"

@defect M3 | band: recorded-entry-absent accounting dropped (level-B loop removed)
@old   for pair in ${table//,/ }; do\n    eid=${pair%%:*}\n    case " $seen " in\n      *" $eid "*) ;;\n      *)\n        flips=$((flips + 1))\n        diffs+="REGRESSION_DEFECT $name $eid: measured=ABSENT recorded=${pair#*:}"$'\\n'\n        ;;\n    esac\n  done\n
@new

@defect M4 | band: over-count ignored (total != recorded weakens to total < recorded)
@old   (( total != exp_total )) && reasons="$reasons defects=$total-recorded=$exp_total"
@new   (( total < exp_total )) && reasons="$reasons defects=$total-recorded=$exp_total"

@defect M5 | sweep rc=1 (DEGRADED, inconclusive) rejected as an engine error instead of table-compared
@old   if [[ $rc -ne 0 && $rc -ne 1 ]]; then
@new   if [[ $rc -ne 0 ]]; then

@defect M6 | band: recorded-killed reference read from the SURVIVED column of the recorded table
@old   exp_killed=$(table_count "$table" KILLED)
@new   exp_killed=$(table_count "$table" SURVIVED)
```

Probes: strip a revision at `# ---- main`, append `/tmp/w6-t6-4-meta/probe/driver.txt`,
run with `PROBE_SELF` = the intact revision, `PROBE_FX` = the extracted
fixtures, `PROBE_SHA` = the fixture target's sha256; diff outputs per mutant.