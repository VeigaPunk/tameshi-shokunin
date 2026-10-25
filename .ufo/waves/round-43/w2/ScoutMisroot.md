# ScoutMisroot — fleet-root misroot sweep for tameshi round 43

Seat: `L1Tameshi43.ScoutMisroot`, round 43 wave 2 (falsify), axis **calibration**, milestone **fleet-root misroot**.
Read-only throughout: no file created, moved, or deleted outside this report; no mutating `git`/`jj`; no package installed. `.ufo/state/` and `.scratch/` were **read only** (`cat`, `stat`, `sha256sum`, read-only `git diff`), never written.

**Verdict: no tameshi round-43 seat artifact is misrooted at the fleet root — but the check is only valid for the instant it was taken, and the fleet-root status cannot see the lane at all.** Two *foreign* lane misroots occupy the same surface; tameshi's own fleet-side round-43 report is **missing** while its watchdog baseline already records round 43.

## 1. Exact command and snapshots

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all
```

Captured twice, 24 entries each (17 tracked-modified + 7 untracked):

- 2026-10-25T08:05:00-03:00 (first capture)
- 2026-10-25T08:06:45-03:00 (re-run; byte-identical to the first capture — verified with `diff`)

`-uall` is mandatory: plain `--porcelain` collapses both stray directories into `?? .ufo/waves/round-69/` and `?? .ufo/waves/round-24/`, which read as ordinary orchestrator wave directories. Only the file-level view exposes the seat notes.

## 2. Every untracked file, classified

| # | path | size / mtime | writer | tameshi / round-43 content |
|---|---|---|---|---|
| 1 | `.omp/mcp.json` | 285 B, 10-24 18:07 | tooling config (oh-my-pi MCP schema, server `rea`) | none (`grep -niE 'tameshi'` → 0) |
| 2 | `.scratch/goal-20261025-hyaku-12h.md` | 4863 B, 10-25 07:45 | **orchestrator** — line 1 self-declares `<!-- ORCHESTRATOR-OWNED run state (hyaku run 6). Not a misroot … -->` | **names tameshi, not round 43** — lines 55 and 64, see §3 |
| 3 | `.ufo/state/kotoba.report-baseline` | 69 B, 07:00 | watchdog (`scripts/shokunin-watchdog.sh:116-138`), content `69 e3b0c442…` | none |
| 4 | `.ufo/state/kotodama.report-baseline` | 70 B, 06:59 | watchdog, `70 e3b0c442…` | none |
| 5 | `.ufo/state/revenger.report-baseline` | 68 B, 06:56 | watchdog, `69 e3b0c442…` | none |
| 6 | `.ufo/waves/round-24/w2/RevUnlandedResolution.md` | 15891 B, 05:55:04 | **tabi round-24 wave-2 reviewer seat** (`L1Tabi24.RevUnlandedResolution`, line 3; line 6 `Lane root …/tabi-shokunin`) | none — no `tameshi`/`round 43` string |
| 7 | `.ufo/waves/round-69/w1/ScoutAmp.md` | 10163 B, 07:16:36 | **kotoba round-69 wave-1 scout seat** (`Lane measured: HEAD a238989a…`, line 13 → kotoba commit) | none — no `tameshi`/`round 43` string |

Files 3–5 are the documented driver format `<round> <sha256-of-report-bytes>`, one line, written by `record_report_baseline()` at `scripts/shokunin-watchdog.sh:115-138`; `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` is the empty-stream digest (`report_digest()`, same file, lines 108-114), i.e. "report absent". Their mtimes (06:56/06:59/07:00) chain to the `launch …` lines in `.ufo/watchdog.log` (revenger 06:56:04, kotodama/others 07:00), not to any seat.

**Zero paths under `.ufo/waves/round-43/` and zero paths under `.ufo/reports/round-43/` appear as untracked.** `ls .ufo/waves/round-43` → `No such file or directory`.

## 3. Files whose content names tameshi (and the one that names round 43)

Only one *untracked* file names tameshi, plus one *tracked-modified* file names tameshi round 43 outright:

1. **`.scratch/goal-20261025-hyaku-12h.md`** (untracked, orchestrator-owned) — names tameshi twice, never round 43:
   - line 55: `… closed-round scratch (r30fx-*, tameshi-r41-*, mori-r43-*, …)` — a /tmp cleanup note; the `r43` there is **mori's**, not tameshi's.
   - line 64: rotation list `… kake, tameshi, mori.` — lane scheduling, no round.
   - **What the L1 must do: leave it.** It is not a seat note, not r43 evidence, and not deletable (the file's own header forbids lane/seat edits; line ~47 records an earlier incident where an unidentified seat deleted the tracked `.scratch/` tree at 04:10). Do not quote it as evidence about the wave.
2. **`.ufo/state/tameshi.report-baseline`** (tracked, **M**, driver-owned) — content is exactly `43 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; the diff is `23` → `43`. This is the watchdog's launch gate for **tameshi round 43**, set at 07:34:37, recording that `.ufo/reports/round-43/tameshi.md` was absent (empty digest) when the round started. Not written by a seat; must be left un-staged.
3. **`.ufo/watchdog.log`** (tracked, **M**) — `:1319  2026-10-25T07:34:37-03:00 launch tameshi round=43 pgid=280132 driver=hyaku-inline attempt=1`. The authoritative proof that tameshi round 43 is this run's round. Driver log; never a seat deliverable.
4. `.ufo/reports/round-43/` (tracked directory) contains `chousa.md kake.md kotodama.md kumitate.md mori.md` — **no `tameshi.md`**. Round 42 has one (`.ufo/reports/round-42/tameshi.md`, 13097 B, written 06:55 today, `## SHONEN` at line 55), and rounds 40–42 each have one. So the fleet-side tameshi round-43 report is the **one missing lane report** of this round.

**Consequence the L1 must carry into its closure:** once the round-43 report is written at the fleet path, `git status -uall` will legitimately show `?? .ufo/reports/round-43/tameshi.md`. That is **not** a misroot — the directory is tracked and its five sibling lane reports are tracked. A misroot is `?? .ufo/waves/round-43/…`, which is a *tracked-waves* path that does not exist. Do not conflate the two. Note also the commit history for the landing zone: `git log --oneline -3 -- .ufo/reports/round-43/` → `0c9e9999 round-43: mori report (hyaku sweep: L1 returned without committing; attribution defect)`, `484e6eff … (operator stop sweep)`, `15b12848 round-43: chousa report` — two of three round-43 reports were swept in after the L1 failed to commit, recorded as an attribution defect. Leaving the file uncommitted repeats that defect.

## 4. The two foreign misroots — confirmed, not tameshi, do not touch

Both are already filed in `revenger-shokunin/.ufo/waves/round-69/R69MisrootSweep.md`; I re-derived them independently and the sha256 values match that report byte-for-byte:

```
d83b22dfeba7674f2f26bca11c6a92200bccf208a2eec429d623daba0a54cff1  .ufo/waves/round-69/w1/ScoutAmp.md
5f09b9b3b87b96cec62021ac3a605028765f9053b64f7b0b016ebfc6b3499aef  .ufo/waves/round-24/w2/RevUnlandedResolution.md
```

- Ownership proven by content, and the lane copies do **not** exist: `find kotoba-shokunin -name 'ScoutAmp*'` → empty; `find tabi-shokunin -name 'RevUnlandedResolution*'` → empty; `kotoba-shokunin/.ufo/waves/round-69/w1/` has no `*Amp*` entry and its r69 wave completed at 07:34:22 (`watchdog.log:1318 complete kotoba round=69`) **without** ever landing the seat; tabi's `w2/` holds 32 `.md` reports against 33 spec items, the single miss being `RevUnlandedResolution` (verified: `python3` over `w2-spec.json` + `ls`). The single copy of each deliverable is the fleet-root one.
- Shape: `round-24` dir, `w2` dir and file all share mtime+ctime `05:55:04.010735389`; for kotoba, `round-69` = `07:16:36.268740223` and the file = the same, but `round-69/w1` is `07:19:36.283409737` — the stray directory had an entry added/removed 3 minutes later while the file bytes stayed fixed. `[INFERENCE]` a temp write/rename in the stray directory, not a content edit; the hash above is the current state.
- **What the L1 must do: nothing to them.** Moving or deleting them is a git-writing action outside a seat's scope and would destroy the only copy of two other lanes' deliverables. Record them in the report as foreign misroots with the line above and let the orchestrator/owning lane take the move (`R69MisrootSweep.md:§6` already prescribes the triage and the `MANIFEST.json` dead-seat correction for the tabi case). In particular: do not use their presence as evidence about tameshi, and do not subtract them from any tameshi count.

## 5. Calibration checks an L1 misroot sweep usually gets wrong

1. **`git -C fleet status` is blind to the lane by design.** `.gitignore:1` is `*-shokunin/` (`git check-ignore -v tameshi-shokunin/.ufo/waves/round-43/w2/swarm-registry.json` → `.gitignore:1:*-shokunin/`), and `git ls-files tameshi-shokunin | wc -l` → `0`. A clean fleet status therefore **says nothing** about whether the 34 wave-2 seats wrote into `tameshi-shokunin/.ufo/waves/round-43/w2/`. It only detects the misroot class (a seat resolving a lane-relative path against the fleet root), because those files land outside the ignored lane directory. Both halves must be checked; neither substitutes for the other.
2. **A snapshot is not a closure.** The wave-2 dispatch fired at `08:03` (`tameshi-shokunin/.ufo/waves/round-43/dispatch-w2.json` mtime, `counts.spawn: 34`), and at `08:05:00` the lane's `w2/` held **only `swarm-registry.json`** — 0 of 34 seat reports. My clean fleet status was taken two minutes into a live wave. `R69MisrootSweep.md` documents exactly this trap: its first status snapshot did not contain `ScoutAmp.md`; the file appeared 3 minutes later, from the dispatcher, mid-sweep. Re-run the command at closure, not now.
3. **The injurious sentence is present verbatim in this wave's own spec.** `tameshi-shokunin/.ufo/waves/round-43/spec-w2.json` `context` contains: ``Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/tameshi-shokunin — write it at /home/vgpnk/Projects/shokunin/tameshi-shokunin/<that path>.`` together with `Absolute paths only: seat tools start at the FLEET root.` and a lane-relative `reportDir` of `.ufo/waves/round-43/w2`. That is the precise combination that produced both live misroots: a seat with cwd at the fleet root resolving `.ufo/waves/round-43/w2/<Name>.md` creates `.ufo/waves/round-43/w2/` at the fleet root. So the tameshi r43 hazard is **live, not hypothetical** — it simply had not fired yet at 08:05.
4. **Driver state is not seat output.** `.ufo/state/*.report-baseline` (14 M + 3 ??) is watchdog state; `scripts/hyaku/hyaku.env` and `scripts/hyaku/lane-addendum.md` are orchestrator config/instruction (no `tameshi` string in either). None of the 24 entries is a tameshi seat note; none may be staged into a lane commit or cited as wave output.

## 6. What the L1 must do

1. Record in the round-43 report: at 08:05:00/08:06:45 fleet root, **0** tameshi round-43 seat misroots, **0** `?? .ufo/waves/round-43/`, and **2** foreign misroots (`ScoutAmp.md` kotoba r69 w1, `RevUnlandedResolution.md` tabi r24 w2) left in place per `R69MisrootSweep.md`; both hashes above.
2. **Re-run `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` at closure** and fail the round if any `.ufo/waves/round-43/` path appears. Use `-uall`; assert on the path prefix, not on a count, because the driver churns `.ufo/state/` and `.ufo/watchdog.log` continuously.
3. Do **not** cite the `.scratch` goal file or the two foreign notes as evidence about tameshi's wave, and do not delete or move any of the three.
4. Write and **commit** `.ufo/reports/round-43/tameshi.md` in the fleet repo (with a `SHONEN` heading — `report_of()` at `scripts/shokunin-watchdog.sh:146-160` requires it, plus `MIN_REPORT_BYTES=400`), because every peer lane at round 43 has one, rounds 40–42 have one, and `.ufo/state/tameshi.report-baseline` already reads `43 <empty>`; leaving it absent is the documented attribution defect (`0c9e9999`, `484e6eff`). Expect and allow `?? .ufo/reports/round-43/tameshi.md` in the closure status — that is the deliverable, not a misroot.

## 7. Limits

- Snapshot scope only (08:05:00 / 08:06:45); the set can grow while a sweep runs. `/tmp` was not swept (out of item scope). `--ignored` was expanded once (`--untracked-files=all --ignored=matching`): its only tameshi/round-43 hits are `!! tameshi-shokunin/` (the whole lane, `.gitignore:1`) and ` M .ufo/state/tameshi.report-baseline`; no tameshi-named or round-43 path hides outside the lane directory.
- Tooling: nothing installed or upgraded.

## Reproduction

```
git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all | tee /tmp/r43-status-now.txt | wc -l      # 24
grep -E 'round-43|tameshi' /tmp/r43-status-now.txt          # only ' M .ufo/state/tameshi.report-baseline'
sha256sum .ufo/waves/round-69/w1/ScoutAmp.md .ufo/waves/round-24/w2/RevUnlandedResolution.md
cat .ufo/state/tameshi.report-baseline                      # 43 e3b0c44298fc…  (round 43, empty digest)
ls .ufo/reports/round-43/                                   # chousa kake kotodama kumitate mori  — no tameshi.md
git check-ignore -v tameshi-shokunin/.ufo/waves/round-43/w2/swarm-registry.json   # .gitignore:1:*-shokunin/
```
