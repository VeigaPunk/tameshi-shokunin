# Audit35: wave2 Section1806 / Section1814 / Section1846 accounting audit

Role: connector (read-only). Axis: calibration. Scope: exactly three frozen identities, all wave2. No production edits, no checks run, no tools installed.

## Scoped population

| name | expected id | expected status |
|---|---|---|
| Section1806 | TameshiR21.Section1806 | failed |
| Section1814 | TameshiR21.Section1814 | failed |
| Section1846 | TameshiR21.Section1846 | failed |

## Inputs (sha256 computed this session)

- `.ufo/waves/round-21/original-outcomes-final.json` `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785`. This matches `derivation.json` input_sha256.
- `.ufo/waves/round-21/w2/swarm-registry.json` `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f`. This matches `derivation.json`.
- `.ufo/waves/round-21/spec2.json` `e07159109d91a2fea95a2722a45142a06f41e2e3225e25dbcc05eb375720f6b3`
- `.ufo/waves/round-21/run2.json` `8dcdbbddd89d773d5a5ddadb8dffca052b246b818ea0d170f31710d9c59f3922`
- `.ufo/waves/round-21/dispatch2-attempt-01.json` `3c50b0fa50e67d5d6a1e626982963b4b7b129b72f83731360934abd90122fc40`
- `.ufo/waves/round-21/assignments2.json` `a514a99b…3bad`, `record2.json` `08939676…eb59`
- Gate fixture `.ufo/evidence/round-22/bundle.json` (wave-accounting-v1), wave2 at `members[24..26]` and `outcomes[24..26]`.

## Per-identity rows

| identity | outcome row (final.json L883–911) | registry members[name] | spec2 item | dispatch2 | expected report `w2/<name>.md` | expected mark `w2/sections/<n>.json` | bundle r22 | agreement |
|---|---|---|---|---|---|---|---|---|
| Section1806 | id TameshiR21.Section1806, role scribe, status failed, report null, replaced false, provider haiku, last_error 429 rate limit (retry-after-ms=8412000) | spawn, agentId TameshiR21.Section1806, role scribe, axes [calibration], no status field | role scribe; Report `.ufo/waves/round-21/w2/Section1806.md`; mark `w2/sections/1806.json` | index 24, status `pending`, toolCount 0 | absent | absent | member and outcome failed/replaced false; not in `reports[]` | identity, role, and status agree; no report |
| Section1814 | same shape; failed, report null, replaced false, haiku 429 | agentId TameshiR21.Section1814, scribe | scribe; `w2/Section1814.md`; `sections/1814.json` | index 25, pending, toolCount 0 | absent | absent | failed; not in reports | agree; no report |
| Section1846 | same shape; failed, report null, replaced false, haiku 429 | agentId TameshiR21.Section1846, scribe | scribe; `w2/Section1846.md`; `sections/1846.json` | index 26, pending, toolCount 0 | absent | absent | failed; not in reports | agree; no report |

Partial report versus completed callback: none of the three left any seat-authored artifact. `ls w2/` lists 40 `.md` files and none of them is 1806, 1814, or 1846. `w2/sections/` contains only 1, 131, 314, 375, 405, 933, 1155, 1925, 1938, and 1964. No report text exists that could claim completed execution. The only terminal signal is the outcome row, which says failed with a 429. The 429 is a provider death, not a partial execution. `dispatch2` shows `pending` with toolCount 0, which is consistent with the seats never doing work.

## Contradictions and uncertainty (stated, not smoothed)

1. Callback provenance cannot be authenticated. The status `failed` comes only from `original-outcomes-final.json`. No retained per-seat callback or transcript exists in the repo, and a search of `~/.omp` for `TameshiR21.Section1806` found nothing. This agrees with the contract bound ("retained callbacks are declared inputs, not authenticated provider telemetry"). The agreement shown above is input-consistency only.
2. The registry has no status field. It carries only name, agentId, role, and axes. The status-enum check therefore relies entirely on the outcome file. Registry binding can prove identity and role, not death.
3. Non-terminal snapshots carry divergent values. `run2.json` has `agentId: null` because it is the pre-spawn plan, and `dispatch2-attempt-01.json` says `status: pending` because it is a spawn-time snapshot. Neither contradicts `failed`, but a gate MUST NOT read either one as a status source.
4. Adjacent artifacts can masquerade as reports. `.ufo/evidence/round-21/coldread/source-{1806,1814,1846}.stdout` and `traces/L1/source-*.json` exist (10:06, rev 8eaae28). These are L1 source re-anchors: the trace cwd is `/tmp/tameshi-r21-source-refresh…`, and spec2 says "The L1 source re-anchor is a separate traced read, never fabricated from this mark." Any matcher that searches by section number, rather than by the exact basename in `w2/`, would find "evidence" for these dead seats. This is the concrete rehabilitation hazard for this population.
5. Out-of-scope context: wave2 does have two failed-with-report rows, `ProfileBashTsukuroiCensus` and `V01WitnessTests`. Both have status failed with a non-null report. They explain why the gate's `reports[]` count is 40 against 38 completed. They are not part of this population and were not audited.

## Assertion the gate must make for these identities

For each of the three, the gate MUST assert all of the following:
- `outcome.id == registry.members[name].agentId`
- `outcome.role == registry.role`
- `status == "failed"`, and that value is in the enum
- `replaced == false`
- the seat counts toward `dead`, not `completed`

These hold regardless of `reports[]` membership. Today they also have `name ∉ reports`, but that is an observation, not a premise.

## Bounded recommendation

Add one fixture: `bundle.json` with `"Section1806"` appended to wave2 `reports[]` and nothing else changed. This is the honest form of predicate `failed-with-report-counted-completed` for a provider-dead seat, and it is the C1 rehabilitation path. The gate MUST still compute completed=38 and dead=37 and pass. It MUST reject only when the claimed totals are bumped to 39/36.

- Affected axes: calibration improves, because it proves report presence is inert. No other axis is harmed, because the fixture is additive and changes no production files.
- Risk: this overlaps the existing failed-with-report predicate. If that fixture already uses a provider-dead (429) row, this one is redundant and SHOULD be dropped.
- Verification for L1: run the gate's public CLI on the mutated bundle and assert the exit code and the recomputed totals. Also confirm the gate's report source is exactly `w2/<name>.md` basenames, never `evidence/**/coldread/*<n>*`.
