# ScoutRefreshRecon — round-36 cold-read refresh apparatus recon

Seat: ScoutRefreshRecon (leaf, read-only). Judged on: calibration.
Attacked: claim **C1** only — "cold-read monitor refresh of the four round-35-drifted SKILL headings restores credit 6 -> 8" under `contract.json` (frozen 2026-10-24). C2 (tally-audit v2 counter) shares the wave but is NOT part of the refresh apparatus; nothing under `coldread/` feeds it.

## Commands / reads exercised (recon only; no monitor run by this seat — the deciding before/after runs belong to the L1 claim receipt)

- Read `.ufo/evidence/round-36/contract.json` (claim C1: before rev `796e08b888849308d0c4d5e932e56833600a139f`, expected 6 → 8, kill rule: refresh entries + trace receipts are the only delta).
- Read `.ufo/evidence/round-21/coldread/measure.py` (the C1 monitor; selector over `.ufo/evidence/round-18/measure.py`).
- Read `.ufo/evidence/round-18/measure.py` sections 25-29, 113-141, 330-350, 353-429, 459-546, 549-656 (credit algorithm actually executed by the monitor).
- Read `.ufo/evidence/round-21/coldread/ledger.json` head + tail; `python3` count: **497 entries total**, last 4 are the round-36 refresh entries at `read_rev e423c41ba253357ab8c8513f0376dad9d38ab248`.
- Read `.ufo/evidence/round-36/coldread/refresh-specs.json`, `refresh-receipts.json`, `affected-sections.json`, `traces/L1/source-{1..4}.json`.
- Grepped `SHONEN.md` — box-3 line 10 carries `[~]` and links `.ufo/evidence/round-21/coldread/ledger.json` (the monitor's `BOX3_LINK` override target).

## How the score moves (monitor mechanics, observed in round-18/measure.py)

`calibration_restraint_score` = 2·(box1 `~`) + 2·(box2 `~`) + 2·(box4 `~`) + 2·(box3 `~` **and** `box3_full_page` **and** SHONEN box-3 block links the ledger). Baseline 6 = three `~` legs holding while box-3's `box3_full_page` leg fails. `box3_full_page` is `sections_covered == sections_total` (line 655); the four drifted sections were the only uncovered ones (60/64 → the refresh targets 64/64).

A ledger entry earns `credited` only when ALL of `entry_reason` gates pass (lines 513-526):
1. `entry_failure` — verdict ∈ VALID_VERDICTS, not FAIL; `blocking_gaps==0`, `wrong_expectations==0`.
2. `entry_credit_reason` — for `class:"record"`, verdict ∈ {verified-record, **gap-minor**} (line 507).
3. `commands_executed_count` > 0 (line 521; **no minimum quality — 1 suffices**).
4. `input_reason` — every `inputs` key (minus IGNORED_INPUTS: SKILL.md, both ledgers) must be a canonical blob whose sha256 at the **measured rev** matches the recorded digest (`input_failures` 330-350). `read_rev` is metadata only — never consulted for credit.
5. `trace_reason` (strict) — since cmd>0, ≥1 committed `tameshi-trace-inputs-v1` receipt whose `inputs` digests all appear verbatim in the ledger `inputs` view (411-417), and `live_lane_reads` must be empty-or-bound (418-428).

## Artifact → claim map (all support C1 exclusively)

| Artifact | Role in the C1 predicate |
|---|---|
| `contract.json` C1 block | Freezes before-rev 796e08b8, expected 6→8, do-nothing control (content commit without ledger delta must still print 6), kill rule (entries+traces the only delta). |
| `coldread/refresh-specs.json` | Plan: `planned_at_revision e423c41b`, 4 specs keyed by section `{start,end,heading,sha256}` + required `paths`. Scope line: "L1-author input-keyed source reads only; not independent/blind cold-read, recipe re-execution or required-command coverage". |
| `coldread/affected-sections.json` | Driver output naming exactly the four sections 131 / 375 / 1380 / 1436 with `input-drift:<path>` reason strings (duplicated per key — cosmetic). Confirms these were the four round-35-drifted sections. |
| `traces/L1/source-{1..4}.json` | `tameshi-trace-inputs-v1` receipts produced by `tools/trace-inputs.py` wrapping a `python3 -c` digest script in a `/tmp` lane copy at rev e423c41b; each records `inputs` sha256s of SKILL.md + spec paths, `exit 0`, empty `live_lane_reads`. Satisfies strict `trace_reason` (gate 5). `rev_reason: null`, `external:{}`, `untracked:{}`. |
| `ledger.json` entries 494-497 (tail) | The payload: four `class:"record"`, `verdict:"gap-minor"`, `blocking_gaps:0`, `wrong_expectations:0`, `minor_gaps:0`, `commands_executed_count:1`, `read_rev:e423c41b`; `inputs` digests byte-identical to the trace receipts; `traces`/`reports`/`seats` point at the artifacts above. Satisfies gates 1-4. Section `sha256` matches spec `sha256` (e.g. `e37cf21e…` for 131-245), so `by_sha` lookup hits. |
| `coldread/refresh-receipts.json` | Provenance rollup: `entries_added:4`, `original_entries_retained:493`, per-section `argv` (trace-inputs.py wrapper), `instrument_sha256`, `stdout_sha256`, `cited_source S103`, `round36_provenance{source_read_entries:4, protocol:"round-21 L1 author source re-anchor"}`. Not consulted by the monitor (reports field is informational). |
| `measure.py` (r21 selector) | Unchanged monitor: refuses `--ledger-file/--ledger-rev/--inputs-overlay` (exit 64), pins `LEDGER_PATH`/`BOX3_LINK`/`IGNORED_INPUTS` to the r21 ledger, delegates to the frozen round-18 algorithm. Guarantees the 6→8 delta is attributable to ledger content alone. |
| `SHONEN.md` box-3 line | Pre-existing `~` + ledger link supplies the non-refresh legs of the 8; refresh only had to restore `box3_full_page`. |

Consistency observed: spec `paths` == receipt `argv` path lists == trace `inputs` keys minus SKILL.md == ledger `inputs` keys minus SKILL.md, with identical digests across trace and ledger for every path (spot-verified all four entries). No stale-failure veto risk: `gap-minor` is non-failing so `vetoes` stays empty even as duplicate `by_sha` entries accumulate.

## NOT covered by the refresh scope statement (explicit + observed gaps)

Explicit in the scope line ("L1-author input-keyed source reads only"):
1. **Independent/blind cold-read** — the L1 authored both the sections and the refresh entries; no fresh seat re-read. Entries 494-497 carry no `binding`/`provenance` block (unlike r32 ColdC03 entries) and `seats` names only "L1 TameshiR36 author source re-anchor".
2. **Recipe re-execution** — the trace argv is a sha256 digester; it emits the section bytes + `SOURCE` digest lines. It never ran the mutation-sweep recipe the section describes.
3. **Required-command coverage** — `commands_executed_count:1` counts the digest invocation itself, not the section's prescribed commands; the monitor only requires >0.

Observed beyond the scope line:
4. **Verdict freshness** — `verdict:"gap-minor"` is asserted, not re-derived; nothing re-adjudicates the four sections' prose. `minor_gaps:0` with a `gap-minor` verdict is self-consistent but unchecked.
5. **The other 493 entries** — no re-validation; any input drift outside the four refreshed sections would still silently uncredit those sections (refresh restored coverage only where `affected-sections.json` flagged drift at e423c41b).
6. **`read_rev` honesty** — the field is ignored by `entry_reason`/`input_reason` (inputs verify at the *measured* rev); a wrong `read_rev` would not be caught by the monitor.
7. **`external_inputs` / `live_lane_reads` / `rev_reason`** — all empty/null; no external-input or live-lane evidence exercised.
8. **Boxes 1, 2, 4 and the SHONEN `~`/link preconditions** — carried over un-re-verified by the refresh; assumed held since the before run (kill rule covers "no monitor/rubric change", not SHONEN content).
9. **Future drift** — entries pin digests at e423c41b; any post-refresh input edit re-drifts coverage (by design; do-nothing control relies on this).
10. **C2** — `c1-measure-v2.py` and the tally-audit panel are untouched by every artifact in `coldread/`.
11. **Selector selftest** — `measure.py --selftest` was not part of the refresh receipts; the packaged synthetic suite is unexercised here.

## Confidence / unknowns

- High confidence the four new entries satisfy every `entry_reason` gate at a rev where the recorded input blobs exist (digests match trace receipts; SKILL.md is ignored anyway). The 6→8 hinge is purely `box3_full_page` — provided no fifth section is uncovered at the refresh rev. **[INFERENCE]** no monitor run performed by this seat; the L1's claimed runs at the named revs are unverified here.
- Cosmetic anomaly: `affected-sections.json` reason strings repeat `input-drift:` keys (driver emitted one entry per historical entry, deduped into `paths`).
- `entries_added:4` / `retained:493` in receipts matches observed 497 total.

## Verdict

APPARATUS-SOUND-FOR-C1 (conditional): the refresh's four entries + four trace receipts + untouched monitor satisfy the credit predicate exactly as the contract's kill rule requires — the only delta is ledger entries and traces. Scope is honestly narrow: author-asserted `gap-minor` verdicts over digest-only reads; no independent seat, no recipe execution, no command coverage, no re-validation of the other 493 entries. Calibration risk: the 8 credits now include four sections whose "read" is a hash observation, which the monitor treats identically to a full cold read.

Report written by ScoutRefreshRecon; no lane files modified; no monitor or git-mutating commands run.
