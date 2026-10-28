# T56W2ExecGateOnC0 — C0 receipt-revision gate

## Result
Ran `receipt-revision-gate.py` against the supplied C0 certified commit and frozen surface. The gate correctly refuses receipts whose declared revision is stale relative to C0's protected bytes, and refuses receipts with no revision token. These refusals are expected, not gate defects: a receipt without a revision cannot certify C0; a stale revision is only acceptable if all listed surface paths are identical. The explicit accept-arm receipt naming C0 passes (exit 0).

## Refusals
All commands below used `--lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --certified c0137451f5b7f22d65f748fc69f1b181f55e1378 --paths /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/control/frozen-surface.paths --receipt <path>:verdict`.

- `.ufo/evidence/round-56/before/c1.stdout`: exit 3, `RECEIPT_REV_CONTENT_DRIFT` (rev `981c5e8b20a2`; changed protected measure/control/contract paths). Correct refusal.
- `.ufo/evidence/round-56/before/c2.stdout`: exit 3, `RECEIPT_REV_CONTENT_DRIFT` (rev `c3e2ca9f0207`; changed protected measure/contract/control/SKILL paths). Correct refusal.
- `.ufo/evidence/round-56/before/c2-at-base.stdout`: exit 3, `RECEIPT_REV_ABSENT`. Correct refusal.
- W1 C0-associated `precheck-base.stdout`, monitor summary JSONs (`monitor-base`, `monitor-base-noexplain`, `monitor-d33053f7`, `monitor-floor`), `demo-monitor.txt`, `precheck-worktree-demo.txt`, mutant `diff-M1_precheck_ok.txt`, and `.exit` receipts: exit 3, `RECEIPT_REV_ABSENT`. Correct refusal: these contain no revision token.
- W1 monitor text receipts `monitor-base.txt` and `monitor-base-summary.json`: exit 3, `RECEIPT_REV_CONTENT_DRIFT` at revisions `981c5e8b20a2...`; correct refusal.
- W1 `monitor-d33053f7.txt`: exit 3, `RECEIPT_REV_CONTENT_DRIFT` at `d33053f7552d`; correct refusal.
- W1 mutant `C_M1_precheck_ok.out` and `.meta`: exit 3, `RECEIPT_REV_UNRESOLVABLE` at synthetic revision `5aef3c...`; correct refusal because that revision is not resolvable in lane.
- W1 mutant `base_M1_precheck_ok.out` and `.meta`: exit 3, `RECEIPT_REV_CONTENT_DRIFT` at base `981c5e8b20a2...`; correct refusal.

The full executed output (including exact paths, commands, changed-path details and exit codes) is retained in the execution transcript. Sweep included all files found under round-56 evidence and W1 receipts whose names contain `precheck`, `monitor`, or `c0`; unrelated receipts were not treated as C0 monitor/precheck inputs.

## Accept arm
A scratch receipt containing `VERDICT: rev=c0137451f5b7f22d65f748fc69f1b181f55e1378 C1_R56_PASS=true` passed: exit 0, `GATE OK ... revs=c0137451f5b7f22d65f748fc69f1b181f55e1378`, summary `receipts=1 ok=1 refused=0 codes=none verdict=PASS`.

## Exact command for L1 to cite
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --certified c0137451f5b7f22d65f748fc69f1b181f55e1378 --paths /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/control/frozen-surface.paths --receipt <receipt-path>:verdict`

No tools installed or updated. No production or frozen evidence files modified.