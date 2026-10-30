# T58W2Read04 — cold re-read

Verdict: **verified-record**. No actionable false statement or failing command found in the assigned section.

- Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534`
- Heading: `### Triggers T1–T3 and the re-pin rule`
- Lines: 1100–1122
- Frozen round-18 section SHA-256: `2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801`

## Sweep and evidence

The complete section was read at C0 in a shared clone detached at C0. Five cited files and nine anchor ranges resolved. The historical runner chronology was independently hashed from seven ancestor commits: d8abee52 → 597e1419 → b56c6e57 → cf41efaa → 75ed934d on October 14, followed by 89722ddb and 0673d2e5 on October 20. Commit timestamps match the section; every ancestry check returned 0. The working-tree intermediate pins are explicitly distinguished from commits in the section and its cited plan.

The three reproducible command/output receipts are in `T58W2Read04-receipts/` and embedded in the JSON beside this report:

- `frozen-sectionize.json`: frozen importlib sectionizer; `1100 1122 2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801`; full section text.
- `runner-hash-chronology.json`: seven committed runner hashes, author timestamps, and `ancestor_rc=0` each.
- `pointer-sweep.json`: pinned cited excerpts; `PASS: all 5 cited files and 9 line ranges resolve at C0`.

All three commands exited 0. The section has no executable recipe command: the REGRESSION and match strings are historical outputs. The original SCR-T6 replay is reported with its explicit missing-scratch/U qualification, not upgraded to a fresh observed replay. No runtime was invoked. Adjacent tick and round-9 rules and the intake owner boundary are consistent with this section.

## Residual risk / verification gaps

LSP device unavailable (`xd://lsp`: No such tool); text/pinned-blob inspection is not semantic LSP proof. Historical replay receipts were inspected, not rerun. The abbreviated RerunSweep basename resolves under `.ufo/waves/round-16/w2/`; making that path explicit is optional clarity, not a false claim.

Axes: calibration, pinned-byte fidelity, pointer resolution, historical consistency. No tools installed or updated. Scratch removed before handoff. No lane source or frozen evidence edited.
