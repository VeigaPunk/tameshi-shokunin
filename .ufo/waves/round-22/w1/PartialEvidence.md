# PartialEvidence — failed seats with retained reports

## Axes and boundary

Axes: **calibration** (completion follows the exact original callback identity/status), **auditability** (retain contradictory historical inputs), and **scope preservation** (no production edits or new admission credit).

Read-first authority: `.ufo/evidence/round-22/contract.json:1-21`, frozen base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`. This is an advisory trace, not a new admission judgment. Round 21 remains admitted; its two claims are not re-evaluated here. Retained callbacks are declared inputs, not authenticated provider telemetry.

## Exact identity trace

All paths below are relative to this repository.

| Seat | Registry binding and original scope | Superseded accounting | Corrected and final accounting | Retained terminal callback |
|---|---|---|---|---|
| `ProfileBashTsukuroiCensus` | `.ufo/waves/round-21/w2/swarm-registry.json:497-505`: `agentId=TameshiR21.ProfileBashTsukuroiCensus`, role `reviewer`, axes `coverage,freshness`. `.ufo/waves/round-21/spec2.json:444-451`: independently falsify the pinned F5 bash-tsukuroi-census observation using seven fresh profiles, not producer helpers. | `.ufo/waves/round-21/original-outcomes2.json:489-498`: same exact ID, `status=completed`, `actual_result=null`, retained report path, `replaced=false`. | `.ufo/waves/round-21/original-outcomes2-corrected.json:490-501` and `.ufo/waves/round-21/original-outcomes-final.json:1122-1133`: same ID, `status=failed`, `actual_result=null`, report path preserved, `replaced=false`. | `.ufo/waves/round-21/wait2-recovered-11.json:199-228`: exact ID and agentUrlId, structured `status=failed`; embedded reviewer task-result `status="failed (exit 1)"`, duration `13m26s`. |
| `V01WitnessTests` | `.ufo/waves/round-21/w2/swarm-registry.json:656-664`: `agentId=TameshiR21.V01WitnessTests`, role `reviewer`, axes `operability,calibration`. `.ufo/waves/round-21/spec2.json:586-593`: read-only review of bash-witness-study.py selftest delta at `790abd2129f153c13b471e381d454186edbde65e` versus `33d03b7`, with item-specific scratch controls. | `.ufo/waves/round-21/original-outcomes2.json:661-670`: same exact ID, `status=completed`, `actual_result=null`, retained report path, `replaced=false`. | `.ufo/waves/round-21/original-outcomes2-corrected.json:664-675` and `.ufo/waves/round-21/original-outcomes-final.json:1296-1307`: same ID, `status=failed`, `actual_result=null`, report path preserved, `replaced=false`. | `.ufo/waves/round-21/wait2-recovered-07.json:416-445`: exact ID and agentUrlId, structured `status=failed`; embedded reviewer task-result `status="failed (exit 1)"`, duration `11m28s`. |

Both terminal callback records report `resolvedModel=zai/glm-5.3-flash:max`, `resolvedModelIdentity=zai/glm-5.3-flash`, thinking level `max`. Both errorText fields state: `[zai/glm-5.3-flash] Retry budget exhausted after 5 retries: 429 Rate limit reached for requests`, followed by `Rate limit reached for requests (type=1302)`. These are provider/runtime failures, not conclusions about the substantive correctness of the report contents. The snapshots say recovery was not auto-delivery. The heading `Completed (1)` in their text is a terminal-job grouping: its individual entry explicitly says `failed`; it does not supply a `completed` status.

## Exact false-positive mechanism

The superseded aggregate treated **report-file presence as evidence of successful job completion**, overriding failed original seats. This is not inferred solely from two null results: `.ufo/waves/round-21/original-outcomes2-corrected.json:5` explicitly names what it supersedes as `original-outcomes2.json file-presence inference`, and line 6 states the corrective rule.

The two retained reports are particularly tempting false-positive inputs:

- `.ufo/waves/round-21/w2/ProfileBashTsukuroiCensus.md:1` says `done`; lines 6-11 claim completed profile reproduction and a scoped recommendation; lines 19-28 describe successful target executions and producer agreement.
- `.ufo/waves/round-21/w2/V01WitnessTests.md:3` says `Verdict: done — review complete` and reports defects and confirmed kills; lines 11-19 describe selftest/mutant results.

Those are retained document assertions about domain work, not terminal callback success. A target selftest exit 0, a report's `done` string, and a provider task's terminal status are separate facts. Neither report existence nor its confident prose can change these callbacks from `failed` to `completed`. This audit did not rerun or authenticate those reports' experiments.

The superseded file declares wave 2 as **75 seats / 40 completed / 35 dead** (`original-outcomes2.json:1-5`). The corrected file declares **75 / 38 / 37** (`original-outcomes2-corrected.json:1-6`). The two named seats each move completed → failed without replacement; their two-seat delta accounts for the declared completed decrease and dead increase. These are read declarations and direct arithmetic, not a newly executed whole-population count check.

## Preserved correction and bounded contradiction

Preserve the existing correction verbatim in meaning: **“Original task callback status wins; partial report creation never rehabilitates a dead seat.”** Both reports and both original identities remain in place, with `replaced=false`.

`.ufo/waves/round-21/original-outcomes-final.json:635-638` preserves wave 2 as **75 / 38 / 37**; lines 1364-1369 declare overall **146 seats / 66 completed / 80 dead** and `partial_report_files_do_not_rehabilitate_failed_jobs=true`. The final rows preserve `failed`, not report-file success.

One adjacent metadata contradiction must not be mistaken for callback identity: both corrected/final rows carry `provider="codex"`, while their `resolved_model` and retained callback model/error identify `zai/glm-5.3-flash`. Their `last_error` is empty and `actual_result` null even though the recovered callback snapshots contain explicit terminal errors. Therefore those aggregate fields are not a lossless substitute for the callbacks. No provider-count recalculation or round-21 admission challenge is made here. Narrow recommendation: bind these seats using exact registry agentId plus the retained structured terminal status, and retain the original callback source/digest rather than reconstructing success from report contents or provider labels.

## Deletion candidate, preserved contract, and tradeoff

No files or code were deleted. The removable decision authority is the **report-presence → completed inference**, not the historical reports or the superseded accounting file. Keep the history as the calibration counterexample; remove only its authority to classify a failed seat as completed. There is no source-symbol deletion proposed, so no semantic-reference absence claim or LSP proof is asserted.

Preserved contract: original-seat identity, exact terminal status, total seats, no replacements, retained historical evidence, and the explicit limit that persisted callbacks cannot authenticate provider provenance. The tradeoff is deliberate: substantive partial work remains available as advisory material but earns no completed-seat credit. Deleting that retained material or treating its domain claims as newly disproved would harm auditability or exceed this lane's boundary; that is the stopping point.

## Actions and verification limits

Read-only inspection used `read`, `glob`, and literal `grep`; only this new assigned report was written. No production file, existing evidence, git/jj/index/ref, sibling tree, or host configuration was modified. No subagents, other runtime, build, lint, formatter, tests, installation, or data-count command were invoked. No shared-tree byte-identity check was executed; non-report immutability here is the operation boundary, not a claimed measured full-tree comparison. No new gate outcome, authenticated callback provenance, numeric expertise, or independent review credit is claimed.
