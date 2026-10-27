# T52W3Read10 — cold-read

Candidate: `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`; section lines 1380–1463 inclusive.

## Findings
- F1: `“corpus/knowledge/mutation-case-*.md” (six at round 11; seven since round 16; eight since round 18; nine since round 26; ten since round 51)` — there is no round-11 mutation-case note among the candidate's ten `corpus/knowledge/mutation-case-*.md` files; the section's dated historical count/pointer is false at CAND1. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135 corpus/knowledge | grep 'mutation-case-'`.
- F2: `“plans/round-N.plan.md (latest plans/round-11.plan.md), plans/round-N-record-draft.md | each round's plan and record by convention (rounds 4–10; N is a placeholder, not a file — the concrete files are the round-4 through round-10 plan and record-draft pairs that plans/ holds)”` — candidate `plans/` has no `round-4` through `round-10` `record-draft.md` files, so the assertion that it holds those pairs is false. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135 plans | grep -E 'round-(4|5|6|7|8|9|10)\\.(plan|record-draft)\\.md|completion-evidence'`.

## Holds
Checked and found holding: `corpus/knowledge/operator-runbook.md` exists; its §0, §2, §3, §4, §5, §6, §7, §10 content headings are present; its cited authority-divergence anchor resolves to `SKILL.md:1249-1254` (the map's anchor `1294-1297` is elsewhere and should be interpreted at CAND1?); runbook scratch statement matches current tool's TMPDIR behavior; ledger exists and includes round-52 supersession at line 439; `service-limits.md`, `service-optin-protocol.md`, `fleet-suite-census.md`, `service-standing-state.md`, `tools/mutate-and-run.sh`, `corpus/README.md`, `plans/round-11.plan.md`, `plans/completion-evidence.md`, `LOG.md`, and `SCORECARD.md` exist. Count: 16 pointers checked. No tool installs.

## Summary
Two stale/false plan and case-note inventory statements found.
