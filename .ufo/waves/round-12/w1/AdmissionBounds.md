# AdmissionBounds — round 12 w1 (critic seat, advisory, lane-internal)

This is a lane-internal advisory review. It does not pass, admit, or promote anything, and it does not count as independent verification. This seat was dispatched by the lane, so it is still the lane (`PROTOCOL.md:63-65`). Reviewed: the L1 claim record `.ufo/evidence/round-12/claims.json`, `before.json`, the worktree `measure.py`, and the wave spec. Baseline HEAD: `18ad5d050ef4bcd830fe513825baed878f025024`. Nothing was executed except read-only count commands and one pristine-target probe (§6).

Canonical clause sources (read 2026-10-19/20):
- `A` = `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md`
- `P` = `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md`

## 1. Causal separability — holds as designed; two coupling risks to watch

Clause: claims must be "causally separable — each verifiable without the others having landed — and name distinct axes" (A:30-33). Precedent: in round 1 the lane withdrew claim K3 for a "same-round rubric, header proxy, depends on K2" (`LOG.md:603-604`).

- Axes are distinct: C1 is calibration, C2 is depth (`claims.json:6-7`). OK.
- C2 does not depend on C1. BashWitness runs the existing mutation CLI, which has its own single pristine control. It does not run `tools/repeat-control.py` (spec BashWitness item). C1 is tested only on isolated fixtures (ControlGate and FailureOracle items). OK.
- **Risk S1 (verification coupling).** C2's attribution assumes a green pristine control. That single control is exactly the weakness C1 is meant to fix (`.ufo/evidence/kaika-round-1/capability-demo/README.md:76-78`). If L1 or SynthesisConnector makes "repeat-control `controls_match` on the bash pristine" a condition of C2, C2 stops being verifiable without C1.
  - **Smallest correction:** C2 keeps the runner's single control as its stated precondition and names it as a limitation. Any repeat-control run on the bash pristine is informational only and is not cited as C2 evidence. Use the §6 probe as that informational datum.
- **Risk S2 (shared counter).** One worktree script, `measure.py`, measures both claims. That is acceptable only if each claim's before→after comes from separate fields: `repeat_control_artifact` for C1 and `bash_witness_summary` for C2. Neither claim's acceptance may read the other's field.

## 2. Lowest-axis condition — satisfied only by C2; `claims.json` overstates C1

Clauses:
- "At least one claim works the lane's lowest-scoring non-retired axis, except when the stagnation nudge … waives it" (A:33-34). The same rule appears in P:96-97 and P:518-520.
- The nudge applies only when every owned axis is at or above the saturation line (A:68-71). The lane's line is 8/10 (`SCORECARD.md:250-255`). The scores are 6/6, so the nudge is not active and the obligation stands.

Measured (read-only):
- Command D at HEAD prints `recorded_cases=6 depth_score=6`.
- Command C at HEAD prints `asserted_mark_upper_bound=8` (mark census only). The pinned calibration score is 6, set by outside adjudication with box 3 excluded (`SCORECARD.md:209-220`; `corpus/lessons/round-1-verifier-spotcheck.md:17`).
- Worktree `measure.py --rev 18ad5d0` prints `calibration_restraint_score: 6`.

Depth is the lowest axis under both readings: tied 6=6 under the pin, or strictly lowest if command C's raw 8 is used. So **C2 must carry the lowest-axis obligation.**

- **Risk L1.** `claims.json:9` says "both worked". But C1 is a capability acquisition with `score_delta 0` and the stated rationale "promotion-restraint score rubric unchanged". A capability can stand in for the lowest-axis move only under the nudge (A:68-71). It still has to land a per-axis verdict (A:40-41), and the calibration rubric cannot register it.
  - **Correction:** state "depth (lowest/tied-lowest at 6) is worked by C2". Record C1 as a capability acquisition whose calibration verdict comes from its own observable, not from the score.
- **Risk L2.** C2's type in `claims.json:7` is "measured evidence deepening". That is not one of the claim types AXES defines (axis-move A:27; capability A:40; exploratory A:43). If C2 is not an axis-move with its own falsifiable before→after (A:27-30; P:523-525), then no claim works the lowest axis.
  - **Correction:** type C2 as an **axis-move (depth)**. Its counting command is the BashWitness summary counter, measured with `--rev` at 18ad5d0 (empty) and at the round commit.
  - Its pre-registered falsifier already exists from round 1: the F2 next-step cell `corpus/README.md:79` ("the same split on a bash leg (surface-census)"; outcome equation in that cell). Cite it so the falsifier is not a same-round goalpost (the K3 precedent).
- **Risk L3 (depth not reaching the skill).** Depth is defined as "verifiable technical detail … A reader can act on SKILL.md alone" (A:11). A split that lands only under `.ufo/evidence/` does not change what the skill knows.
  - **Correction:** C2 lands an appended block in `corpus/knowledge/witness-scoped-kill-verdict.md` (or a new entry) plus its coverage-map row in the same round (`QUALITY.md` criterion 7).

## 3. Score rubrics — honest deltas, but the planned falsifier changed silently

- **D cannot move.** Command D counts the runner's comment ledger at `tools/mutate-and-run.sh:84-89`. The contract forbids runner edits and says a reanalysis is never a seventh gate. So `score_delta 0` for C2 is correct. `measure.py` field `unique_recorded_gates` (6 at HEAD) is a valid guard for this.
- **Risk R1 (plan deviation hidden).** `SCORECARD.md:271-272` planned C2 as "command D 6 → after 7", and F3 planned C1 as a "capability" (`:268-270`). `claims.json:12` calls that row a "stale inherited plan". But that row is the declared next-round plan (A:81, `SCORECARD.md:261`), and P:85-89 forbids relabelling rounds.
  - **Correction:** record the deviation explicitly in LOG/SCORECARD:
    - planned item 1 (freshness) was not worked;
    - item 2 is worked as C1 (capability);
    - item 3 is worked as C2, with the falsifier changed from "D 6→7" to "witness rows undefined→10 classified". The reason is the no-runner-edit contract plus no-seventh-gate.
  - Do not call the row stale without evidence.
- **Risk R2 (rubric drift mid-round).** `before.json` no longer reproduces from the current `measure.py`. Running `measure.py --rev 18ad5d0 | diff - before.json` shows only added fields: `calibration_*` and `unique_recorded_gates`. All original fields match. `measure.py` is also untracked (`git ls-files` fails).
  - **Correction:** regenerate `before.json` from the final `measure.py` at 18ad5d0 and commit both in the round commit. The after value must be measured with `--rev <round commit>`, never the worktree (P:406-407).
- **Note on the calibration encoding.** `measure.py:29-31` hard-codes boxes (1,2,4) and excludes box 3. That reproduces the outside adjudication (`SCORECARD.md:216-218`), so it is re-derivable and not a new goalpost. Keep the citation comment.
- **C1 capability evidence.** A capability enters the capabilities table only with a passing demonstration in the round report (A:62-64). Under P:403, "self-test green is capability, not a measurement". So C1 needs the `--selftest` exit/ID run, the `--snapshot` frozen run with digest-pinned `expected.json`, and the tamper run, all executed by L1 and reported (P:398-410). `repeat_control_artifact` (file presence) is not a demonstration.

## 4. No-axis-harmed — checks L1 should run at the round commit

Clause: "admitted only if every claim verifies and no axis is harmed — a trade anywhere is not an improvement: report every verdict and let the operator rule" (A:34-36).

| Axis | Guard (baseline at 18ad5d0) | Harm trigger |
|---|---|---|
| depth | D=6; `unique_recorded_gates`=6; `git diff --quiet 18ad5d0 -- tools/mutate-and-run.sh` | Runner diff; a ledger or mutation-case table edited to fit the new split. The witness aggregate must reconcile with the recorded leg (expectation lives in the runner's `TABLE_BASH`, `:555`). A contradiction is disclosed as a harm candidate for the operator, never silently resolved. |
| calibration | `calibration_restraint_score`=6; command C shows `checked=0 asserted=4` | Any `[x]`; any lane seat described as independent or non-author; `claims.json:9` "both worked" left as written (an overreach is a calibration signal, A:15). |
| operability | Runner `--selftest` (80/80) and `--regression` (`cases=6`) as last recorded at `.ufo/evidence/kaika-round-1/capability-demo/`; sources census v2 exit 0, `CLEAN` | Any of these fails at the round commit. `SOURCES.md` row edits break census v2 or the fleet `validate`. |
| freshness | Unpinned (`SCORECARD.md:187`) | Claiming "improved" from source re-opens without a pinned rubric. Verdict should be `unchanged (unpinned)`. |
| coverage | No new surface | Counting a reanalysis or a plan as new coverage. |
| adjacency | Kagi worktree `git status --porcelain` = 0 lines (observed after the §6 probe) | Any write into a sibling tree (`PROVINCE.md:16-17`); absorbing engine nondeterminism (`PROVINCE.md:47`). |

- File-integrity guard: `LOG.md`, `SCORECARD.md`, `corpus/README.md`, and knowledge entries are append-only (`QUALITY.md` criterion 4).
- `SKILL.md` may only be appended at its end, so existing line cites stay valid (for example `SKILL.md:148-149` and `:171-178` cited in `witness/README.md:32`). Box 3's pointer is blob-pinned (`SHONEN.md:10`), but inserting rows mid-file would shift lane-wide line cites. Check: `git diff -U0 18ad5d0 -- SKILL.md` has no `-` lines and its first hunk starts after the old EOF.
- Frontier: F2/F3 may move status only as a lane assertion. Moving into Core requires an admitted, source-headed entry (`PROVINCE.md:40-42`), and admission is outside the lane.

## 5. Lane review vs outside reviewer

- **Lane (every round-12 seat, including this one):** every seat in `.ufo/waves/round-12/spec.json` is lane-dispatched. Rules:
  - "a subagent the lane dispatched is still the lane" (P:63-65);
  - "a dispatched subagent does not count" (A:47-48);
  - "Driver completion is not admission; independent non-author verification remains required" (P:173-174);
  - the wave contract: "advisory lane-internal, NOT independent non-author promotion/admission".

  So these seats cannot write `[x]` (P:66-67), cannot supply the discernment admit/reject spot-check (`SCORECARD.md:118`), and cannot admit F-rows into Core.
- **Outside:** the orchestrator or integrator, recorded in a file the lane does not author. The round-1 precedent is `corpus/lessons/round-1-verifier-spotcheck.md:3-6,10-17` (commit `a21e910`, "Written by the integrator, not the lane"; verifier W3ReviewTameshi; it is the only source of the pinned 6). Under UFO invariant I1, only the canonical Rust judge emits judgment (`ufo-fsd-alpha/skills/ufo/references/run-logic.md:58-62`).
- **Correction:** the round-12 report labels every seat verdict "lane self-verdict" and leaves trend discernment `unprovable-but-better`, pending outside review (P:162-163). `claims.json:11` already says this — keep it.

## 6. Counterexample probe (executed, read-only)

Hypothesis tested: the bash pristine's selftest output is not byte-stable. If that were true, risk S1 would be a live defect in C2's precondition.

- Method: materialized kagi `corpus/surface-census.sh` at `fecee874…` with `git show` into `/tmp/tameshi-r12-AdmissionBounds-probe/`. Its sha256 `275d8294…` equals `PIN_BASH` (`tools/mutate-and-run.sh:544`). Ran `bash pristine.sh --selftest </dev/null` three times.
- Observed:
  - exit codes 0, 0, 0;
  - stdout identical across runs, sha256 `09c21ee2…a2fca`;
  - stderr empty in all runs;
  - final line `SELFTEST: PASS (16 cases)`, with one `skip-case 16 … substrate-absent (handler not on PATH)`;
  - kagi worktree unchanged.
- Result: the hypothesis is **refuted on this host**. This is three samples on one host, not a determinism proof.
- Side finding for WitnessThreats/BashDenominator (pristine-only, no mutant outcomes): the 16-case denominator includes a host-dependent skip. C2's "full denominator" rule must say whether a skip counts.
- Retained at `.ufo/evidence/round-12/AdmissionBounds/pristine-repeat-probe.txt` and `pristine-selftest.stdout.1`.

## Exact owned paths (written by this seat)

- `.ufo/waves/round-12/w1/AdmissionBounds.md`
- `.ufo/evidence/round-12/AdmissionBounds/pristine-repeat-probe.txt`
- `.ufo/evidence/round-12/AdmissionBounds/pristine-selftest.stdout.1`

Scratch: `/tmp/tameshi-r12-AdmissionBounds-probe/`.

## Installs

None.
