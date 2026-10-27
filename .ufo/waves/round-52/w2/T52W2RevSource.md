# T52W2RevSource — Bazel source and claim review

## Source reopen

Re-fetched `https://bazel.build/basics/hermeticity.md` (the HTML URL's declared Markdown alternate) on 2026-10-27. `curl -sS -L -o "$S/bazel.md" -w 'HTTP=%{http_code} SIZE=%{size_download} URL=%{url_effective}\n' https://bazel.build/basics/hermeticity.md` returned `HTTP=200 SIZE=5878 URL=https://bazel.build/basics/hermeticity.md`; `wc -c` returned 5878 and `sha256sum` returned `2355150f5e9b08c392de169a67b788f4b3f0c446919a8abea9180bf9daccbbc6`. Thus the wave-1 markdown snapshot's bytes/hash are reproduced. Fetched copy was in scratch, not retained as evidence; original snapshot is `.ufo/waves/round-52/w1/T52W1ScribeSource-snapshot.txt`.

Command used to locate quote literals: Python `str.find` against whitespace-normalized source, with `len(q.split())` for word count. The five source quote strings in S274 row were each found; offsets below are in the normalized page:

| Proposed quote | Words | Result |
|---|---:|---|
| “hermetic build system always returns the same output by isolating the build from changes to the host system” | 18 | Agree; found at 404; snapshot lines 12–14. |
| “In order to isolate the build, hermetic builds are insensitive to libraries and other software installed on the local or remote host machine” | 23 | Agree; found at 513; snapshot lines 16–17. |
| “This makes the build process self-contained as it doesn't rely on services external to the build environment” | 17 | Agree; found at 760; snapshot lines 19–20. |
| “Hermetic build systems try to ensure the sameness of inputs” | 10 | Agree; found at 1204; snapshot lines 28–29. |
| “Execute a build within a docker container that contains nothing but the checked-out source tree and explicit list of host tools” | 21 | Agree; found at 3521; snapshot lines 77–78. |

## S274 proposed row review

Against `tameshi-shokunin/corpus/SOURCES.md:10-11` and fleet `CORPUS.md:86-108`:

- **Agree** 11-column schema and no embedded pipe: row has 13 pipe-delimited fields (`NF=13`, the established encoding for 11 columns). The snapshot reports row validation; table header says `# SOURCES — where tameshi learns`, matching lane convention.
- **Agree** `docs` and tier `A`: official Bazel documentation is primary for the page's own definition of Bazel hermetic builds, within its scoped subject. Tier A is not a global endorsement.
- **Disagree, scope wording needs tightening:** `what "hermetic" asserts for a build or test run` generalizes from this page's claims about *hermetic builds* to test runs. The page is about builds; it does not define the hermeticity contract for arbitrary test runs. Recommend scope “Bazel hermetic-build definition and its described host/environment isolation” (or equivalent).
- **Agree with qualification** anchor names exact sections, URL, unversioned page's lastModified, open date, byte size/hash and snapshot; it is much better than a bare homepage. `§Identifying non-hermeticity` is an exact heading. Open date format and 180d recheck fit the contract. `mined` is conditional: `corpus/lessons/round-52.md` did not exist when checked, so status is only valid once that file exists and actually cites S274; until then use `queued` or make the lesson land before row. This follows `CORPUS.md:103-108, 112-115` (mined means used-by citation; row written after source open; lesson Gate must give URL/date/≤25-word quote/location).
- **Disagree on completeness at time of review:** S274 is not present in the lane SOURCES registry; the cited row is only in the wave-1 draft. Also it relies on a future `used-by` path. The draft reports S274 as the next unused ID based on `corpus/SOURCES.md:502`, but no live append/registry census was part of this review. No claim that it is already admitted/validly mined should be made.

## Claim-sentence judgments (draft lesson §4)

The lesson file `corpus/lessons/round-52.md` was absent when reopened, so judgments below are against the exact proposed sentences in `T52W1ScribeSource.md:73-97`, not a landed lesson.

1. **Agree, accurately bounded source quotation:** “A hermetic build system ‘always returns … host system’” closely matches Bazel §Overview (snapshot 12–14). The draft's next inference, “the outcome must be a function of declared inputs only,” is **not a direct quote or formal theorem stated in that sentence**. The page does separately discuss source identity and controlled tools; present that as an interpretation of Bazel's build definition, not as verbatim definition.
2. **Agree, source supports isolation statement:** the proposed host-software and external-services quotes (snapshot 16–20) are exact and support treating host libraries/software and external services as environmental dependencies the build should not silently rely on.
3. **Disagree, overstates what page establishes for this particular self-test:** the proposed factual mechanism says `round21-measure.py:77-84` obtains a fleet path by parsing `FLEET` from `.ufo/evidence/round-21/c2-count.py` and executes `git -C <fleet>/<repo> show <rev>:<path>`. Those lines establish an external filesystem/repository dependency relative to a standalone clone, if the stated fixture context is accurate. Bazel's build definition and container suggestion make that a plausible *analogy/diagnostic*, but the page does not define Python `--selftest`, a source checkout fixture, or this round's “hermetic” classification. So the source does not alone entail the categorical conclusion “the selftest is fleet-bound, not hermetic.” Label that as the authors' operational classification under an explicitly stated boundary (fresh clone/declared inputs), and cite the code plus an observed isolation test independently.
4. **Disagree, declared-input dichotomy is misstated:** “That is a declared input only if it is written down as one; it is not in the fixture's inputs” conflates documentation with actual environment. Declaring a path in prose does not make it an available/reproducible fixture input; conversely explicit runtime environment and captured fixture blobs can be inputs without being written as prose. Bazel says the container includes an explicit list of host tools and breakages catch implicit dependencies; it does not say every dependency becomes declared merely by writing it down. Reword to say the sibling repository is an ambient dependency unless the test environment supplies and controls it as an input.
5. **Agree on quote, disagree on conclusion as currently sourced:** the “nothing but checked-out source tree and explicit list of host tools” quote is verbatim and its stated purpose is to expose implicit system dependencies. It is a useful proposed falsifier for this case, but running a container is not necessary to establish the shown `git -C` read, and the page does not itself prove that this particular self-test's verdict changes with host state. The “verdict moves with the host's filesystem” sentence requires a demonstrated differential or otherwise careful qualification; a read dependency alone proves dependence, not outcome variation.
6. **Disagree, probe interpretation is not established:** the draft says host `--selftest` passing is “the non-hermetic signature” and means the dependency is invisible where the fleet root exists. A green run in one ambient environment does not show that; it establishes only that the selftest passed there. The code's external read is direct evidence of the dependency. Label the run as a probe and avoid treating its success as a signature.
7. **Agree as a repair fork, not a Bazel prescription:** supplying pinned sibling blobs as fixture inputs, or explicitly classifying the exercise as fleet-bound, are reasonable alternatives for this repository. The source supports isolation as a principle but does not prescribe those exact fixes. The draft cites a source-code docstring at `tools/round21-measure.py:9-12`; that is evidence of the implementation author's stated intent, not independent proof.

## Evidence commands and residual risk

- Source status/size/hash: `curl -sS -L -o "$S/bazel.md" -w 'HTTP=%{http_code} SIZE=%{size_download} URL=%{url_effective}\n' https://bazel.build/basics/hermeticity.md; wc -c < "$S/bazel.md"; sha256sum "$S/bazel.md"` → HTTP 200, 5878 bytes, hash above.
- Quote search/count: Python whitespace-normalized `str.find` and `len(q.split())` against fetched Markdown; all five quotes found, 10–23 words.
- Row contract: `tameshi-shokunin/corpus/SOURCES.md:1-11`; `CORPUS.md:86-115` and `:131-147` provide schema and mined/used-by/census semantics.
- Code location: `tameshi-shokunin/tools/round21-measure.py:77-84`, reread at CAND0. It extracts a path from frozen counter source and invokes `git show` against a sibling repo under that path.
- Residual risk: the fetched live source is an unversioned doc; this review reproduced the wave-1 markdown snapshot hash but did not fetch/re-hash the HTML alternate or independently execute a fixture differential. No claim is made about a landed lesson or SOURCES row because neither was present at review time.

## Summary
- Bazel Markdown source reopened: HTTP 200, 5878 bytes, SHA-256 matches wave-1 snapshot.
- All five proposed quotes are verbatim after whitespace normalization; each is ≤25 words.
- S274 shape/kind/tier are sound; scope overreaches from builds to arbitrary test runs.
- `mined`/`used-by` is conditional on the missing round-52 lesson landing and citing it.
- Bazel supports the isolation analogy, not a categorical verdict about this Python self-test.
- Direct `git show` evidence supports an external dependency; it alone does not prove verdict variation.
