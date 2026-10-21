# Audit41 — wave2 KillD02, KillD11, KillD12

**Axes:** identity/accounting fidelity; calibration between a retained report and the callback status recorded by the outcomes source.

## Scope and sources

Read-only audit of exactly these frozen wave2 identities: `TameshiR21.KillD02`, `TameshiR21.KillD11`, and `TameshiR21.KillD12`. Sources inspected:

- `.ufo/waves/round-21/original-outcomes-final.json`
- `.ufo/waves/round-21/w2/swarm-registry.json`
- the three report paths declared by those outcome rows
- the item-named mutation receipts under `.ufo/waves/round-21/w2/mutations/`
- `.ufo/evidence/round-22/contract.json`

The outcomes source has 75 wave2 rows and 38 rows with `status: completed`; across its wave rows the observed status values are `completed` and `failed` (the aggregate summary labels the latter as `dead`). The wave2 registry has 75 members. The three target identities have no duplicate outcome IDs in the source. Registry membership records identity and role but no status field; status is supplied by the outcomes rows.

## Per-identity findings

| Frozen identity | Outcomes row | Wave2 registry member | Retained report and execution claim | Receipt cross-check |
|---|---|---|---|---|
| **KillD02** (`TameshiR21.KillD02`) | `status=completed`; `role=mutation-tester`; `replaced=false`; report path `.ufo/waves/round-21/w2/KillD02.md` | Member key `KillD02`; `agentId=TameshiR21.KillD02`; `role=mutation-tester`; kind `spawn`. Identity and role agree. | File exists. It opens “done — genuinely discriminated” and claims the frozen detector command completed with `KILLED`, then records a pristine/mutant/restored replay. | `mutations/D02.json` exists, 1,780 bytes; SHA-256 `92ad653830b16b98b2b73c49a7e3fc85d903de1c4ae3c654f3577068c422fefa`, matching the report. Receipt records `killed=1`, `inconclusive=0`, one anchor, pristine `SELFTEST: PASS (66/66)`, and the named nonmaster-attached-branch failure. `mutations/D02.stderr` contains the `KILLED` summary; restoration and detector-output receipts are present. |
| **KillD11** (`TameshiR21.KillD11`) | `status=completed`; `role=mutation-tester`; `replaced=false`; report path `.ufo/waves/round-21/w2/KillD11.md` | Member key `KillD11`; `agentId=TameshiR21.KillD11`; `role=mutation-tester`; kind `spawn`. Identity and role agree. | File exists. It opens “done — D11 genuinely discriminated” and claims the frozen detector completed with `KILLED`, with a pristine/mutant/restored replay. | `mutations/D11.json` exists, 1,783 bytes; SHA-256 `2b8a89d267d448cc3e99f9afe5f36079ddd9c30e6c9ba43fdc5c86ca480d1baa`, matching the report. Receipt records `killed=1`, `inconclusive=0`, one anchor, pristine `SELFTEST: PASS (66/66)`, and the named historical-executable-mode failure. `mutations/D11.stderr.txt` contains the `KILLED` summary and `mutations/D11.exit.txt` records exit 0; restoration receipt is present. |
| **KillD12** (`TameshiR21.KillD12`) | `status=completed`; `role=mutation-tester`; `replaced=false`; report path `.ufo/waves/round-21/w2/KillD12.md` | Member key `KillD12`; `agentId=TameshiR21.KillD12`; `role=mutation-tester`; kind `spawn`. Identity and role agree. | File exists. It opens “done — genuinely discriminated” and claims the frozen detector completed with `KILLED`, with pristine/mutant/restored results. | `mutations/D12.json` exists (2,031 bytes; observed SHA-256 `c3b90341e0b2fb3d6026bcf193e7f7820778a5a97d49d112014706fcfc2a2de5`; the report does not state this receipt digest). The receipt records `killed=1`, `inconclusive=0`, one anchor, pristine `SELFTEST: PASS (66/66)`, and both named nonmaster-branch failures; its row contains `verdict=KILLED`. Restoration and pristine/mutated/restored output files are present. No separate `mutations/D12.stderr` file was found; this is an artifact-retention difference, not a conflicting result in the JSON receipt. |

## Assessment

For all three seats, the persisted outcome identity, `completed` status, `mutation-tester` role, `replaced=false`, and wave2 registry membership agree. Each declared report exists and textually claims completed execution rather than presenting only an unfinished/partial report. The corresponding retained JSON receipts are consistent with those claims; D02 and D11 receipt hashes also match their reports. No identity, role, status, or receipt contradiction was observed in this scoped population.

This is consistency checking of persisted artifacts, not independent authentication of the callback that produced them. In particular, a report's existence or its prose claiming success cannot establish a completed callback. The registry itself has no status field, so the observed status comes from the outcome row. The round-22 contract likewise notes that retained callbacks are declared inputs rather than authenticated provider telemetry.

## Bounded gate recommendation

For these exact identities, count a seat as completed only when there is exactly one wave2 outcomes row whose `id` exactly equals that member's registry `agentId`, whose role agrees with the registry role, whose status is exactly the allowed `completed` enum value, and whose `replaced` value is `false`; derive and validate totals from those rows and the frozen input digests. Do **not** infer completion from a report path existing, a report saying “done,” or retained mutation output. A failed callback must remain failed even if it has a partial or success-claiming report. This gate can enforce persisted identity/status/accounting consistency, but cannot authenticate callback provenance beyond its declared inputs.

No production changes, runtime checks, builds, tests, or tool installations were made for this audit.