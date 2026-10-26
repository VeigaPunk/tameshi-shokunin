# T49ScribeRows — C2 SOURCES rows (round 49, wave 1)

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `8ca67421111fa354b47b803358391d0b07fc6db9`.
Item: draft the two C2 source rows in the lane registry's 11-column schema, ids continuing the
registry, validated in a scratch mirror. This seat decides no claim: the rows are deliverable
text for the L1 to append; nothing under the lane checkout was edited.

## Rows (append under `## Registry`, after `corpus/SOURCES.md:143`)

```
| S269 | QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs (Claessen, Hughes; ICFP 2000; DOI 10.1145/351240.351266) — https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf | paper | A | F10 PBT generator craft — a property is a Haskell predicate the tool applies automatically to randomly generated input, and the tool reports the test-data distribution that reveals generator bias | Abstract, first paragraph (p. 268) and §2.4 Monitoring Test Data (p. 270) @ ICFP 2000, journal pp. 268-279 (Crossref), author-served PDF fetched 2026-10-26, sha256 bfddcaa6, snapshot .ufo/waves/round-49/w1/T49ScribeRows.src/quick.pdf | properties are Haskell functions tested automatically on random input, custom test-data generators can be defined, and classify/collect print each case's classification or a value histogram so a generator's distribution is visible | mined | 2026-10-26 | 365d | corpus/knowledge/pbt-generator-pilot.md |
| S270 | Property-based testing for functional programs (Smallbone; Chalmers University of Technology Technical Report 76L, ISSN 1652-876X, 2011) — https://smallbone.se/papers/lic.pdf | paper | B | F10 generator craft — the generator bounds which laws a random search can reach, an author's own report on QuickCheck-family generator quality and distribution | §2.10 Generating Test Data, p. 34 @ Technical Report 76L, 2011, author-served PDF 117 pp fetched 2026-10-26, sha256 eaee48f9, snapshot .ufo/waves/round-49/w1/T49ScribeRows.src/smallbone.pdf | generator quality bounds the search: an ill-fitting list generator never produces the cases that separate two functions, and drawing elements from a small domain fixes it | mined | 2026-10-26 | 365d | corpus/knowledge/pbt-generator-pilot.md |
```

Field shape checked on the mirror: `awk -F'|' '/^\| S269 |^\| S270 /{print $2, "NF="NF}'`
→ ` S269  NF=13`, ` S270  NF=13` (11 columns, no literal `|` in any cell; `usedby_findings`
in `scripts/sources-census.sh:538-570` splits the used-by cell on `,` (line 562) and takes
`corpus/knowledge/pbt-generator-pilot.md` as one path).

Controlled values used: `paper`, tier `A`/`B`, status `mined`, opened `2026-10-26`,
recheck `365d` (both carriers are stable primary/author documents; the registry uses `365d`
for papers, e.g. `corpus/SOURCES.md:133` S258). `used-by` is `pbt-generator-pilot`; the L1
appends any package entry it admits.

## Id derivation (computed, not assumed)

- Registry maximum by the census-valid 0-3-space extractor:
  `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -V | tail -1`
  → `S268`. The column-zero extractor gives the same `S268`; there are no indented rows today.
- `python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json`
  (receipt `.ufo/waves/round-49/w1/T49ScribeRows.src/guard.json`) → `registry_max S268`,
  `next_free S269`, `safe_floor S269`, `staged_max S255`, `registry_rows 128`, `staged_rows 103`,
  `registry_sha256 7e99c6a0…`, `verdict answered`.
- Ids chosen: **S269** and **S270** — above the registry max (S268) and above the staged max
  (S255), so neither id is a staged id and neither can collide. Guard after appending both rows
  to the mirror (`.ufo/waves/round-49/w1/T49ScribeRows.src/guard-after-append.json`):
  `registry_max S270`, `next_free S271`, `safe_floor S271`, `registry_rows 130`,
  `collisions ["S153"…"S160"]` (unchanged), `column0_miss []`.

## 0-3-space collision check (contract `frontier_step`)

Commands and output in `.ufo/waves/round-49/w1/T49ScribeRows.src/collision-probe.out`:

- `grep -oE '^ {0,3}\|…' corpus/SOURCES.md | … | sort -V > reg-ids` → 128 ids; same over the
  staged package → 103 ids; `comm -12 reg-ids staged-ids` → **8 ids, S153–S160**.
  The staged ids S182 and S183 are **not** in that set:
  `grep -cE '^ {0,3}\|[[:space:]]*S18[23][[:space:]]*\|' corpus/SOURCES.md` → `0` (exit 1).
  So the package's S182/S183 collide with nothing only because the check was run: their ids
  still may not be reused, since they *are* staged ids (the registry's `Next unused id` note,
  `corpus/SOURCES.md:490`, reserves S161–S255 by document).
- Indented-row proof on a scratch copy (`probe.md`): appending `  | S182 | … |` puts S182 in
  the 0-3-space collision set, while the column-zero extractor still reports 8 collisions and
  misses it — the strict extractor is the one used above.

## Gate

Rule 1 of the SOURCES contract: for every new row, the URL, the access date and a ≤25-word
quote with its location. Both documents were opened by this seat on 2026-10-26; the bytes are
committed under `.ufo/waves/round-49/w1/T49ScribeRows.src/` and hash-pinned in the rows.

### S269 — QuickCheck, ICFP 2000

- URL: `https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf` — HTTP 200,
  194,315 B, sha256 `bfddcaa648f836e50804910fc0956cc037c1a8b3e3d6716fb12e4e1ffdcb5172`
  (`curl -sS -L -o quick.pdf -w '%{http_code} %{url_effective} %{size_download}\n'`,
  receipt `.ufo/waves/round-49/w1/T49ScribeRows.src/fetch-receipts.json`). Access date
  **2026-10-26**; fetch moment 2026-10-26 17:33 -03 = **20:33Z** (host TZ America/Sao_Paulo;
  minute precision). The carrier is the article text (ICFP '00 copyright block on p. 1), so tier A.
  Journal pp. 268-279 confirmed against Crossref:
  `curl -sSL https://api.crossref.org/works/10.1145/351240.351266` → `page 268-279`
  (`.ufo/waves/round-49/w1/T49ScribeRows.src/crossref.json`).
- Quote 1 (14 words), location: Abstract, first paragraph, p. 268 (PDF p. 1, lines 12-14 of
  `T49ScribeRows.src/quick-p1-abstract.txt`, soft hyphens removed):
  > Properties are described as Haskell functions, and can be automatically tested on random input
- Quote 2 (20 words), location: §2.4 Monitoring Test Data, p. 270 (PDF p. 3, lines 31-32 of
  `T49ScribeRows.src/quick-p3-2.4-monitoring.txt`):
  > The combinator collect will gather all values that are passed to it, and print out a histogram of these values
- Verbatim check: both strings tested against the extracted text after dehyphenation
  (`t.replace('-\n','')` then whitespace collapse) → `True` for both; word counts 14 and 20.

### S270 — Smallbone, Chalmers TR 76L (2011)

- URL: `https://smallbone.se/papers/lic.pdf` — HTTP 200, 1,269,821 B, sha256
  `eaee48f930ba20a06824fe238cc6a42427e9fb45d1d70b852bf091ad6e44ac08`
  (receipt `.ufo/waves/round-49/w1/T49ScribeRows.src/fetch-receipts.json`). Access date
  **2026-10-26**; fetch moment 2026-10-26 17:33 -03 = **20:33Z** (minute precision), and the
  bytes are independently confirmed: seat `T49ExecSrcSmallbone` fetched the same URL at
  2026-10-26T20:32:43Z and reports the identical sha256 and 1,269,821 B, so the page mapping
  is citable from either copy (`fetch-receipts.json` field `corroboration`). Tier B as the
  item fixes it: the author's own licentiate report (Technical Report 76L, ISSN 1652-876X),
  117 PDF pages.
- Quote 1 (19 words), location: §2.10 Generating Test Data, printed p. 34 (PDF p. 39,
  `T49ScribeRows.src/smallbone-p34-2.10.txt:19-20`; the page's printed number is line 1):
  > As always with random testing tools, the quality of the test data determines the quality of the generated equations
- Quote 2 (15 words), same paragraph, p. 34 (`smallbone-p34-2.10.txt:20-21`):
  > it is important to provide good test data generators, that fit the program at hand
- Verbatim check: both strings → `True` after whitespace collapse; word counts 19 and 15.
  The paragraph continues on p. 34 with the list-generator failure (isPrefixOf vs null) that
  the `teaches` cell summarises (`smallbone-p34-2.10.txt:26-38`).

## Census validation in the scratch mirror

Mirror built as the item prescribes (scratch root
`/fast/scratch/hyaku/tameshi-r49/T49ScribeRows`, `S`):

```
cp -a /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus "$S/v/corpus"
# rows inserted immediately after the `| S268 |` line (mirror line 143)
```

`tools/tally-audit.py` and `tools/tally-audit-v3.py` were also copied into `$S/v/tools/`,
because `--file` resolves a used-by path against `$(dirname file)/..` =
`scripts/sources-census.sh:501` and three pre-existing rows (S097, S102, S104) point at those
two tools; without them the mirror reports false E11s that have nothing to do with these rows.

### Run A — rows as they would land, pilot entry not yet written

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/v/corpus/SOURCES.md"`
→ **exit 1** (full output `T49ScribeRows.src/validate-A2.out`), the only E-codes being:

```
file	E11	S269 missing used-by corpus/knowledge/pbt-generator-pilot.md
file	E11	S270 missing used-by corpus/knowledge/pbt-generator-pilot.md
```

### Run B — same mirror plus a scratch-only placeholder at that path

Placeholder content: `scratch-mirror placeholder for E11 path resolution only — the pilot entry
is authored by the C2 integration seat, not by this row seat`. Same command → **exit 0**
(`T49ScribeRows.src/validate-B.out`, 16 `file` records: 1 `ok` line plus 15 warnings):

```
file	ok	/fast/scratch/hyaku/tameshi-r49/T49ScribeRows/v/corpus/SOURCES.md
```

The 15 warnings are pre-existing lane warnings (W04 duplicate-url pairs including S047/S048/S265/S266/S267/S268, W01 S101); the two new rows produce no E-code and no W-code. Exit 0 means
schema, enums, tier, status, ISO dates, recheck cadence, id uniqueness and used-by resolution
are all clean for S269/S270.

## Findings

1. **The package's S183 anchor is wrong; the words are real but on a different page.**
   The staged row (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:37`) anchors
   "good test data generators, that fit the program at hand" at "§4.1 … p. 44". Those words are
   in **§2.10 Generating Test Data, printed p. 34** —
   `T49ScribeRows.src/smallbone-p34-2.10.txt:18-21` (heading line 18, words lines 20-21);
   shown by `pdftotext -layout smallbone.pdf smallbone.txt` plus a page map
   (`printed = PDF page - 5`; the extract's line 1 is the printed number `34`).
   Printed p. 44 is **§3.4 "shr: Problems with Partiality"** —
   `T49ScribeRows.src/smallbone-p44-3.4.txt:3-4`; §4.1 ("A Parallel Correctness Criterion")
   begins on printed p. 56 (PDF p. 61, first extracted line `56`). The S270 row anchors §2.10
   p. 34, so the row is correct even if the package's citation is not.
   The document is a three-paper thesis, so "§4.1" cannot identify the place by itself: a
   `-layout` extraction of the committed PDF carries two such headings,
   `4.1 A Parallel Correctness Criterion` and `4.1 Automatic Ranking of Solutions`
   (`T49ScribeRows.src/headings-4.1.out`; `pdftotext -layout smallbone.pdf -` then
   `grep -nE '^[0-9]+(\.[0-9]+)*\s+[A-Z]' | grep '4\.1'` → lines 2883 and 4452), neither about
   generators; printed p. 44 has no generator text at all
   (`pdftotext -layout -f 49 -l 49 smallbone.pdf - | grep -ci generator` → `0`).
   Seat `T49ExecSrcSmallbone` reports the same coordinates independently (§2.10 p. 34,
   lic.txt:1789/1792; p. 44 = §3.4 at lic.txt:2302; snapshots under
   `T49ExecSrcSmallbone/`), which is non-author corroboration of F1, not a re-run by this seat.
2. **The package's S182 page range is right.** Crossref returns `page 268-279` for
   DOI 10.1145/351240.351266 (`T49ScribeRows.src/crossref.json`), matching the staged row's
   "pp. 268-279"; the abstract is p. 268 and §2.4 is p. 270. (dblp was not usable —
   `https://dblp.org/rec/conf/icfp/ClaessenH00.xml` answered HTTP 202 with an anti-bot body.)
3. **Staged ids S182/S183 do not collide, but they may still not be reused.** The 0-3-space
   `comm -12` gives S153–S160 only (`collision-probe.out`), and the guard reports
   `collisions ["S153"…"S160"]`, `column0_miss []`; S182/S183 are staged ids of other
   documents, so the rows take S269/S270, which are above both maxima (S268 registry,
   S255 staged) and at/above the guard's `safe_floor S269`.
4. **E11 is the one open condition for these rows.** Until
   `corpus/knowledge/pbt-generator-pilot.md` exists, `sources-census.sh validate` exits 1 on
   S269/S270 (`validate-A2.out`); it exits 0 as soon as that path exists (`validate-B.out`).
   The integration step that writes the pilot entry closes it; no row text change is needed.
5. **Tier and quote discipline.** S269 is tier A only because the carrier is the article
   (copyright block on PDF p. 1) and not a secondary summary; S270 is tier B as the item
   requires even though the author is primary for his own report — the scope cell scopes the
   tier to F10 generator craft, per the contract's "tier is scoped to `scope`".
6. **Both rows are `mined`, so their used-by must resolve or E11 fires** — a `queued` status
   would silence the check but would also misreport the C2 claim's sourcing; `mined` is the
   honest status once the pilot entry cites them.
7. **Integration detail for the L1:** the registry's trailing note "Next unused id: S265 …"
   sits at `corpus/SOURCES.md:490` and is already stale for the frozen rows above it; once
   S269/S270 land it must read **S271**, which is the guard's `next_free` after the append
   (`T49ScribeRows.src/guard-after-append.json`).

## Corrections

- The first draft of `T49ScribeRows.src/fetch-receipts.json` recorded the fetch moment as
  `2026-10-26T17:33:00Z` — that was the host local clock reading (-03, TZ America/Sao_Paulo)
  mislabelled as UTC. Corrected in place: `fetched_at_utc 2026-10-26T20:33Z` plus a
  `fetched_at_local` field, and byte identity re-checked on the committed snapshots
  (`date -u` → `Mon 26 Oct 2026 08:38:37 PM UTC`; `stat`/`sha256sum` on both PDFs). No row
  text, quote, hash or page number changed, and the rows' `opened` date 2026-10-26 holds in
  both clocks.
- A peer challenge (seat `T49ExecSrcSmallbone`, fetch at 2026-10-26T20:32:43Z, taken from
  `date -u` in the same shell call as their curl) produced the independent byte confirmation
  recorded in the S270 gate; their observation is attributed, not presented as this seat's own
  run, and their clock agrees with mine (local 17:32-03 vs 17:33-03). Their independent
  snapshot, page extracts and quote index sit at `.ufo/waves/round-49/w1/T49ExecSrcSmallbone/`,
  `T49ExecSrcSmallbone.json` and `T49ExecSrcSmallbone.md`.

## Bounds observed

- Lane checkout read-only: no write outside `.ufo/waves/round-49/w1/T49ScribeRows.md` and
  `.ufo/waves/round-49/w1/T49ScribeRows.src/`. `contract.json`, `corpus/SOURCES.md`, the
  counters, the package and the evidence dirs were read, never edited; no `git`/`jj` mutation
  was run (the mirror is a plain `cp -a`, no repository).
- Never read `/home/vgpnk/.local/state/`, `c2-WITNESS.stdout`, `c2-CTL_FIX.stdout`,
  `c2-CTL_ABSENT.stdout`; the panel stayed hidden. No model was passed.
- No tool installed or upgraded: `curl` and `pdftotext` were already present (curl 8.x,
  poppler); the pacman guard was not exercised.
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49ScribeRows/` deleted after the evidence copy;
  no `/tmp` path is cited.

## Evidence paths (all under `.ufo/waves/round-49/w1/`)

- `T49ScribeRows.md` — this report.
- `T49ScribeRows.src/quick.pdf`, `smallbone.pdf` — the pinned bytes read.
- `T49ScribeRows.src/quick-p1-abstract.txt`, `quick-p3-2.4-monitoring.txt`,
  `smallbone-p34-2.10.txt`, `smallbone-p44-3.4.txt` — page extracts holding the quotes and the
  page-44 disproof.
- `T49ScribeRows.src/fetch-receipts.json`, `crossref.json`, `headings-4.1.out` — fetch and DOI
  metadata receipts, and the two-§4.1 disambiguation output.
- `T49ScribeRows.src/guard.json`, `guard-after-append.json` — staged-id guard before/after.
- `T49ScribeRows.src/reg-ids`, `staged-ids`, `collisions`, `collision-probe.out` — 0-3-space
  check and the indented-row proof.
- `T49ScribeRows.src/validate-A2.out`, `validate-B.out` — census exit 1 / exit 0 runs.
- `T49ScribeRows.src/rows.md` — the two rows as appended in the mirror.

## Summary

Two rows drafted: S269 QuickCheck (ICFP 2000, tier A, article carrier) and S270 Smallbone
(TR 76L, tier B), both `mined`, opened 2026-10-26, recheck 365d, used-by
`corpus/knowledge/pbt-generator-pilot.md`, no literal pipe in any cell.
Ids computed: registry max S268, next free S269/S270, above staged max S255; 0-3-space collision
set is S153–S160, so S182/S183 collide with nothing (indented-row probe proves the extractor).
Quotes opened and verified verbatim on 2026-10-26, ≤25 words each, located (pp. 268/270; p. 34).
Mirror `validate`: exit 1 with only E11 for the two rows until the pilot entry exists; exit 0
once that path is present — the rows themselves are clean.
Finding: the package anchors S183's words at §4.1 p. 44, but they are §2.10 p. 34 (p. 44 is
§3.4); S182's pp. 268-279 is confirmed by Crossref.
