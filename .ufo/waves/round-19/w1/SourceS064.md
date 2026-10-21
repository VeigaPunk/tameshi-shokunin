# SourceS064 — re-open of S064 (Bazel "Hermeticity") for round-19 C1

Seat: `TameshiR19-2.SourceS064` (round 19, w1, read-only scout). Date 2026-10-21.
Advisory finding only. No registry or production edit, no install, no git write.

**Verdict.** S064 still holds for its existing scope and used-by. The quoted
sentence and both anchored sections are unchanged on the live page. Do **not**
add it as a source or `used-by` for round-19 C1:

- It addresses none of R18-1 through R18-4.
- For R18-5 it gives only an analogy that the lane already holds through
  `corpus/knowledge/input-keyed-coldread-credit.md:30`.

Separate observation: the row's anchor digest `76167a0d…` no longer reproduces
from the live URL. The live markdown is now `029067f4…`, and only the heading
markup changed. The row is not false, but its byte pin can no longer be
re-verified from the URL.

## Row under test

`corpus/SOURCES.md:73`. The row's bytes are identical at R18 tip `4b7c682`, at
baseline `7243e7f`, at delivered `21e7932` (HEAD) and in the working tree.
Round 19 did not touch S064.

| cell | value |
|---|---|
| source | Hermeticity (Bazel docs) — https://bazel.build/basics/hermeticity |
| kind / tier | `docs` / `A` |
| scope | Bazel's own definition of hermetic builds and its catalogue of non-hermetic input sources |
| anchor | §Benefits and §Identifying non-hermeticity @ page fetched 2026-10-20, markdown alternate sha256 `76167a0dacc146cfbc13b54a0d6db03a283d413c75f50a32666611f90b0b73da` |
| teaches | a cached result holds only while its inputs are unchanged; host binaries, absolute paths and source-tree writes are named inputs outside the key, so a cached credit must pin or disclose them |
| status / opened / recheck | `mined` / 2026-10-20 / `180d` |
| used-by | `corpus/knowledge/input-keyed-coldread-credit.md` (cites S064 at `:1`, `:3`, `:30`; observed 2026-10-21) |

## Commands and observed outcomes

Scratch directory: `/tmp/tameshi-r19w1-SourceS064-myQEMx` (disposable). Fetch
time: `2026-10-21T02:49:37-03:00`; the server `date` header was
`Wed, 21 Oct 2026 05:49:38 GMT`.

| # | command | exit | observed |
|---|---|---|---|
| 1 | `curl -sS -L -D md.hdr -o md.body https://bazel.build/basics/hermeticity.md` | 0 | HTTP 200, 5790 B, `content-type: text/markdown`, sha256 `029067f4986cdcd83415db4aeff551b12546c8cd88d6177d225a9b63eda1ad9a`; `x-version: dpl_CUnGQP1HgFUzoxatVC37y4zP83Vx`; `last-modified` equals the request time, so it is generated per request and cannot pin a revision |
| 2 | two more fetches of the same URL with `-H 'Cache-Control: no-cache'` | 0, 0 | 5790 B each; sha256 `029067f4…` both times (stable today) |
| 3 | `curl -sS -L -D html.hdr -o html.body https://bazel.build/basics/hermeticity` | 0 | HTTP 200, 136367 B, sha256 `679273780a1eba5f34ba374a85e1e78a0a0239307440e248e4632b65e1dea911`; `id="benefits"` ×1 and `id="nonhermeticity"` ×1; the quote sentence is present in the serialized payload |
| 4 | `sha256sum /tmp/bazel-hermeticity.md /tmp/bazel-hermeticity-2.md` (retained 2026-10-20 copies, mtime 13:03/13:04 -0300) | 0 | both `76167a0d…`, 5947 B: the row's recorded digest |
| 5 | `diff /tmp/bazel-hermeticity.md md.body` | 1 | 5 hunks only. Each `<h2 id="X"> Title </h2>` block became `## Title`, for overview, benefits, nonhermeticity, troubleshooting-nonhermeticity and hermeticity-bazel. No prose line changed. |
| 6 | Python check: whitespace-joined quote in body; quote between `## Benefits` and `## Identifying non-hermeticity` | 0 | `quote_verbatim_after_ws_join: True`, `quote_inside_benefits: True`; quote at md lines 37–38; `wc -w` = 19 |
| 7 | `grep -ci` term sweep of `md.body` | 0 | `metadata`, `provenance`, `verified`, `receipt`, `revision`, `commit`, `exit`, `invocation` and `argv` have 0 hits each. `hash` has 3 hits (lines 30, 42, 71) and `timestamp` has 1 (line 56). |
| 8 | `git --no-optional-locks -C <lane> show <rev>:corpus/SOURCES.md \| grep '^\| S064 ' \| sha256sum` (GIT_* removed) for `4b7c682`, `7243e7f`, `21e7932` | 0 | `1498665a…` at all three. Baseline and working tree also match with the `grep -n` prefix (`4a2b9793…`, line 73). |
| 9 | same `git show … \| sha256sum` for `.ufo/evidence/round-18/measure.py` at `4b7c682`, `7243e7f`, `21e7932`, plus the working-tree file | 0 | `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` everywhere |
| 10 | lane grep for page-body phrases (`Arbitrary processing in`, `always returns the same output by isolating`) | 1 | no matches: the lane retains no copy of the page body, and the `76167a0d…` bytes survive only in disposable `/tmp` |

## Quote

> "The output of an action can be cached, and the action need not be run again unless inputs change."

Source: https://bazel.build/basics/hermeticity, §Benefits, "Speed" bullet
(markdown alternate `…/hermeticity.md` lines 37–38). Accessed 2026-10-21; 19
words. It matches the round-17 Gate quote (`corpus/lessons/round-17.md:38`) and
sits inside the row's registered anchor.

The following secondary sentences were also checked verbatim today (≤25 words
each):

- §Identifying non-hermeticity, md lines 57–58: "System binaries that differ across
  hosts (such as `/usr/bin` binaries, absolute paths, system C++ compilers for
  native C++ rules autoconfiguration)" (20 words). This is inside the anchor.
- §Overview › Source identity, md lines 30–31: "Hermetic build systems use this
  hash to identify changes to the build's input." (13 words). This is outside
  the registered anchor, so it would need its own anchor if it were ever cited.

## Tier, scope and limits

- **Tier A / `docs` holds for the row's scope.** The frozen contract
  (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:26-30`)
  says: "A: primary or authoritative for that scope (spec, official docs, …)".
  Bazel's own docs page is authoritative for Bazel's own definition and
  catalogue, and for nothing wider.
- **Limit 1, scope.** The page covers build actions, caches and host inputs. It
  contains no text on metadata headers, receipts, revisions, exit status or
  invocation (row 7). Any transfer to lane receipts is [INFERENCE].
- **Limit 2, no revision pin exists.** The page shows no version or commit.
  `last-modified` is generated per request (row 1). The deployment id moved from
  `dpl_8LJVMfxYNq6LJkohTrn2iyWT8umj` (round 17,
  `.ufo/waves/round-17/w1/S19SrcBazelHermetic.md:16`) to
  `dpl_CUnGQP1HgFUzoxatVC37y4zP83Vx` today.
- **Limit 3, the anchor digest is stale (observation, 2026-10-21).**
  - The row's markdown sha256 `76167a0d…` no longer reproduces at the URL. The
    live sha256 is `029067f4…`, stable across three fetches.
  - The cause is renderer output only: five heading blocks changed (row 5). The
    anchored sections and the quoted text are unchanged.
  - The anchor dates the digest ("page fetched 2026-10-20"), so the row is a
    true dated observation, not an error. Contract rule 2 does not require a
    supersede row.
  - Still, a byte-level re-check now fails even though the text is the same,
    and the pinned bytes are not retained in the lane (row 10).
- **Limit 4, wording (carried forward).** "Outside the key" in `teaches` is the
  lane's gloss. The page links keying to hashing only in the §Benefits "Parallel
  execution" bullet ("hash inputs to look up in the cache", md line 42). This was
  already noted in `.ufo/waves/round-17/w2/ReopenS064.md:95-99`.

## Applicability to round-19 C1 (frozen population, `.ufo/evidence/round-19/contract.json`)

| defect | does S064 support the correction? | basis |
|---|---|---|
| R18-1 PENDING `verified-at` metadata | **no** | no metadata, provenance or verified text on the page (row 7) |
| R18-2 S008 "queued" vs `mined` | **no** | registry-status consistency is a lane contract matter (contract rule 2), not Bazel hermeticity |
| R18-3 four vs five deleted lines | **no** | count arithmetic; the page is silent |
| R18-4 failed `--selftest` row (exit 64) | **no** | invocation correctness and observed exit status belong to S049 (`CompletedProcess`), which round 19 already uses (`corpus/lessons/round-19.md:27-40`) |
| R18-5 no 60/60 receipt at `4b7c682` | **analogy only** [INFERENCE] | §Benefits says a stored output stands only while inputs are unchanged. By analogy, a 60/60 receipt at `a85f710` is not a receipt at `4b7c682`. See the consistency check below. |

**R18-5 consistency check (observation).** The round-19 R18-5 receipt and its
ruler agree with S064's principle:

- The receipt binds `"revision": "4b7c6823…"` and
  `--rev 4b7c6823…` (`.ufo/evidence/round-19/round18-final-measure.json:8,11`).
- The ruler requires `value['revision'] == REV18 and value['rev_input'] == REV18`
  (`.ufo/evidence/round-19/measure.py:129`).
- The replay sets `PYTHONDONTWRITEBYTECODE=1` (`round18-final-measure.json:18`).
  This prevents bytecode writes into the source tree, the page's "Writing to the
  source tree during the build" item.

**S064-lens disclosure gap (advisory, not a C1 failure).** The R18-5 receipt
does not record which interpreter ran:

- Its argv runs host `python3` with an absolute `--repo` path
  (`round18-final-measure.json:3,6`). The page names both as non-hermetic inputs
  (md lines 57–58).
- The receipt has no interpreter or tool digest field. Its keys are argv,
  revision, exit, stdout/stderr paths and digests, recorded_at and environment.
- By contrast, the R18-4 receipt `bash-witness-selftest-complete.json` carries
  `tool_sha256`, `runner_sha256` and `cwd_kind`.
- The absolute path is disclosed in argv; `python3` is disclosed by name only.
- Mitigation observed: the executed `measure.py` blob is `7ca87a7c…` at
  `4b7c682`, `7243e7f`, `21e7932` and in the working tree (row 9), so tool drift
  across those revisions is excluded.
- The C1 criterion for R18-5 (a committed 60/60 receipt at `4b7c682`) is met as
  observed.

## Recommendation

1. **Reject S064 as a round-19 C1 source or `used-by` addition.** It grounds
   none of R18-1 through R18-4. For R18-5 its only contribution is an analogy
   ([INFERENCE]) that the lane already states at
   `corpus/knowledge/input-keyed-coldread-credit.md:30` ("A cache hit is sound
   only for what its key records (S059, S064)"). Round 19's declared source
   remains S049, as in `contract.json`'s `sources` and `round-19.md:27-40`.
   Adding S064 would add a transferred citation whose byte pin no longer
   reproduces.
2. **Keep S064 unchanged for its existing use.** The quote is verbatim at its
   anchor today, the tier is correctly scoped, and `mined` is still justified by
   `used-by` (`…credit.md:30`). Round 19 does no harm to S064: the row bytes are
   identical at the baseline and the delivered revision.
3. **Advisory for the registry owner (outside C1; I made no edit).** The next
   S064 re-check (90d in `…credit.md:3`, 180d in the row) should compare the
   anchored prose, not the raw markdown bytes. Alternatively, append a dated note
   recording the digest move `76167a0d…` → `029067f4…` on 2026-10-21 (heading
   markup only, quoted text unchanged). If byte re-verification matters, the
   2026-10-20 bytes need durable retention; today they exist only at
   `/tmp/bazel-hermeticity.md`.

## Observed vs inferred vs unknown

- **Observed:**
  - HTTP status, sizes, digests and headers (rows 1–4).
  - The diff hunks (row 5).
  - The quote's position and word count (row 6).
  - The term sweep (row 7).
  - Row and tool blob identity across revisions (rows 8–9).
  - That the lane retains no page body (row 10).
  - The contents of the R18-4 and R18-5 receipts and ruler lines 61–76 and
    121–136.
- **Inferred:**
  - The Bazel-cache to lane-receipt transfer for R18-5.
  - That the digest change comes from the Mintlify renderer or a deployment,
    based on the heading-only diff and the deployment-id change.
- **Unknown:**
  - The upstream source commit for the page. Round 17 found the raw GitHub path
    returning 404 and the API rate-limited; I did not retry.
  - Whether the CDN-served HTML mixes deployments. The first HTML `link` header
    still names an asset `?dpl=dpl_8LJV…`, while `x-version` is `dpl_CUnG…`.
    This does not affect the quote.

## Untrusted-content note

- The markdown body opens with text addressed to readers: "Fetch the complete
  documentation index at: https://bazel.build/llms.txt" (md lines 1–3).
- The response `link` headers advertise agent-card, mcp-server-card and
  agent-skills endpoints.

I treated both as data and followed neither.

## Scope statement

- Read-only. The only lane write is this report.
- Git use was limited to `git --no-optional-locks … show` and `log -1`, run with
  `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_CEILING_DIRECTORIES` and
  `GIT_OBJECT_DIRECTORY` removed.
- I made no ref, index, JJ, registry or production change.
- I installed or updated no tool.
- I ran no tests, builds, lints, formatters or lane selftests.
- I executed no receipt argv; the receipts were read as files.
