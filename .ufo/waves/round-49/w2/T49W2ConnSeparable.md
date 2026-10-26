# T49W2ConnSeparable — Causal separability, C1 vs C2 @ f181a961ae44061af486f600e5ea257d2baf78f8

Seat: T49W2ConnSeparable (wave 2, falsify). Axes: calibration (C1), coverage (C2).
Scope: list every path C1's evidence depends on and every path C2's depends on; build both
reverted trees in scratch; compare hashes of each counter's inputs. No counter run here is a
verdict; the deciding run is the L1's.

## 1. Method

1. Read `round-49/contract.json` (C1/C2 clauses) and both frozen counters
   (`.ufo/evidence/round-49/c1/measure.py`, `c2/measure.py`).
2. `git -C <lane> diff --name-status 8ca67421111fa354b47b803358391d0b07fc6db9 f181a961ae44061af486f600e5ea257d2baf78f8`
   → integration diff (461 files; the non-wave-1 content paths are listed in §2).
3. Verified the counters at the candidate are the frozen bytes:
   `sha256(git cat-file blob f181a96:<counter>)` = freeze.json digest (c1 `a055e929…`, c2 `f4971d02…`).
4. Built three trees in scratch `S=/fast/scratch/hyaku/tameshi-r49/T49W2ConnSeparable` by
   `git archive` of the candidate + file restores from base:
   - `tree-cand` = candidate f181a96;
   - `tree-r2` = candidate with C2's paths reverted to base (`tools/pbt-staged-id.py` removed,
     `corpus/knowledge/pbt-generator-pilot.md` removed, `corpus/SOURCES.md` and
     `corpus/README.md` restored to base bytes);
   - `tree-r1` = candidate with C1's paths reverted to base (`SKILL.md` and
     `.ufo/evidence/round-21/coldread/ledger.json` restored to base;
     `.ufo/evidence/round-49/coldread/` and `c1/{reads,corrections,l1-rows,readers}.json`
     and `c1/{apply-corrections,merge-reads,refresh}.py` removed; frozen counter files kept).
   Same trees committed in a `git clone --shared` scratch clone as `r2-revert`
   (`4f72efbe5cff3c33dd472e7b3117204abe62e025`) and `r1-revert`
   (`d476537af2b6423ebd1b3c09fc15bf1c7189ec9a`) — `git -C $S/clone rev-parse --show-toplevel`
   asserted before each commit.
5. Compared sha256 of every path in each counter's input set across trees (§3), plus the frozen
   C1 extractor's pointer list at the candidate vs the C2-reverted commit
   (`python3 .ufo/evidence/round-49/c1/measure.py --lane $S/clone --rev 4f72efb… --list`).
   Receipts: `T49W2ConnSeparable.input-hashes.txt` (comparisons A/B),
   `T49W2ConnSeparable.regions.txt` (shared-file region identity),
   `T49W2ConnSeparable.pointers-at-C2-revert.json` (pointer list at r2-revert).

## 2. Dependency paths

### C1's evidence depends on (contract C1 clause + `c1/measure.py` + integration diff)
Frozen contract/counters (identical at base-freeze and candidate):
- `.ufo/evidence/round-49/contract.json`, `c1/measure.py` (frozen sha `a055e929…`),
  `control/c1-pointers-at-base-8ca67421.json`, `control/monitor-at-base-8ca67421.json`,
  `control/c1-controls.py`, `deciding-run.sh`.
- `.ufo/evidence/round-21/coldread/measure.py` (pinned sha `657f009b…`) and
  `.ufo/evidence/round-18/measure.py` (pinned sha `7ca87a7c…`) — the unchanged monitor + credit
  algorithm; verified live (at the lane path) and as blobs at REV.
C1 deliverables (added/modified by the integration at f181a96):
- `SKILL.md` — the seven TARGET sections (heading text frozen; bodies corrected).
- `.ufo/evidence/round-49/c1/reads.json` (94 rows) — the row-per-pointer reads evidence.
- `.ufo/evidence/round-49/coldread/refresh-receipts.json` + `traces/section-{1..7}.json`
  (trace-bound inputs, `tameshi-trace-inputs-v1`).
- `.ufo/evidence/round-21/coldread/ledger.json` — seven re-key entries appended (record class,
  `verified-record`), keyed by section sha256 + non-record input shas.
- Integration helpers (provenance, not counter-read): `c1/{apply-corrections.py,corrections.json,
  l1-rows.json,merge-reads.py,readers.json,refresh.py}`.
Counter-read inputs at REV (from `c1/measure.py` `measure()`/`check_reads()`/`target_sections()`):
- `SKILL.md`; `.ufo/evidence/round-49/c1/reads.json`; the monitor/ledger/traces above.
- Pointer targets (94 pointers at candidate; all lane blobs + external `../PROTOCOL.md` via the
  row's `fleet_commit` from the fleet repo): `corpus/SOURCES.md` (7 S-id rows, lines 14,15,37,50,
  56,58), `corpus/README.md` (3 path pointers), `LOG.md` (2), `SCORECARD.md` (3), `SKILL.md`
  (3), `SHONEN.md` (1), and 31 C1-domain files
  (`corpus/knowledge/*`, `corpus/lessons/round-1.md`, `tools/*`, `plans/*`, `reports/round-1-
  calibration.md`, `round-12/13/14 evidence json/py`); 3 unresolvable path pointers
  (`mutate_driver.py`, `plans/round-N.plan.md`, `plans/round-N-record-draft.md`) read as `absent`.
- The five VOLATILE records (`LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
  `corpus/README.md`) — at REV (blobs for the durability probe append) and the monitor's record
  blobs pinned at each entry's `read_rev`.

### C2's evidence depends on (contract C2 clause + `c2/measure.py` + integration diff)
Frozen contract/counters:
- `contract.json`, `c2/measure.py` (frozen sha `f4971d02…`), `control/c2-controls.sh`,
  `control/c2-fixed-gen.py`, `control/c2-fixed-fixtures.json`, `control/c2-CTL_ABSENT.stdout`,
  `control/c2-CTL_FIX.stdout`, `control/c2-WITNESS.stdout`, `deciding-run.sh`.
- `tools/staged-id-guard.py` (pinned sha `03a796c5…`; round-43 capability, never edited).
- The hidden panel `.ufo/evidence/round-49/c2/panel.json` (sha `d6dd2cf3…`, committed at reveal;
  not present at the candidate; not read here).
C2 deliverables (added/modified by the integration at f181a96):
- `tools/pbt-staged-id.py` (generator, stdlib-only, self-contained).
- `corpus/knowledge/pbt-generator-pilot.md` (pilot entry; leading block cites `source: S269`,
  `source: S270`).
- `corpus/SOURCES.md` — rows S269/S270 appended after line 141, plus three tail notes
  (round-48/49 + next-unused-id) at the `## Paths` end.
- `corpus/README.md` — F10 block appended at the tail (`## Round 49 — the F10 pilot…` and the
  `F10 … open → **held (round 49)**` line).
Counter-read inputs at REV (from `c2/measure.py` `materialize()`/`records()`):
- `tools/staged-id-guard.py`, `tools/pbt-staged-id.py`, `corpus/knowledge/pbt-generator-pilot.md`,
  `corpus/SOURCES.md`, `corpus/README.md`, the panel file (external argument).

## 3. Hash comparisons

### A. C1 counter inputs: candidate vs C2-reverted (tree-r2)
58 input path-instances compared (`T49W2ConnSeparable.input-hashes.txt`): **56 MATCH**; the only
DIFFs are the two shared files `corpus/SOURCES.md` and `corpus/README.md` (each twice — once as a
VOLATILE record, once as a pointer target). Those two files are exactly where C2's deliverables live.
Decision-relevant identity inside the two shared files (`T49W2ConnSeparable.regions.txt`):
- `corpus/SOURCES.md`: 491 → 496 lines; **first 141 lines identical**; every cited S-id row
  (14, 15, 37, 50, 56, 58) byte-identical. C2's rows (S269/S270) and tail notes are appended
  strictly after all rows C1 cites, so C1's S-id resolutions and ranges are unchanged.
- `corpus/README.md`: candidate bytes start with the r2 (base) bytes (append-only); all three
  `reads.json` README path-pointer excerpts occur in both versions.
- Dynamic confirmation: the frozen C1 extractor's pointer list at `r2-revert`
  (`4f72efbe…`) is byte-identical to the candidate's list (JSON equal after dropping the `rev`
  field) — same headings, ordinals, raws, resolved files, and ranges.

### B. C2 counter inputs: candidate vs C1-reverted (tree-r1)
All 6 input paths MATCH byte-for-byte: `tools/staged-id-guard.py`, `tools/pbt-staged-id.py`,
`corpus/knowledge/pbt-generator-pilot.md`, `corpus/SOURCES.md`, `corpus/README.md`, and the frozen
`c2/measure.py`. C1's corrections and re-key ledger entries touch none of C2's counter inputs.

## 4. Findings

- **F1. The claims share exactly two files**, both read by C1's counter and both carrying C2's
  deliverables: `corpus/SOURCES.md` (C1: S-id rows; C2: rows S269/S270 + tail notes) and
  `corpus/README.md` (C1: path pointers + VOLATILE record; C2: F10 block). No other C2 path is
  read by C1's counter (0 of 94 pointers resolve into `tools/pbt-staged-id.py` or
  `corpus/knowledge/pbt-generator-pilot.md`), and no C1 path is read by C2's counter.
- **F2. C2 is causally separable from C1 in the strict byte sense**: reverting every C1 path
  leaves all of C2's counter inputs byte-identical (comparison B, 6/6 MATCH).
- **F3. C1 is causally separable from C2 in the decision-relevant sense**: reverting C2's paths
  changes C1's counter inputs only in the two shared files, and only in regions C1 does not
  consume — C2's edits are pure appends past C1's cited rows/line ranges, the cited rows and
  excerpt regions are byte-identical, and the counter's derived pointer list is unchanged.
- **F4. Strict whole-file byte-identity fails in the A direction for the two shared files only**
  (2 of 58 input path-instances). This is expected and benign: the reverted bytes are C2's own
  deliverables (the generator, entry, rows, and F10 line live in or beside those files), and C1's
  predicate does not read them at the appended positions. Observable, not a violation: C1's
  counter inputs are not byte-identical across the C2 revert as whole files, but every byte C1's
  counter actually resolves/verifies is identical.
- **F5. No pointer in the seven corrected SKILL.md sections resolves into a C2 file**, and the
  trace-bound inputs of the seven re-key ledger entries (section-1..7 traces) contain no C2 path
  (`tools/pbt-staged-id.py`, `corpus/knowledge/pbt-generator-pilot.md`, `corpus/README.md` appear
  only as a record in section-1's argv, read through git blobs at `read_rev`). The counter
  shas at the candidate equal the freeze digests, so the freeze→candidate transition did not
  rewrite either counter.
- **F6. Stability of the measurement itself**: the 90→94 pointer count change between base and
  candidate is entirely within C1's corrected sections (C1's own fix work); candidate and
  C2-reverted lists are identical, so C2's revert does not alter the extraction.

## 5. Risks / notes

- The `../PROTOCOL.md` external pointer resolves through the fleet repo at the row's
  `fleet_commit`; both trees are lane-content-only, so this path is untouched by either revert.
- The durability probe appends `PROBE_LINE` to the five VOLATILE records at REV; record content
  is read through git blobs pinned at each entry's `read_rev`, so appended record content (C2's
  included) cannot lapse the monitor credit — consistent with the contract's volatile-record
  design.
- No tools installed (none needed); no files outside the item's deliverables and scratch were
  written. The two IRC heads-ups received this session concern a round-46 v2 counter (sandbox
  F1/F2), not round-49; out of scope here.

## Summary
- C1 input set: 58 paths (frozen counters/monitor, SKILL.md, reads.json, ledger+traces, 94 pointer
  targets incl. 5 volatile records, fleet external). C2 input set: 6 paths (guard, generator,
  entry, SOURCES.md, README.md, counter).
- Revert C1 → C2 inputs: 6/6 byte-identical (strict separability).
- Revert C2 → C1 inputs: 56/58 byte-identical; the only DIFFs are corpus/SOURCES.md and
  corpus/README.md (the two shared files), whose regions C1 consumes (S-id rows 14/15/37/50/56/58,
  README excerpts, pointer list) are byte-identical.
- Decision-relevant causal separability HOLDS both ways; strict whole-file identity holds one way
  and fails only on C2's own appended bytes in the shared files the other way.
- No pointer/trace of C1 touches a C2 path; no C2 counter input is touched by C1's integration.
- Verdicts left to the L1's deciding run; nothing here is a verdict.
