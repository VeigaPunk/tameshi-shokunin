# LessonEvidence — round 12, wave w2 (tameshi-r12-w2)

Seat: LessonEvidence (scribe, leaf). Read-only except this report. No checks, builds or tests were run. No installs or updates. No routing, config, or model edits. Nothing here is an independent admission, promotion, or non-author verification.

Snapshot caveat: the tree is live. `w2/swarm-registry.json` was rewritten at 00:43:50 (-03) with spawned agentIds; my first read at ~00:43 showed `agentId: null` (`w2/swarm-registry.json:160` now `TameshiR12.LessonEvidence`). Git state below is as observed at read time.

Axes named: (1) inherited-work resolution, (2) wave32 routing roles, (3) independent-review status. Every claim is O (observed, path:line), I (inference), or U (unknown).

## 1. Inherited-work resolution (findings)

F1 [O] Round-1 admission hold is still open. `LOG.md:464-465` "Formal admission is **blocked**"; `LOG.md:467-472` names the unblock list. `corpus/lessons/round-1.md:225-243` (ER-I1) repeats it. The 2026-10-19 close does not record that the hold was lifted; `LOG.md:551-644` only adds the orchestrator adjudication.

F2 [O] Round-1 route-binding evidence names aliases that the current host table no longer uses. `LOG.md:429-433` and `corpus/lessons/round-1.md:225-227` cite `@m_composer`, `@m_grok`, `@m_antigravity`, `@m_zfl`. The 2026-10-19 host ruling at `scripts/hyaku/lane-addendum.md:45-49` uses `m_flash`, `m_antigravity`, `m_haiku`, `m_opus`, `m_luna`, and says `m_zfl` is parked. No record says the older binding requirement is superseded. [I] The hold is still formally valid for the old route check, and the record does not reconcile it.

F3 [O] Round-1 box-3 pin and calibration. `LOG.md:637` re-pins calibration at 6 by orchestrator adjudication, after the kaika review recommended 8 (`.ufo/waves/kaika-w3/tameshi-review.md:16`). `LOG.md:639-642` applies the review's conditions 1-3 (F1/F2 `partly held`, quality trend `unchanged`, K2 pointer to census v2). Condition 4 (spot-check) is handled by `corpus/lessons/round-1-verifier-spotcheck.md`.

F4 [O] SKILL.md pin has drifted in the working tree. `LOG.md:570` and `:618-620` and `corpus/lessons/round-1.md:327` pin `SKILL.md` to sha256 `33e3009c…`. HEAD `18ad5d0` matches (`git show HEAD:SKILL.md | sha256sum` → `33e3009c`). The worktree is `593dfe58`, because of an uncommitted round-12 append starting at `SKILL.md:1479` (`## Repeated controls and gate registry — round 12`). `LOG.md:606` says round-1 deliberately left SKILL.md untouched "so the cold-read binds to its bytes". That binding now holds only for HEAD bytes. Any box-3 or cold-read claim must cite HEAD `33e3009c`, not the worktree.

F5 [O] Round-12 lesson says "No inherited uncommitted work was present" (`corpus/lessons/round-12.md:38`; `LOG.md:658`). This is true at census time. The current worktree is dirty: `M LOG.md`, `M SKILL.md` (+40), `M corpus/QUALITY.md` (+16), `M corpus/README.md` (+20), `M corpus/SOURCES.md`, `M corpus/knowledge/witness-scoped-kill-verdict.md` (+3), and untracked `corpus/knowledge/repeated-control-precondition.md`, `corpus/lessons/round-12.md`, `tools/repeat-control.py`, `tools/bash-witness-study.py`, `.ufo/waves/round-12/`, `.ufo/evidence/round-12/`. The authoring seat for each file is not recorded in `LOG.md`. U: whether all of these are this round's intended writes.

F6 [O] Stale internal claims in the round-12 lesson. `corpus/lessons/round-12.md:30-32` says "Runtime receipts appended below." The 50-line file has none. `LOG.md:663` defers measured revision and claim commands "after runtime verification". Treat as pending, not as evidence.

F7 [O] Role-floor deviation was superseded but not removed. `corpus/lessons/round-12.md:36` records the w1 deviation. `:40-42` supersedes it with the host ruling. `.ufo/waves/round-12/w1/ClaimSkeleton.md:3-5` still says "explicit role-floor deviation". This is historical and should stay append-only.

## 2. Wave32 routing roles (w2)

Roster (32 seats, identical across `spec-w2.json` items, `dispatch-w2.json` `taskCall.tasks[].agent`, `dispatch-w2.json:25-218` registry, and `w2/swarm-registry.json:7-200`; all 32 names match across all four sources):

| role | seats | count |
|---|---|---|
| executor | ControlFinish, WitnessFinish, KnowledgeFinish | 3 |
| scout | ControlSources, WitnessSources, FlakySources, PriorMistakes, EvidenceCensus, InstructionScope | 6 |
| connector | ScopeConnector, ClaimsConnector, FrontierConnector | 3 |
| reviewer | ControlFlow, ControlSnapshot, ControlSelftest, WitnessParser, WitnessIntegrity, KnowledgeSupport, SourceLedger, ScoreRubric | 8 |
| critic | ControlCritic, WitnessCritic, AdmissionCritic, InheritanceCritic | 4 |
| scribe | ReportEvidence, LessonEvidence, CapabilityEvidence, SHONENEvidence | 4 |
| sentinel | ControlSecurity, WitnessSecurity | 2 |
| mutation-tester | RedBefore | 1 |
| revenger | IntentDataWalk | 1 |

Findings:

R1 [O] LessonEvidence is `scribe` in all four sources: `spec-w2.json:132-136`, `dispatch-w2.json:357-360`, `dispatch-w2.json` registry (LessonEvidence member), `w2/swarm-registry.json:158-163`.

R2 [O] No planner seat, consistent with the validator and host ruling. `scripts/hyaku/lane-addendum.md:41-44`: L1 holds the canonical planner seat; a bounded data walk may ride a scout, connector or revenger. Here `IntentDataWalk` (revenger, `spec-w2.json` item) carries the data walk.

R3 [O] Session routing matches the host table for all 32 seats. I read `cfg://task/agentModelOverrides` this turn. Session values: executor/labrat `@m_flash`; scout/connector `@m_antigravity`; reviewer/scribe/simplifier/distiller `@m_haiku`; critic/sentinel `@m_opus`; planner/revenger/mutation-tester `@m_luna`; task/main `@m_strong`. Host table `scripts/hyaku/lane-addendum.md:45-49` gives the same bindings for every w2 role. Result: executor 3, scout+connector 9, reviewer+scribe 12, critic+sentinel 6, revenger+mutation-tester 2 — all match. Caveat: observed once at read time; spawn-time binding is unverified.

R4 [O] Global config disagrees with both the host table and the session value. `~/.omp/agent/config.yml:118-133` sets almost every role to `@m_flash` (critic, planner, main to `@m_strong`). Those 29 seat-role bindings (connector, critic, mutation-tester, revenger, reviewer, scout, scribe, sentinel) differ from `lane-addendum.md:45-49`. The host says seat models "come from this session's `task.agentModelOverrides`" (`lane-addendum.md:45-46`), so the session value governs. Record that precedence explicitly. U: whether the session override was set by a source the host table did not cover.

R5 [O] Mix vs host guidance. `lane-addendum.md:49-51` says "for 48 lanes roughly 14 executor, 8 scout, 4 connector, 8 reviewer, 4 scribe, 6 critic, 2 sentinel, 2 revenger". w2 has 3 executors and no proportional allocation to executor. The host uses "roughly" and does not list mutation-tester. This is an observed deviation, not a violation. Report it; do not reroute.

R6 [O] Payload shape. `dispatch-w2.json` `taskCall.tasks[]` keys are only `agent`, `name`, `task`. No `model` parameter (complies with `lane-addendum.md:49-52`). Lane-bounds line and report path appear in all 32 task texts (`Lane bounds: leaf member`; `Report: write your scoped findings to .ufo/waves/round-12/w2/…`). The tooling directive does not appear in `taskCall` task text or in `spec-w2.json` prompts, though `spawn-w2.json` contains it (`spawn-w2.json:15-16,49-50`). U: which payload was actually sent to the task call.

R7 [O] Registry counts: `dispatch-w2.json` `counts` = spawn 32, resume 0; `policy.maxLanes` 32; `spec-w2.json` 32 items. Matches the one-batched-call rule (`dispatch-w2.json` `note`).

## 3. Independent-review status (honest)

I1 [O] No independent promotion review exists for round 12. `corpus/lessons/round-12.md:24` and `:42` say the outside admit/reject spot-check "remains the external closure duty" and "independent round admission" is not claimed. The w2 spec says reports are "advisory, not independent non-author admission/promotion" (`spec-w2.json` `context`). `SHONEN.md:5-12`: all four boxes are `[~]` lane assertions, each labelled "no independent promotion verifier".

I2 [O] Round-1 outside-review status is recorded in conflicting ways. Quoted verbatim for the judge:
- `corpus/lessons/round-1.md:132-133`: "Spot-check result — NOT performed [O]. No non-author of this lane's gate decisions spot-checked the admits/rejects this round".
- `corpus/lessons/round-1.md:207-212` (ER-I1): "`unprovable` is not the canonical verdict token. Current discernment is **unprovable-but-better**... no outside spot-check of one admit and one reject exists."
- `LOG.md:607-612`: "Verdicts are self-verdicts pending the orchestrator's non-author verification... discernment pending the non-author spot-check."
- `corpus/lessons/round-1-verifier-spotcheck.md:8-17`: a table of one admit and one reject, both `agree`, by `W3ReviewTameshi`; "Verifiers were fresh agents dispatched by the orchestrator"; line 17 says "discernment improved" and "re-pinned at 6".
- `.ufo/waves/kaika-w3/tameshi-review.md:3`: "Reviewer: `W3ReviewTameshi` (fresh orchestrator-dispatched task; non-author)". Its Section 5 (`:149-159`) records 2 admits and 3 rejects, all `agree`, and states "discernment — lane: pending → recommended: improved, provisional". Its sample is not identical to the spotcheck table: review rows 1-5 are witness-scoped (admit), mutation-score-semantics (admit), S029 (reject), S046 (reject), Timeout rule (reject); spotcheck table (`:12-13`) cites witness-scoped + mutation-score-semantics (admit) and S046 + S029 (reject) and omits the Timeout row.

I3 [O] Authority of W3ReviewTameshi is contested by the repo's own rules, which I did not resolve. `LEARNING.md:42-45`: a non-author "a fresh reviewer or the operator" spot-checks; "A subagent the lane dispatched is still the lane." `kimi-shokunin/.../PROTOCOL.md:63-68`: only a non-author `<id>` may write `[x]`. The review states it was orchestrator-dispatched (`tameshi-review.md:3`); `corpus/lessons/round-1-verifier-spotcheck.md:3-6` says the same. The name `W3ReviewTameshi` and `AdmissionBounds.md:79-80` (w1) treat the seat as a lane-named reviewer. **Judgment reserved for the canonical Rust judge.** This seat does not decide it.

I4 [O] Conditions carried by the kaika review are not listed in the round-1 spotcheck file. `tameshi-review.md:11-15` lists four conditions (trend relabel; F1/F2 `partly held`; SCORECARD pointer text and K2 census name; spot-check result). `round-1-verifier-spotcheck.md` says "ADMITTED after post-review fixes" and omits the conditions. `LOG.md:639-642` shows conditions 1-3 applied.

I5 [O] Discernment token is unreconciled across records: `unprovable-but-better` (`round-1.md:207-212`, `LEARNING.md:29` vocabulary); `improved, provisional` (`tameshi-review.md:123`); `improved` (`round-1-verifier-spotcheck.md:17`); `pending` (`LOG.md:611-612`). The canonical token and the status of the outside check must be stated once by the owner.

## 4. Proposed addendum wording (for the lane owner to append; not written by me)

Append-only block for `corpus/lessons/round-12.md` (new ER entry; do not edit existing lines):

> **ER-12-A1 — inherited-state, routing and independent-review addendum (wave tameshi-r12-w2, 2026-10-20).**
> 1. *Inherited work.* Round-1 admission hold (`LOG.md:464-472`, `corpus/lessons/round-1.md:225-243`) is not lifted by this round. Its route-binding requirement (`@m_composer`/`@m_grok`/`@m_antigravity`/`@m_zfl`, `LOG.md:429-433`) is superseded for routing by `scripts/hyaku/lane-addendum.md:45-49` (2026-10-19 host ruling); the hold text itself is not rewritten. The calibration pin is 6 (`LOG.md:637`). Box-3 and cold-read claims bind to SKILL.md sha256 `33e3009c` at HEAD `18ad5d0`; the working tree (`593dfe58`, round-12 append at `SKILL.md:1479`) is not that pin. Uncommitted round-12 files are listed in `git status` and not yet attributed to seats.
> 2. *Routing.* Wave tameshi-r12-w2 has 32 seats: executor 3, scout 6, connector 3, reviewer 8, critic 4, scribe 4, sentinel 2, mutation-tester 1, revenger 1; no planner (validator forbids it). L1 holds the planner function; `IntentDataWalk` is the bounded data walk (`lane-addendum.md:41-44`). Observed session `task.agentModelOverrides` matched the host table for all 32 seats at read time; the global `~/.omp/agent/config.yml:118-133` differs and is not the governing value per `lane-addendum.md:45-46`. Mix is below the host's "roughly" guidance for executors (3 of 32); recorded, not rerouted.
> 3. *Independent review.* No round-12 independent admission or promotion review exists; the outside admit/reject spot-check remains open (`round-12.md:24`). Round-1 has two non-equivalent records: the 2026-10-15 "NOT performed" (`round-1.md:132-133`, ER-I1) and the 2026-10-19 orchestrator-dispatched `W3ReviewTameshi` spot-check (`round-1-verifier-spotcheck.md:8-17`, `kaika-w3/tameshi-review.md:149-159`), whose authority under `LEARNING.md:42-45` is undetermined here and reserved to the canonical judge. The discernment token is `unprovable-but-better` until a named non-author judges otherwise. Conditions in `tameshi-review.md:11-15` are recorded as applied only where `LOG.md:639-642` shows.

Do not write: "independent review passed", "discernment improved" without the judge's ruling, or any `[x]`.

## 5. Conflicts verbatim (for the canonical Rust judge)

- "NOT performed [O]" — `corpus/lessons/round-1.md:132`
- "unprovable-but-better" — `corpus/lessons/round-1.md:208`
- "discernment pending the non-author spot-check" — `LOG.md:612`
- "discernment improved" — `corpus/lessons/round-1-verifier-spotcheck.md:17`
- "improved, provisional (agree)" — `.ufo/waves/kaika-w3/tameshi-review.md:123`
- "fresh orchestrator-dispatched task; non-author" — `.ufo/waves/kaika-w3/tameshi-review.md:3`
- "A subagent the lane dispatched is still the lane" — `LEARNING.md:45`

## 6. Out of scope / debts / unknowns

- Repo-wide owners of the 14+ uncommitted round-12 files (F5) — U.
- Live spawn-time routing for this wave (R3 is one read) — U until the route owner observes it at spawn.
- Whether `IntentDataWalk` or `MistakeMining` is the data walk in the round record (w1 names MistakeMining; w2 names IntentDataWalk) — both are revenger per their records; not contradictory, but the record should name the current seat.
- Sibling `.ufo/evidence/round-12/LessonScribe/outline.md` (dated 02:16Z) is an earlier, unfinished outline; not used for claims here.
- Old model aliases in `LOG.md:429-433` and `corpus/lessons/round-1.md:225-227` remain historical; left untouched per append-only rule.

## 7. Tooling

None installed or updated. No model parameters or routing edits. No checks run. Report written only to `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/LessonEvidence.md`.
