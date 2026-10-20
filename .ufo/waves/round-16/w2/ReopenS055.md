# ReopenS055 — re-open source S055 (Python `doctest`)

Seat: `TameshiR16.ReopenS055` (scout, leaf; no dispatch, no background jobs).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, commit
`c699c8c36d6e4eca4b796b81a8247904aa145ec8` (`git rev-parse HEAD`; `git log -1`:
`round-16: land js-round-gate case 7, cold-read repairs, sources S052-S057,
attribution repair`).
Target: S055's registry row (`corpus/SOURCES.md:64`), its Gate quote
(`corpus/lessons/round-16.md:36`), and the fields the row claims.

**Verdict: holds.** Quote is byte-exact, 18 words, at the first bullet it names;
anchor resolves; kind/tier/scope/teaches are defensible; the one `used-by` path
exists and cites S055. Three calibration notes (C1–C3 below) do not falsify a field.

## Source bytes actually examined

```
curl -sS -L --max-time 30 https://docs.python.org/3/library/doctest.html -o /tmp/doctest-r16w2.html
exit=0   216574 bytes   sha256 2a999bfddb350147ae80d352b6f090fbad076fc35dce667d2088b9f7d98d15a1
<title>doctest — Test interactive Python examples — Python 3.15.0 documentation</title>
<link rel="canonical" href="https://docs.python.org/3/library/doctest.html">
```

```
curl -sSI same URL -> HTTP/2 200; last-modified: Tue, 20 Oct 2026 13:45:59 GMT;
etag: "6ad77097-34dfe"; date: Tue, 20 Oct 2026 13:53:54 GMT
```

Committed rows were read with `git show <rev>:<path>` into
`/tmp/tameshi-r16w2-ReopenS055/` (working-tree `corpus/lessons/round-16.md` is
dirty from another seat; see "Working-tree note").

```
git show <rev>:corpus/SOURCES.md | grep -n S055        -> 64
git show <rev>:corpus/lessons/round-16.md | grep -n S055 -> 36 (single occurrence)
git grep -n S055 <rev> -- .                            -> exactly 2 hits: SOURCES.md:64, lessons:36
```

## Gate quote check (`corpus/lessons/round-16.md:36`)

Recorded: `"To check that a module’s docstrings are up-to-date by verifying that
all interactive examples still work as documented." (module introduction, first bullet)`

Extracted the first `<li>` of the `<ul class="simple">` that follows
`There are several common ways to use doctest:</p>` (raw HTML at
`/tmp/doctest-r16w2.html`):

```
raw: 'To check that a module’s docstrings are up-to-date by verifying that all\ninteractive examples still work as documented.'
normalized: 'To check that a module’s docstrings are up-to-date by verifying that all interactive examples still work as documented.'
byte_equal(lesson_quote, normalized_page_text): True
words: 18 (<= 25)
non_ascii in quote: U+2019 only; nbsp False; no ellipsis; sentence not truncated
```

| Gate criterion (rule 1, contract:45–47) | Observed | Verdict |
|---|---|---|
| quote exact | byte-equal after collapsing the HTML source line-wrap between "all" and "interactive"; curly apostrophe U+2019 preserved | holds |
| ≤25 words | 18 | holds |
| stated location | structurally the **first** `<li>` of the module-introduction list; the string `up-to-date` occurs exactly once in the page (`grep -c` = 1) | holds |
| URL | `https://docs.python.org/3/library/doctest.html`; HTTP 200; canonical link identical | holds |
| access date | `2026-10-20`, same as row `opened` | holds |

`id="module-doctest"` is present, so the "module introduction" anchor resolves.

## Field-by-field (row `corpus/SOURCES.md:64`, NF=13)

| Field | Value | Verdict | Evidence |
|---|---|---|---|
| `id` | S055 | holds | no duplicate ids (census `uniq -d` empty); `SOURCES.md:177–180` allocates S052–S057 to round 16 and states next unused S058; no S058 row |
| `source` | doctest — Test interactive Python examples — URL | holds | page `<title>` matches title fragment; URL canonical per `<link rel=canonical>`; HTTP 200 |
| `kind` | `docs` | holds | enum-valid (contract:24–25); it is the official Python library reference page |
| `tier` | `A` | holds | contract:26–29 names "official docs" as A; grade is scoped, not global |
| `scope` | executable documentation examples | holds | contract:31 allows a topic; correctly narrows the A grade to doctest's domain, not Python at large |
| `anchor` | module introduction, first bullet @ Python 3.15.0 documentation, fetched 2026-10-20 | holds | heading + bullet ordinal + version (page title says 3.15.0, 4 occurrences) + date; `id="module-doctest"` exists; contract:32–33 requires section/heading/line + revision (version allowed) |
| `teaches` | a documented example is a checkable claim: run it as written and compare with the shown output | holds | quoted bullet grounds the "checkable claim" half; the adjacent intro sentence — "The doctest module searches for pieces of text that look like interactive Python sessions, and then executes those sessions to verify that they work exactly as shown." — grounds "compare with the shown output" (same module introduction) |
| `status` | `mined` | holds (literal) | contract:36 defines mined as cited by ≥1 `used-by` path; `corpus/lessons/round-16.md:36` cites S055. See C3 |
| `opened` | 2026-10-20 | holds | equals Gate access date; page reachable and quote present at today's bytes |
| `recheck` | `on-release` | holds | allowed cadence (contract:38–39); apt for `docs.python.org/3`, which retitles per release. See C2 |
| `used-by` | `corpus/lessons/round-16.md` | holds | path exists at the commit; cites S055 at line 36; repo-wide `git grep S055` finds no other citation |

Contract census on the committed bytes (run in `/tmp` copy, paths checked against
the lane root; contract:60–70):

```
rows: 55
malformed (NF!=13): 0
tier: A=47 B=6 C=2
status: mined=28 queued=24 rejected=3
dup ids: (none)
enum violations / tier inflation: (none)
mined rows whose used-by paths do not exist: (none; census exit 0)
```

## Calibration notes (observations, not falsifications)

- **C1 — `teaches` fuses two adjacent sentences of the intro.** The recorded
  quote says examples "work as documented"; the wording "compare with the shown
  output" comes from the sentence immediately above the bullet list ("verify that
  they work exactly as shown"). Same section/heading, so rule 1's location still
  grounds `teaches`; a purist would quote that sentence instead for the second
  clause. No field falls.
- **C2 — anchor has no immutable artifact identity.** Revision is the title-level
  version label `Python 3.15.0` plus the fetch date; unlike S053 (blob sha256),
  S054 (`Last-Modified 2026-08-06`) and S056 (sha256), no digest/Last-Modified is
  pinned. The live page's `Last-Modified` is **2026-10-20 13:45:59 GMT** (today),
  so `/3/library/doctest.html` is a moving target that can change under a fixed
  "3.15.0" label; `on-release` catches release retitling, not daily drift. The
  contract explicitly permits "version" (contract:32–33), so the field holds;
  this is a calibration/robustness point for the registry, not a row defect.
- **C3 — `mined` rests on the Gate table's own citation.** S055's only citation in
  the repo is the sources-opened row at `corpus/lessons/round-16.md:36`; no
  `corpus/knowledge/` entry cites S055 and the lesson body makes no claim that
  rests on doctest. Contract rule 1 obliges the lesson to record every new row,
  so this reading makes `mined` automatic for every new row (the round itself
  states the convention at `round-16.md:40–41`). Literal contract satisfied;
  systemic registry semantics, not an S055 field failure.

Search-log support (rule 5, adjacent): `corpus/SOURCES.md:141–148` records the
round-16 opening list including "Python doctest" with
`identified6/screened6/included6/excluded0`.

## Working-tree note

`git --no-optional-locks status --porcelain` shows `M corpus/lessons/round-16.md`;
`git diff --stat c699c8c -- corpus/SOURCES.md corpus/lessons/round-16.md` is
`1 file changed, 1 insertion(+)`, an unrelated appended defect row near line 54,
not the S055 row. All quoted bytes above come from the commit via `git show`.
No lane file was edited; the only lane write is this report.

Installs/upgrades: none (no tooling change needed or recorded).

## One-line verdict

**HOLDS** — S055's Gate quote is byte-exact and 18 words at the stated first
bullet, its anchor resolves at Python 3.15.0 docs, kind/tier/scope/teaches are
justified, and its `used-by` path exists and cites S055; C1–C3 are calibration
notes only.
