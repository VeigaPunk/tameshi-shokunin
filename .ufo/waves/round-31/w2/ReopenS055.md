# ReopenS055

seat: ReopenS055
rev: 2da841bd9913a2037d2bf612793382e572c9d205
base: 36c1d3933f680125aeefc447f07db0f03004901a

## Verdict

Agree that re-using S055, instead of adding a second row for the same URL, was the right call under the contract. The fresh page matches the sha256 and byte size the round-31 note cites from seat SrcDoctest, and the cited sentence is still the first common-use bullet.

Disagree that the used-by change is logged where the contract requires it. The search-log note does state the old value and the new value. `corpus/lessons/round-31.md` does not exist at this revision, so there is no round-lesson log, and the note's pointer to "the round-31 lesson Gate" does not resolve.

## Evidence

### Fresh fetch

Command, run 2026-10-23 from this seat:

```
curl -fsSL --max-time 60 -A "Mozilla/5.0 (compatible; tameshi-r31-reopen/1.0)" \
  -o /fast/scratch/hyaku/tameshi-r31-seats/ReopenS055/doctest.html \
  "https://docs.python.org/3/library/doctest.html"
wc -c /fast/scratch/hyaku/tameshi-r31-seats/ReopenS055/doctest.html
sha256sum /fast/scratch/hyaku/tameshi-r31-seats/ReopenS055/doctest.html
```

Observed:

```
216574 /fast/scratch/hyaku/tameshi-r31-seats/ReopenS055/doctest.html
369dcc17009a2f36000284ca86eedb7cef4bc10f773e554754bbdad07791cc46  .../doctest.html
```

Header fetch (`curl -sSI`, same URL and user agent):

```
HTTP/2 200
last-modified: Fri, 23 Oct 2026 07:36:14 GMT
etag: "6adb0e6e-34dfe"
content-length: 216574
date: Fri, 23 Oct 2026 09:38:35 GMT
```

`0x34dfe` is 216574, so the etag size and the saved body agree. The body is uncompressed HTML (`file`: HTML document, UTF-8). No tool was installed for this check.

The round-31 note at `corpus/SOURCES.md:368-369` (blob `bb81782ea5641b75c4a1f68f9627879cd79203cd`, identical at HEAD and at `2da841bd`) records the same fetch: 2026-10-23, 216574 bytes, sha256 `369dcc17009a2f36000284ca86eedb7cef4bc10f773e554754bbdad07791cc46`, seat SrcDoctest. This re-open agrees with that note.

### The sentence

It is the first item of the first list under the module heading, before any `h2`.

`/fast/scratch/hyaku/tameshi-r31-seats/ReopenS055/doctest.html:241-250`:

```
<section id="module-doctest">
...
<h1>...doctest... — Test interactive Python examples...
<p>The doctest module searches for pieces of text that look like interactive
Python sessions, and then executes those sessions to verify that they work
exactly as shown.  There are several common ways to use doctest:</p>
<ul class="simple">
<li><p>To check that a module’s docstrings are up-to-date by verifying that all
interactive examples still work as documented.</p></li>
```

Normalized visible text, 18 words:

`To check that a module’s docstrings are up-to-date by verifying that all interactive examples still work as documented.`

The apostrophe is U+2019, not ASCII 0x27. The only version string in the body is `3.15.1` (banner at line 206: `3.15.1 Documentation`). The S055 anchor still says `Python 3.15.0 documentation, fetched 2026-10-20` (`corpus/SOURCES.md:64`). That cell was not rewritten, which rule 2 requires. The bullet text itself is unchanged, so the stale version label does not by itself justify a superseding row.

The same sentence, with U+2019, is already in the round-16 Gate at `corpus/lessons/round-16.md:39` (mark at column 94). The knowledge entry quotes it with an ASCII apostrophe at `corpus/knowledge/executable-self-assessment.md:21-23` (0x27 at column 74 of line 21). The words match; the code point does not.

### Re-use versus a duplicate-URL row

Contract v1, `/home/vgpnk/Projects/shokunin/CORPUS.md:112-118`:

- A new row is written only after opening the source, and the round lesson Gate records URL, access date, and a quote of at most 25 words.
- Only `status`, `recheck`, and `used-by` change in place, and each change is logged old to new in the round lesson.
- A correction is a new row whose `teaches` opens `supersedes S0NN —`.

Census classification, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:24-33` and `:644-649`:

- E04: same URL and same scope, neither row rejected, and `teaches` does not match `supersedes S[0-9]{3}`. That fails validation.
- W04: same URL across different scopes. A warning only.

Diff of the S055 table line, base `36c1d393` to `2da841bd`: the only change is the used-by cell.

Old: `corpus/lessons/round-16.md`

New: `corpus/lessons/round-16.md, corpus/knowledge/executable-self-assessment.md`

`status` stays `mined`, `opened` stays `2026-10-20`, `recheck` stays `on-release`. The row still has 11 cells (`NF=13` with the empty edge fields). Both used-by paths exist at `2da841bd`: `corpus/lessons/round-16.md` and `corpus/knowledge/executable-self-assessment.md` (blob `b8bf555c4de9b8df05021e7125bece4e075b2b0e`). The knowledge entry's first line cites S055.

A second row for `https://docs.python.org/3/library/doctest.html` with the same scope, `executable documentation examples`, and no `supersedes S055` opening, would be E04. The bullet still says what S055's `teaches` says (a documented example is checked by running it and comparing with the shown output; the paragraph above the list says the module executes the sessions "to verify that they work exactly as shown"). There is no correction to record, so a superseding row is not the contract path either. Extending `used-by` in place is the path rule 2 names. The note at `corpus/SOURCES.md:372-373` states that the draft new row was not added because it would duplicate S055's URL. That decision agrees with the contract. Rows in the same note go 92 to 94 because S095 and S096 were inserted, not because S055 was copied.

### Old to new log

Logged in the search log, not in the round lesson.

`corpus/SOURCES.md:370-372`:

```
`used-by`
corpus/lessons/round-16.md → that path plus corpus/knowledge/executable-self-assessment.md;
status, opened and recheck unchanged.
```

That is an old-to-new statement, and it matches the diff. It sits in the search log. Rule 2 names the round lesson.

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -e \
  2da841bd9913a2037d2bf612793382e572c9d205:corpus/lessons/round-31.md
```

Observed: `fatal: path 'corpus/lessons/round-31.md' does not exist in '2da841bd...'`. The same absence holds at HEAD `3351738ad2e84efc30a680d97828be12adc96d88`.

The note's clause "the module-introduction bullet still reads as quoted in the round-31 lesson Gate" (`corpus/SOURCES.md:369-370`) therefore points at a file this revision does not contain. The quote that does exist is the round-16 Gate line (U+2019, matching the page) and the knowledge entry (ASCII apostrophe).

## Smallest safe correction

Do not add a duplicate-URL row, and do not edit the S055 anchor, opened date, or recheck in place.

When `corpus/lessons/round-31.md` is written, its Gate should log the mutable cells in full, the way round 20 and round 30 did: S055 `used-by` `corpus/lessons/round-16.md` to `corpus/lessons/round-16.md, corpus/knowledge/executable-self-assessment.md`; `status` `mined` to `mined`; `recheck` `on-release` to `on-release`. Until that file exists, the search-log arrow is the only log, and the "lesson Gate" clause in the note is a dangling pointer.

Optional, and separate from the row: the knowledge entry's quote at `corpus/knowledge/executable-self-assessment.md:21` uses ASCII 0x27; the page and `corpus/lessons/round-16.md:39` use U+2019. Aligning that one character would make the entry quote the page. It is not a reason to open a new source row.

No install or update was made.
