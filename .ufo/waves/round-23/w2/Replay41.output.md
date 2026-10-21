## `wave-accounting-frozen-entry` — Replay41

Report: [`.ufo/waves/round-23/w2/Replay41.md`](file:///home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-23/w2/Replay41.md)

**Axes:** frozen argv/expect · retained metadata/full stdout · substring binding · wave-accounting semantics · producer auth (out of scope)

**Static binding — confirmed:** `argv` and `expect` match across `tools/registry.json`, `registry-baseline.json`, `requirements.json`, and the replay bundle requirement. The replay receipt matches argv, exit 0, cwd, and revision `496d212…`.

**Evidence — present (not inferred):** Full stdout (752 B) in `replay/bundle.json` and `replay/observations.json` (including `measurement_interval`); `stdout_tail` equals full stdout for this row. `replay-gate-A.json` shows command-binding clean on the full replay bundle (`3d6c99b70b3e…`). Output `bundle_sha256` matches on-disk round-22 bundle/expected.

**Field-level false acceptance:** Registry `stdout_contains` and `command-binding.py` only require four substrings in receipt stdout. Offline mutate: set `waves[1].completed` 38→39 while keeping `total.completed` 66 — all tokens still match; one-row `evaluate()` returns `(0, [])`. A minimal stub JSON with only `total` + `"finding_ids": []` also passes. C1 binds declared receipt shape, not faithful `wave-accounting.py` output.

**Adversarial delta:** Inconsistent per-wave `completed` (or minimal fake stdout) vs real tool → binding/registry still pass; real tool would emit `TOTAL_MISMATCH` / exit 1.

**Rejected:** Producer authentication and historical retrofill (explicit in tool authority / binding design).

**Tooling:** No installs.
