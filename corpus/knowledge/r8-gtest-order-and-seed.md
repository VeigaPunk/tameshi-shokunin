source: S256 — https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/advanced.md — snapshot .ufo/evidence/round-45/coverage/sources/googletest-advanced.md (sha256 05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2)
verified-at: 2026-10-25
recheck: 365d — `curl -fsSL 'https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/advanced.md' | grep -cF 'the random seed value, such that you can reproduce an order-related test failure'` (expect a non-zero count; ran 2026-10-25 → 1)
ground: F3 — determinism precondition: test-order independence, shuffle/seed reproducibility, per-test fixture object (see repeated-control-precondition.md and hermetic-env-differential.md)

# GoogleTest's own statement on test order, shuffle/seed reproducibility, and per-test fixtures

## What was observed

The snapshot (2457 lines, sha256 05546ed6…, opened 2026-10-25 at commit cd8e73f067129f8489e35c7b51c7a68552b289d2) states three things that bear directly on the lane's F3 determinism frontier.

**Test order is undefined and the design must not depend on it.** "Remember that the test order is undefined, so your code can't depend on a test" (`googletest-advanced.md:896`); the sentence continues "preceding or following another. Also, the tests must either not modify the state" (`:897`), and the rule closes with "state to its original value before passing control to the next test." (`:899`).

**The framework ships a shuffle and publishes the seed.** "This helps to reveal bad dependencies between tests." (`:1977`) — the stated purpose of the `--gtest_shuffle` flag (`:1975`). "By default, GoogleTest uses a random seed calculated from the current time." (`:1979`). The console output includes "the random seed value, such that you can reproduce an order-related test failure" (`:1981`), and the seed is settable explicitly: "To specify the random seed explicitly, use the `--gtest_random_seed=SEED`" (`:1982`).

**A new test fixture object is created per test.** "GoogleTest creates a new test fixture object for each test in order to make" (`:872`) "tests independent and easier to debug." (`:873`). The same section notes the one-copy-per-test model can be prohibitively expensive for shared resources (`:874-875`) and then describes the static-member `SetUpTestSuite()`/`TearDownTestSuite()` sharing alternative (`:881-888`) — i.e., the per-test isolation is the default, and sharing is an explicit opt-in.

## What is inferred

- **The seed is the run's ordering identity; publishing it is the reproducibility mechanism.** Because the order is undefined (`:896`) and the default seed is derived from the current time (`:1979`), two runs cannot be compared by order alone; the seed value printed by the console (`:1981`) is exactly what allows a later reproduction, and the explicit `--gtest_random_seed=SEED` form (`:1982`) pins it. This matches the lane's own frontier: `repeated-control-precondition.md` records that `controls_match` documents observed stream stability while determinism is a property of the program across runs, including runs not taken; and `hermetic-env-differential.md` normalizes the compared tuple but excludes run-identity artefacts. The seed is precisely such an artefact, and GoogleTest handles it by *publishing* it rather than merely excluding it — the second half of the discipline the lane's `env-diff.py` implements (it strips, but does not publish, the seed-equivalent artefacts).
- **Shuffle is a detection mechanism for the lane's hazard class, not a nuisance.** "This helps to reveal bad dependencies between tests." (`:1977`) names the shared-resource problem — the same hazard class as the author-side rule "preceding or following another. Also, the tests must either not modify the state" (`:897`) / "state to its original value before passing control to the next test." (`:899`) — and treats a *randomised* order as the mechanism that exposes it.
- **The per-test fixture object is the mechanism-side complement to the author-side rule.** `:872-873` describes the fixture-per-test model as making tests independent and easier to debug; `:897-899` states the author-side obligation. Together they ground the lane's assumption that test isolation is a framework-supported default, not merely an author convention.
- **Normative status, finite scope.** As with `repeated-control-precondition.md`'s treatment of its sources, the snapshot states rules and mechanisms; it does not establish that any particular implementation obeys them, and this entry claims only what the snapshot's bytes support.

## Limits

- The snapshot is one document at one commit (cd8e73f067129f8489e35c7b51c7a68552b289d2). Fetched live on 2026-10-25, the same URL's bytes hash to the same sha256 (05546ed6…) and diff clean against the snapshot (diff exit 0); the `master` alias hashes identically, and `git ls-remote` lists only `refs/heads/main` — the row stays pinned to the commit, not to a branch name.
- The document states rules and intent; it does not describe how GoogleTest *enforces* order-independence beyond the per-test fixture object, and it does not state whether shared-global mutation is checked at teardown. No such enforcement claim is made here. Deeper fixture-lifecycle enforcement questions are out of scope for this snapshot (see the companion S257/primer.md entry).
- "This helps to reveal bad dependencies between tests." is a stated purpose, not a guarantee that shuffle detects every dependency; no such guarantee is claimed.
- The live recheck grep was run once on 2026-10-25 (count 1 for the quoted seed phrase); a future 0 would signal drift from the committed bytes.
