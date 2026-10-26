# T50W2CritScorecard — round-50 SCORECARD section review (candidate `80ea77e99e239982ab0b93e416645ef2359725d3`)

Seat: T50W2CritScorecard (critic, leaf). Scope: the round-50 SCORECARD section — standing axis
table, claims table, and the `**Planned (round 51):**` paragraph. Base `e3729de8`; freeze
`cdbf24c0`; control-commit `f87910f`. All SCORECARD line numbers are at the candidate revision
(`git -C <lane> show 80ea77e9:SCORECARD.md`). All file reads at revisions named. No counter was
run as a verdict; the only probe is the cold-read monitor at base (receipt
`T50W2CritScorecard.coldread-base.json` alongside this file), a no-harm child, not a claim counter.

## 1. Standing axis table (lines 2416–2424) — PASS

- Values vs base monitor `before/no-harm-at-base.stdout` (exists at candidate; `git cat-file -e`
  OK; content verified):
  - depth 9 (line 2422) == `NOHARM commandD recorded_cases=9 depth_score=9 ok` ✓
  - calibration 8 (line 2423) == `NOHARM coldread-floor score=8 credited=64 ok`; the quoted
    strings `calibration_restraint_score=8` and `sections_covered=64` of 64 reproduce exactly the
    cold-read measure's own output at base (probe: `python3 .ufo/evidence/round-21/coldread/measure.py
    --repo <lane> --rev e3729de8` → `"calibration_restraint_score": 8`, `"sections_covered": 64`,
    `"sections_total": 64`; receipt w2/T50W2CritScorecard.coldread-base.json) ✓
  - freshness 9 (line 2424) == `NOHARM r45-freshness population=73 fresh=71 …`; floor(10·71/73)=9 ✓
- `Measured commit` = `e3729de8` (base) on all three rows ✓.
- `Last-change round` 49 / 48 (restated): base round-48 standing rows read depth 9, calibration 6,
  freshness 9, all restated at 48 (`git show e3729de8:SCORECARD.md`); the round-49 section at base
  states `calibration 8 (was 6)` in prose only. The new table's calibration 8 / 49 is the first
  table-level move; the prose at line 2418 discloses this exactly ✓.
- Append-only: `git diff e3729de8 80ea77e9 -- SCORECARD.md` = 23 insertions at the tail, 0
  deletions; nothing above is rewritten ✓.

## 2. Claims table (lines 2428–2429) vs contract and control receipts — PASS (numbers), one wording note

- C1 row: `missing=49 … C1_R50_PASS=false` matches `control/c1-CTL_0.stdout` (`defects=49 rows=0
  … missing=49 … C1_R50_PASS=false`); target `total=0` = contract `claims.C1.target`; counting
  command byte-identical to `claims.C1.command`; controls cell numbers match the committed receipts:
  CTL_OPEN false, CTL_PLANOPEN false, CTL_DECLINE false, CTL_FAB `fixed=40 fixed_this_round=2
  total=5` false (`c1-controls.stdout` last line).
- C2 row: `total=23 C2_R50_PASS=false` matches `control/c2-CTL_ABSENT.stdout`; F6 `open` at
  `corpus/README.md:83` verified at base; controls cell numbers match: CTL_IDENTITY `ok=0 total=20`
  false, CTL_REF `ok=20 units 164→43 total=0` true (`c2-controls.stdout`).
- Note (wording, not a number): C1's controls cell says CTL_FAB is false "only through the
  after-base floor"; the receipt shows `evidence_bad=2` (R40.2/R41.7 empty-evidence) as a second
  failing term. This mirrors the frozen contract prose (`contract.json:42`) and changes no quoted
  figure; disclosed in T50RevControls M1.

## 3. Planned (round 51) paragraph (line 2433) — seven ids PASS; wave-1 carry-overs incomplete

### 3a. Ledger ids — PASS
Exactly the seven open ids in `corpus/routed-defects.json` at candidate (statuses: 31 fixed, 11
declined, 7 open; open = R45.1, R45.4, R46.2, R47.5, R48.4, R49.3, R49.5) are named, and no
other id is. Line 2433 is the newest `**Planned (round` paragraph in the file (`grep -n
'\*\*Planned (round'` → last hit at 2433).

### 3b. Wave-1 left-open items — gaps
The paragraph carries the successor C1/C2 counters and several specific forgery routes (judge bytes
out of the shrinker's reach; run log outside its directory; typed and bounded output reads;
per-row disposition attested by a seat other than the ledger's author), plus the 19 unread citation
forms (`bda60768`, T50ExecSuccC1) and the ledger class field + recurrence clause. But it does not
carry all of what wave 1 left open:

1. **R48.4's append-only rule ask is dropped.** R48.4 is compound (six asks per its ledger row
   note); the parenthetical at line 2433 names five — brace_depth_at helpers, round-47 survivor
   cases, S205/F7 candidates, six-leg class, located-name check — but not the *append-only rule
   for landed seat reports*, which was explicitly planned at base (SCORECARD.md:2380, amended) and
   is confirmed still open by T50ExecAppendOnly.md:257. A round-51 plan that omits one ask of an
   id it declares open under-plans that id.
2. **Generator reach is dropped.** `Planned (round 50)` at base (line 2410) names "generator reach
   (5-cell rows, duplicate map keys, numeric order past the digit boundary)"; it is neither worked
   this round (no ledger row or round-50 section text addresses it) nor carried into line 2433.
3. **Deciding-run harness findings are not carried.** T50RevDeciding F1/F2 (medium): five no-harm
   children + the precheck child still execute working-tree bytes (four r45/46/47 measures absent
   from FROZEN, "working tree must be clean" unenforced), and pre-counter verification failures
   burn the single deciding invocation. No round-51 plan item names either.
4. **SentinelShrink decide-voiding hazards are not carried.** T50SentinelShrink F4 (lone surrogate
   in `out.json` crashes the counter mid-run → void deciding run), F5 (frozen generator re-executed
   unverified; the N−1 margin hides a poisoned copy), F7 (shrinker unsandboxed; no post-run lane
   witness) are not named. F1/F2/F6/F8 are covered by the three named routes; F4/F5/F7 are not.
5. **C2 critic corrections 3–5 are not carried.** T50CritC2Contract: document unit granularity and
   degenerate-empty minima in the README/interface; add a scope qualifier to the F6 README line;
   broaden future hidden panels across generators/seeds/selection. None appears in line 2433.
6. **C1 critic F3/F4 are not carried.** T50CritC1Contract: key design (11 shared keys, R49.5's
   `carried` key = an ACK word, path-suffix matches) and floor calibration (fixed≥20 below the
   40/49 historical saturation) are successor-counter design inputs not reflected in the plan.
7. **Other wave-1 carry-overs not named:** T50ConnCrossClaim's proposed criterion (REV generator
   agreement), T50ExecLogger B1/B3 latent risks, T50MutC2Counter's 12 selftest-coverage gaps
   (m01/m26/m28), T50ScoutB5's B5-not-discharged next moves, and T50ScoutPlanned's no-id open
   items still unplanned after rounds 40–45 (cmp/git-diff lattices, whole-set staged adoption map,
   guard refusal classes, r46 C3/driver survivors, S169/S161/S162, r35 residue).

Observation (not a plan item): T50RevControls H2 — R40.2/R41.7 have no keyed line in any allowed
path at the candidate; C1 becomes satisfiable only if new round prose carries their keys, which is
exactly the fabrication lever H1 describes. The wave-2 per-row semantic attack is the standing
mitigation, not a planned fix.

## Commands / evidence
- `git -C <lane> show 80ea77e9:SCORECARD.md | nl -ba | sed -n '2416,2433p'`
- `git -C <lane> diff e3729de8 80ea77e9 -- SCORECARD.md` (23 insertions, 0 deletions)
- `git -C <lane> show 80ea77e9:corpus/routed-defects.json` (49 rows; 31/11/7; seven open ids)
- `git -C <lane> show e3729de8:corpus/README.md | nl -ba | sed -n '80,86p'` (F6 line 83 open)
- `cat <lane>/.ufo/evidence/round-50/before/no-harm-at-base.stdout`
- `cat <lane>/.ufo/evidence/round-50/control/{c1,c2}-*.stdout` (numbers quoted above)
- cold-read base probe → `T50W2CritScorecard.coldread-base.json` (in this dir)
- Wave-1 reports read: T50CritC1Contract, T50CritC2Contract, T50RevDeciding, T50RevControls,
  T50SentinelShrink, T50ScoutPlanned, T50ScoutB5, T50ExecSuccC1, T50ExecAppendOnly,
  T50ExecLogger, T50ConnCrossClaim, T50MutC1Counter, T50MutC2Counter, T50ScribeConsider,
  T50RevengerRecur, T50ConnSiblingDefects (findings cited with their seat names).

## Summary
- Standing table: all three values (9/8/9) equal the base monitor outputs; quoted monitor strings
  reproduce the cold-read measure at base; the diff is append-only (23 insertions, 0 deletions).
- Claims table: every quoted number matches the committed control receipts and the contract;
  counting commands identical; one wording nit (CTL_FAB "only through the after-base floor"
  omits evidence_bad=2, mirroring contract prose).
- Planned (round 51): names exactly the seven open ledger ids and the successor counters with the
  main forgery routes, the 19 unread citation forms, and the class/recurrence clause.
- Gaps: wave-1 carry-overs not planned — R48.4's append-only-seat-report ask, generator reach,
  deciding-run F1/F2, sentinel F4/F5/F7, C2 corrections 3–5, C1 F3/F4, and the scout's no-id
  open items.
- No verdict on C1/C2; no counter run as a verdict; lane untouched except this report and its
  cold-read receipt.
