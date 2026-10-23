# RerunV3Witness — independent re-measure of the public part of C1 on the frozen fix

## Verdict

The public part of C1 re-measures identically to both prior attempts. All nine
public axes (a)–(i) agree with attempt 1 (v3) and attempt 2 (v4), on the same
frozen fix bytes, at a third independent rev.

- Rerun (v3, my rev `cfcc11ff`): `pristine_selftest=1 harness=19/19 refused_drops=9/9
  killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8
  insert_equiv=4/4`, `PREDICATE: C1_R30_PASS=true`, exit `0`.
- Attempt 1 `witness/c1v3-at-witness-1fed832d.stdout`: identical counts, `true`, exit `0`.
- Attempt 2 `v4/witness.stdout`: identical counts for (a)–(i) plus the v4-only sealed
  axes `sealed_block_match=1 sealed_killed=6/6 sealed_equiv=6/6`, `true`, exit `0`.

The rows that differ are named in "Differing rows" below: the seed-dependent
inserted-term rows (h)/(i) carry different labels and different bytes per rev, and
the 12 `S-` rows exist only under v4. No row's verdict class differs.

**Smallest safe correction.** None is needed for the public axes: the rerun
reproduces both prior receipts. Two facts must travel with the receipt, though,
because they are properties of the counter rather than of the fix:

1. The (f)/(g)/(h)/(i) rows are seeded by `int(REV, 16)`, so **each rev measures a
   different set of mutant instances**. The counts agree; the instances do not. A
   receipt for rev X says nothing about the specific mutants of rev Y, so the
   per-rev receipt must name its rev (the receipts do).
2. The **H-row names are seed-independent but the H-row bytes are not**
   (`heldout()` names rows by class, `H01-drop` … `H12-drop`, but the spelling,
   the shuffled operand order and the respelled arms come from the seeded RNG).
   `H01-drop` at rev A and `H01-drop` at rev B are different byte strings that
   happen to share a label. A receipt that reports only row names would overstate
   what was measured.

## What was measured

Frozen fix: `.ufo/evidence/round-30/witness/fix.diff` (the runner the round will
land). Base: lane commit `f09d3425258403a51422c9959e25340807982947` (attempt-2
base; `refs/heads/master`).

The fix applies to that base as a clean patch, and the post-image blob is exactly
the blob named in the diff header, so the bytes under test are the frozen bytes and
not a re-derivation of them:

```
$ git rev-parse f09d342...:tools/mutate-and-run.sh     # base
c9e255e823e5827e037876ecfd797a268a2f449a
$ grep '^index' .ufo/evidence/round-30/witness/fix.diff
index c9e255e..f0f0abc 100755
$ git rev-parse cfcc11f...:tools/mutate-and-run.sh     # after apply
f0f0abc5e260c9ca80ac132c3be27a22f69e76af
```

The base blob `c9e255e` is also the runner blob at `8a8d2540` (the fix's stated
base) and at `9ed6db84` (attempt-1's base), so all three attempts started from
byte-identical runner sources.

Tally-block identity check (the frozen fix's stated `tally block sha256`, and the
`sealed_block_sha256` in `contract-amendment-3.json`):

```
sha256(tally block at my commit) = e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d
                                   == e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d (expected)
```

Block extent: from `  local nlegs=9 npass=0 nfail=0 nsetup=0 st` to the closing
`}` of `run_regression`, 1562 bytes. It contains the r30 completeness guard
`if (( npass + nfail + nsetup != nlegs )); then` → `REGRESSION: SETUP
(case-tally mismatch: ...)` → exit 2.

## Evidence

### Isolation

All code ran inside the seat's own clone, with `GIT_DIR`, `GIT_WORK_TREE` and
`GIT_INDEX_FILE` unset. No git write command was run in
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` or `/home/vgpnk/Projects/shokunin`;
the only commits were in the seat clone.

```
S=/fast/scratch/hyaku/tameshi-r30a2-seats/RerunV3Witness-7
mkdir -p $S
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $S/clone checkout -q --detach \
    f09d3425258403a51422c9959e25340807982947
```

Clone and checkout exited 0 with no output; HEAD was `f09d342`.

### Patch application and commit

```
$ cd $S/clone
$ git apply --check /home/.../witness/fix.diff   -> APPLY_CHECK_OK
$ git apply       /home/.../witness/fix.diff      -> APPLIED
$ git status --porcelain                          ->  M tools/mutate-and-run.sh
$ git commit -am 'r30 frozen fix (C1 witness rerun seat)'
cfcc11ff6d1b0f19e547070fd9cc36b159ac4cf0
```

`git show --stat` on that commit: `tools/mutate-and-run.sh | 43 ++++++…`, one file
changed, 43 insertions. The counter archives `tools` from the rev under test, so
the commit is the unit of measurement.

### The measured run (assigned command)

```
$ cd $S/clone
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout -k 5 1500 python3 \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py \
    --repo $S/clone --rev cfcc11ff6d1b0f19e547070fd9cc36b159ac4cf0 --jobs 4
```

Full stdout (48 lines; stderr was empty, 0 bytes):

```
C1_R30_ROW: pristine selftest_exit=0 verdict_pass=1
C1_R30_ROW: D1-drop-st_js selftest_exit=1 verdict_pass=0
C1_R30_ROW: D2-drop-st_kagi selftest_exit=1 verdict_pass=0
C1_R30_ROW: D3-drop-st_tsu selftest_exit=1 verdict_pass=0
C1_R30_ROW: D4-drop-st_mado selftest_exit=1 verdict_pass=0
C1_R30_ROW: D5-drop-st_checklist selftest_exit=1 verdict_pass=0
C1_R30_ROW: D6-drop-st_claims selftest_exit=1 verdict_pass=0
C1_R30_ROW: D7-drop-st_roundgate selftest_exit=1 verdict_pass=0
C1_R30_ROW: D8-drop-st_sourcescheck selftest_exit=1 verdict_pass=0
C1_R30_ROW: D9-drop-st_citecheck selftest_exit=1 verdict_pass=0
C1_R30_ROW: A1-pass-arm-noop selftest_exit=1 verdict_pass=0
C1_R30_ROW: A2-fail-arm-as-pass selftest_exit=1 verdict_pass=0
C1_R30_ROW: A3-fail-threshold selftest_exit=1 verdict_pass=0
C1_R30_ROW: A4-setup-arm-as-pass selftest_exit=1 verdict_pass=0
C1_R30_ROW: E1-reorder-operands selftest_exit=0 verdict_pass=1
C1_R30_ROW: E2-arith-commuted selftest_exit=0 verdict_pass=1
C1_R30_ROW: E3-comment-in-block selftest_exit=0 verdict_pass=1
C1_R30_ROW: E4-noop-before-pass selftest_exit=0 verdict_pass=1
C1_R30_ROW: H01-drop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H02-drop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H03-drop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H04-drop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H05-arm-noop selftest_exit=1 verdict_pass=0
C1_R30_ROW: H06-arm-double selftest_exit=1 verdict_pass=0
C1_R30_ROW: H07-fail-as-pass selftest_exit=1 verdict_pass=0
C1_R30_ROW: H08-setup-as-pass selftest_exit=1 verdict_pass=0
C1_R30_ROW: H09-fail-as-setup selftest_exit=1 verdict_pass=0
C1_R30_ROW: H10-fail-thresh selftest_exit=1 verdict_pass=0
C1_R30_ROW: H11-setup-thresh selftest_exit=1 verdict_pass=0
C1_R30_ROW: H12-drop selftest_exit=1 verdict_pass=0
C1_R30_ROW: HE1-equiv selftest_exit=0 verdict_pass=1
C1_R30_ROW: HE2-equiv selftest_exit=0 verdict_pass=1
C1_R30_ROW: HE3-equiv selftest_exit=0 verdict_pass=1
C1_R30_ROW: HE4-equiv selftest_exit=0 verdict_pass=1
C1_R30_ROW: I01-nsetup+1 selftest_exit=1 verdict_pass=0
C1_R30_ROW: I02-nfail-1 selftest_exit=1 verdict_pass=0
C1_R30_ROW: I03-nfail-1 selftest_exit=1 verdict_pass=0
C1_R30_ROW: I04-npass-1 selftest_exit=1 verdict_pass=0
C1_R30_ROW: I05-nsetup-1 selftest_exit=1 verdict_pass=0
C1_R30_ROW: I06-nfail-1 selftest_exit=1 verdict_pass=0
C1_R30_ROW: I07-nsetup+2 selftest_exit=1 verdict_pass=0
C1_R30_ROW: I08-nfail-1 selftest_exit=1 verdict_pass=0
C1_R30_ROW: IE1-nfail+0 selftest_exit=0 verdict_pass=1
C1_R30_ROW: IE2-npass+0 selftest_exit=0 verdict_pass=1
C1_R30_ROW: IE3-nsetup+0 selftest_exit=0 verdict_pass=1
C1_R30_ROW: IE4-nsetup+0 selftest_exit=0 verdict_pass=1
C1_R30: rev=cfcc11ff6d1b0f19e547070fd9cc36b159ac4cf0 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=true
```

Exit status: `0` (recorded in `$S/exit.txt`). Wall time ≈ 150 s.

### Axis-by-axis agreement

| Axis | Contract clause | Rerun `cfcc11f` | Attempt 1 `1fed832d` (v3) | Attempt 2 `7165f904` (v4) | Agree |
|---|---|---|---|---|---|
| (a) pristine `--selftest` | exit 0 + `VERDICT: PASS` | `pristine_selftest=1` | `pristine_selftest=1` | `pristine_selftest=1` | yes |
| (b) harness vectors | 19/19 | 19/19 | 19/19 | 19/19 | yes |
| (c) drop mutants refused at run time | 9/9 | 9/9 | 9/9 | 9/9 | yes |
| (d) family mutants killed by `--selftest` | 13/13 | 13/13 | 13/13 | 13/13 | yes |
| (e) frozen equivalent rewrites pass | 4/4 | 4/4 | 4/4 | 4/4 | yes |
| (f) held-out mutants killed | 12/12 | 12/12 | 12/12 | 12/12 | yes |
| (g) held-out equivalent rewrites pass | 4/4 | 4/4 | 4/4 | 4/4 | yes |
| (h) inserted-term mutants killed | 8/8 | 8/8 | 8/8 | 8/8 | yes |
| (i) inserted-term equivalent rewrites pass | 4/4 | 4/4 | 4/4 | 4/4 | yes |
| (j) sealed block match (v4 only) | 1 | n/a (v3) | n/a | 1 | n/a |
| (k) sealed killed / equiv (v4 only) | 6/6, 6/6 | n/a (v3) | n/a | 6/6, 6/6 | n/a |

Per-row verdict class (`selftest_exit`, `verdict_pass`) for every row name common
to my run and a prior receipt: **0 differences** in both comparisons (37 common
rows vs attempt 1; 35 common rows vs attempt 2, all matching).

### Differing rows

Row-name sets (my run vs each prior receipt):

- vs attempt 1 (v3): the differing names are exactly the seeded inserted-term rows
  `I01-npass+1`, `I02-npass+2`, `I03-nsetup+2`, `I04-nfail-1`, `I05-npass-1`,
  `I06-nfail+1`, `I07-npass-1`, `I08-npass+1` and `IE3-nfail+0` (attempt 1) versus
  my `I01-nsetup+1`, `I02-nfail-1`, `I03-nfail-1`, `I04-npass-1`, `I05-nsetup-1`,
  `I06-nfail-1`, `I07-nsetup+2`, `I08-nfail-1` and `IE3-nsetup+0` (mine). Same
  rows, different labels: the label carries the counter variable and the offset
  the seeded generator chose. All eight are killed (`exit=1, pass=0`) on both sides;
  all four IE rows pass (`exit=0, pass=1`) on both sides.
- vs attempt 2 (v4): the same eight `I` rows and `IE2`/`IE3`/`IE4` differ in
  label, with the same verdict class on both sides; plus 12 rows present only
  under v4: `S-m-fail-exit0`, `S-m-pattern-01`, `S-m-pattern-12`,
  `S-m-pass-prints-nfail`, `S-m-swallow-fail`, `S-m-setup-exit1` (all
  `exit=1, pass=0`, i.e. all killed) and `S-e-preinc`, `S-e-strne`,
  `S-e-arith-truth`, `S-e-guard-diff`, `S-e-minus-neg`, `S-e-pattern-alt` (all
  `exit=0, pass=1`, i.e. all pass).
- The `D*`, `A*`, `E*` and `H*`/`HE*` row names are identical across all three
  receipts and their verdict classes are identical.

Why the seeded rows differ, measured rather than asserted: `heldout()` and
`inserted()` take `int(REV, 16)` (and `+1`) as the RNG seed, so the drawn mutant
bytes are a function of the rev. Re-running the generators locally on the same
runner text with the three revs gives three different instance sets:

```
rev 1fed832d (attempt 1)  seed=182275417725021538647636223621102953438824340353  heldout_set_sha=899ab8ba42e06130  inserted_set_sha=2e738ac1cc21c203
rev 7165f904 (attempt 2)  seed=647390024847713967745294099577892638406931073434  heldout_set_sha=7355b9b96e9f4107  inserted_set_sha=4a6f57cbbb5ec1e5
rev cfcc11ff (mine)       seed=1186312009406925783244177567454009948386458619120  heldout_set_sha=7a107a6bfad33d08  inserted_set_sha=7e5f239342934fc9
rev b85716a8 (mine, seed 2) seed=1052396440466124869887120205180638010056917696694 heldout_set_sha=d5fb9c4db552de3f  inserted_set_sha=dfdd7dbf6301c447
```

### Determinism and seed-robustness

1. **Repeat at the same rev.** Re-running the assigned command at the same rev
   `cfcc11ff` produced a byte-identical stdout (`diff` empty,
   `DETERMINISTIC_IDENTICAL`). No flakiness in the (a)–(i) verdicts.
2. **Different rev, same tree.** I amended the seat commit to a new hash
   `b85716a8` (same tree `157a91cb…`, so the same runner bytes, different rev and
   therefore a different seed) and re-ran the counter. All nine public axes held
   at the same values, `PREDICATE: C1_R30_PASS=true`, exit 0 — with a visibly
   different set of inserted-term mutants (`I01-nsetup+1, I02-npass-1,
   I03-nsetup-1, I04-nfail-1, I05-nsetup+2, I06-npass+1, …`). The public axis
   counts are seed-invariant across four revs; the specific instances are not.

### Discrimination: the counter fails on the unfixed base

Run at the base rev `f09d342` (same counter, same jobs, no fix applied):

```
$ timeout -k 5 1500 python3 .../c1-measure-v3.py --repo $S/clone --rev f09d3425258403a51422c9959e25340807982947 --jobs 4
C1_R30: rev=f09d3425258403a51422c9959e25340807982947 pristine_selftest=1 harness=19/19 refused_drops=0/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4 insert_killed=0/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=false
```

Exit status `1`. This matches the committed base receipt
`.ufo/evidence/round-30/c1v3-at-base.stdout` (rev `9ed6db84`, same counts,
`false`, exit 1) and the v4 base receipt `.ufo/evidence/round-30/v4/base.stdout`.
So the counter separates the fix from its base; the `true` above is caused by the
fix, not by the counter being permissive.

### The fix's own selftest, observed directly

Axis (a) and the runner's self-report, run by hand in the seat clone:

```
$ bash tools/mutate-and-run.sh --selftest
...
PASS tally harness: block extracted, leg status names=9 (want 9)
PASS tally harness: all nine legs pass -> PASS passed=9, exit 0
PASS tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (9/9)
PASS tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (9/9)
...
MUTATE_SELFTEST: 101/101 pass
VERDICT: PASS
```

Exit 0. The base runner reports `MUTATE_SELFTEST: 97/97 pass` — the fix adds four
selftest cases (block extraction, all-pass, and the two per-position status
sweeps), which is where the runner's own detection of the routed leg-sum defect
now lives.

### v4 sandbox spot check

v4 runs every `--selftest` inside a bubblewrap sandbox (`BWRAP` in
`.ufo/evidence/round-30/c1-measure-v4.py:321-326`). I confirmed that sandbox
works in this environment by running the frozen v4 argv by hand against the
fixed runner:

```
$ bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr \
    --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 \
    --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp \
    --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp \
    --bind $S/bw /w --chdir /w bash tools/mutate-and-run.sh --selftest
MUTATE_SELFTEST: 101/101 pass
VERDICT: PASS
```

Exit 0. Bubblewrap version present: `bubblewrap 0.13.1`.

## Comparability limits (stated, not worked around)

1. **My rerun is v3, the public counter.** The assigned command is
   `c1-measure-v3.py`. v4's axes (j) and (k) and its sandboxed selftest runs are
   therefore not exercised by my measurement; attempt 2's `v4/witness.stdout` is
   the receipt for those. The (a)–(i) clause set is identical in both counter
   versions (v4 = v3 plus (j)/(k) plus sandboxing; the only other v4 delta is the
   sandbox and the `--sealed` argument).
2. **I could not re-run v4 end to end.** v4 requires `--sealed SEALED_JSON`, and
   only the sealed file's sha256 (`44116804c5cf990a5dec58d107a8a584b333e3dc89a8962a3d17761e11243729`)
   is committed; the file itself is at
   `.ufo/evidence/round-30/v4/c1-sealed.json` per `contract-amendment-3.json` and
   is not in the lane repo (a bounded search for `c1-sealed*` outside
   `/fast/scratch/hyaku/tameshi-r30a2` found nothing). The sealed set lives under
   `/fast/scratch/hyaku/tameshi-r30a2`, which is out of bounds for this seat, so
   (j)/(k) rest on attempt 2's receipt alone.
3. **The two prior witness revs are not in the lane repo.** `1fed832d…` and
   `7165f904…` are absent from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
   (`git cat-file -t` → `bad object`); they were witness-sandbox commits. Their
   receipts are therefore comparable only through their stdout files, not
   re-derivable. What *is* re-derivable and I did re-derive it: the base runner
   blob is byte-identical across `9ed6db84`, `8a8d2540` and `f09d342`
   (`c9e255e…`), and the fix's post-image is `f0f0abc…`, so the bytes under test
   in all three attempts are the same bytes.
4. **Counter version identity.** The v3 counter I ran is unchanged since
   attempt 1: `sha256(c1-measure-v3.py)` = `3188d4f80e928d1d8b45734ac8f6b253b799c6755abfafc3090b7aa9e76144f8`
   at HEAD and identical at `8a8d2540`. The v4 counter matches
   `contract-amendment-3.json`'s `counter_sha256`
   (`cccae0bd984a7c67c22d83a1e67d19e3ebc76c015094106a1370d330030a5f07`).

## Files

Written (both inside `tameshi-shokunin`, both mine):

- `.ufo/waves/round-30/wA/RerunV3Witness.md` — this report.
- `.ufo/evidence/round-30/wA/RerunV3Witness-c1v3-rerun.stdout` — raw stdout of
  the assigned run at rev `cfcc11ff`.
- `.ufo/evidence/round-30/wA/RerunV3Witness-c1v3-rerun-seed2.stdout` — raw stdout
  of the seed-variant run at rev `b85716a8`.
- `.ufo/evidence/round-30/wA/RerunV3Witness-c1v3-at-base-rerun.stdout` — raw
  stdout of the discrimination run at the unfixed base `f09d342`.

No production file was edited. No git write command ran outside the seat clone
`/fast/scratch/hyaku/tameshi-r30a2-seats/RerunV3Witness-7/clone` (commits
`cfcc11ff`, `b85716a8`). No `jj` command was run. The forbidden sealed
directory was not opened, listed, searched or read. No tool was installed or
updated; bubblewrap 0.13.1 was already present and was used only for the
sandbox spot check above. All long runs were wrapped in `timeout -k 5 1500` with
`--jobs 4`; no process started by this seat was left running (a `/proc/*/cwd`
scan of the seat directory found none, and no `tameshi-r30-c1-*` temp
directory remained).

## Risks

- The public axis counts are seed-invariant as measured here (four revs, two
  counter versions, three independent receipts), but they are not seed-*proof*:
  each rev draws its own mutants, so a future rev draws fresh instances that no
  receipt has covered. The kill rule therefore still requires a receipt per rev.
- The H-row label reuse across revs is the sharpest reporting hazard in this
  counter: a receipt that reports only row names would read as "the same 12
  mutants were killed" when in fact 12 different byte-strings were killed each
  time. The committed receipts print the rev in the summary line; keep that.
- My measurement covers the public axes only. The sealed (j)/(k) axes have one
  receipt (attempt 2's `v4/witness.stdout`) and no independent re-measure from
  this seat.
