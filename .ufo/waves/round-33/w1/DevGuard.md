# DevGuard — round 33 wave 1, dev sweep of the frozen tally-audit v2

## Verdict

Five non-equivalent mutants of the pinned runner survive the frozen tool v2 (`TALLY_AUDIT: PASS`,
exit 0): `p_fail_and_keep`, `p_setup_and_keep`, `p_fail_and_auto0`, `p_setup_and_auto0`,
`p_fail_and_root`. Each adds one conjunct over an **ambient run variable** to the FAIL or SETUP
precedence if. The tool's runtime oracle executes every status vector under
`local root=tally-audit auto=0 KEEP=1` (`tool.py:225`) — a configuration the runner reaches only as
`--workdir DIR --keep`. The runner's default invocation is `auto=1`, `KEEP=0`, `root` under `/tmp/`
(`pristine.sh:190`, `pristine.sh:1357-1361`). Under that default, four of the five mutants turn a
FAIL or a cannot-verify into `REGRESSION: PASS` with exit 0; the fifth (`p_fail_and_root`) does the
same for every workdir outside `/tmp`.

This is a harness-configuration blindness, not vector sparsity: the count sweep (`0..9` failing ×
`0..9` setup) and the dup/drop stress both run inside `run_vectors`, whose driver pins the ambient
triple (`tool.py:219-233`). No number of extra status vectors can see a conjunct whose variable the
driver holds constant. The runner's own selftest pins the identical triple
(`pristine.sh:2003`), so such a copy also passes `--selftest`'s tally comparison.

Sweep totals: 47 mutants (46 generated, 1 added probe) → 29 killed (exit 1), 1 refused (exit 2,
syntactically broken copy), 17 passed (exit 0), of which 12 are behaviorally equivalent and 5 are
genuine survivors. Baseline and restored bytes: PASS. I edited no production file.

## Setup and pins

```
mkdir -p /fast/scratch/hyaku/tameshi-r33-seats/DevGuard
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r33-seats/DevGuard/lane; echo $? > clone.exit
git -C lane checkout -q --detach f6d8a891f1d966c5c3cdda385090da3a6e804675; echo $? > checkout.exit
git -C lane show f6d8a891...:tools/tally-audit-v2.py  > tool.py;      echo $? > tool-fetch.exit
git -C lane show f6d8a891...:tools/mutate-and-run.sh  > pristine.sh;  echo $? > runner-fetch.exit
```

All four exits `0` (`clone.exit`, `checkout.exit`, `tool-fetch.exit`, `runner-fetch.exit`).

```
$ sha256sum tool.py pristine.sh
9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

Both match the contract pins (`tool_sha256`, `runner_sha256`).

## Detector and baseline

Detector = the frozen tool under audit, invoked exactly as the contract's interface:

```
timeout 300 python3 tool.py --runner pristine.sh > out_pristine.txt 2> err_pristine.txt; echo $? > rc_pristine.txt
```

Exit `0` (`rc_pristine.txt`); stdout:

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=2395 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=29/29
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Baseline is a pass, so a mutant's PASS is a survival, and a mutant's FAIL is a kill.

## Mutant construction

`gen.py` applies one exact string replacement per mutant and aborts unless the old string occurs
exactly once and the body changes (`assert` on `src.count(old) == 1`, `body != src`). Files:
`mutants/m_<id>.sh`; manifest `manifest.json` (id, note, edit, sha256). All edits land inside
`run_regression`'s tally region (`pristine.sh:1440-1465`); the head (`st_*=$?`) and the harness
section are untouched, so `CHECK head` and `CHECK harness` stay PASS for every mutant and the
verdicts below are `CHECK runtime` decisions.

Driver (parallel, 16 at a time; exit captured per receipt discipline):

```
xargs -a ids.txt -P 16 -n 1 ./runone.sh     # runone.sh: timeout 300 python3 tool.py --runner mutants/m_$id.sh; echo $? > res/$id.rc
```

`batch_exit=0`; `tool.py` re-hashed after the sweep: `9dbbce62...33a4` (unchanged);
`pristine.sh`: `a7d3f2dd...2eb9` (unchanged).

### Verdict table (47 mutants)

| id | edit | tool exit | verdict |
|---|---|---|---|
| `g_after_pass` | guard after PASS printf | 1 | killed |
| `g_bracket` | arithmetic in `[[ ]]` | 2 | refused (SETUP) |
| `g_double_npass` | npass double counted in the sum | 1 | killed |
| `g_drop_nfail` | nfail term dropped from the sum | 0 | equivalent |
| `g_drop_npass` | npass term dropped from the sum | 1 | killed |
| `g_drop_nsetup` | nsetup term dropped from the sum | 0 | equivalent |
| `g_eq` | `!=` → `==` | 1 | killed |
| `g_exit1` | guard `exit 2` → `exit 1` | 1 | killed |
| `g_exit3` | guard `exit 2` → `exit 3` | 1 | killed |
| `g_false` | guard never fires | 1 | killed |
| `g_ge` | `!=` → `>=` | 1 | killed |
| `g_gt` | `!=` → `>` (overcount only) | 1 | killed |
| `g_keep_conj` | guard gated on `$KEEP -eq 1` | 0 | equivalent (unreachable) |
| `g_le` | `!=` → `<=` | 1 | killed |
| `g_lit8` | `!= nlegs` → `!= 8` | 1 | killed |
| `g_lit9` | `!= nlegs` → `!= 9` | 0 | equivalent |
| `g_lt` | `!=` → `<` (undercount only) | 1 | killed |
| `g_moved_before_fail` | guard block before the FAIL if | 0 | equivalent (unreachable) |
| `g_plus1` | `!= nlegs` → `!= nlegs + 1` | 1 | killed |
| `g_removed` | guard deleted | 1 | killed |
| `g_true` | guard always fires | 1 | killed |
| `p_exit_before_printf` | `exit 1` before the FAIL printf | 1 | killed |
| `p_fail_and_auto0` | `$nfail -gt 0 && $auto -eq 0` | 0 | **SURVIVOR** |
| `p_fail_and_keep` | `$nfail -gt 0 && $KEEP -eq 1` | 0 | **SURVIVOR** |
| `p_fail_and_nosetup` | `$nfail -gt 0 && $nsetup -eq 0` | 1 | killed |
| `p_fail_and_npasslt8` | `$nfail -gt 0 && $npass -lt 8` | 1 | killed |
| `p_fail_and_npassltn` | `$nfail -gt 0 && $npass -lt $nlegs` | 0 | equivalent |
| `p_fail_and_root` | `$nfail -gt 0 && $root != /tmp/*` | 0 | **SURVIVOR** |
| `p_fail_eq1` | `-gt 0` → `-eq 1` | 1 | killed |
| `p_fail_exit2` | FAIL `exit 1` → `exit 2` | 1 | killed |
| `p_fail_ge1` | `-gt 0` → `-ge 1` | 0 | equivalent |
| `p_fail_ge2` | `-gt 0` → `-ge 2` | 1 | killed |
| `p_fail_gt1` | `-gt 0` → `-gt 1` | 1 | killed |
| `p_fail_ne0` | `-gt 0` → `-ne 0` | 0 | equivalent |
| `p_fail_no_exit` | FAIL branch falls through | 1 | killed |
| `p_fail_or_setup1` | `\|\| $nsetup -gt 1` | 1 | killed |
| `p_fail_or_stjs3` | `\|\| $st_js -eq 3` | 1 | killed |
| `p_fail_return` | FAIL `exit 1` → `return 1` | 0 | equivalent |
| `p_setup_and_auto0` | `$nsetup -gt 0 && $auto -eq 0` | 0 | **SURVIVOR** |
| `p_setup_and_fail0` | `$nsetup -gt 0 && $nfail -eq 0` | 0 | equivalent |
| `p_setup_and_keep` | `$nsetup -gt 0 && $KEEP -eq 1` | 0 | **SURVIVOR** |
| `p_setup_eq1` | `-gt 0` → `-eq 1` | 1 | killed |
| `p_setup_exit1` | SETUP `exit 2` → `exit 1` | 1 | killed |
| `p_setup_ge1` | `-gt 0` → `-ge 1` | 0 | equivalent |
| `p_setup_gt1` | `-gt 0` → `-gt 1` | 1 | killed |
| `p_setup_return` | SETUP `exit 2` → `return 2` | 0 | equivalent |
| `p_swap_blocks` | SETUP precedence before FAIL | 1 | killed |

`g_bracket` was refused with exit 2 because `[[ npass + nfail + nsetup != nlegs ]]` is a bash
syntax error inside `[[ ]]`; the tool's SETUP line names the driver failure. A copy that does not
parse is not a survivor candidate.

The 29 kills show the vector sweep is strong on the family's pure-count logic: precedence swaps,
thresholds (`-eq 1`, `-gt 1`, `-ge 2`), disjuncts on a leg variable, guard comparison changes
(`<`, `>`, `<=`, `>=`, `==`, literal 8, off-by-one), guard `exit` code changes, guard removal, and
exit placement are all caught. The dup/drop stress is what kills the two guard `exit` edits and the
guard deletion (`g_exit1`, `g_exit3`, `g_removed`) even though no intact-count vector reaches the
guard. The survivors are exactly the sub-family the count sweep and stress cannot reach, because
the reused driver holds the ambient variables constant.

## Survivors (expected detector output, actual output)

Detector expectation for each: `TALLY_AUDIT: FAIL` (exit 1), since each mutant is a behavior-bearing
change to the PASS/FAIL/SETUP decision. Actual: `TALLY_AUDIT: PASS` (exit 0). All five show
`CHECK runtime PASS vectors=2395 mismatched=0` and `CHECK harness PASS ... 29/29`.

Witnesses come from `cmp.py`, an independent differential that extracts the tally block from
`pristine.sh` and from the mutant (same `local nlegs=9 ...` header to the closing `}`) and runs both
functions in one bash process over 4,891 vectors (every status `0..255` at every position, every
`(failing, setup)` count pair, every placement permutation for `(1,1)`, `(2,1)`, `(1,2)`, `(2,2)`,
plus 1,200 random multi-valued vectors), comparing **full stdout and exit code**, under each
`(auto, KEEP)` configuration. Logs: `cmpres/<id>.a<auto>k<KEEP>.txt`.

### 1. `p_fail_and_keep` — FAIL precedence gated on `--keep`

Edit at `pristine.sh:1441` (mutant `mutants/m_p_fail_and_keep.sh`):

```diff
-  if [[ $nfail -gt 0 ]]; then
+  if [[ $nfail -gt 0 && $KEEP -eq 1 ]]; then
```

Tool: `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`, exit 0.
Witness (`cmpres/p_fail_and_keep.a1k0.txt`, `auto=1 KEEP=0` — the default `--regression`
invocation), vector `1 0 0 0 0 0 0 0 0`:

```
pristine: exit 1  REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
mutant:   exit 0  REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)
```

2,369 of 4,891 vectors differ under the default; 0 differ under the tool's pinned
`auto=0 KEEP=1`. A failing regression leg reports success unless the operator passed `--keep`.

### 2. `p_setup_and_keep` — SETUP precedence gated on `--keep`

Edit at `pristine.sh:1447`:

```diff
-  if [[ $nsetup -gt 0 ]]; then
+  if [[ $nsetup -gt 0 && $KEEP -eq 1 ]]; then
```

Witness (`cmpres/p_setup_and_keep.a1k0.txt`), vector `2 0 0 0 0 0 0 0 0`:

```
pristine: exit 2  REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
mutant:   exit 0  REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)
```

2,512 of 4,891 vectors differ under the default; 0 under the pinned config. A leg that cannot be
verified is reported as a pass, and with `KEEP=0` the workdir is removed on the way out
(`REGRESSION_WORKDIR: ... (removed on PASS; --keep retains)`), so the evidence for the missing
verification is deleted too.

### 3. `p_fail_and_auto0` — FAIL precedence gated on an explicit `--workdir`

Edit at `pristine.sh:1441`:

```diff
-  if [[ $nfail -gt 0 ]]; then
+  if [[ $nfail -gt 0 && $auto -eq 0 ]]; then
```

Witness (`cmpres/p_fail_and_auto0.a1k0.txt`), vector `1 0 0 0 0 0 0 0 0`: pristine exit 1 FAIL,
mutant exit 0 PASS. 2,369 vectors differ whenever `auto=1` (no `--workdir`, i.e. the default), same
output under `auto=0`.

### 4. `p_setup_and_auto0` — SETUP precedence gated on an explicit `--workdir`

Edit at `pristine.sh:1447`:

```diff
-  if [[ $nsetup -gt 0 ]]; then
+  if [[ $nsetup -gt 0 && $auto -eq 0 ]]; then
```

Witness (`cmpres/p_setup_and_auto0.a1k0.txt`), vector `2 0 0 0 0 0 0 0 0`: pristine exit 2 SETUP,
mutant exit 0 PASS. 2,512 vectors differ with `auto=1`.

### 5. `p_fail_and_root` — FAIL precedence gated on the workdir path

Edit at `pristine.sh:1441`:

```diff
-  if [[ $nfail -gt 0 ]]; then
+  if [[ $nfail -gt 0 && $root != /tmp/* ]]; then
```

Witness (`cmpres/p_fail_and_root.a1k0.txt`), vector `1 0 0 0 0 0 0 0 0`: pristine exit 1 FAIL,
mutant exit 0 PASS. The runner's automatic root is `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`
(`pristine.sh:1359`), so the default path always matches `/tmp/*` and the conjunct is always false;
only an explicit `--workdir` outside `/tmp` keeps the FAIL line. 2,369 vectors differ.

The three ambient variables are the whole exposed surface: `$auto`, `$KEEP` and `$root` are the only
`run_regression`-scope variables the tally block reads that the driver does not fix to a value the
real run also uses. `$nlegs` and the nine leg statuses are pinned correctly by the driver; `$auto`,
`$KEEP` and `$root` are pinned to a non-default tuple (`auto=0 KEEP=1 root=tally-audit`).

## Equivalent survivors (12) and why

For each, `cmp.py` reports `TOTALDIFF 0` over 4,891 vectors in all three un-pinned configurations
(`auto=0 KEEP=0`, `auto=1 KEEP=0`, `auto=1 KEEP=1`); the tool's pinned configuration is identical by
construction. Logs: `cmpres/<id>.a<auto>k<KEEP>.txt`.

- **Unreachable-region guard edits** (`g_drop_nfail`, `g_drop_nsetup`, `g_keep_conj`,
  `g_moved_before_fail`): the guard sits after the FAIL if and the SETUP if, both of which exit, so
  it is reached only with `nfail == 0` and `nsetup == 0`. Dropping those terms, gating the whole
  guard on `$KEEP`, or hoisting it above the FAIL if cannot change any state the block can reach
  with nine legs each counted once (`sum == nlegs == 9`). `g_moved_before_fail` would differ on a
  copy that both loses a tally count and carries a non-zero status, but a lost or duplicated
  operand is rejected statically (`CHECK static ... loop operands != legs`), so no copy that reaches
  the runtime comparison can exhibit it.
- **Constant-folded edits** (`g_lit9`): `nlegs` is `9` by the block's own `local nlegs=9`.
- **Integer-equivalent thresholds** (`p_fail_ge1`, `p_fail_ne0`, `p_setup_ge1`): for non-negative
  counts `-gt 0`, `-ge 1`, `-ne 0` are the same predicate.
- **Redundant conjuncts** (`p_fail_and_npassltn`: `nfail > 0` implies `npass <= 8 < nlegs`;
  `p_setup_and_fail0`: the FAIL if already exited when `nfail > 0`).
- **`return` instead of `exit` in a branch** (`p_fail_return`, `p_setup_return`): the block runs
  inside `run_regression`, and the only caller is the final `case "$MODE" in ... regression)
  run_regression ;; esac` at `pristine.sh:2075-2080`, after which the script ends; a function
  `return` propagates the same status the `exit` would. Probe:

  ```
  bash -c 'f(){ return 1; }; case a in a) f ;; esac'; echo $?   # 1
  bash -c 'f(){ exit 1; };   case a in a) f ;; esac'; echo $?   # 1
  ```

  These would diverge if anything ran after the dispatch or an EXIT trap existed; at this pin
  neither holds.

## Smallest safe correction (for the L1; I made no production edits)

`tool.py:219-233` (`run_vectors`) builds its driver with a fixed ambient triple on line 225. Run the
same vector set once per runner configuration rather than once total, and require the oracle for
each. The cheapest set that kills all five survivors, measured by `cmp.py`:

1. Add the runner's default tuple `root=/tmp/tally-audit.XXXX auto=1 KEEP=0`. This single extra
   configuration already kills all five (`p_fail_and_auto0` and `p_setup_and_auto0` differ at
   `auto=1` regardless of `KEEP`; `p_fail_and_keep`, `p_setup_and_keep`, `p_fail_and_root` differ
   with `KEEP=0` and a `/tmp/`-shaped root).
2. Cover the four `(auto, KEEP)` combinations `{0,1} × {0,1}` plus the `/tmp`-shaped root, so a
   future conjunct on any one of the three is visible. Only the 55 `(failing, setup)` count-pair
   vectors plus one single-status vector per configuration are needed for this — a conjunct that is
   invisible on these is invisible on the full sweep for the same configuration. Cost is roughly
  4 × 56 extra runs.
3. Keep the pinned tuple as a fifth configuration if a positive control for the `--workdir --keep`
   shape is wanted; do not keep it as the only one.

The same pin exists in the runner's own selftest at `pristine.sh:2003`
(`local root=selftest-tally auto=0 KEEP=1`), so a runner copy carrying any of these five edits also
passes `--selftest`'s tally comparison. If the runner's selftest is meant to be a second opinion on
this block, it needs the same configuration sweep; that is a runner change, outside this seat's
scope and outside the frozen tool bytes.

Nothing in the audit's static, head, or harness checks needs to change: all 47 mutants kept
`head=pass` and `harness=pass`, and the 29 kills show the existing vector set and stress do their
job within one configuration.

## Restoration and hygiene evidence

- `tool.py` sha256 before and after the sweep: `9dbbce62...33a4` (contract pin). `pristine.sh`:
  `a7d3f2dd...2eb9` (contract pin), unchanged.
- Restored-bytes run: `cp pristine.sh restored.sh`; `sha256sum pristine.sh restored.sh` both
  `a7d3f2dd...2eb9` (`restored_hash.txt`); `timeout 300 python3 tool.py --runner restored.sh` exit
  `0` (`rc_restored.txt`) with
  `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` (`out_restored.txt`).
- Mutants are fresh copies under `/fast/scratch/hyaku/tameshi-r33-seats/DevGuard/mutants/`; the
  pinned bytes were never edited in place, so nothing needed restoring there.
- Every cited command captured its own exit with `cmd; echo $? > file`; runs were wrapped in
  `timeout 300`, parallelized 16 wide (32 cores), and all finished in `batch_exit=0` / `cmp_batch=0`.
- No process started by this seat remains; no kill was issued to any process. No `git` write command
  ran outside the scratch clone; no `jj` command ran anywhere; no production or sibling-lane file
  was written. The only file written outside the scratch directory is this report.
- No tools were installed or upgraded (no pacman, uv, npm or binary installs).
- Sweep log: `/fast/scratch/hyaku/tameshi-r33-seats/DevGuard/` (`ids.txt`, `manifest.json`,
  `res/<id>.{out,rc,last}`, `cmpres/<id>.a<auto>k<KEEP>.txt`, `gen.py`, `cmp.py`).
