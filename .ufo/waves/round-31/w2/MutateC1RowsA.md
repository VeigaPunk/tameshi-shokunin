# MutateC1RowsA — frozen counter row sensitivity

**Verdict: inconclusive for killed/survived classification because the aggregate pristine detector already fails. All six assigned target-row edits were detected as their own `STATEMENT ... MISMATCH`; all six target statements are `MATCH` on both pristine and restored bytes.** No surviving target-line mutation was observed, but the red aggregate control is not counted as a mutant kill.

## Evidence

Seat: `MutateC1RowsA`. Measured axis: calibration. Probe quality axes: sensitivity, scratch isolation and exact restoration. This report does not judge or integrate C1.

All evidence paths below are relative to `/fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/` unless stated otherwise. Content revision: `2da841bd9913a2037d2bf612793382e572c9d205`. Only the six listed last rows of sandbox `SCORECARD.md` were mutated, one value and one sandbox commit at a time, each directly on that revision. Production source files were not edited.

The frozen detector selects the last matching row at `.ufo/evidence/round-31/c1-measure.py:111-123`, declares these six commands/patterns at lines 39-51, and compares parsed claimed/observed tuples at lines 206-224. Expected detector response: the altered target row becomes `MISMATCH` while its command continues to print the pristine tuple. With this already-red control, that adds one mismatch (1 → 2); restoration removes that added mismatch (2 → 1).

### Pristine control

`counter-pristine.stdout:1-6,12-13` (exit 1):

```text
STATEMENT sources-registry: claimed=0,94 observed=0,94 (exit=0) MATCH
STATEMENT mutation sweep runner: claimed=106,106,0 observed=106,106,0 (exit=0) MATCH
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=PASS,9,9,0 (exit=0) MATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=19,19,0 observed=19,19,0 (exit=0) MATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=6 (exit=0) MISMATCH
C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=2da841bd9913a2037d2bf612793382e572c9d205 C1_R31_PASS=false
```

The pre-existing mismatch is calibration, claimed 8 versus observed 6. It is not caused by any assigned mutation and is not treated as a killed mutant.

### Six independent mutations

For row k, the retained changed source is `w-k/clone/SCORECARD.md:<line>`; the exact target output is `counter-k.stdout:k` and the aggregate output is `counter-k.stdout:13`. Each run exited 1. Every other non-calibration statement remained `MATCH`; calibration remained claimed 8 / observed 6.

| Statement | Mutated stated value / source line | Exact STATEMENT line | Exact C1_R31 line | Killed or survived |
|---|---|---|---|---|
| sources-registry | `94 rows → 95 rows`; `w-1/clone/SCORECARD.md:1514` | `STATEMENT sources-registry: claimed=0,95 observed=0,94 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=f34e27aa502793f78f50e56ab89ce5a540372ad8 C1_R31_PASS=false` | Inconclusive: pristine aggregate failed; target edit detected |
| mutation sweep runner | `106/106 pass → 107/106 pass`; `w-2/clone/SCORECARD.md:1515` | `STATEMENT mutation sweep runner: claimed=107,106,0 observed=106,106,0 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=d23004d64dfaea28f2ac6165a701dad80bb5cd61 C1_R31_PASS=false` | Inconclusive: pristine aggregate failed; target edit detected |
| six-leg regression ledger | `cases=9 passed=9 → cases=10 passed=9`; `w-3/clone/SCORECARD.md:1516` | `STATEMENT six-leg regression ledger: claimed=PASS,10,9,0 observed=PASS,9,9,0 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=aac5f2ab5f90adc8c96253600f54fef7b62e753e C1_R31_PASS=false` | Inconclusive: pristine aggregate failed; target edit detected |
| repeated pristine-control gate | `29 cases → 30 cases`; `w-4/clone/SCORECARD.md:1517` | `STATEMENT repeated pristine-control gate: claimed=PASS,30,0 observed=PASS,29,0 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=6fe0f2b0868a3070b79da2710893f213449d8945 C1_R31_PASS=false` | Inconclusive: pristine aggregate failed; target edit detected |
| six-leg content-disposition probe | `19/19 PASS0 → 20/19 PASS0`; `w-5/clone/SCORECARD.md:1518` | `STATEMENT six-leg content-disposition probe: claimed=20,19,0 observed=19,19,0 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=b45514bb43cc806d2b6b080d860ec9b4747193b3 C1_R31_PASS=false` | Inconclusive: pristine aggregate failed; target edit detected |
| exposed witness provenance correction | `selftest39/39 PASS0 → selftest40/39 PASS0`; `w-6/clone/SCORECARD.md:1519` | `STATEMENT exposed witness provenance correction: claimed=40,39,0 observed=39,39,0 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=b3e18633ac1448cb40339e85e022da1ac616f3b6 C1_R31_PASS=false` | Inconclusive: pristine aggregate failed; target edit detected |

### Exact commands and observed exits

All commands ran with cwd `/fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c`. The recorder `run-counter.py` invokes each following command unchanged, strips inherited `GIT_*` environment variables, saves stdout/stderr and records the resolved commit, exit, elapsed time and working-tree hashes in `counter-<label>.json`. Only pristine and mutation 1 overlapped; no more than two full counter runs were active. Subsequent mutation runs were serialized around the shared clone reset/commit dependency.

Setup (exit 0):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c checkout -q --detach 2da841bd9913a2037d2bf612793382e572c9d205
```

Exact detector invocations, each with a fresh work directory (all exit 1; stderr empty):

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c --rev 2da841bd9913a2037d2bf612793382e572c9d205 --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/w-pristine
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/w-1
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/w-2
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/w-3
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/w-4
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/w-5
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/w-6
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsA/w-restored
```

Each mutation was committed using this exact path-limited command, with the following observed subjects. Commit revisions are the `rev=` values in the result table.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c user.name=MutateC1RowsA -c user.email=MutateC1RowsA@shokunin.local -c core.hooksPath=/dev/null commit -qm '<subject>' -- SCORECARD.md
```

- `probe: change sources-registry last-row count 94 to 95`
- `probe: change mutation sweep last-row numerator 106 to 107`
- `probe: change regression ledger last-row cases 9 to 10`
- `probe: change repeated control last-row cases 29 to 30`
- `probe: change content disposition last-row numerator 19 to 20`
- `probe: change witness metadata last-row numerator 39 to 40`

The frozen counter internally supplies `--workdir <work>/regression-wd` for its regression command (line 44). The L1 explicitly confirmed this unchanged, seat-contained spelling satisfies the wave workdir bound; the counter was not patched.

### Before, mutant and restored hashes

Pristine and every post-reset `SCORECARD.md` SHA-256: `dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4`. Each mutant hash below was observed before and after its detector invocation and independently on its retained measured clone with `sha256sum`:

| k | Mutated SCORECARD.md SHA-256 | After restoring SCORECARD.md SHA-256 |
|---|---|---|
| 1 | `26ad196f25b7542418dc7831fddffea9e32e24c6a2dd059948ff70b4be223d7e` | `dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4` |
| 2 | `4d199e6b8007ab3b95ce614818eb4434289c2f63058dcb13e87562b725c18cdd` | `dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4` |
| 3 | `13487ebd5bc5cc15537a5f41160880e364f5066852fe67470b66c961c8871d84` | `dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4` |
| 4 | `51a19db96f6e076ef4573a7be47d575443ec2c9aa876a5763a19a83e90c0ff98` | `dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4` |
| 5 | `5669b6177cdd5cc683135302992328947024902d134b98599e63ffd623dbc8bc` | `dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4` |
| 6 | `62449addf45a4bf9fb97e9703fdb0835873b4589d669c51e99876fd96e4c7aa4` | `dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4` |

The retained measured source hashes came from `sha256sum` over `w-pristine/clone/SCORECARD.md` and all six `w-k/clone/SCORECARD.md` paths. The pristine recorder’s working-tree after-hash is mutation 1’s hash because that control overlapped mutation 1. That field describes the shared sandbox working tree, not the control input: its resolved revision and its retained `w-pristine/clone/SCORECARD.md` both identify pristine bytes, whose SHA-256 is the pristine hash above.

Frozen counter SHA-256 before and after: `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584`, observed both on the sandbox copy and on the exact production counter path used by the commands.

### Restoration evidence

`restorations.stdout:1-5` records the reset command and the same observed output after each of the six mutations (each reset/hash command exited 0):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git reset --hard 2da841bd9913a2037d2bf612793382e572c9d205 && sha256sum SCORECARD.md
```

```text
HEAD is now at 2da841b round-31: content revision — SCORECARD standing rows re-stated (C1 data), S095-S096 + S055 re-open, knowledge entry, README row, QUALITY 66-71, SKILL recipe workdir rule
dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4  SCORECARD.md
```

After the final exact reset, the same full detector was run once on the shared restored revision/bytes. This restored run is common evidence for the six identical post-reset states, not a separate full detector run after every intermediate reset. `counter-restored.stdout:1-6,12-13` (exit 1):

```text
STATEMENT sources-registry: claimed=0,94 observed=0,94 (exit=0) MATCH
STATEMENT mutation sweep runner: claimed=106,106,0 observed=106,106,0 (exit=0) MATCH
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=PASS,9,9,0 (exit=0) MATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=19,19,0 observed=19,19,0 (exit=0) MATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=6 (exit=0) MISMATCH
C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=2da841bd9913a2037d2bf612793382e572c9d205 C1_R31_PASS=false
```

`counter-restored.json` records revision `2da841bd9913a2037d2bf612793382e572c9d205` and equal before/after working-tree hashes `dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4`. Thus the mutations are removed even though the independent calibration mismatch remains. The process-cwd scan after all eight runs found no remaining detector process under this seat (`process-cleanup.json`); no process kill was needed. No tools were installed or updated.

## Smallest safe correction

Restore only each changed numeral by resetting the sandbox to the pinned content revision: completed for all six probes. No frozen-counter or contract correction is indicated by these target-line results. The already-red calibration statement is reported to the L1, not repaired or reclassified by this mutation seat.
