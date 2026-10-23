# CtlWrongHeader: pre-data control for C1

## Verdict

**Finding: shape C survived.** Correct axis rows under `| Axis | Score |` produced `C1_R31_PASS=true`, exit 0. Shapes A (`Capabilities`), B (`capability`), and D (`Axis` / `Verdict`) were rejected. All four wrong-header controls were expected to print `C1_R31_PASS=false`.

The axis parser is looser than the frozen table description `| Axis | Score (0–10) |`: it accepts any second header cell starting with `Score`, without requiring the first cell to be `Axis` or the range suffix. The tested false acceptance is the missing range suffix, not an untested header variant. The frozen JSON uses an ASCII hyphen in `(0-10)`; the counter docstring and the task use an en dash. Shape C omits the entire suffix, so that typographic distinction does not explain its acceptance.

Axes considered: calibration of the detector against the named table types; unchanged frozen inputs; isolated, byte-exact restoration. This report makes no judgment on the full round or its final content.

## Evidence and method

- Frozen contract: `.ufo/evidence/round-31/contract.json:12-17` identifies the two table types and the last-row predicate; lines 26 and 35 freeze the counter and name the wrong-header control.
- Frozen counter: `.ufo/evidence/round-31/c1-measure.py:10-15` names the table types; lines 114-119 require an exact `Capability` first cell for capability tables but only `header[1].startswith('Score')` for axis tables. Lines 120-122 let accepted rows replace the old axis rows.
- Values came from the twelve `observed=` fields in `.ufo/evidence/round-31/before/c1-at-base.stdout:1-12`; no value was invented for a control.
- Each arm is exactly one sandbox commit whose sole parent is `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. Each changes only `SCORECARD.md`, by appending the same rows. The behavior-bearing difference from the passing pristine fixture is one header line: line 1484 for A/B, line 1497 for C/D. The other table family retains its exact frozen header, so rejection in one family cannot mask acceptance in the other.
- All code runs and all work directories were confined to `/fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/`. Production sources and sibling workspaces were not modified. No subagent or other model runtime was invoked. No tools were installed or updated.

The untouched freeze failed with seven mismatches. That red baseline is **not** counted as a killed mutant. A separate pristine fixture with correct rows under exact headers passed before the header mutations. The restoration run uses exactly that fixture again.

| Shape | Changed header | Mismatches | C1_R31_PASS | Detector exit | Mutation verdict |
|---|---|---:|---|---:|---|
| A | `Capabilities` | 5 | false | 1 | killed |
| B | `capability` | 5 | false | 1 | killed |
| C | `Axis` / `Score` | 0 | true | 0 | survived |
| D | `Axis` / `Verdict` | 2 | false | 1 | killed |

For A/B the five stale capability rows remain authoritative; the correctly headed appended axis table matches. For C, both appended table families become authoritative and all twelve statements match. For D, the appended axis table is ignored and the two old axis values remain mismatches. The expected wrong-header behavior is met only by A, B, and D.

### Setup and commit commands

The setup clone and checkout both exited 0 with empty output:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

`df -h /fast` before cloning reported 178G available (78% used). Each header arm was prepared by detaching at `ctl-base`, restoring the passing fixture's `SCORECARD.md`, and applying the single stated header substitution. The exact commit command for each arm was the following, with NAME replaced by `header-A`, `header-B`, `header-C`, or `header-D`; all four exited 0 with empty output:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam NAME
```

The control runner invoked the unchanged production-path frozen counter with the exact commands below. Each work directory was fresh. Raw stdout, stderr, metadata, and full commit diffs are retained under the scratch seat as `LABEL.stdout`, `LABEL.stderr`, `LABEL.json`, and `header-X.diff`. All detector stderr files were empty. `DETECTOR_EXIT` printed by the recorder is not part of counter stdout and is instead reported separately below.
### pristine-base

Exact detector command:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/w-pristine-base
```

Resolved revision: `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. Detector exit: **1**. Full counter stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/pristine-base.stdout:1-13`):

```text
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

### pristine-correct

Exact detector command:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane --rev ef0a526496e095266d7d6f3b18d838095a3e617e --work /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/w-pristine-correct
```

Resolved revision: `ef0a526496e095266d7d6f3b18d838095a3e617e`. Detector exit: **0**. Full counter stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/pristine-correct.stdout:1-13`):

```text
STATEMENT sources-registry: claimed=0,92 observed=0,92 (exit=0) MATCH
STATEMENT mutation sweep runner: claimed=106,106,0 observed=106,106,0 (exit=0) MATCH
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=PASS,9,9,0 (exit=0) MATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=19,19,0 observed=19,19,0 (exit=0) MATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT effective expectation reconciliation: claimed=66,66,0 observed=66,66,0 (exit=0) MATCH
STATEMENT retained invocation-context gate: claimed=0,49,49 observed=0,49,49 (exit=0) MATCH
STATEMENT hermetic env-differential probe: claimed=9,9 observed=9,9 (exit=0) MATCH
STATEMENT callback-authoritative wave accounting: claimed=8,8 observed=8,8 (exit=0) MATCH
STATEMENT depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=8 (exit=0) MATCH
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=ef0a526496e095266d7d6f3b18d838095a3e617e C1_R31_PASS=true
```

### header-A

Exact detector command:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/w-header-A
```

Resolved revision: `d83221df11fc3b3ce6a46cdd32a9d814f4cd0468`. Detector exit: **1**. Full counter stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/header-A.stdout:1-13`):

```text
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
STATEMENT depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=8 (exit=0) MATCH
C1_R31: statements=12 mismatches=5 unparsed=0 unobservable=0 append_only=1 rev=d83221df11fc3b3ce6a46cdd32a9d814f4cd0468 C1_R31_PASS=false
```

Parent: `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. After the behavioral runs, this commit was selected as detached HEAD to collect the exact requested parent-to-HEAD diff. The command below exited 0. It prints only 28 lines, so the full verbatim output below is also the requested first 80 lines; no truncation was needed. It was byte-identical to the earlier pinned-ref diff.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane diff HEAD~1 HEAD -- SCORECARD.md
```

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..465ecba 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,23 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+## Header classification control
+
+| Capabilities | What it can now do | Evidence pointer | First-working round |
+|---|---|---|---|
+| sources-registry | re-stated observed values | exit 0, 92 rows | control |
+| mutation sweep runner | re-stated observed values | `MUTATE_SELFTEST: 106/106 pass`, exit 0 | control |
+| six-leg regression ledger | re-stated observed values | `REGRESSION: PASS (cases=9 passed=9)`, exit 0 | control |
+| repeated pristine-control gate | re-stated observed values | PASS (29 cases), exit 0 | control |
+| six-leg content-disposition probe | re-stated observed values | `--selftest` → 19/19 PASS0 | control |
+| exposed witness provenance correction | re-stated observed values | metadata selftest39/39 PASS0 | control |
+| effective expectation reconciliation | re-stated observed values | PASS66/66 exit0 | control |
+| retained invocation-context gate | re-stated observed values | → exit0, copied-source CLI selftest49/49 | control |
+| hermetic env-differential probe | re-stated observed values | actual9/9 | control |
+| callback-authoritative wave accounting | re-stated observed values | frozen counter8/8 | control |
+
+| Axis | Score (0–10) | Evidence / counting rule |
+|---|---|---|
+| depth | 9 | re-stated observed value |
+| calibration | 8 | re-stated observed value |
```

### header-B

Exact detector command:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/w-header-B
```

Resolved revision: `42f252ae3d7ae1d43c94e22a5cebccb451b088a5`. Detector exit: **1**. Full counter stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/header-B.stdout:1-13`):

```text
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
STATEMENT depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=8 (exit=0) MATCH
C1_R31: statements=12 mismatches=5 unparsed=0 unobservable=0 append_only=1 rev=42f252ae3d7ae1d43c94e22a5cebccb451b088a5 C1_R31_PASS=false
```

Parent: `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. After the behavioral runs, this commit was selected as detached HEAD to collect the exact requested parent-to-HEAD diff. The command below exited 0. It prints only 28 lines, so the full verbatim output below is also the requested first 80 lines; no truncation was needed. It was byte-identical to the earlier pinned-ref diff.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane diff HEAD~1 HEAD -- SCORECARD.md
```

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..305ac48 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,23 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+## Header classification control
+
+| capability | What it can now do | Evidence pointer | First-working round |
+|---|---|---|---|
+| sources-registry | re-stated observed values | exit 0, 92 rows | control |
+| mutation sweep runner | re-stated observed values | `MUTATE_SELFTEST: 106/106 pass`, exit 0 | control |
+| six-leg regression ledger | re-stated observed values | `REGRESSION: PASS (cases=9 passed=9)`, exit 0 | control |
+| repeated pristine-control gate | re-stated observed values | PASS (29 cases), exit 0 | control |
+| six-leg content-disposition probe | re-stated observed values | `--selftest` → 19/19 PASS0 | control |
+| exposed witness provenance correction | re-stated observed values | metadata selftest39/39 PASS0 | control |
+| effective expectation reconciliation | re-stated observed values | PASS66/66 exit0 | control |
+| retained invocation-context gate | re-stated observed values | → exit0, copied-source CLI selftest49/49 | control |
+| hermetic env-differential probe | re-stated observed values | actual9/9 | control |
+| callback-authoritative wave accounting | re-stated observed values | frozen counter8/8 | control |
+
+| Axis | Score (0–10) | Evidence / counting rule |
+|---|---|---|
+| depth | 9 | re-stated observed value |
+| calibration | 8 | re-stated observed value |
```

### header-C

Exact detector command:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/w-header-C
```

Resolved revision: `93f4c3eff7e119f60ebd1ac4381c2208653e507a`. Detector exit: **0**. Full counter stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/header-C.stdout:1-13`):

```text
STATEMENT sources-registry: claimed=0,92 observed=0,92 (exit=0) MATCH
STATEMENT mutation sweep runner: claimed=106,106,0 observed=106,106,0 (exit=0) MATCH
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=PASS,9,9,0 (exit=0) MATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=19,19,0 observed=19,19,0 (exit=0) MATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT effective expectation reconciliation: claimed=66,66,0 observed=66,66,0 (exit=0) MATCH
STATEMENT retained invocation-context gate: claimed=0,49,49 observed=0,49,49 (exit=0) MATCH
STATEMENT hermetic env-differential probe: claimed=9,9 observed=9,9 (exit=0) MATCH
STATEMENT callback-authoritative wave accounting: claimed=8,8 observed=8,8 (exit=0) MATCH
STATEMENT depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=8 (exit=0) MATCH
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=93f4c3eff7e119f60ebd1ac4381c2208653e507a C1_R31_PASS=true
```

Parent: `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. After the behavioral runs, this commit was selected as detached HEAD to collect the exact requested parent-to-HEAD diff. The command below exited 0. It prints only 28 lines, so the full verbatim output below is also the requested first 80 lines; no truncation was needed. It was byte-identical to the earlier pinned-ref diff.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane diff HEAD~1 HEAD -- SCORECARD.md
```

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..90458c1 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,23 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+## Header classification control
+
+| Capability | What it can now do | Evidence pointer | First-working round |
+|---|---|---|---|
+| sources-registry | re-stated observed values | exit 0, 92 rows | control |
+| mutation sweep runner | re-stated observed values | `MUTATE_SELFTEST: 106/106 pass`, exit 0 | control |
+| six-leg regression ledger | re-stated observed values | `REGRESSION: PASS (cases=9 passed=9)`, exit 0 | control |
+| repeated pristine-control gate | re-stated observed values | PASS (29 cases), exit 0 | control |
+| six-leg content-disposition probe | re-stated observed values | `--selftest` → 19/19 PASS0 | control |
+| exposed witness provenance correction | re-stated observed values | metadata selftest39/39 PASS0 | control |
+| effective expectation reconciliation | re-stated observed values | PASS66/66 exit0 | control |
+| retained invocation-context gate | re-stated observed values | → exit0, copied-source CLI selftest49/49 | control |
+| hermetic env-differential probe | re-stated observed values | actual9/9 | control |
+| callback-authoritative wave accounting | re-stated observed values | frozen counter8/8 | control |
+
+| Axis | Score | Evidence / counting rule |
+|---|---|---|
+| depth | 9 | re-stated observed value |
+| calibration | 8 | re-stated observed value |
```

### header-D

Exact detector command:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/w-header-D
```

Resolved revision: `a611b1e9e48b00d940e0c8cac91b149433b1ac54`. Detector exit: **1**. Full counter stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/header-D.stdout:1-13`):

```text
STATEMENT sources-registry: claimed=0,92 observed=0,92 (exit=0) MATCH
STATEMENT mutation sweep runner: claimed=106,106,0 observed=106,106,0 (exit=0) MATCH
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=PASS,9,9,0 (exit=0) MATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=19,19,0 observed=19,19,0 (exit=0) MATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT effective expectation reconciliation: claimed=66,66,0 observed=66,66,0 (exit=0) MATCH
STATEMENT retained invocation-context gate: claimed=0,49,49 observed=0,49,49 (exit=0) MATCH
STATEMENT hermetic env-differential probe: claimed=9,9 observed=9,9 (exit=0) MATCH
STATEMENT callback-authoritative wave accounting: claimed=8,8 observed=8,8 (exit=0) MATCH
STATEMENT depth: claimed=6 observed=9 (exit=0) MISMATCH
STATEMENT calibration: claimed=0 observed=8 (exit=0) MISMATCH
C1_R31: statements=12 mismatches=2 unparsed=0 unobservable=0 append_only=1 rev=a611b1e9e48b00d940e0c8cac91b149433b1ac54 C1_R31_PASS=false
```

Parent: `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. After the behavioral runs, this commit was selected as detached HEAD to collect the exact requested parent-to-HEAD diff. The command below exited 0. It prints only 28 lines, so the full verbatim output below is also the requested first 80 lines; no truncation was needed. It was byte-identical to the earlier pinned-ref diff.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane diff HEAD~1 HEAD -- SCORECARD.md
```

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..e03e3fd 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,23 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+## Header classification control
+
+| Capability | What it can now do | Evidence pointer | First-working round |
+|---|---|---|---|
+| sources-registry | re-stated observed values | exit 0, 92 rows | control |
+| mutation sweep runner | re-stated observed values | `MUTATE_SELFTEST: 106/106 pass`, exit 0 | control |
+| six-leg regression ledger | re-stated observed values | `REGRESSION: PASS (cases=9 passed=9)`, exit 0 | control |
+| repeated pristine-control gate | re-stated observed values | PASS (29 cases), exit 0 | control |
+| six-leg content-disposition probe | re-stated observed values | `--selftest` → 19/19 PASS0 | control |
+| exposed witness provenance correction | re-stated observed values | metadata selftest39/39 PASS0 | control |
+| effective expectation reconciliation | re-stated observed values | PASS66/66 exit0 | control |
+| retained invocation-context gate | re-stated observed values | → exit0, copied-source CLI selftest49/49 | control |
+| hermetic env-differential probe | re-stated observed values | actual9/9 | control |
+| callback-authoritative wave accounting | re-stated observed values | frozen counter8/8 | control |
+
+| Axis | Verdict | Evidence / counting rule |
+|---|---|---|
+| depth | 9 | re-stated observed value |
+| calibration | 8 | re-stated observed value |
```

### restored

Exact detector command:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/w-restored
```

Resolved revision: `ef0a526496e095266d7d6f3b18d838095a3e617e`. Detector exit: **0**. Full counter stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/restored.stdout:1-13`):

```text
STATEMENT sources-registry: claimed=0,92 observed=0,92 (exit=0) MATCH
STATEMENT mutation sweep runner: claimed=106,106,0 observed=106,106,0 (exit=0) MATCH
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=PASS,9,9,0 (exit=0) MATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=19,19,0 observed=19,19,0 (exit=0) MATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT effective expectation reconciliation: claimed=66,66,0 observed=66,66,0 (exit=0) MATCH
STATEMENT retained invocation-context gate: claimed=0,49,49 observed=0,49,49 (exit=0) MATCH
STATEMENT hermetic env-differential probe: claimed=9,9 observed=9,9 (exit=0) MATCH
STATEMENT callback-authoritative wave accounting: claimed=8,8 observed=8,8 (exit=0) MATCH
STATEMENT depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=8 (exit=0) MATCH
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=ef0a526496e095266d7d6f3b18d838095a3e617e C1_R31_PASS=true
```

## Hashes and restoration evidence

The detector was run on the passing pristine fixture, each one-line header mutant, and the byte-restored passing fixture. The restored fixture returned the same twelve MATCH results and exit 0 as pristine. Both use revision `ef0a526496e095266d7d6f3b18d838095a3e617e` and identical `SCORECARD.md` bytes.

| State | SCORECARD.md SHA-256 |
|---|---|
| pristine-base | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` |
| pristine-correct | `3b368f50bc4b87fb9526eed090ee50f2bc54abbe7297d64fe404a29fcaa9a978` |
| header-A | `b138b6c42814cf9b731e9030e73ebb184272238ff0d04638f634fb5b3db23776` |
| header-B | `e8d0717b8b8b5d8b76e4c11feef4d351f529d8032f7f7aca2122a145241ef962` |
| header-C | `58ad7944e1fcd0c65c8a76a59c3fb398bc3e774a7b7868440772455ff56cc735` |
| header-D | `2cf1ad3025cdcfba0b6d4e95a9e2354d44cbb7031c1f8a9730d37472f9f720a2` |
| restored | `3b368f50bc4b87fb9526eed090ee50f2bc54abbe7297d64fe404a29fcaa9a978` |
| Final original-freeze restoration | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` |

Restoration commands observed, both exit 0 with empty checkout output:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane checkout -q --detach ctl-pristine-correct
# Run the restored detector above before any later checkout.
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlWrongHeader/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

The final checkout returns the sandbox to the exact bytes present immediately after initial setup; that last original-freeze restoration is hash evidence, not a claimed additional detector run. Control commits remain available as `ctl-header-A` through `ctl-header-D`; the original passing fixture remains `ctl-pristine-correct`.

For every detector invocation the external frozen counter and contract hashes were identical before and after. Their final hashes also match the initial ones:

- `c1-measure.py`: `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584`.
- `contract.json`: `8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79`.

`restoration-evidence.json` retains all final hashes and exact-diff exit codes. All seven detector commands completed. A final `/proc` check for remaining detector processes whose working directory was in this seat returned `[]` (`remaining-processes.json`); no process needed to be killed.

## Smallest safe correction

Do not change this round's frozen counter, predicate, or target. Preserve shape C as a coverage finding: the frozen counter can be met by correct axis values outside the expressly named axis header. Real re-stated rows should use the exact named table headers rather than rely on the loose match. In an unfrozen successor, bind both axis header cells to `Axis` and the explicit range-bearing `Score (0–10)` label, with these four cases retained as regression fixtures. No correction was applied to production sources.
