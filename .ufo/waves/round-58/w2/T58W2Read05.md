# T58W2Read05: cold-read record

- Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534` (dispatch log agrees).
- Section: `### The service's limits — what tameshi refuses to mutation-test`, lines 1282–1311.
- Frozen round-18 section SHA-256: `7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6`.
- Recommendation: **verified-record**. No false rule or failing command found in scope.

## Sweep and evidence

Read the assigned section end to end in a shared clone detached at C0, compared rows a–j with the detailed refusal table and checked every immediate anchor. Commands plus their full outputs are in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2Read05-receipts/commands.json`; the full section/anchor sweep is also in `section-and-anchor-sweep.txt` there. The frozen API command prints:

```text
1282 1311 7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6
```

Sweep output includes:
```text
cadence section mentions service-limits: False
ledger mentions service-limits: False
compact row ids: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
detail row ids: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
All cited files/ranges resolve; ten refusal row identifiers agree. Semantic row comparison performed by reader, not proved by identifier equality.
```

Three supplemental refusal probes returned exit 2: missing old string (`old-string-count=0 expected=1`, no suite run), no-op (`@new equals @old`), and red control (`CONTROL: RED`, then SETUP). No DONE headline; target bytes unchanged in each observed probe. Tiny fixture inputs are preserved with the receipts. Base-to-C0 SKILL.md diff was empty (exit 0).

## Notes, residual risk and verification gaps

- Stale-but-true anchors (explicitly dated 2026-10-14 and accompanied by a re-resolve instruction): row b's current supporting text is SKILL.md:841-845 and :868-872; row c's is :840 and :851-853; row f's is :907-909. Their printed local ranges exist but no longer point at those particular statements. Treated as notes, not false refusal rules, because the section explicitly requires re-resolution on differing revisions.

- Compared all ten compact refusal rows against service-limits.md:46-55 and read the intake-precondition check at :172-185; no semantic divergence found. The compact h row retains the detail note's exit-code-only harness boundary, not a universal impossibility claim.

- The note's claim of cadence application is correctly attributed, not asserted as integration: the named cadence section and ledger contain no service-limits reference. Literal sweep is textual evidence only.

- LSP device unavailable: reading xd://lsp returned 'No such tool'. Used literal search and pinned source reads; no semantic LSP proof claimed.

- No executable command appears in the assigned section. Supplemental executable refusal probes covered absent old string, no-op mutation, and red control: each returned SETUP/2 without a DONE headline. No full suite, fleet substrate, C2 forgery, or independent historical measurement was run; these are outside this one-section reader scope.

- Axes: factual calibration, coverage of ten refusal rows, reproducible command/output evidence, no lane-source mutation. No tools installed or updated.

Own scratch is deleted before yielding; no lane source file was edited. Historical foreign-scratch counts and real live-session refusal behavior were checked as attributed source records, not independently replayed.

## Self-evaluation

Accuracy 4/5 (historical behavior remains source-attributed); completeness 4/5 (all immediate anchors and rows read, not every historical experiment replayed); clarity 4/5 (long raw commands isolated in JSON); actionability 5/5 (exact revision, digest, commands and outputs supplied); conciseness 4/5 (duplicated digest required for handoff). Overall 4.2/5. Highest-value improvement is refreshing the explicitly dated b/c/f local anchors; no source edit made by this reader.
