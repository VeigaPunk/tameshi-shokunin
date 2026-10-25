source: S160 — https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/; snapshot `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html` (38687 B, sha256 `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce`); `/home/vgpnk/Projects/shokunin/CORPUS.md` — SOURCES.md contract v1, rule 2 (append-only supersede rows)
verified-at: 2026-10-25 (round 44 landing)
recheck: 180d

# Anchor-refresh rule — when a registry row's snapshot digest drifts

## The rule

`CORPUS.md`'s SOURCES.md rule 2 makes the registry append-only: only `status`,
`recheck` and `used-by` change in place; a correction is a new row whose
`teaches` opens `supersedes S0NN —`. A stale `anchor` cell (a digest that no
longer matches the live document) is therefore repaired by a **new supersede
row**, never by editing the old row's anchor cell in place. The old row stays
as history; the new row pins the fresh snapshot and names what it supersedes.

## When it fires

- The live document changes bytes but the cited text survives at the same
  offsets (measured by sha256 change with identical located quotes). Example:
  S089 (2026-10-22 anchor digest `bc572676…`) vs the 2026-10-25 re-open
  (`79f6501a…`); the sentences at lines 15–16 are byte-identical.
- The document moves anchor (heading/paragraph/section), so the old `anchor`
  cell's location no longer resolves. The new row records the new location.

## The evidence discipline

- A new supersede row must be opened in the round that writes it: the round
  lesson's `## Gate` records the URL, the access date, and a ≤25-word located
  quote with its line.
- The change is logged old→new in that round's lesson.
- The census must stay exit 0; a duplicate-URL W04 warning (the same document
  held under the superseded row) is a warning, not an E-code.
- The new row is `mined` only when a knowledge entry or lesson cites it
  (`used-by` non-empty); the record-agreement class m7 then reads it as a
  real row.

## Why not edit in place

An in-place anchor edit rewrites history: a reader of the old row cannot tell
which digest was checked when, and a later audit cannot reconstruct the drift.
The supersede row keeps both facts visible (old digest in S089, new digest in
S160) and satisfies the record-agreement citation grammar: S160 is a registry
row; `key=S###` receipt fields are values, not citations.
