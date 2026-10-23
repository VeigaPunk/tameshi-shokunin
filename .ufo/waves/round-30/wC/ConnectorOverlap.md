# ConnectorOverlap — round 30 wave C

Verdict: No live sibling lane duplicates tameshi's tally defect or its coldread seat-work binding. The only sibling surface that reproduces the tally *shape* is mado-shokunin's frozen R13/R14 harness copies (frozen evidence, not a live tool); the only sibling references to the tally line are quotations. No sibling implements `bind-select`-style credited-read binding. Tameshi retains sole ownership of both surfaces; no cross-lane reuse is safe or needed.

## Axes affected
- Operability (C1 tally surface) and credited-read integrity (coldread binding): no adjacent sibling currently shares either, so no cross-lane calibration gain or conflict is available from this scan.

## Scan method
Read-only: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <sibling> grep` on each sibling HEAD (20 lanes, excluding tameshi). Patterns: `REGRESSION: PASS`/`REGRESSION: FAIL`/`REGRESSION: SETUP`, `nlegs=`, `legs exact`, `case-tally`/`tally mismatch`/`counted=`, and `COLDREAD`/`bind-select`/`trace-inputs.py`/`report-block-unbound`/`transcript-without-assistant-coldread`/`seat-not-registry-member`/`read_rev` in coldread context. No sibling production file was executed or modified.

## (1) Case/leg tally or summary line that could pass with an uncounted leg

| Sibling | path:line | Overlap | Tameshi duplicates? | Conflicts with / could serve |
|---|---|---|---|---|
| mado-shokunin | `.ufo/waves/round-13/frozen/harness.sh:1143` (`local nlegs=6 npass=0 …`), `:1164` (`REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)`) | Frozen copy of tameshi's runner tally; same pre-fix shape (loop sums `st` operands against declared `nlegs`, no completeness guard) | No — mado's frozen harness is a derived copy; tameshi bb681566 is the current origin and now carries the guard | Frozen evidence only; must not be cited as a live tally or used to calibrate C1. Does not conflict, but cannot serve. |
| mado-shokunin | `.ufo/waves/round-14/frozen/harness.sh:1143,1164` | Same as above, R14 vintage | Same | Same; frozen evidence. |
| tsukuroi-shokunin | `LOG.md:186`; `corpus/knowledge/closeout-r11.md:355` | Quotation of tameshi's `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)` | No implementation; citation only | Documentation reference; no conflict. |
| (all other 17 lanes) | none | No `nlegs=` tally, no `legs exact` summary line, no case-tally mismatch guard | n/a | n/a |

No production sibling tool implements the tally; the only copies are frozen mado evidence.

## (2) Seat-work binding for credited reads or reviews

| Sibling | path:line | Overlap | Tameshi duplicates? | Conflicts with / could serve |
|---|---|---|---|---|
| (all 20 lanes) | none | No `bind-select`, `assistant_has`, `transcript-without-assistant-coldread`, `report-block-unbound`, `seat-not-registry-member`, or `trace-inputs.py` binding exists in sibling production or frozen tooling | n/a (tameshi sole owner) | n/a |

Sibling references to `COLDREAD` appear only inside prior connector reports and census artefacts, never as an implementation. The coldread binding contract (`bind-select-v3.py`) is tameshi-specific.

## Proposed move
None. Do not import sibling code or citations into the tally or binding surface. Keep tameshi as sole owner. If a future seat needs a cross-lane tally comparison, treat mado's frozen harness as historical evidence only (pin its bytes and revision) and re-derive rather than reuse.

## Risks
- Citing mado's frozen harness as a live tally would launder a pre-guard copy into current claims.
- Assuming siblings share the coldread binding would overstate credited-read coverage.

## Verification
- `git -C <sibling> grep` run on all 20 sibling HEADs (mado HEAD 2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f; tsukuroi HEAD 5a967ce26f60161e32304d4ec77420d2218b8fcb). No Git writes performed.
- No tests, selftests, or sweeps were run in any lane.
Report: .ufo/waves/round-30/wC/ConnectorOverlap.md
Lane bounds: leaf member — no subagent dispatch.
Judged on: adjacency
Model: openai-codex/gpt-6.1-sol
Installs: none
Scope: read=current round declaration and before receipts, twenty sibling canonical/corpus scopes and discovered Python tooling, relevant local skills; wrote=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-30/wC/ConnectorOverlap.md; executed=read, glob and grep inspections; no lane tool executions
Model: openai-codex/gpt-6.1-sol
Installs: none
