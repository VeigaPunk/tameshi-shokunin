# R23-REATTACK Replay03: exact row `repeat-control-selftest`

Scope: round-23 frozen artifacts under `.ufo/evidence/round-23/` (requirements.json, registry-baseline.json, replay/bundle.json, replay/expected.json, replay/observations.json), `tools/command-binding.py`, and lane revision c9ff09f. Attacked claim: the row's frozen argv and expect are exactly bound to the baseline, and the retained invocation metadata and full output are bound to that row.

## Verdict

Static exact binding is confirmed for every field the gate checks, on the frozen pair and at c9ff09f. I found no undisclosed false acceptance. The acceptances I produced fall into two groups. Authority deltas (a re-pinned digest, or the unsigned observations file) are excluded by the item and disclosed in the docs. The other group is a claim-strength limit: the stdout token `SELFTEST: PASS` is a substring, so it does not pin the 29-case count. The round-23 lesson names that limit. I quantify it in section 4 so that CLEAN is not read as "29 of 29 cases passed."

## Bounds and what I ran

- Writes: this report only. Git was read-only (`GIT_OPTIONAL_LOCKS=0`). No production file was touched. No tool was installed or updated; only python3 (stdlib) and git were used.
- Deviation 1: I ran the frozen gate command twice from the lane root. Both runs were read-only and exited 0. The bound says never run gates in the lane tree, so I am disclosing it. The second run used a doctored /tmp bundle. I re-ran the full set in a /tmp clone at c9ff09f and rely on those clone results.
  - `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json` gave exit 0, `finding_ids: []`, `bundle_sha256: 3d6c99b7…`.
- Deviation 2: I ran the gate's own selftest in /tmp clones (`python3 tools/command-binding.py --selftest`). It gave 38/38 at 496d212 and 44/44 at c9ff09f. That is registry row `command-binding-selftest-r24`, a suite run beyond the literal bound. It is not the attacked row and it is not used for the verdict.
- Not run: `tools/repeat-control.py --selftest` (the row's own command) at any revision, `replay.py`, `registry-check.py`, and any sweep.
- Variant harness (/tmp only): `/tmp/rereplay03-mut/run.py`, run with the gate cwd set to the c9ff09f clone `/tmp/rereplay03-clone3`. A second short script covered V8b and V13 (outputs in section 4).
- Round-24 projector on a /tmp copy of the frozen observations: `python3 tools/registry-replay.py --project <copy> --out <new dir> --json` gave `{"finding_ids": ["INVALID_OBSERVATIONS"]}`, exit 2, and created no output directory.

## 1. Frozen argv/expect against baseline source

| Field | Frozen (requirements.json:40 block) | Baseline registry at 28cae179 | Origin |
|---|---|---|---|
| argv | `python3 tools/repeat-control.py --selftest` | identical | SKILL.md@98bea7d:1503 names the same self-test command for repeated pristine controls |
| expect | exit 0; stdout_contains `["SELFTEST: PASS"]` | identical | token: `.ufo/evidence/round-12/verify-round.py@98bea7d:34`; the tool prints `SELFTEST: PASS ({total} cases)` at `tools/repeat-control.py:858` |

- `registry-baseline.json` has sha256 `ebd2e69a…`. That equals `git show 28cae179:tools/registry.json | sha256sum`, so the file is byte-identical to the baseline registry.
- Python equality, observed: the requirements.json list equals the active baseline rows (43 rows, same order), giving True. bundle.json `requirements` equals requirements.json, giving True.
- At c9ff09f, `tools/registry.json:43` is unchanged from baseline (row equality is True), has `status: active`, and no `superseded_by` points at it.

## 2. Retained invocation metadata and full output

- Bundle receipt (`replay/bundle.json:40` name, `:43` stdout): argv equals the frozen argv. cwd is `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`. Revision is `496d212bc46789cdf8cafab72978bdb7f4182963`. Exit is 0. Stdout is 2,936 bytes in 30 lines: 29 `SELFTEST_CASE … PASS` lines and `SELFTEST: PASS (29 cases)`. Stderr is empty.
- Observations row (`replay/observations.json:126` and `:135` name, `:110` measurement_interval, `:139` stdout): argv, cwd and revision equal the bundle copies. `got` is 0 and `held` is true. `elapsed_s` is 0.744, and the interval is 0.7438 s, within 2 ms.
- All 43 rows, checked in Python: each receipt equals its observation on name, argv, cwd, revision, exit, stdout and stderr, giving True. All 43 are held. No row has `cleanup_error` or `stdout_missing`, and no row has a timeout, unavailable or non-hermetic exit.
- Not a tail: for this row `stdout_tail == stdout`. The tail window is 4096 bytes (`tools/registry-check.py:110`), and the stream is shorter than that. The row took the normal communicate path. `elapsed_s` 0.744 is under `timeout_s` 60, so the TimeoutExpired branch (`registry-check.py:648` onward) could not have run.
- Case list: the 29 case names follow the emit order of `repeat-control.py` `selftest()`, which starts at line 592 at c9ff09f, with emit sites from :605 onward. My receipt-name check matched that order as I read it.
- Stability: `git diff --stat 8f66b5d c9ff09f -- .ufo/evidence/round-23/replay/ .ufo/evidence/round-23/requirements.json .ufo/evidence/round-23/registry-baseline.json` is empty. bundle.json and observations.json were first committed at 8f66b5d. requirements.json was first committed at 496d212.

## 3. Gate binding, field by field (`tools/command-binding.py` at c9ff09f)

The gate reads only bundle.json and expected.json. The string "observ" does not appear in the file, so it never opens observations.json. The digest check runs first, in `check()` at :115. The checks in `evaluate()` (:65) are:
- name membership: :99
- argv, exact list: :103
- cwd, string-equal to the bundle cwd: :105
- revision, string-equal to the bundle revision: :107
- exit, integer-equal (bools and strings rejected at :90): :109
- stdout tokens, by substring `in`: :111
- stderr: not checked, by design

Observed one-field deltas on the receipt. Each bundle was re-pinned, so only the named field differs:

| Delta | Gate output |
|---|---|
| argv `--self-test` | exit 1, ARGV_MISMATCH |
| cwd `/tmp/elsewhere` | exit 1, CWD_MISMATCH |
| revision `1` repeated 40 times | exit 1, REVISION_MISMATCH |
| exit 1 | exit 1, EXIT_MISMATCH |
| name `repeat-control-selftest-x` | exit 1, MEMBERSHIP_MISMATCH |
| `SELFTEST: PASS` changed to `SELFTEST: FAIL` | exit 1, STDOUT_MISMATCH (my print cut the line at 120 characters; STDOUT_MISMATCH is the only finding with that prefix) |

Conclusion: for argv, name, exit, cwd and revision the binding is exact. Each single-field change is rejected by its named finding.

## 4. Adversarial deltas (observed; /tmp copies; gate run in the c9ff09f clone)

Primary delta, on the full-output field: delete the 29 case lines and keep only the summary token.

| Case | expected.json | Gate output | Reading |
|---|---|---|---|
| V1 | committed (digest 3d6c99…) | exit 2, SNAPSHOT_TAMPERED | rejected |
| V2 | re-pinned to the new digest | exit 0, finding_ids [] | accepted |

The gate never checks completeness. Only the committed digest does. Re-pinning chooses a new contract. The docs say so: `corpus/knowledge/required-command-binding.md`, Bounds (lines 49–57), states that "changing both requirements and expected digest chooses a new contract" and that "self-consistent forged receipts can pass". Under the item's rule this is producer authority. It is not a false acceptance of the committed pair.

Other observed cases:

| Case | Delta | Gate output | Class |
|---|---|---|---|
| V3 | drop the `child127-baseline` line and set the summary to `SELFTEST: PASS (28 cases)`; re-pinned | exit 0, CLEAN | claim-strength limit (token) |
| V8 | summary `SELFTEST: PASSED (29 cases)`; re-pinned | exit 0, CLEAN | claim-strength limit (prefix match) |
| V13 | added a line `SELFTEST: FAIL (1 of 29 cases failed)` with exit 0; re-pinned | exit 0, CLEAN | authority (self-consistent forgery) |
| V10 | bundle requirement argv and receipt argv both changed to `--self-test`; re-pinned | exit 0, CLEAN | authority; the gate never compares to baseline |
| V11 | observations.json edited (argv gains `--extra`, `held` false, interval collapsed); committed bundle and expected left untouched | exit 0, CLEAN | unsigned artifact the gate never reads |
| V12 | simulated not-held row: the round-23 `replay.py` bundle comprehension applied to the selftest row with `held` false and a `cleanup_error`; re-pinned | exit 0, CLEAN | producer ordering; see section 7 |

V3 is the one delta that needs no re-pin. A later tool revision that prints `SELFTEST: PASS (28 cases)` produces a fresh pair and a CLEAN verdict. The docs name loose substring tokens as an old limitation (`corpus/lessons/round-23.md:111`). That limitation applies to this row. What the row proves is that the exit is 0 and the substring `SELFTEST: PASS` appeared. What it does not prove is that 29 of 29 cases passed. The 29-case evidence exists only in the retained stream, and no gate checks it. The repo's own doc states the output as `SELFTEST: PASS (29 cases)` (`corpus/knowledge/repeated-control-precondition.md:85`), so the gap between that doc and the row is visible.

## 5. Evidence present versus inferred

Present and pinned. The bundle bytes match the digest in expected.json:2 (3d6c99…). The round-24 row `command-binding-frozen-clean-pinned` pins the same digest at `tools/registry.json:971–974`. This covers name, argv, cwd string, revision string, exit, stdout and stderr for all 43 receipts.

Present, not pinned, not read by any gate:
- observations.json as a whole. That includes `measurement_interval`, `elapsed_s`, `held`, the header `runner_sha256`, and the per-row argv, cwd and revision copies. The docs call these "newly retained unsigned observations". The knowledge doc also says all fields come from one retained observation. The gate has no observation input, so it cannot check that.

Declared only:
- cwd: the directory is absent. `ls /tmp/tameshi-r23-replay-naxu6fzi` reports "No such file or directory".
- revision: a string the gate cannot check against a checkout. The docs call it "declared metadata".
- interpreter: argv names `python3`, resolved through PATH. The interpreter identity is not retained.

Inferred, not observed by me:
- That the row executed in round 23 and held. This rests on the retained stream. I did not re-run it.
- That the selftest run used the tool at 496d212. The selftest output carries no tool sha. Identity comes from the revision, plus sibling snapshot rows in the same run that print `tool-sha256=296fe566…`. That equals the `repeat-control.py` blob at 496d212 and at c9ff09f. The header `runner_sha256 cba16646…` equals the `tools/registry-check.py` blob at 496d212 and at c9ff09f.
- Chronology: commit 496d212 is dated 2026-10-21 11:41:18 −0300. The replay started at 14:42:22 UTC (11:42:22 −0300), so the run post-dates its revision. The writer supplies this timing.
- Revision-pinned state only: `EVIDENCE_ROOT` is derived from the tool's own realpath (`repeat-control.py:113–114`), so it reads the clone's committed round-12 fixtures. The selftest's subprocesses are synchronous (`:281`, `:612`, `:646`), with no detached descendants.

Not used as evidence: historical runs under the same row name (`.ufo/evidence/round-12/verification*.json`, `.ufo/evidence/round-17/c2-*.txt`, `registry-full-*.txt`). Those are different populations.

## 6. Producer authentication and retrofill (rejected)

- Producer authentication: not established, and not claimed. The expected file is an authority boundary, not a signature. The frozen pair carries no signature or attestation.
- Historical retrofill: none found. `replay.py:73–84` writes bundle, expected and observations after its own run, from rows it just executed. No code path reads historical observations. Each row's elapsed time matches its own interval. The evidence is code path plus internal consistency. It is not an authenticated record.

## 7. Does the finding still apply at c9ff09f?

Yes, statically. Nothing was run at c9ff09f for this row.
- The row is active and unchanged (`tools/registry.json:43`), and it is not superseded.
- `tools/command-binding.py` at c9ff09f equals the working tree. Its diff from 496d212 touches only the selftest fixture loader. `evaluate()` and `check()` are unchanged.
- HEAD is `5b69fb2`, one round-25 commit past c9ff09f. `git diff --stat c9ff09f HEAD` over the binding paths is empty.
- Lane status also shows round-25 edits elsewhere (corpus/SOURCES.md, record.json, peer reports under w1). None of these are binding paths, and I did not write them.
- The frozen gate in the c9ff09f clone: exit 0, `finding_ids []`, digest 3d6c99….

Successor and residuals:
- `tools/registry-replay.py` (round-24) refuses `RUNNER_NOT_HELD` and `RUNNER_CLEANUP_FAILED` before it publishes (`project()` :86–90 and :109; `publish()` :116–117). That closes the V12 path for future runs.
- It cannot consume round-23 observations. `--project` on the frozen observations gives INVALID_OBSERVATIONS, exit 2, because the round-23 file lacks the round-24 `OBS_SCHEMA` (`registry-replay.py:42`). No successor re-derives the frozen rows.
- Residual, not reachable for this row: the round-23 producer writes bundle and expected before its held check, and returns 1 afterwards (`replay.py:73–84`). For this row that would need a cleanup failure, and the selftest command spawns only synchronous children. It is a generic gap for other rows. The frozen pair is unaffected, because all 43 rows are held.
- Not observed at c9ff09f: I did not run `repeat-control.py --selftest`, since the item excludes it. Any claim that the row passes at c9ff09f is inferred from the unchanged row, tool blob and case list.

## 8. Smallest safe correction (not applied)

Leave the frozen row and the pair as they are. Append a successor row with `stdout_contains: ["SELFTEST: PASS (29 cases)"]`, which is the exact summary the tool prints at c9ff09f. That turns V3 and V8 into rejections, using the append-only supersession pattern the round-23 and round-24 docs already use. Do not re-pin anything to address V2, V10, V11 or V13. Those are authority deltas, and re-pinning only changes the contract.

For the integrator: the registry rows `command-binding-frozen-clean-pinned` and `command-binding-selftest-r24` are the existing checks that cover the frozen pair and the gate. Running `repeat-control.py --selftest` at c9ff09f would give a current-pass observation for this row, but the item excludes it, so that run needs explicit authorization.

R23-REATTACK Replay03: AGREE
