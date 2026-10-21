# FAudit1905 — Audit1905 falsification (2026-10-21)

## Verdict

**AGREE with Audit1905's strongest material finding, L1:** the `VERIFIED` sentence claims evidence the receipt argv does not compute. This remains an advisory finding, not a round-admission decision.

## Evidence and falsifier

- Audit1905 quotes `audit-1905.stdout:49` (2026-10-20): “VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision”. Its source is trace `.ufo/evidence/round-18/coldread/traces/L1/audit-1905.json`, `rev=a9c94c5…`, `exit=0`.
- The trace's exact Python `-c` argv (line 33) reads the specified current `SKILL.md` section and paths, checks selected output substrings/JSON statuses, then prints that fixed sentence. It does not read an ancestor revision or compare ancestor instrument blobs; `checks.json` is only opened/hashed, not parsed. Its assertions establish selected text facts, not that the archived receipts came from actual executions.
- **Concrete falsifier:** change only an ancestor's `tools/mutate-and-run.sh`, keeping the read-revision blob and the argv's other inputs fixed. The argv has no ancestor input or history operation, so the same final sentence still prints while its “same instrument blobs” clause can be false.

## C1 corrections and stale-input check

- The old trace/ledger record input hashes for the two repair-target files: CASE `dd405bd3…`, `checks.json` `fed3c8e6…`. At delivered `55e1d312…`, plain blob hashes are CASE `d961a0d6…`, `checks.json` still `fed3c8e6…`: **1/2** old target inputs changed. The old `entries[156]`/receipt is therefore stale for the amended CASE; Audit1905's historical hash observation is correct.
- The mid-flight report's CASE hash `a69d9a86…` is no longer the delivered value. The 55e1 ledger has a new `start=1905` source entry (`read_rev=7af123b…`) keyed to CASE `d961a0d6…`; its section SHA remains `1c5c0872…`. The matching `source-1905.json` trace records `rev=7af123b…`, `exit=0`, and that same input hash; 7af123b is an ancestor of 55e1. `refresh-specs.json` labels this **L1-author input-keyed source re-anchoring**, expressly not blind/independent cold-read or required-command coverage. Thus the old entry is still historical/stale, but its missing-current-input concern is superseded by a separate, narrower refresh.
- Defect 4 did not rewrite `checks.json`: its `fed3c8e6…` hash and old `bash-witness-selftest` exit 64 are retained. The separate `bash-witness-selftest-complete.json` records argv `python3 tools/bash-witness-study.py selftest`, revision `4b7c682…`, exit 0, stream digests and an exact `supersedes` list. Frozen `measure.py`'s R18-4 predicate checks that replacement while requiring the old failed row remain; this is an append-only correction, not proof of producer authenticity.
- The 60/60 replay receipt's actual argv/revision are `--rev 4b7c682…` (`round18-final-measure.json`); round-18 lesson lines 148–155 explicitly disclaim a 60/60 claim at any round-19 revision. Frozen ruler blob SHA-256 is `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`; it reads revision-pinned blobs and never executes recorded receipt argv. Do not attribute that historical 60/60 to 55e1.

## Residual risk / verification gap

- L1's overclaim remains in the historical receipt; the C1 R18-2/R18-4/R18-5 corrections do not amend it. The refresh does not create a blind cold-read or command-coverage claim.
- I found no same-ruler `measure.py --rev 55e1…` before/after result in the reviewed evidence. Prior `before.json`/`after-21e7932.json` are not a final 55e1 result; **no final 5/5 at 55e1 is asserted here**. No receipt argv, suite, test, build or selftest was run.