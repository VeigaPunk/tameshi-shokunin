# T49W2CritReadme — attack on the F10 frontier move at f181a961

Item: `corpus/README.md`'s F10 line(s) and coverage-map row(s) at candidate
`f181a961ae44061af486f600e5ea257d2baf78f8`; is `held (round 49)` justified under the
README's own rule; is the move conditioned on the deciding receipt; does it contradict
`PROVINCE.md`. Raw outputs: `T49W2CritReadme.receipts.txt` (this directory). Every line
number below is at `f181a961` unless another rev is named; command `git -C
/home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961:<path>` plus the selector
named per finding. No counter was run; no claim is decided here. No tools installed
(none needed).

## The surface under attack

- Frontier table row: `corpus/README.md:87` — `| F10 | PBT generators for gate fixtures |
  S018, S019, S020, S021 | open | no PBT fixture method → one generator against a named
  fixture gate |` — **byte-identical to base** (`git show 8ca67421:corpus/README.md |
  grep -n '^| F10'` prints the same line 87; `diff` of lines 60–100 base→candidate is
  empty). The table cell still reads `open`.
- Round-49 append: `corpus/README.md:593-599` (the file is 599 lines; the section is the
  last block). Line 599 carries the move: `F10 ... open → **held (round 49)** for its
  stated next move ... conditioned on the round-49 deciding receipt
  .ufo/evidence/round-49/after/c2.stdout printing C2_R49_PASS=true; if it does not, this
  line is void and an erratum below says so.`
- Coverage-map row: `corpus/README.md:597` — `knowledge/pbt-generator-pilot.md | ... |
  S269, S270 |` (knowledge file and row land the same round; QUALITY 7 satisfied).
- Entry: `corpus/knowledge/pbt-generator-pilot.md:1-5` (`source: S269`, `source: S270`,
  `verified-at:`, `recheck:`, `ground: F10`).

## Rule check — the README's own two rules

The README states the held rule twice:

1. `corpus/README.md:72-74` — "A ground moves to `held` only through an admitted
   `knowledge/` entry with a `source:` header citing a `mined` `SOURCES.md` row."
2. `corpus/README.md:120-121` (status-correction section) — "A ground reads `held` only
   when its next move in the table is measured."

Structural half (rule 1) holds at the candidate: the entry opens with two `source:`
headers (`pbt-generator-pilot.md:1-2`); both rows exist, are `mined`, and were opened
this round — `corpus/SOURCES.md:144-145`, parsed: 11 cells, `c7=mined c8=2026-10-26`
for S269 and S270 (the frozen counter enforces exactly this: `c2/measure.py:283-285`);
row admission is recorded (`corpus/lessons/round-49.md:44-49`, "Admit — staged S182 →
S269", "Admit — staged S183 → S270"); the coverage-map row lands with the file
(`README:597`, QUALITY 7; `LOG.md:2390`).

Measurement half (rule 2) is the attack surface — three findings below.

## Finding 1 (defect, conditional) — the void fallback "an erratum below says so" cannot land this round

- Attacks: `corpus/README.md:599` against the frozen tip rule
  `.ufo/evidence/round-49/contract.json:73` (`no_harm.tip`): "after REV only receipt
  files under `.ufo/evidence/round-49/after/` and wave reports land".
- Command/output: receipts R1 (`sed -n '599p'`) and R8.
- The line's own failure path promises an erratum appended below it. Under the frozen
  tip rule, no `corpus/README.md` edit may land after REV; if the single deciding run
  prints `C2_R49_PASS=false`, the round ends with line 599 still standing — condition
  false, erratum never written — and the miss has no errata row in the entry's round,
  against the lane's own QUALITY 6 (`corpus/QUALITY.md:15-17`: "a miss is an errata row
  naming the discriminator, never a silent drop"). The self-voiding clause ("this line
  is void") and the untouched `open` table row keep the README from *reading* held
  (rule 2 is about the table), so the defect is conditional and records-level, not a
  false held status; but the promised mechanism is unexecutable inside round 49.
- Smallest safe correction, available because `corpus/README.md` is a declared volatile
  record and final REV is not frozen yet (contract schedule `:81`: "fixes, final REV"):
  append the miss-erratum text *now* as a paired block ("Erratum — takes effect only if
  the receipt prints C2_R49_PASS=false: F10 remains open ..."), or name the conditional
  erratum as owed debt in `LOG.md`/`SCORECARD.md` so QUALITY 6 has its row either way.

## Finding 2 (defect, epistemic) — the held claim's receipt does not measure the move's defining property, and the substitute evidence is forward-referenced

- Attacks: `corpus/README.md:599` ("held ... for its stated next move") together with
  `corpus/knowledge/pbt-generator-pilot.md:65-68`.
- Command/output: receipts R6 (`awk 'NR>=60 && NR<=69'`).
- The entry itself concedes the frozen counter "cannot tell a property-based generator
  from a differential one" and locates the property-based evidence "outside the
  counter: its code ..., an access trace and oracle-mutation results in the round-49
  wave-2 reports". At `f181a961` no such wave-2 report exists yet (this wave produces
  them). So at the candidate, every check the deciding receipt will apply (panel kills,
  classes, oracle agreement, records — `c2/measure.py:288` even accepts line 599 by
  bare substring `'F10' in ln and 'held (round 49)' in ln`, blind to the conditioning)
  can pass while the *PBT* character of the move rests on a forward reference. Rule 2
  says held only when the next move "is measured"; the named measurement measures a
  generator, not specifically a property-based one. This is disclosed honestly in the
  entry, and wave-2 seats are producing the trace/oracle-mutation evidence before final
  REV — but the README line inherits the gap: it cites only the deciding receipt.
- Smallest safe correction: at final REV, extend `README:599` (or the entry's measure
  section) to cite the landed wave-2 access-trace and oracle-mutation reports by path,
  converting the forward reference into located evidence; if those reports falsify the
  property-based character, the held line must not survive even on a green receipt.

## Finding 3 (observation, no defect) — the mark at REV precedes the run, by pre-registration, and rule 2 survives only because the table stays `open`

- The held mark exists at REV while the deciding run happens after it (contract
  `:48` predicate itself demands "README marks F10 held (round 49)" at REV; `:60`
  kill_rule; `:81` schedule). Under `README:120-121` this is lawful only in the reading
  the lane chose: the status *cell* still reads `open` (`README:87`, byte-identical to
  base — receipts R2), and the held assertion is an explicitly conditioned appended
  note. The frozen counter's substring check (`measure.py:288`) passes on that note by
  design; it would also pass on an unconditional one — the conditioning is a README
  discipline, not a counter guarantee.
- Form asymmetry worth naming: F1/F2 were marked `held (round 1)` *in the table*
  (`README:78-79`) and later downgraded by an appended correction (`:105-121`); F10
  reverses the order — table stays `open`, appended note announces held. An in-place
  status-cell edit shifts no line numbers, so the append-only line-stability rationale
  (`README` addendum, "Appended, not inserted: the rows above keep their line numbers")
  does not force this choice, and after a green run a table-only reader sees F10
  `open` — the same staleness class the round-1 status correction was written to fix.
  Cosmetic; the line declares the choice ("The frontier table row above stays as
  written (append-only)").

## Finding 4 (checked, no contradiction) — PROVINCE.md

- `PROVINCE.md:40-42` governs Frontier→Core moves (admitted, source-headed entry citing
  a mined row). F10's held line claims held, not Core; the entry and row satisfy the
  admission shape anyway (Finding "Rule check" above).
- `PROVINCE.md:12` ("this lane's own corpus and gates") covers the named gate
  `tools/staged-id-guard.py`; the contract pins its sha and the counter refuses any
  other bytes (`c2/measure.py:253-254`), so no sibling surface is touched — consistent
  with `PROVINCE.md:14-17` (never edits a sibling's gate; TWO-lane generality not
  claimed — `pbt-generator-pilot.md:62-63` "not a method shown across the fleet's
  gates").
- `LOG.md:2387/2390-2391` records the step and its conditioning. No PROVINCE
  contradiction found.

## What would falsify the move (for the deciding reader)

1. Receipt `.ufo/evidence/round-49/after/c2.stdout` printing anything but
   `C2_R49_PASS=true` → line 599 self-voids, F10 stays open (and Finding 1's erratum
   debt fires).
2. Wave-2 access-trace/oracle-mutation reports showing the generator imports/execs the
   guard's code outside its CLI or mirrors the pristine guard → the "property-based"
   basis of "held for its stated next move" collapses regardless of the receipt
   (Finding 2).
3. S269/S270 losing `mined`/`2026-10-26` cells, or the entry header changing — the
   counter then fails records (`measure.py:285`, `:288`).

## Summary

- F10 table row `README:87` byte-identical base→candidate, still `open`; held lives in appended line 599, conditioned on the deciding receipt.
- Rule 1 (`README:72-74`) satisfied structurally: entry source-headed, S269/S270 mined 2026-10-26 (`SOURCES.md:144-145`), rows admitted in lesson Gate, coverage-map row same round.
- Defect 1: the promised miss-erratum cannot land after REV under frozen contract tip `:73` — a failed run leaves the fallback unexecuted (QUALITY 6 exposure); fix before final REV.
- Defect 2: the receipt cannot verify the move's defining property (property-based vs differential, entry's own lines 65-68); the substitute wave-2 evidence is forward-referenced at the candidate; cite it by path at final REV.
- Mark-at-REV-before-run is pre-registered (contract `:48`), lawful only because the table cell stays `open`; counter accepts line 599 by substring, blind to the condition.
- No PROVINCE.md contradiction: no Core claim, lane-owned pinned gate, no sibling edits, generality not claimed.
