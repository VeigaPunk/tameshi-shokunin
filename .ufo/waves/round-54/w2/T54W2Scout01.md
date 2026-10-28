# T54W2Scout01 — re-open S277, S278, S279 at C1

Seat: scout. Revision: `99c3bc88d704566197783f66b211ee0a830e0330` (C1).
Worktree and `HEAD` (`097985c18b9a186c310bd35890b95b733cbb7f5b`) have an empty diff against C1 for `corpus/SOURCES.md`, `corpus/knowledge/scratch-root-contract.md`, `corpus/lessons/round-54.md`, and `.ufo/evidence/round-54/assimilation/`. The bytes below are the C1 bytes.

The admitted note is `corpus/knowledge/scratch-root-contract.md`. The opening record that states the sizes, word counts, and section numbers is `corpus/lessons/round-54.md`.

## Verdict

Row sha prefixes match the committed snapshots and the live URLs, which are byte-identical to those snapshots on this re-open. S278's `:163-165` and S279's `tempfile.gettempdir` resolve. S277's `§8.1` does not: the quoted sentence is the §8.3 definition. The note's citation ids (S277, S278, S279) and the `:163-165` number match the rows. Three drifts remain: the §8.1 locator, a semicolon the S278 quote inserts, and lesson numbers (word counts; text-extract size paired with the raw-file sha).

## What matches

| id | row sha prefix | snapshot sha256 | bytes | live vs snapshot |
|---|---|---|---|---|
| S277 | `89294048...` | `89294048dbc032eacc75804005e256eaa7eb6b5c9a2a9cf75b44d8c573d25ad7` | 52350 | `cmp` exit 0, HTTP/1.1 200, `Content-Length: 52350` |
| S278 | `fb44155f...` | `fb44155f430fac1923d3d7b6af1a0210edcfb580291d664e66f338491d68b62b` | 32236 | `cmp` exit 0, HTTP/2 200, `content-length: 32236` |
| S279 | `6b0edccf...` | `6b0edccf2e7f94fd574632a7ef445c7e0852ac0a362a7bfaed3aaf6b6b8ef7ba` | 75190 | `cmp` exit 0, HTTP/2 200, `content-length: 75190`, `last-modified: Wed, 28 Oct 2026 12:45:58 GMT` |

C1 git blobs equal the worktree blobs (`git rev-parse C1:path` = `git hash-object` of each snapshot).

S278 lines 163–165 of `S278-tempfile.py` are exactly:

```
    for envname in 'TMPDIR', 'TEMP', 'TMP':
        dirname = _os.getenv(envname)
        if dirname: dirlist.append(dirname)
```

`_candidate_tempdir_list` is defined at line 156. The row anchor `` `_candidate_tempdir_list` :163-165 `` and the note's `(S278 `_candidate_tempdir_list`:163-165)` name that span. The lesson quote `if dirname: dirlist.append(dirname)` is a substring of line 165.

S279 anchor `§tempfile.gettempdir` is `id="tempfile.gettempdir"` at snapshot line 502. Rendered text of that section is: "The list is:" then "The directory named by the TMPDIR environment variable." then TEMP, then TMP, then "A platform-specific location:", then "As a last resort, the current working directory." The row's "then TEMP, TMP and platform locations" matches that order. The note's phrase "the directory named by the TMPDIR environment variable" (S279) is that first item.

S277's quoted words, under whitespace folding, are the §8.3 `<dd>` at lines 726–727: `This variable shall represent a pathname of a directory made available for programs that need a place to create temporary files.` The raw file breaks the sentence as `temporary\nfiles.`, so the space-joined form is not a contiguous byte substring; the folded form is. The note cites that sentence as (S277) and does not repeat `§8.1`.

Note citation ids, and only those, for this set: S278 (empty arm, and again with `:163-165`), S279 (list starts at TMPDIR and falls through), S277 (the standard fixes meaning, not empty-string handling). Same three numbers as the rows. The note does not cite a different line range.

## Drift

### 1. S277 anchor says §8.1; the sentence is in §8.3

Row source cell: `POSIX.1-2024, Base Definitions §8.1 Environment Variables (TMPDIR)`.
Row anchor: `§8.1 TMPDIR paragraph @ fetched 2026-10-28 (sha256 89294048...)`.
Lesson: `Located quote (21 words, §8.1 TMPDIR paragraph)`.

Snapshot headings:

- line 30, `tag_08`: `8. Environment Variables`
- line 31, `tag_08_01`: `8.1 Environment Variable Definition` (through the next heading at line 389)
- line 389, `tag_08_02`: `8.2 Internationalization Variables`
- line 654, `tag_08_03`: `8.3 Other Environment Variables`
- lines 725–727: `<dt><i>TMPDIR</i></dt>` / `<dd>This variable shall represent a pathname of a directory made available for programs that need a place to create temporary` / `files.</dd>`

The folded quote occurs once, inside the §8.3 slice (`id="tag_08_03"` onward), and zero times inside §8.1 (`tag_08_01` up to `tag_08_02`). §8.1's only `TMPDIR` is the name in the "frequently exported" table at line 239 (`<p class="tent"><i>TMPDIR</i></p>`), not a definition paragraph. Chapter 8 is titled "Environment Variables"; §8.1 is titled "Environment Variable Definition".

### 2. S278 row and note quotes insert a semicolon the file does not have

Row teaches cell and note both quote:

`for envname in 'TMPDIR', 'TEMP', 'TMP': dirname = _os.getenv(envname); if dirname: dirlist.append(dirname)`

That string is not in `S278-tempfile.py` (`in file` is false). Space-joining the stripped lines 163–165 produces:

`for envname in 'TMPDIR', 'TEMP', 'TMP': dirname = _os.getenv(envname) if dirname: dirlist.append(dirname)`

No semicolon. The three statements are the cited lines; the quote is not those bytes. The anchor numbers themselves match.

### 3. S279 teaches cell says "missing or empty"; the page has neither word

Row teaches: `"The list is: The directory named by the TMPDIR environment variable" then TEMP, TMP and platform locations — the documented order a missing or empty TMPDIR falls through`.

Case-sensitive and case-folded counts of `empty`, `missing`, `unset`, and `null` in `S279-tempfile-docs.html` are all 0, including inside the `tempfile.gettempdir` section (it ends at `tempfile.gettempdirb`). The rendered list does not say an empty or missing `TMPDIR` is skipped. That skip is line 165 of S278 (`if dirname:`), which the note attributes to S278, not to S279. The note's S279 citation (list order) matches the page; the row's "missing or empty" clause does not.

The combined string `The list is: The directory named by the TMPDIR environment variable` is not a contiguous substring (tags sit between `the` and `TMPDIR`: `<span class="target" id="index-1"></span><code ...><span class="pre">TMPDIR</span></code>`). It does appear after tags are stripped and whitespace is collapsed. That is rendering, not a second sentence.

### 4. Lesson numbers do not describe the objects they sit next to

Word counts on the lesson's own quoted strings (whitespace split):

| quote in `corpus/lessons/round-54.md` | lesson says | whitespace words |
|---|---|---|
| `TMPDIR This variable shall represent a pathname of a directory made available for programs that need a place to create temporary files` | 21 words | 22 |
| `if dirname: dirlist.append(dirname)` | 5 words | 3 (`if`, `dirname:`, `dirlist.append(dirname)`); 5 identifiers if punctuation is a separator |
| `The directory named by the TMPDIR environment variable` | 11 words | 8 |

The 21-word string is the §8.3 sentence without the leading `TMPDIR`. The 11-token string is the row's longer quote split on whitespace (`The list is: The directory named by the TMPDIR environment variable` → 11). Neither count is the quote it is attached to. The note does not restate these counts.

Sizes. The lesson says S277 was `33758 B text-extracted` with sha `89294048…`, and S279 was `20462 B text-extracted` with sha `6b0edccf…`. Replacing tags with spaces, unescaping, and collapsing whitespace (no strip) yields those figures as **character** counts, not byte counts, and not the digest of that extract:

| file | extract chars | extract bytes | extract sha256 | raw sha (the cited prefix) |
|---|---|---|---|---|
| S277 | 33758 | 33771 | `c1bab31588ff21823aa48a670b14919bb87b51c1e89f51c1945c88d3f370bc3d` | `89294048…` (52350 bytes) |
| S279 | 20462 | 20522 | `6b08641b1510b443b9f7afdb16e4eea5f6432ce8f0623a573774ed1fc5dc648c` | `6b0edccf…` (75190 bytes) |

Same extractor on both files, so the two lesson sizes are one measurement and the two sha prefixes are another. Dropping `<script>`/`<style>` first changes S279 from 20462 to 19351 characters and leaves S277 at 33758, because the POSIX page's scripts do not add collapsed text. The cited digests are the raw snapshots, which do match the rows and the live bodies.

S278's lesson records sha `fb44155f…` with no size. That prefix is the raw file. No size drift there.

## Not drift

- Live bodies were fetched 2026-10-28 (same date the rows say) and `cmp` against the C1 snapshots is exit 0 for all three. S279's URL is `https://docs.python.org/3/library/tempfile.html` (unpinned `/3/`, `last-modified` the same day). It has not moved relative to the snapshot. S277's edition URL and S278's `v3.12.7` blob URL are pinned.
- The note does not claim §8.1, does not claim S279 says "empty", and its `:163-165` is the right span.
- S278's "empty is skipped, so empty behaves as unset" follows from line 165 (`if dirname:`); unset `getenv` returns `None`, empty returns `""`, both falsy. That reading is the note's and the row's, and it matches the code.

## Commands

Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Scout01` (`TMPDIR` set there). Live bodies: `S277.live.html`, `S278.live.py`, `S279.live.html`, plus `S277.hdr`, `S278.hdr`, `S279.hdr`.

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat 99c3bc88d704566197783f66b211ee0a830e0330 HEAD -- corpus/SOURCES.md corpus/knowledge/scratch-root-contract.md corpus/lessons/round-54.md .ufo/evidence/round-54/assimilation/
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse 99c3bc88d704566197783f66b211ee0a830e0330:.ufo/evidence/round-54/assimilation/S277-posix-env.html
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin hash-object .ufo/evidence/round-54/assimilation/S277-posix-env.html
# same pair for S278-tempfile.py and S279-tempfile-docs.html — each pair equal
sha256sum .ufo/evidence/round-54/assimilation/S277-posix-env.html .ufo/evidence/round-54/assimilation/S278-tempfile.py .ufo/evidence/round-54/assimilation/S279-tempfile-docs.html
curl -fsSL -D S277.hdr -o S277.live.html --max-time 40 https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html
curl -fsSL -D S278.hdr -o S278.live.py --max-time 40 https://raw.githubusercontent.com/python/cpython/v3.12.7/Lib/tempfile.py
curl -fsSL -D S279.hdr -o S279.live.html --max-time 40 https://docs.python.org/3/library/tempfile.html
cmp -s S277.live.html .../S277-posix-env.html   # exit 0
cmp -s S278.live.py   .../S278-tempfile.py      # exit 0
cmp -s S279.live.html .../S279-tempfile-docs.html  # exit 0
git -C ... show 99c3bc88d704566197783f66b211ee0a830e0330:corpus/SOURCES.md | sed -n '152,154p'
```

Quote, section, word-count, and extract-sha checks were Python over those three snapshot files (tag-to-space collapse; heading offsets; `in` tests; whitespace `split`). No lane file was modified.

## Artifacts opened

- `corpus/SOURCES.md` lines 152–154 (and the C1 `git show` of those lines)
- `corpus/knowledge/scratch-root-contract.md` lines 11–30
- `corpus/lessons/round-54.md` lines 13–42
- `.ufo/evidence/round-54/assimilation/S277-posix-env.html` (headings, line 239, lines 725–727)
- `.ufo/evidence/round-54/assimilation/S278-tempfile.py` lines 156–181
- `.ufo/evidence/round-54/assimilation/S279-tempfile-docs.html` lines 502–525
- live copies and response headers under `/fast/scratch/hyaku/tameshi-r54/T54W2Scout01/`
