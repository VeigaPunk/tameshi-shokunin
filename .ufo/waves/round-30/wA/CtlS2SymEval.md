CONTROL CtlS2SymEval-11: v3_meets=true built=yes

## Verdict

Built the static symbolic evaluator control. The public v3 counter accepts it, exit 0. The detector computes all 19 fixed verdicts in its own Python model; it does not execute the extracted Bash tally block. The separate dropped-leg mutation probe was killed, and the original control bytes were restored exactly. v4 was not run here; its result remains for the L1.

Axis: operability. Guardrails: exact frozen tally bytes, model fidelity across equivalent spellings, and no execution of extracted shell text.

## Delivered artifacts

- Commit: `f6c7bb329268cb38f53f7e366c8a9a0789b65728`.
- Clone: `/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone`.
- Diff: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/wA/CtlS2SymEval-11.diff`.
- Diff SHA-256: `05474e630940e623cf490d121ff7315b5aa0f984166128a50d6ca15f619a6b24`.
- Committed runner SHA-256: `39085e6df74031ad7bf765917262cc2e96438dd32b289a6981a4442ed08f6eca`.
- Tally block SHA-256: `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`, identical to the frozen fix.

All code locations below refer to `tools/mutate-and-run.sh` in that clone and commit unless explicitly identified as the temporary mutation.

## Implementation evidence

- `tools/mutate-and-run.sh:1430-1468`: the frozen tally, including its completeness guard, is unchanged in the delivered control.
- `tools/mutate-and-run.sh:1987-2477`: only the frozen fix's behavioral selftest hunk was replaced. An embedded Python lexer and structural parser construct a model of loop operands, case arms, assignments, arithmetic, conditionals, printed output, and exit status. Status names are discovered independently from `st_*=$?` assignments preceding the tally.
- The model interprets the parsed structure under the all-zero vector and each of the nine single-leg status-1 and nine single-leg status-2 vectors. Acceptance requires exact equality of exit code and first output line for every vector.
- Arithmetic has its own parser and evaluator, including compound assignments, pre/post increments, comparisons, Boolean operators, and inserted arithmetic terms. No shell subprocess, shell evaluation, Python `eval`, or sourcing of block text is used by this detector. Existing, unrelated selftest cases still invoke Bash as before.
- Unsupported syntax is refused rather than delegated to a shell. This is a bounded shell-subset interpreter, not a claim to implement all Bash semantics.

## Commands and observed output

Working directory for code runs:

```sh
/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone
```

The clone was created and the frozen fix applied with:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11
timeout -k 5 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone
timeout -k 5 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone checkout -q --detach f09d3425258403a51422c9959e25340807982947
timeout -k 5 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone apply /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/witness/fix.diff
```

All returned exit 0 with no output. Before the control replacement, the fix's whole-runner SHA-256 was `9a931bc2d0c31c32dd3a4ccf6594b56c3474628cca513b675901a8666fbec7d4` and its tally hash was the frozen hash above.

### Same detector on pristine, mutated, and restored bytes

After creating `.scratch/tmp`, this exact bounded command was run three times: on the pristine control, on the single mutation described below, and after restoring it. Bubblewrap redirected `/tmp` into this clone, kept the remaining host filesystem read-only, and isolated the process namespace.

```sh
timeout -k 5 180 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bwrap --die-with-parent --unshare-pid --unshare-net --ro-bind / / --bind /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone --bind /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone/.scratch/tmp /tmp --proc /proc --dev /dev --chdir /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone bash tools/mutate-and-run.sh --selftest
```

Pristine control: exit 0.

```text
SYMBOLIC_TALLY: 19/19 model verdicts match; extracted shell executions=0
PASS tally symbolic evaluator: 19 fixed status vectors, no extracted shell execution
MUTATE_SELFTEST: 98/98 pass
VERDICT: PASS
```

Mutant: remove only `"$st_citecheck"` from the loop operands at `tools/mutate-and-run.sh:1431`. Expected detector: the same `--selftest` must exit nonzero because at least one modeled verdict differs. Actual exit: 1.

```text
SYMBOLIC_MISMATCH: statuses=[0, 0, 0, 0, 0, 0, 0, 0, 0] got=(2, 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)') want=(0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)')
SYMBOLIC_TALLY: 0/19 model verdicts match; extracted shell executions=0
FAIL tally symbolic evaluator: 19 fixed status vectors, no extracted shell execution
MUTATE_SELFTEST: 97/98 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.z7sAQs)
```

Restored control: exit 0, with the same four pristine output lines above. Verdict: **killed**, with a passing baseline and passing restored detector.

Hash command run on each state:

```sh
python3 -c "import hashlib,sys;t=open(sys.argv[1],'rb').read();s=t.find(b'  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n');e=t.find(b'\n}\n',s);print('tally_sha256='+hashlib.sha256(t[s:e+1]).hexdigest());print('runner_sha256='+hashlib.sha256(t).hexdigest())" tools/mutate-and-run.sh
```

| State | Whole-runner SHA-256 | Tally SHA-256 |
| --- | --- | --- |
| Pristine control | `39085e6df74031ad7bf765917262cc2e96438dd32b289a6981a4442ed08f6eca` | `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` |
| Mutated | `657da3b1f1650eda9c11e70430685ca9902d3234305e8fe9018d567cbb10feeb` | `6c94056c02f44b272bcc004a0fbeb75623e44317fcfb5e71a608d0dbe40d0b2d` |
| Restored | `39085e6df74031ad7bf765917262cc2e96438dd32b289a6981a4442ed08f6eca` | `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` |

### Commit and public v3 counter

```sh
timeout -k 5 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git add -- tools/mutate-and-run.sh
timeout -k 5 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c user.name=CtlS2SymEval -c user.email=ctls2symeval@shokunin.local commit -q -m 'Control: statically model tally verdicts without shell execution' -- tools/mutate-and-run.sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD
```

Observed exit 0; revision output:

```text
f6c7bb329268cb38f53f7e366c8a9a0789b65728
```

The counter command below was invoked with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed from the environment, using Python `subprocess.run` to capture its output. An initial asynchronous tool launch was refused before execution because the shared background-job limit was reached; the completed invocation was synchronous.

```sh
timeout -k 5 1500 bwrap --die-with-parent --unshare-pid --unshare-net --ro-bind / / --bind /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone --bind /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone/.scratch/tmp /tmp --proc /proc --dev /dev --chdir /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py --repo /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone --rev f6c7bb329268cb38f53f7e366c8a9a0789b65728 --jobs 4
```

Observed summary and exit:

```text
C1_R30: rev=f6c7bb329268cb38f53f7e366c8a9a0789b65728 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=true
COUNTER_EXIT: 0
```

Complete counter output is retained at `/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS2SymEval-11/clone/.scratch/v3.stdout`.

The required patch was exported from the successful, restored commit using `git diff f09d3425258403a51422c9959e25340807982947 HEAD -- tools/mutate-and-run.sh`, with its captured stdout written to the delivered diff path. Export exit: 0.

## Smallest safe correction

Keep this control scratch-only and retain the frozen fix's actual block-execution selftest in the production candidate. The v3 result establishes that matching these verdicts is not, by itself, evidence that the tally ran in Bash. If native block execution is the intended invariant, require independent execution evidence for that invariant rather than treating semantic-model agreement as execution evidence. Do not change the frozen counter or behavioral contract during this probe.

## Bounds and tools

No tools were installed or upgraded. Only this seat's clone, the named diff, and this report were written. No production runner or sibling source was edited, and no sealed-set content was accessed. All bounded code runs returned; the bubblewrap process namespaces have exited. No services, watchers, subagents, or additional runtimes were started. No process belonging to another seat was killed.
