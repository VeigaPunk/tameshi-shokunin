# T58W2Read01 — Standing rules

**Recommendation: verified-record. Findings: none established.** This is a scoped cold-read record, not admission of C2 or any runtime.

- Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534`; dispatch `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline -3` confirmed that head.
- Heading: `## Standing rules`, SKILL.md lines **17–57**, read end to end in a shared scratch clone detached at C0.
- Frozen round-18 sectionizer output: `17 57 d7042aa08484f1a8c72c7228dd668c0cb89baa83533b12b8b8f9839f0ef5093c`.
- Axes: calibration, reproducibility, scope honesty, substrate safety.

## Sweep and observed outputs

Every executed command, environment override, exit, stdout and stderr is retained verbatim in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2Read01-receipts/commands.json` and the companion machine report. The section text is retained beside those receipts.

| Sweep | Observed output |
|---|---|
| Seven self-tests plus env-diff --contract and registry-check --rev, unusable TMPDIR | All nine: exit 2, one matching stderr line naming the unusable value; no traceback. Repeat-control also prints `REPEAT_CONTROL: setup_error` on stdout, which does not contradict the section's stderr guarantee. |
| Five documented lazy modes, usable baseline versus unusable TMPDIR | All five retain exit 0. |
| Seven strict_scratch_root helpers, empty versus unset TMPDIR | All seven: `empty='/tmp' unset='/tmp' equal=True`; helper inspection only, no allocation under /tmp. |
| Newline-bearing unusable TMPDIR, context-capture --selftest | Exit 2; newline escaped as literal `\\n` within the single stderr line. |
| Receipt absent revision | Exit 3, `RECEIPT_REV_ABSENT`. |
| Verdict and positive receipt at another revision, no paths | Both exit 3, `RECEIPT_REV_MISMATCH`. |
| Positive receipt at base, changed tools/registry.json surface | Exit 3, `RECEIPT_REV_CONTENT_DRIFT`, `drift=tools/registry.json`. |
| Verdict receipt at base, identical PROVINCE.md surface | Exit 0, `verdict=PASS`, as explicitly allowed by the table. |
| Unresolvable control revision / certified revision | Exit 3 / 2 respectively, `RECEIPT_REV_UNRESOLVABLE`. |

## Pointer and contradiction read

PROVINCE.md:14–20 agrees with the read-only and secrets boundaries. The cited Kimi :4–7 and Kagi :4–6 ranges contain the historical scratch-copy statements. SKILL.md:1750–1763 contains the named round-16 erratum and expressly discloses its in-place repairs. S278/S279 resolve in corpus/SOURCES.md:153–154. The scratch contract note enumerates all nine allocating modes and five lazy modes. The seven strict-helper registry cells remain present; an additional receipt-gate cell explicitly describes its exclusion from that frozen contract.

The cited historical `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-53/w2r/T53W2R4.md`:65–75 supports the scratch convention census and historical anchors, and marks the host directive's date as inherited provenance. This reader inspected that evidence; it did not independently reconstruct thousands of historical occurrences.

LSP is unavailable (`xd://lsp`: `No such tool`). Literal pointer searches are not presented as semantic reference proof.

## Calibration notes and residual risk

- An initial env-diff invocation referenced the frozen counter's generated fixture-contract.json, absent from the committed tree. A valid equivalent contract was then explicitly created in seat scratch; the resulting command produced the required scratch refusal. The preparation failure remains in receipts and is not a documented-command finding.
- An initial drift fixture used SKILL.md. The gate accepted it correctly: SKILL.md is byte-identical between base and C0. Changing the fixture surface to tools/registry.json produced the expected refusal. Both observations remain recorded; a fixture expectation error is not a product finding.
- No full allocating-mode usable/empty self-test sweeps, strace allocation census, independent historical occurrence census, or historical freeze-positive replay were performed. No universal pass is claimed. The bent-runner forgery was not independently replayed by this one-section reader; this report does not contradict its decisive C2 non-admission.
- No source edits, prior-round evidence edits, installations, updates, or subagent dispatch.

## Self-evaluation

Accuracy 4/5 (raw outputs preserved; historical counts rely on cited evidence). Completeness 4/5 (full section read and targeted behavior covered; exhaustive historical/runtime sweeps excluded above). Clarity 4/5 (large raw output separated from this summary). Actionability 4/5 (exact commands retained; scratch fixture paths require recreation). Conciseness 4/5 (machine output duplicates receipts for portability). Overall 4.0/5. Improvement: independently reconstruct the historical census if stronger historical assurance is needed; no contrary finding was established. User-agreement self-check: these limitations are explicit rather than presented as passes.

## Cleanup

`rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W2Read01 && test ! -e /fast/scratch/hyaku/tameshi-r58/T58W2Read01` completed successfully and printed `Scratch deleted: /fast/scratch/hyaku/tameshi-r58/T58W2Read01`. Scratch was deleted before yield.
