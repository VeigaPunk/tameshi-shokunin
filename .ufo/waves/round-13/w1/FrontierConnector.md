# FrontierConnector — Round 13 Wave 1 Report

**Seat:** `TameshiR13.FrontierConnector` (UFO-FSD read-only connector, leaf member).  
**Baseline Commit:** `546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50`.  
**Lane Bounds:** Leaf member — no subagent dispatch, no git commits, no edits outside this designated report path, no test/build/gate execution, no verdict authority.  
**Tooling Record:** No tools installed or upgraded (zero changes to system or user toolchains).

---

## 1. Declared Axes & Restraint

Following the Godspeed pattern (*Name the axes; Iterate cheap, in parallel; Keep moves that improve any axis and harm none; Don't aim — let the frontier walk itself*):

- **Depth ($C_1$):** 6 → 6 (scalar unchanged).
  - *Improvement:* All six recorded mutation-ledger legs gain explicit content comparisons (pinned commit/digest vs. current HEAD commit/blob vs. working-tree sha256) and an explicit `result_reuse: not_established` disposition.
  - *Restraint:* Identical content is *not* result reuse. No new kill rate is measured, no target gate runs, and no seventh recorded gate is added (`tools/mutate-and-run.sh` recorded legs remain strictly 6).
- **Calibration ($C_2$):** 6 → 6 (scalar unchanged).
  - *Improvement:* Bounded companion metadata gate (`tools/witness-metadata.py`) repairs the producer key-path defect (`summary.json#/declaration/kind = null`) by projecting the frozen top-level kind verbatim without rewriting historical round-12 files.
  - *Restraint:* Zero promotion points claimed; SHONEN marks remain `[~]` (baseline 6); historical null preserved as immutable evidence.
- **Harm Check across other axes:**
  - *Operability:* Unchanged (historical runner `tools/mutate-and-run.sh` and witness tool `tools/bash-witness-study.py` untouched).
  - *Freshness:* Unchanged (stale-successor debts for tsukuroi and mado legs are explicitly documented as open debt, not discharged by content disposition).
  - *Coverage:* Unchanged (province boundaries remain intact; no unearned expansion into sibling domains).
  - *Adjacency:* Unchanged (sibling repositories inspected strictly via read-only git plumbing and sha256 hashing; zero sibling writes or executed sibling code).

---

## 2. Frontier F7 Connection: Bounded Method Acquisition vs. Execution Reuse

### 2.1 The Scope Boundary
Frontier Ground **F7** (`incremental re-sweep granularity`) addresses the progression from crude pin-level cadences toward granular, sound reuse decisions.

**Crucial Distinction:**
- **What Round 13 Achieves (Bounded Method Acquisition):** A machine-readable, content-level disposition method over all six recorded ledger legs (`tools/pin-disposition.py` + `.ufo/evidence/round-13/pin-manifest.json` + `corpus/knowledge/incremental-pin-disposition.md`). It formalizes the invariant that *content identity does not establish safe verdict reuse*, enforces `result_reuse: not_established` across all six legs, and accounts for external blind spots documented in upstream mutation literature.
- **What Round 13 Does NOT Achieve (Entire Incremental Execution Frontier Held):** It does *not* execute an incremental mutation testing run; it does *not* provide a cache of mutant kill verdicts; it does *not* inspect test-to-mutant coverage dependencies; and it does *not* discharge the outstanding stale-successor mutation re-sweeps. Therefore, F7 **cannot** be classified as fully `held`. It must be classified strictly as **partly held (round 13)** or as a bounded method step.

---

### 2.2 Frontier Surfaces: Before vs. After

| Surface | Before (Baseline `546b371`) | After (Round 13 w1 Landing) | Grounded Source / Evidence |
|---|---|---|---|
| **Frontier Registry** (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/README.md`) | Row F7 marked `open`. Next move declared: `pin-level cadence only → per-leg reuse decisions classified`. Candidate sources: `S003, S004, S005, S008, S041`. | F7 moves to **partly held (round 13)** in append-only correction block. Machine-readable six-leg disposition landed; explicit invariant `result_reuse: not_established` enforced. | `corpus/README.md` lines 84, 148–168; `.ufo/evidence/round-13/pin-dispositions.json`. |
| **Source Registry** (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`) | `S003` (StrykerJS incremental) & `S041` (PIT incremental) queued from 2026-10-19. S041 summarized loosely as "all but one reuse optimisations introduce potential error". | `S003` & `S041` re-opened/mined (2026-10-20 search log). Precision correction `S047` added: item 4 is prioritisation, item 5 unimplemented, class dependency assumption unproven. | `corpus/SOURCES.md` S003, S041, S047; fetched digests anchored in knowledge header. |
| **Knowledge Base** (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/`) | No dedicated entry for incremental reuse boundaries. Pre-round cadence treated pin matching purely as a trigger or hygiene check (`fleet-kill-rate-ledger.md` §ER-3). | Dedicated entry landed: `corpus/knowledge/incremental-pin-disposition.md`. Synthesizes S003, S041, S047, and S031; maps blind spots (env vars, dependencies, .snap files, runner test blindness). | `corpus/knowledge/incremental-pin-disposition.md` (280 lines, strict O/I/U labeling, verified-at/recheck headers). |
| **Tooling & Evidence** (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/` & `.ufo/evidence/`) | No stand-alone disposition tool. `mutate-and-run.sh` replayed pins at hardcoded revisions without recording current worktree vs HEAD drift. | Read-only probe `tools/pin-disposition.py` and canonical input `.ufo/evidence/round-13/pin-manifest.json` land; generates isolated-selftest-backed observations. | `tools/pin-disposition.py` (CLI + `--selftest`), `.ufo/evidence/round-13/pin-manifest.json`. |
| **Observed Leg State** (Six recorded legs) | Leg content vs pin drift unmeasured in machine-readable JSON. | Exactly 3 changed, 3 unchanged; all 6 carry `result_reuse: not_established`: <br>1. `js-kimi-census`: changed HEAD/worktree (`5e8d5913…` ≠ pin `83016d45…`).<br>2. `bash-surface-census`: unchanged content (`275d8294…`), commit moved.<br>3. `bash-tsukuroi-census`: changed HEAD/worktree (`d17d32a3…` ≠ pin `084951be…`).<br>4. `bash-mado-verify`: changed HEAD/worktree (`037b05dc…` ≠ pin `d7edaab4…`).<br>5. `bash-checklist-run`: unchanged content (`7e5ec98b…`), commit moved.<br>6. `js-claims-check`: unchanged content (`e9a21b44…`), commit moved. | `pin-manifest.json`; sibling reconnaissance reports (`SurfacePin.md`, `ChecklistPin.md`, `ClaimsPin.md`, `TsukuroiPin.md`, `MadoPin.md`). |

---

### 2.3 Synthesis of the S003 / S041 / S047 Blind Spots
Upstream literature firmly disproves the notion that identical target file bytes permit automatic reuse of mutation verdicts:
1. **StrykerJS (`S003`):** Explicitly documents that incremental detection misses updates to environment variables, dependencies, non-mutated sibling files, and snapshot (`.snap`) files. Furthermore, for command-based runners (`--selftest`), StrykerJS detects *nothing* about tests.
2. **PIT (`S041` / `S047`):** Explicitly documents that incremental optimizations introduce potential error, notes that class behavior is defined by its dependency graph (only super/outer classes are checked), and declares that the assumption of rare dependency-induced verdict flips is "currently unproven".
3. **Application to Tameshi Legs (`[INFERENCE]`):** In `bash-surface-census`, environment variables (`JANITOR`, `SQLITE3`) determine whether test cases run or skip. In `bash-checklist-run`, executable mode bits (not captured in raw sha256 bytes) determine whether the suite executes or aborts with exit 126. In `js-claims-check`, `process.execPath` and `TMPDIR` are external runtime dependencies.
4. **Conclusion:** Content hashing is strictly coarser than an execution reuse predicate. `result_reuse = "not_established"` is the only scientifically defensible status for a content disposition probe.

---

## 3. Grounded Integration Recommendations for L1 / Main

### 3.1 Recommended Update to `corpus/README.md`
Main should retain the historical `## Frontier` table row for auditability and update the status cell, linking to the append-only section:
```markdown
| F7 | incremental re-sweep granularity | S003, S004, S005, S008, S041, S047 | partly held (round 13) | pin-level cadence only → six-leg content disposition classified (`result_reuse: not_established`); execution re-sweeps remain debt |
```
And ensure lines 148–168 in the `## Round 13 — F7 content disposition and outside-review correction` block accurately cite:
- Knowledge artifact: `corpus/knowledge/incremental-pin-disposition.md`
- Evidence receipt: `.ufo/evidence/round-13/pin-dispositions.json`
- Explicit boundary: content disposition ≠ mutation re-sweep; stale successor debts remain open debt.

---

### 3.2 Recommended Entry for `SCORECARD.md`
Append the Round 13 entry to `SCORECARD.md` under `## Move log` or `## Round 13 — measured claims`:
```markdown
| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 13 | depth ($C_1$) | 6 recorded legs without structured content-drift classification | 6 recorded legs with machine-readable content disposition (3 changed, 3 unchanged) and explicit invariant `result_reuse: not_established` across all 6; disposition separated from re-sweep | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → exit 0, 6 legs; `.ufo/evidence/round-13/pin-dispositions.json`; scalar 6 held |
| 13 | calibration ($C_2$) | nested producer defect `declaration.kind = null` in round-12 summary without companion verification | companion metadata gate validates normalized kind against frozen top-level kind verbatim; anchors digests of 4 frozen inputs; preserves historical null; zero promotion points | `python3 tools/witness-metadata.py --check` → exit 0; `.ufo/evidence/round-13/witness-metadata.json`; scalar 6 held |
```
Under `## Capabilities`, record the bounded probe:
```markdown
| leg pin-disposition probe | observe worktree and HEAD content drift across six recorded mutation legs; enforce result_reuse=not_established invariant | `python3 tools/pin-disposition.py --selftest` → exit 0; `tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | round 13 |
| witness companion metadata gate | validate normalized kind and disclosure of frozen declaration without modifying frozen bytes; anchor SHA-256 chain | `python3 tools/witness-metadata.py --selftest` → exit 0; `python3 tools/witness-metadata.py --check` → exit 0 | round 13 |
```

---

### 3.3 Durable Named-Section Anchor Standard & QUALITY Criterion 14
In accordance with `corpus/lessons/round-12-verifier-spotcheck.md` Item 3 and learning from brittle citation shifts (`EvidenceConnector.md`):
1. **Eliminate Brittle Line Numbers:** Never cite `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:33-36` (which drifted to shell code). Cite durably:
   `scripts/hyaku/lane-addendum.md ## 6. Campaign addendum — hyaku` §2 `**Planner seat (orchestrator ruling 2026-10-19, kama/tsukuroi r11–12 L0 lines):**`.
2. **Adopt QUALITY Mistake Criterion 14:** Append to `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md`:
   > **14. A companion repair or metadata normalizer anchors the content digests of frozen input artifacts, reads verified top-level semantic declarations rather than unverified nested paths, preserves prior exposure and historical nulls as immutable fact, and checks digest integrity before evaluating schema consistency.**  
   > *(corpus/lessons/round-12-verifier-spotcheck.md ## Routed defects and residuals, Item 3; corpus/lessons/round-13.md ## Mistakes, metadata-path mistake)*

---

## 4. Risks, Traps & Counter-Measures

| Hazard | Risk Description | Counter-Measure |
|---|---|---|
| **Verbatim Overclaiming** | Claiming F7 is fully "held" based on content hashing alone. | Restrict status to "partly held (round 13)" or "bounded method acquisition". Document that multi-lane execution re-sweeps and dependency tracking remain unheld. |
| **Verdict Smuggling** | Treating `unchanged` content as proof that the mutant kill rate still holds. | Probe hardcodes `result_reuse: "not_established"` on all six rows. S003/S041/S047 cited to prove that unpinned environmental and dependency state can alter verdicts. |
| **Scalar Inflation ($C_1$)** | Counting the probe manifest or new gate as a 7th recorded mutation case. | Depth scalar stays strictly 6. The counting rule `recorded_cases` applies only to `tools/mutate-and-run.sh` ledger legs. No new legs added to the runner. |
| **Promotion Overreach ($C_2$)** | Claiming promotion credit or modifying SHONEN marks for fixing the metadata defect. | Calibration scalar stays strictly 6. The repair does not alter the historical cold-read scope; companion metadata is an honest error repair, not an independent review pass. |
| **Evidence Tampering** | Re-generating or editing `round-12/BashWitness/summary.json` to eliminate the null. | Frozen round-12 files remain byte-identical (verified by hard SHA-256 checks). The companion is an external, additive file in `.ufo/evidence/round-13/`. |
| **Citation Drift** | Re-introducing line numbers for host directives or knowledge entries. | Apply Criterion 14 and durable named-section headings across all round-13 documents. |

---

## 5. Exact Checks L1 Should Run (Not Executed by this Seat)

L1 should execute the following read-only verification commands in sequence:

```sh
# --- 1. Tool Syntax & Static Compilation ---
python3 -m py_compile \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/witness-metadata.py

# --- 2. Pin Disposition Probe: Isolated Selftest ---
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py --selftest
# Expect: exit 0, literal PASS on isolated fixture arms (unchanged, changed HEAD, dirty, missing, malformed)

# --- 3. Pin Disposition Probe: Live Fleet Run ---
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py \
  --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json \
  --root /home/vgpnk/Projects/shokunin
# Expect: exit 0; exactly 6 legs; 3 changed, 3 unchanged; every row result_reuse == "not_established"

# --- 4. Companion Metadata Gate: Isolated Selftest ---
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/witness-metadata.py --selftest
# Expect: exit 0, literal PASS across fixture arms (old null red, corrected green, tamper exit 2, wrong kind exit 1)

# --- 5. Companion Metadata Gate: Live Validation ---
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/witness-metadata.py --check
# Expect: exit 0 (metadata_consistent)

# --- 6. Frozen Round-12 Evidence Byte Preservation ---
git diff --quiet 546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50 -- \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12 \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/bash-witness-study.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
# Expect: exit 0 (zero diff)

# --- 7. Frozen Input Digest Chain Integrity ---
sha256sum \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/BashWitness/summary.json \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/BashWitness/declaration.json \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/BashWitness/declared.tsv \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/BashWitness/manifest.json
# Expect:
# acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9  summary.json
# e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901  declaration.json
# 0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3  declared.tsv
# 273ffc39308a6c55bdb1c8f7a86bac9f95886ec470773c99b4d1e2db5b25e1cf  manifest.json

# --- 8. Knowledge Provenance Headers & Source Registry Census ---
head -n 5 /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md
# Expect: source:, verified-at: 2026-10-20, recheck: 90d, ground: F7

bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/kaika-round-1/sources-census-v2.sh
# Expect: exit 0, SOURCES_CENSUS: CLEAN

# --- 9. Durable Named-Section Anchor Audit ---
! grep -n "lane-addendum.md:33-36" \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/LOG.md \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-13.md
# Expect: clean (no matches)
```
