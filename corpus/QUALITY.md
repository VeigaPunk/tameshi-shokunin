# Admission bar (probation draft)

1. Every claim falsifiable or marked opinion.
2. Every claim carries a source: a measured anchor (path:line, command,
   evidence id) — never oral knowledge.
3. Observation, inference, and unknown stay separate.
4. Errata are append-only blocks.
5. A rejection is kept, not silently dropped.

## Criteria appended — fleet round 1 (kaika continuation, 2026-10-19)

Each criterion cites the mistake it learns from
(`lessons/round-1.md` `## Mistakes`). Criteria 1–5 are unchanged.

6. A pre-registered prediction carries its executed outcome in the same
   entry; a miss is an errata row naming the discriminator, never a
   silent drop. (MK-2, MK-3)
7. A knowledge file lands with its coverage-map row in the same round,
   or the missing row is named as debt in `LOG.md` with an owner.
   (MK-4)
8. A verification that ran lands its report in-repo in the round it
   ran; an executed-but-unreported verification is named debt, never
   cited as a pass. (MK-5)
9. Scratch stays in `/tmp`; evidence a claim rests on is copied into
   the repo (`.ufo/evidence/…`) before the commit that cites it.
   (MK-6)
10. A new `knowledge/` entry opens with `source:`, `verified-at:` and
    `recheck:`; an external source enters through a `SOURCES.md` row
    opened in the round that writes it (tiers: `SOURCES.md`, contract
    v1); a tier-C row is never sole support. (MK-7)

## Criteria appended — round 12

11. A repeated-control clean verdict names its finite sample and compares
    raw exit/stdout/stderr tuples; it never proves determinism. Its
    counterexample must defeat a one-control observation and trigger the
    same committed mismatch oracle after the repair.
    (`lessons/round-12.md`, vacuous mistake)
12. A frozen witness declaration records prior exposure and checks integrity
    before replay. Report all declared defects, unresolved denominators and
    accidental kills; reanalyzing an existing artifact is not a new gate.
    (`lessons/round-12.md`, attribution mistake)
13. Promotion restraint remains separate from partial procedure exercises:
    an Appendix A/B cold-read cannot earn full-page box-3 score credit.
    (`lessons/round-1-verifier-spotcheck.md`, Adjudication;
    `lessons/round-12.md`, attribution mistake)

## Criteria appended — round 13

14. A normalized provenance field must agree with its digest-anchored
    declaration source and preserve its prior-exposure disclosure.
    Missing or null companion metadata is not a clean normalization;
    retain the frozen faulty observation and add a separately checked
    correction. The same checker must reject the old-null companion and
    accept the kind-only repair.
    (`lessons/round-13.md`, reference-drift mistake; outside routed
    `lessons/round-12-verifier-spotcheck.md`, Routed defects item 3)

## Criteria appended — round 14

15. Every retained expectation is explicitly effective or superseded by named,
    checked replacement evidence. A setup error with the expected exit code
    is not proof of the intended assertion; the same reconciliation command
    must reject the unresolved original row and accept the disposition-only
    repair without rewriting its raw observation.
    (`lessons/round-14.md`, stale-expectation mistake; outside
    `lessons/round-13-verifier-spotcheck.md`, Routed defects item1)
16. An environment-injection claim retains its bounded non-secret overrides
    beside argv, cwd and outcome; comparison names every excluded volatile
    field. An undocumented historical setup stays unproven even when a new
    documented experiment succeeds.
    (`lessons/round-14.md`, missing-setup mistake; outside
    `lessons/round-13-verifier-spotcheck.md`, Routed defects item2; S049)

## Criteria appended — round 15

17. Classify an instrument by its behavior, not its label: comparing persisted
    expectations and returning a mismatch verdict makes it a gate. Its public
    isolated self-invocation asserts literal exits and stable finding IDs;
    helper-only controls are not a standalone selftest. Explicitly classify
    every nonzero exit, including usage, and retain the unsupported old
    invocation alongside the same-command repaired result.
    (`lessons/round-15.md`, gate-misclassification and exit-class-ambiguity;
    outside `lessons/round-14-verifier-spotcheck.md`, Routed defects5)
