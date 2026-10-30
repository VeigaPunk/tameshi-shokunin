# T58W2RevLesson — lesson re-check

C0: `8063d0a551fc5b3cb5a2d397da7353af53444534` (dispatch log matched).
Axes: source fidelity, provenance reproducibility, mistake-record calibration.

## Finding — low severity

`corpus/lessons/round-58.md:32-39` says fetch receipts and extracts are committed in `l1/sources/`; that directory contains only three text extracts. S287’s quotation and line 241 are correct, but its original PDF byte count, hash prefix and fetch date cannot be re-derived from its extract. S288 has the same provenance gap. This is **unverifiable original metadata**, not evidence of fabrication. Preserve the original responses and dated fetch receipts, or qualify the provenance claim.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --long 8063d0a551fc5b3cb5a2d397da7353af53444534 -- .ufo/waves/round-58/l1/sources/`

Output (exit 0; blob IDs retained in receipt):
```
1480  arxiv-2406.09843-abstract.txt
1699  atlassian-postmortems.txt
15284 dfcfw-deck.txt
```
The committed round-58 path census finds these extracts and wave-1 `arxiv.html`, but no S287/S288 original-response path under their source names. Exact commands, full outputs, and hash-search corroboration are in `T58W2RevLesson-receipts/sweep.json`.

## Two Gate checks

- **S286:** exact quoted abstract text exists. Reading the committed wave-1 `arxiv.html` with `git show` and hashing its bytes yields `44019 7af7e470fca3ef38e97d858b308dca20e815a4b919c9c235adae4d4f59c4a86e`, matching Gate metadata. The prior review records its 2026-10-30 fetch; this review does not independently establish the historical date.
- **S287:** exact quote exists at newline-delimited line **241** and score-precision hazard at **239**. The extract is 15284 bytes, SHA256 `eaa3d03ac271569300d1417dae420555ce2fb1ecdb7fc4b18600f2692f6f5f7e`; that is not the original PDF and cannot validate its claimed hash/size.

## Mistakes rows

- **stale-premise:** base URL sweep for `2406.09843` returns empty, exit 1. The delta URL sweep returns both `delta-debugging-minimization-contract.md` and `fixture-shrinking-pilot.md`; the first explicitly cites S271. Base SCORECARD’s planned-round-54/55 text retains the delta candidate. The lesson abbreviates the red sweep’s output to one file; its refusal discriminator remains supported.
- **number-drift:** committed intersection is exactly S153–S160, not S165; fixture receipt prints `registry=  | S156 | fixture |` and `collisions=S156`. These carriers support the correction; historical discovery timing remains asserted.

## Residual risk / gaps

No live refetch: immutable committed extracts were the requested comparison target. Date claims are not authenticated by extract content. The C0 Wave record is explicitly unfinished, not falsely counted as completed closure. LSP device unavailable (`No such tool: xd://lsp`); literal Git searches are not semantic proof. No runtime or admission action taken.

No scratch or clone created; no scratch remains. No tools installed or updated. Only this seat’s deliverables written.

Self-evaluation: accuracy 4 (dates not independently established), completeness 4 (two requested Gate samples plus both Mistakes rows checked; original PDF absent), clarity 4 (raw/extract distinction necessary), actionability 5 (specific carriers and repair), conciseness 4 (audit detail retained). Overall 4.2; user agreement is INFERENCE.
