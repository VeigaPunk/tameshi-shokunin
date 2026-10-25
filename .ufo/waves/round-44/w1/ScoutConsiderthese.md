# ScoutConsiderthese — round 44 proposal scan

## Axes and evidence boundary

The frozen round-44 contract names C1 calibration and C2 freshness; C1 is the lowest non-retired axis (6). This read-only scan finds the closest 2026-10-24 proposal to C1 is proposal 2, which directly concerns revision provenance; its wording is quoted below. The 2026-10-24 reflection itself says all five proposals were mined by the lane, and round-42 lesson confirms proposal 5; round-38 through round-41 records establish proposals 2, 4, 3, 1 respectively. Thus none of the five is still unmined. “Unimplemented” here means the proposal's specific ongoing check is not evidenced as a standing capability: the cited checks were mined into criteria / local round work, but no evidence found shows a general per-round provenance audit that flags every unreachable cited revision.

## 2026-10-24 proposals, status

1. **Pin blast-radius report before a tool edit.** **Mined; implemented as a rule/process.** Round 41 lesson records the amendments array naming old/new digests and broken pins; QUALITY criterion 80 requires that pre-edit table. Not the still-unimplemented pick.
2. **Unreachable-provenance check.** **Mined; specific proposal remains unimplemented as a standing check.** Round 38 lesson explicitly mines proposal 2, grounding it in the scratch-only revision `91373d55…`, and QUALITY 76 captures the unreachable-revision case. That is an implemented criterion and one demonstrated instance, not evidence of a general recurring check over every receipt. Closest to round 44 C1 because both concern whether records/citations agree with repository state and revision provenance.
3. **Persistently unreachable sources.** **Mined; implemented as a generalized criterion/practice.** QUALITY 79 and round-40 lesson cite proposal 3, pinned snapshots, and the repeated GNU page timeout; not the still-unimplemented pick.
4. **Attempt and dispatch health per round.** **Mined; implemented.** Round 39 lesson and QUALITY 78 record parent-exit settlement behavior and the falsifiable UNSETTLED fixture; not the still-unimplemented pick.
5. **SHONEN promotion readiness.** **Mined, table-only; not an implementation.** Round 42 lesson states it is the one 2026-10-24 proposal not mined before, then records the four-box table for the operator. It does not promote boxes or create a standing promotion gate.

Proposal 2 text (verbatim): **“Unreachable-provenance check.** Flag any receipt that cites a revision not reachable from the lane repo. The round-36 closure found an emptied-panel mutant commit (`91373d55…`) that only existed in a scratch clone, and round 37 spent a commit on it.” (2026-10-24.md lines 66–67.)

## Recommendation for this round

Recommend landing proposal 2 as a **QUALITY criterion** (rather than only a retrospective lesson): define the scoped receipt/citation surface and require each cited revision to resolve and be reachable from the lane history at the measured revision; retain a falsifier using the known scratch-only object. Cite `considerthese/2026-10-24.md` and date 2026-10-24 in the criterion, alongside the round-38 evidence. A lesson can record that instance, but by itself would not make the recurring check durable. No source-registry row is appropriate: this is an operator proposal, not external-source knowledge.

## Sources / observed details

- `.ufo/evidence/round-44/contract.json:17-36,38-46` declares C1/C2, axes and claims.
- `considerthese/2026-10-24.md:61-75` lists all five proposals; `considerthese/2026-10-25.md:48-59` explicitly says all five were mined and gives their mined destinations.
- `corpus/lessons/round-38.md:84-93` explicitly mines proposal 2; `corpus/QUALITY.md:938-997` records criterion 78 (proposal 4), criterion 79 (proposal 3), criterion 80 (proposal 1). `corpus/lessons/round-42.md:140-153` confirms proposal 5 mining as an operator-facing table.
- `corpus/lessons/round-39.md:43-45` documents round-39 guard lineage for dispatch health; QUALITY criterion 78 supplies its durable rule/falsifier.

This is source-text evidence only; I did not query LSP, run commands, measure claims, or modify lane files other than this assigned report.
