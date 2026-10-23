# ReopenS096

seat: ReopenS096
verdict: AGREE

The S096 row at 2da841bd9913a2037d2bf612793382e572c9d205 matches a fresh fetch of https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html. The named quote is the visible text of HTML lines 181-182 under the heading on line 180. The row meets the SOURCES contract checks for this row: 11 columns, kind docs, tier A, status mined, and a used-by path that exists at that commit and cites S096.

## Fetch

Command, scratch only:

    curl -fsSL -A 'tameshi-r31-ReopenS096/1.0 (source reopen; +https://doc.rust-lang.org)' \
      -o /fast/scratch/hyaku/tameshi-r31-seats/ReopenS096/documentation-tests.html \
      -D /fast/scratch/hyaku/tameshi-r31-seats/ReopenS096/headers.txt \
      --max-time 60 \
      'https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html'
    wc -c /fast/scratch/hyaku/tameshi-r31-seats/ReopenS096/documentation-tests.html
    sha256sum /fast/scratch/hyaku/tameshi-r31-seats/ReopenS096/documentation-tests.html
    md5sum /fast/scratch/hyaku/tameshi-r31-seats/ReopenS096/documentation-tests.html

Observed:

    51137 /fast/scratch/hyaku/tameshi-r31-seats/ReopenS096/documentation-tests.html
    95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7
    ac0a34350413487a907d04e5adcae7d2

Response headers: HTTP/2 200, content-type text/html, content-length 51137, server AmazonS3, last-modified Thu, 15 Oct 2026 17:33:20 GMT, etag "ac0a34350413487a907d04e5adcae7d2", x-amz-version-id OJL1pjxq_lvL4kPf9v4GLOOXJKTiC8lj, date Fri, 23 Oct 2026 09:05:41 GMT, x-cache Hit from cloudfront, age 1942. The body MD5 equals the S3 etag. No redirect. The page title is "Documentation tests - The rustdoc book". The body has no printed rustc version or commit. Copy: /fast/scratch/hyaku/tameshi-r31-seats/ReopenS096/documentation-tests.html (773 lines, no CR).

The row anchor records the same pair: sha256 95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7 and 51,137 bytes. That is 51137.

## Quote and anchors

Row is corpus/SOURCES.md line 105 at that commit (blob bb81782ea5641b75c4a1f68f9627879cd79203cd). A split on the pipe character gives NF=13, which is 11 cells plus the leading and trailing empties. No extra pipe inside a cell. The id appears once. The URL appears once.

- id: S096
- source: Documentation tests (The rustdoc book) — https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html
- kind: docs
- tier: A
- scope: rustdoc's execution of documentation examples as tests
- anchor: §Documentation tests (#documentation-tests), HTML lines 180-182 @ page fetched 2026-10-23 (sha256 above; 51,137 bytes)
- teaches: rustdoc runs documentation examples as tests to check that they remain up to date and working
- status: mined
- opened: 2026-10-23
- recheck: on-release
- used-by: corpus/knowledge/executable-self-assessment.md

At this sha256 the lines are:

- line 180: h1 id=documentation-tests, text "Documentation tests"
- line 181: `<p><code>rustdoc</code> supports executing your documentation examples as tests.`
- line 182: `This makes sure that examples within your documentation are up to date and working.</p>`

The assigned quote is not a raw substring. The tags `<code>` and `</code>` sit around the word rustdoc, so a search for "rustdoc supports" misses. After those tags are removed, lines 181-182 are exactly:

    rustdoc supports executing your documentation examples as tests. This makes sure that examples within your documentation are up to date and working.

That is 22 words. Line 180 is only the heading. The anchor range 180-182 still contains the heading and the quote, and the anchor also names `#documentation-tests`.

teaches is a paraphrase, not the quote. Line 181 says "supports executing", not "runs". Lines 194-195 say that running `rustdoc --test foo.rs` extracts the example and then runs it as a test. Lines 210-211 say a regular doctest passes if it compiles and runs without panicking. The learner benefit is grounded. The verb "runs" is a notch stronger than "supports executing" and is carried by lines 194-195, which the anchor does not cite. That is not a column failure.

Parent 87eb64eb2b4840168d669f9125b2df28982108d5 has no S096 in corpus/SOURCES.md. Its last id line is "Next unused id: S095." This commit adds S095 and S096 and sets the next id to S097 (SOURCES.md line 377). S096 is new, not a reused id and not an in-place rewrite.

## Contract

Checked against /home/vgpnk/Projects/shokunin/CORPUS.md, section "SOURCES.md — where a shokunin learns", lines 64-109.

- Shape: id S096, source is title then canonical URL, kind docs, tier A, scope is the claim the tier covers, anchor is the section plus HTML lines plus the fetched bytes, teaches is one learner benefit, status mined, opened 2026-10-23, recheck on-release (an allowed cadence), used-by one repo-relative path.
- Tier A is the official rustdoc book for that scope. The kind is not community.
- Status mined requires a citation from the used-by path. corpus/knowledge/executable-self-assessment.md is blob b8bf555c4de9b8df05021e7125bece4e075b2b0e at this commit. It cites S096 on line 1, quotes the same 22 words at lines 27-29 under §Documentation tests with this URL, and line 70 says the append-only rule is not a claim of S096.
- Rule 1's quote, URL, and access date are the lines above. The round lesson file corpus/lessons/round-31.md is not in this commit. That file is where the round closes the gate record. It is not a false cell in S096. The same quote is already in the knowledge entry.
- No credential material. No second copy of this URL.

## Correction

None. Do not edit S096. If a later quote audit wants a raw-byte hit, record that line 181 wraps rustdoc in code tags, and that the two sentences are lines 181-182. The heading is line 180.

No tools installed. No production files edited.
