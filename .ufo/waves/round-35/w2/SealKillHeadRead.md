# Round-35 W2 — SealKillHeadRead

**Axis:** depth. **Disposition:** one behaviorally divergent `kill` specimen authored for the held-out C1 set. The final specimen is accepted by the pinned v3 audit, a **CRITICAL false-accept**.

## Exact specimen for transcription

```json
{
  "copies": [
    {
      "class": "head-read-mask-st-js",
      "set": "kill",
      "edits": [
        [
          "  st_js=$?\n",
          "  st_js=$?\n  local leg_suffix=js; read -r \"st_$leg_suffix\" <<< '0'\n",
          1
        ]
      ]
    }
  ]
}
```

The single edit is against the pinned `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh`; the old byte string occurs exactly once. Immediately after the real `st_js=$?`, the new local suffix constructs the variable name `st_js` and `read` overwrites that captured status with zero. This is indirect `read`, not a plain reassignment. The tally block itself remains byte-identical to pristine.

## Behavioral receipt

The independent authoring driver extracts the pinned runner's tally block and executes it in Bash. For the copy it executes the exact new head statement on the supplied nine-status vector before the same block. Auto configs use actual `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` roots (six-character suffix); explicit configs use scratch roots. Each tuple is `(exit, full stdout)`; stdout is JSON-escaped verbatim, including its final newline. `equal` compares both exit and all stdout bytes.

Command:

```text
python3 /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/behavior_receipt.py > /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/behavior-receipt.tsv; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"
EXIT=0
```

The driver checked the pinned runner SHA and that the final copy was exactly the one-occurrence substitution. Pinned runner SHA-256: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`. Final copy SHA-256: `56d1d23c3b9d3393a90d5f7a5b5ea7150bdbed5cb03369bb98d27f51fcf89ee1`.

```text
CONFIG|VECTOR|PRISTINE(exit,full-stdout)|COPY(exit,full-stdout)|EQUAL
(0,1)|all-zero|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-all-zero (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-all-zero (kept)\n")|true
(0,1)|one-1|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-one-1 (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-one-1 (kept)\n")|false
(0,1)|one-2|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-one-2 (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-one-2 (kept)\n")|false
(0,1)|one-3|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-one-3 (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-one-3 (kept)\n")|false
(0,1)|one-255|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-one-255 (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-one-255 (kept)\n")|false
(0,1)|mixed-1|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-mixed-1 (kept)\n")|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-mixed-1 (kept)\n")|false
(0,1)|mixed-2|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-mixed-2 (kept)\n")|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-1-mixed-2 (kept)\n")|false
(1,0)|all-zero|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.4aaM6k (removed on PASS; --keep retains)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.4aaM6k (removed on PASS; --keep retains)\n")|true
(1,0)|one-1|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dLeyKA (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dLeyKA (removed on PASS; --keep retains)\n")|false
(1,0)|one-2|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.pqjr2V (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.pqjr2V (removed on PASS; --keep retains)\n")|false
(1,0)|one-3|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.TegB0y (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.TegB0y (removed on PASS; --keep retains)\n")|false
(1,0)|one-255|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.BuqLTq (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.BuqLTq (removed on PASS; --keep retains)\n")|false
(1,0)|mixed-1|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.mmi8yO (kept)\n")|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.mmi8yO (kept)\n")|false
(1,0)|mixed-2|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.oVsm6C (kept)\n")|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.oVsm6C (kept)\n")|false
(0,0)|all-zero|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-all-zero (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-all-zero (kept)\n")|true
(0,0)|one-1|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-one-1 (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-one-1 (kept)\n")|false
(0,0)|one-2|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-one-2 (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-one-2 (kept)\n")|false
(0,0)|one-3|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-one-3 (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-one-3 (kept)\n")|false
(0,0)|one-255|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-one-255 (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-one-255 (kept)\n")|false
(0,0)|mixed-1|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-mixed-1 (kept)\n")|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-mixed-1 (kept)\n")|false
(0,0)|mixed-2|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-mixed-2 (kept)\n")|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/roots/auto-0-keep-0-mixed-2 (kept)\n")|false
(1,1)|all-zero|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.M2eXbN (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.M2eXbN (kept)\n")|true
(1,1)|one-1|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.EeRaNv (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.EeRaNv (kept)\n")|false
(1,1)|one-2|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.js4fMn (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.js4fMn (kept)\n")|false
(1,1)|one-3|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.YvohdV (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.YvohdV (kept)\n")|false
(1,1)|one-255|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.8yTHKy (kept)\n")|(exit=0,stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.8yTHKy (kept)\n")|false
(1,1)|mixed-1|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.cabKmR (kept)\n")|(exit=2,stdout="REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.cabKmR (kept)\n")|false
(1,1)|mixed-2|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.kmrSQC (kept)\n")|(exit=1,stdout="REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.kmrSQC (kept)\n")|false
```

## Findings and ranking

- **CRITICAL — false-accept of a head-masked kill.** Final audit command:

  ```text
  python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/mutant-mutate-and-run.sh > /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/tool-observation.txt; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"
  EXIT=0
  ```

  The observed output (SHA-256 `46746e2b4740813443caccb89d80a96ae0c63d98f1def6b1fc3886d57c4e4e82`) is `CHECK head PASS legs=9`, `CHECK static PASS legs=9 operands=9 nlegs=9`, `CHECK runtime PASS vectors=30316 mismatched=0`, `CHECK harness PASS reference cases=9; faults rejected=34/34`, and `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`. This is only an observation of the tool, not the behavioral ground truth. The table above proves the copy diverges on every nonzero witness set, under all four triples. The head scanner counts literal leg names; `st_$leg_suffix` avoids a literal `st_js` occurrence, and the runtime oracle executes only the unchanged tally block, so the head `read` is not exercised by it.

- **BOUND — direct-name read is fail-closed.** The first literal-name attempt (`read -r st_js <<< '0'`, copy SHA-256 `e15507b3d50c39853a51c0778ef4491b3898f6c17a8282e25babee13a91cdd23`) was not selected because the audit rejects it at `head`, not the contract-required `runtime` check. Exact observation command: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/mutant-mutate-and-run.sh > /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/tool-observation.txt; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"` — exit 1. It reported `CHECK head FAIL legs=9; leg st_js appears 3 times in the head (want exactly 2: the local declaration and its bare st_x=$?)`; static, runtime and harness passed. Retained output SHA-256: `aa68fed5720feb8cb1703e93d72ada8f95b5b7bca637b97f9b1f521381a0cfed`. This establishes only that the direct-name form is caught; the final indirect `read` is not.

## What I could not break / limits

- Pin identity commands/results: `sha256sum /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/pristine-mutate-and-run.sh` (exit 0) returned runner `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/tally-audit-v3.py | sha256sum` (exit 0) returned tool `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-35/c1/c1-measure.py | sha256sum` (exit 0) returned counter `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`.
- All-zero is behaviorally identical under all four triples (four `true` rows); the single-status 1/2/3/255 vectors and both mixed vectors diverge under all four triples. For mixed-2 with `(1,1)`, exit remains 1 but full stdout differs (`failed=1 setup=3` versus `failed=1 setup=2`), confirming the comparison used the full output, not just exit status.
- No accept specimen was authored or evaluated in this seat; no conclusion about accept-side coverage is made. The sealed JSON is to be transcribed and committed by L1 after the freeze, per the contract.

## Evidence commands and files

- Pinned source extraction command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh > /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/pristine-mutate-and-run.sh` (exit 0); extracted bytes hash to the pinned runner SHA above.
- Final artifact hash command (exit 0): `sha256sum /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/pristine-mutate-and-run.sh /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/mutant-mutate-and-run.sh /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/mutant-literal-mutate-and-run.sh /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/behavior_receipt.py /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/specimen.json /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/behavior-receipt.tsv /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/tool-observation.txt`; outputs include final copy `56d1d23c3b9d3393a90d5f7a5b5ea7150bdbed5cb03369bb98d27f51fcf89ee1`, literal copy `e15507b3d50c39853a51c0778ef4491b3898f6c17a8282e25babee13a91cdd23`, driver `a0a5701d957b1825fd431a001bb1278bb5b4becbebc970d39916184b30b5270e`, JSON `ee87e3764c76d0364f31f49599434ea196fd27e9a57660e9b4c15c42f462f15c`, and receipt TSV `4cce43d075168e102fc63ee8f538a63848a7cac18f10d097b8aef939dea2042f`.
- Final and literal audit-output hash command (exit 0): `sha256sum /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/tool-observation.txt /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/tool-literal-observation.txt`; outputs are `46746e2b4740813443caccb89d80a96ae0c63d98f1def6b1fc3886d57c4e4e82` and `aa68fed5720feb8cb1703e93d72ada8f95b5b7bca637b97f9b1f521381a0cfed`, respectively.
- No tools were installed. Scratch artifacts are under `/fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/`; no runner, tool, counter, panel, lane, or fleet file was modified. The only repository file created by this seat is this report.
- Authoring-driver iteration note: the first literal-read receipt invocation `python3 /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/behavior_receipt.py > /fast/scratch/hyaku/tameshi-r35-w2/SealKillHeadRead/behavior-receipt.tsv; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"` exited 1 before vector execution. A helper assertion sliced the mutated runner at the pristine pre-insertion offset; the extraction assertion was corrected to locate the marker independently in the copy. The final command in the behavioral-receipt section completed with exit 0; the failed harness attempt is not behavioral evidence.
