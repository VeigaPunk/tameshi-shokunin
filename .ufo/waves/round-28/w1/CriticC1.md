# CriticC1 — round 28, wave 1, claim C1 (calibration)

Seat: TameshiR28.CriticC1 (critic). Read-only against the lane; all code ran in
`/tmp/criticc1-r28/lane` (a `git clone --no-hardlinks` of the lane, detached at
`b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a`, plus scratch branches `sim`, `sim2`
that exist only in that clone). No tool installs or upgrades.

## Verdict

C1 is a sound, falsifiable claim, and it can pass honestly. Three conditions
must hold for it to pass:

1. The headline must state the real delta. Over the base this is 4 sections,
   not 14. The other 10 are credit that this round removed and then restored.
2. The set of files edited after the reads must stay inside the four exempt
   files plus trace receipts.
3. Every one of the 28 reads must land in the ledger, failing reads included.

`restraint=8 box3_mismatch=0` does not overstate SHONEN box 3, but only
because box 3 is marked `[~]` and labelled "lane assertion, input-keyed
monitor only". The number checks that the mark matches the monitor. It does
not show that box 3 holds.

## Evidence

### Reproduced counter readings (my clone)

`python3 .ufo/evidence/round-27/c1-measure.py --repo . --rev <rev>`:

| Rev | Observed | Exit |
|---|---|---|
| 06b59b93 (base) | `covered=60/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| b05d2ee8 (content rev) | `covered=50/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |

The base value matches `.ufo/evidence/round-28/append-probe.txt` (`base:` line).

Uncovered at b05d2ee, from a `--explain` run of
`.ufo/evidence/round-21/coldread/measure.py`:
- 4 are `no-ledger-entry` (the routed remainder): "The report shape",
  "Triggers T1–T3", "Gate/probe registry", "Round-21 gate/probe registry". The
  last one's text changed again in b05d2ee because of the Round 28 correction.
- 10 are `input-drift:corpus/SOURCES.md` (credited at base, lost in b05d2ee):
  start lines 131, 921, 1479, 1517, 1548, 1563, 1609, 1814, 1925, 1938.
- 0 sections are vetoed.

### (1) Is "repair" honest?

The arithmetic is honest, and the claim text discloses the drift. The b05d2ee
SOURCES diff changes only the S059 `used-by` cell and appends a search-log
note plus `Next unused id: S092`. That is lane conformance work for the lesson
that cites S059, and the lesson cites S059 to explain the very drift the edit
caused.

The calibration risk is in how the result gets reported:
- The honest delta against the base is +4 sections, plus restraint 6 → 8 and
  `box3_mismatch` 1 → 0.
- Measured from b05d2ee (50 → 64), the round would look like it repaired 14
  sections. Ten of those are self-inflicted re-credits.
- Any SCORECARD, LOG or lesson line saying "14 sections repaired" or "50 → 64"
  without the base would overstate the round.

The 10 re-reads are fresh, independent reads at a new revision. That is
stronger evidence than the old credit, not laundering, so it is no defect.
Spending 20 read seats to restore credit is a tradeoff the planner chose. It
is not a correctness problem.

### (2) Does 64/64 from reads at b05d2ee survive the landing appends?

For the four exempt files: yes, for the existing credit. I simulated the
landing in the clone. I appended a block to `SCORECARD.md`, `LOG.md` and
`corpus/lessons/round-28.md`, added one new entry to
`.ufo/evidence/round-21/coldread/ledger.json`, committed, and ran the counter:

```
C1_MONITOR: covered=50/64 restraint=6 box3_mismatch=1 depth_score=9 rev=3796d0cb…   (unchanged from b05d2ee)
```

Why this holds:
- The round-21 wrapper adds its ledger to `IGNORED_INPUTS`
  (`.ufo/evidence/round-21/coldread/measure.py:112`).
- No credited entry at b05d2ee records `LOG.md`, `SCORECARD.md` or the round-28
  lesson.
- The wave recipe tells readers to read these four files only via
  `git show` into `external_inputs` (`.ufo/waves/round-28/make-spec-w1.py:30,78-80`).
- `external_inputs` is collected but never gated
  (`.ufo/evidence/round-18/measure.py:603-608`).

Counterexamples outside the exempt set. In the same clone, I appended one line
at b05d2ee and committed:

| File appended | Counter result |
|---|---|
| `SHONEN.md` | `covered=49/64` (one already-credited section lost) |
| `corpus/README.md` | `covered=48/64` (two lost) |
| `corpus/QUALITY.md` | `covered=50/64` (no further loss among the 50) |
| `corpus/SOURCES.md` | `covered=50/64` (no further loss among the 50) |

QUALITY and SOURCES are worse than their row suggests. Fresh trace receipts
already on disk under `.ufo/evidence/round-28/coldread/traces/` record
non-exempt, widely read files:
- `Read01A-1.json` records `corpus/README.md`.
- `Read05B-1.json` records `corpus/SOURCES.md`.
- `Read13B-1.json` records `corpus/SOURCES.md` and `corpus/QUALITY.md`.

So a landing edit to README, QUALITY or SOURCES, or any SHONEN text change,
drops sections at the head. Two edits are especially likely:
- Fixing routed item 4 (README F8 wording) after the reads.
- Fixing routed item 5 (QUALITY 53/54 amendments) after the reads.

The same goes for any `SKILL.md` correction after a failing read: it changes
that section's sha256 and orphans both of its entries. That is the round-27
pattern (`af7b70d` corrections never re-read; spot-check routed item 1).

None of the 16 receipts records the four exempt paths. Read12A-1 records
`.ufo/evidence/round-18/coldread/ledger.json`, which is an ignored input. The
`ReopenS059-1.json` receipt uses non-canonical keys
(`corpus/SOURCES.md@b05d2ee8`). It is not a cold-read entry, but it would fail
`input-missing` if anyone put it in a ledger entry.

### Veto arithmetic: two reads per section raise the bar

The aggregation step vetoes a section when any failing entry's inputs still
verify (`.ufo/evidence/round-18/measure.py:635-639`, docstring rule 6: "A
clean entry never launders a failing one"). With two independent reads for
each of 14 sections, 64/64 needs all 28 reads to be non-failing. One honest
`gap-blocking` or `wrong-expectation` keeps its section uncovered.

The only way to "rescue" such a section at the head is to omit the failing
entry from the ledger, which would be false provenance. The alternative, a
`SKILL.md` correction, orphans the section until it is read again.

### (3) Does restraint 8 / box3_mismatch 0 overstate SHONEN box 3?

Box 3 at b05d2ee (`SHONEN.md:9-10`) reads: "[~] Instructions executable by an
agent without oral context", evidence "[lane assertion, input-keyed monitor
only; no independent promotion verifier](.ufo/evidence/round-21/coldread/ledger.json)".

How the scores are computed:
- Restraint is `2 × (boxes 1, 2, 4 marked ~) + 2 × (box 3 marked ~ AND the
  ledger link is present AND every section is covered)`
  (`.ufo/evidence/round-18/measure.py:679-683`).
- `box3_mismatch` is `marked AND NOT box3_full_page`
  (`.ufo/evidence/round-27/c1-measure.py`).

So 8/0 means the `[~]` mark agrees with full monitor coverage. It is not a
verification of the box. What "full page" contains, measured over the 60
credited sections at base:

| Measure | Count |
|---|---|
| Credited only by `record`-class reads (files read, no instruction executed) | 40 of 60 |
| Credited by `instruction`-class reads | 20 of 60 |
| Credited only by `gap-minor` verdicts (reader listed gaps) | 51 of 60 |
| Credited by at least one clean `executed-ok` or `verified-record` | 9 of 60 |
| Sections whose earliest credit comes from read revisions back to `8eaae28e` | 10 of 60 |

The b05d2ee SKILL correction itself records a non-hermetic path:
`c2-count.py` reads the live lane through `FLEET`. The trace gate accepts
any live read under `.git/` as bound to REV (`.ufo/evidence/round-18/measure.py:448-449`).

The overstatement risk is in prose, not in the number. Text such as "box 3
verified", "page cold-read clean" or "instructions executable, 64/64" would
overstate the evidence. "Box 3 mark consistent with the input-keyed monitor
(64/64, mostly gap-minor, mostly record-class)" would not.

## (4) What would make C1 false

Each check below is concrete:

1. The counter at the landed head, run from a fresh clone, prints anything
   other than `covered=64/64 restraint=8 box3_mismatch=0` with exit 0.
2. `git diff --name-only b05d2ee HEAD` names any file outside these: the four
   exempt files, `.ufo/evidence/round-28/coldread/traces/*`, and new
   `.ufo/waves/round-28/**` or `.ufo/evidence/round-28/**` records. In
   particular, the diff must not include `SKILL.md`, `SHONEN.md`,
   `corpus/README.md`, `corpus/QUALITY.md` or `corpus/SOURCES.md`.
3. The ledger at the head gains fewer than 28 entries for the 14 section
   sha256 values, or any Read report in `.ufo/waves/round-28/w1/` has a verdict
   that differs from its ledger entry. This would be a dropped or softened
   failing read.
4. A new entry's `inputs` lacks a key that its trace receipt records
   (`trace-input-unrecorded`). A new entry's receipt path is also missing at
   the head (`trace-missing`).
5. `git diff b05d2ee HEAD -- .ufo/evidence/round-18/measure.py .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-27/c1-measure.py`
   is non-empty, meaning the frozen instrument changed.
6. Any SHONEN box mark changes. For example, box 3 moving from `[~]` to `[x]`
   would turn a consistency check into an unverified promotion claim.

## Impacted axes

- Calibration: primary. Over-reporting the delta, or describing box 3 as
  verified, would be a calibration harm.
- Operability: secondary. Landing-order fragility for routed items 4 and 5.

## Smallest safe correction

1. In SCORECARD, LOG and the lesson, report C1 as follows: "60/64 at base,
   50/64 at b05d2ee after the round's own SOURCES edit, 64/64 at head". Say
   that 4 sections are newly credited and 10 are re-credited after
   self-inflicted drift.
2. After the reads, land only the four exempt files plus receipts and records.
   Defer README (routed item 4), QUALITY (item 5), any SOURCES, SHONEN or
   SKILL edit to a later content revision, or re-read the affected sections.
   Run the counter at the actual landed head, not at b05d2ee.
3. Append all 28 entries verbatim. If any read fails, report C1 as missed;
   do not drop or correct the entry this round.
4. Keep the SHONEN box 3 wording as is. Call `box3_mismatch=0`
   "mark/monitor consistency" in the round's text.

Checks for the integrator to run: items 1 to 5 of the falsifier list, in a
fresh `/tmp` clone at the landed head.
