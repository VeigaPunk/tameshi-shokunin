# DevMulti — two-edit mutation sweep of the frozen tally-audit-v2 (round 33, wave 1)

## Verdict

**The frozen tool survives 16 of my 62 mutants (9 two-edit pairs and their 7 single-edit block controls) while the runner tally block behaves differently from pristine.** All 16 are tally-block conditional edits whose trigger needs a status `>= 3` in one leg AND a non-zero status in another leg; the frozen runtime sweep never produces that combination (it tests every status 0..255 alone, and only 0/1/2 combinations). The most severe witness turns `REGRESSION: SETUP` (exit 2) into `REGRESSION: PASS` (exit 0).

No pair in the requested "each edit alone is caught, the pair slips" form passed: every two-edit pair whose head or harness edit is caught alone was rejected by the tool (41 of 62 probes exited 1). The misses are not interaction-masking; they are a vector-coverage hole in `check_runtime` plus two unchecked head/harness weakenings that do not change tally behavior.

## Frozen bytes and setup

```
lane commit  f6d8a891f1d966c5c3cdda385090da3a6e804675 (detached clone, --no-hardlinks)
tools/tally-audit-v2.py  sha256 9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4
tools/mutate-and-run.sh  sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  (matches the a7d3f2dd...2eb9 pin)
scratch: /fast/scratch/hyaku/tameshi-r33-seats/DevMulti/  (lane clone + tool.py + pristine.sh + mutants/ + logs/)
```

Extraction commands (all exit 0 in `clone.rc`, `checkout.rc`, `toolshow.rc`, `runnershow.rc`):

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach f6d8a891f1d966c5c3cdda385090da3a6e804675
git -C lane show f6d8...:tools/tally-audit-v2.py > tool.py
git -C lane show f6d8...:tools/mutate-and-run.sh > pristine.sh
```

Baseline detector on pristine (`base/rc.txt` = 0):

```
$ timeout 300 python3 tool.py --runner m.sh
CHECK runtime PASS vectors=2395 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=29/29
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

## Method

1. 38 two-edit mutants (M01-M38): one edit in the tally block (runner:1432-1470) plus one edit in the head (runner:1386-1430) or in the selftest tally harness (runner:1992-2040). 24 single-edit controls (S_*) isolate each edit.
2. Every edit is one exact-string replacement; `apply()` aborts unless the old string occurs exactly once and the pair changes the file. Mutant files are separate copies (`mutants/<id>.sh`); the pinned `pristine.sh` is never modified.
3. Each mutant was audited with `timeout 300 python3 tool.py --runner mutants/<id>.sh`; exit code and final `TALLY_AUDIT:` line are recorded in `results.tsv` and `logs/<id>.out` (`EXIT <rc>` trailer).
4. For every tool PASS, `eqcheck.py` extracted the mutant tally block and compared it with the pristine tally block in bash, using the tool's own runner machinery plus a wider vector set: all 2304 single-status vectors, all 3600 position-pair vectors over statuses {1,2,3,4,5,7,9,120,128,255}, 80 selected triples, and seven all-nonzero vectors. Comparison is (exit code, first stdout line). A difference is a survivor; the witness is the first differing vector.
5. Witnesses for the survivors were re-run independently in plain bash (`verify/*.sh`, `verify.out`, `verify.rc` = 0), outside the tool's driver.

Edits (exact):

- `b_mask3to1` — tally block, after runner:1433 `for st in ...; do`: insert `    if [[ $st == 3 && $st_kagi == 2 ]]; then st=1; fi` (restatus a 3 as fail only when st_kagi is 2)
- `b_mask3to0` — tally block, after runner:1433: insert `    if [[ $st == 3 && $st_kagi == 2 ]]; then st=0; fi`
- `b_printfswap5` — tally block, FAIL printf (runner:1442-1443): args `"$nfail" "$nsetup"` replaced by locals f3/f4, swapped only when `$st_js == 5`
- `b_failskip3` — tally block, runner:1441: `[[ $nfail -gt 0 ]]` -> `[[ $nfail -gt 0 && $st_js != 3 ]]`
- `b_setupskip120` — tally block, runner:1446: `[[ $nsetup -gt 0 ]]` -> `[[ $nsetup -gt 0 && ! ( $st_kagi == 120 && $st_mado == 2 ) ]]`
- `b_sumskip3` — tally block, runner:1455: `!= nlegs` -> `!= nlegs && $st_js != 3`
- `b_double_arm4` — tally block, runner:1436 arm 1: append `; [[ $st_js == 4 ]] && nfail=$((nfail + 1))`
- `b_setup_exit1` — tally block, SETUP branch (runner:1446): insert `if [[ $st_js == 3 && $st_kagi == 2 ]]; then exit 1; fi` before the SETUP printf
- `b_pass_exit2` — tally block, before runner:1470 `exit 0`: insert `[[ $st_js == 6 && $st_kagi == 7 ]] && exit 2`

Second edits:

- `h_mask127` — head, runner:1395: `st_kagi=$?` -> `st_kagi=$(($? & 127))`
- `h_dup` — head, runner:1415: duplicate `st_claims=$?`
- `h_extra` — head, runner:1430: add `st_extra=$?` after st_citecheck
- `h_swapcalls` — head, runner:1386-1396: swap the js-kimi-census and bash-surface-census call blocks including their st_js/st_kagi lines
- `h_swapbodies` — head, runner:1386-1396: swap only the two regression_case_git call bodies, leaving `st_js=$?` and `st_kagi=$?` in place
- `h_forcepass` — head, runner:1394: append ` || :` to the bash-surface-census call so st_kagi is always 0
- `x_skip8` — harness, runner:2022: `for ti in 0 1 2 3 4 5 6 7 8` -> `... 7 7` (position 8 skipped)
- `x_exitonly` — harness, runner:2005: comparison drops the stdout first-line check, keeps rc
- `x_dropguard` — harness, runner:2035-2040: remove the completeness-guard selftest (drop-operand -> SETUP)
- `x_dropstatus3` — harness, runner:2024: remove the status-3 mixed vector
- `x_droptwofail` — harness, runner:2013: remove the two-failing-legs vector
- `x_sanity1` — harness, runner:1996: tnames sanity `-eq 9` -> `-ge 1`
- `x_injectoverride` — harness, after runner:1994: add a second awk extraction piped through sed, so the tool's `tblock=$AUDIT_INJECT` is overwritten with the real block

## Survivors (tool PASS, tally behavior differs)

| id | edits | witness statuses | pristine (exit, first line) | mutant (exit, first line) | tool |
|---|---|---|---|---|---|
| M08 | B:b_mask3to1+X:x_sanity1 | `3 2 0 0 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)` | PASS (all four checks) |
| M09 | B:b_mask3to1+H:h_forcepass | `3 2 0 0 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)` | PASS (all four checks) |
| M12 | B:b_mask3to0+X:x_sanity1 | `3 2 0 0 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `2` `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)` | PASS (all four checks) |
| M16 | B:b_failskip3+X:x_sanity1 | `3 1 0 0 0 0 0 0 0` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=1)` | PASS (all four checks) |
| M18 | B:b_setupskip120+X:x_sanity1 | `0 120 0 2 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `0` `REGRESSION: PASS (cases=9 passed=7; ledger legs exact: killed-delta<=0 flips<=0)` | PASS (all four checks) |
| M20 | B:b_double_arm4+X:x_sanity1 | `4 1 0 0 0 0 0 0 0` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=1)` | PASS (all four checks) |
| M35 | B:b_mask3to1+H:h_swapbodies | `3 2 0 0 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)` | PASS (all four checks) |
| M36 | B:b_setup_exit1+H:h_swapbodies | `3 2 0 0 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `1` (no stdout line) | PASS (all four checks) |
| M38 | B:b_printfswap5+H:h_swapbodies | `5 1 2 0 0 0 0 0 0` | `1` `REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)` | `1` `REGRESSION: FAIL (cases=9 passed=6 failed=2 setup=1)` | PASS (all four checks) |
| S_b_mask3to1 | B:b_mask3to1 | `3 2 0 0 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)` | PASS (all four checks) |
| S_b_mask3to0 | B:b_mask3to0 | `3 2 0 0 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `2` `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)` | PASS (all four checks) |
| S_b_printfswap5 | B:b_printfswap5 | `5 1 2 0 0 0 0 0 0` | `1` `REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)` | `1` `REGRESSION: FAIL (cases=9 passed=6 failed=2 setup=1)` | PASS (all four checks) |
| S_b_failskip3 | B:b_failskip3 | `3 1 0 0 0 0 0 0 0` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=1)` | PASS (all four checks) |
| S_b_setupskip120 | B:b_setupskip120 | `0 120 0 2 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `0` `REGRESSION: PASS (cases=9 passed=7; ledger legs exact: killed-delta<=0 flips<=0)` | PASS (all four checks) |
| S_b_double_arm4 | B:b_double_arm4 | `4 1 0 0 0 0 0 0 0` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)` | `1` `REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=1)` | PASS (all four checks) |
| S_b_setup_exit1 | B:b_setup_exit1 | `3 2 0 0 0 0 0 0 0` | `2` `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | `1` (no stdout line) | PASS (all four checks) |

Witness vectors are ordered `st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck`.

The sharpest witness (`S_b_setupskip120`, `M18`): statuses `0 120 0 2 0 0 0 0 0` give pristine `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` exit 2, mutant `REGRESSION: PASS (cases=9 passed=7; ledger legs exact: killed-delta<=0 flips<=0)` exit 0. A runner that silently reports PASS while two legs need setup cannot be distinguished from a clean pass on this tally.

## Passing mutants that are tally-equivalent

- `M31` (B:b_pass_exit2+X:x_sanity1): tally block identical in behavior over the full 5991-vector sweep.
- `S_b_pass_exit2` (B:b_pass_exit2): tally block identical in behavior over the full 5991-vector sweep.
- `S_h_forcepass` (H:h_forcepass): tally block identical in behavior over the full 5991-vector sweep.
- `S_h_swapbodies` (H:h_swapbodies): tally block identical in behavior over the full 5991-vector sweep.
- `S_x_sanity1` (X:x_sanity1): tally block identical in behavior over the full 5991-vector sweep.

Notes: `b_pass_exit2` is dead code — the PASS path is only reachable when every status is 0, so `st_js == 6 && st_kagi == 7` can never hold there; the tool is right to pass it and the mutant is equivalent. `S_h_forcepass` (`|| :` after a leg call) and `S_h_swapbodies` (call bodies swapped under the original `st_*=$?` lines) are real runner defects the tool does not see: `check_head` is syntactic and the head is never executed, so the tool passes a runner that reports a setup/failing leg as passing or attributes statuses to the wrong leg. `S_x_sanity1` weakens the runner's own selftest sanity check (tnames count 9 -> >=1); the tool's fault panel does not cover it.

## Two-edit pairs: no masking interaction found

All 38 pairs and all 24 singles, with tool exit and verdict:

| id | edits | tool exit | verdict |
|---|---|---|---|
| M01 | B:b_mask3to1+H:h_mask127 | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| M02 | B:b_mask3to1+H:h_dup | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| M03 | B:b_mask3to1+H:h_extra | 1 | FAIL (head=pass static=fail runtime=fail harness=fail) |
| M04 | B:b_mask3to1+H:h_swapcalls | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M05 | B:b_mask3to1+X:x_skip8 | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M06 | B:b_mask3to1+X:x_exitonly | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M07 | B:b_mask3to1+X:x_dropstatus3 | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M08 | B:b_mask3to1+X:x_sanity1 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| M09 | B:b_mask3to1+H:h_forcepass | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| M10 | B:b_mask3to0+H:h_mask127 | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| M11 | B:b_mask3to0+X:x_dropguard | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M12 | B:b_mask3to0+X:x_sanity1 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| M13 | B:b_printfswap5+H:h_swapcalls | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M14 | B:b_printfswap5+H:h_dup | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| M15 | B:b_failskip3+X:x_exitonly | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M16 | B:b_failskip3+X:x_sanity1 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| M17 | B:b_setupskip120+H:h_dup | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| M18 | B:b_setupskip120+X:x_sanity1 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| M19 | B:b_double_arm4+H:h_mask127 | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| M20 | B:b_double_arm4+X:x_sanity1 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| M21 | B:b_setup_exit1+H:h_swapcalls | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M22 | B:b_mask7+H:h_mask127 | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| M23 | B:b_mask7+X:x_sanity1 | 1 | FAIL (head=pass static=pass runtime=fail harness=pass) |
| M24 | B:b_arm3pass+H:h_swapcalls | 1 | FAIL (head=pass static=pass runtime=fail harness=fail) |
| M25 | B:b_arm4setup+X:x_skip8 | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M26 | B:b_nlegs8+H:h_swapcalls | 1 | FAIL (head=pass static=fail runtime=fail harness=fail) |
| M27 | B:b_printfswap+H:h_extra | 1 | FAIL (head=pass static=fail runtime=fail harness=fail) |
| M28 | B:b_dropcite+X:x_sanity1 | 1 | FAIL (head=pass static=fail runtime=pass harness=pass) |
| M29 | B:b_guardover+H:h_dup | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| M30 | B:b_sumskip3+X:x_injectoverride | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M31 | B:b_pass_exit2+X:x_sanity1 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| M32 | B:b_pass_exit2+H:h_mask127 | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| M33 | B:b_mask3to1+X:x_droptwofail | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M34 | B:b_mask3to1+X:x_injectoverride | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| M35 | B:b_mask3to1+H:h_swapbodies | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| M36 | B:b_setup_exit1+H:h_swapbodies | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| M37 | B:b_nlegs8+H:h_swapbodies | 1 | FAIL (head=pass static=fail runtime=fail harness=fail) |
| M38 | B:b_printfswap5+H:h_swapbodies | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_b_mask3to1 | B:b_mask3to1 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_b_mask3to0 | B:b_mask3to0 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_b_printfswap5 | B:b_printfswap5 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_b_failskip3 | B:b_failskip3 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_b_setupskip120 | B:b_setupskip120 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_b_double_arm4 | B:b_double_arm4 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_b_setup_exit1 | B:b_setup_exit1 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_b_pass_exit2 | B:b_pass_exit2 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_b_mask7 | B:b_mask7 | 1 | FAIL (head=pass static=pass runtime=fail harness=pass) |
| S_b_arm3pass | B:b_arm3pass | 1 | FAIL (head=pass static=pass runtime=fail harness=pass) |
| S_b_nlegs8 | B:b_nlegs8 | 1 | FAIL (head=pass static=fail runtime=fail harness=fail) |
| S_h_mask127 | H:h_mask127 | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| S_h_dup | H:h_dup | 1 | FAIL (head=fail static=fail runtime=fail harness=fail) |
| S_h_extra | H:h_extra | 1 | FAIL (head=pass static=fail runtime=fail harness=fail) |
| S_h_swapcalls | H:h_swapcalls | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| S_h_forcepass | H:h_forcepass | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_h_swapbodies | H:h_swapbodies | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_x_skip8 | X:x_skip8 | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| S_x_exitonly | X:x_exitonly | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| S_x_dropguard | X:x_dropguard | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| S_x_dropstatus3 | X:x_dropstatus3 | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| S_x_droptwofail | X:x_droptwofail | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |
| S_x_sanity1 | X:x_sanity1 | 0 | PASS (head=pass static=pass runtime=pass harness=pass) |
| S_x_injectoverride | X:x_injectoverride | 1 | FAIL (head=pass static=pass runtime=pass harness=fail) |

Every pair combining an evasive block edit with a caught-alone second edit failed: `h_mask127`, `h_dup`, `h_extra` fail the head check; `h_swapcalls` moves the `st_*=$?` lines and fails the harness names-order gate; `x_skip8`, `x_exitonly`, `x_dropstatus3`, `x_droptwofail`, `x_dropguard` and `x_injectoverride` fail the harness fault panel. So the requested masking-by-pairing does not occur; the tool's four checks are independent at that level. The survivors instead pair an evasive block edit with a second edit the tool also cannot see (`x_sanity1`, `h_forcepass`, `h_swapbodies`).

## Coverage finding and smallest safe correction (recommendation only; frozen tool untouched)

`tool.py:309-345` (`check_runtime`) builds: every status 0..255 at every single position; every (failing, setup) count pair with status values only 0/1/2; a few 0/1/2 placement mixes; and operand stress on all-zero vectors. It never combines a status >= 3 with another non-zero status. Every survivor above is gated on exactly such a combination, e.g. `[3,2,0,0,0,0,0,0,0]`, `[3,1,0,...]`, `[0,120,0,2,0,0,0,0,0]`, `[5,1,2,0,...]`.

Smallest safe correction: after `tool.py:327`, add position-pair vectors over a status set `{1,2,3,4,5,7,9,120,128,255}` for every pair of leg positions (3600 vectors, the same class used by `eqcheck.py`). That class alone catches all 16 survivors and leaves every currently-caught probe caught. No runner edit and no contract change is proposed; `mutate-and-run.sh` stays at the pinned sha.

## Receipts and restoration

```
pristine.sh before/after : a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 (unchanged)
tool.py (frozen copy)    : 9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4 (unchanged)
lane/tools/*             : same two hashes; git -C lane status --porcelain prints nothing
mutants/                 : one file per probe; per-probe sha256 in results.tsv
exit receipts            : results.tsv exit column; logs/<id>.out ends with EXIT <rc>; base/rc.txt = 0; eqcheck.rc = 0; mutgen.rc/resume.rc recorded
independent witnesses    : verify.out (plain bash, one line per survivor/pristine); verify.rc = 0
processes                : none of my process trees remain (scan of /proc cwd under the scratch dir was empty)
tool installs            : none
```

No production file, lane byte, git index or jj state was touched; the only write outside the scratch dir is this report. The frozen counters were not run (this item does not name them).
