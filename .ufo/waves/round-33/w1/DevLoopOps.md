# DevLoopOps — wave 1 dev sweep, frozen tally-audit-v2 against tally-loop mutants

## Verdict

**Two survivors.** The frozen tool (sha256 `9dbbce62…33a4`) prints `TALLY_AUDIT: PASS` (exit 0)
for two runner copies whose tally block produces different `REGRESSION:` lines from the pristine
block on reachable status vectors. Both defects live in the same coverage hole: **every status in
3..255 is only ever swept alone, with all other legs at 0.** No swept vector mixes a non-{0,1}
status with any other non-zero leg, so an arm that miscounts only in that coexistence is invisible.

**Five benign refactors are refused as SETUP (exit 2)** even though their tally block is
behaviourally identical to pristine over 8456 vectors. One of them (B13, a single-iteration inner
loop wrapping the counting `case`) is the round-32 class-3 defect recurring from the other side:
v2 identifies the tally loop by the literal `case $st in` and by `$st_*`-shaped operands, so an
equivalent loop spelled differently cannot be audited at all.

Everything else in my family was killed: operand duplication/omission, nlegs, arm ordering,
wildcard-first, guard weakening, printf field swap, fail/setup gating, status 3/126 arms, break
and a setup-before-fail conditional break.

## Setup, bytes, restoration

```
mkdir -p /fast/scratch/hyaku/tameshi-r33-seats/DevLoopOps
git clone -q --no-hardlinks <lane> .../DevLoopOps/lane          # rc 0   (clone.rc)
git -C lane checkout -q --detach f6d8a891f1d966c5c3cdda385090da3a6e804675   # rc 0 (checkout.rc)
git -C lane show <freeze>:tools/tally-audit-v2.py  > tool.py      # rc 0 (tool.rc)
git -C lane show <freeze>:tools/mutate-and-run.sh  > pristine.sh  # rc 0 (pristine.rc)
```

Byte facts, before and after the whole sweep (nothing under `tameshi-shokunin` was written):

```
9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh   # a7d3f2dd…2eb9, as required
git -C lane status --porcelain | wc -l  ->  0
```

All mutants are separate copies under `mut/`; `pristine.sh` and `tool.py` were never modified, and
the clone stayed clean (no index or worktree change). No production file, lane jj state, or Git
index was touched; no git write command ran anywhere; no jj command ran anywhere. No tool was
installed or upgraded for this seat.

Baseline on the pristine runner, same command shape as every mutant:

```
timeout 300 python3 tool.py --runner base.sh ; echo $? > base.rc
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=2395 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=29/29
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)      # rc=0
```

## Method

37 mutants, each one **contiguous exact-string replacement** of `pristine.sh` with the occurrence
count asserted to be exactly 1 before writing (`mutants.py`; any zero-count or no-op edit is
reported as NOTAPPLIED — none remained). Every mutant ran the frozen tool unchanged:

```
timeout 300 python3 tool.py --runner mut/<ID>.sh > res/<ID>.out 2> res/<ID>.err ; echo $? > res/<ID>.rc
```

Result distribution: **14 PASS, 18 FAIL, 5 SETUP** (`verdicts.tsv`).

For every PASS and every SETUP mutant I re-ran the *tally block alone* against an independent
oracle — the same wrapping contract the tool uses (`tally()` with nine positionals plus `root`,
`auto`, `KEEP`), and the assignment recipe `out=$(tally <9 statuses>); echo $?:${out%%$'\n'*}` —
over an 8456-vector battery: every status 0..255 at every position (2304), every (failing, setup)
count pair base and reversed (110), every ordered position pair over
{0,1,2,3,4,126,127,128,255} (2916), every triple of positions over {0,1,2,3} (5376), plus 1500
random vectors (`eqcheck.py`, importing the frozen tool's own `tally_block`/`run_vectors` helpers
so the block is extracted identically). A zero diff means behaviourally identical on that battery.

## Survivors

### S02 — a second distinct error status steals a pass

Edit (line 1437 of `pristine.sh`):

```
-      *) nsetup=$((nsetup + 1)) ;;
+      *) nsetup=$((nsetup + 1)); if (( st > 2 )); then if (( ${seen_hi:-0} > 0 )); then npass=$((npass - 1)); fi; seen_hi=1; fi ;;
```

Tool: exit 0, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`.

```
pristine  330000000 > rc=2 REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
S02       330000000 > rc=2 REGRESSION: SETUP (cases=9 passed=6 cannot-verify=2)
```

Witness vector `3 3 0 0 0 0 0 0 0` (two legs that exit 3, seven pass). Same exit code, different
pass count in the report line. 3382 of 8456 battery vectors differ.

### S03 — a non-{0,1} status stops the tally once something already failed

Edit (line 1437):

```
-      *) nsetup=$((nsetup + 1)) ;;
+      *) nsetup=$((nsetup + 1)); if (( st > 2 && nfail > 0 )); then break; fi ;;
```

Tool: exit 0, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`.

```
pristine  130000000 > rc=1 REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
S03       130000000 > rc=1 REGRESSION: FAIL (cases=9 passed=0 failed=1 setup=1)
```

Witness vector `1 3 0 0 0 0 0 0 0` (one failing leg, one leg exiting 3). 1437 of 8456 vectors
differ. This one is directly reachable in ordinary runs: statuses 126/127/255 and any non-0/1/2
exit are routine, and a mixed fail+setup vector is exactly the case the tool's own FAIL line
exists to report.

Why the runner's own sum guard does not save either case: the guard is reached only after the
`nfail -gt 0` and `nsetup -gt 0` branches, i.e. only when every counted status was 0. Both
mutants corrupt the counts while a fail or a setup is present, and the FAIL/SETUP print happens
first.

Coverage statement of the frozen sweep (`tool.py:316-336`, 2395 vectors): 2304 single-status
vectors (one non-zero leg, rest 0), 55 count-pair vectors built from `[1]*f + [2]*s + [0]*rest`,
and 36 placement variants of six (f,s) pairs — again only statuses 0, 1 and 2. The value 3..255
never coexists with another non-zero leg, and no vector contains two distinct error statuses.

## False rejects: benign, behaviourally identical, refused with exit 2

Each of the five is a single contiguous edit, verified `diffs=0` over the 8456-vector battery
(`eqcheck.py`), yet the tool cannot audit it:

| id | edit | tool output | diffs |
|---|---|---|---|
| B13 | single-iteration inner loop `for one in "$st"; do` wrapping the counting `case` | `SETUP (tally loop operand not a leg status: '"$st"')` | 0 |
| B14 | `local arr=("$st_js" …); for st in "${arr[@]}"; do` | `SETUP (tally loop operand not a leg status: '"${arr[@]}"')` | 0 |
| B15 | `case $st in` → `case "$st" in` | `SETUP (counting \`case $st in\` not found)` | 0 |
| B16 | loop variable renamed `st` → `status` on both header and case | `SETUP (counting \`case $st in\` not found)` | 0 |
| B17 | `local legs="$st_js …"; for st in $legs; do` | `SETUP (tally loop operand not a leg status: '$legs')` | 0 |

B13 is the round-32 class-3 failure in the opposite direction: v2 correctly tolerates an auxiliary
loop *around* the tally loop (B12 passes) and a pre-count loop *before* it (B10, before the block;
B11, inside the block) — but when the auxiliary loop wraps the counting `case` instead of the
tally loop, the "innermost loop governing the case" rule selects the wrapper and then refuses its
`"$st"` operand. B15 and B16 show the counting-case identification is still spelling-based
(`CASE_RE = case[ \t]+\$st[ \t]+in`), despite the docstring's dataflow claim. B14 and B17 show the
operand reader requires each operand token to literally be `$st_*`; a list or array carrier is
unreadable even though the loop's dataflow is unambiguous.

## Killed mutants

Operand edits (killed by `static`, static fails alone): K01 duplicate operand (citecheck→js),
K02 drop last operand, K03 drop middle operand. K04 `nlegs=8` (static and runtime and harness).
Runtime kills: K05 status 3 counted as pass, K06 fail arm also increments setup, K07 break after a
fail, K08 wildcard arm moved first, K09 guard `>` overcount-only, K10 guard `<` undercount-only,
K11 FAIL printf `failed`/`setup` fields swapped, K12 `$nfail -gt 1`, K13 `$nsetup -ge 0`,
K14 status 126 counted as pass, K15 setup arm steals a pass when a fail was seen, K16 setup
counted at most once, K17 status 3 also counted as fail, S01 fail arm breaks when a setup was
already seen. Note K15 and K16 are killed precisely because their trigger includes status 2, which
the (f,s) count vectors place next to status 1 — the same shape of defect conditioned on a status
>2 survives (S02/S03).

Benign mutants that PASS (12): B01 reverse operand order, B02 swap two operands, B03 semicolon →
newline before `do` (block body identical, header respelled), B04 extra space in the header,
B05 comment inside the loop, B06 whitespace inside the pass arm, B07 no-op `continue` after the
`case`, B08 `continue` terminating the pass arm, B09 guard condition dropping `+ nsetup`
(unreachable: the setup branch exits first, so the term is always 0 at the guard), B10 pre-count
loop before the tally block, B11 pre-count loop inside the block, B12 single-iteration wrapper
loop around the tally loop.

## Smallest safe correction (tested in my scratch only, not applied anywhere)

`check_runtime` needs the missing mixed family; adding ordered position pairs over a
representative status set closes both survivors for about 2.3k extra vectors (~3× run time:
2.0 s → 6.6 s per invocation here):

```python
    V = (0, 1, 2, 3, 4, 126, 127, 255)
    for i in range(n):
        for j in range(i + 1, n):
            for a in V:
                for b in V:
                    v = [0] * n
                    v[i], v[j] = a, b
                    vectors.append(v)
```

Measured on a scratch copy (`tool_fix.py`, tool.py + that block, everything else byte-identical):

```
base rc=0 TALLY_AUDIT: PASS   S02 rc=1 TALLY_AUDIT: FAIL (runtime=fail)
S03  rc=1 TALLY_AUDIT: FAIL (runtime=fail)   B01 rc=0 PASS   B06 rc=0 PASS
B12  rc=0 PASS   K05 rc=1 FAIL   K11 rc=1 FAIL
```

For the false rejects, the safe direction is to stop keying identification on spelling: match the
counting case as `case\s+"?\$\{?([A-Za-z_]\w*)\}?"?\s+in`, require it to govern the counter
increments, and require that subject variable to be the loop variable of the identified loop (this
alone fixes B15 and B16 without touching operand handling); then resolve a loop's operands through
one level of `local NAME=( … )` / `local NAME="…"` when every element still names a leg status
(B14, B17), and prefer the loop whose subject is the case subject over "innermost" when a
single-iteration loop sits between the tally loop and the case (B13). I did not implement or test
those three; they are the honest next step, not a measured result.

## Files (all inside `/fast/scratch/hyaku/tameshi-r33-seats/DevLoopOps/`)

`mutants.py` (generator with occurrence assertions), `mut/<ID>.sh` (37 copies), `res/<ID>.out|.err|.rc`,
`verdicts.tsv`, `eqcheck.py`, `eq1.out`, `eq2.out`, `witness_*.sh`, `witness.out`, `tool_fix.py`,
`fix.res`, `*.rc` (clone/checkout/extract/generator exit codes).
