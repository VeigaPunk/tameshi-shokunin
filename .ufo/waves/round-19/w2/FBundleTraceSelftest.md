# BundleTraceSelftest — scoped falsification

Audit date: 2026-10-21. Scope: target report and its cited trace-selftest receipt, streams, and CLI source; compare only the delivered C1 measure.

## Strongest assertion / verdict

**AGREE, with one narrow attribution caveat:** the scoped trace-selftest record is a successful retained result, not evidence of a failed invocation. Its evidence does not establish that the command actually ran at the attributed revision; the target report correctly distinguishes those claims.

## Evidence

- `.ufo/evidence/round-18/final/checks.json["trace-selftest"]` records argv `python3 tools/trace-inputs.py --selftest`, revision `921ef8077440f90d092aab4b9fdc750a45de1224`, exit `0`, and stdout SHA-256 `fadbe2c9…feffda1`. The row contains no `cwd`, source hash, stderr path, or stderr hash.
- The retained stdout has exactly 30 `PASS` rows (lines 1–30), then `SELFTEST: 30/30` (line 31); 783 bytes. Its recomputed SHA-256 matches the row. Retained stderr is empty (0 bytes; SHA-256 `e3b0c442…2b855`), but the row does not bind it.
- `checks.json` SHA-256 is `fed3c8e6…5c671d`, both in the working tree and delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c9`; the delivered stdout blob has the same digest as the row. `trace-inputs.py` SHA-256 is `fb1d81f6…f2636` at `921ef…`, at `55e1…`, and in the working tree. Source lines 53–54 say “--selftest runs synthetic fixtures only, location-independent”; lines 978–983 define and dispatch `--selftest`. This verifies source/argv spelling, not execution context.
- Delivered `55e1…/.ufo/evidence/round-19/measure.py` has SHA-256 `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`; current working-tree `measure.py` is different (`3f19a16b…3a2e590f`). Use the delivered blob for the C1 comparison, not later working-tree predicates.
- In that delivered measure, R18-4 checks `bash-witness-selftest-complete.json` and the old `bash-witness-selftest` row (exit 64), then requires typed supersession (`measure.py:183–199, 223–225`). It does not inspect or correct `trace-selftest`. The round-19 lesson likewise describes the failed bash-witness `--selftest` as a separate preserved attempt (line 20). No C1 evidence contradicts the trace-selftest result or makes its old row execution-bound.

## Concrete falsifier and disposition

The row's missing `cwd` falsifies any stronger reading that the relative script path was validated against a *recorded* working-directory context—none is recorded. The target report explicitly discloses that limitation, so this narrows its argv claim but does not overturn its central successful-retained-evidence finding. No stale C1 correction to this trace row was overlooked; its missing execution binding remains an unknown, not one of the five claimed C1 repairs.

## Residual unknowns

Whether the relative argv resolved from the repository root, whether the recorded run used the source blob at `921ef…`, and whether any separate failed trace-selftest attempt exists are not established by this row/streams. No CLI or selftest was run.