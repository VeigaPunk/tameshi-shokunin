# ScoutS132 — Open S132 (axis: depth)

## Finding

**README row D29 title cell** (at `.ufo/evidence/round-40/sources/s132-readme.md:33`):

> Snapshot Testing: Use With Care - Randy Coulman

(Full row: `|D29|Snapshot Testing: Use With Care - Randy Coulman |https://randycoulman.com/blog/2016/09/06/snapshot-testing-use-with-care/|`)

## Pinned artefact: raw README — YES

The pinned artefact is the **raw README**, not the GitHub HTML blob page.

Evidence:

- `.ufo/waves/round-40/assimilation/append-block.md:1` and
  `.ufo/waves/round-40/assimilation/validate/corpus/SOURCES.md:121` record S132's URL as
  `https://raw.githubusercontent.com/VictorGazzinelli/snapshot-testing/master/README.md`
  — the `raw.githubusercontent.com` endpoint serves the raw Markdown bytes, not the
  `github.com/.../blob/...` HTML rendering.
- The source row states "README row D29, raw README opened 2026-10-24, sha256 8871d19c".
- `sha256sum .ufo/evidence/round-40/sources/s132-readme.md` →
  `8871d19c34165b60b5847f390955c247d8665758ecddb206448127bf3b1922ea` — prefix
  `8871d19c` matches the registry pin, and the file content is Markdown table text
  (pipe-delimited rows), consistent with raw README bytes rather than GitHub HTML.

## Confidence

High — observed file content, hash prefix match, and two independent registry rows agree.

## Remaining unknowns

None for this item. Row D29 is also referenced in the frozen claim line as the row naming
"Snapshot Testing: Use With Care" among the table's primary documents — observed consistent.
