# T49W2RevScorecard — SCORECARD.md / LOG.md additions review at `f181a961`

Seat: wave-2 falsifier, round 49 (hyaku run 9). Item: review the round's SCORECARD.md and LOG.md additions at
`f181a961ae44061af486f600e5ea257d2baf78f8` against base `8ca67421111fa354b47b803358391d0b07fc6db9`:
append-only, every pointer resolves, every number matches a committed receipt, no after-value asserted before the
deciding run, capability row conditioned on the deciding receipt. I did not author what I attack. No claim is decided
here; I ran no counter (not even `--selftest`) — every value below was read from committed receipts or recomputed from
committed source bytes. Bounds kept: lane read-only; the three c2 control stdouts that name the hidden panel
(`c2-WITNESS.stdout`, `c2-CTL_FIX.stdout`, `c2-CTL_ABSENT.stdout`) and the combined `c2-controls.stdout` were never
opened (existence and blob ids only); nothing under `~/.local/state/` touched; no tool installed (none needed).

## Item checks

**1. Append-only — PASS.**
`git diff 8ca67421 f181a961 --numstat -- SCORECARD.md LOG.md` → `13 0 LOG.md`, `15 0 SCORECARD.md` (zero deletions).
Both hunks sit at end-of-file (SCORECARD `@@ -2378,3 +2378,18 @@`, LOG `@@ -2379,3 +2379,16 @@`), so the additions are
appended, not spliced. The round-48 correction's own claim "nothing above is rewritten" (SCORECARD.md:2384) holds.

**2. Every pointer resolves — PASS** (two by-design forward pointers noted in OBS-2).

| Pointer (addition line) | Resolves | Shown by |
|---|---|---|
| `14d03ea4…` freeze, `freeze.json` (SCORECARD.md:2388, LOG.md:2385) | yes | `git cat-file -t 14d03ea4…` → commit; `git show 14d03ea4:.ufo/evidence/round-49/freeze.json` prints the digest block; `git merge-base --is-ancestor 14d03ea4 6885adb4` and `… 6885adb4 f181a961` both succeed |
| `6885adb4…` controls commit (SCORECARD.md:2388, LOG.md:2385) | yes | same merge-base checks; `git diff-tree -r 6885adb4` contains all 11 control receipts |
| `8ca67421…` base (SCORECARD.md:2388) | yes | `git cat-file -t` → commit; CTL_0 receipt prints `rev=8ca67421…` |
| `contract.json`, `amendments: []` (SCORECARD.md:2388) | yes | read; `"amendments": []` |
| `control/c1-CTL_0.stdout`, `control/c1-controls.stdout` (SCORECARD.md:2392) | yes | `git show f181a961:.ufo/evidence/round-49/control/<f>` |
| `control/c2-CTL_ABSENT.stdout`, `control/c2-controls.stdout` (SCORECARD.md:2393) | exists; content not opened (bounds) | `git ls-tree -r f181a961 -- .ufo/evidence/round-49/control/` lists both; blob ids identical to 6885adb4's |
| `corpus/README.md:87` F10 `open` (SCORECARD.md:2393, LOG.md:2387) | yes | `git show 8ca67421:corpus/README.md \| sed -n '87p'` → the F10 row, status `open`; unchanged at f181a961:87 |
| `monitor-at-base-8ca67421.json` (LOG.md:2387) | yes | json contains `"calibration_restraint_score": 6` and `"credited": 57` |
| `.ufo/waves/round-49/w1/T49RevengerLapse.md` (LOG.md:2387) | yes | exists; lapse archaeology for the seven sections |
| `corrections.json`, `reads.json`, `refresh.py`, `coldread/` (LOG.md:2389) | yes | all in `git ls-tree -r f181a961 -- .ufo/evidence/round-49/c1/`; `coldread/` holds `refresh-receipts.json` + `traces/section-1..7.json` |
| `tools/pbt-staged-id.py`, `tools/staged-id-guard.py` (LOG.md:2390, SCORECARD.md:2393) | yes | both in tree; `git diff --quiet 8ca67421 f181a961 -- tools/staged-id-guard.py` quiet (guard never edited) |
| rows S269, S270 (LOG.md:2390) | yes | `corpus/SOURCES.md:144-145` at f181a961: both `mined`, opened `2026-10-26`; S270 anchor `§2.10 Generating Test Data, p. 34`; correction note at `:494` |
| `corpus/knowledge/pbt-generator-pilot.md` (LOG.md:2390) | yes | cites S269/S270 "opened 2026-10-26"; defers measured values to `after/c2.stdout` |
| README F10 line conditioned on the deciding receipt (LOG.md:2390) | yes | `corpus/README.md:599`: held "conditioned on the round-49 deciding receipt `.ufo/evidence/round-49/after/c2.stdout` printing `C2_R49_PASS=true`; if it does not, this line is void and an erratum below says so" |
| QUALITY 99, deciding-run gate 0 (LOG.md:2391) | yes | `corpus/QUALITY.md:1446` "Criterion 99 — a control is scored and committed before the deciding run…"; `deciding-run.sh` gate 0 implements exactly the refusals criterion 99 names (missing receipt / not-after-freeze / second invocation, exit 3, nothing run) |
| `considerthese/2026-10-26.md` proposal 3 (LOG.md:2391) | yes | lane file exists at f181a961; line 80: "3. **Recurring-defect tracker for closures.**" |
| lesson Gate counts (LOG.md:2391) | yes | `corpus/lessons/round-49.md` Gate: Admit S269, Admit S270, Reject ×2, Deferred ×1 |
| round-48 spot-check defect 5 (SCORECARD.md:2384) | yes | lesson `:118` routed-defects item 5 names the same correction; conformance defect 5 is the "pasted byte-exact" sentence it fixes |
| saturation line 8 (SCORECARD.md:2388) | yes | standing convention: `round-40/contract.json` `"saturation_line": 8`; rounds 45–48 contracts carry the identical "does not fire … below the saturation line 8" sentence |

**3. Every number matches a committed receipt — PASS** (one bounds-imposed gap, GAP-1).

| Number (line) | Receipt | Result |
|---|---|---|
| C1 Before `sections=64 covered=57 score=6 durable_covered=57/64 pointers=90 unresolved=9 unverified=81 total=105` (SCORECARD.md:2392) | `control/c1-CTL_0.stdout` last line | byte-identical fields, `C1_R49_PASS=false` |
| CTL_J `durable_covered=60/64 total=94` false; CTL_K `unresolved=2 total=2` false; CTL_K2 `total=0` true (SCORECARD.md:2392) | `control/c1-controls.stdout` | byte-identical on every quoted field, exits 1/1/0 |
| pointers=90 (LOG.md:2389, SCORECARD.md:2392) | `control/c1-pointers-at-base-8ca67421.json` | `pointers 90`, `missing_headings []` |
| 57 of 64 sections, score 6 (LOG.md:2387) | `monitor-at-base-8ca67421.json` | `"credited": 57`, `"calibration_restraint_score": 6` |
| 45 line-neutral corrections (LOG.md:2389) | `c1/corrections.json` | `corrections`=44 + `corrections_pass2`=1 = 45; `not_applied`=2 (both outside the seven sections, routed to a later round — honestly recorded in the file); line-neutral confirmed: SKILL.md is 2136 lines at base and at f181a961; pass2 applied (`SKILL.md:221` now reads `:252-254`) |
| 18 reader seats / 7 section critics / 3 command re-runs (LOG.md:2389) | `c1/readers.json` + w1 tree | T49Read01–18, T49Sec{Recipe,Restore,Map,Promotion,R12,R13,R14}, T49Exec{R12,R13,R14}Cmd — all reports present |
| 55 w1 seats (LOG.md:2392) | `spec-w1.json` / `w1-dispatch.json` | `items`=55, `counts` `{"spawn": 55, "resume": 0, "total": 55}` |
| `generator=absent total=25` (SCORECARD.md:2393) | `c2-CTL_ABSENT.stdout` (bounds-forbidden) | corroborated by arithmetic from the frozen counter source: `c2/measure.py` sets `absent=1` when the generator blob is missing, skips pristine (`pristine_bad=0`), all 12 class counts stay 0 → `classes_short=12`, `confirmed=0` → shortfall `max(0,11-0)=11`, and at the freeze tree the pilot entry is absent → `records_bad=1`; total = 1+0+0+12+0+11+1 = **25** |
| 14 selftest fixtures (SCORECARD.md:2393) | `control/c2-fixed-fixtures.json` | list of 14 |
| seed 4949 / 400 cases / 12 classes ≥ 10 / ≥ 11 of 12 (SCORECARD.md:2393) | `contract.json` | identical values |
| 19 capability rows, 3 axis rows (SCORECARD.md:2384) | base SCORECARD tables | programmatic count: last capability table (base line 2330) = 19 rows; last axis table (line 2352) = 3 rows, each ending `runs 3 stable`; the emit's axis branch (`round-48/calibration/measure.py` `emit_row`, `EMIT_AXIS | … | <prose>, tool sha256 …, deps …, runs 3 … |`) corroborates the correction's mechanism claim |
| witness_confirmed=12 (SCORECARD.md:2393) | `c2-controls.stdout` (bounds-forbidden) | corroborated only by the `6885adb4` commit message ("witness 12/12") and contract WITNESS "all 12" — see GAP-1 |

Receipt integrity: all 11 control receipts under `control/` have identical blob ids at `6885adb4` and `f181a961`
(`git rev-parse <rev>:<path>` pairs) — nothing was edited after the controls commit. `freeze.json` digests verified
against the freeze tree: `contract.json` → `d8fb1ad2…`, `c1/measure.py` → `a055e929…` (the value the CTL lines print as
`self=`). All 14 frozen paths are unchanged freeze→candidate (`git diff --stat 14d03ea4 f181a961 -- <frozen list>` is
empty), so `FROZEN_UNCHANGED=1` will hold at the deciding run.

**4. No after-value asserted before the deciding run — PASS.**
The Target cells state targets (`total=0`; monitor 6 → 8; `C2_R49_PASS=true`), matching the contract's `target` fields;
the claim cells state the claims' labels in the same shape as the round-47/48 tables. SCORECARD.md:2395 says
explicitly: "The after values are read from the deciding receipts under `.ufo/evidence/round-49/after/`, never from
this table." `.ufo/evidence/round-49/after/` does not exist at f181a961 (`git cat-file -e f181a961:.ufo/evidence/round-49/after`
→ fatal, not in rev), and no deciding receipt exists anywhere in the tree. The pilot entry likewise defers: "Measured
values live in the deciding receipt `.ufo/evidence/round-49/after/c2.stdout`, never in this text."

**5. Capability row conditioned on the deciding receipt — PASS.**
C2 is the round's capability acquisition. No standing capability-table row was added pre-deciding (the round-49
section adds only the claims table; the standing table ends at the round-43 `staged-id adoption guard` row). The
capability's standing record — the README F10 line — is appended with an explicit void clause tied to
`after/c2.stdout` printing `C2_R49_PASS=true` (`corpus/README.md:599`), and the SCORECARD/LOG both describe it as
"conditioned on the deciding receipt" (LOG.md:2390). The deciding script itself refuses to run without the revealed
panel (`PANEL_NOT_REVEALED`), so the row cannot be decided early.

## Findings

**GAP-1 (verification gap, bounds-imposed — not a defect as written).** SCORECARD.md:2393 asserts CTL_FIX
`confirmed=6 classes_short=4` and `witness_confirmed=12` citing `control/c2-controls.stdout`. My seat bounds forbid
opening that file and the three per-control c2 stdouts (their MUTANT/WITNESS lines name the hidden panel), so I cannot
byte-check these three numbers. Corroboration without opening: the `6885adb4` commit message says "C2 ABSENT/FIX fail,
witness 12/12"; the contract pins CTL_FIX at "fewer than 11" (6 < 11 holds) and WITNESS at "all 12" (12 holds); the
receipts' blob ids are unchanged since the controls commit. Residual: the 6/4 split rests on the L1's paste.
`T49RevControls` (w1 reviewer, spec item names it for the c2 receipts) is the seat that can byte-check them; the
closure spot-check should require that check before the deciding run.

**OBS-1 (observation for the round report).** Two of the 55 dispatched w1 seats have no file under
`.ufo/waves/round-49/w1/` at f181a961: `T49RevControls` (reviewer, controls review) and `T49SentinelCounters`
(sentinel, hostile-input review of the counters). Shown by: `comm -23 <(sorted spec ids) <(sorted T49* names from
git ls-tree -r f181a961 -- .ufo/waves/round-49/w1/)`. The LOG's "w1 build (55 seats)" is accurate as a dispatch count
(spec `items`=55, dispatch `spawn`=55) and defers breakdowns ("counts in the report"); the round report must not claim
55 landed reports at this revision — 53 seats have files.

**OBS-2 (by-design forward pointers).** LOG.md:2394 and SCORECARD.md:2395 point to `.ufo/evidence/round-49/after/`
and "the report", neither of which exists at f181a961. No value is asserted, and QUALITY 88's rule ("a record drafted
before its receipts exist … names them in words as pending") is satisfied; `after/` is created by the deciding run in
this round, so the pointers resolve at the landing tip. If the deciding run is refused, the closure must land an
erratum or these dangle.

**NOTE-1 (phrasing, resolves).** SCORECARD.md:2384 "Routed by … defect 5 and routed defect 5" is dense but accurate:
the spot-check lesson has conformance defect 5 (the "pasted byte-exact" sentence, `:25` list) and routed-defects item 5
(`:118`, the corrections sweep) — both name the same appended correction, which is what the paragraph does.

**CORR-1 (corroboration recorded).** `generator=absent total=25` (SCORECARD.md:2393): reproduced by arithmetic from
the frozen `c2/measure.py` source at the freeze tree (see table above). Not a verdict — the deciding receipt remains
the only value of record.

## Residual risk and verification gaps

- GAP-1 is the only number in either addition this seat could not verify byte-for-byte; it is bounded, corroborated
  qualitatively, and the named seat (T49RevControls) can close it.
- The semantic claims the SCORECARD/LOG make about C1's reads (that the 45 corrections are right, that every read row
  supports its sentence) are outside this item — the contract itself assigns them to wave-2 re-read seats and the
  closure (`claims.C1.cannot_see`).
- The deciding run has not happened; every pass above is about the pre-deciding record only.

## Summary
- Append-only holds: `13 0 LOG.md`, `15 0 SCORECARD.md`, both hunks at EOF; "nothing above is rewritten" true.
- All pointers resolve (commits, receipts, lesson/QUALITY/considerthese/README/SOURCES cites, w1 reports); two
  by-design forward pointers (`after/`, the report) noted.
- All numbers byte-match committed receipts: CTL_0/J/K/K2 exact; monitor 57/64 score 6; pointers 90; corrections
  44+1=45 line-neutral (SKILL.md 2136→2136); 18/7/3 seats; 55 spec seats; 19+3 round-48 rows; 14 fixtures.
- `generator=absent total=25` corroborated by arithmetic from the frozen counter source; `witness_confirmed=12` by the
  controls commit message; CTL_FIX `confirmed=6 classes_short=4` unverifiable by this seat (bounds) — GAP-1 for
  T49RevControls.
- No after-value asserted before the deciding run; Target cells match contract targets; after/ absent at f181a961.
- Capability row conditioned: README:599 void clause on `after/c2.stdout`; no standing capability row added early.
- Frozen paths unchanged freeze→candidate; control receipts blob-identical since 6885adb4; freeze digests verified.
- No defects blocking the candidate's SCORECARD/LOG additions; one bounds-imposed gap, two observations.
