# T57W2ExecNoHarmScope — no-harm tools-scope fix and C0 run

## Staged
`.ufo/waves/round-57/w2/T57W2ExecNoHarmScope/stage/.ufo/evidence/round-57/no-harm.sh` (only `tools-scope` block + two header comment lines changed; installed by L1).

New tools-scope: the sorted set of `git diff --name-status --no-renames BASE REV -- tools` tokens must EQUAL exactly
`A:tools/cold-read-forecast.py A:tools/fixtures/receipt-gate/{accept.receipt,drift.paths,drift.receipt} M:tools/registry.json`.
Equality (not just per-token admit) means a missing or extra path is RED; no glob, `M:tools/receipt-revision-gate.py` is no longer admitted (C0 does not touch it; the old script, run at C0, printed RED on the very five real changes).

## RED proof (receipts/tools-scope-red-proof.txt; scratch clone of the lane at C0, one fixture commit each, `git reset --hard C0` between)
GREEN at C0; RED for: extra M:tools/pbt-staged-id.py, M:tools/receipt-revision-gate.py, extra A:tools/new-tool.py, fourth fixture file, deleted fixture (D), forecast tool missing. Old script at C0: RED (contrast).

## Full no-harm at C0 (receipts/no-harm-at-c0.out), BASE=5e35699…, REV=C0=ca75c26…
Scratch clone of the lane checked out at C0 plus ONE fixture commit (333efea) overlaying only `.ufo/evidence/round-57/` (copy of the lane dir, 12 added files incl. c1/, c2/, control/, contract.json, controls.sh, deciding-run.sh, and no-harm.sh = the staged one; round-57 `tools` overlay: none; ledger `corpus/routed-defects.json` NOT overlaid so old49-ledger reads C0's committed 49 rows). Script run with LANE=clone, REV=C0 (git objects at C0; the overlay commit only supplies the working-tree instruments). Wall 212 s.
```
commandD ok | coldread-floor score=6 credited=46 RED | r45-freshness 74/71 score 9 ok | r45-coverage ok | S160-count 1 ok
registry-rows-not-below-140 145 ok | r46-coverage ok | r47-coverage ok | tools-scope [5 paths] ok | registry-rows-not-shrunk 57->60 ok
r49-generator-capability ok | r50-shrinker-selftest 14/0 ok | r53-scratch-hygiene 0 ok | ledger-not-shrunk 609=609 ok
sources-not-shrunk 142->145 ok | r56-gate-selftest 19/19 ok | registry-check-full held=49/53 (>=48) ok | old49-ledger 49=49 ok
```
Only RED: `coldread-floor` — by design at C0 (C0 changed pinned inputs).

## Cold-read at C0 (receipts/coldread-at-c0.json; full measure outputs beside it)
BASE: score 8, 64/64. C0: score 6, credited 46/64, 18 headings lost (none regained, none uncovered at base). 16 lost to `input-drift` (pinned inputs corpus/SOURCES.md ×12, tools/registry.json ×10, tools/context-capture.py ×8, tools/registry-check.py ×8, tools/repeat-control.py ×7, corpus/QUALITY.md ×5, corpus/README.md ×5, others ≤3); 2 as `no-ledger-entry`: `## Standing rules`, `### Gate/probe registry` (headings re-written/new in C0). Note: tools/registry-check.py and context-capture.py are unchanged by C0; their drift is via pinned inputs/transitive trace, not a file edit. Heading list with start lines and per-heading reasons is in the JSON (`lost_headings_at_c0_vs_base`).

## Notes
- First attempt at the full run died silently (backgrounded with `&` while a second cold-read measure ran concurrently); rerun alone via async job completed cleanly. No tools installed. Scratch removed.
