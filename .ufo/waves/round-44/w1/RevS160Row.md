## Findings

- **Blocking deviation (wrong draft):** `/tmp/row-s160.txt:1` is a Google crawl-budget source, not Stryker equivalent-mutants. It does not establish the required scope `supersedes S089's anchor only`, the Stryker snapshot anchor/hash `79f6501a...`, or teaching clause beginning `supersedes S089 —`; its opened date shown is `2026-10-23 …`, not 2026-10-25. The displayed row is truncated, so remaining fields cannot be reliably validated. No L1 wave report-scratch draft was present in `.ufo/waves/round-44/w1/` (only `swarm-registry.json`).
- Lane `corpus/SOURCES.md:456` says `Next unused id: S160`, so S160 is the next-unused identifier and currently absent as a row (whole-lane search found no S160 row).
- Row contract reference: `corpus/SOURCES.md:10-11` defines the 11 columns and pipe-delimited layout; no proposed Stryker row was available to check NF=13 or embedded/escaped pipes. The current scratch candidate therefore is not contract-validated.
- Census W04 behavior not verified: the supplied lane repo contains only historical `.ufo/evidence/kaika-round-1/sources-census.sh`, a legacy census script (not the required `sources-census.sh validate --root ...` CLI); no scratch validate run was possible without the current CLI and correct row draft. Existing round-44 census-start output reports W04 warnings for existing duplicate URLs and ends `ok`, but has no S160.

## Residual risk / verification gaps

Need the actual L1-generated Stryker row draft and the current fleet `scripts/sources-census.sh` CLI to validate exact columns, required fields/escaping, knowledge-entry used-by, and duplicate-URL W04 (not E-code) exit-0 behavior. No tools installed.
