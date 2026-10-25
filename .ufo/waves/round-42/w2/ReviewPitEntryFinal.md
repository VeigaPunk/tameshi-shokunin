# ReviewPitEntryFinal — PIT entry as landed (round 42 w2, FALSIFY)

Attacked: `corpus/knowledge/pit-outcome-vocabulary.md` at integration tip
`a21845f523b75adbd3e3f7a62af91294db224ad9`. The last commit touching it is `5f739acf`, and the working tree is clean
(`git status --porcelain -- corpus/knowledge/pit-outcome-vocabulary.md` printed nothing).
Bar: `corpus/QUALITY.md` criteria 2, 3, 7, 9, 10 and 82, plus `PROVINCE.md:40-42` and `:99-105`.
Every quote check below is located in the committed snapshot; access date 2026-10-25.
No counters were run. Scratch dir: `/tmp/tameshi-r42w2-ReviewPitEntryFinal`, deleted before return.
No tools were installed.

## Findings (by severity)

### F1 — low/medium: two S158 claims rest on PIT code outside S158 (criteria 2, 10). The claims are true upstream.
- Entry :31 says "PIT's code scores a run error as detected (S158 …)". The snapshot
  `.ufo/evidence/round-42/sources/pit-DetectionStatus.java` shows only the flag: `:63 RUN_ERROR(true)`,
  `:78` field, and `:108 isDetected()`. Nothing in that file computes a score.
- Entry :33-34 says "maps every non-zero child exit … to `RUN_ERROR`". The file maps every `ExitCode` except
  OUT_OF_MEMORY and TIMEOUT (`:91-98`). The "non-zero child exit" scope comes from the caller, not this file.
- I checked both at the pinned commit with
  `git fetch --depth 1 https://github.com/hcoles/pitest.git f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6`.
  Re-fetching the raw `DetectionStatus.java` gives sha256 `3bf295ad…c6`, the same as the snapshot.
  - Score: `pitest-entry/.../statistics/ScorePrecursor.java:34-36,44-45` and `MutationStatistics.java:84-89`
    build the percentage from `isDetected()`. `pitest-html-report/.../MutationTestSummaryData.java:141-146` does the same for the HTML report.
  - Exit scope: `pitest-entry/.../build/MutationTestUnit.java:121-125` calls `getForErrorExitCode` only when
    `!exitCode.isOk()`. `pitest/.../util/ExitCode.java:19` defines `MINION_DIED(-1), OK(0), OUT_OF_MEMORY(11), UNKNOWN_ERROR(13), TIMEOUT(14), TEST_PLUGIN_ISSUE(15)`.
- So both claims are true, but no registered row holds the files that make them true. Row S158
  (`corpus/SOURCES.md:128`, "so its score counts run errors as detections") makes the same step.
  Fix: an appended S158 note, or a new row pinning `ScorePrecursor.java`/`MutationStatistics.java` and `MutationTestUnit.java` at `f7fe5adf`.
- Also found: `MutationStatistics.java:104-106` prints `Generated N mutations Killed <totalDetected> (x%)`.
  PIT's own console summary therefore labels run errors and timeouts as "Killed". That backs the entry's
  inference at :44-46, but it narrows :42-43 ("both separate run error from killed by name"). That holds for the
  per-mutation outcome list (S155 :163-179) but not for PIT's summary line. The entry does not say this.

### F2 — low: E3 anchors only partly carried for the Stryker side (criterion 2)
- Entry :35 anchors S001 once (`corpus/SOURCES.md:12`). That anchor checks out: row S001, whose
  used-by list now includes this entry.
- Entry :38, "runtime errors count as invalid, outside `detected / valid`", has no line. The snapshot that supports it
  is `stryker-mutant-states.html:45` (Valid), `:47` (Invalid = runtime + compile errors) and `:51` (score `detected / valid * 100`).
- Entry :53, "Stryker counts a timeout as detected (S001)", has no line. Support: `stryker-mutant-states.html:21`, or
  `mutation-score-semantics.md:16` (which W1 E3 asked for, along with `:23`). Neither is cited.

### F3 — low: the census-oracle citation has no line, and the cited file's prose contradicts the entry (criteria 2, 82)
- Entry :57-59 cites `.ufo/evidence/round-42/census/measure.py`, oracle, without a line. The behaviour holds:
  `measure.py:311-317` returns `runtime_error` before `killed`.
- The same file's docstring at `measure.py:16-22` still says run error is "PIT's 'Run error' and Stryker's RuntimeError,
  which neither tool counts as a kill". The entry's :60, "not PIT's", contradicts that docstring and does not say so.
  Criterion 82 (QUALITY.md:1034-1037) records why the pinned bytes stay unedited. The entry should name that
  docstring line as superseded, so a reader who follows the citation does not take in the false PIT half.

### F4 — low: inference not labelled (criterion 3)
- Entry :55: "S156 adds a reason for the lane's choice: a timeout verdict depends on machine load." The lane's rule
  (`SKILL.md:208-212`) gives no such reason, so this is inference, but it is not marked as such the way :44 is.
- The source wording is weaker. `pit-faq.html:298` says the measurements "can be affected by external factors (other
  processes on the machine etc)". "Depends on" outruns "can be affected by".

## What survived

- **E1 made.** Entry :49-54 now says the lane's rule makes a timeout or crash Inconclusive and keeps it out of the rate.
  It also says "Held S001 semantics describe Stryker. They do not describe the lane's recorded convention."
  The W1 conflation (W1 :19-21) is gone.
- **E2 made.** Entry :27-28 says "The FAQ names two factors, timeouts and static initializers". This matches
  `pit-faq.html:293` and the `#static-initializers` heading at `:301`.
- **E3 made, with the residue in F2.** The anchors are present and say what the entry claims:
  - `SKILL.md:208-209`: "**Inconclusive** = no definitive verdict (timeout, crash before the summary …). Not a kill."
    `:210-211`: "Kill rate = killed / (killed + survived) — inconclusive runs are excluded from the denominator".
  - `mutation-score-semantics.md:10`: "only Killed and Survived enter its rate".
  - `mutation-score-semantics.md:71`: the Rejected rule, "count Timeout as a kill", with timeout treated as Inconclusive.
  - `corpus/SOURCES.md:12`: row S001, "detected = killed + timeout; compile and runtime errors excluded".
- **E4 made (criterion 9).** `git ls-files --error-unmatch` lists all three PIT snapshots plus `stryker-mutant-states.html`,
  `sha256.txt` and `opened-at.txt`. `sha256sum` matches the entry header (:1-3) and `sha256.txt`: `c51d8423…`,
  `ccf6ac49…`, `3bf295ad…`, and `ac273386…` for the S001 re-open.
- **E5 made (criterion 7).** The coverage-map row is at `corpus/README.md:530`, citing S155, S156, S158 and S001.
- **Criterion 10.** The header (:1-6) has `source:`, `verified-at: 2026-10-25` and `recheck: 180d`. Rows S155, S156 and S158
  (`SOURCES.md:125-126,128`) are tier A, `mined`, opened 2026-10-25, and list this entry as a user.
  The live recheck holds: `curl -fsSL 'https://pitest.org/quickstart/basic_concepts/' | grep -c 'there were no tests that exercised the line of code'` → `1`.
- **Quotes.** All are verbatim, located and at most 25 words. In `pit-basic-concepts.html`: `:163`, `:175` (8 words),
  `:179` (23 words) and `:192` (13 words). The section `§"Running the tests"` is `h2#running-the-tests` at `:154`.
  In `pit-faq.html`: `:293` (24 words) and `:298-299` (17 words); `§"Is it random?"` is at `:287`.
  `stryker-mutant-states.html:26`: "is not represented in your mutation score".
- **Line numbers in S158** are exact: `:37 TIMED_OUT(true)`, `:63`, `:78`, `:91`, `:108`.
- **404 claim** (entry :69): `curl -sSL -o /dev/null -w '%{http_code}\n' 'https://pitest.org/quickstart/mutationcoverage/'` → `404`.
- **PROVINCE.** The entry is `ground: F1`. It claims no Core move, and no PROVINCE append exists
  (`grep -n 'round 4[0-2]\|PIT' PROVINCE.md` → none). It does not classify lane NoCoverage mutants, so
  `PROVINCE.md:105` (F1b stays frontier) is respected. Comparing external tool vocabulary is method, not a product domain (`PROVINCE.md:3-5,14-18`).

## Residual risk and verification gaps

- The upstream PIT files in F1 were read at `f7fe5adf` in a scratch fetch and are not snapshotted in the lane. Those line
  numbers are evidence for this review only.
- I did not check the S158 sibling user `r42-attribute-and-outflag-destinations.md`.

Verdict: SURVIVES. E1–E5 were made, every named lane anchor says what the entry claims, and no claim is false.
The low-severity outruns (F1–F4) are citation gaps, not wrong claims.
