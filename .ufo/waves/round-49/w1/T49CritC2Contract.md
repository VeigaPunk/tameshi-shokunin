# T49CritC2Contract — C2 design falsifier (round 49, wave 1)

Seat: T49CritC2Contract. Item: falsify C2's *design* before data. No claim is decided here; every
line below is a probe result or a code reading, never a verdict.

Read (read-only, in this order): `.ufo/evidence/round-49/contract.json` (claims.C2),
`.ufo/evidence/round-49/c2/measure.py` (all 465 lines), `.ufo/evidence/round-49/control/c2-controls.sh`,
`.ufo/evidence/round-49/control/c2-fixed-gen.py`, `.ufo/evidence/round-49/deciding-run.sh`,
`.ufo/evidence/round-49/freeze.json`, `tools/staged-id-guard.py` (lines 1-200, 430-497),
`corpus/README.md:76-95`, `PROVINCE.md`. Not opened: `/home/vgpnk/.local/state/**`,
`c2-WITNESS.stdout`, `c2-CTL_FIX.stdout`, `c2-CTL_ABSENT.stdout` (item does not name them).

Ran (scratch only, nothing in the lane touched): a fixture repo `D` created as
`D=$(mktemp -d -p "$S") && git -C "$D" init -q` inside
`S=/fast/scratch/hyaku/tameshi-r49/T49CritC2Contract`, holding the guard at its frozen bytes
(`sha256sum` → `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`, matching
`contract.json:52`) plus two probe generators, committed (`85197d90`). `probe.py` imports the frozen
counter and calls `materialize` / `run_generator` / `write_mutant` / `run_guard` / `comparable` /
`case_classes` exactly as `measure()` does:

```
TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 python3 -B probe.py "$S/D" "$S"   # 60.7 s
TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 python3 -B probe2.py "$S/D" "$S"  # 74.9 s
```

Receipts copied into this directory: `T49CritC2Contract.probe.stdout`,
`T49CritC2Contract.probe2.stdout`, `T49CritC2Contract.gen-diff.py`,
`T49CritC2Contract.gen-pad.py`, `T49CritC2Contract.CHEAT-MARKER.txt`. Scratch dir deleted before
yield. No tool installed or upgraded (nothing needed; `python3` and `git` sufficed).

---

## C2-F1 (HIGH) — the mutant run hands the generator the pristine guard in its own cwd, so a generator with no property and no oracle passes every leg

`materialize()` writes the pristine guard to `<work>/tree/tools/staged-id-guard.py`
(`measure.py:250-258`), and `run_generator()` runs the generator with
`cwd=os.path.dirname(gen)` (`measure.py:219`) — that is the same `tree/tools` directory. The mutant
run (`measure.py:336`) reuses the same generator path, so during the mutant run the pristine guard
sits next to it at `./staged-id-guard.py` while `--guard` points at
`<work>/mut/<id>/staged-id-guard.py`.

Counterexample (`T49CritC2Contract.gen-diff.py`, a 3-shape generator with no property, no
expectation, no oracle): for each case it runs `--guard` and `./staged-id-guard.py` and reports a
violation on the first difference. Observed (`T49CritC2Contract.probe.stdout`):

```
PROBE gen_cwd_listing=['pbt-staged-id.py', 'staged-id-guard.py']
PROBE diffgen_on_pristine exit=0 cases=400 violations=0 dump=400
PROBE diffgen_on_mutant exit=1 last=PBT_STAGED_ID: cases=1 violations=1 counterexample=0 dump=1
PROBE marker: reference=<work>/tree/tools/staged-id-guard.py exists=True
PROBE counter_status_for_diffgen=confirmed
PROBE counter_status_for_diffgen_M02=confirmed (last=... cases=7 ... counterexample=6)
```

Two independent mutations (drop `cascade` from `refused`, drop the trailing-slash strip in
`normalise_document`) are both `confirmed` by the counter's own confirmation path
(`measure.py:330-345`). The generator satisfies `pristine_bad=0` and the dump/count contract; it
never consults an oracle, so `oracle_disagree` (C2-F4) never even applies to it.

This directly falsifies the contract's generator clause "checks each output with its own oracle
(never imports or execs the guard's code except through its CLI)" (`contract.json:53`): the counter
cannot observe that clause, and the *strongest* available cheat (differential against a reachable
reference) is strictly easier than writing properties.

Impacted axes: coverage (C2 label); F10 `held` (the "PBT method" is what is being held);
provenance (the label's name is not what it measures).

Smallest safe correction: give each generator run its own directory that contains only the file it
was handed — materialise the generator and the guard-under-test into `<work>/run-<tag>/` and pass
`cwd=<work>/run-<tag>` — so no second guard is reachable. The counter is frozen
(`freeze.json` sha `f4971d02…`), so this needs a `contract.json` amendment (`amendments: []`,
`contract.json:82`) before the deciding run; if the amendment is refused, the wave-2 seat must
carry a source-inspection receipt instead: the final `tools/pbt-staged-id.py` must contain no
`getcwd`/`dirname(__file__)`/`staged-id-guard`/`git`/absolute-path read, and must state its
properties in code.

## C2-F2 (HIGH) — nothing constrains the generator's filesystem access, and the hidden panel is readable from the lane at REV

`run_generator()` sets only `cwd` and `TMPDIR` (`measure.py:214-219`); the process keeps the full
environment and the whole filesystem. The deciding run pulls the panel *out of the lane's git
objects* (`deciding-run.sh:42`, `git show "$REV:$E/c2/panel.json"`), and the contract itself
commits the panel inside the lane at REV (`contract.json:57`: "committed at
.ufo/evidence/round-49/c2/panel.json ... before the deciding run"). The generator therefore has two
absolute, known paths at deciding time: the lane checkout
(`/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py`) and
`git -C <lane> show REV:.ufo/evidence/round-49/c2/panel.json`.

Not executed: reading the panel would void the generator claim and the bounds forbid it. It is
reachable by construction — no sandbox, no path restriction, no audit of the generator's reads.
So `why_hidden` ("the generator is built against the guard's documented contract, not tuned to the
mutants that score it", `contract.json:57`) is a property of the *author's* ignorance at authoring
time, not of the measurement. C2-F1 makes this worse: a panel-agnostic differential generator needs
no knowledge at all.

Impacted axes: coverage; provenance of `why_hidden`; F10 `held`.

Smallest safe correction: run the generator under a namespace that cannot see the lane
(`unshare`/`bwrap` with only `run-<tag>` bind-mounted), or — cheaper and honest — narrow the
contract wording to "the generator's independence is asserted by the author and checked by
inspection, not measured", and require the wave-2 inspection receipt named in C2-F1. Do not leave
the current wording, which reads as a measured property.

## C2-F3 (MEDIUM-HIGH) — the 12 classes / `class_min=10` is a presence count over a dump the generator controls, not a distribution check, and the dump need not be the cases the generator ran

The counter validates the dump only by type and by count/index
(`measure.py:196-215`, `measure.py:310-312`), then increments one counter per dump case
(`measure.py:314-328`) and compares to 10 (`measure.py:352`). Nothing deduplicates, nothing binds a
dump line to a case the generator actually analysed, and nothing requires the classes to be carried
by *distinguishing* cases.

Counterexample (`T49CritC2Contract.gen-pad.py`: 10 handcrafted shapes, dumped 400×, only 2 cases
actually run). Observed (`T49CritC2Contract.probe.stdout`):

```
PROBE padgen exit=0 last=PBT_STAGED_ID: cases=400 violations=0 counterexample=none dump=400
      indices_ok=True distinct=10
PROBE class_counts={"cascade":40,"collision":160,"held":40,"id_4_plus_digits":40,"indent_1_3":200,
      "indent_4_plus":40,"map":120,"map_inadmissible":80,"no_collision":80,"refusal":40,
      "unmapped":40,"url_form_variant":40}
PROBE classes_short=0 (counter formula: sum(counts<CLASS_MIN))
PROBE distinct_cases_carrying_floors=10
```

So `classes_short=0` is obtained with ten distinct cases repeated forty times each, from a
generator that ran two of them. Note also that `materialize()` copies only the one generator file
(`measure.py:250-266`), so a corpus cannot travel as a data file — embedding a fixed corpus in the
`.py` is the path of least resistance, which is exactly the CTL_FIX shape at larger size.

Impacted axes: coverage; the "12 frozen classes" claim in `contract.json:56`.

Smallest safe correction: (a) require the floors over *distinct* cases (dedupe on
`(registry, staged, map)`), and (b) require `len(dump) == cases_run == distinct`, so a dumped case
is a case that was run. Both are a few lines in `classes_short`, but need an amendment.

## C2-F4 (MEDIUM) — `oracle_disagree` measures the *guard*, not the generator's oracle, skips every map case, and is blind to `held`/`unmapped`/`cascade`/exit

`measure.py:314-326`: for each dump case the counter runs the **pristine guard**
(`run_guard(gp, …)`) and compares it to `measure.oracle`. The generator's oracle is never invoked
by the counter at all. The loop body is gated on `if c.get('map') is None:` (`measure.py:316`), so
no map case is ever checked; and the comparison is `collisions`, `registry_rows`, `staged_rows`
plus the exit-2 boundary only (`measure.py:317-323`), with `out[0] in (0, 1, 2)` tolerating exit 1
for any analysis case (`measure.py:319`).

Counterexample (`T49CritC2Contract.probe2.stdout`, measure's own formula applied to three mutants
whose output is wrong in exactly the unchecked places):

```
PROBE2 M03-exit-flip      oracle_disagree=0 cases_differing_from_pristine=200
PROBE2 M04-held-emptied   oracle_disagree=0 cases_differing_from_pristine=40
PROBE2 M05-cascade-emptied oracle_disagree=0 cases_differing_from_pristine=120
```

200/40/120 cases change behaviour and `oracle_disagree` stays 0. The predicate's sentence "agrees
with the counter's oracle on every analysis case" (`contract.json:48`) also has the wrong subject:
as implemented, the *guard* is checked, not the generator. The exit-1 tolerance is what papers over
the recorded documentation mismatch — `tools/staged-id-guard.py:38-39` documents exit 1 as
"the map is not admissible", while `tools/staged-id-guard.py:491-494` returns 1 for an analysis
refusal too (`contract.json:54` records this as "a documentation mismatch").

Impacted axes: coverage; the independence claim that makes a kill count meaningful.

Smallest safe correction: extend the oracle comparison to map cases and to
`held`/`unmapped`/`cascade`/`next_free`/`safe_floor`, and pin the exit code per verdict
(answered → 0, analysis refused → 1, map inadmissible → 1, setup → 2) so the tolerance is removed.
Requires an amendment; without one, say in the round report that `oracle_disagree` is a
three-field payload check.

## C2-F5 (MEDIUM) — `--generator-path` is accepted unconditionally and the label line never names the generator

`measure.py:433` defaults it to `GENERATOR`; `measure.py:458` passes it straight through; the label
line prints `generator=%s` with only `'present'`/`'absent'` (`measure.py:363-364`). The substitution
target is in-tree at REV: `c2-controls.sh:17` itself passes
`.ufo/evidence/round-49/control/c2-fixed-gen.py`, which `materialize()` will read from the lane
because it is committed there (`git ls-tree` at HEAD lists it).

Counterexample: a receipt from
`--generator-path .ufo/evidence/round-49/control/c2-fixed-gen.py` is indistinguishable, line for
line, from the contract command's receipt (`contract.json:51` has no `--generator-path`), so the
kill rule "exactly one deciding invocation at REV by deciding-run.sh" (`contract.json:60`) cannot
see a substituted generator. `deciding-run.sh:44` happens not to pass the flag — the hole is that
the counter cannot show it didn't.

Impacted axes: coverage; receipt integrity (identity of the measured artifact).

Smallest safe correction: print the generator path and its sha256 in the `C2_R49:` line, and reject
`--generator-path` unless a `--controls` flag is given (the controls harness is the only legitimate
caller).

## C2-F6 (MEDIUM) — gate 0 enforces that the control receipts exist, not that the controls passed

`deciding-run.sh:23-27` only does `git cat-file -e` and `merge-base --is-ancestor` for
`c1-controls.stdout`, `c1-controls.exit`, `c2-controls.stdout`, `c2-controls.exit`. The harness does
record a verdict (`c2-controls.sh:23-25` sets `rc=1` unless `C2_R49_PASS=false` for CTL_FIX and
`witness_confirmed=12`), and `c2-controls.exit` holds it — but nothing reads the value, so a
*failed* control run still lets the deciding run proceed.

This is load-bearing for C2 specifically: CTL_FIX is the only control that would catch a
fixture-replay generator (`contract.json:63`), and the WITNESS receipt is the only check that the
panel's mutants are non-equivalent. A CTL_FIX that reached the kill target would be recorded as a
receipt and then ignored.

Impacted axes: coverage; the controls' authority over the label.

Smallest safe correction: in gate 0, require `c2-controls.exit`/`c1-controls.exit` to be `0` at REV
and `c2-controls.stdout` to contain `C2_CONTROLS ok=true` (and the C1 analogue); refuse with exit 3
otherwise. One `case`/`[` line per file, no counter change.

## C2-F7 (LOW) — the records leg is lexical and does not check the source the claim names

`measure.py:277-287` accepts any `source: S###` in the entry's head block whose `SOURCES.md` row is
`mined` with `opened` = 2026-10-26 (`cells[7]`, `cells[8]`); nothing checks that the row is the
QuickCheck/Smallbone row the claim names (`contract.json:47`). `measure.py:288` accepts *any* line
of `corpus/README.md` carrying both `F10` and `held (round 49)`, while the F1/F2 precedent shape is
`held (round N) — \`knowledge/<entry>.md\`` (`corpus/README.md:78-79`) and F10's row currently
carries its own candidate sources (`corpus/README.md:87`).

Impacted axes: provenance; calibration of the frontier row.

Smallest safe correction: require the README status cell to match
`held (round 49) — \`knowledge/pbt-generator-pilot.md\`` and require at least one cited id to be one
of the rows the contract names.

---

## Attacked and held (not defects)

- **F10 `held` scope (item attack 5).** The README's own crossing bar is "no PBT fixture method →
  one generator against a named fixture gate" (`corpus/README.md:87`), and the gate is named and
  sha-pinned (`contract.json:52`). PROVINCE's two-lane rule binds "general" claims
  (`PROVINCE.md:14-15`); a frontier `held` is not Core (`PROVINCE.md:40-42`), so one lane-owned gate
  is inside the bar as written. Residual: `held` must not be worded as a transferable method — and
  the counter cannot see the wording (`measure.py:288`). Recommend the status cell read
  "held (round 49), one lane-owned gate".
- **The 12 class predicates themselves are correct** on the guard's real exit semantics: analysis
  refusal returns 1 (`tools/staged-id-guard.py:491-494`) and `map_inadmissible` requires a map, so
  `refusal` (exit 2) and `map_inadmissible` do not collide (`measure.py:142-148`). Only the
  *counting* is weak (C2-F3).
- **Panel validity is only `count(old) == 1`** (`measure.py:236`); non-equivalence is established
  outside the label by WITNESS (`contract.json:62-64`) — the right place for it, since an equivalent
  mutant would otherwise be an unkillable one.
- **`selftest_kills` is printed but not scored** (`measure.py:335`): correct — a mutant the guard's
  own suite already kills still has to be confirmed by the generator.
- **Pristine-leg binding is sound**: `cases == 400`, `violations == 0`, `len(dump) == 400` and
  `indices == range(400)` (`measure.py:310-312`) cannot be faked by a short run, only by a padded
  dump (C2-F3).

## Summary

- HIGH C2-F1: mutant runs execute the generator with the pristine guard in cwd
  (`measure.py:219,250-258`); a property-free differential generator is `confirmed` on 2/2 mutations
  and passes the pristine leg (probe receipts in this directory).
- HIGH C2-F2: no sandbox — the lane path and `REV:.ufo/evidence/round-49/c2/panel.json`
  (`deciding-run.sh:42`) are readable by the generator, so `why_hidden` is an authoring-time
  property, not a measured one.
- MED-HIGH C2-F3: class floors are per-dump-line counts with no distinctness and no run binding —
  10 distinct cases × 40 gives `classes_short=0` while the generator ran 2.
- MED C2-F4: `oracle_disagree` checks the guard, not the generator, skips map cases, and ignores
  `held`/`unmapped`/`cascade`/exit (0 disagreements across 200/40/120 differing cases).
- MED C2-F5: `--generator-path` is accepted unconditionally and the label prints only
  present/absent, so the receipt cannot name the measured generator.
- MED C2-F6: gate 0 checks control-receipt existence and ancestry, never their verdict
  (`deciding-run.sh:23-27`), so a failing CTL_FIX/WITNESS does not block the deciding run.
- LOW C2-F7: records leg is lexical — any mined 2026-10-26 row and any README line with
  `F10`+`held (round 49)`.
- F10 `held` is justified by the README's own crossing bar; it inherits C2-F1's weakness, so the
  label can be true of a generator that is not property-based.
