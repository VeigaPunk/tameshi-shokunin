# MutateToolC

**Verdict: C06 and C08 were killed; C01–C05 and C07 survived both assigned detectors.** The six survivors are demonstrated tool-check gaps, not equivalent mutants: separate supplemental inputs distinguished each mutant from pristine and restored bytes. Supplemental results do not change the public-v1 verdicts. No C1 measurement verdict is issued here.

## Evidence and detector

Seat: `MutateToolC`. Scratch root, abbreviated `S` below: `/fast/scratch/hyaku/tameshi-r32-seats/MutateToolC`. All scratch-relative evidence paths below resolve under `S`.

Axes: behavioral mutation sensitivity; parsing-surface coverage; bounded operability; exact-byte isolation and restoration.

The isolated clone was detached at `a4f718138bdad20de741faeca57891645e5a64d9`. The pristine tool was copied to `S/tally-audit.py`. Each of eight mutants changes exactly one source line; `mutant-manifest.json:1-106` records the old/new lines and full hashes.

The public detector imported only the builder functions of `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py`, SHA-256 `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca`. For each seed 1–5, a fresh `random.Random(seed)` built `frozen_kill + generated_kill`, then `frozen_accept + generated_accept` using the same RNG, exactly as v1 orders those calls. Every seed supplied 18 must-kill and 8 must-accept copies: 130 executions per tool, including repeated frozen copies. See `preparation.json:1-22`, `fixtures.json`, and the v1 source at lines 82–168.

Expected behavior: selftest exits 0 and prints `TALLY_AUDIT_SELFTEST: 11/11 pass`; a must-kill copy exits 1 with a stdout line beginning `TALLY_AUDIT: FAIL`; a must-accept copy exits 0 with a stdout line beginning `TALLY_AUDIT: PASS`. Other combinations are misses. Each individual tool execution had a 300-second GNU timeout, a five-second kill grace, its own scratch cwd/HOME/TMPDIR, and captured stdout/stderr.

### Mutation table

“Kill/accept misses” are counts out of 90 must-kill and 40 must-accept executions across all five seeds. The source anchor is the named mutant file under `S`.

| Mutant | Single edit and source anchor | Own selftest: actual output, exit | Public v1 family misses | Verdict |
| --- | --- | --- | --- | --- |
| C01 | `regression_body`: remove whitespace allowance before `()`; `mutant-C01.py:99` | `11/11 pass`, 0 | None; kill/accept misses 0/0 | Survived |
| C02 | `tally_block`: require exactly two spaces before `local nlegs`; `mutant-C02.py:112` | `11/11 pass`, 0 | None; 0/0 | Survived |
| C03 | `leg_names`: scan the entire body instead of only the pre-tally head; `mutant-C03.py:120` | `11/11 pass`, 0 | None; 0/0 | Survived |
| C04 | `tally_loop`: replace whitespace splitting with `.split(' ')`; `mutant-C04.py:132` | `11/11 pass`, 0 | None; 0/0 | Survived |
| C05 | `harness_section`: search for the end marker from the file start, not the harness start; `mutant-C05.py:304` | `11/11 pass`, 0 | None; 0/0 | Survived |
| C06 | `main`: return 0 instead of the audit exit code; `mutant-C06.py:455` | `2/11 pass`, 1 | All nine kill families; 90/0 | Killed |
| C07 | `main`: return 1 instead of 2 on cannot-audit exceptions; `mutant-C07.py:452` | `11/11 pass`, 0 | None; 0/0 | Survived |
| C08 | `audit`: aggregate checks with `any` instead of `all`; `mutant-C08.py:374` | `3/11 pass`, 1 | All nine kill families; 90/0 | Killed |

For C06 and C08, the missed families were T08, N05, H03, H04, H05, N01, N02, N03, and D01, including their generated variants at every seed. C06 produced `OTHER` for all 90 must-kill copies: it retained the FAIL text but exited 0. C08 produced `ACCEPT` for all 90: it printed PASS and exited 0. No required public execution timed out; their exits were exclusively 0 or 1.

Selftest evidence for every row is `selftest-mutant-CNN.json:14-25`: exit at line 14, complete stdout at line 19, restoration hash at line 25. Public evidence is `public-mutant-CNN.json:3644-3655` for C01–C05/C07 and `public-mutant-C06.json:3644-3694` / `public-mutant-C08.json:3644-3694` for the killed mutants.

### Exact commands and observed outputs

All commands ran with cwd `S`; no source-lane gate or counter main ran.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/c
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/c checkout -q --detach a4f718138bdad20de741faeca57891645e5a64d9
cp c/tools/tally-audit.py tally-audit.py
python3 -B probe.py prepare
timeout --signal=TERM --kill-after=10s 1200 python3 -B probe.py public --tag baseline --jobs 4
timeout --signal=TERM --kill-after=10s 310 python3 -B probe.py selftest --tag baseline
timeout --signal=TERM --kill-after=10s 1500 python3 -B probe.py matrix --jobs 12
timeout --signal=TERM --kill-after=10s 1200 python3 -B probe.py selftests
timeout --signal=TERM --kill-after=10s 900 python3 -B witnesses.py
timeout --signal=TERM --kill-after=10s 600 python3 -B probe.py public --tag restored --jobs 8
timeout --signal=TERM --kill-after=10s 310 python3 -B probe.py selftest --tag restored
python3 -B receipt.py
```

The pristine and restored selftests both exited 0 with `TALLY_AUDIT_SELFTEST: 11/11 pass` (`selftest-baseline.json:13-19`, `selftest-restored.json:13-19`). Both full public controls matched all 130 expectations: kill misses 0, accept misses 0, exit counts `{0: 40, 1: 90}` (`public-baseline.json:3644-3655`, `public-restored.json:3644-3655`). Thus neither killed verdict rests on a failing baseline.

The selftest harness placed each mutant at `S/c/tools/tally-audit.py`, ran this exact child command, then restored the saved pristine bytes in a `finally` block:

```sh
timeout --signal=TERM --kill-after=5s 300 /usr/bin/python3 -I /fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/c/tools/tally-audit.py --selftest
```

Concrete public discriminator commands, recorded with their complete output in the corresponding public JSON results:

```sh
timeout --signal=TERM --kill-after=5s 300 /usr/bin/python3 -I /fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/mutant-C06.py --runner /fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/fixtures/seed-1/kill-00.sh
timeout --signal=TERM --kill-after=5s 300 /usr/bin/python3 -I /fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/mutant-C08.py --runner /fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/fixtures/seed-1/kill-00.sh
```

Both reported `CHECK runtime FAIL vectors=349 mismatched=12`. C06's final line was `TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)`, exit 0. C08's final line was `TALLY_AUDIT: PASS (static=pass runtime=fail harness=pass)`, exit 0. Those are detector failures, not successful kills of the runner copy.

## Inputs that kill the six survivors

These are supplemental discriminators only, not additions to either frozen counter or the wave's held-out set. Each was actually run on pristine, mutated, and restored bytes in a separate `witness-tools/CNN/tally-audit.py` slot. Their complete commands and outputs are in `witness-CNN.json:16-100`; mutant stdout is line 40, pristine stdout line 69, restored stdout line 98, and the supplemental verdict line 103.

| Survivor | Concrete input under `S/witnesses` | Pristine → mutant → restored exits | Mutant's actual final stdout |
| --- | --- | --- | --- |
| C01 | `accept-01.sh`: `run_regression () {`, with its awk start-marker regex also allowing that whitespace | 0 → 2 → 0 | `TALLY_AUDIT: SETUP (run_regression() not found)` |
| C02 | `accept-02.sh`: tab indentation before `local nlegs`, with both awk header-marker regexes adjusted to recognize that indentation | 0 → 2 → 0 | ``TALLY_AUDIT: SETUP (tally start `local nlegs=` not found)`` |
| C03 | `accept-03.sh`: capture `st_audit_helper=$?` after tally output, immediately before the successful exit | 0 → 1 → 0 | `TALLY_AUDIT: FAIL (static=fail runtime=fail harness=fail)` |
| C04 | `accept-04.sh`: two spaces between the first two tally operands | 0 → 2 → 0 | ``TALLY_AUDIT: SETUP (tally loop `for VAR in "$st_..." ...; do` not found)`` |
| C05 | `accept-05.sh`: an unused helper before `selftest()` contains `tblock=$tblock_full`, but no `local tblock` declaration | 0 → 2 → 0 | `TALLY_AUDIT: SETUP (harness block extraction line not found exactly once)` |
| C07 | Explicitly nonexistent `accept-07.sh` | 2 → 1 → 2 | `TALLY_AUDIT: SETUP ([Errno 2] No such file or directory: '/fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/witnesses/accept-07.sh')` |

For C01–C05, pristine and restored output was exactly:

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=349 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

For C07, pristine and restored both printed the same SETUP message shown in the table, correctly exiting 2. The `accept-07.sh` filename is only a local bookkeeping name: it does not exist and is not a must-accept runner fixture. Its supplemental detector explicitly expects SETUP/2, not PASS/0.

Example exact witness child command, run at all three byte stages:

```sh
timeout --signal=TERM --kill-after=5s 300 /usr/bin/python3 -I /fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/witness-tools/C05/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/MutateToolC/witnesses/accept-05.sh
```

The C01/C02 correlated awk changes are important: whitespace-only edits without those changes can invalidate the runner's own extraction harness. The reported inputs include those adjustments and were observed to pass the pristine audit. No full runner regression was invoked on these inputs.

## Hashes and restoration

Common pristine/before and restored SHA-256 for every mutation slot:

`9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef`

| Mutant | Mutated SHA-256 |
| --- | --- |
| C01 | `33b039f46271772e20b17fad739325708429a06b283f0defb92a66406ead35d1` |
| C02 | `a0ae6d3420e6511cc0a654c86c1970eacb7c450b2d29b33e1e636e143f8b0753` |
| C03 | `9f0c38d55dd6f45da4ace89ad70487781d93335f7a8c8e06bf1eb53850d76f59` |
| C04 | `d80a6624fb58de04fffae5790fb91cb8a7ebdda972f88b0f29a3f4e99b947f77` |
| C05 | `5c7fec2ee76db7f6f1be5cc546589abab8f6cafb50d6e940f1d0d696a6b9f49e` |
| C06 | `4d91f7dde0465450772b9cfe94b2905e59cd8449823d6c37671deeff913ee8f5` |
| C07 | `b76b9ddedcf7b8bb5574570e78eb08246757683acf388fcbac9d134f91e66467` |
| C08 | `4ba7e2d647b3882b7e6cfd8b705260006cca5c367d17f3cd97d8f717790de725` |

All eight selftest placements record exact-byte restoration (`selftest-restorations.json`; each individual receipt at lines 22–25). All six supplemental witness slots also record exact-byte restoration (`witness-CNN.json:2-13`). Standalone mutant files are retained as the requested probe artifacts; the clone's actual tool is restored.

Final aggregation observed `controls_match: true`, `final_slot_exact_pristine: true`, and identical pristine-copy/tool-slot hashes (`receipt.json:15-21`). The scratch runner's before and final SHA-256 was:

`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`

The final one-shot scoped process check found no remaining process with cwd under this seat (`receipt.json:595`). No process was killed manually. No tools were installed or updated. No production source, sibling scratch, production Git index, or frozen counter was edited; only this report was written outside the seat. Neither v2 counter main nor v1 counter main was invoked. No `--regression` or `--then-regression` run occurred.

## Smallest safe correction

Add the five observed pristine-passing parsing discriminators to a separately versioned tool selftest expansion, and add an independent CLI test asserting that an unreadable/missing runner produces SETUP with exit 2. Preserve the frozen v1/v2 contracts and tool bytes for this measurement. The observed gaps justify additional tests, not a changed contract or an integration decision; no production correction was applied by this seat.
