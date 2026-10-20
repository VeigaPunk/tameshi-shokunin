# ContextGate — round15 w1 executor report

Lane: tameshi-shokunin. Scope: `tools/context-capture.py` only (new file). No historical
bytes edited, no sibling tool files touched, no commits, no gate/selftest execution.

## Axes

- **calibration — improved (bounded capability).** The round-14 context instrument is
  promoted from an unregistered probe into a retained-receipt gate with a standalone
  isolated self-invocation and an explicit 0/1/2/64 lattice. Raw retained fields are
  re-derived; stored summary booleans, `status`, `exit` and `reasons` are never trusted.
  This is a capability declaration, not a measured score change.
- **operability — improved (bounded).** One maintained command (`--check`), one digest-bound
  explicit form, one hermetic `--selftest`; no capture, no live inputs, no writes in check
  mode, no git/probe execution.
- **depth / coverage / freshness / adjacency — unchanged.** No new target surface, no
  successor sweep, no seventh mutation case, no source ownership absorbed.
- Tool installs/updates: **none**.

## Delivered file

`tools/context-capture.py` — 2116 lines, untracked (`git status --porcelain` shows
`?? tools/context-capture.py`). sha256 of the delivered bytes at write time:
`0ed784e0076b3de5ec5000c3862a771a3e3e2eb83241da347a6cf3f2f2c61edc`.

Design authority taken from L1's final direction: minimal retained-only gate; no live
capture; no `--root`; historical script remains archived and is **not imported** (its
`main`/`evaluate`/`write_receipt` paths are never referenced). No `sys.path`/`runpy` import
of archived code, so no bytecode-disable hazard arises.

## CLI contract (landed, declared not executed)

```text
usage: context-capture.py --check [--receipt FILE --expected FILE] [--json]
       context-capture.py --selftest
```

| Invocation | Meaning |
|---|---|
| `python3 tools/context-capture.py --check` | Digest-bound replay of the frozen round-14 clean receipt against the built-in literal pin. |
| `python3 tools/context-capture.py --check --receipt FILE --expected FILE` | Check the named receipt against an expected-pin file (sha256 + exact id/exit). Both flags or neither. |
| `python3 tools/context-capture.py --selftest` | Real CLI subprocesses over synthetic mkdtemp fixtures. |
| no args / one of `--receipt`,`--expected` / unknown flag / `--selftest --json` | `usage_error`, exit 64, no files written. |

Expected pin schema `tameshi-context-expected-v1`, exactly four keys:

```json
{"schema": "tameshi-context-expected-v1",
 "receipt_sha256": "<64 lowercase hex>",
 "id": "<stable finding id or context_consistent>",
 "exit": 0}
```

Exit map: **0** clean; **1** re-derived or pinned-verdict mismatch (a matched exit-1 pin
still exits 1 — the pin asserts the retained verdict, never a clean substrate); **2**
could-not-evaluate (missing/unreadable/malformed/structurally invalid receipt or expected
pin, unusable baseline, snapshot digest mismatch, retained invalid-input record, internal
error); **64** usage/could-not-evaluate invocation.

Built-in frozen pin (`tools/context-capture.py:136-144`):
`.ufo/evidence/round-14/context-receipt.json`, sha256
`05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`,
id `context_consistent`, exit 0, tool declaration `7313e9a2…`.

L1's second frozen pair (expected file to be created by L1; values observed from the
retained file, not re-executed):
`.ufo/evidence/round-14/context-missing-env.json`, sha256
`1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`,
id `missing_injected_environment`, exit 1.

## Raw-field re-derivation (not stored-boolean replay)

- `recompute_comparison` (`:878`): strict-parses both `runs.*.stdout` documents with
  duplicate-key rejection; baseline must be a six-leg ok `pin-disposition-v1` document with
  `pinned.status == "verified"` and a top-level `observed_at`; canonical payloads are
  compared after removing **only** top-level `observed_at`; comparable digests,
  `raw_stdout_equal`, `equal`, `error` and both observed_at values are recomputed and
  compared to the recorded block. A payload/tool-digest disagreement yields
  `comparison_tool_digest_mismatch`; other disagreements yield `comparison_mismatch`.
- `recompute_environment` (`:805`): `injected_env` must be exactly
  `{"GIT_DIR": "/nonexistent/tameshi-round14-poison"}` and `env_delta_keys` exactly
  `["GIT_DIR"]`; absent/null `injected_env` yields the round-14 guardrail literal pair
  `missing_injected_environment`/exit 1; `baseline_has_GIT_DIR` must be literal `False`;
  poison-path facts must match.
- `recompute_runs`: re-derives argv/cwd equality and the bounded env delta from raw run
  records (`run_argv_mismatch`, `run_cwd_mismatch`, `run_env_delta_mismatch`).
- `recompute_positive_control` (`:981`): `baseline_ok`, `injected_reflects_poison`,
  `effective`, the configured env additions and env delta are recomputed from raw
  exits/stdout/stderr; disagreements or an ineffective control yield
  `positive_control_ineffective`.
- `recompute_sources`: probe `sha256 == declared_sha256` and runner
  `sha256 == manifest_declared_sha256` are recomputed as strings; match flags must be
  literal `True` (`probe_source_digest_mismatch`, `runner_source_digest_mismatch`).
- `recompute_mapping` (`:1038`): all five per-leg checks, per-leg `match`, leg
  set/order equality and `all_match` are recomputed from raw header/call/manifest/pin/rev/
  table fields; any recorded disagreement or a false recomputation yields
  `mapping_mismatch`.
- `verify_recorded_verdict` (`:1108`): stored `status`/`exit`/`reasons` are compared with
  the recomputed verdict; a disagreement is a finding (`receipt_verdict_mismatch`), not a
  trusted pass.
- Strict types: booleans must be literal `bool` (`is True`/`is False` checks), integers
  are not booleans, containers and lengths are validated. Wrong type/missing required
  container/duplicate key/non- UTF-8 → exit 2 with a stable id and no traceback.
- `apply_expected` (`:1265`) compares the recomputed primary id/exit to the pin. A clean
  receipt with a non-matching pin becomes `expected_verdict_mismatch`/exit 1; an exit-2
  result stays exit 2 and appends the pin finding.

Stable ids are declared in the module docstring (`:1-119`) and emitted by `check_receipt`.

## Standalone self-invocation

`--selftest` (`:2005`) invokes the **actual public CLI** as
`sys.executable -I SELF --check --receipt … --expected … --json` for every fixture under
one `tempfile.mkdtemp()` root, with a minimal child env including
`GIT_DIR=/nonexistent/context-selftest-poison`, then removes the root in a `finally`.

38 declared checks (not executed here): 31 receipt fixtures, 5 usage invocations, 2 hermetic
meta-checks. Literal expected pairs pinned in the cases include:

| Fixture class | Expected id / exit |
|---|---|
| clean | `context_consistent` / 0, with `findings == []` and echoed receipt sha |
| missing/null injected env | `missing_injected_environment` / 1 |
| raw comparison differs; observed_at summary lie | `comparison_mismatch` / 1 |
| probe digest declaration differs | `comparison_tool_digest_mismatch` / 1 |
| control ineffective / control flag lie | `positive_control_ineffective` / 1 |
| mapping check lie / equal-valued variable swap / order lie | `mapping_mismatch` / 1 |
| probe/runner source declaration lie | `probe_source_digest_mismatch` / `runner_source_digest_mismatch` / 1 |
| truthy match flag, string `all_match`, bool exit, widened exclusions, list comparison | `receipt_structure_invalid` / 2 |
| duplicate key, malformed JSON, non-object root, invalid UTF-8 | `receipt_json_invalid` / 2 |
| missing receipt | `receipt_missing` / 2 |
| wrong pinned digest | `snapshot_tampered` / 2 |
| missing/invalid expected; invalid digest | `expected_missing` / `expected_invalid` / 2 |
| stored verdict lie | `receipt_verdict_mismatch` / 1 |
| retained invalid-input record | `receipt_records_invalid_input` / 2 |
| unusable baseline document | `baseline_unusable` / 2 |
| mismatched expected verdict | `expected_verdict_mismatch` / 1 |
| 5 usage shapes | `usage_error` / 64 |
| hermetic meta | no live lane path in any output; only case dirs under the temp root |

The clean and missing-env fixtures are separate cases in the same temp root and must yield
0 vs 1. The clean case additionally asserts a present `findings` list and the echoed input
digest, so `--help` or a missing-key payload cannot satisfy it. Malformed/duplicate-key
fixtures pin the digest of their **malformed bytes**, so they exercise the parse path
rather than only `snapshot_tampered`.

## Historical preservation

- `.ufo/evidence/round-14/capture-context.py` and both retained receipts were read only.
  Observed digests: script `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`,
  clean receipt `05cb55b8…`, missing-env receipt `1ee9d09b…`.
- Static data inspection confirmed the clean/missing pair differ only by the removal of
  `environment.injected_env`, and that every field the gate re-derives (comparison
  digests/equal/observed_at, control flags, env delta, source equality, all six mapping
  rows) recomputes to the recorded clean values. This is a read-only data check, **not** a
  gate or selftest execution.
- `git status --porcelain` shows only the new `tools/context-capture.py` from this seat;
  round-14 paths are unmodified.

## Bounded non-claims

- The tool's declared `tool_sha256` is reported/pinned as a declaration, not
  authentication. The receipt-file digest pin is the integrity authority.
- A passing `--check` means the retained receipt's raw fields are self-consistent and
  reproduce the pinned verdict. It does **not** prove the historical probe/git commands
  were re-executed, nor establish environment, dependency, fixture or suite identity.
- `sources.*` digests are checked for internal consistency (sha vs declared) but are not
  rehashed against live lane files; the retained-only scope deliberately avoids live reads.
- No round15 prospective capture output is produced because no capture mode exists; L1
  explicitly withdrew that requirement. The archived script remains the only capture
  artifact.
- Selftest green and frozen-replay green are **not** claimed; L1 owns the single
  post-integration execution.

## Risks / review notes

1. The expected-pin file is an L1-created artifact; exact schema and both frozen pins are
   supplied in the handoff. A pin must use the **primary** finding id; for the missing-env
   receipt that is `missing_injected_environment`, with `receipt_verdict_mismatch` retained
   as a secondary finding.
2. The gate treats a recorded exit/status disagreement as exit 1, per the retained-verdict
   recomputation rule; it does not silently reclassify a stored "ok" as malformed.
3. `missing_injected_environment` is deliberately exit 1 (round-14 guardrail literal pair),
   while other missing required containers/types are exit 2.
4. Frozen mode reads exactly one archived receipt; explicit mode reads only the two named
   files. No network, no subprocess in check mode, no writes.

## Recommendations (bounded)

- L1: run `python3 tools/context-capture.py --selftest`; then
  `--check` (frozen clean) and `--check --receipt .ufo/evidence/round-14/context-missing-env.json
  --expected <new pin with sha 1ee9d09b…, id missing_injected_environment, exit 1>`.
- Registry: register the landed usage block verbatim; mark historical `capture-context.py`
  archived/not active; declare 0/1/2/64 with 64 = could-not-evaluate invocation.
- Do not claim a live capture or a broad environment result from this gate.
