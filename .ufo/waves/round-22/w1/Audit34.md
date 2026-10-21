# Audit34 — round-21 wave2 dead scribe seats Section1597 / Section1609 / Section1676

Role: connector (read-only). Population: exactly the three frozen wave2 identities below; nothing else audited.
Tool installs: none.

## Inputs read (sha256 where it is the gate's persisted input)

- `.ufo/waves/round-21/original-outcomes-final.json` — `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` (rows at lines 853-880)
- `.ufo/waves/round-21/w2/swarm-registry.json` — `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f` (members at lines 197-222)
- `.ufo/waves/round-21/spec2.json` — `e07159109d91a2fea95a2722a45142a06f41e2e3225e25dbcc05eb375720f6b3` (entries at lines 176-196)
- Corroborating: `assignments2.json:23-25`, `record2.json:198-222`, `run2.json:215-240,853-865`, `dispatch2-attempt-01.json:365-409`, `original-outcomes2.json:220-247`, `original-outcomes2-corrected.json:221-248`, `wait2-recovered-01..22.json`, `run2.err`, `w2/`, `w2/sections/`.

## Per-identity rows

| Name | Outcome row (final) | Registry member | Spec | Dispatch snapshot | Raw callback in wait2-recovered-* | Declared report / mark | Agreement |
|---|---|---|---|---|---|---|---|
| Section1597 | id `TameshiR21.Section1597`, role scribe, status `failed`, report `null`, replaced `false`, provider haiku, last_error 429 retry-after-ms=8412000 | agentId `TameshiR21.Section1597`, role scribe, kind spawn | role scribe, axes [calibration] | index 21, modelRole m_haiku, status `pending` | none (ID absent from all 22 files) | `w2/Section1597.md` absent; `w2/sections/1597.json` absent | identity/role/status consistent; failure provenance not retained raw |
| Section1609 | same shape, status `failed`, report `null`, replaced `false`, haiku, same 429 | agentId `TameshiR21.Section1609`, scribe, spawn | scribe, [calibration] | index 22, m_haiku, `pending` | none | `w2/Section1609.md` absent; `w2/sections/1609.json` absent | same |
| Section1676 | same shape, status `failed`, report `null`, replaced `false`, haiku, same 429 | agentId `TameshiR21.Section1676`, scribe, spawn | scribe, [calibration] | index 23, m_haiku, `pending` | none | `w2/Section1676.md` absent; `w2/sections/1676.json` absent | same |

Observed facts:
- There is no partial report for any of the three, so there's nothing that could rehabilitate them, and no text claims they finished. `w2/` contains `Section{0001,0131,0314,0375,0405,0933,1155,1925,1938,1964}.md` only; `w2/sections/` has 10 marks, none for 1597/1609/1676.
- The original and corrected outcomes agree for these rows. `original-outcomes2.json` and `original-outcomes2-corrected.json` give identical rows (failed, report null). The correction ("Original task callback status wins; partial report creation never rehabilitates a dead seat", supersedes file-presence inference) didn't change them.
- The final file's totals recompute exactly. Wave2 has 75 rows: 38 completed and 37 failed. Every row has `replaced=false`. Grand total is 146/66/80. `haiku` dead count is 22.
- The round-22 bundle (`.ufo/evidence/round-22/bundle.json:1011-1022,1431-1442`) mirrors id/name/role/status=failed/replaced=false for these three. It is in-flight production and I did not wait on it.

## Contradictions / uncertainty

1. **The failure provenance is asserted but not retained in raw form.** The `failed` status and the `429 … retry-after-ms=8412000` string appear only in the three derived outcomes files (plus the sibling report `round-22/w1/Audit49.md`). They are absent from `run2.err`, `dispatch2-attempt-01.json` (which shows `pending` at spawn), and every `wait2-recovered-*.json`. The recovered wait snapshots contain callbacks only for other Section seats (0001/0006/0131/0314/0375/0405/0933/1155). So "failed" is consistent but cannot be authenticated from retained callback artifacts. That matches the contract's statement that the gate cannot authenticate callback provenance. It is not a contradiction between files.
2. **Unrelated files share the section numbers.** These L1 cold-read files use the same numbers but are not seat reports: `.ufo/evidence/round-21/coldread/source-{1597,1609,1676}.stdout` and `traces/L1/source-*.json` (schema `tameshi-trace-inputs-v1`, mtime 10:06:45-46, a `SKILL.md` line-range dump). A gate or auditor that links evidence to a seat by section number or glob `*1597*` would wrongly attach a "report" to a dead seat. This is how partial or foreign files can rehabilitate a dead seat.
3. Out of scope, context only: wave2 has two other failed rows with a non-null `report` (`ProfileBashTsukuroiCensus`, `V01WitnessTests`). They are the live test of the rule; my three are the trivial case.

## Gate recommendation (one, bounded)

For each wave row, key the join on the exact registry identity: `rows[i].id == registry.members[rows[i].name].agentId` and `rows[i].role == members[name].role`. Then require the following for every `status == "failed"` row:
- it counts in `dead`;
- `replaced is False`;
- its `report` field, and any file at the spec-declared `Report:` path, are never consulted to compute `completed`.

Report linkage, if checked at all, must use only the exact spec-declared path (`.ufo/waves/round-21/w2/<name>.md`). It must never use section-number or substring matching, because that would pull in the L1 `coldread/source-NNNN.*` evidence.

For these three, the gate's concrete assertion is: name ↔ agentId ↔ role=scribe match the registry; status=failed; report=null; replaced=false; counted among wave2 dead=37. The gate should label the failure as "derived outcome status, raw callback not retained" and not as an authenticated callback.

Verification for L1: recompute wave2 totals from `original-outcomes-final.json` (75/38/37), and confirm `members[name].agentId` equality for all 75 rows with the persisted digests above.
