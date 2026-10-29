# T57W1ScribeItemsR52x4to6 — ledger rows R52.4-6 (round-52 routed items)

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `5e3569969b532310d2b8a3d130901757a3df356b`.
Spot-check `corpus/lessons/round-52-verifier-spotcheck.md` added at `c1d49d76` (the counter's `routed_at`).
Judged on: calibration. Milestone: ledger rows R52.4-6.

## Dispositions

| item | status | fixability | commit | basis |
|---|---|---|---|---|
| R52.4 uncommitted round work | fixed | none needed | `6db1d220b337c35ff1e25bf9cfd74abc9db1498d` | commit 6db1d22 tracks `build-readers.py`, `w3.ready`, `w3.ready.dispatched`, `w3/`; base worktree carries no round-52 untracked work |
| R52.5 hard-coded `/tmp` in `tools/registry-check.py:766` | fixed | none needed | `218bc6b5c25d6a3c57dd44600febd552f0167cee` | at `c1d49d7` line 766 is `work = tempfile.mkdtemp(prefix="tameshi-registry-check-", dir="/tmp")`; 218bc6b replaced it (5b703c6 later routed through `strict_scratch_root()`); base has no executable `/tmp` literal |
| R52.6 report-contract repairs | open | not-fixable | — | no lane commit after `c1d49d7` changed a lane surface the item names; see below |

Not declined, no unresolved rows.

### R52.6 — why open, why not in-lane fixable
- Trend vocabulary: `SCORECARD.md:37` reads `` `harmed` / `unchanged` / `unprovable-but-better` verdict. `` and is byte-identical at `c1d49d7` and base (receipt `r52-6-vocabulary-and-report-scope.txt`).
- Per-box SHONEN form: lane `SHONEN.md` untouched since `c1d49d7` (`git diff --stat` empty).
- Report surfaces are fleet-owned, outside the lane: the round-52 report is fleet commit `53fdd555` `.ufo/reports/round-52/tameshi.md` (line 32 still reads "written but not committed/pushed"); the prompt is fleet `.ufo/prompts/tameshi-round-52.md`. Lane `.ufo/reports/` holds only `round-1/tameshi.md`.
- A cheap in-lane fix would need to invent a report-contract document; that is not a repair. Nothing staged. The lane-side residue (per-box SHONEN lines, Landed changes and Before → after sections, allowed trend vocabulary, no "not committed" sentence) is the round-57 report's content for the L1 to write.

## Evidence (all resolved with the round-50 rules, `measure.py` functions imported, not copied)
- R52.4 keyed items: `.ufo/evidence/round-52/integrate/build-readers.py:5-6` "the wave results are committed before refresh runs"; `.ufo/waves/round-52/w3.ready:1-1` `{"lane":"tameshi","round":52,"wave":"w3"`.
- R52.5 keyed items: `tools/registry-check.py:786-786` "raise RuntimeError(f"cannot create clone scratch under the scratch root: {exc}") from exc"; `tools/registry-check.py:78-78` "fixtures only under the scratch root (TMPDIR), never touches the lane".
- R52.6 keyed items: `SCORECARD.md:37-37`; `SHONEN.md:5-5`.
- Excerpts absent at `c1d49d7` and present at base: `fixed-excerpts-routed-vs-base.txt` (all `excerpt_at_routed=False`, `excerpt_at_base=True`).
- Ancestry: both fixing commits are ancestors of base and not of `c1d49d7` (`ancestry-and-touched.txt`).

## Verification run
- Scratch clone (`git clone --shared`, detached at base), fixture commit whose `corpus/routed-defects.json` holds only the three rows; `measure()` imported from `.ufo/evidence/round-50/c1/measure.py`, `fixed_floor=0`, `this_round_floor=0`:
  `counts open_unplanned=1 total=1`, `stat fixed=2 open=1 declined=0 fixed_this_round=2`. The only nonzero counter is the expected R52.6 planned check; every evidence item resolves (`fixture-measure-r50-rules.txt`).
- Negative control A: R52.5 credited to 6db1d22 (no registry-check touch) → `fixed-not-new R52.5`, `fixed_bad=1`. The fixed check discriminates.
- Negative control B: a newest `**Planned (round 57):**` paragraph naming R52.6 → the round-50 regex `\bR4\d\.\d+\b` finds nothing and the counter still reports `open_unplanned=1`; the staged round-57 counter regex `\bR5[0-6]\.\d+\b` finds `R52.6`. The inherited round-50 regex cannot credit an R5x open row.
- Keys (2-5 per id, in `rows.json`): R52.4 three keys; R52.5 three keys (`/tmp` auto-key matches the extractor's); R52.6 four keys.
- Extractor cross-check: `items_of()` on base found six items; R52.4 and R52.5 auto-keys equal the curated keys.

## Cold-read cost
No file is changed by this seat; nothing is staged. Cited paths: `SCORECARD.md`, `SHONEN.md`, `tools/registry-check.py` are plain pinned inputs of the round-21 ledger, but read-only citation costs nothing. The R52.6 planned paragraph will change `SCORECARD.md`, which IS pinned by 6 entries under `## Standing rules`, `## Mutation-sweep recipe…`, and `## The cadence's first scheduled tick…` — the L1 should batch it with the other SCORECARD edits before C0.

## Artifacts
- Rows: `.ufo/waves/round-57/w1/T57W1ScribeItemsR52x4to6/rows.json` (ledger rows with `keys` and `verdict_basis`; drop those two fields when copying into `corpus/routed-defects.json`).
- Machine-readable: `.ufo/waves/round-57/w1/T57W1ScribeItemsR52x4to6.json`.
- Receipts: `.ufo/waves/round-57/w1/T57W1ScribeItemsR52x4to6-receipts/` — `ancestry-and-touched.txt`, `fixed-excerpts-routed-vs-base.txt`, `fixture-measure-r50-rules.txt`, `r52-6-vocabulary-and-report-scope.txt`, `lane-status-sweep.txt`.

## Findings for the L1
1. Name R52.6 in the newest `**Planned (round 57):**` paragraph of `SCORECARD.md` at the content-final rev, or the open row is `open_unplanned`. The inherited round-50 planned regex (`R4\d`) cannot credit an R5x id; the staged round-57 counter's `R5[0-6]` regex does. Do not copy the round-50 regex into the round-57 counter unchanged.
2. Floors: R52.4 and R52.5 contribute `fixed=2`, `fixed_this_round=2` (both after BASE `e3729de`). Floor decisions are the L1's.
3. Lane worktree at base shows only the wave's own staging untracked (`?? .ufo/evidence/round-57/`, `?? .ufo/waves/round-57/`). Commit them under the round-57 entry; carrying them over is the R52.4 defect class.

## Sweep
- `git -C LANE status --porcelain` and `rev-parse HEAD` (read-only) — `lane-status-sweep.txt`: HEAD `5e35699…`; only the two round-57 untracked directories.
- No mutating git command ran in the lane. Fixture commits ran only in the scratch clone; scratch removed at the end.

## Tooling
None installed or updated. Used `python3` standard library and `git` only.
