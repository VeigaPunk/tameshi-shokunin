# SrcDoctestReopen — C2 source re-open

Verdict: the versioned page is still Python 3.15.1 and still 216574 bytes, but a live fetch does not match the frozen snapshot. `cmp` exits 1. The only changed line is the footer clock (snapshot `18:17 UTC`, live `18:41 UTC`). Pin the committed snapshot digest in the Gate. Do not replace it with the live digest.

The module introduction's first grammatical sentence is 27 words, over the 25-word Gate cap. The Gate quote below is the 14-word opening clause of that sentence (HTML lines 245-246). That clause is the byte string the C2 counter requires inside the snapshot.

## Evidence

Access date: 2026-10-23. Two ordinary `curl` fetches, no browser. Scratch: `/fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-SrcDoctestReopen-4/`. No tools installed.

Fetch 1, exit 0 (`curl.ec`):

```
curl -m 60 -sS -D headers.txt -o doctest-live.html -w 'http_code=%{http_code}\nsize_download=%{size_download}\n' https://docs.python.org/3.15/library/doctest.html > curl-meta.txt; echo $? > curl.ec
```

Observed: `http_code=200`, `size_download=216574`. Response: `HTTP/2 200`, `last-modified: Fri, 23 Oct 2026 18:43:12 GMT`, `date: Fri, 23 Oct 2026 18:45:25 GMT`, `content-length: 216574`.

Fetch 2, exit 0 (`curl2.ec`), same command to `doctest-live2.html` / `headers2.txt` / `curl-meta2.txt`. Observed: `http_code=200`, `size_download=216574`, `date: Fri, 23 Oct 2026 18:46:55 GMT`, `age: 90`, same `last-modified`.

```
sha256sum doctest-live.html doctest-live2.html /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/c2/doctest-snapshot.html > sha-all.txt; echo $? > sha-all.ec
```

Exit 0. Digests:

- live and live2: `65a734a8ef4d4c7bead9d8e59beb97b937504e76349de333f6f9221219a22ef7`
- snapshot `.ufo/evidence/round-33/c2/doctest-snapshot.html`: `217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899`

```
wc -c doctest-live.html doctest-live2.html /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/c2/doctest-snapshot.html > wc-all.txt; echo $? > wc-all.ec
```

Exit 0. Each file is 216574 bytes.

```
cmp -s /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/c2/doctest-snapshot.html doctest-live.html; echo $? > cmp1.ec
cmp -s doctest-live.html doctest-live2.html; echo $? > cmp-live.ec
cmp -s /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/c2/doctest-snapshot.html doctest-live2.html; echo $? > cmp2.ec
```

Exits: snapshot vs live = 1, snapshot vs live2 = 1, live vs live2 = 0.

Line diff (both files 2216 lines): only line 2205.

- snapshot: `Last updated on Oct 23, 2026 (18:17 UTC).`
- live: `Last updated on Oct 23, 2026 (18:41 UTC).`

`18:17` and `18:41` are the same width, so the byte count does not move. Title line 20 and breadcrumb line 206 still say Python 3.15.1. The counter byte string `The doctest module searches for pieces of text that look like interactive Python sessions` is present in the snapshot and in both live bodies.

Module introduction, snapshot HTML (same text on the live page):

- Lines 245-247, opening paragraph, first sentence (27 words): "The doctest module searches for pieces of text that look like interactive Python sessions, and then executes those sessions to verify that they work exactly as shown."
- Lines 245-246, clause before the comma (14 words): "The doctest module searches for pieces of text that look like interactive Python sessions"
- Lines 249-250, first list bullet (18 words; the page uses U+2019 in "module's"): "To check that a module’s docstrings are up-to-date by verifying that all interactive examples still work as documented."

That 18-word bullet is what S055's Gate and `corpus/knowledge/executable-self-assessment.md:21-23` already quote. It is not the sentence the C2 counter searches for.

Registry at read time: highest id S099, S100 free, S098 also unused (left unused; this draft is S100 as assigned). `corpus/lessons/round-33.md` is absent (`test -f` exit 1). `corpus/knowledge/executable-self-assessment.md` exists (`test -f` exit 0) and still cites S055 plus the moving `/3/` URL.

## Smallest safe correction

Record sha256 `217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899` in the round-33 lesson Gate. That is the committed snapshot, and it is the digest `c2-measure.py` looks up after the label `sha256`. The live digest `65a734a8ef4d4c7bead9d8e59beb97b937504e76349de333f6f9221219a22ef7` may be named beside it as a later footer stamp. It must not be the only digest: the counter then fails `gate_sha_ok`.

Do not paste the 27-word sentence into the Gate. Use the 14-word clause.

Land the S100 row in the same commit as `corpus/lessons/round-33.md`. A `mined` row whose `used-by` path is missing fails the SOURCES census. The knowledge file exists, but it does not name S100 yet; an append-only citation belongs with the integrator, not in this seat.

## (a) SOURCES.md row (S100)

Eleven cells, no extra `|`. `teaches` opens with the required prefix. Status `mined` assumes the lesson file lands with the row.

| S100 | doctest — Test interactive Python examples — https://docs.python.org/3.15/library/doctest.html | docs | A | executable documentation examples | module introduction, opening paragraph, HTML lines 245-246 @ Python 3.15.1 documentation (URL path /3.15/; title line 20 and breadcrumb line 206 say 3.15.1); snapshot .ufo/evidence/round-33/c2/doctest-snapshot.html | supersedes S055 - the /3/ alias drifts; this pins the 3.15 build | mined | 2026-10-23 | on-release | corpus/lessons/round-33.md, corpus/knowledge/executable-self-assessment.md |

## (b) Lesson Gate bullet

S100 — https://docs.python.org/3.15/library/doctest.html — accessed 2026-10-23 — 216574 bytes — sha256 217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899 (committed snapshot `.ufo/evidence/round-33/c2/doctest-snapshot.html`; a later same-length fetch on 2026-10-23 hashed to 65a734a8ef4d4c7bead9d8e59beb97b937504e76349de333f6f9221219a22ef7 and differed only at the footer, 18:17 UTC to 18:41 UTC). Quote (14 words; module introduction, opening paragraph, HTML lines 245-246): "The doctest module searches for pieces of text that look like interactive Python sessions".
