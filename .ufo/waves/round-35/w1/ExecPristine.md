# ExecPristine — round 35, wave 1

## Scope and setup

Attacked the pinned v3 audit against the pristine runner snapshot at revision `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`. To respect the seat's prohibition on mutating Git commands, I materialized a read-only working-tree snapshot with `git archive` rather than the requested `git clone`/`checkout`; no `.git` directory was created in scratch. Setup command:

```text
set -o pipefail && mkdir -p /fast/scratch/hyaku/tameshi-r35-seats/ExecPristine/lane && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive --format=tar d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc | tar -x -C /fast/scratch/hyaku/tameshi-r35-seats/ExecPristine/lane
```

It completed successfully (exit 0). Revision resolution evidence: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --verify 'd16f9b5a18945ede3852ec3df7eb4ee4b0afbafc^{commit}'` → `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`, exit 0.

## Audit evidence

The audit command was run twice from `/fast/scratch/hyaku/tameshi-r35-seats/ExecPristine/lane` (first unwrapped, then repeated with an exit-status wrapper because the first tool response did not display the process status). Both produced the same output. Captured invocation:

```text
python3 /fast/scratch/hyaku/tameshi-r35-seats/ExecPristine/lane/tools/tally-audit-v3.py; rc=$?; printf 'EXIT_CODE=%d\n' "$rc"; exit "$rc"
```

Exit code: **0**. Exact output:

```text
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
EXIT_CODE=0
```

Pinned input hashes, from `sha256sum /fast/scratch/hyaku/tameshi-r35-seats/ExecPristine/lane/tools/tally-audit-v3.py /fast/scratch/hyaku/tameshi-r35-seats/ExecPristine/lane/tools/mutate-and-run.sh` (exit 0):

- `tools/tally-audit-v3.py`: `da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f`
- `tools/mutate-and-run.sh`: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`

These match the frozen tool and runner hashes in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/contract.json:7-19`.

## Independent `vectors=` recomputation

The observed 9 legs are reported by the check output; vector-generation implementation is `/fast/scratch/hyaku/tameshi-r35-seats/ExecPristine/lane/tools/tally-audit-v3.py:457-509`, four configs are at `:340-341`, and operand stress is at `:520-534`.

Per config, generated vector entries (not deduplicated unique vectors):

- One status `0..255` at each of 9 positions: `9 × 256 = 2,304` (`:475-482`).
- One representative for each `(failing, setup)` pair with `fc + sc ≤ 9`: `Σ(fc=0..9)(10-fc) = 55` (`:457-464`).
- Six listed position-varied count mixes, three placements each: `6 × 3 = 18` (`:485-497`).
- Every unordered pair of positions and ordered pair from the 12-value `CO` set: `C(9,2) × 12² = 36 × 144 = 5,184` (`:498-509`).

Thus `2,304 + 55 + 18 + 5,184 = 7,561` entries per config; four configs produce `30,244`. Operand stress adds `9 operands × (duplicate, drop) × 4 configs = 72` (`:520-529`). Total: `30,244 + 72 = 30,316`, matching the tool's `vectors=30316` exactly.

Independent arithmetic command (exit 0):

```text
printf 'single_status=%d count_pairs=%d position_mixes=%d cooccurrence=%d per_config=%d configs=%d stress=%d total=%d\n' "$((9*256))" "$(((10*11)/2))" "$((6*3))" "$((36*12*12))" "$((9*256 + (10*11)/2 + 6*3 + 36*12*12))" "$((4*(9*256 + (10*11)/2 + 6*3 + 36*12*12)))" "$((9*2*4))" "$((4*(9*256 + (10*11)/2 + 6*3 + 36*12*12) + 9*2*4))"
```

Output: `single_status=2304 count_pairs=55 position_mixes=18 cooccurrence=5184 per_config=7561 configs=30244 stress=72 total=30316`.

## Ranked findings

- **CRITICAL:** None observed.
- **BOUND:** The evidence is this pristine-run audit and its declared finite vector/fault panel; it is not a proof over ungenerated runner states or a remeasurement of C1/C2. No broader claim is made.
- **HYGIENE:** No vector-count mismatch: tool-reported and independently recomputed totals are both `30316`.

The pristine runner's structure/static checks passed, all 30,316 runtime executions matched the oracle, and the harness rejected all 34 injected fault cases. I could not break any of those checks in this run. No runner/tool bytes were edited; no C1/C2 counter, public/sealed panel, build, lint, or unrelated verification was run. No tools were installed. There are no blockers beyond the stated finite-scope bound.