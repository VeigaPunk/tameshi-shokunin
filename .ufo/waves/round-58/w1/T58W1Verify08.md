# T58W1Verify08 — row verification

Base inspected: `2a32aa8228d5f86a85c81a923a3148bf792a9538`, detached scratch clone at `/fast/scratch/hyaku/tameshi-r58/T58W1Verify08/clone`.

All four assigned defects remain **open** at base. Proposed ledger status is open with a round-58 correction intent; no resolving commit is claimed. Evidence below comes from commands run against the detached base.

- **R54.2 — open.** Command: `git show BASE:corpus/lessons/round-54-verifier-spotcheck.md | grep -n -A2 -B1 R54.2` yielded line 110: the three pointers `7883e0e5`, `fe70474d`, `097985c1` conflict with receipt `freeze=077d431e`. No resolution in that passage. Proposed fix: reconcile freeze pointer throughout report/SCORECARD to the deciding receipt.
- **R54.3 — open.** Command: `git show BASE:corpus/lessons/round-54-verifier-spotcheck.md | grep -n -A2 -B1 R54.3` yielded line 112 describing the `total=14` citation versus 13. Independent receipt command `git show BASE:.ufo/evidence/round-54/before/c2.stdout | grep -n 'total='` yielded `C2_R54 ... total=13 ...`. Proposed fix: correct the SCORECARD total and disclosure wording.
- **R54.4 — open.** Command: `git show BASE:corpus/lessons/round-54-verifier-spotcheck.md | grep -n -A2 -B1 R54.4` yielded line 114, retaining stale `49280fe5` citation. Command: `git show BASE:.ufo/evidence/round-54/freeze.json | grep -n -E '077d431|8528ee85|c2/measure'` showed `c2/measure.py` pinned to `8528ee8555da068519af4159f5f9e0efac8b29de88a53534a7043d7ec007e790`. Proposed fix: cite the frozen digest.
- **R54.5 — open.** Command: `git show BASE:corpus/lessons/round-54-verifier-spotcheck.md | grep -n -E 'resolutions.json|minor_gaps|99c3bc8|25 findings in 12 sections'` yielded the defect at line 116 and extended comparison at 241–244: report counts conflict with committed artifacts (wave 1 25 vs 28; wave 2 report 22/9 vs artifacts/ledger 25/12). Proposed fix: re-derive both counts from committed readers and ledger, then correct count claims.

The JSON records evidence excerpts and planned correction intents for each row. No tools were installed. Scratch clone and work directory removed before handoff.
