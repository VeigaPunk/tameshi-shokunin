# Fleet round-1 calibration audit — tameshi-shokunin

- Author: EvidenceExecutor (fleet round-1, tameshi-dispatched seat). Per PROTOCOL.md:63–68 a
  subagent the lane dispatched is still the lane: every finding in this file is a lane-local
  check, never independent promotion authority.
- Audited baseline: commit `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d`. Repo-path cites below
  resolve at that commit unless a line is explicitly marked (worktree).
- Move: calibration only — a truthful restatement of what the retained, committed sources
  support. No tool change, no promotion, no scope broadening.
- Status: lane-local evidence correction; no independent promotion review is claimed.

## canonical protocol source pointers

- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:63–68` — promotion
  gate: each `[x]` names a non-author verifier; a lane-dispatched subagent is still the lane;
  an `[x]` with no named non-author verifier counts as `[~]`.
- `PROTOCOL.md:419–428` — canonical four-box `SHONEN.md` seed, verbatim (`<name>` substituted
  with the repo directory name); `PROTOCOL.md:413` — marks confined to the box character plus
  one indented evidence line per box.
- `PROTOCOL.md:430–431` — mark spec: `[~]` = lane assertion with a required evidence pointer;
  `[x]` = only with a named non-author verifier.
- `PROTOCOL.md:327–344` — evidence standard: resolvable pointers only; `/tmp` and session
  `local://` pointers are not evidence at closure time; claimed ≠ re-executed (:345–346).
- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL-APPENDIX.md:28`
  ("Evidence standard" incident row) and `:30` ("Canonical form" row — variant SHONEN files).

## baseline mark census

Counting commands C and D are in `SCORECARD.md`, the appended Current axes section.
The historical `SCORECARD.md:1–56` remains unchanged; the score rubrics do not
retrospectively grade the training arc.

- Parent-observed, from the shared round-1 contract, executed against
  `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d`:
  - D: `recorded_cases=6 depth_score=6`
  - Original C: `boxes=4 checked=4 asserted=0 untouched=0 calibration_score=0`.
    That original field was subsequently renamed: the current capped census reports
    `asserted_mark_upper_bound=0`, not an independently awarded score.
- The executor also inspected the baseline's checked marks and documented ledger rows;
  those are historical-input observations, not fresh mutation runs.
- Census only: C counts mark characters, not semantic proof. The awarded local score
  additionally requires canonical wording, same-revision durable links, and the source
  audit below. Box 3 is rejected, so the candidate score is 6, not the initially proposed 8.

## supersession of historical independence claims

Historical bytes are preserved. This section supersedes the *interpretation* of
the following statements. The records report the named runs; those runs were not
freshly replayed here. Their classification as independent promotion verification,
and reliance on temporary pointers for closure, are withdrawn:

- `LOG.md:283–290` — "SHONEN.md boxes updated with the audit lanes as named non-author
  verifiers": the audit lanes (TAMESHI-B1/B2/B3/B4) were fleet seats this lane dispatched or
  hosted; per PROTOCOL.md:63–68 they are still the lane.
- `plans/completion-evidence.md:44–59` — "all four boxes `[x]`, each naming a non-author
  verifier with retained evidence": the four verifiers are not non-authors, and the cited
  evidence lives under `/tmp/tameshi-b*-r3b-*` scratch trees, which PROTOCOL.md:340–344
  excludes at closure.
- `reports/r11-aud-t11.md:140` — completeness-table row CONFIRMED: it re-measured the fact of
  the marks (four `[x]`, last touched `53e74a8`), and at spot-check depth; it did not and
  could not adjudicate verifier independence.
- `plans/round-11.plan.md:23–25` — "definition of done is already receipted (the four
  `SHONEN.md:5-34` boxes, each `[x]` with a named verifier)": receipted as lane-internal
  review only.

Disposition under the gate: the baseline's four `[x]` marks count as `[~]` per
PROTOCOL.md:66–68. TAMESHI-B1/B2/B3/B4 are preserved here as historical lineage of the runs,
not as independent authority. The parent owns the corrective `LOG.md` append and any pointer
into the completion pack; this file is the durable audit basis for that correction.

## box-1

Canonical seed row: `PROTOCOL.md:425` — "SKILL.md contains real decision tables, error
patterns, checklists, cited sources".

Baseline claim: `SHONEN.md:5–11` — `[x]` "SKILL craft", verifier TAMESHI-B3 (historical
lineage only; see supersession).

What the retained, committed sources actually establish:

- `SKILL.md:58–92` (baseline blob): a gate-shape decision table and cited rules
  distinguishing hermetic suites, live gates and audit lanes.
- `SKILL.md:497–525`: the fail-closed error-pattern taxonomy distinguishes SETUP,
  malformed data, POLICY, zero-work and deferral, citing kagi/kumitate survey ranges.
- `SKILL.md:466–495`: a no-permissiveness checklist, with source citations for
  revision pins, byte comparison, verdict discipline, deferral and unknowns.
- The cited survey notes are committed in-repo, and three cited ranges were spot-checked to
  resolve with matching content at write time: `corpus/knowledge/gates-survey-kumitate.md:19–31`
  (six-suite exit/summary table + hermeticity lines), `corpus/knowledge/gates-survey-kagi.md:24–31`
  (gate census table incl. the 16-case `surface-census.sh` selftest row),
  `corpus/knowledge/verification-patterns-fleet.md:24–35` (P1 claim-before-move, P2
  named-non-author-verifier pattern — the very pattern box 1's independence depends on).

What remains unknown: every single citation across `SKILL.md:58–129` and the recipe was not
re-resolved line-by-line (three sampled; the rest carry no fresh pointer); the TAMESHI-B3
manifest-replay result (`/tmp/tameshi-b3-r3b-1-work`, `/tmp/tameshi-b4-r3b-verify`) is not
durable closure evidence; the active SKILL preamble's broad cold-read assertion is
narrowed by the parent in the same change and is not support for box 3.

Why `[~]` rather than `[x]`: the decision table, error-pattern list, checklist and cited
sources exist and are durable at baseline, asserted by the lane with this file as pointer;
no non-author verifier reviewed this box (PROTOCOL.md:63–68, 430–431 — the parent ruling
names no independent promotion verifier in this batch).

## box-2

Canonical seed row: `PROTOCOL.md:426` — "At least one end-to-end domain task executed and
logged in LOG.md".

Baseline claim: `SHONEN.md:12–18` — `[x]` "End-to-end task", verifier TAMESHI-B1
(historical lineage only).

What the retained, committed sources actually establish:

- `corpus/knowledge/mutation-case-kagi-census.md:1–17` (TAMESHI-R3-1): a real domain task —
  the kagi `surface-census.sh` gate (sha/size/mtime pinned at :13–17) run through the
  mutation sweep, read-only on a sibling substrate, restore proof recorded, O/I/U anchors
  per :9–11; the note itself was the run's only fleet file written (:4–7).
- `LOG.md:277–298` records the round-3 execution trail: second kill-rate on a bash gate,
  first in-tree tool (`tools/mutate-and-run.sh`), and the round's carried unknowns (:292–298)
  — trigger → action → outcome structure per PROTOCOL.md:332–335.

What remains unknown: the historical TAMESHI-B1 scratch driver is not a durable
reproduction dependency. The fresh, parent-executed CLI task below supplies this
round's direct outcome, separately from the historical task recorded in LOG.md.

Why `[~]` rather than `[x]`: at least one end-to-end domain task is executed and durably
logged (note + LOG entry at the audited revision), asserted by the lane; the verifier named
at baseline was lane-dispatched, so the box is not independently reviewed
(PROTOCOL.md:63–68).

## box-3

Canonical seed row: `PROTOCOL.md:427` — "Instructions executable by an agent without oral
context".

Baseline claim: `SHONEN.md:19–26` — `[x]` "No-oral-context", verifier TAMESHI-B2
(historical lineage only).

What the retained, committed sources actually establish — exactly one historical fact, and
this audit rejects any wider reading of it:

- `corpus/knowledge/executor-test-sufficiency.md:3–8` (TAMESHI-R3-4): an executor with only
  `SKILL.md` at pinned revision `dd2f4dee…3753` reproduced ONE killed JS mutant (D5)
  end-to-end — control green (`43/43`), kill (`42/43 FAIL`), manifest strings unique,
  restore pin held.
- `:52–54` scopes it: "the bash case (Appendix B) was not touched … ONE killed mutant, per
  the assignment — not a full 10-defect sweep."
- `:104–158` gives per-step sufficiency verdicts confined to that single-mutant scope, and
  `:155–163` assesses the SKILL's core claim only "for the executed scope".

What remains unknown: the reviewed records and this round do not establish a
current-revision full cold-read. The historical note explicitly excludes full sweeps,
survivor probes and bash (`executor-test-sufficiency.md:160–184`). Its temporary
driver/snapshot dependencies are not recovered by linking the durable testimony.
Whether the current full instructions are executable without oral context remains
unproven; this is not a claim that no unobserved executor ever tried them.

Why `[ ]` — no lane assertion at all: the parent ruled (2026-10-15) that the retained
historical single-JS-mutant result cannot support a broad current assertion, so this box
does not qualify even for `[~]`; and the baseline `[x]` fails twice over — TAMESHI-B2 was
lane-dispatched, not a non-author verifier (PROTOCOL.md:63–68). Consequence for the score
claim: three `[~]` plus one `[ ]` permits a local score of 6, not 8, after the
three asserted boxes' source audits. Box 3's two points and the separate independent-
review two points remain unearned.

## box-4

Canonical seed row: `PROTOCOL.md:428` — "No cross-domain bleed (PROVINCE.md still accurate)".

Baseline claim: `SHONEN.md:27–34` — `[x]` "PROVINCE accuracy", verifier TAMESHI-B3
(historical lineage only).

What the retained, committed sources actually establish:

- `PROVINCE.md:3–18` (baseline blob): the domain statement (verification-fixture craft), the
  owned surfaces list, and the refusal rules — two-lane rule for generality (:14–16),
  never-edit-a-sibling's-gate (:16–17), credentials→kagi / endpoint health→kama (:18).
- Committed in-repo artifacts consistent with it: `tools/mutate-and-run.sh:84–89` records
  the six cross-lane cases as *recorded pins* only (replay targets in sibling repos, read
  as git blobs), and `corpus/knowledge/mutation-case-kagi-census.md:4–7` states the run's
  own discipline: sibling tree untouched, mutants confined to its own scratch namespace,
  secrets shape-only.

What remains unknown: no complete historical no-bleed audit is recreated here.
Sibling trees may contain their owners' concurrent work; their global cleanliness is
not a premise. The parent resolved the declared directories read-only: kumitate
`scripts/`, kagi `corpus/`, kaidoku's lane root and fleet `.ufo/waves/`.

Why `[~]` rather than `[x]`: the lane's work is its own checklist, skill, corpus,
records and fleet report; the CLI task below mutates only its disposable target.
That work matches `PROVINCE.md:3–18`. No sibling gate, credential or endpoint was
modified. This is a bounded lane assertion, not an externally audited history.

External content support, not promotion attestation: the fleet's
`.ufo/waves/shokunin12h-20261014-p1-repair/members/FleetBoundaryConnector.md:39,42,114`
at fleet commit `cb3c1039297b6dd112bb745bf8ba771e09910347` describes tameshi's
method/product split and refusal to edit sibling gates. CalibrationConnector
located it and the parent re-read those lines. That historical boundary review
does not mark a SHONEN box, so box 4 remains the lane's `[~]` assertion.

## lane-local dispositions (calibration target)

| Box | Canonical row | Baseline mark | Audit disposition | Durable pointer |
|---|---|---|---|---|
| 1 | `PROTOCOL.md:425` | `[x]` TAMESHI-B3 | `[~]` | this file, `## box-1` |
| 2 | `PROTOCOL.md:426` | `[x]` TAMESHI-B1 | `[~]` | this file, `## box-2` |
| 3 | `PROTOCOL.md:427` | `[x]` TAMESHI-B2 | `[ ]` (assertion rejected) | this file, `## box-3` |
| 4 | `PROTOCOL.md:428` | `[x]` TAMESHI-B3 | `[~]` | this file, `## box-4` |

Marks, wording and evidence lines in `SHONEN.md` are the ChecklistExecutor's edit under the
canonical seed (PROTOCOL.md:419–428, 430–431); this table states what this lane's evidence
supports, nothing more. None of the nine fleet round-1 checks is promotion authority.

## executed verification

Parent-observed on 2026-10-15. Runner bytes were unchanged from baseline:
`75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`.
Command: `bash tools/mutate-and-run.sh --selftest` → exit 0:

```text
MUTATE_SELFTEST: 80/80 pass
VERDICT: PASS
```

Actual CLI task, observed at `MUTATE_DATE: 2026-10-15T04:58:33Z`:
create a disposable target, inject one observable defect and one unasserted
assignment defect, run the same output predicate for control and both mutants,
then verify byte identity. No sibling gate was invoked. This small fixture
checks the real CLI; it is not a new fleet kill-rate measurement or a cold-reader
exercise. The six-leg `--regression` was **not** run this round.

Exact command used (`W=/tmp/tameshi-r1-smoke-hqx47wf8` for this observation):

```sh
bash tools/mutate-and-run.sh --target "$W/target.sh" --defects "$W/defects.spec" --suite 'test "$(bash "$MUTANT")" = good' --workdir "$W/evidence" --label fleet-round-1-calibration-smoke --timeout 15 --tail 1
```

Observed output (timings and paths are receipt values, not future expectations):

```text
MUTATE_TOOL: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh sha256=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
MUTATE_DATE: 2026-10-15T04:58:33Z
MUTATE_TARGET: /tmp/tameshi-r1-smoke-hqx47wf8/target.sh sha256=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26 bytes=67
MUTATE_SPEC: /tmp/tameshi-r1-smoke-hqx47wf8/defects.spec defects=2
CONTROL: GREEN (exit=0 duration-ms=1 pristine-sha256=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26)
  | (no output)
DEFECT wrong-value: KILLED (exit=1 duration-ms=2) asserted output changes
  | (no output)
DEFECT unread-value: SURVIVED (exit=0 duration-ms=2) unasserted assignment changes
  | (no output)
MUTATE_RESTORE: OK (target-sha256 before=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26 after=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26 pristine-sha256=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26)
MUTATE_EVIDENCE: /tmp/tameshi-r1-smoke-hqx47wf8/evidence
MUTATE: DONE (target=fleet-round-1-calibration-smoke defects=2 killed=1 survived=1 inconclusive=0 kill-rate=50%)
```

Exit 0; parent additionally compared target SHA-256 before/after: identical.
The first invocation used invalid `--tail 0` and was refused with exit 64;
only that invocation was retried with `--tail 1`. The successful receipt's
`50%` initially disagreed with the observer's mistaken `50 %` expectation;
the observer was corrected without rerunning the successful CLI.

Self-contained reproduction (new scratch paths; no retained `/tmp` files required):

```sh
python3 - <<'PY'
import hashlib, pathlib, shutil, subprocess, tempfile
w = pathlib.Path(tempfile.mkdtemp(prefix="tameshi-r1-smoke-"))
try:
    target = w / "target.sh"
    target.write_bytes(b"#!/usr/bin/env bash\nvalue=good\nunused=quiet\nprintf '%s\\n' \"$value\"\n")
    spec = w / "defects.spec"
    spec.write_text("@defect wrong-value | asserted output changes\n@old value=good\n@new value=bad\n@defect unread-value | unasserted assignment changes\n@old unused=quiet\n@new unused=loud\n")
    before = hashlib.sha256(target.read_bytes()).hexdigest()
    p = subprocess.run(["bash", "tools/mutate-and-run.sh", "--target", str(target),
        "--defects", str(spec), "--suite", 'test "$(bash "$MUTANT")" = good',
        "--workdir", str(w / "evidence"), "--label", "fleet-round-1-calibration-smoke",
        "--timeout", "15", "--tail", "1"], capture_output=True, text=True)
    print(p.stdout, end="")
    print(p.stderr, end="")
    assert p.returncode == 0
    assert "CONTROL: GREEN (exit=0 " in p.stdout
    assert "DEFECT wrong-value: KILLED (exit=1 " in p.stdout
    assert "DEFECT unread-value: SURVIVED (exit=0 " in p.stdout
    assert "MUTATE_RESTORE: OK " in p.stdout
    assert "defects=2 killed=1 survived=1 inconclusive=0 kill-rate=50%" in p.stdout
    assert hashlib.sha256(target.read_bytes()).hexdigest() == before
finally:
    shutil.rmtree(w)
PY
```


## dispatch and adversarial review

Parent-observed dispatch: one `functions.task` call returned nine seats in a
single batch. This is the Shokunin OMP host binding of the mission's batched
AgentSwarm requirement, not a claimed validated generic UFO wave.

| Seat | Taxonomy role | Owned scope / observed result |
|---|---|---|
| CalibrationPlanner | planner | C is only a mark census; source/shape/link checks required. |
| CalibrationConnector | connector | Sibling-overlap and authority-boundary scan, read-only. |
| ChecklistExecutor | executor | Canonical SHONEN wording and four evidence links. |
| EvidenceExecutor | executor | Per-box source/provenance audit in this file. |
| LessonExecutor | executor | `corpus/lessons/round-1.md`; no promotion claim. |
| CalibrationScribe | scribe | Count/identity/report-order conformance checks. |
| CalibrationScout | scout | Historical B1/B2/B3 evidence and durable-source map. |
| CalibrationReviewer | reviewer | Canonical form and source-entailment review, lane-local. |
| CalibrationCritic | critic | Rejected current broad cold-reader credit from historical D5. |

Only taxonomy roles were supplied; no model parameters or routing mutations.
The host tool applies its route table. Resolved model identities were not
exposed in the dispatch result and are not asserted here. The mission requires
a planner, unlike the generic UFO wave taxonomy; this heterogeneous craft
batch follows the explicit mission and native Shokunin host mapping without
padding seats to another framework's floor.

The planner and critic both falsified mark-only scoring. The critic's
historical-subset counterexample was accepted: box 3 stays `[ ]`, lowering
the candidate score from 8 to 6. None of these agents is an outside
promotion verifier or the outside admit/reject spot-check in `LEARNING.md:39–43`.

CalibrationReviewer checked the substantive source mappings for boxes 1, 2
and 4 and the historical supersession quotes. The review accepted the bounded
box-3 rejection and identified an incidental rule-count error; that count was
removed rather than made part of the calibration metric. The review's remaining
conditions—bounded cold-reader wording, renamed mark-census field, durable
smoke inputs/output and frozen-commit checks—are parent integration work.

Cross-domain routing: protocol/integrator owns promotion decisions and fleet
dispatch/round-number reconciliation. Tameshi owns this self-defect correction
and reports it for the aggregator's durable queue; it does not edit fleet
protocol, rank/roster records, routing, counters, or any sibling gate.

## Interactive continuation — blocked dispatch, local correction retained

This section is the current L1's observation, not a reconstruction of the
prior native session. Everything above arrived as uncommitted predecessor
work. Its nine-seat dispatch narrative and 04:58:33Z smoke are inherited
testimony; they are not this session's dispatch or fresh verification.
The current exact-32 operator contract supersedes the rationale at
lines 294–317. That historical batch does not satisfy current admission.

The actual current round remains **fleet round 1**, calibration. HEAD at
entry was `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d`; the historical
rounds 1–11 are preserved, not renumbered or re-adjudicated. The launch
counter is not a verified-round counter. The initial tracked changes are
preserved in `.ufo/evidence/fleet-round-1/inherited-calibration.patch`.
The WWKD plan is `.ufo/plans/fleet-round-1-interactive-wwkd.md`.

**Dispatch is blocked, not completed.** Both the global routing metadata
and `cfg://task/agentModelOverrides` show the old generic buckets rather
than the operator-required role aliases. Executor is `@m_mid`, scribe and
simplifier `@m_fast`; scout and mutation-tester `@m_fast`; reviewer,
sentinel and revenger `@m_mid`; critic `@m_strong`; connector `@m_mid`.
Required bindings are content `@m_composer`, audit `@m_grok`, connector
`@m_antigravity` with `@m_zfl` fallback. The current connector chain does
not contain the configured `@m_zfl` target. Exact evidence:
`.ufo/evidence/fleet-round-1/route-bindings.json` and
`live-seat-bindings.txt`. No configuration was changed and no substitute
route was used. No current specialist was spawned.

Exactly 32 distinct, substantive calibration scopes were saved in
`.ufo/waves/fleet-round-1-interactive/spec.json` and validated by the
canonical `ufo-swarm-wave.mjs plan --spec-json … --route-families`:
exit 0, schema `ufo-swarm-wave-v1`, 32 tasks, 32 distinct names, all fresh
tasks carrying the renderer's leading `/skill:godspeed`. Full output:
`plan.stdout.json`; command/exit: `validation.json`. `run` and native
`task` were deliberately not invoked under the wrong bindings. A
validated plan is neither a launched wave nor a verified round.

### Fresh local observations

The parent read the actual canonical seed and source ranges supporting
boxes 1, 2 and 4 and the narrow historical box-3 result. This is author-local
source review, not outside promotion or discernment review.

- `.ufo/evidence/fleet-round-1/calibration-acceptance.json` retains the
  reproducible comparison program and complete output. Baseline:
  `CALIBRATION_BASELINE: FAIL (canonical=false marks=["x","x","x","x"] durable-links=0/4 independent-promotion=false full-cold-read=false)`.
  Candidate:
  `CALIBRATION_CANDIDATE: PASS (canonical=true marks=["~","~"," ","~"] durable-links=4/4 independent-promotion=false full-cold-read=false)`.
  Comparison exit 0. The mechanical check covers box rows and links;
  the title and semantic support were separately read, not inferred from
  the mark count.
- `.ufo/evidence/fleet-round-1/selftest.json` captures this parent's full
  invocation of `bash tools/mutate-and-run.sh --selftest`:
  `MUTATE_SELFTEST: 80/80 pass`, `VERDICT: PASS`, exit 0.
- `.ufo/evidence/fleet-round-1/cli-smoke.json` captures the real CLI at
  `MUTATE_DATE: 2026-10-15T05:10:40Z`: green control, `wrong-value`
  KILLED (exit 1), `unread-value` SURVIVED (exit 0),
  `MUTATE_RESTORE: OK` with identical full before/after SHA-256, and
  `MUTATE: DONE (target=fleet-round-1-interactive-smoke defects=2 killed=1 survived=1 inconclusive=0 kill-rate=50%)`,
  exit 0. Inputs follow the self-contained recipe above; disposable files
  were under this repo's `.ufo/scratch/`, not a sibling tree.

No sibling regression suite, live target, native transcript body, raw
journal or secret/session contents were read or exercised. Tool bytes
were unchanged at `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`.
The reported Phase 0 failure was not rerun.

**Disposition:** the local calibration correction is supportable; formal
round admission and verified-round credit are withheld because the
required wave cannot be dispatched. The numeric candidate upper bound is
not an awarded verdict. Outside admit/reject review and current full
cold-read evidence remain open. The lane report and continuation live
inside this repository's `.ufo/`; only the fleet integrator may update
shared ledgers or arrange an authorized fresh-session redispatch.

### Scratch erratum — current CLI acceptance supersedes lines 390–396

The 05:10:40Z run and `.ufo/evidence/fleet-round-1/cli-smoke.json` are
truthful behavioral output but **nonconforming craft evidence**:
repo-local `.ufo/scratch` violated `SKILL.md:25-28`, which requires the
lane/round namespace under `/tmp` from the first fixture write. Deleting
the files did not cure that violation. The output and this error remain
retained; they are not the current smoke admission evidence.

The parent corrected only that namespace and repeated the actual CLI
scenario in a fresh `/tmp/tameshi-r1-interactive-4oejhl9z/` at
`MUTATE_DATE: 2026-10-15T05:14:49Z`. Complete output, exit and a
self-contained reproduction program are retained in
`.ufo/evidence/fleet-round-1/cli-smoke-canonical.json`, which explicitly
supersedes the earlier file for admission. It observed:

```text
CONTROL: GREEN (exit=0 duration-ms=2 pristine-sha256=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26)
DEFECT wrong-value: KILLED (exit=1 duration-ms=2) asserted output changes
DEFECT unread-value: SURVIVED (exit=0 duration-ms=2) unasserted assignment changes
MUTATE_RESTORE: OK (target-sha256 before=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26 after=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26 pristine-sha256=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26)
MUTATE: DONE (target=fleet-round-1-interactive-canonical-smoke defects=2 killed=1 survived=1 inconclusive=0 kill-rate=50%)
SMOKE_RUNNER_EXIT: 0
SMOKE_ASSERTIONS: PASS (control, kill, survivor, restore, canonical-scratch; independent-sha256=0cf28b95af5402d3f1e71deae00e9eba43ec0d57d4eff39808f055505ce54f26)
```

Driver exit 0. Its fresh temporary tree was removed in `finally` after
capture; durable evidence is the committed command/program/output, not
the temporary path. The valid selftest was not repeated. Route/receipt
blocks and withheld round credit are unchanged.

