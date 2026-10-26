# T47ScoutQuarantine — quarantine slice re-derivation and row check

## Slice re-derivation (observed)

Command (as given) against `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, output kept at `/tmp/tameshi-r47-T47ScoutQuarantine/slice.txt`.

- Count: **17** rows. `diff` against `.ufo/evidence/round-46/assimilation/quarantine-slice`: **identical** (no row added, dropped or reclassified since round 46).
- 14 `payload-absent` (register lines 215-228): S105, S109, S110, S118, S119, S124, S126, S129, S131, S132, S137, S140, S141, S143.
- 3 `the cited source could not be fetched, so no quote was checked` (register lines 363-365): S113, S123, S134. Their awk column 4 prints as `S113`` etc. (the register's own row has a stray backtick in the id cell), the same as the committed slice.
- Rounds: S105/S109/S110/S113/S118 = round1; S119/S123/S124/S126 = round2; S129/S131/S132 = round3; S134/S137 = round4; S140/S141/S143 = round5.

## Overlap with this round's adopted rows

**No slice id is one of S155, S158, S206, S207, and none is S160.** The slice stops at S143. Nothing the package entries cite by `source:` id (S155, S158, S160, S206, S207) is in the tameshi quarantine slice; the package-entry `source:` lines carry only those five ids, and the entries' prose also names S152 (held, `mined`), S205 and S208 (neither is in the slice).

Cross-lane note: the register has other lanes' payload-absent rows at the staged ids: `kake` S206, `kama` S206, `tabi` S158 (register lines 91, 94, 206). They are other lanes' ids that happen to equal staged ids; they say nothing about tameshi's rows, but they confirm the staged ids are shared with other lanes and must be re-pointed by document (the contract says so).

### The one document-level overlap: S110 = the Lam camera-ready PDF = staged S158

- Slice row S110 (round1): URL `https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf`, quote `one can use ≤ 5 reruns (50% less than Google's default ten reruns [6]) and still check correctly ≥ 82% of the time.` — status `payload-absent`.
- Staged S158 (package `flaky-aware-verdict-evidence.md` `source:` line 3, `SOURCES.append.md` line 12) is the **same URL** and the same quote. Round 40/42 already recorded S110 as "present, verbatim; adopt-eligible, not appended" (`corpus/lessons/round-40.md` line 57; `.ufo/waves/round-42/w1/ScoutQuarantine.md` line 25). No S110 row is in `corpus/SOURCES.md` now (120 `| S` rows, none S110, none by Lam), so S110 is quarantine-only and S158→S262 is the row that will hold that document.
- Does the fresh snapshot resolve it? **Yes, with a fold.** Committed `coverage/sources/lam-2020-reruns.pdf` (sha256 prefix `0b880458`) with `pdftotext` (non-layout mode) then whitespace-collapse gives the staged quote contiguous and byte-exact, **with the PDF's curly apostrophe `Google’s`** (count 1). The ASCII `'` in the register/staged quote is the likely cause of the register's payload-absent (fold: `’`→`'`). The committed `lam-2020-reruns.txt` (81725 B) is a layout-mode extraction in which the two columns interleave: the sentence there reads `…Google's default ten conducted surveys of developers after the tests were fixed and reruns [6]) and still check correctly ≥ 82% of the time`, so the full quote is **not contiguous in the .txt**; only fragments are (`one can use ≤ 5 reruns`, `50% less than Google's default ten`, `still check correctly ≥ 82% of the time`). The second quote in the entry (`run tests in a test suite instead of in isolation, and run tests in different orders with fewer times each, rather than fewer orders with more times each`) is likewise absent from the .txt (column interleave, `…in different` / `orders with fewer times each, rather than fewer orders with` split) but is contiguous in the non-layout `pdftotext` of the PDF (count 1).
- **Consequence for the counter/row author:** the fourth (uncounted) row and the entry's quotes should be located against the PDF's non-layout extraction, or the `.txt` snapshot should be regenerated without `-layout`; locating the full quote in `lam-2020-reruns.txt` as committed fails. This is not a refusal: the quote is present in the PDF.

## Staged rows' quotes vs. fresh snapshots (not in the slice, checked as asked for entry `source:` rows)

| staged | adopted id | snapshot | quotes located |
|---|---|---|---|
| S155 (arXiv 2302.09330) | S261 | `arxiv-2302.09330-abs.html` | `does not require additional reruns, since it gathers this data from existing test executions`, `the tests' outcomes and durations, as well as basic information about the code evolution`, `without such requirements on the underlying` — all present (HTML-unescaped). Not in quarantine. |
| S158 (Lam PDF) | S262 | `lam-2020-reruns.pdf` / `.txt` | see above: present in the PDF (non-layout), not contiguous in the layout `.txt`. Same document as quarantined S110. |
| S206 (arXiv 2607.09345) | S263 | `arxiv-2607.09345-abs.html` | title, `15 pages, 7 figures, under review`, `not a static property`, `found that widely used benchmarks contain shortcuts that inflate reported F1 scores`, `evaluation protocols overstate generalizability` — all present. Not in quarantine (the register's S206 rows belong to kake and kama). |
| S207 (S2 record) | S264 | `s2-icst24-cost-of-flaky.json` | title, year 2024, DOI `10.1109/ICST60714.2024.00037`, DBLP `conf/icst/LeinenEPSSJ24`, and the abstract quotes (`at least 2.5% of`, `Contrary to most other studies, we find the cost for rerunning tests to be negligible and`, `not rerunning and thus letting the pipeline fail results in a manual investigation costing`) — all present. Not in quarantine. |
| S160 (PIT FAQ, cited by `flaky-aware-verdict-evidence.md` `source:` line 4) | — | **no fresh snapshot** (not one of the four rows this round adopts) | quote `Both these measurements can be affected by external factors…` cannot be resolved from round-47 sources; the lane's held S160 is a different document (Stryker equivalent mutants, corpus/SOURCES.md line 130). Not in the quarantine slice; **S160 is a held-id collision**, so the entry's `source: S160` must be re-pointed or dropped (a document without a registry row in this round). Not a refusal of a slice row — a gap to note for the entry author. |

Two entry strings flagged absent by my scan are not source quotes: `one control per sweep → N ≥ 3 byte-identical controls…` (lane's own text) and `re-sweep versus no re-sweep` / `re-sweep versus a human investigating a red build` (paraphrase labels in `r8-flaky-cost-baseline.md`, not in the S2 record).

## Refusal candidates

None among the staged S155/S158/S206/S207 rows: every quoted span of the three entries located in its fresh snapshot (S158 only via the PDF non-layout extraction). Open gaps: (1) S160 snapshot absent and its id is held by the lane for another document; (2) `lam-2020-reruns.txt` is a layout-mode extraction with column interleave, so contiguous-quote locating against that file fails.

No register row was appended; the lane was not edited. Tooling: `pdftotext` (poppler) already installed; nothing installed.
