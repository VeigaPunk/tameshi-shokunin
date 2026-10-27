# T51CritC3Counter — attack on the frozen C3 counter (operability)

Seat T51CritC3Counter, wave 1, round 51. Read-only on the lane; all experiments ran
against scratch clones of the lane (one live clone at a time) with the frozen counter bytes
(`.ufo/evidence/round-51/c3/measure.py`, the same path the committed controls harness runs).
Counter selftest passes: `TMPDIR=$S/st python3 .ufo/evidence/round-51/c3/measure.py --selftest`
→ `C3_R51_SELFTEST: cases=10 failed=0`.

## Result: the counter is passable by a pure SKILL.md edit that does none of the claimed true-row work

Fixture **A** (scratch lane, checkout at freeze `84aa673a`, then one commit that appends 30
registry rows after SKILL.md:1504) — `python3 .ufo/evidence/round-51/c3/measure.py --lane LANE --rev ab3e08c --work wc3-A --explain`
→ `C3_R51: tools=30 rows=32 covered=30 missing=0 deleted=0 total=0 C3_R51_PASS=true` (RC 0).
The rows are: 29 run the tool's real `--selftest`; two do not run a self-test at all
(`tools/round21-measure.py --help --selftest` and `tools/bash-witness-study.py selftest` —
the latter *is* its selftest subcommand, the former is argparse help output); every row stamps
kind `gate`, pinned `none`, write scope `none`, owner `tameshi`, and declares verdict map
`0 clean; 1 failed; <observed-usage-code> usage`. Receipt text in
`T51CritC3Counter-forge.out` (fixture A block).

## What the counter verifies, and what it does not

The frozen predicate (measure.py:4-27) and checks:
- `row_reason` (measure.py:117-157): kind ∈ {gate,probe} (string enum only); entry cell merely
  contains the substring `tools/T` (line 121-122); verdict map must contain standalone tokens 0
  and 1 (line 123); self-test cell must hold exactly one backticked command, no shell
  metacharacters (lines 125-130), whose shlex argv is `python3 [-I] tools/T ARGS...` or
  `bash tools/T ARGS...` with **some ARG containing the substring `selftest`** (lines 136-143);
  pinned cell non-empty and either starts with `none` (short-circuits all existence checks,
  lines 144-151) or every backticked token that looks like a repo path exists at REV; write
  scope merely non-empty (line 152-153); owner string `tameshi`.
- `run_row` (measure.py:173-184): self-test must exit 0 from a `--shared` clone at REV, and the
  **first token of the last non-empty stdout line** must appear literally in the self-test cell;
  then the usage probe (interpreter+tool+`--r51-no-such-flag`) must exit with a code present as
  a token in the verdict map.

Measured blind spots (each exploited by fixture A):

1. **Self-test command that is not a self-test.** The only enforced link between the row and the
   tool's real selftest is the substring `selftest` in some ARG (measure.py:142-143). `python3
   tools/round21-measure.py --help --selftest` passes: argparse processes `--help` and exits 0
   without running anything; the recorded "finding id" is `--selftest`, the option name from the
   help listing (fixture A, line 1520 covered, `last=--selftest`). This tool's genuine selftest
   fails (`--selftest` → rc 1, no stdout), so this is the only way to cover it without fixing the
   tool (which the no-harm tools-scope forbids).
2. **Finding id is author-controlled.** The marker is whatever text the row includes; nothing ties
   it to a real diagnostic. In fixture A the help-mode marker is an argparse option name; the
   pre-existing round-12 row for the same tool fails exactly here (`finding-id-not-in-row
   (VERDICT:)`, line 1504) because its cell does not include that token.
3. **Verdict map unknown only for 0, 1 and today's usage-code.** Any other exit code (timeout
   124, git 128, or the tool's other documented codes) stays undeclared — and the label
   "N usage" is not validated against the tool's semantics (e.g. `golden-verdict.py` exits 2
   for could-not-evaluate, not usage). The contract's own `cannot_see` (contract.json:57) names
   exactly this residual.
4. **Kind is unchecked semantically.** All 30 rows in fixture A stamp `gate`, including tools the
   lane itself registers as probes or plain utilities (e.g. bash-witness-study is `probe` at
   SKILL.md:1504; write-path-census-* are audit utilities). The counter only tests the literal
   `gate`/`probe` string.
5. **Pinned values bypass via `none`.** `none` skips existence checks (measure.py:146). Real
   instruments pin files (repeat-control pins `.ufo/evidence/round-12/ControlGate/expected.json`
   and `mismatch/expected.json`; pin-disposition pins the round-13 manifest; witness-metadata
   pins digests; bash-witness-study pins its declaration.json) — the forged rows all say `none`
   and pass.
6. **Write scope unchecked beyond non-empty.** `none` is accepted for tools that write: trace-
   inputs.py writes trace receipts (round-49 refresh uses it to record reads), receipt-measure.py
   writes destinations, witness-metadata.py writes bytes, write-path-census-v4.py writes golden
   files during selftest, mutate-and-run.sh writes sweep receipts/scratch.
7. **Usage probe runs the tool in the same clone, unisolated.** The probe argv shares the clone
   worktree with every other row's selftest (6 worker threads over one clone, measure.py:212-215)
   and gets only a per-command TMPDIR. Empirically, probing all 30 tools at base left the clone
   `git status`-clean (no untracked writes), so no side effect materialized in this run — but the
   counter provides no guarantee; a tool whose main mode writes relative to cwd could mutate the
   verification environment mid-run.

## Contrast: committed controls and honest generator

- **CTL_TEMPLATE (controls.py:119-133, run as fixture B)**: fails with `covered=0 missing=30`.
  Reasons: every row `finding-id-not-in-row` (the template cell holds only the command text, never
  the marker), `repeat-control.py` additionally `pinned-path-missing:mismatch/expected.json`
  (its real pin does not exist at REV), and `round21-measure.py` `selftest-exit=1`. So the
  uniform template fails for two independent reasons, exactly as the committed control reports
  (control plan, controls.py:15-16).
- **CTL_HELP (template with `--help`)**: fails statically at `selftest-arg-missing`
  (measure.py:142-143) because no ARG contains `selftest`.
- **Pure observed-code generator (fixture C: same rows but honest commands for all 30, observed
  exit codes declared)**: fails `covered=28 missing=2` — `round21-measure.py` (real selftest
  rc 1) and `bash-witness-study.py` (`--selftest` is not its flag; rc 64). So a generator that
  only records observations cannot emit passing rows for the two red tools; the passing fixture A
  therefore *must* include at least one non-self-test command (the `--help --selftest` alias).

## Pre-existing non-conformance (bonus finding)

At freeze, the registry's own two rows (SKILL.md:1503-1504) already fail the frozen counter:
`repeat-control.py` row pins `mismatch/expected.json` which does not exist at REV
(`pinned-path-missing`), and the `bash-witness-study.py` row's selftest prints `VERDICT:`
which its cell does not contain (`finding-id-not-in-row`). So "2 of 30 covered" (contract
before-state) is optimistic: neither existing row currently covers its tool.

## Cold-read interplay

Any registry-section byte change (all fixtures) changes the section's sha, so the round-21
cold-read monitor drops that section (score 8→6) unless the round-49-style re-key
(`.ufo/evidence/round-49/c1/refresh.py`) is run by reading seats before the deciding run — that
cost is borne by the claim, not by the counter, and does not affect the counter result.

## Commands that show the evidence

- counter selftest: `python3 .ufo/evidence/round-51/c3/measure.py --selftest`
- fixture A: `python3 .ufo/evidence/round-51/c3/measure.py --lane LANE --rev ab3e08c1283a78e70bb9a786637ed8960ad426f0 --work wc3-A --explain`
- fixture C: same with `--rev f6d3414d4ea792ec71cadeddaf61c1c5632e7eff --work wc3-C`
- fixture B (CTL_TEMPLATE): same with `--rev 9ed578e25c71fdf2605d50a2f747ea2f3400a3c2 --work wc3-B`
- tool ground truth: `python3 tools/T --selftest` and `python3 tools/T --r51-no-such-flag`
  at base in a `--shared` clone (full 30-tool table in `T51CritC3Counter-probe.out`)

## Summary

- Frozen C3 counter passes on a pure SKILL.md registry edit adding 30 forged rows
  (C3_R51_PASS=true, rev ab3e08c, fixture A); no tool touched, no real "true row" work done.
- 29/30 tools' real selftests are green; `round21-measure.py`'s is red (rc 1), and
  `bash-witness-study.py` takes a `selftest` subcommand, not `--selftest`.
- The counter checks argv shape only: `--help --selftest` (argparse help, exit 0) passes as a
  "self-test"; the recorded finding id is author-chosen; verdict maps, kind, pins and write scope
  are checked shallowly (0/1/usage code, enum string, `none` bypass, non-empty).
- CTL_TEMPLATE and CTL_HELP fail as committed; a pure observed-code generator fails on the two
  red tools — a passing forgery must alias at least one tool's selftest.
- Pre-existing rows SKILL.md:1503-1504 already fail the frozen counter at freeze (pinned-path-
  missing; finding-id-not-in-row), so base "covered 2" is overstated.
- Usage probes ran in the shared clone with no observed side effects (git status clean), but the
  counter gives no isolation guarantee between rows.
- Recommendation for a stricter counter: require the self-test ARG to be exactly `--selftest`
  (or the tool's documented mode) and bind the marker to a real finding-id token; require pinned
  cells to enumerate real inputs (no `none` for instruments that pin); validate kind and write
  scope against the tool; and declare all possible exit codes.
