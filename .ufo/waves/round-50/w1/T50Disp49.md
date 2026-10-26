# T50Disp49 — C1 disposer, round-49 spot-check items (R49.1–R49.6)

Seat: T50Disp49 (C1 disposer, spot-check round 49). Lane `tameshi-shokunin`, base
`e3729de862f73ae080d98fcf522a7081ce16e40a`, lane tree read at `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`
(the round-50 tip; the only commit after base that touches anything a row names). Statement set
`.ufo/evidence/round-50/c1/defects.json` (never edited) and counter `.ufo/evidence/round-50/c1/measure.py`
read in full; contract `.ufo/evidence/round-50/contract.json` read for `claims.C1`. No tool installed or
upgraded (nothing needed; `python3` 3.x and `git` sufficed — pacman is paused host-wide and no install
was attempted). No lane file touched except this report and the deliverable files under
`.ufo/waves/round-50/w1/`. Scratch `/fast/scratch/hyaku/tameshi-r50/T50Disp49` deleted before yield.

Deliverables: `T50Disp49.rows.json` (`{"round":49,"rows":[…]}` in the ledger schema plus `fix_plan`),
this report, and the receipts `T50Disp49.validate.out`, `T50Disp49.explain-rows-only.out`,
`T50Disp49.explain-with-planned-ids.out`, `T50Disp49.probe-unreadable-guard.{out,err}`,
`T50Disp49.postbase-log.out`.

## Disposition table

| Item | Status | What the tree shows at the content revision | Commit |
|---|---|---|---|
| R49.1 generator error paths | **open** | `main()` still admits an unreadable guard; probe exits 1, docstring promises 2 | — |
| R49.2 counter blind spots | **open** | no successor C1 counter and no generator-kind test anywhere at base | — |
| R49.3 outside-section stale sentences | **open** | SKILL.md:1503, :1509, :1555 byte-unchanged | — |
| R49.4 standing axis table | **fixed** | round-50 section appends the re-stated table with `calibration | 8` | `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2` |
| R49.5 carried round-48 items | **open** | both dead `brace_depth_at` helpers still present; four other asks absent | — |
| R49.6 SHONEN | **declined** | operator-owned promotion act; boxes still `[~]` | — |

Slice totals from the frozen counter (`T50Disp49.explain-rows-only.out`):
`fixed=1 open=4 declined=1 fixed_this_round=1 missing=43 evidence_bad=0 key_miss=0 fixed_bad=0
declined_bad=0 open_unplanned=4`. `missing=43` are the other seats' rows and are expected in a
six-row slice.

## R49.1 — Generator error paths — open

**Ask** (spot-check routed item 1, `.ufo/evidence/round-49/w2/T49W2RevGenCode.md` F1–F3, the file the
item cites): an unreadable guard must exit 2, as the docstring promises, not 1; F2/F3 are the two
minor error paths; "each fix needs a selftest case that fails before it".

**Found.** The docstring still promises the exit-2 path — `tools/pbt-staged-id.py:41` "2 = setup
problem (bad arguments, unwritable dump, unreadable guard)" — while `main()` still gates only on
`os.path.isfile`: `tools/pbt-staged-id.py:981-982` (`guard = os.path.abspath(args.guard)` /
`if not os.path.isfile(guard):`), and `run_guard` catches only `subprocess.TimeoutExpired`
(`tools/pbt-staged-id.py:771-774`). F2's uncaught mid-run writes and F3's `makedirs`-outside-`try`
(`tools/pbt-staged-id.py:791` vs the `try` at `:794`) are unchanged too. Re-probed at the content
revision, uid 1000: `cp tools/staged-id-guard.py $S/u.py && chmod 000 $S/u.py && python3 -I
pbt-staged-id.py --guard $S/u.py --seed 4949 --cases 2 --dump $S/d.jsonl` → **exit 1**, stdout
`VIOLATION index=0 exit 2, oracle expects 1` (receipt `T50Disp49.probe-unreadable-guard.out`; stderr
empty because the failure is `python3`'s, printed into the violation line). `os.path.isfile` on the
same path returns `True` — the check that fails is the one that is missing. No commit after base
touches `tools/pbt-staged-id.py` (`git -C … log e3729de8..4afb060 -- tools/pbt-staged-id.py` → empty;
`T50Disp49.postbase-log.out`), so the row cannot be `fixed`.

**Status: open.** `fix_plan` (in the row): replace the `isfile` gate with an `open()`/`os.access`
readability check returning `_setup_error(...)` (exit 2), wrap the loop's `dump.write`/`flush` and
`write_text` in the same `OSError` guard, move `os.makedirs(case_dir)` inside the `try`, and add a
`selftest()` case that `chmod 000`s a temp guard and asserts the exit-2 message (it fails before the
change, which is what the ask requires).

## R49.2 — Counter blind spots — open

**Ask**: close the two blind spots "with a successor counter, not prose" — C1's `absent` verdict is
uncapped and needs no evidence, and C2 cannot distinguish a property-based generator from a
differential one.

**Found.** The uncapped `absent` is still exactly as routed: the round-49 C1 counter sums
`res['unresolved'] + res['unverified'] + res['excerpt_miss'] + res['not_holds']` and omits `absent`
(`.ufo/evidence/round-49/c1/measure.py:401-403`; the term is only printed, `:406`,
`res['absent'], total` at `:410`), and no cap or floor for it exists in the file (`grep -n
"ABSENT\|absent" .ufo/evidence/round-49/c1/measure.py | grep -i "cap\|floor\|>="` → only the format
string at `:406`). The C2 gap stands as the pilot entry records it:
`corpus/knowledge/pbt-generator-pilot.md:70-71` "The counter cannot tell a property-based generator
from a differential one that compares the mutant with a copy of the pristine guard"; the round-49 C2
counter has no generator-kind test (`grep -n "property\|differential" .ufo/evidence/round-49/c2/measure.py`
→ only its title docstring, `:2`). No successor instrument exists at the revision: the round-50
evidence tree holds `.ufo/evidence/round-50/c1/{defects,extract-defects,keys,measure}.py` and
`.ufo/evidence/round-50/c2/measure.py` only (`find .ufo/evidence/round-50 -maxdepth 2 -type f`), and
the round-50 C1 counter is the routed-defect ledger, which has no `absent` concept at all. The ask is
still only prose: `SCORECARD.md:2410` plans "a successor C1 counter that caps `absent` and requires
evidence for it".

**Status: open**, `fix_plan` = *not this round*: both are new frozen instruments, and the round-50
contract froze C1 as the ledger at `cdbf24c0` (`claims.C1.counter`), so amending it mid-round would
violate the freeze. It stays on Planned (round 50) for a round that pre-registers it.

## R49.3 — Outside-section stale sentences — open

**Ask**: correct the three sentences outside the seven cold-read sections — SKILL.md:1503 (the
`/tmp/tameshi-r12-*` selftest namespace overlapping the round-12 recipe's evidence path) and the
true-but-stale sentences at 1509 and 1555.

**Found.** All three are byte-identical at the content revision. `SKILL.md:1503` (the `repeated
pristine controls` registry row) still says "isolated `/tmp/tameshi-r12-*` selftest; snapshot
read-only"; `SKILL.md:1509` still says "deepens one recorded case, never a seventh independently
measured gate."; `SKILL.md:1555` still says "No registry row changes rank, SHONEN authority, or the
six recorded cases." Round 49 routed instead of editing: `corpus/lessons/round-49.md:79` ("Not
applied: two true-but-stale sentences outside the seven sections (SKILL.md:1509, 1555), because
editing them would lapse a credited section; routed below") and `:125-126` for 1503. No commit after
base touches `SKILL.md` (`T50Disp49.postbase-log.out`).

**Status: open.** `fix_plan`: (a) rename the selftest temp prefix in `tools/repeat-control.py` to
`tameshi-r12-selftest-` and reword the SKILL.md:1503 cell to the same string (same line, no pointer
moves); (b) append one erratum paragraph at the end of SKILL.md recording that 1509's "seventh" and
1555's "six recorded cases" are the round-13 registry values while the ledger now records nine legs,
leaving both sentences as written so no credited section's excerpt changes. Editing either sentence
in place is what would lapse the credit, so the append is the smallest closing move. Note for the
integrator: editing line 1503's text makes this row's 1503 excerpt stop resolving, so the row must be
re-pointed to the new text in the same commit.

## R49.4 — Standing axis table — fixed

**Ask**: the round-49 section raised calibration to 8 in prose while the last standing table
(round-48, SCORECARD.md:2355) still read `calibration | 6`; append a restated standing table with the
round-49 values; do not rewrite.

**Found.** Commit `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2` ("round-50: SCORECARD pre-registration
section and the standing axis table restated with round-49 values (routed R49.4); no-harm at base")
appends `SCORECARD.md:2416` "### Standing axis table — re-stated at round 50 (round-49 values; routed
by the round-49 spot-check, defect 4)" and the three-row table at `:2422-2424`, whose calibration row
is `SCORECARD.md:2423`: "| calibration | 8 | round-21 cold-read monitor
`calibration_restraint_score=8`, `sections_covered=64` of 64 …". The values match the round-49
section's numeric axes ("calibration 8 (was 6), depth 9, freshness 9 unchanged", `SCORECARD.md:2408`).
"Do not rewrite" is respected: `SCORECARD.md:2355` still reads `calibration | 6`, and the new text says
so explicitly ("The round-48 standing table above still reads calibration 6 … nothing above is
rewritten", `:2418`). Counter check: the keyed excerpt is absent at `routed_at` (= base), the commit
touches `SCORECARD.md` (`git diff-tree --name-only -r 4afb060`), the cited line carries none of the
acknowledgement words, and the commit is a non-ancestor of base → `fixed_bad=0`, `fixed_this_round`
includes it.

**Status: fixed** by `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`, evidence `SCORECARD.md:2423` and
`:2416`.

## R49.5 — Carried round-48 items — open

**Ask** (round-48 spot-check routed defect 4, the item R49.5 re-routes): the dead `brace_depth_at`
helpers; the round-47 C1/C3 counter survivors' selftest cases; the S205 / F7 package candidates; a
pinned-leg successor or a declared nondeterministic class for the six-leg regression ledger; the
located-name (entry-author) check; an append-only rule for landed seat reports.

**Found.** The first ask is plainly unmet: `tools/tally-audit-v2.py:135-143` and
`tools/tally-audit-v3.py:234-242` still define `brace_depth_at`, and nothing calls it
(`grep -rn "brace_depth_at(" tools/ | grep -v "def brace_depth_at"` → no line; receipt command in
this paragraph). The other five asks leave no trace in the rounds after them: `grep -n
"located\|append-only\|six-leg\|S205\|S161\|S162\|F7\|survivors" corpus/lessons/round-49.md` returns
only `:14`, `:22-23`, `:30`, `:58`, `:115`, `:134` — none of them about these asks. `SCORECARD.md:2410`
carries them only as "carried items from round 48's list", and no commit after base touches the two
tool files (`T50Disp49.postbase-log.out`). The item is compound, so even the cheap part being undone
settles it.

**Status: open**, `fix_plan` = *not this round* for the item as a whole: the only cheap part is
deleting `tools/tally-audit-v2.py:135-143` and `tools/tally-audit-v3.py:234-242` plus re-pinning the
two sha-pinned standing rows; the remaining five asks are separate work items (survivor selftests from
`w1/T47MutC1Counter.md`/`w1/T47MutC3Counter.md`, the S205/F7 package candidates, the six-leg
successor-or-class decision, a located-name check, and an append-only landing rule) and each needs its
own seat. Splitting it into one row per ask would be the honest alternative; the frozen defect set
does not allow splitting, so the item stays open as a unit.

## R49.6 — SHONEN — declined

**Ask**: all four boxes remain `[~]`; box 3's evidence is lane-dispatched readers plus an 8-item
sample, not a full non-author cold read; no box is checkable by a non-author this round; "promotion
stays operator-owned".

**Found.** `SHONEN.md:5-11` still lists four `[~]` boxes with "lane assertion, no independent
promotion verifier" carriers, exactly as the item describes. The monitor's ceiling is 8 for this
reason (`SCORECARD.md:2423`, "8 is that monitor's ceiling (two points per restrained, evidence-linked
`[~]` box)"), so the box is structural, not a missed edit.

**Status: declined** — promotion is an operator act; a lane seat writing its own box would be the
defect, and no lane file this round can make a box checkable by a non-author. Reason recorded in the
row (≥ 40 chars), evidence `SHONEN.md:5` and `:11`.

## Findings for the integrator (read before assembling the ledger)

1. **The newest Planned paragraph names no item ids.** `SCORECARD.md:2410` is the last line starting
   `**Planned (round` and contains no `R4\d.\d+` token, so every `open` row — mine and any other
   seat's — scores `open_unplanned`. Probe, scratch clone with my six rows only:
   `python3 .ufo/evidence/round-50/c1/measure.py --lane $S/lane --rev HEAD --explain` →
   `open_unplanned=4 total=70` (`T50Disp49.explain-rows-only.out`). After appending "R49.1, R49.2,
   R49.3, R49.5" to that paragraph in the clone and committing:
   `open_unplanned=0 total=66` with no `EXPLAIN` line naming an R49 id
   (`T50Disp49.explain-with-planned-ids.out`). The ids must be in the *newest* such paragraph at REV.
2. **What this slice contributes.** `fixed=1` (R49.4, via `4afb060`, already an ancestor of the
   content revision, so it counts toward `fixed_after_base_min`), `open=4`, `declined=1`. The
   remaining floors (`fixed>=20`, `fixed_after_base_min>=5`, `declined<=12`) depend on the other 43
   rows; my slice alone leaves `fixed_short=19 this_round_short=4` (`T50Disp49.explain-rows-only.out`).
3. **If the L1 lands a fix this round**, the affected row flips to `fixed` with that commit and a
   keyed excerpt from the lines it adds; my `fix_plan` texts are written to be executable as-is. If
   line 1503 or 1509/1555 are edited in place, my R49.3 excerpts stop resolving and the row must be
   re-pointed (see that item's paragraph).
4. **Frozen-set integrity held** in both probes: `spotcheck_changed=0 defects_pin=0 bad_status=0
   evidence_bad=0 key_miss=0 fixed_bad=0 declined_bad=0`. I never edited the contract, the defect set,
   the counters, the controls, the spot-check files, SCORECARD, or any tool.

## Out of scope / not done here

- I did not decide claim C1, run a deciding invocation of any counter, or score controls; all counter
  runs are `--explain` on scratch clones with scratch work dirs (`TMPDIR=$S/w`).
- The round-50 lesson (`corpus/lessons/round-50.md`) does not exist yet, so nothing is read from it;
  the round-50 SCORECARD sections (`:2412-2431`), QUALITY criteria 94-99 (`corpus/QUALITY.md:1380-1460`)
  and the round-50 evidence trees were read instead.
- Nothing under `/home/vgpnk/.local/state/` was read; no hidden C2 panel or mutant name appears here.
- No tool install or upgrade (none needed).

## Summary

_Disposition: R49.4 fixed (commit `4afb060`), R49.1/R49.2/R49.3/R49.5 open, R49.6 declined (operator-owned)._
_Frozen counter on my rows: fixed=1 open=4 declined=1 fixed_this_round=1, every evidence term 0; only `open_unplanned=4` and the other seats' `missing=43` remain._
_Blocker for the ledger: `SCORECARD.md:2410` carries no item ids — binding the four open ids takes total 70 → 66 with no R49 explain line._
_R49.1 re-probed live at the content revision: unreadable guard still exits 1 while the docstring promises 2 (`tools/pbt-staged-id.py:41` vs `:981-982`)._
_R49.3's three sentences are byte-unchanged; R49.5's dead helpers have no caller and the other five asks left no trace._
_No lane file edited; contract, defect set, counters, controls, spot-check files untouched; frozen-set terms all 0._
_Receipts in `.ufo/waves/round-50/w1/T50Disp49.*`; scratch `/fast/scratch/hyaku/tameshi-r50/T50Disp49` deleted._
