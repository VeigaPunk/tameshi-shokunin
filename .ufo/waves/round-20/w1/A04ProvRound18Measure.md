# A04 — Round-18 measure provenance and output scope

## Verdict

**Agree; no actionable defect found in this scoped check.** Axes reviewed: instrument provenance, pinned-revision semantics, and the boundary between measured metadata and stronger behavioral claims.

## Findings by severity

None.

## Commands and observed outputs

All instrument execution was from a byte-for-byte copy in `/tmp/a04_r18`; no lane production file was changed.

1. Provenance requested by the assignment:

   ```text
   git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 4b7c682:.ufo/evidence/round-18/measure.py | sha256sum
   7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37  -
   ```

   This exactly matches the frozen `round18-measure` SHA. A raw-byte comparison also observed the `4b7c682` blob and `HEAD` blob both at that SHA, identical, 76,144 bytes (1,659 newline characters). The target commit resolves to `4b7c6823a462f5ea2eafcb262275300a545f3ed7` (`round-18: measured SCORECARD depth7→8…`, dated 2026-10-20 18:49:16 -0300); `git diff --stat 4b7c682 HEAD -- .ufo/evidence/round-18/measure.py` produced no output.

2. CLI surface:

   ```text
   python3 /tmp/a04_r18/measure_r18.py --help
   usage: measure_r18.py [-h] [--rev REV] [--repo REPO]
                         [--ledger-file LEDGER_FILE] [--ledger-rev REV:PATH]
                         [--inputs-overlay FILE] [--explain] [--selftest]
   ```

3. Strict measurement with section explanations (no override flags):

   ```text
   python3 /tmp/a04_r18/measure_r18.py \
     --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
     --rev 4b7c682 --explain
   ```

   Observed JSON summary (the full output also contains per-section details and declared `external_inputs`):

   ```json
   {
     "revision": "4b7c6823a462f5ea2eafcb262275300a545f3ed7",
     "rev_input": "4b7c682",
     "recorded_cases": 8,
     "depth_score": 8,
     "ledger_guardrail": {
       "header_legs": 8,
       "regression_calls": 8,
       "selftest_tuples": 8,
       "lists_agree": true,
       "unique_recorded_gates": 8
     },
     "shonen": {
       "marks": ["~", "~", "~", "~"],
       "box3_ledger_link": true,
       "box3_points": true
     },
     "coldread": {
       "sections_covered": 60,
       "sections_total": 60,
       "missing": [],
       "box3_full_page": true,
       "reasons": {"credited": 60},
       "inputs_overlay_merged": 0
     },
     "calibration_restraint_score": 8,
     "sources": {
       "rows": 76,
       "malformed": 0,
       "tiers": {"A": 67, "B": 7, "C": 2},
       "status": {"mined": 48, "queued": 23, "rejected": 5}
     },
     "overrides_used": false,
     "trace_gate": "strict",
     "ledger_source": "rev",
     "ledger_committed": true
   }
   ```

## What the output certifies

For the resolved commit named in `revision`, the instrument computes the following predicates from committed blobs:

- `depth_score: 8` is a count of eight matching case-header comment lines in `tools/mutate-and-run.sh`, capped at ten. `ledger_guardrail` separately reports that this count agrees with eight regression-call patterns and eight selftest tuple patterns.
- `coldread.sections_covered: 60/60` means each section produced by the script's SKILL sectionizer has a matching section hash and at least one ledger entry passing its defined verdict/class, command-count, input-digest, and strict trace-receipt gates. The default ledger is read from the same pinned revision; the output says it is committed there. In strict mode an executed-command entry needs a committed trace receipt; trace inputs are compared to the recorded input set and input digests, and lane-local live reads are checked against the pinned revision.
- The `shonen` fields report parsed checklist marks and whether box 3 carries the expected round-18 ledger link; `box3_points` also requires full-page cold-read coverage. `calibration_restraint_score: 8` is the script's formula over those marks/link/coverage predicates.
- `sources` is a row/shape/tier/status census of `corpus/SOURCES.md`.
- With `--explain`, each cold-read section additionally has its ending line (`end`) and a sorted, deduplicated list of per-entry credit/failure reasons. The normal fields and score are still computed by `measure()`; explain mode only changes the per-section detail shape (source lines 540–546, 659–713; synthetic explain assertion at lines 1003–1011).

The current run used no overrides: `overrides_used: false`, `trace_gate: "strict"`, `ledger_source: "rev"`, and `ledger_committed: true`.

## What it explicitly does not certify / residual risk

- **No override-based run is claimable.** The header explicitly calls `--ledger-file`, `--ledger-rev`, and `--inputs-overlay` a measurement aid, changes their trace mode to `legacy`, and says “A claim must never use overrides” (source lines 67–71). The observed run did not use them.
- It does not execute the eight listed mutation/regression cases: `depth_score` is derived from regex-counted header comments, while the guardrail only compares source-pattern counts. The direct run was a measurement, not `--selftest` or the lane's final suite.
- The cold-read result is a validation of committed ledger declarations and trace/input bindings, not proof that a human independently read every section, that a claimed command actually ran or passed, or that the ledger/trace author was truthful. The trace code binds inputs and receipt metadata; it does not execute or verify command argv/output (header lines 33–76; `trace_reason()` lines 373–429).
- Coverage is per the script's fail-closed aggregation rule, not a claim that every matching ledger entry is clean: a section may be covered by a credited entry while stale failing entries do not veto. The observed `--explain` arrays include `input-drift` and `verdict:wrong-expectation` reasons on some otherwise covered sections; their `vetoed` fields are false. The summary histogram counts final section outcomes (`credited: 60`), not every reason observed.
- `external_inputs` is copied from ledger entries into the output (source lines 602–608); this operation does not independently fetch or validate those external files/digests. `sources` likewise counts/parses table rows; it is not a source-content audit. The restraint score is a static checklist formula, not an independent calibration study or promotion authorization.

## Verification gaps

- The mounted tools do not provide an `lsp` device: `read xd://lsp` returned “No such tool: xd://lsp” and listed the available devices. Accordingly, no LSP status/references/definition/diagnostics were available. This was a historical single-script behavior check, not a changed-caller review; no grep result is used as semantic proof.
- `--help` and the pinned strict `--rev … --explain` invocation were exercised. Malformed/unresolvable `--rev` exits and `--selftest` were not separately run; their handling was read in source (lines 89–97, 1520–1567 and 884–1501). No lane final suite, build, linter, or formatter was run.
- No tools were installed or updated.
