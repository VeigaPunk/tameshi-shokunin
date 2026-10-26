# T50W2ExecC2Probe — non-deciding probe of the frozen C2 counter at the candidate

Seat: `T50W2ExecC2Probe` (executor, leaf). Item: run the frozen C2 counter at
`80ea77e99e239982ab0b93e416645ef2359725d3` in a scratch clone with the public round-49 panel and a
**synthetic** hidden panel built by this seat, report every MUTANT line and the records/selftest terms.
This is a probe, never a verdict; the deciding run is the L1's.

- Lane checkout was read-only: every lane read used `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:<path>` or the scratch clone. No lane file, index or jj state was written.
- Scratch root `S=/fast/scratch/hyaku/tameshi-r50/T50W2ExecC2Probe` (deleted before yield; nothing citable lives there).
- One clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane"` then `git -C "$S/lane" checkout -q 80ea77e99e239982ab0b93e416645ef2359725d3`; `git -C "$S/lane" rev-parse --show-toplevel` printed `$S/lane` and `rev-parse HEAD` printed `80ea77e99e239982ab0b93e416645ef2359725d3`.
- Counter bytes are the candidate's own: `git -C "$S/lane" show 80ea77e9:.ufo/evidence/round-50/c2/measure.py` → sha256 `c3da7e59abf279db2ebf165d1a8d8298295ca234cd83b49027b9cb0b1823dfe3`, matching the run's `self=c3da7e59abf2`.
- No tool installs or upgrades were needed (python3/git only); no pacman transaction attempted.

## A. Frozen counter, unmodified bytes (expected `panel_invalid=1`)

Command (from `$S`):

```
TMPDIR="$S" python3 -I measure-frozen.py \
  --lane "$S/lane" --rev HEAD --work "$S/w-frozen" \
  --panel "$S/lane/.ufo/evidence/round-49/c2/panel.json" --hidden "$S/hidden.json"
```

Public panel digest at the clone is `d6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1`
(`sha256sum "$S/lane/.ufo/evidence/round-49/c2/panel.json"`), equal to `PUBLIC_SHA256`
(`.ufo/evidence/round-50/c2/measure.py:56`). The synthetic hidden panel digest is
`c8b8223460f09fd3d31609b5349b1bf5fb3d4e0387e42bd4e24551ec8a22033c`, not `HIDDEN_SHA256`
(`measure.py:57`), so the digest branch at `measure.py:215-217` counts it and the hidden panel is
excluded rather than scored.

Every MUTANT line, verbatim from `T50W2ExecC2Probe.frozen.stdout`:

```
SELFTEST exit=0 last=SHRINK_SELFTEST: cases=14 failed=0
MUTANT M01 panel=public exit=0 units=8->1 runs=9 logged=9 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M02 panel=public exit=0 units=8->1 runs=9 logged=9 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M03 panel=public exit=0 units=7->1 runs=7 logged=7 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M04 panel=public exit=0 units=11->3 runs=33 logged=33 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M05 panel=public exit=0 units=8->3 runs=27 logged=27 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M06 panel=public exit=0 units=8->3 runs=27 logged=27 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M07 panel=public exit=0 units=8->2 runs=18 logged=18 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M08 panel=public exit=0 units=8->3 runs=17 logged=17 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M09 panel=public exit=0 units=8->2 runs=8 logged=8 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M10 panel=public exit=0 units=7->1 runs=7 logged=7 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M11 panel=public exit=0 units=10->2 runs=8 logged=8 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M12 panel=public exit=0 units=9->2 runs=18 logged=18 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
C2_R50: self=c3da7e59abf2 rev=80ea77e99e239982ab0b93e416645ef2359725d3 mutants=12 ok=12 units_before=100 units_after=24 entry=1 readme_f6=1 shrinker_absent=0 gen_pin=0 guard_pin=0 panel_invalid=1 unfound=0 ok_short=0 no_reduction=0 records_bad=0 selftest_bad=0 total=1 C2_R50_PASS=false
EXIT=1
```

Observed: 12/12 public mutants OK on every flag (`exit0 valid subset kills minimal cost reduced`), the
cost term honest on all 12 (`runs == logged`), aggregate 100 → 24 units, `records_bad=0`,
`selftest_bad=0`; `total=1` is exactly the synthetic-digest `panel_invalid` term, so the run exits 1
with `C2_R50_PASS=false`. No other term is non-zero.

## B. Synthetic hidden panel (built by this seat)

Built from the candidate guard (`80ea77e9:tools/staged-id-guard.py`, sha256
`03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`, equal to `GUARD_SHA256` at
`measure.py:53`), each mutant a single `old`→`new` edit whose `old` occurs exactly once
(`src.count(old)==1` checked per mutant), and each verified found by the **frozen** round-49 generator
(`git -C "$S/lane" show 7d3d977f…:tools/pbt-staged-id.py`, sha256
`0cbee392…bc01f05` = `GEN_SHA256`) at seed 4949, 400 cases. Receipt:
`T50W2ExecC2Probe.generator-finds.txt`, verbatim VIOLATION lines:

```
H01 row-indent-5 count(old)=1 gen_exit=1
  VIOLATION index=20 field staged_max: guard 'S007', oracle 'S000'
H02 column0-widened count(old)=1 gen_exit=1
  VIOLATION index=6 field column0_collisions: guard ['S003'], oracle []
H03 safe-floor-plus-two count(old)=1 gen_exit=1
  VIOLATION index=0 field safe_floor: guard 'S024', oracle 'S023'
H05a prose-as-document count(old)=1 gen_exit=1
  VIOLATION index=0 exit 0, oracle expects 1
H05b case-sensitive-documents count(old)=1 gen_exit=1
  VIOLATION index=21 field held: guard {}, oracle {'S018': 'S005'}
H06 column0-miss-inverted count(old)=1 gen_exit=1
  VIOLATION index=0 field column0_miss: guard [], oracle ['S022']
```

Panel bytes: `T50W2ExecC2Probe.synthetic-hidden-panel.json` (schema
`tameshi-r50-synthetic-hidden-probe-v1`, note field says it is not the custodied panel).
A seventh candidate was built and **discarded** because the frozen generator did not find it:
`document_key` `len(head) > 8` → `len(head) > 7` returned
`PBT_STAGED_ID: cases=400 violations=0 counterexample=none` (exit 0) — so panel membership is decided by
the finder, not by hand.

## C. Same counter with only the hidden pin changed (probe, not the frozen run)

To exercise the shrinker on the six synthetic mutants, a scratch copy `measure-probe.py` was derived by
changing exactly the `HIDDEN_SHA256` line:

```
sed "s/^HIDDEN_SHA256 = .*/HIDDEN_SHA256 = '<synthetic digest>'/" measure-frozen.py > measure-probe.py
diff <(grep -v '^HIDDEN_SHA256' measure-frozen.py) <(grep -v '^HIDDEN_SHA256' measure-probe.py)   # no output
sha256sum measure-probe.py   # 3ee21411e73b9fe13c789ad0d32112db05bb1e5096f68e1036bdbd7cfd3876ba
```

Command: same as A with `measure-probe.py` and `--work "$S/w-probe"`. Every MUTANT line, verbatim from
`T50W2ExecC2Probe.probe-modulated-pin.stdout` (public 12 identical to A; the six synthetic lines are the
new information):

```
SELFTEST exit=0 last=SHRINK_SELFTEST: cases=14 failed=0
MUTANT M01 panel=public exit=0 units=8->1 runs=9 logged=9 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M02 panel=public exit=0 units=8->1 runs=9 logged=9 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M03 panel=public exit=0 units=7->1 runs=7 logged=7 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M04 panel=public exit=0 units=11->3 runs=33 logged=33 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M05 panel=public exit=0 units=8->3 runs=27 logged=27 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M06 panel=public exit=0 units=8->3 runs=27 logged=27 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M07 panel=public exit=0 units=8->2 runs=18 logged=18 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M08 panel=public exit=0 units=8->3 runs=17 logged=17 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M09 panel=public exit=0 units=8->2 runs=8 logged=8 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M10 panel=public exit=0 units=7->1 runs=7 logged=7 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M11 panel=public exit=0 units=10->2 runs=8 logged=8 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M12 panel=public exit=0 units=9->2 runs=18 logged=18 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT H01 panel=hidden exit=0 units=8->1 runs=9 logged=9 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT H02 panel=hidden exit=0 units=8->2 runs=16 logged=16 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT H03 panel=hidden exit=0 units=8->0 runs=10 logged=10 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT H05a panel=hidden exit=0 units=8->2 runs=18 logged=18 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT H05b panel=hidden exit=0 units=7->3 runs=14 logged=14 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT H06 panel=hidden exit=0 units=8->2 runs=18 logged=18 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
C2_R50: self=3ee21411e73b rev=80ea77e99e239982ab0b93e416645ef2359725d3 mutants=18 ok=18 units_before=147 units_after=34 entry=1 readme_f6=1 shrinker_absent=0 gen_pin=0 guard_pin=0 panel_invalid=0 unfound=0 ok_short=0 no_reduction=0 records_bad=0 selftest_bad=0 total=0 C2_R50_PASS=true
EXIT=0
```

Observed: 18/18 OK, aggregate 147 → 34 units, `runs == logged` on all 18, `panel_invalid=0`. This is a
probe of the shrinker against six mutants the seat built itself; it is not a score on the custodied
hidden panel and not a claim decision.

## D. Records terms (independently of the run)

`readme_f6=1` and `entry=1` reproduce, checked directly by importing the candidate counter's own
`records()` on the clone:

```
python3 -c "import importlib.util; spec=importlib.util.spec_from_file_location('m','measure-frozen.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print(m.records('lane','80ea77e99e239982ab0b93e416645ef2359725d3','e3729de862f73ae080d98fcf522a7081ce16e40a'))"
# {'readme_f6': True, 'entry': True}
```

What each term rests on (file:line at the candidate):

- `corpus/README.md:608` — `F6 (fixture minimization for survivors): open → **held (round 50)** for the method on killing cases … conditioned on the round-50 deciding receipt …` (`readme_f6`, `measure.py:326-330`). Note `corpus/README.md:83` still shows the old frontier-table row `| F6 | fixture minimization for survivors | S022, S023, S024 | open | …`; the counter's regex scans every line, so the `## Round 50` line is the one that satisfies it.
- `corpus/knowledge/delta-debugging-minimization-contract.md:1` and `:5` — `source: S271 — …` / `ground: F6 (fixture minimization for survivors)`; the file is new since base (`git -C "$S/lane" diff --name-only --diff-filter=A e3729de8… 80ea77e9… -- corpus/knowledge` lists it and `fixture-shrinking-pilot.md`).
- `corpus/SOURCES.md:146` — the `S271` row whose cells carry `mined | 2026-10-26` (`measure.py:350-352` reads cells[7]/cells[8] and `OPENED='2026-10-26'` at `measure.py:61`). `corpus/knowledge/fixture-shrinking-pilot.md:1` also names S271.

## E. Shrinker selftest — two deployment shapes

1. **As the counter runs it** (`measure.py:219-240` copies only `shrink-case.py` and `pbt-staged-id.py` into `work/tool`): `SELFTEST exit=0 last=SHRINK_SELFTEST: cases=14 failed=0`. In that layout `staged-id-guard.py` is absent, so the M02 leg prints `skip (no staged-id-guard.py beside this tool)` — the strongest selftest leg is skipped in the counter's own deployment.
2. **Full layout** (guard and round-49 panel staged beside the tool, as the tool's own repository has it), receipt `T50W2ExecC2Probe.shrinker-selftest-full.stdout`:

```
cd "$S/toolA/tools"   # shrink-case.py, pbt-staged-id.py, staged-id-guard.py copied from the clone
                      # panel copied to $S/toolA/.ufo/evidence/round-49/c2/panel.json
TMPDIR="$S" python3 -I shrink-case.py --selftest
# SELFTEST M02: the embedded edit is the panel M02 edit         ok
# SELFTEST M02: the shrink exits 0 on the public mutant         ok
# SELFTEST M02: the mutant violates the oracle on the input case ok
# SELFTEST M02: the result is a sub-case that still kills       ok
# SELFTEST M02: the result is 1-minimal                         ok
# SELFTEST M02: the unit counts are honest                      ok
# SELFTEST M02: the run count equals the logged invocations     ok
# SHRINK_SELFTEST: cases=21 failed=0     (rc=0)
```

So the selftest passes in both shapes; shape 1 simply exercises 14 of its 21 cases.

## Observations and limits (probe, not verdict)

- **`panel_invalid` is a pin term, not a shrinker result.** The frozen counter scores a panel only when `sha256(file)` equals its pinned digest (`measure.py:208-218`); an unverified panel is excluded. The synthetic panel therefore cannot be graded by the frozen bytes, and the frozen run's `total=1 / C2_R50_PASS=false` is the pin working, not a finding against the shrinker. The seat's modulated-pin copy in §C exists only to obtain MUTANT lines for its own six mutants.
- **Verification oracle vs import oracle.** The shrinker imports the REV generator placed beside it (`shrink-case.py:217-236`, `load_generator`), while the counter's `Judge` verifies kills/minimality with the frozen generator (`measure.py:153-160`, `measure.py:289`, `measure.py:298-299`). On all 18 mutants the two agreed in the sense that `kills`, `minimal` and `cost` were green, and `runs == logged` in every line — the cost is the real instrumented invocation count, not a self-report.
- **A 1-minimal reduction can be an empty case.** `H03` (`safe_floor` +2) reduces 8 → 0 units and still kills: the mutant changes a constant field, so a case with no rows still separates oracle and guard. That is valid under the frozen definition (`subset`/`kills`/`minimal` all green, `units_after <= units_before`) but the reduced case names no row, so a reader learns only that the constant differs. Not a counter defect; a property of the predicate. The counter's aggregate reduction term is `after_sum < before_sum` (`measure.py:314`), met here 147 → 34.
- **M02 is skipped in the counter's tool dir** (§E.1). The panel loop does exercise the real guard/shrinker pair (all 12 public and all 6 synthetic lines), so this is a redundancy observation about the selftest, not a hole in the panel scoring.
- **Scope of this probe.** Six synthetic mutants at one seed (4949), 400 cases, one shrunk case each. It says nothing about the eight custodied hidden mutants, whose panel was not read (`/home/vgpnk/.local/state/` untouched; `control/c2-*.stdout` only ever consulted as ids H01..H08, and not at all here).

## Summary

- Frozen C2 counter at `80ea77e9` (clone, `--rev HEAD`) scores 12/12 public round-49 mutants OK with `runs==logged` throughout, records `readme_f6=1 entry=1`, selftest exit 0 (14 cases), and `total=1` solely from `panel_invalid=1` on the seat's synthetic hidden digest — `C2_R50_PASS=false`, exactly as expected for a non-custodied panel.
- A six-mutant synthetic hidden panel was built from single edits of `tools/staged-id-guard.py`; each is found by the frozen round-49 generator at seed 4949 (counterexample indices 20, 6, 0, 0, 21, 0), while a seventh candidate (`len(head) > 8` → `> 7`) survived all 400 cases and was discarded.
- With only `HIDDEN_SHA256` changed in a scratch copy (diff-verified), the shrinker scores 18/18 OK, 147 → 34 units, `panel_invalid=0` — the six synthetic mutants shrink to 1-minimal sub-cases at an honest logged cost.
- The shrinker's own selftest passes as the counter runs it (14 cases) and passes its full 21-case form, M02 real-guard leg included, when the guard and panel are staged beside the tool.
- Observation: `H03` (constant-field off-by-one) legitimately reduces to an empty case; the frozen 1-minimality definition permits it, and the aggregate reduction term still holds.
- No lane file, index or jj state was written; scratch was removed; receipts are in `.ufo/waves/round-50/w2/T50W2ExecC2Probe.*` (`frozen.stdout`, `probe-modulated-pin.stdout`, `synthetic-hidden-panel.json`, `generator-finds.txt`, `shrinker-selftest-full.stdout`).
