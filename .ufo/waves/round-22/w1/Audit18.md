# Audit18 — round-21 wave1 RV08/RV09/RV10 callback vs registry vs report

**Verdict:** all three frozen identities agree across the outcome row, the wave1 registry, the spec, the dispatch record, the parent's terminal callback, and the retained report. No contradiction on identity, role, or status. Each "completed" is backed by a parent `async-result` callback with `status="completed"`, not just by a report existing. All three are positive controls: a report exists, the callback completed, and mid-run provider errors were recovered. A gate MUST NOT demote them.

Scoped population: exactly 3 rows, `wave1.rows[]` where name ∈ {RV08SourcesContract, RV09BatteryBaseline, RV10DepthBaseline}. No other rows were opened beyond computing the totals.

## Per-identity agreement

| name | outcome row (`original-outcomes-final.json`) | registry `w1/swarm-registry.json` `.members[name]` | parent callback (`async-result`, TameshiR21.jsonl) | seat terminal turn | report | agreement |
|---|---|---|---|---|---|---|
| RV08SourcesContract | id `TameshiR21.RV08SourcesContract-3`, role reviewer, status completed, report `.ufo/waves/round-21/w1/RV08SourcesContract.md` (lines 430-435) | agentId `TameshiR21.RV08SourcesContract-3`, kind spawn, role reviewer, axes [coverage] (lines 466-474) | 2026-10-21T12:12:29.819Z, jobId equal, `status=completed`, durationMs 682031; exactly 1 callback | last assistant `stopReason=stop` 12:12:26.426Z (openai-codex/gpt-6-luna, after zai 429 failover at 12:10:03); session_exit normal | exists, mtime 12:12:18.674Z (before callback), opens with `done —`, claims validator exit 0 + six W04 warnings | **agree** |
| RV09BatteryBaseline | id `TameshiR21.RV09BatteryBaseline-3`, reviewer, completed, report `.../RV09BatteryBaseline.md` (437-442) | agentId equal, spawn, reviewer, axes [operability] (475-483) | 12:11:47.633Z, `status=completed`, durationMs 641537; exactly 1 callback | last assistant `stop` 12:11:45.927Z (openai-codex; earlier zai 429s and one codex `unsupported_native_inflight_message` error, recovered after the parent IRC at 12:06:43); exit normal | exists, mtime 12:11:16.785Z (before callback), `done`, 36/36 active held, exit 0 | **agree** |
| RV10DepthBaseline | id `TameshiR21.RV10DepthBaseline-3`, reviewer, completed, report `.../RV10DepthBaseline.md` (444-449) | agentId equal, spawn, reviewer, axes [depth] (484-492) | 12:15:43.765Z, `status=completed`, durationMs 867847; exactly 1 callback | last assistant `stop` 12:15:32.242Z (zai/glm-5.3-flash, after 5 zai 429 errors); exit normal | exists, mtime 12:15:20.022Z (before callback), `Verdict: done`, D=8, REGRESSION PASS 8/8 | **agree** |

The same identity also appears in these files:
- `assignments1.json`: name → `-3` id for all three.
- `record1.json`: same agentId and role.
- `spec1.json` `items[47..49]`: name, role reviewer, axes equal. There is no agentId; that is expected before dispatch.
- `run1.json`: agentId `null`, from before dispatch.
- `dispatch-attempt-03.json`: index 47-49, ids `-3`, agent reviewer, with the `Report:` trailer pointing at the exact report paths above.
- The earlier `-2` attempts and the attempt without a suffix were refused with "Background job limit reached (100)" (`dispatch-attempt-02.json`, `dispatch-refusal-01.json`). They never ran, so the `-3` id is the original surviving spawn, not a replacement.

The callback output text matches each seat's session final-output file. Session `.md` sha256 values:
- RV08: `16c0430c…`
- RV09: `b75c383f…`
- RV10: `a32a8089…`

## Report-claim spot checks (hashes only, no checks rerun)

- RV09 claims `battery-baseline.json` sha256 `5b2cc16f…`. The committed file hashes to `5b2cc16f922f546ffd548dbfd26b4e7139fb47b209a45a7cf00e3fdf6a897bf4`, which matches. The scratch `battery.stdout.json` has the same hash, and `battery.exit` = `0`.
- RV10 hashes match its claims:
  - `command-D.txt`: `dde8df2e…`
  - `regression.out`: `4fbaf0e1…`, 46 lines
  - `regression.err`: empty (`e3b0c442…`)
  - `regression-attempt1-setup.out`: `a6d1f1dc…`
  - The scratch clone HEAD is `33d03b716d3edcf1d8656d46d6df61801d232c52`.
- RV08: its validator exit 0 claim was not rerun (out of scope). The claim is consistent with the callback summary.
- One cosmetic inconsistency in RV10: under Evidence paths, the `regression-attempt1-setup.*` files are labeled "attempt-3 SETUP refusal". In the table they are row 3, and the text calls them attempt 1. Only the label is wrong; status and results are unaffected.

## Partial report vs completed callback

For these identities the two cannot be confused. Each report is final: it says done, it was last written before the callback, and it was not modified after the callback. Each callback is terminal-completed. The calibration hazard runs the other way. All three transcripts contain provider error turns: zai 429 (`type=1302`) in all three, and a codex in-flight error in RV09. RV08 and RV09 switched credential to openai-codex mid-run. A gate that classes a seat as provider-dead because its transcript contains a provider error would falsely kill all three. "Dead" must be keyed to the terminal callback status only.

## Contradictions and narrow-scope findings

1. **Registry carries no status.** `ufo-swarm-registry-v1` members hold only `kind`, `agentId`, `role`, `item`, and `axes`, and its `wave` is `null`. The status enum (`completed`/`failed`) exists only in the outcome file; the totals use the key `dead`. A gate can bind identity and role to the registry, but status is never cross-checked against it.
2. **Completed rows lack `replaced` and `provider`.** All 28 wave1 completed rows have keys exactly `[id,name,report,role,status]`. Only failed rows carry `replaced:false`, `provider`, and `last_error`. A gate that requires `replaced == false` on every row would reject these three valid rows. A gate that treats an absent field as false passes them without checking anything.
3. Totals are consistent: wave1 seats 71 equals the 71 registry members, and the statuses split into 28 completed and 43 failed. `partial_report_files_do_not_rehabilitate_failed_jobs: true` is present at line 1369.

## Bounded gate recommendation

For each `completed` row, the gate should assert:
- `id == registry.members[name].agentId`
- `role` equals the registry role
- `kind == "spawn"`
- `report == registry.reportDir + "/" + name + ".md"`, and that file exists

It should assert "no replacement" through identity equality to the registry's original spawn id, not through the `replaced` key. It should require `replaced === false` only on `failed` rows, and reject a `completed` row that carries `provider`, `last_error`, or `replaced` with any value other than `false`.

Since the gate cannot authenticate callbacks, it should state in its output that `completed` is trusted from the outcome writer. Report existence must never upgrade `failed` to `completed`. That rule is already encoded at line 1369, and these three rows do not exercise it.

## Evidence paths

- `.ufo/waves/round-21/original-outcomes-final.json` (sha256 `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785`)
- `.ufo/waves/round-21/w1/swarm-registry.json` (sha256 `7756c3b1ff7fdd6f20f4db2e0f2652742f899c945c6210756092061795a105b2`)
- `.ufo/waves/round-21/spec1.json` (sha256 `f78fe7472ed8243d46e23ca29f1bff34e646ff47832093fee815f858c22317af`)
- Other dispatch files in `.ufo/waves/round-21/`: `assignments1.json`, `record1.json`, `run1.json`, `dispatch-attempt-03.json`, `dispatch-attempt-02.json`, `dispatch-refusal-01.json`
- Reports: `.ufo/waves/round-21/w1/RV08SourcesContract.md`, `RV09BatteryBaseline.md`, `RV10DepthBaseline.md`; `w1/battery-baseline.json`; `w1/depth/*`
- Callbacks and transcripts (outside the repo, read-only), under `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22/`:
  - `TameshiR21.jsonl` (`custom_message`/`async-result` entries at the timestamps above)
  - `TameshiR21/TameshiR21.{RV08SourcesContract,RV09BatteryBaseline,RV10DepthBaseline}-3.{jsonl,md}`

Uncertainty: the callback records live in a mutable home-directory session store, and no digest of them is persisted in the repo. If they are rewritten later, this audit's callback rows can no longer be re-verified from the repo alone. No tools were installed or updated.
