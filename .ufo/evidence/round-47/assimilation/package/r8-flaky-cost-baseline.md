
source: S207 — https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICST60714.2024.00037?fields=title,abstract,year,venue,authors,externalIds — the Semantic Scholar record of DOI 10.1109/ICST60714.2024.00037, "Cost of Flaky Tests in Continuous Integration: An Industrial Case Study" (Leinen, Elsner, Pretschner, Stahlbauer, Sailer, Jürgens; IEEE ICST 2024), opened 2026-10-24; the record carries the publisher's abstract verbatim, the DOI, the DBLP key `conf/icst/LeinenEPSSJ24` and the green open-access pointer
verified-at: 2026-10-24
recheck: 180d — `curl -fsSL 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICST60714.2024.00037?fields=title,abstract,year,venue,authors,externalIds' | grep -c 'Automatically rerunning a test costs 0.02 cents'` (expect a non-zero count; the string was present in the copy opened 2026-10-24)
ground: F7 (the cost baseline a re-sweep cadence trades against)

# The expensive branch of a flaky test is the failed pipeline, not the rerun

## What was observed

From the publisher's own abstract, over five years of a commercial project with
~30 developers and ~1M SLoC, drawing on CI test logs, VCS commits, issue
tickets and tracked work time:

- "the time spent dealing with flaky tests in the studied project represents at
  least 2.5% of the productive developer time", split into 1.1 % investigating
  suspected flaky failures, 1.3 % repairing them and 0.1 % building monitoring
  tools;
- "Contrary to most other studies, we find the cost for rerunning tests to be
  negligible and inexpensive. Automatically rerunning a test costs 0.02 cents,"
  while "not rerunning and thus letting the pipeline fail results in a manual
  investigation costing $5.67".

## What is inferred

- **This is the F7 cost baseline, and it inverts the intuition the lane had
  been carrying.** The lane's F7 has been treating a re-sweep as a cost to be
  minimised. This paper prices the two branches: the rerun is nearly free
  (0.02 cents) and the *failed pipeline* is not ($5.67 of human investigation).
  So the trade is not "re-sweep versus no re-sweep" priced in reruns; it is
  "re-sweep versus a human investigating a red build", and the second is ~280×
  the first.
- **That makes the cadence question a different question than the lane has been
  asking.** If a rerun is cheap and a red build is expensive, the cadence
  should be set by the cost of a *false red* (a rerun that hides a real
  failure), not by the cost of a rerun. The guarantee in S205 (over 95 % of
  individual test failures still reported) is the quantity that bounds that
  false-red cost, and the two rows have to be read together.
- **The 2.5 % figure is the honest ceiling on any flaky-tolerance budget.**
  It is a floor ("at least"), measured on one commercial project, and it
  includes the monitoring tooling the lane's own corpus would also have to
  build. It is a cost *of the problem*, not of a mitigation.

## What is still unknown

- Only the abstract was opened: the cost model itself, the derivation of the
  factors, and the per-project variance are not read here.
- The publisher's own article page renders as a JavaScript shell carrying no
  abstract text, and the open full text at mediaTUM timed out twice this
  round; the Semantic Scholar record carries the publisher's abstract verbatim
  and is the reachable copy, which is why this row is tier B and not A.
- One commercial project. Whether the 2.5 % and the $5.67 transfer to a
  thirty-developer fleet of small shell gates is not established by this source.

---
