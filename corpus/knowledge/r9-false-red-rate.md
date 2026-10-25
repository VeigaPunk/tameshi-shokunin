source: S260 — https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json — post body "Flaky Tests at Google and How We Mitigate Them" (Micco, 2016-05-27) — snapshot .ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json (sha256 434d8658…)
verified-at: 2026-10-25
recheck: 365d — `curl -fsSL 'https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json' | sha256sum` → `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929  -` (run 2026-10-25, byte-identical to the committed snapshot); `curl -fsSL 'https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json' | grep -c '84% of the transitions we observe from pass to fail'` → 1; `curl -fsSL 'https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json' | grep -c 'Almost 16% of our tests have some level of flakiness'` → 1
ground: F3 (determinism precondition, flaky-aware verdicts) — the false-red prior a single red observation carries; F7 (incremental re-sweep granularity) — what a rerun attempt costs in discovery latency

# Four red builds in five are not defects, by the publisher's own numbers

## What the snapshot states

S260 is the publisher's per-post Atom feed. The post body is the HTML string at `entry.content.$t`; the snapshot is one JSON line (0 newlines, 8,353 bytes, sha256 `434d8658…`), so citations below name the field, not a line number. The feed's `entry.link[rel=alternate].href` names `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html` — the rendered page this lane already holds as S026 — so the feed is a second carrier of the same document, not a second document: the two rows' figures must agree, and opening the feed adds no claim the page does not carry.

**Definition and corpus rate.** A flaky result is "a test that exhibits both a passing and a failing result with the same code" (15 words); across the corpus "we see a continual rate of about 1.5% of all test runs reporting a" (14 words) flaky result. The rate is a steady state, not a backlog being worked off: "the insertion rate is about the same as the fix rate" (11 words).

**Reach.** "Almost 16% of our tests have some level of flakiness associated with them" (13 words); equivalently "more than 1 in 7 of the tests written by our world-class engineers occasionally fail" (15 words) in a way the code change did not cause.

**Post-submit transitions.** The CI system flags a passing test that transitions to failing so the submission can be investigated, and "about 84% of the transitions we observe from pass to fail involve a flaky test" (15 words). The lane's S026-ground entry `corpus/knowledge/repeated-control-precondition.md` already quotes this sentence from the rendered page; the feed states it in the same words.

**The default mitigation is a rerun, and the post prices it as a delay.** "build monitors typically wait for additional CI cycles to run this test again" (13 words), "adding to the delay of identifying real problems and increasing the pool of changes that could contribute" (17 words). At project scale the arithmetic is the post's: "If 1.5% of test results are flaky, 15 tests will likely fail" (12 words) in "the average project contains 1000 or so individual tests" (9 words).

**A declared-flaky mechanism, with its latency stated.** The post's own gate is "causing it to report a failure only if it fails 3 times in a row" (15 words); "This reduces false positives, but encourages developers to ignore flakiness in their own tests" (14 words). The wait is explicit: "The breakage will not be discovered until 3 executions of the test complete, or 45 minutes" (16 words) for a 15-minute integration test.

**Masking, stated as an observed habit rather than a hypothesis.** "It is quite common to ignore legitimate failures in flaky tests due to the high number of false-positives" (18 words), generalised as "It is human nature to ignore alarms when there is a history of false signals coming from a system" (19 words). The quarantine strategy is named together with what it hides: "A tool that monitors the flakiness of tests and if the flakiness is too high, it automatically quarantines the test" (20 words), which "could easily mask a real race condition or some other bug in the code being tested" (16 words).

**The publisher's own direction.** "we are seeing promising correlations with features that should enable us to identify a flaky result accurately" (17 words) without re-running the test — an aspiration in the post, not a measured result.

## What is inferred

- **Inference — the false-red prior.** If about 84% of observed pass→fail transitions in a large corpus involve a flaky test, one red observation is weak evidence of a defect. A verdict rule that reads a single red as a defect carries a false-red share of that order unless it states an attempt budget or an independent witness. The lane's own verdicts are where this bites: a leg that flips a declared class on one run is not yet a kill, and a gate that fails once is not yet a broken gate.
- **Inference — same-job rerun blindness.** The publisher's default mitigation reruns in later CI cycles, and the post reports the wait as a delay, not as identification. A gate that reruns inside one job without a declared attempt count cannot separate "flaked three times in a row" from "broken" — the post's own declared-flaky mechanism needs exactly three consecutive failures before it will say so.
- **Inference — the discovery-latency term.** Attempts multiply test duration: the post's 15-minute test becomes 45 minutes at three attempts. A per-attempt rerun budget is therefore priced in executions × duration, and that term is bounded by the test's runtime, not by the flake rate.
- **Inference — suppression without a stated floor converts a known failure into an ignored one.** Because developers are reported to ignore legitimate failures among flaky ones, a cadence that suppresses red builds without a stated detection floor moves a real failure into the ignored class. The floor is the condition under which the cadence is being paid for at all, so it belongs in the claim, not in the report.
- **Inference — a prior on the lane's own variance.** The same figure is a prior on how much of the lane's measured run-to-run variance is worth chasing: in a large corpus a red that does not reproduce is the expected case, which is why the lane's F3 repeated-control entry treats one clean control as finite-sample agreement rather than as proof of determinism.

## What is not claimed

- One company's post-submit suite, at its scale, in 2016. The denominator is not this lane's gate fleet, and nothing here measures the lane's own false-red rate.
- The relationship between the 84% transition rate and the 1.5% result rate is the publisher's; it is not derived here.
- The post's mitigation strategies are reported, not adopted: no claim is made that quarantine, declared-flaky flags or automatic reruns transfer to this lane's corpus.
- The package copy of this entry priced a rerun, priced a manual investigation and attributed a detection-floor percentage to S156. None of those figures is restated: the lane holds no row carrying those prices, and this snapshot states no such numbers. What is kept is only the ratio the snapshot itself states.
- F3 stays open. This entry supplies the false-red prior a flaky-aware verdict is judged against; it does not measure the lane's controls, and it does not raise the frontier's status.
