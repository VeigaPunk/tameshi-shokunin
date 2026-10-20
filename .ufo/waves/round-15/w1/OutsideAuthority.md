# Outside-authority reconstruction — round 14

## Finding

A review self-dispatched inside the tameshi wave is lane-internal advice, not outside admission or promotion. The reviewer role/task label does not change who commissioned the review or its authority. Round 14's outside admit/reject sample belongs to the separate non-author closure; seat reports may inform that closure but cannot stand in for it.

## Evidence chain

- `corpus/lessons/round-12.md:20-25` explicitly rejects treating lane-dispatched reviewers as outside admission/promotion and assigns the admit/reject spot-check to external closure. Its `:207` reiterates that final claim admission belongs to the separate non-author closure.
- `corpus/lessons/round-14.md:64-67` says the round-13 outside review was not a round-14 admit/reject sample, all dispatched seats belong to tameshi, and a separate non-author closure owns round-14 admission and sampling; it claims no `[x]`.
- The round-14 wave specification (`.ufo/waves/round-14/spec.json`, `items[].role`) assigns reviewer seats within the tameshi wave. The outside note's header (`corpus/lessons/round-14-verifier-spotcheck.md:1-7`) identifies its author as the non-author integrator and records the admission decision. Its `:117-128` calls the table the actual claim-level outside spot-check and records its agree/reject judgments. This is the source-backed distinction: same-wave reviewer reports are not the external decision.
- The historical context source reinforces the narrow claim: `.ufo/evidence/round-14/capture-context.py:2-18,26-29` describes a prospective, bounded observation and states its exit map, while `:553-580,605-643` shows source/mapping or observation mismatches becoming `mismatch`/exit 1 and unexpected arguments returning 64. `SKILL.md:1592-1602` nevertheless recorded it as a probe, with no standalone selftest and no 64 classification. The routed correction is stated explicitly in `corpus/lessons/round-14-verifier-spotcheck.md:160`.

## Exact minimum correction

1. **Authority:** keep any self-dispatched review explicitly lane-internal/advisory. Do not describe it as outside admission, an independent sample, promotion evidence, or an `[x]`. A separate non-author closure must own the outside claim-level judgment. No change to round-14 historical text or evidence is warranted to establish this boundary; it is already explicit there.
2. **Routed context-tool conformance (for the active maintained command, not this review):** register the maintained context command as a **gate**, because its persisted source/mapping expectations can produce a mismatch verdict and exit 1; add a standalone hermetic self-invocation that runs the public CLI on isolated synthetic fixtures and asserts literal expected exits and stable finding IDs; explicitly classify exit 64 as usage/could-not-evaluate. Preserve the historical round-14 script and receipts. This correction makes a tool's contract testable; it does not confer outside-admission authority on its author, its selftest, or another same-wave reviewer.

## Scope boundary and confidence

This is a status-neutral C1 calibration/conformance correction only. It does not revise the scalar, admit another claim, create a mutation case/rate, prove broad environment independence or result reuse, or authorize sibling execution. The strongest evidence for the authority boundary is explicit and repeated in the round-12 and round-14 lessons and the non-author closure note; confidence is **high**. The gate classification follows the historical source's checked expected predicates and explicit routed defect; no current active implementation was evaluated here.

LSP was unavailable: `read xd://lsp` returned `No such tool`. I used direct source reads; text search was discovery only. No checks, builds, tests, or runtime commands were run. No tools were installed or updated.