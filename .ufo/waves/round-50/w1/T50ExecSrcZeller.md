# T50ExecSrcZeller — C2 source snapshot: S167 Zeller & Hildebrandt (TSE 2002)

Seat: `T50ExecSrcZeller` (leaf executor, milestone "C2 source snapshot").
Item: re-open and snapshot Zeller & Hildebrandt, *Simplifying and Isolating Failure-Inducing Input*,
IEEE TSE 28(2):183–200, Feb 2002, DOI 10.1109/32.988498 (staged as S167 in
`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`, read-only); locate four verbatim
quotes; state whether the package's quotes and locators are exact.

All paths below are relative to
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-50/w1/T50ExecSrcZeller/`.

## 1. Fetch outcome

| attempt | result |
|---|---|
| DOI landing `https://doi.org/10.1109/32.988498` | **302** → `https://ieeexplore.ieee.org/document/988498/`; the followed request returned **202** with a **0-byte** body (bot-shielded, `server: cloudflare`). No readable landing, no full text. |
| course mirror `https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf` | **200**, `application/pdf`, **247738 bytes**, 17 pages |

Evidence for the DOI attempt: `doi-landing.headers.txt:1` = `HTTP/2 302 `, `doi-landing.headers.txt:4` =
`location: https://ieeexplore.ieee.org/document/988498/`; command
`curl -sS -D doi-headers.txt -o /dev/null --max-time 60 'https://doi.org/10.1109/32.988498'`.
The followed-request status is recorded in `receipt-doi-landing.json` (`followed.http_status = 202`,
`bytes_downloaded = 0`), from
`curl -sS -L -o doi-landing.html -w 'HTTP=%{http_code} FINAL=%{url_effective} BYTES=%{size_download}' ...`
→ `HTTP=202 FINAL=https://ieeexplore.ieee.org/document/988498/ BYTES=0 CT=text/html; charset=UTF-8`.

Bibliographic cross-check (open metadata, not the paywalled text):
`curl -sS 'https://api.crossref.org/works/10.1109/32.988498'` → `crossref-10.1109-32.988498.json:1`
carries `"page": "183-200"`, `"volume": "28"`, `"issue": "2"`, `"published-print": 2002-02`,
`"container-title": ["IEEE Transactions on Software Engineering"]`. That matches the package's
`IEEE TSE 28(2):183-200` exactly.

PDF identity: `sha256 7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`, bytes 247738,
`pdfinfo` → `PDF version 1.2`, `Producer: GNU Ghostscript 5.50`, `CreationDate: Thu Dec 20 06:50:05 2001`,
`Pages: 17`, A4. The typeset two-column IEEE layout with running heads, i.e. the published version, not a preprint.

## 2. Artifacts written

| file | sha256 | note |
|---|---|---|
| `zeller-delta.pdf` | `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa` | the fetched bytes, unmodified |
| `zeller-delta.pdftotext-raw.txt` | `2157fadf4f0c45151a5fa6bee89e839fb6cec81ce2034f110cedb1762a412145` | `pdftotext` default mode; **single-column reading order** (the citable extract; 4227 lines, 85611 bytes) |
| `zeller-delta.pdftotext-layout.txt` | `19b9289a723c1eb812ddb46a613a9275a2a5fe367f9f1e8587f5224d91d1f8ce` | `pdftotext -layout`; columns interleave, kept only for fidelity comparison (1587 lines, 165644 bytes) |
| `receipt-pdf.json` | — | `{url, final_url, http_status, bytes, sha256, fetched_at, tool}` + derived hashes + pdf metadata |
| `receipt-doi-landing.json` | — | DOI landing status chain (302 → 202/0 bytes) |
| `crossref-10.1109-32.988498.json` | — | Crossref metadata response (page-range cross-check) |
| `doi-landing.headers.txt` | — | raw response headers of the DOI resolution |
| `T50ExecSrcZeller.json` | — | deliverable: `{url, sha256, quotes: [{topic, quote, location}], exactness}` |
| `verify-quotes.py` / `verify-quotes.stdout.txt` | — | re-runnable check: every quote present on its page, all hashes match → `VERIFY_QUOTES: PASS` |
| `count-spans.py` / `count-spans.stdout.txt` | — | re-runnable check: reading-order vs `-layout` occurrence counts (the fold measurement of §5) |
| `pdf-head.headers.txt` | — | HEAD response of the mirror URL (Last-Modified, ETag, Content-Length) |

`fetched_at` for the PDF: `2026-10-26T22:15:07Z` (file mtime `19:15:07 -0300`). Tool: `curl` 8.23.0.

## 3. The four required quotes (verbatim, collapsed whitespace)

Command used for every line below:
`pdftotext -f <pdfpage> -l <pdfpage> zeller-delta.pdf -` (page-level extract; the saved
`zeller-delta.pdftotext-raw.txt` holds the same text at the cited line numbers).

**(1) 1-minimal test case definition — "removing any single input entity"**
> is reached, where removing any single input entity would cause the failure to disappear.

Sect. I Introduction, paragraph *"Simplification of test cases"*; **printed p. 183** (PDF page 1).
Shown by `grep -n 'input entity' zeller-delta.pdftotext-raw.txt` → `69:is reached, where removing any single input entity would cause`.
Full sentence: "It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappear." (14 words quoted.)
The *formal* counterpart is Definition 10 on printed p. 186 (PDF page 4): "A failing test case c composed of c changes would be 1-minimal if removing any single change would cause the failure to disappear." — i.e. "change", not "input entity", in the formal statement.

**(2) ddmin chunk granularity — initial partition (n = 2)**
> We begin with partitioning the total set of changes in two halves

Sect. III-B *A Minimizing Algorithm*, worked example of Fig. 6; **printed p. 188** (PDF page 6).
`grep -n 'partitioning the total set of changes in two' zeller-delta.pdftotext-raw.txt` → `1343:` (12 words).

**(2b) ddmin chunk granularity — the doubling rule (n ← 2n)**
> Increase granularity. Otherwise (that is, no test failed), try again with 2n subsets.

Sect. III-B, rule text of Fig. 5 (*Minimizing Delta Debugging algorithm*); **printed p. 187** (PDF page 5).
`grep -n 'Increase granularity. Otherwise' zeller-delta.pdftotext-raw.txt` → `1298:` (13 words).
The rule's cap clause is split off by the page break and the maths layer; it appears at `zeller-delta.pdftotext-raw.txt:1316` as "7 c 7 subsets instead, each containing one change.)" — i.e. |c✘| chunks of one unit each, the glyph run `7 c 7` being `|c✘|`.
The algorithm's own text is `zeller-delta.pdftotext-raw.txt:802-822`: the initial call `ddmin₂(c✘, 2)` at `:811`, and the granularity step as the glyph-degraded `ddmin2 c6  min  7 c6 7  2n` at `:817` (n ← min(|c✘|, 2n)), with `else if n = |c✘| ("increase granularity")` at `:818`. The math layer is degraded by the 2001 Ghostscript producer (glyph runs `7 c6 7` for `|c✘|`), so the formal step is present but should be read alongside the clean prose rule.

**(3) Case-study cost — 896 lines / 139 runs**
> Likewise, it simplified 896 lines of HTML to the single line that caused the failure.

**printed p. 183**, Abstract (PDF page 1); `zeller-delta.pdftotext-raw.txt:13-14` (15 words).

> The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC.

**printed p. 183**, Abstract (PDF page 1); `zeller-delta.pdftotext-raw.txt:14-15` (16 words).
(`grep -n '139 automated test' zeller-delta.pdftotext-raw.txt` → `14:line that caused the failure. The case study required 139 automated test`.)
The detailed figures sit in Sect. IV-B, printed pp. 190–191: `zeller-delta.pdftotext-raw.txt:2118` = "39094 characters or 896 lines; an excerpt is shown in Figure 1." and
`:2125` = "896 lines to a 1-line input:", with "After 57 test runs, the ddmin algorithm minimizes the original ..." (`:2123-2125`); the Mozilla user-action run took "82 test runs (or 21 minutes)" (`:2106`).

**(4) The article's own venue block (running head)**
> IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002

Running head, every verso page, incl. **printed p. 183**; `zeller-delta.pdftotext-raw.txt:1` (11 words).
Recto head (odd pages): `ZELLER AND HILDEBRANDT: SIMPLIFYING AND ISOLATING FAILURE-INDUCING INPUT`
(`pdftotext -f 3 -l 3 zeller-delta.pdf - | head -1`).

Page-folio caveat: this mirror's text layer carries no printed folios and no DOI string
(`grep -c -E '183|988498' zeller-delta.pdftotext-raw.txt` → `0`). Printed pages above are the linear
mapping PDF page N → printed 182+N, corroborated by the section map (Sect. II starts p. 184,
Sect. III p. 185, Sect. IV p. 188, Sect. V p. 192, Sect. IX p. 198, references p. 199) and by Crossref's
`183-200`. The copy has 17 pages, so printed **p. 200 is absent** from it.

## 4. Is the package (S167) exact?

Package row, verbatim in part: locator "§I Introduction (ddmin definition and the 896-line HTML case
study), p. 183-184", summary "a failing test case is reduced by successive testing until removing any
single input entity would make the failure disappear, and the reduction is itself a measured cost (139
automated test runs, 35 minutes on a 500 MHz PC)", verification
``curl -fsSL '<url>' | grep -c 'minimal test case'``.

**Exact:** the phrase "removing any single input entity" is verbatim at p. 183; "successive testing" is
verbatim in the same paragraph (`zeller-delta.pdftotext-raw.txt:68`); "896 lines of HTML" is verbatim in
the abstract (p. 183); "139 automated test runs" and "35 minutes on a 500 MHz PC" are verbatim (p. 183);
the venue `IEEE TSE 28(2):183-200` matches Crossref field for field; Sect. I does occupy pp. 183–184.

**Inexact / loose (five defects, none fatal to the row's use):**
1. **Locator conflates intro with formal definition.** "ddmin definition ... p. 183-184" is true only of
   the one-sentence informal version. Definition 10 (n-minimality) and the ddmin algorithm (Fig. 5) are
   Sect. III-A/III-B on printed **pp. 186–187**. A citation relying on the p. 183-184 locator for the
   algorithm's contract points at the wrong page.
2. **"the 896-line HTML case study ... p. 183-184"** is also loose: p. 183 carries only the abstract
   claim; the case study (39094 characters = 896 lines, 57 test runs, result a 1-line input) is
   Sect. IV-B, printed **pp. 190–191**.
3. **The row's verification command does not reproduce as written.** Run against the fetched bytes:
   `grep -c 'minimal test case' zeller-delta.pdf` → `0`, exit `1` (the text layer is encoded/compressed;
   `grep -a -c` also → `0`). The same grep against a `pdftotext` extract → `8`. So the row's stated
   check would fail on the artifact it names; its "string was present" observation must have been made
   on extracted text, and the row should name `pdftotext | grep` to be a re-runnable proof.
4. **No content hash is pinned** in the row (only a URL and a 365-day window), and the mirror's copy is
   17 pages against the citation's 18 (p. 200 missing). This snapshot supplies the missing pin:
   `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`, 247738 bytes.
5. **The 139/35-min figures are the whole study's cost, not the 896-line reduction's.** The row's
   "the reduction is itself a measured cost (139 automated test runs, 35 minutes ...)" is verbatim to
   the abstract but invites the reading that one reduction cost 139 runs. The paper's own per-reduction
   numbers are 57 runs for the 896-line HTML case (`zeller-delta.pdftotext-raw.txt:89` "After 57 tests, the
   original 896-line HTML input is reduced to the minimal failing test case <SELECT>." and `:2124`
   "After 57 test runs, the ddmin algorithm minimizes the original") and 82 runs / 21 minutes for the
   Mozilla user actions (`:2105-2106`). 82 + 57 = 139, so the abstract total is the sum of the two runs
   described in Sect. IV; the paper states no separate wall-clock figure for the HTML reduction
   (21 min + 14 min = 35 min is arithmetic on my side, [INFERENCE], not a printed number). A citation
   that wants the per-reduction cost must use 57, not 139.

Side note, substantive rather than bibliographic: the package's own one-line summary drops the paper's
distinction between a 1-minimal *test case* ("removing any single change", p. 186) and a 1-minimal
*difference* (Definition 15, p. 194) — relevant to C2, whose shrinker torch is 1-minimality of a
*sub-case*, i.e. the test-case notion, not the isolating-difference notion.

## 5. Corroboration, peer cross-checks, and the S119 "payload-absent" quarantine

**Bytes are triple-confirmed.** My own fetch gives 247738 bytes /
`7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`; peers `T50ExecIdGuard` and
`T50ScribeRows` independently report the identical byte count and hash (their receipts live in their own
`w1/` dirs, not here), and `T50ScribeRows` reports two GETs byte-identical plus a dead author copy at
`st.cs.uni-saarland.de` (curl 28) — attributed, not re-run by me. My own HEAD of the mirror
(`pdf-head.headers.txt`, `curl -sS -I  <url>`) gives `last-modified: Thu, 09 Aug 2007 22:13:20 GMT`,
`etag: "3c7ba-4374b90e76000"`, `content-length: 247738`, so the bytes have been stable at that URL since 2007.

**The payload-absent quarantine on this document is a false positive — measured.**
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:219` records
package id S119 as `payload-absent` for this URL, quoting
`It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappea`
and concluding "the quote is in none of them". The sentence *is* in the mirror; what fails is one extract
mode, because the two columns interleave under `pdftotext -layout`:

| span | count in reading-order extract | count in `-layout` extract |
|---|---|---|
| "…removing any single input entity would cause the failure to disappear." | 1 | 0 |
| "The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC." | 1 | 0 |
| "Likewise, it simplified 896 lines of HTML to the single line that caused the failure." | 1 | 1 |
| "IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002" | 9 | 9 |

Reproduce: `python3 count-spans.py` → `count-spans.stdout.txt` (the table above verbatim). The flip side of the same artifact: in the `-layout` extract the intro
sentence is hyphen-folded (`sim-` / `plifies`, `zeller-delta.pdftotext-layout.txt:30-31`), while the
reading-order extract carries it whole (`zeller-delta.pdftotext-raw.txt:68`); the only hyphen fold inside
my reading-order extract is `other-` at `:2024`, outside every quoted span. Consequence for anyone
re-checking this source: state the extract mode, or the same bytes produce opposite verdicts.
`T50ScribePkgDD` reached the same 57-vs-139 attribution and the same `sim-/plifies` fold independently
(their point 2 and 6, their own snapshot dir) — three seats, one set of bytes, one conclusion.

**Lane id facts (verified myself, read-only).** `corpus/SOURCES.md` holds 130 registry rows, ids up to
S270, and no `S167` row (`grep -c '^| S[0-9]\+ |' corpus/SOURCES.md` → `130`; `grep -c '^| S167 |'` → `0`;
max id `270`; `S271` absent). The paper appears only as an unopened Lead bullet at `corpus/SOURCES.md:278`
and in lead-history prose at `:184` (both read with `sed -n '184p;278p'`), and `corpus/SOURCES.md:495`
reads "Next unused id: S271 (staged ids S161-S255 stay reserved by document for the package)". I do **not**
open a row — adopting the id is another seat's decision; this seat's deliverable is the snapshot.

**Peer locators I correct (denied as stated).** `T50ScribeRows` labels the p. 186 1-minimality passage
"§II-A" and the p. 188 properties passage "§II-C"; both are Sect. **III** (`zeller-delta.pdftotext-raw.txt:484`
= "A. Minimal Test Cases", `:1365` = "C. Properties of ddmin", with Sect. III opening at `:445`).
Their Proposition 12 formula (|c|²+3|c|) is *not verifiable* from this copy: `:1473` renders
"tests carried out by ddmin c✘ is c✘ 2 3 c✘ in the worst case." with the exponents lost, so I neither
confirm nor deny it. Their raw line numbers (73-75) are extract-local; in the snapshot here the sentence
sits at `:68-70` (same page, same text).

## 6. Bounds compliance

- Wrote only `w1/T50ExecSrcZeller/` (this directory) and this report `w1/T50ExecSrcZeller.md`; lane
  checkout otherwise untouched — no git/jj command was run in the lane, no add/commit/checkout/stash,
  no index or jj mutation.
- Nothing written to `/home/vgpnk/Projects/shokunin` (fleet root), any sibling lane, or
  `/home/vgpnk/Projects/shokuknow` (S167 row read only).
- Scratch root `/fast/scratch/hyaku/tameshi-r50/T50ExecSrcZeller/` deleted before yielding; no `/tmp`
  or scratch path is cited as evidence — every cited file lives in this directory.
- Never read anything under `/home/vgpnk/.local/state/`; never opened
  `.ufo/evidence/round-50/control/c2-*.stdout`; ran no counter and no control (no `measure.py`
  invocation at all), so nothing here is a verdict on C1 or C2.
- Tooling: no installs, no pacman (host-wide pause respected). Used pre-installed
  `pdftotext` 26.08.0 (poppler), `curl` 8.23.0, `python3` 3.14.8. The `aaron` CLI route was not used:
  a copy openly served by a university course mirror (the URL the package names) was obtained, so no
  shadow-library fetch was needed. No model was passed; no routing table touched. No `agent://all`.

## Summary

DOI 10.1109/32.988498 resolves 302 to IEEE Xplore, which answers 202 with a 0-byte bot-shielded body; full text came from the packaged course mirror (200, 247738 B, 17 pp).
Snapshot + receipts + two pdftotext extracts in `w1/T50ExecSrcZeller/`; `verify-quotes.py` → `VERIFY_QUOTES: PASS` on the saved bytes.
(1) "removing any single input entity" p. 183; (2) "two halves" p. 188 and "try again with 2n subsets" p. 187; (3) 896 lines / 139 runs p. 183; (4) venue head p. 183 — Crossref confirms 28(2):183-200.
Package quotes are verbatim; its locators are wrong for the formal contract (Definition 10 / Fig. 5 on pp. 186-187, the 896-line case study on pp. 190-191).
The 139 runs / 35 min are the whole study, not one reduction: the 896-line reduction cost 57 runs (82+57=139) — do not cite 139 per reduction.
The package's `grep` on the PDF bytes returns 0, exit 1; a re-runnable check must go through `pdftotext` first.
The S119 payload-absent quarantine is a fold false positive: the quoted span counts 1 in reading order, 0 under `-layout`.
Copy is 17 pages (no printed p. 200) with folios absent; page numbers are the verified N→182+N mapping.
