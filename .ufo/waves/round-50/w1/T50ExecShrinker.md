# T50ExecShrinker — F6 fixture shrinker (round-50 C2)

Seat: T50ExecShrinker (leaf). Item: build the F6 fixture shrinker for
`tools/staged-id-guard.py` — delta debugging to a 1-minimal killing sub-case, with its cost stated
in guard runs. Deliverable: `.ufo/waves/round-50/w1/T50ExecShrinker.shrink-case.py` (632 lines,
28848 bytes, sha256 `1ac31ae58d807df76d632d5eb18b06c2e62eae0428fc1fb3b2dc3f01ebb3526f`), for the L1 to
copy byte-exact to `tools/shrink-case.py`.

Nothing in the lane checkout, the fleet repo, `merge/tameshi` or the Git index was touched; no
`/home/vgpnk/.local/state/` path was read; no mutant name or edit from the round-50 control receipts
was quoted. No tool was installed (pacman is paused host-wide and nothing here needed an install).

## What the tool does

Interface exactly as frozen (`contract.json` `claims.C2.shrinker_interface`):
`python3 -I tools/shrink-case.py --pristine P --mutant M --case CASE.json --out OUT.json` and
`--selftest`. `OUT = {case: {registry, staged, map}, runs, units_before, units_after}`.

- **Units** (`T50ExecShrinker.shrink-case.py:63` `unit_count`): registry lines + staged lines +
  entries of `map['map']` when that is an object — the counter's own formula
  (`measure.py` `units()`), recomputed rather than trusted from the input.
- **Kill** (`:174` `Shrinker.kills`): the round-49 generator's oracle, imported from
  `pbt-staged-id.py` beside the tool (`:217` `load_generator`), passes on the pristine guard and
  fails on the mutant. Mutant first, pristine only if the mutant violated — the counter's order.
- **Search** (`:100` `ddmin`): Zeller & Hildebrandt ddmin — drop chunks at granularity n, then the
  complement, then refine to single units — followed by a single-unit pass to a fixpoint that also
  tries the empty case (`:129-138`). The fixpoint is what makes 1-minimality a property of this
  loop, not a theorem about the chunk search above it; the tool never keeps a candidate it has not
  seen violate, which is the round-29 F6 failure mode (`corpus/knowledge/survivor-fixture-
  minimization.md`, "ddmin made 171 oracle tests and kept nothing").
- **Sub-case** (`:193` `build`): lines kept in file order, map entries a subset, every other map
  field copied unchanged — so the counter's `is_subcase` holds by construction, not by luck.
- **Cost** (`:162` `matches`): one increment per real `run_guard` call, and a verdict cache keyed by
  case content (`:69` `case_key`), so no case is run twice and `runs` equals the instrumented
  `const counter's .runs` count. `units_before`/`units_after` are this tool's counts of the input
  and of the case it returns.
- **Determinism / stdlib / errors**: no randomness, no clock, stdlib only, `exit 2` + stderr reason
  for a bad argument, an unreadable/invalid file, a missing generator, or a case that carries no
  kill (`:247` `run_from_arguments`, `:609` `main`). Verified by command below.

One trap fixed during the work, worth knowing: the generator runs each guard with `cwd` set to its
own case directory, so a *relative* `--pristine/--mutant` path resolves against the wrong directory
and every run looks like a failure. `:250` absolutises both paths; observed before the fix as
`shrink-case: the case carries no kill` on a case that the same generator judges a kill.

## Evidence (all commands run here; receipts copied into w1)

Scratch: `/fast/scratch/hyaku/tameshi-r50/T50ExecShrinker/` (mirror `tools/` + `.ufo/…/panel.json`),
one clone, deleted at the end.

1. **Selftest, both shapes, exit 0** — receipt `w1/T50ExecShrinker.selftest.txt`.
   `cd $S/mirror/tools && python3 -I shrink-case.py --selftest` → 21 checks, `failed=0`, exit 0:
   *core* legs (sentinel predicate → its one unit; the same verdict never asked twice; 1-minimality
   of the result; size-floor predicate → a 1-minimal three-unit set; unsatisfiable → None;
   always-true → empty set; empty start), a *CLI end to end on a stub guard pair with a stub oracle*
   (sub-case, kill, 1-minimality, unit counts, `runs` == logged), and the *M02 leg on the real
   guard*: the panel M02 edit `ROW_RE = re.compile(r'^ {0,3}\|` → `r'^\|'`
   (`T50ExecShrinker.shrink-case.py:44`, cross-checked against
   `.ufo/evidence/round-49/c2/panel.json` M02 when the panel is reachable) applied to a guard copy,
   shrunk 7 → 1 units in 7 runs, verification by the real generator's oracle, `runs` == logged. In the
   counter's tooldir shape (tool + generator only) the M02 leg prints
   `skip (no staged-id-guard.py beside this tool)` and the selftest still exits 0 with
   `cases=14 failed=0` — receipt, second block.
2. **All 12 public round-49 mutants** — receipt `w1/T50ExecShrinker.public-runs.json`, harness
   `w1/T50ExecShrinker.panel-harness.py`. For each mutant: the edit applied to a guard copy, the
   counterexample found with
   `python3 -I tools/pbt-staged-id.py --guard <mutant> --seed 4949 --cases 400 --dump F`, guards
   instrumented with the counter's own run logger, shrinker run, result judged by the generator's
   oracle. **12/12 ok** on every flag (`exit0 valid subset kills minimal cost reduced`), units
   **100 → 24**, `runs` 188 total (all equal to the logged invocations), 17.1 s wall. Per mutant
   (units before→after, runs): M01 8→1/9, M02 8→1/9, M03 7→1/7, M04 11→3/33, M05 8→3/27,
   M06 8→3/27, M07 8→2/18, M08 8→3/17, M09 8→2/8, M10 7→1/7, M11 10→2/8, M12 9→2/18. Worst cost
   33 runs / 1.1 s against the counter's 900 s per-mutant budget.
3. **The frozen counter's own `measure()` on a scratch fixture lane** (probe, never a verdict) —
   receipt `w1/T50ExecShrinker.counter-probe.log`, driver
   `w1/T50ExecShrinker.counter-probe.py`. Substitutions, named: lane = a scratch git repo
   (`git init` in scratch, `git -C "$D" rev-parse --show-toplevel` == that dir, base = its first
   commit, rev = its second) holding the pinned guard bytes, the pinned generator bytes, this
   shrinker, and *fixture* F6 records (README `held (round 50)` line, `S001 … mined 2026-10-26`
   row, `corpus/knowledge/shrink-case.md`); `gen_lane` = the real lane so the generator is read at
   `7d3d977f`; hidden panel = four mutants invented here (ids X01–X04, recorded in that receipt),
   because the real hidden panel is outside this seat's custody. Observed:
   `C2_R50: … mutants=16 ok=16 units_before=133 units_after=28 … records_bad=0 selftest_bad=0
   total=0 C2_R50_PASS=true`, every per-mutant line `OK` with `minimal=1 cost=1`, and
   `SELFTEST exit=0 last=SHRINK_SELFTEST: cases=14 failed=0` from the counter's own selftest
   invocation in its tooldir. The public panel digest it checked is the frozen pin
   `d6dd2cf3…`; the guard digest `03a796c5…` and generator digest `0cbee392…` are the pins in
   `measure.py`.
4. **The counter's own selftest** (probe): `python3 -I .ufo/evidence/round-50/c2/measure.py
   --selftest --lane <lane> --work <scratch>/ctl` → `C2_R50_SELFTEST: cases=9 failed=0`, exit 0,
   including `reference shrinker passes`. Its referee harness is sane; my tool's bar is that same
   judge plus the corpus records, which are not this seat's files.
5. **Determinism and paths**: three consecutive runs on the M04 case gave the identical output bytes
   (`sha256sum det1.json det2.json det3.json out.json` → all
   `7906cda450fb1fb245454706b107e2b31748ed82e55ce2c074be72496f0bb9de`), including with *relative*
   `--pristine/--mutant/--case` arguments.
6. **Sub-case edge that the counter checks and a naive shrinker breaks**: a case with an extra map
   field (`map.note = "keep-me"`) shrank 11 → 3 units and returned
   `map = {'note': 'keep-me', 'map': {'S015': 'S005'}}` — other map fields unchanged. A 54-unit case
   (padding + 3 extra map entries) shrank to a 3-unit 1-minimal kill in 53 runs / 1.6 s, verified by
   the generator (kill holds, no single removal keeps it).
7. **Error paths, all exit 2 with a stderr reason, no traceback**: no arguments
   (`missing --pristine, --mutant, --case, --out`), missing case file, non-JSON case, wrong case
   shape (`{"registry": 3}`), unreadable pristine guard, generator absent beside the tool, and a case
   that does not kill (`the case carries no kill: …`).
8. **Lane untouched**: `git -C <lane> status --porcelain` lists only untracked `.ufo/…` paths of
   other seats; `sha256sum tools/staged-id-guard.py tools/pbt-staged-id.py` still
   `03a796c5…`/`0cbee392…`, so the no-harm scope `{A tools/shrink-case.py, M tools/pbt-staged-id.py}`
   is met by adding one file and changing nothing.

## Risks and what this seat cannot attest

- **The hidden panel is unseen.** The eight hidden mutants come from the same thirteen recipes, so
  their counterexamples have the same shape (public cases: 7–11 units); observed worst cost is 33
  runs and ddmin is bounded by O(units²) distinct cases, far inside the 900 s budget. I cannot
  attest the hidden 8 — that is the L1's deciding run.
- **ddmin returns *a* 1-minimal sub-case, not the smallest.** On a padded variant of the M04 case it
  landed on a different 1-minimal result (3 units, empty map) than on the unpadded case (3 units,
  map entry kept); both are verified kills from which no single unit can be removed. That is the
  documented limit of the method, not a defect.
- **A mutant that differs on every input shrinks to nothing**: two of my substitute mutants (X01,
  X04 — a field-label and a floor off-by-one that change on any case) reduced to 0 units, which is
  honestly 1-minimal (there is no unit to remove) but says nothing about which unit matters. If the
  hidden panel held such a mutant the reduction would still pass; it just would not be informative.
- **Copy must be byte-exact and placed beside the generator.** The counter runs
  `git show REV:tools/shrink-case.py` inside a tooldir with `pbt-staged-id.py`; a copy that is not
  committed at REV, or a `tools/pbt-staged-id.py` edit, makes the tool exit 2 (or trips
  `gen_pin`). My deliverable's sha256 is recorded above and in
  `w1/T50ExecShrinker.public-runs.json`.
- **Not my files**: the F6 records the claim needs (`corpus/README.md` `held (round 50)` line and a
  new knowledge entry citing a `mined` SOURCES row opened 2026-10-26) belong to the L1; the probe
  above shows the counter's `records()` terms turn green with that record text present.
- I did not decide, judge or score the claim, and did not run the counter as a verdict.

## Summary

- Delivered `.ufo/waves/round-50/w1/T50ExecShrinker.shrink-case.py` (sha256 `1ac31ae5…`): ddmin to
  a 1-minimal killing sub-case over registry lines, staged lines and `map['map']` entries, honest
  run cost, verdict cache, deterministic, stdlib only, exit 2 with a reason on bad input.
- `--selftest` exits 0 in both shapes (21 checks with the guard beside it, 14 without), including a
  real M02 end-to-end leg with cost checked against instrumented invocations.
- All 12 public round-49 mutants: every counter flag green, units 100 → 24, 188 runs all matching
  the logged invocations, 17.1 s total, worst case 33 runs.
- Frozen `measure()` on a scratch fixture lane with my tool: `mutants=16 ok=16 units 133 → 28
  total=0 C2_R50_PASS=true` (probe; substitute 4-mutant "hidden" panel, fixture F6 records).
- Deterministic output bytes across repeats and with relative paths; 54-unit case 53 runs / 1.6 s.
- Limits stated: ddmin gives *a* 1-minimal case, the hidden 8 are unseen, all-differing mutants
  shrink to 0 units, and the F6 corpus records are the L1's files.
