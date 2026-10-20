# ReportEvidence — round 12 w2 evidence pointer map (advisory, lane-internal, read-only)

Seat: ReportEvidence (scribe, leaf). Repo: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base HEAD `18ad5d050ef4bcd830fe513825baed878f025024` (`18ad5d0`). Pushed commit: not supplied; L1 owns it.

Scope: pointer map only. No build, lint, test, mutation, or gate was run by this seat. "Recorded" entries are quoted from existing receipts. Not a pass, admission, or independent authority. No installs, no commit, no edits outside this file.

## Required report sections → evidence pointers

Ordered set: `.ufo/waves/round-12/w1/ReportScribe.md:7-13`.

### 1. Behavior
- Claims: `corpus/lessons/round-12.md:3`. Gate contract: `.ufo/waves/round-12/spec.json` context.
- `tools/repeat-control.py`: usage `:1-95`; `EXIT_BY_ID` `:115-123`; `classify` `:191-205`; `run_mode` `:211`; `snapshot_mode` `:412`; `selftest` `:545`; `main` `:782`.
- `tools/bash-witness-study.py`: modes and classification rule `:1-47` (disclosure "declared-witness mapping, NOT a blind preregistration" `:47`); declared rows `:98-170`; `classify` `:411`; `run_sweep` `:522`; `cmd_count` `:880`; `cmd_selftest` `:962`.
- Review outcome: `corpus/lessons/round-12.md:20-24`.

### 2. Gates (status = what the receipt records; none re-run here)

| Gate | Receipt | Recorded result | Note |
|---|---|---|---|
| Mutation runner `--selftest` | `.ufo/evidence/round-12/runner-selftest.txt`; `LOG.md:660` | `MUTATE_SELFTEST: 80/80 pass`, exit 0 | Recorded only. |
| Mutation runner `--regression` | `.ufo/evidence/round-12/runner-regression.txt`; `LOG.md:660` | six legs PASS, exit 0 | Recorded only. |
| Repeat-control stable control | `.ufo/evidence/round-12/ControlGate/run-{1,2,3}.*` (exit `0`,`0`,`0`) | 3 identical observations | No gate verdict file for this dir located; L1 confirms producing command. |
| Repeat-control mismatch fixture | `.ufo/evidence/round-12/ControlGate/mismatch/` | not read in detail | Expected `controls_mismatch`/1 needs a `--snapshot` run. |
| Repeat-control snapshot design | `.ufo/evidence/round-12/SnapshotReview/probe-output.txt:1-20` | digest-only misses additions/pin rewrites; strict check catches them | Design probe, not a `--snapshot` run. |
| Repeat-control `--selftest` | none located | — | **Gap.** |
| Witness study `selftest` | `.ufo/evidence/round-12/BashWitness/selftest.out` | `WITNESS_SELFTEST: 21/21 pass`, `VERDICT: PASS` | Recorded. Trailing unrelated shell-state sentence: artifact defect, do not cite. |
| Witness study sweep (`run`/`count`) | none located | — | **Gap**: no measured C2 attribution. |
| Pristine target copy | `.ufo/evidence/round-12/BashWitness/pristine.sh` | — | L1 compares digest with pin at `tools/bash-witness-study.py:85-98`. |
| Scalar measure | `.ufo/evidence/round-12/measure.py`; `LOG.md:663` | depth 6, calibration 6, delta 0 | Recorded. |

Exit map (`tools/repeat-control.py:115-123`; `corpus/knowledge/repeated-control-precondition.md:34-41`): controls_match 0; controls_mismatch 1; baseline_nonzero 2; command_unavailable 2; snapshot_tampered 2; setup_error 2; invalid_usage 64.

Six legs: `tools/mutate-and-run.sh:84-89`, unchanged (`corpus/knowledge/repeated-control-precondition.md:49`). Recorded pin sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`.

### 3. Claim C1 — repeated pristine-control gate
- Knowledge note: `corpus/knowledge/repeated-control-precondition.md:1-60` (S004 located `:10-14`; S026 located `:16-22`; "retries do not repair" `:27`; contract `:34-41`; boundaries `:51-56`).
- Source rows: `corpus/SOURCES.md:15` (S004), `:17` (S006), `:22` (S011), `:37` (S026), `:39` (S028), `:41` (S030, rejected).
- Gate decisions: `corpus/lessons/round-12.md:20-24`. The 3-run rule is "the round's choice, not a sourced rule" (`corpus/knowledge/repeated-control-precondition.md:48`).
- Filing ambiguity for L1: calibration (spec) vs capability F3 at `SCORECARD.md:268-270`.
- State: gate and knowledge present; selftest and snapshot receipts not located. Do not write "C1 passes".

### 4. Claim C2 — declared-witness split on pinned bash census
- Pin: `fecee8743e52eb8fb5fbb40782934cb619a1a96e` (kagi `corpus/surface-census.sh`), `.ufo/waves/round-12/w1/BashDenominator.md:5, :28`; registry S033 `corpus/SOURCES.md:44`. L1 confirms against BashWitness output.
- Declared mapping and disclosure: `tools/bash-witness-study.py:32-47, 98-170`.
- Attribution correction: `corpus/knowledge/witness-scoped-kill-verdict.md:60` (E1), `:67` (E2), `:68` (E3); contamination note `:63-66`.
- Lesson rows: `corpus/lessons/round-12.md:30-32`.
- Count rule: `corpus/knowledge/repeated-control-precondition.md:53`; `corpus/lessons/round-12.md:24`.
- Depth: `SCORECARD.md:66`; command D `:72-73`. A witness-split case scores only if recorded as a ledger case; none recorded (`LOG.md:663`, delta 0).
- State: declaration and selftest present; sweep receipt not located.

### 5. Touched surfaces
`git diff --stat`: `LOG.md` +10; `corpus/SOURCES.md` +12/−5 (round-12 entry `:101`); `corpus/knowledge/witness-scoped-kill-verdict.md` +3 (`:67-68`). Untracked: `tools/repeat-control.py` (790 lines), `tools/bash-witness-study.py` (1163), `corpus/knowledge/repeated-control-precondition.md` (60), `corpus/lessons/round-12.md` (50), `.ufo/waves/round-12/`, `.ufo/evidence/round-12/`.
- Not touched: `tools/mutate-and-run.sh` (`corpus/knowledge/repeated-control-precondition.md:49`).

### 6. Commits
- Base `18ad5d0` (`corpus/lessons/round-12.md:3`). Round-12 commits observed: none. Pushed commit: supplied by L1.
- `LOG.md:663` still reads "New claim commands and the final measured revision are recorded below after runtime verification." L1 completes or appends.
- Evidence-before-citation: `corpus/QUALITY.md:24-25`.

### 7. Trend caveats
- Round-1 calibration: 0 at `SCORECARD.md:67` vs pinned 6 at `SCORECARD.md:217-218`. Name the cited value.
- Round-1 depth 6: `SCORECARD.md:66`.
- Saturation 8/10, window N=2: `SCORECARD.md:250-255`.
- Discernment `unprovable-but-better`: `SCORECARD.md:118`.
- Round-12 scalar delta 0 (`LOG.md:663`).
- Round-2 freshness plan item 1, outside round-12 scope: `SCORECARD.md:263-267`.

### 8. Stale lanes
- tsukuroi `tools/tsukuroi-census.sh` and mado `tools/mado-verify.sh`: stale + drift as read 2026-10-14 (`corpus/knowledge/fleet-kill-rate-ledger.md`; `.ufo/waves/round-12/w1/ReportScribe.md:74-76`). Not re-measured; report as stale, never current.

### 9. Installs
- This seat: none. Environment observed by sibling probe, not re-measured: Python 3.14.7 (`.ufo/waves/round-12/w1/ReportScribe.md:82`).
- Sibling installs not visible here; L1 collects from each seat report under RULES.md. None located in `corpus/lessons/round-12.md`.

### 10. Out of scope
- Sibling gate code and product clauses: `PROVINCE.md:16-17`, `PROVINCE.md:44-45`.
- Mutation runner: unchanged (`corpus/knowledge/repeated-control-precondition.md:49`).
- Credentials (kagi): `PROVINCE.md:16-17`. Visual UI diffing: `corpus/SOURCES.md:41`, `PROVINCE.md:46`. Engine nondeterminism: `PROVINCE.md:47`.

### 11. Findings and risks
1. **C1 receipt gap**: no `--selftest` or `--snapshot` receipt under `.ufo/evidence/round-12/`. Blocking for any C1 pass line. `tools/repeat-control.py:545`, `:412`.
2. **C2 receipt gap**: no `run`/`count` output under `.ufo/evidence/round-12/BashWitness/`. Blocking for measured C2 attribution. `tools/bash-witness-study.py:522`, `:880`.
3. **LOG incomplete**: `LOG.md:663` defers final measured revision. L1 owns.
4. **Stale ReportScribe draft**: `.ufo/waves/round-12/w1/ReportScribe.md:19` and `:96` say the tool is absent; it now exists untracked. Do not cite the draft as current.
5. **C1 filing ambiguity**: `SCORECARD.md:268-270` vs spec. L1 decides.
6. **Pin confirmation**: `.ufo/waves/round-12/w1/BashDenominator.md:5, :28`; L1 confirms.
7. **Artifact defect**: `.ufo/evidence/round-12/BashWitness/selftest.out` trailing sentence.
8. **Round-1 calibration conflict**: `SCORECARD.md:67` vs `:217-218`.
9. **Clock**: round files UTC 2026-10-20; session header differs. Cite one source.
10. **Authority**: seat reports are not independent admission or promotion (`corpus/knowledge/repeated-control-precondition.md:55`; `corpus/lessons/round-12.md:24`, `:38`).

### 12. Artifact paths
- This map: `.ufo/waves/round-12/w2/ReportEvidence.md`.
- Gate code: `tools/repeat-control.py`, `tools/bash-witness-study.py`.
- Knowledge: `corpus/knowledge/repeated-control-precondition.md`, `corpus/knowledge/witness-scoped-kill-verdict.md`, `corpus/lessons/round-12.md`.
- Sources: `corpus/SOURCES.md`. Evidence: `.ufo/evidence/round-12/`. Log: `LOG.md:655-663`.

## Checks for L1 (not run here)
- `python3 tools/repeat-control.py --selftest`; `--snapshot .ufo/evidence/round-12/ControlGate` (expect 0); on `mismatch/` (expect 1).
- `python3 tools/bash-witness-study.py selftest` and `check`; sweep only if WitnessFinish assigned.
- `bash tools/mutate-and-run.sh --selftest` / `--regression` only if cited as current.
- `git status --short` before commit; include round-12 untracked directories (QUALITY 9).
