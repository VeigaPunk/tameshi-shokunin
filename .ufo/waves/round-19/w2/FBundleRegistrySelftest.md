# FBundleRegistrySelftest — scoped falsification (2026-10-21)

## Strongest assertion / verdict

**Agree, scoped to `registry-selftest`:** the w1 report’s §6.1 assertion that this row is not one of the five routed defects and needs no correction survives the delivered C1 surface. Confidence: high for scope; this is not independent round-admission authority.

## Evidence

- Frozen row `.ufo/evidence/round-18/final/checks.json:25-34` records argv `python3 tools/registry-check.py --selftest`, revision `921ef807…`, exit 0, stdout SHA-256 `7ecd750f…34256`. At baseline `7243e7f1` and delivered `55e1d312`, the checks blob is `d8c98a92…` and the stdout blob is `5e975416…`; both match the inspected files. The script blob is `41541d75…` at `921ef`, `7243e7f1`, and `55e1d312`; `921ef` is an ancestor of the baseline.
- `tools/registry-check.py:1793-1797` dispatches the exact one-argument `--selftest` invocation. The retained stdout SHA recomputes to `7ecd750f…34256`; `wc -l` gives 49 lines, i.e. 48 case lines plus the trailer (2,481 bytes). This independently reproduces the report’s 1/1 recorded-digest match and 48-case arithmetic using file operations; no selftest was run.
- `corpus/lessons/round-18-verifier-spotcheck.md:180-204` enumerates the five routes; item 4 is the mis-invoked `bash-witness-selftest`, not `registry-selftest`. In the delivered `.ufo/evidence/round-19/measure.py:183-199`, the receipt/witness predicate likewise targets that bash-witness row and its replacement. `evaluate()` emits only R18-1 through R18-5 (`:223-225`); no predicate selects `registry-selftest`.
- Provenance distinction: the corrected bash-witness receipt’s recorded execution revision is `4b7c6823…`, not `55e1d312`. Its receipt and stream blobs are included in `55e1d312`; `4b7c` is an ancestor of `55e1`. `.ufo/evidence/round-19/measure.py` is the exact delivered blob (`d13dc4fb…`); its `receipt()` validates declared argv/revision/exit, stdout/stderr names and hashes, freeze timestamp, and empty stderr (`:78-96`).

## Concrete falsifier / stale point

The report’s §6.4 future-facing recommendation to supersede the failed **bash-witness** row is already fulfilled: `.ufo/evidence/round-19/bash-witness-selftest-complete.json` records exit 0, digest-bound streams, `historical_receipt_preserved: true`, and supersedes both the old row and the earlier round-19 receipt. Its stdout hashes to the recorded digest and matches the preserved `final/bash-witness.stdout`. The dated `corpus/lessons/round-18.md:135-155` Errata R18-4/R18-5 documents the replacement. This concretely makes that recommendation stale as an outstanding action, but does **not** falsify the row-specific no-correction assertion.

## Residual unknowns

The original `registry-selftest` execution remains self-attested: no independent execution log was found in the report’s scoped evidence, and its row has no stderr digest. The delivered ruler’s predicates do not independently authenticate that row. I did not run the measure, suites, or selftests.