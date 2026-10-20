# ControlThreats — C1 contract critic (round 12, w1)

Seat: critic, leaf. This report is advisory and internal to the lane. It is not
non-author promotion or admission, and it records no gate pass. The gate file
`tools/repeat-control.py` did not exist while I wrote this
(`ls tools/` → `mutate-and-run.sh` only), so no gate output appears anywhere in
this report.
Axes: calibration (primary), depth (as it bears on the C1 claim's wording).

## Evidence (all owned, in `.ufo/evidence/round-12/ControlThreats/`)

- `probes.py` measures the raw facts the contract compares: exit, stdout bytes
  and stderr bytes per run. It is not a gate model and never assigns finding IDs.
- `probes.out` is the output of
  `python3 .ufo/evidence/round-12/ControlThreats/probes.py --legs /home/vgpnk/Projects/shokunin`
  (2026-10-20T02:16:05Z, Python 3.14.7, node v24.21.0). It ends with an
  append-only errata block.
- `gate-probes.sh` holds 23 refusal rows for the gate (R1–R12 plus the note
  R13). I have not run it against the gate because the gate is absent. Its only
  observed run is `bash gate-probes.sh` → `GATE_PROBES: SETUP (gate missing …)`
  with exit 2. I checked that the fixture argv's per-run values are right by
  running them directly three times: CRLF/LF/CRLF, stderr e/e/f, and exits
  1/0/0. `bash -n` reports no syntax errors.

## Counterexamples (strongest first)

### CT-1 Precedence makes one clause unreachable (contract defect, fixable)
The contract says "any nonzero baseline is could-not-evaluate, any output/exit
disagreement fails". Read nonzero-first, the exit-disagreement half can never
fire, because every exit disagreement includes a nonzero exit. Under that
reading `controls_mismatch`/1 is reachable only through output differences with
exits [0,0,0].
- Measured case: `probes.out` P6 cold-first-run gives exits `[1, 0, 0]` and
  stdout `cold/warm/warm`.
- Smallest correction: disagreement in exit, stdout or stderr →
  `controls_mismatch`/1. Then all-equal with a nonzero exit →
  `baseline_nonzero`/2. Otherwise → `controls_match`/0.
- ExitReview confirmed this by message. ExitReview reports that Main's L1
  ruling is disagreement-first; I have not seen that ruling myself.
- Probe rows: R5 `[0,0,1]`, R5b `[1,0,0]`, R5c `[1,2,1]` expect
  `controls_mismatch`/1; R6 `[1,1,1]` and R6b SIGKILL expect
  `baseline_nonzero`/2.
- Axis: calibration.

### CT-2 `controls_match` admits flaky and time-dependent controls (claim bound, a tradeoff rather than a defect)
- **P1 (measured):** a control that fails at random 10% of the time produced
  three exit-0 runs in **223/300** triples. The model (1-p)^3 gives 0.729.
  With N=3, a control flaking at rate p still gets `controls_match` with
  probability (1-p)^3, which is 0.97 at p=0.01.
- **P2 (measured):** `date +%s` gave identical triples in **50/50** trials,
  because the output depends on the wall clock but back-to-back runs share a
  second. `date +%N` gave 0/50.
- **P6 (measured):** a second invocation with warm state gives an identical
  `[0,0,0]` triple. A match therefore says nothing about cold-start behaviour,
  because runs share the filesystem and the earlier invocations' state.
- Wording correction (no code): `controls_match` means "N identical byte
  observations in one environment, run back to back". It does not mean
  deterministic, stateless, cross-environment, or not flaky. The contract
  already disclaims determinism, so the risk is report wording that says
  "clean" or "pristine control stable".
- Probe rows: R10 `date +%s` expects `controls_match`/0, which is a deliberate
  non-refusal row; R10b `date +%N` expects `controls_mismatch`/1.
- Axis: calibration.

### CT-3 Same digest, different control: input digests do not pin control identity (false-provenance risk)
- **Measured, recorded as an errata row in `probes.out`:** my P9 extraction
  dropped the git mode of kagi `corpus/checklist-run.sh`. The blob is
  `100755` at `fecee874`, and its pin sha matched. Its selftest went red:
  exits `[1,1,1]`, every case reporting `exit 126`. Re-running with only
  `chmod 755` added gave `[0,0,0]` with identical stdout
  (`CHECKLIST_SELFTEST: PASS (34 cases)`).
- So control identity includes file mode, env (`MUTANT`/`PRISTINE`/
  `WORKDIR`/`DEFECT_ID` at `tools/mutate-and-run.sh:394`) and cwd. None of
  these is in argv, and none is covered by a sha256 of the bytes. The
  contract's evidence set (numbered stdout/stderr and exit) does not record
  even argv.
- Smallest correction: `--out` writes the argv (JSON), cwd and run count, and
  `--snapshot` digests include that record. Probe R13 reports whether argv is
  recorded.
- Axes: calibration and provenance.

### CT-4 Do not count it as the runner's control (identity change and overreach)
- The runner still runs **one** control: `run_one "$PRISTINE" …` at
  `tools/mutate-and-run.sh:466`. That run is `timeout bash -c "$SUITE"` with
  merged `2>&1` on a mktemp pristine copy (`:394-395`, `:421`, `:431`).
- `repeat-control` runs exact argv with split streams and no timeout in the
  contract. P8 shows that merged and split streams record different
  observables.
- No wording may say the 6 recorded legs now have repeated controls. Nothing
  wires the gate into the runner, and the contract forbids runner edits.
- The runner's own sweep stdout contains `MUTATE_DATE` (`:437`), `duration-ms`
  (`:471`, `:474`) and a mktemp `MUTATE_EVIDENCE` path (`:506`). Wrapping the
  runner itself in the gate would therefore always give `controls_mismatch`
  `[INFERENCE from source lines; not run]`. The gate's targets are suite
  commands, not the runner.
- A hypothesis I tested and that turned out false: "byte-exact equality is
  unusable on real controls". P9 ran all 6 leg selftests 3× on pin-verified
  blobs, with the runner's env and argv shape and the mode fixed for
  checklist-run, and stdout/stderr/exit were byte-identical within every
  triple. So byte-exact comparison is not an over-strict refusal of the
  lane's own legs, at least on this host and at this time.
- Axes: depth and calibration.

### CT-5 Python defaults that silently normalise bytes or turn spawn failures into crashes (fixable implementation traps)
- **P3:** with `text=True`, `'a\r\n' == 'a\n'` is `True`; with bytes it is
  `False`. `.strip()` hides trailing newlines. Probes R4 and R12 cover this.
- **P4:** spawn failures raise different exceptions:
  - missing command → `FileNotFoundError` errno 2
  - non-executable file → `PermissionError` 13
  - directory → `PermissionError` 13
  - no shebang → `OSError` 8 (ENOEXEC)

  An uncaught traceback exits **1** (measured `traceback-exit=1`), which
  collides with `controls_mismatch`/1 and would turn a crash into a false
  "failed". Correction: map every spawn `OSError` to `command_unavailable`/2.
  Probes R9a–d cover this. A command wrapped in `bash -c` that is missing or
  not executable spawns normally and exits 127/126, giving `baseline_nonzero`
  rather than `command_unavailable`. That is the same exit class under a
  different ID, and it should be documented rather than special-cased.
- **P5:** SIGKILL returns `-9`, and `exit 256` returns `0`. The saved exit file
  must record the returncode verbatim (for example `-9`).
- **P7:** inherited stdin turns `cat` output into `payload`; with DEVNULL it is
  empty. Probe R7 feeds the gate non-empty stdin.
- Axis: calibration.

### CT-6 Selftest mutants that need specific fixtures to be killed
I sent these to ControlGate by message:
- An `[A,A,B]` fixture (only run 3 differs) kills "compare runs 1-2 only"
  (R1). `[A,B,A]` kills "compare first vs last" (R2). R3 covers stderr.
- `--runs 2` and `--runs 1` must return 64 (R11a/b). A selftest that rejects
  only `0`/`abc` leaves the single-control case, the limitation C1 exists to
  fix, uncaught.
- `--snapshot` vacuity: if snapshot only re-hashes the files and then echoes
  the committed expectation, a classifier mutant (for example mismatch →
  match) survives. The snapshot must reclassify the stored bytes and compare
  the result with a hand-committed expected ID and exit. Digest integrity
  catches accidental edits only; editing a file and its digest together is not
  detected. That limit belongs in the claim. SnapshotReview owns the details.

## Risks not resolved here
- None of the 23 `gate-probes.sh` rows has an observed outcome. They need L1
  or ControlGate to run them once the gate lands.
- The rows assume the finding ID appears on stdout or stderr; the contract
  does not fix the output format.
- No timeout is in the contract, so a hanging child hangs the gate. GateSecurity
  owns that, and also out-dir clobber and stale `runN` files.
- P1/P2 are statistical measurements on this host; P9 is one host at one time,
  and the harness shell (bash 5.2.37) differs from `/usr/bin/bash` 5.3.15.

## Exact owned paths
- `.ufo/evidence/round-12/ControlThreats/probes.py`
- `.ufo/evidence/round-12/ControlThreats/probes.out`
- `.ufo/evidence/round-12/ControlThreats/gate-probes.sh`
- `.ufo/waves/round-12/w1/ControlThreats.md`

Scratch went to `/tmp/tameshi-r12-ct*` and was removed. No production, sibling
or runner file was written. I installed or upgraded no tools.
