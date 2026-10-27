## Findings
- F1: “(mutation-case-kimi-census.md:20-21)” — this relative pointer resolves to a missing `corpus/lessons/` path at CAND1; the note is at `corpus/knowledge/mutation-case-kimi-census.md`.
- F2: “(mutation-case-kagi-census.md:27-35,42-43)” — this relative pointer resolves to a missing `corpus/lessons/` path at CAND1; the note is at `corpus/knowledge/mutation-case-kagi-census.md`.
- F3: “(gates-survey-kumitate.md:19-31)” — this relative pointer resolves to a missing `corpus/lessons/` path at CAND1; the note is at `corpus/knowledge/gates-survey-kumitate.md`.
- F4: “(gates-survey-kagi.md:44-47)” — this relative pointer resolves to a missing `corpus/lessons/` path at CAND1; the note is at `corpus/knowledge/gates-survey-kagi.md`.

## Holds
Checked and holding (4 pointers): `tools/mutate-and-run.sh:434` and `:579-583`; `SKILL.md:377-378` and `:377-380` (restore wording); `corpus/README.md` G-R2-1 row and its knowledge-path target; `corpus/knowledge/mutation-case-kimi-census.md`, `corpus/knowledge/mutation-case-kagi-census.md`, `corpus/knowledge/gates-survey-kumitate.md`, `corpus/knowledge/gates-survey-kagi.md` exist at CAND1 and contain the cited historical evidence. The section's dated history is not treated as a finding.

Commands showing the findings: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -e 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:<path>` (fails for each cited `corpus/lessons/` path); `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135` (shows corrected `corpus/knowledge/` targets).

## Summary
- 4 stale corpus pointers recorded.
- 4 pointer families checked as holding.
- Section SHA-256: `d15097cf3a0dafdb3f3f8847eb81bbc60d73d66598fd299b5c95786395871bbc`.
