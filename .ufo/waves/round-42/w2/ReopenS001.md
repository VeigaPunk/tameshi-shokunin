# ReopenS001 — round 42, wave 2 (FALSIFY)

Seat: `L1Tameshi42.ReopenS001`, read-only. Attacked: the round-42 S001 re-open (snapshot
`.ufo/evidence/round-42/sources/stryker-mutant-states.html`), the quote and timeout claims the
two new knowledge entries make from it, and the S001 used-by change logged in
`corpus/lessons/round-42.md`. Accessed 2026-10-25. No counter was run. No tools were installed.

## Findings

F1. **The live page is byte-identical to the snapshot.**
`curl -sSL -A "Mozilla/5.0" -o /tmp/tameshi-r42w2-ReopenS001-live.html -w "%{http_code} %{size_download}\n" https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/`
→ `200 27068`. `sha256sum` of the live file →
`ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11`. `cmp live snapshot` →
`IDENTICAL`. The same hash appears in `.ufo/evidence/round-42/sources/sha256.txt`, in the blob at
the integration tip (`git show a21845f5…:.ufo/evidence/round-42/sources/stryker-mutant-states.html | sha256sum`),
in `corpus/lessons/round-42.md:35-36` (27068 B) and in
`corpus/knowledge/r42-attribute-and-outflag-destinations.md:3`.

F2. **The line-26 quote is exact and sits under Runtime error.** In
`grep -n -o "It is not represented in your mutation score[^<]*" <snapshot>`, the quote appears at
`26:` and `31:`. With tags stripped, the snapshot reads:
- line 23: `Runtime error`
- line 26: "Don't spend too much attention looking at this mutant. It is not represented in your mutation score."
- line 27: `Compile error`. The second hit, line 31, is under Compile error.

The quote is 8 words, as `r42-attribute-and-outflag-destinations.md:60-61` and
`corpus/lessons/round-42.md:36-37` state. Both entries cite line 26 under Runtime error, which is
correct. Line 31 has the same wording under Compile error, but that does not change the claim.

F3. **Stryker counts a timeout as detected.** With tags stripped, the snapshot reads:
- line 17: `Timeout`
- line 21: 'It is counted as "detected".'
- line 39: `Detected killed + timeout`
- line 51: `Mutation score detected / valid * 100`
- lines 45-48: `Valid detected + undetected`, "They didn't result in a compile error or runtime error", `Invalid runtime errors + compile errors`

These lines support three claims:
- `pit-outcome-vocabulary.md:52-53`, "Stryker counts a timeout as detected (S001)".
- The Stryker half of `corpus/lessons/round-42.md:163-164`, "both tools count a timeout as detected". The PIT half rests on S158 and is outside this seat.
- `pit-outcome-vocabulary.md:38`: runtime errors are invalid and outside `detected / valid`.

The page lists eight states (Pending, Killed, Survived, No coverage, Timeout, Runtime error,
Compile error, Ignored; lines 8-32), which matches the S001 row's "eight mutant states".

F4. **The S001 used-by change matches the logged old → new.** I ran
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff c77c2b7e64d2e356381441ecf94abac03e984606 a21845f523b75adbd3e3f7a62af91294db224ad9 -- corpus/SOURCES.md`.
Its S001 hunk, at `corpus/SOURCES.md:12`, changes the used-by cell:
- old: `corpus/knowledge/mutation-score-semantics.md, corpus/knowledge/mutation-case-kumitate-sources-check.md`
- new: the old cell plus `corpus/knowledge/pit-outcome-vocabulary.md, corpus/knowledge/r42-attribute-and-outflag-destinations.md`

`corpus/lessons/round-42.md:89-90` logs the same change: S001 gains `pit-outcome-vocabulary.md`
and `r42-attribute-and-outflag-destinations.md`, with the paths given relative to `corpus/knowledge/`.

I split the old and new rows on ` | ` and compared them field by field. Only field 11 (used-by)
differs, and both rows have 11 fields. The other ten cells are unchanged. All four used-by files
exist at the tip, and each one cites S001 (`git show <tip>:corpus/knowledge/<f>.md | grep -c S001`
→ 12, 5, 5, 2). The SOURCES.md round-42 note in the same diff says the same thing: "S001 gains
both round-42 entries".

F5. **Observation, not a break.** The S001 anchor cell still reads "docs page fetched 2026-10-19".
It does not point to the round-42 re-open snapshot. That snapshot is cited from the entries and
the lesson instead. Because the bytes are identical today (F1), nothing that the row's anchor or
"teaches" cell says has drifted.

## Verdict
SURVIVES
