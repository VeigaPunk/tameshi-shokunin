# ControlSources — Round 12 Wave 2 (TameshiR12.ControlSources)

**Role**: Scout, leaf member. Read-only inquiry.  
**Advisory Notice**: This report is lane-internal advisory evidence and does NOT constitute independent non-author admission, promotion, or verdict authority.

---

## 1. Axes

- **Calibration (Primary)**: Truthful accounting of what an empirical check proves versus what remains unproven; grounding C1 in external literature as an operational reliability precondition without overclaiming determinism or flakiness cure.
- **Depth**: Precise technical specification with exact byte, line, and HTTP metadata anchors (`path:line`), verbatim quotes, and source registries.
- **Adjacency / No-Harm**: Preserving strict boundaries; read-only examination of external and sibling sources; no mutation of shared files or code outside the assigned report path.

---

## 2. Located Quote & Access Metadata

- **Source URL**: `https://mutants.rs/using-results.html` (Source ID: `S004`)
- **Section**: `## Tests fail in an clean tree?`
- **Location Anchor**:
  - Remote HTML: `lines 184–187` (header line 184; quote line 187)
  - In-repo Knowledge Anchor: `corpus/knowledge/repeated-control-precondition.md:1, 10–12`
  - In-repo Evidence Anchor: `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv:5` (Row `Q1`)
  - In-repo Source Registry: `corpus/SOURCES.md:15` (Row `S004`)
- **Access Date**: `2026-10-20` (HTTP response header `date: Tue, 20 Oct 2026 03:43:57 GMT`; `last-modified: Mon, 19 Oct 2026 16:14:11 GMT`)
- **HTTP Payload Metadata**:
  - Status: `200 OK`
  - ETag: `"6ad641d3-738b"`
  - Content-Length: `29,579` bytes
  - SHA-256: `5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334`

### Verbatim Quote (23 words, $\le$ 25 words)

> "Fix this first: cargo-mutants can’t do anything until you have a tree where `cargo test` passes reliably when copied to a temporary directory."

---

## 3. Grounding & Relationship to Claim C1

1. **Support for C1 as an Operational Precondition**:
   - Claim C1 implements `tools/repeat-control.py`, verifying pristine control baseline stability ($N \ge 3$ repeated executions requiring identical exit code, stdout, and stderr) prior to mutation testing.
   - S004 frames clean-tree execution explicitly in *reliability* terms: mutation analysis cannot begin until baseline tests pass *reliably* in an isolated directory. If a baseline fails or behaves erratically, the evaluation cannot proceed (`baseline_nonzero` or exit-2 could-not-evaluate).

2. **Not a Proof of Determinism**:
   - S004 acknowledges that tests in a clean copy may exhibit intermittent failures ("there might be an (intermittent) failure in the source directory").
   - Demanding that tests pass reliably is a pragmatic prerequisite, not a mathematical or empirical proof of universal determinism. Observing $N \ge 3$ identical runs confirms observed stream stability across those specific trials, but cures no underlying flakiness and proves nothing about unobserved trials.

---

## 4. Concrete Findings (path:line)

- `https://mutants.rs/using-results.html:184-187`: Section `## Tests fail in an clean tree?` defines the clean-tree baseline requirement.
- `tameshi-shokunin/corpus/SOURCES.md:15`: S004 registry row records `§Tests fail in an clean tree?` under scope "cargo-mutants outcome semantics and run-scoping options".
- `tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:10-12`: Notes S004 `S004.html:185-187` as primary justification for exit-2 / could-not-evaluate baseline handling.
- `tameshi-shokunin/.ufo/evidence/round-12/ControlKnowledge/quotes.tsv:5`: Verifies SHA-256 `5ec9ba95...` and exact text alignment.

---

## 5. Tooling & Authority Disclosures

- **Tooling Record**: No package installs or system updates were performed. Used host `curl` and `grep` for read-only remote verification.
- **Authority / Province**: Leaf seat execution. No independent admission or promotion asserted.
