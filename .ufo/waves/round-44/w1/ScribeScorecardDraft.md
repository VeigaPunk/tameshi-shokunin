# ScribeScorecardDraft — round-44 SCORECARD block draft (L1Tameshi44.ScribeScorecardDraft)

Item: draft the `## Round 44` SCORECARD block in the report (SCORECARD.md not edited).
Bounds respected: read-only on the lane; no counter run as a measurement (the only deciding run is the
L1's); no installs made (python3/git already present; nothing needed).
Tooling record: no tool installed or updated.

## Findings (grounding)

- Contract: `.ufo/evidence/round-44/contract.json` — C1 axis calibration (lowest non-retired axis,
  round-21 coldread monitor), counter `.ufo/evidence/round-44/calibration/measure.py`
  (sha256 c0c6199f...), counting command `python3 .ufo/evidence/round-44/calibration/measure.py
  --lane LANE --rev REV --freeze FREEZE`, predicate C2_R44_PASS=true iff self_pin=1, classes=7,
  total=0; C2 axis freshness, counting command `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md`
  (0 at base, 1 at landing).
- Base receipts committed: `.ufo/evidence/round-44/before/c2-old-at-base.stdout`
  (`C2_R43: ... m7=1 ... total=1 ... C2_R43_PASS=false first=m7:SCORECARD.md#round-43_unknown_S256`)
  and `.ufo/evidence/round-44/before/c2-new-at-base.stdout`
  (`C2_R44: ... m12=1 ... total=1 ... C2_R44_PASS=false first=m12:newest_block_is_round_43,_the_contract_round_is_44`).
- S089 row bytes: `corpus/SOURCES.md:98` anchor cell names "html sha256 bc572676…e04d" (fetched
  2026-10-22) — matches the C2 stale-anchor before-state. `corpus/SOURCES.md:456` currently reads
  `- Next unused id: S160.`; no S160 row exists in the tree yet (landing appends it).
- Freeze `ba01973c73ad7de60e5bd19ae08255a1b7ef917e` (contract + C1 counter + Stryker snapshot,
  committed before any seat and before the first deciding run); snapshot
  `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html` (sha256 79f6501a...).
- Planned knowledge entry path per wave spec (SentinelScope item): `corpus/knowledge/r44-anchor-refresh-rule.md`.
- Numeric-axes base receipts are produced by wave-1 seat ExecMeasureBase (spec-w1.json item 194):
  round-44 counter at base (1), round-43 counter at base (2), command D (3)
  `git show 506e99c7...:tools/mutate-and-run.sh | python3 -c '…'` → `recorded_cases=9 depth_score=9`,
  coldread monitor (4) `python3 .ufo/evidence/round-21/coldread/measure.py --repo … --rev 506e99c7...`
  → `calibration_restraint_score: 6`; receipts staged in /tmp/tameshi-r44-ExecMeasureBase-/ for the
  L1 to copy into `.ufo/evidence/round-44/before/`.
- Do-nothing controls (contract C1/C2 do_nothing_control): round-43 counter at base prints
  `m7=1 total=1 C2_R43_PASS=false`; the round-44 counter with the ASSIGN_ID mask line removed fails
  its own T6 selftest cases with `['r unknown S256']` (receipt
  `.ufo/evidence/round-44/control/mask-removed.selftest.stdout`); with no row appended the grep
  prints 0 and the stale anchor remains in S089's cell.
- Round-43 planned/holds that remain open (SCORECARD.md:2076-2079; `corpus/lessons/round-43.md:203-217`):
  whole-set staged adoption (a map over all ~103 staged rows, injective and disjoint from the
  registry, at or above the safe floor) unmeasured; two guard refusal classes open (prose-document
  unmapped message does not say which cause fired; a registry row indented four spaces is invisible
  to both patterns); `cmp` / `git diff --exit-code` comparator lattices unmeasured since round 39;
  m13 remains a presence/pattern check, not proof the standing command produced the printed number.

## Drafted `## Round 44` block (for SCORECARD.md)

```
## Round 44 — record agreement with the value-vs-citation grammar repaired (calibration) + S160 anchor refresh (freshness) (2026-10-25)

L1 tameshi, hyaku run 6, attempt 1. Nothing was inherited. Two claims on distinct axes. Calibration
(6, measured by the round-21 coldread monitor) is the lane's lowest non-retired axis and carries C1;
the stagnation nudge does not fire because round 43 admitted a capability inside the window N=2.
Contract `.ufo/evidence/round-44/contract.json`, frozen at `ba01973c73ad7de60e5bd19ae08255a1b7ef917e`
before any seat ran and before the first deciding run (the round-44 counter, the contract and the
Stryker snapshot are committed together at the freeze); the verified amendments list is empty.

| Claim | Axis | Before | After | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|
| C1 the lane's records agree with the tree across seven classes — m6 m7 m8 m10 m11 m12 m13 carried from round 43, with the round-43 false m7 alarm resolved because an S-id bound to an assignment (key=S###) is a field value, not a citation, while genuine unknown and unmined citations still flag | calibration (lowest axis) | round-43 counter at base prints `m7=1 total=1 C2_R43_PASS=false`, exit 1, first=`m7:SCORECARD.md#round-43_unknown_S256` (`.ufo/evidence/round-44/before/c2-old-at-base.stdout`); round-44 counter at base prints `m12=1 total=1 C2_R44_PASS=false`, exit 1, first=`m12:newest_block_is_round_43,_the_contract_round_is_44` (`.ufo/evidence/round-44/before/c2-new-at-base.stdout`) | target `self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 C2_R44_PASS=true`, exit 0 at the landing commit | `python3 .ufo/evidence/round-44/calibration/measure.py --lane LANE --rev REV --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e` | see the after subsection | `.ufo/evidence/round-44/before/c2-old-at-base.stdout`, `.ufo/evidence/round-44/before/c2-new-at-base.stdout`, `.ufo/evidence/round-44/control/mask-removed.selftest.stdout` | see the after subsection |
| C2 S089's stale anchor digest (bc572676..., page fetched 2026-10-22) is superseded by a new census-valid row S160 opened this round from the live Stryker equivalent-mutants page (sha256 79f6501a..., snapshot `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html`), status mined, cited by a knowledge entry, with the old->new change logged in the round-44 lesson | freshness (sourced) | `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` prints 0 at base; S089's anchor cell names the stale digest bc572676... | target `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` prints 1 at the landing commit; `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exit 0 at round end | `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` | see the after subsection | `corpus/SOURCES.md` S160 row, `corpus/knowledge/r44-anchor-refresh-rule.md`, `corpus/lessons/round-44.md`, `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html` | see the after subsection |
```

Numeric axes at the base: depth 9 (command D `recorded_cases=9 depth_score=9`), calibration 6
(round-21 coldread monitor `calibration_restraint_score: 6`), both re-run at the base by wave-1
seat ExecMeasureBase (`.ufo/waves/round-44/w1/ExecMeasureBase.md`). Neither claim edits the runner or
a SHONEN box, so neither number is expected to move; C1's gain is record agreement with the repaired
value-vs-citation grammar, and C2's gain is a sourced surface move.

Do-nothing controls, committed before the deciding run: the round-43 counter at base prints
`m7=1 total=1 C2_R43_PASS=false` (`.ufo/evidence/round-44/before/c2-old-at-base.stdout`). The
round-44 counter with the ASSIGN_ID mask line removed fails its own T6 selftest cases with
`['r unknown S256']` (`.ufo/evidence/round-44/control/mask-removed.selftest.stdout`). For C2, with
no row appended the grep prints 0 and the stale anchor remains in S089's cell.

Capabilities table: no new row. The S160 row is a sources-registry (freshness) surface move, not a
repertoire capability; the C1 counter is the round-43 C2 successor and is not a capability claim.

| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, zero E codes; row count from the census-valid command `grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` → 114 rows at round 43, 115 at round 44 (S160 appended) ; `corpus/SOURCES.md` | fleet round 1 (kaika) |

**Planned (round 45):** the whole-set staged adoption the guard's floor rule now admits (a map over
all ~103 staged rows, injective and disjoint from the registry, at or above the safe floor) stays
unmeasured; the two guard refusal classes wave 1 leaves open — a prose-document staged row's refusal
message does not say which of the three causes fired, and a registry row indented four spaces is
invisible to both patterns; the `cmp` / `git diff --exit-code` comparator lattices stay unmeasured
since round 39; m13 remains a presence/pattern check of the standing census command, so proving that
command produced the printed number is still open.
```

## Out-of-scope / not done

- SCORECARD.md itself not edited (draft only, per item).
- No measurement runs: the deciding C1/C2 runs are the L1's; only the committed base receipts were
  read. The landing commit hash is not yet known at draft time (`.ufo/evidence/round-44/after/` is
  empty), so the draft carries the frozen targets verbatim in the After cells and "see the after
  subsection" placeholders for Measured commit / Verdict.
