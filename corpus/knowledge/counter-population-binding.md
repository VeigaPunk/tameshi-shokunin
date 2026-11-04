source: S103 — Git, git-hash-object documentation — https://git-scm.com/docs/git-hash-object — §DESCRIPTION, first sentence; S289 — Git, git-cat-file documentation — https://git-scm.com/docs/git-cat-file — §DESCRIPTION (blob at a revision); S291 — Git, index-format documentation — https://git-scm.com/docs/index-format — §Cache entry (mode field); S305 — Git, git-ls-tree documentation — https://git-scm.com/docs/git-ls-tree — §OPTIONS `-r` and the listing form; S294 — Git, gitattributes documentation — https://git-scm.com/docs/gitattributes — `text` attribute, end-of-line conversion (re-opened 2026-11-04; the page's furniture moved, the contract did not); all opened 2026-11-04. Own-work: tools/defect-bind.py at `4005a48ac73a66c794ff8fd528e6926633fe2af3`.
verified-at: 2026-11-04 — the instrument measured `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0 manifest=bound` at `b6658e7a`; the narrowed-manifest control is refused `manifest-rev-mismatch` exit 2 (`.ufo/evidence/round-82/final/c1-narrowed-refused.txt`); the base reading is `rows=5 closed=5` exit 0 (`.ufo/evidence/round-82/controls/c1-before-narrowed-certifies.txt`).
recheck: 180d — re-run `python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json --manifest-rev HEAD` and re-open S294 if the binding's declared limit is ever claimed without it.

# Counter population binding: bind the denominator to bytes, and read the object's type

## Why the population is part of the verdict

A counter's verdict is `mismatches / population`. If the population is read
from a path in the worktree, the same tool that reports `rows=6 closed=6` can
report `rows=5 closed=5` after a caller deletes a row — and both readings exit
0 (measured: `.ufo/evidence/round-82/controls/c1-before-narrowed-certifies.txt`).
The register therefore has two halves that must both be bound:

1. **The bytes.** `--manifest-rev REV` requires the manifest on disk to be
   byte-identical to `REV:<manifest path>` before any row is measured. A
   mismatch is `manifest-rev-mismatch`, exit 2, no row effect. This is the
   binding S103 states: the object id names the content, and S289 is how the
   content is read.
2. **The object kind.** A row that means "a regular file is committed here"
   cannot be satisfied by *presence*: `git cat-file -e REV:PATH` accepts a tree
   and a symlink as readily as a file (measured at the base: a directory row
   read `state=closed detail=paths-present`). The row must read the entry's
   mode and type from `git ls-tree -z` (S305's listing form; S291's mode field
   — only 0755/0644 are regular files, symlinks are a distinct type). A
   symlink is the sharper case: its blob is the *target string*, so a
   mode-blind `min_bytes` measures the link, not the artifact.

## Declared limit

`--manifest-rev` compares worktree bytes to blob bytes. S294 states that a
`text`/`eol`/filter attribute may convert a file on checkout/checkin, so the
two can legitimately differ with no edit. The binding is therefore exact only
where no conversion attribute applies to the manifest path; a repository that
sets one needs either a path outside the conversion set or a comparison on the
object bytes alone. The lane's manifest carries no conversion attribute.

## Measured evidence

| Reading | Population | Result |
|---|---|---|
| base instrument, base tree, narrowed manifest | 5 rows | `rows=5 closed=5 open=0 unexpected=0`, exit 0 — the narrowing is invisible |
| base instrument, directory row | 1 row | `state=closed detail=paths-present`, exit 0 — a tree stands in for a file |
| declared instrument, full register, `--manifest-rev` | 6 rows | `rows=6 closed=6 open=0 unexpected=0 manifest=bound`, exit 0 |
| declared instrument, narrowed manifest, `--manifest-rev` | 5 rows | `manifest-rev-mismatch`, exit 2, no row effect |
| declared instrument, directory row | 1 row | `state=open detail=not-regular-file:…=040000`, exit 1 |

The do-nothing control is the first row: the cheapest change that skips the
claimed work (delete a row) still certifies under the base instrument, which is
why the target is the *bound* line on the full population, not "the counter
runs".
