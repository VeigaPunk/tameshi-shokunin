# ScoreRubric — tameshi round 12, wave w2

Seat: `TameshiR12.ScoreRubric` (leaf reviewer, read-only). Advisory, lane-internal.
Not an independent non-author promotion review; not an admission; no score awarded here.
Owned write: this file only. No edits to SCORECARD.md, SHONEN.md, LOG.md, tools/,
corpus/, reports/, or .ufo/evidence/. Probe files created in /tmp and removed.
Tooling installed: none (used git, python3, grep, sed already present).

## 1. Axes named

| Axis | Rubric as written | Counting command as written | What the command actually reads |
|---|---|---|---|
| depth | 1 pt per recorded mutation case in pinned ledger, cap 10 (`SCORECARD.md:66`; command D `:72-73`) | regex `^#   (js\|bash)-\S+\s+\S+\s+\d+/\d+` over `tools/mutate-and-run.sh` header | header comment rows (`tools/mutate-and-run.sh:84-89`), not executed legs |
| calibration | 2 pts per correctly restrained, durable-evidence-linked `[~]`, cap 8; last 2 need independent review (`SCORECARD.md:67`; command C `:74-75`) | `[~]`/`[x]` mark census over `SHONEN.md` | mark counts only; no restraint, evidence-link, or independence check |
| capability (not an axis) | a row enters only via a round that demonstrates it running (`SCORECARD.md:244`) | none | — |

Scored artifact actually used for the pinned values: `.ufo/evidence/round-12/measure.py`
(`measure.py:30-31`, `:45`), not the literal SCORECARD commands.

## 2. Measurements (read-only, this seat)

| Command / probe | Revision | Output |
|---|---|---|
| command C literal (`SCORECARD.md:75`) | 121696b | `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8` |
| command C literal | HEAD (18ad5d0) | same: upper bound **8** |
| command D literal (`SCORECARD.md:73`) | 121696b, HEAD | `recorded_cases=6 depth_score=6` |
| `measure.py --rev 284ab0f` | 284ab0f | calibration 0, recorded_cases 6, unique_recorded_gates 6 |
| `measure.py --rev 121696b` / `01b358c` / `a21e910` / `18ad5d0` | — | calibration **6**, recorded_cases 6, unique 6 (`before-with-score-exclusions.json` reproduces at 18ad5d0) |
| `measure.py` worktree | uncommitted | calibration 6, recorded 6, unique 6, `mined 15` (HEAD: 12) from uncommitted `corpus/SOURCES.md` |
| duplicate-row probe (one extra `#   bash-surface-census …` row appended to a `/tmp` copy of HEAD runner) | HEAD+1 row | recorded_cases **7**, unique_gates **6** |
| pinned legs `REV_*` (`tools/mutate-and-run.sh:543-553`) | sibling repos | all four distinct pins resolve as commit objects (kumitate `175de6b`, kagi `fecee87`, tsukuroi `165307f`, mado `eead56b`) |
| leg invocations | HEAD | six, at `tools/mutate-and-run.sh:1113,1118,1123,1128,1133,1138` |
| mark census of boxes | 121696b, HEAD | `[~]` at SHONEN.md lines 5,7,9,11 (box 3 = line 9) |

Not re-run by this seat: the runner's `--selftest` and `--regression` (not assigned).

## 3. Findings (by severity)

### HIGH-1 — Calibration 6 is not the output of the stated rubric command

- `SCORECARD.md:67` and `:218-219` say the pinned 6 is "rubric of command C, box 3 excluded".
  Command C (`SCORECARD.md:75`) has no exclusion. Literal output at 121696b and HEAD is
  `asserted_mark_upper_bound=8`.
- The 6 is produced only by `measure.py:30` (`scored_boxes = (1, 2, 4)`) and `:31`
  (`calibration = 2 * sum(...)`), with the exclusion hard-coded as a constant (`:44`
  `calibration_excluded_boxes: [3]` is a literal, not computed from anything).
- Consequence: the reproducible command gives 8; the pinned score 6 needs a manual
  adjudication that lives only in the script's constant. The rubric text and the
  command disagree.
- Recommendation (no edit): either (a) make command C reproduce the adjudicated value from
  a committed, named exclusion record, or (b) keep command C's output (8 candidate) and
  state 6 as an adjudicated, not counted, value. Either choice needs an append-only LOG entry.
  `LOG.md:663` currently says measure.py "reproduc[es] 6"; that is true of the script only.

### HIGH-2 — Calibration 6 is pinned on lane self-attestation, which the scorecard forbids

- `SCORECARD.md:163-164`: "Self-verdicts below are pending non-author verification; no
  score is pinned on self-attestation."
- The six points are boxes 1, 2, 4 at `[~]` × 2 (`measure.py:30-31`). Those marks are
  labelled `[lane assertion, no independent promotion verifier]` in `SHONEN.md:6`, `:8`, `:12`.
  The `reports/round-1-calibration.md#box-1/#box-2/#box-4` dispositions likewise state that
  none of the nine round-1 checks is promotion authority (`reports/round-1-calibration.md:211-213`).
- The only independent check cited for the adjudication, `corpus/lessons/round-1-verifier-spotcheck.md:8-13`,
  samples one admit and one reject of knowledge entries (S006/S001, S046/S029). It does not review
  any calibration box. The adjudication itself (`round-1-verifier-spotcheck.md:17`) is an
  orchestrator decision, not a count.
- The rubric requires "correctly restrained, durable-evidence-linked" (`SCORECARD.md:67`).
  `measure.py:31` checks neither restraint nor link. The `reports/...` link targets at
  `SHONEN.md:6,8,10,12` are present as text; this seat did not resolve their anchors (the
  ScorecardReview seat reports box-1/2/4 anchors resolve at `reports/round-1-calibration.md`
  lines 71/105/167 [peer evidence, not re-checked]).
- Consequence: the 6 counts lane-authored marks. It is not evidence of calibration beyond
  the lane's own assertions. Under the rule at `SCORECARD.md:163-164` the pinned value should be
  reported as "lane-asserted, unverified" with the scored value at 0 until independent review,
  or the rule itself must be amended by a dated LOG entry. Silent reliance on the 6 is inflation.

### HIGH-3 — Box 3 is marked `[~]` in the promotion checklist and `[ ]` in the calibration report

- `SHONEN.md:9-10` at HEAD: `[~]` "lane assertion, scope-bounded".
- `reports/round-1-calibration.md:208`: box 3 `[ ]` "(assertion rejected)".
- The 6 depends on excluding box 3 by constant (`measure.py:30`), not by reading either record.
  The two records disagree on the same box, so whichever one a reader trusts changes the
  command-C output (`[~]` → 8; `[ ]` → 6). Recommendation: reconcile SHONEN box 3 with the
  calibration report by append-only LOG entry before any calibration figure is cited.

### MEDIUM-1 — Depth scalar counts duplicate rows; the unique-gate count is informational only

- Depth score is `recorded_cases` (`measure.py:45`, command D `SCORECARD.md:73`), a raw regex
  count. `unique_recorded_gates` (`measure.py:41`) is printed but feeds no score.
- Probe (in `/tmp`, removed): appending one extra header row
  `#   bash-surface-census kagi-shokunin/corpus/surface-census.sh 8/10 (80 %)` yields
  `recorded_cases=7`, `unique_gates=6`. Depth would read 7 with no new gate.
- `LOG.md:663` says the unique-gate reporting prevents duplicate rows from masquerading as
  independent cases. The script does not use it that way; that claim is inaccurate as written.
- Current state is not inflated: 6 header rows, 6 unique gate paths, 6 distinct pins that
  resolve, 6 leg invocations (`mutate-and-run.sh:1113-1138`). Round-12 has not modified
  `tools/mutate-and-run.sh` (git status clean on that path).
- Live risk: `SCORECARD.md:271-272` plans "witness-scoped split on a bash leg … recorded as a
  ledger case. Before: command D 6 → after 7." That is the exact inflation path the probe
  reproduces. Recommendation: depth = unique gate paths, each with a resolving pin and a
  `--regression` PASS at HEAD; a witness split is a sub-measurement on the existing leg, not a
  new header row. The ScorecardReview seat recommends the same rule (its HIGH-2).

### MEDIUM-2 — Depth counts documentation rows, not executed legs

- `SCORECARD.md:66` discloses this ("measures documented case depth, not newly executed cases").
  Reproduced: depth 6 is a count of header comment rows. Execution is not checked by the score.
- The six pins (`mutate-and-run.sh:543-553`) do resolve in their sibling repos (positive
  check above). A "pin resolves" test is not part of command D, so a stale or deleted pin would
  still score 6. Recommendation: add the resolve check to the scored command.

### LOW-1 — Positional mark indexing

- `measure.py:31` uses `marks[box - 1]`, so scoring follows checkbox position, not box identity.
  Inserting or reordering a box in SHONEN.md silently changes which box is scored.

### LOW-2 — Worktree output is not a pinned measurement

- `measure.py` without `--rev` reads the working tree: `source_status.mined` = 15 vs 12 at HEAD
  from uncommitted `corpus/SOURCES.md` (git status ` M`). Scalars are unaffected, but worktree
  output must not be cited as a measured commit (`SCORECARD.md:88-89`, the measured-commit cells).

## 4. Capability inflation check (positive finding)

- `measure.py:35` (`repeat_control_artifact`) and `:36` (`bash_witness_summary`) are output-only.
  Neither feeds `calibration_restraint_score` (`:31`) or `recorded_cases` (`:45`). The presence
  flag is `bool(content)`, so a non-empty file counts as present, not as demonstrated.
  Landing `tools/repeat-control.py` as-is does not change depth or calibration.
- `tools/repeat-control.py` and `tools/bash-witness-study.py` contain no `#   js-…`/`#   bash-…`
  header rows (grep, none). They do not feed depth.
- Caveat: a C2 edit adding a witness row to `tools/mutate-and-run.sh` header would raise depth
  (see MEDIUM-1). The witness split must not add a header row.
- `LOG.md:663` states "Depth and calibration stay 6 (delta 0)". That matches the measured output
  at HEAD. The gain is in repertoire/detail, not in scalars.

## 5. Verdict on the two pinned values (advisory)

- **depth 6:** the value is numerically reproducible at HEAD and each counted gate has a resolving
  pin. It is not capability-inflated. It is inflatable by a duplicate header row, and one planned
  step (`SCORECARD.md:271-272`) would do exactly that. Hold at 6 under a unique-gate rule.
- **calibration 6:** not reproducible from the documented command (command C → 8; HIGH-1). Rests
  on lane self-attested marks that `SCORECARD.md:163-164` excludes (HIGH-2). Box 3 record conflict
  (HIGH-3). Treat as **inflated relative to the scorecard's own rules** until a non-author review
  of boxes 1, 2, 4 exists or the rule is amended by a dated LOG entry.

## 6. Residual risk and verification gaps

- Not executed by this seat (not assigned): `tools/mutate-and-run.sh --selftest`,
  `--regression`, `tools/repeat-control.py --selftest`, the C2 sweep.
- The box-1/2/4 anchor resolution and the independence of the admit/reject spot-check were
  taken from `ScorecardReview` (`.ufo/waves/round-12/w1/ScorecardReview.md`) and from reading
  `corpus/lessons/round-1-verifier-spotcheck.md`; neither was re-verified here.
- Discernment trend: `round-1-verifier-spotcheck.md:17` says "discernment improved"; the
  SCORECARD fleet table records discernment as `unprovable-but-better` (`SCORECARD.md:118`).
  Learning-trend, not one of the two scored axes; reported for L1 to reconcile.

## 7. Tooling

None installed or updated by this seat.
