Verdict: SURVIVED. Both valid must-kill copies were accepted by the frozen tool. Both valid must-accept copies were correctly accepted. Pristine and restored controls passed for every copy. These are direct detector results, not a full C1 counter measurement.

# HeldOutTallyArms

Seat: HeldOutTallyArms.

Axes: held-out validity; frozen-tool disagreement; small behavior-bearing tally-arm changes; byte-exact restoration.

## Results

Expected detector: each must-kill copy must exit 1 with `TALLY_AUDIT: FAIL`; each must-accept copy must exit 0 with `TALLY_AUDIT: PASS`.

| ID | Set | Validity | Tool exit | Exact TALLY_AUDIT line | Defeats tool |
| --- | --- | --- | --- | --- | --- |
| HeldOutTallyArms-01 | kill | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | Yes: survived |
| HeldOutTallyArms-02 | kill | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | Yes: survived |
| HeldOutTallyArms-03 | accept | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | No: correctly accepted |
| HeldOutTallyArms-04 | accept | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | No: correctly accepted |

All four JSON artifacts are under `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/heldout/`. Their materialized runner copies are `copies/01.sh` through `copies/04.sh` under that same seat directory.

## Evidence

The clone was detached at `a4f718138bdad20de741faeca57891645e5a64d9`. Production source files were not edited. The pinned runner was obtained using this command, with Git environment overrides removed by the probe script:

```sh
git -C /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/c show e24688b2ff6cca1c9ad20e112f02c629b8597ff8:tools/mutate-and-run.sh
```

`probe.py:29-36` captured its stdout as `pinned.sh` and checked its SHA-256. `probe.py:75-82` imported the counter and called `v2.validate(ho, pristine, pinned_path, temporary_directory, [])` for each file. Every call returned the copy text without `v2.Invalid`. The counter's main was never invoked. The validity rules exercised are `.ufo/evidence/round-32/v2/c1-measure-v2.py:206-252`.

The actual bounded batch command, run only in the assigned scratch directory, was:

```sh
timeout 1800 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/probe.py
```

It exited 0. Four independent workers each ran the same bounded audit on pristine, changed and restored bytes, plus the retained held-out copy. The held-out copy commands were:

```sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/copies/01.sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/copies/02.sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/copies/03.sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/copies/04.sh
```

Each command exited 0 and printed:

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=349 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

These were direct tool runs, not sandboxed full-counter runs. Each run used `PATH=/usr/bin:/bin`, `LC_ALL=C`, the seat directory as `HOME`, and a separate `TMPDIR` inside the seat directory. Exact commands, environments, stdout, stderr, return codes and hashes are recorded in `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutTallyArms/probe-evidence.json`:

- `:18-130`: fixture 01, including the copy command at line 59 and witness at lines 99-122.
- `:133-245`: fixture 02, including the copy command at line 174 and witness at lines 214-237.
- `:248-335`: fixture 03, including validity at line 322 and copy output at lines 297-300.
- `:338-425`: fixture 04, including validity at line 412 and copy output at lines 387-390.

### Mutant 01: conditional double increment

The original failure arm is `tools/mutate-and-run.sh:1436`. The copy increments `nfail` a second time when more than one setup result has already been counted.

Observed witness, obtained with the counter's `tally_outputs` instrument:

```text
vector: 2 2 1 0 0 0 0 0 0
pinned:  exit 1; REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)
mutated: exit 1; REGRESSION: FAIL (cases=9 passed=6 failed=2 setup=2)
```

The defect changes the exact reported counts, not the existing failure exit. The runtime panel in `tools/tally-audit.py:221-235` has single-status vectors, selected pairs and uniform all-failure/all-setup vectors; it does not exercise this mixed triple. The count difference was observed; the panel explanation follows directly from its listed vectors.

### Mutant 02: setup counter treated as a flag

The original setup arm is `tools/mutate-and-run.sh:1437`. A new `126|127` pattern list assigns `nsetup=1` instead of incrementing it. A single such status is classified correctly, but two are undercounted.

Observed witness:

```text
vector: 126 127 0 0 0 0 0 0 0
pinned:  exit 2; REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
mutated: exit 2; REGRESSION: SETUP (cases=9 passed=7 cannot-verify=1)
```

The runtime panel sweeps these statuses singly, but its pair status choices at `tools/tally-audit.py:229-233` omit them. This is a counter-update defect, not a T08 status-to-pass reclassification or a generated T08 variant.

### Equivalent copies

Fixture 03 merges the zero and one arms and uses arithmetic predicates to increment only the appropriate counter. Fixture 04 normalizes the case selector to the three tally classes and uses reordered preincrement arms. Both passed the mandatory accept validation, including the sweep, duplicate/drop stresses and harness comparisons with the supplied empty held-out block-witness list. Neither changes the operand multiset. These are not the v1 cosmetic, permutation, guard or harness-variable rewrites.

## Restoration evidence

Every `probes/01.sh` through `probes/04.sh` was restored in a `finally` block (`probe.py:95-105`). For every probe, both the before and restored SHA-256 were:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
```

Every restored byte comparison returned true. Every pristine and restored audit exited 0 with the exact PASS line in the results table. The intentionally retained `copies/*.sh` files contain the submitted fixture bytes, distinct from the restored `probes/*.sh` targets.

| Fixture | Changed/retained copy SHA-256 |
| --- | --- |
| 01 | `f16185281b9e6dbe544707049dd05166de62858351602a0420e50989b65414d1` |
| 02 | `a3ae612ea62941706f9dbc6dff63bba75fcc2fd940ac9d0b9bd2e549123321e9` |
| 03 | `529c4c631905bad091df2ea8dd2dd134345a962693f5c16767087a4ef53ef3f8` |
| 04 | `e87e02a1b8dfc51cabed05273364a92364867812e9569261b895d2fd2361c312` |

The clone's runner remained at the pinned hash above before and after the batch. The tool remained at `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` before and after (`probe-evidence.json:9-14`).

All launched audit subprocesses were waited for; no timeout or forced kill occurred. An earlier asynchronous submission was refused by the shared background job cap before execution; the successful batch was then submitted synchronously. No regression replay, full counter, production gate, subagent, package install or tool update was run.

## Held-out file contents

HELDOUT-FILE HeldOutTallyArms-01
```json
{
  "id": "HeldOutTallyArms-01",
  "author": "HeldOutTallyArms",
  "set": "kill",
  "edits": [
    {
      "old": "      1) nfail=$((nfail + 1)) ;;\n",
      "new": "      1) nfail=$((nfail + 1)); if (( nsetup > 1 )); then nfail=$((nfail + 1)); fi ;;\n"
    }
  ],
  "rationale": "The failure arm increments nfail twice after two setup results, so a mixed three-status vector reports too many failures.",
  "witness": {
    "vector": [2, 2, 1, 0, 0, 0, 0, 0, 0]
  }
}
```

HELDOUT-FILE HeldOutTallyArms-02
```json
{
  "id": "HeldOutTallyArms-02",
  "author": "HeldOutTallyArms",
  "set": "kill",
  "edits": [
    {
      "old": "      *) nsetup=$((nsetup + 1)) ;;\n",
      "new": "      126|127) nsetup=1 ;;\n      *) nsetup=$((nsetup + 1)) ;;\n"
    }
  ],
  "rationale": "The grouped command-invocation error arm treats nsetup as a flag instead of a counter, undercounting two setup results while still classifying either single result correctly.",
  "witness": {
    "vector": [126, 127, 0, 0, 0, 0, 0, 0, 0]
  }
}
```

HELDOUT-FILE HeldOutTallyArms-03
```json
{
  "id": "HeldOutTallyArms-03",
  "author": "HeldOutTallyArms",
  "set": "accept",
  "edits": [
    {
      "old": "      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n",
      "new": "      0|1) npass=$((npass + (st == 0))); nfail=$((nfail + (st == 1))) ;;\n      *) nsetup=$((1 + nsetup)) ;;\n"
    }
  ],
  "rationale": "A shared zero-or-one arm uses arithmetic predicates to increment exactly the original pass or failure counter, while all other statuses still increment the setup counter."
}
```

HELDOUT-FILE HeldOutTallyArms-04
```json
{
  "id": "HeldOutTallyArms-04",
  "author": "HeldOutTallyArms",
  "set": "accept",
  "edits": [
    {
      "old": "    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n",
      "new": "    case $((st == 0 ? 0 : st == 1 ? 1 : 2)) in\n      1) ((++nfail)) ;;\n      0) ((++npass)) ;;\n      2) ((++nsetup)) ;;\n    esac\n"
    }
  ],
  "rationale": "Normalizing each integer exit status to pass, fail or setup and using reordered preincrement arms preserves all tally counts and verdicts."
}
```

## Smallest safe correction

For a future, unfrozen detector revision, add the two observed witness vectors to the runtime panel; they expose the missing mixed-triple and repeated command-invocation-error interactions. Keep the current frozen tool, contract and runner unchanged for this measurement, and retain all four submitted files. The surviving mutants are coverage findings, not permission to relax the predicate.
