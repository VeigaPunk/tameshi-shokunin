# Reopen S059 — Bazel Remote Caching (round 17, wave 2)

Target: re-open source row S059 of `corpus/SOURCES.md` at
`eb7838b16490ca7ba17ea3242ade76a61f744af2` live, and check the quote, the
tier/scope/teaches cells, and the used-by citation.

Method: lane cloned at the landing rev in a fleet-mirror scratch tree
(`/tmp/tameshi-r17w2-ReopenS059-Scout/w/fleet`, `git rev-parse HEAD` prints the
rev, `git status --porcelain` prints 0 lines), live HTTP fetches compared
against the row's claimed SHA-256, and the frozen fleet contract
(`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`,
sha256 `6c674a2281afb75b2de11790ebfe34fdcf7ddde61a6734d2eca302f023966119`)
used for the tier, anchor and census rules.

## Commands and results

Live fetch, 2026-10-20 16:05 UTC (`date -u`):

```
curl -sSL -w '%{http_code} %{content_type} %{size_download}' https://bazel.build/remote/caching
  -> 200 text/html; charset=utf-8 293138          (exit 0)
curl -sSL -o v.md https://bazel.build/remote/caching.md
  -> 200 text/markdown; charset=utf-8 16722       (exit 0)
sha256sum v.md
  -> 0d362d113cdb9c434779bc7601f79844db12339da0207fa2a1b31d5b08badac5
```

The same URL fetched three times returned the same byte count and the same
SHA-256. The row's anchor claims exactly
`0d362d113cdb9c434779bc7601f79844db12339da0207fa2a1b31d5b08badac5` for the
markdown alternate — match.

The HTML declares the markdown alternate itself:
`<link rel="alternate" type="text/markdown" href="/remote/caching.md">`, so the
hashed document is the page's own alternate, not a hand-picked mirror.

## Quote check

Stated location: §Known issues, "Bazel does not track tools outside a
workspace" (`corpus/lessons/round-17.md:33`, `corpus/SOURCES.md:68`).

Live markdown (`v.md`):

```
353: <h2 id="known-issues">
354:   Known issues
377: **Bazel does not track tools outside a workspace**
379: Bazel currently does not track tools outside a workspace. This can be a
380: problem if, for example, an action uses a compiler from `/usr/bin/`. Then,
381: two users with different compilers installed will wrongly share cache hits
382: because the outputs are different but they have the same action hash. See
383: [issue #4558](https://github.com/bazelbuild/bazel/issues/4558) for updates.
```

- The lesson quote is `Then, two users ... same action hash.` — it begins at the
  end of md:380 and continues on md:381-382. After a line-wrap join
  (whitespace-normalised containment) it is **verbatim** in the named
  subsection: check prints `VERBATIM_AFTER_WRAP_JOIN: True`.
- Word count is **24** (`len(q.split())`), within the contract's ≤25-word rule 1.
- Subsection bounds are md:377-383 (next bold subhead "Incremental in-memory
  state..." begins md:384-385); §Known issues is the h2 at md:353-355.
- Rendered HTML confirms the same location: after tag-stripping,
  `h2#known-issues` (idx 2590) precedes the subhead (14787) and the quote
  (15030); the quote appears twice in the served HTML (rendered body + the
  inline JSX data payload, where it is split by `\n`).

## Cell support

Row at `corpus/SOURCES.md:68`, 11 data cells (13 fields, matching the
contract's NF=13 shape).

- **tier `A`** — supported. The served page is Bazel's own documentation
  (`<title>Remote Caching - Bazel Documentation</title>`,
  `"siteName":"Bazel Documentation"`); contract v1 defines A as "primary or
  authoritative for that scope (spec, official docs, ...)".
- **kind `docs`** — supported; a documentation page, not a paper/code source.
- **scope** — supported. "action-cache reuse keyed by action hash" is md:36:
  "The action cache, which is a map of action hashes to action result
  metadata." The "documented false-hit class for inputs outside the key" is
  md:377-383 (compiler under `/usr/bin/` not tracked -> same action hash,
  different outputs).
- **teaches** — supported. "a cache hit is reuse keyed to the recorded inputs"
  rests on md:20-22 (each action has declared inputs, outputs, command line,
  environment variables), md:36, and the env-var sub-section md:363-372.
  "an input outside the key keeps the same hash while the outcome changes" is
  literally md:379-382 ("same action hash", "outputs are different").
  "credit is sound only for what the key records" is the lane's lesson
  statement, grounded in the above; it is not presented as a page quote.
- **status `mined`, opened `2026-10-20`, recheck `90d`** — consistent: status
  `mined` requires a citing used-by path (present), opened matches the lesson
  access date, and `90d` is an allowed cadence in the contract.

## Used-by

`corpus/knowledge/input-keyed-coldread-credit.md`:

```
git cat-file -e eb7838b16490ca7ba17ea3242ade76a61f744af2:corpus/knowledge/input-keyed-coldread-credit.md
  -> exit 0 (exists at the landing rev)
sha256sum (rev blob and worktree) -> 1fad5a57c56ea059ebfecedf37edb8256739d94382f89cf302d49d319ab9e57c (both)
```

It cites S059 on four lines:

- `:1` — `source:` line with the same URL and §Known issues anchor, fetched
  2026-10-20;
- `:3` — the recheck line: "re-open S059 and S064 (the tighter cadence)";
- `:30` — "A cache hit is sound only for what its key records (S059, S064).";
- `:66` — "the same false-hit class S059 documents for compilers outside a
  Bazel workspace."

## Registry context

Contract census run from the lane root (clone at the rev):

```
rows                     62
malformed                 0          (awk NF!=13 -> 0)
tiers                     A=54 B=6 C=2
statuses                  mined=35 queued=24 rejected=3
duplicate ids             (none)
enum violations           (none)
mined rows, missing used-by paths   (none)
```

The lesson's rule-1 Gate row is present under `## Gate` at
`corpus/lessons/round-17.md:14`; the S059 line is `:33` with URL,
Accessed 2026-10-20 and the located 24-word quote. The lesson's own
registry note (`corpus/lessons/round-17.md:40-44`) states which rows take the
lesson itself as used-by (S061-S063) versus the knowledge entry (S058, S059,
S060, S064), so the single knowledge path in S059's used-by is the documented
convention, not an omission by accident.

## Observations (non-blocking)

1. "version unstated" is literally true — the page body carries no doc version
   label. The served HTML's embedded nav nevertheless maps the canonical
   `/remote/caching` under the `HEAD` channel
   (`"firstHrefInVersion":{"HEAD":{"href":"/remote/caching",...`). The anchor is
   still pinned by the fetched date plus the byte SHA-256, which is a stronger
   revision identifier than a version label; no action needed.
2. S059's `## Gate` table quote and the used-by note are consistent with each
   other; the target check ("the used-by file exists ... and actually cites
   S059") passes on the named file alone.
3. The lane preamble (`corpus/SOURCES.md:3`) names `SOURCES-CONTRACT-v1.md`
   without a path; that file does not exist inside the lane at this rev — the
   frozen contract lives at the fleet path
   `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`.
   Pre-existing and registry-wide, outside S059's row.
4. A wave-1 proposal in `.ufo/waves/round-17/w1/S18SrcGitToplevel.md:52` used
   the label "S059 (L1 assigns)" for a different (git) source; the registry
   assigned S059 to Bazel and the git row to S063. No duplicate ID exists in
   `corpus/SOURCES.md` (duplicate check empty), so this is a stale proposal
   label, not a registry defect.

**Verdict: S059 holds** — the quote is verbatim (24 words) at
`v.md:380-381` inside §Known issues under the named subhead; the live
markdown alternate's SHA-256 equals the row's claim on three fetches; tier A,
scope and teaches are each supported by the page text; and the used-by file
exists at `eb7838b16490ca7ba17ea3242ade76a61f744af2` and cites S059 on four
lines (`:1`, `:3`, `:30`, `:66`).
