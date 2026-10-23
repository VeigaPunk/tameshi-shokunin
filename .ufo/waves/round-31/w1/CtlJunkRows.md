# CtlJunkRows — pre-data junk-row control

## Verdict

Expected rejection observed: the junk-row commit prints `C1_R31_PASS=false`, with 12 mismatches, no unparsed or unobservable statements, append-only satisfied, and exit 1. There is no unexpected passing-control finding.

Mutation classification: **INCONCLUSIVE, not KILLED**. The pristine frozen revision already fails C1 with seven mismatches, and the byte-restored revision does too. The narrower observed result is that every injected wrong value was parsed as the last statement and rejected; the five previously matching statements became mismatches.

Axis: calibration. Probe axes: value sensitivity, parse fidelity, append-only integrity, and exact byte restoration. No axis improvement or promotion is claimed.

## Mutant and expected detector

- Scope: `/fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane` only; one sandbox commit, `22070aa40e2ad14f49d97c7aa0adf63beef73de9` (`junk`), parent `c111dab58b0a8d55e991bbd2efe3aad56717b95a`.
- Mutation: append one section at `22070aa40e2ad14f49d97c7aa0adf63beef73de9:SCORECARD.md:1482-1502`, containing all ten exact capability identifiers and both axis identifiers under the required table headers. All twelve measurements are deliberately off by one from pristine observed values. No existing SCORECARD bytes or executable files were edited.
- Frozen predicate and kill rule: `.ufo/evidence/round-31/contract.json:12-26`; named negative control: `:28-31`.
- Expected detector: the unchanged counter's command set at `.ufo/evidence/round-31/c1-measure.py:38-64`, last-row selection and claim parsing at `:111-133`, and mismatch/exit decision at `:196-224`. Expected junk result: false, exit 1.

The sandbox was created with:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

The directory creation used Python `os.makedirs(..., exist_ok=True)`; the two Git commands above ran as written, exit 0, no output. All Git and detector subprocesses used this seat or its clone as their working directory; Git environment selectors were unset.

The single commit command ran with exit 0 and no output:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qam junk
```

Observed commit identity, from `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane log -1 --format=%H%n%P%n%s` (exit 0):

```text
22070aa40e2ad14f49d97c7aa0adf63beef73de9
c111dab58b0a8d55e991bbd2efe3aad56717b95a
junk
```

## Full detector outputs

Each command used a distinct, initially absent work directory. The frozen counter ran from the production path but operated only on sandbox clones. All three stderr streams were empty.

### Pristine frozen revision

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/w-pristine
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

Exit code: `1`.

### Junk-row commit

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/w-junk
```

Full stdout, verbatim:

```text
STATEMENT sources-registry: claimed=0,93 observed=0,92 (exit=0) MISMATCH
STATEMENT mutation sweep runner: claimed=107,107,0 observed=106,106,0 (exit=0) MISMATCH
STATEMENT six-leg regression ledger: claimed=PASS,10,10,0 observed=PASS,9,9,0 (exit=0) MISMATCH
STATEMENT repeated pristine-control gate: claimed=PASS,30,0 observed=PASS,29,0 (exit=0) MISMATCH
STATEMENT six-leg content-disposition probe: claimed=20,20,0 observed=19,19,0 (exit=0) MISMATCH
STATEMENT exposed witness provenance correction: claimed=40,40,0 observed=39,39,0 (exit=0) MISMATCH
STATEMENT effective expectation reconciliation: claimed=67,67,0 observed=66,66,0 (exit=0) MISMATCH
STATEMENT retained invocation-context gate: claimed=0,50,50 observed=0,49,49 (exit=0) MISMATCH
STATEMENT hermetic env-differential probe: claimed=10,10 observed=9,9 (exit=0) MISMATCH
STATEMENT callback-authoritative wave accounting: claimed=9,9 observed=8,8 (exit=0) MISMATCH
STATEMENT depth: claimed=8 observed=9 (exit=0) MISMATCH
STATEMENT calibration: claimed=7 observed=8 (exit=0) MISMATCH
C1_R31: statements=12 mismatches=12 unparsed=0 unobservable=0 append_only=1 rev=22070aa40e2ad14f49d97c7aa0adf63beef73de9 C1_R31_PASS=false
```

Exit code: `1`.

### Restored frozen revision

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/w-restored
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

Exit code: `1`.

## Requested commit diff

Executed before restoration, exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane diff HEAD~1 HEAD -- SCORECARD.md
```

The entire raw diff is 30 lines, so this is also the requested first 80 lines; no truncation was needed.

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..004dbcd 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,25 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+## Round 31 — junk-row negative control (sandbox only)
+
+Deliberately incorrect measurements. The original standing rows above remain unchanged.
+
+| Capability | What it can now do | Evidence pointer | First-working round |
+|---|---|---|---|
+| sources-registry | curate opened, tiered, rechecked sources under the census gate | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 93 rows | fleet round 1 (kaika) |
+| mutation sweep runner | inject, run and restore single-edit mutants with a pristine-control gate | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass`, exit 0 | historical round 3 |
+| six-leg regression ledger | replay every recorded mutation case at its pinned blob | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=10 passed=10 …)`, exit 0 | historical round 7 |
+| repeated pristine-control gate | compare repeated raw exit, stdout and stderr tuples | `python3 tools/repeat-control.py --selftest` → PASS (30 cases), exit 0 | round 12 |
+| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations | `python3 tools/pin-disposition.py --selftest` → 20/20 PASS0 | round 13 |
+| exposed witness provenance correction | validate digest-anchored companions without rewriting frozen observations | metadata selftest40/40 PASS0 | round 13 |
+| effective expectation reconciliation | reconcile historical expectations while retaining superseded failures | `python3 tools/evidence-disposition.py --selftest` → PASS67/67 exit0 | round 14 |
+| retained invocation-context gate | re-derive raw receipt predicates with the standalone public CLI | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest50/50 | round 15 |
+| hermetic env-differential probe | distinguish repeat variation from environmental sensitivity | `python3 tools/env-diff.py --selftest` first actual10/10 | round 21 |
+| callback-authoritative wave accounting | reconcile registered identities and terminal states | `python3 tools/wave-accounting.py --selftest`: frozen counter9/9 | round 22 |
+
+| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
+|---|---|---|---|---|
+| depth | 8 | Command D: recorded mutation cases, capped at 10; deliberately wrong by one. | c111dab58b0a8d55e991bbd2efe3aad56717b95a | round 31 sandbox control |
+| calibration | 7 | Frozen calibration command; deliberately wrong by one. | c111dab58b0a8d55e991bbd2efe3aad56717b95a | round 31 sandbox control |
```

## Hashes and exact restoration

Command used in the clone before mutation, after mutation, and after restoration:

```sh
sha256sum SCORECARD.md .ufo/evidence/round-31/c1-measure.py .ufo/evidence/round-31/contract.json
```

All hash commands exited 0. SCORECARD SHA-256 values:

| Phase | SHA-256 |
|---|---|
| Pristine | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` |
| Mutated | `8de3c5cc6b1b33cd4d742fed8f4362d7678067c946d5039a199fe6800137453f` |
| Restored | `518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0` |

The counter and contract hashes were identical in all three clone phases and at the external frozen paths before and after the runs:

```text
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  c1-measure.py
8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79  contract.json
```

Exact external hash command, exit 0 both times:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/contract.json
```

Restoration command, exit 0, no output:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlJunkRows/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

The restored detector output names the frozen commit and reproduces the pristine seven-mismatch result. The junk commit remains identifiable by its full hash; the clone's checked-out files are restored, not left mutated.

Cleanup observation: after all three detector subprocesses returned, inspection of `/proc/<pid>/cwd` found `PROCESSES_WITH_CWD_IN_SEAT=0`. No process needed killing. No tools were installed or updated. No production file was changed other than this assigned report.

## Smallest safe correction

Discard the junk append, as already done by restoring the frozen sandbox revision. Keep the counter, predicate, statement set and target unchanged. This probe supplies no evidence for changing that contract or claiming C1 met.
