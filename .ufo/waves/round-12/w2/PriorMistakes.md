# PriorMistakes — Round 1 Outside Spot-Check & Round 12 Defect Routing

**Seat:** `TameshiR12.PriorMistakes` (leaf scout).  
**Role & Posture:** Godspeed scout; read-only analysis; advisory only. No independent non-author admission, promotion, or verification authority claimed.  
**Write Scope:** `tameshi-shokunin/.ufo/waves/round-12/w2/PriorMistakes.md` only. No inherited historical rewrites; no shared production file edits.  
**Tool Installations / Updates:** None. Standard system utilities used.

---

## 1. Axes Named

- **Depth:** Count of independently recorded mutation cases in the pinned replay ledger (`tools/mutate-and-run.sh:84-89`; `SCORECARD.md:66,72-73`). Value at baseline and round start: **6**.
- **Calibration:** 2 points per correctly restrained, durable-evidence-linked `[~]` mark in `SHONEN.md`, capped at 8, with the last 2 reserved for independent promotion review (`SCORECARD.md:67,74-75`). Value at baseline and round start: **pinned 6** (boxes 1, 2, 4 restrained `[~]` × 2 = 6; box 3 excluded per outside adjudication).

---

## 2. Round 1 Outside Spot-Check Analysis

The normative outside spot-check from fleet round 1 is anchored in:
- `corpus/lessons/round-1-verifier-spotcheck.md:1-18` (written by the integrator/orchestrator, not the lane; reporting on verifier `W3ReviewTameshi` at commit `a21e910`)
- Supporting fleet external reviews: `.ufo/waves/kaika-w3/tameshi-review.md:1-172` (Reviewer) and `.ufo/waves/kaika-w3/tameshi-critic.md:1-30` (Critic)
- Lane append-only reflections: `corpus/lessons/round-1.md:474-490`, `LOG.md:633-644`, and `SCORECARD.md:204-235`

### 2.1 Adjudication & Disagreements

1. **Disagreement D1 — K1 Calibration / Box-3 Increment Rejected:**
   - *Observation & Evidence:* The lane initially claimed candidate calibration 8 by advancing Box 3 from `[ ]` to `[~]` based on a cold-read report (`corpus/lessons/round-1.md:325-330`). The Critic rejected K1 as measured (`.ufo/waves/kaika-w3/tameshi-critic.md:7-11`): the cold-read covered only Appendix A + B; Appendix B survivor-probe fixtures were reconstructed from gate contracts rather than following page-defined commands; and substantial sections (`SKILL.md:466-525`, including the no-permissiveness audit recipe and fail-closed taxonomy) were unexercised. The orchestrator adjudicated K1 as rejected, re-pinning calibration at 6 without box 3 (`corpus/lessons/round-1-verifier-spotcheck.md:17`; `LOG.md:635-638`; `SCORECARD.md:209-220`).
   - *Carried Debt:* `round-1-verifier-spotcheck.md:17` records: *"Debts: box 3 needs a fresh reader to run the full page-defined procedure; 19 legacy entries lack provenance headers (L0: migration approach)."*
   - *Round 12 Relevancy & Status:* **Unresolved debt.** Neither C1 nor C2 conducts a whole-skill fresh cold-read. Box 3 remains restrained `[~]` with an explicit scope note (`SHONEN.md:9-10`) and scores 0 points in `.ufo/evidence/round-12/measure.py:30-31`.
   - *Criterion Needed:* Grounded in ER-K7 (`corpus/lessons/round-1.md:462-470`) and MK-10: *A mark's evidence must cover the mark's whole wording, or the mark does not score.*

2. **Disagreement D2 — Discernment Token Conflict (`improved` vs `unprovable-but-better`):**
   - *Observation & Evidence:* `corpus/lessons/round-1-verifier-spotcheck.md:17` records trend *"discernment improved"* based on the spot-check agreeing on one admit and one reject sample. However, `SCORECARD.md:118,234`, `LOG.md:463`, and `corpus/lessons/round-1.md:208-212` (ER-I1) committed the canonical token as **`unprovable-but-better`**, noting that lane-dispatched seats cannot supply outside authority. `SCORECARD.md:234` left discernment to *"the orchestrator's adjudication"* without reconciling the two terms.
   - *Round 12 Relevancy & Status:* **Unresolved defect / unreconciled tokens** (Candidate MK-12 in `.ufo/evidence/round-12/LessonScribe/outline.md:54`).
   - *Criterion Needed:* *Discernment trend tokens must cite a specific non-author sample of ≥1 admit and ≥1 reject; multiple tokens in circulation must be reconciled via append-only errata.*

3. **Disagreement D3 — Calibration Score Pin Discrepancy (6 vs 8):**
   - *Observation & Evidence:* Reviewer recommended pinning 8 (`.ufo/waves/kaika-w3/tameshi-review.md:16`), lane candidate was 8 (`LOG.md:611`), but orchestrator adjudicated 6 (`corpus/lessons/round-1-verifier-spotcheck.md:17`; `LOG.md:635-638`).
   - *Round 12 Relevancy & Status:* **Resolved by pin; lingering citing risk.** Pinned at 6 across all Round 12 baselines (`claims.json:6`, `before-with-score-exclusions.json`, `corpus/lessons/round-12.md:3`). Candidate MK-14 cautions against citing the unadjudicated candidate 8.

4. **Methodological Defect — Spot-Check Sample Excluded Contested Admit:**
   - *Observation & Evidence:* `corpus/lessons/round-1-verifier-spotcheck.md:10-13` sampled K2 admit and S046/S029 rejects. Both verifiers agreed on those items. The spot-check sample excluded the contested admit K1 (Box 3), on which the Critic explicitly disagreed (`.ufo/waves/kaika-w3/tameshi-critic.md:11`).
   - *Round 12 Relevancy & Status:* **Unresolved sampling limitation** (Candidate MK-13 in `outline.md:55`).
   - *Criterion Needed:* *A non-author spot-check sample must include at least one item on which outside reviewers/critics disagree, when a disagreement exists.*

### 2.2 Defects Routed from Non-Author Review

From `.ufo/waves/kaika-w3/tameshi-review.md:125-148`:
1. **Defect M1 — Fleet-Census `validate` TZ-dependence (Outside the Lane):**
   - *Evidence:* `tameshi-review.md:68,128`. `sources-census.sh` compared local `date -d` against UTC `today_s`, emitting false `E08` errors on negative-offset hosts.
   - *Status:* **Resolved in fleet script** (`scripts/sources-census.sh:49-63,583-586` now uses gawk `iso_epoch()` with UTC epoch math). Round 12 records observed UTC date 2026-10-20 rather than local calendar dates (`corpus/lessons/round-12.md:7`).
2. **Defect M2 — `quality: improved` Self-Verdict Unsupported:**
   - *Evidence:* `tameshi-review.md:122,129`. No pre-round entry was re-verified, deepened, or superseded.
   - *Status:* **Resolved in post-review.** Quality trend corrected to `unchanged` (`SCORECARD.md:233-234`; `LOG.md:641-642`).
3. **Defect M3 — Frontier Status `held` Overstated:**
   - *Evidence:* `tameshi-review.md:130`. F1/F2 were held for a single pinned leg, not general coverage.
   - *Status:* **Resolved in post-review.** F1 and F2 relabelled `partly held` (`corpus/README.md:78-79`; `SCORECARD.md:209-220`).
4. **Defect L4 — `SKILL.md` Stale Status Sentences (`:14-15`, `:133-135`):**
   - *Evidence:* `tameshi-review.md:136`; `corpus/lessons/round-1.md:442-449` (ER-K5); `corpus/README.md:91-95`. Status sentences claiming Appendix A/B unverified became stale after the cold-read.
   - *Status:* **Unresolved debt.** Intentionally left unedited in `SKILL.md` to prevent modifying the byte hash `33e3009c...` that anchors Box 3.
5. **Defect L5 — Box-3 Text Broader than Evidence:**
   - *Evidence:* `tameshi-review.md:137`. Same as Disagreement D1. Unresolved debt; bound by scope qualifier in `SHONEN.md:9-10`.
6. **Defect L6 — `ground:` Header Pointers External Worktree Dependency:**
   - *Evidence:* `tameshi-review.md:138`. Knowledge headers cite `tameshi-art.md §4`, which resolves only in fleet worktrees.
   - *Status:* **Carried observation.** Present in `corpus/knowledge/witness-scoped-kill-verdict.md:4` and `repeated-control-precondition.md:4`.
7. **Defect L9 — Inconsistent Rejection Reasons (Popularity vs Method):**
   - *Evidence:* `tameshi-review.md:145`. S029 rejected citing "0 stars", while admitted S006 was also 0 stars.
   - *Status:* **Resolved in practice.** Round 12 rejections cite operational contract semantics and lack of per-row verdict contracts, not star or commit counts (`corpus/lessons/round-12.md:22-24`).
8. **Defect / Debt MK-7 — 19 Legacy Knowledge Entries Lack Provenance Headers:**
   - *Evidence:* `corpus/lessons/round-1.md:286,295-300`; `corpus/QUALITY.md:27-30` (Criterion 10).
   - *Status:* **Unresolved debt by design.** Adding headers would shift cited line numbers and invalidate depth/calibration anchors (violating MK-1). Grandfathered as immutable debt.

---

## 3. Round 12 Mistakes & Defect Analysis

Grounded in `corpus/lessons/round-12.md:26-33`, `.ufo/waves/round-12/w1/MistakeMining.md:7-11`, `.ufo/evidence/round-12/LessonScribe/outline.md:38-60`, `.ufo/waves/round-12/w1/WitnessSourceReview.md:1-35`, and `.ufo/waves/round-12/w2/IntentDataWalk.md:15-38`.

### 3.1 Mined Mistakes in Round 12

1. **Vacuous Pristine Control (Single-Control Limitation):**
   - *Evidence:* `.ufo/evidence/kaika-round-1/capability-demo/README.md:48-78` (one control run); `tools/mutate-and-run.sh:465-475` checks control exit once.
   - *Defect:* A single pristine observation cannot detect subsequent control flakiness or non-deterministic test outputs (`BaselineControl.md:74-119`).
   - *Captured by:* `corpus/QUALITY.md` 1–3.
   - *Fix in Round 12:* C1 implements `tools/repeat-control.py`, verifying N≥3 runs with exact `(exit, stdout, stderr)` tuple equality.
   - *Criterion Needed:* *A pristine control check must verify repeated execution stability across exact output streams before mutation verdicts are credited.*

2. **Attribution Overreach & Declaration Contamination:**
   - *Evidence:* `corpus/lessons/round-1-verifier-spotcheck.md:17`; `corpus/knowledge/witness-scoped-kill-verdict.md:54,60-65` (E1). Unscoped searches exposed historical outcomes before declarations were frozen.
   - *Defect:* Laundering evidence scope or claiming blind pre-registration when prior outcomes were visible (`MistakeMining.md:9`).
   - *Captured by:* `corpus/QUALITY.md` 3 and 6.
   - *Fix in Round 12:* C2 enforces pre-execution declaration freezing with content hashes (`declared.tsv` sha256), discloses prior exposure, and scopes claims strictly to executed cases.

3. **Reference Drift & Grammar Divergence (S006 vs Tameshi):**
   - *Evidence:* `.ufo/waves/round-12/w1/WitnessSourceReview.md:1-35`; `corpus/knowledge/witness-scoped-kill-verdict.md:67-68` (E2/E3).
   - *Defect:* Conflating S006's single-token line grammar (`FAIL: <token>`) with tameshi's multi-assertion whole-suite line matching (`FAIL <label>`), and failing to note that D6's second alternative was a passing expectation.
   - *Captured by:* `corpus/QUALITY.md` 2–4.
   - *Fix in Round 12:* Retain historical declaration byte-unchanged; append errata E2 and E3 explicitly distinguishing adapter mechanics from shmutant semantics.

### 3.2 Unresolved Routed Defects & Inferences

4. **Seventh-Leg Depth Error (Reanalysis Masquerading as New Leg):**
   - *Evidence:* Stale plan in `SCORECARD.md:271-272` predicted `command D 6 → after 7` by adding a bash witness split. Command D regex (`SCORECARD.md:73`) counts comment lines in `tools/mutate-and-run.sh:84-89` (`ScoreRubric.md:13,30`).
   - *Defect:* Re-analyzing an existing leg (`bash-surface-census`) across an attribution dimension does NOT constitute an independent gate leg.
   - *Status:* **Resolved in Round 12 claim definition.** C2 explicitly keeps depth `6 → 6` (`claims.json:7`; `corpus/lessons/round-12.md:3,23`).
   - *Criterion Needed:* *Re-analyzing an existing mutation case across a new attribution dimension adds depth of evidence, not depth score points; depth increments require a genuinely new, independently recorded gate leg.*

5. **Determinism Overclaim from Finite Reruns (Inference R1):**
   - *Evidence:* `corpus/lessons/round-12.md:22`; `.ufo/evidence/round-12/LessonScribe/outline.md:40-44`; `.ufo/evidence/round-12/MistakeMining/fourth-run-diverges.sh`. S011 reports 9% unknown status under repeat runs; S026 notes reruns are mitigations, not proofs.
   - *Defect:* Claiming that N=3 matching runs "proves determinism" or "cures flakiness".
   - *Status:* **Explicitly rejected in Gate.** Outcome is strictly named `controls_match` (observed stability in the sample), never determinism (`corpus/lessons/round-12.md:22`; `repeated-control-precondition.md:26`).
   - *Criterion Needed:* Grounded in QUALITY 5 (falsifier/flip condition): *A finite matching sample of test runs establishes only absence of observed variation in that sample; it must never be claimed as proof of program determinism.*

6. **Conflating Lane Policy with Sourced Requirements (Inferences R2 & R3):**
   - *Evidence:* `.ufo/evidence/round-12/LessonScribe/outline.md:45-46`; `corpus/lessons/round-12.md:46,50`. S026 defines fail-3-in-a-row as a mitigation convention; S028 (Bazel) states exit code alone decides success and stdout PASS/FAIL has no significance.
   - *Defect:* Attributing lane-specific policies (N=3 threshold, byte-identical stdout/stderr) to external literature that does not mandate them.
   - *Status:* **Explicitly scoped in Round 12.** N=3 and byte equality are documented as lane policy choices, not sourced requirements (`corpus/lessons/round-12.md:46`).
   - *Criterion Needed:* Grounded in QUALITY 2: *Lane-chosen heuristics or strictness policies must be explicitly designated as lane policy, not cited as external source mandates.*

7. **Premature `mined` Transition in `SOURCES.md`:**
   - *Evidence:* `.ufo/evidence/round-12/LessonScribe/outline.md:28,72`; `RegistryReview.md:68`. Worktree flipped S026 to `mined` with `used-by: corpus/knowledge/repeated-control-precondition.md` before that file existed, which would fail `sources-census.sh validate`.
   - *Status:* **Resolved in landing order.** `repeated-control-precondition.md` was authored with full S004/S026 headers before round close.
   - *Criterion Needed:* Grounded in QUALITY 10 and `SOURCES-CONTRACT-v1`: *A registry row must not transition to `mined` until its referencing knowledge file exists in-repo with a valid `source:` header.*

8. **Same-Lane Authority Claimed as Independent (Candidate MK-15):**
   - *Evidence:* `tameshi-review.md:3` vs `corpus/lessons/round-1.md:207-213`; `corpus/lessons/round-12.md:24`; `AdmissionBounds.md:79-81`.
   - *Defect:* Treating subagents or lane-dispatched reviewers as independent admission or promotion authority.
   - *Status:* **Reaffirmed in Round 12 Gate.** All seat outputs in Wave 1 and Wave 2 are lane-internal advisories (`corpus/lessons/round-12.md:24`); outside spot-check remains external closure duty.
   - *Criterion Needed:* *No seat or subagent within the lane's own batch can supply non-author spot-check or promotion authority; all within-lane evaluations are lane self-verdicts.*

9. **Swarm Planner Role Taxonomy vs Canonical Host Ruling:**
   - *Evidence:* `spec.json:36` / `corpus/lessons/round-12.md:36` noted ClaimSkeleton performed planner function under reviewer role.
   - *Status:* **Superseded by binding host ruling.** Host directive `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:33-44` assigns canonical planner to L1 and forbids a swarm planner. L1 holds scope and contracts; ClaimSkeleton provides review; MistakeMining provides revenger data walk (`corpus/lessons/round-12.md:40-43`).

---

## 4. Master Defect & Criterion Matrix

| Defect / Debt ID | Source Anchor | Relevant Round-12 Context | Resolution Status | Criterion Needed / Binding Rule |
|---|---|---|---|---|
| **D1 / L5 (Box 3 Scope)** | `round-1-verifier-spotcheck.md:17`; `tameshi-critic.md:7-11` | C1/C2 do not rerun whole-skill cold-read; Box 3 remains unscored. | **Unresolved Debt** (managed by scope note `SHONEN.md:9-10`) | *A mark's evidence must cover the mark's whole wording, or the mark does not score* (QUALITY 1, 3). |
| **D2 (Discernment Token)** | `round-1-verifier-spotcheck.md:17` vs `SCORECARD.md:118,234` | Two conflicting tokens in circulation (`improved` vs `unprovable-but-better`). | **Unresolved Discrepancy** (Candidate MK-12) | *Discernment tokens must cite a specific non-author sample; conflicting tokens must be reconciled via append-only errata.* |
| **D3 (Calibration Pin)** | `tameshi-review.md:16` (pin 8) vs `round-1-verifier-spotcheck.md:17` (pin 6) | Calibration correctly pinned at 6 across all Round 12 baselines. | **Resolved by Pin** (Candidate MK-14 cautions against citing 8) | *Cite only the adjudicated pin with its specific adjudication row.* |
| **MK-13 (Sample Composition)** | `round-1-verifier-spotcheck.md:10-13` | Outside spot-check sampled consensus items, excluding disputed Box 3. | **Unresolved Methodological Gap** | *A spot-check sample must include ≥1 item on which outside reviewers disagree, when one exists.* |
| **MK-7 (Legacy Headers)** | `round-1-verifier-spotcheck.md:17`; `round-1.md:286` | 19 pre-round knowledge entries lack headers; lines cannot be shifted. | **Unresolved Debt by Design** (grandfathered immutable debt) | *QUALITY 10 binds all new entries; historical entries keep byte stability to preserve citation anchors.* |
| **L4 (SKILL Stale Sentences)** | `tameshi-review.md:136`; `round-1.md:442-449` | `SKILL.md:14-15,133-135` stale; editing would invalidate Box-3 sha256. | **Unresolved Debt** (documented in README gaps) | *Preserve execution-bound hashes; document friction in README/errata until next whole-skill revision.* |
| **L9 (Rejection Criteria)** | `tameshi-review.md:145` | Rejection of S029 cited stars/commits rather than contract properties. | **Resolved in Practice** | *Rejections must rest on fixture-method contract semantics, never popularity metrics.* |
| **Vacuous Control** | `round-12.md:28-30`; `capability-demo/README.md:48-78` | Single pristine control cannot detect intermittent baseline flakiness. | **Resolved by C1 Gate** (`repeat-control.py`) | *A pristine control check must verify repeated execution stability before verdicts are credited.* |
| **Attribution Overreach** | `round-12.md:28-31`; `witness-scoped-kill-verdict.md:54,60-65` | Exposed unscoped search contaminated witness declarations. | **Resolved by C2 Freezing** (`declared.tsv` sha256) | *Declarations must be committed before run; prior exposure must be prominently disclosed* (QUALITY 3, 6). |
| **Reference Drift** | `round-12.md:28-32`; `WitnessSourceReview.md:1-35` | S006 single-token line vs tameshi whole-suite line adapter grammar. | **Resolved by Errata E2/E3** | *Document adapter mechanics in append-only errata; never claim selector equivalence without implementation.* |
| **Seventh-Leg Overclaim** | `SCORECARD.md:271-272`; `mutate-and-run.sh:84-89` | Stale plan predicted depth 6→7 by adding bash witness split. | **Resolved in Claim Scope** (depth stays 6) | *Re-analyzing an existing leg across attribution dimensions adds evidence, not depth points.* |
| **Determinism Overclaim** | `round-12.md:22`; `fourth-run-diverges.sh` | Claiming N=3 matching runs proves determinism. | **Explicitly Rejected in Gate** (named `controls_match`) | *A finite matching sample establishes only absence of observed variation in that sample, never determinism.* |
| **Lane Policy Conflation** | `round-12.md:46,50`; S026, S028 | Attributing N=3 and byte equality to external literature. | **Explicitly Scoped** (declared as lane policy) | *Lane-chosen strictness heuristics must be labeled lane policy, not external source mandates.* |
| **Premature `mined` Status** | `outline.md:28,72`; `RegistryReview.md:68` | S026 flipped to `mined` before `repeated-control-precondition.md` existed. | **Resolved in Landing Order** | *A source must remain `queued` until its referencing knowledge file lands with `source:` header* (QUALITY 10). |
| **Same-Lane Authority** | `round-12.md:24`; `AdmissionBounds.md:79-81` | Treating lane seats as outside spot-check or promotion authority. | **Reaffirmed in Gate** (lane self-verdicts only) | *Lane-dispatched seats cannot supply non-author verification or promotion authority.* |
| **Planner Seat Routing** | `round-12.md:36,40-43`; `spec.json:36` | Validator rejects swarm planner; ClaimSkeleton mapped to reviewer. | **Resolved by Host Ruling** (`lane-addendum.md:33-44`) | *L1 holds canonical planner seat; swarm seats provide review/data walk; no validator bypass.* |

---

## 5. Verification Commands for Main Agent (L1)

To be executed once by L1 after all seats land:
```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin

# 1. Verify discernment tokens across committed files
grep -n 'discernment' corpus/lessons/round-1-verifier-spotcheck.md SCORECARD.md LOG.md

# 2. Verify calibration and depth measurements with exclusion
python3 .ufo/evidence/round-12/measure.py --rev HEAD

# 3. Verify SOURCES census under UTC
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi

# 4. Verify repeated-control precondition gate selftest
python3 tools/repeat-control.py --selftest
```
