# ReReplay04: fresh falsification of exact row `bash-witness-count`

## Verdict

AGREE. The attacked binding holds on the frozen round-23 artifacts and at lane revision c9ff09f.

- The frozen argv, expect.exit, expect.stdout_contains token and name equal the baseline registry row. That row is JSON-identical (same keys and values) in round-23 (496d212b), c9ff09f and HEAD (5b69fb2), and it is still `active`.
- The round-23 receipt for this row carries the same argv, exit 0, and the full 1758-byte stdout, which contains the token exactly once, as the final line.
- Observation and bundle are consistent: re-encoding a projection of `observations.json` reproduces `bundle.json` byte for byte, for all 43 rows.
- I found no field-level false acceptance on the frozen artifacts.
- The one concrete adversarial delta I built is a forged `unresolved` line that the validator accepts when the bundle digest is re-minted (section 3, V2). It is not reachable from the real `count` output. The in-repo registry row added in round 24 pins the bundle digest and would catch it unless that literal is also rewritten.
- Present versus inferred is tabulated in section 4. I do not claim producer authentication. The digest chain and the `held` field are self-recorded, and the report says so.

## Scope, bounds and tooling

- Read: `round-23/requirements.json`, `round-23/replay/bundle.json`, `round-23/replay/observations.json`, `round-23/replay/expected.json`, `round-23/registry-baseline.json`, `round-23/replay.py`, `tools/command-binding.py`, `tools/registry-check.py` (runner), the `count` path of `tools/bash-witness-study.py`, `tools/registry.json` at HEAD, and git history for all of these.
- Executed: only the validator CLI, `python3 <copy of command-binding.py> --bundle <bundle> --expected <expected> --json`. It ran on the frozen pair and on scratch copies under `/tmp/r23reattack04/`.
- Not executed: the registry command `bash-witness-study.py count`, `registry-check.py`, `replay.py`, any selftest or suite, any sweep, any mutation run.
- Writes: this report only. Scratch files are under `/tmp` only.
- Git: read-only subcommands with `GIT_OPTIONAL_LOCKS=0`, with one exception. My first call, `git status --porcelain`, ran without that variable and may have refreshed the lane index stat cache. No content changed. Disclosed for the record.
- Tools installed or upgraded: none. I used the system `python3` standard library and `git`.

## 1. Static binding: frozen row against baseline source

| Field | Frozen `requirements.json` | Baseline registry | SKILL source | Round-23 run | Validator |
|---|---|---|---|---|---|
| name | `bash-witness-count` (L54) | identical (`registry-baseline.json`, sha ebd2e69a, equals `tools/registry.json` at 496d212b; HEAD row at `tools/registry.json` L64) | — | `bundle.json` L53; `observations.json` L178 | key/name exact |
| argv | `python3 tools/bash-witness-study.py count` (L43–47) | identical | `python3 tools/bash-witness-study.py count` (table row at 98bea7d:1504) | requirement, observation argv and receipt argv all equal | exact list compare, `command-binding.py:103` |
| expect.exit | 0 | 0 | "0 complete classified sample" | got 0 (`observations.json` L175; `bundle.json` L52) | int compare, `:109` |
| expect.stdout_contains | `["unresolved\tnone"]` (L51) | identical | not in the SKILL row; a registry-author addition | token present in full stdout | substring compare, `:111` |
| cwd | not in requirement | — | — | clone path (deleted after run) | canonical form only, `:105` |
| revision | not in requirement | — | — | `496d212bc46789cdf8cafab72978bdb7f4182963` | equals bundle revision, `:107`; never checked against a repo |

Checks I ran:

- `git show 496d212b:tools/registry.json | sha256sum` returned `ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a`. That matches `requirements.json` `registry_sha256` and `sha256sum .ufo/evidence/round-23/registry-baseline.json`.
- Projection check: the active rows of `registry-baseline.json`, projected to `{name, argv, expect}`, equal `requirements.json` `requirements` in order (43 rows). `replay.py:40` enforces the same equality at run time.
- `git show 98bea7d:SKILL.md` and `git show 496d212b:SKILL.md` print identical lines 1503–1504, so the citation holds. The whole-file hashes differ, which does not matter for this row.
- The SKILL row gives argv and exit 0. The `stdout_contains` token is not in the SKILL row. It was added by the registry author, and the runner's contract says needles are literal substrings (`registry-check.py:36–37`).

## 2. Retained invocation metadata and full output (not tails)

- `observations.json` row for this requirement: `argv` and `requirement.argv` equal (L163–169). `runner_result` (L172–184) has `got` 0, `expect` 0, `held` true (L176), `elapsed_s` 0.092 (L173), `stderr` `""` (L180), and no `cleanup_error` or `stdout_missing` key. Row interval is 14:42:23.904536 to 14:42:23.996582. That is consistent with elapsed_s.
- Full output: `stdout` is 1758 bytes (L182). `stdout_tail` (L183) equals `stdout`, because `TAIL_BYTES = 4096` (`registry-check.py:110`). For this row, tail and full output are the same, so the tail-versus-full question does not change the result.
- The token `unresolved\tnone` occurs exactly once, as the final line. There is no `\r` in the stdout.
- `bundle.json` receipt (L51–56): cwd (clone path), exit 0, name, revision `496d212b…`, `stderr` `""`, and a `stdout` byte-equal to the observation stdout.
- Whole-bundle projection: `replay.py` encoding applied to `observations.json` rows reproduces the bundle bytes exactly (43 rows). The receipt is therefore derived from the observations, not independent of them.
- The `count` stdout contains the run-specific temp path `/tmp/tameshi-r23-replay-…/`. Byte-level reproduction would need that path normalised. The token check does not depend on it.
- Doc drift: `registry-check.py:37` says needles match "over the retained tail". The code checks the full decoded stdout (`:717–718`, `missing = [n for n in needles if n not in stdout_text]`). The code is the stricter check, so this is documentation drift and not a false acceptance.

## 3. Adversarial deltas (scratch copies only)

Method: copy `bundle.json` into `/tmp/r23reattack04/`, change the bash receipt, re-encode with the same `encode()` that `replay.py` uses at line 72, then run the validator with either a re-minted `expected` (digest of the new bytes) or the frozen `expected`.

| Variant | Change to bash receipt | Expected file | Validator result | Reading |
|---|---|---|---|---|
| V0 | none | frozen | rc 0, `[]`, digest `3d6c99b7…` at both 496d212b and c9ff09f | baseline holds |
| V1 | token becomes `unresolved\tnone-B3` | re-minted | rc 0, `[]` | substring accepts a suffix |
| V2 | append line `unresolved\tB3` after the real line | re-minted | rc 0, `[]` | **primary delta**: substring accepts a contradictory line |
| V3 | token moved to stderr; stdout has `unresolved\tB3` | re-minted | rc 1, `STDOUT_MISMATCH` | stderr cannot supply the token |
| V4 | stderr set to a traceback, exit 0 | re-minted | rc 0, `[]` | stderr is not checked |
| V5 | argv `./tools/bash-witness-study.py` | re-minted | rc 1, `ARGV_MISMATCH` | argv exact |
| V6 | revision with one hex character changed | re-minted | rc 1, `REVISION_MISMATCH` | revision exact |
| V7 | extra receipt key `held: false` | re-minted | rc 2, `INVALID_RECEIPT` | receipt schema is closed |
| V8 | exit 1 | re-minted | rc 1, `EXIT_MISMATCH` | exit exact |
| V9 | stdout edited, frozen expected kept | frozen | rc 2, `SNAPSHOT_TAMPERED` | pin defeats naive edits |
| V10 | token removed | re-minted | rc 1, `STDOUT_MISMATCH` | token required |

Primary delta (V2, substring acceptance):

- Reachability from the real tool: none. `count` prints the unresolved line exactly once (`bash-witness-study.py:1124`) and exits 0 only when that set is empty (`:1125`). For any output the tool can print, token presence means the single unresolved line reads `none`. V2 is therefore reachable only by editing retained output.
- Attacker effort: V2 also needs the bundle digest re-minted. The validator's own check (`command-binding.py:125–126`) passes with a re-minted expected file.
- In-repo catch: `tools/registry.json` L971–974, row `command-binding-frozen-clean-pinned` (active; added in round 24, commit d2eaecd), runs the validator on the frozen bundle and requires `"bundle_sha256": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9"`. V2's digest is `73770a2de7cd310701406760b2ada72a1f04a603bc4c60cbb1f98a8e22cbb19a`, so that row would fail unless its literal is also rewritten. I did not run that row. I only compared the literal with the forged digest.

Secondary delta (CLEAN is not held):

- The runner's hold is `held = got == expected_exit and not missing and cleanup_ok` (`registry-check.py:720`). A cleanup failure sets `held` to false while `got` can still equal the expected exit, and records `cleanup_error`.
- `replay.py:66–71` builds receipts from `got`, `stdout` and `stderr` only. `held` and `cleanup_error` do not reach the bundle, and V7 shows the validator rejects them as extra keys.
- I built a synthetic cleanup-failed observation (copy of this row, `held` false, `cleanup_error` set) and ran replay's receipt construction on it. The two receipts were identical. The validator therefore says CLEAN for a row the runner would mark not held.
- For this row, `held` is true and no `cleanup_error` exists (`observations.json` L176 and the key list above). The CLEAN verdict does not claim `held`, so this is a scope limit and not a counterexample to the attacked binding.

Observation-only delta:

- Editing `observations.json` stdout leaves the validator verdict unchanged, because the validator never opens that file (zero references to observations, requirements or registry in the 496d212b validator). `observations.json` is not in any digest in git: `git grep` for its sha256 returns no hits.

## 4. Evidence present versus inferred

| Claim | Status | Evidence |
|---|---|---|
| Frozen argv/expect equal the baseline registry row | Present, checked | `requirements.json` L43–54; `registry-baseline.json` (sha ebd2e69a) = `tools/registry.json@496d212b`; HEAD row at `tools/registry.json` L64 |
| argv and exit match the SKILL table | Present | `SKILL.md@98bea7d:1504` |
| The stdout token is a baseline requirement | Not present in SKILL; registry-author addition | `SKILL.md@98bea7d:1504` contains no stdout text |
| Full stdout of the round-23 run | Present, full (1758 bytes) | `observations.json` L182 equals `bundle.json` L56 |
| cwd, revision and argv recorded for the run | Present, self-recorded by `replay.py` | `replay.py:62–63`; `observations.json` L163–184; `bundle.json` L51–56 |
| The run executed the recorded command in the recorded clone | Inferred | `replay.py:49–50` clones and checks out 496d212b with `check=True`; the clone is deleted; no independent process record |
| The bundle digest binds the bundle bytes | Present, but minted by the producer in the same run | `expected.json` L2, written by `replay.py:73–75` in commit 8f66b5d. The validator docstring requires a caller-owned commitment |
| A later record pins the digest | Present, repo-internal | `tools/registry.json` L971–974 (round 24, d2eaecd); `replay-gate-A.json` stdout (validator run at 14:45:21 UTC); `reader-freeze2.json`; `final-verification.json` |
| Producer authenticity | Not established; out of scope for this item | — |
| `held` true for the row | Present in observations only; not in the bundle; not digest-pinned | `observations.json` L176 |
| Measurement interval | Present, self-recorded | row object in `observations.json`; top-level interval 14:42:22.624871 to 14:44:58.826834 |
| `unresolved none` means classification is complete | Present, recomputed from round-12 raw logs | `bash-witness-study.py:1051–1125` (count path); `.ufo/evidence/round-12/BashWitness/summary.json` declaration disclosure (at 496d212b) says the witness mapping was declared after the author saw aggregate outcomes |
| Full-output evidence exists for other runs of this row | Not present. Other retained runs keep only `stdout_tail` (4 KB) for this row | `.ufo/evidence/round-23/registry-C.json` (no escaped full `stdout` key in any embedded row); `.ufo/evidence/round-24/landing-verification.json` (same); `.ufo/evidence/round-23/final-verification.json` (this row's record at line 161 has `stdout_tail` only) |

No retrofill found:

- `git log` lists one commit for each of `observations.json`, `bundle.json` and `expected.json`: `8f66b5d`. None was edited afterwards.
- `requirements.json`, `registry-baseline.json` and `replay.py` were committed in `496d212`, the same commit as the replayed revision, and not changed afterwards.
- The observation fields are exactly the output schema of `replay.py:62–81`.
- The timestamps fall inside the run window. The validator run recorded in `replay-gate-A.json` (14:45:21) comes after the run.
- None of this proves the recording is authentic. It only shows the fields were written by the same run and were not added later.

## 5. Does the finding still apply at c9ff09f?

- Row: unchanged. The bash row is JSON-identical at 496d212b, c9ff09f and HEAD, and it is `active`, not `superseded`. The attacked binding holds at c9ff09f.
- `tools/command-binding.py`: created in 496d212 (round 23). Its only later change is d2eaecd (round 24), which touched only the selftest. The selftest now also reads `round-24/extra-cases.json`, which exists at c9ff09f. `evaluate` and `check` are unchanged. The validator sha is `d533dc1e…` at 496d212b, which matches the instrument record in `replay-gate-A.json`. It is `9230c68e…` at c9ff09f and at HEAD. Both copies return rc 0, `[]` and digest `3d6c99b7…` on the frozen pair. I did not run the selftest.
- `tools/registry.json`: changed in d2eaecd (+49 / −7). The registry sha is no longer `ebd2e69a…`. HEAD has 54 rows and 47 active rows. The round-23 frozen set covers 43 active rows, so `requirements.json` pins the round-23 registry and not the current one. This does not affect the row.
- `tools/registry-check.py`, `tools/bash-witness-study.py` and `.ufo/evidence/round-12/BashWitness`: unchanged between 496d212b and c9ff09f, and between c9ff09f and HEAD (`git diff --name-status` shows no entries for these paths). The `count` output should reproduce at c9ff09f from identical inputs. That is inferred, not run.
- Surviving finding: the V2 substring delta still exists in the validator at c9ff09f. It is mitigated only by the registry literal at `tools/registry.json` L971–974.

## 6. Residual risks and smallest safe corrections

1. Pin provenance. `expected.json` was minted by the same producer run as the bundle. Correction: none needed for this row. Do not describe `expected.json` as an independent commitment. The round-24 registry literal is the second pin.
2. Substring token semantics. A forged or contradictory `unresolved` line passes when the digest is re-minted. Correction: none needed to keep this row exact for real output, since exit 0 already implies no unresolved rows. If the lane needs line-exact gates, extend the runner or validator with line-anchored needles. That is a tool change and out of scope here.
3. CLEAN is not held. Held, `measurement_interval` and `elapsed_s` live only in `observations.json`, which is unpinned. Correction: any consumer should read `REPLAY … held` from observations and should not read command-binding CLEAN as held.
4. Documentation drift. `tools/registry-check.py:37` says "over the retained tail"; the code checks the full stdout (`:717–718`). Correction (doc-only, not applied): change the sentence to "over the full decoded stdout".
5. Scope of `unresolved none`. It is a completeness gate over a witness mapping declared after the author saw aggregate outcomes. It does not prove witness independence, and it does not gate `accidental` kills (0 in this run). Correction: scope any claim to "classification complete".

## 7. Verification gaps

- I did not re-run `count` at c9ff09f. The statement that it reproduces there is inferred from unchanged inputs.
- The clone was deleted after the run. The clone-to-revision checkout is the producer's assertion, consistent with `check=True` at `replay.py:50`. I could not re-verify it.
- I did not run the HEAD registry row `command-binding-frozen-clean-pinned`. The pin check is a literal comparison, not an execution.
- Beyond the whole-bundle byte projection, I did not check the other 42 rows.
- I did not run any selftest or suite, per bounds.

Scratch files (outside the lane): `/tmp/r23reattack04/cb-496.py`, `/tmp/r23reattack04/cb-c9ff.py`, `/tmp/r23reattack04/bundle.json`, `/tmp/r23reattack04/expected.json`, plus `/tmp/rcheck-496.py`, `/tmp/bws-496.py`, `/tmp/declared-496.tsv`, `/tmp/summary-496.json` and `/tmp/reg-*.json`, which were `git show` extracts.

R23-REATTACK Replay04: AGREE
