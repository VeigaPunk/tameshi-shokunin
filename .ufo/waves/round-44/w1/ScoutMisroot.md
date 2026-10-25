# Fleet-root misroot scan

Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain -- /home/vgpnk/Projects/shokunin` (0); listed entries below. Classification is from each file's head; state baseline files contain only round and hash, and thus do not name round-44 or a seat.

## Modified/untracked paths and head matches

- `.ufo/l0-questions.md` — no round-44 or wave seat name in head (lines 1–23 show existing questions; truncated portions not assessed).
- `.ufo/reports/round-25/tabi.md` — no match; head identifies tabi round 25.
- `.ufo/state/chousa.report-baseline` — no match; head `47 e3b0...`.
- `.ufo/state/kagi.report-baseline` — no match; head `28 e3b0...`.
- `.ufo/state/kaidoku.report-baseline` — no match; head `34 de33...`.
- `.ufo/state/kake.report-baseline` — no match; head `53 e3b0...`.
- `.ufo/state/kama.report-baseline` — no match; head `39 e3b0...`.
- `.ufo/state/kasegi.report-baseline` — no match; head `26 e3b0...`.
- `.ufo/state/kengaku.report-baseline` — no match; head `32 e3b0...`.
- `.ufo/state/kumitate.report-baseline` — no match; head `61 e3b0...`.
- `.ufo/state/mado.report-baseline` — no match; head `37 e3b0...`.
- `.ufo/state/mori.report-baseline` — no match; head `46 e3b0...`.
- `.ufo/state/souji.report-baseline` — no match; head `25 e3b0...`.
- `.ufo/state/tabi.report-baseline` — no match; head `25 e3b0...`.
- `.ufo/state/tameshi.report-baseline` — no match; head `44 e3b0...` (round number alone is not the `round-44` identifier).
- `.ufo/state/tsukuroi.report-baseline` — no match; head `36 e3b0...`.
- `.ufo/watchdog.log` — no match at head (lines 1–13).
- `scripts/hyaku/closure-prompt.md` — no match at head (lines 1–21).
- `scripts/hyaku/hyaku.env` — no match at head (lines 1–15).
- `scripts/hyaku/lane-addendum.md` — no match at head (lines 1–21).
- `.omp/mcp.json` — no match; configuration only.
- `.scratch/goal-20261025-hyaku-12h.md` — no round-44 or seat-name match in head (lines 1–23).
- `.ufo/state/kotoba.report-baseline` — no match; head `70 e3b0...`.
- `.ufo/state/kotodama.report-baseline` — no match; head `71 e3b0...`.
- `.ufo/state/revenger.report-baseline` — no match; head `69 e3b0...`.
- `.ufo/waves/round-24/` — directory is untracked; contains `w2/RevUnlandedResolution.md` (15.5KB).
- `m-rev-vs-rev.py` — no match; head describes round-24/25 coverage instrument.

For `.ufo/watchdog.log`, `scripts/hyaku/closure-prompt.md`, `scripts/hyaku/hyaku.env`, `scripts/hyaku/lane-addendum.md`, and `m-rev-vs-rev.py`, searched the full files for `round-44`, `ScoutMisroot`, and `L1Tameshi44`: `grep` reported no matches. All other content classification above is head-only as requested.

## Round-44 wave directory

Exists: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-44/`. Contents listed: `dispatch-w1.json`, `spec-w1.json`, `build-spec.py`, and `w1/swarm-registry.json` (directory listing also confirms `w1/`).

No files were edited or deleted. No tools installed.