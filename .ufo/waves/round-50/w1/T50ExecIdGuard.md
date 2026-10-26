# T50ExecIdGuard — assimilation id-collision check + guard proof (round 50, w1)

Seat: executor, axis coverage, milestone "assimilation id check". Reads only; the lane checkout was
not modified. Scratch root `/fast/scratch/hyaku/tameshi-r50/T50ExecIdGuard` (deleted before yield);
receipts under `.ufo/waves/round-50/w1/T50ExecIdGuard/` (referenced below as `receipts/`).
Commands: `receipts/commands.txt`.

Inputs (bytes actually read, hashed by the guard itself, `receipts/guard-run.json`):

| input | file | sha256 | rows |
|---|---|---|---|
| registry | `corpus/SOURCES.md` | `530a3c7865611a4404e2ad97b926ffcb666eea2e720ae7c33807d53c872b56b1` | 130 |
| staged | `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` | `020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807` | 103 |

## 1. Both id counts and the collision list

- **Registry ids: 130** (`S001` … `S270`, 130 rows, 111 distinct documents).
  `receipts/reg-ids`; first `S001`, last `S270`.
- **Staged ids: 103** (`S153` … `S255`).
  `receipts/staged-ids`; first `S153`, last `S255`.
- `comm -12` → `receipts/collisions`, **8 ids**:
  `S153 S154 S155 S156 S157 S158 S159 S160`.

The guard agrees exactly — `collision_count=8`, same list, `unmapped=[]`,
`registry_max=S270`, `staged_max=S255`, `next_free=S271`, `safe_floor=S271`,
`naive_map={S153…S160 → S271…S278}`, `cascade=[]`, `cascade_count=0`,
`refused=false`, `verdict=answered` (`receipts/guard-run.json`). Both extractors agree on the real
files (`column0_collisions` = the same 8, `column0_miss=[]`) because every row in both files is
written at column 0 today; the indented case is proved separately in §3.

## 2. Renumber map — by document, the id follows the URL

Held documents (the registry already carries the staged row's document; append nothing, dedupe to
the registry id). Guard `held` + registry rows:

| staged | document (URL/DOI) | target | registry row |
|---|---|---|---|
| `S153` | `pubs.opengroup.org/…/utilities/diff.html` | `S105` | `corpus/SOURCES.md:117` |
| `S154` | `raw.githubusercontent.com/google/golden/master/golden.go` | `S106` | `corpus/SOURCES.md:118` |
| `S155` | `arxiv.org/abs/2302.09330` (Gruber et al.) | `S261` | `corpus/SOURCES.md:136` |
| `S158` | `mir.cs.illinois.edu/…/LamETAL20ManyFlakyTestsAreNDOD.pdf` | `S262` | `corpus/SOURCES.md:137` |
| `S159` | `pitest.org/quickstart/basic_concepts/` | `S155` | `corpus/SOURCES.md:125` |
| `S160` | `pitest.org/faq/` | `S156` | `corpus/SOURCES.md:126` |

New documents (no registry row carries the URL), fresh ids at/above the safe floor `S271`:

| staged | document | target |
|---|---|---|
| `S156` | `arxiv.org/abs/2406.09843` (LLMs for mutation testing) | `S271` |
| `S157` | `doi.org/10.21105/joss.01891` (Hypothesis, JOSS 2019) | `S272` |

That 8-entry map is **admissible**: `--map receipts/maps/mapA.json` → `verdict=admitted`, exit 0
(`receipts/maps/mapA.out.json`).

### The staged `S167` entry

`S167` is **not a collision**: `grep -x S167 reg-ids` is empty and `grep -n 'S167'
corpus/SOURCES.md` matches nothing — the registry has no `S167` row. Nor does any registry row carry
its document: the URL `www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf`
(Zeller & Hildebrandt, TSE 2002) appears nowhere in `corpus/SOURCES.md` (no `purdue` match); the
paper exists there only as an **unopened Lead bullet** naming the DOI,
`corpus/SOURCES.md:278` — `- Zeller & Hildebrandt, *Simplifying and Isolating Failure-Inducing Input* (TSE 2002) — doi:10.1109/32.988498.` —
and as lead-history prose at `corpus/SOURCES.md:184` ("Zeller & Hildebrandt TSE 2002 (F6) stays a
lead: author PDFs timed out (HTTP 000), ResearchGate HTTP 403, DOI resolver gave metadata only").
Neither is a row, so there is no registry id for the id to follow.

**Renumber entry for staged `S167`: none required (no collision).** The id follows the URL to a
document the registry does not hold, so if this round adopts that document it takes a **fresh id
above the tail — `S271`, first free above `registry_max S270`** (precedent: every fresh row since
round 41 takes `max+1`, `corpus/SOURCES.md:467` "Next unused id: S155", `:478` "Next unused id:
S160"), and never `S167` itself. Proven on the guard, three variants:

- `--map receipts/maps/mapB_self.json` (`S167→S167`) → **exit 1, `inadmissible`**,
  `["map targets are still staged ids: S167"]` — a staged id can never be an adoption target.
- `--map receipts/maps/mapD_arith.json` (`S167→S175`, the naive "+8 for the 8 collisions below it")
  → **exit 1, `inadmissible`**, `["map targets are still staged ids: S175"]` — `S175` is the GNU
  Diffutils row at `SOURCES.append.md:29`, i.e. arithmetic repairs one citation and breaks the next.
- `--map receipts/maps/mapC_fresh.json` (map A plus `S167→S273`) → **exit 0, `admitted`** — a fresh
  id above the floor is the only admissible shape for the row.

## 3. Guard proof (the false-green the prompt warns about)

Fixture (`receipts/proof/`): a scratch copy of the registry
(`proof/SOURCES.indented-S167.md`) with the real staged `S167` row inserted after the table
separator as `  | S167 | … |` — two leading spaces, census-valid, indented.

- `--registry proof/SOURCES.indented-S167.md --staged $A` → `collisions` **nonempty, 9 ids**
  (`S153`–`S160` + `S167`), `held[S167]=S167`, `column0_miss=[]` because the staged side is not
  indented (`receipts/proof/guard-proof.json`).
- Same registry copy against a staged copy whose `S167` row is also indented
  (`proof/staged-indented.md`, row 21) → `collisions` still 9, but `column0_collisions` **8** and
  **`column0_miss=["S167"]`** (`receipts/proof/guard-proof-column0.json`): the column-zero pattern
  loses the indented collision, the guard's 0–3-space extractor keeps it.

Verdict on the guard: **not broken** — the indented collision produces a nonempty `collisions` file
both by `comm -12` on the 0–3-space extractor and by the tool. Nothing appends on the strength of a
column-zero census.

## 4. Quarantine slice (`absent-defect-register.md`, lane `tameshi`)

Slice (`receipts/quarantine-slice`, 17 rows): 14 `payload-absent` — `S105 S109 S110 S118 S119 S124
S126 S129 S131 S132 S137 S140 S141 S143` — plus 3 rows whose class cell reads "the cited source
could not be fetched, so no quote was checked" (`S113`, `S123`, `S134`; their id cell is malformed
with a trailing backtick). All 17 are `S105`–`S143`; the register's own note agrees:
`corpus/SOURCES.md:271` "Quarantine 0 (the tameshi slice S105–S143 intersects none)".

- **`S167` as an id: not in the tameshi slice.** The register's two `S167` rows belong to other
  lanes' packages — `kotoba` (`absent-defect-register.md:108`) and `tabi` (`:211`) — so a campaign
  id is package-local, not lane-global; `S167` here carries no tameshi meaning.
- **`S167`'s document: present, quarantined.** `absent-defect-register.md:219` —
  `| `tameshi` | round2 | S119 | `payload-absent` | https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf | `It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappea` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |`.
  Class meaning (`:13`): "every relevant source fetched cleanly and the quote is in none of them —
  the fabrication class: verify by hand, then correct the quote or refuse the row".

**Hand re-check of that hit (advisory, read-only fetch, `receipts/s167-source-check.txt`)**: the
mirror fetched cleanly this round, 247 738 B, sha256
`7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`, 17 pages, masthead "IEEE
TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002", title `zeller.txt:6`, authors
`:7`. The quarantined span is **present verbatim after whitespace collapse in reading-order text
(pdftotext, count=1)** and **absent from `-layout` text (count=0)** — the TSE page is two-column and
the sentence is split across the gutter ("…would cause" | "the failure to disappear"). The row's
other anchor facts also resolve: "896 lines" (`zeller.txt:18`, `:883`, `:892`) and "139 automated
test runs, or 35 minutes on a 500 MHz PC" (`:19`–`:20`).

So the `payload-absent` class on this document reads as a **layout-fold false positive of the quote
census, not a fabrication**: the staged row's quote is real in the mirror. Residual, reported not
resolved: (a) this is my byte snapshot of 2026-10-26, not the campaign's snapshot; (b) the row's
"p. 183-184" anchor cannot be confirmed from the mirror — the text layer carries 0 occurrences of
the folios `183`/`184`, so the page range is bibliographic only.

## 5. What the L1 gets from this

- Collision count 8, both id lists, guard verdict `answered`/`not refused`, `next_free=safe_floor=S271`.
- Adoption map, by document, admissible at exit 0: dedupe `S153→S105`, `S154→S106`, `S155→S261`,
  `S158→S262`, `S159→S155`, `S160→S156`; fresh `S156→S271`, `S157→S272`.
- Staged `S167`: no renumber entry; if its document is adopted this round it takes the next fresh id
  above the tail (`S271`, or `S273` after the two new collision rows), never `S167`, never `S175`.
- Two facts that bear on adopting `S167` at all (C2's F6 source row): the campaign register
  quarantines the document as `payload-absent` under the package id `S119`, and that class does not
  survive a hand re-check on the mirror bytes.

Risks / limits: the register's ids are campaign-package ids and drift from the staged ids
(`tameshi round2 S119` is this document; the current staged package calls it `S167`), so no
quarantine decision may be keyed on an id — only on the document. The safe floor `S271` is computed
against the registry as read today (`S270` max); any append landed by a sibling seat before this
round's adoption moves it.

## Summary

- Registry 130 ids (`S001`–`S270`), staged 103 (`S153`–`S255`), `comm -12` → 8 collisions `S153`–`S160`; guard agrees (`collision_count=8`, `verdict=answered`, `refused=false`, `next_free=safe_floor=S271`).
- Guard proof holds: an indented `  | S167 |` row in a registry copy yields 9 collisions, and with the staged row indented too `column0_miss=["S167"]` — the 0–3-space extractor catches what the column-zero pattern false-greens.
- By-document adoption map admissible at exit 0: dedupe `S153→S105`, `S154→S106`, `S155→S261`, `S158→S262`, `S159→S155`, `S160→S156`; fresh `S156→S271`, `S157→S272`.
- Staged `S167` collides with nothing (no registry row, and its document exists only as an unopened Lead at `corpus/SOURCES.md:278`): no renumber entry; adopted, it takes a fresh id above the tail, never `S167` (self-map refused) and never `S175` (arithmetic cascade refused).
- Quarantine slice: 17 tameshi rows, all `S105`–`S143`; id `S167` absent (the register's `S167` rows are kotoba/tabi), but its document sits at `absent-defect-register.md:219` as `payload-absent`.
- That quarantine class does not survive a hand re-check: the span is verbatim in reading-order pdftotext of the mirror (sha256 `7ed0c812…`) and absent only from `-layout` text — a two-column fold false positive, not a fabrication.
- Residuals: my snapshot is 2026-10-26, not the campaign's; the `p. 183-184` anchor is not confirmable from the mirror (0 folio occurrences).
