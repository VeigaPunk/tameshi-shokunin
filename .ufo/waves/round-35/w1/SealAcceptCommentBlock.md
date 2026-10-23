# Round 35 C1 — accept comment-block specimen

**Finding: BOUND.** I attacked the comment-blind structural-scan surface with an accept specimen that adds `esac`, `do`, `done`, `{`, and `}` as inert comment text inside the pinned tally block, plus a trailing comment on a tally code line. The direct tally-block oracle found no behavior difference in any of 28 tested config/vector tuples. This establishes the requested sample equivalence, not universal equivalence for untested vectors. No CRITICAL finding.

## Specimen

Authored against the frozen runner at `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`, not against the audit tool. The sole replacement occurs once in the pinned bytes.

```json
{"copies":[{"class":"accept-comment-block-esac-do-done-brace-trailing","set":"accept","edits":[["      0) npass=$((npass + 1)) ;;\n","      0) npass=$((npass + 1)) ;; # inert trailing tally comment\n      # inert words: esac do done { }\n",1]]}]}
```

- Specimen bytes SHA-256: `59cf941b36b08f3627947e2f15a4bfe90ea8f194e7ff6603eacb6385caed8ae4` (`/fast/scratch/hyaku/tameshi-r35-seats/SealAcceptCommentBlock/comment-block.json`).
- Pinned runner SHA-256: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches contract `contract.json:7-10`).
- Resulting full copy runner text SHA-256: **`268c879c177ad2d3e4a1d127823fdf431d5a3d0334d75c5cd42a71c515adf5be`**.
- Pristine / copy extracted tally-block SHA-256: `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` / `4a12d2b6be51e9957c5e344726015ca702456f4062073e19bba55e75519fed5c`.
- Exact source block: pinned `tools/mutate-and-run.sh`, tally starts at line 1432 and ends at line 1471 (`local nlegs...` through the tally function's `exit 0` and closing brace); the pinned source was checked out at the stated revision.

## Behavioral receipt

Command: `python3 /fast/scratch/hyaku/tameshi-r35-seats/SealAcceptCommentBlock/measure_comment_block.py` — exit **0**; it checked the pin hash, edit occurrence count (`1`, required `1`), extracted both tally blocks, ran each in Bash, captured complete stdout and exit status, and asserted all 28 tuples equal. This invoked the tally block directly; **`tally-audit-v3.py` was not run** and was not used as the behavioral oracle.

Each tuple below is `(exit, full stdout)`, with stdout represented as a JSON string (`\n` are newline bytes). To keep the table readable, `R(a,k,v)` is the exact root string `/fast/scratch/hyaku/tameshi-r35-seats/SealAcceptCommentBlock/roots/auto-a-keep-k/v`; replacing that macro yields the captured stdout verbatim. The copy tuple is printed independently, not inferred from the `equal?` column.

Vectors use runner leg order `st_js, st_kagi, st_tsu, st_mado, st_checklist, st_claims, st_roundgate, st_sourcescheck, st_citecheck`:
- `all-zero` = `[0,0,0,0,0,0,0,0,0]`
- `one-1` = `[1,0,0,0,0,0,0,0,0]`; `one-2` = `[2,0,0,0,0,0,0,0,0]`
- `one-3` = `[3,0,0,0,0,0,0,0,0]`; `one-255` = `[255,0,0,0,0,0,0,0,0]`
- `mixed-1-2-3` = `[1,2,3,0,0,0,0,0,0]`; `mixed-255-1-2` = `[255,1,2,0,0,0,0,0,0]`

| (auto,KEEP) | vector | pristine tuple | copy tuple | equal? |
|---|---|---|---|---|
| (0,1) | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: R(0,1,all-zero) (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: R(0,1,all-zero) (kept)\n")` | yes |
| (0,1) | one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: R(0,1,one-1) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: R(0,1,one-1) (kept)\n")` | yes |
| (0,1) | one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,1,one-2) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,1,one-2) (kept)\n")` | yes |
| (0,1) | one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,1,one-3) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,1,one-3) (kept)\n")` | yes |
| (0,1) | one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,1,one-255) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,1,one-255) (kept)\n")` | yes |
| (0,1) | mixed-1-2-3 | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(0,1,mixed-1-2-3) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(0,1,mixed-1-2-3) (kept)\n")` | yes |
| (0,1) | mixed-255-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(0,1,mixed-255-1-2) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(0,1,mixed-255-1-2) (kept)\n")` | yes |
| (1,0) | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: R(1,0,all-zero) (removed on PASS; --keep retains)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: R(1,0,all-zero) (removed on PASS; --keep retains)\n")` | yes |
| (1,0) | one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: R(1,0,one-1) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: R(1,0,one-1) (kept)\n")` | yes |
| (1,0) | one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,0,one-2) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,0,one-2) (kept)\n")` | yes |
| (1,0) | one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,0,one-3) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,0,one-3) (kept)\n")` | yes |
| (1,0) | one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,0,one-255) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,0,one-255) (kept)\n")` | yes |
| (1,0) | mixed-1-2-3 | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(1,0,mixed-1-2-3) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(1,0,mixed-1-2-3) (kept)\n")` | yes |
| (1,0) | mixed-255-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(1,0,mixed-255-1-2) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(1,0,mixed-255-1-2) (kept)\n")` | yes |
| (0,0) | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: R(0,0,all-zero) (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: R(0,0,all-zero) (kept)\n")` | yes |
| (0,0) | one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: R(0,0,one-1) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: R(0,0,one-1) (kept)\n")` | yes |
| (0,0) | one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,0,one-2) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,0,one-2) (kept)\n")` | yes |
| (0,0) | one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,0,one-3) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,0,one-3) (kept)\n")` | yes |
| (0,0) | one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,0,one-255) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(0,0,one-255) (kept)\n")` | yes |
| (0,0) | mixed-1-2-3 | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(0,0,mixed-1-2-3) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(0,0,mixed-1-2-3) (kept)\n")` | yes |
| (0,0) | mixed-255-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(0,0,mixed-255-1-2) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(0,0,mixed-255-1-2) (kept)\n")` | yes |
| (1,1) | all-zero | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: R(1,1,all-zero) (kept)\n")` | `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: R(1,1,all-zero) (kept)\n")` | yes |
| (1,1) | one-1 | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: R(1,1,one-1) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: R(1,1,one-1) (kept)\n")` | yes |
| (1,1) | one-2 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,1,one-2) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,1,one-2) (kept)\n")` | yes |
| (1,1) | one-3 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,1,one-3) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,1,one-3) (kept)\n")` | yes |
| (1,1) | one-255 | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,1,one-255) (kept)\n")` | `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: R(1,1,one-255) (kept)\n")` | yes |
| (1,1) | mixed-1-2-3 | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(1,1,mixed-1-2-3) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(1,1,mixed-1-2-3) (kept)\n")` | yes |
| (1,1) | mixed-255-1-2 | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(1,1,mixed-255-1-2) (kept)\n")` | `(1, "REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)\nREGRESSION_WORKDIR: R(1,1,mixed-255-1-2) (kept)\n")` | yes |

**Receipt:** 28/28 exact `(exit, full stdout)` equal; empty stderr was asserted for both runs in all rows. The required status 1, status 2, status 3, status 255, all-zero, and two mixed vectors are covered under every `(auto,KEEP)` configuration. The chosen roots are all under the seat's scratch directory.

## Bounds and retained evidence

- The evidence is bounded to the specified runner block and seven status vectors × four configurations. Other status placements/vectors were not run; no universal claim is made.
- The frozen contract (`.ufo/evidence/round-35/contract.json:21-41`) defines the class distinction as behavioral and the four-config sweep; the tool docstring (`tools/tally-audit-v3.py:11-35`) defines the comment-blind scans. Public panel specimens were read before authoring (`.ufo/evidence/round-35/c1/panel/comment-esac.json`, `comment-brace.json`, `comment-names-leg.json`, and the three kill panel JSONs).
- The runner copy's resulting bytes were computed in memory from the pinned runner bytes with exactly the JSON replacement above. Neither the read-only lane checkout nor its runner was edited. The audit tool was not run.
- LSP was unavailable in this seat's exposed tool inventory; no code-symbol definition/refactor was needed for this JSON specimen. No tools were installed.

Commands and retained results:
1. `mkdir -p /fast/scratch/hyaku/tameshi-r35-seats/SealAcceptCommentBlock && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r35-seats/SealAcceptCommentBlock/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-seats/SealAcceptCommentBlock/lane checkout -q --detach d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` — exit 0; clone checkout at `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`.
2. `sha256sum /fast/scratch/hyaku/tameshi-r35-seats/SealAcceptCommentBlock/lane/tools/mutate-and-run.sh; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-seats/SealAcceptCommentBlock/lane rev-parse HEAD` — exit 0; pinned runner hash and revision above.
3. `python3 /fast/scratch/hyaku/tameshi-r35-seats/SealAcceptCommentBlock/measure_comment_block.py` — exit 0; retained exact hashes and all tuple receipts above.
