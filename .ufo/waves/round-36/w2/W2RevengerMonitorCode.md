# W2RevengerMonitorCode — monitor backdoor audit (round 36, C1 calibration surface)

Seat: revenger, leaf (no subagents). Attacked the two monitor scripts behind the C1
cold-read claim for round-36-specific special-casing that could inflate the
restored credit (6 -> 8):

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py`
  (1659 lines, the frozen credit algorithm; sha256 of worktree and HEAD blob both
  `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37`)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py`
  (113 lines, the selector actually cited by the C1 command; sha256 worktree == HEAD
  `657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb`)

## What was checked (evidence chain)

1. **Full-body read of both files** (no elided ranges left): constants, parsers,
   sectionizer, census, input gate (`input_failures`), trace gate
   (`trace_reason`, `live_read_bound`), verdict/class/commands gates
   (`entry_failure`, `entry_credit_reason`, `entry_reason`), aggregation
   (`coldread`), score assembly (`measure`), `main`, both selftests.
2. **Round-36 special-casing grep**: pattern `round[-_]?3[456]|r3[456]` over both
   files — zero matches. Pattern `[0-9a-f]{40}|2026-|sha256=|rev ==|== rev` — only
   selftest fixture rows (S001/S002 dated 2026-10-20); no 40-hex literals, no
   revision comparisons, no date gates anywhere in gate logic. The only hardcoded
   absolute path is `LIVE_LANE_ROOT=/home/vgpnk/Projects/shokunin/tameshi-shokunin`
   (live-lane trace binding, documented round-17 refinement, not round-specific).
3. **Exemption surfaces**: `IGNORED_INPUTS = {SKILL.md, round-17 ledger, round-18
   ledger}` is the only input exemption; documented rationale (page keyed by
   section sha, ledger is its own output); it only removes those keys from the
   required-inputs check, never weakens verdict/class/commands/trace gates.
   Verdict sets are strict; unknown verdicts fail (`verdict:probably-fine`
   selftest); class cross-crediting is rejected both ways; zero-command entries
   are `commands-unrecorded`; aggregation is fail-closed (clean entry cannot
   launder a failing twin; only a *drifted* failing entry loses veto power).
   Recorded `read_rev` is never consulted during gating — every input digest is
   re-verified at the measured REV (`input_failures(repo, rev, …)`), so stale
   entries at old read_revs cannot credit through their historical rev.
4. **Selector monkey-patch scope**: the round-21 selector overrides exactly
   `DEFAULT_LEDGER_PATH`, `LEDGER_PATH`, `BOX3_LINK`, and adds the round-21
   ledger to `IGNORED_INPUTS`, then calls `module.main()`. All four globals are
   read at call time inside the implementation (no default-argument capture of
   any patched name anywhere in the 1659 lines). Net effect: box-3 of SHONEN.md
   must link the round-21 ledger, the ledger is read from
   `REV:.ufo/evidence/round-21/coldread/ledger.json`, and that ledger may omit
   itself as a verified input — the same self-referential exemption the round-18
   ledger already had. No historical fallback: the packaged selftest
   (`no-historical-ledger-fallback`) proves a missing round-21 ledger yields 0
   covered and score 6; `carried_from`/`round21_provenance` keys in the ledger
   are inert metadata the monitor never reads.
5. **Override locks**: the selector rejects `--ledger-file`, `--ledger-rev`,
   `--inputs-overlay` in separate-arg, `=`, and argparse-abbreviation forms
   (selftest covers `--i=`, `--ledger-f=`, `--inputs-o=`), so every run through
   this entry point is strict (`trace_gate: "strict"`); the legacy absent-trace
   skip is unreachable here. Remaining accepted flags (`--rev`, `--repo`,
   `--explain`, `--selftest`) cannot relax any gate.
6. **Supply-chain surface** (the only live-filesystem reads the cited command
   makes): (a) the selector loads the round-18 implementation from the worktree
   via `parents[4]`, not from REV — verified worktree bytes == `git show HEAD:`
   bytes for both monitors and the ledger, and `git status --porcelain` clean on
   all four audited paths, so the executed algorithm is the committed one;
   (b) stdlib-shadow modules: `round-21/coldread/` contains only
   `measure.py`, receipts (.json/.stdout/.stderr) and `traces/` — no
   `json.py`/`hashlib.py`/`re.py` etc.; `round-18/` extras (`defect-probes.py`,
   `git-env-canary.py`) shadow nothing; (c) `__pycache__/measure.cpython-314.pyc`
   (untracked): header (mtime 1792528890, size 76144) matches the source, so
   importlib would load this bytecode instead of the audited source — tested by
   recompiling the source under the same interpreter (python 3.14.8, magic
   `2b0e0d0a`) and comparing marshal payloads: **byte-identical (97330 ==
   97330)**. The loaded bytecode is exactly the audited code.
7. **Live reproduction of the cited command** (rev `HEAD` =
   `fbb01cf46f8437fd1264c1a3acc053c882fa2164`):
   `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev HEAD`
   -> `calibration_restraint_score: 8`, `sections_covered: 64/64`, `missing: []`,
   `trace_gate: strict`, `overrides_used: false`, `ledger_committed: true`,
   `ledger_source: rev`, SHONEN marks `['~','~','~','~']` with
   `box3_points: true`. The 8 is produced strictly from committed blobs.
8. **Selector selftest**:
   `python3 …/round-21/coldread/measure.py --selftest` -> `12/12 pass`
   (configured-default-ledger, relocated-package-default-repo,
   no-historical-ledger-fallback, 9 override-refusal cases).
9. **Frozen pin re-check**: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/c1/c1-measure-v2.py`
   sha256 `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` ==
   the pinned value. The four entries appended to the round-21 ledger by the
   refresh (traces `.ufo/evidence/round-36/coldread/traces/L1/source-1..4.json`)
   are structurally ordinary: class `record`, verdict `gap-minor`,
   `commands_executed_count: 1`, zero blocking/wrong, digest-pinned inputs
   (including `tools/mutate-and-run.sh` at the frozen `a7d3f2dd…`), committed
   trace receipts; extra keys (`seats`, `reports`, `minor_gaps`) are never read
   by the monitor and cannot gate or ungate anything.

## Commands run (all read-only; no lane mutation, no pacman, no tool installs)

- `read` (full paging) of both monitor files; `grep` scans listed above.
- `sha256sum` of the 4 audited files; `git show HEAD:<path> | sha256sum` for the
  two monitors + ledger; `git status --porcelain=v1` on the four paths.
- `git ls-files` on `round-18/__pycache__` and `round-21/coldread/` (pyc untracked).
- pyc-header inspection + marshal compare against a fresh `compile()` of the source.
- Cited monitor command at `--rev HEAD` (rev `fbb01cf4…`), summarized.
- Selector `--selftest`.

## Findings

- **No round-36-specific special-casing, hardcoded revision, exemption, or
  relaxed gate exists in either monitor.** Nothing in the code path knows round
  36 exists.
- Observation 1 (pre-existing, not round-36-specific, current state verified
  clean): the selector executes the round-18 implementation from the live
  worktree rather than from REV; worktree == HEAD byte-verified today, but the
  guarantee is procedural, not structural.
- Observation 2 (same class): `round-18/__pycache__/measure.cpython-314.pyc` is
  untracked yet header-valid, so importlib prefers it over the source;
  `sys.dont_write_bytecode` in the selector prevents writes, not reads. Verified
  byte-identical to an honest compile of the audited source today. A future
  writer could in principle plant a header-valid pyc with different bytecode;
  pinning/deleting `__pycache__` or loading the implementation from the REV blob
  would close this structurally. Recorded as hardening note, not a backdoor.

## Verdict

**CLEAN — no backdoor found: the round-18 algorithm and the round-21 selector
contain no round-36-specific special-casing or relaxed gate; the cited command
reproduces calibration credit 8 strictly (trace_gate strict, overrides_used
false, ledger committed at REV `fbb01cf46f8437fd1264c1a3acc053c882fa2164`,
64/64 sections credited, selector selftest 12/12, audited sources byte-equal to
HEAD, and the only importable bytecode cache is byte-identical to the audited
source).** Confidence: high (full static read + live strict reproduction +
bytecode-level check).
