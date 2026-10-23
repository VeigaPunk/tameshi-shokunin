Verdict: both valid must-kill copies survived; both valid must-accept copies were falsely rejected. All four defeat the frozen tool in the assigned direct audits. Every pristine and restored control passed. This is a held-out probe result, not the full C1 measurement.

# HeldOutLoop — sealed held-out author

Axes: **operability** (valid runnable copies and bounded detectors), **coverage** (late-leg status corruption, untested leg interactions, nested loop selection), **calibration** (separate validity, audit output, and the unrun full counter).

Scratch root: `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop`. Paths beginning `c/`, `heldout/`, `copies/`, `evidence/`, or `probe.py` below are relative to that root. Clone revision: `a4f718138bdad20de741faeca57891645e5a64d9`.

## Per-file result

| id | set | validity | tool exit and TALLY_AUDIT line | defeats tool | verdict |
|---|---|---|---|---|---|
| HeldOutLoop-1 | kill | valid | 0; `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes | survived |
| HeldOutLoop-2 | kill | valid | 0; `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes | survived |
| HeldOutLoop-3 | accept | valid | 1; `TALLY_AUDIT: FAIL (static=fail runtime=fail harness=pass)` | yes | false rejection |
| HeldOutLoop-4 | accept | valid | 1; `TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)` | yes | false rejection |

Expected detector: must-kill copies must exit 1 with `TALLY_AUDIT: FAIL`; must-accept copies must exit 0 with `TALLY_AUDIT: PASS`. No baseline failed, so none of these outcomes is inconclusive.

## Evidence and commands

The counter fixes the tally start anchor and extracts pre-tally captures at `c/.ufo/evidence/round-32/v2/c1-measure-v2.py:70-105`; its validity rules are implemented at lines 206-252. Every file was passed to `v2.validate(ho, pristine, pinned_path, tempfile.mkdtemp(...), [])`, which returned its copy text without raising `Invalid` (`probe.py:40-53`). This includes `bash -n`, the required kill witnesses, and the accept sweep, duplicate/drop stresses, and reference/fault harness verdicts. The empty block-witness list is exactly the assigned local validation call; the integrated held-out panel was not run here.

Pinned bytes were extracted using the following Git argv, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed from the subprocess environment; stdout was saved as `pinned.sh`:

```sh
git -C /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/c show e24688b2ff6cca1c9ad20e112f02c629b8597ff8:tools/mutate-and-run.sh
```

The bounded probe was executed once, with four independent files processed concurrently:

```sh
timeout 1200 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/probe.py
```

It completed with exit 0. The script imports the counter only to call validation and its instrumentation; it never invokes the counter main. Tool runs set `TMPDIR` inside this scratch root. Each changed-copy command below was actually run; all stderr captures were empty.

### HeldOutLoop-1

```sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/copies/1.sh
```

Observed exit: `0`. Exact stdout (`evidence/HeldOutLoop-1-mutated.stdout:1-4`):

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=349 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

Witness vector: `[0, 128, 0, 0, 0, 0, 0, 0, 0]`.

- Pinned: exit `2`, `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)`.

- Changed: exit `0`, `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`.

The inserted seven-bit mask is immediately after the fixed `local nlegs=9` anchor (`heldout/HeldOutLoop-1.json:7-8`). Status 128 at kagi becomes zero. The auditor exhausts statuses only at its first leg, and its sampled late-leg statuses do not expose this mask (`c/tools/tally-audit.py:218-235`). The nine original `st_*=$?` captures remain unchanged.

### HeldOutLoop-2

```sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/copies/2.sh
```

Observed exit: `0`. Exact stdout (`evidence/HeldOutLoop-2-mutated.stdout:1-4`):

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=349 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

Witness vector: `[0, 0, 0, 1, 0, 0, 1, 0, 0]`.

- Pinned: exit `1`, `REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)`.

- Changed: exit `1`, `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)`.

The inserted conditional assignment overwrites a second failing leg only on the mado error path (`heldout/HeldOutLoop-2.json:7-8`). The auditor tests mixed pairs only at positions (0, 8) and (4, 5), not (3, 6); its all-one and all-two vectors preserve the overwritten value (`c/tools/tally-audit.py:229-235`). This is a status-flow defect, not a duplicated or dropped loop operand.

### HeldOutLoop-3

```sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/copies/3.sh
```

Observed exit: `1`. Exact stdout (`evidence/HeldOutLoop-3-mutated.stdout:1-4`):

```text
CHECK static FAIL legs=9 operands=1 nlegs=9; loop operands != legs (missing ['st_checklist', 'st_citecheck', 'st_claims', 'st_kagi', 'st_mado', 'st_roundgate', 'st_sourcescheck', 'st_tsu']; miscounted -)
CHECK runtime FAIL vectors=333 mismatched=332; first: statuses 0 0 0 0 0 0 0 0 0: got (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)'), want (2, 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=1)')
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: FAIL (static=fail runtime=fail harness=pass)
```

The original `  for st in ...; do` line and all operands are retained. A single-operand outer loop executes it exactly once (`heldout/HeldOutLoop-3.json:7-8`). The auditor selects the first loop over status operands regardless of iterator variable (`c/tools/tally-audit.py:129-142`), and therefore mistakes the wrapper for the counting loop.

### HeldOutLoop-4

```sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/copies/4.sh
```

Observed exit: `1`. Exact stdout (`evidence/HeldOutLoop-4-mutated.stdout:1-4`):

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime FAIL vectors=349 mismatched=18; first: stress dup operand 0: got (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)'), want (2, 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=10)')
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)
```

The original inner counting loop is retained. A nine-operand outer loop breaks after its first iteration (`heldout/HeldOutLoop-4.json:7-8`), so all real counts are unchanged. Static presence passes, but `with_operands()` changes the wrapper rather than the counting loop (`c/tools/tally-audit.py:149-151,242-251`); all 18 generated stresses then report false mismatches. This isolates a stress-targeting error from the static false rejection in copy 3.

These shapes do not edit case arms, guards, harness comparisons, harness positions or vectors, and do not duplicate, drop, reverse, or permute the real tally operand list. They are not the excluded v1 fixtures or their generated variants.

## Pristine and restoration evidence

`probe.py:65-76` writes pristine bytes, runs the same bounded auditor, stages the changed bytes, and restores exact pristine bytes in `finally` before running the auditor again. The changed audit uses the required retained `copies/<k>.sh` file; its bytes equal the staged changed probe bytes. Every pristine and restored run exited 0 and printed exactly:

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=349 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

The exact pristine/restored command for each k in 1, 2, 3, 4 was:

```sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/copies/probe-<k>.sh
```

Per-file stdout is retained as `evidence/HeldOutLoop-<k>-pristine.stdout:1-4` and `evidence/HeldOutLoop-<k>-restored.stdout:1-4`; all stderr files are empty. Full command arrays, witness outputs, exit codes, and byte-equality results are in `evidence/results.json` and each `evidence/HeldOutLoop-<k>-result.json`.

Pinned/before SHA-256: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`.

Frozen tool SHA-256: `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef`.

| id | changed copy SHA-256 | restored SHA-256 | exact restoration |
|---|---|---|---|
| HeldOutLoop-1 | `f9e0ac08a3da7242942b2433049f53975d9af80bf86aaaad52961720c02798c9` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | true |
| HeldOutLoop-2 | `51085f3a4e1a8ad9c37c9965c87be8047aa1b659e30b681cc58f0ebf2e305b2f` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | true |
| HeldOutLoop-3 | `d0ba0a89bbf44eabfe84dcbbffee5d63372af1e2db987eae762d0f41f15f87e5` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | true |
| HeldOutLoop-4 | `7be273bff723119c7d081cb646a4ba23a1abe754c3934044f7629ac0b9c22e6a` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | true |

The four `copies/probe-<k>.sh` files were restored. The four requested changed fixture copies and held-out JSON files are intentionally retained. No production file was edited, no full counter or regression was run, no Git write command was issued outside the isolated clone, and no runtime was invoked other than the assigned Python/Bash audit machinery. All bounded subprocess calls returned; no persistent service was started and no process was killed manually. Tool installs or updates: none.

## Sealed files

The following blocks are the exact contents of the corresponding files under `heldout/`.

HELDOUT-FILE HeldOutLoop-1
```json
{
  "id": "HeldOutLoop-1",
  "author": "HeldOutLoop",
  "set": "kill",
  "edits": [
    {
      "old": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n",
      "new": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  st_kagi=$((st_kagi & 127))\n"
    }
  ],
  "rationale": "Masking the kagi status to seven bits converts status 128 into success and loses a real setup result.",
  "witness": {
    "vector": [
      0,
      128,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ]
  }
}
```

HELDOUT-FILE HeldOutLoop-2
```json
{
  "id": "HeldOutLoop-2",
  "author": "HeldOutLoop",
  "set": "kill",
  "edits": [
    {
      "old": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n",
      "new": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  if (( st_mado != 0 )); then st_roundgate=$st_sourcescheck; fi\n"
    }
  ],
  "rationale": "An error-path copy and paste overwrites the round-gate status from sources-check after the mado leg fails, losing a second failing leg.",
  "witness": {
    "vector": [
      0,
      0,
      0,
      1,
      0,
      0,
      1,
      0,
      0
    ]
  }
}
```

HELDOUT-FILE HeldOutLoop-3
```json
{
  "id": "HeldOutLoop-3",
  "author": "HeldOutLoop",
  "set": "accept",
  "edits": [
    {
      "old": "  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n",
      "new": "  local tally_once\n  for tally_once in \"$st_js\"; do\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n  done\n"
    }
  ],
  "rationale": "A one-operand outer loop executes the unchanged tally loop exactly once for every status vector and does not change the tally or harness contract."
}
```

HELDOUT-FILE HeldOutLoop-4
```json
{
  "id": "HeldOutLoop-4",
  "author": "HeldOutLoop",
  "set": "accept",
  "edits": [
    {
      "old": "  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n",
      "new": "  local tally_once\n  for tally_once in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n    break\n  done\n"
    }
  ],
  "rationale": "An outer status loop with an unconditional break executes the unchanged tally loop once, preserving every tally output and harness verdict."
}
```

## Smallest safe correction

Do not change the frozen tool or exclude these valid copies during this measurement. For a separately authorized future revision: sweep all 256 statuses at every leg to catch copy 1; add the missing cross-leg error-path pairs to catch copy 2; and identify the actual loop that increments the tally counters, then use that same loop for static comparison and stress replacement, rather than taking the first status-operand loop, to avoid copies 3 and 4. No correction was applied in this seat.
