Verdict: **C1 is a miss under its own amended kill rule.** The first full v2 measurement reports false with nine surviving must-kill copies and four unsuccessful must-accept classifications. Neither the perfect public-v1 subset, the skipped pre-measurement control re-score, nor the tool's documented non-exhaustiveness authorizes re-scaling, exclusion, a replacement first run, or an earned capability row. A runnable, boundedly useful audit artifact was added; the declared C1 operability improvement was not demonstrated. This is an advisory reading of the recorded rule and evidence, not the canonical Rust judgment or a round-admission decision.

# CriticMeasurement — round 32 residual review

Seat: `TameshiR32.CriticMeasurement`. All repository-relative paths below are in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Axes implicated: **operability** (wrong diagnostic outcomes on in-scope copies), **coverage** (status, interaction, and syntax blind spots underlying those outcomes), and **calibration** (reporting the failed demonstration without turning partial utility into success). No score or promotion inference is made.

## Evidence

### 1. The deciding run and its provenance

The original `contract.json:13-35` defined C1, its all-copies predicate, and its first-full-run kill rule. Amendment 1 superseded the v1 label/predicate before the v2 measurement: `v2/contract-amendment-1.json:10-35` requires all 18 v1 kills, all 8 v1 accepts, **every valid held-out copy**, at least six held-out copies of each kind, and the identity/timing pins. Its kill rule is explicit:

> C1 fails if the first full v2 counter run at the measurement revision prints C1_R32V2_PASS=false; reported as a miss, never re-scaled, re-seeded or amended. Every other run is reported as observed.

Amendment 2 records the changed tool identity and two counter hardenings; it expressly leaves the predicate, thresholds, held-out rules, kill rule, and measurement protocol unchanged (`contract-amendment-2.json:4-14`). The final tool pin is `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef`.

**Exact measurement command excerpt, not executed by this critic:** the L1 transcript's Bash tool call `toolu_01GyZMZU5XwtrohQLrz7j6sh`, titled “Committing measurement revision and first v2 run,” has this counter invocation, with the lane as cwd and shell variable `M` set from `git rev-parse master` immediately beforehand:

```sh
timeout 1800 python3 .ufo/evidence/round-32/v2/c1-measure-v2.py --lane . --rev $M --work /fast/scratch/hyaku/tameshi-r32/w-measure >.ufo/evidence/round-32/after/c1v2-at-measurement.stdout 2>.ufo/evidence/round-32/after/c1v2-at-measurement.stderr
```

The original process result was:

```text
landed 24a5a5bb598ae919546715267d76f814efaf8912
24a5a5bb598ae919546715267d76f814efaf8912


Wall time: 42.69 seconds

Command exited with code 1
```

The receipt `after/c1v2-at-measurement.stdout:71` reads, verbatim:

```text
C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=63d2e2e95a1e35c5 rev=24a5a5bb598ae919546715267d76f814efaf8912 C1_R32V2_PASS=false
```

`after/c1v2-at-measurement.stderr` is empty. `after/c1v2-at-measurement.exit:1` contains `1`. **Provenance qualification:** that exit file was written immediately afterward from the observed Bash-call status, not by the original chained `echo $?`; `after/c1v2-at-measurement.exit-note.txt:1` explicitly records this. The original tool result independently records exit 1. Do not describe the exit file as a successful inline capture.

The receipt lists all 22 submitted measurement files as `valid=1` (`stdout:1-22`). The minimum counts and all three pin/timing flags are satisfied. This is therefore not a no-tool, invalid-fixture, insufficient-sample, identity-mismatch, or all-sandbox-runs-failed result. In particular, the public v1 copies produce the required real classifications, and held-out failures reproduce the authors' specific diagnostic outcomes.

The counter computes validity before auditing (`c1-measure-v2.py:345-356`), then requires exact kill/accept outcomes (`:268-273,388-401`). An auditor's `SETUP` response does not retroactively invalidate an accept fixture. Only mechanically invalid fixtures are excluded; this run has none. Guard-2's whole-panel-duplication witness is explicitly permitted by the optional `witness.loop` form (`:30-33,225-230`), not an excuse to remove that result.

**Answer to question 1:** yes. The rule is all-copies, not a percentage threshold or a comparison with the old selftest. Public-v1 success is a component observation, not a separate passing C1 authority. No post-result seed, patch, dropped fixture, narrowed surface, or exploratory reclassification can replace this first result. Whether the amendment-2 identity change is itself acceptable is separately reserved to the canonical judge; any additional protocol defect supplies no route to claim C1 succeeded.

### 2. What the nine surviving kill copies actually expose

All nine rows below are `COPY src=ho set=kill ... outcome=ACCEPT exit=0` with the exact final line:

```text
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

The integrated receipt is the classification evidence. Witness outputs are existing observations in the named author reports, not fresh executions by this critic. Every vector has nine positions in the pinned runner's leg order.

| Cause | Surviving copy and receipt line | Existing witness observation and mechanism |
|---|---|---|
| Missing count regimes 3–8 | `HeldOutPrintf-1`, line 46 | Vector `[0,1,1,1,0,0,0,0,0]`: pinned exit 1 reports `passed=6 failed=3 setup=0`; copy exit 1 reports `passed=6 failed=2 setup=0`. A conditional printf under-reports failures when `nfail > 2 && npass > 0`. |
| Missing count regimes 3–8 | `HeldOutPrintf-2`, line 48 | Vector `[2,2,2,0,0,0,0,0,0]`: pinned exit 2 reports `passed=6 cannot-verify=3`; copy exit 2 reports `passed=6 cannot-verify=2`. The runtime panel never reaches setup count 3. |
| Missing mixed-count/precedence regime | `HeldOutGuard-1`, line 47 | Vector `[1,2,2,2,2,2,0,0,0]`: pinned exit 1 prints `REGRESSION: FAIL (cases=9 passed=3 failed=1 setup=5)`; copy exit 2 prints `REGRESSION: SETUP (cases=9 passed=3 cannot-verify=5)`. A setup-majority qualification wrongly suppresses FAIL precedence. |
| Statuses beyond the per-position list | `HeldOutLoop-1`, line 43 | Vector `[0,128,0,0,0,0,0,0,0]`: pinned exit 2 prints `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)`; copy exit 0 prints `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`. A seven-bit mask turns the kagi status into zero. Status 128 is swept only at position 0, not at kagi. |
| Statuses beyond the per-position list | `HeldOutRefactor-k1`, line 50 | Vector `[0,0,0,5,0,0,0,0,0]`: pinned SETUP/exit 2 becomes FAIL/exit 1. The copy misclassifies status 5 only after the first leg; the exhaustive sweep therefore misses it. |
| Conditional double counting | `HeldOutTallyArms-01`, line 45 | Vector `[2,2,1,0,0,0,0,0,0]`: both exit 1; pinned `passed=6 failed=1 setup=2` becomes `passed=6 failed=2 setup=2`. The failure arm increments twice after two setup results. Neither singleton, selected pair, nor uniform vectors exercise that mixed triple. |
| Uncovered conditional cross-leg status flow | `HeldOutLoop-2`, line 44 | Vector `[0,0,0,1,0,0,1,0,0]`: both exit 1; pinned `passed=7 failed=2 setup=0` becomes `passed=8 failed=1 setup=0`. On the mado error path, roundgate is overwritten from sourcescheck. The selected pair positions do not exercise this dependency; uniform vectors preserve the overwritten value. |
| Status-pair counter updates, despite single-status coverage | `HeldOutTallyArms-02`, line 41 | Vector `[126,127,0,0,0,0,0,0,0]`: both exit 2; pinned `passed=7 cannot-verify=2` becomes `passed=7 cannot-verify=1`. The `126|127` arm assigns `nsetup=1` instead of incrementing. Both statuses are in the per-position list, but their repeated/pair interaction is not covered. |
| Incomplete guard cardinality stresses | `HeldOutGuard-2`, line 49 | All-zero vector with the whole nine-leg panel counted twice: pinned exit 2 reports `case-tally mismatch: cases=9 counted=18`; copy exit 0 reports `cases=9 passed=18`. A divisibility guard passes the tool's counts 8 and 10 but wrongly accepts count 18. The submitted copy itself retains the original nine operands; the counter-owned witness substitutes the doubled list into both compared blocks. |

Author evidence locations: `w2/HeldOutPrintf.md:80-134`; `HeldOutGuard.md:74-90`; `HeldOutLoop.md:38-82`; `HeldOutTallyArms.md:63-89`; `HeldOutRefactor.md:133-154`.

These are different failure causes, not nine flat T08 copies. In particular, the status-126/127 counter-flag defect is **not** an omitted-single-status case; the mixed double increment is **not** an omitted loop operand; and Loop-2 is an error-path status-flow defect. Several copies retain the correct exit code but corrupt the exact tally fields. That still violates the declared first-line-and-exit contract.

The only held-out kill that was killed is `HeldOutRefactor-k2` (`stdout:42`): a non-conditional off-by-one in the FAIL line. Its success makes the printf blind spot more specific, not less real.

#### Source cross-check: coverage, not a broken oracle

`tools/tally-audit.py:218-253` schedules:

- All-zero plus statuses 1–255 at the **first leg only**.
- Statuses `{1,2,3,4,126,127,255}` singly at every position.
- Two independently varied pair positions, `(0,8)` and `(4,5)`, with five status pairs.
- All-one and all-two vectors.
- One-operand duplicate/drop stresses with all legs zero.

For the unchanged nine-operand loop, the ordinary vectors reach failure/setup counts `{0,1,2,9}`, not 3–8. There are 331 scheduled ordinary vectors and 18 stresses, explaining the authors' `CHECK runtime PASS vectors=349 mismatched=0`; that number is not exhaustive joint-state coverage. Uniform all-nonzero vectors do not substitute for isolated pair or mixed-triple tests. In particular, do not turn `HeldOutPrintf.md:129`'s “all 36 leg pairs sampled” boolean into a claim of independently varied coverage of all pairs: the actual pair loop contains only the two pairs above.

The oracle (`tally-audit.py:183-195`) computes counts and precedence independently and compares both exit and first line. The listed surviving witnesses expose missing inputs to that oracle, not evidence that its basic count arithmetic is wrong. Likewise, `CHECK harness PASS ... faults rejected=27/27` checks the runner's harness against injected reference faults (`:338-354`); it does not enlarge the audited tally's runtime vector coverage. Do not present it as a second exhaustive check of those surviving tally edits.

### 3. The four wrong must-accept classifications

“Four wrong accept copies” means **four valid copies the tool was required to accept**, not four defective runners wrongly accepted. Three receive FAIL/exit 1; the fourth receives SETUP/exit 2.

| Cause | Copy and integrated receipt | Why this is the auditor's error |
|---|---|---|
| Wrong loop selected for both accounting and instrumentation | `HeldOutLoop-3`, line 66: `outcome=KILL exit=1`, `static=fail runtime=fail harness=pass` | A one-operand outer loop executes the unchanged real tally loop once. The tool mistakes the wrapper's operand list for the counting loop, reports only one operand, and compares the real nine-count output with an oracle based on that wrong list. |
| Wrong loop selected for stress mutation | `HeldOutLoop-4`, line 63: `outcome=KILL exit=1`, `static=pass runtime=fail harness=pass` | A nine-operand wrapper breaks after one iteration. Its operands happen to satisfy the static multiset check, but duplicating/dropping wrapper operands does not alter the real tally. The tool manufactures 18 stress mismatches by changing the wrong loop. |
| Wrong loop selected for stress mutation | `HeldOutRefactor-a4`, line 65: `outcome=KILL exit=1`, `static=pass runtime=fail harness=pass` | An output-neutral auxiliary pass over the same nine statuses precedes the real tally. The tool chooses that pass and again expects its 18 operand stresses to affect the tally. |
| Harness extraction confused with semantic invalidity | `HeldOutRefactor-a3`, line 59: `outcome=OTHER exit=2`, `TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)` | A redundant, deeper-indented extraction assigns the same block before the existing extraction. The counter's fixed two-space extraction anchor still finds the intended line; the tool's whitespace-tolerant regex finds both and refuses to audit a valid equivalent runner. This is not `ho_invalid=1`. |

Mechanism: `tally-audit.py:129-151` explicitly selects the **first** status-operand `for` loop, without identifying its data-flow role, and reuses that selection in `with_operands()`. A matching operand multiset is therefore not proof that the correct loop was selected. `:295-314` requires exactly one broad regex match for harness extraction; the counter uses its separately declared fixed anchor at `c1-measure-v2.py:71-74,141-149`. Author observations and details: `HeldOutLoop.md:84-116`; `HeldOutRefactor.md:115-126,156-188`.

The counter validated these copies, including its own correctly targeted stresses. They are not failures caused by altered real tally operands. A conservative refusal can be a deliberate parser tradeoff in another contract; under this contract's explicit must-accept obligation it remains a failed classification, not a permissible exclusion. Retaining static and stress checks while silently changing their target is a fixable instrumentation defect.

### 4. Strongest local counterexample and exact existing detector evidence

`HeldOutLoop-1` is the clearest challenge to any softened “the tally is now externally verified” wording: a nonzero late-leg setup status becomes a false PASS, yet all three audit checks say PASS. It is not merely a cosmetic count discrepancy or a hypothetical unsampled input.

The author's exact recorded direct-audit command (`w2/HeldOutLoop.md:40-50`) was:

```sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutLoop/copies/1.sh
```

Observed there: exit 0, with:

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=349 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

The author's existing witness observation is quoted in the table above. The frozen JSON contains the exact mask and vector (`heldout/HeldOutLoop-1.json:7-23`). The independent integrated sandbox measurement agrees on this same materialized-copy SHA prefix `f9e0ac08a3da7242` (`after/c1v2-at-measurement.stdout:43`). Source inspection shows exactly why status 128 at position 1 is omitted. This review did not re-run an already reported failure to confirm it.

### 5. Skipped amendment-1 control re-score — answer to question 3

`contract-amendment-1.json:35` requires, **before** the L1's first real-tool v2 run, a v2 re-score against the committed held-out set of always-pass/fail, both CriticC1 allowlist variants, an embedded v1 allowlist, SHA-table, static-only, runtime-only, harness-only, and old-selftest controls. The assignment records that this ordering step was skipped.

That is a real protocol/conformance defect. A later residual control run can show what those controls do now, but cannot retrospectively satisfy “before.” Do not call a later result a pre-data receipt, or treat old v1 control scores as the required v2 re-score.

It **does not turn the miss into an unmeasured success or grant another first run**. The kill rule is not conditional on satisfactory controls, and the evaluated receipt contains actual valid-copy misclassifications. Missing controls weaken assurance that a positive result would discriminate the intended capability from shortcuts. They do not erase these observed counterexamples. If a later shortcut meets v2, that additionally weakens the counter; it cannot strengthen C1. Formal handling of this process defect remains with the canonical judge.

There is a second provenance limitation already disclosed by amendment 2 (`data_disclosure:8-11`): the tool identity changed after real-tool data on public v1 fixtures, and the tool was developed against many public-v1 seeds. Thus `18/18` and `8/8` are useful regression observations, not independent proof against memorization. The sealed held-out exercise was meant to provide that additional challenge, and it falsified the intended C1 demonstration.

### 6. What can honestly be claimed — answer to question 4

- **Capability row: no.** The claimed runner-tally-audit acquisition did not achieve its declared demonstration. Do not enter a narrower “first working round 32” capability from the public-v1 subscore after the sealed result failed. The repertoire rule in canonical `AXES.md:57-64` also requires a passing demonstration; this critic does not exercise the admission gate.
- **Unqualified “operability improved”: not established by C1.** Availability and bounded utility are observed: the new tool executes, catches all measured public-v1 kills, accepts their equivalents, and leaves the pinned runner unchanged. Those are reportable implementation facts. They do not establish that the declared all-valid-copies audit is operationally correct, or authorize relabeling the failed capability claim as a successful axis move or an exploratory claim after seeing the data. Conversely, this evidence alone does not prove an existing production workflow was harmed: no runner change is claimed.
- **Repairs: retain their own bounded evidence, separately.** The exact-header/byte-prefix repair counter and fresh base/Command-D receipts are described independently in `contract.json:38-42` and `w1/ReviewRepairReceipts.md:7-17,45-50`. They are not substitutes for C1. Preserve the explicit statement that the missing original round-31 Command-D exit was not reconstructed. This review does not certify the repair counter as complete or overwrite the separate repairs review.
- **Held-out falsifier design: a concrete useful result.** Five non-tool-author seats supplied 22 mechanically valid measurement copies after the freeze; the integrated exercise exposed nine false accepts and four failed accept obligations. It is honest to report those counterexamples and the finite sealed-test mechanism. It is not honest to claim the skipped v2 control program was completed before data, that the counter is proved ungameable, or that the audit now covers all status/interaction/syntax regimes.

The contract's non-exhaustiveness disclaimer concerns arbitrary edits outside a finite demonstration. It cannot excuse failure on copies expressly included in that demonstration. Saturated depth/calibration scores and a stagnation nudge motivate trying the capability; they do not lower its kill rule or provide evidence that it was acquired.

## Smallest safe correction

**For this round, correct the interpretation and report, not the frozen objects.** Keep the tool, counter, amendments, held-out files, deciding receipt, seed, and measurement revision intact. Retain all 22 valid files and disclose the skipped pre-data controls. Describe later runs as later observations. Attribute any independently evidenced repairs separately. No production correction was applied by this critic.

**Recommended one-paragraph C1 verdict — answer to question 5:**

> C1 missed. At measurement revision `24a5a5bb598ae919546715267d76f814efaf8912`, the first full v2 run of the frozen audit tool (`9639c458…99ef`) returned exit 1 and `C1_R32V2_PASS=false`: the public-v1 subset was `18/18` kills and `8/8` accepts, but the sealed held-out set was only `1/10` kills and `8/12` accepts, with zero invalid copies and all identity/timing checks satisfied. Nine defective copies survived; three valid equivalents were falsely failed and one valid equivalent produced SETUP. These expose count-regime, positional-status, interaction, guard-stress, loop-selection, and harness-extraction gaps. The required v2 control re-score was not completed before this run, a separate disclosed process defect that does not erase the miss or authorize a replacement first run. We claim no acquired C1 capability or demonstrated C1 operability improvement; we retain the runnable audit artifact, separately evidenced repairs, and the held-out counterexamples as bounded results, without re-scaling or excluding failures.

For a separately authorized future, unfrozen revision, the smallest evidence-led repair set is: cover count bands 3–8 and setup-majority/conditional interaction witnesses; exercise all 0–255 statuses at each leg rather than conflating status coverage with position coverage; include the repeated 126/127 and whole-panel-duplication witnesses; and identify the actual counting loop and effective harness extraction for instrumentation rather than selecting a first textual match. Preserve already accepted helper/refactor forms. Merely deleting the duplicate-extraction check or ignoring stress mismatches would suppress the symptom, not fix the target-selection problem. These are future correction requirements, not evidence that any fix has passed or permission to amend this measurement.

### Review bounds and exercised work

The only shell command executed by this critic was isolated checkout preparation:

```sh
timeout 15 mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CriticMeasurement && timeout 90 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CriticMeasurement/c
```

It completed successfully with no output. Evidence was inspected with bounded `read`/`grep`/`glob` calls, including the original measurement command/result in the L1 transcript. The critic did not execute a counter, auditor, selftest, regression, model, judge, or another runtime; did not spawn seats; did not modify production code or frozen evidence; and did not issue Git writes outside its private clone or any `jj` command. Only this requested report was written in the lane. No process was manually killed. Tool installs/updates: none; existing tools sufficed.
