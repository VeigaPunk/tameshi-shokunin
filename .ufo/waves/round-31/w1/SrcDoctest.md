# SrcDoctest report

**Verdict:** The official Python doctest page was fetched and contains a direct statement supporting the requested docstring-freshness claim. S095 is provided below for the L1 integrator; `SOURCES.md` was not edited.

## Evidence

- The SOURCES contract specifies 11 columns and requires the round's `## Gate` to record each new row's URL, access date, and a quote of no more than 25 words with its location (`/home/vgpnk/Projects/shokunin/CORPUS.md:86-115`). The frozen `corpus/SOURCES.md` at `c111dab58b0a8d55e991bbd2efe3aad56717b95a` has that same 11-column header; S092-S094 are its final registry rows and its id allocation names S095 as next unused. S055 already cites this same Python page for a broader executable-documentation scope; S095 narrows the focus to docstring freshness and the named knowledge path.
- Fetched page identifies itself as Python 3.15.1 documentation (`doctest.html:20`). The first common-use bullet in the module introduction is at `doctest.html:249-250`.
- Exact fetch and metadata command (run from the assigned scratch directory):

  ```sh
  curl --fail --location --silent --show-error https://docs.python.org/3/library/doctest.html -o /fast/scratch/hyaku/tameshi-r31-seats/SrcDoctest/doctest.html && printf 'access-date-utc=' && date -u +%F && wc -c /fast/scratch/hyaku/tameshi-r31-seats/SrcDoctest/doctest.html && sha256sum /fast/scratch/hyaku/tameshi-r31-seats/SrcDoctest/doctest.html
  ```

  Observed output:

  ```text
  access-date-utc=2026-10-23
  216574 /fast/scratch/hyaku/tameshi-r31-seats/SrcDoctest/doctest.html
  369dcc17009a2f36000284ca86eedb7cef4bc10f773e554754bbdad07791cc46  /fast/scratch/hyaku/tameshi-r31-seats/SrcDoctest/doctest.html
  ```

## Proposed SOURCES row

```text
| S095 | doctest — Test interactive Python examples — https://docs.python.org/3/library/doctest.html | docs | A | Python doctest's documented use for checking that module docstrings remain up to date via their interactive examples | §doctest — Test interactive Python examples (module introduction), first common-use bullet, HTML lines 249–250 @ Python 3.15.1 documentation, fetched 2026-10-23; HTML SHA-256 369dcc17009a2f36000284ca86eedb7cef4bc10f773e554754bbdad07791cc46 (216574 bytes) | doctest can check that module docstrings are up to date by verifying that all interactive examples still work as documented | mined | 2026-10-23 | on-release | corpus/knowledge/executable-self-assessment.md |
```

## Gate

URL: https://docs.python.org/3/library/doctest.html; accessed 2026-10-23 UTC; quote (module introduction, first common-use bullet, HTML lines 249–250): “To check that a module’s docstrings are up-to-date by verifying that all interactive examples still work as documented.” (18 words.)

## Touched surfaces and limits

- Downloaded source artifact: `/fast/scratch/hyaku/tameshi-r31-seats/SrcDoctest/doctest.html`.
- Report: `.ufo/waves/round-31/w1/SrcDoctest.md`.
- No product files, registry rows, or knowledge files were edited; no software gates or tests were run.
- The named `corpus/knowledge/executable-self-assessment.md` path was not present in the checked lane tree (`read` returned “not found”). The requested `mined` status and `used-by` cell are included as specified, but this checkout does not establish that the knowledge entry already cites S095; the integrator should ensure that citation exists before treating `mined` as contract-verified.
