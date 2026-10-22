# DraftLesson — round-25 lesson draft (`## Mistakes`, `## Gate`)

Role: scribe (leaf, no subagent dispatch). Target: draft
`corpus/lessons/round-25.md` sections `## Mistakes` and `## Gate` following the
shape of `corpus/lessons/round-24.md`, mining one mistake (round 24 declared a
routed population that omitted three closure-routed items), naming the existing
QUALITY.md criterion that should have caught it, and stating whether the
round-25 c1-measure can fail on it. This file is the draft only; the L1
(TameshiR25) is the sole integrator of `corpus/lessons/round-25.md`.

Verdict first: the mined mistake is **population declaration / unrouted
denominator** — round 24 declared a routed population ("eleven named …
predicates routed by round23 critics and closure"; Erratum I "Of the eight
round23 routed defects") that omitted the three closure-routed items named in
MANIFEST rounds[421].notes (multi-token stdout fixture in the ruler, re-run
guard sweep, dead-falsifier coverage gap). The existing criterion that should
have caught it is **QUALITY 12** ("report all declared defects, unresolved
denominators"); QUALITY 44 is the closest structural analogue (never dropped
from the denominator) but is scoped to frozen mutation-population anchors, and
QUALITY 48 as applied has no membership clause — as round 24's own residual seat
already recorded (`CorpusQuality48.md:84`). The round-25 c1-measure **can**
fail on the three named items (executed checks + records are required; red
states reproduced), but it **cannot** fail on the general omission class: its
population is the hard-coded three-label literal at `c1-measure.py:43` and is
never derived from the routing source (phantom label probe). Both halves are
shown with executed probes below.

---

## Drafted section: `## Mistakes` (for round-25.md)

Table shape mirrors round-24.md.

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| population declaration / unrouted denominator | MANIFEST `rounds[421].notes` (fleet root, read-only) routes eleven items: "eight deferred repairs (…), multi-token stdout fixture in the ruler, re-run guard sweep, and dead-falsifier coverage gap"; round-24 contract `.ufo/evidence/round-24/contract.json:3` claims "eleven named weakening/substitution/projection predicates routed by round23 critics and closure" and `:66` cites that closure note as a source; round-24 lesson `corpus/lessons/round-24.md:128-135` (Erratum I) reports "Of the eight round23 routed defects" — silently dropping the three; verifier `corpus/lessons/round-24-verifier-spotcheck.md:34,37` records "three closure-routed items remain unrecorded" and "C1 as fully worded … Unprovable as declared"; round-24 w1 `ClosureCarry.md:39-41` maps items 9/10/11 (delegated / partial / criterion-only); `CorpusQuality48.md:84` finds "QUALITY48 has no clause requiring every routed gap to enter the denominator or carry an explicit disposition" | QUALITY 12 (`corpus/QUALITY.md:39-41`) — a frozen declaration must "report all declared defects, unresolved denominators"; QUALITY 44 (`:432-439`) is the nearest structural analogue ("never dropped from the denominator") but is scoped to a frozen **mutation** population's anchors; QUALITY 48 (`:489-502`) governs only whether a routed gap counts as repaired and, as written, has no membership clause (round-24 residual seat `CorpusQuality48.md:84`) | Round-25 C1: each of the three closure-routed items carries a SCORECARD row and an executed check that holds, including negative controls that can fail (`c1-measure.py`, `c1-pins.py`). Shown able to fail: at HEAD `09dc114` in a /tmp clone, exit 1, `C1_ROUTED: dispositioned=0/3` (no SCORECARD rows, no disposition file). The three-item population itself is a hard-coded literal (`c1-measure.py:43`); **not** able to fail on an omitted routed item outside those three labels (probe: added `| R23-ROUTED-4 |` row; total stays 3) |

Note for the L1: the same table can carry the round-25 measured after-receipt rows
once the wave's receivers land (matching round-24's mistakes + addendum shape).

---

## Drafted section: `## Gate` (for round-25.md)

Shape mirrors round-24.md (Admit candidate / Reject / Flip condition / source
rows / bounded lookup). Placeholders `[L1]` where the L1's own receipts must be
cited; nothing here asserts an unobserved measurement.

```
## Gate

Admit candidate: the three round-23 closure-routed dispositions
(R23-ROUTED-1/2/3): the SCORECARD rows, the executed C1 checks
(`.ufo/evidence/round-25/c1-measure.py` sha256
`b18460c7…`, `c1-pins.py` sha256 `48bfde94…`) and the
`dead-falsifier-disposition.json` record; for C2, the MTE-interop tool
(`tools/mte-interop.py` sha256 `8c24255c…`) with the two sha512-pinned
vendored packages in `tools/vendor/`.

Reject:
- reading `C1_ROUTED: dispositioned=3/3` as closure of the whole round-23
  routed breadth: the counter's population is the literal label set
  (`c1-measure.py:43`), not a list derived from the routing source;
- reading a SCORECARD row's presence as a disposition statement: the counter's
  row test is a bare label regex (`^\|\s*LABEL\b`), and the companion
  c1-pins P5 substring check accepts "NOT dispositioned" rows;
- reading one item's executed check as a general mutation-adequacy claim;
- reading the MTE official score algebra as a tameshi capability claim: it is
  an interop mapping (1:1 status mapping), not a Stryker run and not producer
  authentication.

Flip condition: an independently retained, applicable execution or authority
record.

Source rows opened this round: S086/S087 (npm mutation-testing-report-schema
3.9.0; npm mutation-testing-metrics 3.9.0) — drafted by the sources seat in the
same round; this section cites them by id only.

Bounded lookup: identified 2, screened 2, included 2, excluded 0 (packages);
[L1] tie to the sources seat's row and any additional source cited in the
knowledge entry.
```

---

## Findings

### F1. The mined mistake and its evidence

Round 24's declared routed population omitted three closure-routed items. The
round-23 closure note (`MANIFEST.json` `rounds[421].notes`, fleet root,
read-only; verified by `python3 -c` JSON parse) routes eleven items — eight
deferred repairs plus "multi-token stdout fixture in the ruler, re-run guard
sweep, and dead-falsifier coverage gap". Round 24's contract
(`.ufo/evidence/round-24/contract.json:3`, `:66`) declared "eleven named …
predicates routed by round23 critics and closure" and cited that same closure
note as its source, and its lesson's Erratum I (`corpus/lessons/round-24.md:128-135`)
reported "Of the eight round23 routed defects" — no disposition for the three.
The verifier spot-check lesson (`corpus/lessons/round-24-verifier-spotcheck.md:34,37`)
records "three closure-routed items remain unrecorded" and "Unprovable as
declared". Round 24's own w1 seat `ClosureCarry.md:39-41` mapped all eleven but
the lesson/contract carried none of the three dispositions. ResErrataCritic D7
(`.ufo/waves/round-24/residual/ResErrataCritic.md:175-179`) records the 8-vs-11
discrepancy.

Which existing QUALITY criterion should have caught it:

- **QUALITY 12** (`corpus/QUALITY.md:39-41`): "A frozen witness declaration
  records prior exposure and checks integrity before replay. Report all
  declared defects, unresolved denominators and accidental kills". The round-24
  declaration was frozen and named its source; the three items were declared
  defects in that source and were unresolved — 12's duty to report all declared
  defects/unresolved denominators is the rule that should have caught it.
- **QUALITY 44** (`:432-439`): "never dropped from the denominator" — nearest
  structural analogue, but its letter is scoped to a frozen mutation
  population's anchors, so it does not reach a routed-item inventory.
- **QUALITY 48** (`:489-502`): governs whether a routed hardening gap counts as
  repaired (predicate fails at base, holds after). It has no clause requiring
  every routed gap to enter the denominator or carry an explicit disposition —
  round 24's own residual seat wrote this verbatim at
  `.ufo/waves/round-24/w1/CorpusQuality48.md:84`. So 48 as applied could not
  catch the omission; the new criterion drafted in this wave (QualityCriterion
  seat) covers the gap.

### F2. Can the round-25 c1-measure fail on it? — partially, with a structural limit

The C1 counter (`c1-measure.py`, sha256 `b18460c7…`, unchanged across
amendments) requires, per item, (a) a SCORECARD row matching
`^\|\s*LABEL\b`, and (b) an executed check that holds (R1/R2: runner exit 0 +
control green + restore OK + every spec defect killed with a witness; R3:
disposition file present, row set exactly equal to the derived 34 dead seats,
and two doctored negative controls each fail).

It **can** fail on the three named items (all executed in /tmp clones of the
lane at 5b69fb2 / HEAD 09dc114; lane never written):

| Probe | State | Observed result |
|---|---|---|
| Baseline (HEAD clone) | no SCORECARD rows; no disposition file | `C1_ROUTED: dispositioned=0/3`, exit 1; R1 10/10 killed, R2 14/14 killed, R3 "disposition file absent" |
| P1 | three SCORECARD rows appended | `dispositioned=2/3`, exit 1 (R3 still absent) |
| Q | three rows with negating/placeholder text + a fourth phantom row | R1/R2 still `scorecard_row=true`,`dispositioned=true`; total stays 3; exit 1 (R3 absent) |
| P | multitoken fixture set degraded to a single single-token case | R1 `holds=false`, `killed=[]` (0/10), exit 1 |
| G | one disposition row dropped; R2 SCORECARD row removed | `1/3`: R3 fails "row set differs from the 34 dead round-23 wave-2 seats"; R2 `scorecard_row=false` |
| H1 | all 34 disposition rows `reattack-seat-died` | R3 `holds=false` via `negative_controls_fail_as_required.flip-one-status=false` |
| D | full synthetic 34-row disposition (AGREE + report files) | `3/3`, exit 0 — target reachable only when both halves are satisfied |

It **cannot** fail on the general omission class. The population is the
hard-coded literal `LABELS = {'R1': 'R23-ROUTED-1', 'R2': …, 'R3': …}` at
`c1-measure.py:43`; the counter never reads MANIFEST rounds[421] or
fresh-adjudication.json's routed list, so an omitted routed item outside the
three labels is invisible (probe Q: `| R23-ROUTED-4 |` row changed nothing).
Thus the class "declared routed population omits an item" is not detectable by
the round-25 ruler; only the three named omissions are. The c1-pins companion
extends checks (P1-P5) but also pins a fixed label/title population and its P5
substring check accepts a "NOT dispositioned" row (verified: rows
`| R23-ROUTED-1 | NOT dispositioned - deferred |` and `… not dispositioned at
all …` produce **zero** P5 failures). This limit is stated in the drafted Gate's
Reject list.

### F3. Out-of-scope / sibling-owned material

- `SOURCES.md` S086/S087 rows and round-25 search log → DraftSources seat.
- `knowledge/mte-report-interop.md` → DraftKnowledge seat.
- SKILL.md decision table → DraftSkillTable seat.
- New QUALITY criterion text + falsifier → QualityCriterion seat.
- Counter vacuity deep-dive (e.g. P5 substring semantics) → MeasureVacuity seat
  (I observed and reported the P5 "NOT dispositioned" acceptance as a finding,
  but the detailed attack is that seat's lane).
- C2/mte-interop measurement receipts → C2 seats + L1.
- The `## After measurement` section (round-24 shape) is the L1's to fill with
  the measured after-receipt; not drafted here because no after measurement is
  observable yet (R3 disposition file absent at HEAD; SCORECARD rows not yet
  landed by the wave receivers).

### F4. Tooling / environment

No installs or updates performed (tooling directive recorded: n/a — stock
`python3` 3.14.8, `git` 2.56.0, `bash` 5.3.20 used). All probes ran in /tmp
clones (`/tmp/r25-draft-probe/clone*`); the lane and fleet repositories were
never written. Read-only git accesses used `GIT_OPTIONAL_LOCKS=0`.

## Artifacts

- This report: `.ufo/waves/round-25/w1/DraftLesson.md`.
- Probe receipts (scratch, /tmp): `/tmp/r25-draft-probe/{A,P1,Pc,Pd,Pe,Pf,Pg,H,H1,H2,P,Q}.stdout` (and `SCORECARD.orig`).
- Cited lane evidence: `MANIFEST.json` (fleet root, read-only) `rounds[421].notes`; `.ufo/evidence/round-24/contract.json:3,66`; `corpus/lessons/round-24.md:128-135`; `corpus/lessons/round-24-verifier-spotcheck.md:34,37`; `.ufo/waves/round-24/w1/ClosureCarry.md:39-41`; `.ufo/waves/round-24/w1/CorpusQuality48.md:70,84`; `.ufo/waves/round-24/residual/ResErrataCritic.md:175-179`; `corpus/QUALITY.md:39-41,432-439,489-502`; `.ufo/evidence/round-25/c1-measure.py:43,60-69,99-116,143-152`; `.ufo/evidence/round-25/c1-pins.py:9-17,54-74`; `.ufo/evidence/round-25/contract-amendment-2.json`.
