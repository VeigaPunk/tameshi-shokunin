# Audit33 — round-21 wave2 dead-seat accounting: Section1517, Section1548, Section1563

Role: connector (leaf, read-only). Axis: calibration. No tools installed. No checks run.

## Scoped population (exactly 3)

| Identity | Registry key / agentId / role | Outcome row (final) | Dispatch snapshot | Expected report `.ufo/waves/round-21/w2/<name>.md` | Declared evidence `w2/sections/<N>.json` | Callback text retained locally | Agreement |
|---|---|---|---|---|---|---|---|
| `TameshiR21.Section1517` | `Section1517` / same / `critic`, `kind: spawn` | `failed`, `report: null`, `replaced: false`, `provider: codex`, `last_error: "Retry budget exhausted after 5 retries: Codex error event: Codex is at capacity … (code=turn_rate_limit_exceeded)"` | `pending`, `modelRole: m_luna`, `toolCount 0`, `requests 0`, `tokens 0`, `durationMs 0` | absent | `sections/1517.json` absent | none (0 of 22 `wait2-recovered-*.json` mention the ID) | agree: dead, no partial report |
| `TameshiR21.Section1548` | `Section1548` / same / `scribe`, `kind: spawn` | `failed`, `report: null`, `replaced: false`, `provider: haiku`, `last_error: "429 … rate limit … retry-after-ms=8412000"` | `pending`, `modelRole: m_haiku`, 0 tools/requests/tokens | absent | `sections/1548.json` absent | none | agree: dead, no partial report |
| `TameshiR21.Section1563` | `Section1563` / same / `scribe`, `kind: spawn` | `failed`, `report: null`, `replaced: false`, `provider: haiku`, `last_error: "429 … rate limit … retry-after-ms=8412000"` | `pending`, `modelRole: m_haiku`, 0 tools/requests/tokens | absent | `sections/1563.json` absent | none | agree: dead, no partial report |

Provider/route consistency: `~/.omp/agent/config.yml` maps `m_luna: openai-codex/gpt-6-luna:max` (matches `provider: codex`) and `m_haiku: anthropic/claude-haiku-5-5:high` (matches `provider: haiku`). The role in all five places agrees for each seat: spec2, assignments2, registry, dispatch `agent`, and outcome row.

## Evidence (paths relative to repo root; sha256 at audit time)

- `.ufo/waves/round-21/original-outcomes-final.json`, `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785`: rows in `.wave2.rows`. `wave2 = {seats 75, completed 38, dead 37}`, status enum observed `{completed: 38, failed: 37}`, top-level `partial_report_files_do_not_rehabilitate_failed_jobs: true`.
- `.ufo/waves/round-21/w2/swarm-registry.json`, `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f`: `members.Section1517/1548/1563`. `reportDir: .ufo/waves/round-21/w2`.
- `.ufo/waves/round-21/spec2.json`, `e07159109d91a2fea95a2722a45142a06f41e2e3225e25dbcc05eb375720f6b3`: three entries with targets SKILL §1517-1547, §1548-1562, §1563-1596. Their prompts carry no `Report:` trailer; they declare only the evidence path `.ufo/waves/round-21/w2/sections/<N>.json`. Completed `Section0314` follows the same spec pattern, so the trailer's absence is not an anomaly specific to these seats.
- `.ufo/waves/round-21/dispatch2-attempt-01.json`: indexes 18/19/20, all `pending` with zero activity.
- `.ufo/waves/round-21/original-outcomes2.json` (file-presence inference), `original-outcomes2-corrected.json`, and `-final.json`: all three files give the same `failed`/`null` row for these seats. The corrected 40→38 change touched only `ProfileBashTsukuroiCensus` and `V01WitnessTests` (failed with a report present). The only corrected→final row diff is `Section0827`'s provider. Neither change touches this scope.
- Directory listings of `.ufo/waves/round-21/w2/` and `w2/sections/` show no file for 1517, 1548 or 1563.
- On-disk mentions of `1517-1547`, `1548-1562` and `1563-1596` exist only in earlier rounds (for example `evidence/round-20/coldread/source-15{17,48,63}.stdout` and `waves/round-16/w2/Replica1548.md`). None of these are round-21 reports, so the gate MUST NOT treat them as such.

## Partial report vs completed callback

There is no partial report for any of the three seats, so the "partial report rehabilitates a dead seat" hazard does not apply here. The risk for these seats is the opposite: a gate that scans by file presence would still classify them correctly, so they cannot discriminate between a file-presence gate and a callback-authoritative gate. The discriminating fixtures are `ProfileBashTsukuroiCensus` and `V01WitnessTests`, which are outside this audit's scope.

Uncertainty, stated rather than resolved:
1. The `failed` status and `last_error` strings are not backed by any retained callback text in the wave directory. The 22 `wait2-recovered-*.json` snapshots contain no record of these IDs. The only raw run artifact, `dispatch2-attempt-01.json`, shows them `pending` with zero activity. `~/.omp/agent/history.db` holds prompt history only, not task callbacks. The status is therefore an L1-declared input, consistent with the contract bound "retained callbacks are declared inputs, not authenticated provider telemetry". It is not corroborated by a retained callback.
2. `m_luna` has a fallback chain in config (`devin/gpt-6-luna`, `anthropic/claude-haiku-5-5`). Failed rows carry no `resolved_model`, so whether those fallbacks were attempted before the codex retry budget ran out cannot be observed. This does not change the dead classification.
3. The outcome `last_error` is recorded against provider `codex`/`haiku` only; the attempt count, apart from "5 retries" for 1517, is unverifiable locally.

No contradiction exists among the registry, spec, assignment, dispatch and outcome artifacts for these three identities.

## Gate assertion (bounded recommendation)

For each of these identities the accounting gate MUST assert this exact tuple against the digest-pinned registry and outcome file:

`registry.members[name].agentId == row.id && registry.members[name].role == row.role && row.status == "failed" && row.report == null && row.replaced == false`

The gate counts the seat in `dead`, never in `completed`, and does so independently of any file under `reportDir` or `sections/`. If `.ufo/waves/round-21/w2/Section15{17,48,63}.md` or `sections/15{17,48,63}.json` later appears, the gate MUST NOT flip these rows to completed. That would be the `failed-with-report-counted-completed` predicate.

Narrow-scope recommendation: use these three seats as "dead with no report" controls (the gate must pass them unchanged). Do not build any of the eight rejection fixtures from them, because they exercise no rejection predicate. The gate cannot authenticate the `failed` status for these seats, and its output SHOULD carry that limitation (callback provenance is declared, not verified) instead of implying that `failed` is telemetry-verified.
