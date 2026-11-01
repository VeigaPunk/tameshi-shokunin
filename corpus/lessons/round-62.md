# tameshi round 62 — lesson (hyaku run 14, 2026-11-01)

L1 `TameshiR62` (round 62). Base `ed3a66c2c5458fc6e4ecbc41cbaf93ed05f6db98`
(= origin/master; the r61 admitted spot-check landing). Dispatch host:
win32 (python 3.13.15, git 2.55.0.windows.3, `core.symlinks=false`).
Receipts: `.ufo/evidence/round-62/win-host/` — they land in the commit
following the work commit (receipt-after-subject ordering, the r61
precedent).

Fresh-start duty: the last three rejected closures (r58, r59, r60 —
`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md` re-read) and the
r61 spot-check (`round-61-verifier-spotcheck.md`, in full) were read before
anything was declared. r61 was ADMITTED, so the fresh-start premise is
stale, but the duty was performed. Ruled out, with reasons: (a) the r61
fresh-start rulings stand — the frozen spawning precheck as-is
(host-infeasible, ~112 min/rev, five failed runs), no-harm claims from
r60's lane-authored substitute (cross-revision attribution unmeasured),
counter-family extension (admission is an operator ruling), Linux counting
commands (host-scoped, criterion 118); (b) a new SOURCES row or any
registry edit — a byte change to `corpus/SOURCES.md` re-stales the 18
batch-2 rekey pins and owes an 18-section re-read rekey (the r61 carry
note), and no correction this round requires a registry write; (c) a
QUALITY.md criterion append for the mined mistake class — same
monitored-record pricing; recorded as a proposal in `## Mistakes` below;
(d) chasing capability admission (the r59 row) — an operator ruling, not
lane work.

## Claims

- **C1 (calibration; routed defect RD1; sourced S289).** The shipped
  precheck bytes are made to match the documented probe contract, and the
  probe is proven able to fail. Before (base `ed3a66c2`): the r61 report
  C1 bullet and `corpus/lessons/round-61.md` (lines 32, 123–124) claim the
  spawn-equivalence probe "fails the run on any mismatch OR an empty
  sample" / "exit 2 … requires sampled ≥ 1 and mismatches = 0", but the
  bytes gate only on `mismatches`
  (`git show ed3a66c2:tools/coldread-precheck-portable.py | grep -c
  "probe_failed\|sampled.*< 1"` → 0): an empty candidate set returns
  `{'sampled': 0, 'mismatches': 0}` and the run proceeds — the r61
  `probe-cannot-fail-empty` defect class, spot-check RD1. After: a
  `probe_failed` gate (sampled ≥ 1 AND mismatches = 0) guards both measure
  modes (same grep at the work commit → 4); ARM-VACUOUS drives `main()`
  with the exact dict the REAL probe returns for an empty candidate set
  (captured at runtime, not assumed) at floor == cand so the verdict arm
  is `ok` — base bytes exit 0 (VACUOUS-PASS: the red-before, committed),
  guarded bytes exit 2 (GUARD-FIRED); ARM-MISMATCH tampers one resume
  chunk AND its manifest sha256 and re-runs the CLI — exit 2 with
  `mismatches=1` on BOTH byte versions (the pre-existing mismatch gate,
  intact); ARM-CLEAN reads `floor_mismatches=0 cand_mismatches=0`; and the
  guard re-run on the real repo at the work commit reads `lost=0 ok` with
  sampled ≥ 1 both revs, mismatches = 0, exit 0 — the r61 verdict
  unchanged, no harm. Score: calibration 8 unchanged (at the lane-
  attainable cap); the move is the no-harm instrument's honesty — the same
  axis grounding as r61 C2 ("the move is the no-harm guard, the
  discernment surface"). Arm-liveness rule adopted from considerthese
  2026-10-28 proposal 2: every arm carries an input that moves the outcome
  it is named for.

## Gate

- Sourced row opened this round: **S289 re-accessed** (held row, mined;
  NOT re-written — why below). Git `git-cat-file` documentation,
  https://git-scm.com/docs/git-cat-file, re-fetched 2026-11-01 (HTTP Date:
  Sun, 01 Nov 2026 11:36:48 GMT; 79,360 B; sha256
  `624464ef7a3d64de06038200bff85ac09389a9d217d379dd660aa6b5165048d7` —
  byte-identical to the r61 extract
  `.ufo/evidence/round-61/win-host/sources/s293-cat-file-batch.html`; the
  r62 receipt records headers + size + digest and does not duplicate the
  extract). Located quote (§Output, `--batch` without a custom format,
  page lines 2676–2677; 8 tokens): "<oid> SP <type> SP <size> LF
  <contents> LF". Grounding: the probe re-derives its sample through the
  original per-input spawns and compares against what the batched reader
  (the `--batch` output framing) served — the guard requiring that
  comparison to exist and be clean rests on this framing.
- No registry write this round, and why: any byte change to
  `corpus/SOURCES.md` re-stales the 18 batch-2 rekey pins and owes an
  18-section re-read rekey (the r61 carry note — "that is the instrument
  working, not a defect"); no correction this round requires a registry
  write. RD4's wrong "12 words" label also sits in the registry note
  (line 539); it is corrected of record in the r61 lesson append and the
  SCORECARD erratum, not in place. Rule-2 fields (status/recheck/used-by)
  are unchanged; the S293 W04 census warning stands as the rejection
  marker.
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (153 rows; 17 W04 + 1 W01, all
  pre-existing) and exit 0 at round end (receipt in the round report).
- Rejected this round, with reason and flip: **dropping the batched
  prefetch for per-input spawns so the empty-sample scenario becomes
  CLI-reachable** — REJECTED: it re-creates the ~112 min/rev instrument
  the portable form exists to replace; flip: a repo whose ledger is
  untracked at the measured revision would make the candidate set empty
  through the CLI, and the guard would then be exercised end-to-end.

## Mistakes

1. **A fix described in prose can be absent from the shipped bytes
   (class: documented-contract-not-in-bytes; r61 routed defect RD1).**
   Evidence: the r61 report C1 bullet and `corpus/lessons/round-61.md`
   lines 32 and 123–124 describe an exit-2 gate requiring `sampled ≥ 1`;
   at base `ed3a66c2` `grep -c "probe_failed\|sampled.*< 1"` → 0 and
   `main()` gates only on `mismatches`. Captured-by: the r61 verifier
   spot-check (§5 RD1); no QUALITY.md criterion required a described fix
   to be grep-addressable in the shipped bytes. Fix: the guard lands this
   round with the red-before receipt (ARM-VACUOUS base exit 0) and the
   fail-closed arms; PROPOSAL (not appended — QUALITY.md is a monitored
   record, an append re-stales pinned sections and owes a rekey, the same
   pricing as ruled-out (b)): "a described fix is grep-addressable in the
   shipped bytes, with the counting command in the claim"; append it in a
   round already paying a rekey.
2. **Number/word-count drift recurred in r61 prose in the same round the
   number-drift class was mined (class: number-drift; r61 routed defects
   RD2–RD4).** Evidence: "21 files" (lesson lines 58, 134; fleet report)
   against 20 committed (`git ls-tree -r 19d7e996 | grep -c first-family/`
   → 20); "2,215-line" (fleet report) against 2,214
   (`git show ed3a66c2:SKILL.md | wc -l` → 2214); "12 words" (lesson line
   75; SOURCES note line 539) against 8 tokens. Captured-by: the r61
   spot-check (§5 RD2–RD4). Fix: errata pinned (SCORECARD erratum + r61
   lesson append); the drift happened in prose written without its count's
   command inline — every number in this lesson carries its command. Also
   recorded: the spot-check's own RD2 site list over-stated (LOG,
   SCORECARD and the `19d7e996` commit subject carry no count) — each
   erratum site list in this round was re-verified against bytes before
   being written.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this host;
  the r60 L0 question (`.ufo/l0-questions.md`, tameshi | round-60, option
  (b)) stands unanswered — again an L1-only round, disclosed here.
- The empty-sample arm is function-level (`main()` driven with the real
  probe's empty-candidate dict), disclosed in the claim, the harness
  docstring and here: through the CLI on a valid repo the candidate set is
  always non-empty (the ledger is always prefetched and tracked), which is
  exactly why the r61 vacuous pass was latent rather than observed.
- The probe-arms harness imports the committed r61 differential builder
  (`build_repo`) for its fixture; both tool byte versions are extracted
  from committed revisions (base `ed3a66c2`, the work commit) before the
  run, so the arms bind to committed bytes.

## Verdicts

- **C1, measured.** Receipts (in the commit following this lesson's work
  commit): `probe-arms.stdout` ending `PROBE_ARMS: PASS (vacuous/base=ok
  vacuous/new=ok mismatch/base=ok mismatch/new=ok clean/new=ok)` with the
  red-before line `ARM-VACUOUS tool=base exit=0 VACUOUS-PASS (empty sample
  did not fail the run)` and `ARM-VACUOUS tool=new exit=2 GUARD-FIRED
  (fail-closed)`; `guard-rerun.out`/`guard-rerun.json` —
  `COLDREAD_PRECHECK floor=8b0042bde0ca floor_credited=46 cand=<work>
  cand_credited=64 lost=0 ok` + `EQUIVALENCE floor_sampled=20
  floor_mismatches=0 cand_sampled=20 cand_mismatches=0`, exit 0.
  Counting commands: the greps in the claim (0 → 4), the `PROBE_ARMS:`
  line, the `COLDREAD_PRECHECK` line.

## Next-round carry

- The guarded tool digest is
  `892a045d8b508214804e2b26b78c15b83aae65bdae4bd5bf022b8cb735f3b33e`
  (the r61 bytes stay preserved as-run in the r61 evidence dir; the r61
  capability-row digest refers to those).
- Any round that edits SOURCES/PROVINCE/QUALITY/README/pinned tools still
  owes the rekey; the probe-arms harness is re-runnable and should be
  re-run after ANY future edit to the probe or its gate (arm-liveness).
- The QUALITY criterion proposal (mistake 1) awaits a round already paying
  a rekey.
