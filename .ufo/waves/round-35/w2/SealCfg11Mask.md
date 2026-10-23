# Round 35 W2 — SealCfg11Mask

Pin: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. Scope: author one C1 sealed `kill` specimen whose behavior diverges only under `(auto=1, KEEP=1)`. Scratch: `/fast/scratch/hyaku/tameshi-r35-w2/SealCfg11Mask/`.

## Result and ranked findings

The authored `cfg11-workdir-wording` specimen is behaviorally a kill: across the required 4 configurations × 7 vectors, exactly one tuple differs (the all-zero vector under `(1,1)`). It changes the PASS-path `REGRESSION_WORKDIR` wording only; it does not alter the runner's removal behavior. This is a different construction from public `cfg11-pass-mask` (which alters `npass` before the fail guard; panel blob SHA256 `f5da18e89dd5df6175e565149ec28fde2fb357c8b237e6c8a812251fbb6d5c30`, at `panel/cfg11-pass-mask.json:4-10`).

No CRITICAL claim falsifier is asserted: this seat did not run the frozen audit tool or C1 counter to score the specimen. No BOUND or HYGIENE finding against the frozen artifacts was established. The table is the independent behavioral ground truth for the specimen, not a tool verdict.

## Specimen JSON

```json
{
  "copies": [
    {
      "class": "cfg11-workdir-wording",
      "set": "kill",
      "edits": [
        [
          "  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0",
          "  else\n    if [[ $auto -eq 1 && $KEEP -eq 1 ]]; then\n      printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    else\n      printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    fi\n  fi\n  exit 0",
          1
        ]
      ]
    }
  ]
}
```

The exact old string occurs once in the pinned runner; the independent driver rejects any count other than one before applying the edit.

## Evidence and byte identities

- Pinned source command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh | sha256sum` — exit 0; `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches the frozen runner pin).
- The output of applying the JSON edit to those pinned bytes has full-runner SHA256 `e34a3f4b2c040e46f7b93ad7a5512896fe2b9a050804bf3ec1335dffe137ab4a`. Extracted source/copy tally-block SHA256s are `acbba9ab80e64b98e1e1e793c2f753bc4e25f2ee74873cbb42b4fb45d8027572` and `55ae3a41b6288e69841cae9384093a7dda48cdc6d1832b034bc115d3dc181d7c`, respectively.
- Frozen-artifact hash commands (each exit 0): `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-35/contract.json | sha256sum` -> `a9eb2b97226ad192352f9da8cc32f3f719db22a93f14355a5e2d1306cea027c0`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-35/c1/c1-measure.py | sha256sum` -> `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-35/c1/panel/cfg11-pass-mask.json | sha256sum` -> `f5da18e89dd5df6175e565149ec28fde2fb357c8b237e6c8a812251fbb6d5c30`.
- Independent driver: `/fast/scratch/hyaku/tameshi-r35-w2/SealCfg11Mask/exercise.py`, SHA256 `55a772da465376302d2bab7aa3caeb28c37d89249bb20a60d575178ee314bf21` (`sha256sum /fast/scratch/hyaku/tameshi-r35-w2/SealCfg11Mask/exercise.py`, exit 0). Command `python3 /fast/scratch/hyaku/tameshi-r35-w2/SealCfg11Mask/exercise.py; rc=$?; printf 'EXERCISE_EXIT=%s\n' "$rc"; exit "$rc"` — `EXERCISE_EXIT=0`.
- The driver extracts the runner's `run_regression()` tally block and leg names from the pinned runner, applies the specimen edit to the complete runner text, then runs pristine and edited tally blocks in separate Bash processes and compares their exit code plus captured full stdout. The auto root was created using `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` and was `/tmp/tameshi-r4-2-regression.6eBlhX` (six-character suffix). Explicit roots were `tally-audit` and `tally-audit-explicit`.
- Vectors (nine statuses each): `all-zero=[0,0,0,0,0,0,0,0,0]`; `one-1=[1,0,0,0,0,0,0,0,0]`; `one-2=[2,0,0,0,0,0,0,0,0]`; `one-3=[3,0,0,0,0,0,0,0,0]`; `one-255=[255,0,0,0,0,0,0,0,0]`; `mixed-1=[0,1,2,0,0,0,0,0,0]`; `mixed-2=[0,3,255,1,2,0,0,0,0]`.

## Behavioral receipt

Tuple format is `(exit, FULL stdout)`; `\n` in table cells denotes the exact newline byte. Every pair is pristine tuple / copy tuple / equality.

| Config (root) | Vector | Pristine tuple | Copy tuple | Equal? |
|---|---|---|---|---|
| `(0,1)` `tally-audit` | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| `(0,1)` `tally-audit` | one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| `(0,1)` `tally-audit` | one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| `(0,1)` `tally-audit` | one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| `(0,1)` `tally-audit` | one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| `(0,1)` `tally-audit` | mixed-1 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| `(0,1)` `tally-audit` | mixed-2 | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| `(1,0)` `/tmp/tameshi-r4-2-regression.6eBlhX` | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (removed on PASS; --keep retains)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (removed on PASS; --keep retains)\n")` | yes |
| `(1,0)` `/tmp/tameshi-r4-2-regression.6eBlhX` | one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,0)` `/tmp/tameshi-r4-2-regression.6eBlhX` | one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,0)` `/tmp/tameshi-r4-2-regression.6eBlhX` | one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,0)` `/tmp/tameshi-r4-2-regression.6eBlhX` | one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,0)` `/tmp/tameshi-r4-2-regression.6eBlhX` | mixed-1 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,0)` `/tmp/tameshi-r4-2-regression.6eBlhX` | mixed-2 | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(0,0)` `tally-audit-explicit` | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| `(0,0)` `tally-audit-explicit` | one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| `(0,0)` `tally-audit-explicit` | one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| `(0,0)` `tally-audit-explicit` | one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| `(0,0)` `tally-audit-explicit` | one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| `(0,0)` `tally-audit-explicit` | mixed-1 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| `(0,0)` `tally-audit-explicit` | mixed-2 | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| `(1,1)` `/tmp/tameshi-r4-2-regression.6eBlhX` | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (removed on PASS; --keep retains)\n")` | **no** |
| `(1,1)` `/tmp/tameshi-r4-2-regression.6eBlhX` | one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,1)` `/tmp/tameshi-r4-2-regression.6eBlhX` | one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,1)` `/tmp/tameshi-r4-2-regression.6eBlhX` | one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,1)` `/tmp/tameshi-r4-2-regression.6eBlhX` | one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,1)` `/tmp/tameshi-r4-2-regression.6eBlhX` | mixed-1 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |
| `(1,1)` `/tmp/tameshi-r4-2-regression.6eBlhX` | mixed-2 | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.6eBlhX (kept)\n")` | yes |

## What was not broken / limits

- **Proved closed on this sample set:** divergence is confined to `(1,1)` and its all-zero PASS row; all other 27 config×vector tuples are identical. This is the complete bounded result, not a claim about untested vectors.
- **Risk:** the mutant changes only a diagnostic line and falsely says the retained auto-root was removed when `KEEP=1`; it does not delete the root. It targets the full-stdout contract, not tally-arm logic or filesystem cleanup.
- **Audit verdict:** deliberately not run. Therefore no claim is made here about whether v3 accepts or kills this specimen; the parent must rely on the planned measurement after the sealed set lands.
- **Artifact drift note:** `sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c1/c1-measure.py` — exit 0, current worktree hash `d27e6769c0def37900eea4d860f9b23bf2ce4e7c876a49eb0a1e92b7bf2052c2`, unlike the frozen blob hash above. The behavioral exercise reads only the pinned runner object with `git show` and does not execute or rely on the worktree counter. No frozen artifacts were changed; this scoped report is the only repository file written.
- No installs or pacman operations; no Git mutations, frozen-artifact edits, or sibling writes. No blockers.
