seat: ScribeGtestPrimer

# Round 45 w1 — ScribeGtestPrimer report

Item: draft the re-grounded knowledge entry for S257 (googletest primer.md at cd8e73f067129f8489e35c7b51c7a68552b289d2). Draft at `/tmp/tameshi-r45-ScribeGtestPrimer/entry.md` (29 lines). The lane corpus file `corpus/knowledge/r8-gtest-primer-independence.md` was NOT written by this seat (lane is read-only except this report).

## 1. Header conformance (mirror of measure.py `entry_ok` checks)

```
line1_source: True          (line 1 starts "source: " and cites S257)
line1_cites_S257: True
line2_verified_at: True     (verified-at: 2026-10-25 >= 2026-10-25)
line3_recheck: True         (line 3 starts "recheck: ")
```

## 2. Snapshot identity and live re-grounding (commands + output)

Snapshot: `.ufo/evidence/round-45/coverage/sources/googletest-primer.md` (482 lines).

```
$ sha256sum .../googletest-primer.md
03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e  .../googletest-primer.md
```

Live fetch at the pinned commit, 2026-10-25:

```
$ curl -fsSL 'https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md' | tee /tmp/tameshi-r45-ScribeGtestPrimer/live-primer.md | grep -cF 'GoogleTest always deletes a test fixture before it creates the next one.'
1
$ sha256sum /tmp/tameshi-r45-ScribeGtestPrimer/live-primer.md
03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e  /tmp/tameshi-r45-ScribeGtestPrimer/live-primer.md
```

Live bytes are byte-identical to the committed snapshot (same sha256), and the recheck quote occurs exactly once. This is the recheck line's command (count 1).

## 3. gtest_for_dummies.md 404 sweep (re-verified live, 2026-10-25; 18/18 → 404)

Command: `for u in <18 URLs>; do curl -sS -o /dev/null -w '%{http_code}' "$u"; done` — output:

```
404 https://raw.githubusercontent.com/google/googletest/master/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/main/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/googletest/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/master/googletest/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/main/googletest/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/v1.7.0/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/v1.8.0/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/v1.8.1/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/release-1.7.0/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/release-1.8.0/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/release-1.8.1/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/v1.7.0/googletest/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/v1.8.0/googletest/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/v1.8.1/googletest/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/release-1.7.0/googletest/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/release-1.8.0/googletest/docs/gtest_for_dummies.md
404 https://raw.githubusercontent.com/google/googletest/release-1.8.1/googletest/docs/gtest_for_dummies.md
```

The dead-name paragraph in the draft is kept on the strength of this re-verification. The rename-chain commit details (de47b0d30c1d, 2018-06-11; 1f87a0970dc0, 2015-08-25) are NOT in the draft; retained GitHub API responses from this seat's scratch dir (`/tmp/tameshi-r45-ScribeGtestPrimer/api-*.json`) confirm them, but the draft deliberately omits non-snapshot claims beyond the 404 sweep.

## 4. Quote verification — `grep -cF` counts

Every quote appears byte-exact in the folded snapshot (`/tmp/tameshi-r45-ScribeGtestPrimer/primer.folded.md`, built with measure.py's `fold()`), in the raw snapshot where single-line, and in the draft itself:

```
Q01 folded=1 raw=0 entry=1 tokens=23 :: Tests should be *independent* and *repeatable*. It's a pain to debug a test that succeeds or fails as a result of other tests.
Q02 folded=1 raw=0 entry=1 tokens=13 :: GoogleTest isolates the tests by running each of them on a different object.
Q03 folded=1 raw=1 entry=2 tokens=12 :: GoogleTest always deletes a test fixture before it creates the next one.
Q04 folded=1 raw=1 entry=1 tokens=11 :: GoogleTest does **not** reuse the same test fixture for multiple tests.
Q05 folded=1 raw=0 entry=1 tokens=13 :: Any changes one test makes to the fixture do not affect other tests.
Q06 folded=1 raw=0 entry=1 tokens=18 :: The assertions come in pairs that test the same thing but have different effects on the current function.
Q07 folded=1 raw=0 entry=1 tokens=13 :: `ASSERT_*` versions generate fatal failures when they fail, and **abort the current function**.
Q08 folded=1 raw=0 entry=1 tokens=11 :: `EXPECT_*` versions generate nonfatal failures, which don't abort the current function.
Q09 folded=1 raw=0 entry=1 tokens=17 :: Usually `EXPECT_*` are preferred, as they allow more than one failure to be reported in a test.
Q10 folded=1 raw=0 entry=1 tokens=15 :: If a fatal failure occurs, it aborts the current function; otherwise the program continues normally.
Q11 folded=1 raw=1 entry=1 tokens=9 :: GoogleTest constructs a `QueueTest` object (let's call it `t1`).
Q12 folded=1 raw=1 entry=1 tokens=7 :: The first test (`IsEmptyInitially`) runs on `t1`.
Q13 folded=1 raw=1 entry=1 tokens=7 :: Runs the test on the fixture object.
Q14 folded=1 raw=1 entry=1 tokens=6 :: Cleans up the fixture via `TearDown()`.
Q15 folded=1 raw=1 entry=1 tokens=7 :: Restores the state of all GoogleTest flags.
Q16 folded=1 raw=1 entry=1 tokens=13 :: Repeats the above steps for the next test, until all tests have run.
```

(`raw=0` = multi-line span in the raw snapshot, expected; `folded=1` is the operative predicate, identical to the counter's fold+substring check.) The full mirror of the counter's quote predicate (QUOTE_RE capture → fold → 6–25 tokens → substring of folded snapshot) reports `quotes_captured=15 all_ok=True`. Single-line quote raw grep: Q03, Q04, Q11–Q16 each `grep -cF` = 1 on the raw snapshot.

## 5. Full draft (as written to /tmp/tameshi-r45-ScribeGtestPrimer/entry.md)

```markdown
source: S257 — https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md — snapshot .ufo/evidence/round-45/coverage/sources/googletest-primer.md (sha256 03d756ab…)
verified-at: 2026-10-25
recheck: 365d — `curl -fsSL 'https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md' | grep -c 'GoogleTest always deletes a test fixture before it creates the next one.'` (expect 1; ran 2026-10-25 → 1, and the live fetch's sha256 was 03d756ab…, byte-identical to the snapshot)
ground: F3 — determinism precondition, flaky-aware verdicts (corpus/README.md F3 frontier row; QUALITY.md criterion 62) and F2 — witness-scoped kill verdicts (knowledge/witness-scoped-kill-verdict.md)

# Independence is a property of the fixture lifecycle, and a kill verdict names the function it was decided in

## What was observed

**The named source had moved, and the move is recorded.** The brief named `docs/gtest_for_dummies.md`. That path answers HTTP 404 at every ref tried on 2026-10-25: `master`, `main`, the pinned commit `cd8e73f…`, and the `v1.7.0`, `v1.8.0`, `v1.8.1`, `release-1.7.0`, `release-1.8.0`, `release-1.8.1` tags, at both the `docs/` and the `googletest/docs/` prefixes (18/18 404s; curl `-w '%{http_code}'` outputs pasted in the wave report). The document survives as `docs/primer.md` at the pinned commit, fetched live on 2026-10-25 with sha256 `03d756ab…` — byte-identical to the committed snapshot.

**Independence and repeatability are the first requirement, not a later refinement.** At [snapshot:14-15] the good-test list opens: "Tests should be *independent* and *repeatable*. It's a pain to debug a test that succeeds or fails as a result of other tests." At [snapshot:15-16] the structural enforcement: "GoogleTest isolates the tests by running each of them on a different object."

**The fixture lifecycle is the mechanism.** For each `TEST_F()` test: "GoogleTest always deletes a test fixture before it creates the next one." ([snapshot:251]) and "GoogleTest does **not** reuse the same test fixture for multiple tests. Any changes one test makes to the fixture do not affect other tests." ([snapshot:252-253]) The per-test sequence is concrete at [snapshot:329-330]: "GoogleTest constructs a `QueueTest` object (let's call it `t1`)." then "The first test (`IsEmptyInitially`) runs on `t1`." For `RUN_ALL_TESTS()` the same per-test cycle is listed at [snapshot:356-364]: "Runs the test on the fixture object." → "Cleans up the fixture via `TearDown()`." → "Restores the state of all GoogleTest flags." → "Repeats the above steps for the next test, until all tests have run."

**The verdict has a scope.** At [snapshot:107-109]: "The assertions come in pairs that test the same thing but have different effects on the current function." and "`ASSERT_*` versions generate fatal failures when they fail, and **abort the current function**." At [snapshot:109-110]: "`EXPECT_*` versions generate nonfatal failures, which don't abort the current function." At [snapshot:110-111]: "Usually `EXPECT_*` are preferred, as they allow more than one failure to be reported in a test." General wording at [snapshot:83-84]: "If a fatal failure occurs, it aborts the current function; otherwise the program continues normally."

## What is inferred

- **F3's determinism precondition has a concrete, checkable form upstream, and it is a fixture-lifecycle property, not a test-ordering property.** The primer's isolation mechanism is structural — a fresh fixture per test, deleted before the next one is created ([snapshot:251-253]) — independent of run ordering. The lane's F3 name (corpus/README.md:80) requires clean repeated controls; the primer shows the isolation boundary the control must exercise: per-test construction, `SetUp()`/`TearDown()`, and deletion.
- **The fatal/nonfatal distinction is an upstream instance of F2's witness-scoped verdict.** The lane's F2 asks for a kill verdict that names the witness rather than the case (knowledge/witness-scoped-kill-verdict.md). GoogleTest's `ASSERT_*`/`EXPECT_*` split draws the same line inside the framework: a fatal failure aborts *the current function* ([snapshot:108-109]) — the verdict is scoped to the witness — while a nonfatal one continues and lets the case collect more findings ([snapshot:110-111]). A gate that reports a bare case label (for example, case 05 failed) without saying whether execution continued past the witness is strictly less informative than this.
- **The brief's named target being dead is itself a finding about the round's inputs.** The stale path 404s cleanly rather than serving a redirect (18/18 on 2026-10-25), so a lane that trusted the name would have recorded a lead rather than a row. The live successor was opened and pinned instead.

## What is still unknown

- The primer describes the fixture lifecycle; it does not describe how `SetUp()`/`TearDown()` failures are reported — no such passage exists in the snapshot — which is where the lane's zero-work-gate finding lives.
- Whether upstream has changed this behaviour since the pinned commit is unknown; the row is pinned at one commit (`cd8e73f…`) and the 365d recheck compares a live fetch against the recorded quote.

---
```

## 6. Landing prerequisites (other seats / main agent)

- Land the draft byte-exact at `corpus/knowledge/r8-gtest-primer-independence.md`.
- S257's used-by cell must list the entry path; the entry must be backticked in `corpus/README.md` (indexed == entries).
- Final deciding run of `.ufo/evidence/round-45/coverage/measure.py` at the landing tip (per landing rule), after S256/S257 rows exist.

## 7. Bounds compliance

- Lane checkout read-only except this report file. No git/jj mutations, no writes to the fleet repo or shokuknow. No campaign tool runs; measure.py never invoked (only a read-only mirror of its quote predicate against the committed snapshot).
- Scratch all under `/tmp/tameshi-r45-ScribeGtestPrimer/` (entry.md, live-primer.md, primer.folded.md, quotes.txt, verify_entry.py).
- Tooling: no installs/upgrades (curl, python3, git already present). RULES.md read; no pacman transaction needed.
