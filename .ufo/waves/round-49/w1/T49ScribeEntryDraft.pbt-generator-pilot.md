source: S_QC — https://doi.org/10.1145/351240.351266 — §Abstract; §1 Introduction; §2.4 Monitoring Test Data; §3.2 Generators for User-Defined Types; §6.6 Some Reflections; §7 Conclusions — Claessen & Hughes, "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs", ICFP 2000, pp. 268–279 — re-opened 2026-10-26 (placeholder id: the L1 replaces `S_QC` with the S-id of the row it appends this round)
source: S_SB — https://smallbone.se/papers/lic.pdf — §2.10 "Generating Test Data", printed p. 34 (PDF page 39) — Smallbone, "Property-based testing for functional programs", Chalmers Technical Report 76L, ISSN 1652-876X, 2011; 1,269,821 B, sha256 `eaee48f930ba20a06824fe238cc6a42427e9fb45d1d70b852bf091ad6e44ac08` — re-opened 2026-10-26 (placeholder id: the L1 replaces `S_SB`; see "The pointer that was wrong" below, the §4.1/p. 44 anchor the merge carried does not resolve)
verified-at: 2026-10-26
recheck: 365d — `curl -fsSL 'https://smallbone.se/papers/lic.pdf' | sha256sum` (expect `eaee48f9…44ac08`) and `curl -fsSL 'https://smallbone.se/papers/lic.pdf' | pdftotext -layout - - | grep -c 'fit the program at hand'` (expect 1); and `aaron papers fetch 10.1145/351240.351266 | grep -c 'no measurement of test coverage'` (expect 1 — the fetched copy breaks words, e.g. `prop erties`, so grep spans of a few words, not whole sentences; both chains run and returned 1 on 2026-10-26)
ground: F10 (PBT generators for gate fixtures) — open → held (round 49)

# A property-based generator for a gate fixture is a programme, not a sampler: one QuickCheck-shaped generator against `tools/staged-id-guard.py`, scored by a hidden mutant panel

This entry is the pilot admission for frontier row F10. It states the generator craft
the two sources actually teach, what the lane built from it (one generator against one
named gate — not a suite, not a library), how a frozen counter measures it, and what the
measurement does not reach. Numbers the deciding run fills are left as `@CLASSES@`,
`@KILLS@` and `@FIXKILLS@`; nothing here states a count the lane has not observed.

## What the sources state

S_QC was fetched as markdown by DOI and is quoted **verbatim as fetched**, including its
pervasive word splits (`prop erties`, `p ossible`, `b e`) and its ligature losses (`dene`
for `define`, `de ne`, `ma jor` for `major`, one control byte inside `su?ciently`).
Nothing is silently repaired, because a repaired quote cannot be re-located in the
snapshot. Verified by de-spacing: each span below occurs exactly once in the fetched text
(all whitespace removed from both sides; receipt in the round-49 wave-1 records). S_SB was
fetched as a PDF, quoted from `pdftotext -layout`, and its text is clean.

- **Properties are executable functions, and the generator is a separate artefact.**
  S_QC, §Abstract: QuickCheck is "a to ol which aids the Haskell programmer in formulating
  and testing prop erties of programs. Prop erties are describ ed as Haskell functions, and
  can b e automatically tested on random input, but it is also p ossible to dene custom test
  data generators." §3 (`3. DEFINING GENERATORS`) is a whole section on the second half of
  that sentence: the generator is written by the tester, not inferred from the code under
  test.
- **The generator must fit the program at hand.** S_SB, §2.10, printed p. 34: "As always
  with random testing tools, the quality of the test data determines the quality of the
  generated equations. As such, it is important to provide good test data generators,
  that fit the program at hand." The same paragraph supplies the counter-example that
  makes this operational: "if we use an inappropriate generator" the laws you obtain say
  little.
- **The distribution is the thing you must look at, not assume.** S_QC, §1: "it is
  meaningless to talk ab out random testing without discussing the distribution of test
  data", and QuickCheck's choice is "to put distribution under the h uman tester's con
  trol", with "a way to observe the distribution of test cases." §2.4 ("Monitoring Test
  Data") is the mechanism: `classify` and `collect` print a histogram, and the paper's
  own worked example is a warning — "it is worrying that very short lists dominate the
  test cases so strongly. After all, it is easy to de ne an erroneous version of insert
  which nevertheless works for lists with at most one element." S_QC, §6.6 states the
  consequence as a limit: "The ma jor limitation of QuickCheck is that there is no
  measurement of test coverage: it is up to the user to investigate the distribution of
  test data", and to decide whether enough tests have been run.
- **Size is a knob the tester sets.** S_QC, §3.2: `newtype Gen a = Gen (Int -> Rand -> a)`
  "where the new parameter is to b e interpreted as some kind of size b ound"; the `sized`
  combinator "generates an a by passing the current size b ound to its parameter. It is
  then up to the programmer to interpret the size b ound in some reasonable way during
  test data generation." §7 lists this as a contribution: "a novel way of controlling
  size when generating random elements of recursive data typ es."

Inference for this lane (not in the sources): the four statements map onto one
deliverable — a generator that (a) is written to the gate's *documented* contract, (b)
stays inside the input sizes the gate is meant to survive, (c) prints what it produced
per class instead of asserting coverage, and (d) states its properties as executable
predicates over the gate's CLI answer.

## What the lane built

`tools/pbt-staged-id.py` (wave-1 draft: `.ufo/waves/round-49/w1/T49ExecGenerator.pbt-staged-id.py`;
a live seat is still editing it, so this entry names symbols, not line numbers) drives the
round-43 gate `tools/staged-id-guard.py` — pinned at sha256
`03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` and never edited this
round. Five construction choices follow the sources:

- **CLI only, own oracle.** The generator never imports or execs the guard's code; it runs
  `python3 -I GUARD --registry R --staged G [--map M] --json` and compares the answer with
  an oracle it implements from the guard's module docstring (`analyse`/`validate_map`
  docstrings, `tools/staged-id-guard.py:132-305`), not from the guard's source. This is
  S_QC's separation of property from generator taken literally: the property is "the
  guard answers what its docstring says", written once, checked per case.
- **Sized inputs.** Cases are small on purpose: at most 1–4 id-bearing rows per table
  (0–8 rows with the extras the recipes add; the module docstring's bound), ids drawn
  as `S001`…`S090`, documents drawn from a short form pool (scheme, `www.`, trailing
  slash, case), rows placed at 0–6 leading spaces. Mirrors §3.2: size is set by the tester and held
  small enough that every answer is inspectable.
- **Twelve recorder recipes, shuffled, round-robin.** The draft's `RECIPES` tuple
  holds one recipe per class pair —
  no-collision, collision, indent 1–3, indent ≥4, ≥4-digit ids, setup refusal, unmapped,
  held, cascade, admissible map, inadmissible map, map setup refusal. The seed shuffles
  the order and each recipe draws its parameters from `random.Random(seed)`; the schedule
  is round-robin, so with 400 cases each recipe runs 33–34 times. This is *stratified*
  random generation, not an `Arbitrary` instance — stated here because it is the honest
  description of what the distribution is.
- **Distribution observed, not asserted.** Every case is classified into the twelve frozen
  classes and printed (`CLASS <name>=<n>`, plus `classes=k=v,…` on the last line), exactly
  S_QC §2.4's `classify`/`collect`; the generator's own floor is 20 per class
  (`CLASS_MIN = 20`), twice the contract's 10.
- **Stop at the first violation.** A disagreement writes `VIOLATION index=<i> …` with the
  observed exit/stdout/stderr and exits 1; otherwise the last line reads
  `PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=…` and exit is 0. Every case run is dumped as one
  JSONL line `{index, registry, staged, map}` so a counterexample is replayable.

### The twelve classes and what each one asks of the guard

Classes are the counter's frozen predicates (`.ufo/evidence/round-49/c2/measure.py:52-53`,
`case_classes` at `:117-150`); the generator mirrors them with its own `case_classes`.
A class is credited when the *counter*
classifies a dumped case into it, from the case text plus the pristine guard's answer.

| class | what the case exercises |
|---|---|
| `collision` | a staged id present in the registry — the question the gate exists to answer (`collision_count > 0`) |
| `no_collision` | no id in both tables — the gate must still answer, not refuse |
| `held` | a colliding row whose document the registry already carries — dedupe to the registry id, do not append |
| `unmapped` | a colliding row with no URL/DOI/path — refused, because renumbering an undocumented row is arithmetic |
| `cascade` | the naive `max+1…` fix whose targets are themselves staged ids — refused |
| `indent_1_3` | a collision on a row at 1–3 leading spaces, which the census pattern accepts and the column-zero pattern misses |
| `indent_4_plus` | a row at ≥4 spaces, which the 0–3-space extractor must not see as a row at all |
| `id_4_plus_digits` | an id with ≥4 digits, where numeric and lexicographic order disagree |
| `refusal` | setup refusal (exit 2): a row with <5 cells, a duplicate id, unreadable/oversized input |
| `url_form_variant` | the same document written differently across the tables (scheme, `www.`, trailing slash, case) |
| `map` | analysis plus a `--map` document |
| `map_inadmissible` | a map that must be refused (exit 1): clash with the registry, target below the safe floor, target on another staged id, uncovered collision, self-map, undocumented row decided, held document moved, non-injective |

## How it is measured

The counter is frozen at `.ufo/evidence/round-49/c2/measure.py` (label `C2_R49_PASS`);
its predicate is `total == 0` over seven terms (`:359-361`), all computed from REV bytes:

1. **Generator present** at `tools/pbt-staged-id.py` in REV — else `absent=1`.
2. **Pristine run** `--guard GUARD --seed 4949 --cases 400 --dump FILE` (the constants
   `SEED, CASES = 4949, 400` are at `:49`): exit 0, last line `cases=400 violations=0`,
   and a dump of exactly 400 lines with `index` 0…399 (`:310-313`).
3. **Oracle agreement**: for every dump case without a map, the counter's own oracle
   (`:90-115`) is compared with the pristine guard — exit 2 must agree, exit must be
   0/1/2, and on exit 0 `collisions`, `registry_rows`, `staged_rows` must match
   (`:315-327`). Exit 1 is accepted as an answer, because the observed semantics are
   "1 = analysis refused (unmapped or cascade non-empty) or map inadmissible"
   (contract `claims.C2.guard_exit_semantics_observed`) while the guard's docstring
   names exit 1 only for a bad map (`tools/staged-id-guard.py:39`, against `analyse`
   `:157` and `main()` `:471-493`).
4. **Class coverage**: each of the twelve classes in at least 10 dump cases
   (`CLASS_MIN = 10`, `:50`); the counter prints `CLASS <name>=<n>` and marks shorts
   (`:352-354`). Observed at the deciding run: `@CLASSES@`.
5. **Hidden panel**: 12 mutants, sha256
   `d6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1` (`:47`); the counter
   refuses any other bytes, and requires every mutant's `old` string
   to occur exactly once in the guard (so each mutant is a single-site text edit). The
   panel lives outside the lane until the generator is final and is committed with its
   witness cases before the deciding run.
6. **Differential confirmation**: for each mutant the same generator run is replayed
   against the mutant; a kill is *confirmed* only when the generator exits 1 naming a
   counterexample index and that dumped case makes the pristine and mutant guards print a
   different `(exit, JSON)` — sha fields excluded (`:331-350`, `comparable()` `:188-192`).
   Target: at least 11 of 12. Observed at the deciding run: `@KILLS@`.
7. **Records**: this entry's head block cites a `source: S###` whose SOURCES row is
   `mined` and opened 2026-10-26, and `corpus/README.md` carries a line with both `F10`
   and `held (round 49)` (`:268-291`).

Controls, scored at freeze bytes and only then: `CTL_ABSENT` (no generator) must print
`C2_R49_PASS=false`; `CTL_FIX` — a fixture-replay stub carrying the guard's own selftest
fixtures and their golden outputs through the same interface — must also print
`C2_R49_PASS=false` and confirm fewer than 11 mutants; its confirmed count is
`@FIXKILLS@`. The guard's selftest itself, run at base this round, prints
`STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` / `VERDICT: PASS`, exit 0 — that is the
replay stub's whole case pool, and the reason a replay cannot reach most of the panel.
`WITNESS` (11 hand-made cases confirming all 12 mutants) is a non-equivalence receipt for
the counter's kill path, not a PASS.

## What it does not establish

- **No shrinking.** The generator stops at the first violation and reports the case that
  failed; it never minimises it. Every reported counterexample is whatever size the
  recipe drew, not a minimal one. S_QC's own reducer is not implemented.
- **One gate, one property.** The evidence is about `tools/staged-id-guard.py` against its
  documented contract. Nothing here says the same generator shape works for another gate;
  F10 would need a second, differently-shaped gate before that was a method rather than a
  pilot.
- **The panel is 12 mutants held outside the lane and revealed only after the generator
  is final — not a sample of a mutation space.** `@KILLS@`/12 is a demonstration that
  generated cases can confirm non-equivalent mutants of this gate; it is not a mutation
  score, and 11/12 does not estimate what a larger panel would yield. The panel's
  existence is also what makes the differential step cheap: the counter, not the
  generator, runs the differential.
- **The oracle is a second reading of one docstring.** The generator's oracle and the
  counter's oracle are both written from `tools/staged-id-guard.py`'s documentation. A
  wrong-but-documented behaviour is invisible to both, and the counter's oracle check
  covers analysis-mode cases only — a `--map` case is scored by class membership and by
  the panel, not by an independent map oracle.
- **The class list was designed, not discovered.** Twelve named classes and twelve
  recipes mean coverage of *these* twelve; §2.4's warning is about classes nobody named.
  A stratified schedule also fixes the per-recipe frequency in advance (33–34 of 400), so
  the printed histogram measures the schedule as much as the input space.
- **The guard's docstring is imprecise and stays that way.** It documents exit 1 only for
  an inadmissible map (`:39`), while `analyse` sets `refused` for unmapped rows or a
  cascade and `main()` returns 1 for `verdict='refused'` with no map (`:157`,
  `:473` and `:493`). The generator checks the *observed* semantics and the discrepancy is
  recorded here rather than repaired, because the guard is a pinned capability.
- **The numbers in this draft are placeholders.** `@CLASSES@`, `@KILLS@` and `@FIXKILLS@`
  are filled from the single deciding invocation; a number in this entry that is not one
  of those three is either a frozen constant of the contract or an observation named as
  such above.

## The pointer that was wrong

The assimilation source for S_SB
(`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:37`, and the lane's
read-only copy of `r4-quickcheck-primary-correction.md`) anchors "good test data
generators, that fit the program at hand" at **§4.1, p. 44**. Fetching the row's own URL
on 2026-10-26 (`sha256 eaee48f9…`, above) puts the sentence in **§2.10 "Generating Test
Data", printed p. 34 (PDF p. 39)**; §4.1 of that thesis is "A Parallel Correctness
Criterion" and printed p. 44 falls inside §3.4 "shr: Problems with Partiality". The quote
itself is exact and still present. A row appended this round must carry the corrected
anchor, or the lane would pin a pointer that does not resolve — the same defect class as
round 44's `r44-anchor-refresh-rule.md`.

## Summary

One QuickCheck-shaped generator (`tools/pbt-staged-id.py`) drives one pinned fixture gate
(`tools/staged-id-guard.py`) through its CLI, with its own contract-written oracle, sized
0–8-row cases, twelve stratified class recipes, and a printed per-class histogram. A
frozen counter runs it at seed 4949 / 400 cases on the pristine gate (no violation,
oracle agreement, every class ≥10: `@CLASSES@`) and replays it against a hidden 12-mutant
panel, confirming a kill only on a differential re-run (`@KILLS@` of 12, target 11), with
a fixture-replay control that must fail (`@FIXKILLS@`). It does not shrink counterexamples,
covers one gate, does not measure a mutation score, and shares its oracle's authority with
a docstring whose exit-1 wording is known to be wrong. S_SB's anchor is corrected here:
§2.10 p. 34, not §4.1 p. 44.
