source: S258 — https://arxiv.org/abs/2504.16777 — §Abstract — arXiv:2504.16777v1 — snapshot .ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html (sha256 28d2954d…)
verified-at: 2026-10-25; extraction tool `.ufo/evidence/round-45/freshness/measure.py` sha256 `ba64041f49ffcf15bb0d881604a5fe3ccf9d24e56f72bef055035fbe3d27c6ed`; lane revision `eada0b36d4c9e6380d111d2037acd97cdf91d2eb`; receipt `.ufo/evidence/round-46/after/entry-rechecks.stdout`
recheck: 365d — `curl -fsSL 'https://arxiv.org/abs/2504.16777' | grep -c 'co-occurring failures that share the same root causes'` → `3` (run 2026-10-25; the fetched page was 43,376 bytes, sha256 `28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14`, `cmp`-identical to the snapshot). A zero count means the abstract was reworded: reopen the page and re-locate every quote below before reusing this entry.
ground: F3 — determinism precondition, flaky-aware verdicts (`corpus/README.md` F3 row: one control per sweep → N ≥ 3 byte-identical controls, or a named mismatch). F8 is kept on the located premise alone: co-occurring failures are stated to share the same root causes; Inference: a shared cause is what makes two observations one observation.

# Flaky failures come in clusters (published); that green reruns are therefore not independent observations is this lane's inference

Snapshot: the arXiv abstract page of arXiv:2504.16777v1 [cs.SE], *Systemic Flakiness: An Empirical Analysis of Co-Occurring Flaky Test Failures* (Owain Parry, Gregory Kapfhammer, Michael Hilton, Phil McMinn), submitted 23 Apr 2025. Every quotation below was re-located in the extracted text of the committed snapshot; the number beside each quote is its whitespace-token count after the same fold the coverage counter applies, and 14 of the 15 located quotes do not occur in the committed package copy `.ufo/evidence/round-46/assimilation/package/r6-flaky-failures-cluster.md`.

## 1. What the snapshot states

**The property.** Flakiness is an outcome change with no code change: "Flaky tests produce inconsistent outcomes without code changes, creating major challenges for software developers" (14 tokens).

**The cost it is set against.** "An industrial case study reported that developers spend 1.28% of their time repairing flaky tests at a monthly cost of $2,250" (21 tokens).

**The finding.** "flaky tests often exist in clusters, with co-occurring failures that share the same root causes, which we call systemic flakiness" (20 tokens). The stated consequence for repair: "This suggests that developers can reduce repair costs by addressing shared root causes" (13 tokens). The stated framing: "This study represents an inflection point by challenging the deep-seated assumption that flaky test failures are isolated occurrences" (18 tokens).

**The data.** "We used an established dataset of 10,000 test suite runs from 24 Java projects on GitHub, spanning domains from data orchestration to job scheduling" (24 tokens); "It contains 810 flaky tests, which we levered to perform a mixed-method empirical analysis of co-occurring flaky test failures" (19 tokens).

**The measurement.** "We performed agglomerative clustering of flaky tests based on their failure co-occurrence" (12 tokens), "finding that 75% of flaky tests across all projects belong to a cluster, with a mean cluster size of 13.5 flaky tests" (22 tokens). The aggregate verdict in the abstract is "Systemic flakiness is significant and widespread" (6 tokens).

**The cheap substitute.** "Instead of requiring 10,000 test suite runs to identify systemic flakiness" (11 tokens) "we demonstrated a lightweight alternative by training machine learning models based on static test case distance measures" (17 tokens).

**The attributed causes.** "Through manual inspection of stack traces, conducted independently by four authors and resolved through negotiated agreement" (16 tokens) "we identified intermittent networking issues and instabilities in external dependencies as the predominant causes of systemic flakiness" (17 tokens).

## 2. What this does and does not say about the lane's F3 control count

The F3 move (`corpus/README.md` F3 row) is "N ≥ 3 byte-identical controls, or a named mismatch". A byte-identical control is one exact argv run N times (`tools/repeat-control.py:7-9`: "runs one exact argv N >= 3 times"), so an F3 sweep holds one case repeated, not several cases: the paper's unit — distinct flaky tests that fail together — does not exist inside such a sweep, and the count of those controls bounds independent evidence from above by construction (`corpus/QUALITY.md` criterion 11: a repeated-control clean verdict "never proves determinism"), not because of anything S258 reports.

What the abstract can bear on is evidence drawn from different cases. Inference: if the lane's cases behave like the authors' flaky tests, cases that fail together would share a cause, so several of them are fewer independent observations than their number; the snapshot states the authors' clustering used a 10,000-run dataset and that they demonstrated a lightweight non-rerun alternative (quoted in §1), and it states nothing about the failures this lane's controls probe or about three-control sweeps. Inference: a sweep that draws several cases from one gate should record that they share a gate rather than scoring them as separate controls.

## 3. The F8 link (the premise is located; the reading is inference)

F8 (`corpus/README.md` F8 row: oracle anchoring as a survivor class; next move "one survivor classified against an independently anchored expectation") is the question this section reads the abstract against; the abstract says nothing about test oracles or mutation survivors. The located premise is that the members of a cluster have a shared cause: "co-occurring failures that share the same root causes" (8 tokens). Inference: if the members of a cluster share a root cause, an expectation anchored on one member's observed outcome is not evidence about the other members' outcomes, so two survivors from one cluster would supply one anchor, not two, and a per-survivor verdict table that does not record cluster membership would overstate the number of independent anchors it holds.

## 4. Fixture-craft meaning for this lane (Inference)

- **Survivor lists are not independent observations.** Inference: if a survivor set contains several members of one flaky cluster, it is one finding counted N times; the classification should carry cluster membership beside each per-survivor verdict.
- **Rerun evidence is not independent either.** Inference: a green rerun of one member licenses nothing about its cluster, so rerun evidence and survivor lists are not independent when failures cluster.
- **Scope of the transfer.** The snapshot reports flaky *test failures* in 24 Java projects; it contains no data on mutation survivors, and the application to this lane's survivor sets is an inference, not a result of the paper.

## 5. Boundary of this entry

- The snapshot is the arXiv abstract page only: the extracted text has no journal-reference or comments field (zero occurrences of `Journal reference` and of `Comments`), and the visible venue facts are `arXiv:2504.16777v1 [cs.SE]`, `Submitted on 23 Apr 2025` and the submission-history line `Wed, 23 Apr 2025 14:51:23 UTC (79 KB)`. Whether the paper was later peer-reviewed is not stated in this snapshot, so no peer-review status is claimed here.
- The abstract reports the authors' own dataset and their own clustering of it; no gate of this lane is in it.
- The abstract gives one aggregate clustering figure and one mean cluster size. It gives no per-project cluster rate, no cluster-size distribution and no rerun-blindness rate; a same-job-rerun miss rate is not stated in this snapshot and is not restated in this entry.
- The paper body (PDF/HTML) is linked from the page but was not fetched; this entry rests on the abstract text alone.
