# W2ScoutFleetClean — fleet-root misroot sweep (tameshi r36, w2)

## Attacked
Verify that no round-36 seat notes leaked to the fleet root as untracked files, and
characterize the full dirty set of the fleet repo `/home/vgpnk/Projects/shokunin`
at HEAD `59e9631` (`round-37: tameshi dispatch evidence`, 2026-10-24 03:35:57 -0300).
Sweep ran ~03:40, after the w2 dispatch (lane `dispatch-w2.json` mtime 03:13).

## Commands run
- `git -C /home/vgpnk/Projects/shokunin status --porcelain`
- `git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/reports .ufo/waves` → empty
- `git -C /home/vgpnk/Projects/shokunin diff --stat` and `git -C /home/vgpnk/Projects/shokunin diff SCORECARD.md`
- `git -C /home/vgpnk/Projects/shokunin log -5` and `log -2 -- .ufo/reports/round-36`
- `stat -c '%y %n'` on every dirty path; `find /home/vgpnk/Projects/shokunin -maxdepth 4 -name '*round-36*' -o -name 'W2*.md'`

## Untracked list (verbatim, 17 entries)
```
?? .omp/mcp.json
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? AGENTS.md
?? bm.json
?? live.html
?? live_s228.html
?? nama.html
?? s395.txt
?? scripts/hyaku/append-closure.py.bak-20261023T040735Z
?? scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z
?? tf_bavelas.html
?? unblob.log
?? wb2.html
?? write
?? xc.xml
```

## Modified (tracked) list
`M` on 12 `.ufo/state/*.report-baseline` files (chousa, kagi, kaidoku, kake, kama,
kengaku, kumitate, mado, mori, souji, tameshi, tsukuroi — each a 1-line baseline
writer update), `.ufo/watchdog.log` (+550 lines), `SCORECARD.md` (+1 blank line).

## Findings
1. **No misrooted round-36 seat notes.** No untracked entry is under `.ufo/waves/`
   or matches a seat-report name. The fleet repo has no `.ufo/waves/round-36/` at
   all; round-36 wave dirs exist only inside lane checkouts (kake-, kumitate-,
   tameshi-, tsukuroi-shokunin), confirmed by `find`.
2. **Round-36 fleet report is committed, not dirty.** `.ufo/reports/round-36/`
   holds 7 per-lane reports including `tameshi.md`; both it and `.ufo/waves/` are
   clean in status. `tameshi.md` landed at commit `f4ef953` (03:23:42). The only
   fleet-level round-36 paths are orchestrator artifacts: `.ufo/reports/round-36/`
   and `.ufo/prompts/{,closure/}*-round-36.md` — all tracked/committed.
3. **Remaining churn is orchestrator bookkeeping + pre-wave debris.** The
   `.report-baseline` writes and `watchdog.log` appends are the dispatch
   pipeline's own side effects (mtimes track each dispatch: tameshi baseline
   03:35:57 ↔ round-37 dispatch commit 03:35:57; kama 03:35:22 ↔ `bad6725`).
   Every non-baseline untracked file has an mtime of Oct 19–23 — predating this
   wave; they are stale debris (`write` is a 25-byte stray from Oct 21; two
   `*.bak-20261023T040735Z` files; loose html/log/xml). `SCORECARD.md`'s diff is a
   single trailing blank line (mtime Oct 23 20:10, pre-wave).

## Verdict
**PASS** — zero round-36 seat notes at the fleet root. The dispatch expectation
"only the round-36 report file changes" holds in spirit with one honest caveat:
the round-36 report is properly committed and clean, while the worktree carries
only orchestrator bookkeeping deltas (state baselines, watchdog.log, +1 blank
line in SCORECARD.md) and older unrelated debris — none attributable to round-36
seats and none misrooted.
