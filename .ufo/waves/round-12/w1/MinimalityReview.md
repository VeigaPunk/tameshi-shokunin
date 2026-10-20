# MinimalityReview — tameshi round 12, wave w1

Status: advisory, lane-internal. Deletions and merges only. No production edits, no tests or suites run, no independent authority claimed.
Evidence: .ufo/evidence/round-12/MinimalityReview/probes.md (P1–P7).

## 1. State observed

- `tools/repeat-control.py` does not exist yet. `tools/bash-witness-study.py` does not exist yet. `.ufo/evidence/round-12/` did not exist before this seat wrote its own directory. So this review targets the contract text in `.ufo/waves/round-12/dispatch.json` plus the existing runner `tools/mutate-and-run.sh` (1642 lines).
- Pinned kagi object resolves at `kagi-shokunin/` (fleet root). The path `.tower/worktrees/kaika/kagi-shokunin` named in older evidence does not resolve here. Object `fecee874` exists and `git show fecee874:corpus/surface-census.sh` has sha256 `275d8294…3009f`, equal to `PIN_BASH` (runner:544).

## 2. Deletions and merges, ranked by size saved

### Repeat-control gate (`tools/repeat-control.py`)

R1. **One comparator, one finding map.** Contract IDs are `controls_match`, `controls_mismatch`, `baseline_nonzero`, `command_unavailable`, `snapshot_tampered`, plus usage. The task text lists separate "output mismatch / stderr mismatch / exit mismatch" selftest cases. Do not create per-kind finding IDs. Report the kind in the detail line and in the saved files. Delete any per-kind enum.

R2. **Do not use argparse.** Python 3.14.7 argparse exits **2** on bad usage (probe P3). The contract requires usage errors to exit **64**, and exit 2 means could-not-evaluate. Hand-parse `--runs N --out DIR -- ARGV…` (about 15 lines) or subclass `error` to exit 64. Either way, no second exit-code path.

R3. **One expected-values file.** The task asks for `expected.json` for fixtures and for `--selftest` to check "exact IDs/exits". Keep one table. `--selftest` and `--snapshot` both read `.ufo/evidence/round-12/ControlGate/expected.json`. Do not hard-code a second table in the script.

R4. **`--snapshot` reuses the comparator.** Snapshot verification should compare saved `N.stdout`, `N.stderr`, `N.exit` files with the same equality function used for live runs, then check digests and expected ID/exit. A separate diff or classifier path is unneeded.

R5. **No timeout, retry, or statistics.** The contract asks for equality only: "no flakiness cured or determinism proven". Do not add `--timeout`, retry, or entropy or flake scoring. Not a deletion, but a guard against feature creep.

R6. **Precedence is undefined in the contract (decision needed, not a deletion).** A run can be nonzero and also differ from another run, and the command may be missing. Proposed fixed order: usage (64) > command_unavailable (2) > baseline_nonzero (2) > controls_mismatch (1) > controls_match (0). "Any nonzero baseline" is read as: any run exits nonzero. L1 should confirm both readings before the selftest is written.

### Bash witness study (`tools/bash-witness-study.py`)

B1. **Do not copy the 10-defect spec.** It already lives in the runner at heredoc lines 630–674. A second copy in Python is a drift surface. Extract the bytes between `cat >"$d/bash-surface-census.spec" <<'EOT'` and the closing `EOT` line at run time, then write them to a temp file. The runner's own sweep already checks count==1 per `@old` and `defects=10`.

B2. **Do not copy the materialization.** `regression_case` (runner 932–963) does `git show` + sha check + mode mirror. The study needs only `git -C kagi-shokunin show fecee874:corpus/surface-census.sh` plus `sha256 == PIN_BASH`. Drop the exec-bit mirror: the suite is `bash "$MUTANT" --selftest`, so the file is never re-executed. The runner cannot be sourced as a library (R-probe P4: top-level dispatch at 1620–1642), so the duplication of three lines is forced. Accept it; do not refactor the runner (contract: no edits).

B3. **Do not re-classify exits.** The runner already writes `results.tsv` with the verdict column (run_sweep 477–494). The study must read that column and add only the witness split on top. Deleting the study's own exit→verdict mapping removes one of two copies.

B4. **One "rerun" path, not two.** The contract asks for rerun-with-static-TSV and for a counting command. Implement a single `classify` step that reads `evidence/*.out` + `declared.tsv` + `results.tsv` and writes `summary.json`. `run` = sweep then classify. Printed counts come from `summary.json`, not a second computation.

B5. **One failure-label grammar: `bad-case`.** Peer measurement (WitnessThreats, not re-run here): pristine `--selftest` stdout has 0 lines starting with `PROBE`; PROBE lines appear only inside `    | ` bad-case dumps when a the-janitor handler resolves. So `bad-case NN <name> exit=…` is the only top-level failure grammar and there is no double-count choice. My earlier "two grammars" claim is withdrawn. Declare witnesses against `bad-case` names and record them in declared.tsv before the experiment. [INFERENCE: run_case body not fully read.]

## 3. Risks (not fixable by deletion)

- **Default-path determinism of the kagi selftest is unverified.** A probe detail prints `after ${wall}s` (surface-census ~617), but only under `--deep`; the default path is `SKIP` (~605). The contract's byte-identity rule would then hold for the default path. Not run; BashWitness's repeat-control step is the first real check.
- **Stale evidence paths.** `.ufo/evidence/kaika-round-1/witness/README.md` and `declared.tsv` cite `.tower/worktrees/kaika/…` pins that do not resolve. Use `kagi-shokunin/` for new pins; do not cite the old paths as reproduction.
- **Prior exposure (disclosed).** This seat read the recorded per-defect bash verdicts (runner:555, TABLE_BASH), the js witness declared.tsv, and recorded kill-rate totals (8/10 for bash-surface-census). BashWitness must not treat declarations written after this review as blind.

## 4. Checked and kept (not deletion candidates)

- `tools/mutate-and-run.sh`: no edits in scope; the sweep control and the regression comparator are separate concerns and both stay.
- Control concept in two tools (runner `run_sweep` 465–474 and the new N-run gate): intentional per contract ("New capability independent of mutation runner"). Do not add `--repeat` to the runner.
- `.ufo/evidence/kaika-round-1/sources-census.sh` (10 lines) and `sources-census-v2.sh` (20 lines): both retained. v1 is cited in `LOG.md`, `SCORECARD.md`, and `corpus/lessons/round-1.md`; cited provenance is not deleted.

## 5. Tooling record

- No tools installed or updated by this seat. Used `python3` 3.14.7 (host), `git`, `sha256sum`, `grep`, `sed`.

## 6. Owned paths

- Written: `.ufo/waves/round-12/w1/MinimalityReview.md` (this report).
- Written: `.ufo/evidence/round-12/MinimalityReview/probes.md`.
- Scratch (outside repo): `/tmp/mr-surface-census.sh` (pinned blob copy, sha `275d8294…`).
- Not written: any production file (`tools/*`, corpus, LOG, SCORECARD, SKILL).

## 7. Checks for L1 after siblings land

- `python3 tools/repeat-control.py --selftest` exit codes and IDs must match `expected.json` exactly, with usage exit 64 (R2).
- Confirm no second exit-2 path in repeat-control (R2, R6).
- Confirm `bash-witness-study.py` spec bytes equal the runner heredoc (B1) and that `results.tsv` verdicts are used directly (B3).
