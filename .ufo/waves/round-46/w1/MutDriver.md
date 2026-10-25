seat: MutDriver
item: mutation-audit of the C2 driver `.ufo/evidence/round-46/hardening/mutate.py` (freeze 745a583181648cfc7f9c1b476cd1be7dc68f7433) — one minimal mutation per declared rule, detected by the driver's own 8-case `--selftest` plus real runs on scratch git fixtures; lane untouched except this report.

## Setup and provenance
- Scratch root `/tmp/tameshi-r46-MutDriver/` (tree mirror `.ufo/evidence/round-46/hardening/`, probes, fixtures, out logs). All runs used `TMPDIR=/tmp/tameshi-r46-MutDriver/tmp`.
- Driver and manifest extracted from the freeze rev into the scratch tree:
  `git -C LANE show 745a5831...:mutate.py | sha256sum` = `999e0a4b6e4725666d002130ada8dcad05f81d2fbaaefb4ba7ada4b1fd82ca66`; `mutants.json` = `bd21304a48a0d1e5427387485ffce90dfe02dddfeb3873dc2b9f46a3a03847cd`. Lane worktree files and lane `HEAD:` blobs hash identically — freeze bytes = working tree.
- Pristine selftest (scratch copy): `PASS` x T1..T8, `C2_R46_SELFTEST: cases=8 failed=0`, `VERDICT: PASS`, exit 0.
- No tool installs were needed (python3 + git already present); pacman untouched.

## Required real run (--targets orig, lane, freeze rev) — CONFIRMED
`python3 $LANE/.ufo/evidence/round-46/hardening/mutate.py --lane $LANE --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433 --targets orig` (wall 1.54 s, exit 1):
```
C2_R46: self_pin=1 targets=orig declared=25 killed=0 survived=25 inapplicable=0 neutral_killed=0
        pristine=1 equivalence=-1 rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C2_R46_PASS=false
```
25 mutants all `survived` (freshness F01–F15, coverage C01–C10), all 6 neutrals (FN1–FN3, CN1–CN3) survived, both pristine selftests `pass VERDICT: PASS`. `killed=0 survived=25` — exactly the do-nothing control the contract states.

## Probe matrix — one minimal mutation per rule, detected by `--selftest`
| Rule | Mutation (old -> new, asserted to occur exactly once) | Selftest verdict | Real-run evidence | Audit verdict |
|---|---|---|---|---|
| exact-once replacement | `apply`: `count(old) != 1` -> `> 1` | **KILLED** exit 1, `FAIL T2_missing_old_is_inapplicable` (T7 still passes) | — | covered |
| inapplicable counted as survived | measure: dropped `survived += 1` from the inapplicable branch | survivor, cases=8 failed=0 | D1 vs D2 pair: `survived=2 inapplicable=1` -> `survived=1 inapplicable=1` on the same fixture | survivor |
| timeout counted as killed | `judge`: `'survived' if state == 'pass'` -> `in ('pass','timeout')` | survivor, cases=8 failed=0 | judge() pair on a hanging toy mutant (TIMEOUT bounded to 6 s for the probe): pristine `('T01','killed','timeout')` vs QR3 `('T01','survived','timeout')` | survivor |
| pristine must pass | measure: `pristine_ok &= int(state == 'pass')` -> `&= 1` | survivor, cases=8 failed=0 | D4 pair: failing toy selftest -> pristine driver `pristine=0`, QR4 `pristine=1` (both `declared=0`, judging silently skipped) | survivor |
| neutral survivors required | measure: dropped `and neutral_killed == 0` from `passed` | survivor, cases=8 failed=0 | D5 pair: neutral-labeled killer -> pristine driver `neutral_killed=1 ... PASS=false`, QR5 `neutral_killed=1 ... C2_R46_PASS=true` exit 0 | survivor — PASS flips on a non-compliant fixture |
| killed >= 23 | `MIN_KILLED = 23` -> `= 22` | survivor, cases=8 failed=0 | D6 pair: `killed=22` -> pristine driver `PASS=false`, QR6 `C2_R46_PASS=true` exit 0 | survivor — boundary untested |
| equivalence masking | `mask`: dropped `and '_PASS=' not in t` | **KILLED** exit 1, `FAIL T8_mask_drops_pin_and_pass_tokens` | — | covered |
| `_PASS=true` guard on round-45 output | `equivalence`: `'_PASS=true' not in p.stdout` -> `'_PASS=' not in p.stdout` | survivor, cases=8 failed=0 | direct equivalence() pair with toy counters whose orig prints `C1_R45_PASS=false`: pristine `0`, QR8 `1` (vacuous compare accepted) | survivor |
| self pin | measure: dropped digest compare -> `self_pin = int(blob is not None)` | survivor, cases=8 failed=0 | D9: committed blob = pristine+`# decoy` comment; honest P run `self_pin=0` exit 1, QR9 run `self_pin=1` despite running bytes != pinned blob | survivor |
| `--targets orig` mode | measure: `spec['orig'] if targets == 'orig' else HARDENED[group]` -> `HARDENED[group]` | survivor, cases=8 failed=0 | QR10 vs lane@freeze: `group freshness/coverage target absent ...: .ufo/evidence/round-46/hardening/{freshness,coverage}-counter.py`, `declared=0 killed=0 survived=0 pristine=0` — the required `0/25` baseline is unproducible | survivor — killed by the required baseline confirmation itself |

## Positive control (the driver can pass a compliant fixture)
Fixture D1 (scratch repo, rev f03b2a46992e…, toy counter with 24 independent selftest facts, mutants 24 flips + 1 survivor-weakening + 1 inapplicable + 1 neutral comment, driver bytes committed at SELF_PATH and run from that path):
```
SURVIVORS freshness:S01
C2_R46: self_pin=1 targets=orig declared=26 killed=24 survived=2 inapplicable=1 neutral_killed=0
        pristine=1 equivalence=-1 C2_R46_PASS=true (exit 0)
```
Note: the `SURVIVORS` line lists only the plain survivor; the inapplicable mutant is counted in `survived=` but not listed — consistent with the code, worth knowing when diffing receipts.

## Findings
1. Selftest coverage is exactly toy-shaped: the 8 cases pin `apply`/`judge`/`run_selftest`/`mask` (T1–T8) and kill both mutants aimed there (R1, R7). `measure()`'s predicate assembly — inapplicable counting, timeout classification flow-through, pristine gating, `neutral_killed == 0`, `MIN_KILLED`, the equivalence `_PASS=true` guard, self pin, and orig-mode path selection — has zero selftest coverage; all 8 probes of those rules survived the selftest.
2. Highest-risk survivors are R5 (neutral_killed==0 dropped) and R6 (MIN_KILLED 23->22): each flips `C2_R46_PASS=true` on a fixture a hardened counter could realistically produce (a killed neutral; killed=22). R4 and R9 print lying `pristine=`/`self_pin=` fields without flipping PASS today. R2 and R3 corrupt reported counts only. R8 lets a vacuous equivalence comparison return 1 when the round-45 counter no longer passes its own data revision. R10 silently destroys the orig-mode baseline (its kill case is the very command in my item).
3. No pristine run misbehaved: selftest 8/8, the required lane run matches the contract's do-nothing control field-for-field, and the positive control passes end-to-end. These are coverage findings against the selftest, not defects in the frozen driver's actual behavior, and not grounds to change the contract or the manifest.
4. Unrun check: no probe ran the deciding `--targets hardened` mode against real hardened copies (they do not exist at the freeze rev — observed via the QR10 run's `target absent` lines); equivalence was exercised only on toy counter sources, never over DATA_REV ea25e0224fc81060414b27301c27bd1344669165.

## Restoration evidence
- Probes never mutated the audited tree copy: `cmp tree/.ufo/evidence/round-46/hardening/mutate.py stash/mutate.py` -> identical; sha256 after all runs `999e0a4b…ca66` (mutate.py), `bd21304a…87cd` (mutants.json) — equal to the freeze blobs.
- Each probe file QR1–QR10 differs from pristine by exactly the one asserted-once replacement (construction asserted count==1 before writing).
- Final selftest of the restored tree copy: `C2_R46_SELFTEST: cases=8 failed=0` / `VERDICT: PASS`, exit 0.
- Scratch fixtures are throwaway git repos under `/tmp/tameshi-r46-MutDriver/fixtures/` (each `git init`'d per bounds, `rev-parse --show-toplevel` asserted equal to the repo root before the first commit, throwaway identity used only there): D1 f03b2a46992e, D2 6bea9f88ed9e, D4 d229ffec2f9a, D5 eda3c758f0da, D6 50983f458562, D9 688ec1e4a063. Full run logs in `/tmp/tameshi-r46-MutDriver/out/`.
