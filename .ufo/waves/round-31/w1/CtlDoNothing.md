Verdict: the do-nothing control is rejected. At frozen revision `c111dab58b0a8d55e991bbd2efe3aad56717b95a`, C1 reports seven mismatches, `C1_R31_PASS=false`, exit 1.

## Scope and expected detector

- Measured axis: calibration. Preservation constraint: leave SCORECARD and the frozen detector inputs unchanged.
- Control: do nothing. No mutation, new commit, or SCORECARD edit was made. This is a negative control, not a killed mutant; a failing baseline would be inconclusive as a mutation test.
- Expected detector: the frozen counter rejects unchanged stale statements through its mismatch rule (`.ufo/evidence/round-31/c1-measure.py:196-224`). Contract: `.ufo/evidence/round-31/contract.json:14-26,28-36`.
- Frozen standing rows: `SCORECARD.md:64-67,238-249` in the isolated clone at the revision above. The counter selects the last row of each matching table type (`c1-measure.py:111-133`).

## Commands and observed output

Working directory for all shell commands: `/fast/scratch/hyaku/tameshi-r31-seats/CtlDoNothing`, or its `lane` clone as noted. No production Git write command was run.

Setup, from the seat directory:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r31-seats/CtlDoNothing && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlDoNothing/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlDoNothing/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

Observed: no stdout; exit 0. Before cloning, `df -h /fast` reported 178G available.

Detector, from the isolated `lane` directory:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlDoNothing/lane --rev c111dab58b0a8d55e991bbd2efe3aad56717b95a --work /fast/scratch/hyaku/tameshi-r31-seats/CtlDoNothing/w-nothing
```

Full observed stdout:

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

Observed exit: **1**. Wall time: 312.89 seconds; the command completed rather than timing out. Receipt: `/fast/scratch/hyaku/tameshi-r31-seats/CtlDoNothing/c1-nothing.stdout:1-13`; exit receipt: `c1-nothing.exit:1` in the same directory. The regression invocation is the counter's frozen invocation with its work directory under this seat (`c1-measure.py:43-45,136-142`).

An earlier asynchronous launch request returned `Background job limit reached (100). Wait for running jobs to finish or cancel one.` It produced no detector result. The identical command above then completed once; no detector rerun or mutation was performed.

## Byte preservation and restoration evidence

The following command ran from the isolated `lane` directory both before and after the detector:

```sh
sha256sum SCORECARD.md .ufo/evidence/round-31/c1-measure.py .ufo/evidence/round-31/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/contract.json && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD
```

Both observed outputs were identical:

```text
518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0  SCORECARD.md
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  .ufo/evidence/round-31/c1-measure.py
8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79  .ufo/evidence/round-31/contract.json
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py
8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/contract.json
c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

Both hash commands exited 0. Saved hash receipts: `/fast/scratch/hyaku/tameshi-r31-seats/CtlDoNothing/before.sha256:1-5` and `after.sha256:1-5` in the same directory. Restoration was unnecessary: no bytes were mutated, and the assigned surface, counter, contract and clone HEAD remained unchanged. No additional pristine/mutated/restored detector runs were made because this assignment explicitly requires the do-nothing control only.

## Smallest safe correction

The assigned do-nothing round cannot meet the target: unchanged SCORECARD and unchanged measured state retain seven mismatches, rather than the required zero. This result concerns the tested do-nothing revision; it does not test a different revision that changes command outputs while leaving SCORECARD untouched.

The smallest safe content correction is an append-only, visible correction of the mismatching rows under the frozen table headers, using actual observations, followed by measurement at the landed revision. Preserve the complete base prefix; do not change the frozen counter, predicate or target. No correction was applied by this seat.

Tool installations or updates: none.
