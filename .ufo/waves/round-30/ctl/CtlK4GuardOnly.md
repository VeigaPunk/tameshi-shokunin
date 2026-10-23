CONTROL CtlK4GuardOnly: meets=false C1_R30_PASS=false

```text
C1_R30: rev=a5f1f41574c25c1e1b85123fdcbda1c1c7beb721 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4
PREDICATE: C1_R30_PASS=false
exit=1
```

Diff summary: `tools/mutate-and-run.sh`, +6/-0, only the proposed runtime completeness guard immediately before the PASS printf. No selftest case or other source change. The condition is `if (( npass + nfail + nsetup != nlegs )); then`; mismatch prints SETUP and the retained workdir, then exits 2. The insertion exactly follows `.ufo/waves/round-29/w1/MutateLegSum.md:175-195`.

**Result:** the expected separation is confirmed. Runtime refusal improves from `refused_drops=0/9` to `9/9`, while the runner's detector still kills `0/13` public-family mutants and `0/12` held-out mutants. The frozen counter rejects this runtime-only/no-detector control. Every mutant selftest exits 0 with `verdict_pass=1`: those mutants **survive** the runner detector; this is not a killed-mutant result. The whole predicate was already false at baseline, so its nonzero exit alone is not credited as a kill.

## Clauses and axes

Claim axis: **operability**. Probe dimensions: runtime completeness, detector sensitivity, preservation of equivalent behavior, and exact restoration. No round-admission or integration judgment is made here.

| Frozen clause | Required | K4 observed | Result |
|---|---|---|---|
| (a) pristine selftest | exit 0 and `VERDICT: PASS` | exit 0, `verdict_pass=1` | pass |
| (b) pristine fixed-status harness | 19/19 | 19/19 | pass |
| (c) runtime drop refusal | 9/9 | 9/9 | pass |
| (d) public-family selftest kills | 13/13 | 0/13 | **fail** |
| (e) public equivalent rewrites | 4/4 | 4/4 | pass |
| (f) held-out selftest kills | 12/12 | 0/12 | **fail** |
| (g) held-out equivalent rewrites | 4/4 | 4/4 | pass |

The runtime result covers the counter's two vectors for each drop (all-zero and dropped-leg-status-1). It establishes the assigned missing-leg false-PASS repair under that harness, not protection against every possible tally defect.

## Execution and actual outputs

Sandbox: `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK4GuardOnly/clone`.

The clone was detached at `e59728df5ebb053c9810049c05fd4e9d59d82dee`. The control was committed only in that sandbox as `a5f1f41574c25c1e1b85123fdcbda1c1c7beb721`, message `ctl`, identity `ctl <ctl@sandbox>`.

The same unchanged frozen detector was run synchronously on pristine, control, and restored revisions:

```text
timeout --kill-after=10s 900 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v2.py --repo /fast/scratch/hyaku/tameshi-r30/ctl/CtlK4GuardOnly/clone --rev REV
```

`GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset; cwd and TMPDIR were under this sandbox. No counter argument, source, contract, or predicate was changed.

| Byte state | REV | Runtime refusals | Public kills | Held-out kills | Other clauses | Exit |
|---|---|---|---|---|---|---|
| Pristine | `e59728df5ebb053c9810049c05fd4e9d59d82dee` | 0/9 | 0/13 | 0/12 | selftest=1, harness=19/19, equiv=4/4, heldout_equiv=4/4 | 1 |
| K4 control | `a5f1f41574c25c1e1b85123fdcbda1c1c7beb721` | 9/9 | 0/13 | 0/12 | selftest=1, harness=19/19, equiv=4/4, heldout_equiv=4/4 | 1 |
| Restored | `e59728df5ebb053c9810049c05fd4e9d59d82dee` | 0/9 | 0/13 | 0/12 | selftest=1, harness=19/19, equiv=4/4, heldout_equiv=4/4 | 1 |

Pristine and restored stdout were byte-identical:

```text
C1_R30: rev=e59728df5ebb053c9810049c05fd4e9d59d82dee pristine_selftest=1 harness=19/19 refused_drops=0/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4
PREDICATE: C1_R30_PASS=false
exit=1
```

Full control stdout, including all 34 selftest rows and the final exit line: `.ufo/evidence/round-30/ctl/CtlK4GuardOnly.stdout`. Exact committed diff: `.ufo/evidence/round-30/ctl/CtlK4GuardOnly.diff`.

Full pristine/control/restored stdout, stderr, argv, exits, elapsed times, and cleanup receipts remain in `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK4GuardOnly/{pristine,control,restored}.json`. Runs completed in 36.521 / 57.637 / 61.384 seconds respectively, with empty stderr and no timeout.

## Restoration and containment

The sandbox was detached back to the original revision before the restored detector run.

| Runner byte state | SHA-256 |
|---|---|
| Pristine before detector | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| K4 control | `d40c7dc33d5b3a56ed7f5ace2d71a050a022062620ab9d99e2060ad698c533ee` |
| Restored before detector | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| Restored after detector | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |

Exact restored/pristine byte equality was true. Frozen counter SHA-256 before and after all probes remained `5ed4e663ff16556d0bfef68a9fc1e3cf820ab8bc2b620169e800da914f0c8719`. Additional restoration evidence: `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK4GuardOnly/restoration.json`.

Each external invocation was bounded by timeout. Per-run cleanup found no remaining owned sandbox process to kill; the final owned-sandbox process scan returned `{}`. No background job, subagent, sibling-source edit, lane Git write, or `jj` command was used. Lane writes were limited to this report and the named `.diff` and `.stdout`. No tools were installed or updated.
