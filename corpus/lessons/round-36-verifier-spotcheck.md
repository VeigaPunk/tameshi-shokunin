# Round 36 verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-24
lane-round: tameshi 36 · base `796e08b888849308d0c4d5e932e56833600a139f` · content `e423c41ba253357ab8c8513f0376dad9d38ab248` · refresh `b455001e2589b3f4f471d94a3de7e5e549b9f54c` · tip `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`
report: `.ufo/reports/round-36/tameshi.md` @ fleet `f4ef95369577f8e0311db76d8537e5d0d327ed8c` (author `tameshi-shokunin`)

Watchdog digest (`.ufo/watchdog.log` lines 1143/1154, mutable log — digest is the resolving pointer):
- `2026-10-24T02:51:48-03:00 launch tameshi round=36 pgid=722781 driver=hyaku-inline attempt=1`
- `2026-10-24T03:24:28-03:00 complete tameshi round=36; hyaku-inline attempt=1`

## Step-1 conformance

| Check | Result |
|---|---|
| Report committed by lane identity | pass — `git log --format='%an %H' -- .ufo/reports/round-36/tameshi.md` → `tameshi-shokunin f4ef95369577f8e0311db76d8537e5d0d327ed8c` |
| SHONEN heading, one line per box | pass — `## SHONEN`, 4 boxes, all `[~]` with resolvable pointers (lane-asserted, no named non-author verifier — promotion is operator-owned) |
| Cited lane commits exist + ancestor of branch | pass — `796e08b`, `e423c41b`, `b455001e`, `d9c496b1` all `git cat-file -e` OK and `git merge-base --is-ancestor <hash> master` OK |
| Lane repo clean + pushed | pass — `jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0 head=detached` (jj-colocated, expected); `git status --porcelain` empty |
| Prompt carries template contract | pass — dispatched `.ufo/prompts/tameshi-round-36.md` carries §§1–5 heads verbatim (MISSION/AXES, claims, frontier, L2 floor, report contract, commit scope) + §6 hyaku addendum |
| Marker test | real report, not a marker — claims, receipts, pointers throughout |

Defects named (status-neutral): none at step 1.

## Per-claim re-check

Which claims were re-measured vs evidence-verified: C1 was **re-measured** by this closure
re-running the lane's monitor command over committed revs (read-only). C2's counter is a
lane-owned gate; per PROTOCOL §Gate standard (Closure consequence) it was **not executed** —
its committed evidence (freeze pin, frozen-run verdicts, revision measured, predicate source)
was verified, plus plain independent measurements over committed bytes.

### C1 — cold-read monitor refresh (calibration 6 → 8, 60/64 → 64/64)

Closure re-measurement, command `python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev REV` (wall 130 s, run by this closure):

| Rev | score | covered | overrides |
|---|---|---|---|
| `796e08b` (before) | 6 | 60/64 | False |
| `e423c41b` (do-nothing control) | 6 | 60/64 | False |
| `b455001e` (refresh) | 8 | 64/64 | False |
| `d9c496b1` (tip) | 8 | 64/64 | False |

Matches the report and the committed receipts (`after/monitor-at-796e08b.stdout`,
`control/monitor-at-e423c41b.stdout`, `after/monitor-at-b455001e.stdout`) exactly.
Kill rule verified: `git diff --name-status e423c41b b455001e` touches only
`.ufo/evidence/round-21/coldread/ledger.json` (M) and `.ufo/evidence/round-36/coldread/*` (A) —
the coldread evidence set only, no monitor/ledger-algorithm/rubric change.
Ledger delta verified: 493 entries at `796e08b` → 497 at tip (4 appended).
Refresh-protocol scope honesty: lesson `## Holds` discloses the credit is by L1 author
source reads (input-keyed), not a blind cold-read; the monitor is input-keyed by design.
Verdict: **verified** (re-measured).

### C2 — successor counter `c1-measure-v2.py` (depth surface: predicate completeness)

Evidence-verified (gate not executed):

- Freeze pin: `contract.json` records counter sha256 `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`; `git show b455001e:…/c1-measure-v2.py | sha256sum`, same at tip, and worktree all match. `frozen_before_any_data_run: true`.
- Predicate source (lines 68–70, 539–541): frozen targets `PUB_KILL_SLOTS_TARGET=6`, `PUB_ACCEPT_SLOTS_TARGET=3`, `PUB_DISTINCT_TARGET=9`; PASS requires slots and counts equal the frozen targets and `pub_distinct==9`.
- The v1 gap is real in the frozen v1 source (`.ufo/evidence/round-35/c1/c1-measure.py:517`): v1 PASS compares counts to *observed* slots only, so an emptied panel (0/0) satisfies it — the vacuous-accept defect the r35 closure routed.
- Frozen artifacts byte-identical base↔tip: `tools/tally-audit-v3.py` = `6188db16de045f29…` (capability pin), `tools/mutate-and-run.sh` = `a7d3f2dd7d47511a…`; v1 counter unchanged (`d360a159…` at both revs).
- Receipts verbatim: before/control `C1_R35: mode=deciding … pub_kill=0/0 pub_accept=0/0 … C1_R35_PASS=true` exit 0 at mutant `91373d55…`; v2 on the same mutant `pub_slots=0 pub_distinct=0 … C1_R36V2_PASS=false` exit 1; deciding run at `b455001e` `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 C1_R36V2_PASS=true` exit 0. Exactly one deciding v2 receipt committed (`after/c1v2-at-b455001e.stdout`); the other two are controls, per the kill rule.
- Deciding receipt carries 16 COPY lines (10 kill = 6 pub + 4 holdout; 6 accept = 3 pub + 3 holdout) matching the tallies; revision measured is named in every receipt line.
- Sealed inputs committed (`.ufo/evidence/round-35/c1/sealed/`, manifest + per-copy JSON).
Verdict: **verified** (evidence-verified gate + closure pin re-checks).

### Numeric guardrails

- depth: receipt `after/depthD-at-b455001e.stdout` → `recorded_cases=9 depth_score=9`, runner sha `a7d3f2dd…` — unchanged 9 → 9 as declared (evidence-verified).
- SHONEN census re-derived from the monitor at both revs: `boxes=4 checked=0 asserted=4 untouched=0` — matches report (unchanged, all `[~]`).
- Sources census re-derived from the monitor: `796e08b` → 99 rows (mined 71 / queued 22 / rejected 6); tip → 100 rows (mined 72 / queued 22 / rejected 6). Matches the report's 99 → 100.

## Discernment spot-check (LEARNING.md — checked from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S103 admit (git-hash-object, git-scm.com) | admit | committed snapshot `.ufo/evidence/round-36/src/s103-git-hash-object.html` re-opened: sha256 `dd826dae…` = row + lesson + LOG; 29,933 bytes; quote at §DESCRIPTION (line 1604 region) present verbatim modulo HTML line-wrap; located quote 18 words ≤ 25 | agree | row is tier A, status `mined` with two used-by pointers that both resolve (refresh-receipts.json cites S103; this lesson's Gate); teaches-claim (content-addressed identity grounds byte-pins) is exactly what the snapshot's first sentence says |
| gnu.org Bash manual Comments/Exit-Status pages (standing reject, r34/r35, re-affirmed r36) | reject | re-fetched both URLs this closure: `curl --max-time 60` → both timed out at 60.001 s (http=000), same class as r32/r34 receipts | agree | still unreachable from this host; the reject reason (unreachable + scope already tier A at S097) stands; no row was written, consistent with the r36 lesson Gate's "Rejected this round: none … not re-tried" |

`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` run by this closure: exit 0, final line `tameshi ok …/corpus/SOURCES.md` (W04 duplicate-URL warnings on other rows only; none touch S103).

## Trend verdicts

- **expansion: improved** — rows 99 → 100 re-measured (monitor sources block, base↔tip); S103 opened, tier A, mined into the round's own evidence the same round (used-by resolves).
- **quality: improved** — the r35-disclosed v1 predicate defect is real in the frozen v1 source and is closed by v2 (mutant FAIL, deciding PASS, pins verified); the r35 dead-LOG-pointer defect is corrected append-only and backed by new criterion 72 (verified in the QUALITY diff); the four drifted headings are re-anchored with disclosed scope.
- **discernment: improved** — both r35-closure disagreements (dead pointer; predicate defect) became lesson-backed fixes this round (`## Mistakes` names captured-by; criterion 72 lands behind it). No disagreement left unlearned.

## Routed defects / notes for the lane

1. (minor, status-neutral) The emptied-panel mutant commit `91373d55…` cited in the two control receipts was created in a scratch clone and is not reachable from the lane repo. The receipts are committed, coherent, and name the revision measured, and the mutant is reconstructable from the committed sealed panel — but a future control should commit the mutant tree (or its spec) so every input pointer resolves at closure time (PROTOCOL §Evidence standard).
2. (note for operator) SHONEN boxes remain all `[~]` lane-asserted with no named non-author verifier; the four boxes look mechanically checkable by a non-author in a future closure — promotion is operator-owned, no action taken here.
3. (disclosed, not a defect) The two v1 waves (w1 build 39, w2 falsify 39) are prepared-but-undispatched: specs validate under policy v1 (band 32–64; 39 tasks each, stderr empty), dispatch records carry the validator's taskCall, but 0 seats ran this seat (host surface: no dispatch tool). Orchestrator dispatch expected between rounds.
4. (planned, confirmed) `code_view` ANSI-C quote class stays routed to round 37 with freeze-before-data + re-pin; the reason (editing `tools/tally-audit-v3.py` would void three pins) is recorded in contract.json, SCORECARD, and the lesson Holds.
