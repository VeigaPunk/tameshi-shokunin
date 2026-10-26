# T50ConnSiblingDefects — Sibling-overlap scan for C1 (routed-defect ledger)

Seat: `T50ConnSiblingDefects` (connector, wave 1, round 50). Read-only scan of the fleet for
how sibling lanes track the defects their closures route, so `corpus/routed-defects.json`
(C1) adopts proven patterns and absorbs nothing it must not.

Method: read-only `read`/`grep`/`find` over `/home/vgpnk/Projects/shokunin/*-shokunin`
(never the scratch state, never hidden C2 panel). Commands that show each finding are given
per item; all line numbers are at the revision read today (2026-10-26).

---

## 1. The fleet-wide routing convention (source of the 49 items)

Every lane's non-author closure writes a `*-verifier-spotcheck.md` with a routed-defect
section. The canonical wording is in the hyaku closure template,
`scripts/hyaku/closure-prompt.md:44-48` (step 4): *"…trend verdicts with evidence, and
routed defects the lane must fix next round."* Observed headings (file:line):

| Lane / round | Heading | Location |
|---|---|---|
| tameshi r40 | `## Routed defects (status-neutral; the lane fixes these next round)` | `tameshi-shokunin/corpus/lessons/round-40-verifier-spotcheck.md:291` |
| tameshi r45 | `## Routed defects for the lane next round` | `round-45-verifier-spotcheck.md:83` |
| tameshi r48 / r49 | `## Routed defects for the lane next round` | `round-48-verifier-spotcheck.md:112`, `round-49-verifier-spotcheck.md:120` |
| kake r49 | `## Routed defects` | `kake-shokunin/corpus/lessons/round-49-verifier-spotcheck.md:109` |
| kama r47 | `## 6. Routed defects (lane fixes next round unless marked)` | `kama-shokunin/corpus/lessons/round-47-verifier-spotcheck.md:95` |
| mado r46 | `## 6. Routed defects (lane fixes next round)` | `mado-shokunin/corpus/lessons/round-46-verifier-spotcheck.md:105` |
| mori r49 | `## 5. Routed defects (lane must fix next round)` | `mori-shokunin/corpus/lessons/round-49-verifier-spotcheck.md:108` |
| tsukuroi r42 | `## 6. Routed defects (owner: tsukuroi, next round)` | `tsukuroi-shokunin/corpus/lessons/round-42-verifier-spotcheck.md:189` |
| kaidoku r41 | `## 5. Routed defects (lane fixes next round; status-neutral)` | `kaidoku-shokunin/corpus/lessons/round-41-verifier-spotcheck.md:89` |
| chousa r49 | `## Routed defects (the lane fixes next round)` | `chousa-shokunin/corpus/lessons/round-49-verifier-spotcheck.md:93` |
| kotoba r49 | `## Routed defects (the lane fixes these next round)`; separate `## Routed items from round 48 (as claimed?)` | `kotoba-shokunin/corpus/lessons/round-49-verifier-spotcheck.md:214`, `:182` |
| kotodama r50 | `## Accounting, limits and routed debt` | `kotodama-shokunin/corpus/lessons/round-50-verifier-spotcheck.md:84` |
| kasegi r38 | `## 5. Routed defects (kasegi owes these next round)` | `kasegi-shokunin/corpus/lessons/round-38-verifier-spotcheck.md:153` |
| kengaku r40 | `## 5. Routed defects (round 41)` | `kengaku-shokunin/corpus/lessons/round-40-verifier-spotcheck.md:90` |

The tameshi wording (`round-40…:291` "status-neutral; the lane fixes these next round") is
an early form of the fleet convention; later tameshi rounds dropped "status-neutral".
kaidoku kept the "status-neutral" qualifier — the best wording because routing is a
forwarding act, not a verdict.

---

## 2. Lanes with a machine-checkable disposition record

Four lanes already turn routed defects into machine-checked records. They are the direct
predecessors of C1's `corpus/routed-defects.json`.

### 2a. kagi — `closure-dispositions.py` + `closure-dispositions.json` (closest to C1)
- `kagi-shokunin/corpus/closure-dispositions.py` parses the closure spot-check into an
  obligation set and verifies one typed disposition per obligation against the tree.
  Schema `kagi-closure-dispositions-v1` (`:59`), source default `corpus/lessons/round-22-verifier-spotcheck.md`
  (`:60`), disposition vocabulary `KINDS = {"fixed", "reported", "rejected", "no-action", "operator-owned"}`
  (`:62`), obligation parsing `HEAD_RE`/`ROUTED_RE` (`:64-65`), `verify()` resolves every
  `pointer` in-tree (`:106-129`, `:147-228`); pinned source digest
  (`:74-76`). Selftest `:274-375`.
- The record itself: `corpus/closure-dispositions.json:2-4` pins `source` and
  `source_sha256`; `:5-111` one disposition per obligation with `id`, `class`,
  `disposition`, `note`, `pointer`. The gate is claimed as a ledger row
  (`corpus/claim-ledger.tsv:60`, R23-02: `CLOSURE_DISPOSITIONS: CLEAN (obligations=15 fixed=6 reported=3 operator_owned=1 no_action=5 rejected=0 pointers=15)`).
- Command that shows it: `python3 kagi-shokunin/corpus/closure-dispositions.py` (read-only
  verification; executed by the lane's own claim ledger).

### 2b. kengaku — JSONL routed-findings and defect ledgers with per-row checks
- `kengaku-shokunin/corpus/routed-findings.jsonl` — one JSON row per routed finding:
  `id` `R{round}-R{n}`, `class`, `source` (spot-check file:line), `opened_round`,
  `status` (`closed`/`open`/`blocked`), `close` (free text naming the fixing commit and
  what it added), `blocker`, `check` (a shell command that re-verifies), `note`
  (`:1-16`; e.g. `R39-R2` open with a concrete measured traceback, `R39-R3` blocked with a
  pinning conflict).
- `corpus/defects.jsonl` — round-34 defect rows carry `recurrence_of` (e.g.
  `R34-D1` → `"R33-N1 (round-32 wave paths untracked at tip; plans/round-33-claims.md:87)"`,
  `:1`), the one structured recurring-defect criterion found in the fleet.
- `plans/defect_ledger.py` — round-35 C2 calibration counter that binds ledger rows to named
  check functions (`CHECKS = {f.__name__: f …}` at `:111`; `r34_d1` at `:37-44`), proving
  the ledger is machine-checked, not prose.

### 2c. kotoba — verifiers over routed repairs (a full counter)
- `kotoba-shokunin/verifiers/check_r63_routed_repairs.py` — a C2 calibration counter over
  the five round-62 routed corrections: pins `BASE_REV` = the pre-correction tip
  (`:77-81`), verifies append-only `LOG.md` growth (`:153-162`), scans only the appended
  suffix with non-hex token boundaries (`:171-181`), checks the erratum entry and the
  falsifier receipt (`:83-87`, `:109-135`). Also `check_r64…check_r69_routed_repairs*.py`
  in the same directory (siblings of the same pattern).

### 2d. kotodama — routed-resolution JSON lineage
- `kotodama-shokunin/reports/round-14/routed-resolution.json:6-12` — one `resolutions`
  entry per routed id: `id`, `disposition` (`applied-with-control` /
  `resolved-by-documentation`), `fixer`, `evidence`, `control`; `all_routed_from:
  reports/round-12/defects/routed.md` (`:5`). Same schema at `reports/round-22/routed-resolution.json:4-42`,
  `reports/round-30/routed-resolution.json`, plus later `closure-ledger.json` (r31),
  `completion-ledger.json` (r32), `ledger.json` (r73/r74). Longest-lived ledger practice in
  the fleet.

### 2e. Adjacent but not defect-disposition records (do not absorb)
- kagi `corpus/claim-ledger.tsv` (claims as commands, `:1-14`) — a *claim* ledger, not a
  route ledger.
- kama `registry/{claim-outcome,digest,hexrun,verdict}-ledger.tsv` — outcome/verdict ledgers.
- chousa `corpus/evidence/round25-final-ledger.log`, `round25-ledger-recount.log` — evidence
  logs, not records.
- mori `corpus/evidence/effective-disposition-r21.json:2-33` — disposition of *observations*
  (sensor/regression state), not routed defects.
- kake `scripts/ledger_latest_check.py:278-298` — checks the last declared ledger statement
  against receipts (a checker, not a routed-defect ledger).

---

## 3. Recurring-defect criteria

- Only structured criterion in the fleet: kengaku's `recurrence_of` field
  (`kengaku-shokunin/corpus/defects.jsonl:1`), linking a defect to a prior round's item.
- Prose recurrences: mori marks `D-a` as *"This is round 48's routed defect 2 again"* and
  *"recurring from round 48 defect 2"* (`mori-shokunin/corpus/lessons/round-49-verifier-spotcheck.md:24`, `:110`);
  kasegi marks `R5` as *"lane self-routed, carried"* (`kasegi-shokunin/corpus/lessons/round-38-verifier-spotcheck.md:175`);
  tameshi's own round-49 routed defect 5 is *"Carried round-48 items … still listed as
  carried, not landed"* (`tameshi-shokunin/corpus/lessons/round-49-verifier-spotcheck.md:126`).
- C1's own provenance is a recurring-defect tracker proposal (contract.json C1
  `routed_from`: considerthese proposal 3 "recurring-defect tracker", mined in round 49 as
  "a routed defect is not a closed defect").

---

## 4. What tameshi's ledger should adopt

1. **One row per routed id, with status + evidence + fix pointer** — the kengaku JSONL and
   kotodama JSON shapes; C1's schema (fixed/open/declined with evidence/commit/reason) is a
   stricter, checkable superset.
2. **Source digest pinning** — kagi pins the spot-check digest beside the record
   (`closure-dispositions.json:4`); C1 already freezes the statement set's sha256 in the
   counter (`measure.py:47`). Keep both.
3. **Machine-checked rows, not prose** — kengaku binds each row to a check
   (`defect_ledger.py:111`), kotoba builds a counter over the repairs; C1's counter
   re-derives each row from the tree. This is the right end-state.
4. **Status-neutral routing wording** — kaidoku's `"lane fixes next round; status-neutral"`
   heading; keep "routed ≠ closed" visible so a route never reads as a fix.
5. **Recurrence linkage** — add a `recurrence_of`-style field in future rounds (kengaku
   schema), so "recurring defect" stops being prose.

## 5. What C1 must not absorb

1. **Never cite spot-check files as evidence** — kengaku/kagi/kotodama records naturally
   point at the spot-check (`source`/`pointer` fields); C1's `measure.py:58-60` hard-blocks
   spot-checks, the ledger itself, `c1/`, `control/` and the contract/freeze. The ledger may
   *name* the spot-check as origin (like kengaku's `source`) but evidence excerpts must be
   tree files only.
2. **No extra statuses** — kagi's `reported/rejected/no-action/operator-owned`, kengaku's
   `blocked`, kotodama's `applied-with-control/resolved-by-documentation` would break C1's
   exactly-one-row `fixed/open/declined` mapping. Keep the three.
3. **No free-text "close" fields** — kengaku's `close` is prose; C1 requires a keyed excerpt
   absent at `routed_at` and present in a post-routing commit. Do not relax.
4. **No acknowledgment words on cited lines** — the counter bans `planned/carried/still
   open/not worked/stay open/remain open/routed to round/not fixed/unfixed/not landed`
   (`measure.py:54-55`); tameshi's own Planned paragraphs and routed items are full of these
   (e.g. `SCORECARD.md:2367` "not worked here", `round-49-verifier-spotcheck.md:126`
   "carried … not landed") — never cite lines that carry them.
5. **Nothing from `~/.local/state/` or the hidden C2 panel** — reading them voids the C2
   claim; the ledger must never point there.
6. **No log-line scanning** — kotoba's append-only `LOG.md` suffix technique depends on a
   volatile record (the cold-read monitor already excludes `LOG.md`); C1's tree-path evidence
   avoids that fragility.
7. **Don't absorb claim-ledgers** (kagi TSV, kama registry) — those record command/expect
   pairs, not defect dispositions; mixing them into `routed-defects.json` would entangle the
   two surfaces.

## Summary

- Fleet routing convention is uniform: closures write "Routed defects" under a numbered
  heading; canonical wording is `scripts/hyaku/closure-prompt.md:47`.
- Machine-checkable disposition records exist in kagi (closure-dispositions.py/json),
  kengaku (routed-findings.jsonl + defect_ledger.py), kotoba (check_r63_routed_repairs.py)
  and kotodama (routed-resolution.json lineage).
- Recurring-defect criterion exists in structured form only in kengaku (`recurrence_of`);
  everywhere else it is prose.
- C1's schema is stricter than every sibling record (keyed excerpt + commit + line-span
  constraints) — adopt source-digest pinning, row-level checks and status-neutral wording;
  keep the three statuses and the hard evidence bans.
- C1 must not absorb: spot-check citations as evidence, extra statuses, free-text closes,
  ACK-word lines, hidden-state/c2-panel references, log-scanning, or claim-ledger rows.
