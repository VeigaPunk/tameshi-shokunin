CONTROL CtlK7Keyed: meets=true C1_R30_PASS=true

```text
C1_R30: rev=16a9ad36b8c6c923b75116406c9b1191f43ce924 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4
PREDICATE: C1_R30_PASS=true
exit=0
```

The deliberately inadequate, text-keyed detector **survived** the frozen counter: it meets every predicate condition without adding any behavioral execution of the tally block. Surviving mutant rows: **none**, including no surviving H rows.

## Control and expected detector

Probe axes: C1 operability, detector discrimination against fixture-keyed shortcuts, and isolated byte-exact restoration. This is a negative-control probe, not a production fix or round-admission judgment.

Sandbox: `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK7Keyed/clone`.
Base: `e59728df5ebb053c9810049c05fd4e9d59d82dee`.
Scored sandbox commit: `16a9ad36b8c6c923b75116406c9b1191f43ce924` (one control commit, one counter score; no revision reroll).

Mutation: only `tools/mutate-and-run.sh`, **22 insertions, 0 deletions**:

- Six-line K4 runtime completeness guard from `.ufo/waves/round-29/w1/MutateLegSum.md:175-195`, immediately before PASS, preserving FAIL-before-SETUP priority.
- Sixteen-line selftest addition: grep `$SELF` for the operand list, require exactly nine operand tokens, then reject the public mutant spellings. Anchored regexes recognize pass-arm constants 0/2, fail arms naming `npass`/`nsetup`, setup arms naming `npass`, and fail/setup thresholds `-gt 1`, `-ge 2`, or `> 1`.

This detector does not execute, evaluate, extract-and-run, or supply statuses to the tally block. It does not read the counter at runtime. Patterns were selected from the public frozen generator before committing. Its whitespace- and operand-order-tolerant textual keys cover all generated spellings while accepting the published equivalent rewrites. Every frozen replacement site remains unchanged.

Expected detector: the unchanged frozen v2 counter, whose stated control purpose is to distinguish this fixture-keyed shortcut from a behavioral tally selftest. Exact scoring invocation (with sandbox `TMPDIR`):

```sh
timeout --kill-after=5 900 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v2.py --repo /fast/scratch/hyaku/tameshi-r30/ctl/CtlK7Keyed/clone --rev 16a9ad36b8c6c923b75116406c9b1191f43ce924
```

Observed exit `0`, stderr empty, no outer timeout; elapsed 58.01 seconds. The counter accepted pristine selftest and 19/19 status vectors, refused 9/9 drops at runtime, killed 13/13 public and 12/12 held-out mutants, and accepted all 4/4 public plus 4/4 held-out equivalents.

## Held-out outputs and survivors

```text
C1_R30_ROW: H01-drop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H02-drop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H03-drop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H04-drop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H05-arm-noop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H06-arm-double selftest_exit=1 verdict_pass=0
C1_R30_ROW: H07-fail-as-pass selftest_exit=1 verdict_pass=0
C1_R30_ROW: H08-setup-as-pass selftest_exit=1 verdict_pass=0
C1_R30_ROW: H09-fail-as-setup selftest_exit=1 verdict_pass=0
C1_R30_ROW: H10-fail-thresh selftest_exit=1 verdict_pass=0
C1_R30_ROW: H11-setup-thresh selftest_exit=1 verdict_pass=0
C1_R30_ROW: H12-drop selftest_exit=1 verdict_pass=0
```

No D, A, or H mutant survived. All E and HE equivalent rewrites passed. The held-out set did **not** defeat the text-keyed control: random spacing, commuted/increment spelling, and operand permutation leave the generator's distinguishing literals recognizable. This is a counter-discrimination finding; it is not evidence that tally behavior is covered by the new selftest. Under the frozen contract's pre-data control rule, a control meeting the predicate requires redesign before data, rather than accepting this shortcut.

## Pristine / control / restored detector

The same bounded direct detector, `timeout --kill-after=5 300 bash tools/mutate-and-run.sh --selftest`, ran from the sandbox clone on all three byte states. All stderr was empty and no execution timed out.

| State | Exit | Actual final stdout lines |
|---|---:|---|
| pristine | 0 | `MUTATE_SELFTEST: 97/97 pass` / `VERDICT: PASS` |
| control | 0 | `MUTATE_SELFTEST: 98/98 pass` / `VERDICT: PASS` |
| restored | 0 | `MUTATE_SELFTEST: 97/97 pass` / `VERDICT: PASS` |

The control additionally printed `PASS case tally: known counter fixture spellings absent (text only)`. These direct selftest runs establish green pristine/restored baselines; the frozen counter was scored once on the committed control. No failed baseline is being counted as a killed mutant.

## Restoration evidence

| Byte state | SHA-256 |
|---|---|
| Pristine | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| Scored control | `698e1f8bdf3e5be8ae895491ef5bb947418e9df76ca60d4833abd4d6f43d04bb` |
| Restored, before detector | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| Restored, after detector | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |

Exact pristine/restored byte equality: `True`. Restored stdout equals pristine stdout byte-for-byte: `True`. The sandbox worktree source was restored; the scored commit and exported diff preserve the control.

Frozen counter SHA-256 before and after scoring: `5ed4e663ff16556d0bfef68a9fc1e3cf820ab8bc2b620169e800da914f0c8719` / `5ed4e663ff16556d0bfef68a9fc1e3cf820ab8bc2b620169e800da914f0c8719` (unchanged, matching the freeze).

## Receipts and bounds

- Committed diff: `.ufo/evidence/round-30/ctl/CtlK7Keyed.diff`.
- Full counter stdout, followed by final `exit=0`: `.ufo/evidence/round-30/ctl/CtlK7Keyed.stdout`.
- Full direct-detector stdout/stderr, argv, elapsed times and restoration record: `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK7Keyed/probe-receipts.json`.
- All explicitly launched processes were bounded with `timeout`; no background jobs or subagents were used. Final `/proc/*/cwd` scan found no live process under the owned sandbox. No timeout occurred.
- Only this report and the named `.diff`/`.stdout` were written in the lane. No lane/fleet Git write command, counter/contract edit, production edit, sibling edit, or `jj` command was run. Sandbox Git commands had `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset.
- No tools were installed or updated.
