# Reopen S064 — Hermeticity (Bazel docs)

Seat: `ReopenS064-2` (wave 2, falsify). Target: re-open row S064 of
`corpus/SOURCES.md` at `eb7838b16490ca7ba17ea3242ade76a61f744af2` against the
live page, and check the quote, the cell support, and the used-by citation.

Clone used for every lane read (fleet-mirror layout, detached at the landing
rev, worktree clean `git status --porcelain` → 0 lines):

```
/tmp/tameshi-r17w2-ReopenS064-cIE07A/fleet/tameshi-shokunin  @ eb7838b16490ca7ba17ea3242ade76a61f744af2
```

No tool installed or upgraded (nothing needed).

## Row under test

`corpus/SOURCES.md:73` (blob at rev, sha256 `ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5`):

| field | value |
|---|---|
| source | Hermeticity (Bazel docs) — https://bazel.build/basics/hermeticity |
| kind / tier | `docs` / `A` |
| scope | Bazel's own definition of hermetic builds and its catalogue of non-hermetic input sources |
| anchor | §Benefits and §Identifying non-hermeticity @ page fetched 2026-10-20, markdown alternate sha256 `76167a0d…b0b73da` |
| teaches | a cached result holds only while its inputs are unchanged; host binaries, absolute paths and source-tree writes are named inputs outside the key, so a cached credit must pin or disclose them |
| status / opened / recheck | `mined` / 2026-10-20 / 180d |
| used-by | `corpus/knowledge/input-keyed-coldread-credit.md` |

Lesson quote under test, `corpus/lessons/round-17.md:38`:

> "The output of an action can be cached, and the action need not be run again unless inputs change." (§Benefits)

## Commands, exits, key output

| # | command | exit | key output |
|---|---|---|---|
| 1 | `curl -sS -L https://bazel.build/basics/hermeticity.md -o /tmp/bazel-hermeticity.md -w '%{http_code}'` | 0 | `200`; `sha256sum` = `76167a0dacc146cfbc13b54a0d6db03a283d413c75f50a32666611f90b0b73da` — byte-identical to the row's stated markdown-alternate sha |
| 2 | refetch same URL with `-H 'Cache-Control: no-cache'` | 0 | `200`; sha256 again `76167a0d…b0b73da` (stable; `cf-cache-status: EXPIRED`, `last-modified: Tue, 20 Oct 2026 16:04:32 GMT`) |
| 3 | `curl -sS -L https://bazel.build/basics/hermeticity` (HTML page of the row URL) | 0 | `200`, 135609 bytes; payload contains `The output of an action can be cached, and the action need not be\nrun again unless inputs change.`; `id="benefits"` ×1, `id="nonhermeticity"` ×1 |
| 4 | python join-check over the markdown: join the Speed bullet to one line, compare to the lesson quote | 0 | `verbatim: True`, `words: 19`, `quote inside benefits section: True`; heading lines: benefits 35, non-hermeticity 52, quote 41 |
| 5 | `printf '%s\n' '<quote>' \| wc -w` | 0 | `19` (≤25) |
| 6 | `git show <rev>:corpus/lessons/round-17.md \| sed -n '38p'` | 0 | quote cell matches the markdown sentence exactly, location `(§Benefits)` |
| 7 | `git show <rev>:corpus/SOURCES.md \| grep -n '| S064 '` | 0 | `73:` the row above |
| 8 | contract census from `SOURCES-CONTRACT-v1.md` (rows / malformed / dups / enum / mined-used-by-exists) | 0 | `rows: 62`, `malformed: 0`, `dups:` empty, `enum:` empty, `missing used-by:` empty |
| 9 | `git cat-file -e <rev>:corpus/knowledge/input-keyed-coldread-credit.md`; `git show <rev>:… \| grep -n S064` | 0 | file exists; S064 cited 3× — line 1 (`source:` header naming §Benefits and §Identifying non-hermeticity), line 3 (`recheck:` cadence names S064), line 30 `cache hit is sound only for what its key records (S059, S064)` (load-bearing use) |
| 10 | `git show 98bea7da5801f4bc58e4187690ee1687c8a5061f:corpus/SOURCES.md \| grep -c S064` | 1 | `0` — S064 is a new round-17 row, not an in-place edit |
| 11 | `git show <rev>:corpus/lessons/round-17.md \| sed -n '40,42p'` | 0 | `Registry changes: rows S058–S064 added, status mined (used-by knowledge/input-keyed-coldread-credit.md for S058, S059, S060, S064; this lesson for S061, S062, S063); no existing row's status, recheck or used-by …` — matches the row |
| 12 | `date -I` | 0 | `2026-10-20` — the row's `opened`/access date is today |

Quote is 19 words; joins are whitespace only (`cached,` + `run again`). The
trailing period is the page's.

## Cell support

- **kind `docs` / tier `A`** — supported. Contract (`SOURCES-CONTRACT-v1.md`,
  frozen, external copy sha256 `6c674a2281afb75b2de11790ebfe34fdcf7ddde61a6734d2eca302f023966119`):
  tier A = "primary or authoritative for that scope (spec, official docs, …)".
  The row is Bazel's own documentation of Bazel's own definition; `docs` is an
  allowed kind and `A`+`docs` is not the forbidden `community` inflation.
- **scope** — supported verbatim by the page intro: "This page covers
  hermeticity, the benefits of using hermetic builds, and strategies for
  identifying non-hermetic behavior in your builds." and the list introducer
  "Some common sources of non-hermeticity in builds are:" (markdown lines 7-8,
  57-58).
- **anchor** — supported. Both named sections exist as `<h2 id="benefits">`
  (line 35) and `<h2 id="nonhermeticity">` (line 52) in the markdown, and as
  `id="benefits"` / `id="nonhermeticity"` in the HTML. The anchor's sha256 is
  the live markdown alternate, re-fetched byte-identical twice.
- **teaches, first clause** ("a cached result holds only while its inputs are
  unchanged") — supported directly by the §Benefits Speed bullet, markdown
  lines 41-42 (the quoted sentence).
- **teaches, second clause** ("host binaries, absolute paths and source-tree
  writes are named inputs") — supported by §Identifying non-hermeticity,
  markdown lines 63-67: "System binaries that differ across hosts (such as
  `/usr/bin` binaries, absolute paths, system C++ compilers for native C++
  rules autoconfiguration)" and "Writing to the source tree during the build."
- **status `mined`** — supported: the used-by path exists as a regular blob at
  the rev and cites the row in a claim-bearing sentence (`…credit.md:30`), which
  is the contract's definition of `mined`.
- **used-by** — `corpus/knowledge/input-keyed-coldread-credit.md` exists at
  `eb7838b…` (README:246 also lists S064 among that entry's sources) and
  cites S064 three times; the citation at `…credit.md:30` is not decorative —
  it supports the entry's core rule ("a cache hit is sound only for what its
  key records").

## Gaps (non-blocking)

1. **gap-minor — quote grounds only half the teaches cell.** Contract rule 1
   asks for a ≤25-word quote "grounding `teaches`", and the teaches cell has
   two conjuncts. The 19-word quote grounds the caching clause; the
   host-binaries/absolute-paths/source-tree-writes clause is true on the page
   (lines 63-67) but is not carried by the lesson quote. The anchor does name
   §Identifying non-hermeticity, so a reader reaches it; nothing is false.
2. **gap-minor — "outside the key" is the lane's gloss.** The page never uses
   "key" in §Identifying non-hermeticity; the keying idea comes from the
   §Benefits Parallel-execution bullet ("hash inputs to look up in the cache").
   The cell states it as page content without an inference label. Same style as
   S059's transfer; supported by the page but [INFERENCE] in wording.
3. **gap-minor (pre-existing, not S064's)** — `corpus/SOURCES.md:4` names
   `SOURCES-CONTRACT-v1.md`; that file is absent from the lane repo at every
   tested rev (`98bea7d`, `eb7838b`, tip), and the frozen contract lives at
   `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`
   (already recorded by round 12 `RegistryReview` R6). Tier verification above
   used the external copy.

Note, not a gap [INFERENCE]: `used-by` lists only the knowledge entry, not
`corpus/lessons/round-17.md`, although the lesson quotes S064 in its rule-1
provenance table. That is the same convention as S058-S060 (lesson quotes them
but only the knowledge entry is in `used-by`); the provenance table is read as
the row's record, not a "use". Under a literal reading of `used-by` ("paths of
the knowledge entries or lessons citing the row") the lesson could be added;
this does not change `mined`.

## Verdict

Holds — the S064 quote is verbatim at §Benefits (markdown lines 41-42, 19
words), tier `A`/`docs` and the scope/teaches cells are supported by the live
page (markdown sha256 `76167a0d…b0b73da`, stable across two fetches), and the
used-by file exists at `eb7838b…` and cites S064 in a claim-bearing line; only
the unquoted second conjunct and the unlabelled "outside the key" gloss are
minor wording gaps.

## Inputs (sha256)

| path / URL | sha256 |
|---|---|
| `corpus/SOURCES.md` @ `eb7838b…` | `ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5` |
| `corpus/knowledge/input-keyed-coldread-credit.md` @ `eb7838b…` | `1fad5a57c56ea059ebfecedf37edb8256739d94382f89cf302d49d319ab9e57c` |
| `corpus/lessons/round-17.md` @ `eb7838b…` | `0047f2492b0e0d273ebb96ee85c7f88ff1fa5a606ad3c6a066df927a16ca0dc5` |
| `https://bazel.build/basics/hermeticity.md` (live, twice) | `76167a0dacc146cfbc13b54a0d6db03a283d413c75f50a32666611f90b0b73da` |
| `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (external) | `6c674a2281afb75b2de11790ebfe34fdcf7ddde61a6734d2eca302f023966119` |
