# SourceScope — S082 for callback-authoritative seat accounting

Seat: `TameshiR22.SourceScope-2` (simplifier, leaf). **Report:** `.ufo/waves/round-22/w1/SourceScope.md`

Tool installs/updates: **none**.

## Godspeed axes

| Axis | Move kept |
|------|-----------|
| **Calibration** | Seat totals follow retained callback `status` + membership, not report paths or `actual_result` absence alone. |
| **Source precision** | External row scoped like S081: one located quote, explicit supersession of shorthand, named non-goals. |
| **Authority boundary** | Declared retained inputs (contract + `wave-accounting-v1`) ≠ provider telemetry or cryptographic honesty proofs. |
| **Harm** | R21 admitted claims and erratum bytes stay; recommendation only—no `SOURCES.md` / lesson edits. |

## Contract (read)

`.ufo/evidence/round-22/contract.json` — claim: **callback-authoritative seat accounting, not report-file success**; bound: **retained callbacks are declared inputs, not authenticated provider telemetry**; r21 remains admitted.

## Reopened: `original-outcomes-final.json`

Authoritative retained callback snapshot for round-21 waves (read-only):

| Slice | seats | completed | dead | Notes |
|-------|------:|----------:|-----:|-------|
| wave1 | 71 | 28 | 43 | Most `failed` rows have `report: null`. |
| wave2 | 75 | 38 | 37 | Two **failed + report path** stress rows (below). |
| **total** | **146** | **66** | **80** | Top-level flag: `partial_report_files_do_not_rehabilitate_failed_jobs: true`. |

**False-positive mechanism (wave2 census):** `original-outcomes2.json` inferred `completed` from report presence when `actual_result` was null (`completed: 40`, `dead: 35`). Corrected file `original-outcomes2-corrected.json` rule: *Original task callback status wins; partial report creation never rehabilitates a dead seat.* Same two rows stay **`status: "failed"`** in both corrected and final:

| Seat | `status` | `actual_result` | `report` |
|------|----------|-------------------|----------|
| `ProfileBashTsukuroiCensus` | failed | null | `.ufo/waves/round-21/w2/ProfileBashTsukuroiCensus.md` (exists; prose says “done”) |
| `V01WitnessTests` | failed | null | `.ufo/waves/round-21/w2/V01WitnessTests.md` (exists) |

Final wave2 totals **38/37** match corrected accounting, not the 40/35 file-presence inference.

## Reopened: round-21 outcome-accounting erratum

`corpus/lessons/round-21.md` § **Outcome-accounting erratum (round21)** (`:163-180`):

- Supersedes the earlier **40 returned / 35 provider-dead** wave2 narrative with **38 completed / 37 dead**; names **ProfileBashTsukuroiCensus** and **V01WitnessTests** as partial-report failures never rehabilitated.
- Round total **146** seats → **66 completed / 80 dead**; no replacements.
- Points at `original-outcomes2-corrected.json` for callback metadata; mistake class **attribution/provider**; cites **QUALITY 43** falsifier tail *never … count its dispatch as completed work* (`corpus/QUALITY.md:431`) alongside the **dispatched ≠ completed** lesson reading (capacity guard, not a substitute for callback fields).
- Requires **re-anchor** before a final no-harm assertion after source-input change; prior ledger rows remain data.

Internal alignment (not tier-A external): `tools/wave-accounting.py` module doc and `authority` field — *Reports are artifacts, never terminal-state authority*; *validates caller-declared retained data … not provider telemetry* (`:1-7`, `:116`). `QUALITY.md` criterion **41** — receipt metadata validation is **not producer authenticity** (`:405-406`).

## Proposed SOURCES row **S082** (integrator-only; not written this wave)

Next id already reserved: `corpus/SOURCES.md:267` (`Next unused id: S082`).

| Field | Proposed value |
|-------|----------------|
| **id** | S082 |
| **source** | HTTP Semantics (RFC 9110) — https://www.rfc-editor.org/rfc/rfc9110.html |
| **kind** | spec |
| **tier** | A |
| **scope** | declared terminal status for finite seat/request accounting only; not server or provider honesty |
| **anchor** | §15 Status Codes, opening paragraph @ RFC 9110, reopened 2026-10-21 |
| **teaches** | the response **status code** describes the **result of the request** and response semantics; saved **content** is interpreted **under** that status, not as a replacement for it—parallel to retained callback `status`/`actual_result` over report-file presence; does **not** authenticate that the responder performed honest work (same boundary as contract bounds and QUALITY 41) |
| **status** | mined (proposal) |
| **opened** | 2026-10-21 |
| **recheck** | on-release |
| **used-by** | (integrator) round-22 C1 calibration / `wave-accounting` gate; link `corpus/lessons/round-21.md` erratum; optional future `corpus/knowledge/callback-seat-accounting.md` |

### Located quote (≤25 words)

§15 Status Codes, first sentence:

> “The status code of a response is a three-digit integer code that describes the result of the request and the semantics of the response”

**24 words** (whitespace count). Verified against `https://www.rfc-editor.org/rfc/rfc9110.txt` lines 6791–6793 on 2026-10-21.

### Scope qualification (calibration)

- **In scope:** Treating persisted **declared** outcome fields (`status`, membership, `replaced`, digest-pinned bundle) as the accounting input—analogous to the protocol status code field—while still allowing report paths as **non-authoritative artifacts** (inventory / partial-evidence), matching r21 final flag and `wave-accounting` `failed_with_report` observation.
- **Out of scope for S082:** Provider identity, retry truth, model routing, capacity preflight (QUALITY 43), or cryptographic producer authentication (explicitly excluded by contract and QUALITY 41/39).
- **Not superseding S081:** S081 bounds Bazel **exit code vs stdout**; S082 bounds **declared terminal status vs side artifacts** for orchestrator seat ledgers. Different failure class (r21 Profile/V01 vs S028 shorthand).

### Rejected alternate (frontier note)

`wait(2)` **WEXITSTATUS** (man7) — viable 19-word quote on child **exit status** in the wait status word—but overlaps the exit-channel theme already mined via S028/S081; RFC 9110 separates **status-line outcome** vs **entity body** closer to **callback JSON vs report markdown**.

## Bounded recommendation

1. L1 may add S082 when landing round-22 C1 tooling, with search-log entry mirroring S081’s round-21 pattern.
2. Gate inputs should remain **`original-outcomes-final.json`** (or digest-pinned successor), not report directory census.
3. Do not relitigate round-21’s two admitted precision claims (S079/S081); this row only supplies external vocabulary for the **already-corrected** outcome-accounting erratum.

## Evidence paths

| Path | Role |
|------|------|
| `.ufo/evidence/round-22/contract.json` | C1 claim and bounds |
| `.ufo/waves/round-21/original-outcomes-final.json` | Retained callbacks + totals |
| `.ufo/waves/round-21/original-outcomes2.json` | Superseded 40/35 inference |
| `.ufo/waves/round-21/original-outcomes2-corrected.json` | Correction rule + 38/37 |
| `corpus/lessons/round-21.md:163-180` | Outcome-accounting erratum |
| `corpus/SOURCES.md:90,267` | S081 precedent; S082 id reserved |
| `tools/wave-accounting.py` | Declared-authority semantics (internal) |
| `https://www.rfc-editor.org/rfc/rfc9110` §15 | Proposed S082 anchor |
