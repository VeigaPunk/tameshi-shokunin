# DevPrintf — round-33 wave-1 dev sweep, printf REGRESSION family

Seat: `tameshi-r33-w1-DevPrintf-3`. Scratch: `/fast/scratch/hyaku/tameshi-r33-seats/DevPrintf/`.
Object under test: `tools/tally-audit-v2.py` at freeze `f6d8a891f1d966c5c3cdda385090da3a6e804675`
(sha256 `9dbbce62…33a4`, matching `contract.json:frozen_artifacts.tool_sha256`), against runner
copies of `tools/mutate-and-run.sh` (sha256 `a7d3f2dd…2eb9`, never edited).

## Verdict

**7 of 31 single-edit mutants in the printf REGRESSION family are SURVIVORS**: the frozen v2 audit
prints `TALLY_AUDIT: PASS` and exits 0 while the runner's stdout changes. The tool kills 19; the
other 5 passes are provably behaviourally equivalent and were verified so over 2414 vectors in two
flag contexts (exit and full stdout identical).

Root cause, one sentence: the runtime oracle compares **only the first line** of the tally block's
stdout (`tool.py:45`, capture at `tool.py:227`, expected value from `tool.py:236-248`), so every
`REGRESSION_WORKDIR` line and any extra or duplicated `REGRESSION*` line after the first is
invisible; and it pins the **selftest flag context** `auto=0 KEEP=1`, so the production PASS
disclosure branch (`auto=1 KEEP=0`, which is what `--regression` without `--workdir` sets) is never
executed at all.

The single most consequential survivor is **W2**: on the FAIL path the mutant prints
`REGRESSION_WORKDIR: (kept)`, dropping the only machine-readable pointer to the kept scratch root —
the directory holding the evidence log. The audit still passes it.

## Environment and evidence discipline

Every cited command captured its exit code in a sibling file.

```
mkdir -p /fast/scratch/hyaku/tameshi-r33-seats/DevPrintf && df -h /fast
git clone -q --no-hardlinks …/tameshi-shokunin …/DevPrintf/lane ; echo $? > clone.rc      # 0
git -C …/lane checkout -q --detach f6d8a89… ;            echo $? > co.rc                   # 0
git -C …/lane show f6d8a89…:tools/tally-audit-v2.py > tool.py ;  echo $? > tool.rc          # 0
git -C …/lane show f6d8a89…:tools/mutate-and-run.sh > pristine.sh ; echo $? > pr.rc         # 0
sha256sum pristine.sh tool.py
  a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
  9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tool.py
```

`pristine.sh` hash equals the contract's runner pin `a7d3f2dd…2eb9`; `tool.py` equals the tool pin.
No tool installation or upgrade was needed (python3 and bash only; nothing added to the host).

Baseline before any mutant (a control, not a substitute for the data seat):

```
python3 tool.py --runner pristine.sh ; echo $? > out/pristine.rc      # 0
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=2395 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=29/29
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Mutant generation (`gen_mutants.py`) applies each edit by exact string replacement, asserting the
old string's occurrence count first and discarding no-ops. Every mutant is one logical edit;
`m/<id>.sh` differs from `pristine.sh` only in the lines shown below (`diff -u` was reviewed for
each).

```
python3 gen_mutants.py ; echo $? > gen.rc         # 0, 28 definitions applied
# W7 needed 5 occurrences, not 4 (the removed-path line also carries the label); generated separately
ls m/*.sh | wc -l                                 # 31 (29 generation + X1 + X2)
```

Per-mutant audit, frozen tool:

```
timeout 300 python3 tool.py --runner m/<id>.sh > out/<id>.txt ; echo $? > out/<id>.rc
```

## Roster of 31 mutants and frozen-tool verdicts

`rc=1` is the tool's FAIL (mutant killed); `rc=0` is `TALLY_AUDIT: PASS`.

| id | edit (exact) | frozen rc | class |
|---|---|---|---|
| F1 | FAIL line args: `"$npass" "$nfail"` → `"$nfail" "$npass"` | 1 | killed (runtime) |
| F2 | FAIL line args: `"$nfail" "$nsetup"` → `"$nsetup" "$nfail"` | 1 | killed |
| F3 | FAIL `failed=%s` → `failed=%d` | 0 | equivalent |
| F4 | FAIL `setup=%s` field + arg dropped | 1 | killed |
| F5 | FAIL relabel `failed=` → `failing=` | 1 | killed |
| F6 | FAIL relabel `passed=` → `passing=` | 1 | killed |
| F7 | FAIL extra ` nlegs=%s` field + arg | 1 | killed |
| F8 | FAIL relabel `cases=` → `legs=` | 1 | killed |
| F9 | FAIL cases arg `$nlegs` → `$((npass + nfail + nsetup))` | 0 | equivalent |
| F10 | FAIL format order `passed/failed` swapped | 1 | killed |
| S1 | SETUP relabel `cannot-verify=` → `cannot_verify=` | 1 | killed |
| S2 | SETUP `cases` field + arg dropped | 1 | killed |
| S3 | SETUP cannot-verify arg `$nsetup` → `$nfail` | 1 | killed |
| S4 | SETUP cases arg `$nlegs` → `$npass` | 1 | killed |
| M1 | mismatch `counted=%s` → `counted=%d` | 0 | equivalent |
| M2 | mismatch `case-tally` → `case tally` | 1 | killed (stress only) |
| M3 | mismatch counted arg → `$npass` | 0 | equivalent |
| M4 | mismatch relabel `cases=` → `legs=` | 1 | killed (stress only) |
| P1 | PASS suffix `; ledger legs exact: …` dropped | 1 | killed |
| P2 | PASS `ledger legs exact` → `ledger-legs exact` | 1 | killed |
| P3 | PASS passed arg `$npass` → `$nlegs` | 0 | equivalent |
| P4 | PASS format `passed/cases` order swapped | 1 | killed |
| W1 | all four `(kept)` → `(kept, inspect)` | 0 | **SURVIVOR** |
| W2 | FAIL-path WORKDIR `%s` arg dropped | 0 | **SURVIVOR** |
| W3 | removed-path `(removed on PASS; --keep retains)` → `(removed on PASS)` | 0 | **SURVIVOR** |
| W4 | final-else WORKDIR suffix ` (kept)` dropped | 0 | **SURVIVOR** |
| W5 | PASS path: WORKDIR printf moved before the PASS printf | 1 | killed |
| W6 | FAIL path: extra line printed before the FAIL line | 1 | killed |
| W7 | label `REGRESSION_WORKDIR:` → `REGRESSION_WORKDIR :` (all 5) | 0 | **SURVIVOR** |
| X1 | PASS printf duplicated (second identical PASS line) | 0 | **SURVIVOR** |
| X2 | FAIL path: extra `REGRESSION_NOTE:` line after the FAIL line | 0 | **SURVIVOR** |

Tool verdict files: `out/<id>.rc` and `out/<id>.txt` per id; summary lines are in the report text
below where relevant.

## Survivors — exact edits, witnesses, both outputs

Witnesses come from an independent oracle (`difftest.py`): it extracts pristine and mutant tally
blocks the same way the tool does, runs both in bash over **2414 vectors** (every status 0..255 at
every one of the nine positions, every (failing, setup) count pair 0..9, each pair also reversed)
under **two flag contexts** `auto=0 KEEP=1` and `auto=1 KEEP=0`, and compares **exit code and the
whole stdout** (newlines shown as `|`). Raw results: `out/diff2.txt`, `out/diff3.txt`.

### W1 — `(kept)` → `(kept, inspect)` on all four disclosure lines

```
-    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"        (×4: FAIL, SETUP, mismatch, final else)
+    printf 'REGRESSION_WORKDIR: %s (kept, inspect)\n' "$root"
```

Witness vector `0 0 0 0 0 0 0 0 0`:

```
pristine exit=0 REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)|REGRESSION_WORKDIR: …/root (kept)
mutant   exit=0 REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)|REGRESSION_WORKDIR: …/root (kept, inspect)
```

Frozen tool: `CHECK runtime PASS vectors=2395 mismatched=0`, `TALLY_AUDIT: PASS`, exit 0.

### W2 — FAIL path loses the scratch-root pointer (highest consequence)

```
-    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
+    printf 'REGRESSION_WORKDIR: (kept)\n'                 (FAIL path only, followed by `exit 1`)
```

Witness vector `1 0 0 0 0 0 0 0 0`:

```
pristine exit=1 REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)|REGRESSION_WORKDIR: …/root (kept)
mutant   exit=1 REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)|REGRESSION_WORKDIR: (kept)
```

The FAIL line is byte-identical, so every first-line consumer and the frozen audit agree; the
operator loses the only reference to the kept work directory, which is where `sweep.log`,
`results.tsv` and the defect specs live. Frozen tool: PASS, exit 0.

### W3 — production PASS disclosure branch reworded

```
-    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\n' "$root"
+    printf 'REGRESSION_WORKDIR: %s (removed on PASS)\n' "$root"
```

Witness vector `0 0 0 0 0 0 0 0 0` with `auto=1 KEEP=0` (the production `--regression` context:
`pristine.sh:1357-1362` sets `auto=1` when the root came from `mktemp`; `pristine.sh:190` sets
`KEEP=0` by default):

```
pristine exit=0 …PASS…|REGRESSION_WORKDIR: …/root (removed on PASS; --keep retains)
mutant   exit=0 …PASS…|REGRESSION_WORKDIR: …/root (removed on PASS)
```

Note this mutant is **equivalent** in the tool's own context (`auto=0`, `KEEP=1`) — the audit's
driver pins `auto=0 KEEP=1`, the runner's selftest context (`pristine.sh:2003`), so the branch is
never taken. Frozen tool: PASS, exit 0.

### W4 — final-else disclosure suffix dropped

```
-    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"        (the last, pre-`exit 0` occurrence)
+    printf 'REGRESSION_WORKDIR: %s\n' "$root"
```

Witness vector `0 0 0 0 0 0 0 0 0`, `auto=0 KEEP=1`:

```
pristine exit=0 …PASS…|REGRESSION_WORKDIR: …/root (kept)
mutant   exit=0 …PASS…|REGRESSION_WORKDIR: …/root
```

(With `auto=1 KEEP=0` the two are identical — that branch takes the removed line — so the hole is
context-specific and only a second context exposes it.) Frozen tool: PASS, exit 0.

### W7 — label colon reworded on every WORKDIR line

```
-printf 'REGRESSION_WORKDIR: %s …      →  +printf 'REGRESSION_WORKDIR : %s …       (5 occurrences)
```

Witness vector `0 0 0 0 0 0 0 0 0`:

```
pristine exit=0 …|REGRESSION_WORKDIR: …/root (kept)
mutant   exit=0 …|REGRESSION_WORKDIR : …/root (kept)
```

Any consumer keying on the `REGRESSION_WORKDIR:` prefix stops matching. Frozen tool: PASS, exit 0.

### X1 — the PASS line printed twice

```
  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
    "$nlegs" "$npass"
+ (the same two lines appended immediately after)
```

Witness vector `0 0 0 0 0 0 0 0 0`:

```
pristine exit=0 PASS|REGRESSION_WORKDIR: …/root (kept)
mutant   exit=0 PASS|PASS|REGRESSION_WORKDIR: …/root (kept)
```

A ledger parser that sums `REGRESSION: PASS` occurrences or counts reporting lines double-counts.
Frozen tool: PASS, exit 0.

### X2 — an extra stdout line inside the FAIL disclosure

```
+    printf 'REGRESSION_NOTE: setup=%s legs=%s\n' "$nsetup" "$nlegs"
```

Witness vector `1 0 0 0 0 0 0 0 0`:

```
pristine exit=1 FAIL|REGRESSION_WORKDIR: …/root (kept)
mutant   exit=1 FAIL|REGRESSION_NOTE: setup=0 legs=9|REGRESSION_WORKDIR: …/root (kept)
```

Frozen tool: PASS, exit 0.

## The five passes that are genuinely equivalent (not coverage holes)

Each was swept over all 2414 vectors in both flag contexts with full stdout and exit compared:
`EQUIV F3`, `EQUIV F9`, `EQUIV M1`, `EQUIV M3`, `EQUIV P3` (`out/diff2.txt`). Structural reasons:

* **F3** `%d` for a decimal string: bash `printf '%d' 1` prints `1`, byte-identical.
* **F9** FAIL `cases=` printed as `$((npass + nfail + nsetup))`: the FAIL line is reachable only
  after the tally loop counted every leg, so the sum is always `nlegs` there.
* **M1** `%d` on an integer sum: identical bytes.
* **M3** mismatch `counted=` printed as `$npass`: the mismatch guard is reachable only with
  `nfail == 0` and `nsetup == 0` (the earlier guards return first), hence `counted == npass`.
* **P3** PASS `passed=` printed as `$nlegs`: the PASS line is reachable only when all counted
  statuses are 0 and the sum guard held, hence `npass == nlegs`.

These are the useful "accept" half of the sweep: a correction must keep accepting them.

## Why the harness check cannot compensate

The `harness` check runs the runner's own tally selftest, which compares only the first line:
`pristine.sh:2006` (`tally_line … "${out%%$'\n'*}" == "$want_line"`). The fault panel
(`tool.py:360-399`) is built from `REF_BLOCK` and contains 29 faults, **none of which touches a
`REGRESSION_WORKDIR` line** — the only place a WORKDIR line appears is inside the `guard` string
(`tool.py:384`) used to delete the completeness guard. Injecting a WORKDIR fault would be
pointless, because the runner's harness (first-line comparison) accepts it, which would turn into a
false rejection of the pristine runner. So the disclosure lines are unverified by construction in
both the audit and the runner's selftest.

## Smallest safe correction (verified in scratch, not applied to production)

Two lines of change in `check_runtime`; `head`, `static` and `harness` untouched.

1. **Compare the whole stdout.** `run_vectors` captured `${out%%$'\n'*}`; capture all lines with
   newlines normalised (`nl=$'\n'; bar='|'`; `${out//$nl/$bar}`), and let `oracle()` return the
   full expected text: first line plus `|REGRESSION_WORKDIR: tally-audit (kept)` for
   FAIL/SETUP/mismatch and the flag-appropriate disclosure for PASS.
2. **Run the sweep in both flag contexts.** The driver pinned `auto=0 KEEP=1`; add a second pass
   with `auto=1 KEEP=0` whose PASS expectation is
   `|REGRESSION_WORKDIR: tally-audit (removed on PASS; --keep retains)`. Without this, W3 survives
   even the full-stdout fix (observed: `out/p/W3.rc` = 0).

Scratch implementations: `tool_patched.py` (step 1 only) and `tool_patched2.py` (both steps),
produced by `patch_tool.py` / `patch_tool2.py` from the frozen bytes.

Observed result of `tool_patched2.py` (`out/q/<id>.rc`, `out/q/<id>.txt`):

```
pristine  rc=0  TALLY_AUDIT: PASS
F3 F9 M1 M3 P3   rc=0   (all five provable equivalents still accepted — no false reject)
F1 F2 F4 F5 F6 F7 F8 F10 S1 S2 S3 S4 M2 M4 P1 P2 P4 W5 W6   rc=1   (all previous kills kept)
W1 W2 W3 W4 W7 X1 X2   rc=1   (all seven survivors now killed)
```

Representative post-fix detail lines:

```
W2: got (1, '…FAIL…|REGRESSION_WORKDIR: (kept)')  want (1, '…FAIL…|REGRESSION_WORKDIR: tally-audit (kept)')
W3: statuses 0…0 auto=1 KEEP=0: got (0, '…PASS…(removed on PASS)') want (0, '…PASS…(removed on PASS; --keep retains)')
X1: got (0, '…PASS…|REGRESSION: PASS (cases=9 passed=9; …)|REGRESSION_WORKDIR: tally-audit (kept)')
```

Inter-step evidence that step 1 alone is insufficient: with `tool_patched.py`, W1/W2/W4/W7/X1/X2
flip to killed but **W3 still exits 0** (`out/p/W3.rc` = 0), because the flag context keeps the
branch unreachable.

Cost: the runtime sweep doubles (about 2.4 s to 3.2 s on pristine here; `vectors=2395` reported as
before because the counter is per-context). Residual false-reject risk: a runner copy that
deliberately rewords `REGRESSION_WORKDIR` would now be rejected. That is intended: the runner's own
header registers the line (`pristine.sh:136-142`, `/ REGRESSION_WORKDIR / …`), so its wording is
part of the declared output surface, and the round-32 closure's false-reject classes were about
*auxiliary loop structure* (`HeldOutLoop-3`, `HeldOutRefactor-a4`), not about declared output
lines. If the data seat prefers a looser rule, the minimal looser version is to require the line to
exist and contain the root path, not to fix its suffix — but that leaves W1, W3, W4 and W7 alive.

## Restoration and containment evidence

* No production file was written. Mutants live only in `m/`; patched tools only in the scratch dir.
* `pristine.sh`, `tool.py`, `lane/tools/mutate-and-run.sh`, `lane/tools/tally-audit-v2.py` hashed
  before and after the sweep — identical (`out/hashes.before`, `out/hashes.after`, `diff` empty,
  `echo $?` = 0):

```
a7d3f2dd…2eb9  pristine.sh          a7d3f2dd…2eb9  lane/tools/mutate-and-run.sh   (before and after)
9dbbce62…33a4  tool.py             9dbbce62…33a4  lane/tools/tally-audit-v2.py    (before and after)
```

* `git -C lane status --porcelain` printed nothing (`out/lane.status.rc` = 0): the lane clone is
  still at the freeze with no working-tree drift. No `git` write command and no `jj` command was
  run anywhere; no network access was needed.

## Scan log (kept in scratch, not committed)

```
gen_mutants.py        mutant generator (exact-string edits with occurrence assertions)
mutants.json          id → description → edit strings
m/<id>.sh             31 mutant runner copies
out/<id>.txt|.rc      frozen-tool audit per mutant (31 + pristine)
out/p/<id>.txt|.rc    tool_patched.py audit (step-1 correction)
out/q/<id>.txt|.rc    tool_patched2.py audit (full correction, pristine + 31)
difftest.py           independent full-stdout/exit oracle, 2414 vectors × 2 flag contexts
diff.json, out/diff*.txt   witness vectors and both outputs
```
