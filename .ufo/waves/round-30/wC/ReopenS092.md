# ReopenS092 — freshness of the S092 anchor

Seat: ReopenS092. Axes: live digest, cited-line presence, SOURCES contract shape. No tools installed. No lane file except this report was written. No gate was run.

## Verdict

Agree. At `bb681566b18211adf8ae9c28df91e17678e3f545`, row S092's pinned markdown digest is the live page, the quoted known-issue wording is on the cited lines, and the row is the contract's append-only correction of S059. No change to the row.

## Evidence

### Live markdown

Command (first), 2026-10-23T07:14:23Z:

`curl -sSL -D /tmp/reopen-s092/headers.txt -o /tmp/reopen-s092/caching.md https://bazel.build/remote/caching.md && sha256sum /tmp/reopen-s092/caching.md && wc -c /tmp/reopen-s092/caching.md`

Observed: `HTTP/2 200`, `content-type: text/markdown; charset=utf-8`, sha256 `266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b16d67768a5b`, 16210 bytes. `wc -l` is 404 because the file has no trailing newline; `splitlines` is 405. `last-modified` equals the response `date` (both `Fri, 23 Oct 2026 07:14:23 GMT`). That equality is the same dynamic-generation artifact already recorded for this URL. It is not a publication date. Page version is still unstated. Line 30, "Use Bazel version 0.10.0 or later", is an implementation floor.

Command (second), 2026-10-23T07:15:44Z, after `sleep 35`:

`curl -sSL --max-time 60 -D /tmp/reopen-s092/headers2.txt -o /tmp/reopen-s092/caching2.md https://bazel.build/remote/caching.md && sha256sum /tmp/reopen-s092/caching2.md && cmp -s /tmp/reopen-s092/caching.md /tmp/reopen-s092/caching2.md`

Observed: `HTTP/2 200`, same sha256, 16210 bytes, `cmp` exit 0.

That digest is the one in S092's anchor (`corpus/SOURCES.md` at `bb681566`, the S092 line). It is not S059's pinned digest `0d362d113cdb9c434779bc7601f79844db12339da0207fa2a1b31d5b08badac5`. The 2026-10-20 body was not recovered. Round 17 recorded that older digest at 16722 bytes (`.ufo/waves/round-17/w1/S15SrcBazelCache.md:18-19`). The committed snapshot `bb681566:.ufo/evidence/round-30/sources/S059-bazel-remote-caching.md` hashes to the same `266915c5…a5b` as both live fetches.

The access times `2026-10-23T05:50:48Z` and `05:51:42Z` in the anchor are the earlier seat's record (`.ufo/waves/round-30/wA/ReopenS059.md:15-19`), not re-clocked here. The digest those fetches named is the digest fetched again above.

### Cited lines

Live file, newline-split:

- Line 321: `## Known issues`
- Line 343: `**Bazel does not track tools outside a workspace**`
- Line 345: `Bazel currently does not track tools outside a workspace. This can be a`

The heading string S092 quotes, "Bazel does not track tools outside a workspace", is wholly on line 343 (8 words). The prose sentence "Bazel currently does not track tools outside a workspace." is wholly on line 345 (9 words). Both match the anchor's "heading … at markdown line 343, prose at line 345".

The 24-word sentence round 17 quoted for S059 is in the same paragraph, not on 343 or 345. Lines 347–348, joined:

`two users with different compilers installed will wrongly share cache hits because the outputs are different but they have the same action hash.`

Full sentence, 24 words: "Then, two users with different compilers installed will wrongly share cache hits because the outputs are different but they have the same action hash." Round 17 located that sentence at markdown lines 380–382 against digest `0d362d11…` (`.ufo/waves/round-17/w2/ReopenS059.md:47-51`; the gate quote is `corpus/lessons/round-17.md:33`). The words match that record. The lines moved. S092 cites the new lines and does not claim the 24-word sentence sits on line 345. "The known-issue sentence is unchanged" holds for this wording. It is a comparison with the recorded quote, not a byte diff of the two markdown files.

### Contract

Section "SOURCES.md — where a shokunin learns", `/home/vgpnk/Projects/shokunin/CORPUS.md:64-118`. Rule 2 (`CORPUS.md:116-118`): append-only; only `status`, `recheck`, and `used-by` change in place; a correction is a new row whose `teaches` opens `supersedes S0NN —`.

S092 at `bb681566` (python `split('|')`, NF=13, 11 cells, no `|` inside a cell):

| cell | value |
|---|---|
| id | S092 |
| source | Remote Caching (Bazel docs) — https://bazel.build/remote/caching |
| kind | docs |
| tier | A |
| scope | supersedes S059's anchor only: the markdown digest of the known-issues false-hit |
| teaches | opens `supersedes S059 —` (the dash is U+2014) |
| status | queued |
| opened | 2026-10-23 |
| recheck | 90d |
| used-by | — |

Parent `713dee6a0cae8979cf8df58944e5c82825414674` has no `| S092 |` row (`git grep -F`). The S059 row is byte-identical in parent and `bb681566`. `git diff --numstat` of `corpus/SOURCES.md` is 13 insertions and 1 deletion. The deletion is S087's `used-by` only (`corpus/knowledge/mte-report-interop.md` → that path plus `corpus/knowledge/regression-tally-completeness.md`); every other S087 cell is unchanged. The search log at `corpus/SOURCES.md` records that old→new pair. S059 was not rewritten. S092 is a new row.

`queued` means opened and worth mining. `mined` means cited by at least one path in `used-by`. `used-by` lists knowledge entries or lessons (`CORPUS.md:103-108`). At `bb681566`, `git grep -F S092 -- corpus/knowledge` prints nothing. Lesson hits are earlier notes that S092 was the next id or that a draft row was removed (`corpus/lessons/round-27-verifier-spotcheck.md:194`, `corpus/lessons/round-28.md:47-50`). They do not cite this row. `corpus/README.md:454` indexes the correction; the index is not a knowledge entry or a lesson, so it is not a `used-by` path. No `corpus/lessons/round-30.md` exists at this commit. `queued` with `used-by` `—` matches that.

Same canonical URL as S059 is what a supersedes row is for. The contract forbids editing S059's anchor in place. It does not forbid a second row whose `teaches` opens `supersedes S059 —`.

## Smallest safe correction

None. Do not edit S059. Do not flip S092 to `mined` until a knowledge entry or a lesson cites it, and log that old→new pair when it happens.

## Unknowns

- The 2026-10-20 markdown bytes were not recovered, so "unchanged" is against the recorded sentence, not a diff of the two files.
- HTML at `https://bazel.build/remote/caching` was not fetched this pass.
- Census was not run.
