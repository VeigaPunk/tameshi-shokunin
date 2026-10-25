source: S257 — https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md — snapshot .ufo/evidence/round-45/coverage/sources/googletest-primer.md (sha256 03d756ab…)
verified-at: 2026-10-25
recheck: 365d — `curl -fsSL 'https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md' | grep -c 'GoogleTest always deletes a test fixture before it creates the next one.'` (expect 1; ran 2026-10-25 → 1, and the live fetch's sha256 was 03d756ab…, byte-identical to the snapshot)
ground: F3 — determinism precondition, flaky-aware verdicts (corpus/README.md F3 frontier row; QUALITY.md criterion 62) and F2 — witness-scoped kill verdicts (knowledge/witness-scoped-kill-verdict.md)

# Independence is a property of the fixture lifecycle, and a kill verdict names the function it was decided in

## What was observed

**The named source had moved, and the move is recorded.** The adopted package entry (shokuknow `merge/tameshi`, staged S203) was written against a brief that named `docs/gtest_for_dummies.md`. That path answers HTTP 404 at every ref tried on 2026-10-25: `master`, `main`, the pinned commit `cd8e73f…`, and the `v1.7.0`, `v1.8.0`, `v1.8.1`, `release-1.7.0`, `release-1.8.0`, `release-1.8.1` tags, at both the `docs/` and the `googletest/docs/` prefixes (18/18 404s; curl `-w '%{http_code}'` outputs in `.ufo/waves/round-45/w1/ScribeGtestPrimer.md`). The document survives as `docs/primer.md` at the pinned commit, fetched live on 2026-10-25 with sha256 `03d756ab…` — byte-identical to the committed snapshot `.ufo/evidence/round-45/coverage/sources/googletest-primer.md`.

**Independence and repeatability are the first requirement, not a later refinement.** At [snapshot:14-15] the good-test list opens: "Tests should be *independent* and *repeatable*. It's a pain to debug a test that succeeds or fails as a result of other tests." At [snapshot:15-16] the structural enforcement: "GoogleTest isolates the tests by running each of them on a different object."

**The fixture lifecycle is the mechanism.** For each `TEST_F()` test: "GoogleTest always deletes a test fixture before it creates the next one." ([snapshot:251]) and "GoogleTest does **not** reuse the same test fixture for multiple tests. Any changes one test makes to the fixture do not affect other tests." ([snapshot:252-253]) The per-test sequence is concrete at [snapshot:329-330]: "GoogleTest constructs a `QueueTest` object (let's call it `t1`)." then "The first test (`IsEmptyInitially`) runs on `t1`." For `RUN_ALL_TESTS()` the same per-test cycle is listed at [snapshot:356-364]: "Runs the test on the fixture object." → "Cleans up the fixture via `TearDown()`." → "Restores the state of all GoogleTest flags." → "Repeats the above steps for the next test, until all tests have run."

**The verdict has a scope.** At [snapshot:107-109]: "The assertions come in pairs that test the same thing but have different effects on the current function." and "`ASSERT_*` versions generate fatal failures when they fail, and **abort the current function**." At [snapshot:109-110]: "`EXPECT_*` versions generate nonfatal failures, which don't abort the current function." At [snapshot:110-111]: "Usually `EXPECT_*` are preferred, as they allow more than one failure to be reported in a test." General wording at [snapshot:83-84]: "If a fatal failure occurs, it aborts the current function; otherwise the program continues normally."

## What is inferred

- **The fatal/nonfatal distinction is an upstream instance of F2's witness-scoped verdict.** The lane's F2 asks for a kill verdict that names the witness rather than the case (knowledge/witness-scoped-kill-verdict.md). GoogleTest's `ASSERT_*`/`EXPECT_*` split draws the same line inside the framework: a fatal failure aborts *the current function* ([snapshot:108-109]) — the verdict is scoped to the witness — while a nonfatal one continues and lets the case collect more findings ([snapshot:110-111]). A gate that reports a bare case label (for example, case 05 failed) without saying whether execution continued past the witness is strictly less informative than this.
- **A dead named path is a finding about the input, not about the source.** The stale path 404s cleanly rather than serving a redirect (18/18 on 2026-10-25), so trusting the name would have recorded a lead rather than a row. The live successor was opened and pinned instead.

## What is still unknown

- The primer describes the fixture lifecycle; it does not describe how `SetUp()`/`TearDown()` failures are reported — no such passage exists in the snapshot.
- Whether upstream has changed this behaviour since the pinned commit is unknown; the row is pinned at one commit (`cd8e73f…`) and the 365d recheck compares a live fetch against the recorded quote.


