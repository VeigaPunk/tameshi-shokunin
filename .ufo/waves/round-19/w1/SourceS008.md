# S008 — bounded source re-open for round-19 calibration

Accessed 2026-10-21.

- **Registry:** `corpus/SOURCES.md:19`, S008, *Practical Mutation Testing at Scale*, tier A, paper; canonical URL `https://arxiv.org/abs/2102.11378`; registered anchor: Abstract, arXiv:2102.11378v2.
- **Re-open method and outcome:** read the registered URL and the versioned anchor `https://arxiv.org/abs/2102.11378v2`; both returned the matching title, authors, and abstract via the arXiv reader/API. The v2 result explicitly identifies itself as `2102.11378v2`.
- **Located quote (18 words):** “Mutation testing is done incrementally, mutating only changed code during code review, rather than the entire code base.” — arXiv:2102.11378v2, Abstract, item (1), accessed 2026-10-21.
- **Observed internal mismatch:** `corpus/knowledge/mutation-case-kumitate-sources-check.md:1` labels S008 “queued” and “not yet a mined row”; `corpus/SOURCES.md:19` records it as `mined` and lists that note in `used-by`.
- **Scope and limits:** the paper's abstract supports the stated diff-scoped mutation approach, filtering/capping, and history-based operator selection. This re-open was of the abstract, not the full paper or its experimental details. The external source cannot establish the repository's current S008 status, whether its `used-by` metadata was durably corrected, receipt validity, or the five-defect calibration result.
- **Recommendation:** use S008 as scoped primary support for the mutation-method context already attributed to it; reject it as evidence for closing round-19's metadata/receipt defects or for the 0/5-to-5/5 correction count. Those require repository-state and failure-capable audit evidence. The mismatch above is repository evidence of the stale label, not a conclusion drawn from the paper.

No registry changes or tool installs were made.