# Round 35 W2 — SealAcceptHeredoc

## Scope and result

Authored the assigned **accept** specimen: a single inert comment inside the pinned tally block. Its comment text contains the heredoc-looking string `# <<EOF` and the apostrophe in `don't`. The specimen has one insertion and leaves the runner's behavior identical in all 28 required configuration/vector comparisons. This establishes the specimen's accept label; I did **not** run `tally-audit-v3.py` or the C1 counter as behavioral ground truth.

**Ranked findings:** CRITICAL — none found; BOUND — none found; HYGIENE — none found. No broader claim about the auditor is made by this one equivalent specimen.

## Specimen JSON

```json
{
  "copies": [
    {
      "class": "inert-heredoc-apostrophe-comment",
      "set": "accept",
      "edits": [
        [
          "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n",
          "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  # <<EOF -- don't open a heredoc; inert comment\n",
          1
        ]
      ]
    }
  ]
}
```

The specimen JSON is SHA-256 `94882f067465ab774c662b4c428a1c74b19f888b0360c5cedd8cc91b76a4d22f` (file `/fast/scratch/hyaku/tameshi-r35-w2/SealAcceptHeredoc/specimen.json`). The copied runner text produced by applying that exact edit is SHA-256 **`64a821bc6e23da7d734910adc146dafe2f07dd42081f3bbcb99910deb1969e51`**.

## Behavioral receipt

Receipt command: `python3 /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptHeredoc/behavior_receipt.py` — exit **0** (`BEHAVIOR_ROWS=28`, `ALL_EQUAL=True`). Harness SHA-256: `5c3f408d162a496307000b80f9bdd422bd54e2bfce6887ae866507240d03c730`.

The harness retrieved the pinned runner with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh` (exit **0**) and verified its SHA-256 against the contract: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`. The tally block and nine pre-tally status names were extracted from those pinned bytes. Each tuple is `(exit, full stdout)`; `\n` in the table denotes a newline, including the final newline. The auto-root command `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` returned exit **0**, root `/tmp/tameshi-r4-2-regression.MfFEUE`. It was shared by the compared runs and cleaned up by the harness.

Vectors (each has nine statuses): `all-zero=[0,0,0,0,0,0,0,0,0]`; `one-status-1=[1,0,0,0,0,0,0,0,0]`; `one-status-2=[2,0,0,0,0,0,0,0,0]`; `one-status-3=[3,0,0,0,0,0,0,0,0]`; `one-status-255=[255,0,0,0,0,0,0,0,0]`; `mixed-1-2=[1,2,0,0,0,0,0,0,0]`; `mixed-3-255=[0,3,255,0,0,0,0,0,0]`.

| (auto,KEEP) | vector | pristine tuple (exit, full stdout) | copy tuple (exit, full stdout) | equal? |
|---|---|---|---|---|
| (0,1) | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| (0,1) | one-status-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| (0,1) | one-status-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| (0,1) | one-status-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| (0,1) | one-status-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| (0,1) | mixed-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| (0,1) | mixed-3-255 | `(2, "REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: tally-audit (kept)\n")` | yes |
| (1,0) | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (removed on PASS; --keep retains)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (removed on PASS; --keep retains)\n")` | yes |
| (1,0) | one-status-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,0) | one-status-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,0) | one-status-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,0) | one-status-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,0) | mixed-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,0) | mixed-3-255 | `(2, "REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (0,0) | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| (0,0) | one-status-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| (0,0) | one-status-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| (0,0) | one-status-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| (0,0) | one-status-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| (0,0) | mixed-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| (0,0) | mixed-3-255 | `(2, "REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: tally-audit-explicit (kept)\n")` | yes |
| (1,1) | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,1) | one-status-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,1) | one-status-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,1) | one-status-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,1) | one-status-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,1) | mixed-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |
| (1,1) | mixed-3-255 | `(2, "REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.MfFEUE (kept)\n")` | yes |

All rows compare both exit code and the complete stdout byte string. Config roots: `(0,1)` relative `tally-audit`; `(1,0)` real auto root above; `(0,0)` explicit `tally-audit-explicit`; `(1,1)` the same real auto root. The bytes relied on are pinned runner SHA-256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`, copied runner SHA-256 above, and harness SHA-256 above.

## What I could not break

The comment did not change the block's result for any tested status class or the `(auto,KEEP)`-dependent workdir wording/removal behavior: 28/28 complete tuples are identical. This is the requested held-out **accept** construction and proof, not a claim that the auditor has accepted it; the auditor was intentionally not used as the behavioral oracle.

Evidence inputs read: freeze contract `.ufo/evidence/round-35/contract.json` SHA-256 `ef878db73dd81849ae2ec97ea28a9a814ac381d58484e4d22da26028a97d3041` (runner pin and A4 at `frozen_artifacts`/amendment A4); public root-keyed panel copies `root-keyed-auto-mask.json` SHA-256 `c02c7851934d4f0b2bdf5319eb731da3ecfe302c9fcd86994188e22dd5a86ddc` and `root-keyed-auto-zero.json` SHA-256 `d6e26e1abb31f31ff8d772724ae3c4ef3e123f7cb956a68c49f3e1134f1295f5`. The panel copies are context only; they were not modified or included in this specimen.
