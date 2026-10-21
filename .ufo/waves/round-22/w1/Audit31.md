# Audit31 — round-21 wave2 dead critic seats Section1380 / Section1396 / Section1449

Axis: calibration. Read-only audit; no checks, builds, or digests run; no tools installed.

## Scoped population (exactly three frozen identities, wave2 only)

| name | agent id | role | outcome status | report on disk |
|---|---|---|---|---|
| Section1380 | TameshiR21.Section1380 | critic | failed | none |
| Section1396 | TameshiR21.Section1396 | critic | failed | none |
| Section1449 | TameshiR21.Section1449 | critic | failed | none |

None of the three appears in `.ufo/waves/round-21/w1/swarm-registry.json`.

## Per-identity agreement

All three seats share one evidence pattern. Every line below holds for each name N ∈ {1380, 1396, 1449}.

- **Callback outcome** (`.ufo/waves/round-21/original-outcomes-final.json` wave2 rows, lines 773-801): `status: "failed"`, `report: null`, `replaced: false`, `provider: "codex"`, `last_error: "Retry budget exhausted after 5 retries: Codex error event: Codex is at capacity ... (code=turn_rate_limit_exceeded)"`. These rows have no `actual_result` field, but completed rows do (for example Section0001 at line 648). So the only callback trace for these seats is the `last_error` string.
- **Stable across snapshots**: `original-outcomes2.json` (lines 140-167) and `original-outcomes2-corrected.json` (lines 141-170) have byte-identical field values for these rows. The 40/35 → 38/37 correction (`rule: "Original task callback status wins; partial report creation never rehabilitates a dead seat."`) moved two *other* seats. These three were failed in all three snapshots.
- **Registry** (`.ufo/waves/round-21/w2/swarm-registry.json` lines 125-150): `kind: spawn`, `agentId: TameshiR21.SectionN`, `role: critic`. This matches the outcome id and role exactly. `record2.json` (lines 126-149) matches too. The registry has no status field: it gives membership only, never success.
- **Spec / assignment**: `spec2.json` (lines 112-131) gives role critic. `assignments2.json` (lines 15-17) maps SectionN to TameshiR21.SectionN. The spec told each seat to write `.ufo/waves/round-21/w2/SectionN.md` and `.ufo/waves/round-21/w2/sections/N.json`.
- **Report**: there is no `SectionN.md` and no `sections/N.json` anywhere in the repo (searched for `**/Section{1380,1396,1449}*` and `w2/sections/**`, which lists only 1, 131, 314, 375, 405, 933, 1155, 1925, 1938, 1964). Since no partial report exists, no report text claims completed execution.
- **Gate input** (`.ufo/evidence/round-22/bundle.json`): the members rows at lines 971-984 give id, name, and role critic. The outcomes rows at lines 1375-1394 give `status: failed` and `replaced: false`. All three names are missing from wave2 `reports[]` (lines 1809-1850). `wrong-count-bundle.json` has identical rows.
- **Verdict**: callback, registry, spec, and bundle agree on identity, role, and status. Absence of a report agrees with the callback. **What remains uncertain:** callback provenance cannot be authenticated. The failed row is only a declared input, as `contract.json` itself bounds it.

## Contradictions and attribution hazards (stated, not smoothed)

1. **Verdict could be credited to the wrong seat (1380).** `.ufo/evidence/round-21/coldread/affected-sections.json` lines 157-169 list `verdict:wrong-expectation` as a reason for section 1380 (`credited: false`). That verdict comes from a carried ledger entry, `ledger.json` lines 8688-8700 (`read_rev 01d586dd…`, `wrong_expectations: 1`). Its seat is round-18 `CR31` (`seats`/`reports` at lines 8788-8792, `.ufo/waves/round-18/w2/CR31.md`). It does **not** come from TameshiR21.Section1380. Nothing may read it as round-21 review output from the dead seat.
2. **The L1 traces are not seat reports.** `.ufo/evidence/round-21/coldread/source-{1380,1396,1449}.stdout` and `traces/L1/source-N.json` are L1 source-refresh reads (`refresh-receipts.json` lines 473-557, `--out …/traces/L1/source-N.json`). They exist even though the seats died. Treating their existence as evidence that a critic ran would be the same error as "report existence implies success".
3. **Earlier states, not contradictions.** `run2.json` lines 143-168 have `agentId: null`, which is the pre-registration plan. `dispatch2-attempt-01.json` lines 231-271 have `status: "pending"`, which is the dispatch-time snapshot. Neither is a terminal status, and the final callback supersedes both. Neither file is a gate input according to `derivation.json`.
4. **The projection drops the cause of death.** `derivation.json` projects outcomes to name/id/role/status only. The bundle therefore drops `report: null`, `provider: codex`, and `last_error`. The gate can assert "failed". It cannot assert "provider-dead (codex capacity)". That fits the C1 contract, but any downstream wording of "provider-dead" for these seats rests on `original-outcomes-final.json`, not on the gate.

## Gate recommendation (one, bounded)

For each of these three identities, the accounting gate should assert:

- `members[name=SectionN].id == outcomes[name=SectionN].id == "TameshiR21.SectionN"`, and roles are equal (`critic`).
- `status == "failed"` (a member of the enum), and `replaced == false`.
- The seat counts toward wave2 `dead = 37` and not toward `completed = 38`.
- **Status comes only from `outcomes[]`. Never derive it from `reports[]`.** Absence or presence in `reports[]` must not move a seat between completed and dead.

Narrow fixture gap: in `measure.py`, the `failed-with-report-counted-completed` case only perturbs `claimed` totals (line 64). The control already places a failed seat in `reports` (line 36). So the current fixtures never cover a frozen failed seat whose basename appears in `reports[]` *after* the freeze while `claimed` stays consistent. For these three seats, `reports[]` currently omits them, which is correct. A later re-freeze that adds a stray report must still yield `failed`. The gate is judged on totals and status, so it would catch a flipped status. It would not catch a silently edited `reports[]`, except through the snapshot digest. That is acceptable only because `derivation.json` declares "no status inferred from reports". Keep that declaration binding.

## Evidence paths

- `.ufo/waves/round-21/original-outcomes-final.json` (wave2 lines 635-638 totals 75/38/37; rows 773-801; line 1369 `partial_report_files_do_not_rehabilitate_failed_jobs: true`)
- `.ufo/waves/round-21/original-outcomes2.json`, `.ufo/waves/round-21/original-outcomes2-corrected.json`
- `.ufo/waves/round-21/w2/swarm-registry.json`, `record2.json`, `run2.json`, `spec2.json`, `assignments2.json`, `dispatch2-attempt-01.json`
- `.ufo/evidence/round-21/coldread/affected-sections.json`, `ledger.json`, `refresh-receipts.json`
- `.ufo/evidence/round-22/bundle.json`, `wrong-count-bundle.json`, `derivation.json`, `measure.py`, `contract.json`

I did not recompute the input digests in `derivation.json`.
