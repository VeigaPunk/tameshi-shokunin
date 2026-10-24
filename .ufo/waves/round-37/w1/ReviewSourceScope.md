# ReviewSourceScope — S104 vs official Bash 5.3 source (round 37, w1)

Verdict: the pinned official source supports the lane's bounded `$'...'` claim and
nothing more; every enum field conforms to `SOURCES-CONTRACT-v1.md`. One
citation-precision defect: the recorded line range misses the located quote by
five lines.

## Evidence

Opened the pinned bytes directly (no committed snapshot exists):

```
curl -fsSL 'https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303' -o s104-bashref.texi
# 11553 lines, 415804 bytes, sha256 f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5
```

Actual line numbers at that pin (`awk 'NR>=486 && NR<=540'`):

- L489 `@node ANSI-C Quoting` — anchor name correct.
- L490 `@subsubsection ANSI-C Quoting`; L491–492 `@cindex` lines; L493 blank.
- **L494–495** — the located quote: `Character sequences of the form
  @code{$'@var{string}'} are treated as / a special kind of single quotes.`
- L496–498 — `The sequence expands to @var{string}, with backslash-escaped
  characters in @var{string} replaced as specified by the ANSI C standard.
  Backslash escape sequences, if present, are decoded as follows:`
- Escape table L501–539 includes `\` → backslash (L518–519) and `\'` → single
  quote (L520–521).

## What the source supports — matches the claim exactly

- `$'...'` is "a special kind of single quotes" (L494–495) → tool docstring
  "scanned as single-quoted strings with backslash escapes"
  (`tools/tally-audit-v3.py:157-161`) is grounded.
- `\'` decodes to a literal single quote (L520–521) → keeping quote state open
  through an escaped single quote is grounded → fixture 1
  (`code-view/measure.py:48` `: $'it\'s' # inert st_tsu=0`) correctly treats the
  closing `'` as terminator and blanks the `#` comment per S102's word-start rule.
- A `#` inside the region is literal string content → fixture 2
  (`code-view/measure.py:52` `: $'literal # data'`) byte-identical is grounded.

## What the source does not support — and nothing claims it

- §ANSI-C Quoting says nothing about `#`/comments; comment semantics come from
  S102 (POSIX §2.3). The row's `teaches` frames only the bounded interaction.
- No support for nested `$(...)`, unquoted backslash-newline (`\newline` is
  described only as *non-quoted* behavior at L446), or full lexing — all
  explicitly held: docstring L160–161, lesson `round-37.md:23` Holds,
  SCORECARD capability row `corpus/SOURCES.md`-adjacent SCORECARD.md:1809,
  QUALITY criterion 74 (`corpus/QUALITY.md:871-879`). No unsupported claim found.

## Enum conformance (`SOURCES-CONTRACT-v1.md`, `.ufo/waves/kaika/`)

`awk -F'|'` on `corpus/SOURCES.md:113` → NF=13; `kind=docs` ∈ enum, `tier=A`
official-source justified, `status=mined` with `used-by`=
`tools/tally-audit-v3.py, corpus/lessons/round-37.md` — both files cite S104
(tool:157-158, lesson:7-8); `opened=2026-10-24` matches this review's access
date; `recheck=365d` conforms. Row count 101, `sources-census.sh validate`
exit 0 at start and end (`census/{start,end}.exit`). The W04 duplicate-URL flag
(`census/end.stdout:10`) is the same pinned `bashref.texi` shared with S097 —
disjoint sections (§Exit Status/`case` vs §ANSI-C Quoting), warning disclosed
with the census still `ok`.

## Finding (low severity)

The recorded quote range **lines 489–493** is wrong: at the pinned commit the
quote occupies **494–495**; 489–493 covers only the node heading, two `@cindex`
lines and a blank. The off-by-five propagates to the URL fragment `#L489-L493`
(`corpus/SOURCES.md:113`), the lesson Gate (`corpus/lessons/round-37.md:7`), the
LOG frontier note (`LOG.md:1983-1984`), and the round-37 append note
(`SOURCES.md:425` cites §ANSI-C Quoting without lines — that one is fine). The
quote itself is verbatim and 15 words (`wc -w` → 15); the node anchor is exact;
the pin is exact. An honest citation would read `@node ANSI-C Quoting`, lines
494–495 (or 489–498 for node-plus-sentence).

## Residual risk / gaps

- No committed snapshot and no recorded sha256 for S104 (unlike S102/S103 rows);
  the in-URL commit pin is the reproducibility anchor — same convention as S097.
- `teaches` wording "so a following `#` is not misclassified as comment text" is
  loose: a `#` at word-start *after the true closing quote* is correctly blanked
  (fixture 1); the sentence holds only when read as "a `#` still inside the
  escape-extended region."
- Could not verify that the row author opened the source on 2026-10-24 (no
  fetch receipt under `.ufo/evidence/round-37/`); date accepted as asserted.
