# NoHarmSelftests — no-harm rerun of every lane selftest at eb7838b

Seat: `TameshiR17.NoHarmSelftests-2` (leaf; no dispatch). Wave context claims attacked: C1 *calibration* and C2
*operability* only insofar as "nothing else regressed" — this seat re-executed the full selftest surface and compared
it row-by-row with the wave-1 baseline receipt.

**Verdict: holds. No regression. Every baseline row still exits 0 with the same or a strict superset of checks.**

- Landing rev verified in clone: `eb7838b16490ca7ba17ea3242ade76a61f744af2` (2026-10-20 12:59:15 -0300).
- Baseline compared against: `.ufo/evidence/round-17/noharm-baseline-98bea7d.json` (rev `98bea7da…`, 12 runs, 428 checks).
- Environment reproduced exactly: Python 3.14.8, GNU bash 5.3.20(1)-release (baseline `environment` block).
- Clone: fleet-mirror layout under `/tmp/tameshi-r17w2-NoHarmSelftests-2-XE1iS4/fleet/tameshi-shokunin`; nothing run
  against the live lane root.

## 1. Baseline row-by-row parity

| # | baseline row | baseline | now at eb7838b | exit | delta |
|---|---|---|---|---|---|
| 1 | mar-selftest | 83/83 | **95/95** | 0 | +12 (all added; none dropped) |
| 2 | mar-regression | 7/7 cases | **7/7 cases** | 0 | 0 |
| 3 | bws-selftest | 41/41 | **41/41** | 0 | 0 |
| 4 | cc-selftest | 49/49 | **49/49** | 0 | 0 |
| 5 | ed-selftest | 34/34 | **56/56** | 0 | +22 (all added; none dropped) |
| 6 | pd-selftest | 18/18 | **19/19** | 0 | +1 (`detached-head-uses-branch-tip`) |
| 7 | rc-selftest | 29 cases | **29 cases** | 0 | 0 |
| 8 | wm-selftest | 39/39 | **39/39** | 0 | 0 |
| 9 | r16measure-selftest | 38/38 | **38/38** | 0 | 0 |
| 10 | r16assemble-selftest | 38 `[ok]` | **38 `[ok]`** | 0 | 0 |
| 11 | r16reattr-selftest | new 8/8, old 5/8 fails (intended), fidelity 14/14 | **same** | 0 | 0 |
| 12 | r15verify (`--rev 7650fe4…`) | 44/44, exit 0 | **44/44, exit 0** | 0 | 0 |

Check math: baseline total 428 + 12 + 22 + 1 = **463** checks in the 12 baseline rows now, all passing; zero `FAIL`
and zero `[not ok]` lines in any captured output (`grep -l '^FAIL' *.txt` → nothing; `[not ok]` counts all 0).

Key output lines (verbatim):

```
MUTATE_SELFTEST: 95/95 pass            / VERDICT: PASS
REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)
WITNESS_SELFTEST: 41/41 pass           / VERDICT: PASS
SELFTEST: PASS (49/49)                 (context-capture)
SELFTEST: PASS (56/56)                 (evidence-disposition)
SELFTEST: PASS (19/19)                 (pin-disposition)
SELFTEST: PASS (29 cases)              (repeat-control)
SELFTEST: PASS 39/39                   (witness-metadata)
MEASURE_SELFTEST: 38/38 pass           (round-16 measure)
SELFTEST: all checks passed            (round-16 assemble; 38 [ok], 0 [not ok])
SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)
44 PASS, 0 FAIL  → verification-4.json passed=true, failed_checks=[]
```

## 2. New round-17 rows (no baseline entry exists)

| tool | command | result | exit |
|---|---|---|---|
| `tools/registry-check.py` | `--selftest` | `SELFTEST: PASS (34 cases)` | 0 |
| `.ufo/evidence/round-17/measure.py` | `--selftest` | `MEASURE_SELFTEST: 89/89 pass` | 0 |
| `.ufo/evidence/round-17/coldread/trace-inputs.py` | `--selftest` | `SELFTEST: 27/27` | 0 |
| `.ufo/evidence/round-17/coldread/assemble.py` | `--selftest` | `SELFTEST: all checks passed` (59 `[ok]`, 0 `[not ok]`) | 0 |

Total this rerun: **16 runs, 16 × exit 0, 672 passing checks** (463 baseline-surface + 209 new round-17).

## 3. Why three tool hashes moved (and proof the movement is additive)

`.ufo/evidence/round-17/noharm-baseline-98bea7d.json` `tools_sha256` vs the clone at eb7838b:

```
SAME  tools/bash-witness-study.py       49e9e5e2…  (hash unchanged from baseline)
SAME  tools/context-capture.py          c4a1d165…
DIFF  tools/evidence-disposition.py     1609a9df… → f8f05c7a…   (R16-OP1 v2 hardening)
DIFF  tools/mutate-and-run.sh           0673d2e5… → fb6d86d5…   (GIT_* scrub + repo-identity guard)
DIFF  tools/pin-disposition.py          29725397… → 331529ea…   (jj branch-tip resolution)
SAME  tools/repeat-control.py           296fe566…
SAME  tools/witness-metadata.py         df339068…
SAME  .ufo/evidence/round-16/measure.py 03b67f58…
SAME  .ufo/evidence/round-16/coldread/assemble.py 9ee9264a…
SAME  .ufo/evidence/round-16/attribution/reattribute.py eaf564e4…
SAME  .ufo/evidence/round-15/verify.py  7e4519d9…
NEW   tools/registry-check.py           0bf9d1d2971c…  (no baseline row by design)
NEW   .ufo/evidence/round-17/measure.py                f348adc3d88a…
NEW   .ufo/evidence/round-17/coldread/trace-inputs.py  521be95581a5…
NEW   .ufo/evidence/round-17/coldread/assemble.py      d525c1807d55…
```

To prove the count growth is not silent case loss, I ran the **baseline-rev versions** of the three changed tools in a
second fleet-mirror clone at `98bea7d` and diffed emitted case-name sets:

- `mutate-and-run.sh --selftest`: old 83 PASS lines / new 95, `comm -23 old new` = **empty**; new-only = 7 × `GIT_*` +
  5 × `repo-identity` (exactly the r17 runner guard; `tools/mutate-and-run.sh:1685-1721`).
- `evidence-disposition.py --selftest`: old 34 cases / new 56; dropped = **none**; added = 22 `v2-*` cases
  (`v2-gitdir-env`, `v2-shallow-repo` at `tools/evidence-disposition.py:2580,2595`, etc.).
- `pin-disposition.py --selftest`: old 18 / new 19; dropped = none; added =
  `detached-head-uses-branch-tip` (`tools/pin-disposition.py:1299`).

## 4. Falsification probe: did the r17 hermetic-git fix overcorrect?

The r17 commit exists because `GIT_CONFIG_GLOBAL=/dev/null` once left fixture `commit-tree` without an identity.
Re-running the affected selftests under that exact hostile env still passes:

```
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 bash tools/mutate-and-run.sh --selftest        -> 95/95 PASS, exit 0
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 python3 tools/evidence-disposition.py --selftest -> 56/56 PASS, exit 0
GIT_CONFIG_GLOBAL=/dev/null                       python3 .ufo/evidence/round-17/measure.py --selftest -> 89/89, exit 0
```

So the guard is effective and is not masking a dependency on ambient git identity.

## 5. Observed non-regressions worth naming

- **Timing differs, correctness does not.** mar-regression 192 s here vs 121 s in the baseline receipt; host load
  average was 41.4 on 32 CPUs (other lanes live) while the baseline seat ran quieter. All 7 cases still PASS with
  `killed-delta<=0 flips<=0`, and the workdir removed on PASS (`/tmp/tameshi-r4-2-regression.bV8o78 (removed on PASS)`).
- **r15 verify side effect unchanged in kind.** It increments to `attempt-4` (attempts 1–3 already exist) and writes
  `.ufo/evidence/round-15/attempt-4/` + `verification-4.json` create-only; both appear as untracked files in the clone
  and neither is tracked at either rev (`git ls-tree` at 98bea7d and eb7838b list only `attempt-3/*`). `git diff --stat`
  against eb7838b is empty — **no tracked file was modified by any run** (`git status --porcelain` shows only those two
  untracked paths).
- **Scratch retention is parity, not new leakage.** `round-17/measure.py --selftest` keeps its scratch and prints it
  (`measure.py:1343`), exactly as round-16 measure does in the baseline row; `trace-inputs` selftest asserts
  `temp-workdirs-deleted` (`trace-inputs.py:916`) and passed, keeping only its own outer fixture dir. `round-17 assemble`
  left 0 dirs; `registry-check` left 0.
- **All four r17 scratch trees are under /tmp**, none inside the lane root (the `no-artifacts-inside-root` and
  `hermetic-no-lane-path` assertions in the new suites passed).

## 6. Commands executed (all from `$C`, clone at eb7838b)

```
git clone -q <lane> … && git checkout -q --detach eb7838b16490ca7ba17ea3242ade76a61f744af2   exit 0
python3 tools/bash-witness-study.py selftest                       exit 0
python3 tools/context-capture.py --selftest                        exit 0
python3 tools/evidence-disposition.py --selftest                   exit 0
python3 tools/pin-disposition.py --selftest                        exit 0
python3 tools/repeat-control.py --selftest                         exit 0
python3 tools/witness-metadata.py --selftest                       exit 0
python3 tools/registry-check.py --selftest                         exit 0
bash tools/mutate-and-run.sh --selftest                            exit 0
bash tools/mutate-and-run.sh --regression                          exit 0
python3 .ufo/evidence/round-16/measure.py --selftest               exit 0
python3 .ufo/evidence/round-16/coldread/assemble.py --selftest     exit 0
python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest exit 0
python3 .ufo/evidence/round-17/measure.py --selftest               exit 0
python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest exit 0
python3 .ufo/evidence/round-17/coldread/assemble.py --selftest     exit 0
python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72  exit 0
# baseline-rev comparison clone (98bea7d):
bash tools/mutate-and-run.sh --selftest                            exit 0 (83/83)
python3 tools/pin-disposition.py --selftest                        exit 0 (18/18)
python3 <98bea7d copy>/evidence-disposition.py --selftest           exit 0 (34/34)
# env probes:
GIT_CONFIG_GLOBAL=/dev/null … mutate-and-run.sh --selftest         exit 0 (95/95)
GIT_CONFIG_GLOBAL=/dev/null … evidence-disposition.py --selftest   exit 0 (56/56)
GIT_CONFIG_GLOBAL=/dev/null … round-17/measure.py --selftest       exit 0 (89/89)
```

No tool installs or upgrades were needed for this seat.

## 7. Residual unknowns

- I did not re-execute the baseline seat's exact mar-regression wall clock; the 71 s delta is attributed to host load
  (41.4/32) — [INFERENCE], not measured against an idle host.
- I checked selftest/verify surfaces only, as assigned. Non-selftest behaviour of the changed disposition/pin tools
  (v2 manifests, registry rows) is C2 territory and belongs to the C2/registry seats.
- The `attempt-4` name is a function of pre-existing attempt serials; a fresh clone would regenerate the same serial
  deterministically, but I did not assert byte-equality of the regenerated receipt across clones.

**One-line verdict: attacked the "no-harm" claim across all 16 lane selftest/verify entry points at eb7838b — every
baseline row still exits 0 with a strict superset (428 → 463 checks, +209 new round-17 checks, 0 failures, 0 tracked
files modified), so the claim holds and I found no regression.**
