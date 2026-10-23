# ReopenS059 — S059 pinned digests no longer reproduce

Routed item 2 of `corpus/lessons/round-28-verifier-spotcheck.md`. Fetches run
2026-10-23 01:29–01:32 UTC with `curl -sL`, five HTML responses total (three
spaced ~30 s plus two cache-busted with `?cb=`), three markdown responses ~30 s
apart. Scratch under `/tmp/s059`; nothing written outside this report.

## Verdict

**HTML: deploy-keyed — stable within a deployment, new bytes on every redeploy,
so it behaves non-deterministically on the recheck timescale.** Five responses
in ~90 s (01:29:38, 01:30:09, 01:30:39, plus two `?cb=` variants) were
byte-identical: sha256 `83f1c659d34b2c10a060b543d3551593d2f78d70f42a9175be821454b0361173`,
300387 bytes each. That digest matches neither the lesson's `9e3a2ebb…`
(297255 B, `corpus/lessons/round-28.md:13`) nor the spot-check's live
`4fe02a79…` (`corpus/lessons/round-28-verifier-spotcheck.md:71`). Three
distinct digests in ~30 h means the HTML is not stable across checks — but the
churn is the build stamp, not random per-request output: every redeploy rewrites
embedded `dpl_*` ids and hashed asset filenames inside the page body, so a
sha256 of the served HTML keys the deployment, not the content.

**Markdown alternate: content drift, once, then stable.** Three fetches at
01:31:11 / 01:31:41 / 01:32:11Z all returned sha256
`266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b16d67768a5b` (16210 B) —
identical to the round-28 trace's live value
(`.ufo/evidence/round-28/coldread/traces/ReopenS059-1.json:26`), different from
the row's recorded `0d362d11…` (`corpus/SOURCES.md:68`, fetched 2026-10-20).
The markdown changed once between the row's fetch and 2026-10-22 and has been
stable since.

## Evidence

Alternate URL: live page head carries
`<link data-mint-head rel="alternate" type="text/markdown" href="/remote/caching.md">`
→ `https://bazel.build/remote/caching.md`.

```
$ date -u '+now_utc=%FT%TZ'
now_utc=2026-10-23T01:29:38Z
html1 code=200 size=300387 t=0.294532 @2026-10-23T01:29:38Z
html2 code=200 size=300387 t=0.082252 @2026-10-23T01:30:09Z
html3 code=200 size=300387 t=0.262486 @2026-10-23T01:30:39Z
83f1c659d34b2c10a060b543d3551593d2f78d70f42a9175be821454b0361173  h1  (= h2 = h3)
cb1 code=200 size=300387 ; cb2 code=200 size=300387
83f1c659…1173  cb1  83f1c659…1173  cb2        # ?cb= variants identical
md1..md3 code=200 size=16210 @01:31:11/01:31:41/01:32:11Z
266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b16d67768a5b  m1  (= m2 = m3)
```

Varying region (the bytes a digest actually pins). Same page across deploys:

```
wayback 2026-09-11 capture        : dpl_7hZ6jxtgycdcE9n1eU8TGPD9xvC9   (405906 B)
stale 103 Early-Hints today 01:29Z: dpl_GnxaU9nEer7XK27kw3dpfPrs9geh
live 200 today 01:29Z             : dpl_5UDDZ9hnigTkoV7QtvQ39eUp84nu   (300387 B)
dateModified                       "2026-09-05T03:00:05.915Z" → "2026-10-20T15:33:42.539Z"
<link …BannerMarkdown-DDchecE6.js?dpl=dpl_5UDDZ9hnigTkoV7QtvQ39eUp84nu>
headers: x-version/x-served-version: dpl_5UDDZ… ; last-modified: Thu, 22 Oct 2026 22:30:16 GMT
```

The 10-22 22:30Z `last-modified` alone explains the `4fe02a79…` (2026-10-22
~19:30Z) → `83f1c659…` (2026-10-23) rotation; `9e3a2ebb…` predates that day's
redeploys. The recorded 2026-10-22 HTML bytes are not preserved anywhere in
`.ufo`, and no wayback capture exists in the window (nearest 2026-09-11), so a
byte diff against `9e3a2ebb…` itself is not possible; the deploy stamp and size
(297255 → 300387 B) are what moved.

Row scope still holds: the live markdown contains both row quotes verbatim —
"The action cache, which is a map of action hashes to action result metadata."
and "Bazel does not track tools outside a workspace".

## Contract answer — supersedes row, not a note

SOURCES contract rule 2 (`/home/vgpnk/Projects/shokunin/CORPUS.md`, "Append-only"):
only `status`, `recheck` and `used-by` change in place; **a correction is a new
row whose `teaches` opens `supersedes S0NN —`**. The stale digest lives in
S059's `anchor` cell, which is immutable — a recorded note in a lesson cannot
repair the row, and an in-place edit is forbidden. A supersedes row is
therefore required either way; the non-determinism finding belongs in the new
row's `anchor`/`teaches`, not as a substitute for it.

Caveat for the integrator: CriticRound (`w1/CriticRound.md:161`) flags that
appending to `corpus/SOURCES.md` after milestone A collides with criterion 56
(input edits must precede cold reads). The row is needed under the contract;
the sequencing is the lane's to schedule.

Smallest safe correction (draft, not applied — this seat may not edit corpus):
new row `S092` (or next free id), same URL and scope, `teaches` opening
`supersedes S059 —`, `anchor` pinning content-borne fields only —
`dateModified: 2026-10-20T15:33:42.539Z` plus
`markdown alternate sha256 266915c5…, fetched 2026-10-23` — with a note that the
served HTML sha256 is deploy-stamped (`dpl_*` + hashed asset names) and must
not be pinned as a page digest.

Report: .ufo/waves/round-29/w1/ReopenS059.md
