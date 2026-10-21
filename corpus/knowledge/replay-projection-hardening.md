source: S085 — .ufo/waves/round-23/fresh-adjudication.json@6a1821a8897eea6e7d9669292160ec9593669409:53-104 (routed defects); S084 — https://docs.python.org/3/library/os.path.html#os.path.realpath ("Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path"); .ufo/evidence/round-24/contract.json
verified-at: 2026-10-21 — frozen eleven-predicate ruler before 1/11 at 6a1821a; later executed results are recorded in the round24 lesson and SCORECARD only after execution
recheck: python3 .ufo/evidence/round-24/measure.py --repo CLONE_AT_REV; python3 tools/registry-replay.py --selftest; python3 tools/command-binding.py --selftest

# Hardening a command-binding demonstration

A self-consistent replay can stay green while its weakest links drift. In
round23, falsifiers named the links. This entry turns each into a predicate
that can fail.

| Weak link | Hardened rule | Fails when |
|---|---|---|
| argv compared name-insensitively, case-folded, stripped or de-duplicated | supplemental fixtures swap argv between two names, change only case, pad a token, repeat a flag | a weakened comparison lets the public selftest pass |
| negative (signal-style) exits ignored | a fixture expects 0 and receives -9; a declared -15 that matches stays clean | `>= 0` short-circuits the exit check |
| stdout tokens checked with any() instead of all() | existing `all-of-tokens` fixture (round23) | only one of two required tokens is present |
| frozen-bundle registry row checks only `finding_ids` | the row also requires the exact `"bundle_sha256": "…"` literal from the sorted-key report | a different valid bundle plus regenerated expected file replaces the frozen one |
| replay publishes a bundle although the runner rejected a row | `tools/registry-replay.py --project` refuses: RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED | `held` is not `true` or `cleanup_error` is set |
| unbounded retained streams | `--max-stream-bytes` (default 1 MiB) refuses with STREAM_LIMIT | a stdout/stderr exceeds the bound |
| live-dependent rows reported as revision-pinned | `external` source rows and runner `non_hermetic_argv` rows are listed in `live_dependent` | the list omits such a row |
| sibling identity by string | `--plan` realpath-normalises lane, fleet root and siblings | a symlinked or `..` path alias changes identity |
| runner digest from the live tree | the runner is hashed from the clone copy that executes | — (recorded per run, not a ruler predicate) |

Superseding a registry row is append-only. The old row gets
`status: superseded` and `superseded_by`, and a new active row carries the
stronger expectation. The runner still executes superseded rows; they do
not count toward `held`.

## Bounds

- Receipt argv, cwd and revision remain the invocation parameters the
  instrument passes to the runner. They are not observed process metadata.
- A bundle digest pin means a later commit that changes both the row and the
  bundle selects a new contract. Neither the pin nor the gate authenticates
  the producer.
- Row commands run in a clone whose fleet mirror symlinks the live sibling
  repos. Realpath identity is not write isolation. Non-strict `realpath` may
  still leave missing components unresolved (S084).
- Four specific mutants killed is not general mutation adequacy.
- The eleven predicates are synthetic capability checks. They are not
  historical defects or an expertise score.

## Errata — round24 fresh wave 1 (2026-10-21, replacement L1 TameshiR24-2)

The table above overstates four rows. This section corrects them, append-only.
Seat reports: `.ufo/waves/round-24/w1/`. Executed after-measurement: 11/11,
exit 0 at c8c5b88 (`.ufo/evidence/round-24/after.json`). K4 is a control, so
ten predicates moved, covering seven mechanisms.

- Argv row: only name-insensitivity (K1) and whole-vector case-folding (K2)
  are predicates. The padded-token and repeated-flag fixtures are controls
  with no mutant. Case-folding only `argv[0]` and per-token prefix matching
  survive the selftest.
- Stdout row: only the any-token mutant is killed. Last-token-only,
  case-insensitive and whitespace-stripped matching survive (PredK4).
- Stream row: `--max-stream-bytes` refuses publication of the bundle only.
  `--run` retains complete streams in `observations.json` before the check,
  and no redaction exists. It does count UTF-8 bytes and is strict `>`
  (LabStreamBytes).
- Sibling row: the lane and fleet root are resolved. A symlinked sibling is
  mirrored under its target's name, unlike `registry-check --rev`, and that
  case is untested (PredK11, MutPlan, LabPlanLaneLink).

### Routed-defect disposition (round23 `fresh-adjudication.json` lines 48–106)

| Routed defect | Round24 disposition |
|---|---|
| argv name-insensitive mutant | K1 predicate |
| negative-exit mutant | K3 predicate |
| bundle_sha256 pins on two rows | K5/K6 predicates |
| runner held/cleanup/external carried | K7/K8/K10 predicates; the receipt schema still carries no live marker (sidecar `live-dependent.json`, not digest-covered) |
| runner digest from the live tree | implemented (clone copy hashed), verified by RevRunnerHash; no predicate |
| fleet root realpath | K11 predicate |
| unbounded streams / redaction | size half only, publication-only (K9); redaction open |
| loose stdout tokens | left frozen (no retrofill of the round23 requirements); open |

K2 (case-fold) is author-added, and K4 is a carried control.

### Further bounds

- `revision_pinned` means "not declared live". A row whose tool reads sibling
  objects through the mirror symlinks counts as pinned. Example:
  `mutate-and-run-regression` against kagi `fecee874` (OverlapKagi).
- `--project` validates less than its consumer. It can publish bundles that
  `command-binding.py` refuses with exit 2, and it can bind requirements that
  no frozen registry declares. A lone-surrogate stream exits 1, not 2
  (CodeProjectInputs).
- `--run` reads the frozen requirement/baseline pair from the working tree
  and binds the two files only to each other, not to `--rev`
  (OverlapKumitate).
- A refused run does not clear an earlier bundle in the same `--out`
  (CorpusSkill).
- Each of K7–K11 uses one fixture shape. See QUALITY49.
- The published bundle includes the live-dependent rows as ordinary receipts.
  So the command-binding gate's clean verdict covers all 43 rows. The 41/2
  split is visible only in the replay report and `live-dependent.json`
  (CodeRunReplay).
