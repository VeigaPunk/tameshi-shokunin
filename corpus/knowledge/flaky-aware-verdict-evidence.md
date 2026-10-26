source: S261 — https://arxiv.org/abs/2302.09330 — §Abstract — arXiv:2302.09330v2; S262 — https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf — §I Introduction guidelines block (RQ1 & RQ3; RQ2 & RQ3), §V-C, §VI-B, §VII
verified-at: 2026-10-25
recheck: 365d — `curl -fsSL 'https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf' | sha256sum` (expect `0b88045817f146db3eb26d305c864291010e5c083aa8d5cac480be3c5350895d`) and `curl -fsSL 'https://arxiv.org/abs/2302.09330' | grep -cF 'we rely only on the most commonly available artifacts'` (expect 1); the digest check and the phrase count were run 2026-10-25 against the committed snapshots below, not against the live URLs — the live fetch is the future recheck, and a moved digest or a zero count means every quotation must be re-located before this entry is reused
ground: F3 — determinism precondition, flaky-aware verdicts (`corpus/README.md` F3 row: one control per sweep → N ≥ 3 byte-identical controls, or a named mismatch)

# A flaky verdict can be predicted from recorded history (reported); what a one-run gate verdict is worth is this lane's inference

Two committed snapshots are the whole ground of this entry: the arXiv abstract page of arXiv:2302.09330v2 (S261) and the camera-ready text of Lam, Winter, Astorga, Stodden and Marinov (S262). Both were read through their committed bytes, not fetched live for this draft. Every quotation below was located in the snapshot's folded text, and its whitespace-token count after that fold is given; every number is followed by the line of the committed text file or the page field it came from. Statements about what this lane should do are marked `[INFERENCE]`.

## What the sources state

**Snapshots and visible fields.** S261 is `.ufo/evidence/round-47/coverage/sources/arxiv-2302.09330-abs.html`, 43,549 B, sha256 `2965343ceaac627ccf71f587d3108073c6b45e08b89db3bbe1521a5716e14bc6`, fetched 2026-10-25. Its metadata cells read `arXiv:2302.09330v2 [cs.SE]`, `Submitted on 18 Feb 2023 (v1), last revised 18 Mar 2023 (this version, v2)`, `12 pages, to be published in the Proceedings of the IEEE International Conference on Software Testing, Verification and Validation (ICST 2023)`, and the DataCite DOI `10.48550/arXiv.2302.09330`; the title is *Practical Flaky Test Prediction using Common Code Evolution and Test History Data* (Martin Gruber, Michael Heine, Norbert Oster, Michael Philippsen, Gordon Fraser).

S262 is the camera-ready PDF `.ufo/evidence/round-47/coverage/sources/lam-2020-reruns.pdf`, 11 pages, 565,435 B, sha256 `0b88045817f146db3eb26d305c864291010e5c083aa8d5cac480be3c5350895d`, and its committed text snapshot `.ufo/evidence/round-47/coverage/sources/lam-2020-reruns.txt`, produced with pdftotext 26.08.0 `-layout`, 81,725 B, sha256 `bf52c9089e331f18bb65c3c03449de070723c7ec52725c0e6dc84ca249b025b9`. The text is two columns per page, so a sentence that crosses the column gutter is interleaved in the extracted text: every quotation below is a fragment wholly inside one column, and `lam-2020-reruns.txt:NNN` names the line it occupies. The text carries `©2020 IEEE` (`:63`) and contains no venue string; the PDF metadata names TeX and pdfTeX 1.40.20 only, so this snapshot does not state where the paper was published and this entry does not claim it.

### S261 — flakiness predicted from outcomes, durations and code history, with no added reruns

The motivation is a loss of trust, not a taxonomy: "Non-deterministically behaving test cases cause developers to lose trust in their regression test suites" (14 tokens) and "Detecting flaky tests is therefore a crucial task in maintaining code quality" (12 tokens) — §Abstract.

The obstacle the paper is built against is deployment inside industry: "their reliance on instrumentation, test reruns, or language-specific artifacts was inhibitive" (11 tokens) — §Abstract. What the authors do instead: "we therefore investigate the prediction of flaky tests without such requirements on the underlying programming language, CI, build or test execution framework" (22 tokens) — §Abstract.

The inputs are cheap and already recorded: "we rely only on the most commonly available artifacts, namely the tests' outcomes and durations" (15 tokens), and "our approach does not require additional reruns, since it gathers this data from existing test executions" (16 tokens) — both §Abstract.

The evaluation is one system, with a balanced set: "evaluated their performance on a large-scale industrial software system" (9 tokens) and "we collected a data set of 100 flaky and 100 non-flaky test- and code-histories" (14 tokens) — §Abstract. The headline: "The best model was able to achieve an F1-score of 95.5% using only 3 features" (15 tokens) — §Abstract — with the three named in the same abstract as "the number of changes to source files in the last 54 days" (12 tokens) plus the flip rate and the changed-file count of the most recent pull request.

### S262 — what reruns buy, and how little a single order says

The paper's flaky label is a rerun outcome, not a static property: "we label tests as flaky if our runs have both pass and fail" (13 tokens) — §I, `lam-2020-reruns.txt:29`. The measurement is heavy: "we run each test suite exactly 4000 times, potentially" (9 tokens, `:91`), "running every test suite 4000 times in 40 batches, and every" (11 tokens, `:591`), and "we again run it 4000 times in isolation" (8 tokens, `:593`). Its population is Java and Maven: "we perform our empirical evaluation on Java projects that rely" (10 tokens, `:25`), with "A threat to validity is that our study uses only 26 modules" (12 tokens, `:582`) and 23 Maven-based Java projects (`:583`).

The guidance block, §I `:114-115`, prices the check: "one can use ≤ 5 reruns (50% less than Google's default ten" (12 tokens) "reruns [6]) and still check correctly ≥ 82% of the time." (11 tokens). The detection guidance is about order, not repetition: "RQ2 & RQ3: To detect flaky tests, one should run tests in" (12 tokens) "orders with fewer times each, rather than fewer orders with" (10 tokens) — §I `:116-118`.

Order matters because the old category was wrong: "In contrast to OD tests that fail deterministically" (8 tokens, `:48`), "the majority of NOD tests are actually" (7 tokens, `:122`) NDOD, and of the manually inspected set, "found 7 OD, 14 NDOD, 4 NDOI, and 3 more NOD that are" (13 tokens) difficult to classify — §VI, `:459-460` after "In sum, we inspected 28 tests and" (7 tokens, `:459`).

Reproducing a suite failure in isolation is not free: "ISO did not detect 57 tests by itself" (8 tokens, §V-C, `:438`), and "Guideline: We find that 53% of flaky tests detected in TSO" (11 tokens, `:452`) "runs are not detected in ISO runs." Failure rates move as well: of the 50 tests ISO detected, "tests that ISO detected, 19 tests have their failure rates lower" (11 tokens, `:446`) for ISO, "for ISO, 3 have it equal, and 28 have it higher" (11 tokens, `:447`). The burst length needed is longer in isolation: "we observe that TSO reaches 82% for a maximal" (9 tokens, `:439`) burst length of 2, while "for a maximal burst length of 5 test failures instead" (10 tokens, `:442`) is what ISO needs to reach the same share.

The worked example is a wall-clock verdict: "This test is flaky because some runs take longer than" (10 tokens, §II-B, `:148`) "the timeout limit of 1500ms. We find that the test is NDOD" (12 tokens, `:149`); "this test has a failure rate of 39.1%" (8 tokens, `:164`) "when run by itself in isolation, while its failure rate is 10.9%" (12 tokens, `:165`) in its suite, ranging 0%–20.1% by order (`:167`). The authors' own reading is that the JIT compiler, triggered by earlier tests, moves the runtime across the 1500 ms limit (`:150-159`).

The suite-level price is measured, not estimated: "developers encounter TSR failures between <0.1%" (6 tokens, §V-D, `:479`) and 50% (`:480`), and "TSR failure in 5.4% of TSRs." (6 tokens, `:482`) on average. One such failure is enough to block a merge: "from a test-suite run (TSR) would prevent the developers from" (10 tokens, `:465`).

**Every number in this entry, with its location**

| Number | Source | Location |
|---|---|---|
| 100 flaky and 100 non-flaky histories; one industrial system | S261 | §Abstract |
| F1-score 95.5% from 3 features; 54 days of source-file changes | S261 | §Abstract |
| 12 pages; ICST 2023 (comments field); v1 2023-02-18, v2 2023-03-18 | S261 | snapshot metadata cells |
| ≤ 5 reruns; Google default 10; 50% less; ≥ 82% correct | S262 | `lam-2020-reruns.txt:114-115` |
| 4000 suite runs, 40 batches, ≥ 100 runs per TCO | S262 | `:591-592` |
| 4000 isolation runs per detected flaky test | S262 | `:593` |
| 26 modules from 23 Maven Java projects | S262 | `:582-583` |
| 107 flaky tests in the dataset | S262 | `:96` |
| 50 detected in ISO; 57 not detected by ISO | S262 | `:436-438` |
| 19 ISO-lower / 3 equal / 28 ISO-higher failure rates | S262 | `:446-447` |
| 53% of TSO-detected tests not detected in ISO | S262 | `:452` |
| burst length 2 (TSO) vs 5 (ISO) to reach 82% | S262 | `:439-442` |
| 5.4% mean TSR failure rate; range <0.1% to 50% | S262 | `:479-482` |
| 28 inspected: 7 OD, 14 NDOD, 4 NDOI, 3 unclear | S262 | `:459-460` |
| 1500 ms limit; 39.1% ISO vs 10.9% TSO; 0%–20.1% across TCOs | S262 | `:148-167` |
| 11 pages; ©2020 IEEE | S262 | pdfinfo Pages field; `lam-2020-reruns.txt:63` |

## What this means for fixture craft

Everything in this section is `[INFERENCE]`: neither snapshot measures this lane, its gates, its controls or its counters.

- **A single run is a sample, and the sources price the second one.** S262 states what a small budget buys: at most five reruns still check correctly at least 82% of the time on their data (`:114-115`), and S261 states that a model over recorded history needs no added reruns at all (§Abstract). `[INFERENCE]` A lane that wants a flaky-aware verdict therefore has exactly two honest routes: pay reruns at verdict time, or consume a history that already exists. The evidence this round's claims rest on is one observation per statement-profile and one selftest invocation per mutant — the C1 surface compares the (line, exit) a statement prints under six profiles (`.ufo/evidence/round-47/contract.json` C1 `surface`) and C2's kill rule is a predicate on one selftest invocation's exit status and its `FAIL ` line (same file, C2 `statement`) — so no flaky-aware claim can be read off those observations without a repeat or a history.
- **Order diversity and repetition answer different questions.** S262's detection advice is more orders with fewer runs each, not fewer orders with many runs each (`:116-118`), because the paper reports that the majority of NOD tests are actually NDOD, i.e. order-dependent (`:122`, `:459-460`). `[INFERENCE]` The F3 control (`corpus/README.md` F3 row: N ≥ 3 byte-identical controls) is the other question — whether one exact argv prints the same stream — so the 82% figure must not be transferred to it, and three identical controls do not constitute evidence about detection.
- **A verdict that reads the clock is partly a verdict about the host.** S262's example test is flaky only because runs cross a 1500 ms limit, and its failure rate is 39.1% in isolation against 10.9% in its suite, 0%–20.1% by order (`:148-167`). `[INFERENCE]` Any gate that scores a timeout, or compares durations, is measuring load as well as code; the frozen C2 kill rule already declines that class — a crash or a timeout is not a kill (`.ufo/evidence/round-47/contract.json` C2 `statement`) — which keeps a load-sensitive outcome out of this round's mutation score. The same inference argues against a gate that reads a wall-clock budget without recording it.
- **The 82% has a narrow referent.** The quoted sentence is about checking whether a failure is due to flakiness (§I `:113-115`), on 26 modules from 23 projects (`:582-583`), with their flaky definition being both outcomes across reruns (`:29`). `[INFERENCE]` It is not a bound on verdict correctness, not a promise that five reruns settle a mutation score, and not measured on bash or JavaScript CLI suites.
- **Prediction features are code-history features of a different subject.** S261's features are flip rate, source churn over 54 days and the size of the latest pull request (§Abstract) for the test cases of one industrial system. `[INFERENCE]` Nothing in the abstract supports computing them for this lane's statements and gates, and the abstract reports no transfer experiment.

## What is not shown

- **No transfer to this lane's substrate.** S262's own threat section says the 26 modules from 23 projects may not generalise (`:582-584`) and that the numbers are sample-dependent — "likely that some specific numbers (e.g., number of NOD tests" (10 tokens, `:588`) "or failure rates) would change if the tests were run more times" (12 tokens, `:589`) — or on different machines; its population is Java projects run through Maven Surefire (`:25-26`). S261 reports one large-scale industrial software system and 200 histories and names no language (§Abstract). A case-insensitive search of the two snapshot texts returns 0 occurrences of `mutation`, `bash`, `Node` and `shell` in either, 0 of `Java` in S261, and 2 of `JavaScript` in S262 (both the JavaScript-in-Java sandbox test of §VI-B2); neither snapshot measures a mutation gate or a shell/Node gate, and no measurement of this lane appears in either.
- **S261's abstract is a result, not an ablation.** It gives one aggregate F1-score and the names of 3 features; it gives no precision or recall, no per-feature contribution, no baseline classifier, no CI-cost figure, and no replication. The class balance is the authors' fixed 100/100.
- **S262 states no cost in money or CI minutes.** It names a machine cost and a human cost (`:42`, `:47`) but reports no monetary or CI-minute figure: `$` occurs 0 times in the text. The cost reading belongs to `r8-flaky-cost-baseline.md` (S264) and is not restated here. It also states no mutation-testing result (`mutation` occurs 0 times in either snapshot).
- **The venue of S262 is not in its snapshot.** The text carries `©2020 IEEE` (`:63`) and no proceedings string; the PDF's own metadata names only TeX and pdfTeX 1.40.20. This entry therefore does not name a venue for S262.
- **S261's peer-review status is only what its comments field says.** The snapshot's comments cell states it is to be published at ICST 2023; the page carries no journal reference and no later version, so a later revision or publication is not claimed.

## Gate-relevant limits

- **F3 stays open.** These two documents state what the literature measures about prediction, rerun price and order dependence; they do not measure this lane's controls, and `corpus/QUALITY.md` criterion 11 still governs: a repeated-control clean verdict names its finite sample and never proves determinism.
- **No gate number moves.** Nothing here re-scores C1, C2 or C3; the only change this entry makes to the lane is a covered registry row (S261) and a cited uncounted row (S262).
- **S262 is the uncounted fourth row.** The three documents the round-47 C3 counter counts are arXiv:2302.09330, arXiv:2607.09345 and the Semantic Scholar record of DOI 10.1109/ICST60714.2024.00037; the Lam camera-ready continues the registry as S262 (from staged S158, by document) and the coverage counter does not count it (`.ufo/evidence/round-47/contract.json` C3 `extra_row`).
- **The locator is the fold, and the layout is lossy.** S262's text is two-column `-layout` extraction, so a sentence crossing the gutter is interleaved: this entry quotes only fragments inside one column, which is why two adjacent quotations sometimes complete one sentence. S261's abstract is one folded paragraph, so its quotations carry no line numbers. A reader re-checking a quotation must apply the same whitespace fold (NFKC, curly quotes to straight, dash normalisation, whitespace collapse) before searching the committed bytes.
- **Quotations were verified against the committed snapshots only.** The digest check and the phrase count in the `recheck:` line ran against those files on 2026-10-25; the live URLs were not fetched for this draft, and the recheck line above is the future command that would detect drift.
