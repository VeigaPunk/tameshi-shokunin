done

# S081 precision audit

**Verdict: agree, with one scope qualification.** The reopened Bazel Test Encyclopedia supports the lesson's normal-completion quote (verbatim, 20 words), the zero-exit condition, and the irrelevance of `PASS`/`FAIL` on stdout. It labels `TEST_PREMATURE_EXIT_FILE` optional and describes its use as catching calls to `exit()`. This supports the new bounded wording as a correction to S028's shorthand; it does not support treating the optional variable as a required or exhaustive detector.

## Observed source evidence

- Reopened `https://bazel.build/reference/test-encyclopedia` through `functions.read` on 2026-10-21 (alternate Markdown). Under **Role of the test runner**, the page says: “If a test process runs to completion and terminates normally with an exit code of zero, the test has passed.” This exactly matches `corpus/lessons/round-21.md:32`. The lesson quote is **20 words** (counted by whitespace), within the stated 25-word limit.
- The same paragraph says any other result is a test failure and that writing `PASS` or `FAIL` to stdout “has no significance to the test runner.” This directly supports S081's `PASS/FAIL stdout is irrelevant` wording.
- Concrete boundary/counterexamples on the same page: (1) a process killed by the runner after timeout/resource-limit/prohibited behavior is failure, and the runner must not report a pass after signaling the test or its children; therefore stdout saying `PASS`, or a simplified “exit code alone decides” paraphrase, is not a sufficient success rule. (2) If the main test process exits while children remain, the page says the run is counted based on the main process's exit code and the runner may kill stray children; “normal completion” should not be expanded to require all descendants to have exited.
- Under **Initial conditions**, the `TEST_PREMATURE_EXIT_FILE` row describes an absolute path to a private writable file “used for catching calls to `exit()`”; its status is **optional**. This verifies the specific documented purpose and optional status. The page does not say that this mechanism catches every early termination, is mandatory for all tests, or provide an exhaustive coverage guarantee. Accordingly, S081's limited “documented optional exit()-call detector” is supported. Read “not every early termination” as a refusal to claim universal coverage, not as a quoted explicit exclusion by Bazel; the page itself does not state that exact negative.

## Supersession and S028 history

- `corpus/SOURCES.md:90` records S081 as the precision correction and says: normal completion plus exit zero; stdout `PASS`/`FAIL` is irrelevant; `TEST_PREMATURE_EXIT_FILE` is optional and documented for catching `exit()` calls, not every early termination. That summary agrees with the live source subject to the coverage qualification above.
- `corpus/lessons/round-21.md:39-48` records reopening S028, the source quote, and the old-to-new `used-by` transition. Lines 44-45 give `corpus/lessons/round-12.md` → `corpus/lessons/round-12.md, corpus/knowledge/hermetic-env-differential.md` and state that immutable cells remain unchanged. Lines 46-48 explicitly say S081 supersedes S028's “exit code alone” / “catches early exits” shorthand.
- Compared the S028 row at baseline `08175c6` with the row at target `790abd2129f153c13b471e381d454186edbde65e`: all row content through `recheck` is identical; only the final `used-by` cell gained `corpus/knowledge/hermetic-env-differential.md`. This directly supports preservation of S028's original cells and the logged backlink. `corpus/SOURCES.md:265-266` also records S081 as the correction while retaining the original S028 row.
- The old S028 teaches wording remains in that row, including “the exit code alone decides” and “TEST_PREMATURE_EXIT_FILE catches early exits.” S081 does not silently rewrite it; it explicitly supersedes those shorthands with narrower wording. That is an appropriate corrective record, not a contradiction in the new claim.

## Commands and outcomes

- `functions.read https://bazel.build/reference/test-encyclopedia` — successful live page retrieval; inspected **Role of the test runner** and the `TEST_PREMATURE_EXIT_FILE` row under **Initial conditions**.
- `git --no-pager diff --unified=0 08175c6 790abd2129f153c13b471e381d454186edbde65e -- corpus/SOURCES.md corpus/lessons/round-21.md` (filtered to S028/source-log references) — successful, exit 0; showed the S028 `used-by` addition and the S081/lesson records.
- Read-only `git show 08175c6:corpus/SOURCES.md` versus the target S028 row, and a `python3 -c` comparison/count — successful, exit 0; output `S081_quote_words 20` and `same_except_usedby True`.
- No production files changed; no Bazel test, F5 profile, or end-to-end suite was run for this source-wording audit.