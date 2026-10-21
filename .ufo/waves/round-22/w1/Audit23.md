# Audit23 — round-21 wave1 SB07/SB08/SB09 seat accounting (critic, read-only)

Axis: calibration. Scope: exactly three frozen identities, wave1 only.
No tools installed or updated. No production, git, or evidence files touched; this file is the only write.

## Scoped population

| name | id | role | wave |
|---|---|---|---|
| SB07CapabilityRow | TameshiR21.SB07CapabilityRow-3 | scribe | wave1 |
| SB08GuardKillAddendum | TameshiR21.SB08GuardKillAddendum-3 | scribe | wave1 |
| SB09ReportSkeleton | TameshiR21.SB09ReportSkeleton-3 | scribe | wave1 |

## Inputs (sha256 observed now)

- `.ufo/waves/round-21/original-outcomes-final.json` `029fc1e0…698785` (matches `.ufo/evidence/round-22/derivation.json` `input_sha256`)
- `.ufo/waves/round-21/w1/swarm-registry.json` `7756c3b1…5b2` (matches derivation)
- `.ufo/waves/round-21/spec1.json` `f78fe747…17af`
- `.ufo/waves/round-21/record1.json` `9ca4efc4…54b0`
- `.ufo/waves/round-21/dispatch-attempt-03.json` `951d710a…2674`
- `.ufo/evidence/round-22/bundle.json` `dfb1027f…5e` (matches `expected.json` `bundle_sha256`)
- Out-of-repo corroboration (read-only, not a declared gate input): `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22/TameshiR21/TameshiR21.<name>-3.{jsonl,md}`, `~/.omp/logs/omp.2026-10-21.2967303.log.{3,4}`

## Per-identity agreement

| identity | outcomes-final row | w1 registry / record1 / assignments1 | spec1 / dispatch-03 | report path in task | report on disk | session transcript (callback corroboration) | verdict |
|---|---|---|---|---|---|---|---|
| SB07CapabilityRow-3 | :546-553 status=failed, report=null, provider=haiku, replaced=false, 429 retry-after-ms=10131000 | registry :600-609 spawn, agentId exact, role scribe; record1 :601-603 same; assignments1 :63 same | spec1 :539 role scribe; dispatch-03 idx 61 modelRole m_haiku, status `pending` (non-terminal snapshot, async running) | `.ufo/waves/round-21/w1/SB07CapabilityRow.md` | ABSENT; draft `w1/drafts/scorecard-21.md` ABSENT (`drafts/` empty) | 11 entries; single assistant msg `stopReason=error`, 429 rate_limit_error, retry-after-ms=10131000, 0 tool calls; output `.md` 0 bytes (sha256 e3b0c442…b855) | AGREE: failed, no report, provider-dead |
| SB08GuardKillAddendum-3 | :556-563 same fields/values | registry :610-619; record1 :611-613; assignments1 :64 | spec1 :548; dispatch-03 idx 62 m_haiku `pending` | `.ufo/waves/round-21/w1/SB08GuardKillAddendum.md` | ABSENT; draft `w1/drafts/guard-kill-addendum.md` ABSENT | same shape: one errored assistant turn, 429, 0 tools; output `.md` 0 bytes | AGREE: failed, no report, provider-dead |
| SB09ReportSkeleton-3 | :566-573 same fields/values | registry :620-629; record1 :621-623; assignments1 :65 | spec1 :557; dispatch-03 idx 63 m_haiku `pending` | `.ufo/waves/round-21/w1/SB09ReportSkeleton.md` | ABSENT; draft `w1/drafts/report-tameshi-21.md` ABSENT | same shape: one errored assistant turn, 429, 0 tools; output `.md` 0 bytes | AGREE: failed, no report, provider-dead |

Bundle projection (`.ufo/evidence/round-22/bundle.json`): wave1 members :317-329 and outcomes :797-815 carry id/name/role/status=failed/replaced=false exactly. wave1 `reports` (28 basenames) contains none of the three, which matches the 28 `.md` files present in `w1/`. wave1 claimed 71/28/43 matches the outcome status histogram {completed:28, failed:43}. No replacement seat for these names appears in w2, spec2, run2, or dispatch2. A content grep of round-21 found matches only in wave1 files.

None of the three seats has a partial report, so this population cannot test the "partial report rehabilitates a failed seat" case positively. The failure evidence is consistent across every source. Uncertainty: the outcomes `last_error` is a normalized string, not the verbatim callback body, so its provenance rests on the transcript and is not authenticated (contract bound 1).

## Counterexamples a naive gate would get wrong (found locally)

1. **Report-like artifacts exist for dead seats.** `TameshiR21.<name>-3.md` exists in the session dir for all three seats, at 0 bytes. A gate that tests "output file exists" or "any report-shaped file for this id" would count these seats as completed.
2. **The session exit looks normal.** Each transcript ends with `custom session_exit {reason:"dispose", kind:"normal"}`. That records process disposal, not task success.
3. **The fallback provider succeeded, but only for titles.** omp log.4 :1068, :1432, :1445 show `title-generator: success` for all three on openai-codex fallback after the 429. The main run's fallback chain was only `anthropic/claude-haiku-5-5:high` (log.3 :40090/:40102/:40258), and the main turn errored. Provider liveness for the seat must not be inferred from title generation.
4. **Non-terminal snapshots carry a status.** dispatch-attempt-03 shows `status: "pending"`, and run1 shows `agentId: null`. A gate that reads status from any file other than the declared outcomes would see a non-terminal or unknown status for terminally failed seats.

## Impacted axes

Calibration: false-completion risk via counterexamples 1 and 2. Identity: the registry has no status field (0 `"status"` matches), so status authority is the outcomes file alone; there are not two authorities.

## Gate recommendation (bounded)

For each of these ids, the gate must assert that the outcome row exists exactly once, its `id`/`name`/`role` byte-match the w1 registry spawn entry, `status ∈ {completed, failed}` and equals `failed`, `replaced == false`, and the seat is counted in wave1 `dead`. Report presence must be advisory only. Any report file for a failed id, including an empty file or a file outside `w1/`, must never move the seat to `completed`; it should be rejected under `failed-with-report-counted-completed`. Status must be read only from the digest-pinned outcomes input, never from dispatch or run snapshots, session exit kind, or title-generator events.

Smallest safe correction: none is needed for these three rows. Recommend a fixture that pairs a `failed` outcome with a present 0-byte report basename. It must be rejected if counted as completed, and it must leave totals unchanged when correctly counted dead. That counterexample class is not covered by any existing partial-report row in this scope.
