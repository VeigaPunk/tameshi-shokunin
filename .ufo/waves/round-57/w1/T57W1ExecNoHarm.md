# T57W1ExecNoHarm — round-57 no-harm monitor re-base

Staged: `.ufo/waves/round-57/w1/T57W1ExecNoHarm/stage/.ufo/evidence/round-57/no-harm.sh` (`no-harm.sh LANE BASE REV`). No lane file edited. Tools installed: none.

## Result at BASE (5e35699, REV=BASE): 18 monitors, 18 ok, 0 RED. Total wall 1026 s
Receipt: `T57W1ExecNoHarm-receipts/no-harm-at-base.out` (per-line `[+Ns]` timestamps).

| monitor | BASE value | state |
|---|---|---|
| commandD | recorded_cases=10 depth_score=10 | ok |
| coldread-floor | score=8 credited=64 | ok (~49-72 s, the only slow one besides registry-check) |
| r45-freshness | population=74 fresh=71 score=9 | ok |
| r45-coverage | rows=2 entries=2 C2_R45_PASS=true | ok |
| S160-count | 1 | ok |
| registry-rows-not-below-140 | 142 | ok |
| r46-coverage | rows=3 entries=3 C3_R46_PASS=true | ok |
| r47-coverage | rows=3 entries=3 C3_R47_PASS=true | ok |
| tools-scope | [] (no tools diff) | ok |
| registry-rows-not-shrunk | base=57 rev=57 | ok |
| r49-generator-capability | PBT_STAGED_ID: cases=400 violations=0 ... | ok |
| r50-shrinker-selftest | SHRINK_SELFTEST: cases=14 failed=0 | ok |
| r53-scratch-hygiene | tmp_hits=0 | ok |
| ledger-not-shrunk | base=609 rev=609 | ok |
| sources-not-shrunk | base=142 rev=142 | ok |
| **r56-gate-selftest** (new) | GATE_SELFTEST: 19/19 pass | ok |
| **registry-check-full** (new) | REGISTRY_CHECK: held=48/50 superseded=7 | ok |
| **old49-ledger** (new) | base_rows=49 rev_rows=49 | ok |

## Wave timing for the L1
- Everything except registry-check-full: ~74 s.
- registry-check-full: BASE standalone 622 s (exit 1), 952 s inside the full run — host-load dependent (57 rows, summed timeouts 7800 s; two 900 s-timeout rows). Plan 10-16 min per scoring of this monitor; it grows when the 3 new gate rows are added (small).
- BASE registry-check facts (receipts `registry-check-at-base.stdout/.time`): held=48/50, superseded=7, exit 1. The 2 `differs` rows are `sources-census` (got 1) and `verify-round15` (got 1) — they fail in the clone layout at BASE already, so BASE held is 48, not 50. First attempt with a 900 s tool deadline timed out (not a result).
- Decision: BASE's count is a constant `BASE_HELD=48` in the script (overridable via env) rather than re-measured every run (would add 10-16 min). Header says so. If the L1 wants live BASE measurement, run registry-check at BASE once and pass `BASE_HELD`.

## Re-base declarations
- Args now `LANE BASE REV` (BASE no longer hardcoded). Scratch dir `tameshi-r57/no-harm`, removed on exit, TMPDIR exported.
- tools-scope: admits `M:tools/registry.json` and `M:tools/receipt-revision-gate.py` only (the C2 targets). The round-56 `A:` and the other `M:` allowances are dropped (base content now; round-57 touches no other tool). If the L1 adds/changes another tool, tools-scope goes RED by design — widen it deliberately.
- Everything reads `git show REV:...`; tools (gate, registry-check, pbt, guard, shrinker) are extracted to `$SCR` and run there. Exception inherited from earlier rounds: coverage/freshness/coldread measure.py files run from the lane worktree (instruments, frozen) and registry-check takes `--root LANE --rev REV` (clones the git object at REV).
- old49-ledger: loads `defects` at BASE and REV via `git show`; ok iff REV list begins with BASE's list element-for-element (parsed JSON equality) and is not shorter; an appended 50th+ row is fine, edit/reorder/delete of an old row is RED.

## Negative controls (`negative-controls.txt`, fixture clone, shell-verified toplevel)
- old49-ledger: appended row ok; mutated note in row 4 RED.
- r56-gate-selftest: renaming a real code occurrence in the gate gives `18/19 pass` RED. (A docstring-only edit correctly stays ok.)
- Other 15 monitors carried verbatim from round 56 (their R56 behaviour unchanged); not re-mutated here.

## Risks
- coldread-floor stays 64/64 at BASE; any byte change to SOURCES/QUALITY/README/knowledge/pinned tool will make it RED until the wave-3 re-key (as the contract says).
- The scoring-time wall of registry-check-full may exceed a 900 s tool deadline: run async/with timeout 0.
