# CriticSize — C1 size and axis review

**Verdict: the axis fits, but “closes the runner items” is too large and premature.** The changed surface is a separate runnable audit, so **operability; capability acquisition** is a defensible description. It does not land the in-runner per-leg check or harden the runner's existing selftest. The route can instead be explicitly retired in favor of an external audit, as the previous spot-check permits, but successful audit coverage must first be demonstrated under the frozen v2 predicate. This is a scoped objection, not a claim-admission or runtime judgment.

## Strongest objection: a second gate is not a repaired first gate

At the content revision `a4f718138bdad20de741faeca57891645e5a64d9`, the original entry points still bypass the new audit. A copy that repeats `st_js` and omits a failing `st_citecheck` can still print a nine-of-nine regression PASS. The new tool rejects that same copy. This is real additional detection when the new command is used, not a change to the old command's guarantee.

The distinction matters especially for the eight survivors: the audit detects a weakened tally harness by injecting faults into it; it does not add the missing negative controls to `bash tools/mutate-and-run.sh --selftest`. Calling those items “fixed in the runner,” or treating the unchanged selftest as the stronger gate, would be false. Calling the external gate useless merely because it leaves those bytes unchanged would also be false.

## Evidence

Paths below are lane-relative unless absolute. The executable probe read committed bytes at `a4f718138bdad20de741faeca57891645e5a64d9`; it did not run a full counter, selftest, or regression replay.

### 1. The route permits retirement, not an undisclosed change of meaning

- `corpus/lessons/round-31-verifier-spotcheck.md:202-203`: the twice-deferred per-leg check and eight survivors must be landed **or the route retired with a stated reason**.
- `corpus/lessons/round-31.md:176-179,188`: the runner edits were explicitly deferred to preserve input-keyed cold-read credit.
- `.ufo/waves/round-32/w1/ScoutDeferrals.md:3-9,53`: the scout already distinguishes retirement by an external audit from landing the requested in-runner changes; its initial closure assessment was inferred, not an executed result.
- `.ufo/waves/round-30/wC/MutateHead.md:70,73-80,155-173`: the recorded eight real survivors are T08, H03, H04, H05, N01, N02, N03 and N05. Only N05 is a guard mutant; its failure is overcount-stress-bounded. I did not rerun the reported surviving selftests to confirm them.

### 2. Executed counterexample: the normal tally remains weaker

Exact parent command, working directory `/fast/scratch/hyaku/tameshi-r32-seats/CriticSize`:

```sh
timeout 150 python3 -I /fast/scratch/hyaku/tameshi-r32-seats/CriticSize/size-probe.py
```

It exited 0. The script obtained the two inputs with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a4f718138bdad20de741faeca57891645e5a64d9:<path>`, copied them only into this seat's scratch directory, and checked the hashes below. Its base comparison used the same read-only command at `e24688b2ff6cca1c9ad20e112f02c629b8597ff8`.

```text
runner_sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
tool_sha256=9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef
runner_equal_base=True
```

Reproducible construction: extract the actual tally block from `tools/mutate-and-run.sh:1432-1470`, wrap it in a Bash function with all nine `st_*` locals bound to `0 0 0 0 0 0 0 0 1` in assignment order, and bind `root=probe-tally auto=0 KEEP=1`. For the mutant, change only the loop's final operand `"$st_citecheck"` to `"$st_js"` at line 1433. Apply that same one-operand replacement to the complete runner copy supplied to the audit. The tally's sum guard at `:1456-1460` remains unchanged.

Exact child commands executed by the script, with observed output:

```sh
timeout 10 bash /fast/scratch/hyaku/tameshi-r32-seats/CriticSize/direct-pristine.sh
# exit 1
# REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
# REGRESSION_WORKDIR: probe-tally (kept)

timeout 10 bash /fast/scratch/hyaku/tameshi-r32-seats/CriticSize/direct-dupdrop.sh
# exit 0
# REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
# REGRESSION_WORKDIR: probe-tally (kept)

timeout 90 python3 -I /fast/scratch/hyaku/tameshi-r32-seats/CriticSize/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CriticSize/runner-dupdrop.sh
# exit 1
# CHECK static FAIL legs=9 operands=9 nlegs=9; loop operands != legs (missing ['st_citecheck']; miscounted ['st_js'])
# CHECK runtime PASS vectors=349 mismatched=0
# CHECK harness PASS reference cases=9; faults rejected=27/27
# TALLY_AUDIT: FAIL (static=fail runtime=pass harness=pass)
```

These are extracted-tally runs, not executions of the full `--regression` path. They establish the boundary directly: the external static check catches this fault, while the old tally still accepts a dropped failing leg. The runtime PASS does not independently repair per-leg identity: its oracle uses the actual counted operands (`tools/tally-audit.py:183-195,218-251`), leaving identity to `check_static` (`:200-215`). The three checks must not be advertised as three independent detections of every routed defect.

The same executed script counted, over the committed files:

```text
capability_rows_with_tally_audit=0
skill_tally_audit_references=0
skill_then_regression_references=0
runner_tally_audit_references=0
```

The first count selected SCORECARD lines beginning `|` and containing `tally-audit`; the other counts were exact substring counts in SKILL.md and the runner. This is a bounded search, not a claim about every caller everywhere. Existing raw replay instructions remain at `SKILL.md:399,1319-1322`; the runner's registry entry still names its raw selftest/regression at `:1810`. The new tool's combined path is opt-in: `tools/tally-audit.py:439-455` calls `then_regression` only with `--then-regression` after audit success. Nothing in this evidence establishes mandatory adoption by existing callers.

### 3. Some prose already outruns the pending measurement

- `SCORECARD.md:1561-1572` describes the new tool and target, but `:1564-1565` already says it “closes” the runner items.
- `corpus/knowledge/runner-tally-audit.md:7` and `corpus/README.md:470` likewise assert closure. The knowledge entry's limit at `:26` correctly says the original selftest remains unchanged and still passes the eight survivors.
- `SCORECARD.md:1579-1580` correctly reserves measured results until execution; there is **no tally-audit capability row** at the reviewed revision.
- `.ufo/evidence/round-32/v2/contract-amendment-1.json:10,25-36` requires the public copies **and every valid held-out copy**, minimum six kills and six accepts, fixed tool/runner identities, and the first full measurement run. This one public duplicate/drop probe is not `C1_R32V2_PASS` and supplies no held-out result. A finite panel is not completeness over runner edits.

## Impacted axes and capability timing

- **Operability:** the surface actually changed: an additional executable audit with observed negative behavior. This supports the axis choice, not the unrun full C1 result. Addendum §9 says to name the axis by the changed surface (`/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:203-225`); canonical `AXES.md:13` defines operability as runnable artifacts. “Capability acquisition” is the claim type, not a seventh axis.
- **Calibration:** the risk is reporting pending detection as demonstrated closure, or reporting external detection as repaired runner behavior. This is fixable disclosure, not a necessary tradeoff of the design.
- **Depth, coverage, freshness, adjacency:** neither the number of vectors nor the panel size establishes a move on these axes. This review does not assess their round-wide no-harm evidence.

**A capability row is not forbidden solely because it precedes v2.** The canonical rule is a passing demonstration in the round report (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:57-64`); selftest capability and measurement are explicitly different (`PROTOCOL.md:403-410`). But an unqualified row promising C1's complete declared audit scope before its deciding v2 result would pre-claim that result. A separately evidenced, explicitly narrower demonstration must not substitute for C1, change its target, or mark it passed. The smallest and clearest choice here is to keep the candidate outside the standing capability table until the measurement, then record exactly what was demonstrated. No present table violation was found.

## Smallest safe correction and honest report wording

1. Keep the frozen runner, tool and predicate unchanged. Do not turn this criticism into a post-data repair or a narrower success rule.
2. Replace premature “closes” statements consistently with “adds an external audit for; C1 measurement pending.” Distinguish the unchanged raw commands from the opt-in audit/combined command. Name v2 as the deciding measurement, not the public v1 recipe still printed at `corpus/knowledge/runner-tally-audit.md:2-3,19`.
3. After the deciding run, report its actual result. Only if it succeeds, describe the route as **retired in favor of the demonstrated external audit, to preserve runner-keyed cold-read inputs**; explicitly retain the fact that in-runner hardening was not landed. Do not state that the old entry points now reject the survivors. If it fails, report the frozen miss, not closure.

Honest wording for the current report:

> C1 adds a separate runner-tally audit, an operability capability candidate. The runner is byte-identical and its selftest retains the eight documented survivor gaps. In this review's public duplicate/drop witness, the extracted old tally falsely passed a dropped failing leg, while the new audit rejected the copy through its static check. This does not establish C1's sealed held-out result; the first full v2 measurement remains decisive. The proposed route disposition is external-audit retirement, not in-runner repair.

Preserving the old runner is a disclosed design choice, not by itself a defect requiring rejection. A false v2 result or an unresolved no-harm failure cannot be traded away by renaming that choice a capability; those outcomes belong to the canonical judge, not this critic.

Scope: no production edits, no git writes, no counter main, no full selftest/regression, no native judgment, no persistent service started. All spawned commands finished. Tool installs or updates: none.
