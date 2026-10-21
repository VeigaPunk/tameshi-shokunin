**Verdict:** Row `context-capture-selftest` is green on its declared fields and the frozen row is an exact copy of the baseline registry row — but the acceptance is a 15-byte substring plus a producer-declared exit, and the gate never sees the frozen contract. Evidence is *present*; execution is *inferred*; fresh-vs-retrofilled is *undecidable* from the receipt.

## Evidence (read-only, verified)

- Frozen row: `.ufo/evidence/round-23/requirements.json` → `{"name":"context-capture-selftest","argv":["python3","tools/context-capture.py","--selftest"],"expect":{"exit":0,"stdout_contains":["SELFTEST: PASS"]}}`.
- Baseline registry row (`registry-baseline.json:418-433`) is field-identical (same argv/expect; `kind=selftest`, `timeout_s=60`, `source=SKILL.md@98bea7d:1680`). The live `tools/registry.json` row is also field-identical. No drift.
- Frozen projection is exact: reconstructing `{name,argv,expect}` from the 43 active baseline rows equals `requirements.json`'s 43 rows; `sha256(registry-baseline.json)=ebd2e69a…` equals `requirements.registry_sha256`. Verified by hashing, not by trusting the label.
- Receipt (`bundle.json:226-235`): exit 0, stderr `""`, stdout 5201 bytes, 49 `SELFTEST_CASE` lines, exactly one `SELFTEST: PASS`, final line `SELFTEST: PASS (49/49)`. Observations row is byte-identical (`observations.json`, row interval 14:42:29.709848–14:42:31.059665Z, `elapsed_s=1.35`, Δ=1.3498 s). `stdout_tail` is a true 4096-byte suffix of the same full stream; `stdout` ≠ tail, so "full output, not tails" is literally true here.
- `sha256(bundle.json)=3d6c99b7…` equals `replay/expected.json`; `replay-gate-A.json` exit 0, `finding_ids: []`.
- Tool source: `tools/context-capture.py:1770-1786` prints PASS only when `failed` is empty; 49 cases match the observed 49 lines. Honest implementation.

## Field-level false acceptance

`tools/command-binding.py:65-113` takes its required set from `bundle['requirements']`, never from the frozen contract or registry. The strict top-level key set at line 68 (`{schema,revision,cwd,requirements,receipts}`) forbids even carrying a contract/registry digest. `MEMBERSHIP_MISMATCH` (line 99) is `set(receipts) != set(requirements)` — both sides producer-supplied. Deleting the `context-capture-selftest` requirement **and** its receipt (42/42) returns `(0, [])`; `duplicate
