# W2LabratScoreEight — tameshi round 36 w2 probe (read-only)

## Attacked
C1 (calibration): hand-recompute `calibration_restraint_score` from the monitor's
own JSON at the round-36 refresh commit using the round-18 algorithm header
(`2 * #(boxes 1,2,4 marked ~) + 2 * (box3 ~ AND box3 ledger link AND
box3_full_page)`; box3_full_page = sections_covered == sections_total) and check
it equals 8.

## Commands run (all read-only, cwd = /home/vgpnk/Projects/shokunin/tameshi-shokunin)
- `python3 -c` — load `.ufo/evidence/round-36/after/monitor-at-b455001e.stdout`,
  `after/monitor-at-796e08b.stdout`, `control/monitor-at-e423c41b.stdout`;
  extract `shonen.{marks,box3_marked,box3_ledger_link,box3_points}`,
  `coldread.{sections_total,sections_covered,box3_full_page,missing,reasons,sections}`,
  `calibration_restraint_score`; re-derive `2*sum(marks[b-1]=='~', b in 1,2,4) +
  2*box3_points` by hand.
- `python3 -c` — diff `coldread.missing` across the three runs; compare to
  `.ufo/evidence/round-36/coldread/affected-sections.json`.
- `python3 -c` — `.ufo/evidence/round-21/coldread/ledger.json` (tip): 497
  entries; per-start listing for 131/375/1380/1436; veto-eligible census (40
  entries, all old-read-rev/stale-input by aggregation rule).
- `git show b455001e...:SHONEN.md` — four `- [~]` boxes (lines 5,7,9,11);
  box-3 continuation line 10 carries `.ufo/evidence/round-21/coldread/ledger.json`
  (the round-21 selector's `BOX3_LINK` override).
- `git rev-parse` / `git merge-base --is-ancestor` / `git log` — ledger blob at
  796e08b and e423c41b = `b2fe6191…`, at b455001e = `b0522d3c…`; e423c41b is an
  ancestor of b455001e; exactly one commit between them (`b455001e` "round-36:
  cold-read refresh — four L1 author source re-anchor entries"). Lane tip HEAD:
  `fbb01cf46f8437fd1264c1a3acc053c882fa2164`.
- Head of `.ufo/evidence/round-36/coldread/refresh-receipts.json` — `entries_added: 4`.

## Arithmetic
Refresh commit `b455001e2589b3f4f471d94a3de7e5e549b9f54c`:
- marks `['~','~','~','~']` → boxes 1,2,4 all `~` → `2 * 3 = 6`
- `box3_marked=True`, `box3_ledger_link=True`, `box3_full_page=True`
  (sections_covered 64/64, all reasons `credited`, 0 vetoed) → `+2`
- Hand total = **8** = monitor-reported `calibration_restraint_score` **8**. Equal.
- Controls hold: at 796e08b and e423c41b the same arithmetic gives
  `2*3 + 2*0 = 6` (60/64, box3_full_page False) — the identical missing set is the
  four drifted sections (starts 131, 375, 1380, 1436) per affected-sections.json;
  after the refresh each of the four is `credited` via the four new ledger
  entries (read_rev e423c41b, class record, verdict gap-minor, 1 command, 1
  trace each).

## Verdict
VERDICT: CONFIRMED — hand-recomputed calibration_restraint_score = 8 at refresh
commit b455001e2589b3f4f471d94a3de7e5e549b9f54c (2*3 shonen + 2*box3_full_page),
matching the monitor output and the 6→8 claim; before/control runs recompute to
6 with the identical four-section missing set.

## Residual unknowns / notes
- Veto aggregation not re-derived independently: 40 veto-eligible ledger entries
  exist (wrong-expectation/gap-blocking) but none vetoed at rev — consistent
  with the stale-input rule; the monitor's per-section `vetoed` flags were
  trusted, not recomputed via `git cat-file` input-hash checks.
- Ledger JSON schema/entry fields used as-is; new entries are L1-author
  input-keyed source reads per refresh-receipts.json scope disclaimer.
- No tools installed; no lane writes outside this report.
