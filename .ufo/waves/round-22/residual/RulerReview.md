# RulerReview — round22 C1 frozen ruler, gate selftest, bundles, callback projection

Reviewer: `TameshiR22.RulerReview` (critic). Candidate `e4da41c3102f6f90b42257d4b8785335806ef954`,
base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`. Static read only: no tests, no gate execution,
no git/jj mutation, no installs. Read-only facts were taken with `git show`/`git rev-parse`,
`sha256sum`, and `python3` JSON comparisons that do not import the gate.

## Verdict

No blocking defect in the ruler, the gate, or the bundles. There is one blocking release
precondition: a receipt is cited but not yet landed (R1). Six nonblocking ruler-strength or
provenance limits follow; the judge should weigh them as tradeoffs and not treat them as fixable
candidate defects.

## Frozen identity

- `.ufo/evidence/round-22/measure.py` has blob `b29573dbea55884eb6f6372d55ed58f6bb111d99`, the same at
  `81106f9` (freeze), at `e4da41c` (candidate), and in the worktree; sha256 is
  `f833d067afd3ca17b8534fc942d6e8ed529edd3d55476802c18ea631c0678056`. Its only commit is
  `81106f9`. It was frozen at 10:36:06-03:00, before `tools/wave-accounting.py` existed
  (`66a25ab`, 10:42:58-03:00). So the expected IDs predate the evaluator, and the selftest oracle
  is independent of `evaluate()` in authorship order.
- `tools/wave-accounting.py` has sha256 `d63e89e1…5ac5f4`. `e4da41c` changes only
  `sys.dont_write_bytecode = True`, which has no verdict effect. Tracked
  `tools/` and `.ufo/evidence/round-22/` are clean against the candidate.
- The `contract.json` predicate list matches `measure.CASES` names in order.

## All eight expected exit/finding pairs (static trace of `evaluate`/`run`)

Control fixture: two members, both outcomes with `replaced: false`, one completed, one failed,
both reports present, claimed totals 2/1/1. The trace gives exit 0 with `finding_ids == []`, and
the failed-with-report seat is only inventoried in `failed_with_report`. The control guard holds.

| Case | Mutation | Predicted exit | Predicted finding set | Expected | Pass |
|---|---|---|---|---|---|
| false-completion-count | claimed seats=3 | 1 | {TOTAL_MISMATCH} | 1 / TOTAL_MISMATCH | yes |
| failed-with-report-counted-completed | claimed completed=2, dead=0 | 1 | {TOTAL_MISMATCH} | 1 / TOTAL_MISMATCH | yes |
| missing-outcome | pop dead outcome | 1 | {MEMBERSHIP_MISMATCH, TOTAL_MISMATCH} | 1 / MEMBERSHIP_MISMATCH | yes |
| duplicate-agent | member[1].id and outcome[1].id = seat.pass | 1 | {DUPLICATE_AGENT} | 1 / DUPLICATE_AGENT | yes |
| unknown-status | outcome[1].status=unknown | 1 | {TOTAL_MISMATCH, UNKNOWN_STATUS} | 1 / UNKNOWN_STATUS | yes |
| registry-id-mismatch | outcome[1].id=seat.other | 1 | {IDENTITY_MISMATCH} | 1 / IDENTITY_MISMATCH | yes |
| replacement-seat | outcome[1].replaced=true | 1 | {REPLACEMENT_FORBIDDEN} | 1 / REPLACEMENT_FORBIDDEN | yes |
| snapshot-tampering | append `b' '` after the digest is written | 2 | {SNAPSHOT_TAMPERED} (`run`, before decode) | 2 / SNAPSHOT_TAMPERED | yes |

The static prediction is 8/8. Tampering is distinguished from the other exit-2 path
(`INVALID_INPUT`) by its finding ID, so a parse failure cannot pass case 8.

## Tool-absent baseline meaning

`before.json` contains exit 1, `tool_present: false`, `cases: []`, and `discriminated: 0`, taken at
13:35:48Z. That is after base `51d49d5` (13:15:40Z) and before freeze `81106f9` (13:36:06Z). The
early return at `measure()` lines 26–28 is the only code path it exercised. So 0/8 means "the public
CLI does not exist", not "eight fixtures ran and were accepted". SCORECARD, LOG, `corpus/lessons/round-22.md:48`, and
`w1/CounterThreats.md` state this honestly ("tool absent, discriminated0/8, exit1").

## Frozen 146 bundle and wrong-count bundle

- Digests match: `bundle.json` hashes to `dfb1027f…845c18e` (= `expected.json`) and
  `wrong-count-bundle.json` hashes to `d984c49c…a17a17e` (= `wrong-count-expected.json`).
- The only difference between the two is the wave2 `claimed` block: 38/37 (corrected) versus 40/35
  (wrong). 40 is exactly the wave2 report-file count, which reproduces the historical
  report-count inference. Wave1 is identical (reports 28 = completed 28).
- Static invariant replay of the corrected bundle found no duplicate agent across the 146 IDs.
  Reports are a subset of members, outcome names equal member names, and the only statuses are
  {completed, failed}. Claimed totals are ints equal to 71/28/43 and 75/38/37, all
  `replaced: false`. So the expected result is exit 0 with `finding_ids == []`, totals 146/66/80,
  matching the `tools/registry.json` `wave-accounting-frozen-entry`. The wrong-count bundle should
  give exit 1 with `{TOTAL_MISMATCH}` only, from wave2.
- The bundle agrees with the base sources pinned in `derivation.json`. All four input sha256 values
  verify at `51d49d5`. The members' name, agentId, and role match `round-21/w{1,2}/swarm-registry.json`
  exactly, with 0 mismatches and no extras. Outcome name, id, role, and status match
  `original-outcomes-final.json` rows with 0 diffs. Report basenames equal the `.md` files in each
  base reportDir (28 and 40). The failed-with-report seats are `ProfileBashTsukuroiCensus` and
  `V01WitnessTests`, and both stay failed.

## Raw callback corroboration and projection limits

- `round21-callbacks.json` has 146 unique rows. Every `callback_sha256` equals sha256(callback),
  and every `<task-result id agent status>` header equals the row's id, role, and status. Statuses
  are 66 completed and 80 `failed (exit 1)`. Normalized, they agree with the bundle on all 146
  (status and role), matching `round21-callback-corroboration.json` (146/146/146).
- The 24 rows with a `source` field (all wave2, including both failed-with-report seats) cite
  `.ufo/waves/round-21/wait2-recovered-*.json`. I verified that all 24 callback texts are present in
  those files at base. They are independently corroborated by retained repo bytes.
- The 122 rows with `source_line`/`timestamp` name no file. The top-level `source` points to the
  predecessor session's async deliveries, which are not in the repo. Projection limit: their
  corroboration is self-referential. The same lane copied the text and authored the bundle, and
  no repo artifact lets a third party re-derive them. This is within contract bound 1 ("declared
  inputs, not authenticated provider telemetry") and is stated in the lesson and knowledge file.
- The 28 wave1 completed rows lack `replaced` in `original-outcomes-final.json`. The bundle
  normalizes them to `false` from the round21 lesson declaration (per `derivation.json`). So for
  those 28 seats, a clean REPLACEMENT_FORBIDDEN on the historical bundle comes from that
  normalization and is not evidence from the data. This is disclosed.

## Findings

R1 — **blocking (release precondition, not a code defect).** The header of
`corpus/knowledge/callback-authoritative-accounting.md` ("final committed-revision execution is
retained in .ufo/evidence/round-22/final/verification.json") and `corpus/lessons/round-22.md:46`
("Actual streams are retained in round22 final/verification.json") cite a file that does not exist
at the candidate. Glob `.ufo/evidence/round-22/final/**` returns 0 files. Impacted axis: false
provenance. Smallest correction: L1's single integrated run lands that receipt, with the measured
commit, `measure.py` sha256 `f833d067…`, tool sha256, the exits and streams of the selftest, the
frozen entry, the wrong-count entry, and `measure.py`, before admission. Otherwise, reword both
citations to future tense.

R2 — nonblocking (ruler strength; frozen, so a judge tradeoff). `measure.py` line 77 accepts any
finding superset (`finding in finding_ids`) and does not check exclusivity. Counterexample: a
degenerate CLI could exit 0 with [] on a sha match of the control fixture and otherwise exit 1
with all seven IDs, plus the digest check. That CLI scores 8/8 with no accounting logic. Only the
146 frozen entry and the wrong-count pair would reject it. The actual tool emits exact sets (see
the table), so the candidate is unaffected. Impacted axis: calibration ruler validity. Do not count
8/8 as stronger than "eight predicates discriminated by a real evaluator, confirmed by the 146
replay". Do not edit the frozen counter.

R3 — nonblocking (duplicate authority). `wave-accounting.py --selftest` calls the same
`measure.measure()`. The selftest pass and the contract's after = 8/8 are one observation, and the
SKILL row discloses this. The selftest covers none of these other branches: `DUPLICATE_WAVE`,
`DUPLICATE_MEMBER`, `DUPLICATE_OUTCOME`, `UNKNOWN_REPORT`, cross-wave `DUPLICATE_AGENT`, or the
`INVALID_INPUT` paths (schema, duplicate JSON key, nonfinite value, bool or negative claimed,
lowercase-digest check). Impacted axis: premature saturation if those branches are cited as
tested. Smallest correction: claim only the eight.

R4 — nonblocking (falsifier not registered). QUALITY45's falsifier is the wrong-count bundle,
expected to exit 1 with TOTAL_MISMATCH. It appears in QUALITY, the lesson, and the knowledge file,
but there is no `tools/registry.json` entry for it, although the registry already holds five
entries that expect exit 1. The census therefore never re-runs the red half. Smallest correction:
append a `wave-accounting-wrong-count` entry with `expect.exit: 1` and
`stdout_contains: ["TOTAL_MISMATCH"]`.

R5 — nonblocking (verdict-map edge). An uncaught `subprocess.TimeoutExpired`, a non-dict JSON
stdout (`result.get` raises `AttributeError`), or an `OSError` in `measure()` would exit 1 with a
traceback. The documented map reserves 2 for setup could-not-evaluate. This also applies under
`--selftest`, where the `FINDING:` line would be missing. None of these is reachable with the
candidate tool on the frozen fixtures. The counter is frozen, so record this and don't change it.

R6 — nonblocking (provenance binding). `before.json` records argv and stdout but not the sha256 of
`measure.py`, and it ran 18 s before the freeze commit. The 0/8 outcome depends only on the
tool-absent branch (lines 26–28), so drift could not change it. The final receipt should still
record the frozen blob `b29573db…`. `round21-callback-corroboration.json` has no generating command
and no input digests (callbacks sha `c2db7db5…`, bundle sha `dfb1027f…`). It is a retained
assertion, not a re-derivable projection. Smallest correction: add both digests and the
comparison rule to the final receipt.

R7 — nonblocking (naming and denominator). Case 1, "false-completion-count", mutates `seats`, not
`completed`. Cases 1 and 2 hit the same `claimed != summary` comparison through different fields.
The eight predicates are seven distinct detector branches, and neither case emits a dedicated
report-inference finding. The docs already separate 8 synthetic predicates from 146 seats and 2
historical false positives. No change is needed, provided no one claims 8 independent detectors.

## Not observed / inference

- [INFERENCE] The exit/finding predictions come from reading code. Python version effects were not
  exercised. The environment of `python3` is unscrubbed except for `GIT_*`, so
  `PYTHONPATH`/`PYTHONHOME` could in principle shadow stdlib modules. That is a hermeticity limit,
  not a candidate defect.
- No installs or updates were performed.
