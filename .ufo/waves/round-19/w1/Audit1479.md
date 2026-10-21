# Audit1479 — scoped retained-evidence review

Review date: 2026-10-21. Advisory only; no re-execution, production edits, installs, or tests/builds/linters/formatters.

## Axes

- Receipt integrity: current stdout/stderr bytes and any independent digest binding.
- Trace binding: whether the recorded argv explains the retained output.
- Revision/input provenance: what revision and inputs the trace actually records.
- Repair stability: whether the C1 repairs can affect this historical evidence.

## Findings, by severity

- **Low — trace/ledger range differs by one line (coverage convention unresolved).** The trace argv spec is `start: 1479, end: 1497` (trace `argv`, lines 33–34), and the retained stdout prints `SECTION 1479 1497`. The matching ledger entry records `start: 1479, end: 1498` (ledger lines 12259–12270). Thus the trace does not demonstrate the ledger's full stated range if `end` is inclusive. The assigned evidence does not specify whether ledger `end` is inclusive or exclusive, so this is a coverage discrepancy, not a confirmed omitted source line.
- **Verification gap — stdout is hashed locally but lacks an expected-digest anchor in the assigned trace/ledger.** I ran only `sha256sum <audit-1479.stdout> <audit-1479.stderr> && wc -c <audit-1479.stdout> <audit-1479.stderr>`: stdout is 4,624 bytes, SHA-256 `7e823eb18fc71fa52ec70e9458c17cf9ebe4d09e73efe9bf984d6b1cc9f4e817`; stderr is empty (0 bytes), SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Neither the trace nor the matching ledger entry records an expected stdout/stderr digest; the ledger input map also contains no match for the stdout digest. Therefore these hashes identify the bytes currently present, but cannot be compared against an independently recorded expected hash. No alteration is established.

## Established facts and limits

The retained trace (`.ufo/evidence/round-18/coldread/traces/L1/audit-1479.json`, especially `argv` lines 3–41 and `inputs` lines 52–73) records a `bwrap`-isolated `python3 -c` command, with exit 0. Its script reads `SKILL.md`, prints the requested section, hashes the `spec.paths`, and checks the listed assertions. The retained stdout's `SECTION`, `OPEN` digest/byte-count records, and final verification line are consistent with that argv/spec. The trace and ledger both identify revision `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`; the ledger entry also records `commands_executed_count: 1`, the same skill digest, and the same listed input digests. The trace says `tracked_filter: true`, with `untracked`, `external`, and `live_lane_reads` empty and `dropped_home_count: 0`.

This binds the recorded command to a bounded cold-read/probe, not to arbitrary commands or full command completeness. The revision established here is `a9c94c…`; it is not the round-19 frozen baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`. No execution timestamp or independent receipt-output digest is present in the assigned trace/ledger.

## C1 repair impact

The round-18 spot-check §5 lists five routed defects (lines 180–208). One named target, `.ufo/evidence/round-18/final/checks.json` for the mis-invoked selftest row, is explicitly among this trace's hashed inputs (`fed3c8e6…`, trace line 57 and stdout `OPEN` row). A C1 correction that changes that file would make the old logged digest describe the pre-correction bytes, not the new tree. That does **not** retroactively alter the retained stdout/trace as historical records; it does mean this run cannot establish the corrected file's contents. The other four §5 targets are not named in this trace's `spec.paths`.

Residual risk: because the output digest is not recorded alongside the trace/ledger, the retained stdout's historical immutability cannot be verified from this assigned pair alone. Preserve the old bytes as historical evidence and use separate evidence for post-repair state; do not treat this trace as a round-19 baseline run.