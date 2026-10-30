# T58W2Read13 — scoped cold re-read

Verdict: **verified-record**. No false statement or failing documented behavior found in the assigned section.

- Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534` (dispatch log and detached clone agree).
- Heading: `## Context gate classification and explicit exit classes — round 15`.
- Frozen round-18 sectionizer: lines **1652–1718**, SHA-256 `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6`.
- Axes: factual calibration, command operability, pointer integrity, bounded evidence.

## Findings by severity

None. Expected negative exits below are successful discriminating checks, not defects.

## Executed sweep

Full commands, stdout, stderr, and exits: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2Read13-receipts/commands.json`. Reproduction driver: the same receipts directory's `sweep.py`; entry command was `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read13/sweep.py`.

| Command family | Observed output |
|---|---|
| Frozen `measure.py` imported; `sectionize(git show C0:SKILL.md)` | `1652 1718 132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6` |
| `git -C CLONE diff BASE C0 -- SKILL.md tools/context-capture.py` | exit0, empty output |
| `python3 TOOL --check --json` | exit0, `context_consistent`, digest matches |
| `python3 TOOL --selftest` | exit0, `SELFTEST: PASS (49/49)` |
| Explicit retained missing-env receipt with pinned expected id/exit | exit1, `missing_injected_environment`; retained contradictory verdict also reported |
| Explicit duplicate-key / wrong-root-type / non-UTF-8 receipts | exit2, `receipt_json_invalid`; no traceback |
| Edited retained snapshot against original digest | exit2, `snapshot_tampered` |
| Missing receipt | exit2, `receipt_missing` |
| `python3 TOOL --check --unknown` | exit64, `usage_error`, empty stdout |
| Archived script and both retained receipts, `sha256sum` before/after | all three published digests match and remain unchanged |

`CLONE` and `TOOL` above abbreviate the absolute paths recorded verbatim in commands.json, not literal runnable shell variables.

Read the entire section, the historical source's cited ranges, round-15 Gate/Mistakes, routed defect 5, source rows S049/S051, adjacent archive and registry language, and canonical maintained dispatch. `tools/context-capture.py:1359–1405` binds the read bytes to the digest before parsing and `:2305–2338` dispatches check mode directly to replay without invoking the archived experiment. File reading in check mode is limited to explicitly chosen receipt/expected files and its own source digest; subprocess invocation belongs to the separate selftest. This supports the section's replay boundary rather than asserting that recorded argv ran anew.

Retained `verification-3.json` contains 44 checks, all passed, with `failed_checks: []`; this is inspected historical evidence, not a rerun of that harness. All assigned local pointers exist; fleet `../PROTOCOL.md` resolves in the original lane layout and Gate standard agrees with the explicit classes.

## Residual risk / verification gaps

No exhaustive proof of every possible malformed input, unreadable-file setup, concurrent mutation, or external authenticity is claimed. The old experiment was deliberately not executed because it writes the frozen receipt. LSP is unavailable (`xd://lsp`: `No such tool`); source/text inspection is the fallback, not semantic reference proof. Standalone scratch clone does not contain the external fleet PROTOCOL file; the original absolute fleet target was read instead. Resume and saturation claims are absent from this assigned section and were not inferred.

No lane source edited, no tool installed. Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2Read13` was removed; `test ! -e` exited0.

Self-evaluation: accuracy4 (finite sweep, no universal proof), completeness4 (external fleet pointer not C0-pinned), clarity4 (full output delegated to receipts), actionability5 (exact commands and retained driver), conciseness4 (matrix duplicates some JSON detail); average4.2. Highest-value improvement would be future fleet-document revision pinning, not a finding under this section's contract. INFERENCE: the user should agree with the explicitly bounded verdict.
