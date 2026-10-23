# MutateToolB

## Verdict

**Six mutants were killed by the assigned detectors; two survived both the tool's selftest and all public v1 families.** The survivors are test-coverage gaps, not failures observed in the pristine tool. Two supplemental inputs distinguish each survivor from pristine and restored bytes. No baseline failure or inconclusive result occurred.

Axes: **operability** (assigned); coverage and calibration are diagnostic lenses, not additional round claims.

## Scope and detector

Revision: `a4f718138bdad20de741faeca57891645e5a64d9`. All execution and mutations were confined to `/fast/scratch/hyaku/tameshi-r32-seats/MutateToolB/` (abbreviated `S` below). Production files were not mutated; the only lane write is this report. No subagents, v2 counter main, full regression, gates, package installs, or tool updates were run.

Executed clone commands, with working directory `S` after its creation:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/MutateToolB/c
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/MutateToolB/c checkout -q --detach a4f718138bdad20de741faeca57891645e5a64d9
cp c/tools/tally-audit.py tally-audit.py
timeout -k 20 1800 python3 -B probe.py
```

The last command completed in 978.47 seconds. `S/probe.py:137-159` imports the PUBLIC `.ufo/evidence/round-32/c1-measure.py` module without invoking its main, validates the pinned runner digest, and uses `random.Random(seed)` for seeds 1 through 5. For each seed it builds `frozen_kill + generated_kill`, then `frozen_accept + generated_accept`, preserving RNG consumption order. All 130 copies were actually executed per tool: 90 must-kill and 40 must-accept, including repeated frozen copies; no result caching.

Expected family detector: exit 1 plus a stdout line starting `TALLY_AUDIT: FAIL` for must-kill; exit 0 plus a stdout line starting `TALLY_AUDIT: PASS` for must-accept. Other outcomes would be inconclusive rather than credited as kills.

Every tool invocation uses this exact argv shape (`S/probe.py:74-105`):

```sh
timeout -k 5 300 /usr/bin/python3 -I TOOL --runner COPY
timeout -k 5 300 /usr/bin/python3 -I /fast/scratch/hyaku/tameshi-r32-seats/MutateToolB/c/tools/audit-mNN.py --selftest
```

Selftests use separate mutant copies under `c/tools/`, beside the pinned runner; canonical `c/tools/tally-audit.py` is never overwritten. Runs have separate scratch working directories, HOME and TMPDIR. Sixteen subprocess jobs are bounded concurrently. Exact argv, cwd, return code, elapsed time, stdout and stderr are recorded in `S/evidence/runs/PHASE/CASE.json`; public copy names, labels and hashes are in `S/evidence/fixtures.json`. Public module digest: `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` (`S/evidence/before.json:3`).

The same detector ran first on pristine bytes, then each mutant, then a shared byte-identical restored tool on the same copy paths. Pristine and restored each produced:

```text
cases=130 kill_correct=90 accept_correct=40 other=0 misses=0
TALLY_AUDIT_SELFTEST: 11/11 pass
```

Selftest exit was 0 in both controls. All public outcomes were recognized KILL or ACCEPT, with no timeout/OTHER outcome. Controls and full mutant outputs: `S/evidence/all-summaries.json` and per-phase summary files.

## Single-edit mutants and assigned-detector results

Source locations below are in pristine `tools/tally-audit.py`. Each mutant changes or deletes exactly one behavior-bearing line; exact diffs are retained as `S/evidence/mNN.diff`. “Misses” means incorrect fixture classifications out of the 130 public copies, not missed tool mutants. A mutant is killed when its selftest fails or its public classifications differ from passing pristine controls. Supplemental witnesses are excluded from this verdict column.

| Mutant | Single edit | Own selftest, observed exit | Public v1 misses | Assigned verdict |
|---|---|---|---|---|
| m01 | `check_harness:343`: remove `or good[1] != 0`, so a harness rejecting the reference is not rejected | 11/11 pass, exit 0 | 0 | **Survived** |
| m02 | `check_harness:347`: iterate `panel[:-1]`, omitting `status-3-passes` | 11/11 pass, exit 0 | 2 false accepts: `gN01(vector=3)`, seeds 1 and 5 | **Killed by v1 only** |
| m03 | `check_harness:351`: inspect `r[0] == 0` instead of `r[1] == 0` (cases versus failures) | 6/11 pass, exit 1 | 60 false accepts: frozen and generated H03/H04/H05/N01/N02/N03, all seeds | **Killed by both** |
| m04 | `run_harness:314`: inject `tblock=$AUDIT_INJECT` before extraction instead of after it; extraction overwrites the injected block | 9/11 pass, exit 1 | 40 false rejects: every must-accept copy | **Killed by both** |
| m05 | `run_harness:317`: failure predicate `$2 -ne 0` becomes `$2 -gt 1`, losing ordinary status-1 failures | 9/11 pass, exit 1 | 40 false rejects: every must-accept copy | **Killed by both** |
| m06 | `faults:264`: delete the `label` fault | 10/11 pass, exit 1 | 10 false accepts: H03 and generated H03, all seeds (generated forms 0,0,2,0,2) | **Killed by both** |
| m07 | `faults:273`: position-only fault loop uses `REF_NAMES[:4] + REF_NAMES[5:]`, omitting `ignore-alone-st_checklist` | 11/11 pass, exit 0 | 0 | **Survived** |
| m08 | `faults:288`: delete `setup-before-fail` | 11/11 pass, exit 0 | 6 false accepts: frozen N01, all seeds, plus seed-2 `gN01(vector=2)` | **Killed by v1 only** |

Actual selftest failures: m03 loses exit-only, swallowed-status and skipped-position 8/0/1 cases; m04/m05 lose pristine and reversed-operands acceptance; m06 loses exit-only. These exact `CASE ... PASS|FAIL` outputs are preserved in `S/evidence/runs/mNN/selftest.json`.

Example public kill of a selftest survivor: `S/evidence/runs/m02/s1-kill-14.json:17-27` records `gN01(vector=3)`, exit 0, and:

```text
CHECK harness PASS reference cases=8; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

Its pristine classification was KILL. Thus m02 is not credited as surviving merely because its own selftest stays green. The misleading 27/27 diagnostic remains unchanged by this single-edit mutant.

## Inputs that kill the two survivors

These are supplemental falsifiers, not additions to or revisions of any frozen counter. Both were exercised under the same timeout/exit/stdout detector on pristine, mutated and restored bytes.

### m01: a harness that rejects every reference result

Input: `S/witness-reject-good.sh`, sha256 `bba58091980a27d47303f676cfed5ac5caff689b74233559ddded351376cf9d5`.

Only the harness comparator at runner line 2006 is changed to `return 1`. The actual regression tally is unchanged. All harness tally checks fail, including the correct reference, so this runner must be rejected. It cannot receive credit merely for also rejecting faulty blocks.

Executed mutant command:

```sh
timeout -k 5 300 /usr/bin/python3 -I /fast/scratch/hyaku/tameshi-r32-seats/MutateToolB/m01.py --runner /fast/scratch/hyaku/tameshi-r32-seats/MutateToolB/witness-reject-good.sh
```

Observed control → mutant → restored:

```text
pristine: exit 1; CHECK harness FAIL harness rejects or cannot run the reference block ((9, 8))
m01:      exit 0; CHECK harness PASS reference cases=9; faults rejected=27/27
restored: exit 1; CHECK harness FAIL harness rejects or cannot run the reference block ((9, 8))
```

Final lines were respectively `TALLY_AUDIT: FAIL`, `TALLY_AUDIT: PASS`, `TALLY_AUDIT: FAIL` with their normal check summaries. Evidence: `S/evidence/runs/pristine/witness-reject-good.json:22-27`, `S/evidence/runs/m01/witness-reject-good.json:22-27`, and the matching restored receipt.

### m07: a skipped sole position masked by broader multi-status coverage

Input: `S/witness-skip4-multi45.sh`, sha256 `39e71981e71d12a3603ed4efba226b826cb8dbf399ca6f4bb6df53f0bb506362`.

The single-position loop at runner line 2013 becomes `0 1 2 3 5 5 6 7 8`, skipping position 4. A valid additional mixed-position vector is inserted after line 2024:

```text
0 0 0 0 1 1 0 0 0:1:REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
```

That added vector still rejects the unconditional `ignore-st_checklist` fault; only the distinct position-only `ignore-alone-st_checklist` fault exposes the missing sole-leg test. Without the additional vector, the unconditional fault would mask the omitted position-only panel member, so a simple skipped-middle-position fixture alone would not kill m07.

Executed mutant command:

```sh
timeout -k 5 300 /usr/bin/python3 -I /fast/scratch/hyaku/tameshi-r32-seats/MutateToolB/m07.py --runner /fast/scratch/hyaku/tameshi-r32-seats/MutateToolB/witness-skip4-multi45.sh
```

Observed control → mutant → restored:

```text
pristine: exit 1; CHECK harness FAIL reference cases=10; faults rejected=26/27; accepted: ignore-alone-st_checklist
m07:      exit 0; CHECK harness PASS reference cases=10; faults rejected=26/26
restored: exit 1; CHECK harness FAIL reference cases=10; faults rejected=26/27; accepted: ignore-alone-st_checklist
```

Final lines were respectively FAIL, PASS, FAIL. Evidence: `S/evidence/runs/m07/witness-skip4-multi45.json:22-27`, `S/evidence/runs/restored/witness-skip4-multi45.json:22-27`, and the matching pristine receipt. These observations establish that m07 is not merely an equivalent mutation.

## Restoration evidence

Common before and restored tool sha256:

`9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef`

| Mutant | Observed mutated sha256 |
|---|---|
| m01 | `073d4f86d33784258c5b94395dc1bd9215602ea09c88785b025064f68ca21e62` |
| m02 | `09908a5860085c6c86eb95fba92ef17ba966a85dfd9baf0d2e453eda19bd49ed` |
| m03 | `3feb5720941e039ee70cb9aaf7b34611b094d7121b2b8b39bd9dac727aa68779` |
| m04 | `22e350d2d0fccac531521f739eef23cdb3b13ce3bb72c165c2ed56224b6e788d` |
| m05 | `6d2cde15a23d9517c991634c0f7625bdab1d483939167855a075345935ec6ce6` |
| m06 | `f9b44a5a6a70094294a5828ad1a0e931ce3d282611c5e9aba896f6de668786b9` |
| m07 | `0aa1551979250a1375c29faa6f1616f1fb4f81354282325314c32493bf84b206` |
| m08 | `af94476cc847c7fa7b21a68f1e038da36c3baddc98f822f25253407144175ce2` |

`S/evidence/mutation-manifest.json:1-58` records before/mutated digests and diff paths. `S/probe.py:195-207` restores every `m01.py` through `m08.py` using exact-byte copies, removes all staged `c/tools/audit-mNN.py` files, records hashes, reruns the shared restored detector, and asserts no active subprocess handles remain. All child invocations were waited for; no timeout termination was needed.

`S/evidence/restoration.json:2-15` confirms every restored mutant and both pristine tool copies equal the common tool digest, and `staged_files_absent` is true. The runner before and after is exactly:

`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`

## Smallest safe correction

Add the two demonstrated must-reject harness inputs to the tool's selftest and to an explicitly versioned future detector expansion. Keep the current reference-acceptance condition and complete position-only fault panel intact. The public v1 families already expose the omitted status-3 and mixed FAIL/SETUP faults (m02/m08), but the tool selftest does not; adding those two existing public cases would close that narrower selftest gap as well.

Do not change the frozen tool, runner, public fixtures, counter contracts, or current measurement to erase these findings. No correction was integrated by this seat.
