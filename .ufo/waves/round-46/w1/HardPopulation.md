seat: HardPopulation

item: selftest cases for the round-45 freshness counter's `population()` that kill the three declared survivors F04 (population needs a URL), F14 (status exactly `mined`) and F15 (MAX_ID bound inclusive), changing no counter behaviour and killing no neutral mutant.

## Deliverable

`.ufo/waves/round-46/w1/HardPopulation.addition.py` — sha256 `68e03a51231b75b96b40c0175ff6236f34171e18623ca0635ec83a0f812459be`.

Top-level definitions (one `extra_*`, two `_xHardPopulation_*` helpers):

```
$ grep -n '^def ' .ufo/waves/round-46/w1/HardPopulation.addition.py
11:def _xHardPopulation_row(rid, source, status):
16:def _xHardPopulation_ids(probe_id, probe_source, probe_status):
23:def extra_HardPopulation():
$ grep -c '^def extra_' .ufo/waves/round-46/w1/HardPopulation.addition.py
1
```

`extra_HardPopulation()` returns `(cases, failed)` and prints one `PASS <case>` / `FAIL <case> got=... want=...` line per case.

## Before state (the survivors as declared)

```
$ cp .ufo/evidence/round-45/freshness/measure.py /tmp/tameshi-r46-HardPopulation/orig.py   # sha256 ba64041f49ffcf15bb0d881604a5fe3ccf9d24e56f72bef055035fbe3d27c6ed
$ python3 .ufo/evidence/round-46/hardening/try-mutants.py --group freshness --file /tmp/tameshi-r46-HardPopulation/orig.py --ids F04,F14,F15
PRISTINE pass VERDICT: PASS
MUTANT F04 mutant survived
MUTANT F14 mutant survived
MUTANT F15 mutant survived
exit=0
```

## Cases (smallest fixture per mutant)

Each case is two registry rows: control `S100` (`a — https://e.org/control`, status `mined`, id 100 <= MAX_ID), which every variant includes, plus one probe row that differs from that control in exactly the dimension under test. Assertion is on the exact sorted population id list, so a case cannot pass vacuously. All cases call the counter's own `parse_rows` / `population`; none reads the counter's bytes.

| id | case name | probe row | pristine population | mutant population |
|---|---|---|---|---|
| F04 | `F04_population_requires_url` | `S101`, source cell `a — this cell carries no link`, status `mined` | `['S100']` (no URL -> out) | `['S100', 'S101']` (URL test dropped) |
| F14 | `F14_population_status_exactly_mined` | `S101`, source cell with `https://e.org/rejected`, status `rejected` | `['S100']` (status != mined -> out) | `['S100', 'S101']` (`!= 'queued'` admits `rejected`) |
| F15 | `F15_population_id_bound_inclusive` | `S%03d % MAX_ID` = `S160`, source cell with `https://e.org/boundary`, status `mined` | `['S100', 'S160']` (160 <= 160 -> in) | `['S100']` (160 < 160 -> out) |

The probe id for F15 is derived from the module constant `MAX_ID`, not hardcoded: the case states the bound is inclusive, so it survives any future change of the constant.

Why the existing selftest did not already cover these: `T15_population_bounds` feeds `S001` (included), `S161` (id above MAX_ID), `S002` (status `queued`) and an unindented `S003`. It pins the id-above-bound side, one non-`mined` status that is exactly `queued` (so F14's `!= 'queued'` is indistinguishable), never `S160` itself (so F15's `<` is indistinguishable), and never a row whose only defect is a missing URL (so F04 is indistinguishable).

## Helper output after the addition

Assemble (deterministic — a second run produced the identical sha256):

```
$ python3 .ufo/evidence/round-46/hardening/assemble.py --group freshness \
    --add .ufo/waves/round-46/w1/HardPopulation.addition.py --out /tmp/tameshi-r46-HardPopulation/hard.py
wrote /tmp/tameshi-r46-HardPopulation/hard.py (1 additions)
sha256 hard.py = f3b64a8b36e3d12aa9144f756417337e2e29127ecf10f3d3f18d0422f8b01fd2
sha256 hard2.py (rerun) = f3b64a8b36e3d12aa9144f756417337e2e29127ecf10f3d3f18d0422f8b01fd2
```

Full declared sweep, my ids only present (no other seat's additions were combined here):

```
$ python3 .ufo/evidence/round-46/hardening/try-mutants.py --group freshness --file /tmp/tameshi-r46-HardPopulation/hard.py
PRISTINE pass VERDICT: PASS
MUTANT F01 mutant survived
MUTANT F02 mutant survived
MUTANT F03 mutant survived
MUTANT F04 mutant killed
MUTANT F05 mutant survived
MUTANT F06 mutant survived
MUTANT F07 mutant survived
MUTANT F08 mutant survived
MUTANT F09 mutant survived
MUTANT F10 mutant survived
MUTANT F11 mutant survived
MUTANT F12 mutant survived
MUTANT F13 mutant survived
MUTANT F14 mutant killed
MUTANT F15 mutant killed
MUTANT FN1 neutral survived
MUTANT FN2 neutral survived
MUTANT FN3 neutral survived
```

Pristine `pass`, my three `killed`, all three neutrals `survived`. The other ten survivors of the group are outside this seat's item and remain survivors in this one-addition assembly; they are killed or not by the other seats' additions.

Isolation per mutant (each mutant applied alone to `hard.py`, selftest run, `FAIL`/tally lines only):

```
F04 mutant exit=1
   FAIL F04_population_requires_url got=['S100', 'S101'] want=['S100'] (F04)
   C1_R45_SELFTEST: cases=22 failed=1
F14 mutant exit=1
   FAIL F14_population_status_exactly_mined got=['S100', 'S101'] want=['S100'] (F14)
   C1_R45_SELFTEST: cases=22 failed=1
F15 mutant exit=1
   FAIL F15_population_id_bound_inclusive got=['S100'] want=['S100', 'S160'] (F15)
   C1_R45_SELFTEST: cases=22 failed=1
FN1 neutral exit=0
   C1_R45_SELFTEST: cases=22 failed=0
FN2 neutral exit=0
   C1_R45_SELFTEST: cases=22 failed=0
FN3 neutral exit=0
   C1_R45_SELFTEST: cases=22 failed=0
```

Exactly one case fails per mutant and it is the case named after that mutant: no case is killed for a reason other than its own mutant.

Selftest tally of the assembled file:

```
$ python3 /tmp/tameshi-r46-HardPopulation/hard.py --selftest
... T1..T19 PASS ...
PASS F04_population_requires_url got=['S100'] want=['S100'] (F04)
PASS F14_population_status_exactly_mined got=['S100'] want=['S100'] (F14)
PASS F15_population_id_bound_inclusive got=['S100', 'S160'] want=['S100', 'S160'] (F15)
C1_R45_SELFTEST: cases=22 failed=0
VERDICT: PASS
exit=0
```

Baseline before the addition was `C1_R45_SELFTEST: cases=19 failed=0` / `VERDICT: PASS`; the three added cases raise the tally to 22.

## Behaviour preservation

`diff -u orig.py hard.py` contains exactly three hunks, all attributable to `assemble.py` plus my block:

1. `SELF_PATH` repointed from `.ufo/evidence/round-45/freshness/measure.py` to `.ufo/evidence/round-46/hardening/freshness-counter.py` (the assembler's documented job; the hardened copy must be committed at that path by the L1).
2. the selftest tally line extended with `extra_cases` and the `extra_HardPopulation()` call;
3. my addition inserted before `def main():`.

`measure()`, `grade()`, `parse_rows()`, `population()`, `review_sets()`, `wave_seats()`, `check()`, `live()` and the CLI are byte-identical. My function is reachable only from `selftest()`, so `--lane/--rev` measurement output cannot change.

Neutral-mutant survival is the evidence that no case pins source bytes: `FN1` (appended comment), `FN2` (`13` spelled `0xD`) and `FN3` (trailing comment on `MAX_ID`) all survive, while all three behavioural mutants die.

## Unrun by this seat (L1-owned, deliberately not executed here)

- The deciding `mutate.py --lane LANE --rev REV --targets hardened` run and the `equivalence=1` check at data rev `ea25e0224fc81060414b27301c27bd1344669165`: that rev is outside this seat's allowed `--rev` set, and equivalence needs the hardened file committed at its `SELF_PATH`. Unrun.
- The committed hardened counter `.ufo/evidence/round-46/hardening/freshness-counter.py`: does not exist yet (the hardening dir holds only `assemble.py`, `build-manifest.py`, `mutants.json`, `mutate.py`, `try-mutants.py`); assembly and commit are the L1's. Unrun.
- Any `--rev 745a583181648cfc7f9c1b476cd1be7dc68f7433` / `--rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d` counter run: not needed for a population()-level case, and a seat run is never a verdict. Unrun.

## Bounds compliance

- Read-only on the lane checkout; the only files I wrote are `.ufo/waves/round-46/w1/HardPopulation.addition.py` and this report.
- All scratch under `/tmp/tameshi-r46-HardPopulation/` (`orig.py`, `hard.py`, `hard2.py`, `mut_*.py`, `probe.py`).
- No `git add/commit/stash/checkout/switch/reset/pull/push` in the lane, no mutating `jj` command, no fixture repo needed (the cases are pure `parse_rows`/`population` calls, so no scratch git repo was built).
- No writes under `/home/vgpnk/Projects/shokuknow`, no campaign tool there, no network fetch.
- No tool installs or upgrades were needed; nothing installed, no `pacman`.

## Risks

- None for the counter: the cases touch only `population()`, are pure, and run inside `--selftest` only.
- Scope note for the L1: F04's mutant makes the population strictly larger (a URL-less `mined` row enters, changing `len(pop)` and therefore `score`); F14's admits any status except `queued`; F15's drops `S160` itself. The three cases pin those three directions; no other population dimension is claimed.
