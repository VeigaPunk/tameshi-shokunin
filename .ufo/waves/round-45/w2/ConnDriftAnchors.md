seat: ConnDriftAnchors

# Anchor-digest drift cross-map (C1 ledger × registry anchors)

Scope: cross the committed C1 ledger `.ufo/evidence/round-45/freshness/ledger.json` at
`ad5942c6e9858af19d00000b58439b321ddfa62b` with the registry anchors (`corpus/SOURCES.md` at the
same rev) for every held row whose anchor/source cell pins a digest (sha256 full/prefix, `currentOid`,
commit hash, revid, version, or a committed snapshot path), classify each against today's
`raw_sha256` / fetched content, and output anchor-refresh candidates for a later round.

Method (read-only): all inputs read via `git -C <lane> show ad5942c6:<path>` (no writes to the lane,
no jj/git mutation, no counter run). Snapshot bytes = committed `S###.raw.gz` decompressed at the same
rev; each was re-hashed and matched `raw_sha256` (73/73). Quote-holds evidence was re-derived with the
counter's `measure.grade()` logic on those committed snapshots (73/73 graded `verified`: quote located
afresh, ≥2 shared content words, not copied from row cells) — this is analysis, not a measurement run.

## Summary

| category | rows |
|---|---|
| same bytes (pin == today raw) | 18 |
| bytes drifted, quote holds → **anchor-refresh candidate** | 6 (S089 already refreshed via S160; S100, S153, S154, S157, S159 open) |
| pinned to an immutable ref | 4 (S086, S087, S104; S158 immutable URL + anchor-snapshot drift) |
| different-object pin (not byte-comparable with the URL fetch) | 3 (S059, S064, S093) |
| `currentOid` pin, no byte baseline | 1 (S006) |
| no digest pin in anchor/source | 41 |

## Anchor-refresh candidates (table)

Per `corpus/knowledge/r44-anchor-refresh-rule.md`: a stale anchor digest is repaired by a **new
supersede row** in a later round (never by in-place anchor edit). Each candidate below has a pinned
digest/snapshot ≠ today's raw, with the C1 quote still verified afresh in the today snapshot.

| row | pinned digest / committed snapshot (rev ad5942c6) | today raw_sha256 prefix | quote holds | evidence / note |
|---|---|---|---|---|
| S153 | `.ufo/evidence/round-41/sources/ast.html` → `183a4f8c3d593be4…` | `f4c18b31aea74525…` | yes (grade verified) | Python 3.15.1 ast docs; anchor pins round-41 snapshot digest; quote `Get source code segment of the source that generated node` found afresh today. |
| S154 | `.ufo/evidence/round-41/sources/pathlib.html` → `0044cae699c55963…` | `7ae9b7205cf1a793…` | yes (grade verified) | pathlib 3.15.1 docs; quote `Open the file pointed to in text mode, write data to it, and close the file` found afresh today. |
| S157 | `.ufo/evidence/round-42/sources/python-argparse.html` → `3158c439e504752c…` | `421e389138e80a47…` | yes (grade verified) | ledger note: `page hash changed since round-42`; quote `For optional argument actions, the value of dest is normally inferred from the option strings` found afresh today. |
| S159 | `.ufo/evidence/round-43/sources/wikipedia-mutation-testing.html` → `6e4a06c0863ca2b0…` + pinned revid `1373580212` | `616dd5a510906c44…` | yes (grade verified) | ledger note: `page revid changed since round-43`; quote `Equivalent mutants detection is one of the biggest obstacles…` found afresh today. |
| S100 | committed snapshot `2026-10-23` → `.ufo/evidence/round-33/c2/doctest-snapshot.html` `217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899` | `6f6c1467595ab400…` | yes (grade verified) | pins the 3.15 build by committed bytes; today's /3.15 fetch differs from the round-33 committed snapshot; quote `doctest module searches for pieces of text that look like interactive Python sessions…` found afresh today. Same page bytes also served to S055 (`/3/` alias). |
| S089 | html sha256 `bc572676…e04d` (2026-10-22) | `79f6501ad8f2a74e…` | yes (grade verified) | **already refreshed**: S160 is the round-44 supersede row (`supersedes S089 — … this row pins the re-opened snapshot`, sha256 `79f6501a`), now grade-verified today. No further action. |

Later-round action for the five open candidates: open one supersede row per drifted document (S153,
S154, S157, S159, S100) pinning the round-45 snapshot digest, per r44 rule; keep the old row as
history. (S089/S160 already demonstrate the pattern.)

## Same bytes (pin matches today raw) — 18 rows

S056 (`a31331da…`), S058 (`d6c175a4…` full), S094 (`6e9532a9…` full, arXiv v3 PDF),
S095 (`1a40ae77…` full), S096 (`95572c73…` full), S097 (`f3d37d57…` full; cgit commit URL),
S099 (`b0c7e050…` full), S101 (`0fde8a7b…` full + committed snapshot match), S102 (`0889867a…` full +
committed snapshot match), S103 (`dd826daee…` full + committed snapshot match), S105 (`dda9f57d…`),
S106 (`4b2c2ad0…`), S107 (`eb9dcedc…`; raw TFF commit URL), S132 (`8871d19c…`), S152 (`65f9603f…`),
S155 (`c51d8423…` + committed snapshot match), S156 (`ccf6ac49…` + committed snapshot match),
S160 (`79f6501a…` + committed snapshot match). All keep their anchor digests valid this round.

## Pinned to an immutable ref — 4 rows

| row | pin | status |
|---|---|---|
| S086 | npm `mutation-testing-report-schema@3.9.0` tarball; sha512 integrity `28CobrcLdQm35zySemaLMKrU…`; gitHead `00aa7bdc…` | tarball sha512 recomputed from today's snapshot and **matches** the pinned integrity; gitHead matches. Version-frozen artifact. |
| S087 | npm `mutation-testing-metrics@3.9.0` tarball; sha512 integrity `E2i+8bXoEST8KIyJymc+OjO3…`; gitHead `00aa7bdc…` | tarball sha512 recomputed and **matches**; gitHead matches. Version-frozen artifact. |
| S104 | cgit Bash 5.3 `?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303` (immutable commit) | URL cannot move; today's bytes equal S097's pinned full sha `f3d37d57…`. No refresh possible/needed. |
| S158 | GitHub blob URL at commit `f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6` | **anomaly**: the URL is frozen at a commit, yet the anchor's round-42 committed snapshot `3bf295ad53126560…` ≠ today raw `51deedf9340ac8d9…`. Quote still verified afresh today. Not a refresh candidate (the ref is immutable; mismatch indicates fetch variance/rendering drift, not document drift) — worth a note, not a supersede row. |

## Different-object pins (pinned digest is a different artifact than the URL fetch) — 3 rows

| row | pinned object vs fetched URL | note |
|---|---|---|
| S059 | anchor pins markdown alternate sha256 `0d362d113cdb9c43…`; fetched URL is the rendered HTML page (`c9653cfb…`) | not byte-comparable; S092 (queued) already records the markdown-digest mismatch and supersedes S059's anchor. |
| S064 | anchor pins markdown alternate sha256 `76167a0dacc146cf…`; fetched URL is the HTML page (`70e9d811…`) | not byte-comparable; no drift conclusion from bytes. |
| S093 | anchor pins `bwrap.xml` sha256 `2cb77df2f4be0b2a…` (33289 B, re-fetched by L1 with same digest); fetched URL is the GitHub blob **HTML** page (`f8a95822…`) | tag v0.13.1 / commit `362936ae…` URL; xml pin is for a different object than the HTML fetch — no byte drift conclusion. |

## `currentOid` pin — S006

Anchor pins page `currentOid 7eefc73010ad6342b80e3ed43915503e02c90618` (2026-10-19); today's fetched
HTML (`a61a08aa…`) does not contain that oid string and is not byte-comparable to a repo oid. Row
grades verified today (quote holds). This is a version-era marker, not a byte digest; recommend a later
round re-resolve the live oid if the row is re-opened.

## No digest pin in anchor/source — 41 rows (out of cross-map scope)

S001 S002 S003 S004 S005 S008 S011 S012 S024 S026 S028 S041 S047 S048 S049 S052 S054 S055 S057 S060
S061 S062 S063 S065 S066 S068 S069 S070 S072 S073 S074 S075 S076 S077 S078 S079 S081 S084 S090 S091
S108. (Version-only mentions — e.g. S055 Python 3.15.0→3.15.1 note, S061/S076 jj v0.46.0, S068/S069/
S072/S077/S078 man-pages 6.19, S090 FreeBSD 15.1, S091 Git 2.56.0 — carry no hash to compare; S055's
version move is already recorded in the ledger note.)

## Tooling

No tools installed or updated (no pacman, no uv/npx/binary installs). Analysis used only existing
`git` (read-only `show`/`ls-tree`), `jj log` (read-only), Python 3 stdlib, and the counter module's
grade logic read via importlib.
