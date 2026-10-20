# S02 — `tools/repeat-control.py` registered commands at the live lane

Seat: TameshiR17.S02RunRepeatControl (scout, leaf). Lane rev `98bea7da5801f4bc58e4187690ee1687c8a5061f`
(HEAD unchanged before and after). All runs read the live lane and wrote only under
`/tmp/tameshi-r17w1-S02RunRepeatControl-3I7pJa` (scratch), cwd = lane root for every invocation.

Tool identity [O]: `tools/repeat-control.py`, committed blob `70c91e7e6b1957d6b1eaa106b2be2659d042cfd7`,
35,454 B, sha256 `296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25`,
`VERSION` `repeat-control.py r12 (tameshi-shokunin, 2026-10-20)`; interpreter `python3` 3.14.8
(every run's `command.txt` records tool path, tool sha256, cwd, python).

Registered sources: `SKILL.md:1503` (round-12 gate/probe registry row: entry
`--runs 3 --out DIR -- COMMAND ARG...` or `--snapshot DIR`, verdict map `0 clean; 1 failed; 2 and 64
could-not-evaluate`, self-test `--selftest`, pinned values `.ufo/evidence/round-12/ControlGate/expected.json`
and `.../mismatch/expected.json`); the concrete live invocations are registered in
`.ufo/evidence/round-12/verify-round.py:34-37,48` with retained results in
`.ufo/evidence/round-12/verification-final.json` (checks 0–5, `tool_sha256` `296fe566…`, `passed: true`).

## Results

Every command below was run once unless a repeat is named; raw stdout/stderr and exits were saved under
the scratch path and are quoted from those files.

| # | Command (registered) | Registered outcome | Observed exit / marker | Held? |
|---|---|---|---|---|
| 1 | `python3 tools/repeat-control.py --selftest` | exit 0, all embedded cases at recorded ID/exit, `SELFTEST: PASS` | exit 0; `SELFTEST: PASS (29 cases)`; all 29 `SELFTEST_CASE … PASS` incl. `snapshot-committed-stable`/`-mismatch` | **yes** |
| 2 | `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` | pinned `controls_match` / exit 0 (`expected.json`) | exit 0; `SNAPSHOT_INPUTS 9 verified`; `SNAPSHOT_EXPECTED id=controls_match exit=0`; `SNAPSHOT_OBSERVED id=controls_match exit=0`; `REPEAT_CONTROL: controls_match` | **yes** |
| 3 | `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch` | pinned `controls_mismatch` / exit 1 (`expected.json`) | exit 1; `SNAPSHOT_INPUTS 9 verified`; `SNAPSHOT_EXPECTED id=controls_mismatch exit=1`; `SNAPSHOT_OBSERVED id=controls_mismatch exit=1`; `REPEAT_CONTROL: controls_mismatch` | **yes** |
| 4 | `--runs 3 --out DIR -- env -u THE_JANITOR_BIN -u SQLITE3_BIN -u CENSUS_BREAK -u DEEP bash .ufo/evidence/round-12/BashWitness/pristine.sh --selftest` (verify-round.py:37, `real-pristine-three-controls`) | exit 0, `REPEAT_CONTROL: controls_match`, three identical 1202-byte stdouts | exit 0; `REPEAT_RUN 1..3 exit=0 stdout-bytes=1202 stderr-bytes=0`; `REPEAT_COMPARE identical=yes runs=3`; `REPEAT_CONTROL: controls_match` | **yes** |
| 5 | `python3 .ufo/evidence/round-12/FailureOracle/verify_gate.py --gate tools/repeat-control.py --fixture changing-fixture.sh --out DIR --expect controls_mismatch` (verify-round.py:48, `green-after-restored-repetition`; fixture rebuilt by the same substitution: `CONTROL` on run 1, `ALTERNATE` after) | verifier exit 0 / `VERDICT: PASS`; gate `controls_mismatch` exit 1 | verifier exit 0; `observed_exit=1`; `expected_finding_observed=true`; `VERDICT: PASS`; gate stdout `run 1 … 8 B`, `run 2/3 … 10 B`, `REPEAT_COMPARE identical=no`, `REPEAT_CONTROL: controls_mismatch`; `finding.txt` `REPEAT_EXIT: 1` | **yes** |
| 6 | `--runs 3 --out DIR -- sh .ufo/evidence/round-12/FailureOracle/fixture.sh` with `FAILURE_ORACLE_STATE` in scratch (registered receipt `FailureOracle/actual-pristine/gate-runs/`) | exit 0, `REPEAT_CONTROL: controls_match` | run twice, both exit 0; `REPEAT_COMPARE identical=yes runs=3`; three 8-byte `CONTROL\n` stdouts; fixture state advanced 1→3 | **yes** |
| 7 | verdict map class 1: `--runs 3 --out DIR -- sh -c 'date +%s%N'` | 1 (`controls_mismatch`) | exit 1; `REPEAT_COMPARE identical=no runs=3`; `finding.txt` `REPEAT_EXIT: 1` | **yes** |
| 8 | verdict map class 2: `--runs 3 --out DIR -- sh -c 'exit 7'` | 2 (`baseline_nonzero`) | exit 2; `REPEAT_RUN 1..3 exit=7`; `REPEAT_COMPARE identical=yes runs=3`; `finding.txt` `REPEAT_EXIT: 2` | **yes** |
| 9 | verdict map class 2: `--runs 3 --out DIR -- tameshi-r17-no-such-command-xyz` | 2 (`command_unavailable`) | exit 2; `REPEAT_RUN 1..3 exit=unavailable`; `REPEAT_CONTROL: command_unavailable`; `finding.txt` `REPEAT_EXIT: 2` | **yes** |
| 10 | verdict map class 64: `--runs 2 …`, existing `--out`, and no args | 64 (`invalid_usage`) | exit 64 each: `--runs must be >= 3, got 2`; `--out already exists (refused, never overwritten)` (refused dir unchanged); `no arguments` — each ends `REPEAT_CONTROL: invalid_usage`, and none created the requested `--out` | **yes** |
| 11 | boundary: `--snapshot` on a run-mode DIR (no `expected.json`) | docstring: run-mode DIR refused, `snapshot_tampered` (2, could-not-evaluate) | exit 2; `SNAPSHOT_TAMPER expected.json unreadable …`; `REPEAT_CONTROL: snapshot_tampered` | **yes** |
| 12 | boundary: `--snapshot /nonexistent-r17-dir` | 64 (could-not-evaluate in the row map) | exit 64; `--snapshot DIR is not a directory`; `REPEAT_CONTROL: invalid_usage` | **yes** |

Note on the `REPEAT_COMPARE identical=` line: it is emitted as `yes` only for the two agreement
classes (`controls_match`, `baseline_nonzero`) — `tools/repeat-control.py:335-336` computes
`agreed = finding in ("controls_match", "baseline_nonzero")` — so `identical=no` beside
`command_unavailable` (row 9) is the fixed precedence, not a disagreement finding.

## Observed facts

- The selftest's own scratch tree (`/tmp/tameshi-r12-repeat-control-selftest.*`) was removed on pass:
  after runs 1–2 no such directory existed. The selftest re-validated both committed snapshots
  internally (`snapshot-committed-stable`, `snapshot-committed-mismatch`), matching rows 2–3.
- The registered live control (row 4) reproduced the round-12 recorded observation exactly:
  same tool sha256 `296fe566…`, `stdout-bytes=1202` on all three runs, same finding/exit. Row 5
  reproduced the recorded mismatch arm (gate exit 1 under a changing fixture) with the verifier's
  `VERDICT: PASS`.
- The run-mode pristine receipt (row 6) is stateful (`FAILURE_ORACLE_STATE` increments) yet emits
  identical bytes; both repeats produced `controls_match`, so the registered outcome is not a
  one-shot observation.
- Immutability of inputs: `git status --porcelain -- tools/repeat-control.py
  .ufo/evidence/round-12/ControlGate .ufo/evidence/round-12/BashWitness/pristine.sh
  .ufo/evidence/round-12/FailureOracle tools/` printed nothing before and after the runs; the tool
  sha256 was identical at start and end. No lane file was written by this seat.
- Concurrent sibling activity was visible lane-wide during the window (` M .gitignore`,
  ` M .ufo/evidence/round-16/round-gate/runner-sha256.txt`, new round-15/17 untracked trees). None of
  those paths is read by these commands; HEAD stayed `98bea7d`.

## Discrepancy found (not a registered-command failure)

`corpus/knowledge/repeated-control-precondition.md` carries stale identity/snapshot facts at this rev:

- `:58` records the tool as 30,557 B, sha256 `29d8025490f3…`; the committed blob is 35,454 B,
  sha256 `296fe566…` (`git cat-file -s HEAD:tools/repeat-control.py` → 35454;
  `git show HEAD:tools/repeat-control.py | sha256sum` → `296fe566…`). `git log -- tools/repeat-control.py`
  has a single commit (`9df9212`), so `29d80254…` is not a committed lane blob —
  [INFERENCE] it was a mid-round worktree revision, consistent with the older `actual-pristine`
  receipt that records it.
- `:64` calls `29d80254…` "the … now in the tree"; `:66` states no `expected.json` exists anywhere
  under `.ufo/evidence/round-12/` and that no snapshot verdict is claimed. Both
  `ControlGate/expected.json` and `ControlGate/mismatch/expected.json` are committed at this rev and
  validate (rows 2–3: 9 inputs each, recorded IDs/exits reproduced). The note's *behavioural*
  description (interface, precedence, exit classes) matches every observation above; only those two
  `[O]` identity/arm claims are stale at `98bea7d`.
- Round-12 receipts span two tool revisions (actual-pristine at `29d80254…`, `verification-final.json`
  at `296fe566…`); the registered live commands hold at the later, committed revision.
- `command.txt` records python 3.14.8; round-12 receipts recorded 3.14.7. The control was byte-stable
  under the current interpreter, so this is host drift, not a registered pin for this row.

## Remaining unknowns

- No timeout/hang arm was exercised: the registry row declares no timeout and no process supervisor,
  and a hang yields no verdict by design. Untested here.
- `--snapshot` behaviour on arbitrary caller directories copied out of other contexts is not a
  registered expectation; only the two pinned lane directories (rows 2–3) and the refusal boundaries
  (rows 11–12) were measured.
- `tools/registry.json` (the round-17 contract-B entry registry) did **not** exist at this rev
  (`ls tools/registry.json` → no such file), so no round-17 registry row wraps this tool yet. The
  ready-to-register observed outcomes for it would be: `--selftest` 0, `--snapshot ControlGate` 0,
  `--snapshot ControlGate/mismatch` 1, live three-control run 0, mismatch replay 1.

Verdict: **holds** — every registered `repeat-control.py` command returned its registered outcome at
`98bea7d` (tool sha256 `296fe566…`), and the only discrepancy is a stale tool-digest/“open arm” claim
in `corpus/knowledge/repeated-control-precondition.md`, not a behavioural deviation of the gate.
