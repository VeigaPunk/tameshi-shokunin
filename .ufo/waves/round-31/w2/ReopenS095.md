# ReopenS095

seat: ReopenS095
verdict: AGREE

The S095 row at 2da841bd9913a2037d2bf612793382e572c9d205 matches a fresh fetch of https://go.dev/blog/examples. The named quote is in the Output comments section. The cited HTML spans are the sections the row names. The row meets the named SOURCES contract checks: 11 columns, tier A for docs, status mined with an existing used-by path that cites S095.

## Fetch

Command, scratch only:

    curl -fsSL --retry 3 --retry-delay 1 -A 'tameshi-r31-ReopenS095/1.0' \
      -o /fast/scratch/hyaku/tameshi-r31-seats/ReopenS095/examples.html \
      -D /fast/scratch/hyaku/tameshi-r31-seats/ReopenS095/examples.headers \
      -w 'http_code=%{http_code} size_download=%{size_download} content_type=%{content_type} url_effective=%{url_effective}\n' \
      'https://go.dev/blog/examples'
    sha256sum /fast/scratch/hyaku/tameshi-r31-seats/ReopenS095/examples.html
    wc -c /fast/scratch/hyaku/tameshi-r31-seats/ReopenS095/examples.html

Observed: HTTP/2 200, content-type text/html; charset=utf-8, date Fri, 23 Oct 2026 09:38:04 GMT, url_effective https://go.dev/blog/examples, size_download 40059.

    1a40ae77c967d7e203b8d7706784bd6633542ff3583d197d854755233c958178
    40059

The row anchor records the same pair: 40059 bytes and SHA-256 1a40ae77c967d7e203b8d7706784bd6633542ff3583d197d854755233c958178. Copy: /fast/scratch/hyaku/tameshi-r31-seats/ReopenS095/examples.html.

## Quote and anchors

Row is corpus/SOURCES.md line 104 at that commit. A split on the pipe character gives NF=13, which is 11 cells plus the leading and trailing empties. No extra pipe inside a cell.

- id: S095
- source: Testable Examples in Go (Andrew Gerrand) — https://go.dev/blog/examples
- kind: docs
- tier: A
- scope: the Go blog's documented behavior of package examples, including output-comment verification
- anchor: Introduction, Examples are tests, and Output comments; HTML lines 462-467, 473-479, 512-519; article published 2015-05-07; fetched 2026-10-23 UTC; 40059 bytes; the SHA-256 above
- teaches: Go examples appear in documentation and are compiled or run as tests; with an Output comment, the test passes only when captured standard output matches the comment
- status: mined
- opened: 2026-10-23
- recheck: 180d
- used-by: corpus/knowledge/executable-self-assessment.md

Headings in the fetch:

- line 461: h2 id=introduction, Introduction
- line 473: h2 id=examples-are-tests, Examples are tests
- line 512: h2 id=output-comments, Output comments

Lines 462-467 open Introduction: examples are displayed as package documentation and verified by running them as tests.

Lines 473-479 are Examples are tests: compiled and optionally executed; example functions take no arguments and begin with Example.

Lines 512-519 are Output comments. Line 517 is the pass sentence.

The assigned sentence is not a byte-identical substring. Line 517 reads: The test passes if the test&rsquo;s output matches its output comment.

Unescaped, that apostrophe is U+2019 RIGHT SINGLE QUOTATION MARK, not U+0027. An ASCII-apostrophe search returns no hit. The words are the same sentence, in Output comments, inside the cited span 512-519.

The byline is HTML line 457, "7 May 2015", not the literal token 2015-05-07. That ISO date is the same calendar day and sits outside the cited line spans. Author line 456 is Andrew Gerrand. Title line 453 is Testable Examples in Go.

teaches tracks those spans: documentation display (line 463), compiled or run as tests (lines 463-464 and 474; the word "or" keeps the page's "optionally executed"), and a pass when captured standard output matches the Output comment (lines 514-517). The phrase "only when" is a notch stronger than the page's "if". Lines 518-533 show a mismatched comment failing. That is not a column failure.

## Contract

Checked against /home/vgpnk/Projects/shokunin/CORPUS.md, section "SOURCES.md — where a shokunin learns", lines 64-109, limited to the named checks.

- 11 columns. kind is docs and status is mined, both in the frozen enums.
- Tier A is scoped to what this official Go Blog post documents, not to a measured compiler boundary. docs may be A. The kind is not community.
- Status mined names corpus/knowledge/executable-self-assessment.md. That path is blob b8bf555c4de9b8df05021e7125bece4e075b2b0e in commit 2da841bd9913a2037d2bf612793382e572c9d205 (git ls-tree) and the file exists on disk. It cites S095 at line 1 (source), lines 24-25 (the quote, under Output comments, with the URL), and line 70 (explicitly not a claim of S095). The worktree copy at HEAD 3351738ad2e84efc30a680d97828be12adc96d88 still has those three citations.

## Correction

None for the named checks. If a later quote audit wants byte identity, record the page apostrophe as the HTML entity rsquo (U+2019) at HTML line 517, and the byline as "7 May 2015" at line 457. The knowledge entry already normalizes the apostrophe to ASCII.

No tools installed. No production files edited.