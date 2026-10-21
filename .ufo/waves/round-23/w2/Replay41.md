# Replay41 — `wave-accounting-frozen-entry` falsification (round-23 W2)

**Seat:** TameshiR23.Replay41  
**Revision audited:** replay at `496d212bc46789cdf8cafab72978bdb7f4182963` (artifacts on disk; not re-executed).

## Axes

| Axis | Result |
|------|--------|
| Frozen argv/expect vs baseline source | **Exact match** |
| Retained invocation metadata + full stdout | **Present in artifacts** |
| Registry/replay `held` / command-binding token binding | **Field-level false acceptance** |
| Wave-accounting semantic integrity via C1 layer | **Not established** |
| Producer authentication / historical retrofill | **Rejected (by design)** |

## Static exact binding (confirmed)

Sources agree byte-for-byte on argv and `expect`:

- `tools/registry.json` row `wave-accounting-frozen-entry`
- `.ufo/evidence/round-23/registry-baseline.json` (same row)
- `.ufo/evidence/round-23/requirements.json` requirement entry
- Replay requirement embedded in `.ufo/evidence/round-23/replay/bundle.json` `requirements[]`

Frozen argv:

```json
["python3", "tools/wave-accounting.py", "--bundle", ".ufo/evidence/round-22/bundle.json", "--expected", ".ufo/evidence/round-22/expected.json", "--json"]
```

Frozen expect:

```json
{"exit": 0, "stdout_contains": ["\"completed\": 66", "\"dead\": 80", "\"seats\": 146", "\"finding_ids\": []"]}
```

Replay receipt for this name matches argv, `exit: 0`, `cwd` `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`, and revision `496d212…`.

## Evidence present (not inferred)

| Artifact | What is retained |
|----------|------------------|
| `replay/bundle.json` `receipts[]` | Full stdout (752 B JSON), stderr `""`, argv, cwd, revision, exit |
| `replay/observations.json` `rows[]` | Same full stdout as receipt; `measurement_interval`; `runner_result.held: true`; argv/cwd/revision |
| `replay-gate-A.json` | `command-binding.py` over `replay/bundle.json` + `replay/expected.json` → exit 0, `finding_ids: []`, digest `3d6c99b70b3e…` |

For this row, `stdout_tail` equals full `stdout` (output fits tail budget). Audit used complete `stdout` fields, not tails.

Actual tool output (present in receipt) includes wave-level detail, e.g. wave2 `"failed_with_report": ["ProfileBashTsukuroiCensus", "V01WitnessTests"]` with `"finding_ids": []` — consistent with `wave-accounting.py` semantics (failed + report ≠ completed).

Reported `bundle_sha256` `dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e` matches on-disk `.ufo/evidence/round-22/bundle.json` and `expected.json`.

## Field-level false acceptance

**Layer:** registry `stdout_contains` and `tools/command-binding.py` `STDOUT_MISMATCH` (substring-only on receipt stdout).

**Failure mode:** Per-wave counts and cross-field JSON consistency are not bound. Only four substrings must appear anywhere in stdout.

**Demonstration (offline mutate of retained receipt stdout, no registry re-run):**

1. Parse actual receipt JSON from `replay/bundle.json`.
2. Set `waves[1].completed` from `38` → `39` while leaving `total.completed` at `66`.
3. All four required tokens still match (`"completed": 66` lives only under `total`).
4. `command-binding.evaluate()` on an isolated one-row mini-bundle returns `(0, [])` — same as clean row.

A **minimal** fabricated stdout containing only a stub `total` block plus `"finding_ids": []` also passes command-binding for this row.

**Implication:** C1 replay binding for this command proves **exact argv + cwd + revision + exit + substring tokens** on the **declared receipt**, not that stdout is a faithful emission of `wave-accounting.py` on the pinned round-22 bundle. The retained receipt in round-23 replay is internally consistent; the **gate contract** would still accept an inconsistent or minimal stdout with the same tokens.

This aligns with `command-binding.py` docstring: validates retained declarations, not producer authenticity.

## Concrete adversarial delta

| Field | Legitimate receipt (artifact) | Adversarial delta |
|-------|------------------------------|-------------------|
| `waves[1].completed` | `38` | `39` (sum with wave1 no longer equals `total.completed`) |
| `total.completed` | `66` | unchanged |
| Registry / command-binding | would pass | still pass (tokens unchanged) |
| Real `wave-accounting.py` | exit 0, `finding_ids: []` | would exit 1, `TOTAL_MISMATCH` on wave2 |

Swap of `--bundle` / `--expected` argv paths (registry row A10) is a separate argv-level attack; wave-accounting would fail digest or evaluation before substring checks matter.

## Producer authentication / retrofill

- Output `authority` explicitly disclaims provider authentication.
- No acceptance of producer-checked-live or historical metadata retrofill in this row’s binding path.
- Source-read bundles (`source-read-gate-A.json`) correctly reject argv-only credit via `ARGV_MISMATCH`; that is orthogonal to this replay receipt.

## Tooling

No installs or upgrades.

## Calibration summary

- **Argv/expect frozen binding:** confirmed across baseline sources and replay artifacts.
- **Execution evidence:** full stdout and invocation metadata are **actually present** in `replay/bundle.json` and `replay/observations.json`.
- **Calibration gap:** one **field-level false acceptance** at the substring binding layer (per-wave inconsistency and minimal fake stdout); adversarial delta above.
