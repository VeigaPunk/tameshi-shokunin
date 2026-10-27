# T52W3RevGate — S274 / Gate review

## Findings

1. **S274 lacks the required located quote and its full source identity.** `corpus/SOURCES.md:149` has 11 columns and valid `docs`/`A` classifications, opened/recheck dates, a `mined` used-by path that resolves, and an anchor. But the `teaches` cell is a synthesized explanation, not the required ≤25-word verbatim quote; the anchor gives only a truncated hash (`2355150f…`) rather than the confirmed full digest. The lesson Gate does record quotes, but they are not in the row and do not cure the row's falsifiable claim/grounding. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/SOURCES.md` (line 149); compare `/home/vgpnk/Projects/shokunin/CORPUS.md:86-115`.

2. **S274's tier-A scope overstates Bazel's source.** The row scope says “hermetic build or test asserts” and “every declared input,” while the source describes hermetic *build systems/builds* and their inputs, not tests as a category. The Gate's scope-limit note correctly says applying it to a test is analogy, but that distinction is absent from the row's scope. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/SOURCES.md` (line 149); source text at `https://bazel.build/basics/hermeticity.md`, “Overview” and “Source identity”.

3. **Gate's displayed quotes do not match the opened source verbatim.** `corpus/lessons/round-52.md:9` quotes “hermetic build system always returns the same output by isolating the build from changes to the host system”, omitting the source's leading “When given the same input source code and product configuration, a” and changing its quote boundary; this is a fragment of a sentence, not the exact asserted quotation. The second quote “Hermetic build systems try to ensure the sameness of inputs” is verbatim (source's line wraps after “a”). The Gate otherwise supplies the URL, access date, and locations and quotes are below 25 words. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/lessons/round-52.md` (line 9); compare re-fetch below.

## Checks and evidence

- Re-fetched `https://bazel.build/basics/hermeticity.md` with `curl -L --fail --silent --show-error`; HTTP retrieval succeeded, 5878 bytes. `sha256sum` returned `2355150f5e9b08c392de169a67b788f4b3f0c446919a8abea9180bf9daccbbc6`, matching Gate's recorded digest. Both source sentences were confirmed; the precise first sentence begins “When given the same input source code and product configuration, a hermetic build system…”; the second appears under Source identity.
- Census validator unavailable in lane checkout at `scripts/sources-census.sh` (read returned not found); did not run a substitute validator. `CORPUS.md` documents the census contract at lines 131-147. This is a verification gap, not evidence of validator failure.
- LSP device/status unavailable in this environment (`read xd://lsp` returned “No such tool”); findings use pinned-revision text evidence and source comparison, not semantic-reference claims.

## Summary
- S274 has 11 columns, valid kind/tier, dates, and a resolvable used-by path.
- S274 row omits the required located verbatim quote and records only a truncated digest.
- Its scope classifies tests too broadly; Gate acknowledges the analogy but row does not.
- Gate first quote is not verbatim; second quote is accurate.
- Source re-fetch digest and 5878-byte size match the reported values.
- Census validator not available in lane; validation remains unverified.
