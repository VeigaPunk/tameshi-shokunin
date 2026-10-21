# FAudit1814 — round 19, w2

Date: 2026-10-21. Read-only scoped falsification; advisory only.

Axes: claim fail-capability · receipt/argv attribution · delivered-revision arithmetic.

## Strongest assertion and verdict

**Agree, narrowly:** Audit1814 F1 says `.ufo/evidence/round-18/final/audit-1814.stdout:50` — “VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision” — cannot fail on the claims it prints. The cited trace `coldread/traces/L1/audit-1814.json:33-34` contains this as an unconditional literal `print`; that captured Python has no Git/ancestor lookup or instrument comparison. Its prior asserts can fail for other captured inputs, but not for the ancestor clause.

**Concrete falsifier:** Change only an ancestor's instrument blob while keeping this captured workspace/input set fixed: the trace script reads no ancestor identity/blob, so it still reaches the same `VERIFIED … ancestor runs …` print. This is source inspection, not an executed mutation.

The consequence is concrete, not hypothetical: `round-18/final/checks.json` still records `bash-witness-selftest` argv `python3 tools/bash-witness-study.py --selftest`, revision `921ef807…`, exit `64`, stdout SHA-256 of empty bytes. The trace hashes `checks.json` but does not parse that row. Thus the line cannot establish that all receipts were successful. This does not contradict the historical fact that a failed receipt existed.

## Correction/revision comparison

At delivered `55e1d312c4e8ac67aefad80099bd27581ff805c9`, the original stdout, trace, and checks blobs remain exactly the reported hashes: `e5f76ad4…`, `76a1caca…`, and `fed3c8e6…`. The new witness is separate: `bash-witness-selftest-complete.json` records argv without `--` (`…study.py selftest`), revision `4b7c682…`, exit 0, stdout/stderr digests; its stdout says `43/43 pass`. It explicitly supersedes but preserves the old failed row. These are distinct invocations/revisions; the correction does not make the old `VERIFIED` print failure-capable.

`measure.py:183-199` verifies that new argv/revision/exit and stream digests, exact tally bytes, tool/runner pins, and the old exit-64/empty-stdout row. Its five predicates are R18-1…R18-5; none checks `audit-1814.stdout:50` or ancestor instrument equality. Round-19 lesson lines 146-150 cautions that historical ancestry print text is not established or reused; it does not name this exact stdout line. The prior report's “delivered revision may land after this audit” gap is stale for the checked byte identity, but its F1 remains valid for the immutable historical output.

## Arithmetic and residuals

Plain JSON row counts reproduce the retained receipts: baseline `before.json` at `7243e7f…` = 0 corrected / 5 open; existing `after-21e7932.json` = 5 corrected / 0 open, with all five IDs. That after receipt uses old ruler SHA `c538c33d…`, not current `measure.py` (delivered blob SHA `bb651eef…`). No `after-55e1d31.json` receipt is present in delivered revision, so these files do not yet prove a final 55e1 count under the hardened same ruler. The delivered monitor is a different no-harm measure (60/60, restraint 8), not the C1 five-item tally.

Residual unknowns: no final same-ruler 55e1 before/after result observed here; no independent producer authentication is established. `lsp` is not mounted in this session; no LSP checks were available. No tests, suites, or selftests were run.