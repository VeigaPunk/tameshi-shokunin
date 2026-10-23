# SealAcceptTrailing — round-35 C1 sealed accept specimen

## Scope and result

Attacked the assigned trailing-comment class against the pinned runner at `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`: appended inert shell comments to the tally-loop header (`for st ...; do`) and the last line of the extracted tally block (`exit 0`). No source runner or tool was changed. The edits each matched exactly once in the pinned runner text.

**Result: ACCEPT.** Direct Bash execution of pristine and copied tally blocks produced identical exit status and full stdout on all 28 config/vector pairs below. This is a behaviorally equivalent specimen; it is not a kill. The tool under test was not run as the source of truth.

## Specimen JSON

```json
{
 "copies": [
  {
   "class": "accept-trailing-comments",
   "set": "accept",
   "edits": [
    [
     "  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do",
     "  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do # inert sealed trailing comment",
     1
    ],
    [
     "  exit 0\n}\n\n# ------------------------------------------------------------------ selftest",
     "  exit 0 # inert sealed trailing comment\n}\n\n# ------------------------------------------------------------------ selftest",
     1
    ]
   ]
  }
 ]
}
```

## Exact evidence and commands

- Clone/checkout completed successfully; `git -C /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptTrailing/lane rev-parse HEAD` exited `0` and returned `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`.
- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptTrailing/lane show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh | sha256sum` exited `0`: pristine `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches contract.json:9).
- `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` exited `0`, yielding `/tmp/tameshi-r4-2-regression.xMVaq2`; this real runner-prefix root was used for both `auto=1` triples. Explicit-root strings were `/tmp/tameshi-r35-explicit-01` and `/tmp/tameshi-r35-explicit-00`.
- `python3 /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptTrailing/authoring-receipt.py` exited `0`. It extracted the runner's `run_regression` tally span, applied each declared edit once, and compared `(exit, full stdout)` from Bash for pristine and copied blocks under `(auto,KEEP)=(0,1),(1,0),(0,0),(1,1)` and seven vectors. Receipt JSON: `/fast/scratch/hyaku/tameshi-r35-w2/SealAcceptTrailing/work/behavioral-receipt.json` (`all_equal: true`, `edit_occurrences: [1,1]`).
- `sha256sum /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptTrailing/work/pristine-mutate-and-run.sh /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptTrailing/work/copy-mutate-and-run.sh /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptTrailing/authoring-receipt.py /fast/scratch/hyaku/tameshi-r35-w2/SealAcceptTrailing/work/behavioral-receipt.json` exited `0`:
  - pristine runner text: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
  - copied runner text: **`99f8a6213baccdb410fc4c4900331348de613689555638ee982e24352149e7e8`**
  - authoring/receipt driver: `d4fc23d6a331d3b1ce85e090337008a55d3fb1823898f022cdc4b6d08f7abf85`
  - behavioral receipt JSON: `b7f7ea926e6a971979c2d9c87d626f8efe4f25ca858f0618e844e3150d885e27`

The receipt driver’s first invocation exited `1` before any vector run because its local extraction assertion only allowed the pristine `exit 0` line. I corrected that assertion to also accept the assigned comment-appended line; the rerun above completed all 28 pairs. No pinned artifact was changed.

## Behavioral receipt table

Tuple aliases below expand to the **exact** exit and complete stdout bytes observed (including the final newline); `{R}` is replaced by the root shown in that row. They are shorthand only. Each row records pristine and copy independently; both resolved to the same alias and equality was `true`.

- `PASS-KEEP(R)` = `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: {R} (kept)\n")`
- `PASS-REMOVE(R)` = `(0, "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\nREGRESSION_WORKDIR: {R} (removed on PASS; --keep retains)\n")`
- `FAIL-1(R)` = `(1, "REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: {R} (kept)\n")`
- `SETUP-1(R)` = `(2, "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: {R} (kept)\n")`
- `MIX-A(R)` = `(1, "REGRESSION: FAIL (cases=9 passed=5 failed=1 setup=3)\nREGRESSION_WORKDIR: {R} (kept)\n")`
- `MIX-B(R)` = `(1, "REGRESSION: FAIL (cases=9 passed=1 failed=2 setup=6)\nREGRESSION_WORKDIR: {R} (kept)\n")`

| auto,KEEP | Root `{R}` | Vector | Pristine tuple | Copy tuple | Equal? |
|---|---|---|---|---|---|
| (0,1) | `/tmp/tameshi-r35-explicit-01` | all-zero | PASS-KEEP(R) | PASS-KEEP(R) | yes |
| (0,1) | `/tmp/tameshi-r35-explicit-01` | one-1 | FAIL-1(R) | FAIL-1(R) | yes |
| (0,1) | `/tmp/tameshi-r35-explicit-01` | one-2 | SETUP-1(R) | SETUP-1(R) | yes |
| (0,1) | `/tmp/tameshi-r35-explicit-01` | one-3 | SETUP-1(R) | SETUP-1(R) | yes |
| (0,1) | `/tmp/tameshi-r35-explicit-01` | one-255 | SETUP-1(R) | SETUP-1(R) | yes |
| (0,1) | `/tmp/tameshi-r35-explicit-01` | mixed-a | MIX-A(R) | MIX-A(R) | yes |
| (0,1) | `/tmp/tameshi-r35-explicit-01` | mixed-b | MIX-B(R) | MIX-B(R) | yes |
| (1,0) | `/tmp/tameshi-r4-2-regression.xMVaq2` | all-zero | PASS-REMOVE(R) | PASS-REMOVE(R) | yes |
| (1,0) | `/tmp/tameshi-r4-2-regression.xMVaq2` | one-1 | FAIL-1(R) | FAIL-1(R) | yes |
| (1,0) | `/tmp/tameshi-r4-2-regression.xMVaq2` | one-2 | SETUP-1(R) | SETUP-1(R) | yes |
| (1,0) | `/tmp/tameshi-r4-2-regression.xMVaq2` | one-3 | SETUP-1(R) | SETUP-1(R) | yes |
| (1,0) | `/tmp/tameshi-r4-2-regression.xMVaq2` | one-255 | SETUP-1(R) | SETUP-1(R) | yes |
| (1,0) | `/tmp/tameshi-r4-2-regression.xMVaq2` | mixed-a | MIX-A(R) | MIX-A(R) | yes |
| (1,0) | `/tmp/tameshi-r4-2-regression.xMVaq2` | mixed-b | MIX-B(R) | MIX-B(R) | yes |
| (0,0) | `/tmp/tameshi-r35-explicit-00` | all-zero | PASS-KEEP(R) | PASS-KEEP(R) | yes |
| (0,0) | `/tmp/tameshi-r35-explicit-00` | one-1 | FAIL-1(R) | FAIL-1(R) | yes |
| (0,0) | `/tmp/tameshi-r35-explicit-00` | one-2 | SETUP-1(R) | SETUP-1(R) | yes |
| (0,0) | `/tmp/tameshi-r35-explicit-00` | one-3 | SETUP-1(R) | SETUP-1(R) | yes |
| (0,0) | `/tmp/tameshi-r35-explicit-00` | one-255 | SETUP-1(R) | SETUP-1(R) | yes |
| (0,0) | `/tmp/tameshi-r35-explicit-00` | mixed-a | MIX-A(R) | MIX-A(R) | yes |
| (0,0) | `/tmp/tameshi-r35-explicit-00` | mixed-b | MIX-B(R) | MIX-B(R) | yes |
| (1,1) | `/tmp/tameshi-r4-2-regression.xMVaq2` | all-zero | PASS-KEEP(R) | PASS-KEEP(R) | yes |
| (1,1) | `/tmp/tameshi-r4-2-regression.xMVaq2` | one-1 | FAIL-1(R) | FAIL-1(R) | yes |
| (1,1) | `/tmp/tameshi-r4-2-regression.xMVaq2` | one-2 | SETUP-1(R) | SETUP-1(R) | yes |
| (1,1) | `/tmp/tameshi-r4-2-regression.xMVaq2` | one-3 | SETUP-1(R) | SETUP-1(R) | yes |
| (1,1) | `/tmp/tameshi-r4-2-regression.xMVaq2` | one-255 | SETUP-1(R) | SETUP-1(R) | yes |
| (1,1) | `/tmp/tameshi-r4-2-regression.xMVaq2` | mixed-a | MIX-A(R) | MIX-A(R) | yes |
| (1,1) | `/tmp/tameshi-r4-2-regression.xMVaq2` | mixed-b | MIX-B(R) | MIX-B(R) | yes |

The input vectors were nine statuses each: all-zero `[0,0,0,0,0,0,0,0,0]`; one-1 `[1,0,0,0,0,0,0,0,0]`; one-2 `[2,0,0,0,0,0,0,0,0]`; one-3 `[3,0,0,0,0,0,0,0,0]`; one-255 `[255,0,0,0,0,0,0,0,0]`; mixed-a `[0,1,2,3,255,0,0,0,0]`; mixed-b `[2,3,1,255,0,1,2,3,255]`.

## Findings / what could not be broken

- **HYGIENE — assigned accept class behaves as expected.** The two trailing comments preserve the complete tally behavior on every required triple/vector: 28/28 identical tuples (receipt above). No CRITICAL false claim or BOUND failure was found in this assigned class.
- **Could not break:** no divergence was observed on the four `(auto,KEEP)` triples or any of the seven required vectors; this is proven by the per-row tuples and `all_equal: true` in the receipt JSON. No broader claim about unrelated mutation classes is made.
- **Evidence bound:** the behavioral receipt covers the seven requested representative vectors under each triple (28 pairs); it is not an exhaustive enumeration of all possible 9-status vectors.
- **Blockers:** none. No tools were installed. The C1 audit tool was intentionally not run against the specimen.
