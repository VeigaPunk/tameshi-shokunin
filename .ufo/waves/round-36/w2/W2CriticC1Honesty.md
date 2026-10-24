# W2CriticC1Honesty — honesty attack on the C1 calibration "8"

Seat: UFO-FSD critic (calibration axis), round 36 wave 2, leaf seat, no subagents.
Attacked: claim C1 — "cold-read monitor refresh of the four round-35-drifted
headings restores `calibration_restraint_score` 6 → 8 (60/64 → 64/64)" — and
specifically the hypothesis that the four refresh entries being **L1 author
re-anchors** makes the restored 8 an overstatement of what the instrument
now measures.

## Commands run (all read-only; scratch under /fast/scratch/hyaku/tameshi-r36-seats/W2CriticC1Honesty/)

- `python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev b455001e2589b3f4f471d94a3de7e5e549b9f54c`
  → `calibration_restraint_score: 8`, `sections_covered 64/64`, `box3_full_page: true`, exit 0.
  Matches `.ufo/evidence/round-36/after/monitor-at-b455001e.stdout`. (reproduced, after-rerun.json)
- `python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev e423c41ba253357ab8c8513f0376dad9d38ab248`
  → `calibration_restraint_score: 6`, `60/64`, the four named headings uncovered.
  Matches `.ufo/evidence/round-36/control/monitor-at-e423c41b.stdout`. (reproduced, control-rerun.json)
- `git show e423c41b:…/ledger.json` vs `git show b455001e:…/ledger.json`:
  493 → 497 entries, **prefix identical** (all 493 prior entries equal as data),
  all non-entry top-level keys unchanged; kill-rule delta confirmed — exactly
  four appended entries + refresh traces/specs/receipts between control and
  refresh commits.
- Reads: `contract.json`, `refresh-specs.json`, `refresh-receipts.json`,
  `affected-sections.json`, `traces/L1/source-{1..4}.json`, the four new ledger
  entries, `measure.py` credit rules (round-18 algorithm), r21 refresh
  specs/receipts, r32 `append-entries.py` + `bind-receipt-w2.json`, r32/r35
  contracts, LOG.md and `corpus/lessons/round-36.md` at `e423c41b`.

## What the 8 actually is (instrument semantics)

`restraint = 2·(box1 ~) + 2·(box2 ~) + 2·(box4 ~) + 2·box3_points` where
`box3_points = marked ∧ ledger-linked ∧ sections_covered==sections_total`.
A section is covered iff ≥1 entry keyed by section-sha256 passes: verdict ∉
{gap-blocking, wrong-expectation, not-executed}, class-consistent verdict,
`commands_executed_count > 0`, every recorded input blob-verifies at REV, and a
committed trace exists. The rubric's own text already caps at 8 because the
final 2 need independent promotion review — the `[~]` mark is annotated "lane
assertion, input-keyed monitor only; no independent promotion verifier".

## Honesty assessment — improved, not overclaimed

The claim is worded as instrument truth — "`calibration_restraint_score 6 → 8`
at the refresh commit" — and that is exactly what the frozen instrument prints
(reproduced). The weaker evidentiary class of the new entries is disclosed at
every level a reader checks:

1. **Precedent is real, not invented.** The round-21 refresh (34 entries) ran
   the identical "L1-author source re-anchor" protocol with the identical scope
   banner ("input-keyed source reads only; not independent/blind cold-read,
   recipe re-execution or required-command coverage"), and that scope text is
   carried verbatim into `refresh-receipts.json` round36_provenance. The r32
   precedent (fresh independent w2 seats via `append-entries.py` +
   `bind-receipt-w2.json`) is a *stronger* precedent but not the contract's
   required one; C1's contract names the r21 protocol.
2. **The 8-cap already encodes the absence of independent verification.**
   Restoring 8 via author re-anchors does not cross the instrument's own
   honesty boundary, because box-3 credit never claimed blindness — it claims a
   fresh, trace-bound, input-keyed entry exists per section. That is true and
   verified: the four entries' input sha256s match the blobs at `b455001e`.
3. **Provenance is self-labeling, not false.** Seat field says
   "L1 TameshiR36 author source re-anchor"; the ledger's own `provenance` key
   disclaims blind reads; `corpus/lessons/round-36.md` `## Holds` records
   "credited by L1 author source reads … not by a fresh blind cold-read" and
   defers the stronger credit. The claim does not hide what bought the credit.
4. **The control isolates the delta honestly.** Same command at the content
   commit prints 6; only the ledger entries + trace receipts differ
   (prefix-identical append). The 6→8 is caused by the refresh and nothing
   else — the cleanest possible causal attribution, and the kill-rule's
   no-monitor/rubric-change clause held.

## Defects found (fixable; none reverses the score)

- **a. `minor_gaps: 0` under `verdict: gap-minor`** on all four new entries —
  self-inconsistent (a minor-gap verdict reporting zero minor gaps). Every
  prior re-anchor recorded `mg ≥ 1`. Cosmetic for scoring (`mg` is never
  checked) but overstates the entry's self-audit.
- **b. `class` flipped `instruction → record` on sections 131 and 375**
  (previous drifted entries for both are `instruction`; r36 specs even write
  `"previous_class": "record"` for 131 — false). Score-neutral today
  (`gap-minor` is valid under both class gates, `cec=1>0` satisfies either),
  so no predicate was dodged — but it silently re-labels two recipe sections
  and weakens the entry schema's meaning.
- **c. `skill_sha256` field corrupted**: all four new entries store the
  *section* sha256 there (identical to the `sha256` field); every prior entry
  stores the whole-SKILL.md blob sha256 (`2381873162…` at this rev). Breaks the
  field's identity meaning; monitor ignores it, but future tooling keyed on
  `(skill_sha256, start)` will mis-group these entries.
- **d. Evidence-base asymmetry**: the 8 lost in r35 rested partly on
  independent-seat cold-read entries; the restored 8 rests on four entries
  whose trace is a sha256-printing script and whose verdict/gaps fields are
  self-asserted. The number is honest; the evidence behind it is strictly
  weaker. This is precisely what the lesson `## Holds` admits, so it is a
  disclosed regression, not a hidden one — but it means the 8 now reads
  "ledger re-anchored at current bytes", not "sections freshly read".

## Smallest safe correction

No re-run needed for the claim itself; the safe correction is metadata hygiene
in a future ledger-touching round: restore `class: instruction` on 131/375 (or
justify `record` in the entry), write a real `minor_gaps` (≥1 as the re-anchor
protocol's standing convention), fix `skill_sha256` to the blob sha, and keep
the Holds note until an independent cold-read restores the stronger base. None
of this changes the measured 8 — it makes the ledger tell the truth about what
earned it.

## Verdict line

**improved** — the 6→8 is real, isolated, precedent-backed and honestly scoped;
the author re-anchor class of the new entries is disclosed rather than
overclaimed (residual: entry-metadata defects a–d, none score-bearing).
