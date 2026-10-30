# Blind re-seat: R52.5 / R52.6

Axes: calibration, evidence fidelity, blindness. Recommendations only; no admission judgment.

Scope: shared scratch clone `/fast/scratch/hyaku/tameshi-r57/T57W3ReseatR525R526/clone`, detached at `5e3569969b532310d2b8a3d130901757a3df356b`. No lane-working-tree reads, lane git commands, round-57 evidence/wave reads, or routed-defect ledger reads. Only output files were written outside scratch. No installations or source edits.

## R52.5 — fixed

`git -C <clone> show --format=fuller 218bc6b5c25d6a3c57dd44600febd552f0167cee -- tools/registry-check.py` shows both hard-coded `dir="/tmp"` allocations changed to `tempfile.gettempdir()`. The commit follows spot-check addition `c1d49d76be4028df2a68322e7117ff3aafaccd5c` and precedes the assigned base (both `merge-base --is-ancestor` commands exit 0).

Base bytes further strengthen that repair: `tools/registry-check.py:761-772` selects TMPDIR with an explicit unusable-root rejection; line 784 passes that helper into `mkdtemp`. Executed Python `runpy.run_path` probe under redirected TMPDIR prints:

```text
TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3ReseatR525R526/tmpdir-probe
strict_scratch_root=/fast/scratch/hyaku/tameshi-r57/T57W3ReseatR525R526/tmpdir-probe
allocated_under_TMPDIR=True
exit=0
```

## R52.6 — open under the required lane-commit criterion

`git -C <clone> ls-tree -r --name-only HEAD .ufo/reports` exits 0 and prints only:

```text
.ufo/reports/round-1/tameshi.md
```

`git -C <clone> log --format='%H %s' c1d49d76be4028df2a68322e7117ff3aafaccd5c..HEAD -- .ufo/reports` exits 0 with empty stdout. Thus no lane commit after the spot-check repairs the cited report surface. `corpus/lessons/round-52-verifier-spotcheck.md:8` explicitly identifies the round-52 report as a fleet commit, and round-53's spot-check line 9 does the same for its report. Although round-53's closure line 22 claims per-box SHONEN compliance, that is not the underlying report's bytes and does not establish all requested repairs. No owner withdrawal was observed; external location alone does not mean the lane author is not responsible.

Residual risk: this is not evidence that future fleet reports remain malformed. Actual fleet report content is outside the mandated blind clone scope, so full external-report conformance remains unverified; no qualifying lane repair can be named. The requested binary classification therefore remains open rather than claiming an unproved fix or a withdrawal.

## Evidence and verification limits

Exact executable commands, outputs, exit codes, and repair diff: `T57W3ReseatR525R526-receipts/commands.json` beside this report. Review used textual and Git-object evidence, not semantic-reference proof: `xd://lsp` is unavailable (tool returned `No such tool: xd://lsp`). No full registry selftest or fleet report inspection was run. The executed scratch probe covers allocation-root selection, not every registry behavior.
