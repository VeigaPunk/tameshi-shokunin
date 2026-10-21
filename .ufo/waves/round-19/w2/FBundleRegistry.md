# FBundleRegistry — round 19 / wave 2

## Verdict
- **Agree** with the strongest assertion: `checks.json#registry` is a failed raw attempt at `921ef807…`; the 31/31 pass is a distinct capture at `5923d89a…`, not a correction of that row.
- The recommendation to append another registry receipt is **stale as a C1 requirement**, not evidence that the row was repaired. C1 is frozen to five other routed defects.

## Evidence (opened 2026-10-21)
- `.ufo/evidence/round-18/final/checks.json:2-12`: registry argv is `python3 tools/registry-check.py --rev 921ef807… --json`; revision `921ef807…`, exit `1`, stdout digest `fe15a4d0…1cf4`. Recomputed checks/stdout SHA-256 values match (`fed3c8e6…671d`, `fe15a4d0…1cf4`).
- Parsed the three retained stdout JSONs and their stderr trailers, without running any recorded command: `registry` = exit 1, 30/31; `registry-success` = exit 1, 29/31; `registry-branch-aligned` = exit 0, 31/31. Each stderr `REGISTRY_CHECK` tally agrees. The latter two both report `5923d89a…`; their `registry_sha256` values, and the first run's, are all `3e6785ee…f1e6`.
- `tools/registry-check.py` at `921ef807…` documents the recorded `--rev`/`--json` form (lines 11-13) and clone-at-revision behavior (59-65); its blob is identical at frozen `55e1d312…`. Both run revisions are ancestors of `55e1d312…`. No execution or attribution beyond retained bytes is claimed.
- `.ufo/evidence/round-18/coldread/ledger.json` binds `checks.json` and the pass stdout digest; `audit-1925.stdout:19-20` independently opens `tools/registry.json` and `registry-branch-aligned.stdout` at matching digest/byte count. The frozen round-19 ledger also has 23 input bindings for that pass stdout. None of these binds the registry stderr bytes; the checks row has no stderr path/hash.

## Concrete falsifier / correction boundary
- A claim that the old `checks.json#registry` row itself passed is falsified by its digest-matched stdout (`exit=1`, `held=30/31`) and matching stderr tally; only the differently named, differently revised branch-aligned capture passes.
- Frozen `measure.py` at `55e1d312…` uses a five-item `PATHS` set and evaluates only `R18-1`–`R18-5` (lines 46-51, 223-226); it does not require a registry receipt. Frozen `corpus/lessons/round-19.md:141-145` says the failed registry row and the branch-aligned pass are not reclassified across revisions and “it is not a sixth frozen defect” (opened 2026-10-21). Thus the report's suggested extra explicit receipt is not a missed C1 correction. It remains true that no separate receipt binds registry stderr/argv together.

## Residual unknowns
- The unbound stderr files cannot be proven to originate from the corresponding stdout invocation solely from the checked receipt data; their matching tallies are consistency, not process-level provenance.
- This read-only review establishes retained content and revision attribution, not historical producer authenticity or independent round admission.