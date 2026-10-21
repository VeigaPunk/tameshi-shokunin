# FAudit1479 — FALSIFY

Review date: 2026-10-21. Axes: evidence truth, revision/argv attribution, C1 scope.

## Judgment

**Partial disagree (low, evidentiary wording only).** Audit1479 correctly identifies the historical trace/ledger range and output-digest limitations. Its line 19 assertion that the final verification line is “consistent with that argv/spec” overstates what the command establishes: the captured script emits an ancestry claim without checking it.

## Evidence

- The cited historical trace is `.ufo/evidence/round-18/coldread/traces/L1/audit-1479.json`: `rev=a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`, exit 0, `start=1479,end=1497`. The matching ledger row has `read_rev` equal to that revision, `commands_executed_count=1`, and `start=1479,end=1498`; its input map has no stdout/stderr digest fields (`ledger.json:12259-12300`). This confirms the report’s historical attribution and one-line discrepancy.
- In trace `argv` line 33, the Python code checks bounded status/tally strings, then literally prints “VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision”. It has no ancestor-revision reads or instrument-digest equality assertion. Thus the line is observed text, not verification of that assertion. This does not prove the hashes differed; it disproves treating this command as proof they matched.
- C1 arithmetic from retained JSON: `before.json` has 5 rows, all `open` (corrected 0) at baseline `7243e7f...`; `after-21e7932.json` has the same five IDs all `corrected` (5/5, open 0) at `21e7932...`. Both carry ruler SHA `c538c33d...`, matching `measure.py` at `21e7932`. At frozen `55e1d31...`, `measure.py` SHA is `bb651e...`; the only `after*` receipt is `after-21e7932.json`. Therefore 0/5→5/5 is supported for the earlier 21e run, not a final C1 measurement at 55e; the retained 55e monitor is a different 60/60 no-harm measure.
- The old `checks.json` digest remains `fed3c8e6...` in both C1 receipts. The new successful witness is a separate receipt (`bash-witness-selftest-complete.json`, exact selftest argv, exit 0, stream digests, supersedes the failed row); C1 did not rewrite the historical failure. Audit1479’s conditional warning about a changed checks file is not an actual missed rewrite.
- Separate later refresh evidence is not retroactive: `refresh-receipts.json` records a new `source-1479` read at `7af123b...`, output digest `215d567...`, and stdout `SECTION 1479 1498`; it is neither the old `a9c94c...` trace nor a 55e measurement.

## Concrete falsifier

The old `argv` itself is the falsifier for the report’s unqualified verification wording: the ancestry sentence is a hardcoded `print`, with no corresponding equality check. Keep it as an unverified historical assertion unless independent evidence is supplied.

## Residual risk and verification gaps

The old stdout’s reported local hash cannot be authenticated from its cited trace/ledger; no finding here establishes that ancestor instrument hashes actually differed. C1’s final same-ruler count at 55e remains unobserved in the scoped receipts. No `lsp` device/server was mounted (`xd://lsp` unavailable), so semantic LSP checks could not be made; no suites, tests, builds, or formatters were run.