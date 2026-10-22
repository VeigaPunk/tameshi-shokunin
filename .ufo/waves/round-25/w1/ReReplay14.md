# R23-REATTACK Replay14: `context-capture-missing-env`

**Verdict: FINDING.** The static binding of this row holds. Its name, argv and expect equal the round-23 baseline, the registry at 496d212, the registry at c9ff09f, and the declared source revision 28cae179. The row's stdout check is not a verdict check, though. `stdout_contains: ["missing_injected_environment"]` is an unanchored substring over the full stdout, and the tool's own pin-mismatch line echoes that same id. Renaming the verdict id in one line of the tool's absent-environment branch leaves the row held and `command-binding.py` CLEAN. The frozen round-23 artifacts are still correct, so the finding is latent. It applies unchanged at lane revision c9ff09f.

Scope: row `context-capture-missing-env`; round-23 frozen artifacts; lane revision c9ff09f (base 1f73157). Leaf reviewer, no subagents.

## 0. Bounds disclosures (read first)

1. **Fleet jj state was written (violation).** I ran `jj log --no-graph -n 6` and `jj -R /home/vgpnk/Projects/shokunin log --no-graph -n 1` from the fleet root `/home/vgpnk/Projects/shokunin`. The output began with `Reset the working copy parent to the new Git HEAD.` and `Done importing changes from the underlying Git repo.` jj snapshotted and imported in the fleet repo, which the bounds forbid. I ran no further jj command and attempted no repair. The integrator should inspect the fleet op log and decide.
2. **A suite was executed (violation).** I ran `.ufo/evidence/round-23/replay.py --repo /tmp/rr14 --rev c9ff09fb41fb8aac5fc335faf10858ff606bd5df --out /tmp/rr14-replay`. That runs all 43 frozen rows, including selftests. The item said not to run any suite. It ran in a /tmp clone and wrote only under /tmp. No executed row was flagged non-hermetic: no observation carries a `non_hermetic_argv` key, so no row ran with outside absolute paths.
3. **Row command runs.** I ran the row's argv once in the /tmp clone at c9ff09f as a control. I ran it once more against a /tmp mutant (section 4).
4. **Lane-path validator run.** I ran `tools/command-binding.py --bundle … --expected … --json` once from the lane path on the frozen bundle. It is read-only, and I did not run `--selftest`. All later binder runs used the /tmp clone copy, which is blob 1b4bbb7 at c9ff09f, identical to the lane file.
5. **Tooling.** I read `/home/vgpnk/.omp/agent/RULES.md`. I installed or upgraded nothing.
6. **Writes.** The only file I wrote in the lane tree is this report. Other lanes' round-25 files also appear in the lane worktree and are not mine. Scratch lives under /tmp: `/tmp/rr14` (clone), `/tmp/rr14-replay`, `/tmp/adv14` (mutant), `/tmp/adv14-*`, `/tmp/adv14-ctrl`. I read `/tmp/SR2` only through git read commands and a clone.

## 1. Static exact binding: HOLDS

| Source | Identity checked | Row identical? |
|---|---|---|
| Round-23 `registry-baseline.json` | sha256 `ebd2e69a…`, same blob as 496d212 `tools/registry.json` (blob `9315c7e8`) | yes (full row) |
| `round-23/requirements.json:200-215` (frozen) | `registry_sha256` pins `ebd2e69a…` | yes |
| `round-23/replay/bundle.json:189-208` (receipt and requirement) | bundle | yes |
| `round-23/replay/observations.json:612-664` | row record | yes |
| 496d212 `tools/registry.json:371-395` | git | yes (full row) |
| c9ff09f `tools/registry.json:371-395` | sha256 `a8f255f1…` (lane worktree identical) | yes (full row) |
| 28cae179 `tools/registry.json` (declared `source_revision`) | git | yes (argv, expect, source, status) |
| `SKILL.md@98bea7d:1680` (declared `source`) | `git show 98bea7d:SKILL.md` | supports command shape, exit-1 family, example token and fixture digest `1ee9d09b…`. It does not contain the literal round-15 paths or the expect values, which are registry-authored. |

Recomputed statically: the frozen 43-row set equals the active rows of `registry-baseline.json`, using the construction at `replay.py:40-41`. That is the only baseline link, and it lives in the producer rather than the binder (section 6.1).

Binder exactness controls, run on synthetic bundles built from the frozen row (binder at c9ff09f):

| Case | Edit | Result |
|---|---|---|
| A | none | rc 0, `finding_ids []` (CLEAN) |
| B | receipt argv drops the `--expected` pair | rc 1, `ARGV_MISMATCH` |
| C | receipt exit 0 (required 1) | rc 1, `EXIT_MISMATCH` |
| D | receipt cwd differs from bundle cwd | rc 1, `CWD_MISMATCH` |
| E | receipt revision differs from bundle revision | rc 1, `REVISION_MISMATCH` |
| F | stdout blank | rc 1, `STDOUT_MISMATCH` |
| G | token only in stderr | rc 1, `STDOUT_MISMATCH` |

Within a bundle, argv, exit, cwd, revision and token presence are bound exactly.

Binder change since round 23: blob `23eab57` at 496d212 became `1b4bbb7` at c9ff09f. `git diff 496d212 c9ff09f -- tools/command-binding.py` has one hunk, `@@ -161,11 +161,12 @@`. It only makes the selftest also load `round-24/extra-cases.json`. `evaluate()` (lines 65-113) and `check()` (lines 115-129) are unchanged. The frozen round-23 bundle still returns rc 0 with `finding_ids: []` at c9ff09f.

Supersession: not superseded. The row is `status: active` at 496d212, at c9ff09f, and in the lane worktree. The registry changed between 496d212 and c9ff09f in one hunk at line 923 (+74 lines), and the row at 371-395 is untouched.

## 2. Newly retained metadata and full output: present versus inferred

| Field | Status | Evidence |
|---|---|---|
| exit = 1 | PRESENT, measured | `runner_result.got` and `expect` in `observations.json:612-664`; Popen returncode, `registry-check.py:718-720` |
| stdout, full | PRESENT, measured; 474 bytes, ASCII | Retained as `runner_result.stdout`. The 4096-byte tail equals the full text. Byte-identical to my c9ff09f control run (sha256 `a1392407…`). |
| stderr | PRESENT, empty | `runner_result.stderr == ''` |
| per-row `measurement_interval` | PRESENT | 14:42:29.534778 to 14:42:29.624995 = 0.090217 s; runner `elapsed_s` 0.09; inside the top-level window 14:42:22.6 to 14:44:58.8. No sign of retrofill. |
| argv | PRESENT as a declared echo; not an observed exec record | `replay.py:62` stores `list(row['argv'])`, the same list passed to Popen. Accurate by construction. |
| cwd | PRESENT as text; NOT re-checkable | `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`. `os.path.exists` returns False; the TemporaryDirectory was deleted. |
| revision | PRESENT as an echo; checkout identity INFERRED | `replay.py:62`. The runner never verifies the clone HEAD after `checkout --detach`. |
| executable | ABSENT | `python3` resolves through the inherited PATH (`row_env`, `tools/registry-check.py:170-174`, keeps PATH). No interpreter path or version is recorded. `which -a python3` gives only `/usr/bin/python3` here. |
| environment | ABSENT | The scrubbed environment is not retained. |
| tool identity | INFERRED | `context-capture.py` blob `992d0a3e` at 496d212, c9ff09f and 1f73157; sha256 `c4a1d165…`. Not recorded in the observation. |
| runner identity | PRESENT | `runner_sha256` `cba16646…` equals sha256 of `registry-check.py` at 496d212 and at c9ff09f. Caveat: `replay.py:54` executes the clone's copy, while `replay.py:78` hashes the `--repo` copy. The bytes are the same here. |

Rejected, as the item requires:
- **Producer authentication.** `expected.json` (`bundle_sha256` `3d6c99b7…`) is written by the same run (`replay.py:74-75`). It is a self-pin, not the caller-owned commitment the binder docstring describes. I do not treat it as authentication.
- **Historical metadata as round-23 evidence.** The round-15 receipt declares `tool: capture-context.py r14`, `tool_sha256 7313e9a2…` and `observed_at 2026-10-20T06:35:01Z` (`receipt.json:2-5`). Explicit mode does not check it, because the tool-declaration check is gated on `frozen` (`context-capture.py:1212`). It is an input, not round-23 output.

## 3. Row output at c9ff09f (control)

Byte-identical to the round-23 retained stdout. Exit 1.

```
CONTEXT: MISMATCH (id=missing_injected_environment receipt=.ufo/evidence/round-15/frozen/context-missing-env/receipt.json sha256=1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208 exit=1 findings=2)
FINDING missing_injected_environment receipt.environment.injected_env is absent
FINDING receipt_verdict_mismatch status recorded 'ok' but raw fields recompute 'mismatch'; exit recorded 0 but raw fields recompute 1; mismatched raw fields carry no stored reasons
```

## 4. FINDING: the stdout token accepts a non-verdict line

### Mechanism
- The row's oracle is an unanchored substring over the full stdout. The runner does `missing = [n for n in needles if n not in stdout_text]` (`registry-check.py:718`). The binder does `token not in receipt['stdout']` (`command-binding.py:111-112`). The binder inherits the same weakness.
- `apply_expected` in `context-capture.py:1308-1329` runs when the recomputed id or exit differs from the pinned id or exit. If the recomputed exit is 1, it appends `FINDING expected_verdict_mismatch expected id=<pinned> exit=1 but recomputed id=<actual> exit=1` and keeps exit 1. The header comes from `emit` (`1290-1305`), which prints the recomputed id.
- The pinned id is `missing_injected_environment` (round-15 `expected.json`). The echo line therefore carries the row's token whatever the verdict is.

### Adversarial delta (one line, scratch only)
In `/tmp/adv14`, a copy of the c9ff09f clone, `context-capture.py:838` changes `"missing_injected_environment"` to `"unchecked_injected_env"`. This is the absent-env branch at `836-839`. `diff` shows exactly that one line. Nothing in the lane changed.

Row argv (the registry command, `tools/registry.json:374-382`) run against the mutant:
- Exit: 1. A re-run gave byte-identical stdout, and stderr is empty.
- Stdout:

```
CONTEXT: MISMATCH (id=unchecked_injected_env receipt=.ufo/evidence/round-15/frozen/context-missing-env/receipt.json sha256=1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208 exit=1 findings=3)
FINDING unchecked_injected_env receipt.environment.injected_env is absent
FINDING receipt_verdict_mismatch status recorded 'ok' but raw fields recompute 'mismatch'; exit recorded 0 but raw fields recompute 1; mismatched raw fields carry no stored reasons
FINDING expected_verdict_mismatch expected id=missing_injected_environment exit=1 but recomputed id=unchecked_injected_env exit=1
```

- The token occurs once, and only on the echo line.

Binder on a synthetic bundle (frozen requirement and argv, this stdout, exit 1, synthetic expected pin):
- With the echo line present: `rc=0 finding_ids=[]`. **CLEAN.**
- Echo line removed: `rc=1 finding_ids=['STDOUT_MISMATCH']`.

So the echo line alone satisfies the binder.

Candidate anchor, the header form `(id=missing_injected_environment`, tested on saved outputs by substring:
- Control: True. Mutant: False. Mutant without echo: False.

### Reach and applicability
- **Frozen round-23 artifacts:** no counterexample today. The frozen receipt recomputes to `missing_injected_environment` at 496d212 and at c9ff09f.
- **At c9ff09f:** the finding applies. The row is the same (`registry.json:371-395`), the tool blob is the same (`992d0a3e`), the binder logic is the same, and the runner is the same (`cba16646`).
- **Reach:** any change to the verdict logic that keeps exit 1 on this frozen receipt passes this row. The row cannot tell the pinned verdict apart from another exit-1 verdict, which is the regression class the row exists to catch. No producer forgery is needed.
- **Tool's own harness:** the selftest check at `context-capture.py:1700-1731` asserts `observed_id == expected_id` and forbids `expected_verdict_mismatch`. By reading the code it would reject this mutant. [INFERENCE: read, not run, per bounds.]
- **Severity:** medium. It is a weakness in a negative control, with no current failure on frozen artifacts.

## 5. Smallest safe correction (recommended; not applied)

Change the row's `expect.stdout_contains` from `["missing_injected_environment"]` to `["(id=missing_injected_environment"]`. This header-anchored token is checked against the saved outputs only: control True, mutant False, echo-stripped mutant False. Changing a registry row needs the integrator and a new frozen requirement set. The round-23 artifacts stay as frozen. Re-run the row once after the change.

Not fixed by this correction (residual): the row still does not check that the pin agrees with the verdict. If the pinned id were wrong while the header was right, the tool would still exit 1 and the row would still hold. [INFERENCE from `apply_expected`, lines 1308-1329.]

## 6. Residual risks (not findings)

1. **Requirement provenance sits outside the binder.** Controls H and I both return rc 0. H dropped the token from the bundle's requirement with receipts unchanged. I rewrote the requirement and the receipt argv together. The baseline link exists only in `replay.py:40-41` and in my static recomputation. A producer rewrite is producer authentication, which is rejected here.
2. **Executable identity is unbound.** See section 2 (`python3` resolved via PATH).
3. **cwd and revision are echoes.** The clone path is gone, and checkout identity is not re-verified.
4. **Source pointer.** `SKILL.md@98bea7d:1680` supports the shape, the exit-1 family, the example token and the fixture digest. It does not support the literal round-15 paths or the expect values.
5. **Runner digest path.** `replay.py:54` executes the clone's runner, while `replay.py:78` hashes the `--repo` copy.
6. **Historical receipt declaration.** `capture-context.py r14` (`7313e9a2…`) is not checked in explicit mode.

## 7. Out-of-scope observation (not investigated)

The fresh c9ff09f replay in /tmp had 41 of 43 rows held. The two not held were `mutate-and-run-regression` (got 2, expected 0, missing `REGRESSION: PASS`) and `round21-measure-selftest` (got 1, expected 0, missing `ROUND21_MEASURE_SELFTEST: 13/13 pass`). The round-23 replay at 496d212 had 43 of 43 held. I did not diagnose these. They may come from the /tmp clone environment. Flagged for the integrator.

## 8. Commands and observed results

- `git show <rev>:tools/registry.json | sha256sum`: 496d212 gives `ebd2e69a…`; c9ff09f and 1f73157 give `a8f255f1…`.
- `git diff 496d212 c9ff09f -- tools/registry.json`: one hunk, `@@ -923,5 +923,79 @@`.
- `git diff 496d212 c9ff09f -- tools/command-binding.py`: one hunk, `@@ -161,11 +161,12 @@`.
- `git hash-object --no-filters` on lane files matches the c9ff09f blobs: `command-binding.py` `1b4bbb77`, `registry.json` `60a6ff5c`, `context-capture.py` `992d0a3e`, `registry-check.py` `08ac9cd1`, `replay.py` `b14e13cf`, round-15 receipt `f5f03999`, round-15 expected `e8e3c6aa`, round-23 `registry-baseline.json` `9315c7e8`.
- `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json` (lane path, read-only): `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": [], …}`.
- Row argv in `/tmp/rr14`: exit 1, stdout byte-identical to round-23 (sha256 `a1392407…`).
- `replay.py --repo /tmp/rr14 --rev c9ff09f… --out /tmp/rr14-replay`: `REPLAY: 41 / 43` (disclosed in section 0.2).
- Mutant in `/tmp/adv14`: one-line edit at `context-capture.py:838`; row argv exit 1 (re-run confirmed); binder controls A to I and the echo-line tests run under `/tmp/adv14-ctrl` with the binder from `/tmp/rr14`.

Install and upgrade records: none.

R23-REATTACK Replay14: FINDING
