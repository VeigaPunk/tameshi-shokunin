# CtlLabelShortcut — round 31, wave 1

## Verdict

- **Old-value label shortcut: rejected as expected.** The counter returned `C1_R31_PASS=false`, seven mismatches, exit 1. This is **inconclusive as a mutation kill**, not a killed mutant: pristine bytes already returned the same failure.
- **Static contract-linked receipt shortcut: accepted.** It returned `C1_R31_PASS=true`, zero mismatches, exit 0. This survives an expectation that every no-execution shortcut must fail, but does **not** violate frozen C1. Every copied value equals the observed value and the original file remains a prefix. The contract explicitly discloses this route control at `contract.json:36`.
- Axis: **calibration**. This probe distinguishes stale assertions from value agreement; it does not establish how the appended values were obtained. No round admission or wider-axis conclusion is made here.

## Evidence

### Scope and frozen inputs

All explicitly selected working directories, mutations and evidence files were under `/fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/`; the only write in the production lane is this report. Frozen selftests retain their own internal temporary-directory behavior (for example, `tools/repeat-control.py:597` explicitly uses `/tmp`); those implementations were not changed. No production Git write command, `jj`, sibling modification, model invocation, subagent dispatch, or tool installation was used.

Both clones start at `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. The frozen counter and contract were read before either payload was constructed. Payloads were sealed in `sealed-inputs.json` before the first detector invocation. Baseline commands began only after those static payloads had been selected; their output was not used to choose row values.

Frozen input SHA-256, observed before the probe and after byte restoration:

```text
c1-measure.py  657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584
contract.json  8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79
```

Relevant frozen source locations under `.ufo/evidence/round-31/`:

- `c1-measure.py:38-64`: the 12 statement ids, command bindings and row patterns.
- `c1-measure.py:111-133`: the last matching table row supplies each claim.
- `c1-measure.py:136-166`: commands supply the observed tuple.
- `c1-measure.py:196-224`: prefix, equality, final label and exit logic.
- `contract.json:14-26`: frozen outcome predicate and target.
- `contract.json:28-36`: old-value and committed-receipt controls.
- `contract.json:46-47`: static calibration and depth values used by shape 2.
- `before/c1-at-base.stdout:1-12`: the pre-existing committed tuples used by shape 2, linked by `contract.json:21`. Reading this file was not a new capability-command execution.

The counter source does not contain literal expected tuples for all capabilities; shape 2 therefore uses the contract-linked committed receipt, within the requested “anything a reader can get without running a command” route. This is explicitly not a source-only reconstruction of those capability counts.

### Setup and sandbox commits

The seat directory was created with `Path.mkdir(parents=True, exist_ok=True)`. `df -h /fast` then reported 804G total, 627G used, 177G available (79%), exit 0, before cloning.

For each sandbox, the following Git argv were prefixed with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`. Clone and checkout produced no stdout:

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane
git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source
git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

Exactly one control commit was made in each clone; both have the frozen commit as their parent:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam labels
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source -c user.name=ctl -c user.email=ctl@sandbox commit -qam static-contract
```

Both commits produced no stdout. Observed commit identities:

```text
labels  6754dd2d149d608e968045e6a648ec8cf816a258
source  1494177cc7a2731942f21d0f9c2240ec4a1af172
parent  c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

### Mutants and expected detector

1. **Labels:** append the exact existing capability rows from `SCORECARD.md:240-249` and the exact existing axis rows from `SCORECARD.md:66-67`, under identical table headers. These are appended at the labels commit's `SCORECARD.md:1482-1500`. No row value was recomputed. Expected control result: `C1_R31_PASS=false`, because copying a stale claim does not repair equality.
2. **Static contract route:** append syntactically matching rows at the source commit's `SCORECARD.md:1482-1502`, using only the contract-linked pre-existing baseline receipt for capability values and the contract's no-harm fields for axis values. Expected generic shortcut rejection: false. Expected under the actual frozen outcome predicate when these copied values remain current: true. No capability command was run to select this payload.

### Detector commands and complete stdout

Each command ran from the indicated scratch clone, with inherited `GIT_*` variables removed, `PYTHONDONTWRITEBYTECODE=1`, and `TMPDIR=/fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/tmp`. Every `--work` was absent before its run. The frozen detector itself supplied the regression `--workdir` beneath that run's scratch root. All six runs used the same unchanged detector and a 2700-second external bound.

#### pristine-labels

Cwd: `/fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane`.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/w-pristine-labels
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

Exit code: **1**. Stderr: empty. Elapsed: 305.239 seconds.

#### pristine-source

Cwd: `/fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source`.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/w-pristine-source
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

Exit code: **1**. Stderr: empty. Elapsed: 304.898 seconds.

#### labels

Cwd: `/fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane`.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/w-labels
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
C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=6754dd2d149d608e968045e6a648ec8cf816a258 C1_R31_PASS=false
```

Exit code: **1**. Stderr: empty. Elapsed: 195.023 seconds.

#### source

Cwd: `/fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source`.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/w-source
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
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=1494177cc7a2731942f21d0f9c2240ec4a1af172 C1_R31_PASS=true
```

Exit code: **0**. Stderr: empty. Elapsed: 195.001 seconds.

#### restored-labels

Cwd: `/fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane`.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/w-restored-labels
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

Exit code: **1**. Stderr: empty. Elapsed: 251.423 seconds.

#### restored-source

Cwd: `/fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source`.

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/w-restored-source
```

Full stdout, verbatim:

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

Exit code: **1**. Stderr: empty. Elapsed: 251.147 seconds.

### Observed restored-run variance

Restored source bytes were exact, but that run's regression observation was `FAIL,9,8,1`, whereas its pristine run observed `PASS,9,9,0`. The overall C1 result remained false with seven mismatches. This is an observed variation in one frozen command, not evidence that byte restoration failed. It was not rerun or suppressed, and this report does not generalize the single accepted static-route run to all executions.

Evidence: `/fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/w-restored-source/obs-six-leg-regression-ledger.stdout:17-20,51`:

```text
REGRESSION_DEFECT bash-tsukuroi-census B7: measured=KILLED recorded=SURVIVED
REGRESSION_TABLE bash-tsukuroi-census: match=9/10 recorded-killed=6 measured-killed=7 survived=3 inconclusive=0 flips=1
REGRESSION_WORKDIR bash-tsukuroi-census: /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/w-restored-source/regression-wd/bash-tsukuroi-census
REGRESSION_CASE bash-tsukuroi-census: FAIL (out of band: killed-delta=1 flips=1; log: /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/w-restored-source/regression-wd/bash-tsukuroi-census/sweep.log)
REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
```

### Requested SCORECARD diff excerpts

The requested `git -C <clone> diff HEAD~1 HEAD -- SCORECARD.md | head -80` excerpts follow. The Git commands were executed through `subprocess.run`; Python selected their first 80 lines without a paging subprocess. Each complete diff is shorter than 80 lines, so no diff content is omitted.

#### labels (28 lines)

```sh
git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane diff HEAD~1 HEAD -- SCORECARD.md
```

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..08f6e75 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,23 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+## Round 31 label shortcut control
+
+| Capability | What it can now do | Evidence pointer | First-working round |
+|---|---|---|---|
+| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 44 rows, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; `corpus/SOURCES.md` | fleet round 1 (kaika) |
+| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 80/80 pass`, exit 0 (`.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout`) | historical round 3 (`SCORECARD.md:16`); re-demonstrated fleet round 1 |
+| six-leg regression ledger | replay every recorded mutation case at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=6 passed=6 …)`, exit 0 (`…/capability-demo/h1b-regression.stdout`) | historical round 7 (four legs) / round 10 (six); re-demonstrated fleet round 1 |
+| repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0; real bash controls match; red-before loop mutant fails the same mismatch oracle, restored loop passes; `.ufo/evidence/round-12/verification-final.json`, `oracle-repair.json`; measured `9df9212d33dc2dbda133e88f28ad47bb08839a5b` | round 12; lane demonstrated, outside admission pending |
+| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → 18/18 PASS0; real read changed3/unchanged3/unavailable0; `.ufo/evidence/round-13/verification.json`, `pin-dispositions.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
+| exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations; prevent wrong-nesting in future producer output | metadata selftest39/39 PASS0; null-only companion FAIL1/corrected PASS0; producer same-oracle40/41 FAIL1→41/41 PASS0; `.ufo/evidence/round-13/producer-oracle-repair.json`, `verification-verdict.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
+| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → PASS34/34 exit0; same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded; `.ufo/evidence/round-14/verification-final.json`, S050; executable measurement6431478 | round14; lane demonstrated, separate outside admission pending |
+| retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49, registered frozen0, missing-env1, tamper2, usage64; `.ufo/evidence/round-15/verification-3.json`; S051 | round15; lane demonstrated, separate non-author admission pending |
+| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles, separating repeat variation from environmental sensitivity | `python3 tools/env-diff.py --selftest` first actual9/9; real receipt `f5/receipt-initial.json` under `.ufo/evidence/round-21/` classifies9/9 (eight invariant, one raw-output-variable); `corpus/knowledge/hermetic-env-differential.md`, S079/S081 | round21; lane demonstrated, separate non-author admission pending |
+| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | at11f55d64968778aaed07b001fc8b2480c38e1896: frozen counter8/8, actual146-seat replay66 completed/80 failed, wrong-count1/TOTAL_MISMATCH; `.ufo/evidence/round-22/final/verification.json`, S082 | round22; lane demonstrated, separate non-author admission pending |
+
+| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
+|---|---|---|---|---|
+| depth | 6 | One point per recorded mutation case listed in the tool's pinned replay ledger, capped at 10. `tools/mutate-and-run.sh:84-89`; command D below. This measures documented case depth, not newly executed cases. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
+| calibration | 0 | Two points per correctly restrained, durable-evidence-linked promotion assertion (`[~]`), capped at 8; the remaining 2 require independent promotion review of all boxes. Baseline has four `[x]` marks attributed to tameshi's own dispatched agents, not independent verifiers. `SHONEN.md:5-34`; command C below. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
```

#### source (30 lines)

```sh
git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlLabelShortcut/lane-source diff HEAD~1 HEAD -- SCORECARD.md
```

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..22b7767 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,25 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+## Round 31 static contract shortcut control
+
+Values copied only from the frozen contract and its committed baseline receipt; no capability command was executed to construct these rows.
+
+| Capability | What it can now do | Evidence pointer | First-working round |
+|---|---|---|---|
+| sources-registry | Static contract shortcut | exit 0, 92 rows | control |
+| mutation sweep runner | Static contract shortcut | `MUTATE_SELFTEST: 106/106 pass`, exit 0 | control |
+| six-leg regression ledger | Static contract shortcut | `REGRESSION: PASS (cases=9 passed=9)`, exit 0 | control |
+| repeated pristine-control gate | Static contract shortcut | PASS (29 cases), exit 0 | control |
+| six-leg content-disposition probe | Static contract shortcut | `--selftest` → 19/19 PASS0 | control |
+| exposed witness provenance correction | Static contract shortcut | metadata selftest39/39 PASS0 | control |
+| effective expectation reconciliation | Static contract shortcut | PASS66/66 exit0 | control |
+| retained invocation-context gate | Static contract shortcut | → exit0, copied-source CLI selftest49/49 | control |
+| hermetic env-differential probe | Static contract shortcut | actual9/9 | control |
+| callback-authoritative wave accounting | Static contract shortcut | frozen counter8/8 | control |
+
+| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
+|---|---|---|---|---|
+| depth | 9 | Frozen contract no_harm.depth | frozen contract | control |
+| calibration | 8 | Frozen contract no_harm.calibration_monitor | frozen contract | control |
```

### Restoration and byte identity

After the mutated runs completed, the appended lines alone were removed with two surgical edits: labels `SCORECARD.md:1481-1500` and source `SCORECARD.md:1481-1502`. Neither sandbox history was rewritten and no second commit was made. Each mutant commit remains at sandbox `HEAD` for inspection; the restored worktree deliberately differs from its mutant HEAD.

Restored detector runs use `--rev c111dab58b0a8d55e991bbd2efe3aad56717b95a`: that committed revision has exactly the restored bytes. The counter reads committed revisions, not an uncommitted restoration, so this avoids falsely presenting mutant HEAD as restored.

Observed SHA-256 values from `sha256sum`:

```text
pristine SCORECARD (both clones)  518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0
labels mutant                    19d3e95fb771d0d5908bf43585d624c9ca0d39f1ae04f9ba22d0cc5dced48daf
source mutant                    a40b0b27c2ff5a64fd9171ffbf8f9c1d06b4db344d29fd3f8c27645857528aed
saved pristine-SCORECARD.md       518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0
labels restored                  518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0
source restored                  518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0
```

Scratch evidence is retained under the seat root: `sealed-inputs.json`, `controls.json`, `restoration-hashes.json`, `pristine-SCORECARD.md`, both append payloads, both diffs and first-80-line excerpts, and one `.stdout`, `.stderr`, and `.json` per detector invocation. This report embeds every detector stdout and both complete diffs rather than relying only on scratch paths.

### Process cleanup

All six managed detector processes returned. A final `/proc/<pid>/cwd` census found no remaining process with a working directory inside the assigned seat; the managed-process registry was also empty. No process was killed. Evidence: `process-cleanup.json` under the seat root.

## Smallest safe correction

Do not change the frozen counter, predicate or target. Keep the finding scoped to outcome equality plus prefix preservation. For the real lane repair, append current values under the frozen headers and measure the final delivered revision; copying old claims does not do this. A correct static-data route already meets the frozen property, as disclosed at `contract.json:36`, and its acceptance must not be recast as evidence that the row-writing process ran those commands.

No production correction was made by this probe. Tool installs or updates: none.
