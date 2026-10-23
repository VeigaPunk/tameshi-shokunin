# MutateLegSum — routed item 6

**Verdict: the missing completeness guard exists; the mutant SURVIVED the existing `--selftest`.** Removing only `"$st_citecheck"` from the tally list produces `REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)` and exit 0, including when the omitted leg is fixed to FAIL (1) or SETUP (2). Pristine and restored selftests both pass, so this is not an inconclusive baseline. No production change was made.

## Evidence

Axes: **operability** (the assigned axis: runnable, bounded reproduction), with **coverage** as the observed gap (the selftest does not exercise tally completeness). This report does not judge either round-level claim.

All source line references below are at `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`, in my isolated clone `/tmp/tameshi-r29-MutateLegSum.Anwjjq/clone`. The pristine loop has all nine entries; the defect is the absent invariant check, not a claim that the pinned runner already omits a leg.

- `corpus/lessons/round-27-verifier-spotcheck.md:202-203` routes the still-open leg-sum check.
- `tools/mutate-and-run.sh:1424-1431` executes the ninth leg, saves its exit status, declares `nlegs=9`, and separately enumerates statuses for the tally.
- `tools/mutate-and-run.sh:1430-1459` counts the enumerated statuses, rejects observed failures/setup statuses, then prints PASS and exits 0 without checking `npass + nfail + nsetup == nlegs`.
- `tools/mutate-and-run.sh:1936-1945,1957-1958` checks call sites, spec files, declared `nlegs`, and selftest tuples. It does not count the tally loop's status operands. None of those structural counts changes in this mutation.

### Isolation and one mutation

Observed setup commands:

```sh
mktemp -d /tmp/tameshi-r29-MutateLegSum.XXXXXX
# /tmp/tameshi-r29-MutateLegSum.Anwjjq
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r29-MutateLegSum.Anwjjq/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /tmp/tameshi-r29-MutateLegSum.Anwjjq/clone checkout --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
# HEAD is now at 9f3084b round-29: freeze contract and counters (C1 calibration repair, C2 F6) with all widely read input edits (SOURCES S024, README, QUALITY 55-57)
```

Only the following one-line edit was applied to the scratch clone, using the edit tool, and later reversed with the same tool:

```diff
--- a/tools/mutate-and-run.sh
+++ b/tools/mutate-and-run.sh
@@ -1431 +1431 @@
-  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_citecheck"; do
+  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck"; do
```

A byte comparison asserted that this exact replacement was the entire mutation. No regression call, saved status, `nlegs`, spec, or selftest tuple was changed.

### Minimal behavioral harness

The harness extracts the exact block starting at `  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n` and ending immediately before the following function-closing `\n}` (pinned lines 1430–1459). The same extraction and wrapper were used for pristine, mutant, and restored bytes. It never sources or invokes the runner's regression entry point.

The first eight statuses are 0; the ninth is the fixed argument 0, 1, or 2. `auto=0 KEEP=1` prevents deletion; all tally, verdict, and exit statements remain unchanged. The complete mutant harness is:

```bash
#!/usr/bin/env bash
set -u -o pipefail
fixed_statuses() {
  local st_js=0 st_kagi=0 st_tsu=0 st_mado=0 st_checklist=0 st_claims=0 st_roundgate=0 st_sourcescheck=0 st_citecheck=${1:-0}
  local root=fixed-status-harness auto=0 KEEP=1
  local nlegs=9 npass=0 nfail=0 nsetup=0 st
  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck"; do
    case $st in
      0) npass=$((npass + 1)) ;;
      1) nfail=$((nfail + 1)) ;;
      *) nsetup=$((nsetup + 1)) ;;
    esac
  done

  if [[ $nfail -gt 0 ]]; then
    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\n' \
      "$nlegs" "$npass" "$nfail" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 1
  fi
  if [[ $nsetup -gt 0 ]]; then
    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
      "$nlegs" "$npass" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 2
  fi
  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
    "$nlegs" "$npass"
  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then
    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\n' "$root"
    rm -rf "$root"
  else
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
  fi
  exit 0
}
fixed_statuses "$@"
```

The completeness detector should reject nine declared cases with only eight counted statuses. The known-status cases also distinguish a masked FAIL/SETUP from merely incorrect summary text.

Exact executed argv and observed output follow. All ran from `/tmp/tameshi-r29-MutateLegSum.Anwjjq/clone` with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset and `GIT_OPTIONAL_LOCKS=0`. The same detector was regenerated from each byte state; only its artifact filename identifies that state.

```text
$ timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-pristine.sh 0
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: fixed-status-harness (kept)
[exit 0]
$ timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-pristine.sh 1
REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
REGRESSION_WORKDIR: fixed-status-harness (kept)
[exit 1]
$ timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-pristine.sh 2
REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
REGRESSION_WORKDIR: fixed-status-harness (kept)
[exit 2]
$ timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-mutant.sh 0
REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: fixed-status-harness (kept)
[exit 0]
$ timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-mutant.sh 1
REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: fixed-status-harness (kept)
[exit 0]
$ timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-mutant.sh 2
REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: fixed-status-harness (kept)
[exit 0]
$ timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-restored.sh 0
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: fixed-status-harness (kept)
[exit 0]
$ timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-restored.sh 1
REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
REGRESSION_WORKDIR: fixed-status-harness (kept)
[exit 1]
$ timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-restored.sh 2
REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
REGRESSION_WORKDIR: fixed-status-harness (kept)
[exit 2]
```

Thus the behavioral probe exposes the defect; the mutant incorrectly exits 0 for all three inputs. The pristine/restored exits 1 and 2 above are expected fixed-status controls, not failed baselines.

### Existing selftest detector

Expected kill rule: with a green pristine baseline, a nonzero mutant exit would kill this mutant; exit 0 means it survives. The existing leg-count assertions are the candidate detector named in the assignment.

The exact command was run once in each byte state, with the same working directory and environment as above:

```sh
timeout 900 bash tools/mutate-and-run.sh --selftest
```

| Bytes | Exit | Observed duration | Observed final output |
|---|---|---|---|
| pristine | `0` | `5.425 s` | `MUTATE_SELFTEST: 97/97 pass`; `VERDICT: PASS` |
| mutant | `0` | `5.53 s` | `MUTATE_SELFTEST: 97/97 pass`; `VERDICT: PASS` |
| restored | `0` | `5.549 s` | `MUTATE_SELFTEST: 97/97 pass`; `VERDICT: PASS` |

The mutant's existing count checks and final result were:

```text
PASS leg-count agreement: calls=9 specs=9 nlegs=9 (want 9)
PASS leg-count agreement: selftest leg tuples=9 (want 9)
MUTATE_SELFTEST: 97/97 pass
VERDICT: PASS
```

Therefore the existing `--selftest` does **not** catch this omitted tally operand. The regression aggregation itself also accepts it in the extracted behavioral probe. This is bounded to those checks, not a claim about every possible repository check. No full `--regression` replay was run. The selftest's fixture-engine checks and its expected usage refusal for `--regression --target` are part of the requested selftest, not a full ledger replay.

### Restoration and receipts

SHA-256 of `tools/mutate-and-run.sh`:

| Byte state | SHA-256 |
|---|---|
| Pristine, before probes | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| Mutant | `ab14287950fa9bb0a0fee4e0960855f53b773453b0bc6fbe866e0deb1ca71461` |
| Restored, before probes | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| Restored, after probes | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |

Observed: `restored_byte_identical_to_pristine=True` and `exact_restoration=True`. The restored harness's output and exit codes match the pristine harness for all three statuses, and the restored selftest passes.

Scratch receipts: `/tmp/tameshi-r29-MutateLegSum.Anwjjq/{pristine,mutant,restored}-{selftest,tally-0,tally-1,tally-2}.json` contain exact argv, cwd, exit, elapsed time, stdout, stderr, and outer-timeout state. `/tmp/tameshi-r29-MutateLegSum.Anwjjq/restoration.json` records the hashes and byte-equality result; the three extracted harnesses and the pristine byte backup remain in that scratch directory. The essential outputs and full mutant harness are embedded above so the report does not depend on scratch retention.

All 12 detector processes completed without an outer timeout and with empty stderr. Each subprocess was started in its own process group, waited for, and its group was sent SIGKILL in a `finally` block (ignoring an already-gone group), so no detector process tree was left running. An initial asynchronous tool dispatch was refused by the shared 100-job limit before running a detector; the recorded executions above used bounded direct subprocesses instead. No tools were installed or updated. No Git write command ran in the lane or fleet repository; no `jj` command ran anywhere.

## Smallest safe correction — proposal only, never applied

Insert a completeness refusal immediately before the PASS path. This retains the existing FAIL-before-SETUP priority and retained-workdir diagnostics. [INFERENCE] For this mutant, the sum is 8 rather than 9, so the proposed guard would refuse with exit 2 instead of false PASS. The proposal was neither applied nor tested.

```diff
--- a/tools/mutate-and-run.sh
+++ b/tools/mutate-and-run.sh
@@ -1448,6 +1448,12 @@ run_regression() {
     printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
     exit 2
   fi
+  if (( npass + nfail + nsetup != nlegs )); then
+    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
+      "$nlegs" "$((npass + nfail + nsetup))"
+    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
+    exit 2
+  fi
   printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
     "$nlegs" "$npass"
   if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then
```
