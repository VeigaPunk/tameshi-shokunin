# BundleAssembleSelftest — scoped falsification

Date: 2026-10-21. Read-only; no replay/selftest invoked. Axes: receipt integrity, source/revision/argv attribution, C1 fit.

## Strongest assertion and verdict

**Agree** (high confidence on retained bytes and C1 scope): `checks.json#assemble-selftest` is an effective historical assembler-selftest receipt, not the R18-4 failed Bash-witness invocation; it is outside C1’s five-item population. This does not independently close C1.

## Evidence and arithmetic

- `.ufo/evidence/round-18/final/checks.json:75-83` records argv `python3 .ufo/evidence/round-18/coldread/assemble.py --selftest`, revision `921ef8077440f90d092aab4b9fdc750a45de1224`, exit 0, stdout SHA-256 `bce10627…`.
- Read-only JSON/byte recomputation: output 8,340 bytes / 89 lines; 80 `[ok]`, zero `FAIL`, terminal `SELFTEST: 80/80 pass`; its digest matches the row. Stderr is 0 bytes, SHA-256 `e3b0c442…` (but the historical row has no stderr digest field).
- Frozen `55e1d312c4e8ac67aefad80099bd27581ff805c9` retains the same `checks.json` SHA-256 `fed3c8e6…` and stdout/stderr digests. `assemble.py` hashes to `bf7c12f7…` at both `921ef80` and `55e1d31`; worktree bytes match. `main()` defines `--selftest` (`assemble.py:1965-1968`), dispatches to `_selftest()` before requiring `--reports`/`--carry` (`1970-1975`), and `_selftest()` returns 0 only with no failures (`1920-1925`). Quote, opened 2026-10-21: “SELFTEST: 80/80 pass” (`assemble-selftest.stdout:89`).
- The eight cited observations reproduce as: checks row (1) + separate `registry*.stdout` receipts (3; each `registry*.stderr:34` says `expect=0 got=0`) + trace JSON observations (4). Seven bind tool exit; `CR48/7.json` only binds the wrapper’s `echo` exit. `CR50/25.json` is a CLI-surface inspection, and `CR45/07.json` invokes the round-16 tool, so both are excluded. The JSON-only scan described in the report does not itself include the three `.stdout` files.
- `contract.json:5-11` defines exactly five C1 targets (R18-1…R18-5); R18-4 is only `bash-witness-selftest`. `measure.py` at frozen revision `55e1d31` is byte-identical to the worktree; its five predicates (`evaluate`, lines 129-226) contain no `assemble-selftest` target. The scoped round-19 `*assemble*` artifact search returned no files.

## Concrete falsifier / correction missed

The report’s statement that round-19 `measure.py` reads `OLD_CHECKS` only for the Bash-witness supersession is **false**: `evaluate.guard()` reads `strict_json(data[OLD_CHECKS])['probes']` and checks that row (`measure.py:139-148`), in addition to the Bash-witness predicate (`183-199`). This corrects the report’s source description but does **not** reveal an assembler correction or bring this receipt into C1.

## Remaining unknowns

The assembler receipt does not bind the run’s cwd, runner, interpreter version, or tool digest at execution time; the tool-byte attribution is reconstructed from matching revision bytes. The missing historical `stderr_sha256` remains a QUALITY 39 receipt-format gap, already identified by the build report and outside C1. No LSP device was available; CLI findings above are direct source-text inspection.