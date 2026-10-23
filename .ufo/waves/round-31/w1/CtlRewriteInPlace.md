Verdict: all three history-rewrite controls were rejected as expected; none printed `C1_R31_PASS=true`. The formal mutation-kill verdict is **INCONCLUSIVE**, not killed: the pristine frozen revision already fails C1. These runs establish the requested negative-control outcomes, not a green-to-red kill.

# CtlRewriteInPlace — pre-data C1 control

Axis under test: calibration. Probe dimensions: history preservation, last-row precedence, and exact restoration. No production content or frozen detector was edited.

| Shape | Sandbox commit | Mismatches | append_only | Counter result | Exit | Rejection reason |
|---|---|---:|---:|---|---:|---|
| A: correct existing rows in place | `a880d32b7213bafde88a3ef86fcbaa9306f2668b` | 0 | 0 | false | 1 | Append-only breach alone |
| B: correct tables before old tables | `2c1b9b6374aa864cae30c1e683833d9b8b458473` | 7 | 0 | false | 1 | Both last-row precedence and append-only breach |
| C: correct tables appended, unrelated old line deleted | `0ff3f0655b0a8a350a60a52fdb840978000578fe` | 0 | 0 | false | 1 | Append-only breach alone |

All three are separate, one-commit children of frozen revision `c111dab58b0a8d55e991bbd2efe3aad56717b95a`, not a three-commit stack. All twelve commands were observable in every completed run. Every run's stderr was empty.

## Evidence and frozen contract

Paths in this section are relative to `/home/vgpnk/Projects/shokunin/tameshi-shokunin`:

- `.ufo/evidence/round-31/contract.json:14-26`: exact predicate, target and kill rule.
- `.ufo/evidence/round-31/contract.json:34`: in-place rewriting is explicitly a pre-data control.
- `.ufo/evidence/round-31/before/c1-at-base.stdout:1-13`: the observed values used for all corrected rows.
- `.ufo/evidence/round-31/c1-measure.py:111-123`: later same-type rows replace earlier rows.
- `.ufo/evidence/round-31/c1-measure.py:196-202,221-224`: prefix requirement and conjunction with zero mismatches.

At shape A's commit, `SCORECARD.md:66-67,240-242,244,246` are the seven corrected historical rows. At shape B's commit, `SCORECARD.md:7-26` inserts correct tables before both old table types; the original axis rows are now at `86-87`, and capability rows at `260-269`. Their later position explains the seven old claims in B's stdout. At shape C's commit, `SCORECARD.md:1481-1499` carries the correct final tables, but the original line 5 (`Axes will be pinned with their counting commands as rounds land.`) is deleted. A and C have zero mismatches, isolating the prefix rejection from value parsing.

### Isolated setup

The clone and all command work directories are under `/fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace`. Git operations ran with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset. No sibling scratch directory was opened. No tools were installed or updated.

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

Observed setup output: none; exit 0. `df -h /fast` reported 178G available before detector clones were created. An initial asynchronous detector submission was refused by the host's background-job limit and did not start a detector. The completed runs below used synchronous Python subprocess capture, the same `timeout 2700` command, and fresh work directories.

## Pristine detector run

Expected detector: the frozen C1 counter without modification. A false result is expected at this frozen revision because the historical claims are stale. This red baseline is why a formal killed-mutant claim would be invalid.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/w-pristine
```

Full stdout, verbatim:

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

Exit code: `1`. Stderr: empty.

## Shape A — In-place rewrite

Only the seven historically mismatching rows were changed; the five already-correct rows were left alone. Expected: false because the original prefix was modified.

Mutant commit: `a880d32b7213bafde88a3ef86fcbaa9306f2668b`.

Each shape started from the frozen revision using:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

After the scoped SCORECARD edit, the exact commit command was:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam rewrite-A
```

Commit output: none; exit 0.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/w-rewrite-A
```

Full stdout, verbatim:

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
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=0 rev=a880d32b7213bafde88a3ef86fcbaa9306f2668b C1_R31_PASS=false
```

Exit code: `1`. Stderr: empty.

Requested diff evidence, captured while this commit was HEAD:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane diff HEAD~1 HEAD -- SCORECARD.md
```

The complete diff is 34 lines, so this is also the requested first-80-lines view. Exit code: `0`.

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..a3018f3 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -63,8 +63,8 @@ without retrospectively grading the training arc.
 
 | Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
 |---|---|---|---|---|
-| depth | 6 | One point per recorded mutation case listed in the tool's pinned replay ledger, capped at 10. `tools/mutate-and-run.sh:84-89`; command D below. This measures documented case depth, not newly executed cases. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
-| calibration | 0 | Two points per correctly restrained, durable-evidence-linked promotion assertion (`[~]`), capped at 8; the remaining 2 require independent promotion review of all boxes. Baseline has four `[x]` marks attributed to tameshi's own dispatched agents, not independent verifiers. `SHONEN.md:5-34`; command C below. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
+| depth | 9 | One point per recorded mutation case listed in the tool's pinned replay ledger, capped at 10. `tools/mutate-and-run.sh:84-89`; command D below. This measures documented case depth, not newly executed cases. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
+| calibration | 8 | Two points per correctly restrained, durable-evidence-linked promotion assertion (`[~]`), capped at 8; the remaining 2 require independent promotion review of all boxes. Baseline has four `[x]` marks attributed to tameshi's own dispatched agents, not independent verifiers. `SHONEN.md:5-34`; command C below. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
 
 Commands, run from this repo with `REV` set to the measured commit:
 
@@ -237,13 +237,13 @@ written and are superseded here:
 
 | Capability | What it can now do | Evidence pointer | First-working round |
 |---|---|---|---|
-| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 44 rows, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; `corpus/SOURCES.md` | fleet round 1 (kaika) |
-| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 80/80 pass`, exit 0 (`.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout`) | historical round 3 (`SCORECARD.md:16`); re-demonstrated fleet round 1 |
-| six-leg regression ledger | replay every recorded mutation case at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=6 passed=6 …)`, exit 0 (`…/capability-demo/h1b-regression.stdout`) | historical round 7 (four legs) / round 10 (six); re-demonstrated fleet round 1 |
+| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 92 rows, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; `corpus/SOURCES.md` | fleet round 1 (kaika) |
+| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0 (`.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout`) | historical round 3 (`SCORECARD.md:16`); re-demonstrated fleet round 1 |
+| six-leg regression ledger | replay every recorded mutation case at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9 …)`, exit 0 (`…/capability-demo/h1b-regression.stdout`) | historical round 7 (four legs) / round 10 (six); re-demonstrated fleet round 1 |
 | repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0; real bash controls match; red-before loop mutant fails the same mismatch oracle, restored loop passes; `.ufo/evidence/round-12/verification-final.json`, `oracle-repair.json`; measured `9df9212d33dc2dbda133e88f28ad47bb08839a5b` | round 12; lane demonstrated, outside admission pending |
-| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → 18/18 PASS0; real read changed3/unchanged3/unavailable0; `.ufo/evidence/round-13/verification.json`, `pin-dispositions.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
+| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → 19/19 PASS0; real read changed3/unchanged3/unavailable0; `.ufo/evidence/round-13/verification.json`, `pin-dispositions.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
 | exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations; prevent wrong-nesting in future producer output | metadata selftest39/39 PASS0; null-only companion FAIL1/corrected PASS0; producer same-oracle40/41 FAIL1→41/41 PASS0; `.ufo/evidence/round-13/producer-oracle-repair.json`, `verification-verdict.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
-| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → PASS34/34 exit0; same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded; `.ufo/evidence/round-14/verification-final.json`, S050; executable measurement6431478 | round14; lane demonstrated, separate outside admission pending |
+| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → PASS66/66 exit0; same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded; `.ufo/evidence/round-14/verification-final.json`, S050; executable measurement6431478 | round14; lane demonstrated, separate outside admission pending |
 | retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49, registered frozen0, missing-env1, tamper2, usage64; `.ufo/evidence/round-15/verification-3.json`; S051 | round15; lane demonstrated, separate non-author admission pending |
 | hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles, separating repeat variation from environmental sensitivity | `python3 tools/env-diff.py --selftest` first actual9/9; real receipt `f5/receipt-initial.json` under `.ufo/evidence/round-21/` classifies9/9 (eight invariant, one raw-output-variable); `corpus/knowledge/hermetic-env-differential.md`, S079/S081 | round21; lane demonstrated, separate non-author admission pending |
 | callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | at11f55d64968778aaed07b001fc8b2480c38e1896: frozen counter8/8, actual146-seat replay66 completed/80 failed, wrong-count1/TOTAL_MISMATCH; `.ufo/evidence/round-22/final/verification.json`, S082 | round22; lane demonstrated, separate non-author admission pending |
```

## Shape B — Correct tables inserted before old tables

The twelve correct values were inserted at the top. Expected: false because the old rows still occur last, and the insertion also breaks the base prefix.

Mutant commit: `2c1b9b6374aa864cae30c1e683833d9b8b458473`.

Each shape started from the frozen revision using:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

After the scoped SCORECARD edit, the exact commit command was:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam rewrite-B
```

Commit output: none; exit 0.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/w-rewrite-B
```

Full stdout, verbatim:

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
C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=0 rev=2c1b9b6374aa864cae30c1e683833d9b8b458473 C1_R31_PASS=false
```

Exit code: `1`. Stderr: empty.

Requested diff evidence, captured while this commit was HEAD:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane diff HEAD~1 HEAD -- SCORECARD.md
```

The complete diff is 31 lines, so this is also the requested first-80-lines view. Exit code: `0`.

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..7094cd5 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -4,6 +4,26 @@ Lane axes per AXES.md (six-axis vocabulary; primary verdicts per
 LEARNING.md trends). Probation rounds 1-3 build the initial measurements.
 Axes will be pinned with their counting commands as rounds land.
 
+## Re-stated values control
+
+| Capability | Observed values |
+|---|---|
+| sources-registry | exit 0, 92 rows |
+| mutation sweep runner | `MUTATE_SELFTEST: 106/106 pass`, exit 0 |
+| six-leg regression ledger | `REGRESSION: PASS (cases=9 passed=9)`, exit 0 |
+| repeated pristine-control gate | PASS (29 cases), exit 0 |
+| six-leg content-disposition probe | `--selftest` → 19/19 PASS0 |
+| exposed witness provenance correction | metadata selftest39/39 PASS0 |
+| effective expectation reconciliation | PASS66/66 exit0 |
+| retained invocation-context gate | → exit0, copied-source CLI selftest49/49 |
+| hermetic env-differential probe | actual9/9 |
+| callback-authoritative wave accounting | frozen counter8/8 |
+
+| Axis | Score (0–10) |
+|---|---|
+| depth | 9 |
+| calibration | 8 |
+
 ## Move log
 
 | Round | Axis | Before | After | Evidence |
```

## Shape C — Correct final tables plus unrelated deletion

The same correct tables were appended at EOF, and only the unrelated original line 5 was deleted elsewhere. Expected: false from the prefix requirement; last-row values should match.

Mutant commit: `0ff3f0655b0a8a350a60a52fdb840978000578fe`.

Each shape started from the frozen revision using:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

After the scoped SCORECARD edit, the exact commit command was:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam rewrite-C
```

Commit output: none; exit 0.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/w-rewrite-C
```

Full stdout, verbatim:

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
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=0 rev=0ff3f0655b0a8a350a60a52fdb840978000578fe C1_R31_PASS=false
```

Exit code: `1`. Stderr: empty.

Requested diff evidence, captured while this commit was HEAD:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane diff HEAD~1 HEAD -- SCORECARD.md
```

The complete diff is 36 lines, so this is also the requested first-80-lines view. Exit code: `0`.

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..379f9dd 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -2,7 +2,6 @@
 
 Lane axes per AXES.md (six-axis vocabulary; primary verdicts per
 LEARNING.md trends). Probation rounds 1-3 build the initial measurements.
-Axes will be pinned with their counting commands as rounds land.
 
 ## Move log
 
@@ -1478,3 +1477,23 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+## Re-stated values control
+
+| Capability | Observed values |
+|---|---|
+| sources-registry | exit 0, 92 rows |
+| mutation sweep runner | `MUTATE_SELFTEST: 106/106 pass`, exit 0 |
+| six-leg regression ledger | `REGRESSION: PASS (cases=9 passed=9)`, exit 0 |
+| repeated pristine-control gate | PASS (29 cases), exit 0 |
+| six-leg content-disposition probe | `--selftest` → 19/19 PASS0 |
+| exposed witness provenance correction | metadata selftest39/39 PASS0 |
+| effective expectation reconciliation | PASS66/66 exit0 |
+| retained invocation-context gate | → exit0, copied-source CLI selftest49/49 |
+| hermetic env-differential probe | actual9/9 |
+| callback-authoritative wave accounting | frozen counter8/8 |
+
+| Axis | Score (0–10) |
+|---|---|
+| depth | 9 |
+| calibration | 8 |
```

## Exact restoration and final detector run

The sandbox was returned to the original frozen commit after C with:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

Observed output: none; exit 0. A direct comparison with the retained original byte string printed:

```text
RESTORED_SCORECARD_SHA256=518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0
EXACT_ORIGINAL_BYTES_RESTORED=true
```

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/w-restored
```

Full stdout, verbatim:

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

Exit code: `1`. Stderr: empty.

Pristine and restored full stdout were byte-identical. Original and restored SCORECARD hashes below are equal; the exact byte comparison also succeeded.

### SHA-256 evidence

| Artifact / stage | Before | After |
|---|---|---|
| SCORECARD, pristine → restored | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` |
| SCORECARD, shape A | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` | `45e2a5c31ee43aec1ce6841be5d0420899f5c685ea3845704d9bb227534e56d8` |
| SCORECARD, shape B | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` | `92b7b93dd89f6dc373874b3bdc13eb1cc411527574e87c7a342102b6a3aceb2c` |
| SCORECARD, shape C | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` | `06b74c206041d325910a7260c56c939a4041bd49ec91c6ab368690ad75b42204` |
| Frozen counter, source and sandbox | `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584` | `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584` |
| Frozen contract, source and sandbox | `8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79` | `8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79` |

The original and final hash command was:

```sh
sha256sum /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane/SCORECARD.md /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane/.ufo/evidence/round-31/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane/.ufo/evidence/round-31/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/contract.json
```

Both invocations exited 0 and emitted these identical lines:

```text
518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0  /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane/SCORECARD.md
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane/.ufo/evidence/round-31/c1-measure.py
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py
8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79  /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane/.ufo/evidence/round-31/contract.json
8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/contract.json
```

Per-mutant hashes were captured with `sha256sum /fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/lane/SCORECARD.md` while each respective mutant was HEAD; each invocation exited 0.

After all runs, enumerating `/proc/*/cwd` for this seat (excluding the current tool interpreter) found no remaining seat processes: `REMAINING_SEAT_PROCESSES=[]`. No process was killed. Raw stdout, stderr, diffs and the combined `runs.json` are retained directly under `/fast/scratch/hyaku/tameshi-r31-seats/CtlRewriteInPlace/`; the five fresh detector work directories are `w-pristine`, `w-rewrite-A`, `w-rewrite-B`, `w-rewrite-C`, and `w-restored`.

## Smallest safe correction

Do not alter the frozen counter or predicate. Preserve every original SCORECARD byte, then append the correct re-stated tables after the old tables. For A, restore the historical rows; for B, place the new tables at EOF instead; for C, restore the deleted old line. No production correction or passing-result claim is made by this control probe.
