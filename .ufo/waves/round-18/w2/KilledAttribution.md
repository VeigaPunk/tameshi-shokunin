# KilledAttribution — round 18 w2 (FALSIFY C1): which selftest checks kill each KILLED mutant

Seat: `TameshiR18.KilledAttribution` (leaf, advisory). Read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
Target: kumitate-shokunin `scripts/sources-check.mjs` @ `0acb7752d19058b953ebbeba253b1e35f6548de5` (blob `6b57424f…`, sha256 `6a293a72…e258f`, 897 lines, 43497 bytes; matches spec line 2).
Evidence directory (mine): `.ufo/evidence/round-18/sources-check/attribution/` (50 evidence files plus `SHA256SUMS` covering them; `sha256sum -c` OK).

Axes: **attribution depth** (which checks fail, and how many independent detectors back each kill), **calibration** (does each predicted `selftest_case` fail; is the round's retained evidence enough to show it), **host robustness** (do kills depend on host `awk`).

## Method (commands, exits)

1. Scratch `W=/tmp/tameshi-r18w2-KilledAttribution-3xtmud`. Cloned the lane and checked out the read rev with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`. Siblings were symlinked under `$W/fleet`. The pinned blob came from `git -C kumitate-shokunin show 0acb7752:scripts/sources-check.mjs` (read-only). All six cited lane inputs have the same sha256 in the lane working tree and the read-rev clone: spec `c8d24cb4…`, suite `6e550d5a…` (both equal the registered values in `predictions.json:6-7`), predictions `5749a27a…`, `sweep/sweep.txt` `4ba2a595…`, `control.txt` `74061bdf…`, `tools/mutate-and-run.sh` `d22c4025…`.
2. Built the mutants with the `apply` helper copied byte-for-byte from `tools/mutate-and-run.sh:308-438` at the read rev. Output: `APPLY OK … old-count=1` for all five (`attribution/runner.log`). Each diff changes exactly one line (`attribution/diffs/<ID>.diff`).
3. Ran the registered suite string (`suite.txt`) once per mutant. Each run used `WORKDIR=$W/work` and `DEFECT_ID=<ID>`, captured stdout, stderr and the exit code to separate files, and ran inside `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind $W $W --unshare-net --die-with-parent … env -i PATH=<P> HOME=$W/home TMPDIR=$W/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C MUTANT=… WORKDIR=… DEFECT_ID=… timeout 300 bash -c "$(cat suite.txt)"`. Runners: `attribution/run-attribution.sh` (exit 0) and `attribution/run-noawk-rest.sh` (exit 0).
4. **awk hidden from PATH:** `$W/noawk-bin` is a symlink farm of every executable on the host PATH (first match wins, 4084 entries). It leaves out only the `*awk*` names `/usr/bin/awk /usr/bin/gawk /usr/bin/gawk-5.4.1 /usr/bin/gawkbug`. Probe through that PATH: `command -v awk` → absent; node, sh, grep, sort, uniq, wc, tr, mkdir, env, bash and timeout all resolve (`attribution/runner.log`). Ran the pristine control and K_ROWS with this PATH (`WORKDIR=$W/work-noawk`), then the other four killed mutants as an extra.
5. Cross-check: re-ran the read-rev tool itself, `bash tools/mutate-and-run.sh --target <pin> --defects <spec> --suite "$(cat suite.txt)" --workdir $W/toolsweep --tail 200`, in the same envelope. It exited 0 and printed `MUTATE: DONE (… killed=5 survived=5 inconclusive=0 kill-rate=50%)` (`attribution/toolsweep/toolsweep.txt:559`).

Host: node v24.21.0 (fnm), `/usr/bin/awk` = GNU Awk 5.4.1, `/usr/bin/grep` = GNU grep 3.12-modified, bash 5.3.20, bubblewrap 0.13.1, Linux 7.2.11-arch1-1.

## Result: failing checks per KILLED mutant (full stdout, host PATH)

| defect (site) | exit · tally | failing checks — `attribution/runs/<ID>.stdout:line` → detail | predicted `selftest_case` fails? | sole killer? |
|---|---|---|---|---|
| K_KIND (`sources-check.mjs:293`) | 1 · 43/46 | `:8` **TIER_ENUM: fixture reports kind with expected exit** → `exit=1 kinds=[KIND_ENUM]`; `:27` 1-3-space indented invalid registry rows report their field and tier findings → `empty=3 tier=0`; `:37` every declared finding kind fires in a fixture → `unfired=[TIER_ENUM]` | yes (`predictions.json:12`) | no (3) |
| K_EXIT (`:492`) | 1 · 44/46 | `:43` **invalid/missing option value uses usage exit 64** → `exit=65`; `:45` unknown option uses usage exit 64 → `exit=65` | yes (`predictions.json:22`) | no (2) |
| K_STRICT (`:434`) | 1 · 45/46 | `:40` **--strict promotes warnings to drift** → `exit=0 kinds=[USED_BY_ASYMMETRY] last=SOURCES_CHECK: CLEAN (rows=1 …)` | yes (`predictions.json:32`) | **yes** (1) |
| K_CLOSED (`:182`) | 1 · 44/46 | `:37` **SOURCES_MISSING: fail-closed exit 2** → `exit=2 last=SOURCES_CHECK: FAIL-CLOSED (READ_FAILED)`; `:40` every fail-closed arm fires in a fixture → `unfired=[SOURCES_MISSING]` | yes (`predictions.json:37`) | no (2) |
| K_ROWS (`:247`) | 1 · 41/46 | `:1` clean fixture returns CLEAN → `rows=2`; `:26` 1-3-space Markdown headings and rows are normalized; a 4-space row stays code → `rows=8`; `:43` --json prints one parseable contract object → `rows=2`; `:45` S1000 is accepted and counted → `rows=4`; `:50` **frozen awk census parity: rows, malformed, duplicate ids** → `node=8/1/1 awk=4/1/1` | yes (`predictions.json:42`) | no (5) |

The predicted case is in **bold**. Totals: **5/5 predicted `selftest_case`s fail.** The predicted case is the only failure for just **1/5** (K_STRICT). There are 13 failing checks in total; **8 of them are not named** in `selftest_case`. One of those 8, K_ROWS's clean-fixture check, is mentioned in that prediction's `reason` (`predictions.json:43`).

Source of each failing check in `kumitate-shokunin@0acb7752:scripts/sources-check.mjs`:

| check | where it is defined |
|---|---|
| clean fixture | `:587`, assertion `:589` |
| TIER_ENUM case | label template `:669`, case row `:614`, assertion `expectKind` `:579` |
| indented-valid rows | `:675`, assertion `:690` |
| indented-invalid rows | `:694`, assertion `:710` |
| kind coverage | `:784-785` |
| SOURCES_MISSING arm | `:793`, `:797`, assertion `:800` |
| fail-closed coverage | `:799`, `:803-804` |
| strict | `:807`, assertion `:809` |
| json | `:813`, assertion `:816` |
| S1000 | `:822`, assertion `:824` |
| usage exit 64 | `:827`/`:829` and `:831`/`:833` |
| awk parity | `:840`; awk gate `:853` → SKIP `:861`; compare `:866` |

All other checks PASS in every run. No host-PATH run produced a SKIP. Every run's stderr is 0 bytes.

## K_ROWS and host awk: the kill does NOT depend on awk (measured)

| run | exit | tally | parity line |
|---|---|---|---|
| K_ROWS, host PATH | 1 | 41/46 | `FAIL frozen awk census parity …` `node=8/1/1 awk=4/1/1` (`runs/K_ROWS.stdout:50-51`) |
| K_ROWS, awk hidden | **1** | **41/45**, VERDICT: FAIL | `SKIP frozen awk census parity: rows, malformed, duplicate ids: awk is unavailable` (`runs/K_ROWS.noawk.stdout:50`) |
| pristine control, awk hidden | 0 | 45/45, VERDICT: PASS | same SKIP (`runs/CONTROL.noawk.stdout:46-48`) |

The green control shows that the awk-hidden environment adds no failures of its own.

With awk hidden, K_ROWS is still killed by the same four row-pinning checks at the same stdout lines (`runs/K_ROWS.noawk.stdout:1,26,43,45`). That failing set equals the host failing set minus the parity check.

Extra measurement: the other four kills also hold with awk hidden. K_KIND 42/45, K_EXIT 43/45, K_STRICT 44/45 and K_CLOSED 43/45 all exit 1, and each has the same failing set as its host run (`runs/<ID>.noawk.*`). awk appears only in the parity script (`:853-856`). `runTool` spawns `process.execPath` (`:549`), so it does not depend on PATH.

## Calibration findings

1. **The predicted case for K_ROWS is the suite's only host-conditional check.** On a host without awk it prints SKIP, not FAIL, and is dropped from the denominator (46→45, `:876`). The verdict prediction still holds there, but the named case cannot be observed. Host-independent alternatives exist: `clean fixture returns CLEAN` (already in the `reason`) or `S1000 is accepted and counted`.
2. **The round's retained evidence did not show the per-check predictions.** `sweep/sweep.txt` keeps only the last 8 lines of output (`TAIL_N=8`). The predicted FAIL line is visible only for K_EXIT (`sweep.txt:39`) and K_ROWS (`sweep.txt:79`). The K_KIND (`sweep.txt:20-28`), K_STRICT (`:56-64`) and K_CLOSED (`:65-73`) tails contain only PASS lines and the tally. `sweep.txt:75` is a detail line cut off from its FAIL header; the header is `S1000 is accepted and counted`, at `runs/K_ROWS.stdout:45`. The `PREDICTION_COMPARISON` (`sweep.txt:117-130`) compares verdicts only. The full outputs existed only in the ephemeral `/tmp/tameshi-r4-2-run.ZIz4V0/evidence/` (`sweep.txt:111`). They are now kept in the lane under `attribution/runs/`.
3. **How many independent fixtures detect each kill:**

   | defect | fixtures that fail | aggregate checks that fail | note |
   |---|---|---|---|
   | K_ROWS | 5 (clean, indented-valid, json, s1000, parity); 4 without awk | — | |
   | K_EXIT | 2 (missing value, unknown option) | — | |
   | K_KIND | 2 (tier-enum case, indented-invalid rows) | kind coverage | |
   | K_CLOSED | 1 (SOURCES_MISSING arm) | fail-closed coverage | the aggregate follows from the arm's seen-set at `:799` |
   | K_STRICT | 1 | — | single point of detection |

   For K_STRICT: `reflip:` also runs with `--strict` (`:740`), but it expects `REJECTED_NO_FLIP`, which is already an error, so it cannot see promotion being lost. That explanation is [INFERENCE] from code; the PASS itself is measured in `runs/K_STRICT.stdout`.
4. **K_KIND is caught by the kind half of the assertion only.** The exit stays 1 (`runs/K_KIND.stdout:9`) because the mutated `KIND_ENUM` is still an error. The `reason` text ("asserts both the error exit and the TIER_ENUM kind") is accurate, but the exit half is not what catches this mutant.

## Reproducibility (three independent executions agree byte-for-byte)

- Full stdout sha256 for each killed mutant (`attribution.json` → `defects.<ID>`):
  - my direct run = my tool re-sweep's `evidence/<ID>.out` = w1's retained `/tmp/tameshi-r4-2-run.ZIz4V0/evidence/<ID>.out`;
  - K_KIND `7bdfc370…`, K_EXIT `188ccd81…`, K_STRICT `5711b9b6…`, K_CLOSED `9bb5ecfc…`, K_ROWS `0b7daae8…`.
- The last 8 lines of each full stdout equal the recorded `sweep.txt` tails exactly (control and all 5 killed).
- Mutant sha256 values are equal across my build, my tool re-sweep (`attribution/toolsweep/results.tsv`) and w1's `results.tsv`:
  - K_KIND `8d3e017c…`, K_EXIT `c416a4ea…`, K_STRICT `fa65a865…`, K_CLOSED `26ce5f93…`, K_ROWS `d2d18a6a…`.
- Control stdout sha256 is `e0880a5a…`, which equals `control.txt:6`. The tool re-sweep also prints every FAIL header (`toolsweep/toolsweep.txt:62,81,91,198,200,295,342,345,357,382,399,401,406`).

## Risks / limits

- I ran on a single host and checked only GNU awk; no mawk or busybox exists on it. No installs were needed, and none were attempted (pacman pause respected). **Tool installs: none.**
- The awk-hidden PATH is a symlink farm, not the original directories. The green awk-hidden control (45/45) bounds that difference.
- I am not a CR seat, so there are no `trace-inputs.py` receipts. The evidence is the raw stdout, stderr and exit files plus the runner scripts and logs, all covered by `SHA256SUMS`.
- The w1 `/tmp/tameshi-r4-2-run.ZIz4V0` directory is ephemeral. Its hashes are recorded in `attribution.json`.
- Lane safety: there were no git writes outside my `/tmp` clone. Every git call ran with `GIT_*` unset. Suite runs had the whole filesystem read-only except `$W`, with no network.

## Files written

- `.ufo/evidence/round-18/sources-check/attribution/`:
  - `attribution.json` `4de229dd…`
  - `run-attribution.sh` `73e36e94…`
  - `run-noawk-rest.sh` `192528d8…`
  - `runner.log` `583ad579…`
  - `runner-noawk-rest.log` `6460077a…`
  - `runs/{CONTROL,K_KIND,K_EXIT,K_STRICT,K_CLOSED,K_ROWS}{,.noawk}.{stdout,stderr,exit}`
  - `diffs/K_*.diff`
  - `toolsweep/{toolsweep.txt 4a3220f1…,toolsweep.exit,toolsweep.stderr,results.tsv f92e4ad7…}`
  - `SHA256SUMS` `e75c0533…`
- `.ufo/waves/round-18/w2/KilledAttribution.md` (this report).
- Scratch, kept so it can be inspected (outside the lane; safe to delete): `/tmp/tameshi-r18w2-KilledAttribution-3xtmud`. It holds the read-rev clone, the mutants under `work/`, `noawk-bin/` and the tool re-sweep under `toolsweep/`.

**Verdict: holds.** All 5 KILLED verdicts reproduce byte-for-byte. All 5 predicted `selftest_case`s are among the failing checks, though only K_STRICT's is the only failure. K_ROWS stays KILLED with awk hidden (41/45, four row-pinning checks), so its kill does not depend on host awk. Its predicted case is the one host-conditional check, and on an awk-less host it shows SKIP.
