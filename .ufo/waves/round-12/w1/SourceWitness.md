# SourceWitness — S006 Pinned README Capture & Witness Semantics Analysis

**Lane / Seat:** UFO-FSD scout (`SourceWitness`), Wave 1, Round 12.  
**Role:** Leaf scout advisory. No independent non-author promotion/admission authority; no subagent dispatch; leaves only.

---

## 1. Named Axes

1. **Extraction Fidelity:** Exact verbatim byte capture and sha256 checksum matching against the pinned remote commit artifact.
2. **Grammar & Semantics Precision:** High-fidelity delineation of shmutant's tri-verdict triage (`killed`, `survived`, `accidental`) and pre-execution guard verdicts (`baseline`, `unapplied`, `aborted`, `timeout`, `unsettled`, `lost`).
3. **Boundary Identification & Limitations:** Clear separation between tool-specific token-matching heuristics, single-witness constraints, bash 5.3+ runtime requirements, and broader mutation testing theory.
4. **Hermetic Provenance & Integrity:** Retention of evidence in seat-owned `.ufo/evidence/round-12/SourceWitness/` without modifying `corpus/SOURCES.md` or sibling worktrees.

---

## 2. Located Quote, Access Date, & URL

- **Target URL:** `https://raw.githubusercontent.com/BWBama85/shmutant/7eefc73010ad6342b80e3ed43915503e02c90618/README.md`
- **Pinned Commit OID:** `7eefc73010ad6342b80e3ed43915503e02c90618`
- **Access Date:** `2026-10-19`
- **Located Primary Quote (<=25 words):**
  > "Each row of a mutation table names a defect (an old literal and its replacement) and a **witness**: the assertion that must fail."
  *(Location: `README.md:23-24`, § "The three verdicts"; Word count: 23 words)*

- **Supporting Secondary Operational Quotes:**
  - Witness Token Matching:
    > "Red is exit 1 with a line starting `FAIL: ` that carries the witness as a whole token"
    *(Location: `README.md:104-105`, § "How a row is run", step 4; Word count: 17 words)*
  - Killed Definition:
    > "`killed`: The suite went red **on its witness**. The test detects the defect."
    *(Location: `README.md:29`, § "The three verdicts"; Word count: 12 words)*

---

## 3. Witness Semantics

From the pinned README of `shmutant`:

1. **Row Tuple Contract:**
   Every test mutation row specifies three components:
   - Target defect: `old_literal` (the code fragment to be replaced).
   - Defect mutation: `replacement` (the injected fault).
   - `witness`: the named assertion token that is explicitly claimed and expected to fail.

2. **Tri-Verdict Evaluation:**
   Rather than treating any suite failure ("red") as a kill, the harness parses the specific failure output:
   - `killed`: The suite exited red (exit code 1) and emitted a failure line containing the declared witness token. The test caught the defect through the claimed assertion.
   - `accidental`: The suite exited red, but the failure line did *not* match the declared witness token. The defect broke something unexpected or was caught by an incidental side-effect rather than the intended check.
   - `survived`: The suite remained green (exit code 0). The injected defect went completely undetected by the test suite.

3. **Harness Integrity & Guard Verdicts:**
   - `baseline`: The selected test unit was executed against the pristine (uninjected) code and failed to come back green, or failed assertion count invariants (`SHMUTANT_COUNTS=1`). If the baseline is red or aborted, a subsequent red run proves nothing.
   - `unapplied`: The `old_literal` did not exist in the pristine source tree, injecting 0 mutants and testing nothing. (Also: rows where `old_literal` appears more than once are refused upfront to prevent ambiguous multi-site substitution).
   - `aborted`: The test exited with a status other than 0 or 1, or produced exit 1 without a recognized failure line.
   - `timeout` / `unsettled` / `lost`: Indeterminate execution states where worker process trees hung, forked beyond process group control, or died without reporting.

4. **Matching Mechanism:**
   Red requires exit 1 with a line prefixed `FAIL: ` (or configured TAP counterpart) carrying the witness token as a discrete whole word (e.g., token `parse-empty` will not match `parse-empty-list`).

---

## 4. Limitations & Structural Boundaries

1. **Single-Witness Constraint:**
   `shmutant`'s schema associates each mutation row with exactly one witness token. It does not provide native grammar for disjunctive (`witness_A OR witness_B`) or multi-stage cascading witnesses.
2. **String Token / Text Heuristic Matching:**
   Witness validation is purely text-based token search on stdout lines starting with `FAIL: `. It lacks semantic AST reflection; an error string coincidentally containing the witness token can produce a false `killed` classification.
3. **Rigid Exit Code Contract:**
   The runner expects strictly exit 1 for intentional failure. Any unhandled exit code (such as shell syntax errors returning 2 or 127) defaults to `aborted` rather than witness failure.
4. **Single-Line Literal Replacement:**
   Mutations are restricted to single-line text replacements of unique literals. Multiple identical tokens in a file trigger rejection rather than disambiguated AST mutation.
5. **Heavy Shell & Runtime Dependencies:**
   Requires bash >=5.3 and POSIX utilities. Highly dependent on system `ps` for process tree freezing/killing; fails or aborts in sandboxed runner environments where setuid `/bin/ps` is restricted.
6. **Provenance & Scope Authority:**
   Tier A for its own harness semantics, but represents a single-author shell tool (0 stars, 239 commits at open), not an established cross-industry normative standard.

---

## 5. Owned Paths & Evidence Retention

- **Owned Evidence Directory:** `.ufo/evidence/round-12/SourceWitness/`
  - `.ufo/evidence/round-12/SourceWitness/S006.md`: Exact byte-for-byte capture of pinned README (231 lines, 12,117 bytes, SHA-256 `dc0051c79ab792d0f4e1b19404ed661b4c94a8e54016595aeae853d5410178a3`).
  - `.ufo/evidence/round-12/SourceWitness/capture-meta.json`: Full machine-readable capture manifest (URL, commit OID, timestamp, sha256, byte length, quotes, word counts).
- **Owned Wave Report:** `.ufo/waves/round-12/w1/SourceWitness.md`
- **Untouched:** `corpus/SOURCES.md` (read-only per contract; no edits made).

---

## 6. Risks & Observations

1. **Risk of Semantic Drift in Re-implementation:**
   In tameshi's witness experiments, failure verification used exact-line equality (`FAIL <label>`), whereas S006 specifies whole-token substring search on `FAIL: ` lines. Downstream lanes using S006 as a foundation must acknowledge this strictness delta.
2. **Risk of Misclassifying Accidental Kills as Coverage:**
   Tools lacking witness discrimination conflate `accidental` with `killed`. S006's value is isolating accidental kills, but its token-matching limitation means assertions must emit distinct, non-overlapping tokens.

---

## 7. Tooling Record

- No new tools installed or updated. Used standard coreutils (`sha256sum`) and harness fetch routines.
