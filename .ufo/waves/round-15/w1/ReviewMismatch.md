# ReviewMismatch — planned C1 comparison-mismatch (exit 1) stable ID

Lane: tameshi · Round 15 · Wave w1 · Role: leaf reviewer (no dispatch, no gate runs, no verification execution).

## Read revision and scope

- Tameshi HEAD read: `a9cf4da78f2514c7bedd91a850a88590009d7df0`.
- `tools/context-capture.py` **does not exist** at read time. The C1 review is therefore against the historical source and the planned contract only. Every statement about the new tool is a requirement, not an observation.
- Historical bytes unchanged at read (`git status` clean for `.ufo/evidence/round-14`, `tools`, `SKILL.md`):
  - `.ufo/evidence/round-14/capture-context.py` sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` (matches the pin in `round-14/verification.json:8`)
  - `tools/pin-disposition.py` sha256 `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`
  - `tools/mutate-and-run.sh` sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`
  - `.ufo/evidence/round-13/pin-manifest.json` sha256 `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6`
  - `.ufo/evidence/round-13/expected.json` sha256 `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336`
- Peer edits present in the working tree and out of C1 scope: `corpus/QUALITY.md` and `corpus/SOURCES.md` modified; `corpus/lessons/round-15.md` untracked.
- Tools installed or updated by this seat: **none**. Read-only hashing (`sha256sum`), `git status`, and `os.path` arithmetic were the only commands run.

## 1. Observable evidence in the historical source

| Fact | Where |
|---|---|
| The comparison predicate is `comparison.equal is not True`. It is the first reason in `decide()`. | `capture-context.py:560-563` |
| Every other failure is a separate predicate that returns the same exit 1: env delta, baseline GIT_DIR, positive control, probe digest, runner digest, mapping. | `:564-577` |
| `decide()` returns `("mismatch", 1, reasons)`, where reasons are **free-text strings**. There are no stable finding IDs anywhere in the file. | `:553-580` |
| stdout prints `CONTEXT: MISMATCH (...)` via `status.upper()`. That is a status token, not a finding ID. | `:637-642` |
| `main` returns 64 on any argument (no `--selftest` mode exists). | `:605-613` |
| Output path is hardcoded to round-14 (`OUTPUT_REL`), and `LANE_ROOT` derives from **four** `dirname` calls. | `:46-47`, `:58` |
| `comparison_block` normalizes by removing only top-level `observed_at`, then compares canonical JSON. `raw_stdout_equal` is recorded but not a predicate. | `:350-392` |
| Injected-run unusable (non-zero exit, non-JSON, missing `observed_at`) is folded into `equal: False` and therefore into exit 1. | `:362-379` |
| `safe_env()` strips every `GIT_*` key before building `base_env`; the injection adds only `GIT_DIR`. | `:184-187`, `:524-536` |
| The probe itself scrubs `GIT_*` through `git_env()`. | `tools/pin-disposition.py:196-210` |

Retained round-14 evidence:

- `round-14/verification.json:63-75`: the only retained run of the context tool is `context_capture`, exit 0, `CONTEXT: OK (... probe-equal=True poison-control=True runner-mapping=True)`. **No retained run of the historical tool exits 1.**
- `round-14/context-receipt.json`: `status: ok`, `exit: 0`, `reasons: []`. `comparison.equal: true`, `raw_stdout_equal: true`, `observed_at` baseline and injected both `2026-10-20T06:35:01Z`. Positive control `baseline.exit 0 → injected.exit 128`, effective.
- `round-14/guardrails.json:30-33`: the exit-1 control `context_setup_missing_field` is an **ad hoc `python -c` argv** that reads the receipt JSON and prints `missing_injected_environment`. It does not call `decide()` and the string is not emitted by the tool.
- `SKILL.md:1602`: the registry row for the context probe says `0/1/2` with `no standalone selftest`. It has no `64` entry, and the probe's exit-1 covers both comparison mismatch **and** failed control with one code.
- Routed defect 5 (`corpus/lessons/round-14-verifier-spotcheck.md:160`) requires: register as a gate; standalone isolated self-invocation; literal expected exit **and** finding-ID pairs; helper-only controls do not satisfy this clause.

## 2. Exact acceptance criterion — comparison mismatch, exit 1

**AC-1 (token minted, not found).** The promoted `tools/context-capture.py` MUST emit one stable finding token for the failure of predicate `comparison.equal is not True`. No such token exists in historical source. Naming is the planner's choice; the sibling pattern is `controls_mismatch` (repeat-control), `metadata_inconsistent` (witness-metadata). Suggested: `comparison_mismatch`.

**AC-2 (exit mapping literal).** Exactly one literal table maps finding token → exit code (mirror `repeat-control.py:122-128` `EXIT_BY_ID`). `comparison_mismatch` → `1`. The token must not be inferred from `status`.

**AC-3 (CLI-visible).** The token appears in stdout as a single deterministic line (suggested `CONTEXT_FINDING: comparison_mismatch`) **and** in the receipt as one canonical field. Pick one field name; do not rely on parsing the free-text `reasons` list.

**AC-4 (isolated self-invocation).** `--selftest` copies the tool file into a `tempfile.mkdtemp()` tree laid out as `<tmp>/tameshi-shokunin/tools/context-capture.py` and invokes that copy as a child process via `subprocess`. It asserts, for the comparison case: child exit == `1`, the finding line == `comparison_mismatch`, and the recorded finding list == `[comparison_mismatch]` exactly. Cases are a literal tuple in the style of `witness-metadata.py:659-690` (`case`, `expected_id`, `expected_reason`, `expected_exit`, `setup`). The `rmtree` runs in `finally`.

**AC-5 (fixture must isolate the predicate).** Each of the following is required, or the case confounds another predicate:

- `git init -q` in the fixture root. Without it the positive control fails baseline (`rev-parse --git-dir` non-zero), producing a control finding rather than a comparison finding.
- A synthetic six-leg runner using the canonical leg names, with six header rows matching `HEADER_ROW_RE`, six `PIN_*`/`REV_*` constants, and six `regression_case_git` calls in `run_regression()`, matching a fixture manifest. Otherwise the mapping predicate fires with exit 1 for the wrong reason.
- Fixture `.ufo/evidence/round-13/expected.json` and `pin-manifest.json` whose digests match the fixture probe and runner.
- Fixture probe: `schema: pin-disposition-v1`, `status: ok`, six legs each with `pinned.status == verified` and `content_status != unavailable`, top-level `observed_at`, `tool_sha256` equal to its own digest.
- The injected run differs from baseline in a **non-`observed_at`** key (e.g. a marker derived from the `GIT_DIR` env value). Baseline must not depend on `GIT_DIR`.
- `/nonexistent/tameshi-round14-poison` must not exist; the fixture must not create it.
- No live lane, sibling, or network reads. Writes only inside the temp tree.

**AC-6 (sub-reason pinned).** The expected reason string (the `normalized JSON mismatch` branch of `comparison_block`) is pinned in the case tuple. If the injected-unusable branch is kept under the same token (historical policy, `lesson:97`), it gets a second pinned case with a distinct `expected_reason` (e.g. `injected_unusable`).

**AC-7 (controls distinct).** A failed positive control and an ineffective control MUST NOT emit `comparison_mismatch`. They get their own tokens (or are pinned as their own case) and their own exit-1 case. The SKILL registry row must reflect the split.

**AC-8 (load-bearing check, L1 only).** With the comparison predicate disabled (`equal` forced `True`), the AC-4 case must fail. This is the SKILL mutation bar for nominal suites. L1 runs this once; it is not a selftest requirement.

**AC-9 (round-15 output and roots).** `LANE_ROOT` derives from **two** `dirname` calls for a `tools/` location (see FP-6). Output path is `.ufo/evidence/round-15/context-receipt.json` only. The round-14 path is never written.

## 3. Likely false positives (guard against)

- **FP-1 — exit-only assertion.** Exit 1 is shared by at least eight predicates (`capture-context.py:560-577`). A selftest asserting only `exit == 1` passes for the wrong reason. Reject. AC-4 requires the exact token.
- **FP-2 — missing git init.** Without `git init`, the control fails and exit 1 is attributed to the wrong predicate. Required fixture detail (AC-5).
- **FP-3 — raw-stdout equality as a predicate.** `observed_at` is second-resolution (`%Y-%m-%dT%H:%M:%SZ`). Baseline and injected runs straddling a second boundary give `raw_stdout_equal: false` with normalized `equal: true`. Making raw equality a predicate yields spurious exit 1. Keep normalized comparison only.
- **FP-4 — live sibling movement.** The probe reads live worktree and HEAD state; `not_compared` already lists "concurrent sibling movement". Two real runs can differ for reasons unrelated to `GIT_DIR`. The mismatch detail must describe "observation differed between runs" and must not attribute cause. Retry remains out of scope (historical "no retry, no A-B-A").
- **FP-5 — `baseline_has_GIT_DIR` is unreachable from the CLI.** `safe_env()` strips every `GIT_*` key before `base_env` is built, so `"GIT_DIR" in base_env` is always False. Likewise `env_delta` is always `["GIT_DIR"]`. Do not claim a selftest case for `baseline still carries GIT_DIR`; it can only be exercised by changing code, which is out of scope.
- **FP-6 — root depth (implementation-critical).** Copying the historical four-`dirname` `LANE_ROOT` derivation into `tools/` yields `LANE_ROOT=/home/vgpnk/Projects` and `FLEET_ROOT=/home/vgpnk`. Consequences: reads of `tools/pin-disposition.py` fail as exit 2 `missing_input`; and `write_receipt` would create `/home/vgpnk/Projects/.ufo/evidence/round-15/` **outside the lane**. Verified by path arithmetic only: naive → `/home/vgpnk/Projects`; correct (2 dirnames) → `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- **FP-7 — duplicate keys in probe output.** `parse_probe_document` (`:340-347`) uses plain `json.loads`, whereas `parse_json` rejects duplicate keys (`:158-181`). A probe emitting duplicate keys can change the normalized comparison silently. Low severity; optional hardening.
- **FP-8 — retained-receipt replay.** The historical receipt records `tool_sha256 = 7313e9a2…` (the historical file). A checker comparing against the new file will false-mismatch every round-14 receipt. Also, `mapping.all_match` cannot be replayed without retained runner bytes (only the parsed mapping is retained). A replay checker must report *not replayable* for mapping, not trust the recorded `all_match`.

## 4. Unearned claims to reject

- **U-1** — "capture-context.py already has stable finding IDs." False. `decide()` emits free-text reasons; the only token is the status word.
- **U-2** — "round-14 retains exit-1 comparison evidence." False. The only retained run is exit 0. The exit-1 control in `guardrails.json` is an ad hoc argv that never calls `decide()`.
- **U-3** — "equal raw stdout including timestamp shows determinism." Coincidence at second resolution (both `06:35:01Z`). Not evidence.
- **U-4** — "exit 1 means GIT_DIR changed the probe." Exit 1 means normalized observations differed between two runs. Cause is not established; the probe itself scrubs `GIT_*`, so the injection tested the scrub.
- **U-5** — "the selftest proves hermeticity, environment independence, or round-14 receipt correctness." It proves only CLI semantics on synthetic fixtures.
- **U-6** — "a passing comparison-mismatch selftest upgrades the registry or scalar." Registry promotion and the scalar are separate claims and must cite their own evidence.

## 5. Minimum fix vs optional hardening

Required for C1 (minimum):
- AC-1 through AC-7 and AC-9.
- Two-`dirname` root derivation (FP-6). This is a blocker: without it the tool can write outside the lane.
- Separate tokens for comparison mismatch and control failures (AC-7).

Optional hardening (not required for the ID):
- Refuse overwrite of an existing round-15 receipt (`write_new`-style, as in `repeat-control.py`).
- Duplicate-key rejection in `parse_probe_document` (FP-7).
- Separate token for injected-unusable (AC-6 alternative).
- L1 mutation check (AC-8) — run once by L1, not in the tool.

Not required: broad validation features, new environment claims, sibling-gate execution.

## 6. Expected CLI semantics for the comparison case (recommendation)

- Stdout: `CONTEXT: MISMATCH (...)` then `CONTEXT_FINDING: comparison_mismatch`.
- Exit: `1`.
- Receipt: `status: mismatch`, `exit: 1`, one canonical finding field `comparison_mismatch`, `reasons` retained as free text.
- The 64 path remains usage only and is not part of this case.

## 7. Blockers and handoff

- Blocker for the implementer: FP-6 (root depth). Message sent to `TameshiR15` (see below).
- Not a blocker: round-15 peer edits in `corpus/` are out of C1 scope.
- No checks, builds, tests, or formatters were run. No gate executed. No installs. No commits.
- The main agent should run once after all seats land: `python3 tools/context-capture.py --selftest` and the AC-8 mutation check; and confirm the AC-4 case's stdout and exit against the literal tuple.
