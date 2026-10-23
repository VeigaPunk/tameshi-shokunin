# ReviewTool — tally-audit.py code review at a4f718138bdad20de741faeca57891645e5a64d9

Seat: ReviewTool
Verdict first: the tool is operable and honest on every runner shape I could construct — its three
checks are real and independent, its exit codes match its docstring, and its fault panel of 27 is
fully rejected by the pinned harness. One Medium contract-fidelity defect (stdout/stderr
stream-blindness in the runtime oracle) and a handful of Low/Info items. Recommendation: fix the
Medium before or with the next counter run; the rest are safe as documented follow-ups.

Base: clone of the lane at a4f718138bdad20de741faeca57891645e5a64d9 in
`/fast/scratch/hyaku/tameshi-r32-seats/ReviewTool/c`; observed
`tools/tally-audit.py` sha256 `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef`,
`tools/mutate-and-run.sh` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
(both match the frozen pins). All runs were in the clone or `…/ReviewTool/copies`; every
`--regression` run used `--workdir /fast/scratch/hyaku/tameshi-r32-seats/ReviewTool/rg-1`. No
tools installed (python3/bash only). No stray processes remain.

## Verified correct (with evidence)

1. **REF_BLOCK is the pinned block, byte for byte.** Extracting runner lines 1432-1470 and
   comparing with the module's `REF_BLOCK` (tools/tally-audit.py:48-95) printed `True`; the tool's
   own `regression_body` + `tally_block` extraction from the pinned runner also equals `REF_BLOCK`.
   Leg names: the nine `st_*=$?` assignments, in reference order.
2. **Pinned runner passes all three checks.** `python3 tools/tally-audit.py --runner tools/mutate-and-run.sh`
   → exit 0:
   `CHECK static PASS legs=9 operands=9 nlegs=9` / `CHECK runtime PASS vectors=349 mismatched=0` /
   `CHECK harness PASS reference cases=9; faults rejected=27/27` / `TALLY_AUDIT: PASS (…)`.
3. **Fault panel is 27 and each fault is rejected by the pinned harness.** `faults()` enumerates
   exactly: label, fail-exits-0, drop-last-operand, ignore-<leg> ×9, ignore-alone-<leg> ×9,
   guard-removed, guard-overcount-only, setup-before-fail, fail-needs-exactly-one,
   setup-needs-exactly-one, status-3-passes. The harness check reports `faults rejected=27/27`. I
   also cross-checked analytically which runner-harness vector rejects each class (exact-line
   compare at mutate-and-run.sh:1998-2040), e.g. `label` dies on the exact-line compare,
   `drop-last-operand` on both the per-position vectors and the guard-stress sed (the sed removes a
   second operand, so counted=7 ≠ 8), `setup-before-fail` on the `1 2 0…` multi vector.
4. **Oracle matches real bash behavior over the full advertised sweep.** 1 all-zero + 255 single-leg
   statuses at the first leg + 9×7 per-position (1 2 3 4 126 127 255) + 10 multi + all-1/all-2
   vectors, plus dup/drop stress at each of the 9 positions: `mismatched=0`. Oracle precedence
   (any 1 → FAIL exit 1; else any non-zero → SETUP exit 2; else count ≠ nlegs → SETUP mismatch;
   else PASS) matches runner lines 1446-1466.
5. **Exit codes 0/1/2 with the documented prefixes.** Observed: 0 on the pinned runner; 1 with
   `TALLY_AUDIT: FAIL` on dup-drop (static), status-3-passes (runtime), nlegs=8 (all three), leg
   rename (harness); 2 with `TALLY_AUDIT: SETUP` for a missing file (`[Errno 2] …`) and for a
   runner whose harness section was removed.
6. **Check independence (kill attribution).** On `dup-drop.sh`: only CHECK static fails (runtime
   PASS — check 2 audits the loop as it counts, the multiset-vs-legs question is check 1's). On
   `s3pass.sh`: only CHECK runtime fails (12 mismatches, first at `3 0 0…`). On `nlegs8.sh`: all
   three fail (its own harness extraction expects the literal `nlegs=9` line, so check 3 honestly
   reports `harness rejects or cannot run the reference block ((9, 1))`). Harness-only weakening is
   caught by check 3 alone (selftest cases below).
7. **`--selftest`: 11/11 pass, exit 0.** All ten seeded mutations are detected as intended
   (dup-drop operand, nlegs wrong, status 4 passes, guard undercount only, harness exit-only,
   harness swallowed, harness position 8/0/1 skipped — each exit 1 with the intended CHECK failing)
   and `reversed operands` is correctly accepted (exit 0). The `harness swallowed` case works
   because appending `rc=$?` after the `[[ ]]` makes the assignment tally_line's last statement, so
   every comparison returns 0 and all 27 faults are accepted.
8. **`--then-regression` behaves as documented.** On the pinned clone runner with
   `--workdir …/rg-1`: audit PASS first, then the full replay ran, the `REGRESSION:` line was
   parsed, `cases=9` equals the 9 legs found, and the runner's exit code was propagated verbatim:
   `TALLY_AUDIT_REGRESSION: SETUP (cases=9 legs=9 exit=2)`, tool exit 2, workdir kept. All nine
   legs are SETUP here because the sibling repos do not exist as repositories under my scratch
   clone (`repo_identity_mismatch … toplevel=unresolved`) — expected outside the real lane layout;
   the gate, the cases==legs check and the pass-through are what this verifies, and they hold.
   It did not run the replay when the audit fails (code path :451-453, only on `rc == 0`).

## Defects

### Medium

**M1. The runtime oracle is stream-blind: a tally block that prints its REGRESSION lines to stderr
passes check 2.** tools/tally-audit.py:174 builds the driver line
`out=$(tally %s 2>&1); rc=$?; printf "R\t%s\t%s\n" "$rc" "${out%%$'\n'*}"` — the "first line" the
oracle compares is taken from stdout and stderr merged, so the audit cannot tell a stdout contract
line from a stderr one. The runner's printed contract puts `REGRESSION: …` on stdout
(mutate-and-run.sh:1447, 1453, 1461, 1467).

Exact exposing input — a copy of the pinned runner with the PASS printf redirected to stderr:
`printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' >&2 \`
Observed: `CHECK runtime PASS vectors=349 mismatched=0` (static and harness also PASS),
`TALLY_AUDIT: PASS`, exit 0. A runner whose success line lands on stderr — observable behavior
different from the pinned runner for any stdout consumer — audits clean.

Smallest safe correction: capture stdout only for the compared line (`out=$(tally …)` without
`2>&1`, stderr kept in a separate capture) and treat a REGRESSION line that arrived via stderr, or
any non-empty stderr on a matching run, as a mismatch. This changes the verdict only for
non-contract blocks; driver-level errors are still visible through rc and the separate stderr.

### Low

**L1. `--then-regression` runs the replay with no timeout.** tools/tally-audit.py:384
`p = subprocess.run(argv, capture_output=True)` has no `timeout=`, while the tool's own internal
bash helper enforces `TIMEOUT = 120` (:38, :162, :325). One hung leg hangs the audit past its own
discipline. Smallest safe correction: pass a bounded `timeout=` and map
`subprocess.TimeoutExpired` to a `TALLY_AUDIT_REGRESSION: SETUP (…)` line with exit 2.

**L2. Check 3 refuses any runner whose leg names differ from the reference — an unstated validity
boundary.** tools/tally-audit.py:339 `if names != REF_NAMES: return False`. Exact input: pinned
copy with `st_js` renamed to `st_alpha` everywhere (assignments, loop, harness). Observed: CHECK
static PASS, CHECK runtime PASS, `CHECK harness FAIL leg names differ from the reference panel
(st_alpha st_kagi …)`, overall FAIL exit 1. The coupling is structural — the 27-fault panel is
built from `REF_BLOCK`'s names while the audited harness binds statuses by its own `tnames`, so
cross-feeding aborts under `set -u` — and the message is honest, but any held-out copy that renames
legs is rejected regardless of equivalence. Smallest safe correction: state the boundary in the
docstring (or translate `REF_NAMES` to the audited names when driving the panel). Whether any
held-out must-accept copy renames legs is not visible from this seat.

### Info

**I1. A runner with the harness section removed is SETUP (2), not FAIL (1).** Exact input: pinned
copy with the `  local tblock tgot tvec ti tj` … `  tblock=$tblock_full` section deleted. Observed:
`TALLY_AUDIT: SETUP (selftest tally harness (`local tblock`) not found)`, exit 2. Defensible as
"cannot audit"; note the knowledge doc's "a runner whose harness is broken is caught by check 3"
holds only for weakened-but-present harnesses.

**I2. Dead constant.** tools/tally-audit.py:44 `START = '  local nlegs='` is never referenced (the
code uses `START_RE`, :108). Delete.

**I3. `--workdir` is silently ignored without `--then-regression`.** main() (:439-456) parses
`--workdir` unconditionally but forwards it only inside the `then_regression` call; no warning.

**I4. Docstring line-range nit.** tools/tally-audit.py:47 says the reference block is
"(round 30, lines 1432-1472)"; in the pinned runner the block body is lines 1432-1470
(`local nlegs=` … `exit 0`), closing `}` at 1471. Off by two (or by one counting the brace).

## Residual risk and verification gaps

- The oracle restates the runner's printed contract (a stated limit of the approach); its agreement
  with real bash is verified only on the tested vectors. Multi-nonzero-status × wrong-operand-count
  combinations are not exercised (the dup/drop stress uses all-zero statuses), so a variant block
  that matches everywhere tested but differs exactly there would false-PASS. [INFERENCE —
  theoretical, no such input constructed.]
- M1 was probed only on the PASS printf; the FAIL/SETUP printfs share the same merged-stream
  comparison and are presumed equally blind.
- The nine regression legs of `--then-regression` could only be exercised as SETUP (cannot-verify)
  outside the real lane layout; lane bounds forbid running gates inside the lane itself. The
  gate-on-PASS, the cases==legs check and the exit-code pass-through are verified; the per-leg
  replay is not.
- Held-out impact of M1/L2 (whether any valid held-out copy shifts streams or renames legs) cannot
  be judged from this seat; the held-out set is written by other seats.
