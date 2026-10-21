# Audit25 — round-21 wave1 SM2/SM3/SM4 callback vs registry vs report (critic, read-only)

**Verdict:** all three identities agree across the registry, the outcome row, and the bundle. Each has a full report. **Uncertainty:** the "completed" status comes only from a declared callback that cannot be authenticated, and the bundle's `replaced:false` is normalized, not observed.

**Axes:** calibration (primary), provenance integrity, identity exactness, accounting completeness.

**Scoped population:** exactly 3 seats in round-21 wave1: `TameshiR21.SM2MeasureHelpers-3`, `TameshiR21.SM3SelftestHelpers-3`, and `TameshiR21.SM4RegistryRows-3`. No other seat is assessed.

**Tool installs:** none.

## Inputs (sha256 observed now; the first three match `.ufo/evidence/round-22/derivation.json` `input_sha256`)

| Path | sha256 |
|---|---|
| `.ufo/waves/round-21/original-outcomes-final.json` | `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` |
| `.ufo/waves/round-21/w1/swarm-registry.json` (`ufo-swarm-registry-v1`, 71 members) | `7756c3b1ff7fdd6f20f4db2e0f2652742f899c945c6210756092061795a105b2` |
| `corpus/lessons/round-21.md` (L119: "Wave1 has real provider deaths, retained as deaths without replacements.") | `35444ddc32116089f87733c8f0a635dc7b452407d2bd0f47de483e8aacfb1a7d` |
| `.ufo/waves/round-21/original-outcomes1.json` (pre-final; same 3 rows) | `3b83e588…e217` |
| `.ufo/waves/round-21/w1/SM2MeasureHelpers.md` | `18b3fbbf…48ef` |
| `.ufo/waves/round-21/w1/SM3SelftestHelpers.md` | `dde05821…224` |
| `.ufo/waves/round-21/w1/SM4RegistryRows.md` | `88f094c8…40be` |

Spec: `.ufo/waves/round-21/spec1.json` (rows at L592/L600/L608, role `simplifier`, axes `[operability]`). Dispatch: `dispatch-attempt-03.json` indices 67/68/69 at launch time `status: pending`, `modelRole: m_composer`. Assignment map: `assignments1.json` L69–71.

## Per-identity rows

| Identity | Registry (`members.<name>`) | Outcome row (`wave1.rows`) | Bundle (`evidence/round-22/bundle.json` wave1) | Report on disk | Report text claim | Agreement |
|---|---|---|---|---|---|---|
| `TameshiR21.SM2MeasureHelpers-3` | `kind=spawn`, agentId exact, role `simplifier` (L659–667) | `status=completed`, role `simplifier`, report path set, **no `replaced` key** (L603–608) | member + outcome `completed`, `replaced:false` (L839–843); name in `reports` | yes, 11486 B, mtime 09:02:32 | "**Verdict: done**"; full inventory and proposal; lane snapshot `33d03b7` | identity/role/status agree; status rests on declared callback |
| `TameshiR21.SM3SelftestHelpers-3` | same shape (L668–676) | `status=completed`, **no `replaced` key** (L610–614) | `completed`, `replaced:false` (L845–850); in `reports` | yes, 14955 B, mtime 09:02:43 | "**Verdict: done**"; complete MB03–12, D02/D11/D12, R02/R05/R07, and T04/T12 tables | agree; same caveat |
| `TameshiR21.SM4RegistryRows-3` | same shape (L677–685) | `status=completed`, **no `replaced` key** (L617–621) | `completed`, `replaced:false` (L852–857); in `reports` | yes, 8295 B, mtime 09:03:32 | "**Verdict:** done (proposal-only)"; findings 1–5 and P1–P5 with citations | agree; same caveat |

Cross-checks (all wave1, used only to place the three seats): each name appears once in the outcomes, and each ID appears once. Registry ID set equals outcome ID set (71 = 71 unique). Wave1 completed-name set equals the set of `.md` basenames in `w1/` (28 = 28; no failed seat has a report, so no partial-report seat exists in wave1). Bundle `reports` equals the completed set.

## Partial report vs completed callback

- None of the three reports is partial. Each one fully answers its Acceptance line from spec1. Report content is still **not** evidence of completion. The `outcome_source` of `original-outcomes1.json` is "original delivered task completion/failure messages". No such message is retained anywhere: there are no transcripts under `~/.omp`, `run1.err` is 0 bytes, and the `run1.json` registry has `agentId: null` because it predates the spawn.
- The timeline is consistent but not proof. Registry and record were written at 09:02:01, the reports between 09:02:32 and 09:03:32, `original-outcomes1.json` at 09:21:48, and final at 10:12:55. A seat that wrote its report and then died before its callback would produce exactly these files.

## Contradictions / calibration findings

1. **Field-presence asymmetry (fixable, not a contradiction).** All 28 wave1 completed rows have no `replaced` key. All 43 wave1 failed rows, and every wave2 row, carry `replaced:false`. The bundle supplies `false` by normalization. `derivation.json` declares this explicitly: "Missing completed-row replaced normalized false from explicit no-replacement declaration in round21 lesson." That source exists and matches its digest (lesson L119). So the `replacement=false` assertion for these three seats rests on a **declaration**, not a per-row observation.
2. **The callback cannot be authenticated** (`contract.json` bounds: "retained callbacks are declared inputs, not authenticated provider telemetry"). For these seats, "completed" is a transcription by L1, not a retained callback artifact. A gate that passes them proves consistency with the declared inputs, not provider success.
3. No identity, role, status-enum, duplicate, or registry mismatch was found for the three seats.

## Bounded gate recommendation

For each of these identities, the gate SHOULD assert exactly these five things:

1. The registry `members[name].agentId` equals the outcome `id`, and the role matches.
2. The outcome `status` is in `{completed, failed}`. Here it is `completed`, taken **only** from the outcome row.
3. The report's existence never sets or upgrades status. The report set may be a superset of completed only for seats that stay `failed` (partial reports). It must never be the source of `completed`.
4. `replaced` is false. A **missing** `replaced` on a source row is accepted **only** when a pinned, digest-verified wave-level no-replacement declaration exists. Otherwise it MUST be refused as `missing-outcome`/`replacement-seat`, never silently defaulted.
5. Totals: wave1 has 28 completed and 43 dead out of 71, all contributing to the round total of 66 completed and 80 dead out of 146.

Smallest safe correction: make the normalization in item 4 visible in the bundle. Either record per-row `replaced_source: "declared:corpus/lessons/round-21.md@35444ddc…"`, or require the declaration digest in `derivation.json` to be part of gate input validation. Today it is listed but only prose ties it to the `replaced` default. Do not claim that "completed" is callback-authenticated for these seats.
