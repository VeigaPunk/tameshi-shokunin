# DeterminismProbe — pre-data determinism control for C1 (round 31)

Seat: `TameshiR31.DeterminismProbe`. Control, not production. No production file was edited, no tool was installed or upgraded, no gate was run outside the seat scratch clone. Report path: `.ufo/waves/round-31/w1/DeterminismProbe.md`.

## Axes

- Calibration: whether a base-versus-target change in C1's mismatch count can be attributed to the SCORECARD rows rather than run-to-run noise.
- Reproducibility: same frozen revision, fresh scratch, identical parsed values.
- Containment: which inputs each of the 12 frozen commands reads outside the measured revision.

## Verdict

Hypothesis **not falsified**. Two sequential runs of the frozen counter at `c111dab58b0a8d55e991bbd2efe3aad56717b95a`, each with a fresh `--work`, printed **byte-identical** `STATEMENT`/`C1_R31` lines (12 statements, `mismatches=7 unparsed=0 unobservable=0 append_only=1`, `C1_R31_PASS=false`, exit 1 both times). The signature files hash equal:

```
sha256 5b17059a4b43f3c61e1c657d6808d94437f036b44785f57267d3db5983ce9b1e  run1.sig
sha256 5b17059a4b43f3c61e1c657d6808d94437f036b44785f57267d3db5983ce9b1e  run2.sig
cmp run1.sig run2.sig -> identical
```

The nine selftest commands behind the ten `| Capability |` statements were each executed at least three times; every repetition in the counter's intended layout printed the same summary line and exited 0 (the bare-mirror negative control for the regression ledger exits 2 deterministically, see Risks). The noise floor of the counter's parsed values in this window is **zero mismatching values** across runs. This determinism is a property of the parsed value tuples, not of raw stdout: 2 of 12 observation files differ between runs, and only in temp-directory names or timestamps (see Risks 3).

Second, calibration-relevant pre-data fact: the 12 statement lines at `c111dab` are byte-identical to the frozen base receipt `.ufo/evidence/round-31/before/c1-at-base.stdout` (diff of the `STATEMENT` lines exits 0; only `rev=` differs in the `C1_R31` line). The revision frozen for this round carries no corrected rows; the 7 mismatches there are exactly the 7 of base. A later revision must carry the SCORECARD edits, and the target's delta is therefore attributable to those edits under the measured conditions.

## Exact commands and observed output

Clone and pin (working directory only under the seat scratch dir; `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset):

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r31-seats/DeterminismProbe/lane
git -C .../lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a   # HEAD verified c111dab...
```

Counter invocation (seat clone pinned as `--lane`; `--work` fresh and empty each run, runs strictly sequential; everything else is the contract command):

```
cd .../DeterminismProbe/lane
python3 .ufo/evidence/round-31/c1-measure.py --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a \
  --lane /fast/scratch/hyaku/tameshi-r31-seats/DeterminismProbe/lane \
  --work /fast/scratch/hyaku/tameshi-r31-seats/DeterminismProbe/w1   # then w2
```

The counter copy used hashes to the frozen value: `sha256 657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584` (matches `contract.json:counter_sha256`). Deviation from the contract's literal argv: `--lane` points at the seat's frozen clone rather than the live lane; git subcommands address the immutable revision, and the observed values are identical to the base receipt measured against the live lane.

Run 1 (elapsed 319 s as reported by the harness; counter exit 1; stderr empty):

```
STATEMENT sources-registry: claimed=0,44 observed=0,92 (exit=0) MISMATCH
STATEMENT mutation sweep runner: claimed=80,80,0 observed=106,106,0 (exit=0) MISMATCH
STATEMENT six-leg regression ledger: claimed=PASS,6,6,0 observed=PASS,9,9,0 (exit=0) MISMATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=18,18,0 observed=19,19,0 (exit=0) MISMATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT effective expectation reconciliation: claimed=34,34,0 observed=66,66,0 (exit=0) MISMATCH
STATEMENT retained invocation-context gate: claimed=0,49,49 observed=0,49,49 (exit=0) MATCH
STATEMENT hermetic env-differential probe: claimed=9,9 observed=9,9 (exit=0) MATCH
STATEMENT callback-authoritative wave accounting: claimed=8,8 observed=8,8 (exit=0) MATCH
STATEMENT depth: claimed=6 observed=9 (exit=0) MISMATCH
STATEMENT calibration: claimed=0 observed=8 (exit=0) MISMATCH
C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=c111dab58b0a8d55e991bbd2efe3aad56717b95a C1_R31_PASS=false
```

Run 2 (elapsed 236 s; exit 1; stderr empty) reproduced every line above byte for byte; `diff run1.sig run2.sig` exits 0. The 83 s wall-time spread is host scheduling, not parsed-value variance (statements run in 12 threads; timeouts are 300–2700 s, with the slowest command observed at ~240 s alone against a 2700 s limit).

Per-command observation files (`w1/obs-*.stdout` vs `w2/obs-*.stdout`):

- 10 of 12 byte-identical, including `depth` (`depth_score=9`), `sources-registry` (`== A rows` / `92`), and `calibration` (`calibration_restraint_score` 8).
- `obs-retained-invocation-context-gate.stdout` differs on one line only: `/tmp/tameshi-r15-verify-8tq4cncu/...` vs `/tmp/tameshi-r15-verify-dp8bdowa/...`; the matched `summary SELFTEST: PASS (49/49)` is identical.
- `obs-six-leg-regression-ledger.stdout` differs only in `REGRESSION_WORKDIR` paths and `REGRESSION_DATE` (`2026-10-23T09:06:13Z` vs `09:11:43Z`); pins, case lines, and the summary `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` are identical.

## Selftest repetitions (three or more each)

Run in the seat clone (`lane`), with the counter's environment (`GIT_*` stripped, `PYTHONDONTWRITEBYTECODE=1`, `REV` set), eight commands per repetition in one parallel wave; the regression ledger ran four times in a mirror clone with the counter's fleet layout (see below). All exits 0, all summaries identical across repetitions:

| command | summary line, 3/3 repetitions |
|---|---|
| `bash tools/mutate-and-run.sh --selftest` | `MUTATE_SELFTEST: 106/106 pass` |
| `python3 tools/repeat-control.py --selftest` | `SELFTEST: PASS (29 cases)` |
| `python3 tools/pin-disposition.py --selftest` | `SELFTEST: PASS (19/19)` |
| `python3 tools/witness-metadata.py --selftest` | `SELFTEST: PASS 39/39` |
| `python3 tools/evidence-disposition.py --selftest` | `SELFTEST: PASS (66/66)` |
| `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4d...` | `summary SELFTEST: PASS (49/49)` |
| `python3 tools/env-diff.py --selftest` | `ENVDIFF_SELFTEST: 9/9 pass` |
| `python3 tools/wave-accounting.py --selftest` | `ACCOUNTING_SELFTEST: 8/8 pass` |
| `bash tools/mutate-and-run.sh --regression --workdir <fresh>` | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` (2 in-counter runs + 2 isolated runs, distinct workdirs) |

Each summary equals the value the counter parsed in both runs (including the appended exit code 0). Per-repetition millisecond timings vary widely (e.g. `env-diff` 503/314/329 ms); values do not.

Regression containment check: `mutate-and-run.sh:1358` sets `FLEET_ROOT` to the third parent of the script, and `:1340-1341` resolves legs as `$FLEET_ROOT/<repo>/<path>`. Running `--regression` from a bare mirror without sibling repos produced, deterministically over 3/3 attempts, `REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)` with `repo_identity_mismatch` per leg and exit 2. Recreating the counter's layout (`work/fleet/` with symlinks to live siblings plus the mirror at `work/fleet/tameshi-shokunin`) gives the `PASS (cases=9 passed=9)` above. This confirms the statement's value is a function of the pinned sibling revisions/blobs, not the sibling working trees.

## Risks

1. **Pre-data state, not a defect.** At `c111dab` the counter is exactly the base receipt: `mismatches=7`, `C1_R31_PASS=false`. Any later PASS must come from row edits; the target revision named by the claim must be the one carrying them, and later commits must not touch `SCORECARD.md` or the 12 commands' inputs (the counter re-reads them from that revision).
2. **External fleet input for one statement.** The counter symlinks live `*-shokunin` repos into `work/fleet` and the regression ledger resolves its legs through that directory at pinned revs. Values are stable across runs because pins are blob-addressed (`sha256` and `rev` in each `REGRESSION_PIN`), but a sibling repo that is moved, deleted, or has its pinned revision pruned would flip legs to SETUP and change the observed tuple. The other 11 commands read only the clone (`sources-census-v2.sh:6` reads `corpus/SOURCES.md`; `depth` uses `git show REV:tools/mutate-and-run.sh`; `calibration` receives `--repo <clone> --rev <rev>`).
3. **Parsed values are deterministic; raw stdout is not.** Temp-directory names and timestamps differ between runs. A future acceptance check must compare the `STATEMENT`/`C1_R31` lines (or the parsed tuples), not the observation files byte for byte. `mutate-and-run.sh:970` documents the same for its own stdout.
4. **Timeout sensitivity under load.** Statements run concurrently; a heavily loaded host could push a command past its per-statement timeout (300 s for `depth`, 900–2700 s for the rest) and produce UNOBSERVABLE where this probe saw a value. Observed headroom is large (slowest ~240 s vs 2700 s), but the counter has no retry.
5. **Truncated observation storage.** `observe()` stores only the last 200,000 bytes. The `calibration` obs file is exactly 200,000 bytes (truncated head); the counter itself parses the full stdout, so the matched value is unaffected, but the saved artifact is not complete evidence for that statement.

## Smallest safe correction

No correction is needed for C1 or its counter; the control found no run-to-run value variance to correct. For evidence hygiene only: record the two-run signature hash `5b17059a4b43f3c61e1c657d6808d94437f036b44785f57267d3db5983ce9b1e` next to the target receipt, and re-run the counter twice at the target revision, requiring identical signatures before accepting `C1_R31_PASS=true`. Do not compare raw observation files.

## Retained evidence (seat scratch, read-only for the parent)

- `/fast/scratch/hyaku/tameshi-r31-seats/DeterminismProbe/out/run1.stdout`, `run2.stdout`, `run1.sig`, `run2.sig` (sha256 above), both stderr empty.
- `/fast/scratch/hyaku/tameshi-r31-seats/DeterminismProbe/w1/obs-*.stdout`, `w2/obs-*.stdout` — per-statement observations for the two runs.
- `/fast/scratch/hyaku/tameshi-r31-seats/DeterminismProbe/out/nine/` — `index-fast.txt` (24 lines: 8 commands x 3 repetitions, every exit 0), `index-regression.txt`, `<command>-r{1,2,3}.stdout/.stderr`, `regression-fleet-r1.stdout` and `regression-fleet-r2.stdout` (fleet layout, exit 0 at 240 s and 190 s), and `regression-r{1,2,3}.stdout` (the no-sibling SETUP demonstration, exit 2 each).
- Host conditions during the probe: Linux 7.2.11-arch1-1, Python 3.14.8, git 2.56.0, 32 CPUs.
