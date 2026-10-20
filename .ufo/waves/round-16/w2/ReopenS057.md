# ReopenS057 — source re-open (round 16, wave 2)

Seat: `TameshiR16.ReopenS057` (leaf, no dispatch).
Target: S057 row `corpus/SOURCES.md:66` and its Gate quote
`corpus/lessons/round-16.md:38`, both read at
`c699c8c36d6e4eca4b796b81a8247904aa145ec8` (= lane HEAD).
Scratch: `/tmp/tameshi-r16w2-ReopenS057-CajvSK`.
Tools installed/updated: none.

## 1. Source actually opened

```
curl -sS --max-time 120 -o survey.pdf <row URL>   # HTTP 200, 1,129,278 B
```
- Re-fetch with a browser UA: HTTP 200, same 1,129,278 B; `cmp survey.pdf survey2.pdf` → rc 0, IDENTICAL.
- `sha256sum` = `63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023`.
- `md5sum` = `ee9eebefd06f0c98566806778c6ef0c1`; HTTP `content-md5:
  7p7r79BvDJhWaAZ3jG7wwQ==` decodes to the same digest.
- `pdfinfo`: 153 pages, `CreationDate: Thu Dec 14 19:37:04 2017 -02`,
  Producer `pdfTeX-1.40.17`.
- Page 1: title "Mutation Testing Advances: An Analysis and Survey", authors
  Papadakis, Kintis, Zhang, Jia, Le Traon, Harman — matches the row's author
  list and order. Page-1 footer: `Preprint submitted to Journal of LATEX
  Templates    December 14, 2017` → "author preprint" and the 2017-12-14 date
  hold (observed; the venue named by the row is not printed in the PDF).

## 2. Gate quote — `corpus/lessons/round-16.md:38`

Cell text (extracted programmatically from the committed bytes):

> `"Detecting equivalent mutants is a well-known undecidable problem" (§5.3.1, p. 29, preprint)`

- Word count: **8** (`len(quote.split())`), ≤25 required.
- `pdftotext -f 29 -l 29 -layout survey.pdf p29.txt`:
  - `p29.txt:5` → `5.3.1. Identifying Equivalent Mutants`
  - `p29.txt:6` → `Detecting equivalent mutants is a well-known undecidable problem [28]. This`
  - last non-empty line of `p29.txt` → `29` (printed folio).
- Programmatic `quote in p29_text` → **True**; normalized whole-document text
  also contains it (`survey.txt:1075`).
- The bracketed reference `[28]` is elided after "problem"; wording,
  hyphenation (`well-known`) and punctuation are otherwise exact.
- Physical PDF page 29 and printed page 29 coincide, so "p. 29, preprint"
  needs no offset convention.

## 3. Registry anchor — `corpus/SOURCES.md:66`

Row fields (`awk -F'|'` on the committed file; NF=13, 11 cells): kind `paper`,
tier `B`, scope `equivalent-mutant problem and mutant selection (survey
scope)`, anchor `§5.3.1 p. 29 @ preprint dated 2017-12-14 (published text not
reached; DOI 10.1016/bs.adcom.2018.03.015)`, status `mined`, opened
`2026-10-20`, recheck `365d`, used-by
`corpus/knowledge/mutation-case-kumitate-round-gate.md`.

Anchor resolution:
- §5.3.1 / p. 29 → verified above (§2).
- Preprint date → PDF `CreationDate` and page-1 footer (§1).
- "published text not reached" → independently reproduced:
  `https://www.sciencedirect.com/science/article/abs/pii/S0065245818300305`
  → **HTTP 403**; DOI `10.1016/bs.adcom.2018.03.015` → **HTTP 302** →
  `https://linkinghub.elsevier.com/retrieve/pii/S0065245818300305`.
  The same 403 is recorded in the round-16 search-log entry at
  `corpus/SOURCES.md:142-149`.
- DOI metadata (Crossref, exit 0): title matches; container
  `Advances in Computers`; page `275-378`; issued `2019`; type
  `book-chapter`. Crossref and OpenAlex both return `volume: null`; the
  volume-112 claim is confirmed only by secondary records surfaced in
  `web_search` — UCL Discovery record "Advances in Computers, 112 pp.
  275-378" and a DSpace catalogue entry "Advances in Computers Vol. 112,
  2019". The live UCL landing page now returns 403 to curl. Marked
  secondary, not a defect (the row does not rest a claim on the volume
  number).

## 4. Tier / kind / scope / teaches

- **tier B — justified.** `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:26-29`
  defines B as "strong secondary (expert write-up with reproducible detail,
  survey, textbook)"; the source is explicitly a survey. A is reserved for
  primary/authoritative work and can never be a survey; B is the contract's
  name for this kind of source. The preprint limitation is stated in the row
  and in the search log, and does not inflate the tier.
- **kind paper — justified.** Contract enum
  (`SOURCES-CONTRACT-v1.md:24-25`) is `spec · docs · paper · code · tool ·
  dataset · talk · book · community · own-work`; there is no `chapter` value
  and Crossref types the published item `book-chapter`. The artifact is a
  paper-form survey preprint; `paper` is the closest legal value. No second
  convention is implied.
- **scope — justified.** The survey contains both named topics:
  `survey.txt:723` `5.1. Mutant Selection (Step 1.)` and `survey.txt:1074`
  `5.3.1. Identifying Equivalent Mutants`.
- **teaches — grounded, with one inference boundary.** First clause ("an
  equivalent mutant cannot be detected in general") is the quoted sentence
  itself. The second clause ("so a survivor needs an off-suite
  non-equivalence witness or an explicit unreachability argument") is the
  lane's operational rule, not a sentence of the survey. The source supports
  the premise and the practice context: §5.3.1 says the best available
  techniques are heuristics, and program verification detects mutants that
  are "unreachable or ... cannot be infected" (`survey.txt:1095-1097`); it
  also names "the manual analysis involved in the identification of ...
  equivalent mutants" (`survey.txt:904`). The row does not attribute the
  witness rule to the authors; the `so` marks it as a consequence. Recorded
  as inference, not a misquote.

## 5. Used-by — exists and cites S057

`corpus/knowledge/mutation-case-kumitate-round-gate.md` is present in the
c699 tree and in the working tree, and contains S057 twice:
- `:1` source header: `...; S057 Papadakis et al. survey §5.3.1; ...`
- `:109` claim: `S057 states the general limit: deciding whether a mutant is
  equivalent is` … (continues with the survivor-witness rule).

`grep -c 'S057'` = 2. Contract's `mined` definition
(`SOURCES-CONTRACT-v1.md:43`, cited by ≥1 used-by path) is satisfied.

## 6. Registry census on committed bytes

Copied `git show c699:corpus/SOURCES.md` to scratch and ran the contract's
checks with cwd = lane root:
- rows = 55; malformed `NF!=13` = 0.
- duplicate ids = none; tier/kind/status enum violations = none;
  tier-inflation (A + community) = none.
- mined rows with missing used-by paths = none.
- S057 specifically: 13 awk fields, used-by path EXISTS.

Gate registry-changes paragraph (`round-16.md:40-44`) also holds: the
search-log entry exists at `corpus/SOURCES.md:142-149` (ScienceDirect 403,
UCL preprint opened instead, tiered B) and the six included sources are
exactly S052–S057.

## 7. Notes / unresolved

- Working tree is not byte-identical to c699: `git --no-optional-locks diff
  c699 -- corpus/lessons/round-16.md` shows **1 insertion** (a `vacuous`
  Mistakes row appended by another seat, `.ufo/waves/round-16/w2/…`). All
  findings above are against the `git show c699:...` bytes as the Target
  requires; the drift does not touch the S057 row or its Gate quote.
- Published pagination and published section numbering were not checked
  (publisher 403). The row explicitly scopes itself to the preprint and
  states that limit, so this neither confirms nor falsifies anything beyond
  what the row claims.
- Volume 112 rests on secondary catalogue snippets only (see §3).

**Verdict: holds** — Gate quote exact (8 words) at §5.3.1 p. 29 of the
2017-12-14 preprint; anchor and DOI resolve; tier B, kind paper, scope and
teaches are justified (teaches' witness clause is a marked consequence, not a
quoted claim); used-by path exists and cites S057 twice; registry census
clean. No field falls.
