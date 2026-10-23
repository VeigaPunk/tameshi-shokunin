# Round-35 W2 — SealStdoutDetail

## Scope and result

Authored one held-out **kill** specimen against runner pin `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. The extracted tally block's first output line carries the verdict/counts; its second line is `REGRESSION_WORKDIR` and has no count field (pinned runner lines 1462–1468). I therefore attacked the second-line `(kept)` vs `(removed on PASS; --keep retains)` behavior using a nested config conjunct in the cleanup branch. This is distinct from public `workdir-branch-swap`, which changes the outer branch condition.

The copy differs from pristine on **1 of 28** required config×vector cases: all-zero under `(auto,KEEP)=(1,1)`. It is identical on the other 27. This establishes the specimen's `kill` label by exit/full-stdout behavior. I did **not** run `tally-audit-v3.py` on it, so this report makes no tool accept/reject or C1 claim verdict.

## Specimen JSON

```json
{
  "copies": [
    {
      "class": "workdir-keep-cleanup-nested-config",
      "set": "kill",
      "edits": [
        [
          "  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n",
          "  else\n    if [[ $auto -eq 1 && $KEEP -eq 1 ]]; then\n      printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n      rm -rf \"$root\"\n    else\n      printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    fi\n  fi\n  exit 0\n",
          1
        ]
      ]
    }
  ]
}
```

The old byte string matched the pinned runner once. Copy runner text SHA-256: `db4579edbee069cb1ac47534092f16fff3822973b05e6bfa3af94d3dc6207dae`.

## Behavioral receipt

**Procedure/evidence.** The command `python3 /fast/scratch/hyaku/tameshi-r35-w2/SealStdoutDetail/authoring.py` exited `0`. Its pinned `git show` exited `0`; it extracted the block beginning at `local nlegs=9 ...` through the pass-path `exit 0`, wrapped the block in a Bash function, and ran pristine and copy separately for every table cell. The script did not invoke the audit tool. Both `(auto=1)` roots came from the runner's real template using `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`; the command exited `0` for each. Explicit-workdir roots were under the scratch directory. Each pair used the same root string; roots were recreated between runs as needed. All Bash runs had empty stderr.

Root values (the table's `Rxx` tokens are exact substitutions in stdout):

- `R01`, `(0,1)`: `/fast/scratch/hyaku/tameshi-r35-w2/SealStdoutDetail/work/roots/a0-k1`
- `R10`, `(1,0)`: `/tmp/tameshi-r4-2-regression.viK4KM`
- `R00`, `(0,0)`: `/fast/scratch/hyaku/tameshi-r35-w2/SealStdoutDetail/work/roots/a0-k0`
- `R11`, `(1,1)`: `/tmp/tameshi-r4-2-regression.NuMAfi`

The seven vectors, in tally operand order, were: `all-zero=[0,0,0,0,0,0,0,0,0]`; `one-1=[1,0,0,0,0,0,0,0,0]`; `one-2=[2,0,0,0,0,0,0,0,0]`; `one-3=[3,0,0,0,0,0,0,0,0]`; `one-255=[255,0,0,0,0,0,0,0,0]`; `mixed-fail-setup=[1,2,0,0,0,0,0,0,0]`; `mixed-multiple-setup=[2,3,255,0,0,0,0,0,0]`.

Tuple registry for the table below. Each tuple is `(exit, FULL stdout)`; `\n` denotes the literal LF byte, including the final newline. `{R}` is replaced by the exact root listed above.

- `K@R`: `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: {R} (kept)\n")`
- `D@R`: `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: {R} (removed on PASS; --keep retains)\n")`
- `F@R`: `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: {R} (kept)\n")`
- `S@R`: `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: {R} (kept)\n")`
- `MF@R`: `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: {R} (kept)\n")`
- `S3@R`: `(2, "REGRESSION: SETUP (cases=9 passed=6 cannot-verify=3)\nREGRESSION_WORKDIR: {R} (kept)\n")`

| Config `(auto,KEEP)` | Vector | Pristine tuple | Copy tuple | Equal? |
|---|---|---|---|---|
| (0,1) R01 | all-zero | K@R01 | K@R01 | yes |
| (0,1) R01 | one-1 | F@R01 | F@R01 | yes |
| (0,1) R01 | one-2 | S@R01 | S@R01 | yes |
| (0,1) R01 | one-3 | S@R01 | S@R01 | yes |
| (0,1) R01 | one-255 | S@R01 | S@R01 | yes |
| (0,1) R01 | mixed-fail-setup | MF@R01 | MF@R01 | yes |
| (0,1) R01 | mixed-multiple-setup | S3@R01 | S3@R01 | yes |
| (1,0) R10 | all-zero | D@R10 | D@R10 | yes |
| (1,0) R10 | one-1 | F@R10 | F@R10 | yes |
| (1,0) R10 | one-2 | S@R10 | S@R10 | yes |
| (1,0) R10 | one-3 | S@R10 | S@R10 | yes |
| (1,0) R10 | one-255 | S@R10 | S@R10 | yes |
| (1,0) R10 | mixed-fail-setup | MF@R10 | MF@R10 | yes |
| (1,0) R10 | mixed-multiple-setup | S3@R10 | S3@R10 | yes |
| (0,0) R00 | all-zero | K@R00 | K@R00 | yes |
| (0,0) R00 | one-1 | F@R00 | F@R00 | yes |
| (0,0) R00 | one-2 | S@R00 | S@R00 | yes |
| (0,0) R00 | one-3 | S@R00 | S@R00 | yes |
| (0,0) R00 | one-255 | S@R00 | S@R00 | yes |
| (0,0) R00 | mixed-fail-setup | MF@R00 | MF@R00 | yes |
| (0,0) R00 | mixed-multiple-setup | S3@R00 | S3@R00 | yes |
| (1,1) R11 | all-zero | K@R11 | D@R11 | **no** |
| (1,1) R11 | one-1 | F@R11 | F@R11 | yes |
| (1,1) R11 | one-2 | S@R11 | S@R11 | yes |
| (1,1) R11 | one-3 | S@R11 | S@R11 | yes |
| (1,1) R11 | one-255 | S@R11 | S@R11 | yes |
| (1,1) R11 | mixed-fail-setup | MF@R11 | MF@R11 | yes |
| (1,1) R11 | mixed-multiple-setup | S3@R11 | S3@R11 | yes |

**What I could not break:** The first `REGRESSION:` line, including its verdict and count fields, was identical in every pair. The exit code and full stdout were identical in 27/28 cells; only the `(1,1)` all-pass workdir line diverged. This is the bounded negative for every other tested config/vector cell, not a claim about untested vectors.

## Exact retained evidence

- Pinned bytes: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh | sha256sum` → exit `0`, SHA-256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`.
- Authoring command above → exit `0`; `authoring.py` SHA-256 `9cc3ecf5ba2d702e2dfad143e0e4fe6c450455ad2f56201682e23563451aaf9a`.
- Retained `specimen.json` SHA-256 `9a8d950d9ad8173cc357538e7cda38bdeee0b78a75cd9a238c0a0d73f3db94c5`; `receipt.json` SHA-256 `ea694551079c8164e7f3e61e21508bde2df2ed816c06abb192eca459912b415e`.
- Retained pristine runner copy SHA-256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`; mutated runner text SHA-256 `db4579edbee069cb1ac47534092f16fff3822973b05e6bfa3af94d3dc6207dae`.
- Scratch evidence is under `/fast/scratch/hyaku/tameshi-r35-w2/SealStdoutDetail/`. No tools were installed. The audit tool was not run; no C1 score is claimed.
