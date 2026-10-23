# CriticC1 — pre-data adversarial review

Advisory review only; no runtime judgment or admission. Reviewed claim C1 frozen at `c31814978969a41a8e9b0f7d99fa308c5993c1b7`, not the concurrently changing implementation.

Axes: **operability** is the changed surface; **calibration** is the guardrail against overstating what the measurement establishes. No depth, coverage, freshness or adjacency gain is established by this review. Capability acquisition is a claim type, not a competing axis.

## 1. Axis fit and novelty

**Finding: operability fits; a reusable independent audit CLI could be a genuine capability acquisition, but the frozen measurement does not establish that acquisition.** This is not new tally knowledge or a coverage/depth gain merely because it scores new runner copies.

Evidence:

- Fleet `.ufo/prompts/tameshi-round-32.md:343-365`, especially `:361-365`, names the axis by the changed surface and distinguishes re-scoring an existing rule from moving a surface.
- Canonical `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:13,40-41,57-64` defines operability as runnable artifacts and capability acquisition as a demonstrated addition to the repertoire.
- `SCORECARD.md:1512-1526` already holds the mutation runner, regression replay and other instruments, but not an independent tally-audit CLI. `SCORECARD.md:1473-1480` records the earlier runner guard and its remaining survivors. `tools/mutate-and-run.sh:1989-2040` already executes its own tally against fixed vectors.
- `.ufo/evidence/round-32/contract.json:10-13,29-35` proposes a new standalone tool, explicitly claims no depth or calibration change, and bounds the claim against exhaustive runner-edit coverage. The committed baseline receipt, `before/c1-at-base.stdout:27`, reports no tool and `C1_R32_PASS=false`; I did not rerun that baseline.

Smallest safe correction: describe the new operation precisely as independent tally/harness auditing, not rediscovery of the tally rule. Do not treat the new filename or a passing finite classifier result as sufficient evidence that the operation was implemented; question 3 demonstrates the distinction.

## 2. Does leaving the runner untouched resolve the routed items?

**Finding: no, not as repairs to the runner. It can add an external detector, but it leaves the runtime per-leg defect and embedded selftest gaps in place.** That is an explicit preservation tradeoff, not an in-place resolution.

Evidence:

- `corpus/lessons/round-30-verifier-spotcheck.md:213-214` routes a runtime tally check beyond the sum and the eight MutateHead survivors. `corpus/lessons/round-31-verifier-spotcheck.md:202-203` says to land them or retire the route with a stated reason.
- `tools/mutate-and-run.sh:1432-1439,1453-1461` counts loop iterations and checks their sum, not equality between independently derived leg identities and loop operands. Duplicating one operand while dropping another preserves that sum.
- `.ufo/waves/round-30/wC/MutateHead.md:69-80,155-171` distinguishes the eight real survivor gaps from equivalent edits and gives behavioral witnesses. For N05 the demonstrated defect requires declared overcount stress; it is not an ordinary intact-loop failure.
- `.ufo/evidence/round-32/contract.json:12-13,35,47` requires byte-identical runner contents. Its predicate invokes only the new tool against copies; it does not require existing `--regression` or `--selftest` callers to invoke the audit first.

Smallest safe correction: retain the original runner-repair items as open, or explicitly retire that repair route because of the pinned-input constraint and name the external audit as its replacement mitigation. If operational protection is promised, document and exercise a guarded invocation, `audit && regression`, without claiming the runner's own selftest was repaired. A byte-identical runner cannot acquire a different embedded detector through a new unrelated entry point.

## 3. Cheap control that meets the frozen target

**Finding: demonstrated. A 27-line counter-reading acceptance allowlist met the entire frozen target twice without executing any runner tally, independent exit-status oracle or faulty-block harness panel.** This is not a Bash semantic implementation; it recognizes the public accepted fixture families and rejects everything else.

### Mechanism and source evidence

- `.ufo/evidence/round-32/c1-measure.py:140-168` publishes all accepted fixture constructors. Its generated accepted families are only operand permutations and two specially formatted nonce comments.
- `c1-measure.py:177-184` resets selected environment variables and uses Python `-I`, but supplies no filesystem isolation. `-I` does not make the counter, Git history or other files unreadable.
- `c1-measure.py:243-250` places all 26 runner copies together before invocation. **[INFERENCE]** A candidate can also inspect sibling copies; I did not exercise that alternative. Random filenames and shuffled execution (`:247,258-263`) do not close filesystem access or answer-family recognition.
- My control reads the frozen counter from its own clone and obtains the pinned runner with read-only `git show`. It imports `frozen_accept`, normalizes only the two known generated acceptance forms, and returns FAIL for every other input. It does not need the fresh seed, labels or a table of generated mutant hashes.

The complete sandbox control, committed as `d1b22ed864d7f02e8c6e1a3a98992da3affcf2d4`, is preserved here:

```python
#!/usr/bin/env python3
"""Adversarial control: recognize counter answers, not tally correctness."""
import argparse
from pathlib import Path
import re
import runpy
import subprocess
import sys

sys.dont_write_bytecode = True
LANE = Path('/fast/scratch/hyaku/tameshi-r32-seats/CriticC1/clone')
c = runpy.run_path(str(LANE / '.ufo/evidence/round-32/c1-measure.py'))
base = subprocess.check_output(
    ['git', '-C', str(LANE), 'show', c['PIN_REV'] + ':' + c['RUNNER']],
    text=True)
a = argparse.ArgumentParser()
a.add_argument('--runner', required=True)
text = Path(a.parse_args().runner).read_text()
answers = {body for _, body in c['frozen_accept'](base)}
normal = re.sub(r'^  # nonce [0-9a-f]{16}\n', '', text, flags=re.M)
accept = text in answers or normal == base
for m in re.finditer(r'^  for st in (.*); do\n', normal, flags=re.M):
    ops = re.findall(r'"\$(st_[a-z]+)"', m.group(1))
    if sorted(ops) == sorted(c['NAMES']) and c['loop_with'](ops) == m.group(0):
        accept |= normal[:m.start()] + c['LOOP'] + normal[m.end():] == base
print('TALLY_AUDIT: ' + ('PASS' if accept else 'FAIL'))
raise SystemExit(0 if accept else 1)
```

### Exact commands and observed output

All commands ran with cwd `/fast/scratch/hyaku/tameshi-r32-seats/CriticC1`. Setup:

```sh
timeout 180 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/clone && timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/clone checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed exit 0, no stdout/stderr. The bounded driver `run-control.py:10-40` cleared `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`, committed only the sandbox control, and ran the following commands. It was invoked as `timeout 220 python3 /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/run-control.py`, exit 0.

```sh
timeout 90 /usr/bin/python3 /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/clone/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/clone --rev d1b22ed864d7f02e8c6e1a3a98992da3affcf2d4 --work /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/counter-fresh --jobs 4
```

Observed exit 0, empty stderr. Final stdout line:

```text
C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1 seed=5cd48390d2449811 rev=d1b22ed864d7f02e8c6e1a3a98992da3affcf2d4 C1_R32_PASS=true
```

```sh
timeout 90 /usr/bin/python3 /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/clone/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/clone --rev d1b22ed864d7f02e8c6e1a3a98992da3affcf2d4 --work /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/counter-replay --jobs 4 --seed 0123456789abcdef
```

Observed exit 0, empty stderr. Final stdout line:

```text
C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1 seed=0123456789abcdef rev=d1b22ed864d7f02e8c6e1a3a98992da3affcf2d4 C1_R32_PASS=true
```

Full per-copy evidence: scratch `control-fresh.stdout:1-27`, `control-replay.stdout:1-27`, with corresponding `.stderr` and `.exit` files. Both runs killed every frozen and generated must-kill copy and accepted every must-accept copy. Only these two seeds were exercised.

Source fingerprint command:

```sh
sha256sum clone/.ufo/evidence/round-32/contract.json clone/.ufo/evidence/round-32/c1-measure.py clone/tools/mutate-and-run.sh
```

Observed exit 0:

```text
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  clone/.ufo/evidence/round-32/contract.json
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  clone/.ufo/evidence/round-32/c1-measure.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  clone/tools/mutate-and-run.sh
```

### Concrete failure outside the answer grammar

`probe-benign.py:9-12` obtained the pinned runner with `git show` and appended only `\n# harmless audit control comment\n`. This does not change Bash execution, the tally or its selftest harness. The same control rejected it:

```sh
timeout 20 python3 /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/probe-benign.py
```

The wrapper exited 0 and recorded the child command/output in `benign-witness.txt:1-3`:

```text
COMMAND: /usr/bin/python3 -I /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/clone/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CriticC1/harmless-comment.sh
EXIT: 1
TALLY_AUDIT: FAIL
```

The witness is not an additional frozen acceptance requirement. It establishes that this passing control is an answer-family classifier, not a general tally auditor.

Smallest safe correction: record this as the contract's control finding, not an alternate successful semantic audit. Do not amend the frozen counter or discard either observation. Denying only counter imports would not be a complete defense: the small public answer grammar can also be embedded.

## 4. Round size and one-command derivation

**Finding: the finite 18-kill/8-accept result is bounded and replayable; it is not a one-command proof of the three proposed audit mechanisms.** The scope is one closely related operation, not a requirement to repair the whole mutation runner. Actual implementation runtime was not measured here.

Evidence:

- `contract.json:13-20,23-32` gives a concrete finite predicate, revision-bound tool/runner bytes, a printed seed and an immutable kill rule.
- `c1-measure.py:213-240` reads the selected tool revision and pinned base runner through Git; `:274-277` derives the final result. Full history containing the pinned base is required, not merely a shallow checkout of the tool revision.
- `c1-measure.py:177-184,205,260-263` bounds each invocation at 600 seconds and defaults to four workers. My cheap control's two full runs completed, but that is not evidence of real-audit runtime.
- The exact seeded command above re-derives the observed finite result over the committed sandbox tool and runner with the counter checkout pinned. A command omitting `--seed` deliberately samples a new population. Random filenames and execution order are not seeded, so a replay claim should concern the declared result, not identical temporary paths or process scheduling.
- The counter checks the public output/exit classifications. It neither checks that each of the 256 statuses was actually exercised nor observes that the runner's harness was run against a fault panel. The stronger mechanism description is not identical to the behavioral predicate.

Smallest safe correction: retain REV, the counter revision/digest, seed, full stdout/stderr/exit and pinned base history. Describe the result as the finite benchmark it is. Do not infer exhaustive implementation behavior or automatic runner protection from its count.

## 5. Strongest objection and smallest safe response before real-tool data

**Finding: the strongest objection is demonstrated target reachability without the claimed auditing work.** The same measurement can report full success for the intended implementation and for a reference-answer classifier. This is a fixable measurement-design defect before freeze, not evidence that the task owner acted improperly.

Impacted axes: operability evidence cannot distinguish the new audit capability from fixture recognition; calibration is harmed if that result is described as repairing the unchanged runner or proving the three internal audit mechanisms. Leaving the runner pinned is a separate tradeoff: it preserves existing inputs but cannot simultaneously repair the embedded runtime/selftest route. These are matters for the canonical judge; this report does not issue its decision.

Smallest safe response **now, before real-tool data**:

1. Preserve the frozen claim and record the passing control and both seeds. `contract.json:6,31` forbids changing this counter/target after controls, and the binding addendum at `.ufo/prompts/tameshi-round-32.md:357-360` also bars changing the claim after any seat scores. A new sandbox rule must not be silently promoted into this claim's predicate.
2. Keep the original runtime repairs open or explicitly retire their route; distinguish independent audit detection from runner correction.
3. Supplemental evidence may exercise the actual tool with only its supplied runner and required runtimes visible, withholding the counter, contract, Git history, pinned reference and sibling copies. Review the committed implementation for an independent oracle and actual harness fault injection. Label this supplemental evidence, not an amendment to C1.

For a newly frozen measured claim, the smallest hardening against this exhibited control is that restricted input boundary plus independently varied benign equivalents outside the public nonce/permutation grammar. Isolation alone does not defeat an embedded reference allowlist, and finite behavior alone does not prove an execution method; a claim specifically about executing a mechanism needs evidence of that mechanism rather than a larger list of expected answers. This cannot be retrofitted as the rule for the already frozen C1.

## Bounds and handoff

Only this report and files under `/fast/scratch/hyaku/tameshi-r32-seats/CriticC1/` were written. Git writes occurred only in the private clone. No production tool, contract or counter was edited; no `jj`, judge, orchestration runtime or subagent was invoked. All started commands returned; no process was killed. No tools were installed or updated. No production regression, selftest, build, lint or formatter was run. The exercised checks are exactly the two frozen-counter control runs and the harmless-comment control probe above.

## Complete frozen-v1 control receipts

The L1 subsequently stated that C1 will be redesigned before real-tool data while preserving v1 and its receipts. This report records the frozen-v1 finding and does not assess a replacement counter. The complete tool source is preserved in question 3 above; both complete receipts follow.

### Fresh run

`control-fresh.exit`: `0`. `control-fresh.stderr`: empty. Complete `control-fresh.stdout`:

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gT08(arm=126) outcome=KILL exit=1 sha256=6794ed5799aef032 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN05(< nlegs) outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH03(form=0) outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH04(rc=$?) outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=3,dup=4) outcome=KILL exit=1 sha256=2c3c436dca27a71b last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN01(vector=3) outcome=KILL exit=1 sha256=c66c1ca66cf8ae0f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN02(true) outcome=KILL exit=1 sha256=29d0e2b6649efed2 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN03(or) outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gD01(drop=st_mado,dup=st_kagi) outcome=KILL exit=1 sha256=a5fd11aed87e1568 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=4c3e5d90c92e7903 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=014c2157e44c272e last='TALLY_AUDIT: PASS'
C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1 seed=5cd48390d2449811 rev=d1b22ed864d7f02e8c6e1a3a98992da3affcf2d4 C1_R32_PASS=true
```

### Seeded run

`control-replay.exit`: `0`. `control-replay.stderr`: empty. Complete `control-replay.stdout`:

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gT08(arm=231) outcome=KILL exit=1 sha256=ad45791a9b3e6c3c last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN05(< nlegs + 0) outcome=KILL exit=1 sha256=461cdc5f098398c4 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH03(form=1) outcome=KILL exit=1 sha256=c307192c9c04517f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH04(true) outcome=KILL exit=1 sha256=eceff075da31e6d4 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=8,dup=3) outcome=KILL exit=1 sha256=5ee347ccd54e3eaa last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN01(vector=2) outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN02(true) outcome=KILL exit=1 sha256=29d0e2b6649efed2 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN03(split) outcome=KILL exit=1 sha256=16566843890d60ab last='TALLY_AUDIT: FAIL'
COPY set=kill id=gD01(drop=st_claims,dup=st_kagi) outcome=KILL exit=1 sha256=71cd57b47372dce6 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=9e27877b0ea3629b last='TALLY_AUDIT: PASS'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=e00a6011160ab96e last='TALLY_AUDIT: PASS'
C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1 seed=0123456789abcdef rev=d1b22ed864d7f02e8c6e1a3a98992da3affcf2d4 C1_R32_PASS=true
```
