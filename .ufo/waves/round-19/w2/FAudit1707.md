# FAudit1707 — scoped falsifier review (2026-10-21)

Read-only review of `w1/Audit1707.md`, its cited receipt/trace/ledger, and frozen C1 revision `55e1d312c4e8ac67aefad80099bd27581ff805c9`. No receipt argv was executed; no tool installed.

## Strongest assertion: M1 — old `audit-1707` output has no recorded digest

**Verdict: AGREE as a historical fact; it is not an unclosed C1 criterion.**

- Reproduced arithmetic from `.ufo/evidence/round-18/coldread/traces/L1/audit-1707.json`, its ledger entry at `ledger.json:12346-12387`, and `final/audit-1707.stdout`: trace has 14 input keys; ledger has 13, dropping only `SKILL.md`; the argv spec has 13 paths and stdout has 13 `OPEN` lines. Its 61 lines are `1 SECTION + 46 section + 13 OPEN + 1 terminal` (zero `TAIL`).
- Computed old stdout SHA-256: `cebcea16f3decbd839177eeebc3b35e52d746859c589913892baf4222bd7e059`. Neither old trace nor ledger entry has a stdout/stderr/output digest field. The `checks.json` input is indeed in the spec, but the captured script only reads and prints its hash; it contains no `checks.json` assertion. `checks.json` records `bash-witness-selftest` exit 64 with the empty-stream digest.
- Revision/argv attribution is consistent: trace `rev` and ledger `read_rev` are both `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`; its argv is the bwrap/env-isolated `python3 -c` invocation with the 1707–1752, 13-path spec. At revision 55, the old stdout, trace and ledger are unchanged (blob IDs respectively `23ccb8a…`, `1ec442e…`, `131510f…`).

## C1 comparison and concrete falsifier to a stale residual

- At revision 55, `measure.py` (`d13dc4f…`) uses `receipt()` to require matching stdout/stderr SHA-256 for its new R18-4 witness and R18-5 measurement receipts. Its frozen input list includes old `checks.json`, but not `audit-1707.stdout` or its trace. Therefore it does **not** retrofit or falsify M1 for the old receipt.
- **Concrete falsifier:** Audit1707’s residual “unknown” about whether the failed old witness row is superseded is resolved at revision 55. The same-revision `.ufo/evidence/round-19/bash-witness-selftest-complete.json` has exact argv `python3 tools/bash-witness-study.py selftest`, revision `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, exit 0, stdout/stderr digests, and `supersedes` exactly includes `.ufo/evidence/round-18/final/checks.json#bash-witness-selftest`; frozen `measure.py`’s R18-4 predicate checks that exact list and the old failed row. This supersedes it without rewriting historical `checks.json` or changing what the old trace proved.
- Thus agree with M1, but disagree that this old-output gap is a current C1 failure. The correction’s digest-bound refresh receipt is separate evidence; it does not authenticate the old `VERIFIED` line or ancestor-instrument claim.

## Residual risk / verification gaps

No producer authentication or independent reproduction of the original run is established. The old receipt’s output-digest gap remains for that historical artifact; it is outside the five frozen C1 corrections. No old argv, suites, tests, or selftests were run. Current `round-19.md:149-150` later states “Old traces need not authenticate stdout bytes; new refresh receipts separately persist output digests” (read 2026-10-21); that later wording is not part of frozen revision 55.