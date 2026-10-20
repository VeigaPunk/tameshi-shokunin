# WitnessSources — S006 Pinned README & Witness Adapter Analysis

**Round / Wave:** Round 12, Wave 2 (TameshiR12.WitnessSources)  
**Seat & Role:** Scout (leaf member). Read-only inquiry on S006; no code or test modifications.  
**Advisory Notice:** Lane-internal advisory evidence only; does NOT constitute independent non-author admission, promotion, or verdict authority.

---

## 1. Named Axes

1. **Quote Fidelity:** Verbatim byte extraction and line-anchored citations against the pinned remote commit artifact `7eefc73010ad6342b80e3ed43915503e02c90618` at `https://raw.githubusercontent.com/BWBama85/shmutant/7eefc73010ad6342b80e3ed43915503e02c90618/README.md` (SHA-256 `dc0051c79ab792d0f4e1b19404ed661b4c94a8e54016595aeae853d5410178a3`). Quotations strictly $\le 25$ words.
2. **Witness Adapter Delineation:** Detailed, multi-dimensional technical contrast between S006 (`shmutant`) native adapter model and Tameshi's witness adapters (JS `kimi-census` in `corpus/knowledge/witness-scoped-kill-verdict.md` and Bash `bash-surface-census` in `tools/bash-witness-study.py`).
3. **Provable Integrity & Boundary Discipline:** Clean separation between observed source text, operational implementations, and downstream interpretations; strict read-only execution with zero out-of-scope edits or tool changes.

---

## 2. Located Primary Quote & Access Metadata

- **Source ID:** `S006`
- **Target URL:** `https://raw.githubusercontent.com/BWBama85/shmutant/7eefc73010ad6342b80e3ed43915503e02c90618/README.md`
- **Pinned Commit OID:** `7eefc73010ad6342b80e3ed43915503e02c90618`
- **Access Date:** `2026-10-20` (historical in-repo capture: `2026-10-19`)
- **Document Extent:** 231 lines, 12,117 bytes
- **SHA-256 Digest:** `dc0051c79ab792d0f4e1b19404ed661b4c94a8e54016595aeae853d5410178a3`
- **In-Repo Registrations & Context:**
  - `tameshi-shokunin/corpus/SOURCES.md:17` (Row `S006`, tier A, scope: "shmutant's own bash mutation verdict semantics")
  - `tameshi-shokunin/corpus/knowledge/witness-scoped-kill-verdict.md:1-5, 8-18, 67-68`
  - `tameshi-shokunin/corpus/lessons/round-12.md:12`
  - `tameshi-shokunin/.ufo/evidence/kaika-round-1/witness/README.md:1-14`
  - `tameshi-shokunin/.ufo/evidence/kaika-round-1/score-semantics/S006.md:1-231`
  - `tameshi-shokunin/.ufo/evidence/round-12/SourceWitness/S006.md:1-231`

### Primary Verbatim Quote ($\le 25$ words)

> "Each row of a mutation table names a defect (an old literal and its replacement) and a **witness**: the assertion that must fail."
*(Location: `README.md:23-24`, § "The three verdicts"; Word count: 23 words)*

### Complementary Operational Quotes ($\le 25$ words)

1. **Accidental Kill Definition:**
   > "The suite went red, but not on its witness. Caught by accident, not by the assertion that claims to cover it."
   *(Location: `README.md:31`, § "The three verdicts"; Word count: 21 words)*

2. **Witness Token Matching Rule:**
   > "Red is exit 1 with a line starting `FAIL: ` that carries the witness as a whole token"
   *(Location: `README.md:100-101`, § "How a row is run", step 4; Word count: 17 words)*

3. **Baseline Guard Definition:**
   > "The selected tests were not green before any defect was injected... A red result would prove nothing."
   *(Location: `README.md:39`, § "The three verdicts"; Word count: 16 words)*

---

## 3. Witness Adapter Differences: S006 (`shmutant`) vs Tameshi

The S006 contract introduces witness-scoped mutation evaluation for shell code. However, Tameshi's witness implementations differ significantly from S006's native specification across six key structural and operational dimensions:

| Dimension | S006 `shmutant` Native Adapter (`README.md`) | Tameshi JS Witness Adapter (`witness-scoped-kill-verdict.md`) | Tameshi Bash Witness Study Adapter (`tools/bash-witness-study.py`) |
|---|---|---|---|
| **Execution Scoping** | **Selected unit only** (`run <root> <select>`, `README.md:98-99`). Full-suite execution per mutant is explicitly denounced (§ "Why selection matters", `README.md:109-112`). | **Full suite execution** (`node "$MUTANT" --selftest`, all 43 cases run for every mutant; `knowledge:21, 29`). | **Full suite execution** (`bash "$MUTANT" --selftest`, all 16 cases run for every mutant; `bash-witness-study.py:14-15, 91`). |
| **Witness Cardinality** | **Single witness token** per mutation row (`shmutant_mut 'name' 'old' 'new' 'witness'`, `README.md:72-73`). | **Disjunctive multi-alternative** (up to 3 pipe-separated labels in `declared.tsv`, e.g., `label1 \| label2 \| label3`; `knowledge:67`). | **Multi-label set/tuple** per defect (`DECLARED_WITNESSES`, e.g., `("clean", "runtime-absent")`; `bash-witness-study.py:102-160`). Supports `None` for defects declared `NONE`. |
| **Output Matching Rule** | **Whole-token search** in stdout lines starting with `FAIL: ` (`README.md:100-102`). Substring tokens rejected (e.g., `parse-empty` $\ne$ `parse-empty-list`). | **Exact-line equality** on complete `FAIL <label>` lines (no colon; `knowledge:67`, `WitnessSourceReview.md:28, 42`). | **Structured line regex** `^(ok-case\|bad-case\|skip-case)\s+(\d+)\s+(\S+)` (`bash-witness-study.py:172, 367-370`), extracting case names into `runinfo["bad"]`. |
| **Baseline Precondition** | **Per-selector baseline**: Every distinct selector runs once uninjected; with `SHMUTANT_COUNTS=1`, checks unit assertion counts against whole suite (`README.md:39, 94-97`). | **Single unselected baseline**: Runs whole suite once uninjected, verifying 43/43 pass exit 0 (`knowledge:29`). | **Single unselected baseline with accounting invariants**: Verifies 16 cases, sequential numbering 1..16, terminal `SELFTEST: PASS`, and matching skip set (`bash-witness-study.py:388-408`). |
| **Accounting & Inconclusive Criteria** | Binary exit / line check: Non-0/1 exit or exit 1 without `FAIL: ` line yields `aborted`; timeouts/process leaks yield `timeout`/`unsettled`/`lost` (`README.md:41-45`). | Suite denominator check: Requires full 43-case denominator to be present on red runs; missing denominator or unrunnable mutant is inconclusive (`knowledge:29`). | Explicit 8-point completeness invariants: missing selftest line, non-terminal line, denominator $\ne 16$, case count $\ne 16$, numbering gaps, unexpected skip labels, or skip set drift from control yield `inconclusive` (`bash-witness-study.py:388-409`). |
| **Process Control & Environment** | Directly invokes `ps` for process tree freezing/killing; requires bash $\ge 5.3$ (`README.md:18, 142-167`). Breaks under sandboxed `ps`. | Node.js process execution via `mutate-and-run.sh`. | Python 3 runner executing bash; includes explicit environment scrubbing of `THE_JANITOR_BIN`, `SQLITE3_BIN`, `CENSUS_BREAK` (`bash-witness-study.py:58-61, 94`). |

---

## 4. Concrete Findings (path:line)

1. **Selector-Scoping Divergence (`README.md:98-99, 109-112` vs `witness-scoped-kill-verdict.md:21, 29` and `tools/bash-witness-study.py:14-15`):**
   - In S006, `shmutant`'s core efficiency and execution contract is *unit selection*: only the tests matching the row's selector are executed (`run <root> <select>`). S006 explicitly states that running the entire suite for every mutant is a predecessor flaw that caused massive CI slowdowns (`README.md:109-112`).
   - In contrast, Tameshi's JS adapter and Bash witness study execute the *entire test suite* against every mutant (`node "$MUTANT" --selftest` and `bash "$MUTANT" --selftest`). Tameshi does not implement S006's `SHMUTANT_SELECT` interface.

2. **Grammar & Matching Strictness Divergence (`README.md:100-102` vs `witness-scoped-kill-verdict.md:67` vs `tools/bash-witness-study.py:172, 367-370`):**
   - S006 parses output lines starting with `FAIL: ` (with colon) and looks for the witness as a whitespace/token-delimited whole word.
   - Tameshi JS adapter (`witness-scoped-kill-verdict.md`, errata E2) checks for exact line equality against `FAIL <label>` (without colon) and permits multiple any-of alternatives.
   - Tameshi Bash study (`tools/bash-witness-study.py:172`) uses regex parsing on `bad-case NN <name>` and matches against a Python tuple of declared case identifiers.

3. **Baseline Precondition Scope (`README.md:39, 94-97` vs `corpus/lessons/round-12.md:12`):**
   - S006 requires each distinct selector to be validated green uninjected, plus optional `SHMUTANT_COUNTS=1` unit-to-suite assertion count verification.
   - Tameshi checks an unselected baseline before the sweep, but does not isolate selectors. As noted in `corpus/lessons/round-12.md:12`: *"tameshi's full-suite/exact-line adapter is not shmutant selector equivalence."*

---

## 5. Owned Paths & Tooling Record

- **Owned Report Path:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/WitnessSources.md`
- **Tooling Record:** No tools installed or updated. Standard read-only analysis tools (`read`, `grep`, `glob`) utilized.
- **Authority / Province:** Leaf scout. No independent promotion or admission authority asserted.
