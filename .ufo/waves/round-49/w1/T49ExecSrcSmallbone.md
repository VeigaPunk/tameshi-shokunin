# T49ExecSrcSmallbone — S183 snapshot + citation check (Smallbone 2011)

Seat: source snapshot for C2 (milestone "C2 source snapshot"). Read-only on the lane; nothing
edited. This is a findings report, not a claim decision.

## Deliverables (all under `.ufo/waves/round-49/w1/`)

| file | sha256 / size |
|---|---|
| `T49ExecSrcSmallbone/lic.pdf` | `eaee48f930ba20a06824fe238cc6a42427e9fb45d1d70b852bf091ad6e44ac08`, 1 269 821 bytes |
| `T49ExecSrcSmallbone/lic.txt` (`pdftotext -layout`) | `613b62e8b68b6b508c527a40188fff925f2a63244b9b57f7638ade260ea7bcad`, 287 828 bytes |
| `T49ExecSrcSmallbone/receipt.json` | fetch receipt (url, final_url, http_status, bytes, sha256, fetched_at + extract metadata) |
| `T49ExecSrcSmallbone.json` | `{url, sha256, quotes:[{topic, quote, location, lic_txt_line, words, printed_page, pdf_page}]}` — 13 quotes, all verified verbatim, all ≤ 25 words |
| `T49ExecSrcSmallbone/pages/*.txt` | single-page `pdftotext -layout` extracts for printed pp. 3, 20, 34, 44, 45, 56, 57, 80, 87 |
| `T49ExecSrcSmallbone/checks.txt` | transcript of every page-anchored check below |

## Fetch

```
$ curl -sS -L -o lic.pdf -w 'http_status=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\nsize_download=%{size_download}\n' 'https://smallbone.se/papers/lic.pdf'
http_status=200
final_url=https://smallbone.se/papers/lic.pdf
content_type=application/pdf
size_download=1269821
$ sha256sum lic.pdf
eaee48f930ba20a06824fe238cc6a42427e9fb45d1d70b852bf091ad6e44ac08  lic.pdf
$ pdftotext -layout lic.pdf lic.txt      # pdftotext version 26.08.0 (poppler), curl 8.23.0
$ pdfinfo lic.pdf                        # Pages: 116, Producer: pdfTeX-1.40.10, Created 2011-01-25
```

`fetched_at`: `2026-10-26T20:32:43Z` (UTC, from `date -u` at fetch time).

Tool installs/upgrades this seat: **none** (poppler, curl already present; no `pacman` transaction run —
host guard respected).

## Document identity (matches the staged row's badges)

- `lic.txt:1` `Thesis for the Degree of Licentiate of Engineering`; `lic.txt:6-8` title, `lic.txt:12` author;
  `lic.txt:27-28` `Technical Report 76L`, `ISSN 1652-876X`, Chalmers CS&E. So the row's
  "Technical Report 76L, ISSN 1652-876X" is accurate, and the artefact is a **thesis compiling three
  papers**, not a single paper with one linear section numbering (`lic.txt:68` `Contents` + `lic.txt:71,78,89`
  `Paper I/II/III`, and the papers themselves restart at §1 at `lic.txt:278,393,519`).
- Page convention: printed folio = PDF page − 5 throughout (first non-empty line of PDF pp. 8, 17, 25, 39, 44, 49,
  50, 56, 61, 62, 85, 92 → folios 3, 12, 20, 34, 39, 44, 45, 51, 56, 57, 80, 87). All locations below give
  the printed page (what a citation consumer would expect) with the PDF page in parentheses.

## Finding 1 — the quoted words are verbatim, but they are in §2.10 "Generating Test Data", printed p. 34

`lic.txt:1792`: `good test data generators, that fit the program at hand. In our property-`
Section heading `lic.txt:1789`: `2.10     Generating Test Data`. The enclosing sentence is
`lic.txt:1790-1792`: "As always with random testing tools, the quality of the test data determines the
quality of the generated equations. As such, it is important to provide good test data generators, that
fit the program at hand."

Page proof:

```
$ pdftotext -layout -f 39 -l 39 lic.pdf - | grep -m1 -v '^$'   # → 34   (folio of PDF p.39)
$ pdftotext -layout -f 39 -l 39 lic.pdf - | tr '\n' ' ' | grep -c 'good test data generators, that fit the program at hand'
1
```

Cross-check with the document's own TOC: `lic.txt:74` `3  Case Studies . . . 34` — §3 opens on the same
page that carries the tail of §2.10, i.e. printed 34. **So the staged location "§4.1 …, p. 44" is wrong on
both coordinates.**

## Finding 2 — printed p. 44 carries no generator text at all

```
$ pdftotext -layout -f 49 -l 49 lic.pdf - | grep -m1 -v '^$'   # → 44
$ pdftotext -layout -f 49 -l 49 lic.pdf - | grep -ci 'generator' # → 0
```
`pages/p044_sec3.4-wrong-page.txt` starts `3.4   shr: Problems with Partiality` (`lic.txt:2302`). It is
about partiality in fixed-point case studies (shr/adjust), not about generators.

## Finding 3 — neither §4.1 in the document is about generators

- paper 2 §4.1 "A Parallel Correctness Criterion" — `lic.txt:2883`, printed p. 56 (PDF 61), generator hits on
  that page: `grep -ci generator` → `0`.
- paper 3 §4.1 "Automatic Ranking of Solutions" — `lic.txt:4452`, printed p. 87 (PDF 92), generator hits: `0`.
- paper 1 §4 "Related Work" (`lic.txt:2394`) has no 4.1 subsection.

The only generator-centred section in the thesis is **§2.10**; the nearest generator-titled 4.x is paper 2
§4.2 "Generating Parallel Test Cases" (`lic.txt:2924`, printed p. 57), which is about parallelising
`eqc_statem` cases, not about generator quality. A `§4.1` reference in this artefact is also intrinsically
ambiguous (three papers, each restarting at §1).

## Finding 4 — the row's own check cannot detect this, because it is location-blind

The S183 row (`SOURCES.append.md:37`) verifies with a whole-document grep:

```
$ pdftotext -layout lic.pdf - | tr '\n' ' ' | grep -c 'we have a range of test data generators for standard types'
1
```
That count is genuinely 1 (`lic.txt:1793-1794`), so the row's evidence line passes while the coordinates it
publishes are wrong. A presence check over a 116-page artefact cannot pin a page. Page-anchored form (run
here, not edited into the row — the row is the L1's to correct):

```
$ pdftotext -layout -f 39 -l 39 lic.pdf - | tr '\n' ' ' | grep -c 'we have a range of test data generators for standard types'
1
```

## Finding 5 — the staged *substance* is supported by the paper, with one strength overreach

Supported verbatim at §2.10, printed p. 34:

- `lic.txt:1790` "the quality of the test data determines the quality of the generated equations" — the row's
  "bounded by the quality of the generator" is a fair paraphrase of "determines".
- `lic.txt:1802-1803` "If one is not careful in defining the list generator, QuickSpec might end up producing
  the law isPrefixOf xs ys == null xs." — i.e. an inappropriate generator *does* yield a false law, matching
  "an inappropriate generator produces wrong laws".
- `lic.txt:1808-1811` the fix ("making sure that the generator used for random lists is likely to pick the list
  elements from a small domain") and "creating custom generators is sometimes necessary to get correct results".

Overreach: the row's "a fixture generator **must** be chosen per program" is stronger than the source, which
hedges in the next paragraph — `lic.txt:1811-1813` "…this does not happen often even if we are careless about
test data generation", because refinement continues until 200 split-free tests. The source says *sometimes
necessary*, not *always per program*.

**Verdict on the staged claim about p. 44: not accurate as a location.** The words exist in the paper and the
claim they are cited for is substantively right, but they sit in §2.10 "Generating Test Data" on printed
p. 34 (PDF p. 39), not in "§4.1 … p. 44"; printed p. 44 is §3.4 "Problems with Partiality" and contains no
generator discussion. Suggested corrected coordinates (for the L1 to apply, not applied here):
§2.10 "Generating Test Data", p. 34 (PDF p. 39).

## Finding 6 — other generator-quality / distribution / test-data-size passages (all in the JSON)

| printed p. (PDF) | section | line | quote |
|---|---|---|---|
| 3 (8) | thesis Introduction, "Random testing or exhaustive testing?" | 249 | we are just sampling the set of test data and it makes no difference how big that set is |
| 20 (25) | §2.3 Equivalence classes | 1082 | if no split has happened for the last 200 tests |
| 34 (39) | §2.10 Generating Test Data | 1793 | we have a range of test data generators for standard types, and a library of functions for building custom generators |
| 34 (39) | §2.10 | 1808 | making sure that the generator used for random lists is likely to pick the list elements from a small domain |
| 45 (50) | §3.4.1 Summing Up | 2367 | QuickSpec runs relatively few tests of each equation (several hundred) |
| 45 (50) | §3.4.1 Summing Up | 2371 | tweak the test data generator to get a better distribution of random data |
| 57 (62) | paper 2 §4.2 Generating Parallel Test Cases | 2946 | We avoid parallelizing too long a suffix (longer than 16 commands), to keep the number of possible interleavings feasible to enumerate |
| 80 (85) | paper 3 §1.0.1 Contribution | 4081 | the distribution of random tests is of almost no importance |

The last row is the interesting one for a gate-fixture generator: this author designs a grading method so
that "the distribution of random tests is of almost no importance" — a *contrast* with the §2.10 line that
distribution is decisive for law inference. Both are his; they are about different artefacts.

## Risks / limits of this snapshot

- Quotes are taken from `pdftotext -layout` text; hyphenated line breaks were avoided by choosing
  fragments that do not straddle a `-` break, so every quote in the JSON is a literal substring of `lic.txt`
  after whitespace normalisation (verified: `occurrences_in_text` ≥ 1 for each).
- Page numbers rely on the folio convention (printed = PDF − 5), spot-verified on the twelve pages listed above but
  not on every page of the artefact.
- The document is a thesis of three papers with restarting section numbers; any downstream reference should
  say *which paper* or use the thesis-level §2.10.
- Nothing in this snapshot says anything about the generator's behaviour or the hidden panel; no counter was
  run (beyond none), and nothing under `~/.local/state/` was read.
- **Timestamp provenance:** `receipt.json` `fetched_at` is genuine UTC, taken by `date -u +%Y-%m-%dT%H:%M:%SZ` in the
  same shell invocation as the `curl` (host TZ is America/Sao_Paulo, i.e. local 17:32-03). Independent
  corroboration, not my own re-run: seat `T49ScribeRows` fetched the same URL one minute later (20:33Z) and
  reports identical bytes/sha256 `eaee48f9…4ac08` / 1 269 821 B; that seat's first receipt draft had mislabelled
  its local clock as `Z` and was corrected in its own file (`.ufo/waves/round-49/w1/T49ScribeRows.src/`). No row
  text, quote or page number of mine changed.

## Summary

- S183 fetched clean: HTTP 200, 1 269 821 bytes, sha256 `eaee48f9…4ac08`, PDF + `pdftotext -layout` text + receipt + 13 verified quotes saved under `w1/T49ExecSrcSmallbone/`.
- The cited fragment "good test data generators, that fit the program at hand" **is** in the paper, at §2.10 "Generating Test Data", printed p. 34 (PDF p. 39), `lic.txt:1792`.
- The staged row's location "§4.1 …, p. 44" is **inaccurate**: printed p. 44 is §3.4 "Problems with Partiality" (0 generator mentions), and neither §4.1 in the thesis is about generators.
- The row's presence-only check still returns 1 over the whole document, so it cannot catch the mismatch; a page-anchored check is given.
- The staged *substance* (quality of equations bounded by the generator; inappropriate generator → wrong law) is supported verbatim at p. 34, except the row's "must be chosen per program", which is stronger than the source's "sometimes necessary".
- Extra distribution/size evidence recorded: pp. 3, 20, 45, 57, 80 — including "the distribution of random tests is of almost no importance" (p. 80) as a deliberate contrast to §2.10.
