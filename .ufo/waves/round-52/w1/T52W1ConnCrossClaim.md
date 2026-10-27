# Round-52 wave-1 — cross-claim separability and surface coupling

Evaluation of the cross-claim separability statement for Round 52 (C1 operability and C2 calibration), analysis of shared read/write surfaces, experimental verification on scratch control trees, and second-order synthesis for wave-2 integration.

## 1. Declarations and Separability Statement

The contract (`.ufo/evidence/round-52/contract.json:17-42`) declares two distinct claims:
- **C1 Operability** (`contract.json:18-29`): verified at REV by `.ufo/evidence/round-52/c1/measure.py`. Asserts: (1) every active row of `tools/registry.json` returns its registered outcome under `tools/registry-check.py` run at BASE against REV (held=49/49); (2) no BASE-active row dropped; (3) `mte-interop-check` expects `legs_conforming=10/10` matching `tools/mte-interop.py`; (4) frozen round-51 C3 counter prints `total=0`; (5) `tools/round21-measure.py` keeps all 11 BASE self-test case literals.
- **C2 Calibration** (`contract.json:30-40`): verified at REV by `.ufo/evidence/round-52/c2/measure.py`. Asserts zero mismatches across the frozen statement set: m1 (`SKILL.md` Round-26 leg count and mention), m2 (`SKILL.md` Round-51 registry runner row write scope), m3 (`SKILL.md` runner line pointers and scratch bullet), m4 (20 correction records in `.ufo/evidence/round-21/coldread/ledger.json` with reader quotes), m5 (supersession note in `corpus/knowledge/fleet-kill-rate-ledger.md`), and m6 (T52 re-key entries carry reader findings).

Contract separability statement (`contract.json:42`):
> "C1 reads tools/registry.json, tools/round21-measure.py (and runs every registry row and the round-51 C3 counter); C2 reads SKILL.md, the round-21 ledger, the round-51 reader files and the kill-rate ledger. C1's registry row edit and C2's SKILL.md text edits touch different files; each claim is verifiable without the other having landed (C1_CTL_POSITIVE carries no C2 edit; C2_CTL_POSITIVE carries no C1 edit). Shared prerequisite for no-harm only: any edited cold-read section is re-keyed (m6 binds how)."

## 2. File Read and Write Sets

Inspection of the counter sources and tool definitions establishes the exact direct read/write inventory:

| File path | C1 read / write | C2 read / write | Interacting clauses / roles |
|---|---|---|---|
| `tools/registry.json` | Read + **Write** | Neither | C1 updates `mte-interop-check` row (`c1/measure.py:53-67`, `113-116`). Not inspected by C2. |
| `tools/round21-measure.py` | Read + **Write** | Neither | C1 replaces `ROOT.parent` with `fleet` and preserves 11 literals (`c1/measure.py:31-34, 132-133`). Not inspected by C2. |
| `SKILL.md` | Read (indirect via C3) | Read + **Write** | C2 writes m1, m2, m3 (`c2/measure.py:98-140`). C1 runs C3 (`.ufo/evidence/round-51/c3/measure.py:89-99`) which parses tool rows under `HEAD_RE`. |
| `tools/mte-interop.py` | Read (direct) | Read (direct) | **Shared read:** C1 (`c1/measure.py:46-50`) and C2 (`c2/measure.py:69-74`) both parse AST `LEG_TABLE` (10 legs). Neither claim writes it in R52. |
| `tools/mutate-and-run.sh` | Read (indirect via C3/reg) | Read (direct) | C2 verifies line pointers `:434` and `:579-583` (`c2/measure.py:77-79, 122-128`). C1 sub-tools execute it. Neither writes it. |
| `.ufo/evidence/round-21/coldread/ledger.json` | Neither | Read + **Write** | C2 checks and populates `corrections` (m4) and re-key findings (m6) (`c2/measure.py:141-176`). Not read by C1 directly. |
| `corpus/knowledge/fleet-kill-rate-ledger.md` | Neither | Read + **Write** | C2 checks supersession note for `drift-pins` cell (`c2/measure.py:177-184`). Not read by C1. |
| `.ufo/evidence/round-51/coldread/reads/T51W2Read*.md` | Neither | Read (direct) | C2 reads 20 reader files to verify verbatim quotes in `corrections` (`c2/measure.py:157-164`). Not read by C1. |

Write sets are strictly disjoint:
- C1 writes: `{tools/registry.json, tools/round21-measure.py}`.
- C2 writes: `{SKILL.md, .ufo/evidence/round-21/coldread/ledger.json, corpus/knowledge/fleet-kill-rate-ledger.md}`.
- Intersection: $\emptyset$.

## 3. Experimental Scratch Clone Verification

A clean scratch clone (`/fast/scratch/hyaku/tameshi-r52/T52W1ConnCrossClaim/clone`) was created from `tameshi-shokunin` at BASE `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`. We built the isolated control trees following `.ufo/evidence/round-52/control/controls.py:159-175` and evaluated both counter surfaces. Receipts were captured and preserved at `.ufo/waves/round-52/w1/T52W1ConnCrossClaim.receipts.txt`.

### Step A: BASE Baseline (`ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`)
- C2 measurement (`c2/measure.py:98-184`): `total=27` (`m1=2`, `m2=1`, `m3a=1`, `m3b=1`, `m3c=1`, `m4=20`, `m5=1`, `m6=0`).
- C1 cheap clauses (`c1/measure.py:53-67, 149-150`): `mte_row_ok=False` (status active, needles expect `9/9` while tool has 10 legs); `cases_missing=[]` (all 11 literals present).
- C1 full baseline (`control/controls.stdout:1`): `held=48/49`, `not_held=2`, `dropped=0`, `mte_row=1`, `c3_covered=29`, `c3_total=1`, `r21_cases_missing=0`, `total=4`, `C1_R52_PASS=false`.

### Step B: C1 Positive Control Tree (`C1_CTL_POSITIVE`, rev `0edf050fb30ccb5f1e0557434fa9c0fcbea0ce61`)
Contains only C1 edits: `tools/round21-measure.py` (fleet-bound fix) and `tools/registry.json` (row `mte-interop-check` expects `10/10`). Zero edits to `SKILL.md`, `ledger.json`, or `fleet-kill-rate-ledger.md`.
- **C2 evaluation on C1 tree:** `total=27` (`m1=2`, `m2=1`, `m3a=1`, `m3b=1`, `m3c=1`, `m4=20`, `m5=1`, `m6=0`).
  - Delta from BASE: **0** (all sub-clauses byte-identical).
- **C1 evaluation on C1 tree:** `mte_row_ok=True` (`legs=10 want='MTE_INTEROP: PASS legs_conforming=10/10'`); `cases_missing=[]`. Full run (`control/controls.stdout:6`) scored `total=0`, `C1_R52_PASS=true`.
- **Conclusion:** C1 edits leave C2 completely unaffected.

### Step C: C2 Positive Control Tree (`C2_CTL_POSITIVE`, rev `7f66b0a6e0946d6b2370af9fb556b356df963cf4`)
Contains only C2 edits: `SKILL.md` (m1, m2, m3), `corpus/knowledge/fleet-kill-rate-ledger.md` (m5), `.ufo/evidence/round-21/coldread/ledger.json` (m4). Zero edits to `tools/registry.json` or `tools/round21-measure.py`.
- **C2 evaluation on C2 tree:** `total=0` (`m1=0`, `m2=0`, `m3a=0`, `m3b=0`, `m3c=0`, `m4=0`, `m5=0`, `m6=0`), `C2_R52_PASS=true`.
- **C1 evaluation on C2 tree:**
  - `mte_row_ok=False` (`needles=['MTE_INTEROP: PASS legs_conforming=9/9']`, unchanged from BASE).
  - `cases_missing=[]` (all 11 literals present, unchanged from BASE).
  - C3 syntax / row-reason audit (`.ufo/evidence/round-51/c3/measure.py:117-157`): All 30 tools across 32 parsed rows produced identical `row_reason` outcomes between BASE and `C2_CTL_POSITIVE`. Specifically, C2's edit to `| fleet mutation runner |` in `#### Gate/probe registry — round 51` changed write scope from `under /tmp` to `under ${TMPDIR:-/tmp}`; C3's `row_reason` checks only `if not scope: return 'write-scope-empty'`, so the row remains covered. Because no tool under `tools/` was edited by C2, `tools/round21-measure.py` remains the single uncovered tool (`c3_covered=29, c3_total=1`), exactly as at BASE.
- **Conclusion:** C2 edits leave C1 clauses completely unaffected.

### Step D: Combined Integration Tree (rev `8c7c5708e0b03a6fda4ffde3ed183afa1eb7310b`)
Combines both C1 and C2 changes into a single integration commit:
- C2 measures: `total=0` (`m1=0, m2=0, m3=0, m4=0, m5=0, m6=0`), `C2_R52_PASS=true`.
- C1 measures: `mte_row_ok=True`, `cases_missing=[]`.
- Both claims pass their respective gates without interference.

## 4. UFO-FSD Connector: Second-Order Coupling and Proposed Move

### A. Surface Contradiction
While the claim predicates are orthogonal at the primary evaluation boundary, there is a second-order coupling on the **cold-read monitor substrate** (`.ufo/evidence/round-21/coldread/measure.py` invoked by `.ufo/evidence/round-48/quality/coldread-precheck.sh` via `.ufo/evidence/round-52/no-harm.sh:47-48`).

The round-21 ledger (`.ufo/evidence/round-21/coldread/ledger.json:2132`) tracks Section `### Round-26 gate/probe registry — report interop`:
1. It hashes the `SKILL.md` section text (`sha256: "f51b853c..."` / `"0ef95e1d..."`). C2 modifies this section text (m1: "ten ledger legs", `mte-interop-check (10/10)`).
2. It hashes the referenced input files in `inputs`, which includes `tools/registry.json` (`sha256: "c1b75366..."`). C1 modifies `tools/registry.json`.

Consequently, Section Round-26 is a **dual-invalidation locus**:
- If wave-2 readers re-key Section Round-26 against an isolated C2 branch, the recorded `tools/registry.json` input SHA will be the BASE SHA; when C1 lands, the input SHA will mismatch and drop the section.
- If wave-2 readers re-key against an isolated C1 branch, the recorded `skill_sha256` will be the BASE text; when C2 lands, the section text SHA will mismatch and drop the section.
- Either scenario causes `lost > 0` under `coldread-precheck.sh`, violating the no-harm constraint (`credited >= 64, lost == 0`).

### B. Proposed Move (Wave-2 Staging Sequence)
- **Evidence:** `contract.json:42,48`; `.ufo/evidence/round-21/coldread/ledger.json:2132`; `considerthese/2026-10-26.md:80-82` (Proposal 3: recurring-defect tracker, mining the principle that cross-claim discrepancies must be gated operationally rather than caught at closure).
- **Affected Axes:** Operability (C1) and Calibration (C2), preserving Cold-Read Calibration Restraint (8) and Freshness (9).
- **Proposed Move:** Enforce a strict integration order for wave 2: create an explicit candidate integration staging commit (`INTEGRATION_BASE = merge(C1, C2)`) *before* dispatching the wave-2 cold-read reader seats for Section Round-26 (`T52W2Read26` or equivalent). The reader's trace and ledger entry must bind the combined revision, ensuring both `tools/registry.json` SHA and `SKILL.md` section text SHA reflect the final content state.
- **Risks:** Delay in either C1 or C2 wave-1 landing postpones wave-2 reader dispatch. Mitigated by wave 1 having already verified clean, non-conflicting patch application on disjoint files.
- **Verification:** Run `.ufo/evidence/round-48/quality/coldread-precheck.sh` on the staged integration tree; assert `credited == 64` and `lost == 0`.

## 5. Verification Commands and Sources

- `python3 -c "import json; print(json.load(open('.ufo/evidence/round-52/contract.json'))['separability'])"` — displays the canonical separability declaration (`contract.json:42`).
- `python3 .ufo/evidence/round-52/c2/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 --explain` — confirms C2 base score `total=27` (`c2/measure.py:98-184`).
- `python3 .ufo/evidence/round-52/control/controls.py /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/ctl` — pre-registered controls confirming `C1_CTL_POSITIVE` and `C2_CTL_POSITIVE` both evaluate `true` in isolation (`control/controls.stdout:6,11`).
- `read .ufo/waves/round-52/w1/T52W1ConnCrossClaim.receipts.txt` — durable receipts capturing the scratch clone evaluations of BASE, C1 tree, C2 tree, and combined integration tree.

## Summary
- Separability holds: C1 and C2 write sets are strictly disjoint ({tools/registry.json, tools/round21-measure.py} vs {SKILL.md, ledger.json, fleet-kill-rate-ledger.md}).
- C1 positive tree leaves C2 score unchanged at 27/27 (m1=2, m2=1, m3=3, m4=20, m5=1, m6=0).
- C2 positive tree leaves C1 mte_row (1) and cases_missing (0) unchanged; all 30 tool rows under C3 parse identically.
- Both claims read tools/mte-interop.py AST dynamically; neither writes it.
- Section Round-26 in SKILL.md is a second-order convergence point: C2 edits its text; C1 edits its recorded input tools/registry.json.
- Non-obvious move: enforce atomic staging of C1+C2 before wave-2 re-key of Section Round-26 to prevent cold-read no-harm failure.
- Receipts committed to .ufo/waves/round-52/w1/T52W1ConnCrossClaim.receipts.txt; scratch clone cleaned up.
