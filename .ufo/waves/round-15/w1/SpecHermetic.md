# SpecHermetic — round-15 w1: isolated CLI selftest fixture recipe

Scope: advice only, no source edits, no verification execution. Subject read in
full: `.ufo/evidence/round-14/capture-context.py` (647 lines, historical bytes,
unmodified). Precedents read: `tools/evidence-disposition.py` (docstring, selftest
harness, usage cases), `tools/witness-metadata.py:1136` (`-I` child invocation),
`tools/pin-disposition.py:603` (hermetic-fixture promise), `SKILL.md:1499-1605`
(registry rows and round-14 probe label). Routing source:
`corpus/lessons/round-14-verifier-spotcheck.md` Routed defects item 5.

No command from the gate, its selftest, git, or any lane gate was executed. No
tool was installed or updated. Claims below are source-text observations or
proposed literals, marked as such.

## 0. Axes

- **A1 hermeticity** — every input and output of a selftest case is a byte under
  one `/tmp` root; no live lane/sibling/fleet read, no network, no write outside
  that root.
- **A2 literal fidelity** — each case pins the process exit *and* a stable
  machine token/ID; exit alone never carries a verdict (round-14 lesson:
  "Exit agreement alone proves intended regression" rejected).
- **A3 single-fact discrimination** — one fixture fact changes per red case, so
  the failing ID is attributable.
- **A4 historical immutability** — round-12/13/14 bytes are read-only; the
  promoted tool writes round 15 only; the selftest never reads the live lane.

## 1. Historical facts that constrain the recipe (read, not run)

| Fact | Anchor |
|---|---|
| Declared exit map: 0 equal + control + env delta + source pins + six mappings; 1 mismatch (including injected run unusable); 2 could-not-evaluate; 64 usage, no receipt | `capture-context.py:26-29` |
| `LANE_ROOT` is derived by four `dirname` calls because the script sits under `.ufo/evidence/round-14/` | `capture-context.py:46` |
| Output is hard-coded to the round-14 receipt | `capture-context.py:58` |
| Injection is the module constant `GIT_DIR=/nonexistent/tameshi-round14-poison` | `capture-context.py:60-61` |
| Machine-stable per-leg check names | `capture-context.py:109-115` |
| Runner parser requires exactly six header rows, six `PIN_`, six `REV_`, six calls in `run_regression()`, and the six declared leg names | `capture-context.py:74-105,214-253` |
| Baseline probe document must be a six-leg `pin-disposition-v1` `ok` with each `pinned.status=="verified"` | `capture-context.py:350-372` |
| Control: `git -C LANE_ROOT rev-parse --git-dir` baseline exit 0 and non-empty; effective iff injected exit != 0 and reflects poison | `capture-context.py:395-412` |
| `decide()` emits free-form `reasons` strings only, no IDs | `capture-context.py:553-580` |
| Receipt written atomically to the fixed lane-relative path | `capture-context.py:583-602` |
| No selftest mode: help exits 0, every other argv exits 64 | `capture-context.py:605-613` |
| `InvalidContext` kinds: `missing_input` 150, `unreadable_input` 152-153, `invalid_json` 162/175-176/180, `invalid_utf8` 171, `missing_executable` 197/520/522, `timeout` 199, `exec_failed` 201-202, `non_utf8_output` 208, `runner_unparsed` 220/243-253, `probe_baseline_unusable` 358, `invalid_manifest` 441-460/495, `poison_path_exists` 471, `invalid_fleet_root` 474, `invalid_expected` 492 | same file |
| Round-14 registry labels this tool "probe" with "no standalone selftest" | `SKILL.md:1602` |
| Round-14 routed correction: register as gate, supply standalone isolated selftest testing exits and stable expected finding IDs; map C1 exit 64 explicitly to could-not-evaluate and declare the context harness 64 path | `corpus/lessons/round-14-verifier-spotcheck.md` Routed defects 5 |

Two source facts that the fixture matrix must not paper over:

1. **Injected-run-unusable is exit 1, not exit 2.** `comparison_block` raises
   `probe_baseline_unusable` only for the baseline run (`:357-362`); a bad
   injected document sets `comparison.error` and `equal=False`, and `decide()`
   returns mismatch/1 (`:560-563`). Both fixtures are needed; they pin different
   classes.
2. **Two `decide()` branches are unreachable through the capture CLI.**
   `safe_env()` removes every `GIT_*` key and then adds exactly the declared
   injection (`:183-186,526-535`), so `env_delta_matches_declared` is true by
   construction and `baseline_has_GIT_DIR` is false by construction
   (`:566-569`). They can only be exercised by a retained document whose fields
   are recomputed. Do not fake a capture fixture for them and do not claim they
   are latently covered.

## 2. Exact existing stable tokens and exits

"Supported today" means pinnable by a literal assertion in a standalone
selftest of the historical bytes.

| Token (exact) | Source | Exit | Supported today |
|---|---|---:|---|
| `CONTEXT: OK (` | printed at `:637` | 0 | No — requires live lane fixtures and injection constants; no root flag |
| `CONTEXT: MISMATCH (` | printed at `:637` | 1 | No — same reason |
| `CONTEXT: INVALID (kind=<kind>` | printed at `:627` | 2 | No — same reason |
| `usage:` (stderr; historical first line also says `capture-context.py: unexpected argument(s)`) | `:610-612` | 64 | **Yes** — `--bogus` (or any arg except `-h/--help`) |
| `header_matches_manifest`, `pin_name_and_value_match_manifest`, `rev_name_and_value_match_manifest`, `leg_call_matches_manifest`, `constant_names_match_leg` | `CHECKS`, `:109-115`; receipt JSON only | 1 when any is false | No — no ID is printed; names exist only inside the receipt's `mapping.legs[].checks` |
| receipt `status` = `ok` / `mismatch` / `invalid_input` | `:579,618,630` | 0/1/2 | No — same fixture blocker |
| receipt `error.kind` = the `InvalidContext` kind | `:618-620` | 2 | No — same fixture blocker |

Consequence: the historical file has **no** standalone isolated
exit+finding selftest and its only literal CLI pair today is
`unexpected argument -> 64 + usage:`. That is the routed defect, restated
against the bytes.

For the promoted tool, the smallest stable-ID set that (a) reuses existing
tokens and (b) gives each `decide()` branch one literal is:

| Condition | Stable ID (proposed literal) | Status |
|---|---|---|
| `comparison.equal is not True` | `injected_observation_mismatch` | new literal |
| `comparison.payload_tool_sha256_matches_disk is not True` | `probe_payload_digest_mismatch` | new literal |
| `environment.env_delta_matches_declared is not True` | `environment_delta_mismatch` | new literal; capture-unreachable |
| `environment.baseline_has_GIT_DIR is not False` | `baseline_carries_git_dir` | new literal; capture-unreachable |
| `control.effective is not True` | `poison_control_ineffective` | new literal |
| probe source digest mismatch | `probe_source_digest_mismatch` | new literal |
| runner source digest mismatch | `runner_source_digest_mismatch` | new literal |
| runner leg set differs | `runner_leg_set_mismatch` | new literal |
| runner leg order differs | `runner_leg_order_mismatch` | new literal |
| a per-leg check fails | the existing `CHECKS` token itself, with `expectation=<leg>` | **existing token** |

Exit-2 IDs are the existing `InvalidContext.kind` strings unchanged. Retained
mode adds only `retained_schema_mismatch`, `retained_tool_digest_mismatch`,
`retained_source_digest_mismatch` (see §5). One catch-all ID
`unexpected_exception` (exit 2) matches `evidence-disposition.py` and
`witness-metadata.py` precedent and prevents a crash being read as a semantic
red.

Emission format should follow the r14 gate precedent:
`FINDING <id> expectation=<leg-or--> <detail>` on stdout, in addition to the
existing `CONTEXT:` summary line. Text is sufficient for the selftest; a
`findings` array in the receipt is optional.

## 3. Isolated fixture recipe

### 3.1 Layout

One `tempfile.mkdtemp(prefix="tameshi-r15-context-capture-selftest.", dir="/tmp")`;
one fresh case tree per case:

```
<scratch>/
  home/                                  # minimal HOME for git/python children
  case-<name>/
    lane/
      tools/context-capture.py           # byte copy of the tool under test
      tools/pin-disposition.py           # synthetic probe stub
      tools/mutate-and-run.sh            # synthetic six-leg runner text
      .ufo/evidence/round-13/pin-manifest.json
      .ufo/evidence/round-13/expected.json
      .ufo/evidence/round-14/context-receipt.json   # sentinel bytes
      .git/                              # present except in control-ineffective
```

Every case invokes the **copy** at `<case>/lane/tools/context-capture.py`. This
does three jobs at once: no input path outside the temp root is read (the tool's
`base_receipt()` hashes the invoked file), the production `tools/` depth is
exercised, and the service protocol's "exercise the copy it is handed" property
holds. Copying reads only the tool's own bytes, which are its identity, not a
live input.

### 3.2 Synthetic probe (`lane/tools/pin-disposition.py`)

Green stub — stdlib only, self-hashing, deterministic, writes only stdout:

```python
#!/usr/bin/env python3
import hashlib, json, os, sys
LEGS = ("js-kimi-census", "bash-surface-census", "bash-tsukuroi-census",
        "bash-mado-verify", "bash-checklist-run", "js-claims-check")
doc = {
    "schema": "pin-disposition-v1",
    "status": "ok",
    "observed_at": "2026-10-20T00:00:00Z",
    "tool_sha256": hashlib.sha256(
        open(os.path.realpath(__file__), "rb").read()).hexdigest(),
    "legs": [{"leg": leg, "content_status": "present",
              "pinned": {"status": "verified"}} for leg in LEGS],
}
# variant hooks are added only in the named fixture variants:
#   mismatch:        if "GIT_DIR" in os.environ: doc["injected"] = True
#   payload-digest:  doc["tool_sha256"] = "0" * 64
#   baseline-exit3:  sys.exit(3)
#   injected-exit3:  sys.exit(3) only when "GIT_DIR" in os.environ
#   non-utf8:        sys.stdout.buffer.write(b"\xff"); sys.exit(0)
#   sleep:           time.sleep(3) before writing the document
sys.stdout.write(json.dumps(doc, sort_keys=True) + "\n")
```

The green stub deliberately ignores `GIT_DIR`; the mismatch variant is the only
one that reads it. `observed_at` is fixed, so `raw_stdout_equal` is true in the
green case. The probe must accept (and may ignore) the production argv
`--manifest .ufo/evidence/round-13/pin-manifest.json --root <fleet>`.

### 3.3 Synthetic runner (`lane/tools/mutate-and-run.sh`)

Must satisfy `HEADER_ROW_RE`, `PIN_CONST_RE`, `REV_CONST_RE`,
`RUN_REGRESSION_RE` and `CALL_RE` exactly (`:83-105`). Generate values, do not
hand-count hex: for suffix index `i` in JS=1, BASH=2, TSUKUROI=3, MADO=4,
CHECKLIST=5, CLAIMS=6, use `PIN_<S> = str(i) * 64`, `REV_<S> = str(i) * 40`.

```
#!/usr/bin/env bash
# js-kimi-census kimi/kimi-census.mjs 0/0 (0%)
# bash-surface-census kagi/surface-census.sh 0/0 (0%)
# bash-tsukuroi-census tsukuroi/census.sh 0/0 (0%)
# bash-mado-verify mado/mado-verify.sh 0/0 (0%)
# bash-checklist-run kagi/checklist.sh 0/0 (0%)
# js-claims-check kimi/claims-check.mjs 0/0 (0%)

PIN_JS=<64 hex digit 1>
REV_JS=<40 hex digit 1>
PIN_BASH=<64 hex digit 2>
REV_BASH=<40 hex digit 2>
PIN_TSUKUROI=<64 hex digit 3>
REV_TSUKUROI=<40 hex digit 3>
PIN_MADO=<64 hex digit 4>
REV_MADO=<40 hex digit 4>
PIN_CHECKLIST=<64 hex digit 5>
REV_CHECKLIST=<40 hex digit 5>
PIN_CLAIMS=<64 hex digit 6>
REV_CLAIMS=<40 hex digit 6>

run_regression() {
  regression_case_git js-kimi-census 'kimi/kimi-census.mjs' "$PIN_JS" "$REV_JS" "cmd" 'arg' "$TABLE_JS"
  regression_case_git bash-surface-census 'kagi/surface-census.sh' "$PIN_BASH" "$REV_BASH" "cmd" 'arg' "$TABLE_BASH"
  regression_case_git bash-tsukuroi-census 'tsukuroi/census.sh' "$PIN_TSUKUROI" "$REV_TSUKUROI" "cmd" 'arg' "$TABLE_TSUKUROI"
  regression_case_git bash-mado-verify 'mado/mado-verify.sh' "$PIN_MADO" "$REV_MADO" "cmd" 'arg' "$TABLE_MADO"
  regression_case_git bash-checklist-run 'kagi/checklist.sh' "$PIN_CHECKLIST" "$REV_CHECKLIST" "cmd" 'arg' "$TABLE_CHECKLIST"
  regression_case_git js-claims-check 'kimi/claims-check.mjs' "$PIN_CLAIMS" "$REV_CLAIMS" "cmd" 'arg' "$TABLE_CLAIMS"
}
```

`run_regression() {` and the closing `}` must start at column 0. No other
`PIN_`/`REV_` definition lines may appear anywhere in the file (the parser
counts exactly six of each). Header and call orders must agree with the
manifest leg order.

### 3.4 Manifest and expected documents

```json
{"schema": "pin-manifest-v1",
 "derived_from": {"path": "tools/mutate-and-run.sh",
                  "sha256": "<sha256 of the runner bytes just written>"},
 "legs": [{"leg": "...", "repo": "...", "path": "...",
           "pinned_commit": "<same as REV value>",
           "expected_sha256": "<same as PIN value>"}, ... six, call order]}
```

```json
{"inputs": {"tools/pin-disposition.py": "<sha256 of the probe bytes just written>"}}
```

### 3.5 Git precondition

Green and every control-dependent case need the fixture lane to be a local
repository. Build it with no network and no user/system config:

```python
subprocess.run(["git", "-c", "init.defaultBranch=main", "init", "-q", str(lane)],
               env=fixture_env, capture_output=True, timeout=30)
fixture_env = {"PATH": os.environ["PATH"], "HOME": str(scratch/"home"),
               "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
               "LC_ALL": "C"}
```

Do not create a commit, remote, or hook. The `control-ineffective` case omits
this step. Scratch under `/tmp` is assumed not to be inside a git work tree; if
the builder can detect upward discovery (`git -C <scratch> rev-parse
--show-toplevel` exits 0), that one case must report
`SELFTEST: COULD_NOT_EVALUATE` rather than a fabricated FAIL.

### 3.6 Child invocation

```python
subprocess.run(
    [sys.executable, "-I", str(copy_path),
     "--root", str(lane),
     "--receipt", ".ufo/evidence/round-15/context-receipt.json"],
    cwd=str(lane), env=fixture_env, stdin=subprocess.DEVNULL,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
```

Capture bytes and decode per assertion: the `non_utf8_output` case deliberately
makes a text-mode capture fail. `-I` follows `witness-metadata.py:1136` and makes
the child independent of `PYTHON*` environment. The tool itself may default
`--root` to the copy's lane; at least one green case should omit `--root` to pin
that derivation.

### 3.7 Hermeticity invariants (assert these, do not assume them)

- H1 One `/tmp` scratch; every case rebuilt from scratch; green cleanup via
  `shutil.rmtree`; red keeps the tree and prints its path.
- H2 Fixture digests are computed from the bytes just written, never copied from
  live lane files.
- H3 No live path is referenced in any fixture: no `/home/...`, no fleet root, no
  round-13/14 evidence bytes.
- H4 No network: only local `git init` / `git rev-parse`; no clone/fetch/remote;
  no URL in any fixture. `GIT_TERMINAL_PROMPT=0` is already in the control env.
- H5 The round-14 sentinel at `lane/.ufo/evidence/round-14/context-receipt.json`
  has fixed builder-written bytes; assert byte identity after every case.
- H6 Recursive digest of the case lane before and after each run: the only
  allowed new/changed path is `.ufo/evidence/round-15/context-receipt.json`
  (and nothing at all for exit 64 and retained mode).
- H7 `python3` and `git` are declared substrate. If `shutil.which` fails, print
  `SELFTEST: COULD_NOT_EVALUATE (...)` and exit 2 with fixtures kept
  (`pin-disposition.py:603` precedent), never pass or fail.
- H8 The selftest wraps fixture construction in `try/except Exception` and maps a
  crash to exit 2 `SELFTEST: COULD_NOT_EVALUATE`, so a setup crash is never
  counted as a red case.
- H9 The probe stub is stdlib-only and self-hashing; it never touches the
  filesystem outside its own lane (except the optional marker below).
- H10 The selftest never invokes the tool with no arguments against the real
  lane: no-argument invocation is the prospective capture path.

### 3.8 Selftest output contract

Follow `evidence-disposition.py:1510-1857` exactly in shape:

- one `SELFTEST_CASE <name> PASS|FAIL (<detail>)` line per executed case;
- `SELFTEST: PASS (<n>/<n>)` and exit 0 on green;
- `SELFTEST: FAIL (<n>/<total> failed: <names>; fixtures kept at <path>)` and
  exit 1 on any red;
- `SELFTEST: COULD_NOT_EVALUATE (<reason>; fixtures kept at <path>)` and exit 2
  for absent substrate or a construction crash;
- the denominator is the number of executed cases, not a declared constant.
  Every case asserts process exit, the expected token/ID set, receipt presence
  or absence, and the sentinel digest.

## 4. Literal case matrix

Base fixture = green tree above. "IDs" are exact; `[existing]` marks tokens
already in the historical source, all others are the proposed literals of §2.
Every case also asserts the §3.7 H5/H6 invariants.

| Case | Delta from green | Exit | Stdout token | Exact IDs | Receipt |
|---|---|---:|---|---|---|
| `ok-bounded` | none | 0 | `CONTEXT: OK (` | none | round-15 receipt, `status=ok`, `exit=0`, `runs.argv_equal=true`, `runs.cwd_equal=true` |
| `ok-default-root` | omit `--root`; invoke the copy | 0 | `CONTEXT: OK (` | none | same, under the copy's lane |
| `mismatch-injected` | probe emits `injected:true` under `GIT_DIR` | 1 | `CONTEXT: MISMATCH (` | `injected_observation_mismatch` | `status=mismatch` |
| `probe-injected-exit3` | probe exits 3 only under `GIT_DIR` | 1 | `CONTEXT: MISMATCH (` | `injected_observation_mismatch` | `comparison.error` present |
| `payload-digest` | probe emits `tool_sha256="0"*64` in both runs | 1 | `CONTEXT: MISMATCH (` | `probe_payload_digest_mismatch` | `status=mismatch` |
| `control-ineffective` | omit `git init` | 1 | `CONTEXT: MISMATCH (` | `poison_control_ineffective` | `positive_control.effective=false` |
| `probe-source-pin` | wrong digest in `expected.inputs` | 1 | `CONTEXT: MISMATCH (` | `probe_source_digest_mismatch` | source flag false |
| `runner-source-pin` | wrong `derived_from.sha256` | 1 | `CONTEXT: MISMATCH (` | `runner_source_digest_mismatch` | source flag false |
| `mapping-header` | change one header path | 1 | `CONTEXT: MISMATCH (` | `header_matches_manifest` | leg expectation |
| `mapping-call` | change one call path | 1 | `CONTEXT: MISMATCH (` | `leg_call_matches_manifest` | leg expectation |
| `mapping-pin-value` | change one `PIN_x` value | 1 | `CONTEXT: MISMATCH (` | `pin_name_and_value_match_manifest` | leg expectation |
| `mapping-rev-value` | change one `REV_x` value | 1 | `CONTEXT: MISMATCH (` | `rev_name_and_value_match_manifest` | leg expectation |
| `mapping-order` | swap two call lines | 1 | `CONTEXT: MISMATCH (` | `runner_leg_order_mismatch` | `leg_order_equal=false` |
| `missing-input` | delete `tools/mutate-and-run.sh` | 2 | `CONTEXT: INVALID (kind=missing_input` | `missing_input` [existing] | `status=invalid_input`, `error.kind` same |
| `unreadable-input` | make manifest path a directory | 2 | `... kind=unreadable_input` | `unreadable_input` [existing] | same |
| `invalid-json` | manifest bytes `{` | 2 | `... kind=invalid_json` | `invalid_json` [existing] | same |
| `invalid-utf8` | manifest bytes `\xff` | 2 | `... kind=invalid_utf8` | `invalid_utf8` [existing] | same |
| `invalid-manifest` | manifest schema `wrong` | 2 | `... kind=invalid_manifest` | `invalid_manifest` [existing] | same |
| `invalid-expected` | expected `{}` (no `inputs`) | 2 | `... kind=invalid_expected` | `invalid_expected` [existing] | same |
| `runner-unparsed` | delete `run_regression() {` | 2 | `... kind=runner_unparsed` | `runner_unparsed` [existing] | same |
| `probe-baseline-unusable` | probe exits 3 always | 2 | `... kind=probe_baseline_unusable` | `probe_baseline_unusable` [existing] | same |
| `poison-path-exists` | point injection at an existing fixture file | 2 | `... kind=poison_path_exists` | `poison_path_exists` [existing] | same |
| `missing-executable` | child `PATH=""` | 2 | `... kind=missing_executable` | `missing_executable` [existing] | same |
| `non-utf8-output` | probe writes `b"\xff"` | 2 | `... kind=non_utf8_output` | `non_utf8_output` [existing] | same |
| `timeout` (optional) | probe sleeps 3 s; `--probe-timeout-seconds 1` | 2 | `... kind=timeout` | `timeout` [existing] | same |
| `usage-unknown-flag` | argv `--bogus` | 64 | `usage:` on stderr | none (no ID exists historically) | **no receipt** |
| `usage-selftest-extra` | argv `--selftest --json` (or `--selftest extra`) | 64 | `usage:` on stderr | none | no receipt |
| `usage-root-no-value` | argv `--root` | 64 | `usage:` on stderr | none | no receipt |
| `usage-check-retained-no-file` | argv `--check-retained` | 64 | `usage:` on stderr | none | no receipt |
| `help` | argv `--help` | 0 (historical) | `usage:` on stdout | none | no receipt |

Deliberately absent:

- **No case for `env_delta_matches_declared` / `baseline_has_GIT_DIR` through
  capture.** They are true/false by construction (§1). If retained mode
  recomputes `decide()`, one doctored retained receipt may pin
  `environment_delta_mismatch`, labeled a recomputed declaration, not a capture.
- **No case for a leg-set mismatch** as a minimal pair: renaming one leg
  consistently yields six IDs at once (`runner_leg_set_mismatch` plus all five
  per-leg `CHECKS` for the absent manifest leg) because the manifest leg has
  neither header nor call. Pin that exact six-ID set only if the extra breadth is
  wanted.
- **No case for `exec_failed` / `invalid_fleet_root` / `unreadable_input` via
  permissions.** They are not deterministically reachable: `exec_failed` requires
  the resolved `python3` path to fail during spawn; fleet root under `--root` is
  always a directory; permission-based unreadability does not hold for uid 0.
  The directory-based `unreadable_input` case above is privilege-independent and
  is preferred.

## 5. Retained-receipt check mode (concrete, minimal)

The interface asks for "a useful retained-receipt check CLI, digest-bound
snapshot mode if needed". Smallest shape that reuses every existing semantic:

```
python3 tools/context-capture.py --check-retained FILE [--root LANE]
```

Read-only, no probe execution, no injection, no write. Ordered fail-closed:

1. read/parse FILE (`invalid_json` / `invalid_utf8` as today);
2. `schema` must equal the round-15 receipt schema, else exit 2
   `retained_schema_mismatch` — this is what stops a round-14 receipt from being
   reinterpreted under new rules;
3. `tool_sha256` must equal the digest of the invoked file, else exit 2
   `retained_tool_digest_mismatch`;
4. every `sources.*.sha256` must re-hash the named lane-relative file under
   `--root`; missing -> exit 2 `missing_input`, mismatch -> exit 2
   `retained_source_digest_mismatch`;
5. recompute `decide(receipt)`; findings -> exit 1 with the §2 IDs, none -> exit 0;
6. print `CONTEXT_RETAINED: OK|MISMATCH|INVALID (receipt=<path> exit=N)` plus
   `FINDING` lines. 64 usage writes nothing.

Boundary that must be in the docstring and registry: retained mode proves the
retained declarations are internally consistent and that the named input bytes
still match their recorded digests. It does not authenticate receipt authorship,
does not prove a capture ran, and does not establish any environment property.
That is the same configured-authority boundary as `evidence-disposition.py`
("It never executes receipt argv").

Selftest cases for it: `retained-clean` -> 0/no finding; `retained-schema` using
the literal `tameshi-round14-context-receipt-v1` -> 2
`retained_schema_mismatch`; `retained-tool-drift` -> 2
`retained_tool_digest_mismatch`; `retained-source-drift` (one byte appended to
the fixture runner after capture) -> 2 `retained_source_digest_mismatch` with
zero semantic findings; `retained-declared-mismatch` (clean receipt with
`comparison.equal=false`) -> 1 `injected_observation_mismatch`. The last is a
recomputation test of `decide()`; label it as such.

## 6. Implementation-critical deltas for `tools/context-capture.py`

These are the points where a literal promotion of the historical file breaks the
selftest or the round-15 contract.

**P0 — required for the promoted gate to work at all**

1. **Root depth.** `LANE_ROOT` is four `dirname`s (`:46`) only because the file
   sits under `.ufo/evidence/round-14/`. At `tools/context-capture.py` the lane
   is **two** `dirname`s; the fleet root is one more. A copied expression puts
   every read outside the intended lane and the selftest's copy case fails
   honestly but loudly. Prefer an explicit `--root` (default two dirnames) and
   use the same root in `lane_path()`.
2. **Output path.** `OUTPUT_REL` (`:58`) must become
   `.ufo/evidence/round-15/context-receipt.json`, with a caller-selected
   `--receipt` override. Never write a round-14 path; round-14 bytes stay frozen.
3. **Stable IDs.** `decide()` (`:553-580`) must return `(id, detail)` pairs and
   print `FINDING <id> expectation=<leg> <detail>`; the free-form
   `reasons` strings alone do not satisfy the gate standard. Keep `reasons` for
   continuity and add the IDs.
4. **Catch-all.** An uncaught exception anywhere in `evaluate`/`decide` must map
   to exit 2 `unexpected_exception`, not a traceback exiting 1. Today only
   `InvalidContext` is caught (`:615-628`).
5. **64 writes no receipt** (already true, `:606-613`) and `--help` must be
   decided explicitly. Preserve historical exit 0 only if the registry states
   help is not a verdict; otherwise return 64 for `-h/--help` so "exit 0" always
   means a written clean receipt. The selftest pins whichever is chosen.
6. **Program name in stderr.** `:610,624` say `capture-context.py`; the promoted
   name is `context-capture.py`. Pin only `usage:` (and `CONTEXT:`/`kind=`), not
   the filename, in the selftest.

**P1 — needed by the fixture recipe**

7. `--root LANE` (scope), `--receipt PATH` (scope), `--check-retained FILE`
   (§5), `--inject-git-dir PATH` (hermetic poison path; default keeps one
   declared constant, updated to the round-15 name). The receipt records the
   actual injected value in `environment.injected_env` and `poison_path`; the
   `env_delta_matches_declared` comparison must compare against the effective
   declared value, not the module literal. No claim changes: the receipt says
   which override was used.
8. `findings: [{"id","expectation","detail"}]` in the receipt for exit 1/2, so
   retained mode and the L1 inspection read machine IDs.
9. `--selftest` implemented in the tool itself, building the §3 fixtures and
   invoking the copy; no import of internal helpers as the test seam.

**P2 — only if the specific path must be covered**

10. `--probe-timeout-seconds N` (default 120, bounded positive integer) purely so
    the `timeout` refusal path can be exercised in one second. Without it,
    declare that path uncovered; do not fake it with a 120 s case.
11. `--json` output for the capture/retained modes (house convention only).

Scope guard: none of 1-11 adds an environment-independence claim or a broad
validation feature. The selftest's injected-mismatch fixture proves the
comparison mechanism responds to a differing observation; it is not evidence of
hermeticity, result reuse, or safe environment substitution. Keep the historical
`not_compared` / `result_reuse` text unchanged.

## 7. Registry and 64-class advice (for Registry / L1; not edited here)

Round-14 routed defect 5 asks for two things beyond the tool: the row must be a
**gate** row, and both exit-64 paths must be explicit. Suggested cells:

| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| invocation context capture | gate | `python3 tools/context-capture.py [--receipt PATH]`; `python3 tools/context-capture.py --check-retained FILE` | 0 bounded equal observation + effective poison control + exact declared env delta + matching source pins + six-leg mapping, or retained snapshot consistent; 1 observed mismatch / ineffective control / mapping mismatch, stable IDs; 2 could-not-evaluate missing, unreadable, invalid, or digest-mismatched input, or unusable baseline probe; 64 could-not-evaluate usage, no receipt written | `python3 tools/context-capture.py --selftest` | round-15 receipt schema; literal expected exit/ID table in the tool selftest; historical round-14 receipt and round-13 manifest/runner/probe bytes unchanged | prospective mode writes only `.ufo/evidence/round-15/context-receipt.json`; retained mode read-only; selftest isolated `/tmp/tameshi-r15-context-capture-selftest.*` | tameshi |

And for the C1 row, the round-14 request "map C1's exit64 explicitly to
could-not-evaluate" means the verdict-map cell should read, additively:

`2 could-not-evaluate invalid/missing/tampered inputs; 64 could-not-evaluate usage`

The same explicit class should appear in the round-15 capability statement: both
the C1 gate and the context gate classify 64 as could-not-evaluate (usage, no
receipt), distinct from the 2 class (could-not-evaluate input/setup). Neither is
a promotion point; the scalar stays 6.

## 8. Checks for L1 after the implementation lands (not executed here)

1. `python3 tools/context-capture.py --selftest` — expect exit 0, every case line
   PASS, and the closing `SELFTEST: PASS (<n>/<n>)` with `n` equal to the number
   of emitted case lines. Confirm the fixtures were removed on green.
2. `python3 tools/context-capture.py --check-retained .ufo/evidence/round-15/context-receipt.json`
   — expect exit 0 after a capture, and no writes.
3. One prospective capture writes only the round-15 receipt; verify the round-14
   receipt digest is unchanged across the run.
4. Negative read: run `--selftest` with `GIT_DIR` and a bogus `HOME` in the
   parent environment; the result must not change, because every case's child
   env is explicit and the tool strips `GIT_*`. If it changes, the selftest is
   leaking ambient environment and the case is not hermetic.
5. Registry spot-check: the context row is a gate row; both rows' 64 class says
   could-not-evaluate.

## 9. Risks, bounds, blockers

- **Not executed.** Everything above is a source-read recipe. I did not run the
  historical script, git, or any selftest, so the fixture tree is unvalidated in
  practice; the first selftest run is the real test. If a regex detail differs
  from my reading, fix the fixture, not the predicate.
- **Proposed IDs.** `injected_observation_mismatch`, `probe_payload_digest_mismatch`,
  `environment_delta_mismatch`, `baseline_carries_git_dir`,
  `poison_control_ineffective`, `probe_source_digest_mismatch`,
  `runner_source_digest_mismatch`, `runner_leg_set_mismatch`,
  `runner_leg_order_mismatch`, and the three `retained_*` IDs are literals I
  propose. If ContextGate picks different names, the selftest, the receipt
  `findings`, and the registry must use those names; the important property is
  one literal per branch, not my spelling.
- **Substrate.** The recipe needs `python3` and `git` in the child `PATH`. Both
  are already the historical tool's declared dependencies (`:31`); the selftest
  must report COULD_NOT_EVALUATE, not pass or fail, if either is absent.
- **Two capture-unreachable branches.** `env_delta_matches_declared` and
  `baseline_has_GIT_DIR` cannot fail through the real CLI; claiming capture
  coverage for them would be false. Retained-doctored recomputation is the only
  honest seam, and it must be labeled as declaration checking.
- **Historical round-14 receipt is not a round-15 input.** It stays byte-frozen
  and is rejected by retained schema binding; it is not a fixture source and not
  a replay target.
- No blocker for ContextGate: the recipe is implementable with the existing
  semantics plus the P0/P1 deltas. The one coordination risk is the `tools/`
  path-depth change (P0.1), which is easy to miss and silently points the copy
  case at the wrong lane; that detail is also sent to L1.

Tool installs/updates by this seat: none. Files written by this seat: this report
only.

Report: .ufo/waves/round-15/w1/SpecHermetic.md
