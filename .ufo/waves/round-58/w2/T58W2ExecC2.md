# T58W2ExecC2 — C2 committed replay

Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534` (verified as newest lane commit at dispatch).

## Counter replay

Command: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/c2/measure.py --lane /fast/scratch/hyaku/tameshi-r58/T58W2ExecC2/clone --rev 8063d0a551fc5b3cb5a2d397da7353af53444534 --work /fast/scratch/hyaku/tameshi-r58/T58W2ExecC2/empty --explain`

Exit: `0`. Retained stdout ended:

```text
EXPLAIN shortfall rows=0
EXPLAIN shortfall executed=0
EXPLAIN shortfall mutants=0
EXPLAIN shortfall skill=0
EXPLAIN shortfall codes=0
EXPLAIN shortfall cell=0
EXPLAIN rows gate_rows=3 exits=0,2,3 missing_exits=none refusal_rows_without_known_code=none
EXPLAIN executed receipt-gate-accept expect=0 got=0 held
EXPLAIN executed receipt-gate-content-drift expect=3 got=3 held
EXPLAIN executed receipt-gate-unresolvable-certified expect=2 got=2 held
EXPLAIN mutants baseline-held=3/3
EXPLAIN mutant M1 accept-on-drift: killed by receipt-gate-content-drift(got=0)
EXPLAIN mutant M2 wrong-refusal-code: killed by receipt-gate-content-drift(got=3)
EXPLAIN mutant M3 exit-0-on-unresolvable: killed by receipt-gate-unresolvable-certified(got=0)
EXPLAIN skill_row 1 (verdict map=0 PASS; 2 certified revision unresolvable (`RECEIPT_REV_UNRESOLVABLE`); 3 refuse)
EXPLAIN codes tokens=['RECEIPT_REV_ABSENT', 'RECEIPT_REV_CONTENT_DRIFT', 'RECEIPT_REV_MISMATCH', 'RECEIPT_REV_UNRESOLVABLE'] unknown=[]
EXPLAIN cell gate emitted=['RECEIPT_REV_CONTENT_DRIFT'] exit=3 verdict=REFUSED; table cell carries=['RECEIPT_REV_CONTENT_DRIFT']
C2_R58: self=d4219039f02c rev=8063d0a551fc gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3 skill_row=1 codes_known=4/4 standing_cell=ok total=0 C2_R58_PASS=true
```

## Independent registered-row replay

On the detached C0 clone, each row was separately run with `python3 tools/registry-check.py --root CLONE --only <name>`; each command exited 0:

- `receipt-gate-accept`: `ROW receipt-gate-accept expect=0 got=0 held`; `REGISTRY_CHECK: held=1/1 superseded=0`.
- `receipt-gate-content-drift`: `ROW receipt-gate-content-drift expect=3 got=3 held`; `REGISTRY_CHECK: held=1/1 superseded=0`.
- `receipt-gate-unresolvable-certified`: `ROW receipt-gate-unresolvable-certified expect=2 got=2 held`; `REGISTRY_CHECK: held=1/1 superseded=0`.

## Executor-forgery falsifier

Inspected frozen wave-1 evidence `.ufo/waves/round-58/w1/T58W1RevengerC2-receipts/attack-out.txt`. Lines 47–60 record the bent-runner case reporting held=3/3, yet its M3 mutation was explicitly not killed (`old string not unique in gate`) and total=1/PASS=false. Crucially, lines 62–74 independently replay through the **real** registry-check: `c2-fx-ok` differs (`expect=0 got=3`), while drift and unresolvable hold. This establishes the bypass claim without modifying the frozen counter/target. Current C0 replay above runs the genuine entry point and all three receipt rows hold.

Machine-readable stdout, status values, and the falsifier receipt pointer are in `T58W2ExecC2.json`. Scratch data removed at command exit; no lane or fleet-repo tracked files were changed.
