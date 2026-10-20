# WitnessIntegrity — bash-witness-study declare/check/count chain (round 12, w2)

Seat: TameshiR12.WitnessIntegrity, leaf reviewer. Advisory, lane-internal. Not an independent non-author admission, not a pass.
Scope: read-only static review. The script was NOT executed (no `check`, `count`, `rerun`, `run`, `selftest`). No installs.
Subject: `tools/bash-witness-study.py`, sha256 `dbfc34d1…d9ea9`, 1173 lines, mtime 2026-10-20 00:44:58. The file changed while I was reading it: an earlier read showed `runner_pins` with a 64-hex `REV_BASH` regex, and the current version uses `REV_RE` with `[0-9a-f]{7,64}`. All line refs below are to the current version.

## Question
Can a stale, tampered, or retrofitted summary or declaration come out of `check` or `count` as clean?

## Answer
**Yes.** Several paths reach a clean outcome (exit 0, `WITNESS_CHECK: CLEAN`, or `count` exit 0 with stored counts) with no tamper detected. The main reasons:
- `check` treats `manifest.json` as optional and trusts whatever file list it contains.
- `declared.tsv` and `declaration.json` are an unanchored pair. Each is only checked against the other.
- `count` does not re-classify. It prints the counts and classifications stored in `summary.json`.
- Nothing outside the evidence directory anchors any of these files.

Current state of `.ufo/evidence/round-12/BashWitness/`: it holds only `pristine.sh`, `declare.out`, `selftest.out`, and `declaration-hash.txt`. There is no `declared.tsv`, `declaration.json`, `summary.json`, or `manifest.json`. `load_declaration` (437-444) raises `Cannot`, so `check` and `count` cannot report clean today. That is the only reason no clean result exists yet.

## Findings (by severity)

### High
**H1. `check` returns CLEAN with no manifest, or with a pruned manifest.**
- `cmd_check` 941-954: if `manifest.json` is absent it prints a note and continues, with no failure.
- 944: the loop covers only the keys of `manifest["files"]`. `{"files": {}}` checks nothing.
- 960-962: the output is `CLEAN`, exit 0.
- Consequence: deleting `manifest.json`, or editing its `files` map, makes `summary.json`, `sweep/**`, and the cli logs unverified while `check` still prints CLEAN. Without a manifest, `summary.json` is never read by `check` at all.
- `check` also never requires the mandatory set (declaration, declared, target, spec, summary) to appear in the manifest.

**H2. `declared.tsv` + `declaration.json` can be rewritten together and still pass.**
- `verify_declared_digest` 447-456 compares `declared.tsv` to `declaration["declared"]["sha256"]`. That value lives in `declaration.json`, which is itself unanchored.
- `declared.tsv` rows are never compared to the in-code constant `DECLARED_WITNESSES` (102-160). Nothing compares them to git either.
- `parse_declared_tsv` 338-358 skips `#` lines. The header's `target/spec/runner sha256=` values (316-321) are decorative and never checked.
- `declaration.json`'s `none_rows`, `rows`, and `spec.defects` (764-779 area in `cmd_declare`) are never checked against the TSV.
- Consequence: changing a witness mapping (e.g. `NONE` to `clean`) after results is undetected by `check` and `count` once the digest in `declaration.json` is updated. Both files live in an untracked directory (`git status`: `?? .ufo/evidence/round-12/`). The tool itself is untracked too (`?? tools/bash-witness-study.py`), so no commit anchors the "frozen before sweep" claim.

**H3. `count` does not re-evaluate. It prints stored results.**
- The docstring (lines 18-19) says "re-evaluate the retained sweep against the static declared TSV". `cmd_count` 883-916 does not do that.
- 887: `declared = parse_declared_tsv(...)` runs, and `declared` is never used.
- 901-908: rows come from `summary["rows"]`. The `declared=` column comes from the stored `row["declared_witness"]` (903), not from the TSV.
- 909: `tally = summary.get("counts", counts(rows))`. Stored counts win over rows. Exit at 916 depends on the stored `unresolved`.
- Consequence: an edited `summary.json` with `counts.unresolved=[]` and `classification` rewritten to `survived` prints clean and exits 0. Its only gate is 892-895, which compares the summary's own `declaration.sha256` (self-reported) to the current declared digest. An attacker can copy that value.
- `count` never checks `summary["status"]`, `row["raw_log_sha256"]`, or the contents of `sweep/`.

**H4. `rerun` destroys the committed summary before comparing, and the comparison cannot succeed.**
- `_execute_sweep` 841-842 writes `evidence/summary.json` and `manifest.json` for the fresh run. `_cannot_summary` (818-819) does the same on failure.
- `cmd_rerun` 868-871: `committed = evidence/summary.json` is read after the overwrite, so `prior` is the new summary. `fresh = rundir/summary.json`, but nothing writes that file: `_execute_sweep` writes only to `evidence/`. The `read_text` (871) raises `Cannot`.
- Consequence: `rerun` silently replaces the committed summary and then exits 2 without ever producing the agreement line. Even if the read succeeded, `prior` would equal `fresh` (tautology). Deviations from the committed run are never detectable through `rerun`.
- The selftest does not exercise `cmd_rerun` (see M3).

### Medium
**M1. `check` and `count` never verify the spec or the pin.**
- `ensure_target_and_spec` (459-506), used by `run` and `rerun` via `_prepare`, checks: target sha vs declaration, spec sha vs declaration, spec-vs-runner heredoc only when the spec file is absent (486-490), runner sha, and `PIN_BASH == declaration target sha` (500-503).
- `cmd_check` 919-962 and `cmd_count` 883-916 call none of these. They do not call `extract_spec`, `runner_pins`, or `ensure_target_and_spec`.
- Consequence: a `bash-surface-census.spec` file that differs from the runner heredoc, with `inputs.spec.sha256` updated to match, passes `check` (481-485 compares only to the declaration). `run` also accepts it, because `ensure_target_and_spec` stops at the committed hash when the file exists (482-485). A tampered `pristine.sh` with `declaration.inputs.target.sha256` updated also passes `check` and `count`, while `run` would refuse with `pin-mismatch`.

**M2. Stale summary can be counted as current.**
- `_execute_sweep` 837 calls `collect_results` after `run_sweep` has already created `sweep/`. If `collect_results` raises `Cannot` (missing raw log, 6-field check), `summary.json` (841) and `manifest.json` (842) are not rewritten. The run exits 2.
- `cmd_run` 856 refuses while `sweep/` exists, and `count` (888-891) then reads the prior summary without comparing it to the current `sweep/` contents. Consequence: `count` shows counts from a summary that no longer describes the directory. Only `check` would catch this, and only if the manifest exists (M3's gap applies).

**M3. Manifest scope and the selftest gap.**
- `write_manifest` 701-716: the covered list (702) omits `manifest.json` itself, so nothing anchors the manifest. Files added under `sweep/` after the manifest was written are never enumerated by `check` (944 iterates only listed names). `rerun-<stamp>/` and `rerun-<stamp>.cli.log` are outside the manifest (862-865; `write_manifest` covers only `sweep/` and `sweep.cli.*`).
- `cmd_selftest` 965-1119 exercises only `extract_spec`, `parse_spec`, `runner_pins`, `unescape`, `spec_precheck`, `classify`, `parse_case_lines`, `declared_tsv_text`/`parse_declared_tsv`, and `verify_declared_digest`. It has no case for `cmd_check`, `cmd_count`, `cmd_rerun`, `write_manifest`, `build_summary`, or summary tamper. The `selftest.out` 21/21 PASS (from an earlier version, same log) therefore says nothing about the integrity chain.

**M4. The freeze is an existence check, not a commitment.**
- `cmd_declare` 721-726 refuses only when `declared.tsv` exists. Deleting `declared.tsv` and `declaration.json` (keeping `pristine.sh`, `summary.json` optional) allows a fresh `declare` with a new mapping and fresh self-reported `created_at` (`utc_stamp`, 756). Only a stale summary's linkage (892-895) would expose that, and only if the summary is kept.
- `.ufo/evidence/round-12/BashWitness/declaration-hash.txt` (sha of `pristine.sh` only) is written outside the tool. No code path reads it. It is not covered by `check`.
- The external time record that `WitnessThreats.md` (correction 7) asked for ("send the sha256 of the declared TSV to Main before the sweep") is not implemented in the tool.

### Low
**L1.** `collect_results` 556-600 gets witnesses from `declared.get(ident)`. A missing TSV row becomes `None`, i.e. `NONE`, so the defect is counted `accidental`. This is fail-visible, not clean, but it is silent about the cause (no reason string names the missing row).

**L2.** Classification trusts stdout labels. `parse_case_lines` 360-390 counts every unindented `bad-case NN name` line in the mutant's own output. A mutant that prints a declared label while exiting nonzero is recorded `killed-on-witness`. `run_problems` only checks the count and numbering of case lines, not their provenance. Residual by design; not a bypass of the chain.

**L3.** `summary["status"]` is written (673) and never read by `count` or `check`. `count` exit depends only on stored `counts.unresolved` (H3).

**L4.** `write_json` (659-662) writes `.tmp` then `os.replace`, so partial writes are not visible. Fine. But `write_manifest` is called after `write_json(summary)` (841-842), so a crash between the two leaves a summary newer than its manifest. `check` then reports TAMPER on the summary, which is the correct outcome.

## What holds (verified by reading)
- Editing `declared.tsv` without updating `declaration.json` is refused with a named `TAMPER declared.tsv` in `check`, `count`, `run`, and `rerun` (447-456; called at 806, 886, 923).
- `check` verifies `pristine.sh` and `bash-surface-census.spec` against the declaration digests when present (926-934), and `tools/mutate-and-run.sh` against `inputs.runner.sha256` (935-940).
- A stale summary written before a re-declaration fails `count` with `TAMPER summary.json declaration-linkage` (892-895), provided the summary's declaration sha was not rewritten.
- `run` and `rerun` refuse a pin mismatch and a spec-vs-declaration mismatch (500-503, 485-489).
- Failure paths emit `could-not-evaluate` with all-inconclusive counts (`cannot_counts` 636-643); a missing summary or declaration yields exit 2, not clean.

## Verification gaps
- Nothing was executed. Each finding is a static reading of the current file. A reproduction would need an evidence dir built with `declare` and `run`, then the edits described in H1–H3. I did not run it per assignment.
- The file changed mid-review (see header). I did not diff the two versions; the earlier version's `REV_BASH` 64-hex regex would have made `declare` exit 2 with `runner is missing pin constant(s): REV_BASH`, which matches `BashWitness/declare.out:1`. That `declare.out` predates the current version and is stale. The current version parses a 40-hex `REV_BASH` (`REV_RE`, 175) and its selftest fixture uses 40 hex (line 998).
- `selftest.out` is from the earlier version. The current selftest has not been observed by me.
- No check of the kagi pin or the runner heredoc against the spec file was performed (static reading only).

## Tooling
Installs or updates: none. Read-only git and sha256 commands only (`git status`, `git -C ../kagi-shokunin show fecee874…:corpus/surface-census.sh | sha256sum`, `cmp`).

## Owned paths
- Written: `.ufo/waves/round-12/w2/WitnessIntegrity.md` (this file).
- Not modified: `tools/bash-witness-study.py`, `.ufo/evidence/round-12/BashWitness/*`, all other seats' files.

## Suggested fixes (for owner BashWitness / L1; none applied here)
1. `check`: require `manifest.json` (fail, not note). Require the mandatory name set in `files`, and enumerate `sweep/**` for unlisted files. Add `manifest.json`'s own digest to an external anchor (commit or main-side record).
2. `count`: re-derive classifications from `results.tsv` and `evidence/<id>.out` (or at minimum `check` first) instead of trusting stored `counts`/`classification`. Compare `counts` to `rows`. Verify `raw_log_sha256` per row.
3. Compare `declared.tsv` rows to `DECLARED_WITNESSES` in `check` and `count`, and pin the mapping to a committed git blob.
4. `rerun`: write to `rundir/summary.json`, or keep the committed summary path distinct, and compare before any overwrite.
5. `check` and `count`: call `ensure_target_and_spec`-equivalent checks (spec vs runner heredoc, PIN_BASH == target sha).
6. Selftest: add cases for `cmd_check` (manifest absent, pruned manifest, summary tamper), `cmd_count` (counts vs rows), and `cmd_rerun` (committed summary preserved).
