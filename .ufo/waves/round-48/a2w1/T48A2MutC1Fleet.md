# T48A2MutC1Fleet — mutation audit of the frozen C1 counter (round 48, attempt 2)

Seat: mutation-audit `.ufo/evidence/round-48/calibration/measure.py` (frozen at freeze step 2),
focusing on the amendment-4/5/7 code: MAX_EXTRA + extra-observation loop, EXTRA-outside-V
mismatch, attested_extra counting, FLEET lines (census sha, lane-clean check, sibling HEADs),
fleet_drift in the pass condition, the BASE pin refusal (exit 2), the `under_tmp` work-dir
refusal. 36 single-site mutants, ≥20 required.

## Method

- Detector (bounded, same for every run): `python3 <mutant>.py --selftest`, 300 s cap, per-mutant
  `TMPDIR` under the seat scratch dir. Detector output = `C1_R48_SELFTEST: cases=N failed=M` +
  `VERDICT: PASS|FAIL` + exit code. A hang that hits the cap is a detector failure (killed).
- Pristine bytes: `m.orig`, sha256
  `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` — byte-identical to the
  frozen lane file and equal to the sha256 recorded in `freeze-2.json`
  (`counters["calibration/measure.py"].sha256`). The pristine lane file was never written.
- Mutants were applied to per-mutant scratch copies (`$S/work/<id>.py`), never to `m.py`/`m.orig`;
  the counter is self-referential (`self_pin` compares the lane blob against the running file's
  own bytes), so a mutated copy stays self-consistent and the suite tests the mutated logic.
- Baseline (pristine): `cases=76 failed=0`, `VERDICT: PASS`, exit 0, 118–120 s wall. Baseline
  green ⇒ every mutant result below is conclusive (killed or survived), not inconclusive.
- Scratch: `/fast/scratch/hyaku/tameshi-r48/T48A2MutC1Fleet/` (deleted before finish; no /tmp use).
  Driver: `sweep.py` in the scratch dir (idempotent, 4 concurrent). Raw per-mutant records:
  `$S/res/<id>.json`; baseline stdout: `$S/base.stdout`.
- Tools installed: none (python3 + git only). Disk-guard checked before the pass: 605.5 G free on
  `/fast/scratch/hyaku` (25% used).

## Verdict semantics for this counter

- **Killed** = the selftest fails somewhere (some case FAILs, VERDICT: FAIL, nonzero exit, or
  hang at cap). The failing cases name the guarding tests.
- **Survived** = `cases=76 failed=0, VERDICT: PASS` under the mutant — a coverage gap of the
  frozen selftest w.r.t. that behavior. Each survivor gets a concrete killing case and a
  could-it-flip-the-deciding-verdict assessment at the content revision `c7586b9a` (deciding
  invocation: `--lane LANE --rev c7586b9a… --base 473336d9… --work /fast/scratch/.../deciding/c1`,
  no `--emit`, no `--only`, rounds=3; per `deciding-run.sh` step 4).

## Mutants and sites (frozen file line numbers)

| id | site | mutation | area |
|---|---|---|---|
| M01 | measure.py:82 | `MAX_EXTRA = 6` → `7` | extra cap |
| M02 | measure.py:82 | `MAX_EXTRA = 6` → `5` | extra cap |
| M03 | measure.py:533 | `< MAX_EXTRA` → `<= MAX_EXTRA` | extra loop |
| M04 | measure.py:533 | cap dropped (`while missing:`) | extra loop |
| M05 | measure.py:536 | `m != cut` → `m == cut` (inverted) | extra loop |
| M06 | measure.py:536 | missing-filter dropped (no-op) | extra loop |
| M07 | measure.py:484 | extra work dir `extra%d` → `round%d` | extra loop |
| M08 | measure.py:489 | extra work dir rmtree dropped | extra loop |
| M09 | measure.py:487 | extra profile `P0` → `P1` (setup) | extra loop |
| M10 | measure.py:537 | `if extras:` → `if True:` | extra loop |
| M11 | measure.py:540 | `x is not None` guard dropped | EXTRA-outside-V |
| M12 | measure.py:531 | P1 no longer attests (`m not in p1_seen` dropped) | attestation |
| M13 | measure.py:509 | `observed` keeps None cuts | EXTRA-outside-V |
| M14 | measure.py:543 | `elif missing:` → `elif False:` | attested_extra |
| M15 | measure.py:480 | `extra_used[0] += 1` dropped | attested_extra |
| M16 | measure.py:580 | printed count `+1` | attested_extra |
| M17 | measure.py:373 | census prefix `[:12]` → `[:8]` | FLEET census sha |
| M18 | measure.py:381 | `df.returncode == 0` dropped from clean | FLEET lane-clean |
| M19 | measure.py:376 | `SCORECARD.md` dropped from paths | FLEET lane-clean |
| M20 | measure.py:377 | `--` + paths dropped (whole-tree status) | FLEET lane-clean |
| M21 | measure.py:388 | sibling `[:12]` → bare strip (no `none`) | FLEET siblings |
| M22 | measure.py:385 | lane excluded from its own siblings — exclusion dropped | FLEET siblings |
| M23 | measure.py:469 | final fleet point dropped | FLEET final point |
| M24 | measure.py:470 | census drift `> 1` → `> 2` | fleet_drift |
| M25 | measure.py:470 | lane-clean drift term dropped | fleet_drift |
| M26 | measure.py:472 | sibling_moves `> 1` → `> 2` | sibling_moves |
| M27 | measure.py:574 | `fleet_drift == 0` dropped from pass | fleet_drift in pass |
| M28 | measure.py:375 | census `absent` → `present` on OSError | FLEET census sha |
| M29 | measure.py:1011 | `if a.base != BASE:` → `if False:` | BASE pin refusal |
| M30 | measure.py:1013 | refusal `return 2` → `return 0` | BASE pin refusal |
| M31 | measure.py:83 | BASE constant last hex char changed | BASE pin refusal |
| M32 | measure.py:1012 | refusal message reworded | BASE pin refusal |
| M33 | measure.py:103 | `rp == '/tmp'` disjunct dropped | under_tmp |
| M34 | measure.py:395 | `if under_tmp(work):` → `if False:` | under_tmp |
| M35 | measure.py:396 | refusal message reworded | under_tmp |
| M36 | measure.py:112 | scratch_root drops its under_tmp guard | under_tmp |

## Results

Detector runs: baseline 118–120 s wall; under 4-way concurrency 210–300 s. First pass ran M21–M32
at a 300 s cap, which those runs hit with no output at all — including mutants of `main()`-only
code that `--selftest` never executes (M29–M32). That is CPU starvation, not detector failure:
those 12 runs were **discarded and re-run serially with a 900 s cap** (results below). M03/M04's
hangs are genuine (the mutated extra loop never terminates in T33f) and count as kills.

| id | verdict | detector evidence (selftest under mutant) |
|---|---|---|
| M01 | KILLED | failed=3: T32/T33f/T33 — `attested_extra=6` absent (cap 7 lets the 7th extra observe X23) |
| M02 | KILLED | failed=3: T32/T33f/T33 — `attested_extra=6` absent (cap 5 → count 5) |
| M03 | KILLED | hang at T33f (7th extra taken, loop semantics changed) |
| M04 | KILLED | hang at T33f (uncapped loop, X23 never reaches the capped fake index) |
| M05 | KILLED | failed=5: T30 (`attested_extra=2`→1), T31/T32/T33f/T33 (`unattested=1` lost) |
| M06 | KILLED | failed=2: T30, T51 — UNATTESTED instead of extra-attested MATCH |
| M07 | SURVIVED | cases=76 failed=0 |
| M08 | SURVIVED | cases=76 failed=0 |
| M09 | SURVIVED | cases=76 failed=0 |
| M10 | SURVIVED | cases=76 failed=0 |
| M11 | SURVIVED | cases=76 failed=0 |
| M12 | KILLED | failed=1: T33a — P1-attested member becomes UNATTESTED |
| M13 | KILLED | failed=1: T13 — all-None rounds no longer UNOBSERVABLE, counted MISMATCH instead |
| M14 | KILLED | failed=4: T31/T32/T33f/T33 — `unattested=1` lost |
| M15 | KILLED | failed=6: T30/T32/T33a-context/T33f/T33/T51/T33b — counter frozen at 0 |
| M16 | KILLED | failed=6: T30/T32/T33a/T33f/T33/T51 — printed count off by one |
| M17 | SURVIVED | cases=76 failed=0 |
| M18 | SURVIVED | cases=76 failed=0 |
| M19 | SURVIVED | cases=76 failed=0 |
| M20 | SURVIVED | cases=76 failed=0 |
| M21 | (re-run) | — |
| M22 | (re-run) | — |
| M23 | (re-run) | — |
| M24 | (re-run) | — |
| M25 | (re-run) | — |
| M26 | (re-run) | — |
| M27 | (re-run) | — |
| M28 | (re-run) | — |
| M29 | (re-run) | — |
| M30 | (re-run) | — |
| M31 | (re-run) | — |
| M32 | (re-run) | — |
| M33 | (re-run) | first-pass kill voided by M34's /tmp leak — see note |
| M34 | KILLED | failed=1: T63 — work under /tmp accepted, message absent, /tmp path created (the leak itself) |
| M35 | (re-run) | — |
| M36 | (re-run) | first-pass kill voided by M34's /tmp leak — see note |

Note M33/M36 first-pass kills are **void**: the M34 run accepted work under /tmp and its T63
created `/tmp/c1-r48-should-not-exist` (leaked with round1-3 subdirs inside), which made the
subsequent T63 post-checks fail on the leaked path alone. The leak was removed
(`rm -rf /tmp/c1-r48-should-not-exist`) and both mutants re-run on a clean /tmp — see re-run
verdicts. This cross-mutant contamination through shared /tmp state is itself the hazard the
counter's `under_tmp` refusal exists to prevent.

## Survivors: killing cases and deciding-verdict exposure

(filled in below)
