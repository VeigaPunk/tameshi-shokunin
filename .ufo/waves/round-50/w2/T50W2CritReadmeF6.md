# T50W2CritReadmeF6 — README `## Round 50` F6 status wording

Seat: `T50W2CritReadmeF6` (UFO-FSD critic). Item: is `F6 ... held (round 50)` justified for the stated scope at candidate `80ea77e99e239982ab0b93e416645ef2359725d3`, given the frontier row, the round-29 B5 stop, the wave-1 C2-counter attacks and CTL_REF? Do the two coverage rows say only what the entries hold? No verdict on the claim; this is a wording finding.

## Facts read (all at `80ea77e9` unless noted)

- `corpus/README.md` `## Round 50` section, lines 601-608. Line 608: "F6 (fixture minimization for survivors): open → **held (round 50)** for the method on killing cases — one shrinker that reduces a gate's killing case to a 1-minimal sub-case and states its run cost — conditioned on the round-50 deciding receipt `.ufo/evidence/round-50/after/c2.stdout` printing `C2_R50_PASS=true`; the round-29 B5 survivor is not discharged (it stays masked, `knowledge/survivor-fixture-minimization.md:53,57`), and if that receipt prints anything else this line is void as of round 50".
- Frontier table row F6, `corpus/README.md:83`: `| F6 | fixture minimization for survivors | S022, S023, S024 | open | B5 probe fixture size: unmeasured → reduced size + kill check |`. Unchanged from base `e3729de8` (the base→candidate README diff adds exactly the 9 lines of the Round 50 section at line 598+; the F6 row is untouched).
- No `.ufo/evidence/round-50/after/c2.stdout` exists at the candidate (path absent from the tree); the condition is a forward registration with a void clause.
- `corpus/knowledge/survivor-fixture-minimization.md:53` = "ddmin made 171 oracle tests and kept nothing, because no subset kills."; `:57` = "## The finding: B5 is masked under the pinned declaration". The section's `:53,57` citation is exact.
- `corpus/knowledge/fixture-shrinking-pilot.md` (new at candidate) and `corpus/knowledge/delta-debugging-minimization-contract.md` (new at candidate) are the entries behind the two rows.
- `corpus/SOURCES.md:146` S271 (Zeller & Hildebrandt, fetched 2026-10-26) — satisfies the contract's "opened 2026-10-26" sourced requirement; S022/S024 cells exist (SOURCES.md:33,35).
- Controls (frozen, scored at freeze bytes): `c2-CTL_REF.stdout` prints `mutants=20 ok=20 units_before=164 units_after=43 … C2_R50_PASS=true` (greedy reference loop passes 20/20); `c2-CTL_ABSENT.stdout` false (shrinker_absent=1); `c2-CTL_IDENTITY.stdout` false (minimal=0); `c2-selftest.stdout` `cases=9 failed=0`.

## Q1 — Is "held (round 50)" justified for the stated scope?

The scoped, conditional core IS justified:

1. The scope qualifier is present and correct: "for the method on killing cases". The contract's C2 axis itself frames the hold as the method-with-cost surface (`contract.json:47,59`), and the claim explicitly does not touch the survivor arm.
2. B5 is disclosed, not hidden: the section names the round-29 stop and cites the exact lines (`survivor-fixture-minimization.md:53,57` — "kept nothing, because no subset kills"; "B5 is masked under the pinned declaration"). The B5 probe cannot be run because no killing subset exists under the pinned declaration, so the row's next move is blocked for a documented reason.
3. The hold is conditional on the deciding receipt with an explicit void clause — it claims nothing about the receipt before it exists.
4. CTL_REF calibrates the bar: the frozen counter's own greedy-to-fixpoint loop passes 20/20 (units 164→43), so "held" is not beyond the reachable predicate; the claim is capability-with-cost, not search efficiency, exactly as the entry and contract say.

Two features of the wording overclaim:

- O1 — status authority conflict: the canonical `## Frontier` row (README:83) still says `open` with next move "B5 probe fixture size: unmeasured → reduced size + kill check". The section's bare "held (round 50)" tag therefore coexists with the tree's own frontier table saying open. The lane's convention for a held row whose next move is blocked is to annotate the move `U` (see F1 row, README:78: "(validator unavailable this round: U)"). The F6 row has no such annotation, so the two authorities (table vs section) disagree without reconciliation.
- O2 — measurement clause overstates force: row 1 (README:604) says the frozen counter "re-checks sub-case, kill, 1-minimality and cost itself on 12 public and 8 hidden mutants". Wave-1 attacks show the counter does not certify what a PASS would assert:
  - `T50SentinelShrink.md` F2 (High) / `T50CritC2Contract.md` Finding 1 (SEVERE): `.runs` lives inside the shrinker's cwd (`measure.py:282-284` vs rewritecwd=shr` at `:276-277`); the audited party owns the log. Demonstrated: real search with instrumentation stripped passes with `runs=0 logged=0`; 5000 fabricated lines also accepted. The "stated run count equal to the logged guard invocations" term is unfalsifiable in both directions.
  - `T50SentinelShrink.md` F1 (Critical): the shrinker can overwrite the counter's judge copies (`../ver/mutant.py`, `measure.py:254-258` vs `:289`) before the judge runs; the forged run prints `C2_R50_PASS=true` with kills/minimality tautologies and no shrinking.
  - `T50CritC2Contract.md` Finding 2 (SEVERE): a precomputed lookup keyed by mutant source passes the 12 public mutants with zero runtime search; the counter cannot distinguish lookup from delta debugging.
  So "re-checks ... cost itself" describes the registered design, not what the measurement guarantees; a PASS receipt would not certify the stated cost or any search.

## Q2 — Do the two coverage rows say only what the entries hold?

Yes — both rows are faithful to their entries:

- Row 1 (README:604) vs `fixture-shrinking-pilot.md`: units (registry/staged lines, map entries), kill definition (oracle None on pristine / non-None on mutant), delta debugging to a single-unit fixpoint with verdict caching, every guard run counted in `runs`, 12 public + 8 hidden mutants, and the limits list (line-level units, tiny cases, one gate, greedy loop meets the same bar, B5 not discharged) all match the entry's text, including its "What this does not establish" list.
- Row 2 (README:605) vs `delta-debugging-minimization-contract.md`: "staged S167, re-grounded as S271", the 1-minimality witness as a removal that loses the failure, "57 runs for the source's 896-line reduction, 139 only as the case study's two-reduction total" (the entry's refused-package correction is reflected), and "what is new against the held S024 restatement" all match. Sources S271/S022/S024 match the entry headers.
- The one clause that reaches beyond what the measurement can hold ("re-checks ... cost itself") is shared with the entry — it is a row-vs-reality gap, not a row-vs-entry gap.

## Verdict: overclaims (bounded) — scoped conditional core justified; two wording corrections

The section's core (scoped to the method on killing cases, B5 disclosed and cited, conditional on the receipt with a void clause) is justified, and CTL_REF shows the bar is calibrated. What overclaims is (a) the bare "held (round 50)" tag placed while the canonical frontier row still reads open and its B5 next move carries no `U` annotation, and (b) the "re-checks ... cost itself" clause, which the wave-1 demonstrations show the frozen counter cannot deliver (self-owned log, rewritable judge, lookup passes).

### Exact wording I would land

Line 608 replacement:

> F6 (fixture minimization for survivors): the method on killing cases → **held (round 50)** — one shrinker that reduces a gate's killing case to a 1-minimal sub-case and states its run cost — conditioned on the round-50 deciding receipt `.ufo/evidence/round-50/after/c2.stdout` printing `C2_R50_PASS=true`; the frontier row's survivor arm, the B5 probe, stays open and masked (`knowledge/survivor-fixture-minimization.md:53,57`) and is marked U in `## Frontier`; if that receipt prints anything else this line is void as of round 50

Row 1 (README:604) measurement clause replacement:

> measured by a frozen counter that re-checks sub-case, kill and 1-minimality itself on 12 public and 8 hidden mutants, and requires the stated runs to equal the logged invocations (the log sits in the shrinker's cwd, so the cost term is not independently authenticated — w1 `T50SentinelShrink.md` F2, `T50CritC2Contract.md` F1)

Frontier row F6 (README:83) sync:

> | F6 | fixture minimization for survivors | S022, S023, S024 | held (round 50) for killing cases; survivor probe open | B5 probe fixture size: unmeasured → reduced size + kill check (U: masked, `knowledge/survivor-fixture-minimization.md:53,57`) |

(If the lane prefers to keep the frontier row update for the round close, the section must at least not carry the bare "held (round 50)" tag without the `U` marker on the row's next move.)

## Summary

- Scoped conditional "held" core: justified; B5 disclosed at the right lines; receipt condition + void clause present; CTL_REF (20/20, 164→43) calibrates the bar.
- Overclaim O1: frontier row F6 (README:83) still open with unmoved B5 next move and no `U` annotation — the tree carries two disagreeing statuses.
- Overclaim O2: "re-checks ... cost itself" (README:604) is not supported after w1 (self-owned log, judge rewrite, lookup passes — SentinelShrink F1/F2, CritC2Contract F1/F2).
- The two coverage rows say exactly what the entries hold (including the 57/139 correction); the defect is shared with the entry, not a row-vs-entry discrepancy.
- No underclaim found.
