# Source S099 — Mutation adequacy

## Verdict

Suitable as the requested primary source: the official PIT page directly describes seeded mutations, rerunning tests, killed versus surviving mutants, and the killed-mutation percentage as a test-quality measure. The homepage URL is not already a row; existing S047/S048 are the separate PIT incremental-analysis URL. Draft row below is for the L1 to commit.

## Evidence

- Read `/home/vgpnk/Projects/shokunin/CORPUS.md`, §“SOURCES.md — where a shokunin learns,” lines 64–115. The contract specifies 11 columns, scoped tiers, exact anchors, `mined` usage, and a Gate quote of at most 25 words with location.
- Read the frozen registry using `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c31814978969a41a8e9b0f7d99fa308c5993c1b7:corpus/SOURCES.md`; it emitted the table header and S094–S096. The PIT homepage URL is distinct from S047/S048's `/quickstart/incremental_analysis/` URL.
- Searched `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` for `https://pitest\.org/([[:space:]]|\||$)` before fetching and again afterward: both searches returned “No matches found.” Searched the assigned ID `S099` in the same file: “No matches found.”
- Opened the source with this command from the assigned scratch directory: `curl --location --fail --max-time 45 --max-filesize 2097152 --silent --show-error --output pitest-homepage.html https://pitest.org/ && printf 'access_date_utc=' && date -u +%F && printf 'bytes=' && wc -c < pitest-homepage.html && sha256sum pitest-homepage.html`.
- Observed output: `access_date_utc=2026-10-23`; `bytes=12023`; SHA-256 `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc` (`pitest-homepage.html`). Downloaded HTML lines 101–114 are under “What is mutation testing?”; lines 110–112 describe seeded faults and kill/live outcomes, and line 114 states how the killed percentage gauges test quality.

## Draft SOURCES row

```text
| S099 | PIT Mutation Testing — https://pitest.org/ | docs | A | PIT's description of seeded mutation testing and the killed-mutant percentage as a test-quality measure | §What is mutation testing?, HTML lines 110–114 @ page fetched 2026-10-23 UTC (12,023 bytes; SHA-256 b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc) | faults are seeded as mutations, tests are rerun, test failure kills a mutant and passing lets it live; the killed-mutant percentage gauges test quality | mined | 2026-10-23 | 180d | tools/tally-audit.py; corpus/knowledge/runner-tally-audit.md |
```

## Gate

Gate: URL `https://pitest.org/`; access date `2026-10-23 UTC`; quote: “The quality of your tests can be gauged from the percentage of mutations killed.” — §What is mutation testing?, downloaded HTML line 114 (14 words).

## Behavior and bounds

PIT's account supplies the conceptual basis for checking whether a regression suite detects seeded faults and for treating killed-mutant share as a quality measure. It does not establish the correctness of tameshi's tally implementation, a run of `tools/tally-audit.py`, or any measured mutation score.

The two prescribed `used-by` paths were checked with `read` and both returned “Path ... not found” at report time: `tools/tally-audit.py` and `corpus/knowledge/runner-tally-audit.md`. The requested `mined` status is therefore a draft for the L1's planned downstream artifacts, not an observed current citation. The SOURCES contract defines `mined` as cited by at least one `used-by` path; if the row is committed before either path exists, the smallest contract-safe correction is `queued` until a path exists, then log the status transition to `mined`.

## Touched surfaces, gates, and out of scope

- New report: `.ufo/waves/round-32/w1/SrcMutationAdequacy.md`.
- Source copy: `/fast/scratch/hyaku/tameshi-r32-seats/SrcMutationAdequacy/pitest-homepage.html` (12,023 bytes; SHA-256 above).
- No production file or `corpus/SOURCES.md` row was changed; the fenced row is for L1 integration.
- No build, test, tally audit, mutation-runner execution, judge invocation, commit, or publish was performed. This report evaluates the source only; it makes no runtime or producer-authentication claim.
