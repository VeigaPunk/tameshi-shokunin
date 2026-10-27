# T51CritExpectedA — frozen C1 expectations F1..F5 (attack / re-derivation)

Seat: `T51CritExpectedA` (critic, wave 1). Item: attack the frozen C1 expectations
for F1..F5 (`.ufo/evidence/round-51/c1/frontier-expected.json`) by independently
deriving each ground's latest declared status from `corpus/README.md` (all sections),
the `knowledge/` entries whose `ground:` line names it, the lessons and
`SCORECARD.md` — without first reading the `basis` fields.

Method (independence): the statuses below were derived from the primary declarations
(README sections, ground lines, lessons, SCORECARD) before the `basis` fields of
`frontier-expected.json` were inspected; basis lines were then read only to confirm
line anchors. Evidence commands: `grep -n '^ground:' corpus/knowledge/*.md`;
`read corpus/README.md:1-608`; `grep -nE 'F[1-5][^\n]{0,80}(held|partly|Core|open)' SCORECARD.md corpus/lessons/*.md`.

## Findings

### F1 — external mutation-score semantics + report interop
Frozen expectation: `{status: "held", round: 25}`.

Independently derived latest declared status: **held (round 25)**, F1b open.
- `corpus/README.md:78` (frontier table row): `held (round 1)` — **stale**.
- `corpus/README.md:111-114` (fleet round-1 correction): F1 **partly held**
  (report interop not yet held).
- `corpus/README.md:133` (round 12): "F1 remains partly held" — still partly held.
- `corpus/README.md:385-395` (round 25): "**F1 status correction (supersedes
  lines 78 and 111–114 for the report-interop half only).** Report interop is now
  held for the eight recorded ledger legs …" — **held declared, round 25**; F1b
  (NoCoverage) explicitly open (lines 392-395).
- `corpus/README.md:413` (round 26): "F1 stays held and F1b open".
- `corpus/README.md:533` (round 42): "F1's report-interop half was already held
  under the round-25/26 entries (`:385-391`, `:413`) … with F1b (NoCoverage) open."
- `corpus/README.md:550` (round 43): F1's outcome vocabulary gains the survivor
  side; no status change, no new round.
- `corpus/knowledge/mte-report-interop.md:4` (`ground: F1`); `mutation-score-semantics.md:4`;
  `pit-outcome-vocabulary.md:6` — none declare a status.

**Match.** The lane's latest declared status is `held`, first declared in round 25;
the round-26/42/43 sections restate it without changing status. Nuance (disclosed):
F1's `held` applies to the report-interop half; the mutation-score-semantics half
was already admitted at round 1, and F1b remains open — the lane itself summarises
this as "F1 stays held and F1b open" (`:413`), so `held (25)` is the lane's own word.

### F2 — witness-scoped kill verdicts / bash mutation tooling
Frozen expectation: `{status: "partly held", round: 1}`.

Independently derived latest declared status: **partly held (round 1)**.
- `corpus/README.md:79` (table row): `held (round 1)` — superseded by the same
  round's correction.
- `corpus/README.md:115-118` (fleet round-1 correction): "**F2 — partly held.**"
  (one JS leg measured; witness declaration partly contaminated; no bash leg).
- `corpus/README.md:136` (round 12): "F2 remains partly held in the broad sense of
  bash mutation tooling".
- Round 13/17/22/30/31/32/35 sections state no frontier row changes status
  (`:161`, `:255`, `:357`, `:456`, `:464`, `:472`, `:485`).
- `corpus/knowledge/witness-scoped-kill-verdict.md:4` (`ground: F2`); `r8-gtest-primer-independence.md:4`
  (F3 + F2 upstream instance) — no status declaration.
- `corpus/lessons/round-1.md:486`: "F1/F2 `held` → `partly held`" (correction).

**Match.** No later section changes F2's status; `partly held` with round 1 stands.

### F3 — determinism precondition, flaky-aware verdicts
Frozen expectation: `{status: "open", round: null}`.

Independently derived latest declared status: **open (no round)**.
- `corpus/README.md:80` (table row): `open`.
- `corpus/README.md:338` (round 21): "F3 universal determinism stays open".
- `corpus/README.md:413` (round 26): "F3 stays open (one control per sweep)".
- `corpus/README.md:565` (round 45): "F3 stays `open`".
- `corpus/README.md:577` (round 46): "F3 stays `open`".
- `corpus/README.md:589` (round 47): "F3 and F7 stay `open`".
- Ground entries (repeated-control-precondition.md, flaky-aware-verdict-evidence.md,
  r5/r6, r8-gtest-*, r8-flakiness-not-static, r8-flaky-cost-baseline,
  r9-false-red-rate) all ground without declaring a status.

**Match.** Never declared held/partly held/Core; `open` with no round.

### F4 — golden / snapshot fixture discipline
Frozen expectation: `{status: "partly held", round: 38}`.

Independently derived latest declared status: **partly held (round 38)**.
- `corpus/README.md:81` (table row): `open` — **stale**.
- `corpus/README.md:491-497` (round 38): "After: F4 **partly held** — the
  *verdict lattice* is now held … and the *write-path census* … is still unmeasured
  and stays the next falsifiable move."
- `corpus/README.md:503` (round 39): census measured (`live_write_sites=99`,
  `live_unflagged=0`) but "The 0 is the pattern's count, not a claim that no
  unflagged write exists … Those limits stay open" — no status change to held.
- `corpus/README.md:511` (round 40): "The round-39 limits are now a successor tool,
  not a closed census … `cmp` and `git diff --exit-code` stay unmeasured."
- `corpus/README.md:519-524` (round 41): write-path half gains
  `tools/write-path-census-v3.py`; "now partly covered (`os.symlink` destination)
  and partly still outside (`shutil.*`, `handle.write`)".
- `corpus/README.md:533-542` (round 42): `tools/write-path-census-v4.py` reads 0
  unflagged sites over tracked `tools/` Python files, but "the note's 'What is not
  claimed' names the shapes the tool does not resolve".
- `corpus/lessons/round-38-verifier-spotcheck.md:62`: "F4 open → partly held with
  the boundary stated"; `round-39-verifier-spotcheck.md:67`: "the round-38 map
  left unmeasured" (consistent).
- Ground entries: `golden-comparison-verdict.md:5`, `r3-snapshot-fixture-update-paths.md:4`,
  `r8-golden-update-flag.md:4`, `r40-write-form-misses.md:4`, `r41-variable-destination-writes.md:5`,
  `r42-attribute-and-outflag-destinations.md:7` — none declare a status.

**Match.** rounds 39-42 refine the write-path half (tools, census counts) without
any declaration of `held`; the status cell remains what round 38 declared:
`partly held`, round 38.

### F5 — hermetic environment normalization
Frozen expectation: `{status: "Core", round: 21}`.

Independently derived latest declared status: **Core (round 21)**.
- `corpus/README.md:82` (table row): `open` — **stale**.
- `corpus/README.md:330-338` (round 21): "F5's finite method moves to **Core** for
  the six fleet-ledger gates … the H3 reference runner, and two explicit additions
  (round-gate and sources-check) … This is finite method acquisition, not closure of
  every possible F5 surface or proof of universal hermeticity."
- `corpus/knowledge/hermetic-env-differential.md:4`: "F5 — hermetic environment
  normalization; finite environment-differential method moves from Frontier to Core."
- `SCORECARD.md:870`: "C2 F5 hermetic env-differential → Core | coverage (frontier
  F5 → Core)"; `SCORECARD.md:895`: "F5 finite method moves to Core, not all possible
  environmental surfaces or universal hermeticity."
- `corpus/knowledge/r5-undetected-flaky-failures.md:4` grounds F5 alongside F3
  without a status declaration.
- No later section revokes or re-rounds F5.

**Match.** Core, declared round 21, never changed since.

## Disagreement check (F1..F5)
No disagreement found between the frozen expectations and the lane's latest declared
statuses: F1 held/25 ✔, F2 partly held/1 ✔, F3 open/null ✔, F4 partly held/38 ✔,
F5 Core/21 ✔. All four stale table cells (F1, F2, F4, F5) are exactly the cells the
frozen expectations supersede; F3's table cell already agrees.

Residual nuances disclosed (not disagreements): (1) F1's `held` is the
report-interop half; the lane keeps F1b open and says so in the same sentences —
the frozen `held (25)` is the lane's own wording at `README.md:413`; (2) F4's
rounds 39-42 improve the write-path half without ever declaring `held` — the frozen
round 38 is the last status-declaring round; (3) a lesson-local label "round17 F5"
(`corpus/lessons/round-24.md:210`, a round-17 routed defect about the
`--tag new-r23` selection guard) is not the frontier row F5 and does not conflict
with the Core status.

## Summary
- C1 frozen expectations F1..F5 were attacked by independent derivation from README
  sections, knowledge `ground:` lines, lessons and SCORECARD, before reading `basis`.
- All five frozen status+round pairs match the lane's latest declared statuses:
  F1 held/25, F2 partly held/1, F3 open/null, F4 partly held/38, F5 Core/21.
- The stale table cells `corpus/README.md:78,79,81,82` (F1/F2/F4/F5) are exactly
  the four the frozen expectations supersede; F3's cell (`:80`) agrees.
- No well-founded disagreement to disclose against C1 for F1..F5; every cited
  declaration is a same-file, same-round status statement with no later override.
- Nuances (F1's half-held wording, F4's post-38 tool-only refinements, the
  lesson-local "F5" label) are disclosed above as non-conflicts.
- Evidence is read-only (no receipts produced, nothing to copy into w1; no scratch
  used, nothing to clean up).
- Deliverable written to `.ufo/waves/round-51/w1/T51CritExpectedA.md`.
