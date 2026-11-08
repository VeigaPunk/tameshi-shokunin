# Draft — `SC1-sources.md`: the two Gate citations verified against the committed snapshots

Verification of the round-97 lesson's `## Gate` (§8–41 of `corpus/lessons/round-97.md`) against
the committed snapshots in `.ufo/evidence/round-97/sources/`. Method: the canonical lane
renderer `.ufo/waves/round-93/w1/R93S1-tagstrip.py` — `strip_tags` (script/style blocks and
comments removed, each tag replaced by one space, entities unescaped, lines right-trimmed) and
`locate` (word-sequence match with edge punctuation stripped, reporting the line span).
Receipt: `.ufo/waves/round-97/w1/SC1-sources-check.txt`.

## What checks out

| item | lesson says | committed bytes | verdict |
|---|---|---|---|
| S159 quote | "Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation testing." | located at **line 762** of `s159.html` under the canonical renderer; span `(762, 762)` | **line ✓** |
| S159 snapshot | `s159.html`, 171 636 B, sha256 `4b5a8374…` | 171 636 B, sha256 `4b5a837439ad81d587eb29bdefbbd4ad0d75232a6ba606f8fff74c6d13092884` | **✓** |
| S006 quote | "A row whose old literal occurs more than once in its target there is refused: the rewrite takes the first copy, which might not be the one the row means." | located at **lines 490-492** of `s006.html`; span `(490, 492)` | **lines ✓** |
| S006 located span | "A row whose old literal occurs more than once in its target there is refused" | span `(490, 491)` | **✓** |
| S006 snapshot | `s006.html`, 281 627 B, sha256 `55bb7196…` | 281 627 B, sha256 `55bb719635d58892dfc271651d3fadb14d5374bbbf7335b0a775a513b65a686a` | **✓** |
| S006 `used-by` | gains `corpus/lessons/round-97.md` | S006's `used-by` cell ends `… corpus/lessons/round-76.md, corpus/lessons/round-97.md` | **✓** |
| S159 `used-by` | (silent) | S159's `used-by` cell ends `… corpus/knowledge/r43-survivor-resolution-rule.md, corpus/lessons/round-97.md` | **✓ (committed)** |
| census | exit 0, rows 183 | rows 183 (A 165 · B 14 · C 4), mined 149 · queued 23 · rejected 11, exit 0 | **✓** |

## Mismatches — exact bytes

### M-A — S159 word count: the lesson says 14, the tokenizer says 15

Lesson (`corpus/lessons/round-97.md:19`):

    to practical usage of mutation testing." (14 words) — grounds the `limit` class: an

The Gate's own convention (line 13: "Word counts are `len(quote.split())`") applied to the
quoted span:

    "Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation testing."
    → len(q.split()) = 15

15 ≠ 14. This is the same defect QUALITY 172 names for round 95 ("a quote's word count is the
accepting tokenizer's count (`len(q.split())`)"), and the round-95 lesson's M1 was exactly
this. **The count should read `(15 words)`.**

### M-B — S006 word count: the lesson says 16, the tokenizer says 15

Lesson (`corpus/lessons/round-97.md:28`):

    there is refused" (16 words) — grounds the `edit-ambiguous` refusal (a matrix that

    "A row whose old literal occurs more than once in its target there is refused"
    → len(q.split()) = 15

15 ≠ 16. **The count should read `(15 words)`.** (The longer two-clause span the lesson
quotes in full, "A row whose old literal occurs more than once in its target there is
refused: the rewrite takes the first copy, which might not be the one the row means.", is 30
words under the same tokenizer and is not given a count in the lesson — the `16 words` is
attached to the shorter located span.)

### M-C — S159 HTTP date: the lesson says 14:31:52 GMT, the committed header says 04:11:08 GMT

Lesson (`corpus/lessons/round-97.md:17`):

      08 Nov 2026 14:31:52 GMT; 171636 B; snapshot `s159.html` sha256 `4b5a8374…`), line 762

Committed `.ufo/evidence/round-97/sources/headers-s159.txt` (CRLF line endings, as fetched):

    HTTP/2 200
    date: Sun, 08 Nov 2026 04:11:08 GMT
    …
    content-length: 171636

`14:31:52` appears in **no committed file** — `git grep -l '14:31:52' HEAD` returns only
`corpus/lessons/round-97.md` itself. The `date:` line the fetch recorded is **04:11:08 GMT**.
(The file's own `last-modified: Sun, 08 Nov 2026 01:39:18 GMT` and `age: 36049` show a
cached Wikipedia response; the `date:` header is the origin's response time, not the fetch
time.) The size (171 636 B) and digest (`4b5a8374…`) in the lesson are correct — only the
date is wrong.

### M-D — S006 HTTP date: the lesson says 14:18:19 GMT, the committed header says 14:04:16 GMT

Lesson (`corpus/lessons/round-97.md:24`):

      14:18:19 GMT; 281627 B; snapshot `s006.html` sha256 `55bb7196…`), lines 490-492 under the

Committed `.ufo/evidence/round-97/sources/headers-s006.txt`:

    HTTP/2 200
    date: Sun, 08 Nov 2026 14:04:16 GMT

As with M-C, `14:18:19` appears in no committed file except the lesson itself. The size and
digest are correct.

### M-E — the S324 note contradicts itself and points at a row that is not in the registry

The Gate's closing paragraph (`corpus/lessons/round-97.md:33-41`) says, in order:

1. line 33-34: "A draft row for the Stryker "Equivalent mutants" page was appended as S324
   and withdrawn before the freeze: the URL already has a row (S160), and the census flagged
   the duplicate (W04)".
2. line 41: "The equivalent-mutant ground was instead opened from S324, which is fetchable."

Sentence 2 says the ground was opened from **S324**; sentence 1 says S324 was **withdrawn**,
and the M3 mistake row (`corpus/lessons/round-97.md:48`) says the ground was "re-opened from
S159 (the definition-and-standing row)". The lesson's own S159 bullet grounds the `limit`
class, so the ground was in fact opened from **S159**. Sentence 2 is a leftover from before
the withdrawal and should read "from S159". The `## Registry changes` section (line 57ff) has
it right — "A draft row … (appended as S324) was withdrawn before the freeze" — so the two
sections of the same file disagree.

Two supporting facts: `git grep -c '^| S324 ' corpus/SOURCES.md` is **0** — no S324 row is
in the registry, and the draft was never committed. And the M3 row's pointer "census output
`W04 S324 duplicate url stryker-mutator.io/…` before the withdrawal" names output that is in
**no committed file**: the committed `census-before.txt` carries
`W04 S160 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants
across scopes` (S160, the row that holds the URL), and `git grep -l 'W04 S324' HEAD` returns
only the lesson itself. The withdrawn row's census warning was never committed.

### M-F — the S159/S006 `anchor` cells were not updated to the re-opened snapshots

The lesson re-opened S159 and S006 with byte-pinned snapshots under
`.ufo/evidence/round-97/sources/` and quotes them by line. The registry rows' `anchor` cells
still name the **old** snapshots:

- **S159** `anchor`: `§Mutation testing overview, p ids mw-Q and mw-w, and §Overview p mw-Q @
  page fetched 2026-10-25, snapshot .ufo/evidence/round-43/sources/wikipedia-mutation-testing.html
  170793 B sha256 6e4a06c0 revid 1373580212`
- **S006** `anchor`: `README §The three verdicts and §How a row is run @ page currentOid
  7eefc73010ad6342b80e3ed43915503e02c90618, fetched 2026-10-19`

Under the S159 anchor's own snapshot the same sentence sits at **line 753**, not 762 (measured
with the same renderer); the lesson's line 762 belongs to the round-97 `s159.html`. So a reader
following the registry's anchor lands 9 lines off the quote the lesson quotes — the round-95
D1 / round-96 M4 renderer-drift class, one layer up. The round-96 lesson handled exactly this
by moving S323's `anchor` line number (`2355` → `2358`) and naming the renderer in the cell.
**S159's anchor should be repointed to `.ufo/evidence/round-97/sources/s159.html` 171636 B
sha256 `4b5a8374…` line 762 (renderer named), and S006's to
`.ufo/evidence/round-97/sources/s006.html` 281627 B sha256 `55bb7196…` lines 490-492.**

### M-G — the S006 anchor quotes a page the snapshot does not carry verbatim

The S006 row's `teaches` cell reads "a non-unique literal is refused". That paraphrase does
not occur in `s006.html` at all (`locate` returns no span). It is a summary of the page, not
a quotation — the same paraphrasing defect round-96's Gate note names for the registry's
`teaches` cells ("These three sentences were paraphrased in the registry's `teaches` cell
(round-95 spot-check D4); quoting them verbatim here closes the gap on the reading side").
The S159 `teaches` cell has the same shape: "equivalent-mutant detection is one of the
biggest obstacles to practical mutation testing" is not in either snapshot (`locate` returns
no span). **Not a defect in the round's own citation** — the lesson quotes the pages verbatim
and correctly — but the registry's `teaches` cells are still paraphrases, and the round's
Gate does not say so.

### M-H — the S324 withdrawal is stated as "not opened" while the page was in fact fetched

The Gate heads its closing paragraph "Refused / not opened this round: **two**" and counts
S324 among them. The Stryker page **was** fetched — `.ufo/evidence/round-97/sources/equiv.html`
(38 687 B, sha256 `00082805…`) and `headers-equiv.txt` (`HTTP/2 200`,
`date: Sun, 08 Nov 2026 14:04:30 GMT`) are committed. What was refused was *admitting a
duplicate registry row*, not fetching the page. The last clause of the paragraph ("which is
fetchable") concedes this. **The heading should separate "one row withdrawn (page fetched)"
from "one source not opened (S009)".**

### M-I — the S009 snapshot is a 403 challenge page, and the lesson says so correctly

`headers-s009.txt`: `HTTP/2 403`, `date: Sun, 08 Nov 2026 14:04:16 GMT`, `cf-mitigated:
challenge`, `content-length: 5474`; `s009.html` is 5 474 B, sha256 `106e61ab…`. The lesson's
"fetched twice on 2026-11-08 and both responses were a Cloudflare challenge page (5 474 B,
sha256 `106e61ab…`, no abstract text)" matches the committed bytes for the one fetch that is
committed. The "twice" is not independently evidenced (one fetch is committed); the claim that
both were challenges rests on the single committed response.

## Also verified

- The `equiv.html` snapshot (38 687 B, sha256 `00082805…`) differs from the round-44
  `stryker-equivalent-mutants.html` (same size, sha256 `79f6501a…`) in 385 byte positions —
  the two fetches of the same URL are not byte-identical. S160's row still pins the round-44
  digest; the round-97 fetch was made for the withdrawn draft row and was never adopted.
- `git grep -c 'BATTERY states=' 07e50d6d` → rc 1, empty (C1's "before").
  `git grep -c 'GUARD_INERTIA' 07e50d6d` → rc 1, empty (C2's "before").
- `git cat-file -e 8ed9c526:.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt` → rc
  **128** (a missing path in a tree is a fatal error, not rc 1; rc 1 is what a missing
  *object id* gives). The lesson's D-a closure and the A6 amendment use 128; the committed
  **QUALITY 175 still reads "exit 1"** — see `SC1-quality.md`.
- The claim that S324 has no registry row: `grep -c 'S324' corpus/SOURCES.md` = 0 at HEAD.
