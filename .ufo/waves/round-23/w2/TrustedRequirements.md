**TrustedRequirements — R23 C1 compiler/trust audit (advisory, read-only)**

**Write/execute disclosure:** `.ufo/waves/round-23/w2/TrustedRequirements.md` was **not** written. The wave context explicitly forbids file writes (including the Report trailer) and permits only the three assigned executor fact commands; this seat executed none. Findings below come from static reads, `grep`, and JSON queries. No tools were installed. L1 persists this.

## Axes (calibration decomposed)

| Axis | Question |
|---|---|
| A1 Baseline provenance exactness | Are `registry_sha256` and `source_revision` provable, not merely declared? |
| A2 Trusted-commitment completeness | Does the trusted commitment pin the **requirement inventory**, not just bundle bytes? |
| A3 Gate registry independence | Does the gate avoid reading the registry and avoid self-grading? |
| A4 Revision/scope coherence | Are base, compile, and delivered revisions and finite-vs-live populations explicit? |
| A5 No-harm evidence | Do 10/10, 43/43, 46/46, 62/62, and the source-read red remain intact? |

## Evidence

**E1 — Three revisions exist; only the bundle-relative one is checked.**
- Contract base: `28cae179…` (`contract.json:2`).
- Replay/bundle revision: `496d212…` (`replay/bundle.json`, `replay-command-A.json`, `replay-gate-A.json`).
- Delivered revision: `336565fc…` (`registry-C.json`, `monitor-current-C.json`, `reader-freeze2.json`).
- `requirements.json:646` declares `source_revision: 28cae179…`, but `replay.py` only records it (`replay.py:77`) and never compares it to `contract.base_revision` or resolves it. The bundle’s receipts are executions at **496d212**, not at 28cae179. `command-binding.py` checks only `receipt.revision == bundle.revision`; it cannot see the checkout or the base revision. The SCORECARD wording (“revision”) is accurate for receipt-vs-bundle; “exact baseline source_revision” is not machine-enforced.

**E2 — The registry digest check is two-file self-consistency, not an anchor.**
- `requirements.json:2` declares `ebd2e6…`; `replay.py:34-41` hashes `registry-baseline.json` against it and compares the derived 43 requirements to `frozen['requirements']`. `replay-command-A.json` exit 0 proves that check passed.
- But both files are evidence-local; rewriting them together rewrites the check. No whole-file `git show 28cae179:tools/registry.json` digest is retained. `actual-source-read.json` proves `tools/registry.json` at **496d212** hashes to `ebd2e6…`, not that the file at 28cae179 does. (Per-row `git show 28cae179` matches are claimed in w2 reports, not retained as a whole-registry receipt.)
- `reader-freeze2.json` pins `requirements.json` (`cd5205be…`), `replay/bundle.json` (`3d6c99b7…`), and `replay/expected.json` (`0831c9c8…`) at 336565fc, but **not** `registry-baseline.json` or `contract.json`. The compiler never validates the requirements schema, key sets, or `source_revision` type/format.

**E3 — Baseline vs delivered registry are different objects.**
- Baseline: `ebd2e6…`, 47 rows = **43 active** + 4 superseded, unique names.
- Delivered: `afeb6cb6…`, 50 rows = **46 active** + 4 superseded, including `command-binding-selftest`, `command-binding-frozen-clean`, `command-binding-source-read-red`.
- The frozen bundle has **43** requirements and **0** `command-binding-*` names. The compiler reads only the evidence-local baseline file; it would still compile 43 at 336565fc. `registry-C.json` independently holds 46/46 at 336565fc. The finite-bundle semantics are coherent, but `contract.json` does not state the baseline→delivered delta or the two-tier receipt fidelity (full streams in the bundle vs tails in the live monitor).

**E4 — The machine trust root is `expected.json`, not `contract.json`.**
- `contract.json` contains only `base_revision`, `claim`, and the ten-case `population`; it has no registry, requirements, bundle, or expected digest. `measure.py` hardcodes `CASES` and never reads it; `replay.py` and `command-binding.py` never read it. The gate’s docstring correctly says the expected file is the “trusted caller-owned commitment” and disclaims producer authenticity. So “explicit frozen contract” is documentation-level; choosing another expected file chooses another contract.

**E5 — The source-read red proves argv discrimination, not non-execution.**
- `source-read-bundle.json` declares requirement `receipt-measure-selftest` with argv `["python3","tools/receipt-measure.py","--selftest"]`, but the receipt argv is `["cat","tools/registry.json"]`; the gate returns `ARGV_MISMATCH` (exit 1).
- The receipt’s stdout is the full registry JSON (22,204 bytes) and **contains the required token** `RECEIPT_MEASURE_SELFTEST: 10/10 pass` (verified: `contains` = true). Static trace of `evaluate()` shows that if the receipt copied the required argv, all checks (cwd, revision, integer exit 0, token) would pass. Thus the fixture demonstrates only that a `cat` argv is rejected; source-read non-substitution at the gate level is carried by the trusted bundle, not by the evaluator. This matches the gate’s disclaimer and Command24’s stronger finding: a bundle that weakens both requirement and receipt argv passes as a different trusted contract.

**E6 — Compiler exactness defects (latent, not observed).**
- `replay.py:38` builds `source_rows` with a dict comprehension, silently collapsing duplicate active names; `registry-check.py` rejects duplicate names (lines ~193–208). Baseline currently has 0 duplicates, so no observed effect.
- `replay.py:78` records `runner_sha256` from `args.repo/tools/registry-check.py` (live tree), while the executed module is imported from the **clone** at `--rev` (`replay.py:54`). Both are `cba166…` today; a dirty live tree would make the recorded runner digest describe a different file than the one executed.
- No `requirements.json` schema/key validation; `frozen['schema']` is unused.

**E7 — What holds.**
- `before.json`: 0/10, `tool_present:false` at 28cae179.
- `c1-after-A.json`: 10/10 discriminated at 496d212, control exit 0.
- `replay-command-A.json`: 43/43 held, full streams; `replay-gate-A.json`: bundle `3d6c99b7…` clean 0/[].
- `source-read-gate-A.json`: `db620668…` red 1/`ARGV_MISMATCH`.
- `registry-C.json`: 46/46 held, `afeb6cb6…`, revision 336565fc, including selftest 38/38 and both gate rows.
- `monitor-current-C.json`: revision 336565fc, calibration 8, depth 8, overrides false.
- Gate/instrument digests agree across A and B: `command-binding.py d533dc1e…`, `registry-check.py cba16646…`, requirements `cd5205be…`.

## Contradictions stated explicitly

1. **“Exact baseline source_revision”** vs receipts executed at 496d212. `source_revision` is recorded, never enforced; the gate only binds receipts to the bundle revision.
2. **“Explicit frozen contract”** vs `contract.json` being unconsumed and digest-free. The actual trust root is `expected.json`; contract-level pinning is absent.
3. **“Source reads cannot substitute”** vs the gate accepting any bundle that declares the required inventory. The red fixture tests argv, not execution provenance; the token needed by the gate is already present in the registry read.
4. **Baseline 43 vs delivered 46.** Both are true in different scopes; the contract does not declare the delta or the two-tier monitoring boundary.

## Proposed move (one, bounded)

**Promote the trusted expected commitment into a contract-pinned provenance ledger; keep the gate registry-independent.**

1. **Expected commitment** gains optional `requirements_sha256` (canonical digest over the sorted `{name, argv, expect}` projection), `registry_sha256`, `source_revision`, and `compile_revision`. `command-binding.py` gains `--require-frozen`, used only by the production row: it recomputes `requirements_sha256` from the bundle and refuses mismatch. The gate still opens **no** registry or contract file.
2. **Compiler** (`replay.py`) verifies before execution:
   - `sha256(git show <source_revision>:tools/registry.json) == registry_sha256`;
   - `sha256(requirements.json) == contract.requirements_sha256`;
   - resolved `--rev == contract.compile_revision`;
   - after writing, `sha256(bundle) == contract.bundle_sha256` and `sha256(expected) == contract.expected_sha256`.
3. **Contract** pins baseline `ebd2e6…` (43 active), delivered `afeb6cb6…` (46 active), base/compile/delivered revisions, the bundle/expected/requirements digests, and the three added `command-binding-*` rows.
4. This synthesizes the round’s inventory-pin proposal (Command24) with the revision/digest gap; it improves A1, A2, A4 and preserves A3, A5. It makes explicit that the gate validates a trusted bundle, while the compiler proves the bundle’s inventory came from the pinned registry at the declared source revision.

## Risks

- **Schema compatibility:** the ten-case ruler’s expected writer emits only `schema` + `bundle_sha256`; keep the new fields optional and require them via `--require-frozen` on the production row.
- **Trust relocation:** contract pinning is still out-of-band; pin the contract’s own digest in SKILL/SCORECARD/reader-freeze or the trust merely moves one level.
- **Digest churn:** adding/changing registry rows changes `afeb6cb6…`; freeze the ledger after final registry bytes or in a follow-up commit C.
- **Base reachability:** `git show 28cae179:tools/registry.json` requires base in the clone history; it is an ancestor of A, but the compiler should fail closed if unavailable.
- **Delta rot:** the added-row set is round-scoped; future supersessions must be declared, not silently dropped.
- **Execution attestation remains impossible at the gate:** keep the docstring disclaimers; do not claim the gate proves a process ran.

## Verification (for L1; not executed here)

1. `sha256sum` at 336565fc: `requirements.json` = `cd5205be…`, `replay/bundle.json` = `3d6c99b7…`, `replay/expected.json` = `0831c9c8…`, `tools/registry.json` = `afeb6cb6…`; compare with `reader-freeze2.json`.
2. `git show 28cae179:tools/registry.json | sha256sum` = `ebd2e6…` and 43 active; `git show 336565fc:tools/registry.json | sha256sum` = `afeb6cb6…` and 46 active; added names exactly the three `command-binding-*` rows.
3. Run the compiler’s new `--verify-contract` at 496d212 → exit 0; bundle digest remains `3d6c99b7…`.
4. Gate on `replay/bundle.json` + expected → 0/[]; on `source-read-bundle.json` + expected → 1/`ARGV_MISMATCH`; construct in `/tmp` an argv-echo source-read bundle with matching local expected: today it returns 0 (documenting the boundary), while `--require-frozen` against the contract-pinned `requirements_sha256` rejects it.
5. `registry-check.py --root … --rev 336565fc --json` → 46/46 held, `afeb6cb6…`.
6. `measure.py --repo …` at 496d212 → 10/10; `command-binding.py --selftest` → 38/38 (or updated count); monitor at 336565fc → calibration 8/depth 8/overrides false.

**Calibration verdict:** the delivered gate is internally coherent and matches its own disclaimer; 10/10, 43/43, 46/46, and 62/62 are real. The gap is scope, not a failing check: the exact registry digest is a compiler-time two-file self-consistency check, `source_revision` is declarative, and the trusted commitment pins bundle bytes rather than the requirement inventory’s provenance. The proposed contract-pinned provenance ledger closes that gap without making `command-binding.py` registry-dependent.
