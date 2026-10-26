# T50ScribeRows — C2 SOURCES.md row: Zeller & Hildebrandt, TSE 2002

Seat: T50ScribeRows (leaf). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base
`e3729de862f73ae080d98fcf522a7081ce16e40a`. Lane checkout untouched; every artifact below is a wave file.
Scratch root `/fast/scratch/hyaku/tameshi-r50/T50ScribeRows` was created for the runs and deleted before yield.

## 1. The row (verbatim, one line, 11 cells, no `|` inside any cell)

Append as the line after `S270` — i.e. new line 146 of `corpus/SOURCES.md`, immediately before the blank line
that precedes `## Paths` (`corpus/SOURCES.md:145-147`).

```
| S271 | Simplifying and Isolating Failure-Inducing Input (Zeller, Hildebrandt; IEEE TSE 28(2):183-200, 2002; DOI 10.1109/32.988498) — https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf | paper | A | F6 fixture shrinking — the 1-minimal sub-case criterion for a reduced fixture and the test-run cost of reaching it | §I Introduction, Simplification of test cases paragraph (printed p. 183, PDF p. 1); §III-A Minimal Test Cases, Definition 10 (printed p. 186, PDF p. 4); §III-C Properties of ddmin, Propositions 11 and 12 (printed p. 188, PDF p. 6) @ IEEE TSE vol. 28 no. 2, February 2002, DOI 10.1109/32.988498; course-mirror PDF fetched 2026-10-26, sha256 7ed0c812, 247738 bytes, snapshot .ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf | a failing test case is 1-minimal when removing any single change makes the failure disappear, ddmin returns such a case, and the reduction is itself a cost measured in test runs | mined | 2026-10-26 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
```

Row machine-copy: `.ufo/waves/round-50/w1/T50ScribeRows.row.txt`. Cell check (`python3` split on `|` after stripping the
outer bars): NF=11, no cell contains `|`, no `\|` anywhere in the line.

Cell choices:
- `id` S271 = next free after the registry maximum. `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`
  yields maxima S156–S160 then S256–S270; tail = `S270`. S167 is **not** in the lane registry
  (`grep -nE '^ {0,3}\|[[:space:]]*S167([^0-9]|$)' corpus/SOURCES.md` → exit 1, no line), so the staged id is not
  reused; it is a shokuknow stage row, `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:21`.
- `kind` paper, `tier` A (original journal article, in scope), `status` mined, `opened` 2026-10-26,
  `recheck` 730d (ISO/NN d/symbolic rule at `/home/vgpnk/Projects/shokunin/CORPUS.md:105-106`).
- `used-by` = the F6 entry the L1 will write, `corpus/knowledge/fixture-shrinking-pilot.md`; the entry does not
  exist on disk yet (see §5, finding 2).
- `anchor` quotes printed pages, not reprint pages: the course mirror is a 17-page reprint with no printed folios in
  its text layer, so the map PDF page N → printed 182+N comes from `T50ExecSrcZeller.md:99-103` (section map +
  Crossref 183-200). Section labels were re-checked against the document's own headings in this seat's extract —
  `III. MINIMIZING TEST CASES` / `A. Minimal Test Cases` / `C. Properties of ddmin`
  (`.ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.txt:303,318,507`, all file-local extraction
  coordinates, not document properties): Definition 10 sits in §III-A (printed p. 186) and Propositions 11–12 in
  §III-C (printed p. 188). The earlier draft's §II-A/§II-C labels were wrong and were corrected on the source seat's
  report (`T50ExecSrcZeller.md`, `T50ExecSrcZeller.json`).

## 2. Gate paragraph (for `corpus/lessons/round-50.md` `## Gate`)

> **S271 — Zeller & Hildebrandt, *Simplifying and Isolating Failure-Inducing Input* (IEEE TSE 28(2):183-200, Feb 2002,
> DOI 10.1109/32.988498).** Opened 2026-10-26 at https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf
> (HTTP 200, `application/pdf`, 247738 bytes, sha256 `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`,
> Last-Modified 2007-08-09). Quote (21 words, §I Introduction, "Simplification of test cases" paragraph, printed p. 183,
> PDF p. 1): "It stops when a minimal test case is reached, where removing any single input entity would cause the
> failure to disappear." Supporting quote (15 words, Abstract, printed p. 183): "The case study required 139 automated
> test runs, or 35 minutes on a 500 MHz PC." The formal criterion is Definition 10, §III-A (printed p. 186) and the
> guarantee plus worst-case cost bound are Propositions 11–12, §III-C (printed p. 188; the formula's exponents are lost
> in every extract of this mirror, so it is cited, not quoted). Cost nuance for F6: the abstract's 139 runs is the whole
> case study (Mozilla actions plus the HTML reduction); the per-reduction figure is 57 runs — "After 57 tests, the
> original 896-line HTML input is reduced to the minimal failing test case" (§I, printed p. 183, 16 words). Re-verify at
> 730d: fetch the same URL, then `pdftotext -raw FILE - | tr -s ' \n' ' '` and expect exactly one hit each for
> `removing any single input entity`, `139 automated test runs` and `After 57 tests`.

The re-verify condition lives only in this Gate text, per the item; the row's `recheck` cell is the bare cadence `730d`.

## 3. Validation in scratch (census validator, frozen script)

Setup: `S=/fast/scratch/hyaku/tameshi-r50/T50ScribeRows; mkdir -p "$S"; cp -a <lane>/corpus "$S/v/corpus"`;
`ln -s <lane>/tools "$S/v/tools"` (the registry also cites `tools/tally-audit*.py` used-by paths, resolved from the
registry's parent directory, `scripts/sources-census.sh:538-570`); the row appended at line 146 of `"$S/v/corpus/SOURCES.md"`.
Validator: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.

Command (row present, `corpus/knowledge/fixture-shrinking-pilot.md` **absent**):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/v/corpus/SOURCES.md"
```

Observed (`.ufo/waves/round-50/w1/T50ScribeRows.validate-row-only.stdout`, 16 findings + no `ok` line, **exit 1**):
15 pre-existing W-codes (W04 S047,S048,S075,S076,S077,S078,S081,S092,S104,S160,S265,S266,S267,S268; W01 S101) and
exactly one new verdict:

```
file	E11	S271 missing used-by corpus/knowledge/fixture-shrinking-pilot.md
```

Command (same row, a one-line placeholder written **only inside the scratch copy** at
`"$S/v/corpus/knowledge/fixture-shrinking-pilot.md"`):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/v/corpus/SOURCES.md"
```

Observed (`.ufo/waves/round-50/w1/T50ScribeRows.validate-with-stub.stdout`): identical 15 W-codes, then
`file	ok	/fast/scratch/hyaku/tameshi-r50/T50ScribeRows/v/corpus/SOURCES.md`, **exit 0**. So the row itself adds no
E/W code; the sole E finding is the pending entry file.

Baseline for comparison (lane registry unchanged, `.ufo/waves/round-50/w1/T50ScribeRows.validate-lane-baseline.stdout`):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```
→ the same 15 W-codes plus `file	ok	…/corpus/SOURCES.md`, **exit 0**.

No `--explain`, no counter, no deciding run: this item's gate is the census validator only.

## 4. Provenance and cross-check

| fact | evidence |
|---|---|
| PDF bytes 247738, sha256 `7ed0c812…`, HTTP 200, Last-Modified `Thu, 09 Aug 2007 22:13:20 GMT` | `.ufo/waves/round-50/w1/T50ScribeRows.src/fetch-receipt.json`; two independent GETs by this seat byte-identical (`sha256sum` on both) |
| same bytes as the source seat | `T50ExecSrcZeller/receipt-pdf.json` (`bytes` 247738, `sha256` identical, `fetched_at` 2026-10-26T22:15:07Z); `.ufo/waves/round-50/w1/T50ExecSrcZeller/zeller-delta.pdf` `sha256sum` matches |
| venue/pages/DOI | Crossref `api.crossref.org/works/10.1109/32.988498` → container IEEE TSE, vol 28, issue 2, page 183-200, published-print 2002-02; snapshot `T50ExecSrcZeller/crossref-10.1109-32.988498.json` |
| printed page map (PDF N → 182+N) | `T50ExecSrcZeller.md:99-103`; independently consistent with this seat's extraction (Definition 10 on PDF p. 4, Propositions 11–12 on PDF p. 6) |
| quote 1 contiguity | `zeller-hildebrandt-tse2002.txt:73-75` (`pdftotext -raw`, page 1) — line breaks only, no hyphenation |
| quote 2 contiguity | `zeller-hildebrandt-tse2002.txt:12-13` — "The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC." |
| per-reduction cost | `zeller-hildebrandt-tse2002.txt:96-98` — "After 57 tests, the original 896-line HTML input is reduced to the minimal failing test case"; 57 test runs repeat at `:806-808`, and the study total 139 = 82 Mozilla-action runs + 57 HTML-reduction runs (source seat, `T50ExecSrcZeller.md`) |
| author copy not used | `https://www.st.cs.uni-saarland.de/papers/tse2002/tse2002.pdf` → curl exit 28, HTTP 000, 45 s timeout (recorded in the receipt `note`) |

Line numbers in the `.txt` column are coordinates of this seat's own snapshot file (reproduce with
`pdftotext -raw <pdf> <txt>`, poppler 26.08.0); they are not properties of the article. Printed pages come from the
PDF N → 182+N map in this table.

Snapshot kept in the wave: `.ufo/waves/round-50/w1/T50ScribeRows.src/` = `zeller-hildebrandt-tse2002.pdf` (247738 B),
`zeller-hildebrandt-tse2002.txt` (`pdftotext -raw`, 84048 B), `fetch-receipt.json`.
Tools used, nothing installed: `curl 8.23.0`, `pdftotext 26.08.0` (poppler), `python3 3.14.8`, `gawk`/`grep`/`sort`.

## 5. Findings

1. **The next free id is S271, not S167.** Registry maxima are S160 then S256–S270 (`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`
   + numeric sort, tail `S270`); S167 has no lane row (`grep -nE '^ {0,3}\|[[:space:]]*S167([^0-9]|$)' corpus/SOURCES.md`
   → exit 1) and is the shokuknow stage row for this same document
   (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:21`, mined 2026-10-23, URL identical).
   S271 is unused in the lane registry (no W04/E03 for it).
2. **The row validates clean only once the F6 entry exists.** `ls corpus/knowledge/fixture-shrinking-pilot.md` → "No such
   file or directory"; the entry draft seat has not delivered at the time of writing
   (`ls .ufo/waves/round-50/w1/T50ScribeEntryDraft*` → none). Until the L1 writes the entry, the census reports the single
   `E11 S271 missing used-by corpus/knowledge/fixture-shrinking-pilot.md` (exit 1); with the path present the same registry is
   `ok` (exit 0). This is a dependency, not a row defect: the C2 predicate itself requires a knowledge entry new since base
   naming F6 that cites a row opened 2026-10-26.
3. **The Gate quote is taken from §I, not Definition 10, for an extraction reason.** In this seat's `pdftotext -raw`
   extract of the mirror the Definition-10 sentence (`zeller-hildebrandt-tse2002.txt:349-351`, file-local) renders the
   cardinality bars as the glyph run `7c7` and hyphenates `disap-pear`; the source seat's default-mode extract instead
   drops the bars entirely ("composed of c changes", `T50ExecSrcZeller.md:59-65`). Both are extraction artifacts, so the
   glyph claim is mode-specific and no verbatim Definition-10 quote is claimed from these bytes; the §I sentence is clean
   in both extracts and states the same criterion. `teaches` content is therefore supported by one clean 21-word quote
   for 1-minimality plus one clean 15-word quote for cost, with §III-A/§III-C cited by printed page. Consequence for the
   F6 entry: quote §I, or quote Definition 10 only with a note that the bars do not survive extraction.
4. **The staged S167 anchor is loose for this scope; this row pins the pages.** S167's anchor names "§I Introduction
   (ddmin definition …), p. 183-184", but the §III-A/§III-B minimisation contract sits at printed pp. 186–187 and the
   1-minimal criterion at p. 186 (sibling finding, `T50ExecSrcZeller.md:119-122`; this seat's page-level extraction agrees). No supersede is
   claimed: S167 is not an in-lane row, so `supersedes` would be false, and the URL is therefore not an E04 duplicate of a
   lane row.
5. **Scope of the 1-minimal claim.** The row's `teaches` is deliberately silent on the *difference* notion — Definition 15
   (printed p. 194) is a separate criterion the sibling flags as C2-relevant (`T50ExecSrcZeller.md:136-138`). If the L1 wants
   the row to carry that distinction it should be a second row, not a wider `teaches`.
6. **Not done, deliberately out of scope:** no `## Paths` entry was written (`corpus/SOURCES.md:147-150` reduction path
   still reads `S024 → S022 → …`; the L1 may insert S271 after S024); `corpus/README.md:83` still marks F6 `open`; no
   knowledge entry, no SCORECARD/Planned text, no lane commit, no counter run. No lane file was modified.

## 6. What the L1 should run

1. Append the §1 line at `corpus/SOURCES.md:146` (byte-exact; one line).
2. Write `corpus/knowledge/fixture-shrinking-pilot.md` with `source: S271 — <URL> — <anchor>` in the header form of
   `corpus/knowledge/pbt-generator-pilot.md:1-5`.
3. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md` → expect the 15
   pre-existing W-codes and `ok`, exit 0 (mirror of §3's with-stub run; without the entry it is E11, exit 1).
4. Optionally `census --root /home/vgpnk/Projects/shokunin tameshi` for the fleet row count.

## Summary

- Drafted row S271 for Zeller & Hildebrandt, TSE 28(2):183-200 (2002): 11 cells, status mined, opened 2026-10-26,
  recheck 730d, used-by `corpus/knowledge/fixture-shrinking-pilot.md`, no pipe in any cell.
- Id proven: registry max S270; S167 absent from the lane registry and staged in shokuknow, so not reused.
- Source opened and snapshotted: Purdue mirror, HTTP 200, 247738 B, sha256 7ed0c812…, byte-identical to the source seat's
  fetch; Saarland author copy timed out (HTTP 000).
- Census validate in scratch: exit 0 / `ok` with the used-by path present; exit 1 with exactly one E11 (that missing path)
  when absent; 15 pre-existing W-codes unchanged from the lane baseline (exit 0 / `ok`).
- Gate paragraph supplied with URL, access date, two located quotes (21 and 15 words) and the 730d re-verify command.
- Limit: Definition 10's cardinality bars do not survive extraction in either seat's mode, so the Gate quotes §I and
  cites Definition 10 (§III-A) / Propositions 11–12 (§III-C) by printed page, with the per-reduction cost put at 57 runs,
  not the study total 139.
- Receipts: `.ufo/waves/round-50/w1/T50ScribeRows.row.txt`, `T50ScribeRows.src/{fetch-receipt.json,
  zeller-hildebrandt-tse2002.pdf,.txt}`, three `T50ScribeRows.validate-*.stdout`.
