# Round 35 W2 — SealKillStaticOp

## Attack and outcome

Authored one held-out `kill` specimen for the requested sum-preserving tally-operand miscount. The edit replaces the tally-loop operand `"$st_citecheck"` with `"$st_js"`: the tally still has nine operands, but counts `st_js` twice and drops `st_citecheck`. The changed operand is in the pinned runner's tally block (`tools/mutate-and-run.sh:1432-1470`; the operand list is at `:1433`).

Source was obtained read-only from commit `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` with `git show`; the pinned blob and local runner both hash to `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (106,538 bytes). No clone/checkout was created because the fleet scope prohibits mutating Git; the exact pinned blob was used instead. No frozen file, lane file, sibling report, or w1 report was changed. No tool was installed.

The source-of-truth experiment extracted the pinned tally block and ran pristine and mutated block text with Bash on seven vectors, under the four `(auto,KEEP)` combinations. Each auto trial used a newly created `/tmp/tameshi-r4-2-regression.*` root; a pristine/copy pair shared the same root string, with the directory recreated before each execution. Explicit trials used fresh absolute `/tmp` roots. All stdout below is complete; JSON quoting preserves newlines and the final newline.

### Ranked findings

- **CRITICAL — candidate behavior equivalence is false.** The copy diverges in 20/28 config×vector trials. A lone status `1`, `2`, `3`, or `255` at the dropped `st_citecheck` position changes pristine `FAIL`/`SETUP` to copy `PASS` in every config; the mixed status-2/status-1 vector changes `FAIL` to `SETUP` in every config. This is a valid behavioral kill specimen. This rank is about pristine-vs-copy equivalence, **not** a verdict that the frozen v3 audit claim is false.
- **BOUND — v3/counter detection verdict unmeasured here.** Neither `tally-audit-v3.py` nor the C1 counter was run; per the task, the tool is not the behavioral ground truth, and the parent owns post-integration checks. No acceptance/rejection claim about this specimen is made.
- **HYGIENE — none observed.** No tool install or external substrate change.

## Specimen JSON

```json
{
  "copies": [
    {
      "class": "sum-preserving-operand-miscount-static",
      "set": "kill",
      "edits": [
        ["\"$st_citecheck\"", "\"$st_js\"", 1]
      ]
    }
  ]
}
```

The one edit matched exactly once. The resulting copy runner text is 106,531 bytes, sha256 `71a66c5a611d408fe08c3618a18f30fe6d4e43308e36ee1f074420547c4f695c`. The serialized specimen sha256 is `66003bb4914fc01fa1c8e69dd77b0f962b7de54866a6e2197afa0a5f65fe727b`.

## Behavioral receipt

Operand vector order is `st_js, st_kagi, st_tsu, st_mado, st_checklist, st_claims, st_roundgate, st_sourcescheck, st_citecheck`. Commands and pin hashes: `git show` of the pinned runner exited 0, emitted 106,538 bytes, sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`; the complete receipt harness command exited 0 and recorded 28 rows (20 divergent, 8 equal). See command details below the table.

| Config | Vector | Status vector | Root | Pristine (exit, full stdout) | Copy (exit, full stdout) | Equal? |
|---|---|---|---|---|---|---|
| `auto=0,KEEP=1` | `all-zero` | `[0, 0, 0, 0, 0, 0, 0, 0, 0]` | `/tmp/tameshi-r35-sealkill-explicit.1fnaypwb` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.1fnaypwb (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.1fnaypwb (kept)\n")` | `true` |
| `auto=0,KEEP=1` | `one-1-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r35-sealkill-explicit.sv4cmlz0` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.sv4cmlz0 (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.sv4cmlz0 (kept)\n")` | `false` |
| `auto=0,KEEP=1` | `one-2-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 2]` | `/tmp/tameshi-r35-sealkill-explicit.xhibxant` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.xhibxant (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.xhibxant (kept)\n")` | `false` |
| `auto=0,KEEP=1` | `one-3-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 3]` | `/tmp/tameshi-r35-sealkill-explicit.13lmic08` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.13lmic08 (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.13lmic08 (kept)\n")` | `false` |
| `auto=0,KEEP=1` | `one-255-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 255]` | `/tmp/tameshi-r35-sealkill-explicit.l6ay32rz` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.l6ay32rz (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.l6ay32rz (kept)\n")` | `false` |
| `auto=0,KEEP=1` | `mixed-1-at-js-and-citecheck` | `[1, 0, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r35-sealkill-explicit.jg5gw5e2` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.jg5gw5e2 (kept)\n")` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.jg5gw5e2 (kept)\n")` | `true` |
| `auto=0,KEEP=1` | `mixed-2-at-kagi-and-1-at-citecheck` | `[0, 2, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r35-sealkill-explicit.4qqiz7an` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.4qqiz7an (kept)\n")` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.4qqiz7an (kept)\n")` | `false` |
| `auto=1,KEEP=0` | `all-zero` | `[0, 0, 0, 0, 0, 0, 0, 0, 0]` | `/tmp/tameshi-r4-2-regression.otb58fmu` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.otb58fmu (removed on PASS; --keep retains)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.otb58fmu (removed on PASS; --keep retains)\n")` | `true` |
| `auto=1,KEEP=0` | `one-1-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r4-2-regression.msiabezp` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.msiabezp (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.msiabezp (removed on PASS; --keep retains)\n")` | `false` |
| `auto=1,KEEP=0` | `one-2-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 2]` | `/tmp/tameshi-r4-2-regression.re6hab2j` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.re6hab2j (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.re6hab2j (removed on PASS; --keep retains)\n")` | `false` |
| `auto=1,KEEP=0` | `one-3-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 3]` | `/tmp/tameshi-r4-2-regression.w5m0h3qf` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.w5m0h3qf (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.w5m0h3qf (removed on PASS; --keep retains)\n")` | `false` |
| `auto=1,KEEP=0` | `one-255-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 255]` | `/tmp/tameshi-r4-2-regression.40309yjl` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.40309yjl (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.40309yjl (removed on PASS; --keep retains)\n")` | `false` |
| `auto=1,KEEP=0` | `mixed-1-at-js-and-citecheck` | `[1, 0, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r4-2-regression.oktcsamr` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.oktcsamr (kept)\n")` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.oktcsamr (kept)\n")` | `true` |
| `auto=1,KEEP=0` | `mixed-2-at-kagi-and-1-at-citecheck` | `[0, 2, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r4-2-regression.xi7kmgu8` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.xi7kmgu8 (kept)\n")` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.xi7kmgu8 (kept)\n")` | `false` |
| `auto=0,KEEP=0` | `all-zero` | `[0, 0, 0, 0, 0, 0, 0, 0, 0]` | `/tmp/tameshi-r35-sealkill-explicit.1qbn4wo3` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.1qbn4wo3 (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.1qbn4wo3 (kept)\n")` | `true` |
| `auto=0,KEEP=0` | `one-1-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r35-sealkill-explicit.s8lw7yz4` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.s8lw7yz4 (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.s8lw7yz4 (kept)\n")` | `false` |
| `auto=0,KEEP=0` | `one-2-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 2]` | `/tmp/tameshi-r35-sealkill-explicit.81u4r67o` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.81u4r67o (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.81u4r67o (kept)\n")` | `false` |
| `auto=0,KEEP=0` | `one-3-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 3]` | `/tmp/tameshi-r35-sealkill-explicit.d44kooyy` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.d44kooyy (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.d44kooyy (kept)\n")` | `false` |
| `auto=0,KEEP=0` | `one-255-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 255]` | `/tmp/tameshi-r35-sealkill-explicit.w966jgwy` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.w966jgwy (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.w966jgwy (kept)\n")` | `false` |
| `auto=0,KEEP=0` | `mixed-1-at-js-and-citecheck` | `[1, 0, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r35-sealkill-explicit.73o6dq44` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.73o6dq44 (kept)\n")` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.73o6dq44 (kept)\n")` | `true` |
| `auto=0,KEEP=0` | `mixed-2-at-kagi-and-1-at-citecheck` | `[0, 2, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r35-sealkill-explicit.3sanbikp` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.3sanbikp (kept)\n")` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r35-sealkill-explicit.3sanbikp (kept)\n")` | `false` |
| `auto=1,KEEP=1` | `all-zero` | `[0, 0, 0, 0, 0, 0, 0, 0, 0]` | `/tmp/tameshi-r4-2-regression.789gvfzy` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.789gvfzy (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.789gvfzy (kept)\n")` | `true` |
| `auto=1,KEEP=1` | `one-1-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r4-2-regression.vd7zac2_` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.vd7zac2_ (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.vd7zac2_ (kept)\n")` | `false` |
| `auto=1,KEEP=1` | `one-2-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 2]` | `/tmp/tameshi-r4-2-regression.dfujmxtv` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dfujmxtv (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dfujmxtv (kept)\n")` | `false` |
| `auto=1,KEEP=1` | `one-3-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 3]` | `/tmp/tameshi-r4-2-regression.cex1hxe_` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.cex1hxe_ (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.cex1hxe_ (kept)\n")` | `false` |
| `auto=1,KEEP=1` | `one-255-at-citecheck` | `[0, 0, 0, 0, 0, 0, 0, 0, 255]` | `/tmp/tameshi-r4-2-regression.wyyk0qr4` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.wyyk0qr4 (kept)\n")` | `(exit=0, stdout="REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.wyyk0qr4 (kept)\n")` | `false` |
| `auto=1,KEEP=1` | `mixed-1-at-js-and-citecheck` | `[1, 0, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r4-2-regression.mqo8ei_p` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.mqo8ei_p (kept)\n")` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.mqo8ei_p (kept)\n")` | `true` |
| `auto=1,KEEP=1` | `mixed-2-at-kagi-and-1-at-citecheck` | `[0, 2, 0, 0, 0, 0, 0, 0, 1]` | `/tmp/tameshi-r4-2-regression.tlxp940m` | `(exit=1, stdout="REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.tlxp940m (kept)\n")` | `(exit=2, stdout="REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.tlxp940m (kept)\n")` | `false` |

## Commands, evidence, and bounds

Exact pin-check command (read-only):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh | sha256sum
```

Exit 0; output hash `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`. The same hash was obtained from the local runner path. The receipt harness's internal exact source command was `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh`; exit 0, 106,538 bytes, same sha256.

Behavior command (exit 0; prints `HARNESS_EXIT=0`):

```sh
python3 /fast/scratch/hyaku/tameshi-r35-w2/SealKillStaticOp/receipt.py; rc=$?; printf 'HARNESS_EXIT=%s\n' "$rc"; exit "$rc"
```

The harness's recorded result: `OPERANDS=9 ST_JS=2 ST_CITECHECK=0`, `ROWS=28 DIVERGENT=20 EQUAL=8`, copy runner sha256 `71a66c5a611d408fe08c3618a18f30fe6d4e43308e36ee1f074420547c4f695c`. All scratch artifacts are under `/fast/scratch/hyaku/tameshi-r35-w2/SealKillStaticOp/`; no package/tool changes. The output is a bounded witness, not a run of the audit tool or C1 counter.

## What did not diverge / could not be established

- The all-zero vector remained identical for all four config rows (table rows 14, 21, 28, 35). The mixed vector with `st_js=1` and `st_citecheck=1` also remained identical for all four configs (rows 19, 26, 33, 40): both blocks tally two failures because the dropped status equals the duplicated status. These are the eight equal receipts; the other 20 show behavioral divergence.
- No claim is made that every vector diverges. No claim is made about whether v3 accepts or kills this specimen: invoking the tool/counter was intentionally left to the parent integration gate.
- No blocker to specimen authoring. The only setup deviation was replacing the requested temporary clone/checkout with read-only `git show` to honor the no-mutating-Git fleet constraint; pinned and working-tree runner bytes matched exactly.
