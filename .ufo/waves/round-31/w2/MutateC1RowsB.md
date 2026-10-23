Verdict: five informative **row-level kills**; the calibration mutation is **inconclusive**, not a killed mutant or a demonstrated survivor. The pristine overall C1 detector already fails, so no overall exit-code kill is claimed.

# MutateC1RowsB — appended-row sensitivity

- Seat: `MutateC1RowsB`.
- Axes: calibration (agreement and detector sensitivity), isolation (sandbox-only changes), restoration (exact original bytes).
- Target and parent of every independent sandbox commit: `2da841bd9913a2037d2bf612793382e572c9d205`.
- Scratch root: `/fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/`; all commands below ran in its `c/` clone. No production content was edited.
- Frozen counter: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py`. Its SHA-256 is `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584`, matching `contract.json:17` and the final executed-file hash.

## Evidence and expected detector

The frozen counter selects the last row of each table type (`c1-measure.py:111-133`), compares its parsed values to command output, and emits the statement and overall result (`c1-measure.py:203-224`). The six mutation sites are `c/SCORECARD.md:1520-1523,1536-1537` under the scratch root. Each edit changes just one stated numerator or scalar in that statement's last row; earlier rows, duplicate evidence text and executable commands stay unchanged.

For the first five statements, the expected bounded detector is the named `STATEMENT` line changing `MATCH → MISMATCH → MATCH` on pristine, mutant and restored bytes. The expected overall mismatch count is `1 → 2 → 1`, because calibration already contributes one mismatch. Using only nonzero C1 exits would be invalid attribution.

Pristine output, retained verbatim at `/fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/w-pristine.stdout:7-13`:

```text
STATEMENT effective expectation reconciliation: claimed=66,66,0 observed=66,66,0 (exit=0) MATCH
STATEMENT retained invocation-context gate: claimed=0,49,49 observed=0,49,49 (exit=0) MATCH
STATEMENT hermetic env-differential probe: claimed=9,9 observed=9,9 (exit=0) MATCH
STATEMENT callback-authoritative wave accounting: claimed=8,8 observed=8,8 (exit=0) MATCH
STATEMENT depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=6 (exit=0) MISMATCH
C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=2da841bd9913a2037d2bf612793382e572c9d205 C1_R31_PASS=false
```

### Mutant results

Full stdout transcripts are `w-1.stdout` through `w-6.stdout` under the scratch root. Their relevant statement lines are respectively lines 7, 8, 9, 10, 11 and 12; the C1 line is line 13 in every transcript. All thirteen measurement invocations exited **1**, not timeout or setup error.

| Statement / last-row location | Mutated value | Exact STATEMENT line | Exact C1_R31 line | Killed or survived |
|---|---|---|---|---|
| effective expectation reconciliation / `SCORECARD.md:1520` | `PASS66/66` → `PASS65/66` | `STATEMENT effective expectation reconciliation: claimed=65,66,0 observed=66,66,0 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=427568d989d11a0ce5aa3ac150ea910ee7663834 C1_R31_PASS=false` | Killed by the row detector; overall exit alone inconclusive |
| retained invocation-context gate / `SCORECARD.md:1521` | `selftest49/49` → `selftest48/49` | `STATEMENT retained invocation-context gate: claimed=0,48,49 observed=0,49,49 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=44cd843999842ead2906dbb7449dee15ec9d2557 C1_R31_PASS=false` | Killed by the row detector; overall exit alone inconclusive |
| hermetic env-differential probe / `SCORECARD.md:1522` | `actual9/9` → `actual8/9` | `STATEMENT hermetic env-differential probe: claimed=8,9 observed=9,9 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=1119d11381bb6b63c94fa391933515a519d8fc28 C1_R31_PASS=false` | Killed by the row detector; overall exit alone inconclusive |
| callback-authoritative wave accounting / `SCORECARD.md:1523` | `frozen counter8/8` → `frozen counter7/8` | `STATEMENT callback-authoritative wave accounting: claimed=7,8 observed=8,8 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=9448218d4e2d043b279f7dc36fae1240db27db84 C1_R31_PASS=false` | Killed by the row detector; overall exit alone inconclusive |
| depth / `SCORECARD.md:1536` | scalar `9` → `8` | `STATEMENT depth: claimed=8 observed=9 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=f1c0f5c58c9bbd5e8b2f8533be269e1d9b511e0c C1_R31_PASS=false` | Killed by the row detector; overall exit alone inconclusive |
| calibration / `SCORECARD.md:1537` | scalar `8` → `7` | `STATEMENT calibration: claimed=7 observed=6 (exit=0) MISMATCH` | `C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=e3c8591ee354313cd45a1045c4d4dca79504f877 C1_R31_PASS=false` | Inconclusive: pristine and restored rows already MISMATCH |

**Calibration's apparent kill is not informative.** At this content revision the monitor observes `6`, not the row's `8`. The mutation changes the parsed claim to `7` but leaves the verdict and total mismatch count unchanged. That confirms the new last-row value is read; it does not establish a passing-to-failing kill or a coverage blind spot.

### Exact commands

Clone and initial checkout:

```bash
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c checkout -q --detach 2da841bd9913a2037d2bf612793382e572c9d205
```

Each exact one-line edit was staged with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git add -- SCORECARD.md` and committed with the following command form, substituting the listed message literally:

```bash
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c user.name=MutateC1RowsB -c user.email=MutateC1RowsB@invalid -c core.hooksPath=/dev/null -c commit.gpgsign=false commit -q -m 'MESSAGE'
```

| k | MESSAGE |
|---|---|
| 1 | MutateC1RowsB: effective expectation last-row numerator 66 to 65 |
| 2 | MutateC1RowsB: invocation-context last-row numerator 49 to 48 |
| 3 | MutateC1RowsB: hermetic env last-row numerator 9 to 8 |
| 4 | MutateC1RowsB: wave accounting last-row numerator 8 to 7 |
| 5 | MutateC1RowsB: depth last-row scalar 9 to 8 |
| 6 | MutateC1RowsB: calibration last-row scalar 8 to 7 |

The detector invocations were exactly:

```bash
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/w-pristine
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/w-1
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/w-2
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/w-3
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/w-4
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/w-5
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/w-6
```

After each mutant, the exact sandbox restoration command was:

```bash
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git reset -q --hard 2da841bd9913a2037d2bf612793382e572c9d205
sha256sum SCORECARD.md .ufo/evidence/round-31/c1-measure.py
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD
```

For each literal `k` in `1, 2, 3, 4, 5, 6`, the same detector was then run with the only argument change being its fresh work directory:

```bash
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/c --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/MutateC1RowsB/w-restored-k
```

At most two detectors ran concurrently. Before resetting or making the next edit, the corresponding detector's already checked-out `work/clone/SCORECARD.md` was read to establish that it had captured the intended revision; the counter resolves `HEAD` once and subsequently uses that fixed commit (`c1-measure.py:181-204`). Every mutant output above confirms the intended committed row. Each restored run has a fresh work directory and the pristine revision in its result. The frozen counter's nested regression work directory is inside its seat-owned work directory. Per the parent clarification, runner-owned transient `/tmp` directories created and cleaned by frozen commands were allowed; no private `/tmp` bind was used for any measurement.

## Restoration evidence

Let `B` be the original and restored SHA-256 of `SCORECARD.md`:

```text
dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4
```

The original before every mutation and the after-reset hash after every mutation were exactly `B`.

| k | Sandbox commit | Mutant SCORECARD.md SHA-256 | Before / restored after |
|---|---|---|---|
| 1 | `427568d989d11a0ce5aa3ac150ea910ee7663834` | `ac636c26df60d1feaba0e5a9cb3d735b31f2bc2b512f58085f0706769f043bf0` | B / B |
| 2 | `44cd843999842ead2906dbb7449dee15ec9d2557` | `83edb4aa471258317f7ca6bad6adca1619ab8add74b301255777477dace5232b` | B / B |
| 3 | `1119d11381bb6b63c94fa391933515a519d8fc28` | `6923443d7c8240415652525b2a347137e740e571c5a288691c61c25b8aac77b5` | B / B |
| 4 | `9448218d4e2d043b279f7dc36fae1240db27db84` | `3b307c19d9097c922fd90a4c1180a3ceb78ec0ab2e1b2a33f0a26c82397699ce` | B / B |
| 5 | `f1c0f5c58c9bbd5e8b2f8533be269e1d9b511e0c` | `b430a78bc334f9176d4943f7e5c467e72eed52493ce746dfedf1635f5f4be4a1` | B / B |
| 6 | `e3c8591ee354313cd45a1045c4d4dca79504f877` | `88b5e4535f5e9e873ce8c1fda89fe10d5f7b03af3e827a8e6b646d27ac621507` | B / B |

Every restored stdout transcript, `w-restored-1.stdout` through `w-restored-6.stdout`, has the same thirteen lines as `w-pristine.stdout`: the five initially matching rows return to `MATCH`, calibration returns to `claimed=8 observed=6 ... MISMATCH`, and line 13 is:

```text
C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=2da841bd9913a2037d2bf612793382e572c9d205 C1_R31_PASS=false
```

After all detectors finished, the final command was:

```bash
sha256sum SCORECARD.md .ufo/evidence/round-31/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD
```

Observed output:

```text
dc8eec4d7f62e742f07ee69ee9bf040d45508ce42d4787596824aa18fc7ec3f4  SCORECARD.md
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  .ufo/evidence/round-31/c1-measure.py
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py
2da841bd9913a2037d2bf612793382e572c9d205
```

All thirteen measurement jobs completed. A final process inspection enumerated `ps -eo pid=,ppid=,comm=` and read each available `/proc/PID/cwd`, filtering to this seat's scratch root and excluding the inspecting process. It returned `{"remaining_processes": [], "seat": "MutateC1RowsB"}`; no process kill was needed. No tools were installed or updated.

## Smallest safe correction

Do not count the calibration result as a kill, and do not amend the frozen counter or contract. Complete the already planned cold-read ledger work and measure its resulting committed revision. A subsequent informative calibration mutation probe needs a pristine `MATCH` first. These probes indicate no counter correction; all sandbox changes were restored and no integration was performed.
