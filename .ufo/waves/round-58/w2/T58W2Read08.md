# T58W2Read08 — cold re-read

- Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534`
- Section: `## Repeated controls and gate registry — round 12`, lines 1521–1540
- Frozen sectionize SHA-256: `3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831`
- Verdict: **verified-record**; no false substantive statements or failing documented command found.

## Observed sweep

Commands, full output and cwd are retained in `T58W2Read08.json` and `T58W2Read08-receipts/*.json`.

| Probe | Exit | Final output |
|---|---:|---|
| stable | 0 | `REPEAT_CONTROL: controls_match` |
| nonzero | 2 | `REPEAT_CONTROL: baseline_nonzero` |
| unavailable | 2 | `REPEAT_CONTROL: command_unavailable` |
| mismatch | 1 | `REPEAT_CONTROL: controls_mismatch` |
| selftest | 0 | `SELFTEST: PASS (29 cases)` |
| pointers | 0 | `pointers: True` |
| frozen-sectionize | 0 | `1521 1540 3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831` |

## Notes and residual risk

- Stale-but-true source locator: SKILL.md:1523 cites corpus/SOURCES.md:503; that line is staged-id collision history. S265 actually resolves at line 140 and explicitly supersedes S026. Treat as a locator-only improvement, not a false source claim. See pointers receipt.
- LSP unavailable: xd://lsp reports No such tool; text search used only for literal cross-reference checks, not semantic proof.
- No contradiction observed with the adjacent round-12 registry or the dated ten-leg updates elsewhere in SKILL.md; six-leg wording explicitly refers to round 12.
- Axes: claim accuracy, runnable recipes, pointer resolution, finite-sample calibration.
- Verification gaps: no live external URL freshness check; no intentional hanging process (no-timeout limitation is explicit). Historical receipts are historical data, not current-run claims.
- Scratch clone and all scratch outputs deleted before handoff. No tools installed.

## Self-evaluation

Accuracy 4/5 (finite fixtures, no universal stability claim); completeness 4/5 (no live source freshness check); clarity 4/5 (full commands delegated to JSON receipts); actionability 4/5 (exact stale locator identified, not edited); conciseness 4/5 (some receipt duplication). Mean 4.0. Highest-value improvement: update only the stale source line locator. Assessment is scoped to this section.
