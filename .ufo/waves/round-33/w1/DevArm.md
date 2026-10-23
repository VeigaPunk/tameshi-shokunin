# DevArm — round 33, wave 1: dev sweep against frozen tally-audit-v2

## Verdict

**Nine of 39 single-edit `case $st in` arm mutants survive the frozen v2** (tool exits 0, `TALLY_AUDIT: PASS`) while producing different REGRESSION stdout on status vectors that occur in real runs. Ten further passes are behaviorally equivalent to pristine. The survivor class the all-statuses sweep still misses is **co-occurrence**: the runtime oracle never puts a status ≥ 3 on one leg while any other leg is non-zero, and it drives the tally block with a hardcoded context (`root=tally-audit auto=0 KEEP=1`) that the real `run_regression` default does not use.

Strongest survivors (context-free, pure status co-occurrence): `m17`, `m18`, `m32`, `m33`. They are also accepted 23/23 by the unchanged selftest harness panel that ships inside the runner copy, so a copy carrying one of them passes both the audit and its own `--selftest`.
Weaker survivors (context-only): `m19`, `m20`, `m37`, `m38`, `m39` — invisible only because the tool's bash driver pins `root`/`auto`/`KEEP`, while the real default `--regression` path runs with `auto=1`, `KEEP=0`, `root=/tmp/tameshi-r4-2-regression.XXXXXX`.

Everything below is from the frozen bytes at `f6d8a891f1d966c5c3cdda385090da3a6e804675`; the pinned runner was never edited.

## Setup and hashes

Working directory: `/fast/scratch/hyaku/tameshi-r33-seats/DevArm/`

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../DevArm/lane          # exit 0
git -C lane checkout -q --detach f6d8a891f1d966c5c3cdda385090da3a6e804675  # exit 0
git -C lane show <commit>:tools/tally-audit-v2.py > tool.py               # exit 0
git -C lane show <commit>:tools/mutate-and-run.sh > pristine.sh           # exit 0
sha256sum tool.py pristine.sh
  9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tool.py
  a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh   # matches the pinned a7d3f2dd...2eb9
```

Baseline detector on pristine bytes (exit code captured separately, not with `&&`):

```
timeout 300 python3 tool.py --runner pristine.sh > baseline.out 2>&1; echo $? > baseline.rc
cat baseline.rc        # 0
cat baseline.out
  CHECK head PASS legs=9
  CHECK static PASS legs=9 operands=9 nlegs=9
  CHECK runtime PASS vectors=2395 mismatched=0
  CHECK harness PASS reference cases=9; faults rejected=29/29
  TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

The baseline PASS (not a failure) means a mutant verdict is meaningful.

## Method

1. `mutants.py` builds 39 runner copies, each one exact-string replacement in the tally block. Every edit asserts `pristine.sh.count(old) == 1` before writing and rejects a no-op; the pinned file itself is opened read-only.
2. Each mutant is audited with the frozen tool exactly as the contract names it:
   `timeout 300 python3 tool.py --runner m_<id>.sh`, return code and final `TALLY_AUDIT:` line recorded in `sweep.tsv` (one row per mutant).
3. For every exit-0 mutant, `equiv.py` imports the frozen tool's own parser (`regression_body`, `tally_block`, `leg_names`) and runs the pristine block and the mutant block in bash as
   `tally() { local st_js=${1} ... st_citecheck=${9}; local root=... auto=... KEEP=...; <block>; }`,
   comparing exit code and first stdout line over **6367 vectors** in two contexts:
   - all 256 statuses at every one of the 9 positions;
   - every ordered pair of positions with every status pair 0..9 (7200 vectors, deduplicated below);
   - high-status pairs (2,3,4,5,9,126,127,255) at six placements plus the two-corner placements;
   - 1200 sparse random mixes of 2–4 non-zero legs with statuses {1,2,3,5,9,126,127,255};
   - context `tool-driver` = `(root=tally-audit, auto=0, KEEP=1)`, the exact values at `tool.py:225`;
   - context `real-default` = `(root=/tmp/tameshi-r4-2-regression.witness, auto=1, KEEP=0)`, the values the default regression path uses.
   Exit code of the sweep was captured: `equiv_exit=0`; log `equiv.log`.

## Sweep log (39 mutants, 20 killed, 19 passed)

Killed (18 × exit 1, 2 × exit 2) — these are correct detections:

| id | tool exit | failing check |
|---|---|---|
| m01 arm `0)`→`00)` | 1 | runtime |
| m02 arm `0)` adds 2 | 1 | runtime |
| m06 extra arm `2) npass` | 1 | runtime |
| m07 `*)` moved first | 1 | runtime |
| m09 `0)` fall-through `;&` | 1 | runtime |
| m10 `1)` fall-through `;;&` | 1 | runtime |
| m13 `1)` double count | 1 | runtime |
| m14 `case $st_js in` | 2 | SETUP: counting case not found |
| m15 `case $nlegs in` | 2 | SETUP: counting case not found |
| m16 `*)` keyed on `st_js = 2` | 1 | runtime (16 mismatches, the fixed mixes) |
| m21 `0)` keyed on `KEEP = 1` | 1 | runtime (driver KEEP=1 fires the gate) |
| m22 pattern `+0)` | 1 | runtime |
| m25 pattern `[1-2])` | 1 | runtime |
| m26 pattern `*[!0-1])` | 1 | runtime |
| m28 extra arm `255) npass` | 1 | runtime |
| m29 extra arm `2) nfail` | 1 | runtime |
| m30 `0)`/`1)` bodies swapped | 1 | runtime |
| m34 pattern `'*'` (quoted) | 1 | runtime |
| m35 `0)` counts as fail | 1 | runtime |
| m36 `1)` counts as setup | 1 | runtime |

Passed (exit 0) — 10 behaviorally equivalent, 9 survivors:

| id | equivalence | diffs / 6367 per context |
|---|---|---|
| m03 quoted `"0")` | equivalent | t=0 r=0 |
| m04 unreachable `-*)` before `0)` | equivalent | 0/0 |
| m05 extra `2) nsetup` | equivalent | 0/0 |
| m08 `0)`/`1)` arms swapped | equivalent | 0/0 |
| m11 `0) ((npass++))` | equivalent | 0/0 |
| m12 `0)` arithmetic cancel | equivalent | 0/0 |
| m23 pattern `0*)` | equivalent | 0/0 |
| m24 pattern `[0])` | equivalent | 0/0 |
| m27 pattern `?*` (identical to `*`) | equivalent | 0/0 |
| m31 `*)` body `;;&` at last arm | equivalent | 0/0 |
| **m17** `*)` cascade: prior setup + `st > 2` → fail | **SURVIVOR** | t=3051 r=3051 |
| **m18** `*)` cascade: prior fail + `st > 2` → fail | **SURVIVOR** | t=478 r=478 |
| **m19** `0)` keyed on `auto = 0` | **SURVIVOR** | t=0 **r=6367** |
| **m20** `0)` keyed on `root == /tmp/*` | **SURVIVOR** | t=0 **r=6367** |
| **m32** `*)` double count gated on `st > 2 && nsetup > 1` | **SURVIVOR** | t=3051 r=3051 |
| **m33** `*)` keyed on `st_mado = 3 && st_checklist != 0` | **SURVIVOR** | t=23 r=23 |
| **m37** `0)` keyed on `KEEP = 0` | **SURVIVOR** | t=0 **r=6367** |
| **m38** `*)` keyed on `auto = 1` | **SURVIVOR** | t=0 **r=6320** |
| **m39** `*)` keyed on `root == /tmp/*` | **SURVIVOR** | t=0 **r=6320** |

## Survivor evidence (exact edits, exact outputs)

Each witness below was re-run standalone with the task's own recipe (function `tally()`, nine positional statuses, `echo`-style capture of `rc:first-line`). `witness_one.sh` for the first four and `w33.sh` for m33 use context `(root=tally-audit, auto=0, KEEP=1)`; the context-keyed five use `(root=/tmp/tameshi-r4-2-regression.witness, auto=1, KEEP=0)`.

### m17 — `*)` cascade when a setup leg precedes a status ≥ 3

```
-      *) nsetup=$((nsetup + 1)) ;;
+      *) if [ "$nsetup" -ge 1 ] && [ "$st" -gt 2 ]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
vector 2 3 0 0 0 0 0 0 0
  pristine => 2:REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
  mutant   => 1:REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
```

Real meaning: one leg cannot verify (status 2), another leg fails (status 3 is any non-0/1 status); pristine refuses as SETUP, the copy reports FAIL with a leg miscounted. 3051 differing vectors in both contexts.

### m18 — `*)` cascade when a failing leg precedes a status ≥ 3

```
-      *) nsetup=$((nsetup + 1)) ;;
+      *) if [ "$nfail" -ge 1 ] && [ "$st" -gt 2 ]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
vector 1 3 0 0 0 0 0 0 0
  pristine => 1:REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
  mutant   => 1:REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
```

Same exit code, different first stdout line — the check compares the line, so this is a real behavioural difference, and the sweep compares lines too; 478 differing vectors.

### m32 — conditional double count gated on a prior setup and a status ≥ 3

```
-      *) nsetup=$((nsetup + 1)) ;;
+      *) nsetup=$((nsetup + 1)); if [[ $st -gt 2 && $nsetup -gt 1 ]]; then nfail=$((nfail + 1)); fi ;;
vector 2 3 0 0 0 0 0 0 0
  pristine => 2:REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
  mutant   => 1:REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=2)
```

### m33 — `*)` arm keyed on two other legs

```
-      *) nsetup=$((nsetup + 1)) ;;
+      *) if [[ $st_mado = 3 && $st_checklist != 0 ]]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
vector 0 0 0 3 1 0 0 0 0
  pristine => 1:REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
  mutant   => 1:REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
```

The hand-picked variant `0 0 0 3 5 0 0 0 0` gives the same pair of lines (`pristine => ... failed=1 setup=1`, `mutant => ... failed=2 setup=0`). Only 23 of 6367 vectors differ, so this is exactly the sparse co-occurrence the panel does not sample.

### m19 — `0)` arm keyed on `auto`

```
-      0) npass=$((npass + 1)) ;;
+      0) if [ "$auto" = 0 ]; then npass=$((npass + 1)); else nfail=$((nfail + 1)); fi ;;
vector 0 0 0 0 0 0 0 0 0, ctx auto=1 KEEP=0 root=/tmp/...
  pristine => 0:REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
  mutant   => 1:REGRESSION: FAIL (cases=9 passed=0 failed=9 setup=0)
```

### m20 — `0)` arm keyed on `root`

```
-      0) npass=$((npass + 1)) ;;
+      0) if [[ "$root" == /tmp/* ]]; then nfail=$((nfail + 1)); else npass=$((npass + 1)); fi ;;
same vector/context
  pristine => 0:REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
  mutant   => 1:REGRESSION: FAIL (cases=9 passed=0 failed=9 setup=0)
```

### m37 — `0)` arm keyed on `KEEP`

```
-      0) npass=$((npass + 1)) ;;
+      0) if [ "$KEEP" = 0 ]; then nfail=$((nfail + 1)); else npass=$((npass + 1)); fi ;;
same vector/context
  pristine => 0:REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
  mutant   => 1:REGRESSION: FAIL (cases=9 passed=0 failed=9 setup=0)
```

### m38 — `*)` arm keyed on `auto`

```
-      *) nsetup=$((nsetup + 1)) ;;
+      *) if [ "$auto" = 1 ]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
vector 2 0 0 0 0 0 0 0 0, ctx auto=1 KEEP=0 root=/tmp/...
  pristine => 2:REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
  mutant   => 1:REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
```

### m39 — `*)` arm keyed on `root`

```
-      *) nsetup=$((nsetup + 1)) ;;
+      *) if [[ "$root" == /tmp/* ]]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
same vector/context
  pristine => 2:REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
  mutant   => 1:REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
```

## Why the frozen sweep misses these

1. **Co-occurrence gap in the runtime vector list.** `check_runtime` (`tool.py:309-357`) sweeps every status 0..255 at every position but with all other legs 0 (`tool.py:317-324`), then uses only 0/1/2 for multi-non-zero vectors: `count_vectors` is `[1]*fc + [2]*sc + [0]*...` (`tool.py:299-307`), and the six fixed mixes (`tool.py:327-338`) add contiguous 1/2 blocks plus a reversed copy. Statuses ≥ 3 therefore never co-occur with any second non-zero leg. `m17`, `m18`, `m32` need a prior setup/fail plus a later status ≥ 3; `m33` needs `st_mado=3` together with a non-zero `st_checklist`. All four are rejected by the real runner semantics and accepted by the sweep (0 mismatches in 2395).
2. **Hardcoded block context.** The bash driver writes `local root=tally-audit auto=0 KEEP=1` (`tool.py:219-225`, the literal at `tool.py:225`). The real path does not: `pristine.sh:1357` starts with `local root specs auto=0`, `pristine.sh:1359-1361` takes `root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX)` and sets `auto=1` when `--workdir` is absent, and `KEEP=0` is the default (`pristine.sh:190`) with `--keep` setting 1 (`pristine.sh:2067`). An arm keyed on `auto`, `root` or `KEEP` therefore reads different values in the audit than in the default regression run; `m19`, `m20`, `m37`, `m38`, `m39` show it.
3. **The harness check never runs the copy's own block through the copy's harness.** `check_harness` (`tool.py:447-462`) injects `REF_BLOCK` and 29 fault blocks into the harness; it never injects the runner's own tally block. The four status-combination survivors are accepted 23/23 by the shipped harness panel (all-pass, one status 1/2 at each of nine positions, `1 1`, `2 2`, `1 2`, `3 0`): panel script `panel.sh`, result `m17 23/23, m18 23/23, m32 23/23, m33 23/23; pristine 23/23`, exit 0. So a copy whose block is wrong in a co-occurrence its harness also never samples passes the audit and its own `--selftest`.

## Smallest safe correction (tool side, no runner edit)

- In `check_runtime`, append co-occurrence vectors: for every ordered position pair (i, j) and every status pair from a small high-value set, e.g. `a, b ∈ {0, 1, 2, 3, 5, 126, 127, 255}`, place `a` at i and `b` at j. This costs 8×8×9×8 = 4608 vectors (about 1.6 s of bash time at the measured 2800 vectors/s) and catches `m17`, `m18`, `m32`, `m33` at their first witness.
- In `run_vectors`, run the block twice: once with the current fixed context and once with `local root=/tmp/tameshi-r4-2-regression.audit auto=1 KEEP=0`, the values the default `run_regression` path actually has. This catches `m19`, `m20`, `m37`, `m38`, `m39` and costs one more driver pass.
- Optionally, also inject the runner's own extracted tally block into its harness panel and require acceptance; that would catch a block and harness that share a gap, but it adds a second reading of the copy's own block and is not needed for the four strongest survivors once the co-occurrence vectors are in.

No contract change: these are additions to the existing `runtime` check. I am not judging or integrating; this is a coverage finding for the L1 and for the wave that authors the fresh held-out set.

## Restoration evidence

Mutants were separate files (`m_<id>.sh`); the pinned runner copy was never written. Byte identity after the full sweep:

```
sha256sum pristine.sh tool.py
  a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
  9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tool.py
```

Both hashes equal the values taken before any mutant existed. No process was left running, no install was needed (no pacman, uv or npx transaction), and no file outside `/fast/scratch/hyaku/tameshi-r33-seats/DevArm/` and this report was written.

## Appendix: exact replacement for all 39 mutants

`old` occurs exactly once in `pristine.sh`; `new` is the full replacement. Indentation kept.

```
m01-arm-00:
  -      0) npass=$((npass + 1)) ;;
  +      00) npass=$((npass + 1)) ;;
m02-arm-0-plus2:
  -      0) npass=$((npass + 1)) ;;
  +      0) npass=$((npass + 2)) ;;
m03-arm-quoted:
  -      0) npass=$((npass + 1)) ;;
  +      "0") npass=$((npass + 1)) ;;
m04-arm-unreachable-neg:
  -    case $st in
  -      0) npass=$((npass + 1)) ;;
  +    case $st in
  +      -*) nfail=$((nfail + 1)) ;;
  +      0) npass=$((npass + 1)) ;;
m05-arm-extra2-setup:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      2) nsetup=$((nsetup + 1)) ;;
  +      *) nsetup=$((nsetup + 1)) ;;
m06-arm-extra2-pass:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      2) npass=$((npass + 1)) ;;
  +      *) nsetup=$((nsetup + 1)) ;;
m07-arm-star-first:
  -      0) npass=$((npass + 1)) ;;
  -      1) nfail=$((nfail + 1)) ;;
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *) nsetup=$((nsetup + 1)) ;;
  +      1) nfail=$((nfail + 1)) ;;
  +      0) npass=$((npass + 1)) ;;
m08-arm-swap-disjoint:
  -      0) npass=$((npass + 1)) ;;
  -      1) nfail=$((nfail + 1)) ;;
  +      1) nfail=$((nfail + 1)) ;;
  +      0) npass=$((npass + 1)) ;;
m09-arm-fallthrough-0:
  -      0) npass=$((npass + 1)) ;;
  +      0) npass=$((npass + 1)) ;&
m10-arm-fallthrough-1:
  -      1) nfail=$((nfail + 1)) ;;
  +      1) nfail=$((nfail + 1)) ;;&
m11-arm-arith-postinc:
  -      0) npass=$((npass + 1)) ;;
  +      0) ((npass++)) ;;
m12-arm-arith-cancel:
  -      0) npass=$((npass + 1)) ;;
  +      0) npass=$((npass + 2 - 1)) ;;
m13-arm-double-count-1:
  -      1) nfail=$((nfail + 1)) ;;
  +      1) nfail=$((nfail + 1)); nfail=$((nfail + 1)) ;;
m14-arm-case-var-js:
  -    case $st in
  +    case $st_js in
m15-arm-case-var-nlegs:
  -    case $st in
  +    case $nlegs in
m16-arm-default-keyed-js2:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *) if [ "$st_js" = 2 ]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
m17-arm-cascade-setup-high:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *) if [ "$nsetup" -ge 1 ] && [ "$st" -gt 2 ]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
m18-arm-cascade-fail-high:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *) if [ "$nfail" -ge 1 ] && [ "$st" -gt 2 ]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
m19-arm-keyed-auto:
  -      0) npass=$((npass + 1)) ;;
  +      0) if [ "$auto" = 0 ]; then npass=$((npass + 1)); else nfail=$((nfail + 1)); fi ;;
m20-arm-keyed-root:
  -      0) npass=$((npass + 1)) ;;
  +      0) if [[ "$root" == /tmp/* ]]; then nfail=$((nfail + 1)); else npass=$((npass + 1)); fi ;;
m21-arm-keyed-keep:
  -      0) npass=$((npass + 1)) ;;
  +      0) if [ "$KEEP" = 1 ]; then nfail=$((nfail + 1)); else npass=$((npass + 1)); fi ;;
m22-arm-pattern-literal-plus:
  -      0) npass=$((npass + 1)) ;;
  +      +0) npass=$((npass + 1)) ;;
m23-arm-pattern-0glob:
  -      0) npass=$((npass + 1)) ;;
  +      0*) npass=$((npass + 1)) ;;
m24-arm-pattern-charclass:
  -      0) npass=$((npass + 1)) ;;
  +      [0]) npass=$((npass + 1)) ;;
m25-arm-pattern-range:
  -      1) nfail=$((nfail + 1)) ;;
  +      [1-2]) nfail=$((nfail + 1)) ;;
m26-arm-pattern-negative-class:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *[!0-1]) nsetup=$((nsetup + 1)) ;;
m27-arm-pattern-onechar-plus:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      ?*) nsetup=$((nsetup + 1)) ;;
m28-arm-extra255-pass:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      255) npass=$((npass + 1)) ;;
  +      *) nsetup=$((nsetup + 1)) ;;
m29-arm-extra2-fail:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      2) nfail=$((nfail + 1)) ;;
  +      *) nsetup=$((nsetup + 1)) ;;
m30-arm-swap-bodies:
  -      0) npass=$((npass + 1)) ;;
  -      1) nfail=$((nfail + 1)) ;;
  +      0) nfail=$((nfail + 1)) ;;
  +      1) npass=$((npass + 1)) ;;
m31-arm-star-fallthrough-end:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *) nsetup=$((nsetup + 1)) ;;&
m32-arm-double-count-gated-setups:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *) nsetup=$((nsetup + 1)); if [[ $st -gt 2 && $nsetup -gt 1 ]]; then nfail=$((nfail + 1)); fi ;;
m33-arm-keyed-twolegs:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *) if [[ $st_mado = 3 && $st_checklist != 0 ]]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
m34-arm-star-quoted:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      '*') nsetup=$((nsetup + 1)) ;;
m35-arm-0-nfail:
  -      0) npass=$((npass + 1)) ;;
  +      0) nfail=$((nfail + 1)) ;;
m36-arm-1-setup:
  -      1) nfail=$((nfail + 1)) ;;
  +      1) nsetup=$((nsetup + 1)) ;;
m37-arm-keyed-keep0:
  -      0) npass=$((npass + 1)) ;;
  +      0) if [ "$KEEP" = 0 ]; then nfail=$((nfail + 1)); else npass=$((npass + 1)); fi ;;
m38-arm-keyed-auto-setup:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *) if [ "$auto" = 1 ]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
m39-arm-keyed-root-setup:
  -      *) nsetup=$((nsetup + 1)) ;;
  +      *) if [[ "$root" == /tmp/* ]]; then nfail=$((nfail + 1)); else nsetup=$((nsetup + 1)); fi ;;
```

Count: 39 mutants.
