# T50ScribeSrcHeld — held F6 source rows re-opened (S022, S024)

Item: re-open the two held F6 rows the C2 shrinker method rests on; re-fetch each URL with
provenance, check the row's anchor and teaches/quote cell are still carried by the page, and
locate a <= 25-word passage per topic. Read-only on the lane.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, revision read `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`
  (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log -1 --format='%H %cI %s'`); round-start base `e3729de8…`.
  No lane file was modified; no git/jj mutation.
- Rows: `corpus/SOURCES.md:33` (S022), `corpus/SOURCES.md:35` (S024)
  (`grep -n '| S022 |\|| S024 |' corpus/SOURCES.md`).
- F6 frontier row: `corpus/README.md:83` — sources `S022, S023, S024`, status `open`.
- Verdicts: **S022 still valid: yes** (no cell must change). **S024 still valid: yes** (no cell must change).

## S022 — MacIver & Donaldson, ECOOP 2020

### Fetch receipt

| field | value |
|---|---|
| URL | `https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13` |
| method | `curl -sS -L -A 'Mozilla/5.0 (X11; Linux x86_64) tameshi-source-check/1.0'` |
| HTTP status | 200 |
| effective URL | same as requested (no redirect) |
| bytes | 115315 |
| sha256 | `fa3036a38b8ba6f9827219c07a7db179f272ac798932cb75edd9cfd37d2d58e3` |
| fetched (UTC) | 2026-10-26T22:15:06Z |
| HEAD (UTC) | 2026-10-26T22:16:32Z |
| cache headers | `Cache-Control: no-cache, private`; sets `XSRF-TOKEN` and `drops_session`; **no `Last-Modified`, no `ETag`** |
| DOI resolution | `curl -L https://doi.org/10.4230/LIPIcs.ECOOP.2020.13` → 200, lands on the same entity URL (2026-10-26T22:16:59Z) |

Page metadata confirmed in the fetched bytes: title "Test-Case Reduction via Test-Case Generation:
Insights from the Hypothesis Reducer (Tool Insights Paper)"; authors David R. MacIver, Alastair F.
Donaldson; 34th ECOOP 2020, LIPIcs; publication date 2020-11-06; 27 pages; DOI
10.4230/LIPIcs.ECOOP.2020.13; URN `urn:nbn:de:0030-drops-131700`. This is the document the row names.

### Anchor check — still present

Row anchor cell: `Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19)`.

- `<section class="metadata abstract">` at raw offset 62338, `<h2>Abstract</h2>` at 62383,
  visible abstract in `<pre class="content">` at 62551 — complete, 1583 characters, no ellipsis,
  ending "…applicable to any random generator of test cases."
- The abstract is carried three times in the same bytes: `<meta name="DC.Description">` (copy at
  raw 2018), the JSON-LD `ScholarlyArticle.abstract` (copy at 13682), and the visible section (62551).
  All three carry the sentence quoted below.

### Teaches cell — every clause still carried

Row teaches: "internal reduction shrinks the sequence of random choices made during generation, so
every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging".

Verbatim page fragments (`python3` strip-then-substring check over the fetched bytes, all `True`):

- "we apply it internally, to the sequence of random choices made during generation"
- "by ensuring that any reduced test case is one that could in principle have been generated"
- "comparing its effectiveness with that of several other test-case reducers, including C-Reduce and delta debugging"

### Located passage (a) — validity problem of reduced test cases, 25 words

> significantly mitigates the impact of the test-case validity problem, by ensuring that any reduced test case is one that could in principle have been generated

- 25 words, 159 characters, contiguous in the fetched bytes (present at raw 2803 / 14467 / 63336 in
  the three copies); this is the tail of the sentence whose subject is "It also".
- Its containing sentence in full is 29 words, over the 25-word cap, hence the tail span.
- Context that fixes the referent: "The key idea … is that instead of applying test-case reduction
  externally to generated test cases, we apply it internally, to the sequence of random choices made
  during generation".

### Drift

- **No content drift observed.** All anchor and teaches fragments are present; the paper identity is unchanged.
- **No byte-level baseline exists for S022.** `find .ufo/evidence -iname '*S022*'` returns nothing —
  only S024 has a committed snapshot (`.ufo/evidence/round-29/sources/`). Because the DROPS entity page
  is dynamic (`Cache-Control: no-cache, private`, per-request session cookies, no `Last-Modified`/`ETag`),
  today's sha256 can only be a *new* baseline, not a comparison against the 2026-10-19 bytes.
  Freshness for S022 is therefore asserted at content level, not byte level.
- **Citation label is a paraphrase, not drift.** The page title carries the subtitle
  ": Insights from the Hypothesis Reducer (Tool Insights Paper)"; `corpus/SOURCES.md:33`'s source cell
  abbreviates it to "Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020)".
  No cell must change.
- **Cell-change recommendation: none.** Anchor `Abstract …` still resolves; teaches still holds;
  recheck window `730d` from `2026-10-19` is not due.

## S024 — The Fuzzing Book, "Reducing Failure-Inducing Inputs"

### Fetch receipt

| field | value |
|---|---|
| URL | `https://www.fuzzingbook.org/html/Reducer.html` |
| method | `curl -sS -L -A 'Mozilla/5.0 (X11; Linux x86_64) tameshi-source-check/1.0'` |
| HTTP status | 200 |
| effective URL | same as requested |
| bytes | 496906 (`content-length: 496906`) |
| sha256 | `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99` |
| fetched (UTC) | 2026-10-26T22:15:06Z |
| HEAD (UTC) | 2026-10-26T22:16:33Z |
| `Last-Modified` | Thu, 22 Jan 2026 11:32:38 GMT |
| `ETag` | `"69720ad6-7950a"` |
| server | GitHub Pages (GitHub.com / Fastly) |

**Byte-identical to the committed round-29 snapshot** — strongest possible freshness evidence:

```
sha256sum .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html
  → 3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99  (496906 bytes)
cmp -s .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html <fetch>/s024.html  → IDENTICAL
```

The `Last-Modified` date (2026-01-22) predates the row's 2026-10-19 fetch, so the page could not have
changed between the row's opening and today.

### Anchor check — still present

Row anchor cell: `§Delta Debugging`.

- `<h2>Delta Debugging&#182;</h2>` at raw offset 297699; the next `<h2>` (`Grammar-Based Input
  Reduction`) at 332485. The 1-minimal paragraph (raw 322972) and the guarantee sentence (323188)
  fall inside that range.
- Cited section is not renamed or reordered; section order is Synopsis, Why Reducing?, Manual Input
  Reduction, Delta Debugging, Grammar-Based Input Reduction.

### Teaches cell — carried, with one wording note

Row teaches: "a runnable delta-debugging reducer: a Runner returns FAIL only on the precise error,
and the input is cut to the minimum that still reproduces it".

- "Runner returns FAIL only on the precise error" — page: "To use a Reducer, one first has to build a
  `Runner` whose outcome is FAIL if the precise error occurs. We therefore build a `ZeroDivisionRunner`
  whose `run()` method will specifically return a FAIL outcome if a `ZeroDivisionError` occurs."
  The row's "only" is a mild strengthening of "whose outcome is FAIL if the precise error occurs";
  the following sentence ("specifically … if a ZeroDivisionError occurs") supplies the exclusivity.
- "the input is cut to the minimum that still reproduces it" — page: the 1-minimal statement below.
- The reducer is runnable in the page: `class DeltaDebuggingReducer(CachingReducer)` with
  `assert self.test(inp) != Runner.PASS` and the granularity loop calling `self.test(complement) == Runner.FAIL`.

### Located passage (b) — 1-minimality / interestingness test

Primary (1-minimality guarantee), 22 words:

> This property is guaranteed by the delta debugging algorithm, which in its last stage always tries to delete characters one by one.

Interestingness-test equivalent, 20 words (§Synopsis; the page never uses the term — see drift):

> To use a Reducer, one first has to build a Runner whose outcome is FAIL if the precise error occurs.

Definition (17-word contiguous prefix; the full clause including its parenthetical is 31 words):

> Its result is 1-minimal, meaning that every character contained is required to produce the error; removing any

Full clause for context: "Its result is 1-minimal, meaning that every character contained is required
to produce the error; removing any (as seen in tests #27 and #29, above) no longer makes the test fail."

`1-minimal` is emphasized (`<em>1-minimal</em>`) and appears exactly once in the page.

### Drift

- **No content drift: zero bytes changed** versus the committed round-29 snapshot (see `cmp` above).
- **Terminology:** the phrase "interestingness test" occurs **0** times in the fetched bytes. The page
  expresses the same concept as the Runner outcome contract. This is a standing property of the page,
  not a change; the row's scope ("delta-debugging reducer practice") already matches the page's vocabulary.
- **Anchor precision:** the teaches cell draws on two sections — the Runner/FAIL sentence sits at raw
  268220, inside `§Synopsis` (h2 at 266347, next h2 `Why Reducing?` at 283651), while the 1-minimal
  clause sits in `§Delta Debugging` (297699–332485). The anchor cell names only `§Delta Debugging`,
  which does locate the 1-minimal claim the shrinker method rests on. Since the bytes are unchanged
  from the round-29 verification and the anchor still resolves the decisive claim, **no cell must change**;
  if the L1 touches the row for another reason, `§Synopsis and §Delta Debugging` would be exact.
- **Cell-change recommendation: none.**

## Findings (file:line + showing command)

1. **S022 row present and well-formed** — `corpus/SOURCES.md:33`, 11 cells, status `queued`, recheck `730d`, used-by `—`.
   `grep -n '| S022 |' corpus/SOURCES.md`.
2. **S022 anchor resolves** — `corpus/SOURCES.md:33` anchor cell "Abstract …" matches `<h2>Abstract</h2>` at raw 62383 in the fetched bytes; DOI resolves 200 to the same entity.
   `curl -sSI -L https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13`; `curl -sS -o /dev/null -w '%{http_code} %{url_effective}\n' -L https://doi.org/10.4230/LIPIcs.ECOOP.2020.13`.
3. **S022 passage (a) located, 25 words** — validity sentence in the visible abstract at raw 62551/63336.
   `python3` tag-strip + `q in txt` → `True`, `len(q.split()) == 25` (check block below).
4. **S022 has no byte baseline** — `find .ufo/evidence -iname '*S022*'` prints nothing; HEAD returns no `Last-Modified`/`ETag` and `Cache-Control: no-cache, private`. Content-level freshness only.
5. **S024 row present and well-formed** — `corpus/SOURCES.md:35`, status `mined`, used-by `corpus/knowledge/survivor-fixture-minimization.md`.
   `grep -n '| S024 |' corpus/SOURCES.md`.
6. **S024 unchanged byte-for-byte since round 29** — `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html` sha256 `3abede35…e99`, 496906 bytes, `cmp` IDENTICAL to today's fetch.
   `sha256sum .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html; cmp -s .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html <fetch>/s024.html`.
7. **S024 anchor resolves and 1-minimal sits inside it** — `<h2>Delta Debugging</h2>` raw 297699 < 322972 < next h2 332485.
   `python3` h2-offset scan over the fetched bytes.
8. **S024 passage (b) located: 22 / 20 / 17 words** — guarantee, Runner/FAIL, 1-minimal definition.
   Same check block; all `True`.
9. **"interestingness test" absent from S024** — `re.findall('interestingness', text)` → 0. The equivalent is the Runner FAIL contract; the row's teaches wording ("only on the precise error") is a mild strengthening of the page's "outcome is FAIL if the precise error occurs", backed by the next sentence on `ZeroDivisionRunner`.
10. **Registry hygiene observation (not source drift)** — `corpus/README.md:83` lists S022 among F6's sources, while `corpus/SOURCES.md:33` has `used-by` `—` (S024's used-by names its knowledge file). Whether F6's source list must appear in `used-by` is the L1's call; both rows' anchors and teaches are intact.

## Check block (reproducible)

```
python3 - <<'PY'
import re, html
def flat(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', t)
    t = re.sub(r'(?s)<[^>]+>', '', t)
    return re.sub(r'\s+', ' ', html.unescape(t))
a, b = flat('s022.html'), flat('s024.html')
quotes = [
 ('S022 validity', a, 'significantly mitigates the impact of the test-case validity problem, by ensuring that any reduced test case is one that could in principle have been generated'),
 ('S024 guarantee', b, 'This property is guaranteed by the delta debugging algorithm, which in its last stage always tries to delete characters one by one.'),
 ('S024 runner-fail', b, 'To use a Reducer, one first has to build a Runner whose outcome is FAIL if the precise error occurs.'),
 ('S024 1-minimal prefix', b, 'Its result is 1-minimal, meaning that every character contained is required to produce the error; removing any'),
]
for name, txt, q in quotes:
    print(name, len(q.split()), 'words', q in txt)
print('interestingness occurrences:', len(re.findall('interestingness', b, re.I)))
PY
→ S022 validity 25 words True
→ S024 guarantee 22 words True
→ S024 runner-fail 20 words True
→ S024 1-minimal prefix 17 words True
→ interestingness occurrences: 0
```

Fetch/verify commands actually run (already executed, receipts kept):

```
S=/fast/scratch/hyaku/tameshi-r50/T50ScribeSrcHeld
curl -sS -L -o "$S"/s022.html -w 'status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' \
  'https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13'
curl -sS -L -o "$S"/s024.html -w 'status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' \
  'https://www.fuzzingbook.org/html/Reducer.html'
sha256sum "$S"/s022.html "$S"/s024.html
curl -sSI -L <each url>            # -> headers.txt
date -u +%Y-%m-%dT%H:%M:%SZ
```

## Artifacts

Under `.ufo/waves/round-50/w1/T50ScribeSrcHeld/`:

- `s022.html` — 115315 bytes, sha256 `fa3036a3…d2d58e3`
- `s024.html` — 496906 bytes, sha256 `3abede35…8f0a65e99`
- `headers.txt` — HEAD responses for both URLs (35 lines)
- `sha256.txt` — digests of both fetches
- `provenance.json` — machine-readable record: rows, URLs, statuses, bytes, digests, UTC times, anchors, passages, verdicts
- `excerpts.txt` — the located passages with surrounding context, extracted from the fetched bytes

Scratch `/fast/scratch/hyaku/tameshi-r50/T50ScribeSrcHeld` is removed before yield; nothing citable lives there.

## Out of scope (not done, by design)

- S023 row not re-opened (the item names S022 and S024 only); `corpus/README.md:83` also lists S023 under F6.
- No claim verdict: C1/C2 counters not run; this seat reports source facts only.
- Nothing read under `/home/vgpnk/.local/state/`; no mutant names or edits quoted from
  `.ufo/evidence/round-50/control/c2-*.stdout`.
- No lane edits beyond this report and its receipts; no git/jj mutation; no tool installs needed
  (curl, python3 stdlib, sha256sum, cmp were sufficient).

## Summary

- S022 (ECOOP 2020) still valid: yes — anchor `<h2>Abstract</h2>` and all teaches clauses present in a 200/115315-byte fetch (sha256 `fa3036a3…`); no cell must change.
- S022 passage (a), 25 words: "significantly mitigates the impact of the test-case validity problem, by ensuring that any reduced test case is one that could in principle have been generated".
- S022 has no byte baseline (no committed snapshot; dynamic page, no `Last-Modified`), so its freshness is content-level only.
- S024 (Fuzzing Book Reducer) still valid: yes — fetch is byte-identical to the round-29 snapshot (sha256 `3abede35…`, `cmp` IDENTICAL).
- S024 anchor `§Delta Debugging` present at raw 297699; the 1-minimal paragraph at 322972 sits inside it.
- S024 passage (b), 22 words: "This property is guaranteed by the delta debugging algorithm, which in its last stage always tries to delete characters one by one."; Runner/FAIL equivalent 20 words.
- "interestingness test" never appears in S024; the page's vocabulary is the Runner FAIL contract, which the row's teaches cell summarizes faithfully.
- No drift requiring a SOURCES.md cell change; only unflagged observation is F6 (`corpus/README.md:83`) naming S022 while S022's `used-by` stays `—`.
