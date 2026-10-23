# EquivFamilies — C1 pre-data equivalence control

## Verdict

**No equivalent must-kill value was found in the declared adversarial domain.** All 415 generated parameter configurations and all nine frozen copies have executed distinguishing witnesses: **424 killed case probes, zero survived, zero inconclusive**. These are witness-detector results, not a run of the C1 counter or a claim about the not-yet-written audit tool.

All eight must-accept copies were equivalent on the executed basis: 2,361 tally inputs and 19 harness conditions per copy, repeated on pristine, accepted and restored bytes. The source-level arguments below explain why the accepted transformations preserve behavior beyond the finite basis.

**Important boundary:** N05 and all three gN05 forms are equivalent on an intact nine-operand tally and its existing selftest. Their distinguishing witness requires the **explicitly contracted overcount stress**. Thus “none equivalent” is correct only with that declared stress included, not as a claim about ordinary nine-status executions alone.

Axis: **operability**. Probe dimensions: behavioral discrimination and exact-byte restoration. No production code, frozen counter, contract, Git index, or sibling scratch directory was changed. No integration or round judgment was performed.

## Evidence and execution

Paths used below:

- `S = /fast/scratch/hyaku/tameshi-r32-seats/EquivFamilies`
- `C = S/lane`, an isolated clone detached at `c31814978969a41a8e9b0f7d99fa308c5993c1b7`.
- `R = C/tools/mutate-and-run.sh`, pinned SHA-256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`.

The frozen inputs were opened before setup: `.ufo/evidence/round-32/c1-measure.py:49-168` defines the copy families, and `.ufo/evidence/round-32/contract.json:12-26` defines the stress and acceptance domain. Their observed SHA-256 values, identical in the production read-only source and C, were:

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  contract.json
```

After initializing S with `probe-config.json`, the successful setup command was:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/EquivFamilies/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/EquivFamilies/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed: exit 0, no stdout or stderr. An earlier attempt to use S as the command working directory before it existed was rejected by the tool before executing the command; no clone or source mutation occurred in that attempt.

The complete behavioral run, with working directory S, was:

```sh
timeout 1200 python3 -B /fast/scratch/hyaku/tameshi-r32-seats/EquivFamilies/probe.py
```

Observed: exit 0, 99.04 seconds, no stderr. Terminal summary:

```text
TOTAL mutants=424 killed=424 survived=0 inconclusive=0
ACCEPT copies=8 equivalent_on_basis=8 matrix_cases=2361 fault_panel=17
RESTORATION all_restored=1 before=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 after=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
```

### Construction and expected detector

`S/probe.py` imports **C's frozen counter module**, with bytecode writing disabled. It obtains the pinned runner through that module's read-only `git show`, then calls `frozen_kill`, `generated_kill`, `frozen_accept`, and `generated_accept`. The generated kill copies are not independent reimplementations of the mutations. `ReplayRng` supplies every valid parameter combination to the actual generator (`probe.py:80-98,230-259`). Other family draws stay fixed when a parameter is enumerated.

For each kill case, the same `detector.bash` and exact command run against `cases/NNN/runner.sh` on pristine, mutated and restored bytes:

```sh
timeout 30 bash "$S/cases/NNN/detector.bash" "$S/cases/NNN/runner.sh" "$S/cases/NNN/runtime"
```

The full argument-expanded command is recorded in every phase of `S/mutant-results.jsonl`. `INJECT_FAULT=1` is supplied for harness witnesses and `0` for direct tally witnesses. GIT_* variables are removed; HOME and TMPDIR remain under S. Four mutation probes run concurrently, each in its own case directory.

- **Tally witnesses:** execute the actual extracted `R:1432-1470` block in Bash under fixed statuses. The independent Python oracle classifies 0 as pass, 1 as failure, all other 0–255 exits as setup; failure takes precedence over setup; an all-pass count other than nine is refused. The wrapper fixes `auto=0 KEEP=1`, so the tally does not remove directories.
- **Harness witnesses:** execute the actual source section `R:1992-2040`, retaining the actual `st()` accounting (`R:1482-1490`). Immediately after the harness extracts its tally block, replace only that in-memory block with a declared faulty block. The fault, source extraction, comparisons, singleton loop, multi-status vectors and guard stress then execute in Bash (`probe.py:100-151`). This is not a rewritten model of the harness.
- **Healthy baseline criterion:** direct tallies must match their oracle exit and line. A harness deliberately given a faulty tally must reject it, exit 1; that expected rejection is a healthy baseline, not a baseline detector failure. Natural and healthy-block harness controls must exit 0. Any unexpected baseline result, timeout, stderr, or restoration mismatch is inconclusive rather than killed (`probe.py:266-317`). None occurred.

No full `--regression` or full `--selftest` execution is claimed. These are bounded executions of the requested behavior-bearing sections on generated runner copies; all work and runtime files stayed under S.

## Exhaustive family table

Status positions follow the independent assignment order:

```text
0 st_js; 1 st_kagi; 2 st_tsu; 3 st_mado; 4 st_checklist;
5 st_claims; 6 st_roundgate; 7 st_sourcescheck; 8 st_citecheck
```

`H(a/b)` below means the exact terminal stdout `PROBE_HARNESS: a/b pass`. Restored exit, complete stdout and stderr matched pristine for every row. Each listed parameter value was executed, not merely sampled.

| Family | Parameter values checked | Equivalent values found | Witness and observed pristine → mutant |
|---|---|---|---|
| T08 | Frozen arm 4; 1 copy | None | `4 0 0 0 0 0 0 0 0`: exit 2, SETUP passed=8/cannot-verify=1 → exit 0, PASS passed=9. |
| N05 | Frozen `< nlegs`; 1 copy | None **with overcount stress** | Nine zero statuses, duplicate the last operand to make ten iterations: exit 2, mismatch counted=10 → exit 0, PASS passed=10. |
| H03 | Frozen exit-only comparison; 1 copy | None | Change tally field `passed=%s` to `passing=%s`, preserving exits: exit 1, H(2/9) → exit 0, H(9/9). |
| H04 | Frozen trailing `rc=$?`; 1 copy | None | Drop the final tally operand: exit 1, H(1/9) → exit 0, H(9/9). |
| H05 | Frozen P=8, Q=7; 1 copy | None | Singleton-only normalization at P=8, defined below: exit 1, H(7/9) → exit 0, H(9/9). |
| N01 | Frozen mixed vector deletion; 1 copy | None | Put SETUP before FAIL in the faulty tally: exit 1, H(8/9) → exit 0, H(8/8). |
| N02 | Frozen stress `&&` → `||`; 1 copy | None | Remove the tally completeness guard: exit 1, H(8/9) → exit 0, H(9/9). |
| N03 | Frozen comparison `&&` → `||`; 1 copy | None | Change only FAIL's `exit 1` to `exit 0`, retaining exact output: exit 1, H(6/9) → exit 0, H(9/9). |
| D01 | Frozen drop st_citecheck, duplicate st_js; 1 copy | None | `0 0 0 0 0 0 0 0 1`: exit 1, FAIL passed=8/failed=1/setup=0 → exit 0, PASS passed=9. |
| gT08 | Every K=2..255; **254** values | None | `K 0 0 0 0 0 0 0 0`: exit 2, SETUP passed=8/cannot-verify=1 → exit 0, PASS passed=9, for every K. |
| gN05 | `< nlegs`, `< nlegs + 0`, `<= nlegs - 1`; **3** forms | None **with overcount stress** | Same ten-zero-iteration stress as N05: exit 2, mismatch counted=10 → exit 0, PASS passed=10 in all three forms. |
| gH03 | Exit-only; exit plus nonempty output; exit plus first-11-character comparison; **3** forms | None | Same `passing=%s` fault: exit 1, H(2/9) → exit 0, H(9/9) in all three forms. The correct 11-character prefix `REGRESSION:` remains intact. |
| gH04 | Trailing `rc=$?`, `true`, `:`; **3** forms | None | Same dropped-operand block: exit 1, H(1/9) → exit 0, H(9/9) in every form. |
| gH05 | Every ordered (P,Q), P,Q in 0..8 and P≠Q; **72** pairs | None | Singleton-only normalization at the omitted P: exit 1, H(7/9) → exit 0, H(9/9), for every Q. |
| gN01 | Deleted vector indices 0,1,2,3; **4** values | None | Respectively weaken FAIL to `nfail == 1`, weaken SETUP to `nsetup == 1`, put SETUP before FAIL, or count status 3 as pass. Each: exit 1, H(8/9) → exit 0, H(8/8). |
| gN02 | Stress expression changed to `||`; stress call replaced by `true`; **2** forms | None | Same missing-guard block: exit 1, H(8/9) → exit 0, H(9/9) in both forms. |
| gN03 | Single-test OR; split-test OR; **2** forms | None | Same correct-line/wrong-exit FAIL block: exit 1, H(6/9) → exit 0, H(9/9) in both forms. |
| gD01 | Every ordered (i,j), i,j in 0..8 and i≠j; **72** pairs | None | Set only dropped status i to 1, all others 0. Pristine: exit 1, failed=1/passed=8; mutant duplicates zero-valued j: exit 0, PASS passed=9. |

The primary output table is independently recoverable from `S/summary.json:9-148`. Per-copy parameters, commands, every raw output, verdict and full SHA-256 values are in `S/mutant-results.jsonl`:

| Family | JSONL lines |
|---|---|
| Frozen nine, table order | 1–9 |
| gT08 K=2..255 | 10–263 |
| gN05 forms 0,1,2 | 264,267,270 |
| gH03 forms 0,1,2 | 265,268,271 |
| gH04 forms 0,1,2 | 266,269,272 |
| gH05 all pairs | 273–344 |
| gN01 indices 0..3 | 345–348 |
| gN02 true, OR | 349,351 |
| gN03 split, OR | 350,352 |
| gD01 all pairs | 353–424 |

### Exact direct-tally output witnesses

T08/gT08, pristine and restored:

```text
REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
REGRESSION_WORKDIR: probe-tally (kept)
```

T08/gT08 and D01/gD01, mutant:

```text
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: probe-tally (kept)
```

D01/gD01, pristine and restored:

```text
REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
REGRESSION_WORKDIR: probe-tally (kept)
```

N05/gN05 overcount stress, pristine and restored:

```text
REGRESSION: SETUP (case-tally mismatch: cases=9 counted=10)
REGRESSION_WORKDIR: probe-tally (kept)
```

N05/gN05 overcount stress, mutant:

```text
REGRESSION: PASS (cases=9 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: probe-tally (kept)
```

### Why every H05 pair has a witness

The same P-specific faulty block works for all eight possible duplicate positions Q. Immediately after counter initialization, inject:

```sh
if (( (st_P == 1 || st_P == 2) && (sum_of_other_eight_statuses) == 0 )); then
  st_P=0
fi
```

Here `st_P` and the sum are expanded to the actual nine assignment names in each saved `S/faults/singleton-P.block` (`probe.py:104-108`). This wrongly normalizes only an isolated status 1 or 2 at P. The pristine harness exercises P and rejects both singleton families. The mutant omits P and repeats Q, obtaining nine successful calls while exercising only eight positions.

The restriction is important for P=0 or P=1: an unconditional normalization at either position can also be caught by a retained multi-status vector, so it is not a valid all-P witness. The declared singleton fault leaves the two-failure, two-setup and mixed vectors intact; status 3 is also untouched. The difficult boundary P=0,Q=1 was actually observed at `mutant-results.jsonl:273`: pristine exit 1, H(7/9); mutant exit 0, H(9/9).

### N05 equivalence boundary

For the intact tally loop, every iteration increments exactly one counter, so the sum is always nine. Each gN05 predicate is false at nine, just like `!= nlegs`. The existing harness only deletes an operand; at eight all three weakened guards still reject. No ordinary nine-status vector distinguishes this family.

At ten zero-valued iterations, `10 != 9` is true, whereas `10 < 9`, `10 < 9 + 0`, and `10 <= 9 - 1` are false. That is the executed witness and is explicitly inside C1's planned “overcount/undercount stress” domain (`contract.json:12`). Rejecting this weakness does not require pretending an intact nine-leg execution overcounts. If stress were excluded, all three generated forms and the frozen N05 would be equivalent under the narrower reading.

## Must-accept equivalence

The eight actual acceptance copies were constructed by the counter. The two generated copies used seed **0xc132e9f041**. Each copy, before and after restoration, produced:

```text
ACCEPT_TALLY: cases=2361 mismatches=0
```

Exit 0, empty stderr. The 2,361 tally cases were: 256 statuses at every one of nine positions (2,304), all 55 feasible (failure-count, setup-count) pairs at nine legs, and all-zero undercount and overcount stresses. This is an executed basis, not an assertion that 256^9 vectors were enumerated.

Each acceptance copy also produced `PROBE_HARNESS: 9/9 pass`, exit 0, on its natural tally and on an injected healthy tally. It rejected all 17 injected faulty blocks, with exactly the pristine exit, complete stdout and stderr. The panel comprised bad label, dropped operand, all nine singleton-P faults, two-failure weakness, two-setup weakness, mixed precedence, status-3-as-pass, missing guard and FAIL-exits-zero. These 19 harness conditions were repeated on pristine, accepted and restored bytes (`probe.py:320-351`). Complete receipts are `S/accept-results.jsonl:1-8`.

| Copy | Behavioral equivalence argument | Observed result |
|---|---|---|
| B0-pristine | Identical bytes. | Equivalent on all executed conditions. |
| B1-T07 | Both positive failure and setup counts exit before the guard (`R:1441-1452`), so both terms are zero whenever the guard runs. The full sum comparison and `npass != nlegs` are then identical, including undercount/overcount stress. | Equivalent on all executed conditions. |
| B2-reversed | Each status contributes once to exactly one integer counter. Reordering these independent increments preserves the three totals and output. The harness's missing-operand stress uses all-zero statuses, so which zero-valued operand is removed is immaterial. | Equivalent on all executed conditions. |
| B3-decoys | Added lines are Bash comments outside the tally and selftest sections; the actual extraction anchors and commands are unchanged. | Equivalent on all executed conditions. |
| B4-cosmetic | Spaces inside arithmetic expansion and a trailing comment do not change the `npass + 1` expression. | Equivalent on all executed conditions. |
| B5-renamed | All six `tgot` occurrences are consistently renamed to a previously unused local `tcount`. The loop accumulator's declaration, update, comparison and diagnostic references retain their binding. | Equivalent on all executed conditions. |
| gB6-permuted | Same commutative-count argument as B2 for every generated permutation. The harness stress still removes one zero-valued operand. | One generated permutation executed; equivalent on all conditions. |
| gB7-nonce | Both variable nonce values occur only in comment lines, one in the tally and one after `tblock_full` initialization. Neither changes Bash commands, extraction or the missing-operand edit. | One generated nonce pair executed; equivalent on all conditions. |

All possible generated permutations and nonce strings are covered by those source-level arguments; they were **not** all instantiated. In contrast, every finite generated must-kill parameter value named in the assignment was instantiated and run.

## Restoration and hashes

Every exercised `cases/NNN/runner.sh` and `accept/NN/runner.sh` was restored in a `finally` block before its restored detector phase (`probe.py:283-351`). All 424 kill baselines and all eight acceptance baselines were healthy. All restored detector outputs matched pristine exactly. C's runner was never edited and its independently recorded initial and final SHA-256 were both:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
```

That same full hash is the before and after value in every case receipt. Full mutated hashes for every generated value are retained in `S/plan.json` and `S/mutant-results.jsonl`; immutable `cases/NNN/mutant.sh` files retain the constructed payloads for inspection, separate from the restored execution targets.

The nine frozen payload hashes, in report order:

```text
T08 12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b
N05 e1ef181c1e621962cf19574a0683109ee094387306af1766df14b215413929fe
H03 2ac4ce5344e6100a5980a2d44bbc4983562df5a0325ecf84610973094322f35c
H04 0dc1e6b07452f6108f9dd7f99050aa0d8b8450456c3424f22da1a7fc54e5d6cd
H05 adf6763d6524f342b5496ff52f0fce96e0b4a00b5ab26cfa43be2001654b36d0
N01 c0a32ec4e69d3cb07a7949efb7c9a83ac2b4b431f6e4da3f8bd76a1cd0d4cb34
N02 31128639afc3e57a0d68f0abe94cc5038954ff41d6f9949da4fa903331f56250
N03 741907e82ca7e907881cb985b7a504771de78d14b1179530661066a8f22a5b6f
D01 71a66c5a611d408fe08c3618a18f30fe6d4e43308e36ee1f074420547c4f695c
```

Observed evidence-digest command, working directory S:

```sh
sha256sum probe.py plan.json summary.json mutant-results.jsonl accept-results.jsonl
```

```text
f2cd75f8fe7e08275b8cd079ea12ddd0a547c4331ac04672f00b1bc9bfd198df  probe.py
9c95e474b88727871b25455ef8487890b99b76da32b7282d7eadc46de45331dc  plan.json
6a07672f28fb9a68bd255cce734b277fa84e219c7b66990e896afd5e76e4ce5b  summary.json
63797d9d6649be01b634f89ac0c81c8ed5d9ce9c5f692e6a9b24e36c53d56016  mutant-results.jsonl
3619941e891d441336937333395f27e8ef3516b1f41134f14309d86a8b13d140  accept-results.jsonl
```

All detector subprocesses completed under their timeouts; no background services were started. The driver joined every worker before returning. Installed or updated tools: **none**. Existing versions observed: GNU Bash 5.3.20(1), Python 3.14.8, Git 2.56.0. `df -h /fast` reported 113G available before the probe.

## Smallest safe correction

**No correction to the frozen counter or contract is indicated by this equivalence probe.** Keep the planned explicit overcount stress: ordinary nine-leg status tests cannot distinguish N05. For H05 coverage across every P, use the declared singleton-only P-specific faults (including P=0 and P=1), rather than assuming unconditional normalization is an escaping fault at every position. Preserve acceptance of comments, operand permutations, the T07 guard rewrite and the consistent harness-local rename.
