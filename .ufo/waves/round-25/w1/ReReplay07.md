# R23-REATTACK Replay07: row pin-disposition-selftest at lane c9ff09fb

## Verdict

**AGREE.** For the frozen round-23 bundle, the binding of `pin-disposition-selftest` holds at replay revision 496d212 and still holds at lane revision c9ff09fb.

- The receipt's argv, exit code and name are checked exactly, and its stdout token by containment. The bundle bytes are pinned, and the binder returns CLEAN on them.
- The frozen argv equals the registry row and the baseline SKILL cell. The expect (exit 0 and the token) follows the tool's own convention and literal (§1).
- The retained full output (1409 bytes, 19 PASS case lines, final line `SELFTEST: PASS (19/19)`) matches the receipt.
- Two limits apply to what CLEAN means. I list them as scope limits, not falsifications:
  1. The receipt's argv, cwd and revision are invocation parameters the harness copied. They are not independent observations.
  2. The observations copy of the run is not pinned, and the binder never reads it.
- I found no field-level false acceptance inside the pinned bundle for this row. The latent acceptances (an emptied `stdout_contains` after a re-pin, and an edited observations copy) are in §4 and §7.
- Nothing here authenticates the producer.

The original Replay07 seat died in round 23 before reporting. This is the re-attack, run against the frozen artifacts and checked again at c9ff09fb.

## 0. Scope, bounds, revisions

- Row: `pin-disposition-selftest` only.
- Frozen artifacts: `.ufo/evidence/round-23/`. Copied unchanged to `/tmp/r25-replay07/frozen-round-23`. The four files I hashed (bundle, expected, observations, requirements) match the lane (§10).
- Replay revision 496d212. `requirements.json` and `replay.py` were committed there at 14:41:18Z. The run window is 14:42:22.6Z to 14:44:58.8Z. The outputs `replay/bundle.json`, `replay/expected.json` and `replay/observations.json` were first committed in 8f66b5d at 14:46:12Z.
- Lane revision c9ff09fb. HEAD is 5b69fb23, one commit later (round-25 contract amendment). The worktree has an uncommitted edit to `tools/mte-interop.py`, which this row does not use.
- Not run: the registry command `python3 tools/pin-disposition.py --selftest`, any suite, and any gate or selftest in the lane. The binder ran only as a CLI on `/tmp` copies. No installs or upgrades (python3 stdlib only).

## 1. Frozen argv/expect against the baseline: exact

| Compared | Location | argv | expect |
|---|---|---|---|
| Frozen requirement | `.ufo/evidence/round-23/requirements.json:87-100` (name at :99) | `python3 tools/pin-disposition.py --selftest` | exit 0; `stdout_contains: ["SELFTEST: PASS"]` |
| Bundle requirement copy | `replay/bundle.json:683-696` (name at :695) | same | same |
| Observations requirement copy | `replay/observations.json:308` (requirement name) | same | same |
| Registry row | `tools/registry.json:131-` (name at :132); JSON-identical at 28cae179, 496d212, 336565fc, 8f66b5d, c9ff09f | same | same |
| Baseline SKILL | `SKILL.md@98bea7d:1552`, cited by the row's `source`; same text at `c9ff09f:SKILL.md:1552` | self-test cell: `python3 tools/pin-disposition.py --selftest` | verdict map "selftest 1 failed"; pinned values "literal selftest labels in tool" |

Checks (read-only python, run in the session):

- The requirements.json row equals the active row of `registry-baseline.json` (ordered list equality over all 43 rows): True.
- `bundle.requirements == requirements.json`: True.
- The SKILL cell does not spell out `SELFTEST: PASS`. The tool prints it at `pin-disposition-496d212.py:1329`, and the baseline designates the tool as the source of literal labels. The token is therefore self-referential by the baseline's own design.
- Exit 0 as pass is a convention. The SKILL cell names only the failure exit.

## 2. Receipt and runner output: full output, not tails

- Receipt, `replay/bundle.json:87-99`: argv exact; cwd `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`; revision `496d212bc46789cdf8cafab72978bdb7f4182963`; exit 0; stderr `""`; stdout 1409 bytes, 20 lines. Those lines are 19 `SELFTEST_CASE … PASS (…)` lines, 0 FAIL, and a final `SELFTEST: PASS (19/19)`.
- Observations pin row: runner `got` 0, `expect` 0, `held` true, `elapsed_s` 0.833, `kind` selftest, `status` active, `tags` ["baseline"]. Its `stdout` equals the receipt stdout byte for byte.
- `stdout_tail` also equals the full output. The runner keeps `TAIL_BYTES = 4096` (`registry-check.py:110`), and 1409 < 4096, so no truncation affects this row. Twelve other rows have tails that differ from their full output; this row is not one of them.
- The runner's needle check uses the full decoded stdout (`registry-check.py:717-718`). Its docstring says "over the retained tail" (`:36-38`), which is stale. The two readings are identical for this row.
- Across all 43 rows, the receipt and the observation agree on argv, cwd, revision, exit, stdout and stderr. Python compare reported no disagreement.
- Sibling self-report: `bundle.json:85` (row `pin-disposition-read`) reports `"tool_sha256": "331529ea…"`. That equals the git blob of `tools/pin-disposition.py` at 496d212. It is a self-report, so it supports consistency only.

## 3. Binder on the frozen bundle, and adversarial deltas

Control (C0), same argv shape as the lane gate `command-binding-frozen-clean-pinned`, run on `/tmp` copies:

```
python3 /tmp/r25-replay07/baseline/command-binding-c9ff09f.py --bundle /tmp/r25-replay07/frozen-round-23/replay/bundle.json --expected /tmp/r25-replay07/frozen-round-23/replay/expected.json --json
-> {"bundle_sha256": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}   (exit 0)
```

The 496d212 binder (`command-binding-496d212.py`, sha `d533dc1e…`) gives the identical line.

Deltas were run on copies in `/tmp/r25-replay07/demo`. "Re-pinned" means `expected.json` was regenerated over the changed bundle, using the same encoder `replay.py` uses.

| id | Change | Pin | Binder result |
|---|---|---|---|
| D1 | receipt argv `python3` changed to `/usr/bin/python3` | frozen expected kept | exit 2, `SNAPSHOT_TAMPERED` |
| D2 | same argv change | re-pinned | exit 1, `ARGV_MISMATCH` |
| D3 | receipt stdout `SELFTEST: PASS` changed to `SELFTEST: pass` | re-pinned | exit 1, `STDOUT_MISMATCH` |
| D4 | requirement `stdout_contains` set to `[]`; receipt stdout set to `unrelated output` | re-pinned | exit 0, `finding_ids: []` (accepted; §4) |
| D5 | `observations.json` pin row: argv and runner stdout rewritten to echo the token | bundle and expected untouched | exit 0, `finding_ids: []`. The binder never opens this file (§7). |
| D6 | `requirements.json` pin row: `stdout_contains` set to `[]` | bundle and expected untouched | exit 0, `finding_ids: []`. The binder never opens this file (§4). |

## 4. Field-level acceptance: what the binder accepts for this row

- Exact for the pinned bundle: name (dict key), argv (list equality, `tools/command-binding.py:103-104`), exit (integer equality; bool rejected), cwd and revision (equal to the bundle's own fields), and the stdout token (substring of full stdout, `:111-112`). D1 through D3 confirm each check fires.
- Latent: `stdout_contains: []` is a valid requirement. Validation uses `strings(…, nonempty=False)` (`command-binding.py:54-56`, applied at `:80`), and the check uses `get(…, [])` at `:111`. An emptied list silently drops the only stdout check. This needs a re-pin (D4). The frozen row is non-empty, so there is no current acceptance.
- Containment, not line-anchored (`:111`). For the tool's real output this cannot mislead. Its FAIL path prints `SELFTEST: FAIL` and returns 1 (`pin-disposition-496d212.py:1321-1327`), so a failing run never prints the PASS token.
- stderr is not evaluated (`:111` checks stdout only). The receipt stderr is empty here.
- Binder scope, as stated in its docstring (`command-binding.py:2-16`): exact name, argv, cwd, revision, exit and tokens over retained declarations. "The expected file … pins all bundle bytes." It does not claim producer authenticity, continuous checkout identity or cold reads. The round-23 frozen contract's population (`.ufo/evidence/round-23/contract.json:4-55`) covers bundle fields only.

## 5. Present versus inferred

**Present** (observed by the runner, or pinned bytes):

- Exit 0, full stdout and empty stderr come from the runner (`registry-check.py:693, 717, 725-726`) and are copied into the receipt (`replay.py:68-71`).
- Runner identity: `tools/registry-check.py` at 496d212 has sha `cba16646…`, equal to `observations.json` `runner_sha256`.
- Registry identity: `round-23/registry-baseline.json` has sha `ebd2e69a…`. That equals `requirements.json` `registry_sha256` and the 496d212 blob of `tools/registry.json`.
- Tool identity: `tools/pin-disposition.py` at 496d212 has sha `331529ea…`, matching the sibling self-report at `bundle.json:85`.
- Bundle bytes (`3d6c99b7…`) are recorded in three places:
  - `replay/expected.json:2`, written by the same run (see below);
  - `.ufo/evidence/round-23/reader-freeze2.json:8`, at lane revision 336565fc (committed 14:47:40Z);
  - the active registry row `command-binding-frozen-clean-pinned`, whose expect requires that sha. It was added in d2eaecd (round 24) and was not run here.
- `requirements.json` (`cd5205be…`) is recorded by `reader-freeze2.json:10` and `.ufo/evidence/round-24/source-refresh-entries.json:697`.

**Inferred** (invocation record, not observation):

- Receipt argv: `replay.py:62` and `:68` copy `list(row['argv'])`. Execution is inferred from code: `registry-check.py:676-678` calls `subprocess.Popen(row["argv"], cwd=cwd, …)` with no shell. No exec trace was retained.
- `python3` is bare, so PATH resolves it. No resolved path or version appears in any artifact. The runner_result keys are `elapsed_s, expect, got, held, kind, name, status, stderr, stderr_tail, stdout, stdout_tail, tags`. [INFERENCE, not tested] A different `python3` earlier on PATH would produce an identical receipt.
- Receipt cwd: `replay.py:62, 68` set it to `str(clone)`. The clone is gone (`test -e /tmp/tameshi-r23-replay-naxu6fzi` reports absent), so it cannot be re-verified.
- Receipt revision: `replay.py:32-33` resolves the requested rev, and `:50` checks out that rev. No HEAD is read after checkout in round 23. The round-24 successor reads clone HEAD and refuses a mismatch (`registry-replay.py:155-159`).
- `runner_sha256` (`replay.py:78`) hashes the lane's `tools/registry-check.py`, not the clone copy that executed. It equals the 496d212 blob, which is what the clone ran. That equality rests on the lane being at 496d212 at replay time. The commit order suggests this but does not record it. The round-24 successor hashes the clone copy (`registry-replay.py:163`).
- Measurement intervals: producer clock (`replay.py:59-63`). Consistent with elapsed_s, but not authenticated.
- "SELFTEST: PASS" as a pass signal and exit 0 as pass: the tool's own literal and a convention (§1).

**Not independent:** `replay/expected.json` is written by `replay.py:74-75` in the same run as the bundle. It pins bytes from generation onward. It does not authenticate the producer.

**Unpinned:** `replay/observations.json` (sha `a83d8a0b…`). `git grep` for the full sha at c9ff09f returns no match. The binder never opens this file.

## 6. Retrofill check (consistency only; rejected as authentication)

- 496d212 (11:41:18 -0300, i.e. 14:41:18Z) adds `requirements.json` and `replay.py`. The run starts at 14:42:22.6Z.
- 8f66b5d (11:46:12 -0300, i.e. 14:46:12Z) adds `replay/bundle.json`, `replay/expected.json` and `replay/observations.json`. The run ended at 14:44:58.8Z.
- `git log --name-status -- .ufo/evidence/round-23/replay` lists only 8f66b5d. No later commit touches `replay/*`.
- The worktree equals HEAD for round-23 paths (`git diff --stat HEAD -- .ufo/evidence/round-23` is empty for those paths).
- None of these commits modifies a round-22-or-earlier file that holds replay or receipt metadata for this row. The only round-22-or-earlier file they touch is `.ufo/evidence/round-21/coldread/ledger.json` (336565fc), a coldread ledger outside this row.
- The 43 row intervals are ordered, non-overlapping and inside the run window. The pin row spans 0.83317 s, and its `elapsed_s` is 0.833.
- Commit dates are author-supplied, so they count as consistency evidence only.

## 7. The concrete adversarial delta I keep, and the smallest safe correction

**Delta D5.** Rewrite the pin row's argv and stdout in `observations.json`, and leave `bundle.json` and `expected.json` untouched. The binder still reports exit 0 with no findings. `check()` reads only `--bundle` and `--expected` (`command-binding.py:117-118`), so the retained invocation and output copy sits outside every check. Today that copy matches the receipt on all 43 rows, so this is a coverage gap, not a current defect.

**Smallest safe correction** (recommended only; I did not edit production files):

- Pin `observations.json`'s sha in a gate that already runs. The registry row set is the natural place. Have that gate compare each observation's argv, cwd, revision, exit, stdout and stderr with its receipt.
- Optionally, have the binder reject an empty `stdout_contains` on pinned rows. The frozen row does not need this.

## 8. Lane revision c9ff09fb: does the finding still apply?

- **Row:** unchanged. The JSON is identical at 28cae179, 496d212, 336565fc, 8f66b5d and c9ff09f. It is still `status: active`, has no `superseded_by`, and no second row shares its name.
- **Registry:** append-only from 496d212 to c9ff09f. `git diff -U0 496d212 c9ff09f -- tools/registry.json | grep '^@@'` gives `@@ -925,0 +926,74 @@`.
- **Registry sha:** moved from `ebd2e69a` (28cae179, 496d212) to `afeb6cb6` (8f66b5d, 336565fc) to `a8f255f1` (c9ff09f). The live registry therefore no longer matches `requirements.json`'s `registry_sha256`. That is expected after an append. The frozen replay used its own copy (`ebd2e69a`).
- **Binder:** sha `d533dc1e` at 496d212, `9230c68e` at c9ff09f. The only hunk is `git diff 496d212 c9ff09f -- tools/command-binding.py` → `@@ -161,11 +161,12 @@`, which changes only the selftest fixture loader (it now also reads `round-24/extra-cases.json`). `evaluate()` and `check()` are unchanged, and both binder versions return the same CLEAN result on the frozen bundle.
- **Runner** `tools/registry-check.py` (sha `cba16646`) and **pin tool** `tools/pin-disposition.py` (sha `331529ea`): unchanged between 496d212 and c9ff09f.
- **HEAD 5b69fb23:** `git diff --stat c9ff09f HEAD` over the binder, the registry row and round-23 paths is empty.
- **Still applies:** the bundle-level binding holds (§3). The stronger statements in §4 and §7 apply as written.

## 9. Residual risks and gaps

- Interpreter identity: `argv[0]` is a bare `python3`. No resolved path or version is retained. [INFERENCE, not tested]
- The clone is gone, so cwd and checkout identity cannot be re-verified now.
- The stdout token is defined by the tool. The row confirms the tool's self-report, not an external specification.
- The byte pin is written by the same run. Its strength depends on the later repo records (§5) that repeat the same bytes.
- Retained observations are unpinned (D5).
- Not audited (out of scope): whether the 19 selftest cases are themselves correct; the other 42 rows; the append to `round-21/coldread/ledger.json` in 336565fc.

## 10. Commands and observed output (read-only unless noted)

```
sha256sum .ufo/evidence/round-23/replay/bundle.json .ufo/evidence/round-23/replay/expected.json .ufo/evidence/round-23/replay/observations.json .ufo/evidence/round-23/requirements.json .ufo/evidence/round-23/replay.py
  3d6c99b7…  bundle.json     0831c9c8…  expected.json     a83d8a0b…  observations.json
  cd5205be…  requirements.json     adb41716…  replay.py
git show 496d212:tools/registry-check.py | sha256sum            -> cba16646…   (= observations runner_sha256)
git show 496d212:tools/pin-disposition.py | sha256sum           -> 331529ea…
git show 496d212:tools/registry.json | sha256sum                -> ebd2e69a…   (= round-23/registry-baseline.json)
git show 496d212:tools/command-binding.py | sha256sum           -> d533dc1e…
git show c9ff09f:tools/command-binding.py | sha256sum           -> 9230c68e…
git show c9ff09f:tools/registry.json | sha256sum                -> a8f255f1…
git grep -n a83d8a0b53b6b51a6e2d445da5b99fd843586051b743908e43eff6ba947cfa16 c9ff09f -- .   -> (no output)
git log --name-status -- .ufo/evidence/round-23/replay          -> only 8f66b5d (A ×3)
test -e /tmp/tameshi-r23-replay-naxu6fzi                        -> absent
C0 binder control                                               -> exit 0, finding_ids []  (both binder versions)
D1..D6                                                          -> see §3 table
Intervals (python)                                              -> 43 rows ordered, non-overlapping, inside run window
Receipts vs observations (python, 43 rows)                      -> no disagreement
```

## 11. Disclosure and tooling

- One early `git status --porcelain -- tools/registry.json tools/command-binding.py tools/pin-disposition.py` in the lane ran without `GIT_OPTIONAL_LOCKS=0`. It is read-only in intent, but it may have refreshed the index stat cache. No content changed. Every later git call used `GIT_OPTIONAL_LOCKS=0`.
- The C0 control used the registry gate's argv shape against `/tmp` copies. I did not execute the lane registry row `command-binding-frozen-clean-pinned`.
- No tools were installed or upgraded. Python 3 stdlib only.
- Writes: `/tmp/r25-replay07` (scratch) and this report. Nothing else in the lane.

R23-REATTACK Replay07: AGREE
