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

## Criteria appended — round 16

18. An attributed finding ID comes from the stream's terminal structured
    verdict, cross-checked against the process exit, never from the first
    token match in mixed help and verdict text. The repair keeps any prior
    structured branch (JSON) unchanged. The same command must reject the old
    attribution and accept the repair on the same retained bytes, including a
    forged-line fixture. The faulty receipt is corrected by an appended
    record, never rewritten.
    (`lessons/round-16.md`, attribution mistakes; outside
    `lessons/round-15-verifier-spotcheck.md`, Routed defects 2)
19. A seat note lands under the lane root or reaches the L1 as a message.
    Every per-seat prompt names the L1 as `agent://<id>`; a bare id is a file
    path. The round's misroot sweep checks fleet-root entries with no
    pathspec, and it must flag the archived round-15 bytes.
    (`lessons/round-16.md`, landing mistake)
20. An instrument that seats execute in a wave is not edited in place during
    that wave. Changes are staged at a separate path and installed after the
    readers finish, and every receipt names the instrument sha it ran.
    (`lessons/round-16.md`, scope mistake)

21. Supersedes criterion 20's last clause ("every receipt names the instrument
    sha it ran"). A retained receipt carries the instrument's sha256 beside it
    in the same file, because the runner's `--selftest` prints none
    (`.ufo/evidence/round-16/round-gate/runner-selftest.txt` ends with the
    sha line). Criterion 20's no-in-place-edit rule stands; it recurred once
    in wave 2 (`measure.py` repaired after dispatch), and that wave's
    attackers read the committed bytes, so no verdict mixed the two.
    (`lessons/round-16.md`, scope and vacuous rows; w2 QualityReview,
    MistakeAudit)
22. Supersedes criterion 18's proof clause. An attribution repair's selftest
    must defeat each weaker rule it claims to exclude, one fixture per rule:
    first match, no exit cross-check, a line split wider than the emitter's,
    both-stream ambiguity, and a missing structured branch. A mutant that
    survives is named as equivalent with its reason. One forged-first-line
    fixture does not discriminate.
    (`lessons/round-16.md`, attribution rows; w2 AttrCritic2, MutateReattribute;
    `.ufo/evidence/round-16/attribution/selftest-mutants.json`)

## Criteria appended — round 17

23. Cold-read credit is keyed to what the read ran against, not only to the
    bucket's bytes. Every credited ledger entry carries non-empty `inputs`
    (lane path → sha256); each input must still be a regular blob with that
    sha at the measured rev, and an entry that executed commands must name
    committed trace receipts whose inputs it covers. A failing entry whose
    inputs still verify vetoes the bucket. Shown able to fail: the round-14
    bucket is credited at `e69b488` and uncredited (`input-drift:tools/mutate-and-run.sh`)
    at `09ee1d0` under `.ufo/evidence/round-17/measure.py`.
    (`lessons/round-16-verifier-spotcheck.md` §2, routed R16-C2b; S058, S059)
24. Editing an instrument that a registered gate pins means running that
    gate's registered entry command before landing. An outcome that changes
    is re-pinned or superseded by an appended manifest in the same round —
    "by design" may describe the mechanism, never excuse the outcome — and
    every mention of the old outcome is swept in that round.
    (`lessons/round-16-verifier-spotcheck.md` §3, routed R16-OP1 and R16-C2a;
    `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt`)
25. The no-harm monitor runs every active registered entry command
    (`python3 tools/registry-check.py --rev REV`), not only selftests, and
    grades each row against the outcome its capability was admitted with.
    A row leaves `active` only as `superseded` with a `superseded_by` row,
    and still runs. The monitor runs in a clone, never writing the lane.
    (`lessons/round-16-verifier-spotcheck.md` §3, routed R16-MON1;
    `.ufo/waves/round-17/w1/V02ToolsNoHarmScope.md`, K04RegistrySelfFulfilling.md)
26. A receipt found stale gets a dated correction appended in the round that
    finds it, naming both digests and their revisions; the original line is
    never rewritten. (`lessons/round-16-verifier-spotcheck.md` §6 item 5, routed R16-EV1)
27. Every lane tool that runs git — selftest fixtures included — scrubs the
    inherited `GIT_*` environment first, and its selftest proves it with a
    canary repository named by an exported `GIT_DIR` that must stay
    unchanged. An unscrubbed fixture commit moved the live lane's HEAD and
    index in round 17 wave 1. (`lessons/round-17.md`, environment-leak
    mistake; S063)
28. Correction to criterion 27 (round 17 wave 2, QualityCriteriaReview): as
    landed it was false for two git callers — `tools/bash-witness-study.py:337-341`
    (read-only `git show`, no env scrub; an exported `GIT_DIR` redirects the read)
    and `.ufo/evidence/round-17/jj/head-vs-branch.sh` (fixture commits leaked into
    a canary). The fixture script now scrubs `GIT_*` and proves it on a canary;
    `bash-witness-study.py` is pinned by round-13 `expected.json`, so its scrub
    lands with an appended disposition waiver in a later round and stays open
    debt until then. Criterion 27 applies to every other lane git caller.
    (`.ufo/waves/round-17/w2/QualityCriteriaReview.md`; `lessons/round-17.md`)
