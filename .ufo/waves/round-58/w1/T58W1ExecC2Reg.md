# T58W1ExecC2Reg — C2 registry operability

Executed in an isolated shared clone detached at base `2a32aa8228d5f86a85c81a923a3148bf792a9538`; verified `git -C <clone> rev-parse --show-toplevel` matched the clone path before commits. No lane files were edited. The patched draft was copied to the clone, then the requested round-58 `c1`, `c2`, `control`, `controls.sh`, `no-harm.sh`, `deciding-run.sh`, `contract.json`, and `freeze.json` instruments were overlaid.

## Registry delta

`git -C <clone> diff -- tools/registry.json` showed exactly two additions to `expect.stdout_contains`, with no other registry edits:

- `receipt-gate-content-drift`: `RECEIPT_REV_CONTENT_DRIFT`
- `receipt-gate-unresolvable-certified`: `RECEIPT_REV_UNRESOLVABLE`

The output showed each as one added array element on the corresponding row.

## Patched preview

Committed patched registry and overlaid instruments in the scratch clone. Ran:

`python3 -I <clone>/.ufo/evidence/round-58/c2/measure.py --lane <clone> --rev <patched-rev> --work <scratch>/work-patched --explain`

Verbatim counter line:

`C2_R58: self=d4219039f02c rev=194f86a68e6c gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3 skill_row=1 codes_known=4/4 standing_cell=ok total=0 C2_R58_PASS=true`

The detailed output showed all six shortfall categories at zero, three executed gates held, and 3/3 mutants killed.

## Registry gate execution

Ran `python3 <clone>/tools/registry-check.py --root <clone> --only <name>` for each of `receipt-gate-accept`, `receipt-gate-content-drift`, and `receipt-gate-unresolvable-certified`. Exact row outcomes:

- `ROW receipt-gate-accept expect=0 got=0 held` / `REGISTRY_CHECK: held=1/1 superseded=0`
- `ROW receipt-gate-content-drift expect=3 got=3 held` / `REGISTRY_CHECK: held=1/1 superseded=0`
- `ROW receipt-gate-unresolvable-certified expect=2 got=2 held` / `REGISTRY_CHECK: held=1/1 superseded=0`

The tool warned that live `--root` mode may write into the lane; the root supplied here was the disposable clone, not the lane.

## Red-before control

Restored the base registry bytes in the clone, committed that as a second preview revision, and ran the same counter against that revision. Verbatim line:

`C2_R58: self=d4219039f02c rev=c89ee679d82b gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3 skill_row=1 codes_known=4/4 standing_cell=ok total=2 C2_R58_PASS=false`

The explain output attributed the two shortfalls to refusal rows missing recognized codes: `receipt-gate-content-drift` and `receipt-gate-unresolvable-certified`. Thus patched preview passed while red-before failed as required. Scratch was removed by the shell cleanup trap. No tools were installed or updated.

## Files

- `.ufo/waves/round-58/w1/T58W1ExecC2Reg.json`
- `.ufo/waves/round-58/w1/T58W1ExecC2Reg.md`

Risk/blocker: none observed for the requested clone preview. This is a scratch-clone preview; the parent must integrate the registry change at a deciding revision and run the round-level gate after integration.
