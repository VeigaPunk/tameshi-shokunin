# T54W1ScoutS277 — S277 re-opened independently

Axis: coverage. Milestone: source S277 re-opened independently.

Verdict: the page re-opens and the row's sha prefix matches, but the anchor cell does **not** describe where the TMPDIR sentence is. It names §8.1. The sentence is the `<dd>` under §8.3 Other Environment Variables.

## Re-open

Command:

```
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W1ScoutS277
curl -fsSL --max-time 60 -o /fast/scratch/hyaku/tameshi-r54/T54W1ScoutS277/V1_chap08.html \
  https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html
sha256sum /fast/scratch/hyaku/tameshi-r54/T54W1ScoutS277/V1_chap08.html
```

Output:

```
89294048dbc032eacc75804005e256eaa7eb6b5c9a2a9cf75b44d8c573d25ad7  V1_chap08.html
52350 bytes, HTML document, UTF-8
```

Second fetch (same URL, `-D` headers, separate file) was byte-identical (`cmp` equal, same sha256). Headers: `HTTP/1.1 200 OK`, `Content-Length: 52350`, `Content-Type: text/html; charset=UTF-8`, `Date: Wed, 28 Oct 2026 14:29:02 GMT`.

Snapshot (kept; the item requires it under scratch, not the lane):

- `/fast/scratch/hyaku/tameshi-r54/T54W1ScoutS277/V1_chap08.html`
- `/fast/scratch/hyaku/tameshi-r54/T54W1ScoutS277/V1_chap08.refetch.html`
- `/fast/scratch/hyaku/tameshi-r54/T54W1ScoutS277/headers.txt`

sha256: `89294048dbc032eacc75804005e256eaa7eb6b5c9a2a9cf75b44d8c573d25ad7`

## Located sentence

Only two `TMPDIR` hits in the snapshot.

1. Line 239, inside §8.1 (heading at line 31, section ends before §8.2 at line 389): a table cell `<p class="tent"><i>TMPDIR</i></p>` under the sentence "It is unwise to conflict with certain variables that are frequently exported by widely used command interpreters and applications:". Name only. No definition.
2. Lines 725–727, inside §8.3 (heading line 654: `8.3 Other Environment Variables`):

```
<dt><i>TMPDIR</i></dt>
<dd>This variable shall represent a pathname of a directory made available for programs that need a place to create temporary
files.</dd>
```

The `<dd>` is one sentence (whitespace collapsed; the source breaks after `temporary`):

> This variable shall represent a pathname of a directory made available for programs that need a place to create temporary files.

Word count: **21** (`This variable shall represent a pathname of a directory made available for programs that need a place to create temporary files`). The trailing period is attached to `files`, so stripping it does not change the count.

Headings in the same file: `8. Environment Variables` (line 30), `8.1 Environment Variable Definition` (31), `8.2 Internationalization Variables` (389), `8.3 Other Environment Variables` (654).

## Anchor cell

Row `corpus/SOURCES.md` line 152, 11 cells. Same text at C0 `59c38109bf119d0e9d4f878644a82babc937bc1e` (`git show` of `corpus/SOURCES.md`). Anchor cell, byte-exact:

`§8.1 TMPDIR paragraph @ fetched 2026-10-28 (sha256 89294048...)`

| part of the anchor | what the re-open found |
|---|---|
| `sha256 89294048...` | matches the digest above (prefix of 64 hex chars) |
| `fetched 2026-10-28` | matches this re-open (HTTP 200, 52350 B) |
| `§8.1 TMPDIR paragraph` | does **not** match. There is no TMPDIR paragraph in §8.1. The sentence is the §8.3 definition-list `<dd>` at lines 726–727 |

The anchor cell does not describe where the sentence was found. A locator that would: `§8.3 TMPDIR <dd> @ V1_chap08.html:725-727, fetched 2026-10-28 (sha256 89294048dbc032eacc75804005e256eaa7eb6b5c9a2a9cf75b44d8c573d25ad7)`.

The source cell has the same section error (`Base Definitions §8.1 Environment Variables (TMPDIR)`). Chapter 8 is titled "Environment Variables"; §8.1 is "Environment Variable Definition". Not asked as the anchor check; recorded because it is the same miss.

The teaches cell's quotation (`shall represent a pathname of a directory made available for programs that need a place to create temporary files`) is a substring of the §8.3 sentence (it drops the leading "This variable"). That quotation is about this sentence, not about the §8.1 name-table cell.
