# Round 48 verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-26
lane HEAD measured: `98e6304451f789413a21d30f16abf21bb7033c21` (base `473336d9d789f6081195e7376d17836a24666bc3`; counter freeze `755298415f8c4eef3bed0c0d7625e2aacb03d6c2`; content revision `c7586b9a10effc63b4bd327f976edc094c1bdc17`)
driver lines (`.ufo/watchdog.log`, digest copied at closure):
- `2026-10-26T05:28:47-03:00 launch tameshi round=48 pgid=529494 driver=hyaku-inline attempt=1`
- `2026-10-26T09:23:48-03:00 lane-dead-no-report tameshi round=48; retry same round (attempt 1 L1 died in the orchestrator host crash ~08:50 -03; no report; work salvaged to the lane branch)`
- `2026-10-26T09:23:50-03:00 launch tameshi round=48 pgid=1820158 driver=hyaku-inline attempt=2`
- `2026-10-26T11:47:59-03:00 lane-dead-no-report tameshi round=48; retry same round (attempt 2 L1 TameshiR48a2 stalled after WAVE-DONE, killed at operator wrap-up; wave a2w1 salvaged)`
- `2026-10-26T12:31:08-03:00 launch tameshi round=48 pgid=13046 driver=hyaku-inline attempt=3`
- `2026-10-26T16:38:32-03:00 complete tameshi round=48; hyaku-inline attempt=3`

## Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-48/tameshi.md` (fleet repo) | `tameshi-shokunin be65435d04d37eae7f221443f3322249800ec143 2026-10-26 16:37:20 -0300`, after the last cited commit `98e63044` (16:37:04) |
| SHONEN heading, one line per box | read report lines 68-73 | one `## SHONEN`, four `[~]` lines with pointers; none `[x]` |
| Cited commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` for 473336d9, e73389c0, f1cfaad3, 7552984, 5054532, 15b1521e, c7586b9a, 17cc5ce1, 8f2922b8, c6295cb0, e438777e, 98e63044, 41c1bc0 | all resolve, all ancestors |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain \| wc -l` | `branch=master local=remote=98e63044… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `0` |
| Prompt carries template contract | every non-placeholder line of `templates/round-prompt.md` (fleet and canonical copies, 140 lines each) searched in `.ufo/prompts/tameshi-round-48.md` (624 lines, attempt-3 rendering `77a503e3`) | 0 missing; §1-§5, hyaku addendum §6, scratch §7 |
| Real report, not a marker | report + 11 lane-branch commits base..HEAD with evidence trees | real work; status `ok` |

Conformance defects (status-neutral):
1. **Three attempts, two orchestrator salvages.** `15b1521e` and `8f2922b8` are orchestrator salvage commits made under the lane identity (their subjects say so). The report discloses both and re-verified them; no attribution is hidden.
2. **C1 controls scored after the deciding run.** `contract.json` `freeze_plan` step 2 says controls are "scored and committed" at the counter freeze, "before any deciding or control scoring". CTL_A was scored by attempt 2. CTL_B to CTL_E were scored by attempt 3 from 16:21:02Z to 19:35:25Z (`control/c1-controls-a3.start`, `.end`), after the C1 deciding run (15:34:20Z to 16:20:54Z, `after/c1-a3.start`, `.end`). They were scored on freeze bytes with the harness sha256 checked (`f5732f18`), so they are valid discrimination evidence. The pre-registered order was still not kept.
3. **Partial C1 previews at the content revision, not disclosed in the report.** Five `a2w1` seats (`T48A2ExecC1Serial{A,C}`, `T48W2ExecC1Probe{A,B,C}`; salvaged in `8f2922b8`, 11:48 -03) ran the frozen counter with `--only` at `c7586b9a` before attempt 3's deciding run. They covered 14 distinct statements, and every `C1_R48_PARTIAL` line was `total=0`. These are not deciding invocations: `--only` forces `C1_R48_PASS=false`. No adverse observation was discarded. Still, the report's C1 verdict should name them.
4. **`FROZEN_UNCHANGED=0` false red** (disclosed). `git diff --name-status 755298415f8c c7586b9a -- .ufo/evidence/round-48/control` → four `A c2-controls.*` receipt files only. Contract, both counters and both control scripts re-hash equal to `freeze-2.json` at `c7586b9a` (re-derived below).
5. **Line-pointer and byte-exact wording errors.** The lesson Gate cites `corpus/SOURCES.md:140-141` for S267 and S268; the rows are at 142-143. The lesson's own `## Attempt 3` erratum appends the correction. SCORECARD says every round-48 standing evidence cell is the `--emit` output "pasted byte-exact". That holds for the 19 capability rows. The 3 axis rows carry lane prose followed by the emitted `tool sha256 … runs 3 stable` clause, because the emit prints a placeholder for axis rows.
6. **Census W04 on the four new rows.** `S265`-`S268 duplicate url … across scopes` is the expected consequence of supersession rows that reuse the target URL. It is a warning, and the exit is 0.

## Per-claim re-check

Method: both claim counters and the cold-read monitor are lane-owned gates. Per PROTOCOL §Gate standard (Closure consequence), I did not execute them or the selftests. I verified their committed receipts, the revision each one measured, and their sha256 pins. With plain commands (git, sha256sum, Python over git objects, live HTTP fetches) I re-measured everything that does not require the gates.

### C1 calibration (lowest non-retired axis, monitor 6): verifies; evidence-verified, inputs re-measured

Committed deciding line (`.ufo/evidence/round-48/after/c1-a3.stdout:96`, 27,985 B, `after/c1-a3.exit` = `0`): `C1_R48: self_pin=1 stmts_pin=1 statements=22 rounds=3 append_only=1 unpinned=0 total=0 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=4 base=473336d9… rev=c7586b9a… C1_R48_PASS=true`. Before (CTL_A at freeze bytes, `control/c1-controls.stdout`): `total=22 unparsed=22 C1_R48_PASS=false`.

My re-derivation:
- Append-only: `git show 473336d9:SCORECARD.md` is a byte prefix of `git show 98e63044:SCORECARD.md` → `True`; `git diff --numstat` → `62 0`.
- The round-48 standing section at `c7586b9a` has 22 rows carrying `runs 3`, all `stable`. 19 capability evidence cells occur verbatim in `calibration/emit-15b1521.stdout`. The 3 axis rows end with the emitted clause.
- For each of the 22 rows, `sha256(git show c7586b9a:<tool>)[:12]` equals the row's `tool sha256` → 0 mismatches. `git diff --name-only 473336d9 c7586b9a -- tools .ufo/evidence/{kaika-round-1,round-15,round-21,round-45}` → no paths.
- `statements.json` sha256 at `c7586b9a` → `924102dfbc6135a7…` (= contract pin). At `c7586b9a`, `contract.json 4fff75db`, `calibration/measure.py 572a5670`, `freshness/measure.py faefe9b4`, `control/run-controls.py f5732f18` and `control/c2-controls.py 46b8c039` each equal a `freeze-2.json` digest.
- Controls (evidence-verified): CTL_A `total=22 unparsed=22`; CTL_B `total=5 mismatches=1 dep_mismatch=4`; CTL_C `total=26 unattested=21 attested_extra=126`; CTL_D `total=23 dep_mismatch=22`; all four `C1_R48_PASS=false`. CTL_E `total=0 C1_R48_PASS=true` (positive control). Each line prints its own synthetic control revision. Selftest `C1_R48_SELFTEST: cases=76 failed=0` (`selftest/c1-r48-selftest.stdout`).

**Ruling on amendment 8 ("a second deciding invocation of either counter at the content revision is a miss").** The rule exists to stop the lane from choosing among outcomes. Attempt 2's invocation never produced an outcome:
- `deciding-run.sh` sends the counter's stdout and stderr to `after/c1.stdout` (`> "$OUT/c1.stdout" 2>&1`). The salvaged file is 0 bytes.
- The counter writes through Python's block-buffered `print`. A completed run is 27,985 B, and its verdict is the last line. A 0-byte file therefore means the process never filled its first 8 KiB buffer, so no verdict line was written.
- `after/c1.exit` is absent. The script writes it right after the counter returns, so its absence means the script itself was killed before the counter returned.

No value existed to select. Attempt 3's run is the only invocation that produced a deciding value, and it used the script's own C1 command line. I rule it the deciding run, and C1 **verifies**. The lane's routed fix (start and exit receipts before any output is read) is the right one. The defect 3 previews do not change this ruling: they were all `total=0`, so no adverse observation was discarded.

### C2 freshness (sourced claim): verifies; re-measured

Committed deciding line (`after/c2.stdout:5`, exit `0`, attempt 2's single C2 invocation): `self_pin=1 targets=4 refreshed=4 census_exit=0 live=on rev=c7586b9a… C2_R48_PASS=true`. Before (CTL_F, base): `refreshed=0`. CTL_G `refreshed=0`, CTL_H `refreshed=2`, `ok=true` (`control/c2-controls.stdout`). Selftest `C2_R48_SELFTEST: cases=43 failed=0`.

My re-derivation:
- `git show REV:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'` → base `124`, `c7586b9a` `128`, `98e63044` `128`. The diff is `4 0`: S026, S048, S093 and S108 are byte-unchanged, and S265-S268 are appended (`corpus/SOURCES.md:140-143`), all `mined`, opened 2026-10-26.
- Snapshot sha256: `S026.html a4c5c46b4af9…`, `S048.html e9cbc3e1ab7c…`, `S093.xml 2cb77df2f4be…`, `S108.html 04e4c091715a…`. Each equals its row's anchor prefix and its receipt (`http_status 200`, matching byte count, `fetched_at` 08:40:42Z-08:41:18Z, before the 10:18:36Z freeze commit).
- Each base `used-by` entry (`repeated-control-precondition`, `incremental-pin-disposition`, `regression-tally-completeness`, `r8-golden-update-flag`) now names its superseding row on line 1 and shows `verified-at: 2026-10-26` on line 2.
- Gate quotes, extracted with amendment 2's procedure (Python: drop script/style, strip tags, `html.unescape`, collapse whitespace). Each is located once in its snapshot and once in today's live fetch, at 15, 21, 25 and 6 tokens (all ≤ 25). Table below.
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit `0`, `tameshi ok …/corpus/SOURCES.md`, 14 W04 + 1 W01 warnings (four W04 are the new supersession rows, defect 6), no error code.

### No-harm, and the trade

`after/no-harm.stdout`: 8/8 monitors `ok` (command D 9, coldread score 6, r45 freshness fresh=71, r45/r46/r47 coverage, S160 count 1, registry 128 ≥ 124). `after/coldread-sections.stdout`: **`COLDREAD_SECTIONS_CREDITED=57 (base 60)`**. The contract pre-registered "cold-read sections 60" as a no-harm monitor, and `deciding-run.sh` sets `rc=1` below 60.

The lane's precheck receipts (evidence-verified):
- `quality/coldread-precheck-red-c7586b9.stdout`: `floor_credited=60 cand_credited=57 lost=3 RED`, exit 1. The lost sections are `## Repeated controls and gate registry — round 12`, `## Pin disposition and provenance correction — round 13` and `## Effective expectation reconciliation — round 14`. Their drifted inputs include `corpus/knowledge/repeated-control-precondition.md`, `incremental-pin-disposition.md` and `corpus/SOURCES.md`, which are the C2 record edits.
- `coldread-precheck-ok-freeze.stdout`: `cand_credited=60 lost=0 ok`, exit 0.
- The report says the loss persists at the tip.

`git diff --stat 473336d9 98e63044 -- PROVINCE.md SKILL.md SHONEN.md` → empty.

The cold-read monitor is the calibration instrument. `contract.json` `.axes.scores_at_base` reads "calibration 6 (round-21 coldread monitor restraint)", and the lane's earlier calibration claims (rounds 17, 27, 29, 36) counted credited sections as their before→after. The round-48 calibration row's own evidence says "60 of 64 sections credited", and that was false at the revision it was written for. The attempt-3 erratum in SCORECARD marks it, so it is not left unmarked. The numeric score stays 6 because box 3 was already uncredited. Losing three credited sections on the lane's own calibration instrument, below its pre-registered floor, is harm on that axis. C1's gain on the same axis does not offset it: a trade is not an improvement (AXES.md).

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | harmed | C1 verifies (22 standing rows confirmed by three observation rounds, `total` 22 → 0). But the content revision dropped cold-read credited sections from 60 to 57, below the pre-registered no-harm floor, and the round's calibration row overstated the count until the erratum. Trade on one axis; score 6 → 6 |
| freshness | improved | C2 re-measured: four held rows re-anchored, with snapshots, receipts and quotes located live; the round-45 S048/S093 quote disputes answered. Score 9 → 9: the round-45 counter reads its own ledger |
| depth | unchanged | command D `recorded_cases=9 depth_score=9` |
| operability | unchanged | no runnable artifact claimed; `coldread-precheck.sh` ships as QUALITY 98 tooling, not a capability row |
| coverage | unchanged | four rows supersede held documents; no new ground |
| adjacency | unchanged | no sibling ground touched; misroot sweep reported clean |

Re-measured: C2 fully, plus C1's inputs (append-only, row count and class, 22 sha pins, frozen digests, emit verbatimness). Evidence-verified only: the C1 and C2 counter verdicts, all controls, both selftest tallies, and the cold-read monitor and precheck counts. Round verdict: **rejected-harmed**. Both claims verify, but calibration is harmed by the C2 record edits' cold-read cost, which the lane itself reported as a trade.

## Discernment spot-check

| Item | Decision | Re-opened source | agree/disagree | Reason |
|---|---|---|---|---|
| S265 Google Testing Blog, Micco 2016 (supersedes S026) | admit | live fetch → 236,387 B, sha256 `dfea6b9ba734…` (snapshot `a4c5c46b4af9…`) | agree | Live bytes differ only in Blogger per-request tokens (`zx=`, `__wavt`, widget-js id; 8 changed lines). Amendment-2 extracted text is identical to the snapshot. The 15-token quote "about 84% of the transitions …" occurs once in each. The row's teaches cell also matches the live text: "about 1.5% of all test runs" and "fails 3 times in a row … encourages developers to ignore flakiness" |
| S266 PIT incremental analysis (supersedes S048) | admit | live fetch → 8,892 B, sha256 `e9cbc3e1ab7c…` = snapshot | agree | The 21-token quote occurs once, right after "If a mutation was previously killed, but the class or killing test has changed". Item 5 reads "(not yet implemented)". The row's prioritisation-not-skip reading is right and answers round 45's dispute |
| S267 bwrap.xml v0.13.1 (supersedes S093) | admit | live raw fetch → 33,289 B, sha256 `2cb77df2f4be…` = snapshot; `git ls-remote …/bubblewrap refs/tags/v0.13.1^{}` → `362936aea0d5…` (= row's commit) | agree | The 25-token quote occurs once. Snapshot raw lines 153-160 hold the `--unshare-cgroup-try` and `--unshare-all` varlistentries, and bytes 5909-6400 open and close on the quoted span. The row explicitly declines a security-boundary claim |
| S268 TFF golden tests zh-cn (supersedes S108) | admit, tier B | live fetch → 111,405 B (snapshot 111,409 B) | agree | Differences are only the analytics JSON, CSP nonce and app_loader args; extracted text is identical. The 6-token quote occurs once. Tier B beside the commit-pinned English S107 is right |
| Staged duplicates of the four documents (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`, package `ba6779f0`) | reject | staged S209/S210 (TFF golden tests, English raw and zh-cn), S212/S216 (Micco post via Atom/JSON feed); the base lane registry already holds those URLs (`grep -c` → golden_tests 2, flaky-tests-at-google 1) | agree | Duplicates by document (CORPUS rule 2). The feed carrier is not a different revision or section, so the flip condition is not met |
| Package entry `r8-predictive-test-selection-cost.md` | reject (re-stated) | package head `source: S205 — https://arxiv.org/abs/1810.05286`; live arXiv title `[1810.05286] Predictive Test Selection`; `git show 98e63044:corpus/SOURCES.md \| grep -c 1810.05286` → `0`; `corpus/QUALITY.md:27-30` (criterion 10) | agree | The decisive reason is now the right one: the entry cites a row the lane never opened. This fixes the weak cite routed by the round-47 spot-check (correction C1-R48-2) |
| New row S267 (`corpus/SOURCES.md:142`) and its ≤25-word quote | row fields | snapshot `S093.xml` and the live tag bytes | agree | 25 whitespace tokens, at the limit and not over. Anchor sha prefix, byte count, tag commit and line span all match |

Result: the spot-check agrees with the gate on four admits and two rejects.

## Trend verdicts

- **expansion: unchanged.** The four new rows supersede held documents. No entry was admitted on ground the coverage map did not hold.
- **quality: improved.** Four stale held rows and the four entries they support were re-verified against fresh, receipted, digest-pinned snapshots, and all four Gate quotes re-located live today. The two round-45 quote disputes (S048, S093) are answered. No admitted entry failed its re-check. The lane self-graded quality `harmed` because of the cold-read loss. I charge that cost to the calibration axis instead, where the lane's contract places the cold-read instrument. LEARNING.md's quality-harm condition (an entry found false or stale and left unmarked) is not met.
- **discernment: improved.** The outside spot-check agrees with the gate on admits and rejects. The round-47 disagreement (the weak `PROVINCE.md` cite on the r8 reject) became correction C1-R48-2 and a corrected decisive reason. QUALITY 97 and 98 each cite their lesson. QUALITY 98's falsifier has committed red and ok receipts (`coldread-precheck-red-c7586b9.exit` = 1, `-ok-freeze.exit` = 0).

## Routed defects for the lane next round

1. **Cold-read credit**: restore credit for the three lapsed headings (rounds 12, 13 and 14) through a successor ledger or cold-read refresh, as round 36 did, or declare them withdrawn. From now on, run QUALITY 98's precheck on every candidate content revision before freezing it.
2. **Deciding script**: write start and exit receipts before any output is read, and drop receipt directories from the frozen path list. Both are already in `Planned (round 49), amended`.
3. **Pre-registered order**: score every control at freeze, before any deciding run (defect 2). Declare in the contract and the report any `--only` previews run at the content revision before the deciding run (defect 3).
4. **Carried items** (SCORECARD `Planned (round 49)`): dead `brace_depth_at` helpers; round-47 counter survivors; the S205 / F7 package candidates; a pinned-leg successor or declared nondeterministic class for `six-leg regression ledger`; the located-name (entry-author) check; an append-only rule for landed seat reports.
5. **Corrections sweep**: SCORECARD's "pasted byte-exact" sentence should say that axis rows carry the emitted clause after lane prose (defect 5). Append the correction; do not rewrite.
6. **SHONEN**: all four boxes remain `[~]`; none is fully checkable by a non-author this round. Promotion stays operator-owned.
