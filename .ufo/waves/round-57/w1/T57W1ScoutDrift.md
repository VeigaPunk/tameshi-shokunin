# T57W1ScoutDrift — planning-time cold-read drift forecast (round 57, wave 1)

Item: for the round's planned edit set, measure — not guess — which of the 64 cold-read
headings lose credit, by applying each planned path's smallest edit ONE PATH AT A TIME in
scratch clones of the lane at base `5e3569969b532310d2b8a3d130901757a3df356b`, committing
(fixture identity, `-C`), and running the round-21 monitor per clone. This is the
planning-time cost the round commits to (considerthese proposal 3); wave 3 compares it
with the measured drift at C0.

## Method

- 11 shared clones of the pristine base clone, one single-path edit each (edit/write tools;
  batch 2/3 worktrees verified `status --porcelain` = exactly one path before running).
- Per clone: toplevel assert, `add -A`, fixture commit, then
  `python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev <HEAD> --explain`.
- 4-way parallel batches (81.5 s / 64.2 s / 74.4 s); base re-derived first: **64/64, score 8**
  (112.3 s wall; `base.stdout`). All 11 probe runs exit 0. Receipts: `T57W1ScoutDrift-receipts/`
  (25 files: base + 11 stdout/stderr pairs, `drift-summary.json`, `commands.txt`).
- JSON probes (`routed-defects.json`, `registry.json`) use a minimal JSON-valid byte change
  instead of a raw append — a raw append would corrupt JSON. The input gate hashes whole
  blobs, so the drift effect is identical to any other byte change on the path.

## Result table (path -> lost headings, measured)

| path (smallest edit) | covered | score | lost |
|---|---|---|---|
| base (no edit) | 64/64 | 8 | 0 |
| `corpus/SOURCES.md` (append 1 blank+text line) | 51/64 | 6 | **13** |
| `tools/registry.json` (minimal byte change) | 53/64 | 6 | **11** |
| `corpus/QUALITY.md` (append 1 blank+text line) | 58/64 | 6 | **6** |
| `corpus/README.md` (append 1 blank+text line) | 58/64 | 6 | **6** |
| `SKILL.md` (one word inside `## Standing rules`, line count preserved) | 63/64 | 6 | **1** |
| `corpus/routed-defects.json` (minimal byte change) | 64/64 | 8 | 0 |
| `corpus/knowledge/receipt-revision-binding.md` (append) | 64/64 | 8 | 0 |
| new `corpus/knowledge/cold-read-drift-forecast.md` | 64/64 | 8 | 0 |
| `SCORECARD.md` (append) | 64/64 | 8 | 0 |
| `LOG.md` (append) | 64/64 | 8 | 0 |
| new `corpus/lessons/round-57.md` | 64/64 | 8 | 0 |

Lost-heading lists (probe `input-drift:<path>` unless noted; full reasons in receipts):

- **SOURCES (13):** `## Standing rules`; `## The leg ledger — replay, receipt, and how it is
  read (round 7, measured)`; `## Pin disposition and provenance correction — round 13`;
  `## Repeated controls and gate registry — round 12`; `## Effective expectation
  reconciliation — round 14`; `## Context gate classification and explicit exit classes —
  round 15`; `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`;
  `## Live-tree re-pin and entry-command monitor — round 17`; `### Round-13 gate/probe
  registry`; `### Round-17 gate/probe registry — re-pin and monitor`; `### Round-18
  gate/probe registry — routed-defect closure`; `### Round-21 gate/probe registry — finite
  environment differential`; `### Triggers T1–T3 and the re-pin rule`.
- **registry.json (11):** `## Standing rules`; `## The operator's runbook and the six-leg
  regression (round 10, measured)`; `## Mutation-sweep recipe …`; `## Live-tree re-pin …`;
  `## Context gate classification … round 15`; `### The service's limits — what tameshi
  refuses to mutation-test`; `### Round-17 gate/probe registry …`; `### Round-18 gate/probe
  registry …`; `### Round-21 gate/probe registry …`; `### Round-26 gate/probe registry —
  report interop`; `### Triggers T1–T3 and the re-pin rule`.
- **QUALITY (6):** `## Standing rules`; `## Mutation-sweep recipe …`; `## Live-tree re-pin …`;
  `### Round-18 gate/probe registry …`; `### Round-21 gate/probe registry …`; `### Triggers
  T1–T3 and the re-pin rule`.
- **README (6):** `## Standing rules`; `## The leg ledger …`; `## Mutation-sweep recipe …`;
  `## Live-tree re-pin …`; `### The map — where a reader enters, artifact by artifact`;
  `### Triggers T1–T3 and the re-pin rule`.
- **SKILL.md (1):** `## Standing rules` — reason `no-ledger-entry` (section text sha no
  longer matches any entry; SKILL.md is an ignored *input*, so only edited sections pay).

## Union and minimal reader count

- **Union of lost headings across all 11 paths: 17** (13 SOURCES ∪ 11 registry ∪ 6 QUALITY ∪
  6 README ∪ 1 SKILL — heavy overlap: every one of the four content paths also loses
  `## Standing rules`).
- **Minimal reader count: 47** — 47 of 64 sections keep credit with no new reads; the 17
  union headings are exactly what wave 3 must re-key with fresh readers at C0.
- Forecast if the whole planned set lands as drafted: monitor reads **47/64, score 6**
  (the score drops 8→6 whenever `box3_full_page` goes false, i.e. after the first lost
  heading; more loss does not lower it further).

## Cross-check against the round record

Recorded fact: "appending one line to each of QUALITY/SOURCES/README dropped 64 → 50".
Measured union of exactly those three paths: 14 distinct lost headings → 64−14 = **50**.
Reproduced exactly.

## Mechanism notes (from the reasons, grounded in `.ufo/evidence/round-18/measure.py`)

- Sections match ledger entries by **section-text sha256**; a credited entry with any
  drifted input becomes stale (does not credit, does not veto). A section loses credit when
  its last clean crediting entry drifts → `input-drift:<path>`.
- `SCORECARD.md`/`LOG.md` are pinned by 6 entries each yet lose 0: every section those
  entries serve has another clean crediting entry. Pinning count alone does not predict
  loss; sole-creditor status does. `corpus/routed-defects.json` and
  `corpus/knowledge/receipt-revision-binding.md` are pinned by 0 entries.
- SKILL loss scales with the number of sections whose text changes: the planned round edit
  touches the receipt table cell and adds a `### Gate/probe registry` row — count the
  sections whose text actually changes; each costs 1 heading. My probe changed one word in
  one section → exactly 1.
- Secondary finding: reason strings of lost sections surface **pre-existing stale ledger
  entries** (`input-drift` for paths the probe never touched: `tools/env-diff.py`,
  `.ufo/evidence/round-15/verify.py`, `corpus/knowledge/service-limits.md`, …). They are
  harmless under the stale-does-not-veto rule but show the ledger already carries
  non-verifying entries; the wave-3 re-key must not copy their input sets.

## Honesty

- 11/11 probe runs + base run exit 0; every number above is from a receipt on disk.
- Batch 1 clone worktrees were not `status --porcelain`-checked before commit (they were
  fresh clones with one tool-applied edit each); batch 2/3 were checked and clean.
- No tools installed or upgraded (none needed). No lane production file touched; scratch
  lives under `/fast/scratch/hyaku/tameshi-r57/T57W1ScoutDrift`.
