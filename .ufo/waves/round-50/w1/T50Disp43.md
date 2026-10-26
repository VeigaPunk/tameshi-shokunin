# T50Disp43 — C1 disposer, round-43 spot-check (R43.1–R43.3)

Seat: T50Disp43, C1 disposer for `.ufo/evidence/round-50/c1/defects.json` round 43. Base
`e3729de862f73ae080d98fcf522a7081ce16e40a`. All reads below are against base unless a
revision is named; every `git -C` line names the lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`. I read each item's full text in
`corpus/lessons/round-43-verifier-spotcheck.md:63-65` (frozen sha `7b0357f4…615a`), its
`keys`/`routed_at` (`506e99c7b73c85711f066895984d501fcf7539cd`) from `defects.json`, and
judged the tree, not the prose. Deliverable rows:
`.ufo/waves/round-50/w1/T50Disp43.rows.json` (3 rows, all `fixed`, all committed at
`83beaf980f246412368f89fbe7758375c8ca21e0`). No row is `open`, so no `fix_plan` is
required; no row is `declined`.

## R43.1 — reconcile the round-43 SCORECARD `m7` unknown `S256` citation and re-run C2 at the final intended revision (fixed)

The ask has two parts: (a) reconcile the round-43 SCORECARD `m7` hit on `safe_floor=S256`,
(b) re-run the C2 measurement at the final intended revision, with the correction kept
append-only (round-43 report/lesson not rewritten). All three exist. The reconciliation is
a mask in the successor counter: `.ufo/evidence/round-44/calibration/measure.py:89`
(`ASSIGN_ID`) applied at `:109`, pinned by tests `:419` (`T6_safe_floor_value_not_citation`)
and `:422` (`T6_assign_with_spaces_masked`); the pin is load-bearing — removing only the
mask fails both tests with `['r unknown S256']` (`.ufo/evidence/round-44/control/mask-removed.selftest.stdout:1-5`,
`cases=16 failed=2`, `VERDICT: FAIL`, `selftest_exit=1`; `grep -n ASSIGN_ID
.ufo/evidence/round-44/calibration/measure.py` → `89`, `109`). The old→new record is
`corpus/lessons/round-44.md:83` (the round-43 counter's `m7=1 first=m7:SCORECARD.md#round-43_unknown_S256`
beside its source line) and `:89-91` ("the S256 m7 false alarm is fixed and measured"). The
re-measurement exists twice: at the landing record bytes —
`.ufo/evidence/round-44/before/c2-new-at-base.stdout:1` gives `m7=0` at `rev=506e99c`, and
`git -C … diff --stat 718a1e9 506e99c` shows the only difference between the round-43
landing and the spot-check commit is the added spot-check file, so those are the landing
SCORECARD bytes — and with all seven classes zero at
`.ufo/evidence/round-44/after/c1-at-ef990aa.stdout:1` (`total=0 C2_R44_PASS=true`). The
literal "re-run at the final intended revision" also exists as a receipt:
`.ufo/evidence/round-45/quality/c86-falsifier.stdout:12` runs the round-43 counter at
`rev=718a1e9` and preserves `m7=1` as the historical red rather than rewriting it. Append-only
is verifiable: `git -C … log --format='%H %ad %s' 506e99c7b73c85711f066895984d501fcf7539cd..e3729de8 -- corpus/lessons/round-43.md .ufo/reports/round-43/`
prints nothing, so the filed report and lesson were never edited after routing. Reading
risk disclosed: the successor counter, not the round-43 counter, is what turns `m7` green;
the round-43 counter stays red at `718a1e9` by design, which is the append-only record the
ask asked for.

## R43.2 — restore or explicitly disposition the dirty tracked file `.ufo/waves/round-43/w1/RevC2Classes.md` (fixed)

The ask is a satisfiable-either-way ("restore or explicitly disposition"). The lane
dispositioned it: the worktree edit was retained and committed.
`git -C … log --format='%H %ad %s' --date=short -- .ufo/waves/round-43/w1/RevC2Classes.md`
→ `83beaf98` ("round-44: repair citation masking and supersede S089 anchor"), `3c4003f6`,
`c5335c70`; the 83beaf98 diff carries exactly the A13 pin/line corrections the spot-check
described (`three times … (A6/A7, A8, A10)` at routed_at → `four times … (A6/A7, A8, A10, A13)`
now; compare `git -C … show 506e99c:.ufo/waves/round-43/w1/RevC2Classes.md | sed -n '8p'`
with `.ufo/waves/round-43/w1/RevC2Classes.md:8`). The explicit decision is recorded in the
round-44 lesson: `corpus/lessons/round-44.md:85` ("retain and commit the updated reviewer
note as round-44 inherited evidence"), repeated in the routed-items paragraph
`corpus/lessons/round-44.md:89-91` ("the dirty wave note is explicitly retained"). The
worktree is clean for that path at base: `git -C … status --porcelain` lists only round-50
untracked entries, no modification of the wave note.

## R43.3 — update S089's stale `anchor` to the re-opened snapshot in a future append-only registry change and log old→new (fixed)

The registry change exists and is append-only: `corpus/SOURCES.md:130` is the new row
`| S160 | … | supersedes S089's anchor only: the snapshot digest checked at the 2026-10-25 re-open | … | supersedes S089 — the cited sentences survive at the same offsets but its pinned html digest bc572676… is stale; this row pins the re-opened snapshot | mined | 2026-10-25 | 180d |`.
`git -C … log --format='%H %s' -S'| S160 |' e3729de8 -- corpus/SOURCES.md` → `83beaf98`, a
post-routing commit. The old→new log the ask requires is
`corpus/lessons/round-44.md:35-38` (`bc572676…e04d` → `79f6501a…4079ce`, same offsets), and
the reason the S089 cell is not edited in place is stated at
`corpus/lessons/round-44.md:47-51` (SOURCES contract rule 2) and generalised in
`corpus/knowledge/r44-anchor-refresh-rule.md:37-41` ("Why not edit in place … The supersede
row keeps both facts visible (old digest in S089, new digest in S160)"). The claim was also
measured as the round-44 freshness claim (`SCORECARD.md:2127`, `:2139`: `grep -cE
'^ {0,3}\| S160 ' corpus/SOURCES.md` → 0 at base, 1 at `ef990aaa`, census exit 0 with the
expected W04 duplicate URL). Reading risk disclosed: S089's own `anchor` cell still reads
`page fetched 2026-10-22 … bc572676…e04d` (`corpus/SOURCES.md:98`) — that is deliberate, and
the ask's own condition ("in a future append-only registry change") is what S160 is. A
reader who requires the S089 cell itself to change would have to call this `declined`
(reason: the registry contract forbids in-place anchor edits); I judged `fixed` because the
re-pin, the append-only form and the old→new log all exist in the tree.

## Self-check (probe, not a verdict)

Rows only, in a scratch fixture: `git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin
/fast/scratch/hyaku/tameshi-r50/T50Disp43/lane3` (clone at `4afb060`), `corpus/routed-defects.json`
written as `{"defects": [<the three rows taken verbatim from the deliverable
`.rows.json`>]}`, committed with a scratch identity
(`9947f016ed273e85845833263e699838847ea24c`), then

```
TMPDIR=<scratch> python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-50/c1/measure.py \
  --lane <scratch>/lane2 --rev HEAD --explain
```

observed (exit 1):

```
C1_R50: self=ceee320c9ad8 rev=9947f016ed273e85845833263e699838847ea24c defects=49 rows=3 fixed=3 open=0 declined=0 fixed_this_round=0 missing=46 extra=0 duplicate=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=0 declined_bad=0 fixed_short=17 declined_over=0 this_round_short=5 total=68 C1_R50_PASS=false
```

Every non-zero term is accounted for and none is mine: `missing=46` are the other rounds'
rows (46 `EXPLAIN missing <id>` lines, none naming `R43.*`), `fixed_short=17` and
`this_round_short=5` are the floors a three-row fixture cannot meet, and every term my rows
could trip (`evidence_bad`, `key_miss`, `fixed_bad`, `open_unplanned`, `bad_status`,
`duplicate`, `extra`, `spotcheck_changed`, `declines`) is 0. No `EXPLAIN` line names any of
my ids. A first fixture attempt at base `e3729de8` was refused by the counter with
`setup error: frozen defect set absent at REV: .ufo/evidence/round-50/c1/defects.json` — the
frozen set only exists from round-50 commits on, so the self-check has to sit on a round-50
tree, not at base.

## Findings

- `.ufo/evidence/round-44/calibration/measure.py:89,109,419,422` — the `ASSIGN_ID` mask and
  its two T6 tests; shown by `grep -n 'ASSIGN_ID\|T6_safe_floor\|T6_assign' …`.
- `.ufo/evidence/round-44/control/mask-removed.selftest.stdout:1-5` — mask removal fails
  `cases=16 failed=2`, `VERDICT: FAIL`.
- `corpus/lessons/round-44.md:83,85,89-91` — the three round-43 items' dispositions in one
  place (`m7`/S256 scope row, wave-note landing row, routed-items paragraph).
- `corpus/lessons/round-44.md:35-38,47-51` and `corpus/knowledge/r44-anchor-refresh-rule.md:37-41`
  — old→new digest log and the no-in-place-edit rule behind it.
- `corpus/SOURCES.md:130` vs `:98` — S160 supersedes S089's anchor while S089's cell keeps
  the 2026-10-22 digest; both are visible at base.
- `.ufo/evidence/round-45/quality/c86-falsifier.stdout:12` — round-43 counter re-run at
  `718a1e9`, `m7=1`, `landing_exit=1`, `CRITERION-86-FALSIFIER-OK drift_paths=2` (`:14`).
- `git -C … diff --stat 718a1e9 506e99c` → one file, `corpus/lessons/round-43-verifier-spotcheck.md`;
  this is what makes the `506e99c` measurement cover the landing SCORECARD bytes.

## Tools, scope, limits

- No tool installed or upgraded (none needed; no pacman, no uv, no npx).
- No lane mutation: the lane checkout was read only; both fixtures lived under
  `/fast/scratch/hyaku/tameshi-r50/T50Disp43/` and were removed before this report was
  written. Scratch paths are cited as provenance only, never as evidence.
- Out of scope per the seat: the other 46 routed items, the C1 verdict itself, and the
  hidden C2 panel (nothing under `/home/vgpnk/.local/state/` was read).
- Known limit: my three `fixed` rows predate base, so they cannot contribute to the
  `fixed_after_base_min=5` floor; that floor is other seats' work this round.

## Summary

- R43.1 fixed: `ASSIGN_ID` masking in the round-44 counter makes `m7=0` on the round-43 landing
  SCORECARD bytes, `total=0` at `ef990aaa`, and the round-43 lesson/report are untouched after routing.
- R43.2 fixed: the dirty `RevC2Classes.md` edit was retained and committed at `83beaf98`, with the
  disposition recorded in `corpus/lessons/round-44.md:85,89-91`.
- R43.3 fixed: S160 (`corpus/SOURCES.md:130`) is the append-only anchor re-pin for S089 and the
  old→new digest is logged at `corpus/lessons/round-44.md:35-38`.
- All three rows use commit `83beaf98`; each keyed excerpt is absent at `routed_at` and its span
  carries no acknowledgement word.
- Probe on a scratch round-50 clone: `fixed=3`, `evidence_bad=0`, `key_miss=0`, `fixed_bad=0`,
  no `EXPLAIN` line naming an `R43.*` id; the remaining terms are other rounds' `missing=46`
  and the two floors.
- Residual reading risk disclosed: R43.3 keeps S089's own anchor cell stale by registry rule 2;
  R43.1's green reading comes from the successor counter, not the frozen round-43 one.
