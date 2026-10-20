# EvidenceConnector — Round 13 Wave 1 Report

**Seat:** `TameshiR13.EvidenceConnector` (read-only connector, leaf).  
**Baseline:** `546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50`.  
**Scope:** Read-only connection across companion metadata repair, QUALITY mistake criteria, and the host planner ruling; flagging brittle line numbers and providing grounded integration recommendations without claiming verdict authority.  
**Tooling Record:** No tools installed or upgraded (zero changes to system or user toolchains).

---

## 1. Declared Axes

- **depth:** 6 → 6 (bounded technical detail; durable named-section citations eliminate citation drift; no seventh recorded gate claimed).
- **calibration:** 6 → 6 (honest self-assessment; companion metadata repairs nested producer defect without altering frozen evidence or claiming promotion points; prior exposure preserved verbatim).
- **Harm check across other axes:**
  - *operability:* Unchanged; existing runner `tools/mutate-and-run.sh` and historical probe `tools/bash-witness-study.py` untouched.
  - *freshness:* Unchanged; stale successor debts documented, not hidden.
  - *coverage:* Unchanged; no province boundary expansion.
  - *adjacency:* Unchanged; read-only probes into siblings, no sibling gate code executed or absorbed.

---

## 2. Evidence: The Three Converging Surfaces

### Surface A: Historical Host Planner Ruling and Line Drift
- **Observed Drift:** In round 12, `LOG.md:659` and `corpus/lessons/round-12.md:62` cited `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:33-36` for the host planner ruling. In the current file, lines 33–36 contain the shell invocation block (`cd {{LANE_CWD}} && UFO_CONFIG_PATH=... node ...`). The actual planner ruling paragraph currently resides at lines 42–46. Other seats previously cited `:41-44` or `:33-44` (`w2/AdmissionCritic.md:37`, `w2/LessonEvidence.md:45`).
- **External Ruling:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-12-verifier-spotcheck.md` `## Routed defects and residuals` Item 3 explicitly mandates:
  > *"replace brittle host-addendum line citations with the named planner-ruling section in an append-only correction; the document's lines moved."*
- **Durable Anchor:** File `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md`, named section `## 6. Campaign addendum — hyaku (百), operator directives of 2026-10-19 (binding this round; in-session)`, Subsection 2 `Swarm waves: 32–64 lanes per wave`, paragraph `**Planner seat (orchestrator ruling 2026-10-19, kama/tsukuroi r11–12 L0 lines):**`.

### Surface B: New Companion Metadata Correction (C2 Calibration)
- **Root Producer Defect:** In `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/bash-witness-study.py:787`, `build_summary` queries `"kind": declaration.get("declared", {}).get("kind")`. The writer at `:875` wrote `kind` to the top level of `declaration.json`, while `:877-882` constructed the nested `declared` sub-object without a `kind` key. As a result, `.get()` returned `None`, emitting `"kind": null` in `summary.json:15`.
- **Frozen Invariant Boundary:** 
  - `declaration.json` line 6 top-level: `"kind": "declared-witness mapping (not a blind preregistration)"`.
  - `declaration.json` line 7 top-level `disclosure`: `"declared-witness mapping, not a blind preregistration: before declaring, the author had seen recorded aggregate outcomes of this leg …"`.
  - SHA-256 of frozen `summary.json`: `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9`.
  - SHA-256 of frozen `declaration.json`: `e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901`.
  - SHA-256 of frozen `declared.tsv`: `0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3`.
- **Companion Contract:** The repair cannot modify frozen round-12 artifacts. The new companion metadata file (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/witness-metadata.json`) anchors the frozen input digests, notes the observed historical nested `null`, and derives the normalized kind from the top-level declaration string verbatim.

### Surface C: QUALITY Mistake Criteria and Brittle Line Number Blockers
- **Historical Freeze Caused by Line Numbers:** In `corpus/README.md ## Known gaps` (lines 91–96), adding provenance headers (`source:`, `verified-at:`, `recheck:`) to 19 pre-round knowledge entries was deferred as permanent debt specifically because:
  > *"Prepending would shift every path:line cite into them; left as named debt, route is an operator call."*
- Similarly, `PROVINCE.md:24` notes: *"lines 1-20 above are unchanged (they are cited by line across the lane)."*
- **Section Citations in QUALITY:** In `corpus/QUALITY.md`, Criteria 11–13 already use durable named-section / mistake-class citations:
  - Criterion 11: `(lessons/round-12.md, vacuous mistake)`
  - Criterion 12: `(lessons/round-12.md, attribution mistake)`
  - Criterion 13: `(lessons/round-1-verifier-spotcheck.md, Adjudication; lessons/round-12.md, attribution mistake)`
- While QUALITY Criterion 2 originally listed `path:line` as an allowable anchor, real fleet usage demonstrates that line-number anchors decay on document appends.

---

## 3. Flagged Brittle Line Numbers Across Active Surfaces

The table below catalogs brittle line-number citations identified in active records and provides their durable named-section replacements:

| File Containing Citation | Brittle Line Citation | Target File | What Drifted / Hazard | Durable Named-Section Replacement |
|---|---|---|---|---|
| `LOG.md:659` & `corpus/lessons/round-12.md:62` | `scripts/hyaku/lane-addendum.md:33-36` | `scripts/hyaku/lane-addendum.md` | Lines 33–36 shifted to shell command; planner ruling moved to lines 42–46 | `scripts/hyaku/lane-addendum.md` `## 6. Campaign addendum — hyaku` §2 `**Planner seat (orchestrator ruling 2026-10-19, kama/tsukuroi r11–12 L0 lines):**` |
| `w2/AdmissionCritic.md:37,130` & `w2/LessonEvidence.md:45,80` | `scripts/hyaku/lane-addendum.md:41-44` | `scripts/hyaku/lane-addendum.md` | Shifts whenever earlier directives or examples in §2 change | `scripts/hyaku/lane-addendum.md` `## 6. Campaign addendum — hyaku` §2 `**Planner seat**` |
| `PROVINCE.md:24` | `PROVINCE.md:1-20` | `PROVINCE.md` | Line range freezes header against edits; breaks if lines inserted | `PROVINCE.md ## Domain / ## Owns / ## Refuses` |
| `PROVINCE.md:34` | `tools/mutate-and-run.sh:84-89` | `tools/mutate-and-run.sh` | Brittle to changes in script comment header | `tools/mutate-and-run.sh` header `# Six recorded mutation legs` (table `RECORDED_LEGS`) |
| `corpus/QUALITY.md:45` & `SCORECARD.md:322` | `corpus/lessons/round-1-verifier-spotcheck.md:17` | `corpus/lessons/round-1-verifier-spotcheck.md` | Cites line 17 of spotcheck report; vulnerable to report edits | `corpus/lessons/round-1-verifier-spotcheck.md ## Adjudication` |
| `corpus/lessons/round-12.md:187` | `summary.json:15` | `.ufo/evidence/round-12/BashWitness/summary.json` | Cites line 15 of JSON | `.ufo/evidence/round-12/BashWitness/summary.json` `declaration.kind` |
| `corpus/README.md:91-96` | `corpus/knowledge/*.md:line` | `corpus/knowledge/*.md` | Prepending headers blocked by line-number citations across repo | Replace with named section headings `## <Heading>` within each knowledge note |

---

## 4. The Proposed Move: A Unified Durable Citation & Companion-Anchor Contract

Synthesizing findings across `MetadataSchema`, `MetadataIntegrity`, `MetadataSelftest`, `MistakeDataWalk`, `ScoreRestraint`, and `SourceScribe`, the proposed move connects the three surfaces into one coherent integration pattern:

### 1. Durable Citation Hierarchy Standard
All round-13 documents (lesson, LOG, reports, scorecard notes) MUST use durable semantic anchors instead of line numbers:
- Markdown files: `path/to/file.md ## Section / ### Subsection` or `path/to/file.md **Heading/Term**`.
- Source code / scripts: `path/to/file.py symbol_or_function_name` or `file.sh` header section title.
- Structured JSON: `path/to/file.json json.path.to.key`.

### 2. Candidate QUALITY Mistake Criterion 14
In accordance with `round-12-verifier-spotcheck.md` Item 3 and learning from the `declaration.kind=null` producer defect, L1 should append Criterion 14 to `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md`:
> **14. A companion repair or metadata normalizer anchors the content digests of frozen input artifacts, reads verified top-level semantic declarations rather than unverified nested paths, preserves prior exposure and historical nulls as immutable fact, and checks digest integrity before evaluating schema consistency.**  
> *(corpus/lessons/round-12-verifier-spotcheck.md ## Routed defects and residuals, Item 3; corpus/lessons/round-13.md ## Mistakes, metadata-path mistake)*

### 3. Strict 3-Tier Companion Metadata Contract
For `tools/witness-metadata.py` and `.ufo/evidence/round-13/witness-metadata.json`:
1. **Tier 1 — Integrity before Evaluation:** Compute SHA-256 of `summary.json`, `declaration.json`, `declared.tsv`, and `manifest.json`. Mismatch or unreadable file yields exit 2 (`snapshot_tampered` or `input_unavailable`).
2. **Tier 2 — Verbatim Semantic Projection:** Extract normalized kind strictly from `declaration.json` top-level `kind`. Verify that it equals byte-for-byte `"declared-witness mapping (not a blind preregistration)"`. Verify that top-level `disclosure` is non-empty and matches the frozen disclosure text. Never substitute a shortened token (`declared-witness-mapping`) or a blind label (`blind preregistration`).
3. **Tier 3 — Historical Null Preservation:** Retain `"historical_nested_kind": null` as an observed fact. The companion must succeed (exit 0 `metadata_consistent`), while evaluating the uncorrected old null or a tampered file must fail (exit 1 or exit 2).

---

## 5. Risks and Counter-Measures

1. **Risk: Vocabulary laundering / upgrading toward "blind".**  
   *Hazard:* A normalizer could truncate the string or omit `"not a blind preregistration"`, misleading readers into thinking the witness was blind.  
   *Counter-measure:* Assert exact byte equality with `declaration.json:6`. Any omission of the negative parenthetical must fail the check.
2. **Risk: Rewriting frozen round-12 files.**  
   *Hazard:* Attempting to fix `tools/bash-witness-study.py` or re-generate `summary.json` would alter git-pinned evidence.  
   *Counter-measure:* Hard gate in L1 check: `git diff --quiet 546b371 -- .ufo/evidence/round-12 tools/bash-witness-study.py` must return 0.
3. **Risk: Line number re-introduction in round-13 LOG and lesson.**  
   *Hazard:* The integrator might copy-paste line citations from round-12 drafts.  
   *Counter-measure:* L1 audit check verifying that the host planner ruling citation uses `scripts/hyaku/lane-addendum.md ## 6. Campaign addendum` §2 `**Planner seat**`.

---

## 6. Exact Checks L1 Should Run (Not Executed by this Seat)

L1 should execute the following checks during integrated verification:

```sh
# 1. Verify frozen round-12 evidence remains completely untouched
git diff --quiet 546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50 -- \
  .ufo/evidence/round-12 tools/bash-witness-study.py tools/mutate-and-run.sh

# 2. Verify frozen input digests match literal expectations exactly
sha256sum \
  .ufo/evidence/round-12/BashWitness/summary.json \
  .ufo/evidence/round-12/BashWitness/declaration.json \
  .ufo/evidence/round-12/BashWitness/declared.tsv

# 3. Verify that the new metadata companion tool selftest passes with literal tokens
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/witness-metadata.py --selftest

# 4. Verify companion check succeeds against the live companion
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/witness-metadata.py --check

# 5. Negative check: verify that evaluating the uncorrected summary.json produces exit 1
# (or verify through isolated selftest case 'old_null')

# 6. Verify durable named-section citation for host planner ruling in LOG.md and round-13 lesson
grep -F "Planner seat (orchestrator ruling 2026-10-19" \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/LOG.md \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-13.md

# 7. Confirm no brittle 'lane-addendum.md:33-36' citation introduced in new round-13 text
! grep -n "lane-addendum.md:33-36" \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/claims.json \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-13.md
```
