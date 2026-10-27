# T51W2CritNoHarm — independent candidate falsifier

## Axes
Calibration (cold-read score/credit), depth, freshness, operability/tool scope; cross-claim no-harm.

## Findings

### F1 — Candidate independently trips the frozen cold-read floor; exact lost set is 20

**Evidence/command:**
```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/tameshi-r51/T51W2CritNoHarm \
 bash .ufo/evidence/round-51/no-harm.sh "$PWD" 6d8c11e378aa90b12650808e1b79270742935f15
python3 .ufo/evidence/round-21/coldread/measure.py --repo "$PWD" --rev 6d8c11e378aa90b12650808e1b79270742935f15
```
No-harm emitted `NOHARM coldread-floor score=6 credited=44 RED`; monitor confirms 44/64 and score 6, strict trace, no overrides. 20 lost headings, in order:
1. `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (131)
2. `## Restore discipline — before/after identity, not continuous non-write proof` (375)
3. `### The protocol — ordered, fail-closed` (827)
4. `### The boundaries — what a service run is not` (858)
5. `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` (921)
6. `### Using the ledger` (933)
7. `### Reading a receipt — the discipline` (965)
8. `### The tick and the pin read` (1021)
9. `### The tick, executed` (1164)
10. `### The receipt at this boundary` (1212)
11. `## The operator's runbook and the six-leg regression (round 10, measured)` (1272)
12. `### The six-leg regression — usage and this round's receipt` (1302)
13. `### The map — where a reader enters, artifact by artifact` (1380)
14. `### Gate/probe registry` (1499)
15. `## Seventh recorded case and full-page cold-read — round 16` (1754)
16. `### Round-16 gate/probe registry` (1806)
17. `## Live-tree re-pin and entry-command monitor — round 17` (1814)
18. `### Round-17 gate/probe registry — re-pin and monitor` (1846)
19. `## Eighth recorded case — round 18` (1905)
20. `### Round-26 gate/probe registry — report interop` (2132)

Per-section reasons are present in the command's JSON: 19 lose credit with at least one `input-drift:tools/mutate-and-run.sh` (some also drift on other inputs); the sole `no-ledger-entry` is section 20. The registry section (14) is input-drift, not `no-ledger-entry`. Thus the candidate is below the frozen credit/score floor absent the reading-bound re-key. This is the calibration axis; do not treat the reported expected fixture list as sufficient—the live candidate monitor reproduced it.

### F2 — Four-tool panel scope amendment is necessary and all allowlisted changes pass this monitor

Observed tools-scope: `[M:tools/mte-interop.py M:tools/mutate-and-run.sh M:tools/tally-audit-v2.py M:tools/tally-audit-v3.py M:tools/tally-audit.py ] ok`. This matches amended contract's four panel tools plus runner. Contract `contract.json` amendment 2 and `no-harm.sh:8-10,35-36` document scope. It establishes only allowlist compliance; it does not establish those changed tools are behaviorally safe (the contract delegates that to their tests/C3).

### F3 — S022 freshness rebasing is borne out, at the stated boundary

Observed `population=74 fresh=71 score=9 ok`, i.e. integer floor(10*71/74)=9. This supports precisely the amended frozen floor (`fresh>=71`, score>=9), not exact population invariance. Contract `contract.json:64` and `no-harm.sh:5-7,22-23` state why 73→74 is allowed: S022 status change adds a lawful population member.

### F4 — Other no-harm checks are green; no hidden RED among the 11 printed monitors

Full output: commandD `recorded_cases=10 depth_score=10 ok`; r45 coverage `rows=2 entries=2 C2_R45_PASS=true ok`; S160 count `1 ok`; registry rows `133 ok`; r46 coverage `3/3 C3_R46_PASS=true ok`; r47 coverage `3/3 C3_R47_PASS=true ok`; r49 generator exact expected 400-case result `violations=0 ... ok`; r50 shrinker `cases=14 failed=0 ok`. Tools-scope and freshness are separately detailed above. Only coldread-floor is RED. The no-harm script itself removes its configured scratch on exit; its output was observed from the candidate.

### F5 — Re-key is append-only relative to candidate ledger, but its strongest safety claim is bounded

Inspected `.ufo/evidence/round-51/coldread/refresh.py` and W1 instrument report `.ufo/waves/round-51/w1/T51ExecRekey.md` §§1,3,5. The refresh guard compares working-tree ledger parsed value to the ledger blob at CAND before writing (`refresh.py:164-169` per instrument report); it computes targets by BASE-vs-CAND monitor difference (`:176-186`), rejects no targets/absent or duplicate sections, and requires reader seats (`:204-206`). It appends one record per target, binding section hash, read revision, trace, seats and reports; prior entries are retained by append logic (`:224-243`, report lines 37-45). Reports describe fixture evidence of byte-identical prefix and successful 44→64 restoration, plus controls for missing entry/trace. This is a meaningful anti-overwrite guard, but not proof that a reader actually read or correctly assessed the candidate section: the contract calls it reading-bound re-key, and refresh's own `SCOPE` explicitly disclaims blind cold-read/recipe execution. Every newly credited section should have a named reader report with candidate bytes/excerpts; do not infer truth of claims from ledger append/trace alone. The exact target set is recomputed live, so do not hardcode the 20 fixture targets.

## Counterexample / impacted axes / smallest safe correction

Counterexample to no-harm-at-CAND: the unchanged strict cold-read monitor directly reports 44/64, score 6 where the frozen floor is 64/64 and score 8; therefore no-harm is not established at the content candidate. Impacted axis: calibration. Smallest safe correction is the already specified, correctly sequenced reading-bound re-key: recompute targets at actual CAND, obtain one named reader per target and evidence against candidate bytes, append entries and receipts without changing prior ledger entries, commit them at the measured revision, then run cold-read precheck and deciding run at that revision. Do not claim CAND itself is no-harm or use a shim/altered monitor.

Evidence pointers: `.ufo/evidence/round-51/no-harm.sh`; `.ufo/evidence/round-51/contract.json` (especially amendment 2); candidate monitor output from the exact command above; `.ufo/evidence/round-51/coldread/refresh.py`; `.ufo/waves/round-51/w1/T51ExecRekey.md` §§1,3,5.