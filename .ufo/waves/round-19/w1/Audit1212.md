# Audit 1212 — retained receipt review

**Review date:** 2026-10-21. **Scope:** `round-18/final/audit-1212.stdout`, `.stderr`, its `coldread/traces/L1/audit-1212.json`, and the corresponding coldread ledger entry; no command re-execution.

## Findings, by severity

### Medium — Printed ancestry conclusion is not established by the recorded argv

The stdout's final line says `VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision` (`.ufo/evidence/round-18/final/audit-1212.stdout`, final line; source carries no execution timestamp). Trace argv records one `python3 -c` invocation, exit 0, at revision `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`. Its code reads the supplied current-revision paths and asserts selected receipt values (including `held == total == 31`, `open=0 closed=11`, case counts, JSON status fields, and `controls_match`). The recorded code contains no ancestor lookup or comparison, so it does not establish that ancestor runs have the same instrument blobs. Treat that suffix as unsupported; the listed literal/JSON assertions are the bounded facts this command establishes. It also hashes/prints `checks.json` but does not assert its selftest row.

## Receipt and trace facts

- `sha256sum` of the retained pair observed stdout SHA-256 `2816e2a573dfe482bc2064ea497cb619cf291a5fa4fa234b154c2dfc2031f4db` (3,551 bytes) and stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty). This is a computed hash of the present stdout; neither the trace nor ledger entry contains an independent stdout-digest field to compare against.
- The trace binds the command to the section request `start: 1212, end: 1228` and the 13 listed paths; its `inputs` map records hashes for those paths plus `SKILL.md`. The `OPEN` hashes printed in stdout agree with the trace's path/hash map, including `checks.json` = `fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d`. Trace `exit` is 0; `tracked_filter` is true; `untracked`, `external`, and `live_lane_reads` are empty; `dropped_home_count` is 0. These are recorded trace facts, not a claim of command completeness.
- The selected ledger entry has `commands_executed_count: 1`, `read_rev` equal to trace `rev` (`a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`), and points to this trace. Its `sha256` (`7f411a1a8b92f816a27296cf3863f5c52c4172b60725f464af2168403d366208`) is the section hash, not the stdout hash. The ledger records `start: 1212, end: 1229`, while trace argv/stdout mark end 1228; the scoped artifacts do not define whether these endpoints use different conventions, so the one-line boundary is unresolved rather than treated as proof of missing content. The ledger lists `SKILL.md` as dropped from its inputs.

## C1 repair impact

Round-18 verifier-spotcheck §5 identifies five repairs. Of their named files/targets, only `.ufo/evidence/round-18/final/checks.json` is in this trace's input map. If C1 corrects that file's bytes, its prior pinned digest (`fed3c8e6…`) will no longer identify the corrected file; a fresh comparison to current bytes would then fail. That does **not** retroactively invalidate this retained historical observation at the recorded revision, provided the old receipt pair, trace, and old input bytes remain preserved and the correction is appended as dated errata rather than silently substituted. The other four §5 repair targets are not in this trace's listed input paths. No scoped evidence gives the execution timestamp.
