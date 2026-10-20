# CausalCritic — round 13 w1 (read-only)

Scope: try to falsify the claim that C1 (six-leg pin dispositions, depth) and C2 (normalized `declaration.kind` companion, calibration) are causally separable. Each claim must still hold, measure and verify when the other claim's artifacts are absent, broken or reverted.

State at inspection: HEAD `546b371a`.
- First pass: only `pin-manifest.json`, `incremental-pin-disposition.md`, and L1's `before.json`, `claims.json` and `measure.py` were present.
- Final pass: `tools/pin-disposition.py` and `tools/witness-metadata.py` had landed. I inspected them statically (grep and read only).
- Still absent: `witness-metadata.json` and `pin-dispositions.json`.

No checks, tests or gates were run. No tools were installed.

Landed-tool observations:
- **C2 tool** (`witness-metadata.py`):
  - Anchors only three named frozen files (`:68-84`: summary `acc01268…`, declaration `e8d2024a…`, declared `0def0d3b…`).
  - Does not hash `tools/mutate-and-run.sh` or `bash-witness-study.py`; they appear only inside the disclosure literal and the docstring (`:5`, `:92`).
  - Has no `rglob`, directory listing, `git`, or `pin-` read.
  - So K1 and K2 are satisfied for C2.
  - The rerun summary is not anchored: no `rerun` match in the file. **K6 is open.**
- **C1 tool** (`pin-disposition.py`):
  - Reads only itself (`:136`), the manifest (`:447`) and sibling worktree/git.
  - Builds `GIT_*`-scrubbed env copies per call (`:170`, `:617`) without mutating `os.environ`.
  - Selftest uses `mkdtemp` (`:572`).
  - Has no `witness`, `BashWitness`, `round-12` or `metadata` match.
  - So K5 is satisfied for C1.
  - No runner-digest anchor: no `75ed934d` or `derived_from` match in either the tool or `pin-manifest.json`. **The K1 recommendation remains open for C1.**

## Verdict

**Separable by construction today, with one shared root and two L1 measurement defects that could break that.**
- The landed C1 artifacts have no C2 reference. `pin-manifest.json:1-55` names only runner anchors. `incremental-pin-disposition.md` has no `witness`, `BashWitness`, `round-12`, `metadata` or `calibration` match.
- The two claims share no evidence file: C1 reads sibling git objects, C2 reads the frozen round-12 BashWitness bytes.
- They do share one common-cause input: `tools/mutate-and-run.sh` (`75ed934d…adc5`).

## Counterexamples and evidence

**K1 — shared root: the runner (high).**
- C1 takes its pins from `tools/mutate-and-run.sh:542-553` (`pin-manifest.json:3`).
- C2's precondition is round-12 witness integrity. `tools/bash-witness-study.py check` live-hashes the same runner and reports `DRIFT` on mismatch (`:1138-1147`; committed runner digest at `declaration.json:42-45`).
- So one edit to the runner made for C1 (for example a disposition comment or header row) makes the round-12 witness check fail. If `witness-metadata.py --check` re-verifies `inputs.runner`, C2 fails as well, through no defect of its own.
- The same edit can also shift command D. That count is a raw regex over the runner header (`round-13/measure.py:30`).
- Axes affected: calibration (C2 falsely red), depth (scalar drift).

**K2 — shared directory file-set (medium).**
- BashWitness's checker requires exact file-set equality and reports `UNLISTED` for any extra file (`bash-witness-study.py:1182-1184`; `manifest_files` rglob at `:811-821`).
- If MetadataRepair copies that pattern onto `.ufo/evidence/round-13/`, C1's `pin-manifest.json` and `pin-dispositions.json` would fail C2.
- Correction: anchor C2 to named files only.

**K3 — one measurement script crashes for both claims (L1 defect, medium).**
- `round-13/measure.py:19-20,27-28` calls `json.loads` with no guard. A malformed `pin-dispositions.json` raises before anything is printed, so C2's companion is never measured. The reverse also holds.
- `:39` calls `hashlib.sha256(None)` (a TypeError) when the frozen summary is absent.
- Smallest correction: wrap each artifact read so that a failure is recorded as `{"error": …}` for that key only.
- `metadata_companion_present` (`:32`) records presence only. It is not C2's claim (consistency); that needs the gate exit.

**K4 — `before.json` was not produced by the current `measure.py` (L1 defect, medium).**
- `before.json` (01:46) has 9 keys. It lacks `recorded_cases`, `unique_recorded_gates`, `calibration_restraint_score`, `calibration_*_boxes` and `metadata_companion_present`.
- `measure.py` (01:48) emits all of those.
- So the before side of "depth6/calibration6 unchanged" is not on record from the same script. Regenerate `before.json` at `546b371` with the final `measure.py` before the after-measurement.

**K5 — cross-citation would make a failed claim look good (attribution, high if it occurs).**
- The `bash-surface-census` leg is C2's target. `BashWitness/pristine.sh` has the same digest as `PIN_BASH` (`275d8294…`), and kagi's current blob equals the pinned blob (`dcf878b9` at both `HEAD` and `fecee87`).
- Two shortcuts are tempting:
  - C1 using BashWitness bytes as its "original evidence";
  - C2 or the lesson citing C1's `unchanged` as support for the round-12 witness result.
- Either one makes one claim's failure invisible behind the other.
- Likewise, C1's `result_reuse=not_established` is a restraint statement. If it is cited on the calibration axis, calibration would still read "improved" with C2 removed.
- Per-axis citations must be disjoint: depth cites C1 only, calibration cites C2 only.

**K6 — a frozen null not covered (C2 completeness).**
- `BashWitness/rerun-20261020T035435Z/summary.json:15` (`6726421f…`) also has `"kind": null`.
- A companion that anchors only the top-level `summary.json` (`acc01268…`) leaves one historical null unaddressed. Cover it, or scope it out explicitly.

## Conditions for each owner (messages sent)

**MetadataRepair** (`TameshiR13.MetadataRepair`):
- Do not live-hash `tools/mutate-and-run.sh` or `tools/bash-witness-study.py` in `--check`. Copy their digests from the frozen JSON as historical facts.
- Use named-file anchors only, never round-13 directory equality.
- Never read pin artifacts, sibling repos or git.
- Address the rerun summary null (K6).

**PinProbe** (`TameshiR13.PinProbe`):
- Never read `round-12/BashWitness/*` or `witness-metadata.json`.
- Add `derived_from: {tools/mutate-and-run.sh, 75ed934d…adc5}` to the manifest so drift in the shared root is detectable. Today it pins only line ranges.
- Selftest scratch via `mkdtemp`; scrub `GIT_*` per subprocess, never `os.environ`.

**L1:**
- Fix K3 and K4.
- Keep per-axis citations disjoint (K5).
- The runner must stay byte-identical this round.

## Checks L1 should run (not executed here)

1. Shared root unchanged:
   - `git diff --quiet 546b371 -- tools/mutate-and-run.sh tools/bash-witness-study.py .ufo/evidence/round-12`, expect exit 0.
   - `sha256sum tools/mutate-and-run.sh` = `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`.
2. Static isolation:
   - `grep -nE 'witness|BashWitness|round-12|metadata' tools/pin-disposition.py .ufo/evidence/round-13/pin-manifest.json` must have no match that is read or loaded.
   - `grep -nE 'pin-(manifest|disposition)|mutate-and-run|bash-witness-study\.py|kagi|git' tools/witness-metadata.py` must show no read or hash of those paths (historical literal strings only).
3. C1-only ablation:
   - `git worktree add /tmp/r13-c1 546b371`.
   - Copy only `tools/pin-disposition.py` and `pin-manifest.json` into it.
   - Run `python3 tools/pin-disposition.py --selftest`, and `--manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`.
   - Expect the same exits, and per-row status and `result_reuse` equal to the integrated run (timestamps excluded).
4. C2-only ablation:
   - `git worktree add /tmp/r13-c2 546b371`.
   - Copy only `tools/witness-metadata.py` and `witness-metadata.json` into it.
   - Run `python3 tools/witness-metadata.py --selftest` and `--check`. Expect exit 0 `metadata_consistent`, identical to the integrated run.
5. Cross-tamper in a scratch copy of the integrated tree:
   - Corrupt `pin-manifest.json` (and a constructed `pin-dispositions.json`). `witness-metadata.py --check` exit and stdout must be unchanged.
   - Corrupt `witness-metadata.json`. `pin-disposition.py` output must be unchanged.
   - Add a stray file to `.ufo/evidence/round-13/`. C2 `--check` must still exit 0 (K2).
6. Runner-edit sensitivity, in a scratch copy only: append one comment line to the runner.
   - `bash-witness-study.py check` should report `DRIFT`.
   - `witness-metadata.py --check` must stay exit 0 (K1).
   - Command D must still print `recorded_cases=6`.
7. Measurement isolation, after the K3 fix: run `python3 .ufo/evidence/round-13/measure.py --rev <round>` with a malformed `pin-dispositions.json` blob in a scratch commit. It must still emit `metadata_companion` and `frozen_summary_sha256`.
8. Before/after parity:
   - Regenerate `before.json` with the final `measure.py --rev 546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50`.
   - Its key set must equal the after-run key set.
   - Expect `recorded_cases=6` and `calibration_restraint_score=6` on both sides.
9. Per-axis citation audit: the SCORECARD/lesson depth verdict cites only C1 paths, and the calibration verdict cites only C2 paths plus QUALITY14. No row cites C1's `unchanged` as support for the BashWitness result.

## Not established

- Runtime behaviour of `pin-disposition.py` and `witness-metadata.py`: I inspected source only and executed nothing. Isolation is observed statically (K1/K2 hold for C2; K5 holds for C1). Ablations 3–7 are what make it a runtime fact. K6 (rerun-summary null) and the C1 runner-digest anchor are open, as observed in source.
- ScoreRestraint F3 (C2 cannot move calibration under `measure.py`) is consistent with "6→6". Whether a non-scalar "improved" verdict is admissible is AdmissionCritic's question, not this seat's.
