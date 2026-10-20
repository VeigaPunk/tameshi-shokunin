# ReviewSkillDiff — SKILL.md 183f87b..01d586dd (tameshi round 18, wave 2)

Seat: TameshiR18.ReviewSkillDiff (reviewer; advisory only — this report recommends, it does not judge).
Diff: `git -C <lane> diff 183f87b899e6cae46be98d251cbc87fb5118f6ca 01d586ddbc5fcd78659557c4e93a6ee8517b87d1 -- SKILL.md` (39+/10−, 7 hunks).
Page at read rev: sha256 `2e20e549…bdcdb0`, 1932 lines (verified).

Method: clone at `01d586dd` in `/tmp/tameshi-r18w2-ReviewSkillDiff-gl3db5wb/fleet/tameshi-shokunin` (`$C`), with sibling symlinks. Every command that runs lane code ran under the contract's bwrap envelope (`--ro-bind / /`, `--tmpfs /tmp`, `--bind $W $W`, `--unshare-net`, `env -i … GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`). Sibling repos were only read, with read-only git (`config --get`, `symbolic-ref -q`, `for-each-ref`, `ls-tree`, `show`, `log`, `GIT_OPTIONAL_LOCKS=0`). The only write outside `$W` is this report.
Tooling: no `lsp` device is mounted in this session, so caller and definition checks use literal `grep` and reads. Nothing was installed.

## Findings (by severity)

### F1 — Medium — registry-check timeout row overstates the closure: large finite `timeout_s` still crashes with the round-17 failure class
SKILL.md:1928 says: "`timeout_s` must be a finite positive number (`NaN`/`Infinity` literals refused at parse) → 2 naming the row". It sits in the section titled "routed-defect closure". The guard does refuse the two literals, `0`, negatives and `10^400`. But a finite value of 2147484 or more passes validation (`tools/registry-check.py:234-249`) and then crashes inside `proc.communicate(timeout=row["timeout_s"])` (`:686`).

- Run under bwrap: `python3 $C/tools/registry-check.py --root $W/rc-root --registry reg-<case>.json`. Each registry holds one row, argv `["true"]`:
  - `NaN` / `Infinity` → exit 2, `… rows[0].timeout_s (row 'nan-row'): non-finite JSON number NaN` (holds)
  - `0`, `-1`, `1` followed by 400 zeros → exit 2, `rows[0] ('zero-row').timeout_s must be a finite positive number` (holds)
  - `2147483` → exit 0, `ROW … held`
  - `2147484` and `3000000` → **exit 1**, traceback `OverflowError: timeout is too large` (selectors.py poll); no ROW line, no trailer
  - `1e308` → **exit 1**, traceback `OverflowError: cannot convert float infinity to integer`
- The base tool `183f87b:tools/registry-check.py` with `Infinity` fails the same way: exit 1, `OverflowError: cannot convert float infinity to integer` (with `NaN`: `ValueError`). That is the defect this row claims is closed. It survives for finite values, and the trigger is the most natural way to write "no timeout" once `Infinity` is refused.
- Exit 1 means "any differs" (`tools/registry-check.py:52`), so this crash cannot be told apart from a failed row by its exit code. The ruler cannot see it: P09 probes only the literals `("NaN", "Infinity")` (`.ufo/evidence/round-18/defect-probes.py:581`). The tool's own selftest stops at `1e999` (it parses to `inf`).
- Fix direction (for the L1): bound `timeout_s` to what `communicate()`/poll accepts (at most `INT_MAX` ms, i.e. under 2147483.648 s), or catch `OverflowError` → 2. Then reword the row.

### F2 — Medium — the jj-lane cite repair names the wrong function and splits `<branch>` from the reading's instrument
SKILL.md:1028-1029 now says: "`<branch>` = the `branch=` field of `../scripts/hyaku/jj-lane.sh state <repo>` (function `detect_branch()` by name; …)".

- `cmd_state` resolves `branch=` from `lane_branch_git` (git config `lane.branch`) **first**. `detect_branch` is only the fallback, and after it comes the sole master/main (`scripts/hyaku/jj-lane.sh:162-167`). The helper's own comment says detect_branch is "used ONLY by init for a first recording" (`:113`). The lane's corpus gives the right order: `corpus/knowledge/guard-kill-closure.md:49` says "`lane.branch`; then `detect_branch()` …".
- Demonstration on a /tmp clone, not a live repo: `lane.branch=master`, HEAD attached to `side`. `jj-lane.sh state` → `state branch=master …` (exit 0), while the helper's own `detect_branch` (sourced verbatim) → `side`. So the parenthetical sends a reader to a function whose result differs from the `branch=` field.
- The tool that takes this reading does neither. `tools/pin-disposition.py:42-46, :324-370` mirrors the v1 ladder (attached HEAD → origin/HEAD → master → main → first branch). It never reads `lane.branch` and still cites the stale anchor `jj-lane.sh … (:53-65)` (`:43`, `:325`). Those lines are now the `usage()` text; `detect_branch` sits at `:115-126` (fleet `14df5b9`, jj-lane v2). The corpus ER-jj2 notes (e.g. `corpus/knowledge/fleet-kill-rate-ledger.md:422`) define the resolver as `detect_branch` ("attached HEAD's branch, else origin/HEAD"). At 01d586dd the lane therefore carries three definitions of `<branch>`. They agree today for every leg repo: kumitate and kagi have no `lane.branch` and HEAD attached to master; tsukuroi, mado and tameshi have `lane.branch=master`, a detached HEAD and origin/HEAD → master.
- Running the command as the page now says:
  - (a) `../scripts/hyaku/jj-lane.sh` does not exist in the page's own clone layout (SKILL:1881-1883 symlinks only `*-shokunin`; `$W/fleet/scripts` is absent).
  - (b) `state` exits 1 unless `refs/remotes/origin/<branch>` exists (`jj-lane.sh:170-172`; shown: `jj-lane: refs/remotes/origin/side is not a 40-hex hash`, exit 1). It also exits 1 when no jj binary exists (`:40`), although the section says "no jj calls".
  - (c) `state` runs `git status --porcelain` (`:176`). By default that refreshes and writes the index (git-status(1) "BACKGROUND REFRESH"), so it is not the read-only probe pin-disposition.py promises ("never `status`", `tools/pin-disposition.py:83-85`).
- Fix direction: define `<branch>` once, as "`lane.branch`, else …", and cite `lane_branch_git` → `detect_branch` → master/main. Then align `tools/pin-disposition.py` (code and the `:53-65` cites), or say that it differs.

### F3 — Low — the seven→eight bump missed one count and broke its own cross-references
- SKILL.md:1762 still says "`js-round-gate` (`tools/mutate-and-run.sh --regression` → `cases=7`)", undated. At 01d586dd the command prints `REGRESSION: PASS (cases=8 passed=8; …)` (run below). The page's errata fixed exactly this class in round 16 (SKILL.md:1734 "receipt literal `cases=4` → `cases=N`, N per revision"). A cold reader of the round-16 section gets a wrong expectation.
- The round-18 edit replaced the round-16 dating at :10, :925 and :950 ("seven since round 16" → "eight since round 18"). At :1390-1391 it appended instead. As a result:
  - SKILL.md:1346 ("`:925-929`; dated there since round 16") and errata rows :1733, :1738 and :1739 now describe text that no longer exists at :925 and :10.
  - The replaced lines dropped the round-16 milestone that :1390-1391 keep.

### F4 — Low — "every descendant … is killed" drops the tool's documented limits
SKILL.md:1928 says: "every descendant of a row (including one that called `setsid`/`setpgid`) is killed at timeout and after the row exits".

- The tool's docstring says: "Descendants that change UID may become unreadable or unkillable, and start-time granularity leaves a same-tick PID-reuse residual" (`tools/registry-check.py:42-44`).
- Cleanup is bounded at 0.2 s TERM plus 0.5 s KILL (`:108-109`). Survivors are reported as `cleanup_error` with `held=false`; they are not killed (`:699-703`, `:719-722`).
- The behaviour the row claims holds for the selftest cases: `registry-check.py --selftest` exit 0, with `timeout-kills-setsid-pipe` and `timeout-kills-setpgid-pipe` PASS (survivor=False), `normal-exit-kills-double-fork` PASS and `bounded-pipe-drain` PASS. P10 is closed.
- Suggested wording: "every row-owned descendant visible in /proc is signalled; survivors after bounded cleanup fail the row (`cleanup_error`)". UID-changing descendants were not tested, because that needs sudo, which is out of bounds.

### F5 — Low — evidence-disposition row: one unconditional clause, one contradictory slogan, one omitted dependency
SKILL.md:1929.

- "a jj-colocated repo with no `lane.branch` → 2" holds only if HEAD is also detached. The code takes an attached branch before it checks `.jj` (`tools/evidence-disposition.py:466-490` before `:492-496`). The selftest fixture forces `git checkout --detach` to get the refusal (`:2251`).
- With jj 0.45.1, `jj git init --colocate` on a repo with HEAD on master leaves HEAD **attached**. Observed: `after-init: refs/heads/master`, `after-readonly-jj: refs/heads/master`, `after-jj-new: detached`. A freshly colocated, unbound workspace therefore anchors on `refs/heads/master` and does not exit 2. The tool's own doc wording is right: "An unbound jj workspace is refused" (`:51-53`).
- "Never bare `HEAD`" contradicts the sentence before it. The detached non-jj path returns `("HEAD", commit)` (`:525`), guarded by `for-each-ref --contains` (`:503-524`). "Never unguarded HEAD" is what the code does.
- "unchanged CLI" is true for argv, but `--selftest` now needs `jj` on PATH (docstring `:121`). Without jj it exits 1: `SELFTEST: FAIL (3/63 failed: v2-jj-prebookmark-branch-tip, v2-jj-branch-tip, v2-jj-without-lane-branch …)`. With jj it exits 0 (63/63).

### F6 — Low — survivor table: S_FILE_READ is mis-described, and non-equivalence is still pending
SKILL.md:1921 puts S_FILE_READ under "detail text and non-row counters".

- The entry says the gap is different: "the per-entry read arm is not reached" and its anchor lines are zero-statement under c8 (`corpus/knowledge/mutation-case-kumitate-sources-check.md:124-125, :142-144`). That is an unexercised fail-closed path, not detail text.
- All five survivors are "non-equivalence PENDING" (entry §4, `:150-163`), yet the table routes all five to kumitate as fixes without saying so.

### F7 — Nit — `--carry` is not quite "verbatim"
SKILL.md:1932 says `--carry` "copies prior entries verbatim".

- `load_carry` copies each entry and sets or overwrites `carried_from` (`.ufo/evidence/round-18/coldread/assemble.py`, `entry["carried_from"] = path`).
- With `--carry`, `_finish` also switches the exit-0 coverage basis to section sha256 against `HEAD:SKILL.md` (`carry_coverage_basis`, printed as "informational (measure.py is credit authority)"). The recipe step at SKILL.md:1888 does not mention this change.

### F8 — Nit — the "Entry:" pointer leads to stale status text
SKILL.md:1913 points to the entry. The entry's recheck line says the leg is "not yet installed at base" (`mutation-case-kumitate-sources-check.md:3`). Its §5 says "Status: the leg is not installed at base … An installed-runner receipt is pending the L1 install" (`:174-183`). At 01d586dd the leg is installed and the replay passes (below). This is outside the SKILL diff, but the new section's pointer leads there.

## Statements checked and found true at 01d586dd

| SKILL.md line(s) | Claim | Evidence |
|---|---|---|
| 10, 925, 950, 1390-1391 | eight recorded / eight legs since round 18; N=8 | `git ls-tree R corpus/knowledge/` → 8 `mutation-case-*.md` (7 at 183f87b). `bash tools/mutate-and-run.sh --regression` exit 0 in 196.8 s: `REGRESSION_EXPECT …js-sources-check=5/10`, `REGRESSION_CASE js-sources-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`, `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`, `REGRESSION_TOOL … sha256=d22c4025…`, all 8 `REGRESSION_PIN` lines present |
| 1029 | "line anchors into the helper move" | jj-lane.sh v2 (fleet `14df5b9`). Current `:53-65` is `usage()` text; `detect_branch` is at `:115-126` |
| 1885 | `tools/trace-inputs.py` has the same CLI and receipt as the round-17 copy | `diff -u` r17 copy vs tools copy: only the docstring line 1 and three added selftest cases differ. The r17 copy's sha `521be955…` is identical at 183f87b and R |
| 1888 | `assemble.py --reports <dir> --carry <prior ledger> --out <ledger>` | `--help`: `[--reports …] [--carry PATH]`. `--selftest` exit 0, `SELFTEST: 80/80 pass` (carry checks ok) |
| 1890, 1932 | round-18 `measure.py --rev REV` → `coldread.box3_full_page`, `calibration_restraint_score`; default ledger round-18; `--explain` | `measure.py --rev R` exit 0: `box3_full_page=False`, `calibration_restraint_score=6`, reasons `{'no-ledger': 60}`. Source: `DEFAULT_LEDGER_PATH='.ufo/evidence/round-18/coldread/ledger.json'`, `--explain` argument |
| 1907-1909 | pin rev/sha/897 lines/100755; leg `js-sources-check` 5/10, 10/10 | kumitate `ls-tree 0acb7752 …` → `100755 blob 6b57424f…`; `show | sha256sum` → `6a293a72…258f`; `wc -l` → 897. `predictions.json` (unchanged since 93d22aa, sha `5749a27a…`) vs `TABLE_SOURCESCHECK`: 10/10. Sweep `PREDICTION_MATCH: 10/10`, `MEASURED_KILL_RATE: 5/10` |
| 1910 | spec and predictions committed in 93d22aa before any mutant ran | 93d22aa at 2026-10-20T19:40:21Z adds spec, predictions, suite and control. Sweep `MUTATE_DATE: 2026-10-20T19:41:29Z`. Spec and predictions are byte-unchanged since then, and the spec is embedded verbatim in `tools/mutate-and-run.sh` (diff empty). That no earlier mutant ran is [INFERENCE] from the receipts |
| 1910-1911 | suite = hermetic `env -i` form of case 7 | `.ufo/evidence/round-18/sources-check/suite.txt` is byte-identical to `.ufo/evidence/round-16/round-gate/suite.txt` |
| 1911-1912 | eight pristine controls byte-identical | `control/repeat/run-1..8.stdout` all sha `e0880a5a…`, exits `0`×8; `REPEAT_COMPARE identical=yes runs=8` |
| 1920 | DRIFT verdict line | `sources-check.mjs:483` emits `SOURCES_CHECK: DRIFT (${driftKinds.join(',')})` |
| 1927 | defect-probes exits, output line, closed rule, bwrap | Code `:21`, `:383-392`, `:956-957`, `:1028-1081`, `:191-203`. `--selftest` exit 0 `SELFTEST: PASS (6 cases)`. `--rev 01d586dd…` exit 0 in 49.9 s → `DEFECT_PROBES: open=0 closed=11 total=11` (P01-P07 `pristine_exit=0 mutant_exit=1`) |
| 1928 | NaN/Infinity refused at parse, exit 2 naming the row; pipe drain bounded; setsid/setpgid killed | See F1 and F4 for the probes. `PIPE_DRAIN_TIMEOUT_S = 0.5` (`:110`). Selftest exit 0. CLI unchanged (no argv/USAGE hunk in the diff) |
| 1929 | one anchor for G2 and G3; detached non-jj clone anchors only when contained | `run_mode` resolves the anchor once and passes it to both guards. `:498-525`. On the clone (detached, no `.jj`, `refs/heads/master` contains R), `--dispositions .ufo/evidence/round-18/dispositions.json` exit 0 |
| 1930 | GIT_* scrub for every git child; round-13 bytes read via dispositions.json at 4acc607; round-17 manifests superseded | Every subprocess site uses `git_clean_env`/`sweep_env` (`bash-witness-study.py:347-350, :614-616, :1257-1277`). `selftest` exit 0 with both GIT_DIR/GIT_WORK_TREE canary checks ok. Disposition run prints `HISTORICAL tools/bash-witness-study.py rev=4acc607d… sha256=49e9e5e2…`. Round-17 `dispositions.json` and `-before.json` now exit 2 (`expected_input_digest_mismatch … bash-witness-study.py`); registry rows `evidence-disposition-round17*` are `superseded_by …round18*` |
| 1931 | trace-inputs selftest kills the three guard removals | Pristine `--selftest` exit 0 (`SELFTEST: 30/30`). O_RDWR removed → exit 1 (`FAIL rdwr-open-excluded`). Pycache prefix `"."` → exit 1 (`FAIL pycache-prefix-private`). Root-execve requirement removed → exit 1 (`FAIL root-exec-required`). The prefix deleted outright also fails (28/30) |

## Commands executed (exit, key output)

All ran from `$C` under bwrap unless marked.

- `git diff 183f87b 01d586dd -- SKILL.md` (lane, read-only) → 0
- `git show R:SKILL.md | sha256sum; wc -l` → `2e20e549…`, 1932
- `bash tools/mutate-and-run.sh --regression` → 0 (lines quoted above)
- `python3 tools/trace-inputs.py --selftest`: pristine → 0; mutants P05/P06/P06b/P07 → 1; P07b (count any pid's execve) → 0
- `python3 tools/registry-check.py --root $W/rc-root --registry …` (10 one-row registries) → 2,2,2,2,2,0,**1**,**1**,0,**1**. Same check with `183f87b:tools/registry-check.py` on Infinity and NaN → 1,1
- `python3 tools/registry-check.py --selftest` → 0
- `python3 tools/evidence-disposition.py --root . --dispositions <r18|r17|r17-before|r18-before>` → 0 / 2 / 2 / 1
- `python3 tools/evidence-disposition.py --selftest` → 0 (63/63); with PATH without jj → 1 (3/63 failed)
- jj colocate HEAD probe (`git init`; `jj git init --colocate`; `jj new`) in `$W/jjtest` → 0 (output above)
- `jj-lane.sh state <clone>` with `lane.branch=master`, HEAD on `side` → 0 `branch=master`. Sourced `detect_branch <clone>` → `side`. `state` without `lane.branch` → 1
- `python3 .ufo/evidence/round-18/measure.py --rev R` → 0
- `python3 .ufo/evidence/round-18/coldread/assemble.py --help` → 0; `--selftest` → 0 (80/80)
- `python3 .ufo/evidence/round-18/defect-probes.py --selftest` → 0; `--rev R` → 0 (`open=0 closed=11 total=11`)
- `python3 tools/bash-witness-study.py selftest` → 0. My first try used `--selftest`, which is the wrong form, and got 64 (usage). This was my error; the row says the CLI is unchanged
- Read-only facts, outside bwrap: kumitate `ls-tree`/`show`; leg repos `config --get lane.branch`, `symbolic-ref -q`, `for-each-ref` with `GIT_OPTIONAL_LOCKS=0`; fleet `git log -- scripts/hyaku/jj-lane.sh`; `man git-status` (BACKGROUND REFRESH)

## Residual risk

- The registry row `mutate-and-run-regression` pins only `"REGRESSION: PASS"` (`tools/registry.json:462-481`). A run that silently dropped leg 8 (`cases=7 passed=7`) would still hold. Only the runner's selftest leg-count check (want 8) guards the count.
- Near-equivalent trace-inputs mutant P07b survives (selftest 30/30). It credits a successful execve by any traced pid as the root's. Under `strace -f` the root is the only process that can exec first, so this is not a defect, but the "root" qualifier itself is not pinned.
- F1's crash also affects any finite `timeout_s` at or above about 24.86 days. No current registry row comes close (largest 900 s), so present registry results are unaffected.
- The three `<branch>` definitions (F2) agree for every current leg repo. They diverge only if `lane.branch` differs from the attached or origin/HEAD branch.

## Verification gaps

- I did not run the full registry (32/32 claim) or SCORECARD command D; both are outside this diff.
- I did not test UID-changing descendants (needs sudo; out of bounds).
- I did not run `pin-disposition.py`. F2's divergence is shown from source and a jj-lane run, not from the instrument's output.
- "No mutant ran before 93d22aa" rests on the receipts' timestamps [INFERENCE].

Verdict: partial — the count bumps, replay, pin facts, recipe repoint and most registry rows hold at 01d586dd, but the timeout row overstates the NaN/Infinity closure (finite `timeout_s` ≥ 2147484 still crashes with exit 1), the jj-lane cite repair names the wrong resolver and disagrees with `pin-disposition.py`, and `:1762 cases=7` was missed.
