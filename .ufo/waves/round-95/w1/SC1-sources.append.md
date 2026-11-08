# SC1 — `corpus/SOURCES.md` append draft (round 95)

**Seat:** R95SC1 (scribe). **Lane:** tameshi. **Mode:** read-only — nothing under
`corpus/` was written; this file is a draft for the L1 to integrate.

**Read first.** The L1's instruments commit `0685c358` already landed the `S323` row
and the three `used-by` appends in `corpus/SOURCES.md`, and the appends are **correct as
landed**. What is *not* correct is two numbers inside the landed `S323` row — its
`teaches` word count and its `anchor` line — both of which are hand-written rather than
printed by a command (QUALITY 87's class). This draft therefore has two parts: the
**append block** as specified, and a **corrections block** for the landed row.

## Part 1 — the append block (as specified)

### 1a. New row `S323` — 11 columns, one line

```markdown
| S323 | CommonMark Spec 0.31.2 — Indented code blocks — https://spec.commonmark.org/0.31.2/ | docs | A | why the round-95 note reader treats a 4+-space-indented line as literal text, not a table row or the note's figure | §4.4 Indented code blocks, tag-stripped snapshot `.ufo/evidence/round-95/sources/s323.html` line 2358 @ page fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 10:41:46 GMT; 514698 B; sha256 c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d) | "An indented code block is composed of one or more indented chunks separated by blank lines." (16 words): an indented chunk is literal text, so a presented verdict row inside one is not a keyed table row and an indented `measured:` line is not the note's figure | mined | 2026-11-08 | 365d | corpus/lessons/round-95.md |
```

Column-by-column (11 cells; `awk -F'|'` gives NF=13, i.e. 11 content columns plus the
two pipe-only ends):

| # | column | value |
|---|---|---|
| 1 | id | `S323` |
| 2 | source | `CommonMark Spec 0.31.2 — Indented code blocks — https://spec.commonmark.org/0.31.2/` |
| 3 | kind | `docs` |
| 4 | tier | `A` |
| 5 | scope | why the round-95 note reader treats a 4+-space-indented line as literal text, not a table row or the note's figure |
| 6 | anchor | `§4.4 Indented code blocks`, tag-stripped snapshot `.ufo/evidence/round-95/sources/s323.html` **line 2358** @ page fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 10:41:46 GMT; 514698 B; sha256 `c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d`) |
| 7 | teaches | `"An indented code block is composed of one or more indented chunks separated by blank lines."` **(16 words)**: an indented chunk is literal text, so a presented verdict row inside one is not a keyed table row and an indented `measured:` line is not the note's figure |
| 8 | status | `mined` |
| 9 | opened | `2026-11-08` |
| 10 | recheck | `365d` |
| 11 | used-by | `corpus/lessons/round-95.md` |

### 1b. `used-by` appends for S320 / S321 / S322 (old → new)

Every existing path is kept; `corpus/lessons/round-95.md` is appended. **These three
appends are already landed correctly at `0685c358` and need no change** — the table
below is the record of what was asked for and what is there.

| row | field | old | new |
|---|---|---|---|
| S320 | `used-by` | `corpus/lessons/round-92.md, corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `corpus/lessons/round-92.md, corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-95.md` |
| S321 | `used-by` | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-95.md` |
| S322 | `used-by` | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-95.md` |

Registry rows: **182 → 183**; tier A 164 → 165; status `mined` 148 → 149.

## Part 2 — corrections to the row already landed at `0685c358`

The landed `S323` row differs from the block above in two measurable ways, both
**number-drift** (QUALITY 87: a count that is written by hand instead of printed by a
command).

| cell | landed at `0685c358` (unchanged at HEAD `3ca1981a`) | measured against the committed bytes | corrected |
|---|---|---|---|
| `teaches` — word count | `(15 words)` | the quoted span `"An indented code block is composed of one or more indented chunks separated by blank lines."` is **16** whitespace tokens — `len(q.split())` → 16, the same tokenizer `measure-v95.py:386` `located_quotes` uses to accept a quote; `wc -w` on the sentence → 16 | `(16 words)` |
| `anchor` — line | `line 2355` | under the lane's tag-strip convention (HTML text extraction, one output line per source line, each line stripped — the convention that reproduces the committed round-93 `sources/s321.txt` and `s322.txt` **byte-for-byte**, verified `True` for both) the sentence "An indented code block is composed of one or more" is at **line 2358** (it spans 2358–2359); line 2355 is a blank line and the `§4.4 Indented code blocks` heading is at 2356 | `line 2358` |

The landed `scope`, `kind`, `tier`, `status`, `opened`, `recheck` and `used-by` cells are
correct and need no change. The three `used-by` appends (Part 1b) are correct as landed.

### Measured line table for the four rows' Gate quotes

Every quote below is present in the snapshot's `norm_text` (the counter's own
normalizer, `measure-v95.py:378`) and the line is the first line of the quote in the
tag-stripped snapshot.

| row | quote | words | snapshot | tag-stripped line carrying the quote | span |
|---|---|---|---|---|---|
| S320 | "Print or check SHA256 (256-bit) checksums." | 6 | `.ufo/evidence/round-95/sources/s320.html` | 88 | 85–88 |
| S321 | "a single header row, a delimiter row separating the header from the data" | 13 | `.ufo/evidence/round-95/sources/s321.html` | 4396 | 4393–4396 |
| S321 | "The table is broken at the first empty line, or beginning of another block-level structure" | 15 | `.ufo/evidence/round-95/sources/s321.html` | 4496 | 4494–4497 |
| S322 | "A fenced code block begins with a code fence, preceded by up to three spaces of indentation." | 17 | `.ufo/evidence/round-95/sources/s322.html` | 2618 | 2616–2619 |
| S323 | "An indented code block is composed of one or more indented chunks separated by blank lines." | 16 | `.ufo/evidence/round-95/sources/s323.html` | 2358 | 2356–2359 |

A sixth quote the landed lesson carries — the GFM delimiter-row sentence — is quoted
**with spaces inside the parentheses** ("hyphens ( - )"), which is the counter's
`norm_text` rendering (tags → a space) and is **not** the tag-stripped text's own
rendering ("hyphens (-)"). Measured: the as-landed form is in `norm_text` (`True`) but
**not** in the tag-stripped text (`False`), so it has no line in the tag-stripped
snapshot and its cited line `4400` carries different text. The tag-stripped text reads
at 4403: "The delimiter row consists of cells whose only content are hyphens (-),". The
word count is also off: the landed lesson says `(20 words)`, the span as written is
**24** whitespace tokens (the parentheses are separate tokens).

## Census check (the row and the appends, run on a scratch mirror)

The census was run against a **copy** of `corpus/SOURCES.md` in this seat's scratch
(`/fast/scratch/hyaku/tameshi-r95/R95SC1/lane/corpus/SOURCES.md`), with the `S323` row
and the three `used-by` appends applied. The lane's own `corpus/SOURCES.md` was not
written.

Column-count AWK (the acceptance check):

```
$ awk -F'|' 'NF!=13' s323-final.row.md | wc -l
0
$ awk -F'|' '{print "NF=" NF}' s323-final.row.md
NF=13
```

`NF=13` = 11 content columns + the two pipe-only ends, i.e. the 11-column shape the
census requires.

Full census on the mirror (S323 row + the three appends applied):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /fast/scratch/hyaku/tameshi-r95/R95SC1 \
    --file /fast/scratch/hyaku/tameshi-r95/R95SC1/lane/corpus/SOURCES.md
file	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
file	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
file	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
file	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
file	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
file	W04	S092 duplicate url bazel.build/remote/caching across scopes
file	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
file	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
file	W04	S160 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants across scopes
file	W04	S265 duplicate url testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html across scopes
file	W04	S266 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S267 duplicate url github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml across scopes
file	W04	S268 duplicate url www.tensorflow.org/federated/golden_tests?hl=zh-cn across scopes
file	W04	S274 duplicate url bazel.build/basics/hermeticity across scopes
file	W04	S288 duplicate url www.atlassian.com/incident-management/handbook/postmortem across scopes
file	W04	S293 duplicate url git-scm.com/docs/git-cat-file across scopes
file	W04	S303 duplicate url www.gnu.org/software/sed/manual/sed.html across scopes
file	W04	S314 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
file	W04	S318 duplicate url git-scm.com/docs/git across scopes
file	W04	S323 duplicate url spec.commonmark.org/0.31.2 across scopes
file	ok	/fast/scratch/hyaku/tameshi-r95/R95SC1/lane/corpus/SOURCES.md
exit=0
```

Exit 0, lane `ok`. The census **counts** rows but `validate` reports a `W04`
duplicate-URL warning for `S323`, because `S322` and `S323` are two rows on the same
page (`https://spec.commonmark.org/0.31.2/`) with different scopes. This is the same
warning class the lane already carries 20 times (`W04` for S047, S075, S081 …), so it is
a warning, not a finding; the census exit stays 0. The L1 should expect one more `W04`
line than the before-census had.

Counts on the same mirror:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census \
    --root /fast/scratch/hyaku/tameshi-r95/R95SC1 \
    --file /fast/scratch/hyaku/tameshi-r95/R95SC1/lane/corpus/SOURCES.md
file	rows	183
file	tier.A	165
file	tier.B	14
file	tier.C	4
file	status.mined	149
file	status.queued	23
file	status.rejected	11
FLEET	rows	183
FLEET	tier.A	165
FLEET	tier.B	14
FLEET	tier.C	4
FLEET	tier.invalid	0
FLEET	status.queued	23
FLEET	status.mined	149
FLEET	status.rejected	11
FLEET	status.invalid	0
FLEET	missing	0
exit=0
```

Before-census for comparison (the committed receipt
`.ufo/waves/round-95/census-before.txt`, and re-run by this seat against the lane at
`0685c358`): `rows=182`, tiers `A=164 B=14 C=4`, status `mined=148 queued=23
rejected=11`, exit 0.

**One integration-order note for the L1.** The census's `E11` check requires every
`used-by` path to exist on disk. When the `S323` row and the three `used-by` appends
land, `corpus/lessons/round-95.md` must exist in the same commit, or the census prints
`E11 … missing used-by corpus/lessons/round-95.md` for all four rows and exits 1.
Measured on the mirror with the lesson file removed:

```
file	E11	S320 missing used-by corpus/lessons/round-95.md
file	E11	S321 missing used-by corpus/lessons/round-95.md
file	E11	S322 missing used-by corpus/lessons/round-95.md
file	E11	S323 missing used-by corpus/lessons/round-95.md
```

The lesson exists at `0685c358`, so this is only a hazard if the row and the lesson are
ever split across commits.

## Evidence pointers this draft cites

- `.ufo/evidence/round-95/sources/s320.html` sha256 `b968bc09…2777b`, HTTP date
  `Sun, 08 Nov 2026 08:53:29 GMT`, 12 127 B
- `.ufo/evidence/round-95/sources/s321.html` sha256 `b153d814…a220`, HTTP date
  `Sun, 08 Nov 2026 08:53:23 GMT`, 508 310 B
- `.ufo/evidence/round-95/sources/s322.html` sha256 `c85f56cc…60f0d`, HTTP date
  `Sun, 08 Nov 2026 08:53:28 GMT`, 514 698 B
- `.ufo/evidence/round-95/sources/s323.html` sha256 `c85f56cc…60f0d`, HTTP date
  `Sun, 08 Nov 2026 10:41:46 GMT`, 514 698 B (byte-identical to `s322.html` — the same
  0.31.2 page; recorded in `R95E1-sources.out` and
  `.ufo/evidence/round-95/sources/SHA256SUMS`)
- `.ufo/evidence/round-95/c1/measure-v95.py:386` `located_quotes` (the rule the Gate
  quotes must satisfy) and `:378` `norm_text`
- `.ufo/waves/round-95/census-before.txt` (the before-census receipt)
