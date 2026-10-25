
source: S195 — https://arxiv.org/abs/2504.16777 — §Abstract — arXiv:2504.16777v1 (submitted 23 Apr 2025; CC BY 4.0), fetched 2026-10-23
verified-at: 2026-10-23
recheck: 365d — re-run `curl -fsSL 'https://arxiv.org/abs/2504.16777' | grep -c 'belong to a cluster, with a mean cluster size of 13.5'` (expect a non-zero count; the string was present in the copy fetched 2026-10-23)
ground: F8 (oracle anchoring as a survivor class); also F3

# Flaky failures come in clusters, so a set of green reruns is not a set of independent observations

## What the source states

S195 (Parry, Kapfhammer, Hilton & McMinn; *Systemic Flakiness: An Empirical
Analysis of Co-Occurring Flaky Test Failures*, arXiv:2504.16777, submitted
23 April 2025, CC BY 4.0) reports agglomerative clustering of flaky tests by
failure co-occurrence, "finding that 75% of flaky tests across all projects
belong to a cluster, with a mean cluster size of 13.5 flaky tests", and frames
the result as "challenging the deep-seated assumption that flaky test failures
are isolated occurrences".

## What this means for the lane's F8 and F3

- **The lane's survivor sets are not independent observations.** The lane
  classifies survivors one at a time against an independently anchored
  expectation (its F8 move). S195 shows that flaky *failures* cluster: a
  cluster's members share a cause. Inference: a survivor list that contains
  several members of one flaky cluster is one finding, not several — so the
  lane's classification should record *cluster membership* alongside the
  per-survivor verdict, or it will count one cause N times.
- **It sharpens the lane's determinism precondition.** A rerun that returns
  green says nothing about the other members of a flaky cluster (S140, round
  5: the same-job rerun misses 9.8 %–16.3 % of flaky failures in the first
  place). Inference: the lane's F3 protocol needs "rerun in a fresh
  environment" *and* an awareness of clusters — the green rerun of one case
  cannot license a clean verdict for its cluster.
- **What is still unmade.** The lane has not classified any survivor set
  against this, and it has no cluster data of its own. This source supplies
  the concept and the measurement method (co-occurrence clustering), not the
  lane's classification.

## Boundary of this entry

- S195 is a preprint (arXiv), not a peer-reviewed publication at the time of
  opening; it is tier A for its own scope (the clustering result and its
  method) and not for any broader claim about flakiness.
- The clustering is computed over failure co-occurrence in the authors' own
  data; the lane's own gates are not in it.

---
