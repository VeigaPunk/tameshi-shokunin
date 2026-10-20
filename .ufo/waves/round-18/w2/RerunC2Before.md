# RerunC2Before — round-18 w2: C2 before-state re-run with ruler v2, and the v1→v2 ruler diff

Seat: TameshiR18.RerunC2Before (falsify). Read rev 01d586ddbc5fcd78659557c4e93a6ee8517b87d1.
I checked three things: (1) **before-state**: does v2 still read open=11 at 183f87b; (2) **calibration**: can either v2 change turn a probe closed when the fix is missing; (3) **operability side effects** of the v2 changes.

Scratch: W=/tmp/tameshi-r18w2-RerunC2Before-TcNdSK. The clone is `$C=$W/fleet/tameshi-shokunin`, detached at 01d586d, with sibling symlinks in place. Every ruler run used the contract's outer envelope:
`bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind $W $W --unshare-net --die-with-parent --chdir $C env -i PATH=$PATH HOME=$W/home TMPDIR=$W/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 <ruler> --rev <REV> [--only P08]`
In that envelope the fleet and the lane are read-only. The ruler's hard-coded `/tmp/tameshi-r18w1-X03DefectProbes-*` scratch was created in the outer tmpfs, so none of it reached the host /tmp: a host count after all runs returned `0`. Interpreter: /usr/bin/python3 3.14.8. Other versions: bwrap 0.13.1, jj 0.45.1 at /home/vgpnk/.local/bin/jj. `/usr/bin/jj` and `/bin/jj` are absent.

## 1. Before-state re-run (the assigned command): open=11 reproduced

- Ruler identity: lane file sha256 `99297d96…daebeaa`. This equals `git show 01d586d:.ufo/evidence/round-18/defect-probes.py`. The v1 blob at aee4f36, 58e5d53 and e08271a is `a25fdcdc…f231e97`.
- Command run: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/defect-probes.py --rev 183f87b899e6cae46be98d251cbc87fb5118f6ca` (inside the envelope above) → **exit 0, 31.4 s, `DEFECT_PROBES: open=11 closed=0 total=11`**.
  - P01 and P02: `pristine_exit=0 mutant_exit=0 … SELFTEST: PASS (56/56)`.
  - P03 and P04: `SELFTEST: PASS (34 cases)`.
  - P05–P07: `SELFTEST: 27/27`.
  - P08: `G2-live-bytes open … findings=[]; G3-ancestor open … findings=[]`.
  - P09: `NaN:open exit=1 … ValueError: cannot convert float NaN to integer; Infinity:open exit=1 … OverflowError`.
  - P10: `setsid … survivors=[5]; setpgid … survivors=[5]`.
  - P11: `tainted_exit=2 … declared=False WITNESS_STUDY: CANNOT-EVALUATE (git show fecee87…:corpus/surface-census.sh failed …)`.
- Comparison with the L1 receipt: I normalized 40-hex ids, `selftest.XXXXXXXX` suffixes and declaration sha256s, then sorted and diffed against `.ufo/evidence/round-18/c2-probes-v2-183f87b.txt` (sha256 `f5e657d0…2a2e`). Result: **MATCH**. Re-running every other receipt the same way:

| my run | ruler | rev | exit | summary | matches receipt |
|---|---|---|---|---|---|
| run1 | v2 | 183f87b | 0 | open=11 closed=0 | c2-probes-v2-183f87b.txt |
| run2 | v1 (aee4f36 blob) | 183f87b | 0 | open=11 closed=0 | c2-probes-183f87b.txt (`60e9994e…`) |
| run3 | v1 | e08271a | 2 | could-not-evaluate (P01, P02, P08 error) | c2-probes-e08271a.txt (`1e2fddbb…`) |
| run4 | v2 | e08271a | 0 | open=0 closed=11 | c2-probes-v2-e08271a.txt (`e61e777b…`) |
| run5 | v2 | 01d586d | 0 | open=0 closed=11 | same as run4 (tools unchanged by 01d586d) |

## 2. The v1→v2 diff

`git diff aee4f36 01d586d -- .ufo/evidence/round-18/defect-probes.py` (exit 0) has exactly two hunks:
- **PATH**: `defect-probes.py:154-156`. Child `PATH` changes from `"/usr/bin:/bin"` to `dirname(JJ_COMMAND) + ":/usr/bin:/bin"`. `JJ_COMMAND = shutil.which("jj")` is resolved from the caller's PATH (`:49`).
- **Binding**: `defect-probes.py:482-485`. The P08 fixture now runs `git config lane.branch master` right after `jj git init --colocate`.

I rebuilt v2 from the v1 blob plus these two hunks and got **v2 byte-for-byte** (`v1+both == v2 bytes: True`). The two hybrids below therefore split the delta exactly:
- `dp-hybB-pathonly.py` (`cf4b8d9c…`) has only the PATH change.
- `dp-hybC-lanebranchonly.py` (`0b18e30d…`) has only the binding.

Both were run from `$C/.ufo/evidence/round-18/`, so `LANE_ROOT=$C`.

### Which change affects which probe (tip e08271a, full runs)

| ruler | P01 | P02 | P08 | P03–P07, P09–P11 | exit |
|---|---|---|---|---|---|
| v1 | error: pristine selftest `FAIL (3/63 failed: v2-jj-prebookmark-branch-tip, v2-jj-branch-tip, v2-jj-without-lane-branch)` | error (same) | error: `G2-live-bytes produced unexpected verdict exit=2 status='could_not_evaluate' findings=['historical_input_unavailable']` | closed ×8 | 2 |
| v1 + PATH only (run6) | **closed**: mutant `FAIL (1/63 failed: v2-historical-tag-object)` | **closed**: `v2-historical-symlink-mode` | error (unchanged) | closed ×8 (identical) | 2 |
| v1 + binding only (run7) | error (unchanged) | error (unchanged) | **closed**: G2 `['historical_input_uncommitted']`, G3 `['historical_input_unavailable']` | closed ×8 (identical) | 2 |
| v2 | closed | closed | closed | closed ×8 | 0 |

- Each change affects only the probes it targets, and in each case it turns an **error** into a graded verdict.
- No probe that v1 had already graded changes status, at the base or at the tip.
- The v1 tip errors are three probe errors with two causes. That matches the L1's "two ruler defects".

## 3. Can either change produce "closed" with the fix missing?

### 3a. PATH change (P01, P02): no

- **The kills do not depend on jj.** I ran the tip `tools/evidence-disposition.py --selftest` in a bwrap envelope that mirrors the ruler (`env -i`, HOME=/mnt/home, `/tmp`→`$W/edtest/tmp`, the same GIT_*/JJ_CONFIG values):

  | PATH | pristine | P01 mutant | P02 mutant |
  |---|---|---|---|
  | `/usr/bin:/bin` | exit 1, `FAIL (3/63 …)`; all three are `setup/process error: FileNotFoundError: … 'jj'` | exit 1, `4/63` = the same three **+ v2-historical-tag-object** | exit 1, `4/63` = the same three **+ v2-historical-symlink-mode** |
  | `/home/vgpnk/.local/bin:/usr/bin:/bin` | exit 0, `PASS (63/63)` | exit 1, `1/63 v2-historical-tag-object` | exit 1, `1/63 v2-historical-symlink-mode` |

  The killing cases fire with or without jj. Their setups use git only: `tools/evidence-disposition.py:2137-2146` (`_setup_hist_tag`) and `:2149-2159` (`_setup_hist_symlink`). The PATH change only repairs the **pristine control** (`defect-probes.py:383-386`), which requires pristine exit 0.
- **The tool does not call jj at runtime.** `["jj"]` appears only in the selftest helper `_jj` (`tools/evidence-disposition.py:2035-2049`), which only the fixture setups use (2168–2250). Run6 confirms this: with jj on PATH and no binding, P08 still errors.
- **No PATH shadowing.**
  - jj's directory is `/home/vgpnk/.local/bin`, which holds about 50 user binaries, including omp, codex, uv and rg. None of them is named python3, git, sh, bash, sleep, setsid, bwrap, env, true, strace, sqlite3 or the-janitor; my `[ -e ~/.local/bin/$n ]` loop printed no `SHADOW` lines.
  - A grep for every `~/.local/bin` name as a quoted command string, plus `which(`, across the tip and base `evidence-disposition.py`, `registry-check.py`, `bash-witness-study.py` and both `trace-inputs.py` copies found only:
    - `"jj"` (in `_jj`);
    - `shutil.which` calls for `strace`, `true`, `python3` and `bash` (`trace-inputs.py:608,618,771-772`);
    - `shutil.which` calls for `the-janitor` and `sqlite3` (`bash-witness-study.py:592-599`, base `:582-589`).

  All of those still resolve outside `~/.local/bin`.

### 3b. lane.branch binding (P08): no for the landed tip, but it weakens the ruler's ability to tell fixes apart

**The binding matches real lanes.**
- `scripts/hyaku/jj-lane.sh:439` runs `git config lane.branch "$branch"` during init (comment at `:89`).
- Read-only `git config --get lane.branch` across the fleet: every jj lane is bound (8 of 8). kama, mado, mori, souji, tabi, tameshi and tsukuroi use `master`; **kaidoku-shokunin uses `main`**. No non-jj lane is bound.
- The tameshi lane is detached (`symbolic-ref -q HEAD` exits 1), has `.jj`, and has `lane.branch=master`.
- The tip tool refuses an unbound jj workspace on purpose (`tools/evidence-disposition.py:492-496`, documented at `:51-53`). That refusal is exactly v1's P08 error.

**Counterfactual tool mutants.** I committed each variant only in my scratch clone, on `cf-*` branches made with `mktree`/`commit-tree`; HEAD stayed at 01d586d. Each was run with `--only P08`. "lanetip" is a hardened ruler variant of mine (`dp-v2-lanetip.py`, `5ad5d199…`): v2 with the P08 bookmark and binding renamed `master`→`lane-tip`.

| tool | v1 | **v2** | lanetip | tip selftest (jj on PATH) |
|---|---|---|---|---|
| landed tip 01d586d | error | closed | **closed** | PASS 63/63 |
| base 183f87b | open | open | open | (56/56 at base) |
| M1: anchor = HEAD (round-17 defect re-injected after `:461`) | open | **open** | open | FAIL 4/63 |
| M2: refuse every jj workspace | not run | error | not run | FAIL 2/63 |
| M3: anchor hardcoded to `refs/heads/master` | closed | closed | error | FAIL 3/63 |
| M4: refuse unbound jj, then hardcode `master` | error | **closed** | error | FAIL 2/63 (non-jj `v2-registry-clone-detached-anchor`, `v2-detached-no-published-ref`) |
| M5: one line, `:477` `branch_ref = "refs/heads/master"` (ignores the lane.branch value) | error | **closed** | error | **PASS 63/63** |

- Re-injecting the real defect (M1) still reads **open** under v2. The binding does not hide a HEAD-anchored tool.
- A blanket refusal (M2) reads **error**, because P08 requires exact finding lists per case (`defect-probes.py:541-550`).
- The landed tip also closes under lanetip. So it honours the **value** of lane.branch, and its closure is a real fix whatever the branch name.

## Findings, by severity

No blocking finding. The before-state reproduces (open=11, exit 0). The read-rev after-state also reproduces (open=0, exit 0). Neither v2 change turns a probe closed for the landed tip.

1. **Minor — calibration: P08 binds `master`, which is the only branch name P08 or the tool selftest ever uses.**
   - Evidence: `defect-probes.py:485` binds `"master"` and `:493/:530` set the bookmark `master`. The tool selftest only ever binds `master` (`tools/evidence-disposition.py:2167`).
   - Effect: v2 grades the value-ignoring partial fixes M4 and M5 as closed. v1 graded them error and lanetip graded them error. M5 also passes the tool's own selftest 63/63.
   - Why it matters: a fleet lane with a non-master binding exists (kaidoku-shokunin, `main`). The C2 count is unchanged because the landed tip passes lanetip. But the claim that "v2 closed" proves the lane.branch value is honoured rests on this seat's lanetip run, not on the L1's ruler.
   - Fix (for the L1 to route): bind a non-default name in P08, and add a selftest case with a non-master lane.branch.
2. **Minor — stale envelope doc.** `defect-probes.py:8` (docstring) still says `env -i PATH=/usr/bin:/bin`, but `:156` now puts `/home/vgpnk/.local/bin` first. The receipts' stated envelope no longer matches the code. It has no effect on any verdict (no shadowing, §3a).
3. **Minor — operability: the tip selftest now needs jj.**
   - Under `PATH=/usr/bin:/bin` the tip `tools/evidence-disposition.py --selftest` exits 1 with `FileNotFoundError: … 'jj'` on 3 of 63 cases. The base passed 56/56 under the same PATH.
   - It fails closed with a named cause, so it never falsely passes. But any jj-less gate or registry host now fails this row.
   - The new jj dependency arrived with 58e5d53. Calling v1's P01/P02 errors purely a "ruler defect" is therefore partly a judgment call: the v2 PATH change adapted the ruler to the tool.

## Residual risk / verification gaps

- Not re-checked: the registry 32/32 no-harm claim; the semantics of P09–P11, P03–P07 (v2 does not change them; outputs were identical across v1, v2 and both hybrids).
- P10 is timing-based (`timeout_s=1`, survivor scan). I ran each configuration once. Every result matched the L1 receipts.
- I attributed kills to specific selftest cases for P01/P02 only. For P03–P07, v1 and v2 give byte-identical outcomes, so no attribution was needed.
- My run outputs are ephemeral, under `$W/*.txt`. sha256 prefixes:
  - run1 `d4dcfd7f45484d37`, run2 `a31b05abbc9dee03`, run3 `8c245b029a8a44c2`, run4 `600ceb4af6ecd679`, run5 `9c42fda33a7c19b3`, run6 `26de02325668e531`, run7 `6bca527f4df016a2`;
  - cf-v2-M1 `57a24e2d244ec209`, cf-v2-M5 `5b9c6b82d9489a0e`, lanetip-tip `658cbbffb7ca985e`, selftest-nojj-pristine `1076f5f4b655a0d2`.

## Lane safety and tooling

- Lane access was read-only only: `git log/show/diff/config --get/symbolic-ref/status` and file reads.
- The lane `.git/index` mtime is 17:26:48, which is earlier than my `git status` (about 17:45). So there was no index write.
- I saw an unrelated ` M tools/registry.json` in the lane working copy (mtime 17:44:49). I did not cause it: every write of mine was confined to `$W`, with the fleet read-only under bwrap.
- No tools were installed or updated.

**Verdict: holds.** v2 re-run at 183f87b gives open=11/11 (exit 0), and neither v2 change makes a probe read closed for the landed tip; one calibration gap: binding lane.branch to `master` would also pass a fix that ignores the lane.branch value (M5).
