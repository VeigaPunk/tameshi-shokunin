# Reopen S052 — Supported mutators (Stryker Mutator docs)

Seat: `ReopenS052`, round 16 wave 2 (falsify).
Target: registry row `corpus/SOURCES.md:61` and its Gate quote
`corpus/lessons/round-16.md:33`, both read at lane commit
`c699c8c36d6e4eca4b796b81a8247904aa145ec8` (`rev-parse HEAD` = that commit).
Attacked: quote exactness, ≤25-word bound, stated location, anchor resolvability,
kind, tier, scope, teaches, used-by existence and citation. Source re-opened
2026-10-20.

**One-line verdict: holds** — every enumerated field checks out against the live
page and the committed bytes; one non-blocking calibration caveat on the Gate
quote's grounding role (below).

## Method and evidence

### 1. Source re-opened

```
$ curl -sS -L --max-time 60 -o /tmp/s052.html \
    -w '%{http_code} %{size_download} %{url_effective}\n' \
    'https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/'
200 47923 https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/
exit 0
$ sha256sum /tmp/s052.html
fbbac72439fc5d5194bc76bca6b1826a25b86ed6fe1b1cedb843c7046c0fe98b
$ curl -sSI <same URL> | grep -iE '^(HTTP/|date:|last-modified:)'
HTTP/2 200
date: Tue, 20 Oct 2026 13:51:57 GMT
last-modified: Mon, 19 Oct 2026 18:02:59 GMT
```

A second HEAD at 13:54:07 GMT returned `last-modified: Mon, 19 Oct 2026 18:02:58 GMT`
(one second lower across two Cloudflare edges; same date). The row's
`last-modified 2026-10-19` is correct.

### 2. Quote: exact, 16 words, sentence 2

The page's first `<p>` after `<h1>Supported mutators</h1>`:

> All Stryker versions support a variety of different mutators. We've aligned on a
> standard naming scheme so it is easy to switch and compare implementations. The
> difference in support is listed below.

Extraction (Python, `html.unescape` of that `<p>`; exit 0):

```
lesson row: | S052 | https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ | 2026-10-20 | "We've aligned on a standard naming scheme so it is easy to switch and compare implementations." (§Supported mutators, opening paragraph, sentence 2) |
extracted quote: "We've aligned on a standard naming scheme so it is easy to switch and compare implementations."
quote exact in opening paragraph: True
quote words (split): 16
quote words (wc): 16
sentence1: All Stryker versions support a variety of different mutators.
sentence2: We've aligned on a standard naming scheme so it is easy to switch and compare implementations.
bytes of apostrophe in page: 0x27
```

The lesson quote uses U+0027 (`We've`), matching the page byte-for-byte. There is
no second `S052` quote row; `corpus/lessons/round-16.md:33` is the only Gate quote
for this row.

### 3. Anchor resolution and revision

```
h1 'Supported mutators'          # first heading on the page
h2 'Support'  (id=support)       # table follows in this section
table header: ['Mutator', 'StrykerJS', 'Stryker.NET', 'Stryker4s']
Docusaurus v3.10.2               # HTML body contains this literal
edit link: github.com/stryker-mutator/mutation-testing-elements/edit/master/docs/supported-mutators.md
40-hex tokens in HTML: 0          # no commit pin exposed
docsearch:version = current
```

- `§Supported mutators opening paragraph` resolves to the `<p>` above (byte-identical
  to the meta/og description).
- `§Support table` resolves to the h2 `Support` (the literal heading is `Support`,
  not `Support table`) and the single 4-column table beneath it. Naming is one word
  loose; location is unambiguous. Non-blocking.
- `Docusaurus build` verified as v3.10.2; `no commit pin exposed` verified: no
  40-hex token in the document, and the only source link is `/edit/master/...`.

### 4. `teaches` checked against the table

Full support row values (`Mutator | StrykerJS | Stryker.NET | Stryker4s`):

```
Arithmetic Operator   ✅ ✅ ❌      Assignment Expression ❌ ✅ n/a
Array Declaration     ✅ ✅ ❌      Block Statement       ✅ ✅ ❌
Boolean Literal       ✅ ✅ ✅      Checked Statement     n/a ✅ n/a
Conditional Expression✅ ✅ ✅      Equality Operator     ✅ ✅ ✅
Logical Operator      ✅ ✅ ✅      Method Expression     ✅ ✅ ✅
Object literal        ✅ n/a n/a    Optional chaining     ✅ ❌ n/a
Regex                 ✅ ✅ ✅      String Literal        ✅ ✅ ✅
Unary Operator        ✅ ✅ ❌      Update Operator       ✅ ✅ n/a
```

So: equality, conditional, string literal, boolean literal and array declaration
are all supported by StrykerJS; `Assignment Expression` is the **only** ❌ in the
StrykerJS column. Programmatic recount over the 16 body rows (header located by
`hdr.index('StrykerJS')`): `{'✅': 14, '❌': 1, 'n/a': 1}`, with the five named rows
returning `✅` and `Assignment Expression` returning `❌`. The per-operator
sections use JS/TS examples (`var`, `new Array(1,2,3,4)`, template literals), which
supports the `JS mutant selection` scope.

### 5. Registry row shape, tier, status, used-by

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print "malformed:", n+0}' SOURCES.md
malformed: 0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' SOURCES.md
55
$ grep -c '^| S052 ' SOURCES.md
1
$ awk -F'|' '...S052...' SOURCES.md
tier= A   status= mined   opened= 2026-10-20   recheck= 180d   used-by= corpus/knowledge/mutation-case-kumitate-round-gate.md
```

No duplicate ids (`sort | uniq -c` produced no `DUP` line). Row sha256
`d1d4d42980fe9f5aa0c956812c584161e969b0c8afbf75757ba171845c2245c6`
(committed line 61, trailing newline stripped). Footer says `Next unused id: S058`,
consistent with S052–S057 being this round's rows.

Contract checks (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`,
read-only; `nl` lines):

- `:26-28` tier A = "primary or authoritative for that scope (spec, official docs,
  source code, original paper, maintainer statement, the lane's own re-runnable
  gate output)" → official Stryker docs fit.
- `:24-25` `docs` is an enumerated kind.
- `:32-33` anchor = section/heading plus revision (version, commit, or publication
  date) → sections + Last-Modified date + Docusaurus version satisfy the "or" clause.
- `:36` `mined` = "cited by ≥1 path in `used-by`" → satisfied.
- `:45-48` rule 1: Gate records URL, access date, ≤25-word quote with location.
  The row's access date `2026-10-20` equals the lesson's `Accessed` column and
  today's fetch date.

`used-by` path exists at the commit and actually cites S052:

```
$ git cat-file -e c699c8c...:corpus/knowledge/mutation-case-kumitate-round-gate.md && echo EXISTS
EXISTS
$ git show c699c8c...:corpus/knowledge/mutation-case-kumitate-round-gate.md | grep -n S052
1:source: S053 ... ; S052 Stryker supported mutators; S056 PIT mutators; S057 ...
41:(`.ufo/waves/round-16/w1/RGSpec{A,B,C,E}.spec`). Operator families follow S052
```

Line 41 continues: `(string literal, equality/boundary, array declaration, conditional)` —
the citation names the operator families the row teaches, not a bare id mention.
The round-16 search log also records the page as opened and included
(`corpus/SOURCES.md:143-147`: "Opened Stryker supported-mutators, PIT mutators, ...
identified6/screened6/included6/excluded0").

### 6. Scope of my reads / contamination note

- Lane HEAD is exactly `c699c8c...`. Working tree has unrelated modifications
  from other seats (`git --no-optional-locks status --porcelain` shows
  `M .ufo/evidence/round-16/measure.py`, `M .ufo/waves/round-16/w1/Overlap1.md`,
  `M corpus/lessons/round-16.md`, plus untracked wave-2 files); every lane read
  above used `git show c699c8c...:<path>`, and the S052 lesson row is unchanged
  in the working-tree diff. No lane file was modified by this seat other than this
  report.
- Contract file is not at `corpus/SOURCES-CONTRACT-v1.md` (the bare name in
  `corpus/SOURCES.md:4`): `git show c699c8c...:corpus/SOURCES-CONTRACT-v1.md`
  exits 128. The frozen copy is `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, which I
  used. This is pre-existing lane doc drift (already recorded in earlier rounds),
  not an S052 defect.
- No tools installed or upgraded; no pacman transaction attempted.

## Field verdicts

| field | observed | verdict |
|---|---|---|
| Gate URL = row URL | identical absolute URL; HTTP 200 | holds |
| Quote exact | exact substring of the opening `<p>`; U+0027 matches | holds |
| Quote ≤25 words | 16 words (`split` and `wc`) | holds |
| Stated location | first `<p>` after h1 `Supported mutators`; quote is sentence 2 | holds |
| Anchor resolvable | h1 + first paragraph; h2 `Support` (id=support) + single table; v3.10.2; Last-Modified 2026-10-19; no commit pin (0 × 40-hex, `/edit/master/` link only) | holds (one-word heading naming note: `Support`, not `Support table`) |
| kind = docs | official documentation page | holds |
| tier = A | official docs for its own operator set; contract `:26-28` | holds |
| scope | StrykerJS column + JS/TS-coded operator tables; single-edit mutant entries | holds |
| teaches | five named families all ✅ for StrykerJS; Assignment Expression the only ❌ | holds |
| used-by exists | `corpus/knowledge/mutation-case-kumitate-round-gate.md` at c699 | holds |
| used-by cites S052 | `:1` and `:41` (operator families named) | holds |
| status = mined / row shape | NF=13; unique S052; no duplicate ids; footer S058 | holds |
| opened/accessed date | row `2026-10-20`; lesson `2026-10-20`; page fetched 2026-10-20 | holds |

## Calibration note (non-blocking)

The Gate quote is the page's generic *naming-scheme* sentence. It does not itself
name the operator families or the assignment-expression non-support; that content is
in §Support table, which the **row's anchor** names (`§Supported mutators opening
paragraph and §Support table`, `corpus/SOURCES.md:61`), but the **Gate location** does
not (`§Supported mutators, opening paragraph, sentence 2`,
`corpus/lessons/round-16.md:33`). Under the
strict reading of contract rule 1 ("a ≤25-word quote with its location grounding
`teaches`", `:45-48`), a sentence from the support table would ground the claim more
directly. The quote is exact, in place and within the word bound, and `teaches` is
factually correct, so this is a calibration weakness in quote selection, not a
failed field or an incorrect row.

## Remaining unknowns

- No commit pin exists for this docs site, so the exact page revision cannot be
  independently re-derived beyond HTTP Last-Modified 2026-10-19 18:02:5x GMT and
  the captured HTML sha256 `fbbac724...0fe98b`. A future page change (same
  Last-Modified precision) would need a re-fetch; `recheck: 180d` is the row's
  mitigation, and it is a permitted cadence (contract `:38-39`).
- Whether the support table's second column was `StrykerJS` at row-writing time is
  only checkable through the same undated page; current bytes and the row agree.

**Verdict: holds** for all attacked fields (quote, location, length, anchor,
kind/tier/scope/teaches, used-by), with one minor quote-selection calibration
caveat recorded above.
