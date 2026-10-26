# T48ExecFetchS093 — C2 fetch for target S093

Seat: T48ExecFetchS093 (leaf). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at base
`473336d9d789f6081195e7376d17836a24666bc3`. Contract read first, including `amendments` 1–3
(1: "R's URL" is the URL set of R's source and anchor cells, and the receipt/live-fetch url must be
in it; 2: extraction and quote-freezing rule; 3: C1 grammar only). I edited no registry row, no
knowledge entry, no counter, no lesson file, no Git index and no jj state. Written: the two
deliverables below plus this report. Scratch `/fast/scratch/hyaku/tameshi-r48/T48ExecFetchS093`
removed at completion.

## Deliverables written

- `.ufo/waves/round-48/w1/sources/S093.xml` — fetched bytes, byte-exact.
  sha256 `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da`, 33,289 B.
  `cmp` against the fetched scratch file → identical; `sha256sum`/`stat -c %s` on the deliverable
  re-derived after the copy.
- `.ufo/waves/round-48/w1/sources/S093.receipt.json` — url
  `https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml`, fetched_at
  `2026-10-26T08:41:10Z`, http_status `200`, bytes `33289`, sha256 as above, tool
  `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5 zlib/1.3.2 brotli/1.2.0
  zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.70.0 ngtcp2/1.25.0
  nghttp3/1.18.0 mit-krb5/1.22.2`. JSON re-parsed and re-checked against the snapshot bytes
  (`sha256` equal, `bytes` equal, `http_status` 200) after writing.

## Base row read

`corpus/SOURCES.md:102` (cells split on `|`):

| # | cell |
|---|---|
| 2 (source) | bwrap(1), bubblewrap 0.13.1 — https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml |
| 3–4 | docs / A |
| 5 (scope) | documented meaning of --unshare-all, --clearenv, --proc, --tmpfs, --die-with-parent and --new-session in bwrap 0.13.1; not a measured security boundary for any argv |
| 6 (anchor) | tag v0.13.1 (commit 362936aea0d5c6e70f7af75d2d44b5a914cb4ba2, released 2026-10-14); bwrap.xml:159, :233-235, :403, :412-416, :575-577, :589-592; README.md:52-54 and :133; xml sha256 2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da (33289 bytes), re-fetched by the L1 with the same digest; local man bubblewrap 0.13.1-1 |
| 7 (teaches) | score --unshare-all as its six-flag expansion, with user and cgroup try-else-skip, and score every other flag on its own sentence; the word all is not a sealed isolation claim |
| 8–10 | mined / 2026-10-23 / on-release |
| 11 (used-by) | corpus/knowledge/regression-tally-completeness.md |

The base row's **anchor line numbers are still exact in the live bytes**: `:159` is the
`--unshare-all` `<listitem>`; `:233-235` is the `--clearenv` definition ("Unset all environment
variables, except for PWD and any that are subsequently set by --setenv"); `:403` procfs, `:412-416`
tmpfs (mode 0755 / `--perms` / `--size`), `:575-577` new-session/setsid, `:589-592`
die-with-parent/`PR_SET_PDEATHSIG`. The row's anchor is not stale in either digest or line numbers.

## Round-45 ledger entry and dispute (read, not edited)

`.ufo/evidence/round-45/freshness/ledger.json`, entry `S093`: `verdict: holds`,
`raw_sha256 f8a95822f7277eae4809c664bef2e6b1ca0749f4cb6fb373c123f4c9c303e240`,
`snapshot .ufo/evidence/round-45/freshness/sources/S093.raw.gz`, `author ExecRows17`, quote
`< option >--unshare-user-try</ option > < option >--unshare-ipc</ option > < option >--unshare-pid</ option > < option >--unshare-net</ option > < option >--unshare-uts</ option >`.

`.ufo/evidence/round-45/freshness/reviews.json`, id `S093`, reviewer `CritJudge03`, verdict
**`dispute`**: "Quote is a 25-token markup-only fragment of the --unshare-all listitem that never
names --unshare-all, omits 'Unshare all possible namespaces. Currently equivalent with:' and
truncates before the sixth flag --unshare-cgroup-try, so it does not state the teaches claim
(six-flag expansion, user and cgroup try-else-skip); only shared content words are 'unshare' and
'user'." Round-45's own spot-check (`corpus/lessons/round-45-verifier-spotcheck.md:34-36,73`)
agreed with that dispute and recorded that the round-45 carrier was a *different artifact* from the
row's XML (`S093 differ in bytes (dynamic pages)`), because round-45 snapshotted the GitHub blob
HTML page, not `raw.githubusercontent.com` bytes.

## Fetch facts (first fetch; the retained bytes)

`curl -sS -L -D S093.headers -o S093.xml -w '%{http_code} %{size_download}\n' 'https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml'` → `200 33289`.

Headers (`S093.headers`): `HTTP/2 200`, `content-type: text/plain; charset=utf-8`,
`content-length: 33289`, `etag: "283e47c44715d259d04f715de3115f41d9afb066ff9c2a8a6016f0a3d8656a22"`,
`date: Mon, 26 Oct 2026 08:41:10 GMT`, Fastly `x-cache: HIT`, `accept-ranges: bytes`.
A second fetch at `2026-10-26T08:42:12Z` (local UTC clock bracketing the call) returned `200 33289`
and was `cmp`-identical, sha256 unchanged — the retained bytes are reproducible within the wave.

`fetched_at` in the receipt is the server `date:` header of the retained fetch
(`2026-10-26T08:41:10Z`); the confirming re-fetch is reported here rather than in the receipt, so
the receipt names exactly one fetch of exactly the retained bytes.

## Extraction (amendment 2) and the quote

Extraction applied to the fetched 33,289 B: UTF-8 decode → drop `<script>`/`<style>` element
contents (the file has **0** such elements; it is DocBook XML) → strip tags → `html.unescape`
(one `&` in the file, outside the quote) → collapse whitespace runs to one space. Normalized text
length **16,699** characters.

Quote delivered (exact, already whitespace-collapsed):

```
--unshare-cgroup-try Create a new cgroup namespace if possible else skip it --unshare-all Unshare all possible namespaces. Currently equivalent with: --unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try
```

- **Token count: 25** whitespace tokens (`len(quote.split())` = 25) — at the C2 cap, not over it.
- Contains **both** required phrases for S093: `--unshare-all` and `--unshare-cgroup-try`.
- Verbatim: `text.count(quote)` = **1** in the amendment-2 normalized text (substring, no case or
  punctuation folding).
- States the teaches claim: `--unshare-all` is "Unshare all possible namespaces. Currently
  equivalent with:" its six flags, and the sixth of them is `--unshare-cgroup-try`, whose own
  definition in the same quote is "Create a new cgroup namespace if possible else skip it" — i.e.
  the cgroup try-else-skip half. The user half is carried by `--unshare-user-try` in the six-flag
  list (its own try-else-skip wording, "Create a new user namespace if possible else skip it", sits
  in the sibling `varlistentry` at raw lines 130–131 and does not fit under the 25-token cap).
- **Location**: §**Options**, `<refsect1><title>Options</title>` at raw line 71; the quote spans two
  consecutive `<varlistentry>` blocks inside that section — the `--unshare-cgroup-try` entry at raw
  lines **153–156** (`<term><option>--unshare-cgroup-try</option></term>` at 154, listitem at 155)
  and the `--unshare-all` entry at raw lines **157–160** (`<term>` at 158, `<listitem><para>Unshare
  all possible namespaces. Currently equivalent with: …</para></listitem>` at 159). Contiguous raw
  span = lines **154–159**, raw byte offsets **5909–6400**; normalized-text offset **2641**.
- Dispute answer: round-45's fragment started at the third flag of the expansion and stopped at the
  fifth, so it neither named `--unshare-all` nor reached `--unshare-cgroup-try`. This quote starts
  at the sixth-flag entry with its try-else-skip definition and runs through the
  "Currently equivalent with:" heading and all six flags, so both the name and the sixth flag are
  inside it, and the try-else-skip wording for cgroup is quoted rather than inferred.

## Proposed anchor cell text for the new superseding row

```
§Options (`<refsect1><title>Options</title>`, raw line 71), the `--unshare-cgroup-try` and `--unshare-all` varlistentries at bwrap.xml raw lines 153–160 (quote lines 154–159, bytes 5909–6400), tag v0.13.1 (commit 362936aea0d5c6e70f7af75d2d44b5a914cb4ba2) fetched 2026-10-26 from https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml; sha256 2cb77df2f4be, 33289 bytes
```

sha256 first 12 hex = `2cb77df2f4be`; bytes = 33,289; revision = the tag/commit the row already
pins (the file's `<refentryinfo>` carries no version or date, so the tag is the revision evidence).
**Amendment-1 note for the L1:** S093's base *source* URL is the GitHub **blob** page, while the
snapshot and receipt url are the **raw** file. Amendment 1 is satisfied only if the new row's
source or anchor cell also carries the raw URL — hence it is inside the proposed anchor text above
(the source cell can carry the blob URL unchanged, or both).

## Drift verdict

**No drift; the teaches cell still holds.**

- **Live vs base row anchor: equal on both fields.** Live sha256
  `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da` and 33,289 B are exactly the
  base row's `xml sha256 … (33289 bytes)`; the base row's cited line numbers are all still correct
  (checked above).
- **Live vs round-30 snapshot: equal.** `.ufo/evidence/round-30/sources/S093-bwrap-0.13.1.xml` is
  33,289 B with the same sha256, so the raw XML has been stable from 2026-10-23 through
  2026-10-26.
- **Live vs round-45 snapshot: different artifacts, not different content.** The round-45 ledger's
  `raw_sha256 f8a95822…` is the sha256 of the **gunzipped** `S093.raw.gz`: the gz is 65,568 B
  (sha256 `bcf09dc0c4bde73f1e482942c1df96556c70a65a451bb06c03a423228c919661`) and decompresses to
  601,469 B of GitHub **blob HTML**, sha256 `f8a95822f7277eae4809c664bef2e6b1ca0749f4cb6fb373c123f4c9c303e240`.
  So no byte comparison is possible between it and the 33,289 B XML, and the differing digests are
  not evidence of a source change. What the round-45 carrier *does* show, on re-extraction, is that
  its rendered text already contained `--unshare-all`, `--unshare-cgroup-try` and "Currently
  equivalent with:" — the round-45 defect was the chosen quote fragment, not a stale document.
- **What changed:** nothing in the source. Round 45's snapshot carrier (blob HTML) is replaced by
  the raw XML at the same tag, whose digest equals the row's own pin, and the quote is replaced by
  one that carries both required phrases and the try-else-skip wording.

## Entry cites that the new row must re-point (owner action, not done here)

Base used-by cell is `corpus/knowledge/regression-tally-completeness.md` only. Occurrences of the
id in that file: line 1 (`source: … S093 — bwrap(1), bubblewrap 0.13.1 \`bwrap.xml\``), line 3
(`recheck: … re-open S087, S093, S094`), line 42 (the `v4` row's "bubblewrap sandbox (S093)"), line
68 ("S093's `--unshare-all` is six flags, two of them try-else-skip"), line 72 (E1's
`S093 bwrap.xml:233-235` quote). Under the C2 statement these must cite the new id with
`verified-at: 2026-10-26`. Out-of-cell observations for L1 (not in S093's base used-by cell, so not
required by the frozen statement, flagged rather than acted on): `corpus/lessons/round-30.md:16,36-38,51-52,57`,
`corpus/lessons/round-30-verifier-spotcheck.md:159,193`, `corpus/lessons/round-45.md:162`,
`corpus/lessons/round-45-verifier-spotcheck.md:34-36,73`, `corpus/README.md:453` (rows a name, not
the id, at 453).

## Evidence actually run (scratch only, no verdict scoring)

- `curl -sS -L -D S093.headers -o S093.xml -w '%{http_code} %{size_download}\n' '<raw tag URL>'` → `200 33289`; `sha256sum` → `2cb77df2…1da`; `stat -c %s` → `33289`; `curl --version | head -1` → the receipt `tool` value.
- Second `curl … -o S093.again.xml` bracketed by `date -u` → `before=after=2026-10-26T08:42:12Z`, `200 33289`, `cmp` → `CMP_IDENTICAL`.
- `cp` deliverable then `cmp` fetched vs deliverable → `CMP_OK`; deliverable `sha256sum`/`stat` re-derived.
- Round-45 snapshot: `gunzip` → 601,469 B, sha256 `f8a95822…` (matches ledger `raw_sha256`), gz sha256 `bcf09dc0…`; amendment-2 extraction over it → contains both required phrases.
- Round-30 snapshot sha256 → same `2cb77df2…1da`, 33,289 B.
- Python amendment-2 extraction over the live XML → quote substring count 1, 25 tokens, normalized offset 2641, raw span 5909–6400.
- Receipt JSON re-read and compared against the bytes: `sha256`/`bytes` equal, `http_status` 200.

No counter was built, run or scored; no `--only`/`--no-live` probe was needed (this item is a
fetch, not a measurement); no gate/tests/lint were run, per wave bounds.

## Risks / caveats

- The quote is exactly at the 25-token cap; a counter that counts tokens differently (e.g. a
  stricter splitter that separates `with:` punctuation) would push it over. It is 25 under
  whitespace splitting as amendment 2 specifies.
- The user-side try-else-skip wording ("Create a new user namespace if possible else skip it" for
  `--unshare-user-try`) is at raw lines 130–131 and cannot be included inside the cap; the quote
  carries `--unshare-user-try` as a name and the cgroup try-else-skip wording verbatim.
- Amendment 1 depends on the new row carrying the raw URL somewhere in source/anchor; it is in the
  proposed anchor text. If the L1 keeps only the blob URL, the receipt url would fall outside R's
  URL set — a mechanical C2 miss that is not a document problem.
- `fetched_at` uses the server `date:` header second; the local clock seconds agree within the same
  minute (08:42:12Z for the confirming fetch).
- No tool install/upgrade was needed (curl 8.23.0, python3 present; pacman paused and unused), so
  no tool/version/channel record is due.
- No fixture repo was created, so no throwaway commit identity was used; `/fast/scratch/hyaku/tameshi-r48/T48ExecFetchS093` is deleted before finishing.
