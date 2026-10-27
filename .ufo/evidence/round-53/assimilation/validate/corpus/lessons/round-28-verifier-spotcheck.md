# Round 28 — verifier spot-check (tameshi)

author: hyaku closure (non-author integrator, @m_opus)

Scope: tameshi round 28 (L1 `TameshiR28`, attempt 1). Base `06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c`.
Closure prompt head: `1076914abf513c723d454b9d35b7f04d9101d3af`. The lane kept landing after
that: `41da22a3` (Read14B assembled) and `1dde85f3af3dfeae777c1ca4eed26aaf18df1167` (63/64 reading).
The report was re-committed at fleet `38ae0ff` (the first version was `2012146`) and names `1dde85f3` as its head.
Both heads are measured below. The verdict holds at either one.

Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-22T15:52:18-03:00 launch tameshi round=28 pgid=3552765 driver=hyaku-inline attempt=1`;
`2026-10-22T16:28:50-03:00 complete tameshi round=28; hyaku-inline attempt=1`.

## Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-28/tameshi.md` | `tameshi-shokunin 2012146…`, then `tameshi-shokunin 38ae0ff` ("final 63/64") | pass |
| SHONEN heading, one line per box | read report `## SHONEN` | 4 lines, all `[~]`; `SHONEN.md` has 4 boxes and no diff from base | pass |
| Cited commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` × 10 (b05d2ee, a20e2ba, ae7a11d, c30926e, a269d90, bdf0aa5, c4e0098, 1076914, 41da22a, 1dde85f) | all hold | pass |
| Pushed | `jj-lane.sh state` | first run: `local=remote=41da22a3 ahead=0 untracked=1`; later: `local=remote=1dde85f3 ahead=0 behind=0 tracked=0 untracked=0` | pass (final) |
| Leftovers | `git status --porcelain` | first run: `?? .ufo/evidence/round-28/c1-after-final3.stdout` (round-work receipt, not yet committed); later: empty. The orchestrator reported three uncommitted paths before this closure started. By the second check all of them were committed or gone | defect (transient; resolved by the lane before closure) |
| Prompt carries template contract | `grep '^## ' .ufo/prompts/tameshi-round-28.md` | §1 MISSION/AXES, §2 Claims, §2b Frontier, §3 L2 floor, §4 Report contract, §5 Commit/push, §6 hyaku addendum | pass |
| Marker report? | — | no; 10 landed commits with checkable work | status ok |

Defect (status-neutral): the lane kept landing after the closure prompt was rendered against `1076914a`. It also rewrote the
fleet report in place (`2012146` → `38ae0ff`), so the head that was closed and the head the report names differ.

## Claim C1 — calibration (harm repair), re-measured

The counter is frozen. `git diff --quiet 06b59b93 1076914a -- .ufo/evidence/round-27/c1-measure.py` exits 0, so it is byte-identical.

```
$ python3 .ufo/evidence/round-27/c1-measure.py --repo . --rev 06b59b93
C1_MONITOR: covered=60/64 restraint=6 box3_mismatch=1 depth_score=9 rev=06b59b93…   exit=1
$ python3 .ufo/evidence/round-27/c1-measure.py --repo . --rev 1076914a
C1_MONITOR: covered=62/64 restraint=6 box3_mismatch=1 depth_score=9 rev=1076914a…   exit=1
  uncovered: Round-18 gate/probe registry; Round-21 gate/probe registry
$ python3 .ufo/evidence/round-27/c1-measure.py --repo . --rev master   (= 1dde85f3)
C1_MONITOR: covered=63/64 restraint=6 box3_mismatch=1 depth_score=9 rev=1dde85f3…   exit=1
  uncovered: Round-18 gate/probe registry
```

The re-measured values match what the report says at each head: 62/64 in `2012146`, 63/64 in `38ae0ff`.
The declared target was `covered=64/64 restraint=8 box3_mismatch=0`, exit 0. It is **not met** at either head.
The claim is a declared honest stop, and this closure re-measured it rather than relying on the lane's evidence.

Ledger append-only, re-checked with python/json at `git show <rev>:.ufo/evidence/round-21/coldread/ledger.json`:
- `entries[:354]` equals the base entries at both heads.
- All non-entry keys are equal.
- The entry count is 354 at base, 370 at `1076914a` and 371 at `1dde85f3`.
- `git diff --numstat 06b59b93 1dde85f3`: additions only for the ledger, LOG, SCORECARD and SKILL. SOURCES has +15/−1, and the −1 is the in-place S059 `used-by` edit.

Append probe: `.ufo/evidence/round-28/append-probe.txt` reads SOURCES 50, README 55, QUALITY 57, SHONEN 59, LOG and SCORECARD 60, all six 47, base 60. These match the lesson's Mistake 1 figures.
Evidence-verified only, not re-run here: seat MutateAppendProbe reproduced it.

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | unchanged | The scalar inputs did not move: restraint 6 → 6, box3_mismatch 1 → 1, exit 1 → 1. Covered sections rose 60 → 62 (`1076914a`) or 63 (`1dde85f3`). The claim is not verified, because the target was 64/64 with restraint 8. The axis is still harmed against the pre-r26 reading (62/62, restraint 8) |
| (other owned axes) | unchanged | `git diff 06b59b93 1076914a -- SCORECARD.md` is an append of the round-28 block only; no other scalar changed |

No axis was harmed relative to this round's base.

## Discernment spot-check

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S059 re-open (lesson `## Gate`) | admit (re-open, `used-by` extended) | `curl -sL https://bazel.build/remote/caching` (2026-10-22 ~19:30Z) | agree | The quote "The action cache, which is a map of action hashes to action result metadata." is present verbatim under "The remote cache stores two types of data". It has 14 words, which is ≤25 and matches the corrected count. "Bazel does not track tools outside a workspace" is present as the Known-issues heading, so the row's scope holds. Live HTML sha256 is `4fe02a79…`, not the lesson's `9e3a2ebb…`. The markdown alternate is `266915c5…`, not the row's `0d362d11…`. That reproduces the drift the lane itself flagged, and the row still needs a supersedes row |
| Draft row S092 for the same URL (lesson `## Gate`, Mistake 2) | reject (duplicate, removed before commit) | `grep -c 'bazel.build/remote/caching' corpus/SOURCES.md` at `1076914a` and at the working tree | agree | 1 occurrence (S059 only), and the row count stays 89 → 89 (`grep -c '^\| S[0-9]'`). A second row for the URL would duplicate S059 |
| SOURCES row S059, newly edited (quote check) | — | the row at `1076914a` | agree | The quote "Bazel does not track tools outside a workspace" has 7 words (≤25) and matches the live heading text |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` returned exit 0 and `ok`. It printed only the 7 W04 cross-scope duplicate warnings, for S047, S048, S075, S076, S077, S078 and S081.

## Trend verdicts

- **expansion: unchanged.** Rows went 89 → 89. No new row or knowledge entry.
- **quality: unprovable-but-better.** The SKILL Round-21 correction was appended with 18 lines added and 0 removed. Its basis checks out: `c2-count.py` line 19 is `FLEET = Path("/home/vgpnk/Projects/shokunin")` and line 52 reads through `FLEET`. The corrected section is credited only at `1dde85f3` (Read14B), which is after the closure-prompt head. No counter of my own measures quality.
- **discernment: improved.** The mechanism behind the r26 harm (the input-digest gate de-credits on the round's own edits) is now a committed receipt with per-file figures. The lesson Mistake 1 carries it as a failing case. A duplicate row was caught by the census and rejected before commit. Both spot-checked gate decisions agree with the re-opened source.

## Verdict

Status ok; **not admitted** (`rejected-honest-stop`). C1's declared target of 64/64, restraint 8, exit 0 is not met. The re-measured results are 62/64 at `1076914a` and 63/64 at `1dde85f3`, with restraint 6 and exit 1 at both. No axis was harmed against base. Reviewer seats were not dispatched; every re-check above was run by this closure.

## Routed defects (lane fixes next round)

1. C1 is still open: cover "Round-18 gate/probe registry" and bring restraint 6 back to 8 with box3_mismatch 0. Make every widely read input edit (SOURCES, README, QUALITY, SHONEN) before the content revision that the cold reads target. The round's own Mistake 1 fix says the same.
2. S059 pinned digests no longer reproduce: markdown alternate `0d362d11…` vs live `266915c5…`, and the lesson's HTML sha `9e3a2ebb…` vs live `4fe02a79…`. Add a supersedes row, or record that the HTML is non-deterministic.
3. Close against one head. Stop landing commits and rewriting the fleet report after the driver `complete` line, or declare the final head before the closure is rendered.
4. Routed items 4, 5 and 6 from round 27 are still not done (README, QUALITY and runner ledger inputs).

SHONEN: all four boxes are `[~]`. Box 3 is not checkable while box3_mismatch is 1. Boxes 1, 2 and 4 are lane assertions with no independent verifier, so nothing is ready for operator promotion.
