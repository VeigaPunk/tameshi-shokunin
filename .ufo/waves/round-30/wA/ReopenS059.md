# ReopenS059 — freshness of the S059 anchor

Seat: TameshiR30A2.ReopenS059-11. Axis: freshness. No tools installed. No lane file except this report was written. No gate was run.

## Verdict

The live markdown at `https://bazel.build/remote/caching.md` is stable across two fetches 54 seconds apart, matches the on-disk snapshot byte for byte, and does not match the digest pinned by row S059 at `f09d3425258403a51422c9959e25340807982947`. The known-issue sentence is still on the page. The contract correction is a new row, not an in-place edit of S059's anchor. Id S092 is free in that commit. Draft below. Do not append a second S092: the working tree already has an uncommitted one.

## Evidence

### Two live fetches

Command (first): `curl -sSL --max-time 60 -o /tmp/reopen-s059/fetch1.md -w "http_code=%{http_code} size=%{size_download}" https://bazel.build/remote/caching.md && sha256sum /tmp/reopen-s059/fetch1.md && date -u`

Observed at `2026-10-23T05:50:48Z`: `http_code=200 size=16210`, sha256 `266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b16d67768a5b`.

Command (second, after `sleep 32`): same curl to `/tmp/reopen-s059/fetch2.md`.

Observed at `2026-10-23T05:51:42Z`: `http_code=200 size=16210`, same sha256. `cmp -s fetch1.md fetch2.md` exit 0.

One extra header probe, not a third body: `curl -sSI` at `2026-10-23T05:52:41Z` returned `HTTP/2 200`, `content-type: text/markdown; charset=utf-8`, and `last-modified` equal to `date` (both `Fri, 23 Oct 2026 05:52:41 GMT`). That equality is the same dynamic-generation artifact recorded in `.ufo/waves/round-17/w1/S15SrcBazelCache.md` lines 22–26. It is not a publication date. The anchor pins the access times and the body digest.

Page version is still unstated. Line 30, "Use Bazel version 0.10.0 or later", is an implementation floor. Line 405 says the docs are hosted on Mintlify.

### Snapshot

`sha256sum` of `.ufo/evidence/round-30/sources/S059-bazel-remote-caching.md` is the same `266915c5…a5b`. `cmp -s` against fetch1 exit 0. Both are 16210 bytes; `wc -l` is 404 because the last byte is `0x2e` (no trailing newline). Split into lines, the file has 405 lines.

`git cat-file -e f09d3425258403a51422c9959e25340807982947:.ufo/evidence/round-30/sources/S059-bazel-remote-caching.md` failed: the path exists on disk but not in that commit. `git status --porcelain` shows the snapshot untracked (`??`) and `corpus/SOURCES.md` modified (`M`). HEAD is that commit.

### Row S059 at the commit

`git show f09d3425258403a51422c9959e25340807982947:corpus/SOURCES.md`, the S059 line (field count 13, which is 11 cells):

| S059 | Remote Caching (Bazel docs) — https://bazel.build/remote/caching | docs | A | Bazel's action-cache reuse keyed by action hash, and its documented false-hit class for inputs outside the key | §Known issues, "Bazel does not track tools outside a workspace" @ page fetched 2026-10-20, version unstated, markdown alternate sha256 0d362d113cdb9c434779bc7601f79844db12339da0207fa2a1b31d5b08badac5 | a cache hit is reuse keyed to the recorded inputs; an input outside the key keeps the same hash while the outcome changes, so credit is sound only for what the key records | mined | 2026-10-20 | 90d | corpus/knowledge/input-keyed-coldread-credit.md, corpus/lessons/round-28.md |

The pinned digest `0d362d11…badac5` is not the live digest. This reopen did not re-hash the 2026-10-20 bytes. The old digest is the row's recorded pin. Round 17 recorded it for a 16722-byte fetch (`S15SrcBazelCache.md` lines 18–19).

Committed id pointer, same file, the last such line: `- Next unused id: S092.` Count of committed `S092` rows: 0.

### Quote

Exact string "Bazel does not track tools outside a workspace" (8 words): line 343, the bold heading under `## Known issues` (that heading is line 321).

Prose, line 345 (9 words): "Bazel currently does not track tools outside a workspace."

The shorter pattern `does not track tools outside a workspace` occurs twice (`grep -c` → 2), lines 343 and 345. Lines 347–348 still contain, after whitespace reflow, the 24-word sentence pinned in `corpus/lessons/round-17.md`: "Then, two users with different compilers installed will wrongly share cache hits because the outputs are different but they have the same action hash." Round 17 located that sentence at markdown lines 380–382 (`S15SrcBazelCache.md` lines 30–34). The sentence moved; it was not rewritten. S059's teaches is not contradicted by these bytes.

## Contract shape

`/home/vgpnk/Projects/shokunin/CORPUS.md`, section "SOURCES.md — where a shokunin learns" (contract v1, lines 76–118).

Column order, one header, eleven cells, no `|` inside a cell:

`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`

A correction is a new row. Only `status`, `recheck`, and `used-by` may change in place. S059's digest sits in `anchor`, so it cannot be edited in place. The new row's `teaches` must open `supersedes S0NN —` (line 118). Here that opening is `supersedes S059 —`.

`queued` means opened and worth mining. `mined` means cited by at least one path in `used-by` (lines 103–108). Nothing in the commit cites S092. `corpus/knowledge/input-keyed-coldread-credit.md` line 1 still cites S059. This draft is therefore `queued`, with `used-by` `—`.

Census source (`scripts/sources-census.sh` lines 643–649), not a run: the same URL inside one scope is E04 unless `teaches` matches `supersedes S[0-9]{3}`. The same URL under a different scope string is W04, and W04 does not fail validation. This draft keeps S059's canonical URL and a different scope, and the teaches opening matches that pattern. [INFERENCE] a later census prints W04 and does not print E04. Not run here.

## Draft row for S092

Not written to `corpus/SOURCES.md`. Checked in `/tmp`: 11 cells, `NF=13`, teaches opens `supersedes S059 —`, no `|` inside a cell.

```
| S092 | Remote Caching (Bazel docs) — https://bazel.build/remote/caching | docs | A | supersedes S059's anchor only: the markdown digest of the known-issues false-hit | §Known issues, heading "Bazel does not track tools outside a workspace" at markdown line 343, prose at line 345 @ https://bazel.build/remote/caching.md fetched 2026-10-23T05:50:48Z and 2026-10-23T05:51:42Z, both sha256 266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b16d67768a5b, 16210 bytes, version unstated | supersedes S059 — the pinned markdown digest 0d362d113cdb9c434779bc7601f79844db12339da0207fa2a1b31d5b08badac5 does not match the live page; the known-issue sentence is unchanged, so S059's teaches stands | queued | 2026-10-23 | 90d | — |
```

On landing, if a lesson cites the row, change `queued` → `mined` and `used-by` → that path, and log the change in the lesson. Append `- Next unused id: S093.` Do not edit the older next-id lines.

## Working tree already holds an S092

`corpus/SOURCES.md` line 101 (uncommitted; absent from `f09d342`) is already an S092 whose digest is this same `266915c5…a5b`, stamped `2026-10-23T05:03Z`, status `mined`, used-by `corpus/knowledge/input-keyed-coldread-credit.md, corpus/lessons/round-29.md`. Its source URL is the `.md` alternate, not the canonical URL. Those two used-by files, as read, cite S059; round 29 defers the supersedes row (`corpus/lessons/round-29.md` lines 28–31 and 124; spot-check routed item 7, `corpus/lessons/round-29-verifier-spotcheck.md` line 218). A `mined` cell is not grounded until a path cites S092. The working-tree footer also already says `- Next unused id: S093.` (line 361). Append nothing further until that row is reconciled with this draft.

## Unknowns

- HTML at `https://bazel.build/remote/caching` was not fetched this pass. Round 29's claim that those bytes are deploy-keyed is prior record, not a measurement here.
- The 2026-10-20 markdown bytes were not recovered. Only the recorded digest `0d362d11…badac5` was compared, and it differs.
- Census was not executed.
