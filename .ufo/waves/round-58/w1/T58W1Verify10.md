# T58W1Verify10 — row verification

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. Scratch clone detached at base. No installs or upgrades; no checks/builds/tests run. Scratch removed before yield.

| Item | Status at base | Finding and evidence |
|---|---|---|
| R54.10 | fixed | `git log --all --format='%H %s' --grep=R54.10` located `0a2010acd1e92e4e332774050825e21bcfc7e079`. `git show BASE:SCORECARD.md | sed -n '2694,2705p'` outputs ER-R54-10: old 0/30 cited to controls-a; corrected receipt says `rekeyed=0/7`, with `0/30` attributed to r53-counter-at-88afa941.stdout. |
| R55.1 | open | `git show BASE:corpus/lessons/round-55-verifier-spotcheck.md | sed -n '118,122p'` preserves the issue: measured `4c04c1d3`, green receipts name C0/demo, and `after/c2.stdout` is truncated. No resolution found in inspected base lesson. Planned fix intent: committed measured-revision verdict or correctly retargeted claim. |
| R55.2 | open | `git show BASE:corpus/lessons/round-55-verifier-spotcheck.md | sed -n '123,126p'` says the report claims total=0 while cited receipt is total=1/PASS=false. `git grep` of base found round-57 narrative references but no correction repairing this counterfactual discrepancy. Planned fix intent: quote receipt value or identify the distinct run. |
| R55.3 | fixed | `git log --format='%H %s' --all -- SCORECARD.md` includes restatement commit `2f5512a8ab0771fb2eee463ec16db359174f5edd`. `git grep` at base finds SCORECARD R56 row: prior 46/64 score 6 then 64/64 score 8, 18/18 re-key/readers, restate=8; lines 2747-2750. Round 56 lesson lines 54 and 89 independently state re-measured restoration and row agreement. |

Commands also used: checked base lesson files, ran `git log --grep` for item ids, and searched base SCORECARD/QUALITY/round-56/round-57 lesson for correction tokens. R54.10 excerpt includes whole-token key `controls-a.stdout`; R55.1 excerpt contains `4c04c1d3`; R55.2 excerpt contains `total=1`; R55.3 excerpt contains `64/64`. Fixed-row excerpts are present at the planned base and do not contain ACK_WORD-style acknowledgements.
