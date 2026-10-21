# FAxisBound — scoped result (2026-10-21)

- **Axis:** calibration, C1 no-harm boundary only.
- **Strongest assertion attacked:** AxisBound w1 `AxisBound.md:12–29, 124–134` says the current-revision monitor still reports 49/60 and restraint 6, so the unchanged-8 assertion is harmful.
- **Verdict: DISAGREE as to delivered revision 55e1; AGREE that the cited 21e7932 intermediate was harmful.** The old observation is accurate at its named revision, but is not the final monitor.

## Exact evidence

- Read-only JSON recount of `.ufo/evidence/round-19/current-ledger-monitor-21e7932.json`: revision=rev_input=`21e79329…`; 60 section rows, 49 `credited=true`, 11 not credited; summary 49/60, box3=false, restraint=6, strict trace, no overrides.
- Read-only JSON recount of `.ufo/evidence/round-19/current-ledger-monitor-55e1d31.json`: revision=rev_input=`55e1d312c4e8ac67aefad80099bd27581ff805c9`; 60 rows, 60 credited, 0 uncredited; summary 60/60, box3=true, restraint=8, strict trace, no overrides, `ledger_source=rev`. This directly falsifies “only current-revision measurement says 6.”
- The delivered `.ufo/evidence/round-19/coldread/measure.py:1–21` selects `.ufo/evidence/round-19/coldread/ledger.json` over the unchanged round-18 input-keyed algorithm; the ledger is present in 55e1 (tree entry blob `7c128b44…`). `round-19.md:97–107` labels the refreshed inputs L1-author re-anchoring, “not a new blind or independent cold-read” (2026-10-21). Thus this corrects the 6/49 result under a maintained-ledger predicate, not current-page equivalence, independent cold-read, or command coverage.
- The five-defect `.ufo/evidence/round-19/measure.py:129–226` evaluates only R18-1…R18-5; the cold-read no-harm value is a separate monitor, not a sixth C1 defect or a score increase. `SCORECARD.md:696–697` calls 8 “a dated historical score” (Round 19, 2026-10-21), rather than asserting current-page coverage.

## Concrete falsifier and remaining gap

A current monitor with 60 array entries, all 60 credited, and restraint 8 at `55e1d312…` falsifies the report’s 49/60, restraint-6 current-state conclusion. AxisBound’s own maintained-ledger alternative is reflected in the later result; no numeric promotion follows.

Residual: the 55e1 monitor JSON has no argv, exit, tool hash, or stdout/stderr digest fields; `revision`/`rev_input` are its own recorded values. `git show 55e1d312…:.ufo/evidence/round-19/current-ledger-monitor-55e1d31.json` reports the path exists on disk but not in that commit. The lesson’s `192–200` still says a later-input refresh is required and does not append this final result. Exact invocation and durable receipt binding therefore remain unverified; do not treat the output as independent execution proof. Smallest safe correction: append a post-run receipt/erratum binding the 55e1 revision, exact argv, selected script/ledger digests, exit, and output digest, while retaining the author-read and narrow-predicate labels.