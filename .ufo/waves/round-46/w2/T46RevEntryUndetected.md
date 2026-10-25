seat: T46RevEntryUndetected

item: Non-author claim-vs-source review of `corpus/knowledge/r5-undetected-flaky-failures.md` (row S259; snapshot `.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html`), per the item's checklist: quoted spans, token counts, locations, header trio + recheck run, numbers/names grounding, used-by cell, README index, package-copy diff.

Verdict: **ADMIT-WITH-FIXES** — ten located quotes verified by a method independent of the lane counter (python `html.parser`, whitespace-folded substring, my own occurrence counts); header, row linkage, indexing and all lane citations check out; the recheck command reproduces its stated result today. Two HIGH transcription/false-correction defects and three LOWs, all locally fixable; nothing attacks the C3 claim itself (fold-survival is what the counter tests, and it holds).

## Method (independent of `.ufo/evidence/round-46/coverage/measure.py`)

- `sha256sum .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html` → `5eb59adf099304a07059530b0857f7b517eaa72c832049f46952915a77e71a6f` (51,850 B).
- Own extraction: `html.parser` with `convert_charrefs`, `<script>`/`<style>` skipped, whitespace folded → `my-extract-all.txt` (head kept) and `my-extract-nohead.txt`. Lane extractor for comparison: `python3 .ufo/evidence/round-45/freshness/measure.py --extract <snapshot>` → 1 line, 1668 whitespace words (exit 0). The lane extractor is regex tag-strip + `html.unescape` + `fold()` (NFKC, ‘’→', –→-); it retains the embedded BibTeX/RIS blocks, so counts over it count all four abstract copies.
- Per quote: whitespace-folded substring test + `str.count` over (a) raw HTML, (b) my extract, (c) lane extract; whitespace token count by `len(q.split())`.

## Located quotes — all verify

| # | tokens (claimed / counted) | occurrences (claimed / mine raw / mine extract / lane extract) | package annotation check |
|---|---|---|---|
| 1 | 19 / 19 | 4 / 4 / 4 / 4 | absent ✓ |
| 2 | 15 / 15 | 4 / 4 / 4 / 4 | absent ✓ |
| 3 | 19 / 19 | 4 / 4 / 4 / 4 | absent ✓ |
| 4 | 18 / 18 | 3 / 0* / 0* / 3 | absent ✓ (package bolds mid-span) |
| 5 | 18 / 18 | 3 / 3 / 3 / 0* | "package bolds clause 2" ✓ |
| 6 | 14 / 14 | 4 / 4 / 4 / 4 | present ✓ (folded verbatim in package) |
| 7 | 9 / 9 | 4 / 4 / 4 / 4 | absent ✓ |
| 8 | 19 / 19 | 4 / 4 / 4 / 4 | absent ✓ |
| 9 | 16 / 16 | 3 / 3 / 3 / 3 | absent ✓ (package bolds mid-span) |
| 10 | 18 / 18 | 4 / 4 / 4 / 4 | absent ✓ |

\* See LOW-3: quote 4's straight `'` occurs only after `fold()` maps the snapshot's `’`; quote 5's en-dash `–` occurs in raw but the lane extraction folds it to `-` (its `grep -oF` count is 0; hyphen spelling counts 3). The entry's own line-32 disclosure of the dash behaviour is accurate: my counts `9.8 %–16.3 %`→0 (raw 3), `9.8 %-16.3 %`→3, `9.8 \%{\textendash}16.3 \%`→1 over the lane extraction.

## "Sits where the entry says" — all structural claims verified

- Four abstract copies: visible `<h2 class="subheader">Abstract</h2>` + `<p>Flaky tests produce…` at raw ~17364; BibTeX `abstract` field (field list checked: title/abstract/keywords/author/note/year/doi/language/journal/issn) ~36180; RIS `N2  - ` at 41111; RIS `AB  - ` at 42852. Escaped characters in the BibTeX copy: `{\textquoteright}` ×1, `{\textendash}` ×1, `{\texttimes}` ×1 — exactly the three sentences the entry says occur 3×.
- `class="open-access"`: ×1 in raw, on `<li class="open-access">` wrapping the DOI link (`§Access to Document`) — markup marker only, no visible licence text. Entry accurate.
- State `<span class="prefix">Accepted/In press - </span><span class="date">2026</span>` → backticked `Accepted/In press - 2026` fair rendering.
- Authors appear in order Fabian Leinen → Martin Gruber → Saadet Sena Erdogan → Andreas Stahlbauer → Alexander Pretschner in meta (`citation_author`), visible `<ul class="relations persons">`, BibTeX `author`, RIS `AU`. All five names located.
- `8.8 billion`, `four industry-scale`, `two-month`, `154,000`, `1.7 million` each ×4 in raw; `9.8` ×4; `3×` ×3 (en-dash/× occurrences per the escaped-copies rule).
- Lane extract equality: live fetch today (`sha256 bacd127f…`) extracts to byte-identical 1668 words vs snapshot extract — corroborates the entry's volatile-bytes note.

## Header trio

- Line 1 `source:` — row id S259, URL matches row URL verbatim, snapshot path exists, `sha256 5eb59adf…` matches computed digest (8-hex prefix `5eb59adf` also matches the SOURCES.md anchor). EXACT.
- Line 2 `verified-at: 2026-10-25` — EXACT.
- Line 3 `recheck:` — I RAN the printed command (output path moved into my scratch dir, identical semantics): digest `bacd127fee1a61277756aa29f14e2ce56229bf9b9b9fed892ed9e5f82c4bedbe` + ` | wc -l` → `4`. The stated count `4` reproduces; a third distinct digest corroborates the entry's "volatile bytes, drift signal = count" note rather than contradicting it.

## Registry / index linkage

- `corpus/SOURCES.md:134` row S259: used-by cell (last column) = `corpus/knowledge/r5-undetected-flaky-failures.md` exactly; anchor carries `sha256 5eb59adf` (8-hex).
- `corpus/README.md:574` indexes `` `knowledge/r5-undetected-flaky-failures.md` `` with row id `S259` in the last cell. Index paraphrase `9.8 %-16.3 %` uses the hyphen form — snapshot renders `9.8 %–16.3 %` (cosmetic; INFO-4).
- Committed entry is byte-identical to the frozen deliverable `.ufo/waves/round-46/w1/ScribeEntryUndetected.entry.md` (same read snapshot tag 02D3).

## Lane citations — all verified

- `corpus/README.md:80` F3 row text `one control per sweep` → `N ≥ 3 byte-identical controls, or a named mismatch` verbatim incl. `≥`; `:82` F5 row correct; `:127` scope sentence verbatim.
- `tools/repeat-control.py:18` contains `the environment is inherited unchanged` verbatim (docstring lines 17–18); `:94` contains `is not a determinism proof and it cures no flakiness` verbatim and does describe the clean `controls_match` verdict (lines 92–94).
- `corpus/knowledge/hermetic-env-differential.md:4` contains `F3 universal determinism and successor freshness remain unclaimed` verbatim; `:1-6` does describe varying one input / seven profiles / nine pinned surfaces / clean controls.
- `corpus/SOURCES.md:119` is the S107 TensorFlow Federated golden-tests row; `corpus/knowledge/repeated-control-precondition.md` and `tools/env-diff.py` exist.
- Package-quoted spans all verbatim in the package copy: `online date 2026-09-19`, `open access per the institutional record`, `one green control`, `round 1's \`S107\``, `` `aaron` has no copy of this DOI ``.

## Findings

### HIGH-1 — Entry mistranslates the affiliation name (line 12)
Snapshot renders `Informatics 4 - Chair of Software und Systems Engineering` (German "und"; ×2 raw: meta `citation_author_institution` + visible `relations organisations` link text). Entry prints `Informatics 4 – Chair of Software and Systems Engineering` — silently anglicised `und`→`and` (and -→–). Zero occurrences of `Software and Systems` in snapshot or extract; `Software und Systems` ×2/×1. A claimed grounded name that is not what the source says.
Fix: `Chair of Software und Systems Engineering` on line 12 (keep or restore the hyphen separator).

### HIGH-2 — The "no publication day" correction is itself under-grounded (lines 13 + 58)
Entry: "The snapshot carries no publication day: `grep -c '2026-09-19'` → `0`" and §"the snapshot has no such string … Corrected here." The grep is literally true — but the snapshot carries `<meta name="citation_online_date" content="2026/09/19">` (×1, verified; `citation_publication_date` is year-only `2026`). The package's "online date 2026-09-19" was right in substance, wrong only in separator. The entry discredits a substantially true claim and over-corrects: the record does name an online-publication day — in markup, with `/` separators.
Fix: keep the visible-text correction but acknowledge the markup, e.g. "no visible publication day; the markup carries `citation_online_date` `2026/09/19`, which the package rendered as `2026-09-19`" (lines 13 and 58 in parallel).

### LOW-1 — Keyword case (line 14)
Snapshot keyword is `Flaky tests` (capital F; meta `keywords` and visible `userdefined-keyword` both capitalised). Entry lowercases to `flaky tests`.
Fix: `Flaky tests`.

### LOW-2 — Stale line citation (line 54)
`tools/env-diff.py (the contract and --selftest forms named at corpus/knowledge/hermetic-env-differential.md:6)` — line 6 is the title `# Hermetic environment differential — …`; the `env-diff.py --contract` / `--selftest` recheck is line 3.
Fix: cite `:3`.

### LOW-3 — "verbatim" quote 4 fails a literal verbatim test (line 24)
Snapshot renders `projects’ original CI` (curly `’`, ×3 raw); the printed span uses `'` which occurs 0× in raw. The stated count basis (`fold()` of quote + extraction, which maps `’`→`'`) is honoured, and the counter's own `fold()` makes it operationally fine — but the header "verbatim" is only true post-fold for this one span, while quote 5's en-dash IS literally verbatim. Inconsistent verbatim standard, transparently disclosed basis.
Fix (optional): one clause in line 19 noting that `'`/`–`/`×` spellings are counted post-`fold()`; or print `projects’` curly. Cosmetic.

### INFO-1 — Line 47 self-quote `"N ≥ 3 controls that agree while the environment tuple varies"`
Entry's own proposed wording quoted inside an `Inference:` bullet; not a snapshot substring and not claimed as one. Stylistic only.

### INFO-2 — README index paraphrase hyphen `9.8 %-16.3 %` vs snapshot en dash (README:574). Cosmetic.

### INFO-3 — Recheck ran: digest `bacd127f…` ≠ both stated digests, count `4` as stated; live extract identical to snapshot extract (1668 words). The entry's volatile-bytes framing is confirmed, not refuted.

## Package-copy diff (package `S190` staged → entry `S259`)

Dropped by the entry (with verdict): title overstatement `the same mechanism that misses most flaky failures` (the 9.8–16.3 % scope is failed pipeline runs, not "most flaky failures") — dropped, correct; `online date 2026-09-19` — dropped but see HIGH-2 (over-corrected); `open access per the institutional record` — corrected to markup marker, correct; `round 1's S107` misattribution — corrected to README:80 + `repeated-control-precondition.md`, correct (S107 verified as the TFF golden-tests row); package's `six gate selftests` F5 claim — replaced by the hermetic entry's own description (seven profiles / nine pinned surfaces), better-grounded; `` `aaron` has no copy `` — carried as unverified, unused, correct.

Added by the entry: located quotes 1–4, 7–10 (all verified, incl. dataset figures 154,000 / 1.7 million and the definition quote 1); the four-copy abstract mechanics + escape accounting; lane-file citations (`repeat-control.py`, `env-diff.py`, `hermetic-env-differential.md`); the F3 protocol restatement with a named falsifier (controls agreeing in one environment, disagreeing across two); the explicit not-carried section (no per-project breakdown, no method section — consistent with the snapshot, which carries only abstract + metadata + citation blocks + fingerprints boilerplate).

## Contract-level check

C3 entry requirements for this row: located ≥1 6–25-token quote (10, sizes 9–19 all in band) ✓; ≥1 located quote absent from the package copy (8 of 10, verified absent as folded literal spans) ✓; `verified-at ≥ 2026-10-25` ✓; used-by cell + README index ✓; adopted id S259 per `adoption-map.json` ✓. The fold-apostrophe nuance (LOW-3) does not threaten the counter: it folds both sides.

## Unrun / out of scope

- No verdict run of `.ufo/evidence/round-46/coverage/measure.py` (deciding run is the L1's); only the `--extract` seat-helper mode of the round-45 counter was used, plus my own parser.
- No mutation of the lane, package, or fleet repos; scratch at `/tmp/tameshi-r46-T46RevEntryUndetected/` (extracts, live fetch).
- No tools installed or upgraded (pacman paused host-wide; none needed).

## Residual risk

- Severity counts: 2 HIGH, 3 LOW, 4 INFO (INFO-3 = recheck receipt). Refuse-condition not met: every defect is a bounded transcription/citation fix; the claim-vs-source core (10/10 quotes, header, recheck, row linkage) survives attack.
- If the L1's deciding counter run fails for unrelated rows, this review does not cover that; scope was this entry only.
