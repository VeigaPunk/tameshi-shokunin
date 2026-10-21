# SimplifyReplay — YAGNI review of `tools/registry-replay.py`

**Verdict:** One clear dead parameter and one misleading CLI/doc surface; no falsifying defect in projection or publish logic. Do **not** delete `--run`, `live-dependent.json`, or the r23-shaped clone loop — they are the production integrator and evidence contract. Smallest safe code change: drop unused `publish(code, …)` argument and align `--project` JSON documentation (or gate stdout on `--json` only if human-readable report is still wanted).

**Reviewed revision:** `30feb14747b2543e1ea8e6dc3a55dd20e3121037` (`git rev-parse HEAD:tools/registry-replay.py`, 2026-10-21).  
**LSP:** No language server invoked; intra-file call graph is closed (all defs reached from `main`, `selftest`, or `run_replay`). Cross-repo consumers located via ripgrep only.

---

## Axes (godspeed)

| Axis | Intent |
|---|---|
| **Size** | Fewer lines/options with no caller loss |
| **Single authority** | No second replay publisher beside frozen r23 instrument |
| **Calibration** | K7–K11 + `registry-replay-selftest` behavior unchanged |
| **Evidence** | `--run` artifacts (`observations.json`, `bundle.json`, `live-dependent.json`) remain stable for round-24 receipts |

---

## Deletion candidates (safe → risky)

### 1. Remove unused `code` parameter from `publish` — **APPLY**

```116:118:tools/registry-replay.py
def publish(code, report, bundle, out):
    if bundle is None:
        return report
```

`code` is never read. Call sites at `run_replay` / `main` (`--project`) can pass `(report, bundle, out)` only. **Contract preserved:** exit codes come from `project()` / `main`, not `publish`.

### 2. Fix `--json` on `--project` — **DOC or 1-line behavior**

- Docstring advertises `--project … [--json]` (lines 22–23).
- `--project` branch **always** prints JSON (`283:283:tools/registry-replay.py`), ignoring `a.json`.
- `--json` only affects `--plan` (`271:271:tools/registry-replay.py`).

**Smallest correction:** Remove `[--json]` from the `--project` usage line in the module docstring and SKILL table footnote, **or** wrap line 283 with the same `a.json` ternary as `--plan` (would need a defined human format for reports — currently undefined). Selftest passes `--json` on `--project` but does not assert it; removing the flag from subprocess argv in selftest is optional cleanup.

### 3. Do **not** delete `live-dependent.json` write — **REJECT (YAGNI tradeoff)**

Only written in `publish` (`125:127:tools/registry-replay.py`). No reader under `tools/`. It **is** consumed as round-24 evidence (e.g. `.ufo/evidence/round-24/replay/live-dependent.json`, wave lanes comparing live rows). Deleting the file would duplicate report stdout parsing for reviewers without shrinking the tool meaningfully. **Alternative (later):** document that stdout report is canonical and treat the file as convenience — not a deletion in this wave.

### 4. Do **not** deduplicate `--run` into round-23 `replay.py` — **REJECT**

Frozen instrument (`.ufo/evidence/round-23/replay.py`) always publishes a bundle and lacks `project()`, stream limits, `live_dependent`, realpath `plan()`, and clone HEAD check. The ~50-line overlap (`encode`, env strip, frozen digest check, clone/symlink/run loop) is intentional successor code, not a second live path.

### 5. Do **not** extract shared `encode()` / env helper module — **REJECT**

Would add a new import surface for one consumer; r23 file must stay unchanged. Violates “minimize scope” for zero calibration gain.

---

## Duplicate logic vs round-23 instrument

| Block | r23 `replay.py` | `registry-replay.py` | Note |
|---|---|---|---|
| `encode()` | 21–22 | 53–54 | Byte-identical; keep local (r23 frozen) |
| GIT_-stripped env | inline 30–31 | `env()` 57–60 | Same policy |
| Frozen registry/requirements check | 34–41 | 137–146 | Same; `--run` takes caller paths instead of sibling JSON |
| Clone + symlink + `run_row` loop | 45–65 | 149–175 | r24 adds `plan()` siblings (realpath), HEAD verify, `external`, OBS schema, `runner_sha256_clone_copy` |
| Bundle assembly | inline, no gate | `project()` + conditional `publish()` | **Deliberate hardening (K7–K10)** |
| Observations schema | ad hoc dict | `registry-replay-observations-v1` | Required for `--project` |

**Second authority (fleet-level, not in-tool):** `.ufo/evidence/round-24/measure.py` `replay_rows()` (139–200) re-implements the same synthetic `obs()` fixtures and subprocess `--project` / `--plan` probes as `selftest()` (190–245). Shrinking that duplication belongs in measure.py or shared fixture JSON, not by deleting tool selftest (registry row `registry-replay-selftest` depends on it).

---

## Surfaces without selftest coverage

| Surface | Exercised by | Gap |
|---|---|---|
| `--run` full path | Actual replay receipt (`.ufo/evidence/round-24/replay/`), not selftest | Contract bounds: “actual replay run is separate evidence” |
| Default `--max-stream-bytes` (`1 << 20`) | Live replay stdout report | Selftest only uses explicit `8` / `16` |
| `--plan` without `--json` | None | Human `key: value` lines untested; low risk |
| `--project` invalid file JSON | None | Exit 2 + minimal JSON; no schema field |
| Multi-row observations | Live replay only | `project()` loop semantics not unit-tested with N>1 in selftest |
| Report fields `refused_rows`, `rows`, `max_stream_bytes` | Partially via finding_ids | Selftest does not assert `refused_rows` |
| `plan()` output `repo` key | `measure.py` K11 | Selftest `plan-realpath` checks `fleet_root` + `siblings` only, not `repo` |

None of these are dead code; they are **untested options or metadata**. Adding selftest rows for invalid-input and `repo` would improve calibration without deleting behavior.

---

## Dead / unreachable code

| Item | Evidence |
|---|---|
| Unused `publish(..., code, …)` parameter | Never referenced in function body |
| `--json` effect on `--project` | No branch reads `a.json` in `--project` path |

No unreachable functions: `plan`, `project`, `publish`, `env`, `encode`, `run_replay`, `selftest` all on the CLI path.

---

## Preserved contract (must not regress)

- **K7–K11:** `project()` findings `RUNNER_NOT_HELD`, `RUNNER_CLEANUP_FAILED`, `STREAM_LIMIT`; `live_dependent`; `--plan` realpath (`measure.py` + tool selftest).
- **Registry row:** `registry-replay-selftest` expects `REGISTRY_REPLAY_SELFTEST: 10/10 pass` (`tools/registry.json` 991–998).
- **Gate chain:** `--run` → `observations.json` + gated `bundle.json` / `expected.json` → `command-binding.py` (round-24 replay-gate receipt).
- **Exit map:** 0 publish / 1 refuse / 2 invalid / 64 usage (docstring + `Parser.error`).

---

## Fresh falsification (static)

**Target:** projection refuses when `held` is not strictly `true`, including `held: null` and cleanup errors; still lists `non_hermetic_argv` / `external` under `live_dependent` when otherwise clean.

**Method:** Read `project()` control flow (`80–113:tools/registry-replay.py`) and cross-check selftest case list (`199–206`) against `measure.py` K7–K10 paths.

**Result:** No counterexample found. `held is not True` covers `False` and `None`; cleanup checked before held; stream limit uses UTF-8 byte length with `surrogateescape`; refusal returns `bundle is None` so `publish` writes no bundle.

---

## Tool installs

None (read-only static review).
