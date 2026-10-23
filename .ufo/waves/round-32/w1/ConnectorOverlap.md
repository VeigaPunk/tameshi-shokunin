# Sibling-overlap scan — Tameshi C1 (tally-audit of mutate-and-run.sh)

Axes: operability (primary), freshness. Advisory evidence only; no code edits, no runtime invocation, no integration, no admission, no round verdict. Paths relative to `/home/vgpnk/Projects/shokunin/` unless absolute. Scan covered 20 sibling lanes (`*-shokunin`, excluding `tameshi-shokunin`); executable searches covered 12 sibling script/tool/verifier roots (`corpus/`, `tools/`, `scripts/`, `SKILL.md`, `verifiers/`). `.ufo` historical archives and `corpus/live/` runs were excluded from the executable search (only surfaced incidentally).

## Scope and evidence

Concepts searched: (1) auditing a test harness against seeded faulty implementations ("test the tests", harness meta-tests); (2) a static per-operand tally presence check (`st_*=$?` per leg of `run_regression`); (3) a held-out generated mutant set (must-kill / must-accept copies). Query families: `selftest`, `mutant`, `run_regression`, `st_`, `tally`, `held-out`/`heldout`, `fault injection`, `overcount`/`undercount`, `sum-preserving`, `test the tests`, `meta-test`, plus `mutate-and-run` and `TALLY_AUDIT`. Tools used: `grep -rIl` over the named roots; no files executed, no network, no installs.

Result: no sibling implements the same three checks against `mutate-and-run.sh`. Concept (2) has zero sibling implementations (unique to Tameshi C1). Concepts (1) and (3) are fleet-wide shared practices with lane-specific targets and predicates (adjacent, not same).

## Table — sibling hits

| Lane | Path:line | What it holds | Overlap with C1 |
|---|---|---|---|
| kengaku | `corpus/evidence/round9-fleet/harness-mutation.md:1` (battery `test_harness.py`) | Adversarial "test the tests" battery against round-8 `horizon.py` parser/grader; 50 synthetic cases, fidelity check vs source-extracted originals | adjacent (different harness, no tally, no mutant set) |
| kake | `scripts/base_path_selftest.py:1` (also `citing_set_selftest.py`, `source_recheck_selftest.py`, `robots_audit_selftest.py`, `link_preview_selftest.py`, `sitemap_audit_selftest.py`) | Fixture-based harness meta-tests: tool exit/verdict/reason codes vs `expected.json` per case | adjacent (seeded faulty cases, different audit gate) |
| souji | `tools/cand-c2-clusterc-selftest.sh:1` (plus ~40 `cand-*-selftest.sh`, `round9-selftest.sh`, `cand-merge-selftest.sh`) | Seeded fixture selftests for souji verify/quarantine/vault tools; VERDICT-based assertions | adjacent (different target, no tally) |
| chousa | `tools/research-gate.sh:3934` (`run_selftest`, `--selftest`) | Research-gate selftest with `gate-mutant.sh` copies (13 of 17 cases) | adjacent (mutant-copy concept, different gate) |
| kotoba | `verifiers/fault_injection_corpus.sh:1` | Landable fault-injection harness: plants one fault per throwaway clone, asserts on JSON for corpus instruments | adjacent (seeded-fault harness meta-test, different instruments) |
| kotodama | `tools/harness/round_runner_conformance.py:1` (plus frozen gate selftests under `tools/gates/frozen/.../selftests/`) | Round-runner conformance + frozen-gate selftest outputs | adjacent (conformance, not tally/mutants) |
| tabi | `scripts/selftest-measurement-binding.mjs:1` | Selftest driver for `check-measurement-binding.mjs` | adjacent (different binding check) |
| mado | `tools/mado-verify.sh:2235` (`run_regression`), `corpus/knowledge/gate-mutation-proof.md:17` | Mutation sweep that *consumes* `mutate-and-run.sh` as its harness; gate-mutation proof knowledge | adjacent (consumer of the runner, not an auditor of its tally) |
| kumitate | `scripts/gate-mutants.mjs:1` | Held-out frozen mutant set + kill predicate K43 for `cite-check`/`wave-census` scripts | adjacent (mutant-set mechanism, different target scripts) |
| tsukuroi | `tools/mutants-adjacency-overlap.py:1` (also `mutants-owed-statements-r29*.py`, `mutants-kernel-taint.py`, `mutants-btrfs-space-r30.py`) | Should-fail mutant batteries for tsukuroi's own checkers (round 28/29/30) | adjacent (mutant batteries, different checkers) |
| mori | `tools/mori-round17-seat-regressions.py:1` (also `mori-round13..19-regressions.py`, `mori-misroot-sweep.py`) | Seeded regression batteries for mori tools | adjacent/none (regression, not generated mutants of a runner) |
| kaidoku | `tools/round-28/c1-heldout-naming.py:1` (and `round-29/c1-fresh-naming.py`) | Held-out selector set for EVM selector naming (not mutants) | adjacent (held-out concept only; different domain) |

No sibling entry implements a static per-operand tally presence check (`st_*=$?` per `run_regression` leg) or audits `mutate-and-run.sh`'s tally block. `grep` for `TALLY_AUDIT`, `run_regression` (outside mado's consumer use), `sum-preserving`, and `per-operand` across sibling `tools/`, `scripts/`, `SKILL.md`, `corpus/knowledge/` returned no hits beyond the table above.

## Contested scope (named, not absorbed)

1. **Harness meta-testing / "test the tests" is a fleet-wide shared practice.** kengaku, kake, souji, chousa, kotoba, kotodama, tabi (and mado via its selftest) all own seeded-fault batteries with their own fixtures, kill predicates, and refusal taxonomies. Tameshi C1 must own only the `tally-audit.py` instance over `mutate-and-run.sh`; it must not absorb, redefine, or re-label those siblings' batteries, nor claim ownership of the pattern. Their fixture/reason-code taxonomies are not interchangeable with C1's must-kill/must-accept copies.
2. **Held-out generated mutant sets are multi-owned.** kumitate (`gate-mutants.mjs`, K43), tsukuroi (`mutants-*`), and mori (regression batteries) each define their own kill predicates and target tools. Tameshi's 18 must-kill / 8 must-accept copies are scoped to `mutate-and-run.sh` only; the generated-per-run family must not be generalized into a fleet mutant standard, and sibling predicates must not be imported.
3. **Static per-operand tally presence check is uncontested.** No sibling implements it; no contested scope. It is Tameshi C1's own addition.
4. **Consumer dependency (not ownership).** mado-verify.sh drives `mutate-and-run.sh` as its regression harness and pins a recorded target sha. C1 changes the runner's *audited* tally only (runner stays byte-identical per freeze); any tally-audit verdict must not be read as validating mado's recorded table, and mado's `PIN_MADO`/`TABLE_MADO` remain mado's own.

## Proposed move (one bounded proposal)

Keep `tally-audit.py` scoped strictly to the three frozen checks (per-leg presence; oracle 0–255 + overcount/undercount stress; runner selftest harness lines 1989–2040 against faulty tally blocks) and cite — do not import — the sibling batteries above for vocabulary only (e.g., K43's evaluable-run definition, kake's reason-code pinning). Concretely: add a one-line scope fence to the tool's docstring/usage stating it audits only `mutate-and-run.sh`'s tally block and does not generalize to other harnesses or mutant sets. Expected effect: operability improves (a later reader cannot mistake C1 for a fleet-wide harness-meta-test standard); no axis harmed (no new behavior, no new reads, predicate unchanged). Risk: none beyond documentation; runner sha256 stays `a7d3f2dd…2eb9`.

## Commands executed (read-only)

- `ls -d /home/vgpnk/Projects/shokunin/*-shokunin` (21 dirs incl. tameshi; 20 siblings).
- `grep -rIl -i "tally|mutant|selftest|run_regression|fault injection|held-out|heldout|overcount|undercount|sum-preserving|test the tests|meta-test"` over `tools/`, `scripts/`, `SKILL.md`, `verifiers/`, `corpus/knowledge/`, `corpus/lessons/` per sibling; `.ufo`/`corpus/live/` excluded.
- `grep -n` line-anchor extraction on the twelve representative files listed in the table.
- No tools installed or updated; no files written outside this report.

## Limits

- Classification is from code/doc reads with line anchors; no sibling gate or selftest was executed.
- "No hit" claims rest on the named roots; unpublished history and `.ufo` archives were not scanned exhaustively.
- No sibling selftests or mutation ledgers were run; broad sibling-cache absence remains unverified, not passed.
- This report is advisory; it does not judge, admit, edit, integrate, ship, or invoke any runtime.
