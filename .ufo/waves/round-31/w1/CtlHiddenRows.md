# CtlHiddenRows — pre-data hidden-row controls

## Verdict

**All three assigned controls were rejected as expected.** HTML comment (A), triple-backtick fence (B), and four-space indentation (C) each produced `C1_R31_PASS=false`, seven mismatches, and exit 1. No counter bypass was observed for these shapes.

**Mutation-kill verdict: inconclusive, not killed.** The pristine revision already fails C1 with the same seven mismatches; the restored revision does too. These are successful negative-control observations, not a green-to-red mutation kill.

Claim axis: **calibration**. Probe dimensions: hidden-row exclusion, frozen-counter identity, and exact restoration. No other claim is assessed here.

## Evidence and scope

- Frozen contract: `.ufo/evidence/round-31/contract.json:14-26`; hidden-row control at `:33`.
- Frozen detector: `.ufo/evidence/round-31/c1-measure.py:78-88` removes HTML comments and fenced blocks; `:91-104` accepts table runs only when lines start with `|`; `:111-123` selects the last eligible rows. Thus four-space-indented rows are not eligible tables. Final comparison is at `:201-224`.
- Correct payload values were copied from the `observed=` fields in `.ufo/evidence/round-31/before/c1-at-base.stdout:1-13`, including the unchanged 92-row census. The controls did not alter any tool or counter.
- Existing standing claims remain at frozen `SCORECARD.md:64-67,238-249`. A and B append their payload at `SCORECARD.md:1482-1500`; C appends at `:1482-1498`, in the respective commits below.
- All shell commands ran with working directory `/fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane` or its seat root. No sibling scratch directory was opened. The only production write is this assigned report.

| State | Commit | Parent | SCORECARD SHA-256 |
|---|---|---|---|
| Pristine / restored | `c111dab58b0a8d55e991bbd2efe3aad56717b95a` | frozen revision | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` |
| A: HTML comment | `165ea6773363917f8359b36df1356117456b4e4d` | `c111dab58b0a8d55e991bbd2efe3aad56717b95a` | `844ba7236e9b9248a74cc154cf553d5e30f5e5262653f8d8f6ec2f11a9a87601` |
| B: fenced block | `235075548dde62493ee3ee4c674f8e4a6e651d0c` | `c111dab58b0a8d55e991bbd2efe3aad56717b95a` | `46bedf91b2d922f9ad17ce923a2f86a3b0a3834272a9181e4477d7f8ea6ddeec` |
| C: four spaces | `bac2e70cdd1edd54c64549096772ec717e8a8c01` | `c111dab58b0a8d55e991bbd2efe3aad56717b95a` | `5c180f133aa8d76b33593914de0e47a6ed5881a53b48406bab28f9c34b47153c` |

Each shape is one sandbox commit directly on the freeze, not cumulative with another shape. A and B append 20 lines; C appends 18. Before each subsequent shape, the sandbox was checked out at the frozen revision and the pristine hash was observed again.

Setup executed:

```sh
df -h /fast
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

Observed disk result before cloning: `/fast` had 177G available (79% used). Clone and checkout exited 0. No tools were installed or upgraded. An initial asynchronous pristine launch was refused by the shared background-job cap before execution; its ordinary retry is the pristine run recorded below.

## Pristine detector run

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/w-pristine
```

Full stdout, verbatim; exit **1**:

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

## A — correct tables inside an HTML comment

Mutant: append all 12 correct statements inside `<!-- ... -->`. Expected detector: ignore the appended rows, retain the old visible claims, and reject C1.

Commands executed after appending the payload:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam hidden-A
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/w-hidden-A
```

Full counter stdout, verbatim; exit **1**:

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
C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=165ea6773363917f8359b36df1356117456b4e4d C1_R31_PASS=false
```

Diff command executed while this commit was HEAD:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane diff HEAD~1 HEAD -- SCORECARD.md
```

The complete diff is under 80 lines, so it is also the requested first-80-line content, without truncation:

````diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..b2d4bed 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,23 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+<!--
+| Capability | What it can now do | Evidence pointer | First-working round |
+|---|---|---|---|
+| sources-registry | Hidden correct restatement | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 92 rows | control |
+| mutation sweep runner | Hidden correct restatement | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0 | control |
+| six-leg regression ledger | Hidden correct restatement | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9)`, exit 0 | control |
+| repeated pristine-control gate | Hidden correct restatement | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0 | control |
+| six-leg content-disposition probe | Hidden correct restatement | `python3 tools/pin-disposition.py --selftest` → 19/19 PASS0 | control |
+| exposed witness provenance correction | Hidden correct restatement | metadata selftest39/39 PASS0 | control |
+| effective expectation reconciliation | Hidden correct restatement | `python3 tools/evidence-disposition.py --selftest` → PASS66/66 exit0 | control |
+| retained invocation-context gate | Hidden correct restatement | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49 | control |
+| hermetic env-differential probe | Hidden correct restatement | `python3 tools/env-diff.py --selftest` actual9/9 | control |
+| callback-authoritative wave accounting | Hidden correct restatement | `python3 tools/wave-accounting.py --selftest` frozen counter8/8 | control |
+
+| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
+|---|---|---|---|---|
+| depth | 9 | Correct observed value copied from frozen base receipt | control | control |
+| calibration | 8 | Correct observed value copied from frozen base receipt | control | control |
+-->
````

## B — correct tables inside a fenced block

Mutant: the same correct payload inside a triple-backtick fenced block. Expected detector: ignore the appended rows and reject C1.

Commands executed after restoring the freeze and appending the payload:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam hidden-B
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/w-hidden-B
```

Full counter stdout, verbatim; exit **1**:

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
C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=235075548dde62493ee3ee4c674f8e4a6e651d0c C1_R31_PASS=false
```

The same diff command was executed while B was HEAD. Full output, under 80 lines:

````diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..6a387c6 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,23 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+```
+| Capability | What it can now do | Evidence pointer | First-working round |
+|---|---|---|---|
+| sources-registry | Hidden correct restatement | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 92 rows | control |
+| mutation sweep runner | Hidden correct restatement | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0 | control |
+| six-leg regression ledger | Hidden correct restatement | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9)`, exit 0 | control |
+| repeated pristine-control gate | Hidden correct restatement | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0 | control |
+| six-leg content-disposition probe | Hidden correct restatement | `python3 tools/pin-disposition.py --selftest` → 19/19 PASS0 | control |
+| exposed witness provenance correction | Hidden correct restatement | metadata selftest39/39 PASS0 | control |
+| effective expectation reconciliation | Hidden correct restatement | `python3 tools/evidence-disposition.py --selftest` → PASS66/66 exit0 | control |
+| retained invocation-context gate | Hidden correct restatement | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49 | control |
+| hermetic env-differential probe | Hidden correct restatement | `python3 tools/env-diff.py --selftest` actual9/9 | control |
+| callback-authoritative wave accounting | Hidden correct restatement | `python3 tools/wave-accounting.py --selftest` frozen counter8/8 | control |
+
+| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
+|---|---|---|---|---|
+| depth | 9 | Correct observed value copied from frozen base receipt | control | control |
+| calibration | 8 | Correct observed value copied from frozen base receipt | control | control |
+```
````

## C — correct tables indented by four spaces

Mutant: the same correct tables, each row indented by exactly four spaces. These are code text rather than standing Markdown tables. Expected detector: exclude them because they do not start at column one, and reject C1.

Commands executed after restoring the freeze and appending the payload:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam hidden-C
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/w-hidden-C
```

Full counter stdout, verbatim; exit **1**:

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
C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=bac2e70cdd1edd54c64549096772ec717e8a8c01 C1_R31_PASS=false
```

The same diff command was executed while C was HEAD. Full output, under 80 lines:

````diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..5fec948 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,21 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+    | Capability | What it can now do | Evidence pointer | First-working round |
+    |---|---|---|---|
+    | sources-registry | Hidden correct restatement | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 92 rows | control |
+    | mutation sweep runner | Hidden correct restatement | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0 | control |
+    | six-leg regression ledger | Hidden correct restatement | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9)`, exit 0 | control |
+    | repeated pristine-control gate | Hidden correct restatement | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0 | control |
+    | six-leg content-disposition probe | Hidden correct restatement | `python3 tools/pin-disposition.py --selftest` → 19/19 PASS0 | control |
+    | exposed witness provenance correction | Hidden correct restatement | metadata selftest39/39 PASS0 | control |
+    | effective expectation reconciliation | Hidden correct restatement | `python3 tools/evidence-disposition.py --selftest` → PASS66/66 exit0 | control |
+    | retained invocation-context gate | Hidden correct restatement | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49 | control |
+    | hermetic env-differential probe | Hidden correct restatement | `python3 tools/env-diff.py --selftest` actual9/9 | control |
+    | callback-authoritative wave accounting | Hidden correct restatement | `python3 tools/wave-accounting.py --selftest` frozen counter8/8 | control |
+
+    | Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
+    |---|---|---|---|---|
+    | depth | 9 | Correct observed value copied from frozen base receipt | control | control |
+    | calibration | 8 | Correct observed value copied from frozen base receipt | control | control |
````

## Restoration evidence

Final restoration command and byte comparison:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a && sha256sum SCORECARD.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/contract.json && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane show c111dab58b0a8d55e991bbd2efe3aad56717b95a:SCORECARD.md | cmp -s SCORECARD.md - && printf 'RESTORE_CMP: equal\n'
```

Observed output; exit **0**:

```text
518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0  SCORECARD.md
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py
8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/contract.json
RESTORE_CMP: equal
```

The detector and contract hashes above equal their pre-probe hashes. The detector hash also equals the frozen hash in `contract.json:17`. SCORECARD bytes compare equal to the frozen Git blob, not merely to a normalized rendering.

Same bounded detector on the restored revision, with another fresh work directory:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/lane --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/w-restored
```

Full stdout, verbatim; exit **1**:

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

All five detector invocations completed. A final `/proc` cwd scan found no processes in this seat's detector work directories: `Remaining detector work-directory processes: []`. No process was killed. No subagents or other model runtime were invoked.

Scratch evidence is retained under `/fast/scratch/hyaku/tameshi-r31-seats/CtlHiddenRows/`: `pristine.stdout`, `hidden-A.stdout`, `hidden-B.stdout`, `hidden-C.stdout`, `restored.stdout`, the three `hidden-*.diff` files, and the detector-created `w-*` directories with per-command stdout.

## Smallest safe correction

No frozen-counter correction is indicated by these three controls, and none was made. Correct self-assessment values must be appended as actual standing tables outside comments and code blocks, starting at column one, then measured with the unchanged frozen counter. Hidden copies cannot repair the visible claims. The predicate, statement set, and target remain unchanged.
