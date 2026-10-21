# FEvidenceReuse — falsification report

## Axis and disposition
- C1 calibration only: the defined unit is five routed defects (0/5 to 5/5); no numeric score promotion or claim about the 18 guard survivors.
- Strongest material assertion challenged: “final-revision identity and observed failure-capable exit must therefore be evidenced by L1 before C1 closure” (w1 `EvidenceReuse.md:21`, report header dated 2026-10-21).
- **Partial disagree:** the delivered revision identity is no longer unknown: frozen build revision is `55e1d312c4e8ac67aefad80099bd27581ff805c9`. Agree that the C1 ruler's observed run/exit on that revision remains unproved and must be retained before closure.

## Evidence
- `contract.json:4-5,7-11` fixes baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`, target 5, and IDs R18-1…R18-5.
- Plain JSON arithmetic is correct for the old receipts: `before.json:2,18-42` = corrected 0/open 5 (all five open); `after-21e7932.json:2,18-43` = corrected 5/open 0 (all five corrected). The latter names revision `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`, not the delivered revision.
- The old before/after snapshots both record ruler SHA-256 `c538c33d6d80c9299183b6ff08a21da6f557fa66f99712f38820fdce1473e18e`. The `measure.py` at delivered `55e…` has SHA-256 `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`; current file matches the `55e…` blob. Read-only revision diff shows `measure.py` changed by +170/−17 lines between `21e…` and `55e…`. Thus the 5/5 is evidence for the older ruler/revision only, not the strengthened delivered ruler.
- Current `measure.py:367-403` loads blobs by explicit `--rev`, reports the executing ruler hash, and returns `--check` failure unless all five rows are corrected. `frozen-runs.json:3-6` records expected exits, not observed child exits; no `55e…` C1 result is present in the inspected evidence. `current-ledger-monitor-55e1d31.json:1954-55` identifies `55e…` but is the separate current-ledger monitor, not a C1 five-defect measurement.
- Receipt attribution checked: `bash-witness-selftest-complete.json:2-21` records argv `python3 tools/bash-witness-study.py selftest`, revision `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, exit 0 and stream hashes. It is a historical correction receipt, not a run on `55e…`.

## Concrete falsifier, move, residuals
- **Falsifier:** any claim that the cached 0/5→5/5 receipts establish the delivered `55e…` result is contradicted by their `21e…` revision and stale ruler hash; the delivered ruler hash differs and its code changed materially.
- **Move:** retain the w1 proposal to run the same ruler on baseline and delivered `55e…`, but bind acceptance to the delivered ruler SHA above as well as actual return codes 1/0 and output digests. Do not substitute the 60/60 ledger monitor for the C1 result.
- **Risk / unknown:** no final-ruler process output/exit was observed here, so do not infer closure or change the score 8. The receipt pins do not establish arbitrary historical authenticity; this finding makes no such claim.
