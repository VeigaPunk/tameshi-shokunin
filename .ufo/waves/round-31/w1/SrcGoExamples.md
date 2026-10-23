# SrcGoExamples — S096

**Verdict:** The source was fetched and opened. One `mined` registry-row draft is ready for the L1; no production file was changed.

## Behavior and evidence

The official Go blog article says package examples are displayed as documentation and verified by running them as tests (Introduction, HTML lines 462–467). Under “Examples are tests,” it says examples are compiled and optionally executed as part of a package test suite (lines 473–479). Under “Output comments,” it says the test captures standard output, compares it with the comment, and passes only when they match (lines 512–519). This supports the row's bounded teaching; it is not evidence that a Go test was run for this assignment.

Fetch command, run from `/fast/scratch/hyaku/tameshi-r31-seats/SrcGoExamples/`:

```sh
timeout 30s curl --location --fail --silent --show-error --max-filesize 2000000 --output go-examples.html https://go.dev/blog/examples && printf 'url=https://go.dev/blog/examples\naccess_date_utc=' && date -u +%F && printf 'bytes=' && wc -c < go-examples.html && printf 'sha256=' && sha256sum go-examples.html
```

Observed output; command exited 0:

```text
url=https://go.dev/blog/examples
access_date_utc=2026-10-23
bytes=40059
sha256=1a40ae77c967d7e203b8d7706784bd6633542ff3583d197d854755233c958178  go-examples.html
```

Registry format and neighboring IDs were read with:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c111dab58b0a8d55e991bbd2efe3aad56717b95a:corpus/SOURCES.md
```

It exited 0. The frozen registry has the 11-column header, rows S092–S094, and an allocation note saying “Next unused id: S095.” The assigned source ID is S096; S095 remains an allocation gap in the frozen copy. The SOURCES contract was read at `/home/vgpnk/Projects/shokunin/CORPUS.md:64-115`.

## SOURCES row draft

```markdown
| S096 | Testable Examples in Go (Andrew Gerrand) — https://go.dev/blog/examples | docs | A | the Go blog's documented behavior of package examples, including output-comment verification | §Introduction, §Examples are tests, and §Output comments; HTML lines 462-467, 473-479, 512-519 @ article published 2015-05-07, fetched 2026-10-23 UTC (40059 bytes; SHA-256 1a40ae77c967d7e203b8d7706784bd6633542ff3583d197d854755233c958178) | Go examples appear in documentation and are compiled or run as tests; with an Output comment, the test passes only when captured standard output matches the comment | mined | 2026-10-23 | 180d | corpus/knowledge/executable-self-assessment.md |
```

## Gate

Gate — URL: https://go.dev/blog/examples; access date: 2026-10-23 UTC; quote (§Output comments, HTML lines 514–517): “The test passes if the test’s output matches its output comment.”

## Surfaces, gates, and limits

- **Touched:** the source copy `/fast/scratch/hyaku/tameshi-r31-seats/SrcGoExamples/go-examples.html` and this report, `.ufo/waves/round-31/w1/SrcGoExamples.md`.
- **Gates:** the bounded curl fetch succeeded (exit 0); the frozen `git show` read succeeded (exit 0). No tests, counter, or other project gates were run.
- **Out of scope:** committing the row, editing `corpus/SOURCES.md`, creating or editing knowledge content, and running Go examples.
- **Known limit:** the requested used-by path `corpus/knowledge/executable-self-assessment.md` was not present when checked. I did not create it. The draft follows the assigned `mined` status and used-by value; the L1 should ensure that knowledge entry exists and cites S096 when integrating the row.
- **Provenance:** no tools installed or updated. The source bytes, date, size, digest, quote, and article anchors above are from the successful fetch and opened HTML copy.
