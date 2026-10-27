# T52W1MutC1 — mutation test of the frozen C1 counter

- Seat: T52W1MutC1 (mutation-tester, lane leaf; no subagent dispatch)
- Item: mutation-test `.ufo/evidence/round-52/c1/measure.py` (frozen C1 counter, sha256 `3edfdb8737c667430f5555076899851ecaa25e4b2e5ccfe4c0603ae3e0bb3ec6`) on scratch copies; ≥10 one-edit mutants, each weakening one pre-registered clause; kill with `--selftest` + crafted probes; report KILLED/SURVIVED with restoration evidence.
- Date: 2026-10-27. Base counter bytes = commit `1f72d7d8189042b434a2f3753c2c346aefd5ec0f` (lane HEAD `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`), file sha256 as above, `git status --porcelain -- .ufo/evidence/round-52/c1/` empty before and after (receipts/`restored-check.txt`, `hashes.txt`).
- Axes (godspeed): A1 clause coverage (all 11 pre-registered clauses), A2 kill-evidence strength (selftest case > crafted probe > forged scenario), A3 fidelity (one edit per mutant, lane untouched, exact restoration), A4 cost (zero full registry-check executions).

## Method

- Detector 1: `python3 -I <copy> --selftest` (9 cases). Baseline pristine: `C1_SELFTEST: cases=9 failed=0` (receipts/`pristine-selftest.txt`).
- Detector 2: 19-probe battery importing each mutant module and calling `parse_registry_check`, `parse_c3`, `mte_row_ok`, `leg_count`, `cases_missing` on crafted forged strings/dicts (battery recorded in receipts/`results.json`; per-probe expected values asserted on pristine first: 19/19).
- Restoration: lane counter never opened for write; after-hash identical to before-hash; pristine selftest re-run post-work: 9/9 ok (receipts/`restored-check.txt`).
- Full `tools/registry-check.py` executions: **0** (budget preserved; all verdicts are selftest- or probe-level; survivors carry argued forged trees whose parse-level components are probe-proven).
- Tooling record (operator 2026-10-19): nothing installed or upgraded; used system python3 3.14.8, `diff`, read-only `git`. Pacman untouched.
- Mutant corpus + verdicts: receipts/`results.json`; per-mutant selftest outputs receipts/`selftest-M*.txt`; unified diffs `M*.diff` in this directory. Scratch root `/fast/scratch/hyaku/tameshi-r52/T52W1MutC1` deleted before yield.

## Mutants (21, one edit each; line numbers in the pristine counter)

| ID | clause | edit (measure.py:line) | verdict | killed by |
|----|--------|------------------------|---------|-----------|
| M01 | row regex | drop `\|differs` from `(?: (held\|differs))?` (:29) | KILLED | selftest `rc-differs` (also probe `b1_full`: `differs` row becomes unmatched → invisible) |
| M02 | summary held==N | `extra = 0 if m else 1` (:75) | KILLED | selftest `rc-differs` (summary 1/2 accepted → extra 0 ≠ 1) |
| M03 | summary held==N | `held == n` → `held >= n` (:75) | KILLED | crafted `b2_inflated`: `REGISTRY_CHECK: held=5/2` → pristine `(5,2,[],1)`, mutant `(5,2,[],0)` |
| M04 | superseded exclusion | drop `not sup and ` (:72) | KILLED | selftest `rc-differs` (superseded differing row counted → `['b','c']`) |
| M05 | base-active drop | `dropped = sorted(set(base_active) - active)` → `dropped = []` (:117) | SURVIVED | see forged tree below |
| M06 | base-active drop | status filter `== 'active'` → truthy (:116) | SURVIVED | see forged tree below |
| M07 | mte status | drop `r.get('status') == 'active' and ` (:65) | KILLED | selftest `mte-superseded` |
| M08 | mte kind | drop `r.get('kind') == 'gate' and ` (:65) | KILLED | crafted `mte_kind_probe` (kind `probe` accepted) |
| M09 | mte argv | drop `'--check' in argv and ` (:66) | KILLED | crafted `mte_argv_no_check` (argv without `--check` accepted) |
| M10 | mte exit | `exit == 0` → `exit is not None` (:66) | KILLED | crafted `mte_exit1` (exit 1 accepted) |
| M11 | mte needle K | `want` reduced to prefix `MTE_INTEROP: PASS` (:64) | KILLED | selftest `mte-ok` — **fail-closed direction**: needle membership is element equality, so the shortened `want` matches nothing; breaks availability, not soundness. Soundness cousin is M12. |
| M12 | mte needle K | `want in (…or [])` → `want in str(…or '')` (:66) | KILLED | crafted `mte_needle_extra`: needle `MTE_INTEROP: PASS legs_conforming=2/2 (all legs)` → pristine False, mutant True |
| M13 | LEG_TABLE count | `return len(node.value.keys)` → `return 9` (:49) | KILLED | selftest `mte-ok`. Note: on a forged tree regressing LEG_TABLE to 9 legs + needle `9/9` (exactly the R51.1 stale state) the mutant accepts what pristine rejects — selftest catches it only because the fixture uses 2 legs |
| M14 | C3 digest gate | `if hashlib.sha256(c3_src).hexdigest() == C3_SHA:` → `if True:` (:123) | SURVIVED | see forged tree below |
| M15 | C3 summary parse | `total=(\d+)` → `missing=(\d+)` (:81) | KILLED | selftest `c3-parse`. Fail-closed on well-formed lines (the `(\d+) ` consumes the space before an adjacent `missing=`), but accepts a forged line with filler, see below |
| M16 | C3 garbled default | `(None, 30)` → `(0, 0)` (:82) | KILLED | selftest `c3-garbled` |
| M17 | cases_missing | `if c not in src` → `if False and c not in src` (:150) | KILLED | crafted `cases_missing_empty`: pristine 11 misses, mutant `[]` |
| M18 | R21_CASES literal | `check("c1-killed"` → `check("c1-kiled"` (:31) | KILLED | crafted `cases_missing_r21base` on real base bytes (`git -C LANE show ef19d8e…:tools/round21-measure.py`): pristine `[]`, mutant `['check("c1-killed"']` |
| M19 | total arithmetic | drop `+ len(dropped)` (:142) | SURVIVED | see forged tree below |
| M20 | PASS label | `'true' if total == 0 else 'false'` → `'true'` (:145) | SURVIVED | see below |
| M21 | exit code | `return 0 if total == 0 else 1` → `return 0` (:146) | SURVIVED | see below |

15 KILLED / 6 SURVIVED. All 6 survivors sit in `main()`-inline clauses with zero selftest or probe reachability — a detector-coverage gap, not evidence the clauses are unimportant.

## Survivors — concrete forged trees the mutant passes and pristine rejects

- **M05** (:117). Forge: child commit at REV editing `tools/registry.json`, setting `"status": "superseded"` on any base-active row (49 rows frozen in `base-active.json`, e.g. `assemble-round16-selftest`; receipts/`base-active-facts.json`). Pristine: `dropped=['assemble-round16-selftest']` → total ≥ 1 → `C1_R52_PASS=false`. Mutant: `dropped=[]` → with all other components green, total=0 → `true`, exit 0.
- **M06** (:116). Same forged tree (demote a base-active row to superseded). Pristine active-set excludes it → dropped ≥ 1; mutant's truthy filter keeps it "active" → dropped=0 → passes.
- **M14** (:123). Forge: child commit replacing `.ufo/evidence/round-51/c3/measure.py` with a one-line stub `print('C3_R51: tools=10 rows=10 covered=10 missing=0 total=0 C3_R51_PASS=true')` (stub sha256 ≠ frozen `C3_SHA`; receipts/`m14-forged-stub.txt`). Pristine: digest mismatch → counter never executed → `c3_out=''` → `parse_c3('') == (None, 30)` (proven by selftest case `c3-garbled`) → total ≥ 30 → false. Mutant: runs the attacker's stub → its line parses `(10, 0)` (probe `c3_forged_stub`) → c3_total=0 → passes.
- **M19** (:142). M05's forged tree again: pristine total=1 (`dropped` term) → false; mutant omits `len(dropped)` → total=0 → true, exit 0.
- **M20** (:145). No forgery needed: at BASE (contract erratum records total=4) the mutant prints `… total=4 C1_R52_PASS=true` where pristine prints `false`; any consumer keying on the label accepts. Exit code stays 1 (dual signal: label lies, status does not).
- **M21** (:146). Same BASE run: mutant exits 0 while total=4; consumers keying on process status accept.

## M15 forged stdout (documented since the selftest kill masks its soundness hole)

Line `C3_R51: tools=10 rows=10 covered=10 q missing=0 total=7 C3_R51_PASS=false` (filler `q` gives `missing=` a leading space): pristine `parse_c3 → (10, 7)` (rejects total=7), M15 → `(10, 0)` (accepts) — receipts/`m15-forged-line.txt`.

## Pristine holes observed while probing (coverage findings, not contract changes)

1. `parse_c3` (:80-82) ignores the `C3_R51_PASS` token and covered/total consistency: `C3_R51: … covered=29 missing=1 total=0 C3_R51_PASS=false` parses `(29, 0)` → c3_total=0 → passes while the embedded tool verdict is false (receipts/`pristine-observations.txt` O1).
2. mte needle check is list membership (:66): a row carrying the required `10/10` needle plus the stale `9/9` needle passes `mte_row_ok` (O2).
3. `leg_count` returns `None` when `LEG_TABLE` is absent (:51) → `want` becomes `legs_conforming=None/None` (:64); a REV tree deleting `LEG_TABLE` and setting the row needle to that literal string satisfies `mte_row_ok` (O3, shown with status/kind/argv/exit in place) — end-to-end it would also need the frozen registry-check run to hold for that row, which a tree author controls. [INFERENCE on the end-to-end acceptance; the `mte_row_ok` acceptance is probe-proven.]

## Commands

- Detector: `python3 -I .ufo/evidence/round-52/c1/measure.py --selftest`
- Probes/diffs/receipts: generated per receipts/`results.json` (battery and per-mutant divergent probes recorded there); diffs via `diff -u` pristine vs each mutant copy.
- Restoration: `sha256sum .ufo/evidence/round-52/c1/measure.py` before and after (identical); `git -C <lane> status --porcelain -- .ufo/evidence/round-52/c1/` empty.

## Summary

- 21 one-edit mutants against the frozen C1 counter, all 11 pre-registered clauses covered; 15 KILLED, 6 SURVIVED.
- Killed by selftest: M01 M02 M04 M07 M11 M13 M15 M16 (9-case selftest is genuinely load-bearing).
- Killed only by crafted probes (selftest-blind): M03 M08 M09 M10 M12 M17 M18 — selftest has no kind/exit/argv-no-check/cases_missing coverage.
- Survivors M05 M06 M19 (base-active drop clause family) and M14 (C3 digest gate): no detector reaches `main()`-inline logic; forged trees documented above.
- Survivors M20/M21 (label/exit): single-token edits make the printed verdict or exit status lie; no selftest case guards them.
- Pristine holes (findings, not changes): parse_c3 ignores PASS token; needle list may carry stale 9/9 alongside K/K; LEG_TABLE-absent → forgeable `None/None` needle.
- Lane untouched: sha256 `3edfdb87…` before == after; pristine selftest 9/9 re-verified after all work; zero registry-check executions.
- Receipts: this directory `receipts/` (results.json, 21 selftest outputs, restored-check, hashes, forged-stub/forged-line, pristine-observations, base-active-facts); diffs `M01…M21-*.diff`.

Report: .ufo/waves/round-52/w1/T52W1MutC1.md
