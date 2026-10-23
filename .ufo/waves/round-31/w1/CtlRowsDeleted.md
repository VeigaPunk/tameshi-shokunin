# Verdict

All three controls were rejected: `C1_R31_PASS=false`, exit 1, with 12 unparsed statements and `append_only=0`. No control produced a false pass. The mutation-testing verdict for A, B and C is **INCONCLUSIVE**, not killed: the pristine detector already exited 1 with seven mismatches.

Axis: **calibration**. Guardrails: unchanged frozen counter and contract, isolated sandbox commits, and exact byte restoration. No content fix or integration was performed.

# Evidence

Frozen parent: `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. Every control is one sandbox commit with exactly that parent. A uses `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane`; the independent B and C clones use `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B` and `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C`. All clones were detached at the frozen revision before mutation. The shared pristine run below measures their identical parent bytes; each parent SCORECARD was compared byte for byte with that pristine snapshot.

Expected detector: the unchanged frozen counter must reject absent or blank claim values and a broken base prefix. The frozen contract is `.ufo/evidence/round-31/contract.json:12-26`; its fixed statement list is enforced by `.ufo/evidence/round-31/c1-measure.py:38-65`. Missing rows and blank values are unparsed at `:126-133`, the prefix check is at `:196-202`, and rejection is at `:205-224`. At the restored frozen revision, the targeted source rows are `SCORECARD.md:66-67` and `:240-249`; their headers are at `:64-65` and `:238-239`. Shape C retains only `SCORECARD.md:1-5`.

## Frozen input hashes

| Input | Before SHA-256 | After SHA-256 |
|---|---|---|
| Counter | `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584` | `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584` |
| Contract | `8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79` | `8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79` |

The counter digest equals the digest in the frozen contract. Initial hashes were measured with:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/contract.json SCORECARD.md .ufo/evidence/round-31/c1-measure.py .ufo/evidence/round-31/contract.json
```

Final digests were recomputed from the same source files; all restored clones also have those counter and contract digests. Neither frozen file was edited.

## Setup

The seat directory was created with Python `Path.mkdir(parents=True, exist_ok=True)`. The disk check `df -h /fast` returned:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  628G  176G  79% /fast
```

Initial sandbox commands, exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

The B and C clones were created before A was mutated. There were no writes to the fleet Git index or lane Git index. An attempted asynchronous tool launch was refused at the host background-job limit before execution; the same bounded command was then executed through a subprocess.

## Shared pristine detector

Command, executed with cwd `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane` and Git environment variables removed:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/w-pristine
```

Full stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/receipt-pristine.stdout:1-13`):

```text
STATEMENT sources-registry: claimed=0,44 observed=0,92 (exit=0) MISMATCH
STATEMENT mutation sweep runner: claimed=80,80,0 observed=106,106,0 (exit=0) MISMATCH
STATEMENT six-leg regression ledger: claimed=PASS,6,6,0 observed=FAIL,9,8,1 (exit=1) MISMATCH
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

Exit code: **1**. Stderr: empty. Elapsed: 298.199 seconds.

## Shape A: mutation

Deleted the two Current axes data rows and ten Capabilities data rows; retained both table headers and all other bytes.

Commit command, exit 0, no stdout:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam deleted-A
```

Commit: `a5df625f66e22ae8459bc0e2a0eccdd209d3ba48`. Parent: `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. Subject: `deleted-A`.

Before SCORECARD SHA-256: `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` (118152 bytes). Mutated committed and worktree SHA-256: `144708c1c755fed3dea480b38b231038c2ffeb41a8ab54d953a47ec4a88c2e85` (112922 bytes). Committed bytes were obtained with `git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane show HEAD:SCORECARD.md`; parent bytes with `git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane show HEAD~1:SCORECARD.md`; both commands exited 0. Hashes use `hashlib.sha256`.

## Shape A: frozen counter

Command, executed with cwd `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane` and Git environment variables removed:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/w-deleted-A
```

Full stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/receipt-deleted-A.stdout:1-13`):

```text
STATEMENT sources-registry: claimed=- observed=0,92 (exit=0) UNPARSED
STATEMENT mutation sweep runner: claimed=- observed=106,106,0 (exit=0) UNPARSED
STATEMENT six-leg regression ledger: claimed=- observed=PASS,9,9,0 (exit=0) UNPARSED
STATEMENT repeated pristine-control gate: claimed=- observed=PASS,29,0 (exit=0) UNPARSED
STATEMENT six-leg content-disposition probe: claimed=- observed=19,19,0 (exit=0) UNPARSED
STATEMENT exposed witness provenance correction: claimed=- observed=39,39,0 (exit=0) UNPARSED
STATEMENT effective expectation reconciliation: claimed=- observed=66,66,0 (exit=0) UNPARSED
STATEMENT retained invocation-context gate: claimed=- observed=0,49,49 (exit=0) UNPARSED
STATEMENT hermetic env-differential probe: claimed=- observed=9,9 (exit=0) UNPARSED
STATEMENT callback-authoritative wave accounting: claimed=- observed=8,8 (exit=0) UNPARSED
STATEMENT depth: claimed=- observed=9 (exit=0) UNPARSED
STATEMENT calibration: claimed=- observed=8 (exit=0) UNPARSED
C1_R31: statements=12 mismatches=12 unparsed=12 unobservable=0 append_only=0 rev=a5df625f66e22ae8459bc0e2a0eccdd209d3ba48 C1_R31_PASS=false
```

Exit code: **1**. Stderr: empty. Elapsed: 194.515 seconds.

### Shape A: requested diff prefix

Executed before restoration, exit 0:

```sh
git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane diff HEAD~1 HEAD -- SCORECARD.md | head -80
```

Verbatim output (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/deleted-A.diff-first80:1-30, full diff`):

````diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..96d5f1b 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -63,8 +63,6 @@ without retrospectively grading the training arc.
 
 | Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
 |---|---|---|---|---|
-| depth | 6 | One point per recorded mutation case listed in the tool's pinned replay ledger, capped at 10. `tools/mutate-and-run.sh:84-89`; command D below. This measures documented case depth, not newly executed cases. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
-| calibration | 0 | Two points per correctly restrained, durable-evidence-linked promotion assertion (`[~]`), capped at 8; the remaining 2 require independent promotion review of all boxes. Baseline has four `[x]` marks attributed to tameshi's own dispatched agents, not independent verifiers. `SHONEN.md:5-34`; command C below. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
 
 Commands, run from this repo with `REV` set to the measured commit:
 
@@ -237,16 +235,6 @@ written and are superseded here:
 
 | Capability | What it can now do | Evidence pointer | First-working round |
 |---|---|---|---|
-| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 44 rows, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; `corpus/SOURCES.md` | fleet round 1 (kaika) |
-| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 80/80 pass`, exit 0 (`.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout`) | historical round 3 (`SCORECARD.md:16`); re-demonstrated fleet round 1 |
-| six-leg regression ledger | replay every recorded mutation case at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=6 passed=6 …)`, exit 0 (`…/capability-demo/h1b-regression.stdout`) | historical round 7 (four legs) / round 10 (six); re-demonstrated fleet round 1 |
-| repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0; real bash controls match; red-before loop mutant fails the same mismatch oracle, restored loop passes; `.ufo/evidence/round-12/verification-final.json`, `oracle-repair.json`; measured `9df9212d33dc2dbda133e88f28ad47bb08839a5b` | round 12; lane demonstrated, outside admission pending |
-| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → 18/18 PASS0; real read changed3/unchanged3/unavailable0; `.ufo/evidence/round-13/verification.json`, `pin-dispositions.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
-| exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations; prevent wrong-nesting in future producer output | metadata selftest39/39 PASS0; null-only companion FAIL1/corrected PASS0; producer same-oracle40/41 FAIL1→41/41 PASS0; `.ufo/evidence/round-13/producer-oracle-repair.json`, `verification-verdict.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
-| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → PASS34/34 exit0; same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded; `.ufo/evidence/round-14/verification-final.json`, S050; executable measurement6431478 | round14; lane demonstrated, separate outside admission pending |
-| retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49, registered frozen0, missing-env1, tamper2, usage64; `.ufo/evidence/round-15/verification-3.json`; S051 | round15; lane demonstrated, separate non-author admission pending |
-| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles, separating repeat variation from environmental sensitivity | `python3 tools/env-diff.py --selftest` first actual9/9; real receipt `f5/receipt-initial.json` under `.ufo/evidence/round-21/` classifies9/9 (eight invariant, one raw-output-variable); `corpus/knowledge/hermetic-env-differential.md`, S079/S081 | round21; lane demonstrated, separate non-author admission pending |
-| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | at11f55d64968778aaed07b001fc8b2480c38e1896: frozen counter8/8, actual146-seat replay66 completed/80 failed, wrong-count1/TOTAL_MISMATCH; `.ufo/evidence/round-22/final/verification.json`, S082 | round22; lane demonstrated, separate non-author admission pending |
 
 Rows enter only through a round that demonstrates the capability running (`AXES.md` §Capabilities); none enter through this rollout.
 
````

## Shape B: mutation

Retained the 12 row names and both table headers, but blanked every value cell in those rows. Other bytes are unchanged.

Commit command, exit 0, no stdout:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B -c user.name=ctl -c user.email=ctl@sandbox commit -qam deleted-B
```

Commit: `e22d671d99c30acee1338c96610a695aad45ffa8`. Parent: `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. Subject: `deleted-B`.

Before SCORECARD SHA-256: `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` (118152 bytes). Mutated committed and worktree SHA-256: `fb9b2189cf212cee90f5f1637c8e0ddf862f8c2695caa48115b15cc9e349c81f` (113373 bytes). Committed bytes were obtained with `git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B show HEAD:SCORECARD.md`; parent bytes with `git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B show HEAD~1:SCORECARD.md`; both commands exited 0. Hashes use `hashlib.sha256`.

## Shape B: frozen counter

Command, executed with cwd `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B` and Git environment variables removed:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/w-deleted-B
```

Full stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/receipt-deleted-B.stdout:1-13`):

```text
STATEMENT sources-registry: claimed=- observed=0,92 (exit=0) UNPARSED
STATEMENT mutation sweep runner: claimed=- observed=106,106,0 (exit=0) UNPARSED
STATEMENT six-leg regression ledger: claimed=- observed=PASS,9,9,0 (exit=0) UNPARSED
STATEMENT repeated pristine-control gate: claimed=- observed=PASS,29,0 (exit=0) UNPARSED
STATEMENT six-leg content-disposition probe: claimed=- observed=19,19,0 (exit=0) UNPARSED
STATEMENT exposed witness provenance correction: claimed=- observed=39,39,0 (exit=0) UNPARSED
STATEMENT effective expectation reconciliation: claimed=- observed=66,66,0 (exit=0) UNPARSED
STATEMENT retained invocation-context gate: claimed=- observed=0,49,49 (exit=0) UNPARSED
STATEMENT hermetic env-differential probe: claimed=- observed=9,9 (exit=0) UNPARSED
STATEMENT callback-authoritative wave accounting: claimed=- observed=8,8 (exit=0) UNPARSED
STATEMENT depth: claimed=- observed=9 (exit=0) UNPARSED
STATEMENT calibration: claimed=- observed=8 (exit=0) UNPARSED
C1_R31: statements=12 mismatches=12 unparsed=12 unobservable=0 append_only=0 rev=e22d671d99c30acee1338c96610a695aad45ffa8 C1_R31_PASS=false
```

Exit code: **1**. Stderr: empty. Elapsed: 211.249 seconds.

### Shape B: requested diff prefix

Executed before restoration, exit 0:

```sh
git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B diff HEAD~1 HEAD -- SCORECARD.md | head -80
```

Verbatim output (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/deleted-B.diff-first80:1-42, full diff`):

````diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..96258e5 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -63,8 +63,8 @@ without retrospectively grading the training arc.
 
 | Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
 |---|---|---|---|---|
-| depth | 6 | One point per recorded mutation case listed in the tool's pinned replay ledger, capped at 10. `tools/mutate-and-run.sh:84-89`; command D below. This measures documented case depth, not newly executed cases. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
-| calibration | 0 | Two points per correctly restrained, durable-evidence-linked promotion assertion (`[~]`), capped at 8; the remaining 2 require independent promotion review of all boxes. Baseline has four `[x]` marks attributed to tameshi's own dispatched agents, not independent verifiers. `SHONEN.md:5-34`; command C below. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
+| depth | | | | |
+| calibration | | | | |
 
 Commands, run from this repo with `REV` set to the measured commit:
 
@@ -237,16 +237,16 @@ written and are superseded here:
 
 | Capability | What it can now do | Evidence pointer | First-working round |
 |---|---|---|---|
-| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 44 rows, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; `corpus/SOURCES.md` | fleet round 1 (kaika) |
-| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 80/80 pass`, exit 0 (`.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout`) | historical round 3 (`SCORECARD.md:16`); re-demonstrated fleet round 1 |
-| six-leg regression ledger | replay every recorded mutation case at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=6 passed=6 …)`, exit 0 (`…/capability-demo/h1b-regression.stdout`) | historical round 7 (four legs) / round 10 (six); re-demonstrated fleet round 1 |
-| repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0; real bash controls match; red-before loop mutant fails the same mismatch oracle, restored loop passes; `.ufo/evidence/round-12/verification-final.json`, `oracle-repair.json`; measured `9df9212d33dc2dbda133e88f28ad47bb08839a5b` | round 12; lane demonstrated, outside admission pending |
-| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → 18/18 PASS0; real read changed3/unchanged3/unavailable0; `.ufo/evidence/round-13/verification.json`, `pin-dispositions.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
-| exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations; prevent wrong-nesting in future producer output | metadata selftest39/39 PASS0; null-only companion FAIL1/corrected PASS0; producer same-oracle40/41 FAIL1→41/41 PASS0; `.ufo/evidence/round-13/producer-oracle-repair.json`, `verification-verdict.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
-| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → PASS34/34 exit0; same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded; `.ufo/evidence/round-14/verification-final.json`, S050; executable measurement6431478 | round14; lane demonstrated, separate outside admission pending |
-| retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49, registered frozen0, missing-env1, tamper2, usage64; `.ufo/evidence/round-15/verification-3.json`; S051 | round15; lane demonstrated, separate non-author admission pending |
-| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles, separating repeat variation from environmental sensitivity | `python3 tools/env-diff.py --selftest` first actual9/9; real receipt `f5/receipt-initial.json` under `.ufo/evidence/round-21/` classifies9/9 (eight invariant, one raw-output-variable); `corpus/knowledge/hermetic-env-differential.md`, S079/S081 | round21; lane demonstrated, separate non-author admission pending |
-| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | at11f55d64968778aaed07b001fc8b2480c38e1896: frozen counter8/8, actual146-seat replay66 completed/80 failed, wrong-count1/TOTAL_MISMATCH; `.ufo/evidence/round-22/final/verification.json`, S082 | round22; lane demonstrated, separate non-author admission pending |
+| sources-registry | | | |
+| mutation sweep runner | | | |
+| six-leg regression ledger | | | |
+| repeated pristine-control gate | | | |
+| six-leg content-disposition probe | | | |
+| exposed witness provenance correction | | | |
+| effective expectation reconciliation | | | |
+| retained invocation-context gate | | | |
+| hermetic env-differential probe | | | |
+| callback-authoritative wave accounting | | | |
 
 Rows enter only through a round that demonstrates the capability running (`AXES.md` §Capabilities); none enter through this rollout.
 
````

## Shape C: mutation

Replaced SCORECARD.md with its exact first five lines, including the fifth line ending.

Commit command, exit 0, no stdout:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C -c user.name=ctl -c user.email=ctl@sandbox commit -qam deleted-C
```

Commit: `7cf20b0b205a41fc80864cf54270cf6fa0381ca8`. Parent: `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. Subject: `deleted-C`.

Before SCORECARD SHA-256: `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` (118152 bytes). Mutated committed and worktree SHA-256: `54f3d74ed59af3e2a916b9b35bf3894b62efe23b8fe96239401341a8df4911b0` (238 bytes). Committed bytes were obtained with `git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C show HEAD:SCORECARD.md`; parent bytes with `git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C show HEAD~1:SCORECARD.md`; both commands exited 0. Hashes use `hashlib.sha256`.

## Shape C: frozen counter

Command, executed with cwd `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C` and Git environment variables removed:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/w-deleted-C
```

Full stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/receipt-deleted-C.stdout:1-13`):

```text
STATEMENT sources-registry: claimed=- observed=0,92 (exit=0) UNPARSED
STATEMENT mutation sweep runner: claimed=- observed=106,106,0 (exit=0) UNPARSED
STATEMENT six-leg regression ledger: claimed=- observed=PASS,9,9,0 (exit=0) UNPARSED
STATEMENT repeated pristine-control gate: claimed=- observed=PASS,29,0 (exit=0) UNPARSED
STATEMENT six-leg content-disposition probe: claimed=- observed=19,19,0 (exit=0) UNPARSED
STATEMENT exposed witness provenance correction: claimed=- observed=39,39,0 (exit=0) UNPARSED
STATEMENT effective expectation reconciliation: claimed=- observed=66,66,0 (exit=0) UNPARSED
STATEMENT retained invocation-context gate: claimed=- observed=0,49,49 (exit=0) UNPARSED
STATEMENT hermetic env-differential probe: claimed=- observed=9,9 (exit=0) UNPARSED
STATEMENT callback-authoritative wave accounting: claimed=- observed=8,8 (exit=0) UNPARSED
STATEMENT depth: claimed=- observed=9 (exit=0) UNPARSED
STATEMENT calibration: claimed=- observed=8 (exit=0) UNPARSED
C1_R31: statements=12 mismatches=12 unparsed=12 unobservable=0 append_only=0 rev=7cf20b0b205a41fc80864cf54270cf6fa0381ca8 C1_R31_PASS=false
```

Exit code: **1**. Stderr: empty. Elapsed: 211.302 seconds.

### Shape C: requested diff prefix

Executed before restoration, exit 0:

```sh
git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C diff HEAD~1 HEAD -- SCORECARD.md | head -80
```

Verbatim output (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/deleted-C.diff-first80:1-80, first 80 lines only`):

````diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..bb48e82 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -3,1478 +3,3 @@
 Lane axes per AXES.md (six-axis vocabulary; primary verdicts per
 LEARNING.md trends). Probation rounds 1-3 build the initial measurements.
 Axes will be pinned with their counting commands as rounds land.
-
-## Move log
-
-| Round | Axis | Before | After | Evidence |
-|---|---|---|---|
-| 1 | depth | seed `SKILL.md`: 22 lines, 0 tables, 0 cited sources, corpus empty | 171 lines: gate-shape decision table (3 rows), fail-closed arm taxonomy (5 rows), 7 mutation-bar rules, 8-step no-permissiveness audit recipe — every rule citing a survey-note line; 3 source notes admitted under it (556+335+105 lines) | `git show 40f8e1f:SKILL.md \| wc -l` → 22; `wc -l SKILL.md corpus/knowledge/*.md` → 171 / 556 / 335 / 105; `grep -cE '^\| ' SKILL.md` → 10 (8 rule rows + 2 header rows); `grep -c 'corpus/knowledge/' SKILL.md` → 3. Re-run 2026-10-14 (TAMESHI-SCRIBE) |
-| 1 | calibration | no observation/inference/unknown separation measured anywhere (corpus empty, no notes) | all three notes label every claim and keep the classes apart (kumitate O:33/I:7, kagi [OBS]28/[INF]18/[UNK]7, fleet OBSERVATION×11/INFERENCE×4); unknowns named as unknowns, never green (kumitate §9 ×4; kagi [UNK] ×7; fleet U1–U7); self-caught errors kept as append-only errata, not silently fixed (kagi ER-1 = 16 wrong-line cites + generator analysis); counts quoted from executed counters, never source greps (kumitate 62/42/60/102/39/43 executed vs 62/42/60/71/35/41 literal sites; kagi 250 from suite counters vs static 6/1/0/1/6/2) | `grep -oE '(^|[[:space:]])O:' corpus/knowledge/gates-survey-kumitate.md \| wc -l` → 33 (same for `I:` → 7); `grep -oE '\[OBS\]' corpus/knowledge/gates-survey-kagi.md \| wc -l` → 28 (`[INF]` → 18, `[UNK]` → 7); `grep -cE '^\| §' corpus/knowledge/gates-survey-kagi.md` → 16; `grep -cE '^- U[0-9]' corpus/knowledge/verification-patterns-fleet.md` → 9 (U1–U7 + 2 prediction bullets). Re-run 2026-10-14 (TAMESHI-SCRIBE) |
-| 2 | depth | corpus carried no kill-rate measurement on any gate (round-1 census: "no kill-rate harness or self-code fault injection anywhere in the corpus"; SKILL's mutation bar was nominal-vs-load-bearing by argument only) | first measured kill-rate: `kimi-census.mjs`'s 43-case hermetic suite vs 10 single-edit mutants (fresh /tmp copies, one exact edit each, driver asserts old-string unique; original byte-identical, sha256 before=after `83016d45…`) → **8/10 killed (80 %)**, no inconclusive run (control 43/43; every mutant run still enumerated 43), 7.0 s sweep; survivors D2 `findings.slice(0,6)`→`(0,5)` + D10 `FROZEN.K2 25`→`24` = reported-but-unasserted surfaces (max findings in any suite run = 2 vs cap 6 + prefix-only DRIFT asserts; only `frozen.K5` asserted); per-kill failing-case labels + full reproduce spec in the new 206-line note; distilled into SKILL.md's measured mutation-bar table (kill-rate bands >80 / 50-80 / <50 with admission readings — bands are a report convention, 8/10 admits) + defect taxonomy + when-not-worth-it rules | `node kumitate-shokunin/scripts/kimi-census.mjs --selftest` → `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 (denominator held); `sha256sum kumitate-shokunin/scripts/kimi-census.mjs` → `83016d45049b009a…4f426` (pin held; kumitate HEAD `175de6ba`, path clean); `wc -l corpus/knowledge/mutation-case-kimi-census.md` → 206; `grep -cF '**killed**'` → 8, `grep -cF '**survived**'` → 2 (the 8/10); sensitivity re-runs from the lane's retained scratch: `node /tmp/tameshi-r2-1-work/mutant-D2.mjs --root /tmp/tameshi-r2-1-work/empty-root \| tail -1` → 5 ids + `+23 more`, `node /tmp/tameshi-r2-1-work/mutant-D10.mjs --root … \| grep 'FAMILY K2'` → `frozen=24` (both survivors observably different off-suite, as claimed); `grep -cE '^\| ' SKILL.md` → 14 (round-1 10 + 1 header + 3 band rows), `wc -l SKILL.md` → 244. Re-run 2026-10-14 (TAMESHI-SCR) |
-| 2 | calibration | wave-1 record: kagi ER-1 ×16 the only errata; kumitate + fleet errata blocks "(none yet)"; three carried gaps recorded as recommendations | wave-1 review trail applied append-only to all three notes — 15 errata entries (K-R2 ×4, G-R2 ×6, V-R2 ×4) + E1 in the new mutation note (author's D7-survivor expectation wrong, kept as a calibration miss); 4 substantive corrections: K-R2-2 meta-check anchors → `claims-check.mjs:851-852` / `kimi-census.mjs:841-842`; G-R2-1 claim-ledger pin → 79301 B / `93c5827202b9cdec` (surveyed 79294/`357fb245` never committed; kagi's own round-18 `fecee87` re-pinned stamps.tsv); G-R2-2 §9 citation :53-56 → :26-28; G-R2-3 denied verbs 22→23; the rest holds/dispositions (six kumitate executed counts + pins held; kagi 250 selftest cases + `--falsify` 16/18 held; kaidoku 72 files / 468 vs 467 held; w6-w8 AGREE tallies held; kagi §8.1 [UNK] discharged = own round-18 [INF]; sibling-owned items stay recorded-not-absorbed; U1/U2 open); nothing above any errata block edited | `grep -c '^\*\*K-R2' corpus/knowledge/gates-survey-kumitate.md` → 4; `'^\*\*G-R2'` → 6; `'^\*\*V-R2'` → 4; `grep -c '^E1 —' corpus/knowledge/mutation-case-kimi-census.md` → 1; `grep -n "every finding kind fired by the suite" kumitate-shokunin/scripts/claims-check.mjs scripts/kimi-census.mjs` → :851/:841 and "…fail-closed arm…" → :852/:842 (K-R2-2 exact); `sha256sum kagi-shokunin/corpus/claim-ledger.sh` → `93c5827202b9cdec…` + `stat -c %s` → 79301 + `git -C kagi-shokunin log -1 --format='%h %ci %s'` → `fecee87` round-18 10:05:10; DENY pipeline `grep '^DENY_WORD_RE=' … \| grep -oE … \| tr '\|' '\n' \| wc -l` → 23; `sed -n '26,28p'` = the final-line rule, `'53,56p'` = the usage paragraph (G-R2-2 exact); claim-ledger selftest → `SELFTEST: PASS (97 cases)` exit 0, scope-gate → `SCOPE_SELFTEST: PASS (61 cases)` exit 0, `--falsify` exit 1 → `SCOPE_FALSIFY: FAIL (caught=16/18 failed=2)` with 2× `SCOPE BREADTH-EXCEEDS`, kagi tree porcelain-empty before/after, `corpus/README.md:43` still `18/18`; kaidoku `ls … \| wc -l` → 72, `verify:` → 468, `verified-at:` → 467; w6/w7/w8 closeout AGREE grep → 3×5/5, 3×5/5, 2×6/6+1×5/5. Re-run 2026-10-14 (TAMESHI-SCR) |
-| 3 | depth | one measured kill-rate, one language, one gate (round 2: JS `kimi-census.mjs` 8/10) — PROVINCE's ≥2-lane rule blocked calling the method general, the 50 % crossover and both band interiors were unprobed, and the bash side had no measurement at all | second measured kill-rate on a bash gate, same headline: kagi `surface-census.sh`'s 16-case selftest vs 10 single-edit mutants → **8/10 killed (80 %)**, no inconclusive run, suite count held on every run, 11.0 s for 11 runs; survivors B5 (**fixture-absent arm** — deleted exec x-bit arm reachable by no case, a survivor class round 2 did not have) + B10 (CLEAN-summary `ok=` swapped — reported-never-read, same family as D10); kill widths measured per case (widest bash kill 3/16 vs JS up to 16/43 — per-case fresh fixtures + exit+token asserts vs shared fixtures + exact-line asserts; B4 killed on the token assert alone with the expected exit code); cross-language divergence distilled: same rate, different kill width, shared class reported-but-unasserted data (D2/D10, B10) + bash-only unreached-arm class (B5) — SKILL.md gained the 10-step executable sweep recipe, defect-class catalog with per-class JS+bash evidence columns, restore-discipline checklist, divergence section, and full reproduce appendices for both cases (244 → 665 lines); the plan's anti-claim resolved: the rates do not diverge wildly, the language-class differences sit in kill width and survivor composition, recorded as the finding | `bash kagi-shokunin/corpus/surface-census.sh --selftest` → `SELFTEST: PASS (16 cases)`, exit 0, skip-cases 15/16 `substrate-absent`, kagi tree porcelain-empty before/after (denominator held); `sha256sum kagi-shokunin/corpus/surface-census.sh` → `275d8294…53009f` (pin held; kagi HEAD `fecee87`); `wc -l corpus/knowledge/mutation-case-kagi-census.md` → 258 (final line unterminated); `grep -cF '**killed**'` → 8, `grep -cF '**survived**'` → 2, table rows `grep -cE '^\| (—\|B[0-9]+) \|'` → 11; anchors re-read on the pinned bytes (`sed -n '241p;214p;862p;85p'` = the guard inversion / exec-x-bit arm / summary args / die exit-2 lines, all four matching the note's edits); full independent re-sweep through the shipped tool from a spec cut from the pinned artifact → `CONTROL: GREEN`, B1–B9 per-kill failing counts 1/2/3/1/2/1/2/2 of 16 exactly as the note's table, B5+B10 `PASS (16 cases)`, `MUTATE_RESTORE: OK` before=after, `MUTATE: DONE (… killed=8 survived=2 inconclusive=0 kill-rate=80 %)`. Re-run 2026-10-14 (TAMESHI-B4) |
-| 3 | operability | the mutation method existed only as prose + a per-lane ad-hoc driver left in /tmp (round 2's `mutate_driver.py` was one-off, unversioned, not in-tree); no tameshi-owned runnable instrument existed | first tool: `tools/mutate-and-run.sh` (611 lines, r3-2) — generic inject→run→restore runner: spec v1 with fail-closed parsing (count==1 asserted before any suite run, no-op edit refused, escape allowlist `\n \t \r \\`, CR refused), pinned pristine + fresh byte-copy mutants, green-control gate before any mutant run, per-defect KILLED / SURVIVED / INCONCLUSIVE (timeout 124, 126/127 = not runnable), byte-identity restore proof (`MUTATE_RESTORE: OK\|DRIFT`), evidence workdir (control + per-defect full logs, results.tsv, spec.copy), exit map 0/1/2/64; hermetic selftest builds its own fixture + mini-suite and checks control-green, kill, survivor, exact kill-rate line, restore, DEGRADED and all refusal paths — 24/24; the tool re-ran both fleet cases end-to-end: audit lane B3's dual sweep (`MUTATE: DONE … killed=8 survived=2 … kill-rate=80 %` on BOTH targets, verdict-per-defect identical to both notes, restore OK ×2) and B2's D5 re-run (same kill, same mutant sha as the executor's run) — the round-2 note's manual method now reproduces from one versioned instrument | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 24/24 pass` / `VERDICT: PASS`, exit 0; `sha256sum tools/mutate-and-run.sh` → `d8abee52…eda68` (the revision the audits replayed); scribe re-sweep in own scratch: `bash tools/mutate-and-run.sh --target kagi-shokunin/corpus/surface-census.sh --defects <spec cut from pinned bytes> --suite 'bash "$MUTANT" --selftest'` → `CONTROL: GREEN`, 8× `DEFECT B<n>: KILLED (exit=1 …)`, `DEFECT B5: SURVIVED (exit=0 …)`, `DEFECT B10: SURVIVED (exit=0 …)`, `MUTATE_RESTORE: OK`, `MUTATE: DONE (target=surface-census-b4 defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80 %)`, exit 0; audit evidence re-checked: B3 `results.tsv` ×2 (10 rows each, verdicts identical to the notes) + `MUTATE_RESTORE: OK` lines, B2 `results.tsv` D5 KILLED mutant-sha `b0dfe1a7…` = the executor note's recorded sha; `wc -l tools/mutate-and-run.sh` → 611. Re-run 2026-10-14 (TAMESHI-B4) |
-| 4 | calibration | round-3 state | arm-class matrix (JS+bash cases) + round-gate static projection (§13) | wave-4 32-lane; VER-T1 |
-| 5 | depth | round-4 state | 3rd mutation case (tsukuroi gate, cross-author): 6/10 killed, matrix amended per arm-class evidence (not smoothed) | wave-5 32-lane |
-| 6 | adjacency + operability | round-5 state | the service round on mado's gate: 4/10 killed, in-surface 4/4 vs out-of-surface 0/6 — the co-extensive assertion/kill finding | wave-6 32-lane (2 lanes rerouted alibaba->hyper) |
-| 7 | operability | round-6 state | the leg ledger: --regression replays ALL 4 recorded cases at pinned git blobs (drift-immune | wave-7 32-lane (3 rerouted alibaba->hyper) |
-| 8 | coverage | round-7 state | cases 5+6: kagi checklist-run (47%, third co-extensive instance, 15/15 pre-registered predictions) + kumitate claims-check | wave-8 32-lane (2 rerouted alibaba->hyper) |
-| 9 | operability | round-8 state | the cadence tick fired: 4/4 legs PASS | wave-9 32-lane (2 rerouted alibaba->hyper) |
-| 10 | operability | round-9 state | the operator runbook (511 lines, cold-readable, exercised receipts) | wave-10 32-lane (1 rerouted alibaba->hyper) |
-| 11 | operability (terminal — the close) | round-10 state: the operator runbook landed with executed receipts, but the cadence was "a convention, not a mechanism" (ledger U9) — no firing had been announced in advance; both moved gates read `stale` with no successor rows; the ten rounds had no single restatement and the runbook's leg lines still read four | **the close:** the pre-announced tick fired — announcement `068578f1…` @ `606716f` (21:28:23Z) → first firing 21:32:35Z (**Δ +4 m 12 s**), five independent firings; pin read **4 current · 2 stale · 0 drift** (tsukuroi `084951be…` → live `10452443…` @ `af8adf1`; mado `d7edaab4…` → `93e43f8f…` @ `f7bfc9f`); tool pulse `--selftest` 80/80 + six-leg `--regression` `PASS (cases=6 passed=6; ledger legs exact…)` at `75ed934d…` (**held**), independent leg-check 6/6 clean + 65/65 mutants re-applied byte-identical; the schedule + tick series 1–4 + gap series (45 m 20 s · 51 m 45 s · 40 m 16 s) + interval `[U]` land (`closeout-r11.md` §2.5); the ten rounds restated + the service as it stands + the named debts (§1–§4 of the same note); `plans/completion-evidence.md` (PACK-T); SKILL final-pointers section (+100/−1 → 1 461 L); `corpus/lessons/round-10.md` (T11-2); `reports/r11-aud-t11.md` (12-row verdict table, CONFIRMED ×12); **open at close:** the two stale-gate successor rows (ledger byte-identical `2f25c51e…`, no appended rows), the six-leg registry row, the runbook's four-leg lines (ER-R3), the census §5 re-pin errata, the coverage rows, the r10 fresh-executor table, tsukuroi's 9 clause sites (owner's), the attestation leg + the queue | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 80/80 pass` rc 0; `--regression --workdir /tmp/w11-scr-t11/regr` → `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0, `REGRESSION_DATE 2026-10-14T21:34:27Z`, tool `75ed934d…`; six-case pin read 21:36:27Z → 4 current · 2 stale · 0 drift (`/tmp/w11-scr-t11/pin-read-open.txt`; four lanes' reads agreeing cell-for-cell); ledger `2f25c51e…` unchanged all window; poll `poll.log` (60 s × 30). Re-run 2026-10-14 (SCR-T11) |
-
-## The ten training rounds — verdict table (rounds 2–11 = training r1–r10)
-
-Completed at the arc's close (round 11 = training r10; the arc has no
-successor — `plans/round-11.plan.md:13-25`). One row per training round, every
-cell anchored to the round's landed record; nothing is re-measured and no
-verdict is re-adjudicated — this table restates the move-log rows above and
-`closeout-r11.md` §1 (`:42-59`; its own round-11 row was `in flight` at its
-write, completed here from the round's own receipts). Verdicts as the records
-land them: r1–r2 carry the rounds' recorded `improved` sentences
-(`LOG.md:156-162`, `:278-289`); r3–r10 land an axis move — the records' own
-language ("Axis moved: …", `LOG.md:303`) — and no landed row records a
-`harmed` / `unchanged` / `unprovable-but-better` verdict. A cell with no
-landed verdict renders `—`, never manufactured. Mirror: the parent's one-line
-pack, `plans/completion-evidence.md:27-41`.
-
-| Training | Round | Axis | The move (one line) | Verdict, as recorded | Receipt |
-|---|---|---|---|---|---|
-| r1 | 2 | depth + calibration | first measured kill-rate (kimi-census 8/10, 80 %); wave-1 errata append-only; fleet 4th pattern | improved | `SCORECARD.md:13-14` · `LOG.md:68` · `2587e0a` |
-| r2 | 3 | depth + operability | second kill-rate, first bash gate (surface-census 8/10, 80 %); first tool (selftest 24/24); no-oral-context executor test | improved | `SCORECARD.md:15-16` · `LOG.md:173` · `53e74a8` |
-| r3 | 4 | calibration | arm-class matrix + `--regression` mode + round-gate §13 projection | axis moved (landed) | `SCORECARD.md:17` · `LOG.md:303` · `b58b26f` |
-| r4 | 5 | depth | third kill-rate, cross-author (tsukuroi 6/10, 60 %); incident I1 recorded; six-gate suite/arm census | axis moved (landed) | `SCORECARD.md:18` · `LOG.md:304` · `e0c453e` |
-| r5 | 6 | adjacency + operability | first service engagement (mado 4/10, 40 %): in-surface 4/4 vs out-of-surface 0/6; own-tool meta-hardening | axis moved (landed) | `SCORECARD.md:19` · `LOG.md:305` · `4494715` |
-| r6 | 7 | operability | the leg ledger (4 cases replayed at pinned git blobs); standing ledger + opt-in protocol land | axis moved (landed) | `SCORECARD.md:20` · `LOG.md:306` · `9f1d3c3` |
-| r7 | 8 | coverage | cases 5+6 (47 % · 70 %) → six gates measured; cadence policy + first pin read | axis moved (landed) | `SCORECARD.md:21` · `LOG.md:307` · `c611d5d` |
-| r8 | 9 | operability | first scheduled tick (4 current · 2 stale · 0 drift); the limits note | axis moved (landed) | `SCORECARD.md:22` · `LOG.md:308` · `b8eb96e` |
-| r9 | 10 | operability | the operator runbook; the leg cut resolved (six legs); the boundary note | axis moved (landed) | `SCORECARD.md:23` · `LOG.md:309` · `606716f` |
-| r10 | 11 | operability (terminal) | the close: the pre-announced tick fired; the schedule + the service as it stands; the ten-round record — open items named in the round-11 row above | axis moved (landed) | `SCORECARD.md:24` · `LOG.md:310` · wave-11 landing (this commit) |
-
-Round-11's own commit is the landing that carries this file (no hash exists at
-this write; HEAD `606716f`); the round's receipts ride the record above, and
-its open items are named in the round-11 row — never closed by prose.
-
-## Current axes — fleet round-1 baseline
-
-The historical move log above predates this fleet round. It contains no
-0–10 axis scores; these bounded, reproducible local rubrics establish them
-without retrospectively grading the training arc.
-
-| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
-|---|---|---|---|---|
-| depth | 6 | One point per recorded mutation case listed in the tool's pinned replay ledger, capped at 10. `tools/mutate-and-run.sh:84-89`; command D below. This measures documented case depth, not newly executed cases. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
-| calibration | 0 | Two points per correctly restrained, durable-evidence-linked promotion assertion (`[~]`), capped at 8; the remaining 2 require independent promotion review of all boxes. Baseline has four `[x]` marks attributed to tameshi's own dispatched agents, not independent verifiers. `SHONEN.md:5-34`; command C below. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
-
-Commands, run from this repo with `REV` set to the measured commit:
-
-```sh
-# D: recorded ledger case count = depth score (cap 10).
-git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
-# C: mark census only; this upper bound awards no evidence/authority credit.
-git show "$REV:SHONEN.md" | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~"))+" untouched="+str(m.count(" "))+" asserted_mark_upper_bound="+str(min(8,2*m.count("~"))))'
-```
-
````

## Restoration

Every sandbox was checked out at the original frozen parent after its mutant detector completed. These commands all exited 0 with empty stdout and stderr:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

| Shape | Restored SCORECARD SHA-256 | Exact bytes equal pristine |
|---|---|---|
| A | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` | yes |
| B | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` | yes |
| C | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` | yes |

The pristine hash is `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0`. Restoration was checked using both SHA-256 and direct byte equality. All three restored HEADs are the frozen parent. Details are retained in `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/restoration.json:1-35`.

## Restored A: same bounded detector

Command, executed with cwd `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane` and Git environment variables removed:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/w-restored-A
```

Full stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/receipt-restored-A.stdout:1-13`):

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

Exit code: **1**. Stderr: empty. Elapsed: 246.91 seconds.

## Restored B: same bounded detector

Command, executed with cwd `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B` and Git environment variables removed:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-B --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/w-restored-B
```

Full stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/receipt-restored-B.stdout:1-13`):

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

Exit code: **1**. Stderr: empty. Elapsed: 246.955 seconds.

## Restored C: same bounded detector

Command, executed with cwd `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C` and Git environment variables removed:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/lane-C --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/w-restored-C
```

Full stdout, verbatim (`/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/receipt-restored-C.stdout:1-13`):

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

Exit code: **1**. Stderr: empty. Elapsed: 246.861 seconds.

## Interpretation and limits

Each control changes the parser result from seven stale-value mismatches to twelve `UNPARSED` statements, and breaks the append-only prefix. This is the expected negative-control outcome. It does not establish a mutation kill because the starting detector is already red. There is no surviving false-pass control in this probe.

The initial pristine regression observation was `FAIL,9,8,1`; all mutant and restored regression observations were `PASS,9,9,0`. These are actual differing outputs, not attributed here to a SCORECARD edit. Both observations disagree with the old claimed six-case tuple, so the pristine and restored aggregate mismatch count remains seven. No counter or contract adjustment was made in response.

All seven bounded detector leaders were reaped. The process-group check (`ps -eo pid=,ppid=,pgid=`) found no remaining members of the process groups started by this seat; no kill was needed. Evidence: `/fast/scratch/hyaku/tameshi-r31-seats/CtlRowsDeleted/cleanup.json:1-15`. All detector work directories and all internal regression `--workdir` paths are inside this seat. No tool was installed or updated. No subagent or additional agent runtime was invoked. Production content was not edited; the only write outside this scratch seat is this requested report.

# Smallest safe correction

No counter correction is indicated by these controls. Exact frozen SCORECARD bytes have already been restored in all three sandboxes. A real C1 content repair must retain the base prefix and append correctly typed rows with measured values, rather than deleting or blanking historical rows. The frozen statement set, predicate and target stay unchanged.
