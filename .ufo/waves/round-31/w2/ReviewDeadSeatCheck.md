# ReviewDeadSeatCheck — review of `dead-seat-check.py` at 2da841bd9913a2037d2bf612793382e572c9d205

Seat: `TameshiR31.ReviewDeadSeatCheck` (leaf; no subagents). Scope: the committed artifact
`.ufo/evidence/round-31/dead-seat-check.py` vs QUALITY criterion 68 and round-30 Mistake 4.
Read-only; nothing edited, no tools installed.

## Verdict

1. **Task text, not only names — yes.** The check compares the `# Target` band of each item's
   prompt (token-set Jaccard) in addition to exact normalised names. Verified on real bytes: a
   renamed copy of the real `ConnectorOverlap` target (two edits, name changed) is flagged
   `reason=target-similar jaccard=0.95`, exit 1. The name rule runs independently (the round-30
   dead list flags `ConnectorOverlap` by name, exit 1).
2. **Works on the lane's kept records — partially.** `spec-w1.json` works fully as both the dead
   side and the new-spec side (32 items parsed; targets extracted from `prompt`). `dispatch-w1.json`
   does **not** work: it is rejected with exit 2 and a clear message, because the dispatch record
   nests tasks under `taskCall.tasks` and has no `items`/`dead`/`seats` list. This is a shape
   mismatch, not a silent wrong answer — the gate is designed to run pre-dispatch on the proposed
   spec, not on the dispatch receipt.
3. **Default 0.60 is not sane for cold-read waves.** Measured on the real `spec-w2.json` cold
   targets: pairwise token Jaccard runs 0.938–0.970 (top: `ColdB02`/`ColdC02` 0.970). The real
   renamed re-dispatch copy scores 0.95. The two populations overlap, so the default flags every
   legitimate cold-read pair, while the suggested 0.98 would miss the genuine renamed re-dispatch.
   The limitation is honestly disclosed in the docstring and build report, but the committed default
   remains 0.60 and nothing enforces the documented override.

## Findings, by severity

### F1 (medium) — the committed check is not wired in, and does not itself enumerate the round's dead seats

The script takes a dead list as input and prints only the items it flags. It never derives the list
from the round's registry statuses or missing reports, and it cannot detect that a dead seat was
omitted from the input. Criterion 68's "a committed check lists every dead seat for the round" is
therefore only half-satisfied by the artifact alone.

Evidence:
- `grep "dead-seat-check|DeadSeat" <lane>` finds references only in the artifact itself, the spec/
  dispatch JSON, the build report and the contract; there is no call site in `tools/` or in the
  dispatcher. `BuildDeadSeatCheck.md:231-232` states wiring into the dispatcher is "out of scope".
- The round's own record of applying the rule for wave 2 is manual prose, not a tool run:
  `.ufo/evidence/round-31/contract-addendum-1.json:29` — "wave 1: 32 of 32 seats completed, none
  dead; no dead list exists, so .ufo/evidence/round-31/dead-seat-check.py has nothing to compare
  (it exits 2 on an empty dead list by design). Wave-2 item names are new."
- The author discloses the dependency: `BuildDeadSeatCheck.md:217-218` — "No history lookup. The
  gate does not read transcripts, the roster or attempt2-dead-seats.txt by itself; the operator
  chooses the dead list. Wrong input choice produces a true answer to the wrong question."

Smallest safe correction: commit a thin runner that builds the dead list for the round (from the
registry's member statuses / absent reports) and invokes the check before every wave-spec commit,
recording the invocation, the threshold and the output in the round's evidence directory.

### F2 (medium) — default `--min-jaccard 0.60` is mis-set for the exact wave class the criterion polices

Cold-read targets are near-identical across sections by construction (shared framework sentences),
so a cold-read-to-cold-read comparison — precisely the re-dispatch case criterion 68 exists to
catch — fires at the default. Raising the threshold to 0.98 would then miss genuine renamed
re-dispatches, since the measured renamed copy scores 0.95.

Evidence (measured at 2da841bd, token Jaccard over the `# Target` band, real specs):
- Within `spec-w2.json` (this round's cold-read wave): `ColdB02`/`ColdC02` 0.970,
  `ColdB01`/`ColdC01` 0.962, `ColdB03`/`ColdC03` 0.953, `ColdA02`/`ColdC01` 0.939,
  `ColdA03`/`ColdC02` 0.938. Confirms the wC calibration table (0.907–0.970) in
  `BuildDeadSeatCheck.md:164-171`.
- Real renamed re-dispatch copy (`ConnectorOverlapA2` from the real wC target): 0.95.
- The actual w1→w2 transition is clean at the default (max cross score 0.444; run below), so this
  round is unaffected — the hazard is for future cold-read gating.
- Disclosure lives at `dead-seat-check.py:37-42` (docstring) and `BuildDeadSeatCheck.md:159-187`
  (including the measured rejection of document-frequency and anchor refinements).

Smallest safe correction: require an explicit `--min-jaccard` with per-wave calibration recorded in
the wave contract, rather than letting the 0.60 default decide; or add a discriminator that does
not conflate the cold-read boilerplate with genuine re-dispatch (the author measured two candidates
that fail; a fresh rule is warranted before relying on any fixed cutoff).

### F3 (low) — `dispatch-w1.json` (kept dispatch record) is not an accepted input shape

Observed:
```
$ python3 dead-seat-check.py --dead <lane>/dispatch-w1.json --spec <lane>/spec-w2.json
DEAD_SEAT_CHECK_ERROR: <lane>/dispatch-w1.json: JSON has no "items", "dead" or "seats" list
exit=2
$ python3 dead-seat-check.py --dead <lane>/attempt2-dead-seats.txt --spec <lane>/dispatch-w1.json
DEAD_SEAT_CHECK_ERROR: <lane>/dispatch-w1.json: no "items" list
exit=2
```
The dispatch record's payloads live under `taskCall.tasks` (`name`/`agent`/`tools`/`task`/
`solutionSpace`; schema `ufo-swarm-wave-dispatch-v1`). The failure is loud and safe, and the
intended carrier (the wave spec) works; but anyone gating from the record the lane actually keeps
would hit exit 2. Smallest safe correction: either document this explicitly in the tool's help
(already implied by "new wave spec JSON") or add a tiny adapter mapping `taskCall.tasks` → items
with `prompt=task`.

### F4 (low) — selftest does not cover the explicit `"target"` key on a *spec* item

`entries_from_spec_item` (`dead-seat-check.py:120-121`) prefers an explicit `"target"` key when
present; the selftest exercises that branch only through dead-side JSON-list fixtures
(`:306-318`), never through a spec item carrying `"target"`. The branch works (verified by code
reading), but a future edit could break it silently. Smallest safe correction: add one selftest
fixture with a spec item that has `"target"` and no `"prompt"`-heading.

### F5 (low) — the comparison is not persisted by the tool itself

Flags print to stdout; the tally (`DEAD_SEAT_CHECK: dead=… items=… flagged=… threshold=…`) prints
to stderr. "Records the comparison and disposition" (criterion 68) therefore depends on the caller
redirecting both streams into a receipt. Smallest safe correction: fold the tally into the F1
runner's captured output file (e.g. `2>&1` into the wave evidence dir) and name it in the round
contract.

## Evidence — exact commands and observed output

All runs from `/fast/scratch/hyaku/tameshi-r31-seats/ReviewDeadSeatCheck` (script copied from the
committed file; lane referenced read-only; `timeout`-wrapped; `PYTHONDONTWRITEBYTECODE=1`).

```
$ sha256sum <lane>/.ufo/evidence/round-31/dead-seat-check.py
6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36
$ git -C <lane> show 2da841bd9913a2037d2bf612793382e572c9d205:.ufo/evidence/round-31/dead-seat-check.py | sha256sum
6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36   # file at REV == build source
```

Required fail run (round-30 dead list vs wave-1 spec):
```
$ python3 dead-seat-check.py --dead <lane>/attempt2-dead-seats.txt --spec <lane>/spec-w1.json
FLAG item=ConnectorOverlap dead=ConnectorOverlap reason=name-reuse jaccard=-
DEAD_SEAT_CHECK: dead=9 items=32 flagged=1 threshold=0.60
exit=1
```

Renamed-target rule on real bytes (fixture I built from the real wC `ConnectorOverlap` target, two
edits, renamed):
```
$ python3 dead-seat-check.py --dead dead-renamed.json --spec <lane>/spec-wC.json
FLAG item=ConnectorOverlap dead=ConnectorOverlapA2 reason=target-similar jaccard=0.95
DEAD_SEAT_CHECK: dead=1 items=38 flagged=1 threshold=0.60
exit=1
```

Wave-1 → wave-2 gating (this round's actual transition, at default and at 0.98):
```
$ python3 dead-seat-check.py --dead <lane>/spec-w1.json --spec <lane>/spec-w2.json
DEAD_SEAT_CHECK: dead=32 items=32 flagged=0 threshold=0.60
exit=0
$ python3 dead-seat-check.py --dead <lane>/spec-w1.json --spec <lane>/spec-w2.json --min-jaccard 0.98
DEAD_SEAT_CHECK: dead=32 items=32 flagged=0 threshold=0.98
exit=0
```
Max cross-wave score (w2 item vs w1 target): 0.444 (`CtlBindV5Fresh` vs `CtlBindV4New`).

Selftest and bad inputs:
```
$ python3 dead-seat-check.py --selftest
DEAD_SEAT_CHECK_SELFTEST: ok=17
exit=0
```
Threshold guard rejects `nan`/`inf`/0 (line 242-244) — consistent with QUALITY 31's finite-positive
rule.

## Residual risks and verification gaps

- Dead-list completeness is fully operator-supplied (F1); an omitted dead seat is invisible.
- Text-list dead seats carry no targets, so a renamed re-dispatch of a text-listed seat is
  undetectable unless the prior spec is used as `--dead` — documented at
  `BuildDeadSeatCheck.md:206-208`.
- No single cutoff separates cold-read twins (0.90–0.97) from genuine renamed re-dispatch (0.95)
  under the current tokenizer; the flag is a pointer, not a verdict (documented).
- I did not rerun the full 38-item self-comparison or the clean-pair fixtures from Build's scratch
  (seat boundary); I reproduced the equivalent behaviors: selftest 17/17, the required fail run,
  the renamed-target run on real bytes, and the w1→w2 clean run. The committed bytes are identical
  to the pasted build source (sha256 match above).
