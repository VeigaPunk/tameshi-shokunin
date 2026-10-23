# DevHarness — dev sweep of the selftest-harness region against frozen tally-audit-v2

## Verdict

No mutant escaped the audit as a whole, but the `harness` check itself is weakened by five
reproducible mutants, and one benign variant is false-rejected.

- 36 mutants, one hunk each, all inside the runner's selftest harness region
  (`mutate-and-run.sh:1992-2041`): 28 intended-defect mutants, 8 benign variants.
- Tool killed 17 of the 28 intended-defect mutants (exit 1); 11 survived (exit 0).
- Of the 11 survivors, 5 are genuine weakenings with a reproducer: **H01, H05, H06, H11, H24**.
  **H14** survives the check but is unreachable: every runner that would exercise its weakened
  count assertion is rejected first by the names-equality guard in `check_harness`
  (`tool.py:448-449`). The remaining 5 (**H17, H20, H23, H32, H33**) show no differing harness
  output across the witness corpus; H33 is strictly stricter, the other four are equivalent in the
  probed space.
- **FALSE REJECT: B02.** A runner with a second, equivalent `tblock=$(awk ... $SELF)` extraction
  line (`$SELF` unquoted rather than `"$SELF"`) is behaviourally identical but the tool reports
  `TALLY_AUDIT: FAIL`, harness faults rejected `0/29` (exit 1).
- The 7 other benign variants (B01, B03-B08) pass, including the routed case B01 (second
  extraction line, double-quoted).

Severity note (not an escape): for each of the five harness-level reproducers the tool's
`runtime` check independently rejects the same faulty tally block (measured below), so none of
these five witnesses would slip through the audit as a whole. The finding is that `CHECK harness` — the
certification of the runner's own `--selftest`, which is the gate subsequent edits rely on — no
longer distinguishes those faults.

## Method

Frozen bytes, verified at extraction (also the after-values, see Restoration):

```
$ sha256sum tool.py pristine.sh
9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

`pristine.sh` matches the frozen runner sha prefix `a7d3f2dd...2eb9`. The lane clone is detached
at `f6d8a891f1d966c5c3cdda385090da3a6e804675` and `git -C lane status --porcelain` is empty.

Mutants are exact-string replacements applied to `pristine.sh`; the generator asserts the old
string occurs exactly once and that the result differs (`mutants.py`), then writes `m_<id>.sh`.
`diff -u` confirms every mutant is one hunk (at most 5 changed lines). Each mutant was run as

```
timeout 300 python3 tool.py --runner m_<id>.sh > out/<id>.out 2> out/<id>.err; echo $? > ...
```

with the exit code captured, never `&&`. Verdicts are in `verdicts.tsv`; a 300 s job cap killed
the batch after 35 rows, so `m_H34.sh` was run alone afterwards (exit 1, same check).

Differential detector (bounded, no other runtime): `probe.py` and `probe2.py` import the frozen
`tool.py` and call its own `harness_section()` / `run_harness()` — the same functions `check_harness`
uses — once with the pristine harness section and once with the mutant's, on the same injected
tally block. A row is `(cases, failed)`; `failed == 0` means the harness accepted the block.

## Mutant table

Predicted class was written before the run; the verdict column is the measured one.

| id | designed as | edit | tool exit | harness check detail |
|---|---|---|---|---|
| H01 | survivor candidate | first-line compare `== "$want_line"` -> `== *"$want_line"*` | 0 PASS | reference cases=9; faults rejected=29/29 |
| H02 | kill expected | first-line compare truncated to `"${want_line:0:20}"` | 1 FAIL | harness rejects or cannot run the reference block ((9, 8)) |
| H03 | kill expected | exit-only compare `[[ $rc -eq $want_rc ]]` | 1 FAIL | 27/29; accepted: label printf-counts-swapped |
| H04 | kill expected | first-line-only compare (exit dropped) | 1 FAIL | 28/29; accepted: fail-exits-0 |
| H05 | survivor candidate | drops the one-setup-leg-at-each-position sweep | 0 PASS | reference cases=8; 29/29 |
| H06 | survivor candidate | drops the one-failing-leg-at-each-position sweep | 0 PASS | reference cases=8; 29/29 |
| H07 | kill expected | drops the unknown-status-3 vector | 1 FAIL | 28/29; accepted: status-3-passes |
| H08 | kill expected | drops the mixed fail+setup vector | 1 FAIL | 28/29; accepted: setup-before-fail |
| H09 | kill expected | drops the two-setup vector | 1 FAIL | 28/29; accepted: setup-needs-exactly-one |
| H10 | kill expected | drops the two-failing vector | 1 FAIL | 28/29; accepted: fail-needs-exactly-one |
| H11 | survivor candidate | drops the all-nine-pass reference case | 0 PASS | reference cases=8; 29/29 |
| H12 | kill expected | position sweep pins status at slot 0 | 1 FAIL | 14/29 |
| H13 | kill expected | position sweep accepts 8 of 9 positions | 1 FAIL | 13/29 |
| H14 | survivor candidate | leg-name count `-eq 9` -> `-ge 1` | 0 PASS | reference cases=9; 29/29 |
| H15 | kill expected | position sweep increments `tgot` unconditionally | 1 FAIL | 13/29 |
| H16 | kill expected | drops the completeness-guard undercount stress | 1 FAIL | 26/29 |
| H17 | control | guard stress gains a dead `||` fallback | 0 PASS | reference cases=9; 29/29 |
| H18 | kill expected | guard stress removed, case still counted | 1 FAIL | 26/29 |
| H19 | kill expected | guard stress case hardcoded to pass | 1 FAIL | 26/29 |
| H20 | survivor candidate | mapfile assignment pattern loses `$` anchor | 0 PASS | reference cases=9; 29/29 |
| H21 | kill expected | status-3 vector replaced by a duplicate all-pass run | 1 FAIL | 28/29; accepted: status-3-passes |
| H22 | kill expected | per-position expected rc relaxed to 0 | 1 FAIL | harness rejects the reference block ((9, 2)) |
| H23 | survivor candidate | extraction awk start anchor loosened to `^  local nlegs=` | 0 PASS | reference cases=9; 29/29 |
| H24 | survivor candidate | exit compare `-eq` -> `-ge` | 0 PASS | reference cases=9; 29/29 |
| H25 | kill expected | exit compare `-eq` -> `-le` | 1 FAIL | 28/29; accepted: fail-exits-0 |
| H32 | survivor candidate | drops the `-n "$tblock"` assertion | 0 PASS | reference cases=9; 29/29 |
| H33 | survivor candidate | `out=$(bash ... 2>&1)` -> `2>/dev/null` | 0 PASS | reference cases=9; 29/29 |
| H34 | kill expected | position loop passes `''` as the expected line | 1 FAIL | harness rejects the reference block ((9, 2)) |
| B01 | benign | second extraction line, `"$SELF"` (the routed case) | 0 PASS | reference cases=9; 29/29 |
| B02 | benign | second extraction line, `$SELF` unquoted | 1 FAIL | 0/29; all 29 faults accepted |
| B03 | benign | guard stress removes the first operand, not the last | 0 PASS | reference cases=9; 29/29 |
| B04 | benign | duplicate the mixed vector | 0 PASS | reference cases=10; 29/29 |
| B05 | benign | generated probe loses `set -u` | 0 PASS | reference cases=9; 29/29 |
| B06 | benign | first line re-extracted by an equivalent expression | 0 PASS | reference cases=9; 29/29 |
| B07 | benign | awk start anchor written `^[ \t][ \t]local` | 0 PASS | reference cases=9; 29/29 |
| B08 | benign | expected line supplied through an equivalent capture | 0 PASS | reference cases=9; 29/29 |

Counts: 18 killed by the tool (17 intended-defect, 1 false reject), 18 passed (11 intended-defect
survivors, 7 benign).

## Survivors with reproducers

Witness blocks are `REF_BLOCK` (the pinned reference, `tool.py:67-105`) with one injected change.
Rows are `(cases, failed)` from the tool's own `run_harness`; `failed == 0` is acceptance, so the
baseline row (`pristine`) must be non-zero for the block to be usable — a block the pristine
harness already accepts is not a witness (`ignore-leg-in-multi-only` was discarded for that
reason).

### H05 — the setup-status position sweep is gone

Edit at `pristine.sh:2010-2011`:

```
-  for tvec in '1:1:REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)' \
-    '2:2:REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)'; do
+  for tvec in '1:1:REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)'; do
```

Witness block: reference block plus `  if [[ $st_citecheck == 2 ]]; then st_citecheck=0; fi`
(one setup-status leg is silently counted as pass). Observed:

```
WITNESS setup-alone-citecheck      pristine=(9, 1)      # pristine harness rejects
  m_H05.sh (8, 0) -> ACCEPTS
```

Tool verdict on `m_H05.sh`: `TALLY_AUDIT: PASS`, `CHECK harness PASS reference cases=8; faults rejected=29/29`.

### H06 — the failing-status position sweep is gone

Same two lines, only the `'1:1:...'` entry kept. Witness block: reference block plus
`  if [[ $st_citecheck == 1 ]]; then st_citecheck=0; fi`. Observed:

```
WITNESS failure-alone-citecheck    pristine=(9, 1)
  m_H06.sh (8, 0) -> ACCEPTS
```

H05 and H06 are complementary: the tool's fault panel uses `ignore-alone-<leg>` faults that fire
for status 1 or 2, so dropping either sweep alone still leaves one detector; dropping the sweep
for one status leaves blocks keyed on that status unobserved.

### H01 — the first line is matched by substring

Edit at `pristine.sh:2006`:

```
-    [[ $rc -eq $want_rc && "${out%%$'\n'*}" == "$want_line" ]]
+    [[ $rc -eq $want_rc && "${out%%$'\n'*}" == *"$want_line"* ]]
```

Witness block: every printed line in the reference block prefixed with `x`. Observed:

```
WITNESS first-line-prefixed-x      pristine=(9, 8)
  m_H01.sh (9, 0) -> ACCEPTS
```

A line such as `xREGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` breaks every consumer that
anchors `^REGRESSION:`; the mutant harness accepts it.

### H11 — the all-pass path is no longer exercised

Edit at `pristine.sh:2008-2009` (the `tally_line 0 ...` call and its `st` replaced by `true`).

Witness block: the reference block's PASS printf prints `"$((npass - 1))"`. Observed:

```
WITNESS pass-count-off-by-one      pristine=(9, 1)
  m_H11.sh (8, 0) -> ACCEPTS
WITNESS pass-line-exit-2           pristine=(9, 1)
  m_H11.sh (8, 0) -> ACCEPTS
```

### H24 — the exit comparison accepts higher exit codes

Edit at `pristine.sh:2006`: `$rc -eq $want_rc` -> `$rc -ge $want_rc`.

Witness block: the reference block's final `exit 0` changed to `exit 2` (prints PASS, exits 2).
Observed:

```
WITNESS pass-line-exit-2           pristine=(9, 1)
  m_H24.sh (9, 0) -> ACCEPTS
```

`H25` is the same edit in the other direction (`-le`) and is killed, because the panel's
`fail-exits-0` fault produces a FAIL line with exit 0, which `-le` accepts.

### H14 — the leg-count assertion is vacuous but unreachable

Edit at `pristine.sh:1996`: `[[ -n "$tblock" && ${#tnames[@]} -eq 9 ]]` -> `-ge 1`.

Witness is a runner, not a block: `w_extra.sh` is the frozen runner with one extra `  st_extra=$?`
assignment before the tally block (a tenth head assignment that no tally operand covers). The
harness extracts names from `$SELF`, so the count assertion is what would see it:

```
pristine.sh    witness=w_extra.sh     cases/failed=(9, 1) rejects
m_H14.sh       witness=w_extra.sh     cases/failed=(9, 0) ACCEPTS
```

The weakened assertion is not reachable through the audit, however: `check_harness` first refuses
any runner whose leg names differ from the reference panel, and such a runner is exactly the one
the count assertion would test. Measured on the witness runner itself:

```
$ timeout 120 python3 tool.py --runner w_extra.sh; echo $?
1
CHECK head PASS legs=10
CHECK static FAIL legs=10 operands=9 nlegs=9; loop operands != legs (missing ['st_extra']; miscounted -); nlegs=9 but 10 legs assigned
CHECK runtime FAIL vectors=2662 mismatched=2662; ...
CHECK harness FAIL leg names differ from the reference panel (st_js ... st_citecheck st_extra)
TALLY_AUDIT: FAIL (head=pass static=fail runtime=fail harness=fail)
```

So H14 is a survived mutant without an observable consequence: for the only runner family where the
assertion differs (nine names), the assertion is trivially true; for any other family the names
guard rejects first. It is listed under survivors without a reproducer, not as a finding.

### Runtime coverage of the witness blocks (no escape)

Each surviving harness accepts a block that the tool's `runtime` check still rejects when the same
block is the runner's actual tally block:

```
runtime setup-alone-citecheck    FAIL vectors=2395 mismatched=10
runtime failure-alone-citecheck  FAIL vectors=2395 mismatched=14
runtime pass-line-exit-2         FAIL vectors=2395 mismatched=10
runtime first-line-prefixed-x    FAIL vectors=2395 mismatched=2395
runtime pass-count-off-by-one    FAIL vectors=2395 mismatched=10
```

## Surviving mutants without an observable difference

H14 is covered above (unreachable). The other five:

- **H17** — the added `||` fallback expects a PASS line with `passed=8`, which no block prints for
  the eight-counted block; the mutant's rows are identical to pristine on all eight witnesses.
- **H20** — the loosened mapfile pattern (`/^  st_[a-z]+=\$\?/`) only admits head lines whose name
  extraction is garbage, and such names make the later cases fail anyway; rows identical.
- **H23** — `/^  local nlegs=/` matches the same line as the pinned pattern, so extraction is
  unchanged; rows identical.
- **H32** — dropping `-n "$tblock"` changes nothing observable: a runner with an unextractable
  block (`w_noblock.sh`, block header reflowed to `local  nlegs=`) is rejected either way,
  `pristine=(9, 1)`, `m_H32=(9, 1)`.
- **H33** — `2>/dev/null` is strictly stricter. A block printing the PASS line to stderr is
  accepted by pristine (`9, 0`) and rejected by H33 (`9, 1`), because the pristine harness folds
  stderr into the captured output with `2>&1`. This matches the tool's stated stdout-only
  comparison policy; it is not a weakening. (It does show the frozen runner's own harness compares
  merged streams, unlike `check_runtime`.)

## False reject: B02

The routed round-32 item 4 says a second equivalent `tblock=$(awk ...)` extraction line must be
accepted and the reference spliced after the last one. `EXTRACT_RE` (`tool.py:404`) requires the
form `tblock=$(awk ... "$SELF")` on one line with a double-quoted `$SELF`. A second line written
with `$SELF` unquoted is equivalent shell (the path contains no spaces) but is not counted, so:

1. `harness_section` returns one extraction (the first).
2. `run_harness` splices `tblock=$AUDIT_INJECT` after that first extraction.
3. The unmatched second extraction then re-extracts the runner's own block, overwriting the
   injection.

Every injected fault is discarded, so the harness passes them all:

```
$ cat out/B02.out
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=2395 mismatched=0
CHECK harness FAIL reference cases=9; faults rejected=0/29; accepted: label fail-exits-0 ... guard-overcount-only-alt
TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)
```

B01, the same second line with `"$SELF"`, passes 29/29, so the routed fix works only for the
exactly-quoted spelling. The behaviour of the runner itself is unchanged by B02 (both extractions
read the same file), so this is a false reject of a benign copy, not a defect the audit needs to
report as FAIL.

Smallest safe correction (not applied; the tool is frozen and the fix belongs to the L1): make
`EXTRACT_RE` accept `\$SELF` quoted or bare, or reject the copy as `SETUP` when more than one
extraction is present and any of them is not matched by `EXTRACT_RE`, rather than silently
injecting into a position that a later extraction overwrites.

## Benign variants accepted

B01, B03 (first operand removed instead of last), B04 (duplicated mixed vector, reference cases 10),
B05 (`set -u` dropped from the generated probe), B06 (equivalent first-line capture), B07 (anchor
written with character classes), B08 (expected line through an equivalent capture) all pass with
29/29 faults rejected.

## Restoration and hash evidence

`pristine.sh` and `tool.py` were never edited: every mutant is a separate copy in the scratch
directory, and the witness runners are copies too. Before and after values are identical:

```
$ sha256sum tool.py pristine.sh
9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

Witness runner hashes: `w_extra.sh 63b7b240...a46`, `w_noblock.sh 40d4244b...bfc`.
The lane clone is detached at the freeze commit and `git status --porcelain` is empty; no git
write command, no `jj` command, and no counter run was made in the lane.

Scratch: `/fast/scratch/hyaku/tameshi-r33-seats/DevHarness/` — `mutants.py`, `mutants.json`,
`m_*.sh`, `w_*.sh`, `tool.py`, `pristine.sh`, `out/`, `verdicts.tsv`, `table.md`, `probe*.py`,
`probe_*.out`, `baseline.out`, `hashes_after.txt`.

No tool was installed or upgraded. All runs were bounded by `timeout`; the only long job was the
36-mutant batch, which hit its 300 s cap after 35 rows, and its last mutant was run separately.
No process started here is left running.
