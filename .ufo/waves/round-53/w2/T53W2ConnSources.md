# Cross-lane source adjacency

## Evidence

Read-only registry search across `/home/vgpnk/Projects/shokunin/*/corpus/SOURCES.md` found:

- `https://bazel.build/basics/hermeticity`: tameshi row **S274** (line 149). No sibling registry row matched this URL in the fleet search.
- Tameshi **S275** is the mutation-testing paper at `https://doi.org/10.1145/3540250.3558911`; **S276** is the long-standing-mutants paper at `https://arxiv.org/abs/2212.11762` (lines 150–151). Neither URL was matched in sibling registries.
- The tameshi S275/S276 subjects and URLs are distinct from kotodama S275/S276, which are Malagan sources (`collection-lacharriere.quaibranly.fr/en/malagan-head` and the PagePlace preview PDF). Their numbering is lane-local, not evidence of shared source rows. The sibling matches are exact URL strings, not ID matches.

Report search for round-53 artifacts mentioning merge/tameshi found potential adoption/overlap evidence in:

- `mori-shokunin/.ufo/waves/round-53/w1/Mo53RevSourcesRows.md`
- `chousa-shokunin/.ufo/waves/round-53/w1/R53ConnCrossClaim.md`
- `chousa-shokunin/.ufo/waves/round-53/w1/R53ConnSiblings.md`
- `chousa-shokunin/.ufo/waves/round-53/w1/R53ExecAdopt.md`
- `kotodama-shokunin/.ufo/waves/round-53/build/ConnectSiblingGesture.md`

The term search surfaced these reports but does not establish that any adopted the tameshi rows: the listed tameshi URLs do not appear as sibling registry rows. No sibling registry row for Bazel hermeticity was found either.

## Axis and bounded move

Affected axis: **operability**. Preserve URL-based adjacency checks alongside source-ID checks in cross-lane source census/reporting. S275/S276 are demonstrably reused as IDs for unrelated sources; treating IDs as globally identifying a source would create false overlaps. This is a bounded reporting/checking improvement, with no change to lane registries.

## Risks / verification

A URL-string census misses redirects, mirrors, or semantically equivalent editions; it supports only the stated absence of exact URL matches. Report keyword hits are leads, not proof of adoption; the cited reports need direct content review before claiming semantic overlap. Verification performed here: globbed sibling `corpus/SOURCES.md`, searched the target URLs and S275/S276 strings, and searched round-53 markdown artifacts for `S275`, `S276`, `merge`, and `tameshi`. No files outside the seat report were written.