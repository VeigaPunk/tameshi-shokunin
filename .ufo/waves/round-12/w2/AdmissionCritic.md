# AdmissionCritic — round 12 w2 (critic seat, advisory, lane-internal)

The lane dispatched this seat, so it counts as the lane (`kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:63-65`). It does not admit, reject, pass, promote, or verify independently.

**What I did:** read-only. I read files, ran `git status`/`diff`/`log`, `stat`, `sha256sum`, and parsed JSON. No builds, tests, or checks were run.

**Repo state:** lane HEAD is `18ad5d0`. Working tree state was observed from 2026-10-20 00:41 to 00:50 (-03:00). L1 was editing during that time: `SKILL.md`, `corpus/QUALITY.md`, and `corpus/README.md` changed at 00:44.

**Installs:** none.

**Axes named:** admission authority, role/planner mapping identity, provenance of declarations and evidence, and the six AXES axes (`AXES.md:9-16`).

## Verdict summary

The authority boundary is stated correctly. The lane keeps admission outside the lane, and no `[x]` is claimed:
- `corpus/lessons/round-12.md:24`
- `claims.json` `authority`
- `corpus/README.md` (new block, last paragraph)

The defects are in **identity and provenance**: who did the planning, which waves exist, and which evidence exists. They are not in the authority claim itself. All the corrections below are append-only and small.

## Findings

### F1 — False provenance: "MistakeMining supplied the revenger data walk" (high)

Where the claim appears:
- `corpus/lessons/round-12.md:42` and `LOG.md:658` state it.
- They also recast ClaimSkeleton as "supplemental reviewer analysis".

Counterexample, from the w1 spec (`.ufo/waves/round-12/spec.json`):
- The MistakeMining item (revenger) asks for "Mine previous partly contaminated witness preregistration and outside box3 overclaim into one class/evidence/captured-by/fix candidate. Design demonstrably failing counterexample…". That is mistake mining plus a fixture. It is not a planning data walk.
- Its own report (`w1/MistakeMining.md:1-3`) describes "lane-local evidence mining only".
- The ClaimSkeleton item (reviewer) literally says "Planner seat function (validator forbids planner taxonomy): scrutinize C1/C2 data walk…".
- Its report (`w1/ClaimSkeleton.md:3-5`) says "This is an explicit role-floor deviation; the exact planner seat is not claimed as met".

Why it matters:
- The host ruling lets a planning data walk ride only a **scout, connector or revenger** item (`scripts/hyaku/lane-addendum.md:41-44`; `.ufo/l0-questions.md:52-53` L0 answers).
- In w1, the planning data walk rode a **reviewer**. That carrier is not permitted.
- The w1 text after the ruling relabels both seats after the fact, which is an identity change.
- w2 does conform: `IntentDataWalk` (revenger) carries "Bounded planning data walk" (`spec-w2.json`).

Smallest correction: append to the lesson and the LOG. Rewrite nothing.
- **w1:** L1 held the canonical planner seat. The bounded planning data walk rode ClaimSkeleton, a reviewer. That is a non-conforming carrier under addendum:41-44, so it is disclosed, not cured.
- MistakeMining did mistake mining and the counterexample fixture, not planning.
- **w2:** L1 is the planner. IntentDataWalk (revenger) carries the bounded planning data walk, which conforms.

Impacted axis: calibration (SCORECARD/LOG must match repo state, `AXES.md:15`).

### F2 — Stale wave identity: "One validated 32-seat batch" (high)

Where: `LOG.md:658` and `corpus/lessons/round-12.md:36`.

Counterexample:
- A second validated wave exists: `.ufo/waves/round-12/spec-w2.json`, `dispatch-w2.json` (taskCall with 32 tasks), `record-w2.json`, `spawn-w2.json`, `assignments-w2.json`, and `w2/swarm-registry.json` (createdAt `2026-10-20T03:43:05Z`).
- LOG:658 also cites `{spec,dispatch,assignments,record-result}.json` only.

Correction: append the actual counts.
- Two waves of 32 seats, 64 members in total, within the ≤100 limit.
- w1 role mix: 8 reviewer, 7 scout, 4 scribe, 3 executor, 3 connector, 3 critic, 1 each of revenger, sentinel, simplifier and mutation-tester.
- w2 role mix: 8 reviewer, 6 scout, 4 critic, 4 scribe, 3 executor, 3 connector, 2 sentinel, 1 mutation-tester, 1 revenger.
- Cite the w2 files.

### F3 — Attempt identity: w1 and the declarations belong to the dead headless attempt (medium; InheritanceCritic owns the details)

Timeline (`.ufo/watchdog.log`):
- :405 — attempt 1 launched at 23:10:59.
- :408 — attempt 1 ended with `lane-dead-no-report` at 23:24:27.
- :411 — the inline attempt launched at 00:41:11.

The w1 registry was created at 02:13:06Z, which is 23:13 local. Files authored in the 23:14–23:24 window include `claims.json`, every `w1/*.md`, `corpus/lessons/round-12.md`, `LOG.md`, `corpus/SOURCES.md`, the knowledge entry, and `tools/repeat-control.py`.

So these statements are true only for attempt 1, not for the resumed attempt:
- "clean at round start" (`lesson:3`)
- "No inherited uncommitted work was present" (`lesson:38`, `LOG.md:657`)

The addendum requires that inherited work be re-verified and named (`lane-addendum.md:17-20`). Correction: append the inheritance disclosure. All seats from both attempts remain lane seats, so this does not change authority.

### F4 — Declaration freeze proof is weaker than claimed (medium)

The claim: the lesson Mistakes row requires "freeze declaration before execution" (`lesson:31`).

The evidence against a pre-execution freeze:
- `claims.json` (sha256 `fe4b7da8…99caa`) was last modified at 23:14:33. That is 87 s after w1 dispatch began (02:13:06Z).
- It is untracked, and no file in `.ufo/` pins its digest.
- The only declaration written before dispatch is the `spec.json` context (mtime 23:13, `# Goal` C1/C2 text). It has no `after_acceptance` or `score_delta` fields.
- mtime is weak evidence. [INFERENCE] The acceptance wording was most likely written before any seat output: the first w1 report has mtime 23:14:34. But the repo cannot prove that.

Correction: append a note in the LOG.
- The earliest frozen declaration is the w1 `spec.json` context, dispatched unchanged in `dispatch.json`.
- `claims.json` was finalized after dispatch, at the recorded sha256.
- C2's integrity freeze is `BashWitness/declaration-hash.txt`, not `claims.json`.

### F5 — Claim typing and axis attribution (medium; a tradeoff the judge must see)

Four problems:

1. **`claims.json:9` says "both worked".** C1 cannot register on the calibration rubric: command C counts SHONEN `[~]` marks (`SCORECARD.md:67,213-220`). C2 carries the lowest-axis obligation, because depth is tied at 6 (`w1/AdmissionBounds.md:30-33`). This is not corrected anywhere yet.

2. **C1 is labeled `axis: calibration`** (`claims.json:6`, `lesson:3`). But a repeated-control gate is a runnable artifact, which is operability (`AXES.md:13`), or a capability (`AXES.md:40-41,62-64`). Calibration is "self-assessment quality … SHONEN.md/SCORECARD entries match observed repo state" (`AXES.md:15`).
   - Counterexample: reporting "calibration improved" from C1 would raise the discernment trend (`AXES.md:21-22`) using a measure the calibration rubric never moved.
   - Correction: give C1 its per-axis verdict as calibration **unchanged** (rubric 6→6). Report its gain as a capability row, entered only with a passing demonstration in the round report (`AXES.md:62-64`). If the label stays "calibration", the report must say the label is lane policy and that no calibration rubric moved.

3. **C2 type "measured evidence deepening"** (`claims.json:7`) is not an AXES claim type. Type it as an axis-move (depth). The counter is 0→10 classified defects on the BashWitness summary. The pre-registered falsifier is `corpus/README.md:79`, as already advised at `w1/AdmissionBounds.md:34-36`.

4. **Plan deviation is not yet in the LOG or SCORECARD.**
   - `SCORECARD.md` Planned item 1 (freshness) was not worked.
   - Item 3 planned "command D 6 → after 7".
   - `claims.json:12` calls the plan "stale" without evidence.
   - Record the deviation and its reason (no runner edit, no seventh gate) by appending.

### F6 — Pre-claimed runtime evidence in newly appended skill/corpus text (high, if committed as is)

Two appends cite evidence files that do not exist when checked (`ls` exit 2 / absent at observation):
- `SKILL.md` (append starting at old EOF :1477) cites `.ufo/evidence/round-12/verification.json` as "runtime evidence". The file is absent.
- `corpus/README.md` (new block) cites both `.ufo/evidence/round-12/verification.json` and `.ufo/evidence/round-12/BashWitness/summary.json`. Neither exists: the BashWitness directory holds only spec, declaration, `declared.tsv`, `pristine.sh` and `selftest.out`.

Rules this would break:
- `QUALITY.md` criterion 8: an unreported verification is never cited as a pass.
- `QUALITY.md` criterion 9: evidence must be in-repo before the citing commit.
- `AXES.md:62-64`: no pre-claiming.

Correction: commit these appends only after the cited files exist with the executed outputs. Otherwise mark the citations "pending, not run".

A second issue in the same block: `corpus/README.md` labels the table column "Scope now held" for F2 and F3. Moving ground into Core requires an **admitted** entry (`PROVINCE.md:40-42`), and admission is outside the lane. Append "lane-asserted, pending outside admission".

### F7 — Admission authority mapping (holds; keep it)

| Authority | Holder | Evidence |
|---|---|---|
| Claim measurement, integration, planner seat (§3) | L1, author | `lane-addendum.md:41-44,53-54` |
| Seat reviews (w1 and w2, both attempts) | Lane, advisory | `PROTOCOL.md:63-65`; `AXES.md:47-48`; spec contexts "NOT independent non-author promotion/admission" |
| Claim re-measurement plus ≥1 admit / ≥1 reject spot-check | Fresh non-author hyaku closure session | `.ufo/l0-questions.md:52-53` L0 answers; `lane-addendum.md:57-58` |
| `[x]` marks, F-row admission to Core | Non-author only | `PROTOCOL.md:66-67`; `PROVINCE.md:40-42` |
| Judgment (UFO) | Canonical Rust judge | `w1/AdmissionBounds.md:80` (cites `run-logic.md:58-62`) |

- `lesson:24` and `lesson:42` honestly leave the outside check as future, not already run. `SHONEN.md` holds four `[~]` and no `[x]`.
- There is no previous outside review to answer: there is no `round-11-verifier-spotcheck.md`, and `lesson:38` is correct on that.
- Trend discernment must stay `unprovable-but-better` or `unchanged`, pending closure (`PROTOCOL.md:162-163`).

## Six-axis harm check (state observed; L1 should re-run these at the round commit)

| Axis | Observation | Harm risk |
|---|---|---|
| depth | `git diff --stat 18ad5d0 -- tools/mutate-and-run.sh` is empty, so the runner is unchanged. The `SKILL.md` diff is an append at EOF only; its single `-` line is the no-newline-at-EOF marker with identical text. | F6: depth text cites evidence that does not exist |
| calibration | No `[x]`. `QUALITY.md` adds criteria 11–13 (appended). | F1, F2, F5.1, F5.2 are mismatches between the repo and SCORECARD/LOG, which is a calibration harm if left |
| operability | `LOG.md:659` records the runner `--selftest` at 80/80 and `--regression` cases=6, exit 0 (attempt 1). `repeat-control.py --selftest` and `bash-witness-study.py selftest` were not observed run by me. | A capability row with no demonstration |
| freshness | Unpinned (`SCORECARD.md:185-187`) | Any "improved" verdict drawn from source re-opens |
| coverage | No new surface | README "Scope now held" (F6) read as a coverage gain |
| adjacency | `git -C kagi-shokunin status --porcelain` shows 0 lines. `bash-witness-study.py:297-301` materializes the target through `git show` (read-only). | None observed |

## Owned paths

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/AdmissionCritic.md`, which is this file and the only write.
