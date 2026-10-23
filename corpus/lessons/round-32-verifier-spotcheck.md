# Round 32 — verifier spot-check (tameshi)

author: hyaku closure (non-author integrator, @m_opus)

Scope: tameshi round 32 (L1 `TameshiR32`, attempt 1). Base `e24688b2ff6cca1c9ad20e112f02c629b8597ff8`,
head `6706bbd67835f8cc63ab47c434aba2151bc59377`; measurement revision `24a5a5bb598ae919546715267d76f814efaf8912`.
Fleet report `.ufo/reports/round-32/tameshi.md` at fleet commit `ae7994259ae73af2de164ebbcc3c2bb7e973e7b4`.

Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-23T07:24:57-03:00 launch tameshi round=32 pgid=66510 driver=hyaku-inline attempt=1`;
`2026-10-23T09:18:26-03:00 complete tameshi round=32; hyaku-inline attempt=1`.

Every check below was run by this closure over committed bytes unless marked *evidence-verified*
(a lane receipt read, not re-executed: PROTOCOL §Gate standard, Closure consequence). No seats were
dispatched by this closure; no tool was installed.

## Conformance (step 1)

| Check | Command | Observed |
|---|---|---|
| Report landed by the lane | `git log --format='%an %H' -- .ufo/reports/round-32/tameshi.md` | `tameshi-shokunin ae7994259ae73af2de164ebbcc3c2bb7e973e7b4` |
| `SHONEN` heading, one line per box | read report `## SHONEN` vs `SHONEN.md` | 4 lines, 4 boxes, all `[~]` with pointers |
| Cited hashes exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for c3181497 e9f3b957 b50a18f0 528f8dee a4f71813 21f7de32 4b529ee9 24a5a5bb 29712da5 6706bbd6 36c1d393 08125328 67c0e013 | 13/13 `anc=yes` |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain` | `local=remote=6706bbd6… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty |
| Prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/tameshi-round-32.md) templates/round-prompt.md` | 22 differing lines, every one a `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitution; §1–§5 and the five child-lane items present; no L2 route map quoted |
| Report sections | read | work, landed changes (each tied to LOG Round 32), before→after with commands, Sources & frontier, Trend verdicts, SHONEN, stale-lane, installs: present |

Status: **ok** (real report naming checkable committed work). Conformance defects (status-neutral):
see "Defects" below.

## Claim C1 — operability, capability acquisition (measured): MISS confirmed

Declared predicate (`v2/contract-amendment-1.json` `predicate`, identical sentence in the counter docstring
lines 17–23, code condition `ok = …` at counter lines 394–396, label `C1_R32V2_PASS` in the receipt): every
v1 copy (18 kill + 8 accept) and every valid held-out copy right, ≥6 of each held-out kind, tool sha pinned,
runner sha pinned, held-out files added after the freeze. Kill rule: the first full v2 run at the
measurement revision decides; false is a miss, never re-scaled, re-seeded or amended.

Re-derivation over the committed receipt (`git show 6706bbd6:.ufo/evidence/round-32/after/c1v2-at-measurement.stdout`):

| Quantity | Command | Observed | Reported |
|---|---|---|---|
| held-out kill | `grep -c 'src=ho set=kill .*outcome=KILL'` / `grep -c 'src=ho set=kill '` | 1 / 10 | 1/10 |
| held-out accept | same with `set=accept … outcome=ACCEPT` | 8 / 12 | 8/12 |
| v1 kill / accept | `grep -c 'src=v1 set=kill .*outcome=KILL'`, `… accept … ACCEPT` | 18, 8 | 18/18, 8/8 |
| summary line | last line | `… ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=63d2e2e95a1e35c5 rev=24a5a5bb… C1_R32V2_PASS=false` | same |
| held-out set size | `git ls-tree -r --name-only 24a5a5bb -- .ufo/evidence/round-32/heldout \| wc -l` | 22 (authors Guard, Loop, Printf, Refactor, TallyArms; none from the three dead seats) | 22 from 5 completed authors |
| tool bytes | `git show <rev>:tools/tally-audit.py \| sha256sum` at 24a5a5bb and 6706bbd6 | `9639c458…99ef` both | amendment-2 pin `9639c458…99ef` |

Nothing re-scaled, re-seeded or amended after the run: `git diff --stat 24a5a5bb 6706bbd6 --
.ufo/evidence/round-32/v2 .ufo/evidence/round-32/heldout tools/tally-audit.py .ufo/evidence/round-32/c1-measure.py
.ufo/evidence/round-32/contract.json tools/mutate-and-run.sh` → empty. The 23 files changed after 24a5a5bb are
receipts, residual reports, LOG, SCORECARD (append) and the lesson. `git grep 'C1_R32V2:' 6706bbd6 -- . ':!*.md'`
finds exactly one real-tool receipt line (the measurement); counter history: only b50a18f0 and 528f8dee touch
the counter, both before 24a5a5bb. Reproduction is *evidence-verified*: `res/RerunV2.md` (fresh seed
`ad89611c…` and the L1's seed, exit 1 each, 0 of 22 held-out outcomes differ); `res/CriticMeasurement.md`
rules a miss. Verdict: **miss**; no capability row enters (SCORECARD agrees).

### §9 weighing (addendum §9, "Claim sizing")

1. **v1 redesign before data — conformant.** CriticC1's 27-line allowlist met frozen v1
   (`w1/CriticC1.md:93,103`: `kill=18/18 accept=8/8 … C1_R32_PASS=true`, two seeds) before any real-tool data;
   §9 says a counter a shortcut meets is fixed before data. Amendment 1 (`b50a18f0`) is that fix.
2. **Amendment 2 (`528f8dee`) — not a change to the claim's rule, but disclosed data preceded it.** It changed
   the constant `TOOL_SHA256` (158202f8 → 9639c458) and hardened the counter (copy-order side channel, seed
   check); the predicate sentence and kill rule are unchanged. Data before it: DeterminismProbe's v1 runs on
   working tool bytes (outside its item; v1 had already stopped being the claim's rule at amendment 1) and the
   L1's dev sweep on the public v1 families. No v2 run on real tool bytes predates it (`w2/ReviewAmend2Facts.md`
   (a), absence-of-receipt) and the held-out set did not yet exist. Ruling: under §9's "a rule changed after any
   seat has scored is not the claim's rule", no seat had scored under the rule in force (v2), so amendment 2
   stands as the claim's rule. Immaterial to the outcome either way: under amendment-1 constants the tool at
   24a5a5bb (`9639c458`) fails `tool_sha_ok`, so the claim is false under both readings.
3. **Declared v2 control re-score ran after the first v2 run — deviation.** Amendment 1
   `controls_before_data` required it before the L1's first v2 run; it ran afterwards
   (`res/CtlV2Controls.md:5`: all four controls `C1_R32V2_PASS=false`; embedded allowlist `ho_accept=0/12`).
   The controls are observations, not pre-data evidence. Status-neutral; routed. It cannot have inflated a miss.

## No harm (owned axes depth, calibration; operability is the claim axis)

| Check | Command | Observed |
|---|---|---|
| Runner byte identity | `git show <rev>:tools/mutate-and-run.sh \| sha256sum` at e24688b2, 24a5a5bb, 6706bbd6 | `a7d3f2dd…2eb9` ×3 |
| SCORECARD append-only | `git diff e24688b2 6706bbd6 --numstat -- SCORECARD.md` | `56 0`; depth 9 → 9, calibration 8 → 8 |
| Other lane files | `--numstat` LOG.md / SOURCES.md; `--stat` SKILL.md PROVINCE.md corpus/QUALITY.md | LOG `26 0`; SOURCES `18 1` (S094 used-by cell); SKILL, PROVINCE, QUALITY untouched |
| Cold-read monitor | receipts `after/c1monitor-at-24a5a5bb`, `-at-29712da5`, `before/c1monitor-at-base` (*evidence-verified*) | `covered=64/64 restraint=8 box3_mismatch=0 depth_score=9`, exit 0, all three |
| Cold-read ledger | `jq length` on `.ufo/evidence/round-21/coldread/ledger.json` at e24688b2 / 6706bbd6; prefix test in python | 480 → 493; base entries an exact prefix (`prefix_equal True`) |
| Command D | `after/commandD-at-24a5a5bb.{stdout,exit}` (*evidence-verified*) | `recorded_cases=9 depth_score=9`, exit 0 (base receipt identical) |
| Census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (run by this closure) | 8 W04 duplicate-url warnings, `tameshi ok`, exit 0; `cmp` start vs end receipts identical; rows 94 → 96 by the CORPUS row counter |

### Round-31 repairs (routed by `round-31-verifier-spotcheck.md`)

- Counter v2 header: `repair/c1-r31-measure-v2.py:122` tests `header[1] == 'Score (0–10)'` (exact). ✔
- Byte-level append-only: lines 207–209 read both SCORECARD blobs with `subprocess.run(..., capture_output=True)`
  (no `text=`, so bytes) and test `rev_b.stdout.startswith(base_b.stdout)`. ✔ Same verdicts as v1 at 36c1d393
  (7 mismatches) and 08125328 (0): `w1/RunCounterV2.md:110-111` (*evidence-verified*).
- Base monitor receipt: `repair/c1monitor-at-r31-base-36c1d393.stdout` `covered=64/64 restraint=8`, `.exit` 0. ✔
- Command D exit files: `repair/commandD-at-r31-67c0e013.exit` and `…-final-08125328.exit` both 0, stdout
  `recorded_cases=9 depth_score=9`. ✔

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | unchanged | C1 missed its frozen predicate; tool landed but no capability admitted |
| depth | unchanged | 9 → 9; command D 9; monitor 64/64 |
| calibration | unchanged | 8 → 8; SHONEN marks unchanged |
| coverage | unchanged | one entry on held core ground; no frontier move |
| freshness | unchanged | S094 re-opened at the same digest; recheck 730d → 730d |
| adjacency | unchanged | no sibling ground touched |

Admission: **not admitted** — the only claim missed; no axis harmed. Verdict `rejected-honest-stop`.

## Discernment spot-check (LEARNING.md)

Sample from `corpus/lessons/round-32.md` `## Gate`, re-opened by this closure on 2026-10-23:

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S097 Bash 5.3 `bashref.texi` | admit | `curl` of the cgit URL at id `b8c60bc9…` → HTTP 200, 415804 bytes, sha256 `f3d37d57…32d5` | agree | digest equals the row; line 3896–3897 reads "Exit statuses fall between 0 and 255, though, as explained below, the shell may use values above 125 specially." (19 words ≤ 25); `case` quote at 1081–1082 also verbatim; tier A docs fits a primary manual source |
| S099 pitest.org | admit | `curl https://pitest.org/` → HTTP 200, 12023 bytes, sha256 `b0c7e050…10cc` | agree | digest equals the row; HTML line 114: "The quality of your tests can be gauged from the percentage of mutations killed." (14 words ≤ 25); `used-by` now names only the entry, which cites it |
| S098 Bash manual Conditional-Constructs page | reject (no row) | `curl -m 40 https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html` | agree | still `curl: (28) Connection timed out`; CORPUS rule 1 forbids a row for an unopened source, and the rule it would teach is covered by S097's pinned bytes |
| Counter v1 | reject (before data) | `.ufo/waves/round-32/w1/CriticC1.md:93,103` | agree | the allowlist that runs no tally prints `C1_R32_PASS=true` on two seeds: v1 could not distinguish a shortcut |

New rows checked: S097 and S099 (above); S094 touched-row `used-by` change matches the lesson table.
Census validate: exit 0 (above).

## Trend verdicts

- **expansion: unchanged** — one new knowledge entry (`corpus/knowledge/runner-tally-audit.md`) on ground the
  lane already held; no frontier row moved; no capability admitted.
- **quality: unprovable-but-better** (this closure is the named non-author reviewer) — the four routed round-31
  defects landed with receipts verified above; 13 drifted-section cold reads were re-bound and appended
  without rewriting the ledger prefix; S094 re-verified at its pinned digest; no admitted entry failed a
  re-check. Not `improved`: no entry was superseded by a stronger one and the tool itself measured incomplete.
- **discernment: improved** — the spot-check agrees with the gate on 2 admits and 2 rejects; the gate rejected
  its own counter and its own first tool freeze before data, and the sealed held-out design converted a
  0-miss dev sweep into a measured miss.

## SHONEN (operator note)

All four boxes stay `[~]` with lane-assertion pointers; none is fully checkable by a non-author from this
round's evidence (no independent promotion verifier named). Promotion stays operator-owned.

## Defects (status-neutral) and routed items (lane fixes next round)

1. Declared pre-data step skipped: amendment-1 `controls_before_data` ran after the first v2 run (lesson
   Mistake 7). Route: the next counter refuses to run unless a committed control receipt naming its sha exists.
2. Seat ran outside its item: DeterminismProbe ran counter v1 on working tool bytes; a round-scoped data run by
   any seat must be logged before any re-pin. Route: wave context forbids counter runs on tool bytes outside the item.
3. Measurement `.exit` is a hand-written note (`c1v2-at-measurement.exit-note.txt`: the chained `echo $?` did
   not run). Corroborated by three RerunV2 exits, but route: capture exits with `cmd; echo $? > f`, never `&&`.
4. Counter v2 defects from `w2/ReviewCounterV2.md`: unquoted `witness.loop` names reach bash, non-string
   block witness crashes, held-out discovery not recursive — fix in the next counter.
5. Tool v2 (new file) for the held-out failure classes (3–8 failing/setup legs, statuses beyond the
   per-position list, stress on the wrong loop, second extraction line), measured on a fresh sealed set.
6. Carried queue (lesson routed 5–6): MutCounter M07/M08, dead-seat threshold, binding v5 FA-1..FA-3,
   QUALITY 69/71 errata, `mte-interop.py` SETUP, S055 digest drift.
7. Dead seats HeldOutFree, HeldOutHarnessVectors, HeldOutHarnessCmp (`code=cyber_policy`): not retried, files
   unused (confirmed: no held-out file from those authors). Route: held-out author prompts without "defeat"
   wording.
