# T58W2Read06 — verified-record

## Findings

None in the assigned section at C0 `8063d0a551fc5b3cb5a2d397da7353af53444534`.

Heading: `## The operator's runbook and the six-leg regression (round 10, measured)`.
Frozen round-18 sectionizer output:

```text
1312 1320 636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7
```

The complete section was read. Its boundary precedes the first `###` child. Axes: historical truth, runnable replay, scope calibration.

## Sweep and evidence

Executed the importlib/frozen-sectionizer snippet reproduced in the adjacent JSON. Dispatch history matched the requested C0. Created a shared scratch clone, asserted its toplevel, then checked out C0 detached. No lane source was edited.

Historical corroboration at C0:
- `corpus/knowledge/operator-runbook.md:1–11`: round-10 T10-1 operator entry point exists.
- `corpus/knowledge/fleet-kill-rate-ledger.md:318–350`: round-9 receipt records four embedded legs and the cases-5/6 caveat.
- `plans/round-10-record-draft.md:78–92`: embedding, not re-cut; six-leg exact receipts and executable-bit correction.
- `tools/mutate-and-run.sh:7–18`: round-7 ledger replay and round-10 embedding provenance retained.
- Adjacent `SKILL.md:1344–1398` distinguishes historical six-leg execution from ten legs since round 51; the assigned heading is not a current six-leg saturation claim.

Executed, from the detached clone, with TMPDIR inside seat scratch and read-only sibling object-store symlinks inside scratch:

```bash
bash /fast/scratch/hyaku/tameshi-r58/T58W2Read06/clone/tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r58/T58W2Read06/regression
```

Observed output (exit 0):

```text
REGRESSION_CASE js-kimi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-surface-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-tsukuroi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-mado-verify: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-checklist-run: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=15)
REGRESSION_CASE js-claims-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-round-gate: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-sources-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-drift-pins: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
```

Full output: `T58W2Read06-receipts/regression.stdout`. Exact commands and sectionize snippet: `T58W2Read06.json`.

## Residual risk and verification gaps

Historical receipts are corroboration, not independent reconstruction of historical absence of other operator entry points. No affirmative contradiction found. No broader C1/C2 admission or arbitrary caller correctness is asserted. LSP unavailable (`read xd://lsp`: `No such tool`); textual observations are not semantic references proof.

No tools installed or updated. Seat scratch was removed before yielding; durable receipt retained.

Self-evaluation: accuracy 4 (historical negative cannot be reconstructed independently); completeness 4 (section fully read and replay exercised; historical corroboration remains documentary); clarity 4 (context references exceed the tiny assigned paragraph); actionability 5 (no scoped defect; exact replay evidence supplied); conciseness 4 (full per-leg output retained for audit). Overall 4.2. Improvement: preserve the distinction between documentary historical evidence and independently executed current replay; this report does so.
