# ReviewQ113 — hand-check of S113 (tameshi lane, could-not-be-fetched class)

## Register row

`shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:363`:

```
| `tameshi` | round1 | S113` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1145/3540250.3558911 |
```

Class: could-not-be-fetched (the only register in scope carrying that class;
tameshi-shokunin round-39 lesson line 33 names S113, S123, S134 as that class).

## Fetch result — source is present, not absent

- `https://doi.org/10.1145/3540250.3558911` resolves: doi.org `302 → https://dl.acm.org/doi/10.1145/3540250.3558911`; ACM landing returns HTTP 403 to curl (bot wall), which explains the original "could not be fetched".
- CrossRef metadata fetch succeeds: "Change-aware mutation testing for evolving systems", Miloš Ojdanić, ESEC/FSE 2022, DOI 10.1145/3540250.3558911.
- Author-hosted camera-ready PDF (companion URL listed in `shokuknow/lanes/tameshi/SOURCES-PROPOSED.md:91`, `## Gate — S117`):

```
curl -sL "https://ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf"
→ HTTP 200, bytes=131622, content_type=application/pdf
```

## Quote check — located verbatim

`pdftotext` extraction, `/tmp/tameshi-r40-ReviewQ113/ojdanic.txt:292-294` (§3.2, p. 4):

> "…by selecting only subsuming commit relevant mutants, we reduce the number of mutants requiring analysis by around 93% on average."

Verbatim match of the quote the proposal records for this source.

## Findings

1. **Stale register classification (falsified).** The register's could-not-be-fetched row is falsified today: the DOI resolves and the cited content is fetchable via CrossRef metadata and the author-hosted camera-ready (HTTP 200). The row is verifiable, not absent — the residual truth is only that `dl.acm.org` refuses unauthenticated curl (HTTP 403).

2. **Round-40 lesson claim falsified for this row.** `tameshi-shokunin/corpus/lessons/round-40.md:41` claims "S113 and S123 were fetched this round (HTTP 200, HTML and PDF). Their quotes were not located." For S113 the quote **is** located, verbatim, in the fetched PDF (extract line above). Either the wrong URL was fetched, or the quote search missed — the predicate as written does not hold for this row.

## Notes

- ID ambiguity recorded, does not change the verdict: `shokuknow/lanes/tameshi/ID-REMAP.md` is per-round and pre-remap; the register row's URL cell is the authoritative binding (10.1145/3540250.3558911 → Ojdanić).
- No edits made: lane checkout, `considerthese/`, shokuknow and the register untouched. Scratch: `/tmp/tameshi-r40-ReviewQ113/` (PDF + extracted text). No counters run; no installs.
