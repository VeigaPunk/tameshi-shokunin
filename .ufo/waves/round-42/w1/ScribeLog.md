## Findings

Draft section for `LOG.md`; do not copy as an assertion of completed/deciding results. Base receipts show the motivating defects and `<deciding>` placeholders below are intentional.

```markdown
## 2026-10-25 — round 42: receipt reconciliation and attribute/output-flag write census v4

Motivating evidence: the calibration claim is motivated by the round-41 residual receipt asserting `present=false` for `.ufo/waves/round-41/residual/ResidualReceipts.md`, while the file exists; the C1 base receipt reports `m10=1` and only `records=3` of 6. The depth claim is motivated by the write-path census v3's three live false positives: `tools/context-capture.py:1682`, `tools/context-capture.py:1685`, and `tools/registry-replay.py:123`. The frozen contract records these surfaces and predicates in `.ufo/evidence/round-42/contract.json`.

- Claim C1 (calibration). Reconcile the self-assessment records with observed repo state across m6, m7, m8, m10 and m11. At base `c77c2b7e64d2e356381441ecf94abac03e984606`, receipt `.ufo/evidence/round-42/before/c1-at-base.stdout` reports `m10=1`, `records=3`, `C1_R42_PASS=false`; it identifies the stale `present=false` assertion for `ResidualReceipts.md`. Target: `self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 C1_R42_PASS=true`. Counting command: `python3 .ufo/evidence/round-42/calibration/measure.py --lane LANE --rev REV --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`.
- Claim C2 (depth, capability acquisition). Census v4 resolves attribute-bound destinations (`self.<attr>` through a same-class method return) and argparse output-flag (`--out`) destinations. At base `c77c2b7e64d2e356381441ecf94abac03e984606`, `.ufo/evidence/round-42/before/c2-at-base.stdout` reports `tool_absent=1 live_unflagged_v3=3 C2_R42_PASS=false`. The three live v3 sites are `tools/context-capture.py:1682`, `tools/context-capture.py:1685`, and `tools/registry-replay.py:123`. Target: `<deciding>`. Counting command: `python3 .ufo/evidence/round-42/census/measure.py --lane LANE --rev REV --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`.
- Freeze: `322b5cd32b4319a05340d249ae752d12a9e6b19f` (contract and both counters frozen before any seat score or deciding run; see `.ufo/evidence/round-42/contract.json`). Base revision: `c77c2b7e64d2e356381441ecf94abac03e984606`. Base receipts: `.ufo/evidence/round-42/before/`; control receipts: `.ufo/evidence/round-42/control/`.
- Deciding results: C1 `<deciding>`; C2 `<deciding>`. No deciding result is asserted in this draft.
```

Evidence / exact paths: contract `.ufo/evidence/round-42/contract.json:6-22,33-48`; C1 base output `.ufo/evidence/round-42/before/c1-at-base.stdout:1-3`; C2 base output `.ufo/evidence/round-42/before/c2-at-base.stdout:1`; style source `/home/vgpnk/Projects/shokunin/tameshi-shokunin/LOG.md:2092-2120`.

Could not check: the live tool's three v3 sites against source lines or any eventual deciding run; only the cited contract/base receipt and round-41 LOG style were inspected. No tool installs/updates; no lane product files edited.
