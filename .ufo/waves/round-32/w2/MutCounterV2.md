Verdict: the exact-output behavioral detector killed 3 counter mutants and 5 survived. No baseline was inconclusive. A detector checking only `C1_R32V2_PASS` would distinguish none of the 8: every counter invocation exited 1 and printed `C1_R32V2_PASS=false`. All eight mutation targets were restored exactly.

# MutCounterV2

Axes: detector sensitivity, baseline specificity, restoration fidelity, operability.

## Scope and fixture evidence

All scratch paths below are relative to `S=/fast/scratch/hyaku/tameshi-r32-seats/MutCounterV2`. The only production-tree write was this report. No subagents were dispatched and no v2 execution used the real audit tool.

- Clone `S/c` began at `a4f718138bdad20de741faeca57891645e5a64d9`.
- First sandbox commit: `f1a5daaa94e746504d793b104b460d6f3a00ea02`, replacing `tools/tally-audit.py` with an always-FAIL control. Its complete behavior is `print('TALLY_AUDIT: FAIL always-fail fixture'); raise SystemExit(1)` (`S/c/tools/tally-audit.py:3-4`).
- Second sandbox commit / measured fixture revision: `3b8bacf06271b564b83b2bfe0cd20b53b3290ea7`, adding exactly three held-out JSON files, plus the scratch repository's required log entry:
  - `S/c/.ufo/evidence/round-32/heldout/valid-kill.json:7-11`: change status 1 from fail to pass; witness `[1,0,0,0,0,0,0,0,0]`.
  - `S/c/.ufo/evidence/round-32/heldout/valid-accept.json:7-11`: arithmetic whitespace and comment only.
  - `S/c/.ufo/evidence/round-32/heldout/invalid-accept.json:7-11`: status 42 incorrectly becomes pass. The full first-leg sweep must reject this alleged accept.
- The frozen counter and sibling v1 import were copied into the clone without modification. Separate probe mirrors under `S/probes/CASE/v2/c1-measure-v2.py` each imported their own unchanged `../c1-measure.py`.
- Before mutation, every probe mirror changed only `TOOL_SHA256` to the control's actual SHA-256, as instructed. This common fixture adaptation is not counted as a mutant. Each mutant then changed one behavior-bearing expression, assignment, or call.

Observed pristine classification (`S/results/base/pristine.stdout:1-3`):

```text
HELDOUT file=.ufo/evidence/round-32/heldout/invalid-accept.json valid=0 reason='accept copy tally differs from pinned on the sweep'
HELDOUT file=.ufo/evidence/round-32/heldout/valid-accept.json valid=1 set=accept id=MutCounterV2-valid-accept author=MutCounterV2
HELDOUT file=.ufo/evidence/round-32/heldout/valid-kill.json valid=1 set=kill id=MutCounterV2-valid-kill author=MutCounterV2
```

## Detector and exact commands

`S/probe-detector.py:15-20,45-68` is the same bounded behavioral detector in all three phases. It requires counter exit 1, the exact expected summary, three correct held-out validity classifications, and 28 copy outcomes, all `KILL`/exit 1 with the control's exact output. Counts must be v1 kill 18, v1 accept 8, held-out kill 1, held-out accept 1. It checks counter bytes before and after execution as well.

The negative counter result is the expected result of this deliberately inadequate control, not a failing detector baseline. All eight pristine detector exits were 0; all eight restored detector exits were 0.

Exact argument pattern launched by the detector (`S/probe-detector.py:33-38`), with `CASE` and `PHASE` expanded to each table case and `pristine`, `mutated`, `restored` respectively:

```sh
timeout --signal=TERM --kill-after=5s 180 python3 /fast/scratch/hyaku/tameshi-r32-seats/MutCounterV2/probes/CASE/v2/c1-measure-v2.py --lane /fast/scratch/hyaku/tameshi-r32-seats/MutCounterV2/c --rev 3b8bacf06271b564b83b2bfe0cd20b53b3290ea7 --work /fast/scratch/hyaku/tameshi-r32-seats/MutCounterV2/work/CASE-PHASE --seed 1 --jobs 2
```

The actual outer command for each combination was:

```sh
timeout --signal=TERM --kill-after=5s 210 python3 /fast/scratch/hyaku/tameshi-r32-seats/MutCounterV2/probe-detector.py --case CASE --phase PHASE
```

The eight independent cases ran concurrently within each phase. Every `--work` was fresh. `S/results/CASE/PHASE.json` records each fully expanded counter argv, its exit, summary, detector errors and before/after SHA-256. `S/results/{pristine,mutated,restored}-launches.json` records the fully expanded outer commands and observed detector output. There were 25 bounded counter runs: one initial base calibration and three phases for each of eight mutants.

An initial attempt to launch the base calibration through the shell tool with `async=true` was rejected with `Background job limit reached (100)`. It did not run a counter. The successful bounded subprocess runs above did not use that job queue.

## Single-edit mutants and actual output

Locations refer to the adapted pristine counter `S/probes/base/v2/c1-measure-v2.py`. Exact individual patches are preserved at `S/probes/CASE/mutation.patch`.

| Case / single edit | Exact observed mutated `C1_R32V2` line | Verdict |
|---|---|---|
| `m01-validity-skipped`: line 349, replace `validate(...)` with `apply_edits(text, h['edits'])` | `C1_R32V2: v1_kill=18/18 v1_accept=0/8 ho_kill=1/1 ho_accept=0/2 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=3b8bacf06271b564b83b2bfe0cd20b53b3290ea7 C1_R32V2_PASS=false` | Killed |
| `m02-witness-inverted`: line 229, vector comparison `==` becomes `!=` | `C1_R32V2: v1_kill=18/18 v1_accept=0/8 ho_kill=0/0 ho_accept=0/1 ho_invalid=2 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=3b8bacf06271b564b83b2bfe0cd20b53b3290ea7 C1_R32V2_PASS=false` | Killed |
| `m03-after-ignored`: line 396, remove `and after` from the final predicate | `C1_R32V2: v1_kill=18/18 v1_accept=0/8 ho_kill=1/1 ho_accept=0/1 ho_invalid=1 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=3b8bacf06271b564b83b2bfe0cd20b53b3290ea7 C1_R32V2_PASS=false` | Survived |
| `m04-minho-dropped`: line 69, `MIN_HO = 6` becomes `MIN_HO = 0` | `C1_R32V2: v1_kill=18/18 v1_accept=0/8 ho_kill=1/1 ho_accept=0/1 ho_invalid=1 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=3b8bacf06271b564b83b2bfe0cd20b53b3290ea7 C1_R32V2_PASS=false` | Survived |
| `m05-sandbox-direct`: lines 258-264, replace the bwrap command expression with `['timeout', '600', sys.executable, '-I', tool, '--runner', copy]` | `C1_R32V2: v1_kill=18/18 v1_accept=0/8 ho_kill=1/1 ho_accept=0/1 ho_invalid=1 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=3b8bacf06271b564b83b2bfe0cd20b53b3290ea7 C1_R32V2_PASS=false` | Survived |
| `m06-sha-dropped`: line 358, replace SHA comparison with `int(tool_blob.returncode == 0)` | `C1_R32V2: v1_kill=18/18 v1_accept=0/8 ho_kill=1/1 ho_accept=0/1 ho_invalid=1 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=3b8bacf06271b564b83b2bfe0cd20b53b3290ea7 C1_R32V2_PASS=false` | Survived |
| `m07-sweep-shortened`: line 186, `range(1, 256)` becomes `range(1, 32)` | `C1_R32V2: v1_kill=18/18 v1_accept=0/8 ho_kill=1/1 ho_accept=0/2 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=3b8bacf06271b564b83b2bfe0cd20b53b3290ea7 C1_R32V2_PASS=false` | Killed |
| `m08-other-is-kill`: line 391, kill count accepts `outcome in ('KILL', 'OTHER')` | `C1_R32V2: v1_kill=18/18 v1_accept=0/8 ho_kill=1/1 ho_accept=0/1 ho_invalid=1 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=1 rev=3b8bacf06271b564b83b2bfe0cd20b53b3290ea7 C1_R32V2_PASS=false` | Survived |

Direct output evidence:

- `S/results/m01-validity-skipped/mutated.stdout:1,33`: the invalid accept was admitted; invalid count fell to 0 and held-out accept denominator grew to 2.
- `S/results/m02-witness-inverted/mutated.stdout:3,31`: the genuine kill was rejected as `vector witness shows no difference`; held-out kill became `0/0`.
- `S/results/m07-sweep-shortened/mutated.stdout:1,33`: omitting status 42 from the first-leg sweep admitted the invalid accept.
- Surviving cases' exact summary is at `S/results/CASE/mutated.stdout:32`.

The five survivors are coverage findings for this small always-FAIL fixture, not evidence that the frozen contract should change. In particular, threshold and provenance predicate edits are masked by the control's failed accepts.

## Restoration evidence

The common adapted-pristine and exact-restored SHA-256 was:

```text
509ee7c30633918a4f347471cc9aec4ed5dbfca16a2281388208b02a5789e55f
```

| Case | Mutated SHA-256 | Detector exits pristine / mutated / restored | Exact original bytes restored |
|---|---|---|---|
| `m01-validity-skipped` | `90e055c235597a928eb3b2c621dfc947842bac92e09a75c7f3fa23e44728d0e7` | `0 / 1 / 0` | Yes |
| `m02-witness-inverted` | `5e89f9ac587ee75b8edfa8dfcfccdf0ae806c7112f0d231e659397ef44c91d7f` | `0 / 1 / 0` | Yes |
| `m03-after-ignored` | `717e9c0bdb2f8f60431299e3f56d0da3c2b83270e5bd23a918d5e4c24a7c5913` | `0 / 0 / 0` | Yes |
| `m04-minho-dropped` | `a5d7a45a105b926f8f23af863795c430f7b76dbe100790381031359a1a00b29f` | `0 / 0 / 0` | Yes |
| `m05-sandbox-direct` | `aad123f5432485cb784a4d12893b66a296605f40a97a0c64d8af71dc1e382bcf` | `0 / 0 / 0` | Yes |
| `m06-sha-dropped` | `29df690305e4ec3c170c9f06deba17f24ce4a52cfa8e0c6f67076a3bac1119b4` | `0 / 0 / 0` | Yes |
| `m07-sweep-shortened` | `09664367baefaeb4905cd5b50a3a74e8377ed3196f62618e432e301800007518` | `0 / 1 / 0` | Yes |
| `m08-other-is-kill` | `469471c9465df7f11722082635a47933b2a507413c5ac0429f80aaec1801316b` | `0 / 0 / 0` | Yes |

The initial and final hashes also matched for untouched inputs:

| Input | SHA-256 |
|---|---|
| Frozen v2 counter | `1ab9e9cf8e408f6230110ac42495da2b9c3f51236fe3a32754bd23524f7f7c94` |
| Imported v1 counter | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` |
| Scratch runner | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| Committed control tool | `57caea6660ba2fdd4dab02add9452e5126fc3a28c72a30c26f254002033f697d` |

The frozen v2 and v1 source files' hashes were compared with their production originals before running. `S/results/receipt.json` records all phase hashes, counter exits, detector exits, verdicts and final untouched-input hashes. Each restored phase again checked the detector and the on-disk bytes. No counter target retains a behavior mutation; the explicitly declared control-SHA adaptation remains in the probe mirrors only. The frozen mirrored counter in `S/c` remained untouched throughout.

A final `/proc/*/cwd` check found no remaining processes in this seat's scratch tree (excluding the receipt-writing interpreter itself). No processes were killed. No tools were installed or updated; pre-existing Python, bwrap and timeout were sufficient. The bounded bwrap prerequisite probe printed `sandbox available`.

## Smallest safe correction: add discriminating counter fixtures, not a rule change

The following are named fixture designs, **[INFERENCE] not executed in this assignment**. They would distinguish each survivor without using the real audit tool:

| Survivor | Fixture that would kill it | Expected difference |
|---|---|---|
| `m03-after-ignored` | `FT-after-same-commit`: a separate scratch history introducing the counter and at least 6 valid kill plus 6 valid accept files in the same adding commit. Use a literal fixture-only SHA codebook control, committed before evaluation and matching every seed-1 copy's expected verdict; keep pinned runner and matching control SHA. | All other gates pass, but `heldout_after_freeze=0`. Pristine counter exits 1 / false; mutant exits 0 / true. |
| `m04-minho-dropped` | `FT-minimum-1x1`: retain this fixture's 1 valid kill, 1 valid accept and excluded invalid accept, but replace always-FAIL with a literal fixture-only SHA codebook control that correctly classifies all seed-1 copies; adapt both counters to its SHA. | Every gate except the minimum is satisfied. Pristine exits 1 / false; mutant exits 0 / true. |
| `m05-sandbox-direct` | `FT-sandbox-marker`: retain these held-outs; use a control that emits FAIL/1 unless it can read a fixed harmless marker under this seat's scratch directory, in which case it emits PASS/0. Create the marker outside the sandbox; adapt both counters to this control's SHA. | The sandbox cannot see the marker and preserves the current expected all-KILL outputs. Direct execution sees it and produces ACCEPT outcomes, changing copy counts. |
| `m06-sha-dropped` | `FT-sha-mismatch`: retain the existing committed always-FAIL fixture, but supply both counter versions an intentionally nonmatching `TOOL_SHA256`. | Pristine reports `tool_sha_ok=0`; mutant reports `tool_sha_ok=1`. The exact-field detector kills it even though the overall predicate remains false. |
| `m08-other-is-kill` | `FT-other-exit2`: replace the fixture control with one printing `TALLY_AUDIT: FAIL fixture OTHER` and exiting 2; adapt both counters to its SHA. | Every copy is OTHER. Pristine counts no kills; mutant incorrectly counts all 18 v1 and the held-out kill as killed. |

Keep the frozen counter, minimum, provenance rule, sandbox and outcome contract unchanged. Do not treat this negative fixture's unchanged overall false result as coverage of those five gates.
