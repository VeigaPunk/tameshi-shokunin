# ReReplay18 — re-attack of round-23 Replay18 (row `mutate-and-run-regression`)

## Verdict

FINDING (one concrete counterexample, against the binding, not against the frozen row's data).

- The static binding of argv and expect is exact. The frozen requirement, the source registry and the receipt all agree byte-for-byte, the full stdout is retained (not just a tail), and the frozen bundle binds CLEAN.
- Counterexample: the replay projection (`.ufo/evidence/round-23/replay.py:66-71`) drops the registry runner's `held`/`cleanup_error` result. A run that `tools/registry-check.py` marks as **differs**, because process-tree cleanup failed, projects to a **byte-identical** receipt. `tools/command-binding.py` then binds it CLEAN. In round 23 this row really held, so no actual false acceptance occurred. The gap is reachable, and nothing in the bundle or in `command-binding.py` closes it.
- The finding still applies at lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`. The row is unchanged and active, and `evaluate()` is unchanged.

## What was checked (evidence present)

1. **Frozen requirement = source registry, at every relevant revision.**
   - `requirements.json` row 18 is `{"argv":["bash","tools/mutate-and-run.sh","--regression"],"expect":{"exit":0,"stdout_contains":["REGRESSION: PASS"]}}`.
   - It equals the bundle requirement and the `observations.json` row-17 `requirement` (Python equality: True/True).
   - `git show <rev>:tools/registry.json | sha256sum` gives `ebd2e69a…` at both `28cae17` (the source revision) and `496d212` (the replay revision). That matches `requirements.json.registry_sha256`.
   - The registry row is the same at `28cae17` and `c9ff09f`: `"timeout_s": 900, "source": "SKILL.md@98bea7d:1810", "status": "active"`. It is not superseded.
2. **Receipt fields vs observation (full streams).**
   - Bundle receipt and `observations.json.rows[17]` agree: argv equal, cwd equal, exit `0` == `got 0`, stdout equal (6370 chars, full), stderr equal (empty).
   - `stdout_tail` (4096 chars) is a strict suffix of the full stdout, so the full stream is retained, not reconstructed from a tail.
3. **Token is the real summary line.**
   - `REGRESSION: PASS` occurs exactly once, on `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`.
   - In source, `--regression` reaches `exit 0` only after that printf, with `nfail=0` and `nsetup=0`, which forces `npass=8` (`tools/mutate-and-run.sh:1354-1384`). Every other path exits 1, 2 or 64.
   - So, at this source, exit 0 plus the token implies all 8 legs passed.
4. **cwd is corroborated by the output, not only declared.**
   - `SELF=$(readlink -f "${BASH_SOURCE[0]}")` (`mutate-and-run.sh:170`) is printed as `REGRESSION_TOOL: /tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin/tools/mutate-and-run.sh`.
   - The argv uses a relative path, so this matches the receipt cwd.
   - `REGRESSION_PIN repo=/tmp/tameshi-r23-replay-naxu6fzi/fleet/<sibling>` matches the symlinked fleet in `replay.py:51-53`.
5. **Time is consistent.**
   - `REGRESSION_DATE: 2026-10-21T14:42:36Z` falls inside the row interval 14:42:36.516746 to 14:44:34.673369.
   - `elapsed_s 118.157` equals end minus start, and is under `timeout_s 900`.
6. **Revision is inferred, not evidenced by output.**
   - The receipt `revision` and the bundle `revision` are both copied from one variable (`replay.py:32,63,66`), so `REVISION_MISMATCH` cannot fire on a replay-produced bundle.
   - The stdout tool hash `d22c4025…` matches `git show 496d212:tools/mutate-and-run.sh`, but it matches `1f73157` and `c9ff09f` identically too. The output therefore cannot tell these revisions apart.
   - Delta D2 below relabels both revisions to `1f73157…` and binds CLEAN.
   - This is producer authentication, which is out of scope and rejected as a finding. It is recorded here only as "inferred from the instrument's checkout path (`replay.py:50`), not present in retained output".
7. **No historical metadata retrofill.** The observations carry per-row measurement intervals written at run time (`replay.py:59-63`), and the docstring forbids filling into historical observations. No retrofill was found.

## Counterexample (D1) and other deltas

Commands were run in scratch `/tmp/rereplay18.th75ge`, against copies of `command-binding.py` from `496d212` (`d533dc1e…`) and `c9ff09f` (`9230c68e…`).

- **Frozen bundle, both versions:**
  - Command: `python3 cb-*.py --bundle bundle.json --expected expected.json --json`
  - Observed: `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": []}`, exit 0.
- **Reprojection check:** applying the `replay.py:66-71` formula to `observations.json` reproduces `bundle.json` byte-for-byte (True).
- **D1 (cleanup leak):**
  - Set `rows[17].runner_result.held=False` and `cleanup_error="row descendants remain after bounded cleanup"`. This is the exact state `registry-check.py:720,729-731` produces when descendants survive.
  - The reprojected bundle is byte-identical to the frozen one (True). Both versions report `exit 0, finding_ids []`, `bundle_sha256 3d6c99b7…`.
  - The registry semantic is `held = got == expected_exit and not missing and cleanup_ok` (`registry-check.py:720`). The binding sees only exit and tokens, and its strict receipt key set (`command-binding.py:88`) cannot even carry the cleanup result.
  - This matters for this row specifically. `--regression` fans out 8 legs of mutant suites (`node`/`bash`, sandboxed sub-shells; `mutate-and-run.sh:1314-1352`), which is exactly the process-tree shape the cleanup check guards.
  - Round-23 actual state: every row has `held: true` and none has `cleanup_error` (checked over all 43 rows). Replay stdout `.ufo/evidence/round-23/replay-command-A.json` shows `mutate-and-run-regression 0 True`. The round-23 gate itself (`replay-gate-A.json`) ran `command-binding.py` alone.
- **D2 (revision relabel):** setting all revisions to `1f7315732e0cfe0b…` gives exit 0 and CLEAN. Disposition: producer authentication, out of scope (see point 6 above).
- **D3 (token-only):**
  - Receipt stdout set to `REGRESSION: FAIL (cases=8 passed=7 failed=1 setup=0)\nREGRESSION: PASS (cases=0 passed=0)`, with exit 0. Result: CLEAN.
  - The token does not bind the leg count or the absence of FAIL. Current source cannot reach this state (point 3), so this is a tradeoff, not a defect. It belongs to R23-ROUTED-1's multi-token fixture.
- **D4 (stderr ignored):** stderr `REGRESSION_CASE js-kimi-census: FAIL` with unchanged stdout gives CLEAN. This is documented scope ("stderr cannot supply token"); it is not a finding.

## Still applies at `c9ff09f`?

Yes.

- `git diff 496d212 c9ff09f -- tools/command-binding.py` touches only `selftest()` (it adds `round-24/extra-cases.json`). `evaluate()` and `check()` are unchanged.
- Neither `round-23/extra-cases.json` nor `round-24/extra-cases.json` has a cleanup or held case.
- The registry row is identical and active at `c9ff09f`, and `tools/mutate-and-run.sh` is byte-identical (`d22c4025…`).
- The round-24 replay receipt for this row (`.ufo/evidence/round-24/replay/bundle.json`, rev `d2eaecd4…`) uses the same projection shape (keys name, argv, cwd, revision, exit, stdout, stderr), so D1 carries over unchanged [INFERENCE: I did not inspect the round-24 projector source].

## Smallest safe correction

The projector should not emit a receipt for any row whose runner result has `held is not True` because of a non-exit, non-token cause (`cleanup_error` present). For example, in `replay.py:67`, skip rows with `'cleanup_error' in o['runner_result']`. `command-binding.py` then reports `MEMBERSHIP_MISMATCH` (exit 1) without a schema change.

Add a ruler fixture `cleanup-leak` (an observation with `cleanup_error`, expected `MEMBERSHIP_MISMATCH`) so the case is discriminated.

The alternative is a `command-binding-v2` receipt field `cleanup_ok` (bool, required true, finding `CLEANUP_MISMATCH`). That is a larger contract change and needs its own selftest case.

Impacted axes: calibration (a CLEAN binding over-claims "registry requirement held"). Coverage is not impacted.

## Bounds

- Writes: this report only, plus a `/tmp/rereplay18.th75ge` scratch.
- No registry command, suite, gate or selftest was run.
- Read-only git used `GIT_OPTIONAL_LOCKS=0`.
- Tools installed or updated: none.

R23-REATTACK Replay18: FINDING
