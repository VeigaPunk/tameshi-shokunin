# ReviewEnvironment — round 15 C1: bounded injected GIT_DIR field and no secret capture

Seat: `TameshiR15.ReviewEnvironment` (reviewer, leaf). Lane: tameshi-shokunin.
Scope: review of the planned context-gate receipt against (a) the injected GIT_DIR field and (b) the no-secret-capture boundary. Historical source and round-14 routed defect 5 are evidence. No gate, selftest, probe, or runner was executed.

## Read revision and state

- Lane HEAD read: `a9cf4da78f2514c7bedd91a850a88590009d7df0` (equals `claims.json` baseline).
- `tools/context-capture.py` does **not** exist at this revision. It is the planned file; every statement about it below is a requirement, not an observation.
- Historical `.ufo/evidence/round-14/capture-context.py`: sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, equal to `tool_sha256` in `context-receipt.json`. Historical bytes intact.
- Worktree is dirty with other seats' round-15 work (`corpus/QUALITY.md`, `corpus/SOURCES.md` modified; `.ufo/evidence/round-15/`, `corpus/lessons/round-15.md` untracked). Not reviewed here.
- Read-only actions taken: `git rev-parse HEAD`, `git status --porcelain`, `sha256sum`, `grep`, file reads. No gate, selftest, probe, or runner executed.
- Tool installs or updates: none.

## Axes

1. Injection boundedness: exactly one injected variable, `GIT_DIR`, recorded exactly.
2. Secret-capture boundedness: no ambient environment value reaches a tool-authored receipt field.
3. Claim honesty: each receipt field and each "no leak" or "injection inert" claim is measured, not declared.
4. Hermetic selftest feasibility for the above, with literal expected exits and stable IDs.

## Verdict

The historical design is sound on axes 1 and 2 at the code level. Three things are not sound and must be fixed or disclosed in the promoted tool:

- one self-attested literal (`ambient_env_dumped`) is presented as evidence;
- two predicates are unreachable by construction, so they cannot be pinned by any CLI fixture;
- decide() emits free-text reasons, with no stable IDs, so there is nothing to pin.

Also, the 4-level LANE_ROOT derivation from the historical path will silently point at the wrong root if copied to `tools/`.

## Evidence (historical `.ufo/evidence/round-14/capture-context.py`, read)

| Item | Location | Observation |
|---|---|---|
| Injected value | L60–61 | `INJECTED_ENV = {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}` constant |
| Ambient scrub | L184–187 | `safe_env()` drops every `GIT_*` key, sets `LC_ALL=C`; keeps all other ambient vars (including any token-bearing ones) |
| Raw child output retained | L190–210 | `run_bounded` returns `stdout`/`stderr` verbatim; stored at `runs.baseline/injected` (L541–546) and `positive_control.*` (L407–411) |
| Ambient names only | L466–468 | `ambient_git_keys_removed` = sorted names of `GIT_*` keys in `os.environ`; values not stored |
| Injected dict is built, not observed | L524–536 | `injected_env` = `{k: injected_env[k] for k in delta}`; `delta` ⊆ keys of `INJECTED_ENV` (base has no `GIT_*`). Records the parent-built dict; does not observe the child environment |
| Tautological predicate | L535, L568 | `baseline_has_GIT_DIR = "GIT_DIR" in base_env`; `base_env` comes from `safe_env()`, so always False. Unreachable as mismatch |
| Tautological predicate | L533, L566 | `env_delta_matches_declared` compares a set built from two dicts the script constructs. Unreachable as mismatch |
| Hardcoded literal | L427 | `"ambient_env_dumped": False` in `base_receipt()`. No code path sets or measures it. Appears in `context-receipt.json` L28 and `context-missing-env.json` L25 |
| Declared, not measured | L547 / L411 | `positive_control.env_delta.injected = sorted(INJECTED_ENV)` is a constant |
| Positive control | L395–411 | `git -C LANE_ROOT rev-parse --git-dir` under base and injected env; effective iff baseline ok, injected exit ≠ 0, and poison text appears |
| Hermetic gap | L395–406 | Baseline control depends on LANE_ROOT being inside a git repo via ancestor discovery; `safe_env()` strips `GIT_CEILING_DIRECTORIES` (a `GIT_*` key), so the child cannot be bounded by env |
| Root derivation | L45–47 | Four `dirname` calls from `.ufo/evidence/round-14/capture-context.py` yield the lane root. From `tools/context-capture.py` the lane root is two `dirname` calls. Copying the four-level chain yields `/home/vgpnk/Projects` |
| Free-text reasons | L560–577 | `decide()` returns sentences, not stable IDs. The gate standard (quoted at `.ufo/waves/round-14/w1/VerdictContract.md` L16–19) requires stable finding IDs pinned by selftest |
| Injected-run asymmetry | L371–375 vs L539–540 | Injected nonzero exit → comparison error → exit 1. Injected timeout → `InvalidContext("timeout")` → exit 2. Both are "injected run unusable"; the classification differs |
| Unreachable poison-exists branch | L469–472 | Requires `/nonexistent/tameshi-round14-poison` to exist. A selftest cannot create it without writing outside temp roots |
| Retained result | `verification.json` L73 | `probe-equal=True poison-control=True runner-mapping=True` observed in round 14 |
| Probe scrubs too | `tools/pin-disposition.py` L197–211 | `git_env()` strips `GIT_*`. Equality under injection is expected even if the injection were never delivered (ES-2) |
| Probe does not emit env | `tools/pin-disposition.py` grep | No `os.environ` dump in payload; `environ` appears only in `git_env()` and selftest |
| Python env semantics | round-14 lesson S049 (quoted) | `env=` replaces the child environment wholesale; supports that the injected child received exactly `injected_env`, but this is documentation, not observation |

## Acceptance criteria for the planned C1 (bounded GIT_DIR and no secret capture)

Proposed stable IDs are suggestions for the ContextGate executor. Whatever names are chosen must be pinned by the selftest.

**AC-1 Injection value.** Receipt `environment.injected_env` equals exactly `{"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`. Keep the value identical to round 14 for comparability. Do not rename it to a round-15 string without a selftest pin for the new value. Verified by the ok fixture (AC-7).

**AC-2 Delta shape.** `environment.env_delta_keys == ["GIT_DIR"]`. No other key appears in any delta field.

**AC-3 Ambient GIT_* is names only.** `ambient_git_keys_removed` holds sorted names only. Ambient `GIT_*` values never appear in receipt bytes. Ambient `GIT_*` presence does not change exit. This is a false-positive guard (see below).

**AC-4 No non-GIT ambient capture.** Non-GIT sentinel values in the child environment do not appear anywhere in receipt bytes. Non-vacuity required: a test-only probe stub writes its own environment to a file inside the temp root; that file must contain the non-GIT sentinel in the baseline child, proving the sentinel reached the process tree. Without this, absence from the receipt proves nothing.

**AC-5 Scrub proof at the child.** Same stub file: baseline child does not contain the ambient `GIT_DIR` sentinel value; injected child contains `GIT_DIR` equal to the poison constant and not the ambient sentinel. This is the only way to show the baseline was scrubbed and the injected value was delivered. Equality of probe JSON does not show either.

**AC-6 Positive control.** `positive_control.baseline.exit == 0` with nonempty stdout; `positive_control.injected.exit != 0`; poison text in injected stderr or stdout; `effective == true`. Receipt must retain both argv and both exits.

**AC-7 Ok fixture.** Exit 0; stdout begins `CONTEXT: OK`; receipt `status == "ok"`; `reasons == []`; AC-1 through AC-6 satisfied simultaneously.

**AC-8 Single-reason mismatch fixture.** Unscrubbed stub variant: prints JSON including the exit code of an unscrubbed `git rev-parse --git-dir`. Baseline and injected then differ after `observed_at` removal. Expected: exit 1; `reasons` is exactly one entry, the comparison ID (proposed `context.comparison_differs`). All other predicates must be green in this fixture so the single reason is the only reason.

**AC-9 Hermetic control fixture.** Temp lane root must be `git init`-ed by the harness with a scrubbed env. For the ineffective-control case (proposed `context.poison_control_ineffective`, exit 1), the harness must first verify that no ancestor of the temp root contains `.git`; if one does, the selftest exits 2 (could-not-evaluate) and does not claim the case. Do not rely on `GIT_CEILING_DIRECTORIES`, which `safe_env()` strips.

**AC-10 Unavailable.** Missing manifest or expected file → exit 2; receipt `status == "invalid_input"`; `error.kind` pinned to the kind returned by `read_lane_bytes`. ContextGate must read `read_lane_bytes` to pin this literal; I did not read lines 145–155.

**AC-11 Usage.** Unexpected argv → exit 64; stderr contains usage; no receipt written (assert the receipt path is absent under the temp root).

**AC-12 Write scope.** Selftest writes only inside its temp root. Poison path is never created. Normal mode writes only `.ufo/evidence/round-15/context-receipt.json`, atomically, and never the round-14 path.

**AC-13 Root derivation.** `LANE_ROOT = dirname(dirname(SELF))` for `tools/context-capture.py`; `FLEET_ROOT = dirname(LANE_ROOT)`. Selftest relocates a copy into `<tmp>/tameshi-shokunin/tools/` and runs that copy, so the derivation is exercised without a root override in normal mode.

**AC-14 Field truthfulness.** Receipt must not contain `ambient_env_dumped`. If a policy statement is kept, use a declared string such as `"ambient_policy": "names_only"` and do not present it as a measurement.

## Likely false positives (must not fail the gate)

- FP-1: ambient `GIT_*` variables present in the caller environment. Expected: recorded as names, exit unchanged. Treating presence as a mismatch would make the gate fail on any developer shell that exports GIT_ variables.
- FP-2: a harmless additional volatile field in probe JSON. The round-14 retained comparison was equal after only `observed_at` removal (`verification.json` L73). Any new probe volatile field will produce a false mismatch. [INFERENCE] unverified for future probe changes.
- FP-3: git stderr wording differences. Mitigated because `LC_ALL=C` is in `base_env`; the poison check tests substring presence of the poison path, not full text. Keep the substring check.
- FP-4: `observed_at` absent from the baseline document. Currently treated as `probe_baseline_unusable` (exit 2). Correct; do not downgrade.

## Unearned claims to reject

- U-1: "`ambient_env_dumped` is false, so no environment was dumped." The field is a literal at L427. Reject as evidence. Remove it.
- U-2: "`baseline_has_GIT_DIR` false proves the ambient environment had no GIT_DIR." It is tautological: `safe_env()` always strips it. It proves only that the constructed dict is scrubbed. Reject as ambient evidence. Keep the names list instead.
- U-3: "The probe received GIT_DIR." The receipt does not observe the child environment. It records the parent-built dict. Only AC-5 (stub file) turns this into an observation. Without the stub, the claim is "constructed and passed as child env".
- U-4: "Equal probe output shows GIT_DIR is inert." Vacuous without AC-5 and AC-6 (probe scrubs GIT_*). Equality plus positive control supports only: "the scrubbed probe's normalized output was unchanged in this run, and unscrubbed git honors the poison."
- U-5: "The receipt contains no secrets." Too broad. Accurate scope: tool-authored fields carry no ambient environment values; child stdout and stderr are retained verbatim and are data, not screened.
- U-6: "The child environment is credential-safe." `safe_env()` passes every non-GIT ambient variable, including tokens, to the probe and to git. Not captured by the receipt, but exposed to child processes. Reject any "no credential exposure" wording. Optional hardening: allowlist env (see below).
- U-7: "GIT_* scrubbing and injection are covered." Only `GIT_DIR` is injected and tested. Do not extend to `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_CONFIG_*`. The receipt's own `not_compared` list should keep saying so.
- U-8: "Round-14 receipt proves round-13 setup." Already rejected by the round-14 lesson; keep rejected.
- U-9: "`positive_control.env_delta.injected` is measured." It is a constant (L411). Reject as measurement.
- U-10: "The poison-exists branch is covered by selftest." Cannot be exercised without writing outside temp. Disclose as untested.

## Required vs optional

Required (for the C1 claim to be honest):
- Remove `ambient_env_dumped` (U-1, AC-14).
- Replace free-text reasons with stable IDs for every reachable predicate, pinned by selftest (AC-8, AC-10).
- Label the unreachable predicates (`baseline_has_GIT_DIR`, `env_delta_matches_declared`) as construction invariants with no CLI case. Do not count them as selftest coverage.
- Two-level LANE_ROOT derivation (AC-13).
- Non-vacuity stub file for AC-4 and AC-5.
- Hermetic git init and ancestor guard for AC-9.
- Disclose the untested poison-exists branch (U-10).

Optional hardening (not required for C1):
- Allowlist child environment instead of strip-only (U-6). Changes baseline semantics; would need a new comparison basis. Defer to a later round.
- Record sha256 and byte length of raw child stdout and stderr instead of, or alongside, full text. Reduces retained data without losing the comparison.

## Verification gaps for L1 (do not run now)

1. Confirm `tools/context-capture.py` derives LANE_ROOT with two `dirname` calls (AC-13).
2. Run the selftest once; confirm the AC-4 stub file contains the sentinel in baseline and that the receipt does not.
3. Confirm AC-5: baseline child lacks ambient GIT_DIR sentinel; injected child has the poison constant.
4. Confirm reasons list is exactly one ID in AC-8.
5. Confirm no file exists at `/nonexistent/tameshi-round14-poison` after the run.
6. Grep receipt output for ambient sentinel strings; must be absent.
7. Confirm `ambient_env_dumped` is absent from new receipts and new source.
8. Confirm historical `capture-context.py` sha256 is still `7313e9a2…` and `context-receipt.json` / `context-missing-env.json` are byte-unchanged.

## Messages sent

One implementation-critical message to `TameshiR15` (root derivation depth, ancestor guard, and sentinel non-vacuity). No other peer contacted.
