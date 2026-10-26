# T48ExecSelftestReceipts — round-47 counter selftest receipts (routed defects 2 and 4)

seat: T48ExecSelftestReceipts (executor, leaf)
round: 48 / wave 1 / hyaku attempt 1
base revision measured: `473336d9d789f6081195e7376d17836a24666bc3` (lane `tameshi-shokunin`)
lane HEAD at the time of the run: `f1cfaad360130933983cac19f7036a8151f9054b`
scratch clone: `/fast/scratch/hyaku/tameshi-r48/T48ExecSelftestReceipts/lane` (`git clone -q --shared`, detached at BASE)
deliverables: `.ufo/waves/round-48/w1/selftest/` (23 files, listed in §7)

Item as assigned: the counter selftests the round-47 report cites have no committed L1 receipts
(`corpus/lessons/round-47-verifier-spotcheck.md:23-24` conformance defect 3, and `:104` routed defects 2 and 4).
Run each selftest at BASE, capture stdout / stderr / exit byte-exact, compare every tally with the claimed
tally, and answer whether any of the sources writes under `/tmp` regardless of `TMPDIR`.

## 1. Six files under test, pinned at BASE

`sha256` computed in the BASE clone (`git cat-file` verified BASE; `git diff --stat 473336d9 HEAD -- .ufo/evidence/round-47 .ufo/evidence/round-46` is empty, so these bytes are identical at the lane HEAD used by the file's own hardcoded path).

| # | file | sha256 (BASE) | rev=`473336d9` | rev=HEAD |
|---|---|---|---|---|
| 1 | `.ufo/evidence/round-47/calibration/measure.py` | `c54debb241c0df7fa282f619bb0905472a375ce0b3e5f800edc6f8945daa0f30` | same | same |
| 2 | `.ufo/evidence/round-47/hardening/pool.py` | `7ea9ab1e2bcf0b15df7dc4e8f7ac5b91a5446c899623a5aeefba815fa40e1904` | same | same |
| 3 | `.ufo/evidence/round-47/coverage/measure.py` | `c8fb89e69196fc2401e2364142b848bd8d53e5c6e3d97f17c528951c9f894260` | same | same |
| 4 | `.ufo/evidence/round-47/quality/addition-lint.py` | `c33914274013088d4c266ff2d85bcb34e800815639738690f3ac44a0d99dd56a` | same | same |
| 5 | `.ufo/evidence/round-47/quality/lesson-quote-check.py` | `858b020f6c40a21939a8231e11436e1552658b4489b396e2114fb158ffc83db6` | same | same |
| 6 | `.ufo/evidence/round-47/quality/falsifiers.sh` | `199c7d0953e378a2ed171184cdfd07ca8e33183930f47b278f1f70a4e511f460` | same | same |

## 2. Invocations and receipts (all exit 0)

Run from the BASE clone root, `TMPDIR=/fast/scratch/hyaku/tameshi-r48/T48ExecSelftestReceipts/tmp`.

| claim id | command | tally line (stdout, verbatim) | exit | stdout sha256 | receipt |
|---|---|---|---|---|---|
| C1 | `python3 .ufo/evidence/round-47/calibration/measure.py --selftest` | `C1_R47_SELFTEST: cases=35 failed=0` + `VERDICT: PASS` | 0 | `67399ce23938add1df347eb45c023777c2bd1cb18d0211947febc1463b2da100` | `selftest/c1-measure.{stdout,stderr,exit}` |
| C2 | `python3 .ufo/evidence/round-47/hardening/pool.py --selftest` | `C2_R47_SELFTEST: cases=14 failed=0` + `VERDICT: PASS` | 0 | `e51c59a90a4736b78ceb57b0cd54383b5168a0305c0e140e754b176b48ed6847` | `selftest/c2-pool.{stdout,stderr,exit}` |
| C3 | `python3 .ufo/evidence/round-47/coverage/measure.py --selftest` | `C3_R47_SELFTEST: cases=24 failed=0` + `VERDICT: PASS` | 0 | `75ff3e3b712c6c61e07e5e4bd016dadaec9745808202b84fc9ced39f185c33b4` | `selftest/c3-coverage.{stdout,stderr,exit}` |
| addition lint | `python3 .ufo/evidence/round-47/quality/addition-lint.py --selftest` | `ADDITION_LINT_SELFTEST: cases=7 failed=0` | 0 | `10b4b8814f1cf8e9443c55e3d8921f1f294a367d4d89de8c07aa9e7165140527` | `selftest/addition-lint.{stdout,stderr,exit}` |
| quote check | `python3 .ufo/evidence/round-47/quality/lesson-quote-check.py --selftest` | `LESSON_QUOTE_SELFTEST: cases=11 failed=0` | 0 | `3d38cf33945d744f41fd9f386a07e316cb184af0e1bdbce7e46d4019538c2540` | `selftest/lesson-quote-check.{stdout,stderr,exit}` |
| 91/92/93 | `bash <clone>/.ufo/evidence/round-47/quality/falsifiers.sh` (L→BASE clone, T→scratch, see §5) | 14 lines, 91/92/93 all `-FALSIFIER-OK` | 0 | `1be5af68e1f17c8ae9dd7418ba609f3efd22aef4588c2be84e39415662c6ac95` | `selftest/falsifiers.{stdout,stderr,exit}` + `falsifiers.baselane.sh` + `falsifiers.invocation.diff` |
| 91/92/93 | `bash .ufo/evidence/round-47/quality/falsifiers.sh` (committed bytes, unmodified, live lane path, `TMPDIR` pointed at scratch) | same 14 lines apart from the two temp/absolute paths on lines 2 and 10 | 0 | `472c128d2992d3ae11e532c63a2f1e054c57d35113ba88436d9e3c421daccb46` | `selftest/falsifiers-verbatim.{stdout,stderr,exit}` |

Every `.stderr` is empty (`e3b0c442…`, 0 bytes) except the falsifiers runs, whose only stderr is git's
detached-HEAD advice from block 92's own `git checkout --detach` (`f553068c…`, 580 bytes).
Every `.exit` file contains `0\n` (`9a271f2a…`).

Per-case corroboration: `grep -c '^PASS '` = 35 / 14 / 24 / 7 / 11 and `grep -c '^FAIL '` = 0 in all five;
no case name is duplicated in any of the five (`awk '{print $2}' | sort | uniq -d` empty in all five).

## 3. Tally by tally against what round 47 claims

| tally | claimed value | where the claim lives | observed at BASE | agree |
|---|---|---|---|---|
| C1 | 35/35 | `SCORECARD.md:2308` (`C1_R47_SELFTEST: cases=35 failed=0`); fleet `.ufo/reports/round-47/tameshi.md:12` ("C1 35/35") | `cases=35 failed=0`, 35 `PASS`, exit 0 | **yes** |
| C2 pool | 14/14 | `SCORECARD.md:2309` (`C2_R47_SELFTEST: cases=14 failed=0`); report `:12` ("C2 pool 14/14") | `cases=14 failed=0`, 14 `PASS`, exit 0 | **yes** |
| C3 | 24/24 | report `:12` only ("C3 24/24"); no SCORECARD capability row, no lane receipt file (in-lane mentions: `w1/T47MutC3Counter.md:6`, `w1/T47ScribeEntryPredict.md:28`) | `cases=24 failed=0`, 24 `PASS`, exit 0 | **yes** |
| addition lint | 7/7 | `SCORECARD.md:2310` (`cases=7 failed=0`) | `cases=7 failed=0`, 7 `PASS`, exit 0 | **yes** |
| quote check | 11/11 | `SCORECARD.md:2310` (`cases=11 failed=0`); the only pre-existing committed tally line anywhere is `.ufo/evidence/round-47/quality/c91-lesson-quote-red-green.stdout:2` (a `$ python3 … --selftest` transcript head) | `cases=11 failed=0`, 11 `PASS`, exit 0 | **yes** |

No tally disagreement exists: all five claimed tallies reproduce exactly, from the same bytes, at BASE.
The routed defect is a receipt defect, not a false-tally defect — before this wave the numbers were asserted
in prose with no captured stdout, and for C3 the only written claim was outside the lane repository.

## 4. Disagreements and discrepancies found (none in the tallies)

D1. **C2 selftest case ids are not contiguous: there is no `P13`.** The 14 cases are labelled
`P01…P12, P14, P15`. The tally `cases=14` is correct; a reader counting labels 1–15 would expect 15.
`pool.py` `selftest()` defines exactly 14 `check(...)` calls. Cosmetic, but it is the one place where the
claimed count and the printed ids disagree.

D2. **C1 selftest label groups are re-used.** `T24_*` and `T25_*` are absent from the first block and appear
only as 5 dependence variants each (`T24_undeclared_{bwrap,jj,node,fleet-root,env}_dependence`,
`T25_declared_<dep>_dependence_matches`), while `T26`/`T27` print before them. 23 + 10 + 2 = 35 matches
`cases=35`; no full case name repeats.

D3. **addition-lint prints `L07` first, then `L01…L06`.** 7 cases, 7 pass; label order is non-monotone.

D4. **`addition-lint.py` imports `tempfile` and never uses it** (`addition-lint.py:25`; the only occurrence in
the file). The lint bans `exec/eval/compile`, packed imports and copies, but not its own dead import.

D5. **The counters' stdout is not byte-reproducible across runs.** Each `PASS` line of the C1 selftest embeds
`rev=<40-hex>` of a freshly created fixture commit. A second C1 selftest run is identical to the first
**after masking `rev=[0-9a-f]{40}` → `rev=<sha>`** (`diff` of the two masked streams empty; the unmasked diff is
35/35 lines on `rev=` alone). So a committed C1 selftest receipt is evidence of one execution, not a
re-derivable byte target. The other four selftests are byte-stable (no generated hashes in their output).

## 5. The criterion-93 block, and what the whole script prints

Whole-script stdout at BASE (14 lines; line numbers as committed in `selftest/falsifiers.stdout`):

```
1  LESSON_QUOTE_CHECK: file=corpus/lessons/round-46.md blocks=3 quotes=3 bad=1 unbound=1
2  LESSON_QUOTE_CHECK: file=<BASE clone>/.ufo/evidence/round-47/quality/round46-lesson-dash-restored.md blocks=3 quotes=3 bad=0 unbound=1
3  CRITERION-91-FALSIFIER-OK
4  dep_mismatch=1
5  dep_mismatch=0
6  CRITERION-92-FALSIFIER-OK
7  CTL_E_selftest_pins_rule_ast rc=1 C2_R47: … killed=183 applicable=183 neutral_killed=14 pristine=2 equivalence=1 target=150 rev=HEAD C2_R47_PASS=false
8  CTL_G_round46_hardened_unchanged rc=1 C2_R47: … killed=122 applicable=183 neutral_killed=0 pristine=2 equivalence=1 target=150 rev=HEAD C2_R47_PASS=false
9  CTL_H_ast_pin_by_bare_assert rc=1 C2_R47: … killed=0 applicable=183 neutral_killed=0 pristine=2 equivalence=1 target=150 rev=HEAD C2_R47_PASS=false
10 LINT EXEC <tmp>/oracle.py:4 call to compile
11 ADDITION_LINT: files=1 findings=4
12 ADDITION_LINT: files=6 findings=0
13 c93 oracle_lint_exit=1 real_additions_lint_exit=0
14 CRITERION-93-FALSIFIER-OK
```

Block 93 itself prints lines 7–14 and ends `CRITERION-93-FALSIFIER-OK`: the planted compiled-oracle addition is
refused (`oracle_lint_exit=1`, 4 findings, first finding named with file and line), the six real seat additions
pass (`files=6 findings=0`, `real_additions_lint_exit=0`), and the three acid controls print the shapes the
block requires (`CTL_E` `neutral_killed=14`, `CTL_G` `killed=122` with `C2_R47_PASS=false`, `CTL_H` `killed=0`).
So criterion 93 does pass at BASE and it does print `OK`; only its receipt was missing.

Limits of this 93 receipt, stated plainly:
- The block pipes `run-controls.py` through `grep -E '^CTL_(E|G|H)' | cut -c1-260`. `CTL_A…CTL_D` and `CTL_F`
  executed and their lines were discarded by the script's own filter; nothing here shows how they behaved.
  The `cut -c1-260` also truncates each CTL line (the observed lines are shorter than 260, so nothing is lost
  in this run).
- `falsifiers.sh` has no failure exit: its last statement is `rm -rf "$T"`, so `exit=0` is printed even for a
  VACUOUS run. The exit code carries no verdict; only the `CRITERION-*-FALSIFIER-OK` lines do.

**The committed round-47 receipt cannot be a verbatim capture of this script.**
`.ufo/evidence/round-47/quality/c91-92-falsifiers.stdout` (7 lines) is:

```
1 dep_mismatch=1
2 dep_mismatch=0
3 CRITERION-91-FALSIFIER-OK
4 CTL_E_…   5 CTL_G_…   6 CTL_H_…
7 CRITERION-92-FALSIFIER-OK
```

Against my run it (a) omits both `LESSON_QUOTE_CHECK` lines that block 91 prints, and (b) places
`CRITERION-91-FALSIFIER-OK` at line 3 — *after* the two `dep_mismatch` lines, which the script prints only
inside block 92 (script order: 91-tail, 91-OK, then dep_mismatch ×2, then 92-OK). It also carries three `CTL_`
lines that only block 93 prints. The committed file is therefore an assembled subset of blocks 91–93, not a
run receipt. This is the concrete, checkable form of routed defect 4's "the report says the receipt was taken
before 91 was added to the script, yet it contains the 91 line".

Corroboration of routed defect 3 (no receipts, but the intent existed): the lane working tree contains
`.ufo/evidence/round-47/selftest/` — **empty**, `0` files, `git ls-files .ufo/evidence/round-47/selftest | wc -l` = 0,
and the directory does not exist in the BASE clone (git cannot carry it). Round 46 has the parallel
`.ufo/evidence/round-46/selftest/{c1,c2,c3}-selftest.{stdout,exit}`; round 47 created the directory and wrote
nothing into it.

## 6. Temp paths: does anything write under `/tmp` regardless of `TMPDIR`?

Grep of the six sources plus the script they call (`.ufo/evidence/round-47/control/run-controls.py`) for
`mktemp|mkdtemp|TemporaryDirectory|/tmp|/var/tmp|TMPDIR`:

| script | temp mechanism | honours `TMPDIR`? |
|---|---|---|
| `calibration/measure.py` | `tempfile.TemporaryDirectory(prefix='tameshi-r47-c1-')` (`:426`); profile shim sets child `TMPDIR` to `<work>/<prof>/tmp` (`:185-188`), `--work` is caller-supplied and in `--selftest` lives inside the temp dir | yes |
| `hardening/pool.py` | `TemporaryDirectory` `tameshi-r47-pool-` (`:169`), `tameshi-r47-eq-` (`:196`) | yes |
| `coverage/measure.py` | `TemporaryDirectory` `tameshi-r47-c3-` (`:206`) | yes |
| `addition-lint.py` | imports `tempfile`, never uses it; writes nothing | n/a |
| `lesson-quote-check.py` | `TemporaryDirectory` `tameshi-r47-lq-` (`:127`) | yes |
| `quality/falsifiers.sh` | **`T=$(mktemp -d -p /var/tmp)` (`:8`) — hardcoded, `TMPDIR` ignored** | **no** |
| (called by block 93) `control/run-controls.py` | `tempfile.mkdtemp(prefix='tameshi-r47-ctl-')` (`:54`), **never removed** (no `rmtree` in the file; `shutil` is used only for `copyfile`) | yes, but leaks |

Observed, not inferred:
- With `TMPDIR` pointed at my scratch, the unmodified script still put its work dir under `/var/tmp` — the
  block-93 lint line names `/var/tmp/tmp.fOCdHgxMdZ/oracle.py` (`falsifiers-verbatim.stdout:10`). It removed it
  on exit: `/var/tmp/tmp.*` count before = 0, after = 0.
- Nothing in the six writes under `/tmp`: with `TMPDIR` set, all `tempfile` output landed under my scratch
  `tmp/`, and `/tmp` gained nothing from these runs. The literal string `/tmp` appears in none of the six
  (the only near-hit is the `'TMPDIR'` env key at `measure.py:188`).
- `run-controls.py` leaks: **8 full lane clones per falsifiers.sh execution**, one per control
  (`CTL_A…CTL_H`). Two executions left 16 `tameshi-r47-ctl-*` directories in `TMPDIR`, **2.7 GB** total
  (`du -sh`). On a default `TMPDIR=/tmp` that is 2.7 GB of full lane clones left behind per falsifiers run —
  the real temp-hygiene defect in this set, and it is the *called* script, not the caller.

Incidental, out of my item and outside these six: `/tmp` currently holds 24 empty `tameshi-r4-2-regression.*`
directories (timestamps 05:44–05:45 today) created by `tools/mutate-and-run.sh` (`:142`, `:482` hardcode `/tmp`
defaults), which is another seat's selftest running during this wave. Not attributed, not scored.

## 7. Delivered files

`.ufo/waves/round-48/w1/selftest/` (23 files): `c1-measure`, `c2-pool`, `c3-coverage`, `addition-lint`,
`lesson-quote-check`, `falsifiers`, `falsifiers-verbatim` — each as `.stdout` / `.stderr` / `.exit` — plus
`falsifiers.baselane.sh` (the exact script that produced `falsifiers.*`) and `falsifiers.invocation.diff`
(the two-line substitution: `L=` → BASE clone, `T=` → scratch `tmp/`). Nothing else in the lane was written;
the BASE clone's work tree stayed clean (`git -C <clone> status --porcelain` empty throughout).

## 8. Risks, limits, boundaries

- **What I claim:** the five selftests and the 91/92/93 blocks produce the bytes in §2 at BASE, exit 0, and the
  five tallies agree with every written claim. Nothing here is a verdict on C1/C2/C3 or on any axis.
- **Boundary I crossed only because the item ordered the whole script:** block 93 executes
  `run-controls.py`, i.e. it scores CTL_E/F/G/H over the 183-mutant pool. Those numbers appear in my receipts as
  the script's own printed bytes; I did not use them to score a claim, and they are not a deciding observation.
  CTL_A–D and CTL_F output was discarded by the script's own `grep` (see §5).
- **The falsifiers receipt is not a run of the committed path defaults.** The committed script hardcodes
  `L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`, so a faithful BASE run needs `L` repointed; I recorded the
  exact two-line diff and also ran the committed bytes unmodified (lines identical except the two path-bearing
  lines). Any future reader should treat `falsifiers-verbatim.*` as the "committed script" receipt and
  `falsifiers.*` as the "BASE revision" receipt.
- **The receipts are evidence of one execution each**, not reproducible byte targets for C1 (embedded fixture
  commit hashes) and not for `falsifiers` (temp paths in lines 2 and 10).
- **Routed defect 2 is closed for the five counters and for 91/92/93 only as far as these receipts go**; the
  round-48 deciding run and its own selftest policy remain the L1's. Removing the newly committed receipts
  from the tree would restore the defect exactly.
- **Routed defect 4 is now evidenced at its root**: the round-47 committed 91/92 receipt is an assembled
  subset spanning three blocks (§5), which is why it looked like "taken before 91 was added".
- No tool was installed, upgraded or fetched for this item (nothing was needed; `git`, `python3`, `bash`,
  `mktemp`, `du` were sufficient). No pacman transaction was attempted.
- Scratch `/fast/scratch/hyaku/tameshi-r48/T48ExecSelftestReceipts/` (including the 2.7 GB of leaked clones
  measured above) was deleted before this report was returned.
