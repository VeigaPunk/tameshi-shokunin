# MinimalityReview probes (round 12, w1) — read-only; no suite executed

Scratch copy of pinned kagi blob: /tmp/mr-surface-census.sh (outside repo, per QUALITY.md criterion 9)

## P1 — repo surface present
- tools/ contains only mutate-and-run.sh (1642 lines). tools/repeat-control.py and tools/bash-witness-study.py: absent.
- .ufo/evidence/round-12/: absent before this seat wrote its own directory.
- .ufo/waves/round-12/ contains dispatch.json, spec.json, w1/swarm-registry.json.

## P2 — pinned kagi object
- kagi path that resolves on this host: kagi-shokunin/ (fleet root), NOT .tower/worktrees/kaika/kagi-shokunin (does not exist).
- `git -C kagi-shokunin cat-file -t fecee8743e52eb8fb5fbb40782934cb619a1a96e` → commit
- `git show fecee874:corpus/surface-census.sh` sha256 = 275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f (equals PIN_BASH, tools/mutate-and-run.sh:544)

## P3 — argparse exit code (Python 3.14.7)
- argparse parse_args(['--bogus']) → SystemExit code 2. The contract requires invalid usage → exit 64, so the default argparse error path collides with could-not-evaluate exit 2.

## P4 — runner structure (tools/mutate-and-run.sh)
- Top-level dispatch 1620-1642 (`while [[ $# -gt 0 ]]` … `case "$MODE"`), `set -u -o pipefail` at 155 → the file is not sourceable as a library (sourcing with no args reaches usage_exit 64 path).
- Control concept: run_sweep 465-474 (red control → die_setup exit 2).
- Verdict mapping: run_sweep 484-490 (0 SURVIVED, 124/126/127 INCONCLUSIVE, else KILLED).
- Regression re-classifies the same verdicts: regression_case 999-1047; helpers table_lookup/table_count/table_total 562-585.
- Materialization (git show + pin + mode mirror): regression_case 932-963; regression_case_git 1061-1072.
- Embedded bash-surface-census spec: heredoc 630-674 (10 defects B1-B10).
- Recorded per-defect verdict table for bash-surface-census: TABLE_BASH at runner:555 (verdicts not reproduced).

## P5 — kagi surface-census selftest output shapes (static read of pinned blob)
- probe_open prints `PROBE <name>`; probe_close prints `PROBE <name>: PASS|SKIP|FAIL  <detail>` (lines 455-464); 10 probe_close call sites.
- check() prints `  check <name> ok` or `  check <name> FAIL (want=… got=…)` (lines 447-453).
- selftest prints `ok-case %02d …` / `bad-case %02d %-34s exit=%s` (per run_case; run_case body not fully read).
- Failure grammar: `bad-case` is the only top-level failure grammar. WitnessThreats reports 0 pristine `--selftest` stdout lines starting with `PROBE`; PROBE lines appear only inside `    | ` bad-case dumps when a the-janitor handler resolves. [Peer measurement, not re-run here.]
- probe 'run-ref-signed-out' (line ~617) emits `exit $rc after ${wall}s` in its PASS/FAIL detail, but only under --deep; default path is SKIP "requires --deep" (line 605). Default-path byte determinism NOT verified (not run).

## P6 — stale evidence paths
- .ufo/evidence/kaika-round-1/witness/README.md and declared.tsv cite .tower/worktrees/kaika/… pins; that path does not resolve on this host.

## P7 — exposure record
- Read: TABLE_BASH per-defect recorded verdicts (runner:555, verdicts not reproduced); recorded kill-rate totals for bash-surface-census 8/10 (SKILL.md, fleet-kill-rate-ledger.md); js witness declared.tsv and README (kaika-round-1/witness).
- Did not read: bash-surface-census per-defect witness outcome files (none exist in repo).
