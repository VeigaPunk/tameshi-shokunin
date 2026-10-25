
source: S212 — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html — "Flaky Tests at Google and How We Mitigate Them" (Micco; Google Testing Blog, 2016-05), the post body extracted and persisted at lanes/tameshi/round9/evidence/google-flaky-blog-text.txt
verified-at: 2026-10-24
recheck: 180d — `curl -fsSL 'https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html' | sed -e 's/<[^>]*>//g' | grep -c '84% of the transitions we observe from pass to fail involve a flaky test'` (expect a non-zero count; the string was present in the copy fetched 2026-10-24)
ground: F7 (the false-red rate a re-sweep cadence is priced against)

# Four red builds in five are not defects

## What was observed

From Google's own post-submit test system: "about 84% of the transitions we
observe from pass to fail involve a flaky test", and "If 1.5% of test results
are flaky, 15 tests will likely fail" in a project of roughly a thousand tests.
The post also names the habit the rate produces: "It is quite common to
ignore legitimate failures in flaky tests due to the high number of
false-positives".

## What is inferred

- **The cadence question stops being a judgement call.** Round 8 priced a
  rerun at 0.02 cents against a $5.67 manual investigation of a red build, and
  named the missing input as the false-red rate. With 84 % of pass-to-fail
  transitions flaky, the expected cost of *not* re-sweeping is dominated by
  the false red, and the expected cost of *over*-sweeping is bounded by the
  guarantee round 8's `S156` states — over 95 % of individual test failures
  still reported. The cadence is then chosen to preserve that floor, and the
  arithmetic is the lane's to do, not a matter of taste.
- **The masking sentence is the reason the floor has to be stated.** If most
  red builds are false and developers are known to ignore legitimate failures
  among them, then a cadence that suppresses red builds without preserving
  detection silently converts a known failure into an ignored one. The floor
  is not a nicety on the cost model; it is the condition under which the cost
  model is being paid at all.
- **It also reframes what the lane's own flakiness work is measuring.** The
  lane's F3 and F5 work measures whether the lane's own gates are hermetic.
  Google's figure says that in a large corpus the majority of red-to-green
  transitions are noise, which is a prior on how much of the lane's own
  measured variance is worth chasing.

## What is still unknown

- The figure is one company's system at one scale, and is from 2016; the
  denominator is their post-submit suite, not a small gate fleet.
- The post's own mitigation strategy is not read here, and no claim is made
  that Google's approach transfers to the lane's corpus.
- The relationship between the 84 % transition rate and the 1.5 % result rate
  is Google's, not derived here.

---
