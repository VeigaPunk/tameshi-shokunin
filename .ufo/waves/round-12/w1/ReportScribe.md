# ReportScribe — round 12 w1 report checklist (DRAFT, advisory, lane-internal)

Status: DRAFT. Not a completed round report. No gate in this section was executed by this seat. Every "PENDING" row is owned by L1 or a sibling seat and is listed so L1 can fill it, not so it reads as done. Nothing here is independent non-author promotion, admission, or verification.

Seat: ReportScribe (scribe, leaf, no delegation). Wave: tameshi-r12-w1. Repo: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

## 1. Behavior

- Scope read: `.ufo/waves/round-12/spec.json` (wave context, ReportScribe item), `PROVINCE.md`, `corpus/QUALITY.md`, `/home/vgpnk/.omp/agent/RULES.md`, `LOG.md` tail, `SCORECARD.md` (sections at lines 7, 26, 58, 86, 154, 236, 246, 257, 274).
- Action: read-only probes only; captured in `.ufo/evidence/round-12/ReportScribe/probe-capture.txt`.
- No suite, build, lint, format, or mutation run was made. No file outside the two owned paths (section 5) was written. No commit was made.
- Expected report order (this checklist's own order; the sections below are the ordered required set):
  1. Behavior  2. Gates  3. Claim C1  4. Claim C2  5. Touched surfaces  6. Commits  7. Trend caveats  8. Stale lanes  9. Installs  10. Out of scope  11. Findings and risks  12. Artifact paths

## 2. Gates

| Gate | Command / source | Status for this report |
|---|---|---|
| repeat-control selftest | `python3 tools/repeat-control.py --selftest` | PENDING — `tools/repeat-control.py` is **absent** at HEAD (probe: `test -e` → absent). Owner: ControlGate. |
| repeat-control controls_match / controls_mismatch | `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...` | PENDING — not run by this seat. |
| repeat-control snapshot | `python3 tools/repeat-control.py --snapshot DIR` (tamper → exit 2 `snapshot_tampered`) | PENDING — no snapshot exists from this seat. Owner: SnapshotReview / L1. |
| bash-surface-census declared-witness split | BashWitness experiment, `tools/bash-witness-study.py` (not yet present) | PENDING — owner: BashWitness. |
| existing mutation runner `--selftest` / `--regression` | `bash tools/mutate-and-run.sh --selftest`, `--regression` | NOT RUN by ReportScribe. Last recorded in-repo: `.ufo/evidence/kaika-round-1/capability-demo/` (fleet round 1), not round 12. Must not be cited as round-12 verification. |

Exit map to record verbatim when filled (from wave contract): controls_match exit 0 clean; controls_mismatch exit 1 failed; baseline_nonzero and command_unavailable exit 2 could-not-evaluate; invalid usage exit 64 could-not-evaluate; snapshot tamper exit 2 `snapshot_tampered`.

Count rule to state explicitly: the existing 6 recorded gate legs are unchanged; reanalysis of the bash census is **not** a seventh independent gate.

## 3. Claim C1 — calibration capability: repeated pristine-control gate

- Claim text (from wave context): N ≥ 3 runs; identical exit, stdout, stderr required; nonzero baseline = could-not-evaluate; output or exit disagreement = failed; no flakiness cured and no determinism proven.
- Falsification to print in report: any run pair differing in exit/stdout/stderr → `controls_mismatch` (exit 1); any nonzero baseline reported as clean; any claim of determinism beyond the N runs observed.
- Evidence state: PENDING. Expected artifacts: the tool (ControlGate), the knowledge note `corpus/knowledge/repeated-control-precondition.md` (ControlKnowledge), the control-threat review (ControlThreats), the security review (GateSecurity).
- Axis filed under: calibration (per wave context). **Caveat:** `SCORECARD.md:246-255` / `:257-272` files the same work as "capability (frontier F3)" in the round-2 plan. L1 must pick one filing; this seat does not decide.

## 4. Claim C2 — depth: declared-witness split on pinned bash-surface-census

- Claim text: declared-witness split for the pinned bash-surface-census with 10 defects; existing 6 recorded gate legs unchanged.
- Pin named in sibling prompts: kagi `corpus/surface-census.sh` @ `fecee8743e52eb8fb5fbb40782934cb619a1a96e` (from BashDenominator item). The spec itself names the pin only as "pinned bash-surface-census"; L1 must confirm the pin against BashWitness output.
- Falsification to print: the split changes any of the six recorded legs (`tools/mutate-and-run.sh` cases), or the same reanalysis is counted as a seventh gate.
- Depth arithmetic to state, not assume: `SCORECARD.md:72-73` command D counts recorded cases in the runner's replay ledger. A new witness-split case counts only if it is recorded as a ledger case; otherwise depth is unchanged at the baseline count. Current recorded count was not re-measured by this seat.
- Evidence state: PENDING (BashWitness).

## 5. Touched surfaces

Owned by ReportScribe (this seat):
- `.ufo/waves/round-12/w1/ReportScribe.md` (this file)
- `.ufo/evidence/round-12/ReportScribe/probe-capture.txt`

Not touched (verified by probe: `git status --short` shows only the two untracked round-12 directories, both pre-existing from the dispatcher):
- `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `.ufo/waves/round-12/w1/swarm-registry.json` (not read; mode 600; registry, not evidence).

## 6. Commits

- HEAD at probe: `18ad5d050ef4bcd830fe513825baed878f025024` (`18ad5d0`, branch `master`). Probe timestamp in capture file: 2026-10-20T02:14:10Z (UTC; the date header in the session says 2026-10-19 — the discrepancy is recorded, not resolved).
- Recent history: `18ad5d0` ← `a21e910` (round-1 spot-check) ← `01b358c` (round-1 post-review) ← `121696b` ← `c7986cd` (round-1 close).
- Round-12 commits: **none** at probe time. No commit is authorized to this seat. L1 owns any commit.
- The round-12 working tree is uncommitted (`?? .ufo/waves/round-12/`, `?? .ufo/evidence/round-12/`). A commit citing round-12 evidence must follow the QUALITY criterion 9 (evidence copied into repo before the commit that cites it) — satisfied by the paths above once L1 commits.
- Every change in round 12 needs a `LOG.md` round entry from L1 (wave contract). **PENDING — L1.** ReportScribe does not write `LOG.md`.

## 7. Trend caveats

Stated as recorded, not re-adjudicated:
- Round-1 axes (`SCORECARD.md:58-68`): depth 6 (command D), calibration 0 (command C upper bound 0, pinned at 6 in a later adjudication per LOG `post-review fixes`). The two numbers disagree across sections; the LOG adjudication is the later record. L1 must cite which one it uses.
- Round-1 candidate verdicts were self-verdicts pending non-author verification (LOG round-1 close). The non-author spot-check commit `a21e910` exists; it is not re-read here.
- Discernment: recorded `unprovable-but-better` (`SCORECARD.md:118`). Round 12 does not change this unless an independent admit/reject review exists — none is claimed here.
- Saturation: line 8/10 and stagnation window N = 2 declared in round 1 (`SCORECARD.md:246-255`). A round that lands a capability would reset the window per the stated policy; this seat does not evaluate whether C1 counts as "a capability entering the table", since that requires the table row to be earned.
- Round-2 plan item 1 (freshness re-sweep of stale legs) is **not** in the round-12 wave scope. State it as out of wave scope, not as done or dropped.
- Two claims ≠ two axes: C1 (calibration) and C2 (depth) are the wave's named axes; no third axis is claimed.

## 8. Stale lanes

From `corpus/knowledge/fleet-kill-rate-ledger.md` (probe capture, lines 301-302, 328-329, 358-359):
- tsukuroi-census `tools/tsukuroi-census.sh`: pinned `084951be…`, live `bba6cdf6…`; reading recorded as **stale** (ER-4 @ 2026-10-14) and, in the worktree, **stale + drift** (+63/−0 uncommitted).
- mado-verify `tools/mado-verify.sh`: pinned `d7edaab4…`, live `7da4ec50…`; reading **stale + drift** (+196/−7 uncommitted).
- These readings are from 2026-10-14 (ER-4). Not re-read in round 12. Their current state is **unknown to this report**; the probe does not re-measure them.
- Effect on round 12: none of the two claims touches tsukuroi or mado. Stated so L1 does not cite them as current.

## 9. Installs

- ReportScribe installs in this seat: **none**.
- Environment observed (not installed here): Python 3.14.7 (`python3 --version`). Used only for the read-only probe; no `uv tool install` or `pacman` call was made.
- Tooling rule read: `/home/vgpnk/.omp/agent/RULES.md` (channel order: `sudo pacman -S --needed --noconfirm` → `uv tool install` → official binary → `cargo`/`npm -g`; no partial upgrades; record each install).
- Any install by a sibling (e.g., ControlGate or BashWitness) must be recorded by L1 in the round report; ReportScribe has no visibility into those and records none.

## 10. Out of scope

- Editing any sibling gate code (`kagi`, `kumitate`, `tsukuroi`, `mado`) — PROVINCE `Refuses` / `Adjacent`.
- Mutation runner edits — wave contract forbids them (`tools/mutate-and-run.sh` unchanged in this seat).
- Engine-specific nondeterminism (game lanes) — PROVINCE `Adjacent`.
- Credential material (kagi) — PROVINCE `Refuses`; no secret reads by this seat.
- Freshness re-sweep of stale legs — not in round-12 wave scope (see section 7).

## 11. Findings and risks

1. **Gate absent.** `tools/repeat-control.py` does not exist at HEAD; C1 has no executed evidence. Any report line stating C1 "passes" is a fabrication unless ControlGate's selftest and snapshot runs are attached. Severity: blocking for C1.
2. **Filing ambiguity.** C1 is calibration (wave context) vs capability F3 (SCORECARD round-2 plan). L1 must choose. Severity: report-accuracy.
3. **Two numbers for round-1 calibration** (0 in the baseline table, 6 after post-review adjudication). Report must name which is cited. Severity: trend-accuracy.
4. **Stale legs** (tsukuroi, mado) read from 2026-10-14. Any "current pin" claim in round 12 needs a fresh read. Severity: low for these two claims, high if cited as current.
5. **Date skew.** Probe capture UTC 2026-10-20T02:14Z vs session date 2026-10-19. Report must cite a single clock source. Severity: low.
6. **Working tree uncommitted.** Round-12 evidence is untracked; the commit that cites it must include it (QUALITY 9). Severity: process.
7. **Drafted-not-done risk.** This checklist is a draft; every PENDING row must be replaced by a command + exit + finding ID, or stated as not executed. Severity: contract (no placeholder may read as completed).

Counterexample commands for L1 (run by L1, not by this seat):
- `test -e tools/repeat-control.py || echo ABSENT` → expected `ABSENT` at this HEAD.
- `git status --short` → expected two untracked round-12 directories until L1 commits.

## 12. Artifact paths

- `.ufo/waves/round-12/w1/ReportScribe.md` — this report (draft).
- `.ufo/evidence/round-12/ReportScribe/probe-capture.txt` — probe output (read-only, timestamped).
- Inputs read (not written): `.ufo/waves/round-12/spec.json` (sha256 `e13d92af…cc2`), `.ufo/waves/round-12/dispatch.json` (sha256 `18d3626d…b7e2`), `PROVINCE.md`, `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md`, `corpus/knowledge/fleet-kill-rate-ledger.md`.
- Not yet present, owned by siblings: `tools/repeat-control.py`, `tools/bash-witness-study.py`, `corpus/knowledge/repeated-control-precondition.md`, `.ufo/evidence/round-12/{ControlGate,BashWitness,ControlKnowledge,…}/`.

Stop: report complete as a draft. Nothing in this file is a pass, an admission, or independent authority.
