# SpecEnvironment — bounded injected-`GIT_DIR` fixture and no-secret-capture recipe

Seat: `TameshiR15.SpecEnvironment` (leaf executor). Read revision:
`a9cf4da78f2514c7bedd91a850a88590009d7df0`. `tools/context-capture.py` **does not exist**
at that revision; everything below is a pre-implementation specification against the
historical source. No gate, selftest, probe or CLI was executed. One static check was run:
the fixture runner text below was matched against the historical regex constants copied
verbatim into a throwaway `/tmp` process (no import of the historical module, no lane read
beyond the source bytes). Tools installed or updated: none.

## 1. Historical contract read (evidence anchors)

- Historical script: `.ufo/evidence/round-14/capture-context.py`, 647 lines,
  sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`.
- Retained receipt: `.ufo/evidence/round-14/context-receipt.json`,
  sha256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`.
- Retained field-less snapshot: `.ufo/evidence/round-14/context-missing-env.json`, same
  `tool_sha256`, `status: "ok"`, `exit: 0`, and **no `environment.injected_env` key**.
  This is why the selftest below asserts the injected field itself, not only the status.
  `decide()` (`:553-580`) never reads `injected_env`; it reads only the derived booleans.

Relevant functions and their exact behavior:

| Anchor | Behavior reused |
|---|---|
| `:60-61` `INJECTED_ENV` / `POISON_PATH` | One key only: `GIT_DIR` → `/nonexistent/tameshi-round14-poison` |
| `:184-188` `safe_env()` | Ambient copied minus every `GIT_*` key, plus `LC_ALL=C` |
| `:190-212` `run_bounded()` | Child runs with `stdin=DEVNULL`; records `argv,cwd,exit,stdout,stderr` only |
| `:213-257` `parse_runner_mapping()` | Six headers, six `PIN_*`/`REV_*`, six `run_regression` calls |
| `:259-337` `mapping_block()` | Per-leg five checks + order/set equality |
| `:350-392` `comparison_block()` | Drops top-level `observed_at`, canonical JSON equality |
| `:395-411` `positive_control_block()` | `git -C LANE_ROOT rev-parse --git-dir`, baseline vs injected |
| `:419-428` `base_receipt()` environment block | Ten keys; `ambient_env_dumped: False` |
| `:439-462` `validate_manifest()` | Schema, six legs, string fields, 40/64 hex |
| `:465-550` `evaluate()` | Poison check `:468-472`; env delta `:524-536`; probe argv `:538` |
| `:553-580` `decide()` | `mismatch/1` reasons are **free text**; else `ok/0` |
| `:583-602` `write_receipt()` | Atomic write under `OUTPUT_REL` |
| `:605-643` `main()` | `:607-613` any argv → 64, no receipt; `:618-628` invalid → 2 + receipt; else verdict exit |

## 2. Exact existing stable tokens and expected exits

Decision-level tokens already in source:

| Token | Exit | Source | Hermetic in a temp fixture? |
|---|---:|---|---|
| `ok` (status) | 0 | `:580` | yes (full synthetic lane) |
| `mismatch` (status) | 1 | `:579` | yes, but reasons are free text only |
| `invalid_input` (status) | 2 | `:618` | yes |
| usage (no token) | 64 | `:607-613` | yes; no receipt is written |

`InvalidContext.kind` tokens (all surface as `error.kind` and as `kind=<token>` on stdout,
exit 2): `missing_input`, `unreadable_input`, `invalid_json`, `invalid_utf8`,
`missing_executable`, `timeout`, `exec_failed`, `non_utf8_output`, `runner_unparsed`,
`probe_baseline_unusable`, `invalid_manifest`, `invalid_expected`, `poison_path_exists`,
`invalid_fleet_root`.

**Answer to the assigned question.** For the bounded injected-`GIT_DIR` field the only
existing stable token that can be pinned is **`poison_path_exists` with expected exit 2**
(`:470-472`). It is reachable hermetically **only if the injected target is selectable by
the fixture** (see §5). Without that one input, the exact existing fallback token is
**`missing_input` with expected exit 2** (missing `.ufo/evidence/round-13/pin-manifest.json`;
`read_lane_bytes` `:148-151`). There is **no existing stable finding ID** for the success
path, for exit 1, or for exit 64: success is anchored by `status: "ok"` plus the exact
`environment` field values; exit-1 reasons are the literal free-text strings in
`:561-576`; exit 64 has no token. Do not invent a finding-ID system for this clause.

## 3. Isolated fixture recipe (exit 0, bounded field, no secret capture)

All paths are created under one `tempfile.mkdtemp()` root `S`; nothing outside `S` is
read or written. The CLI under test is a **byte-identical copy** of the committed
`tools/context-capture.py` placed at `<case>/lane/tools/context-capture.py`, so the
promoted tool's `LANE_ROOT = dirname(dirname(SELF))` resolves to `<case>/lane`.

```
S/
  case-bounded-field/
    lane/                                  # LANE_ROOT for the copied CLI
      tools/context-capture.py             # byte-identical copy
      tools/pin-disposition.py             # synthetic probe stub (below)
      tools/mutate-and-run.sh              # synthetic six-leg runner (below)
      .ufo/evidence/round-13/pin-manifest.json
      .ufo/evidence/round-13/expected.json
      .ufo/evidence/round-15/              # CLI writes context-receipt.json here
      .git/                                # `git init -q`, clean env
    absent-git-dir                         # declared injection target; MUST NOT exist
    probe-observations/                    # probe stub writes its two sidecars here
```

Builder rules:

1. `clean_env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}`.
   Build the fixture (including `git init -q <lane>`) with `clean_env`; otherwise an
   ambient `GIT_DIR` would initialize the wrong directory.
2. The probe stub computes its own sha256 at runtime and writes that value into its JSON
   `tool_sha256` field. `expected.json` must then pin that same digest under
   `inputs["tools/pin-disposition.py"]` (`evaluate` `:496`).
3. The manifest pins the runner bytes in `derived_from.sha256` with a path ending in
   `tools/mutate-and-run.sh` (`evaluate` `:497-504`), and carries six legs whose
   `expected_sha256`/`pinned_commit` values equal the `PIN_*`/`REV_*` literals below.
4. The runner is parsed as text only; it is never executed. The historical regexes accept
   both the historical `\`-continued calls and the single-line calls used here. The text
   below was checked against the transcribed regexes: 6 headers, 6 `PIN_`, 6 `REV_`,
   6 calls, all suffixes `JS/BASH/TSUKUROI/MADO/CHECKLIST/CLAIMS` (`PASS`, static only).

Probe stub (`<lane>/tools/pin-disposition.py`) — deterministic; identical stdout under
both runs; writes only its two fixture sidecars:

```python
#!/usr/bin/env python3
import hashlib, json, os, sys

LANE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.abspath(__file__)
LEGS = ("js-kimi-census", "bash-surface-census", "bash-tsukuroi-census",
        "bash-mado-verify", "bash-checklist-run", "js-claims-check")

def main(argv):
    with open(HERE, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    payload = {
        "schema": "pin-disposition-v1",
        "status": "ok",
        "observed_at": "2026-10-20T00:00:00Z",   # constant: upstream drops this key only
        "tool_sha256": digest,
        "legs": [{"leg": leg, "content_status": "pinned",
                  "pinned": {"status": "verified"}} for leg in LEGS],
    }
    marker = "injected" if "GIT_DIR" in os.environ else "baseline"
    sidecar = os.path.join(LANE, ".probe-observation-" + marker + ".json")
    with open(sidecar, "w", encoding="utf-8") as fh:
        json.dump({"git_keys": sorted(k for k in os.environ
                                      if k.startswith("GIT_")),
                   "git_dir_value": os.environ.get("GIT_DIR")}, fh)
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

Runner fixture (parsed as text; `PIN` values are 64 hex, `REV` values are 40 hex):

```sh
#!/bin/sh
PIN_JS=1111111111111111111111111111111111111111111111111111111111111111
REV_JS=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
PIN_BASH=2222222222222222222222222222222222222222222222222222222222222222
REV_BASH=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
PIN_TSUKUROI=3333333333333333333333333333333333333333333333333333333333333333
REV_TSUKUROI=cccccccccccccccccccccccccccccccccccccccc
PIN_MADO=4444444444444444444444444444444444444444444444444444444444444444
REV_MADO=dddddddddddddddddddddddddddddddddddddddd
PIN_CHECKLIST=5555555555555555555555555555555555555555555555555555555555555555
REV_CHECKLIST=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
PIN_CLAIMS=6666666666666666666666666666666666666666666666666666666666666666
REV_CLAIMS=ffffffffffffffffffffffffffffffffffffffff
TABLE_JS='D1:KILLED'
TABLE_BASH='B1:KILLED'
TABLE_TSUKUROI='B1:KILLED'
TABLE_MADO='D1:KILLED'
TABLE_CHECKLIST='A1:KILLED'
TABLE_CLAIMS='D1:KILLED'

#   js-kimi-census        kumitate-shokunin/scripts/kimi-census.mjs   8/10 (80 %)
#   bash-surface-census   kagi-shokunin/corpus/surface-census.sh      8/10 (80 %)
#   bash-tsukuroi-census  tsukuroi-shokunin/tools/tsukuroi-census.sh  6/10 (60 %)
#   bash-mado-verify      mado-shokunin/tools/mado-verify.sh          4/10 (40 %)
#   bash-checklist-run    kagi-shokunin/corpus/checklist-run.sh       7/15 (47 %)
#   js-claims-check       kumitate-shokunin/scripts/claims-check.mjs  7/10 (70 %)

run_regression() {
  regression_case_git js-kimi-census 'kumitate-shokunin/scripts/kimi-census.mjs' "$PIN_JS" "$REV_JS" "$specs/js-kimi-census.spec" 'node "$MUTANT" --selftest' "$TABLE_JS"
  regression_case_git bash-surface-census 'kagi-shokunin/corpus/surface-census.sh' "$PIN_BASH" "$REV_BASH" "$specs/bash-surface-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_BASH"
  regression_case_git bash-tsukuroi-census 'tsukuroi-shokunin/tools/tsukuroi-census.sh' "$PIN_TSUKUROI" "$REV_TSUKUROI" "$specs/bash-tsukuroi-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_TSUKUROI"
  regression_case_git bash-mado-verify 'mado-shokunin/tools/mado-verify.sh' "$PIN_MADO" "$REV_MADO" "$specs/bash-mado-verify.spec" 'bash "$MUTANT" --selftest' "$TABLE_MADO"
  regression_case_git bash-checklist-run 'kagi-shokunin/corpus/checklist-run.sh' "$PIN_CHECKLIST" "$REV_CHECKLIST" "$specs/bash-checklist-run.spec" 'bash "$MUTANT" --selftest' "$TABLE_CHECKLIST"
  regression_case_git js-claims-check 'kumitate-shokunin/scripts/claims-check.mjs' "$PIN_CLAIMS" "$REV_CLAIMS" "$specs/js-claims-check.spec" 'node "$MUTANT" --selftest' "$TABLE_CLAIMS"
}
```

Manifest shape (values must equal the literals above; order = runner call order):

```json
{
  "schema": "pin-manifest-v1",
  "derived_from": {"path": "tools/mutate-and-run.sh", "sha256": "<sha256 of runner bytes>"},
  "legs": [
    {"leg": "js-kimi-census", "repo": "kumitate-shokunin",
     "path": "scripts/kimi-census.mjs", "pinned_commit": "aaaa...40",
     "expected_sha256": "1111...64"}
  ]
}
```

`expected.json`: `{"inputs": {"tools/pin-disposition.py": "<sha256 of probe bytes>"}}`.

Invocation: `[sys.executable, "<lane>/tools/context-capture.py"]`, `cwd=<lane>`, and a child
env built from `clean_env` plus exactly these ambient sentinels (so ambient stripping is
observable and no real value is involved):

```python
child_env = dict(clean_env)
child_env.update({
    "GIT_DIR": "r15-ambient-git-dir-should-not-appear",
    "GIT_WORK_TREE": "r15-worktree-should-not-appear",
    "TAMESHI_SELFTEST_CANARY": "r15-canary-should-not-appear",
})
```

### 3.1 Literal expected results for the exit-0 case

| Assertion | Literal expected value |
|---|---|
| process exit | `0` |
| stdout | starts `CONTEXT: OK (receipt=.ufo/evidence/round-15/context-receipt.json exit=0 probe-equal=True poison-control=True runner-mapping=True)` |
| `status`, `exit`, `reasons` | `"ok"`, `0`, `[]` |
| `environment.injected_env` | `{"GIT_DIR": "<lane>/../absent-git-dir"}` (absolute path to the nonexistent leaf) |
| `environment.env_delta_keys` | `["GIT_DIR"]` |
| `environment.env_delta_matches_declared` | `true` |
| `environment.baseline_has_GIT_DIR` | `false` |
| `environment.ambient_git_keys_removed` | `["GIT_DIR", "GIT_WORK_TREE"]` |
| `environment.poison_path_exists` | `false` |
| `environment.ambient_env_dumped` | `false` |
| `environment` key set | exactly `{baseline_policy, injected_policy, injected_env, env_delta_keys, env_delta_matches_declared, baseline_has_GIT_DIR, ambient_git_keys_removed, poison_path, poison_path_exists, ambient_env_dumped}` |
| `runs.argv_equal`, `runs.cwd_equal` | `true`, `true` |
| `runs.env_delta` | `{"baseline": [], "injected": ["GIT_DIR"]}` |
| `comparison.equal`, `.raw_stdout_equal` | `true`, `true` (constant `observed_at` in the stub) |
| `comparison.payload_tool_sha256_matches_disk` | `true` |
| `positive_control.effective` | `true` (baseline exit 0/`.git`; injected exit 128, stderr contains the declared path) |
| `mapping.all_match`, `leg_set_equal`, `leg_order_equal` | `true`, `true`, `true` |
| each leg's five checks | all `true` |
| `mapping.parsed` | `{"header_rows": 6, "pin_constants": 6, "rev_constants": 6, "leg_calls": 6}` |
| `sources.probe.matches_declared` | `true` |
| `sources.runner.matches_manifest_declaration` | `true` |

Do not pin `observed_at`, `invocation.argv[0]`, absolute git/python paths, temp paths, or
`call_scope.line_start`; they legitimately vary. Assert `runs.argv[1:]` instead of
`runs.argv[0]` (`shutil.which("python3")` may differ from `sys.executable`).

### 3.2 Exact-token negative case, exit 2 (`poison_path_exists`)

Create `S/case-poison/lane/` with only the byte-identical CLI copy, and create
`S/case-poison/poison-target/` (a directory; `os.path.lexists` is true). Invoke the copy
with one argument: `--injected-git-dir <absolute path to poison-target>`. The tool raises
before reading any input, so no probe/runner/manifest fixture is needed.

| Assertion | Literal expected value |
|---|---|
| process exit | `2` |
| stdout | contains `CONTEXT: INVALID (kind=poison_path_exists` and `exit=2` |
| receipt | written at `.ufo/evidence/round-15/context-receipt.json` |
| `status`, `exit` | `"invalid_input"`, `2` |
| `error.kind` | `"poison_path_exists"` |
| `error.message` | starts `injected GIT_DIR target exists: ` |
| `environment.poison_path` | the absolute poison-target path passed on argv |
| `environment.poison_path_exists` | `true` |

This is the exact existing stable token and expected exit the assignment asks for. It is
reachable **only** with the single fixture input described in §5.

### 3.3 Exact-token negative case, exit 2 (`missing_input`), fallback

Build the full exit-0 fixture but delete `.ufo/evidence/round-13/pin-manifest.json` before
invocation (no arguments). Expected: exit `2`; `status: "invalid_input"`; `error.kind:
"missing_input"`; `error.message == "missing lane file: .ufo/evidence/round-13/pin-manifest.json"`;
stdout contains `kind=missing_input`. This is the second existing stable token, and it
needs no new CLI input.

### 3.4 Usage case, exit 64 (optional)

Invoke the copy with `--not-an-option`. Expected exit `64`; stderr starts
`context-capture.py: unexpected argument(s):`; **no receipt file is created**. There is no
stable token here; pin the exit and the absent-receipt fact only.

## 4. No-secret-capture assertions and bounded claim

Add to the exit-0 case:

1. None of the three sentinel values (`r15-ambient-git-dir-should-not-appear`,
   `r15-worktree-should-not-appear`, `r15-canary-should-not-appear`) occurs in the receipt
   bytes, stdout, or stderr.
2. `environment.ambient_git_keys_removed == ["GIT_DIR", "GIT_WORK_TREE"]` — key names only,
   sorted; no values.
3. `environment.ambient_env_dumped is False`, and the `environment` key set is exactly the
   ten historical keys (any additional key must be reviewed; an `env`/`ambient_env` object
   fails the case).
4. `runs.baseline` and `runs.injected` have no `env` key; `runs.env_delta` contains key
   names only.
5. The probe sidecars prove the field reached the children: baseline sidecar
   `{"git_keys": [], "git_dir_value": null}`; injected sidecar
   `{"git_keys": ["GIT_DIR"], "git_dir_value": "<declared absent path>"}`.
6. `environment.injected_env["GIT_DIR"]` is the declared path, never the ambient sentinel.

Bounded claim (state it this way, no more): the tool records no ambient variable values,
removes every ambient `GIT_*` before child execution and before the control, records only
stripped key names, and its own code reads only `SELF` and its four declared lane inputs.
What this does **not** prove: syscall-level non-access to arbitrary files; that a child
cannot print a secret (child stdout is captured verbatim by design into `runs.*.stdout`);
broad environment independence; or credential safety of git itself beyond the disabled
system/global config used by the control.

## 5. Implementation-critical notes for `ContextGate`

1. **The injected target must be selectable or `poison_path_exists` is unreachable
   hermetically.** The hardcoded `/nonexistent/...` lies outside any temp root; creating it
   would violate the no-write-outside-temp rule. Recommendation: one bounded CLI input,
   `--injected-git-dir PATH`, defaulting to the historical literal
   `/nonexistent/tameshi-round14-poison`, still producing exactly the single key
   `INJECTED_ENV = {"GIT_DIR": path}` and recording the actual value in
   `environment.poison_path` (already an existing field). Keep the default literal so the
   retained round-14 receipt and the positive-control literal remain comparable. If the
   option is refused, drop the §3.2 case and pin `missing_input` (§3.3) as the only negative
   stable token; do not manufacture a new token for the field.
2. **`LANE_ROOT` depth.** At `.ufo/evidence/round-14/` the historical `dirname` ×4 is
   correct; at `tools/context-capture.py` it must be `dirname(dirname(SELF))`, or the tool
   binds the fleet root above the lane. The selftest's copy-in-fixture placement only works
   with the corrected depth.
3. **Selftest must invoke a byte-identical copy inside the fixture lane**, never the live
   lane script, or the public CLI run would write the real lane's round-15 receipt. Assert
   the copy's sha256 equals the committed tool's sha256 (read-only read of the source).
4. **Dispatch `--selftest` and any check subcommand before the historical "any argv → 64"
   branch** (`:607-613`), and keep `--selftest` argument-free.
5. **Output/schema round-15 only.** Keep `OUTPUT_REL` at
   `.ufo/evidence/round-15/context-receipt.json`; do not overwrite the round-14 receipt.
   Preserve the historical source file bytes untouched.
6. **Do not broaden the experiment.** No env-dump detection, credential scanning, broad
   environment isolation claim, extra cases beyond the existing bounded comparison/control/
   mapping, or a fixture per risk string. The §3 fixture plus §3.2/§3.3 negatives are the
   complete addition required by the routed defect.

## 6. Snapshot mode: bounded position (not a requirement)

`PROTOCOL.md` §Gate standard ("Two evidences") requires a committed run over a committed
input snapshot only when the verdict depends on a mutable fleet artifact. This gate's
verdict reads lane-committed inputs and compares them to persisted expected values, and the
round-15 receipt records the source digests it observed. A separate snapshot mode is
therefore **not required** by this clause. If one is added, it must pin every snapshot
input digest in committed expected values and classify a digest failure as
could-not-evaluate (`snapshot_tampered`, exit 2), never as the existing exit-1 mismatch;
the historical `decide()` maps source-digest mismatch to exit 1 (`:571-576`), so that
mapping must not be reused for a frozen-snapshot check. This is a guardrail, not a request
to build the mode.

## 7. Residual risks

- The positive-control literal appears in git's stderr on this host's git version; another
  git version could word the failure differently. The stub fixture is independent of that
  wording because the control runs real git in a real (fixture) repo, but the literal
  assertion should remain scoped to the exit/difference and the path substring.
- `environment` key-set pinning must be updated deliberately if the promoted tool adds a
  field; that is the point — an unplanned ambient dump fails closed.
- The probe stub's self-digest technique assumes Python 3.9+ `__file__` semantics; the
  `abspath` call in the stub makes it version-independent.
- All expectations above are pre-implementation; `tools/context-capture.py` is absent at
  `a9cf4da`. This report is advisory and is not an admission verdict.

## 8. Static check actually performed

Transcribed the historical regex constants (`:83-107`) into a throwaway process and matched
the §3 runner text: 6 header rows, 6 unique `PIN_` occurrences, 6 unique `REV_`
occurrences, 6 `run_regression` calls with suffixes `JS/BASH/TSUKUROI/MADO/CHECKLIST/CLAIMS`.
Result: `PASS` (static transcription only). The historical module was not imported or
executed; no lane probe, gate, selftest or CLI was run.
