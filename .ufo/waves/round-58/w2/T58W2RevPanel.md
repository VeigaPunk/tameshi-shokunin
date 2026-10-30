# T58W2RevPanel — panel provenance

## Findings

No actionable provenance defect found at `8063d0a551fc5b3cb5a2d397da7353af53444534`. Recommendation only, not admission.

Axes: digest integrity; unique item coverage; seat provenance; calibrated disagreement accounting.

- Committed panel SHA256 and committed `PANEL_SHA256` both equal `e65445ba73fb9f06f4d98068bf6622059c5d2a100997ef2c6178805edd39569f`.
- All 51 frozen ids occur exactly once across the 11 seat verdict files, panel verdict/detail maps, and installed ledger. Duplicate JSON keys were explicitly checked: none.
- All 11 seat-file hashes match `panel.files`; all 51 verdicts match; all 11 seat names appear once in committed `w1-results.json`.
- Recomputed disagreements: **4/5**, excess **0**. R54.5, R54.6, R56.2, R56.3 each have panel `fixed` versus ledger `status_at_base=open`.

Canonical accounting: `.ufo/evidence/round-58/c1/measure.py:245-274` defines seat provenance; lines 453-466 compare the ledger's `status_at_base` with panel verdicts and count only excess above allowance. This audit independently reproduces those comparisons without executing imported lane code.

## Executed sweep

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2RevPanel-receipts/audit.py
```

Exit 0; stderr empty. Output: all 14 checks true, 51 ids, 11 seats, disagreement_count=4, panel_over=0. Full command output, per-id comparisons, per-seat hashes, and all `git -C ... show C0:path` input digests are preserved in `T58W2RevPanel-receipts/audit-output.json`; the exact reproducible script is beside it. Dispatch `git -C ... log --oneline -3` confirmed C0 as newest commit.

## Residual risk / verification gaps

Provenance consistency does not establish the semantic correctness or independence of panel judgments. The four disagreements are recorded, not adjudicated here. No full criterion runtime was run and no criterion admission is claimed. LSP is unavailable (`xd://lsp`: No such tool); literal AST/text fallback was used, not semantic proof.

No installs, lane source edits, or prior-round evidence writes. Immutable Git blobs avoided clone/scratch data; the seat's empty scratch directory was created and removed successfully before reporting.

## Self-evaluation

Accuracy 4/5: exact Git-object bytes checked; underlying judgments intentionally not re-proved. Completeness 5/5: each assigned provenance condition and disagreement count covered. Clarity 4/5: detailed per-id evidence requires the JSON receipt. Actionability 5/5: reproducible command and script supplied. Conciseness 4/5: full receipt repeats per-id provenance to retain auditability. Overall 4.4/5. Improvement: consume the per-id receipt when adjudicating the four residual disagreements; user agreement with this bounded assessment is INFERENCE.
