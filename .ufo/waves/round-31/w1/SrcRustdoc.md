# SrcRustdoc — S097

**Verdict:** The rustdoc book was opened from its canonical URL. Its `Documentation tests` section directly supports the proposed S095 row and the learner benefit below. The requested `mined` status is not contract-valid yet: the named `used-by` knowledge file was absent when inspected.

**Axes:** source coverage; provenance; SOURCES contract fit.

## Evidence

- Read `CORPUS.md:86–107`: 11-column header, field meanings, and `mined` means “cited by ≥1 path in `used-by`” (`CORPUS.md:103–108`). Read the frozen registry header and S092–S094 using the command below; its output shows S095 as the next unused id (`artifact://20170:5–11,101–103,364`).
- Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c111dab58b0a8d55e991bbd2efe3aad56717b95a:corpus/SOURCES.md`
  - Observed: the 11-column header; rows S092, S093, S094; and `- Next unused id: S095.` The captured output is `artifact://20170`.
- Opened URL: https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html
- Fetch command: `mkdir -p /fast/scratch/hyaku/tameshi-r31-seats/SrcRustdoc && date -u '+%Y-%m-%dT%H:%M:%SZ' && curl -L --fail --silent --show-error https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html -o /fast/scratch/hyaku/tameshi-r31-seats/SrcRustdoc/documentation-tests.html && stat -c '%s' /fast/scratch/hyaku/tameshi-r31-seats/SrcRustdoc/documentation-tests.html && sha256sum /fast/scratch/hyaku/tameshi-r31-seats/SrcRustdoc/documentation-tests.html`
  - Observed output: `2026-10-23T09:05:40Z`; `51137`; `95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7  /fast/scratch/hyaku/tameshi-r31-seats/SrcRustdoc/documentation-tests.html`.
- The local HTML is `/fast/scratch/hyaku/tameshi-r31-seats/SrcRustdoc/documentation-tests.html` (51,137 bytes; SHA-256 above). It has `#documentation-tests` at HTML line 180; lines 181–182 state that rustdoc executes documentation examples as tests and thereby keeps them up to date and working. `rustdoc --test` extracting and running an example is also stated at lines 193–195.
- `corpus/knowledge/executable-self-assessment.md` was not found when read; the `corpus/knowledge/` listing did not contain it. Contract conflict, verbatim: `CORPUS.md:103` defines `mined` as “cited by ≥1 path in `used-by`”; this assignment requires status `mined` with used-by `corpus/knowledge/executable-self-assessment.md`.

## Draft registry row

```md
| S095 | Documentation tests (The rustdoc book) — https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html | docs | A | rustdoc's execution of documentation examples as tests | §Documentation tests (#documentation-tests), HTML lines 180–182 @ page fetched 2026-10-23 (sha256 95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7; 51,137 bytes) | rustdoc runs documentation examples as tests to check that they remain up to date and working | mined | 2026-10-23 | on-release | corpus/knowledge/executable-self-assessment.md |
```

**Gate:** URL https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html; accessed 2026-10-23 UTC; quote: “rustdoc supports executing your documentation examples as tests. This makes sure that examples within your documentation are up to date and working.” — §Documentation tests (`#documentation-tests`), HTML lines 180–182 (22 words).

## Behavior, gates, and surfaces

- Behavior grounded: rustdoc executes documentation examples as tests so stale or broken examples are caught.
- Gates: no project gate, build, test, or counter was run.
- Touched surfaces: this report; the fetched HTML artifact in this seat's scratch directory. No product file or registry was edited; the L1 owns committing the row.
- Out of scope: no knowledge entry was created and no claim is made that the requested `used-by` target exists. Smallest safe integration is to land that cited knowledge entry before committing this row as `mined`; otherwise the status would violate the SOURCES contract.

## Execution note

The scratch directory did not exist for the first attempted fetch, which failed before running. The successful fetch-and-metadata command above ran with shell cwd `/home/vgpnk/Projects/shokunin` and wrote only the HTML file under the permitted scratch path; the follow-up size and digest check ran with cwd `/fast/scratch/hyaku/tameshi-r31-seats/SrcRustdoc`. The frozen `git show` was read-only. No tool was installed.