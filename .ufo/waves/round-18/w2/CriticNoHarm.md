# CriticNoHarm — round-18 wave-2 no-harm falsification

Seat: TameshiR18.CriticNoHarm (FALSIFY lane critic, no-harm axes).
Read rev: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`; baseline `183f87b`.
All commands run in the contract clone `W=/tmp/tameshi-r18w2-CriticNoHarm-7shNsL`,
`C=$W/fleet/tameshi-shokunin` detached at the read rev, `env -u GIT_DIR -u
GIT_WORK_TREE -u GIT_INDEX_FILE [-u GIT_COMMON_DIR]`. No lane or sibling writes.

## Attack 1 — operability: is superseding the round-17 disposition rows a lost capability?

- Registry diff (python row-dict diff of `tools/registry.json` at the two revs):
  29 -> 35 rows; active 28 -> 32, superseded 1 -> 3. Changed:
  `evidence-disposition-round17` and `evidence-disposition-round17-before`
  active->superseded (superseded_by the round-18 rows);
  `evidence-disposition-round14-superseded` superseded_by retargeted
  round17->round18. Added active rows: `evidence-disposition-round18`,
  `-round18-before`, `trace-inputs-selftest`, `measure-round18-selftest`,
  `assemble-round18-selftest`, `defect-probes-selftest`.
- The old capability is still exercisable and still answers correctly:
  `python3 tools/evidence-disposition.py --root . --dispositions
  .ufo/evidence/round-17/dispositions.json --json` at read rev -> exit 2,
  `status=could_not_evaluate`, `expected_input_digest_mismatch` on
  `tools/bash-witness-study.py` (the file wave 2 moved). That is the correct
  v2 verdict for a moved input, and the *preserved* capability is the
  replacement: `--dispositions .ufo/evidence/round-18/dispositions.json` ->
  exit 0 `status=clean` counts `{effective:11, superseded:1, failed:0}`;
  `dispositions-before.json` -> exit 1 `status=failed`
  `expectation=producer_before`. Round-18 rows cover the identical check set:
  row-id diff of the two dispositions files = empty; round-18 adds exactly one
  historical_inputs entry (`tools/bash-witness-study.py` rev
  4acc607d, "moved by design in round 18"), which is what lets the new tool
  verify the old pinned bytes rather than the moved worktree blob.
- `supersedes` field: round-18 points at round-14's file, same as round-17 did
  (it supersedes the round-14 *dispositions file*, not the round-17 one; the
  row-level supersession is recorded in the registry). Correct, not a skipped
  link. Retargeting `round14-superseded`'s superseded_by to the round-18 row
  is the accurate current-replacement provenance.
- Post-receipt drift: `defect-probes.py` changed in 01d586d (ruler v2: P08
  fixture now `git config lane.branch master` like jj-lane init; child PATH
  prepends only `dirname $(which jj)`), while `registry-full-e08271a.json`
  (exit 0, held=32/32 active; the 3 superseded rows ran, printed got=2,
  excluded from the count) predates it. The selftest row at read rev still
  holds: `python3 .ufo/evidence/round-18/defect-probes.py --selftest` ->
  `SELFTEST: PASS (6 cases)`, exit 0 (ran here). v1->v2 diff is +6 lines,
  fixture-only; a jj-less host degrades to the v1 PATH — no new failure mode.
- C2 ruler receipts coherent: `c2-probes-v2-183f87b.txt` ends
  `open=11 closed=0 total=11`, `c2-probes-v2-e08271a.txt` ends
  `open=0 closed=11 total=11`; the errored v1 tip run is retained as
  `c2-probes-e08271a.txt`.

Verdict: no lost capability. Supersession preserved both directions.

## Attack 2 — calibration: does the carry + fresh-read design actually restore 60/60 and restraint 8?

Mechanism read: `measure.py` credits a section iff some ledger entry matches
its *body* sha256 (start-independent; survives line moves and a new page sha)
AND no non-stale failing entry vetoes. The input gate compares recorded
`inputs` sha256 against blobs at the measured REV, so an entry whose inputs
moved is `input-drift` (no credit) and, if failing, `entry_is_stale` =>
no veto (fail-closed only for non-stale failures).

Live experiment at read rev:

- `python3 .ufo/evidence/round-18/coldread/assemble.py --carry
  .ufo/evidence/round-17/coldread/ledger.json --repo . --out
  /tmp/carry-ledger.json` -> exit **1**, "coverage: 52/60 buckets covered
  (skill 2e20e549d8c3)". The 8 uncovered buckets are exactly the sections
  whose bytes wave 2 changed: starts 6 (title), 921/933 (leg ledger rewritten
  for eight legs), 1021, 1380, 1855, 1905 (new "## Eighth recorded case —
  round 18"), 1923 (new registry section). Carry coverage is by section sha
  and does not hallucinate coverage for edited sections — correct.
- `python3 .ufo/evidence/round-18/measure.py --rev 01d586d… --repo .
  --ledger-file /tmp/carry-ledger.json --explain` -> exit 0,
  covered 10/60, `calibration_restraint_score=6`, `depth_score=8`,
  `recorded_cases=8`, `ledger_guardrail.lists_agree=true`
  (header=regression_calls=selftest_tuples=8, unique_recorded_gates=8).
  The other 50 sections all fail as `input-drift:<moved files>` — matching
  the claimed "50 of 60 buckets lost input-keyed credit".
- Hard-veto audit: all 5 failing-verdict carried entries (starts 497, 1021,
  1069, 1676, 1806) have non-empty inputs and every one is stale at read rev
  (each recorded at least one of the files wave 2 rewrote) — zero vetoes in
  the measure run. 60/60 is therefore reachable: the 10 still-verifying
  carried entries plus fresh reads of the 50 drifted sections.
- Traps checked and absent: `IGNORED_INPUTS` now drops both round-17 and
  round-18 ledger paths, so a seat citing the *old* ledger path cannot
  manufacture drift; `assemble.py` likewise drops both ledger keys
  (DROPPED_INPUT_KEYS). `BOX3_LINK` retargeted to
  `.ufo/evidence/round-18/coldread/ledger.json` and `SHONEN.md:10` carries
  that exact link with all four boxes `~` — restraint 8 requires only the
  committed ledger plus full-page credit, i.e. the wave-2 reports themselves.
- Residual risks (seat-level, not landing defects): a fresh entry loses
  credit if a file it lists in `inputs` is appended by L1 before the
  scoring rev (mitigated — the w2 contract routes LOG.md/SCORECARD/
  lessons/.ufo reads to `external_inputs`); any later SKILL.md edit
  post-report invalidates that section's read. These are design properties
  of input-keyed credit, unchanged from round 17.
- Latent inconsistency (minor, not claimed-scope): `assemble.py`'s
  carry-coverage summary already reports 52/60 *coverage*, but only 10
  sections *credit* under measure — the assembler prints the disclaimer
  "measure.py is credit authority", so the two numbers are reconciled, but a
  reader could misread carry coverage as restored credit. Documentation
  smell, not harm.

## Attack 3 — depth guardrail 8/8/8

`grep -cE '^#   (js|bash)-' tools/mutate-and-run.sh` = 8 header legs;
`grep -cE '^  regression_case_git (js|bash)-'` = 8 regression calls;
`grep -cE "^    '(js|bash)-[^:]+:[^:]+\.spec:TABLE_"` = 8 selftest tuples.
Receipt `leg8-L1-check.txt` ends `REGRESSION: PASS (cases=8 passed=8;
ledger legs exact)`, `regression exit=0`, and the js-sources-check pin line
records rev `0acb7752…` sha `6a293a72…` — verified against the sibling:
`git -C kumitate-shokunin cat-file blob
0acb7752…:scripts/sources-check.mjs | sha256sum` = `6a293a72…258f` (exact).
Command D counts 8 at read rev.

## Attack 4 — adjacency

- `git diff --name-only 183f87b 01d586d` restricted to non-(`.ufo/round-18`,
  corpus, tools, top-level docs) paths: **empty**. No fleet-level, sibling,
  MANIFEST.json or .ufo/state touches inside the lane diff. Live kumitate
  worktree: `git status --porcelain` = 0 lines (leg-8 probe left it clean).
- Executable citations of moved tameshi tools in siblings: only
  `mado-shokunin/tools/mado-verify.sh:2245` (live-path harness under
  `--regression`, SHA printed as "provenance, not gated" — survives the
  runner's 132-diff-line wave-2 edit because the CLI flag set
  `--target/--defects/--suite/--workdir/--label/--selftest/--regression` is
  byte-identical old vs new) and `mado-shokunin/.ufo/waves/round-20/
  harm-watch.sh:203-240`, which pins by `HARNESS_SHA_RECORDED` and replays a
  matching historical blob from tameshi's object store — explicitly immune
  to the moved worktree. `tsukuroi-census.sh` cites tameshi in comments
  only. Grep for `trace-inputs|registry-check.py|evidence-disposition.py|
  repeat-control.py|pin-disposition.py|witness-metadata.py|bash-witness-study`
  outside tameshi hits only sibling *survey/report* docs, no executable.
- Promoted `tools/trace-inputs.py` vs `.ufo/evidence/round-17/coldread/
  trace-inputs.py`: 35 diff lines = docstring path + new selftest arms only;
  receipt schema `tameshi-trace-inputs-v1` and CLI unchanged; the round-17
  copy stays byte-identical as evidence. w2 seat contracts citing
  `tools/trace-inputs.py` get the same receipt contract.
- Staged duplicates audit: all 13 `.ufo/waves/round-18/staged/` copies that
  have landed counterparts are byte-identical (sha256 match); 3 staged-only
  docs (LEG8-INTEGRATION, two lesson drafts). No stale-copy provenance trap.

## Findings

- F1 (harm candidate — rejected): superseded round-17 rows fail got=2 at tip.
  Expected v2 input-drift semantics, replacement rows pass, capability
  preserved. Not harm.
- F2 (minor doc smell): carry-coverage 52/60 vs measure credit 10/60 could be
  misread; assembler already disclaims credit authority.
- F3 (accepted residual): fresh-read credit depends on seats recording only
  REV-stable inputs; contract's external_inputs routing mitigates the mutable
  files L1 appends. Not a landing defect.
- No false provenance, no duplicate authority, no identity change, no
  sibling breakage, no guardrail skew found.

Tool installs: none (pacman paused; no tool needed).

## Verdict

holds — wave-2 no-harm stands: supersession is capability-preserving, the
carry+fresh-read design restores calibration credit (10/60 carry-only today,
60/60 reachable), the 8/8/8 guardrail agrees, and nothing outside the lane
moved or broke.
