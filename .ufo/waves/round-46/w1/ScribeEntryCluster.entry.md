source: S258 — https://arxiv.org/abs/2504.16777 — §Abstract — arXiv:2504.16777v1 — snapshot .ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html (sha256 28d2954d…)
verified-at: 2026-10-25
recheck: 365d — `curl -fsSL 'https://arxiv.org/abs/2504.16777' | grep -c 'co-occurring failures that share the same root causes'` → `3` (run 2026-10-25; the fetched page was 43,376 bytes, sha256 `28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14`, `cmp`-identical to the snapshot). A zero count means the abstract was reworded: reopen the page and re-locate every quote below before reusing this entry.
ground: F3 — determinism precondition, flaky-aware verdicts (`corpus/README.md` F3 row: one control per sweep → N ≥ 3 byte-identical controls, or a named mismatch). F8 is kept on the located premise alone: co-occurring failures are stated to share the same root causes; Inference: a shared cause is what makes two observations one observation.

# Flaky failures come in clusters, so a set of green reruns is not a set of independent observations

Snapshot: the arXiv abstract page of arXiv:2504.16777v1 [cs.SE], *Systemic Flakiness: An Empirical Analysis of Co-Occurring Flaky Test Failures* (Owain Parry, Gregory Kapfhammer, Michael Hilton, Phil McMinn), submitted 23 Apr 2025. Every quotation below was re-located in the extracted text of the committed snapshot; the number beside each quote is its whitespace-token count after the same fold the coverage counter applies, and 14 of the 15 located quotes do not occur in the committed package copy `.ufo/evidence/round-46/assimilation/package/r6-flaky-failures-cluster.md`.

## 1. What the snapshot states

**The property.** Flakiness is an outcome change with no code change: "Flaky tests produce inconsistent outcomes without code changes, creating major challenges for software developers" (14 tokens).

**The cost it is set against.** "An industrial case study reported that developers spend 1.28% of their time repairing flaky tests at a monthly cost of $2,250" (21 tokens).

**The finding.** "flaky tests often exist in clusters, with co-occurring failures that share the same root causes, which we call systemic flakiness" (20 tokens). The stated consequence for repair: "This suggests that developers can reduce repair costs by addressing shared root causes" (13 tokens). The stated framing: "This study represents an inflection point by challenging the deep-seated assumption that flaky test failures are isolated occurrences" (18 tokens).

**The data.** "We used an established dataset of 10,000 test suite runs from 24 Java projects on GitHub, spanning domains from data orchestration to job scheduling" (24 tokens); "It contains 810 flaky tests, which we levered to perform a mixed-method empirical analysis of co-occurring flaky test failures" (19 tokens).

**The measurement.** "We performed agglomerative clustering of flaky tests based on their failure co-occurrence" (12 tokens), "finding that 75% of flaky tests across all projects belong to a cluster, with a mean cluster size of 13.5 flaky tests" (22 tokens). The aggregate verdict in the abstract is "Systemic flakiness is significant and widespread" (6 tokens).

**The cheap substitute.** "Instead of requiring 10,000 test suite runs to identify systemic flakiness" (11 tokens) "we demonstrated a lightweight alternative by training machine learning models based on static test case distance measures" (17 tokens).

**The attributed causes.** "Through manual inspection of stack traces, conducted independently by four authors and resolved through negotiated agreement" (16 tokens) "we identified intermittent networking issues and instabilities in external dependencies as the predominant causes of systemic flakiness" (17 tokens).

## 2. What this says about the lane's F3 control count

The F3 rule counts byte-identical controls. The snapshot says the failures such controls probe are not scattered: most of them sit in clusters that share a root cause, and the clusters are large (mean 13.5 members over the authors' 810 flaky tests). Inference: N controls drawn from one cluster are one probe of one cause repeated N times, so the count of controls is an upper bound on independent evidence, and the count of distinct causes touched is the real bound. Inference: the clustering itself needed 10,000 suite runs to become visible, so a three-control sweep cannot detect clustering at all, and the F3 rule's N ≥ 3 is a floor on controls that bounds the distinct causes a sweep can have touched only from above; a sweep that draws several cases from one gate should record that they share a gate rather than scoring them as separate controls.

## 3. The F8 link, stated from the quoted sentences only

F8 asks for an expectation fixed outside the code under mutation (`corpus/README.md` F8 row). The located sentence above names what the members of a cluster have in common: "co-occurring failures that share the same root causes" (8 tokens). An expectation that reads one member of such a cluster therefore reads the cause the other members also carry. Inference: two survivors from one cluster supply one anchor, not two, so a per-survivor verdict table that does not record cluster membership overstates the number of independent anchors it holds.

## 4. Fixture-craft meaning for this lane (Inference)

- **Survivor lists are not independent observations.** Inference: if a survivor set contains several members of one flaky cluster, it is one finding counted N times; the classification should carry cluster membership beside each per-survivor verdict.
- **Rerun evidence is not independent either.** Inference: a green rerun of one member licenses nothing about its cluster, so rerun evidence and survivor lists are not independent when failures cluster.
- **Scope of the transfer.** The snapshot reports flaky *test failures* in 24 Java projects; it contains no data on mutation survivors, and the application to this lane's survivor sets is an inference, not a result of the paper.

## 5. Boundary of this entry

- The snapshot is the arXiv abstract page only: the extracted text has no journal-reference or comments field (zero occurrences of `Journal reference` and of `Comments`), and the visible venue facts are `arXiv:2504.16777v1 [cs.SE]`, `Submitted on 23 Apr 2025` and the submission-history line `Wed, 23 Apr 2025 14:51:23 UTC (79 KB)`. Whether the paper was later peer-reviewed is not stated in this snapshot, so no peer-review status is claimed here.
- The abstract reports the authors' own dataset and their own clustering of it; no gate of this lane is in it.
- The abstract gives one aggregate clustering figure and one mean cluster size. It gives no per-project cluster rate, no cluster-size distribution and no rerun-blindness rate; a same-job-rerun miss rate is not stated in this snapshot and is not restated in this entry.
- The paper body (PDF/HTML) is linked from the page but was not fetched; this entry rests on the abstract text alone.
