# T58W2Read07 — map cold reread

Recommendation: **verified-record**. No actionable false statement found in the assigned section. This is a reader record, not admission of the round or its counters.

- Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534`; lane log at dispatch showed this as newest commit, followed by `0fdb71d2`, `1d1f70d8`.
- Heading: `### The map — where a reader enters, artifact by artifact`.
- Frozen round-18 sectionizer: lines **1421–1436**, SHA256 **30d62e79a81d8e6dfcfc9076f0977b1e14016d527f5fd78e66aab407bd370bea**. Read end to end from the pinned blob, then inspected mapped artifacts in a detached scratch clone.
- Axes: factual accuracy, pointer resolution, executable-command coverage, calibration.

## Findings by severity

None. The command/output sweep is preserved at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2Read07-receipts/sweep.py` and `sweep.txt`; complete executed command records are in the sibling `commands.json`.

Sweep command:

```text
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2Read07-receipts/sweep.py /fast/scratch/hyaku/tameshi-r58/T58W2Read07/clone
```

Observed exit 0. Output includes all 13 concrete mapped paths `exists=True`, mapped runbook/protocol/standing-state headings, six runbook rows, eight measured ledger rows, ten registered runner legs, `MUTATION_CASE_NOTES 10`, `ROUND11_RECORD_FILES []`, `LIMITS_HEADING True`, `POINTER_NOT_SECOND_HOME True`, and `BASE_TO_C0_SKILL_DIFF_BYTES 0`. The two absent newer ledger rows are expressly disclosed in the assigned text, not hidden. README line pointers 125/326/614, LOG 316–317, ledger 439–441, and runner/runbook scratch-default pointers resolve as described. Plan placeholders match the actual historical file ranges.

Runner command:

```text
TMPDIR=/fast/scratch/hyaku/tameshi-r58/T58W2Read07 bash /fast/scratch/hyaku/tameshi-r58/T58W2Read07/clone/tools/mutate-and-run.sh --selftest
```

Observed exit 0: `MUTATE_SELFTEST: 107/107 pass`, `VERDICT: PASS`. Full output: `T58W2Read07-receipts/selftest.txt`.

## Residual risk and verification gaps

```text
TMPDIR=/fast/scratch/hyaku/tameshi-r58/T58W2Read07 bash /fast/scratch/hyaku/tameshi-r58/T58W2Read07/clone/tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r58/T58W2Read07/regression
```

Observed exit **2**, not PASS: all ten legs returned `SETUP (repo_identity_mismatch: … is not its own repository; toplevel=unresolved)` because this isolated clone has no sibling repos. Final output: `REGRESSION: SETUP (cases=10 passed=0 cannot-verify=10)`. Full output: `T58W2Read07-receipts/regression.txt`. The runner documents missing-repo SETUP; this is not evidence of a false map claim. **Actual ten-leg verdict replay remains unverified.**

LSP device unavailable (`xd://lsp`: `No such tool`); checks used literal source inspection, not semantic reference proof. No canonical orchestration/resume behavior is changed or claimed by this map-only reread. No claim about C2 admission or saturation is made.

Style note only: “the runbook §'s” could name the SKILL.md runbook heading explicitly. Its Pointer/not-second-home rule does exist. The map correctly reports and resolves the runbook's stale `/tmp` default against the runner's TMPDIR-aware implementation.

## Discipline and self-evaluation

No tools installed. No source files edited. No prior-round evidence modified. The scratch clone and all scratch execution data were removed with `rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W2Read07` (exit 0) before reporting; durable receipts remain only under the assigned receipts directory.

Self-evaluation: accuracy 4/5 (ten-leg replay unavailable); completeness 4/5 (same explicit environmental gap); clarity 4/5 (historical counts require qualifications); actionability 5/5 (commands and full outputs retained); conciseness 4/5 (receipt detail retained for reproducibility). Overall 4.2/5. Highest-impact improvement is a separate replay with the documented sibling object stores available; it must not be called passed here. The user should agree with the distinction between verified map facts and unverified runtime replay.
