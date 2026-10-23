# CriticTool — round 33, wave 1

## Verdict

**Round-blocking findings:** the frozen v2 audit accepts a runner copy that masks failing/setup exits after a nested tally function, and refuses three correct tally refactors: a renamed loop variable, a `while` traversal, and an `until` traversal. The indirection and stale-printf candidates are caught.

Impacted axis: **operability**, specifically audit soundness and acceptance of equivalent runnable copies. These are fixable implementation defects, not a tradeoff that can be cured by treating SETUP as a successful rejection. This is a development review finding, not a C1 counter result or an admission judgment.

## Evidence

All command working directories were `/fast/scratch/hyaku/tameshi-r33-seats/CriticTool`. Below, `scratch/` means that absolute directory; lane-relative paths refer to `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

### Frozen inputs and receipt discipline

The copied tool and pristine runner have exactly the contract pins (`.ufo/evidence/round-33/contract.json:7-10`). Command:

```sh
sha256sum tally-audit-v2.py pristine.sh > pins.stdout 2> pins.stderr; echo $? > pins.exit
```

Observed (`scratch/pins.stdout:1-2`, `scratch/pins.exit:1`, exit 0):

```text
9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tally-audit-v2.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

Each candidate was a separate copy of that runner, changed only in this seat's scratch. `scratch/<candidate>.patch` contains its complete `diff -u pristine.sh <candidate>.sh`; each diff's exit 1 is recorded in `<candidate>.diff.exit` and means the files differ, not an execution failure. Candidate hashes are recorded in `scratch/candidate-pins.stdout:1-8` with exit 0 in `candidate-pins.exit:1`.

### Concrete sweep and commands

The exact per-copy command, run concurrently for the seven names below by `scratch/run-audits.sh:4-12`, was:

```sh
timeout -k 5s 180s python3 tally-audit-v2.py --runner "$name.sh" >"$name.audit.stdout" 2>"$name.audit.stderr"; echo $? >"$name.audit.exit"
```

The driver set `HOME="$PWD" TMPDIR="$PWD/tmp" LC_ALL=C PYTHONDONTWRITEBYTECODE=1`. Its invocation was:

```sh
timeout -k 5s 240s bash run-audits.sh > sweep.stdout 2> sweep.stderr; echo $? > sweep.exit
```

The driver exited 0; the decisive statuses are the separately captured per-copy exits, not that driver status.

| Runner copy | Intended behavior | Observed exit and final stdout line | Evidence |
|---|---|---|---|
| `pristine` | Accept | 0, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `scratch/sweep.stdout:13-18`; `pristine.audit.exit:1` |
| `boundary-tail` | Flag status masking | 0, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `scratch/sweep.stdout:19-24`; `boundary-tail.audit.exit:1` |
| `variable-name` | Accept equivalent rename | 2, `TALLY_AUDIT: SETUP (counting \`case $st in\` not found)` | `scratch/sweep.stdout:3-4`; `variable-name.audit.exit:1` |
| `while-loop` | Accept equivalent traversal | 2, `TALLY_AUDIT: SETUP (no loop governing the counting case)` | `scratch/sweep.stdout:1-2`; `while-loop.audit.exit:1` |
| `until-loop` | Accept equivalent traversal | 2, `TALLY_AUDIT: SETUP (no loop governing the counting case)` | `scratch/sweep.stdout:5-6`; `until-loop.audit.exit:1` |
| `indirect-duplicate` | Flag duplicated leg via nameref | 1, `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | `scratch/sweep.stdout:7-12`; `indirect-duplicate.audit.exit:1` |
| `stale-printf` | Flag stale printed count | 1, `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | `scratch/sweep.stdout:25-30`; `stale-printf.audit.exit:1` |

### Finding 1: a closing brace hides executable status masking

Exact additions to pristine (`scratch/boundary-tail.patch:3-17`): insert `  tally_result() {` immediately before `local nlegs=9 ... st`; retain the existing tally through its existing `exit 0` and column-zero `}`; then append these lines before the selftest section:

```bash
  (tally_result)
  exit 0
}
```

Thus the original closing brace now closes the nested tally function, not `run_regression`. The complete outer function invokes that function in a subshell, then incorrectly exits 0 regardless of its result. The tally's status variables remain dynamically scoped from the outer function.

Root cause: `tools/tally-audit-v2.py:117-124` ends `run_regression` at the first literal `\n}\n`, without matching shell nesting. `:130-134` slices the tally from that truncated body. It therefore never tests the actual outer call or its unconditional exit. All four checks still print PASS, including `vectors=2395 mismatched=0` (`scratch/sweep.stdout:20-24`).

Independent witness command:

```sh
timeout -k 5s 240s python3 check-semantics.py > semantics.stdout 2> semantics.stderr; echo $? > semantics.exit
```

Observed exit 0 (`scratch/semantics.exit:1`). The probe sourced the copied runner's complete definitions before its main dispatch and executed the complete `run_regression` function. Only external ledger execution and spec generation were replaced with a fixed-status fixture; no real fleet regression result is claimed. Each generated Bash probe was itself run using `timeout -k 5s 120s bash <probe> > <label>.stdout 2> <label>.stderr; echo $? > <label>.exit`.

Observed (`scratch/semantics.stdout:9-14`):

```text
FULL_FUNCTION pristine all-pass exit=0 want_exit=0 line=REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
FULL_FUNCTION pristine one-fail exit=1 want_exit=1 line=REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
FULL_FUNCTION pristine one-setup exit=2 want_exit=2 line=REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
FULL_FUNCTION boundary-tail all-pass exit=0 want_exit=0 line=REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
FULL_FUNCTION boundary-tail one-fail exit=0 want_exit=1 line=REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
FULL_FUNCTION boundary-tail one-setup exit=0 want_exit=2 line=REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
```

Vectors were respectively nine zeros, `1 0 0 0 0 0 0 0 0`, and `2 0 0 0 0 0 0 0 0`. Raw full-function stdout and captured exits are retained as `scratch/{pristine,boundary-tail}.full-{all-pass,one-fail,one-setup}.{stdout,stderr,exit}`.

Important limitation: the frozen counter also extracts through the first `\n}\n` (`.ufo/evidence/round-33/c1/c1-measure.py:130-134`). Its block-vector witness would not expose this particular outer-function fault. The independent full-function witness does; no counter validation or scoring of this development copy was performed.

### Finding 2: loop identity is literal syntax, not the claimed dataflow

The rename copy retains the exact `local nlegs=9 npass=0 nfail=0 nsetup=0 st` marker and all nine original operands. It adds `local leg_status`, changes `for st in` to `for leg_status in`, and changes `case $st in` to `case $leg_status in`. The harness's operand-removal selector is correspondingly changed from `for st in` to `for (st|leg_status) in`; it still stresses the injected reference form as well. Exact delta: `scratch/variable-name.patch:3-23`; resulting tally: `scratch/variable-name.sh:1432-1440`.

The other two copies replace only the tally loop traversal with:

```bash
  local -a tally_statuses=("$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_citecheck")
  local tally_index=0
  while (( tally_index < ${#tally_statuses[@]} )); do
    st=${tally_statuses[tally_index]}
    case $st in
      0) npass=$((npass + 1)) ;;
      1) nfail=$((nfail + 1)) ;;
      *) nsetup=$((nsetup + 1)) ;;
    esac
    tally_index=$((tally_index + 1))
  done
```

The `until` version uses `until (( tally_index >= ${#tally_statuses[@]} )); do` instead. Both use the same ordered nine statuses, the same counter arms, and unchanged guards, output, and exits. Their harness stress selector is changed to remove the last status from either the array initializer or the injected reference loop:

```bash
  tblock=$(printf '%s\n' "$tblock_full" | sed -E '0,/^  (for st in |local -a tally_statuses=)/s/ "\$st_[a-z]+"(; do|\))$/\1/')
```

Exact deltas: `scratch/while-loop.patch:3-29`, `scratch/until-loop.patch:3-29`; actual loop definitions: both copies `:1432-1443`; adapted stress lines: both copies `:2040`.

The independent probe did not use the audit's loop locator. It compared Bash execution against a separate Python status-count oracle: every status 0–255 at each of nine positions, every feasible fail/setup count pair, position-varied mixtures, and duplicate/drop stress at every operand. It also ran each copy's actual extracted tally harness without replacing its tally with the audit's reference.

Observed from the same receipt-captured `check-semantics.py` command (`scratch/semantics.stdout:1-8`):

```text
EQUIVALENCE pristine vectors=2377 stress=18 mismatches=0 driver_exit=0
ACTUAL_HARNESS pristine exit=0 HARNESS cases=9 failed=0
EQUIVALENCE variable-name vectors=2377 stress=18 mismatches=0 driver_exit=0
ACTUAL_HARNESS variable-name exit=0 HARNESS cases=9 failed=0
EQUIVALENCE while-loop vectors=2377 stress=18 mismatches=0 driver_exit=0
ACTUAL_HARNESS while-loop exit=0 HARNESS cases=9 failed=0
EQUIVALENCE until-loop vectors=2377 stress=18 mismatches=0 driver_exit=0
ACTUAL_HARNESS until-loop exit=0 HARNESS cases=9 failed=0
```

These are bounded tested equivalence results, not a universal test-coverage claim. The actual code refactors preserve the traversal by construction. Root cause is explicit: `CASE_RE` fixes `$st` (`tools/tally-audit-v2.py:154`), and the only recognized loop grammar is `for VAR in ...` (`:151-152`, `:167-193`). The header's dataflow description at `:22-26` overstates that implementation.

### Caught candidates: indirection and stale printf

Indirection copy: insert these lines immediately after the unchanged `local nlegs=9 ... st`:

```bash
  local -n final_status=st_sourcescheck
  final_status=$st_citecheck
```

This makes the tally read cite-check's value twice while losing sources-check's real value. Exact delta: `scratch/indirect-duplicate.patch:3-11`. Static and head checks pass, but runtime reports 526 mismatches. Its first witness is `0 0 0 0 0 0 0 1 0`: got exit 0 and `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`, versus expected exit 1 and `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` (`scratch/sweep.stdout:8-12`). This candidate is caught, not a survivor.

Stale-printf copy: insert `local reported_passes=$npass` before the loop and replace only the PASS printf's `"$nlegs" "$npass"` arguments with `"$nlegs" "$reported_passes"`. `nlegs` remains correct. Exact delta: `scratch/stale-printf.patch:3-19`. Runtime reports 10 mismatches; the all-zero witness prints `passed=0` instead of `passed=9` with exit 0 (`scratch/sweep.stdout:26-30`). This candidate is caught.

## Smallest safe correction

1. **Boundary soundness:** match shell constructs rather than ending a function at the first column-zero brace. Preserve enclosing control flow when isolating the tally, and test the outer `run_regression` exit using fixed leg statuses. Merely extending the substring while dropping the nested function opener is not safe. Add the failing/setup wrapper witnesses above to the next version's regression fixtures.
2. **Equivalent forms:** bind the counting case to its actual loop variable and support the concrete indexed `while`/`until` traversal shown here, including operand-removal/duplication stress on the actual status source. Do not repair false rejects by returning PASS for unparsed shell code or by dropping guard stress.
3. **Frozen claim:** the current tool pin cannot be silently changed. Retain these findings and the frozen measurement rule; any repaired successor needs its own freeze. I did not run the round counter, author sealed data, change the runner, or decide the round.

No tools were installed or upgraded. Disk capacity was checked before generating the bounded fixtures (`scratch/disk.stdout:1-2`, `disk.exit:1`: 46G available, exit 0). All started test batches completed, with their child commands waited for; no long-lived service was started. The only lane write by this seat is this report.
