# ScoutMisrootW2 — round 42 wave 2, misroot sweep (2026-10-25)

## Finding 1 — no tameshi round-42 misroots in the fleet repo

Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all`
(exit 0, 23 lines, 6 `??`). Lane checkout is not listed: `.gitignore:1:*-shokunin/` (`git check-ignore -v tameshi-shokunin`).

The untracked entries, after skipping `.scratch/` and `.ufo/state/`:

| Path | `grep -ci tameshi` | `grep -iE 'round[- ]?42\|r42'` |
|---|---|---|
| `.omp/mcp.json` | 0 | none |
| `.ufo/waves/round-24/w2/RevUnlandedResolution.md` | 0 | none |

Skipped: `.scratch/goal-20261025-hyaku-12h.md`, `.ufo/state/{kotoba,kotodama,revenger}.report-baseline`.
I also ran `git status --porcelain --ignored --untracked-files=all | grep -v '^.. tameshi-shokunin/' | grep -iE 'r(ound-?)?42|tameshi'`. Its only hit was the tracked, modified ` M .ufo/state/tameshi.report-baseline`, which is in the skipped `.ufo/state/` area and is not untracked. `ls -d /home/vgpnk/Projects/shokunin/.ufo/waves/round-42*` returned "No such file or directory".
Result: 0 untracked fleet files that name both tameshi and round 42. No wave-1 or wave-2 seat wrote into the fleet root.

## Finding 2 — /tmp/tameshi-r42* leftovers and their owners

Command: `ls -ld --time-style=+%FT%T /tmp/tameshi-r42*` (run at about 06:45–06:46).

### Wave 1: 21 directories named after their seat

Each of these seats has a report at `.ufo/waves/round-42/w1/<Seat>.md`:
CriticFixtureOverfit (`-r1`), CriticOracleSource, ExecC2Oracle (`-probes`), ExecRecheckCmds (`-snap`), ExecSupersedeDraft (`-clone`), ExecV4Tool (`-clone`), ReviewPitEntry (`-L1Tameshi42.ReviewPitEntry`), MutC1M11 (`-0`; `w1/MutC1M11.md:44` says it kept these on purpose as evidence), MutC2Oracle (`-`, a literal trailing dash; `w1/MutC2Oracle.md:74` names it as the scratch root), ReviewCjkGate, ReviewSurvivorGate, ScoutArgparse (`-snap`), ScoutCjkEntry (`-src`), ScoutConsiderthese, ScoutPitConcepts (`-src`), ScoutReceiptSweep, ScoutStrykerStates (`-20261025`), ScoutSurvivorEntry, ScribeEntryPit, ScribeEntryV4 (`-src`), ScribeRows (`-src`).

### Directories whose name does not give the owner

- **`/tmp/tameshi-r42/`** (06:44:16). It holds `build-w1.py`, `build-w2.py`, `dispatch-w1.json`, `dispatch-w2.json`, `c1ctl/`, `dry/` and `junk-tool.py`. Owner: L1Tameshi42, the orchestrator's staging area. It is not a seat misroot. [INFERENCE: drawn from the dispatch and build artifacts in it]
- **`/tmp/tameshi-r42-c1-mutantfix-{341c_lev,8duuu1rb,b_r4qeu8,gfzwhmi4,l0k9it09,lssoxd7j}`**: 6 directories, all at 06:27:51. Each is a git fixture (commit message `fixture`) holding `LOG.md`, `SCORECARD.md` and `corpus/`. Owner: **MutC1M8**. The `mutantfix` prefix appears in only one transcript, `~/.omp/agent/sessions/-Projects-shokunin/2026-10-25T06-15-52-413Z_01a171b3-…/L1Tameshi42/L1Tameshi42.MutC1M8.jsonl`, and no lane file at a21845f or 322b5cd contains it (`git grep mutantfix <rev>` printed nothing). `w1/MutC1M8.md:33` says its harness `/tmp/tameshi-r42-MutC1M8-w1/kill_fixture.py` was "run before cleanup". The `-w1` directory was removed, but the fixtures that harness created were not. **This is a cleanup leak.**
- **`/tmp/tameshi-r42-c1-selftest-{5zb3s5_u,7hjd2joz,85zmhc29,b_d_vfxa,dzchhrxn,g3_1tnmc,jcf0laef}`**: 7 directories, all at 06:18:24, before the wave-1 dispatch (`dispatch-w1.json` is stamped 06:25). The prefix comes from `.ufo/evidence/round-42/calibration/measure.py:268`. The current file deletes its scratch directory at `:337` with `shutil.rmtree(scratch, ignore_errors=True)` and nests fixture roots under scratch at `:271`. These directories instead hold fixture roots at the top level, so an earlier, pre-freeze version of the counter most likely left them. Owner: L1Tameshi42, the author of the counter. [INFERENCE: based on the timestamp and layout; no transcript names these suffixes.]

### Wave 2: `/tmp/tameshi-r42w2-*`, mostly sibling seats still running

ExecLiveShift (`-iXaW`), ExecV3V4Parity (`-out`), ExecV4Robustness (`-sweep`), LabRenamedBattery (`-r1`), MutProbeDepth (`-d0`…`-d8`, `-driver`, `-work-77v1h0rb`), ReopenS001 (the files `-live.html`, `-new.txt`, `-old.txt`), ReopenS155 (`-Vgax`), ReopenS156 (`-aWxf`), ReopenS157 (`-w51D`), ReopenS158 (`-x60W`), ReplayC2 (`-ywSd`), ReplayCensus (`-coll`), ReplayNoHarm (`-clone`), ReviewLessonGate (`-zenn`), ReviewRows (files `-src-{322b5cd,a21845f,c77c2b7}.md`), ScoutSiblingV4 (`-run`).
All of these were modified between 06:45 and 06:46, so they are live work. Judge them only after those seats return.

My own scratch files, `/tmp/r42w2-misroot-status.txt` and `/tmp/r42w2-misroot-w1.txt`, are outside the `tameshi-r42*` pattern and are deleted before I return.

Nothing was moved or deleted apart from my own scratch files, and nothing in the lane was edited except this report. No tools were installed.

Verdict: SURVIVES. No wave-1 or wave-2 seat misrooted files into the fleet repo. Two non-root cleanup leaks remain: MutC1M8's 6 `c1-mutantfix-*` fixtures and 7 `c1-selftest-*` directories from before dispatch.
