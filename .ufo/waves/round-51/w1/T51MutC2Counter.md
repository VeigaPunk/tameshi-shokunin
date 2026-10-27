# T51MutC2Counter — mutation test of the frozen round-51 C2 counter (L1 TameshiR51, wave 1)

Seat: T51MutC2Counter-3 · Lane: tameshi-shokunin · Target: `.ufo/evidence/round-51/c2/measure.py`
(frozen bytes, sha256 `c2c80c0b9e8a7a86ff381b54de8806eb4bcdc415a92b5aa12ddbb366e0432d84`, label `C2_R51_PASS`).
Everything below is observed seat output, run only as `--selftest` or against scratch clones in scratch work
dirs. A probe is never a verdict; this seat decides nothing about claim C2.

## 1. Method

Detectors (the committed, pre-registered ones — no others):

- **D1** — the counter's own `--selftest` (11 named cases): must exit 0 printing
  `C2_R51_SELFTEST: cases=11 failed=0`.
- **D2** — the counter on the **CTL_0** tree (lane at BASE `9962033f`, nothing changed): must exit 1 with the
  last line ending `C2_R51_PASS=false` (contract C2 `before`; controls.py PLAN `('c2','CTL_0',None)`).
- **D3** — the counter on the **CTL_COMMENT** tree (BASE plus only the tenth ledger comment line, the same edit
  controls.py `comment()` makes): must exit 1 with the last line ending `C2_R51_PASS=false`
  (controls.py docstring: "only a tenth ledger comment line — expect false (wired_legs=9)").

A mutant is **killed** iff D1 fails or D2/D3 deviate from the pre-registered outcome; otherwise it **survives**
and is a disclosed counter blind spot. For every weakening survivor I additionally built a **forged tree T_X**
in scratch that satisfies every clause except X and showed the pair (pristine rejects naming `X=0`,
mutant prints `C2_R51_PASS=true`) — the blind spot demonstrated, not argued. M16 (redundancy probe) has no
distinguishing tree; §5 gives the proof and the empirically closed nearest route. M17 is a verdict-wiring
probe, included to measure what the control *harness* (not the clauses) catches.

Protocol per my role: the same detectors were run on pristine bytes, on each mutant, and on restored bytes
(§7). Fixtures: `git clone -q --shared` of the lane, `checkout --detach BASE`, toplevel asserted equal to the
fixture dir before any commit, throwaway identity inside the fixture only. Scratch root
`/fast/scratch/hyaku/tameshi-r51/T51MutC2Counter` (deleted before this report was finished); `HYAKU_SCRATCH`
redirected so no shared controls root is touched. The lane checkout was never written (§7 hashes).

Harness: `receipts/probe.py` (copied beside these receipts); mutants applied as exact single replacements,
each verified `count(old)==1`, compiled, and diffed (`receipts/mutant-diffs.txt`, 17× `compile=OK`).

## 2. Baseline (pristine bytes)

| run | observed | receipt |
|---|---|---|
| D1 selftest | rc=0 · `C2_R51_SELFTEST: cases=11 failed=0` | `selftest-pristine.txt` |
| D2 CTL_0 | rc=1 · wall 148 s · `C2_R51: rev=9962033f… recorded_cases=9 wired_legs=9 depth_score=9 new_legs=0 … C2_R51_PASS=false` — exactly the contract's `before` line and the controls' pre-registered outcome | `run-pristine-ctl0.txt` |
| D3 CTL_COMMENT | rc=1 · wall 141 s · `recorded_cases=10 wired_legs=9 depth_score=9 new_legs=1 … C2_R51_PASS=false` (the lone comment line makes `new_legs=1` but the leg has no wiring, so every flag stays 0) | `run-pristine-ctlcomment.txt` |
| pristine on **T_all** (fully forged tree, §4) | rc=0 · wall 0 s · `recorded_cases=10 wired_legs=10 depth_score=10 new_legs=1 target_new=1 pin_ok=1 spec_prereg=1 sweep_ok=1 sweep_after_freeze=1 table_match=1 regression=1 entry=1 sourced=1 readme=1 predictions_held=7/10 C2_R51_PASS=true` | `run-pristine-tall.txt` |

Two baseline findings, both seat-level observations:

- **F/MUT-1 (forgeability).** The frozen counter passes a fully synthetic tree assembled in a scratch clone:
  tenth ledger line + wiring quadruple (`TABLE_DRIFT`, leg-check entry `…TABLE_DRIFT:10:2`,
  `regression_case_git bash-drift-pins \` call, spec heredoc) + the frozen spec bytes re-committed at
  `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec` + a synthetic `sweep.txt` (GREEN control on the
  true pin `c138d34c…`, one verdict per spec id, restore OK, done, `MUTATE_DATE: 2099-…`) + S272 row
  (`mined`, opened 2026-10-26, used-by naming the entry) + knowledge entry + README line + a runner neutered
  to print `REGRESSION: PASS (cases=10 passed=10…` and exit 0. The counter therefore certifies *receipt
  consistency*, not receipt provenance — its guarantees are exactly the ten clauses, which is the frame for
  every blind spot below.
- **F/MUT-2 (control cost).** One control invocation replays the real 9-leg regression: ≈140–148 s wall per
  run; the C2 pair ≈ 5 min per counter version. Relevant operationally if the controls are ever re-run
  per-commit.

## 3. The mutants (17 single edits)

Each mutant weakens exactly one clause of the frozen predicate; clause line numbers are in the pristine
`measure.py`. All 17 compile and differ from pristine by the one intended edit (`mutant-diffs.txt`); D1 runs:
`selftest-M*.txt`; D2/D3 runs: `run-M*-ctl0.txt`, `run-M*-ctlcomment.txt`.

| id | clause weakened (measure.py:line) | D1 | D2 | D3 | verdict |
|---|---|---|---|---|---|
| M01_wired_clause_drop | all-10-wired dropped from `passed` (275) | pass | pass | pass | SURVIVED — blind spot B1 |
| M02_spec_sha_drop | spec sha256 == frozen `SPEC_SHA` dropped (250) | pass | pass | pass | SURVIVED — B2 |
| M03_embed_equality_drop | embedded heredoc == spec file dropped (250) | pass | pass | pass | SURVIVED — B3 |
| M04_after_freeze_drop | `sweep_after_freeze` dropped from `need` (273-274) | pass | pass | pass | SURVIVED — B4 |
| M05_control_pin_wildcard | CONTROL `pristine-sha256==PIN` wildcarded (137) | pass | pass | pass | SURVIVED — B5 |
| M06_verdict_set_relax | dup/INCONCLUSIVE defect verdict lines accepted (149) | pass | pass | pass | SURVIVED — B6 |
| M07_table_match_drop | `table_match` dropped from `need` (273-274) | pass | pass | pass | SURVIVED — B7 |
| M08_regression_breadth | any `REGRESSION: PASS (` accepted, not `cases=10 passed=10` (187) | pass | pass | pass | SURVIVED — B8 |
| M09_entry_date_drop | SOURCES row `opened 2026-10-26` dropped (211) | pass | pass | pass | SURVIVED — B9 |
| M10_usedby_drop | used-by-lists-entry dropped (211) | pass | pass | pass | SURVIVED — B10 |
| M11_readme_prefix_drop | README append-only (`startswith(base_readme)`) dropped (203) | pass | pass | pass | SURVIVED — B11 |
| M12_target_new_drop | copied leg target accepted (243) | pass | pass | pass | SURVIVED — B12 |
| M13_pin_verify_drop | `PIN == sha256(blob@rev)` dropped, syntactic pin suffices (246) | pass | pass | pass | SURVIVED — B13 |
| M14_base_present_drop | nine-base-legs-retained dropped from branch gate (237) | pass | pass | pass | SURVIVED — B14 |
| M15_freeze_ts_zero | spec first-add commit time ignored (`freeze_ts = 0`, 257) | pass | pass | pass | SURVIVED — B15 |
| M16_recorded_clause_drop | `recorded == 10` dropped from `passed` (275) | pass | pass | pass | EQUIVALENT (§5) |
| M17_exit_always_zero | verdict wiring: `measure()` always exits 0 (280) | **FAIL** (`failed=1`) | **DEVIATES** (rc=0) | **DEVIATES** (rc=0) | KILLED-by-D1/D2/D3 |

(Transcribed from the observed receipts; D1 column = `cases=11 failed=0` on every mutant except M17.)

## 4. The 15 blind spots, each with its forged tree

Every T_X is a scratch clone at BASE plus: the forged tenth leg (fully wired), the forged evidence files, and
one deliberate divergence; `tools/mutate-and-run.sh --regression` is neutered to print
`REGRESSION: PASS (cases=10 passed=10…` so the regression clause is green and the divergence is isolated.
Observed pairs (pristine vs mutant on the identical tree); full stdout with `--explain` in each named receipt.

- **B1 / M01** (`t-wired`): leg-check entry declares `…TABLE_DRIFT:10:3` while the table holds 2 KILLED → the
  tenth leg is **unwired** (`C2_LEG bash-drift-pins: UNWIRED (table-counts)`, `wired_legs=9`).
  Pristine rc=1 `wired_legs=9 … false` vs M01 rc=0 `wired_legs=9 … C2_R51_PASS=true` — the counter would count
  an unwired leg toward depth. `run-flip-wired-{pristine,mutant}.txt`
- **B2 / M02** (`t-spec_sha`): committed spec = frozen bytes + one appended line (and the heredoc matches it),
  so sha256 ≠ frozen `SPEC_SHA` — pre-registration binding broken, receipts self-consistent.
  pristine rc=1 `spec_prereg=0` vs M02 rc=0 true. `run-flip-spec_sha-*.txt`
- **B3 / M03** (`t-spec_embed`): committed spec = frozen bytes (sha green) but the runner's heredoc drops the
  last defect line — the mutation set actually executed by `--regression` diverges from the registered spec.
  pristine rc=1 `spec_prereg=0` vs M03 rc=0 true. `run-flip-spec_embed-*.txt`
- **B4 / M04 + B15 / M15** (`t-after`): `MUTATE_DATE: 2020-01-01T00:00:00Z` — the sweep predates the spec's
  first-add commit (pre-registration violated). pristine rc=1 `sweep_after_freeze=0` vs M04 rc=0 true and
  M15 rc=0 `sweep_after_freeze=1 … true` (M15 hardcodes `freeze_ts = 0`, so *any* parseable date passes).
  `run-flip-after_freeze-{pristine,mutant}.txt`, `run-flip-after_freeze-M15-{pristine,mutant}.txt`
- **B5 / M05** (`t-control_pin`): CONTROL line `pristine-sha256=aaa…` ≠ PIN — the green control measured a
  different blob. pristine rc=1 `sweep_ok=0` vs M05 rc=0 true. `run-flip-control_pin-*.txt`
- **B6 / M06** (`t-verdicts`): `DEFECT S_USAGE_EXIT: INCONCLUSIVE` in receipt and table — an unadjudicated
  defect still counts toward the ten (cosmetic side effect: `predictions_held=6/10`). pristine rc=1
  `sweep_ok=0` vs M06 rc=0 true. `run-flip-verdict_set-*.txt`
- **B7 / M07** (`t-table`): `TABLE_DRIFT` swaps the first two verdicts relative to the sweep — the ledger's
  recorded claim contradicts the recorded run. pristine rc=1 `table_match=0` vs M07 rc=0 true.
  `run-flip-table_match-*.txt`
- **B8 / M08** (`t-reg9`): neutered runner prints `REGRESSION: PASS (cases=9 passed=9…` — the tenth case
  never ran. pristine rc=1 `regression=0` vs M08 rc=0 true. `run-flip-regression9-*.txt`
- **B9 / M09** (`t-entry_date`): S272 row `mined` but opened `2026-10-19` — a stale row stood in for the
  round-day sourcing requirement. pristine rc=1 `sourced=0` vs M09 rc=0 true. `run-flip-entry_date-*.txt`
- **B10 / M10** (`t-usedby`): S272's used-by cell names a different entry — the entry↔row linkage is forged.
  pristine rc=1 `sourced=0` vs M10 rc=0 true. `run-flip-usedby-*.txt`
- **B11 / M11** (`t-readme`): `corpus/README.md` rewritten in place (first-line byte flipped) with the entry
  name appended — not an append beyond base bytes. pristine rc=1 `readme=0` vs M11 rc=0 true.
  `run-flip-readme_prefix-*.txt`
- **B12 / M12** (`t-target_new`): the "new" leg's call targets `kagi-shokunin/corpus/surface-census.sh` (a
  base target) pinned at `fecee874` with its true blob sha — depth claimed for a re-run of an existing case.
  pristine rc=1 `target_new=0` vs M12 rc=0 true. `run-flip-target_new-*.txt`
- **B13 / M13** (`t-pin_verify`): `PIN_DRIFT=ffff…` (64 hex, no such blob) with the receipt consistently
  carrying the fake pin — the pin is never tied to content. pristine rc=1 `pin_ok=0` vs M13 rc=0 true.
  `run-flip-pin_verify-*.txt`
- **B14 / M14** (`t-base`): ledger drops the `js-cite-check` line and duplicates `bash-surface-census` — a
  base leg silently missing while `recorded_cases=10`. pristine rc=1 (branch skipped, all flags 0) vs M14
  rc=0 true. `run-flip-base_present-*.txt`

## 5. M16 — equivalent mutant (no blind spot)

`recorded == 10` is redundant enforcement given the clauses kept: `LEDGER_RE` and `LEG_RE` match the same
lines, so `recorded == len(legs)`; `wired ⊆ legs`, so `len(wired) == 10` forces `recorded ≥ 10`; and
`wiring()`'s checks are **name-keyed** (`in text`), so a duplicate ledger line of an already-wired leg yields
*two wired entries* (`len(wired) = 11`), an unwired extra name is either new (breaks `new_legs == 1`) or a
broken base leg (breaks `base_present`, skipping the branch). Closed empirically on the nearest route:
`t-m16try` (11 ledger lines via a duplicated wired base leg) → pristine rc=1 false **and** M16 rc=1 false
(`run-flip-m16try-{pristine,mutant}.txt`). D1/D2/D3 on M16 are pristine-identical. Verdict: EQUIVALENT —
not a coverage finding, the clause is belt-and-braces.

## 6. What the detectors actually pin

- **D1 (selftest)** pins parser units: ledger/wiring counts, `leg_call` parse, heredoc byte-extraction,
  `spec_defects` parse, `sweep_check`'s GREEN-check/not-ok/after-computation unit behavior, and the e2e
  false-on-empty-ledger contract (`rc == 1` asserted). It does **not** reach any clause-consumer: 16/17
  mutants pass it; the one that fails (M17) fails on the exit-code assertion of the e2e case, not on a clause.
- **D2/D3 (committed controls)** pin that 9-leg trees stay `false` and that the exit-code wiring is intact —
  M17 deviates on both trees (rc=0) and is killed by the harness expectation `rc==1 ∧ …PASS=false` as well.
  They cannot see a clause drop: on their trees `passed` short-circuits at `recorded==10`/`new_legs==1` before
  any dropped clause is consulted, so 15/15 weakening mutants sail through.
- **Net:** the frozen counter has **no regression fixture that exercises a positive (PASS) path per clause**.
  The T_X set in §4 is exactly the per-clause positive fixtures a counter regression suite would need; as
  committed, a one-edit weakening of any of the ten clauses (or the pin/spec/receipt bindings) ships
  undetected. This is a seat finding about the counter's test surface, not about claim C2's truth.

## 7. Bounds, restoration evidence, tooling

- Lane `measure.py` sha256 `c2c80c0b…2d84` before and after the whole probe (never written); all mutant bytes
  lived only in scratch; `measure.restored.py` (byte-identical copy) re-passes D1. No git mutation anywhere
  outside scratch fixtures; no pacman/uv installs (none needed).
- Scratch root `/fast/scratch/hyaku/tameshi-r51/T51MutC2Counter` removed before yielding; every cited output
  is copied to `w1/receipts/`. Fixtures asserted `git rev-parse --show-toplevel` == fixture dir before their
  only commit.
- Detector cost note: D2/D3 ≈ 140–148 s per counter run (real 9-leg regression replay); the full 17×2 matrix
  ≈ 80 min CPU, run 3-way.

## Summary

- Mutation-tested the frozen C2 counter with 17 single-edit mutants against its own 11-case selftest and the
  two committed controls (CTL_0, CTL_COMMENT); baselines reproduce the pre-registered `false` outcomes.
- 15 clause-weakening mutants survive all three detectors; each demonstrated with a forged scratch tree that
  pristine rejects (naming the clause) and the mutant passes — blind spots B1–B15 (wired-count, spec sha,
  spec embedding, sweep date/pre-registration ×2, control pin, verdict set, table match, regression breadth,
  entry date, used-by, README prefix, copied target, pin verify, base-leg retention).
- M16 (`recorded == 10` drop) is equivalent: `wired ⊆ legs` and name-keyed wiring make the clause redundant;
  nearest distinguishing route empirically closed.
- M17 (always exit 0) is the only kill — caught by D1's e2e exit-code assertion and by the control harness
  expectation, not by any predicate clause.
- Finding: the counter has no positive-path regression fixture per clause; a one-edit weakening of any clause
  ships undetected. The T_X fixtures here are the missing per-clause positives.
- The frozen counter also accepts a fully synthetic receipt tree (F/MUT-1): it measures receipt consistency,
  not provenance.
- No tooling installed; lane bytes unchanged (sha256 evidence); scratch cleaned; receipts in `w1/receipts/`.
