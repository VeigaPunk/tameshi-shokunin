# R23-REATTACK Replay01 — row `repeat-control-snapshot-clean` (reviewer role, re-attack)

Round-25 re-attack of the round-23 wave-2 seat that died before reporting. Same scope as the
original item, verbatim goal: fresh falsification of the exact registry row
`repeat-control-snapshot-clean`, comparing the frozen argv/expect to the baseline source, the
newly retained invocation metadata and the full retained output (not tails), deciding between a
field-level false acceptance and a confirmed static exact binding, plus one concrete adversarial
delta — then the same judgment re-checked at lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`.

## Verdict

Static exact binding CONFIRMED. Every field the frozen contract declares for this row
(`name`, `argv`, `expect.exit = 0`) is byte-pinned and agrees at all five layers (SKILL anchor →
registry @ 496d212 → digest-pinned `registry-baseline.json` → `requirements.json` entry → bundle
requirement / receipt / observation), and the row's observable verdict (`controls_match` / exit 0)
was re-derived independently from committed snapshot bytes without executing any command. No
field-level false acceptance found in the round-23 artifacts. One concrete adversarial delta is
recorded (stdout semantics unpinned by the row's expect). The finding and the delta both apply
unchanged at `c9ff09f`.

Nothing was executed from the registry or any suite; the original "no repo writes" clause was
superseded to report-only. All commands below are reads and hash recomputations; scratch stayed in
`/tmp/rereplay01-scratch/`.

## Evidence actually present (all recomputed by me, not trusted from the artifacts)

1. **Registry pin holds.** `git show 496d212:tools/registry.json | sha256sum` →
   `ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a` — identical to the
   `registry_sha256` recorded in `.ufo/evidence/round-23/requirements.json` and
   `.ufo/evidence/round-23/replay/observations.json`, identical at the requirements'
   `source_revision` `28cae179…`, and identical to
   `sha256sum .ufo/evidence/round-23/registry-baseline.json` (the file the runner actually
   digest-checks, `.ufo/evidence/round-23/replay.py:35-37`).
2. **Executed-tool identity holds.** `git show 496d212:tools/repeat-control.py | sha256sum` →
   `296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25` — exactly the
   `tool-sha256=` in the retained stdout banner. The tool has one commit in its history
   (round-12 `9df9212`) and the working-tree file hashes to the same digest today.
3. **Runner pin holds and means what it says.** `observations.json` `runner_sha256` is
   `cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad`;
   `sha256sum tools/registry-check.py` (working tree = 496d212 blob, no commit since 496d212)
   → same value. Note the field digests `tools/registry-check.py`, not `replay.py`
   (`.ufo/evidence/round-23/replay.py:78`) — `replay.py` itself hashes `adb4171652f9…` and
   appears nowhere as a pin (naming gap, not a defect; see gaps).
4. **Bundle tamper pin holds.** `sha256sum .ufo/evidence/round-23/replay/bundle.json` →
   `3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9` ==
   `bundle_sha256` in `.ufo/evidence/round-23/replay/expected.json`
   (schema `command-binding-expected-v1`).
5. **Row equality across all layers.** Registry row @496d212 == `requirements.json` entry ==
   `bundle.json` requirements entry == observation `requirement`, all
   `{"argv": ["python3","tools/repeat-control.py","--snapshot",".ufo/evidence/round-12/ControlGate"],
   "expect": {"exit": 0}}`. Receipt and observation agree byte-for-byte on `argv`, `cwd`
   (`/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`), `revision`
   (`496d212bc46789cdf8cafab72978bdb7f4182963`), `exit` (0), `stdout`, `stderr` (empty).
   Full output retained, not tails: `stdout == stdout_tail` and `stderr == stderr_tail` (the
   5-line output is under the tail cutoff; `run_row` retains complete streams only under
   `retain_streams=True`, `tools/registry-check.py:60` call, `:724-726` retention).
   Invocation metadata is real and internally consistent: row `measurement_interval` delta is
   77.4 ms against `runner_result.elapsed_s = 0.077`.
6. **Verdict re-derived from committed bytes (no execution).** Working-tree
   `.ufo/evidence/round-12/ControlGate/` is byte-identical to the 496d212 blobs (per-file
   `git show` comparison, all 10 top-level files). `expected.json` declares schema
   `repeat-control-snapshot-v1`, `runs: 3`, `expected_id: controls_match`, `expected_exit: 0`,
   and 9 input digests. All 9 digests verify against the committed `run-{1,2,3}.{stdout,stderr,exit}`
   bytes; the three run tuples are byte-identical with exit text `0`, which under the frozen
   `classify()` precedence recomputes to `controls_match` / 0 — equal to the recorded expectation.
   The stdout line `SNAPSHOT_INPUTS 9 verified` is `len(record['inputs'])` (9 = runs×3); the 20
   files under the ControlGate tree include the `mismatch/` subdirectory (a separate row's
   snapshot, excluded by the tool's isdir filter) and both `expected.json` manifests, so "9" is
   exact, not a shortfall.
7. **Frozen evaluator recomputation over the whole bundle: zero findings.** 43 receipts / 43
   requirements, membership exact, no duplicates; for every row `argv`, `cwd`, `revision`, `exit`
   match and `stdout_contains` (absent for this row) is vacuous — the exact predicate set of
   `evaluate()` in `tools/command-binding.py`, unchanged since round 23. The generator's own
   pre-run guards force this equality before anything executes
   (`.ufo/evidence/round-23/replay.py:36-41`: digest check, then requirements-projection equality).
8. **Source anchor is genuine, not retrofilled.** The row's `source: SKILL.md@98bea7d:1503`
   resolves to exactly the "repeated pristine controls" registry row
   (`SKILL.md` @ `98bea7d`, line 1503), and the anchor plus `timeout_s: 60` are already present in
   the frozen 496d212 registry row — nothing was added to this row after round 23.

## Present versus inferred

- **Present:** items 1–8 above. Every digest and every field equality was recomputed from
  committed bytes; none is taken on the artifacts' word.
- **Inferred (unavoidable):** that the recorded stdout came from a real process spawn. The
  `/tmp` clone is deleted and the original item forbids re-execution, so the act of execution is
  witnessed only by the transcripts' mutual consistency (matching banner sha, source-shaped emit
  sequence, plausible intervals). This does not weaken the acceptance: the row's verdict was
  re-derived here from committed snapshot bytes plus the frozen algorithm, so even a wholly
  authored transcript could not change what the committed evidence computes to.
- **Producer authentication rejected:** no signature, identity, or historical attestation was
  relied on; the round-23 author being trustworthy is irrelevant to this result. Historical
  metadata retrofill rejected: the `source` anchor and `timeout_s` predate round 24 (present in
  the 496d212 registry), and `requirements.json`'s `source_revision` `28cae179…` is pinned by the
  same registry digest as the replay revision, so no metadata was backfilled into a changed past.

## Field-level false acceptance check

Confirmed static exact binding instead. The row declares only `expect.exit = 0`, and the runner's
held predicate is `held = got == expected_exit and not missing and cleanup_ok`
(`tools/registry-check.py:720`) with `missing = []` (no `stdout_contains` needles) — so `held`
reduces to exit equality plus process hygiene (hermeticity pre-check `:654-661`, 60 s timeout at
`:690`, descendant cleanup). Every accepted field contradicts nothing in the baseline source: the
retained stdout's five lines are exactly the `snapshot_mode()` emit sequence of
`tools/repeat-control.py` @ 496d212 for an intact, recomputing-clean snapshot, ending in
`REPEAT_CONTROL: controls_match` with `EXIT_BY_ID['controls_match'] == 0`.

## Concrete adversarial delta (bounded, does not invalidate the receipt)

`expect` pins exit only — no `stdout_contains` needle. A mutant `tools/repeat-control.py` whose
snapshot path **trusts the manifest** (returns `expected_id`/`expected_exit` from
`expected.json` without hashing any input — precisely the "recorded values are never trusted as a
verdict" failure its own docstring forbids) would print the identical five-line stdout on this
row (only the banner's `tool-sha256` changes, and no layer compares that field to a pin) and exit
0; the mismatch sibling would still exit 1 from its own manifest (`controls_mismatch`/1), so both
rows stay held, `command-binding.py evaluate()` raises no finding, and the retained full output on
either row cannot distinguish the mutant from the honest tool. Detection lives only in the tool's
`--selftest` tamper arms, which is a different invocation, not this row's frozen expect. The
recorded round-23 receipt remains consistent only with the honest tool given finding 6; the delta
marks what the row's binding does not pin.

## Currency at lane revision c9ff09f

- `c9ff09f` is an ancestor of working-copy HEAD `5b69fb2`;
  `git diff c9ff09f..HEAD -- tools/registry.json tools/command-binding.py tools/repeat-control.py`
  is empty, and `git status --porcelain tools/` is clean.
- Current `tools/registry.json` row `repeat-control-snapshot-clean`: still `status: "active"`
  (NOT superseded), identical `argv`/`expect`/`kind`, same `source` anchor and `timeout_s`.
- `tools/command-binding.py` at `c9ff09f` differs from 496d212 only in selftest fixture loading
  (round-24 commit `d2eaecd` adds `round-24/extra-cases.json`); `evaluate()`/`check()` are
  byte-identical.
- `tools/repeat-control.py` unchanged since round-12 `9df9212` (sha `296fe566…` today);
  `tools/registry-check.py` unchanged since `496d212`.

Therefore both the confirmed binding and the adversarial delta apply verbatim at `c9ff09f`.

## Residual risk and verification gaps

- The original execution act is unobservable (temp clone deleted); presence was established by
  recomputation, not re-execution, per the original item's no-rerun rule.
- `runner_sha256` invites misreading as `replay.py`'s own digest (`adb417…` matches nothing
  recorded); a reader must consult `replay.py:78` to interpret it. Diagnostics gap only.
- The 43-row bundle was recomputed for binding-field equality as a whole, but only this row's
  verdict was re-derived from its snapshot bytes; sibling rows were out of scope.
- The exit-only expect pattern is registry-wide among baseline rows; the adversarial delta
  generalizes beyond this row to every row whose stdout semantics carry the verdict.

R23-REATTACK Replay01: AGREE
