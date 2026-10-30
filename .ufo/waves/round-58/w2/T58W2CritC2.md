# T58W2CritC2 — installed C2 attack

Revision: `8063d0a551fc5b3cb5a2d397da7353af53444534` (confirmed lane HEAD at dispatch).
Axes: operability, fixture/output correspondence, execution provenance.

## Installed state
Frozen counter: exit 0; `total=0 C2_R58_PASS=true`; rows held 3/3, mutants killed 3/3. Exact command/output: `T58W2CritC2-receipts/c0-counter.json`.

Independently ran each installed row through C0 registry-check in detached C0 scratch checkout (`--root CLONE --only NAME --json`). All stdout expectations match the actual fixture outputs:

| Row | Gate exit | Held | Actual summary |
|---|---:|---|---|
| receipt-gate-accept | 0 | true | receipts=1 ok=1 refused=0 codes=none verdict=PASS |
| receipt-gate-content-drift | 3 | true | receipts=1 ok=0 refused=1 codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED |
| receipt-gate-unresolvable-certified | 2 | true | error=unresolvable-certified receipts=1 verdict=REFUSED codes=RECEIPT_REV_UNRESOLVABLE |

Every command, expectation and full stdout is retained in `T58W2CritC2-receipts/rows.json` and per-row receipts. No installed-row semantic defect found. Both bare refusal-code elements actually occur on their fixtures. They duplicate stronger full-line expectations, but neither is an unreachable code accepted merely by static membership. Gate source lines 149–152 and 190–194 match these observed branches.

## Counterexample: known executor forgery independently reproduced
Extracted only CHEAT_GATE/BENT_RC literal bytes from wave-one attack.py (did not execute that artifact's driver). Used the unchanged frozen counter's fixture builder in own scratch; ran its CLI on that isolated forged revision. Counter returned exit 0, held 3/3, mutants 3/3, total=0 PASS=true. The bent executor only checks whether the gate file is dirty; it never executes rows.

The genuine C0 executor against the identical forged fixture rejects `c2-fx-ok`: expected 0, got 3, missing `verdict=PASS`. Actual gate stdout says `detail=sham` and verdict REFUSED. The other two fixture rows held. Exact commands/output: `forgery-counter.json` and `forgery-real-executor.json`; reproduction driver: `review.py`, all under the receipts directory.

Impacted axes: operability and integrity of execution/mutation evidence. This is a fixable measurement defect, not a newly discovered installed registry-row defect. Smallest safe present correction: preserve the frozen target and do not treat its numerical PASS as admission evidence. A successor contract should bind an independently trusted executor for baseline and mutants. No judgment, admission, source edit, or contract change performed here.

## Hygiene
Only own wave-2 report/receipt paths and isolated scratch were written. No tools installed. Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2CritC2` removed before yielding.
