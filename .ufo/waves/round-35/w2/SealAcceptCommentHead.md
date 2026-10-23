# Round-35 W2 — SealAcceptCommentHead

## Scope and attack

Authored one C1 held-out **accept** specimen from pinned runner bytes at `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. It inserts one inert comment in `run_regression`'s head, after the final captured leg and before `local nlegs=`. The comment names three legs and contains `it's`, `"quoted"`, and `}`. This attacks the round-34 comment/leg-name false-kill class (round-34 lesson, “Tool precision,” lines 143–147) against the frozen four-triple/full-stdout/comment-blanking contract (contract.json lines 26–29; v3 docstring lines 19–28).

## Specimen JSON

```json
{"copies":[{"class":"comment-head-comment-quoted-legnames","set":"accept","edits":[["  st_citecheck=$?\n","  st_citecheck=$?\n  # st_js st_kagi st_tsu: it's \"quoted\" and inert }\n",1]]}]}
```

The pinned runner contains the old string exactly once. The copy differs bytewise and retains all nine head leg names. Its extracted tally block is byte-identical to pristine.

## Exact commands and retained evidence

1. Pinned-byte lookup and hash:

   `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -e 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b^{commit} && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh | sha256sum`

   Exit **0**; pristine SHA-256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches contract.json line 9).

2. Direct behavior receipt (not the v3 tool):

   `python3 /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptCommentHead/receipt.py`

   Exit **0**. The retained harness SHA-256 is `0823bbe09f6db862545514d9c0d3a4bbddff3397a5df59e21b14ee0d0df0e11b`; `sha256sum /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptCommentHead/receipt.py` exited **0**. It loads the runner with read-only `git show`, verifies the pinned hash and one-match edit, extracts the head and tally block, then directly runs each extracted block in Bash for pristine and copy. Summary output: `head_comment_present=true`, leg names `st_js, st_kagi, st_tsu, st_mado, st_checklist, st_claims, st_roundgate, st_sourcescheck, st_citecheck`, `block_bytes_identical=true`, `vectors_per_config=7`, `configs=4`, `equal_rows=28`. Every row printed `equal=true`.

   Both auto triples used roots made by the runner's real template, `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`: `/tmp/tameshi-r4-2-regression.T42AC3` for `(auto=1,KEEP=0)` and `/tmp/tameshi-r4-2-regression.IVTgrA` for `(auto=1,KEEP=1)`. Explicit roots were `tally-audit` for `(0,1)` and `tally-audit-explicit` for `(0,0)`. The exact status vectors, in the nine-leg order printed above, were all-zero `[0,0,0,0,0,0,0,0,0]`; one-1 `[1,0,0,0,0,0,0,0,0]`; one-2 `[2,0,0,0,0,0,0,0,0]`; one-3 `[3,0,0,0,0,0,0,0,0]`; one-255 `[255,0,0,0,0,0,0,0,0]`; mixed-1-2 `[1,2,0,0,0,0,0,0,0]`; mixed-3-255-1 `[0,3,255,1,0,0,0,0,0]`.

   Resulting runner-text SHA-256: pristine `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`; copy `09424e99c887414fb5a186aa8ec0ea0e4f7f2dbe210d58bfa3e9584ca3c625a2` (copy hash emitted by the direct receipt command).

The table below records the exact `(exit, FULL stdout)` tuples. `<br>` denotes a literal newline in stdout; neither line is omitted. The copy tuple matches pristine on every row.

## Behavioral receipt table

### `(auto=0, KEEP=1)`, root `tally-audit`

| Vector | Pristine tuple | Copy tuple | Equal? |
|---|---|---|---|
| all-zero | `(0, REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)<br>REGRESSION_WORKDIR: tally-audit (kept))` | `(0, REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)<br>REGRESSION_WORKDIR: tally-audit (kept))` | yes |
| one-status-1 | `(1, REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)<br>REGRESSION_WORKDIR: tally-audit (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)<br>REGRESSION_WORKDIR: tally-audit (kept))` | yes |
| one-status-2 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit (kept))` | yes |
| one-status-3 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit (kept))` | yes |
| one-status-255 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit (kept))` | yes |
| mixed-1-2 | `(1, REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)<br>REGRESSION_WORKDIR: tally-audit (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)<br>REGRESSION_WORKDIR: tally-audit (kept))` | yes |
| mixed-3-255-1 | `(1, REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)<br>REGRESSION_WORKDIR: tally-audit (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)<br>REGRESSION_WORKDIR: tally-audit (kept))` | yes |

### `(auto=1, KEEP=0)`, root `/tmp/tameshi-r4-2-regression.T42AC3`

| Vector | Pristine tuple | Copy tuple | Equal? |
|---|---|---|---|
| all-zero | `(0, REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (removed on PASS; --keep retains))` | `(0, REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (removed on PASS; --keep retains))` | yes |
| one-status-1 | `(1, REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | yes |
| one-status-2 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | yes |
| one-status-3 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | yes |
| one-status-255 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | yes |
| mixed-1-2 | `(1, REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | yes |
| mixed-3-255-1 | `(1, REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.T42AC3 (kept))` | yes |

### `(auto=0, KEEP=0)`, root `tally-audit-explicit`

| Vector | Pristine tuple | Copy tuple | Equal? |
|---|---|---|---|
| all-zero | `(0, REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | `(0, REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | yes |
| one-status-1 | `(1, REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | yes |
| one-status-2 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | yes |
| one-status-3 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | yes |
| one-status-255 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | yes |
| mixed-1-2 | `(1, REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | yes |
| mixed-3-255-1 | `(1, REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)<br>REGRESSION_WORKDIR: tally-audit-explicit (kept))` | yes |

### `(auto=1, KEEP=1)`, root `/tmp/tameshi-r4-2-regression.IVTgrA`

| Vector | Pristine tuple | Copy tuple | Equal? |
|---|---|---|---|
| all-zero | `(0, REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | `(0, REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | yes |
| one-status-1 | `(1, REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | yes |
| one-status-2 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | yes |
| one-status-3 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | yes |
| one-status-255 | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | `(2, REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | yes |
| mixed-1-2 | `(1, REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | yes |
| mixed-3-255-1 | `(1, REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | `(1, REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)<br>REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.IVTgrA (kept))` | yes |

## Findings, limits, and handoff

- **BOUND — bounded no-break result:** this exact head-comment specimen satisfies its `accept` label: byte-distinct runner, unchanged head leg list/tally block, and equal exit/full-stdout tuples for all 28 required config-vector pairs. The evidence is the direct receipt summary and table above. This says nothing about untested comment forms or the rest of C1's set.
- **CRITICAL:** none found for this construction. It diverges under no tested config/vector, so the specimen was retained as `accept`; no revision was needed.
- **What I could not break:** could not induce a behavioral difference with the specified quoted/braced, multi-leg comment; the 28-row direct Bash receipt is the proof. No v3 audit invocation was used as ground truth.
- **Files:** this report is the only lane/repository file written. The retained scratch harness is `/fast/scratch/hyaku/tameshi-r35-w2/SealAcceptCommentHead/receipt.py` (SHA above); runner bytes were read from the pinned Git object, not edited. No tools were installed. No blocker.
