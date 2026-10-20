# MistakeMining — round 12, wave 1

**Axes:** depth + calibration. **Authority:** lane-local evidence mining only; not an independent review, admission, gate, or promotion judgment.

## Finding: one scope/provenance failure candidate

| Class | Evidence | Captured by | Fix candidate |
|---|---|---|---|
| Evidence-scope laundering: downstream wording can discard prior context, tested subset, revision, or sample count and then imply more than the retained evidence. Unifying the two instances is an inference, not a demonstrated common cause. | The witness record hashed declarations before the sweep but also records that an earlier unscoped search exposed prior D2/D10 survivor and D5 kill results and the D5 failure phrase (`.ufo/evidence/kaika-round-1/witness/README.md:15-23`). The knowledge note's append-only E1 acknowledges that the “Pre-registered” heading overstated the situation and corrects it to “declared-witness, partly contaminated,” not blind preregistration (`corpus/knowledge/witness-scoped-kill-verdict.md:54,60-65`). Separately, the historical cold-read record says it executed one D5 JS mutant on one pinned SKILL revision; it expressly excludes the full ten-defect sweep and Appendix B (`corpus/knowledge/executor-test-sufficiency.md:3-8,52-54,155-167`). The old broad box-3 reading is preserved as rejected in `corpus/lessons/round-1.md:70-84,114-120` and `reports/round-1-calibration.md:132-165`. | Existing `corpus/QUALITY.md:3-8` already requires falsifiable sourced claims, separation of observation/inference/unknown, append-only errata, and retained rejections. The specific witness correction is E1; the specific box-3 correction is the recorded rejection/MK-10. `QUALITY.md:15-17` binds a prediction to its result, but alone does not describe which outcome-bearing context was seen before a declaration. | For future claims, carry an evidence envelope into downstream wording: exact revision, tested scope/sample count and exclusions; prior outcome-bearing context exposure before a prospective declaration (unexposed / partly contaminated / unknown); and a claim no broader than that envelope. A hash/time establishes a temporal lock, not blindness. A finite control match establishes equality in the observed runs, not determinism. Reuse existing QUALITY criteria; no new general rule or historical rewrite is proposed from this one-lane case. |

The current `SHONEN.md:9-10` uses a bounded fleet-round-1 cold-read claim; it does not resurrect the older whole-skill claim. No defect is asserted in the current wording based on this mining. `S006` remains the source registry entry for witness semantics; no `SOURCES.md` change is warranted here. This does not add a source, hold F2/F3, alter the six existing gate legs, or count reanalysis as a seventh independent gate.

## Repeat-control counterexample design

The evidence artifact `.ufo/evidence/round-12/MistakeMining/fourth-run-diverges.sh` is a deterministic hidden-state specimen, **not executed by this seat**. With a fresh persistent state-file path, its first three invocations each yield the tuple `(exit=0, stdout="CONTROL: GREEN\n", stderr="")`; invocation four yields `(exit=1, stdout="CONTROL: FLAKE\n", stderr="")` without changing the script. Run as the exact command `/bin/sh <path-to-fourth-run-diverges.sh> <fresh-state-file>`.

Under the stated N=3 contract, the predicted result for the first three samples is `controls_match` (exit 0); a later invocation disagrees. This is a concrete countermodel to *interpreting* a finite matching sample as proof of determinism, not a counterexample to the gate's stated policy: it correctly reports only the three observed tuples. It also contains the legacy one-control sample as its first invocation, which cannot expose the later divergence. Because I did not execute it, these are fixture-derived expected observations, not measured output or a claimed gate pass/fail. It does not establish real-world flakiness or prove any result about the new implementation.

The historical single-control limitation itself is directly evidenced in `.ufo/evidence/kaika-round-1/capability-demo/README.md:48-78` (one `run_one` control call and one observed `CONTROL:` line) and `tools/mutate-and-run.sh:61-65,465-475` (control runs once before mutants; nonzero aborts). That supports “one sample is not a repeat/flake probe”; it does not establish that any particular suite is flaky.

## Provenance, bounds, and risk

- The earlier declaration's temporal order/hash and its exposed context are both in the retained witness receipt. The prior knowledge note already keeps the correction in append-only E1; I made no historical edit.
- The older box-3 assertion's scope mismatch and later correction are grounded in source notes and the lane's existing lesson/report. This mining neither replays the cold-read nor claims an outside review.
- Risks: a proposed envelope might duplicate the existing QUALITY bar; the candidate is not admitted as a general pattern (PROVINCE requires evidence in two independent lanes); a four-run artificial state sequence is a limit demonstration, not an empirical flake finding.
- LSP reconstruction was unavailable: `read xd://lsp` returned “No such tool.” I used literal `read` path/line observations above, not grep as semantic proof. No other runtime, tests, or suite verification was invoked; no tool was installed or updated.

## Exact owned paths

- `.ufo/evidence/round-12/MistakeMining/finding.md`
- `.ufo/evidence/round-12/MistakeMining/fourth-run-diverges.sh` (executable specimen; not run)
- `.ufo/waves/round-12/w1/MistakeMining.md` (this report)

No other file was written. L1 owns integrated checks and the LOG.md round entry.
