## Findings
- F1: “Cases 5–6 were still not embedded at this boundary” — tool source lists `bash-checklist-run` and `js-claims-check` as legs 5 and 6 (command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:tools/mutate-and-run.sh | awk 'NR>=88&&NR<=100'`).
- F2: “their rows carry no `REGRESSION` line — named debt” — ledger §5/ER-3 records the subsequent embedding: the regression now has four legs in the older historical passage, while later ledger row 5/6 are actual measured cases; this statement describes earlier debt as current boundary state (command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | awk 'NR>=275&&NR<=290'`).

## Holds
- Checked 5 pointers: `tools/mutate-and-run.sh:1222-1303` materializes pinned blobs; tool leg list `:88-97` contains four earlier legs as well as later entries; protocol `:59-62` states re-pin-not-reinterpret; ledger historical append preserves old measured rows and names follow-ups; no section source pointer establishes these precise 2026-10-14 runtime outcomes as re-executed at CAND1.
- The dated 2026-10-14 receipt is accurately historical; its dates and recorded outcomes are not, by themselves, stale-claim findings.
## Summary
Two stale claims found: legs 5–6 are embedded in CAND1 and the ledger records their measurements.
