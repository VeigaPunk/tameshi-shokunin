# Round 35 W2 — SealCfg00Guard

Seat: `SealCfg00Guard`. Scope: author one held-out **kill** specimen gated on `(auto=0, KEEP=0)`, using a construct different from public `cfg00-accept-swap`. Work/scratch stayed under `/fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/`; no checkout files or pinned artifacts were edited. No tools were installed.

## Ranked findings

- **BOUND — valid cfg00-only kill specimen.** The mutant changes the tally loop's `*)` SETUP arm, not the FAIL arm or the pre-FAIL guard used by public `cfg00-accept-swap`. It reclassifies each setup status as a pass only when `auto=0 && KEEP=0`. The behavioral receipt has 5 divergent rows, all under `(0,0)`, so this meets the kill rule without cross-config divergence.
- **BOUND — no observed effect in the other triples.** All 21 tested rows for `(0,1)`, `(1,0)`, and `(1,1)` have identical `(exit, full stdout)`; the `(0,0)` all-zero and one-1 rows are identical too. See the complete table below and `behavior_receipt.json` (sha256 `8e59e4451619cd74b2522f746296671f702c3e956826bd5a5af57c4acddcd52f`).
- **Not assessed:** I did not run `tally-audit-v3.py` on the copy. This report establishes the specimen's behavior independently; the parent-owned post-integration measurement decides the audit's classification. No claim that the tool accepts or rejects this specimen is made here.

## Pinned evidence and construction

Inputs were taken from dispatch revision `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` with read-only `git show`. `contract.json` at that revision is sha256 `a9eb2b97226ad192352f9da8cc32f3f719db22a93f14355a5e2d1306cea027c0`; its frozen-artifact entries pin the runner at `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`, the v3 tool at `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`, and C1 counter at `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` (contract lines 7–19). The pinned counter pin matches the extracted counter bytes. A4 (contract lines 99–114) names the real auto-root fix; A5 (115–127) names sealed provenance changes. The pinned public `cfg00-accept-swap.json` is sha256 `c5e5c65257235eb0c9e16dc9227182267bc1d8b85db0c280ab2f556bd3052d46` and edits the pre-FAIL `nfail` guard, unlike this SETUP-arm edit.

Pinned runner capture command (exit 0):

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh > /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/pristine-mutate-and-run.sh
```

The copy was derived from those bytes by the single JSON edit below. `behavior_receipt.py` checks the old string occurs exactly once and that applying the JSON edit produces the copy's complete runner text. The extracted tally block is `run_regression`'s `local nlegs=...` through its `exit 0` (pinned runner lines 1432–1470). The auto roots were generated using `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` and held constant within each config's pristine/copy pairs; explicit roots are listed in the table.

```json
{"copies":[{"class":"cfg00-setup-as-pass","set":"kill","edits":[["      *) nsetup=$((nsetup + 1)) ;;","      *) if [[ $auto -eq 0 && $KEEP -eq 0 ]]; then npass=$((npass + 1)); else nsetup=$((nsetup + 1)); fi ;;",1]]}]}
```

The specimen JSON file sha256 is `cba9a312a0ae0a7b9844aa697d654f55d87664b6d2ece15381ba094b502625bc`. The resulting copy runner sha256 (required copy-text hash) is **`8b3711ad2c5c55fa5d6d56dd526a85ef8f16622875fc4c34bc73879c9f5b22b2`**; pristine remains `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`.

Behavior command and exit:

```text
python3 /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/behavior_receipt.py > /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/behavior_receipt.json
EXIT=0
```

The driver sha256 is `9ac76c5ca2c3c1fc64b5a874bbd9eeb1705163fb12781e592dc90c863d706558`; its JSON receipt sha256 is `8e59e4451619cd74b2522f746296671f702c3e956826bd5a5af57c4acddcd52f`. `sha256sum` over the specimen, pristine/copy runners, driver, receipt, and pinned inputs exited 0; hashes above are its exact output. The behavior driver ran Bash on each extracted block with nine leg statuses and recorded each process exit and complete stdout; stderr was empty for every run.

Vectors (nine leg statuses each): `all-zero=[0×9]`; `one-1=[1,0×8]`; `one-2=[2,0×8]`; `one-3=[3,0×8]`; `one-255=[255,0×8]`; `mixed-1-2=[0,1,2,0×6]`; `mixed-1-2-3-255=[1,2,3,255,0×5]`. In table tuples, each `\n` represents one literal LF byte in stdout; no output line is omitted.

## Behavioral receipt

### `(auto=0, KEEP=1)` — root `/fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1`

| Vector | Pristine `(exit, full stdout)` | Copy `(exit, full stdout)` | Equal? |
|---|---|---|---|
| all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | yes |
| one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | yes |
| one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | yes |
| one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | yes |
| one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | yes |
| mixed-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | yes |
| mixed-1-2-3-255 | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep1 (kept)\n")` | yes |

### `(auto=1, KEEP=0)` — real auto root `/tmp/tameshi-r4-2-regression.uLYAzQ`

| Vector | Pristine `(exit, full stdout)` | Copy `(exit, full stdout)` | Equal? |
|---|---|---|---|
| all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (removed on PASS; --keep retains)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (removed on PASS; --keep retains)\n")` | yes |
| one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | yes |
| one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | yes |
| one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | yes |
| one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | yes |
| mixed-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | yes |
| mixed-1-2-3-255 | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.uLYAzQ (kept)\n")` | yes |

### `(auto=0, KEEP=0)` — root `/fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0`

| Vector | Pristine `(exit, full stdout)` | Copy `(exit, full stdout)` | Equal? |
|---|---|---|---|
| all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | yes |
| one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | yes |
| one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | no |
| one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | no |
| one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | no |
| mixed-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | no |
| mixed-1-2-3-255 | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r35-w2/SealCfg00Guard/explicit-auto0-keep0 (kept)\n")` | no |

### `(auto=1, KEEP=1)` — real auto root `/tmp/tameshi-r4-2-regression.dP3OIP`

| Vector | Pristine `(exit, full stdout)` | Copy `(exit, full stdout)` | Equal? |
|---|---|---|---|
| all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | yes |
| one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | yes |
| one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | yes |
| one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | yes |
| one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | yes |
| mixed-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | yes |
| mixed-1-2-3-255 | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dP3OIP (kept)\n")` | yes |
