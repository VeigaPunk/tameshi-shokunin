seat: RevC1Extract

# C1 extraction false-negative audit (extract/fold on hard formats)

Scope: `.ufo/evidence/round-45/freshness/measure.py` `fold()` (lines 100–108) and
`extract()` (lines 109–127), exercised only via authorized `--extract` runs plus direct
fetches into `/tmp/tameshi-r45-RevC1Extract/`. Lane untouched except this report.
No tools installed; `pdftotext` (poppler 26.08.0, /usr/bin) already present. No pacman use.

Five formats fetched and extracted on 2026-10-25:

| target | file | --extract rc | output size |
|---|---|---|---|
| ISSTA2019.pdf | ISSTA2019.pdf (295,016 B) | 0 | 67,907 B |
| arxiv.org/abs/2102.11378 | arxiv.html (45,029 B) | 0 | 5,499 B |
| github.com/BWBama85/shmutant | github.html (323,925 B) | 0 | 15,807 B |
| npm mutation-testing-report-schema-3.9.0.tgz, member package/src/mutation-testing-report-schema.json | npm.tgz (11,872 B) | 0 | 9,153 B |
| S097 cgit bashref.texi | bashref.texi (415,804 B) | 0 | 413,378 B |

## Findings by severity

**F1 (HIGH — observed false negative): inline markup boundaries inject stray spaces.**
`extract()` line 123 `re.sub(r'(?s)<[^>]*>', ' ', text)` replaces every tag with a space,
so `<em>go red</em>.` extracts as `go red .`. Rendered README says "require that test to
go red."; extracted text says `require that test to go red . A` (gh.txt). A quote copied
from the rendered page fails `quote absent` (measure.py:151).
Command: `python3 .ufo/evidence/round-45/freshness/measure.py --extract github.html | grep -o 'go red .\{0,3\}'` → `go red . A`
Advice: the ledger quote must be copied character-exact from `--extract` output, never
from the rendered page; expect a stray space before punctuation at `</em>`/`</code>`
boundaries and quote it as printed.

**F2 (HIGH — demonstrated false-negative class): line-wrap hyphens are not rejoined.**
`fold()` removes U+00AD and collapses whitespace, but the hyphen-minus at a rendered line
break survives as `x- y`, and a soft hyphen at end-of-line becomes `x y` (two words).
Demonstrated via `--extract` on a crafted HTML file (fold-demo.html):
- `op&#x2010;\nerational` → `op‐ erational` (split)
- `intra­word` inline → `intraword` (correct; U+00AD→'' works mid-line)
- `intra­\nword` → `intra word` (split)
Ligatures are safe: NFKC (line 101) turns ﬁ→fi; demo produced `identifier finder ... fine flow of affine filters` correctly.
Observed on the real PDF: `pdftotext -enc UTF-8 ISSTA2019.pdf raw.txt && grep -cE '[a-z]-$' raw.txt` → `0`, so ISSTA2019.pdf itself has no hyphenated line breaks today; the class remains live for other PDF rows (justified two-column papers often hyphenate).
Advice: avoid quote spans containing words hyphenated at a line break; if unavoidable,
copy the `xxx- yyy` artifact verbatim from `--extract` output.

**F3 (HIGH — observed): pdftotext default reading order interleaves page furniture
mid-sentence in 2-column PDFs.** raw.txt:103-106:
```
of their bug-finding capability. Having a large number of tests in
Permission to make digital or hard copies of all or part of this work for personal or
```
The copyright block lands inside a sentence, and the abstract begins mid-sentence after
`ABSTRACT` (`ABSTRACT the test suite or having high code (statement) coverage does not
necessarily indicate...`). A natural quote reconstructed from the rendered page fails
`quote absent`; only contiguous runs of the extracted stream match.
Advice: take 6–25-token quotes from one uninterrupted `--extract` run and locate them
there before writing the ledger entry.

**F4 (MEDIUM — observed): PDF glyph mis-mapping produces mojibake punctuation.**
pdf.txt contains `ISSTA '19, July 15ś19, 2019` (en-dash → U+015B `ś`) and
`łunknownž` (guillemet-style quotes → `ł`/`ž`). Any quote containing dashes or quotation
marks from this PDF must reproduce these characters exactly.
Advice: prefer quote spans with no dash/quote punctuation; otherwise copy from the
extracted form.

**F5 (MEDIUM — observed): HTTP error pages extract cleanly and would self-verify.**
First fetch of the S097 URL returned a 1,114-byte `502 Bad Gateway` HTML page (Savannah
AI-scraping overload message, "The service is unavailable..."). Its text extracts
normally, and `grade()` (measure.py:132-167) hashes raw bytes and locates the quote in
those same bytes — a ledger built on an error-page snapshot is internally consistent but
verifies the wrong content. No origin-integrity guard exists in the counter.
Retry with backoff succeeded:
`curl -sL --retry 3 --retry-delay 15 --retry-all-errors -o bashref.texi 'https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303'`
→ 415,804 bytes, `sha256sum` → `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`,
byte-identical to the sha recorded in S097's anchor (corpus/SOURCES.md:106). URL healthy.
Advice: before snapshotting, sanity-check bytes against the row's recorded size/sha
(texinfo must start `\input texinfo.tex`); refetch on mismatch.

**F6 (MEDIUM — demonstrated): HTML-detection false positive strips angle-bracket spans
from plain text.** Any file containing literal `<html|body|div|p|head\b` triggers
tag-stripping of the whole file (line 120-123), and `<[^>]*>` deleted `< 3 and y >` from
`if x < 3 and y > 2 then run.` in the demo → `if x 2 then run.`. bashref.texi is safe
today (`grep -c '<p>\|<p \|<html\|<div\|<body\|<head' bashref.texi` → `0`), but raw
source-code snapshots (C comparisons, Java generics) or .md files with inline HTML would
lose spans.
Advice: for code-bearing rows, confirm the chosen sentence survives verbatim in
`--extract` output; avoid spans containing `<`/`>`.

**F7 (LOW): JSON member escapes stay raw.** In the schema member, `\\` and `\"` remain
literal (6 `\"` runs; no `\uXXXX` present); `fold()` decodes no JSON escapes, so a
description like `It is a best practice to \"...\"` can only be quoted with its
backslashes as printed. Clean ≥6-token quote candidates that extract intact include
`Position of a mutation. Both line and column start at one.` and
`A location with start and end. Start is inclusive, end is exclusive.`
Advice: quote plain description strings; never quote across escape runs.

**F8 (INFO — clean formats).** arXiv abs page: abstract contiguous and intact
(`Mutation analysis assesses a test suite's adequacy by measuring its ability to detect
small artificial faults, systematically seeded into the tested program.`), diacritics
preserved (Petrović); avoid the PDF-link alt text containing raw LaTeX `Petrovi\'c`.
Texinfo: `@code{waitpid}`, `@sc{posix}`, `128+@var{n}` survive verbatim — quotes must
carry the @-markup exactly as extracted; a retyped `128+n` fails. Exit Status content
confirmed present in texi.txt.

## Quote-selection advice for row executors (condensed)

1. Copy the 6–25-token quote from `measure.py --extract <snapshot> [--member M]` output,
   contiguous and character-exact; never retype from a rendered page or PDF viewer.
2. The quote must not be a substring of `fold(source+scope+anchor+teaches)` lowercased
   (measure.py:153-154) — don't echo the row's own cells.
3. Ensure ≥2 shared content words with scope/anchor/teaches; `words()` = `[a-z0-9]+`,
   length ≥ 4, minus STOP (measure.py:65, 128-130).
4. PDFs: no dashes/quotes in the span when possible; no hyphenated line breaks; verify
   contiguity (copyright blocks interleave); tolerate ś/ł/ž mojibake only when copied.
5. HTML: keep inline-markup-boundary artifacts (`go red .`) as printed.
6. JSON members: quote plain description strings only.
7. Texinfo: include @-markup verbatim.
8. Before writing a snapshot: check byte size / head bytes against the row's recorded
   sha/size; 502 pages extract cleanly (F5).

## Residual risk / verification gaps

- grade() has no origin-integrity check beyond byte equality (F5): a self-consistent
  error-page ledger would count as fresh; only executor discipline catches it.
- Other PDFs in the held rows were not fetched here; hyphenation and mojibake behavior
  is per-file (poppler 26.08.0 measured one representative ACM paper).
- `--extract` on a gzip-named snapshot decompresses by `.gz` suffix (measure.py:418-421),
  same as load_snapshot (168-180); ledger sha256 is over decompressed bytes on both
  paths — consistent, not independently exercised end-to-end here.
