seat: HardReviews
item: selftest addition hardening the round-45 freshness counter's review-admission gates (F06,F07,F08,F09,F13)

# C2 selftest addition — freshness counter (round 46, w1)

Deliverable: `.ufo/waves/round-46/w1/HardReviews.addition.py` — one top-level
`extra_HardReviews()` plus helpers `_xHardReviews_seats`, `_xHardReviews_run`. Five cases, each
named after the mutant id it kills, each pairing one review that must be refused with one
independent agree (`S002`/`RevZ`) that must still be admitted, so a gate that stops counting
anything at all also fails.

Scratch: `/tmp/tameshi-r46-HardReviews/` (`orig.py` = copy of
`.ufo/evidence/round-45/freshness/measure.py`, `hard.py` = assembled hardened copy).

## Why these five survived the round-45 selftest

`T17_independent_reviews` already contains a self-review (`S002`/`ExecA`) and an out-of-prefix
report (`S007`, `/tmp/Rev.md`), but its single report text is
`'RevX RevY RevZ S001 S002 S003 S004 S005 S008'`:

- F06: the self-review is dropped by the *reviewer-named-in-report* gate (`ExecA` is not in the
  text), not by the author gate — removing `who == authors.get(rid)` changes nothing.
- F08: `S007`'s report path is not in the `reports` map, so `read_text` returns `None` and the
  review is dropped by the readability gate before the prefix gate is consulted.
- F07: `RevZ`'s output is `''`, which is falsy with or without `.strip()`; no whitespace-only
  output exists in the fixture.
- F09: no review names the id but not the reviewer.
- F13: every verdict in the fixture is `agree` or `dispute`.

## Per-mutant evidence

Command (per mutant, scratch harness calling the declared manifest's exact old->new replacement and
then the selftest): printed `FAIL <case>` lines only, for the assembled `hard.py`.

| id | case | input separating pristine from mutant | mutant output |
|---|---|---|---|
| F06 | `F06_review_non_author` | review `S001` by `RevA`, where `authors['S001'] == 'RevA'`; report text `'RevA re-checked S001 and agrees'` names both reviewer and id; `RevA` is a seat with output `done`; verdict `agree` | pristine `(['S002'], [])`; mutant `(['S001','S002'], [])` |
| F07 | `F07_seat_output_nonempty` | `results` = `[{'name':'RevW','output':' \n\t '}, {'name':'RevOK','output':'done'}]` | pristine `['RevOK']`; mutant `['RevOK','RevW']` |
| F08 | `F08_report_outside_prefix` | review `S001` by `RevB` with report `.ufo/waves/round-44/w1/R.md`, mapped in `reports` to readable text naming `RevB` and `S001` | pristine `(['S002'], [])`; mutant `(['S001','S002'], [])` |
| F09 | `F09_report_names_reviewer` | review `S001` by `RevC`, in-prefix report `.ufo/waves/round-45/w2/R.md` with text `'S001 was re-checked against the ledger'` (id present, reviewer absent) | pristine `(['S002'], [])`; mutant `(['S001','S002'], [])` |
| F13 | `F13_verdict_only_agree` | review `S001` by `RevD`, seat, non-author, in-prefix report naming both, verdict `unsure` | pristine `(['S002'], [])`; mutant `(['S001','S002'], [])` |

Exact failing-case lines from the per-mutant sweep (`exit 1` each):

```
F06 exit 1 | FAIL F06_review_non_author got=(['S001', 'S002'], [])
F07 exit 1 | FAIL F07_seat_output_nonempty got=['RevOK', 'RevW']
F08 exit 1 | FAIL F08_report_outside_prefix got=(['S001', 'S002'], [])
F09 exit 1 | FAIL F09_report_names_reviewer got=(['S001', 'S002'], [])
F13 exit 1 | FAIL F13_verdict_only_agree got=(['S001', 'S002'], [])
```

Each mutant fails exactly its own case and no other — no case is a proxy for a different gate.

## Helper runs

`python3 .../hardening/assemble.py --group freshness --add .../HardReviews.addition.py --out /tmp/tameshi-r46-HardReviews/hard.py`

```
wrote /tmp/tameshi-r46-HardReviews/hard.py (1 additions)
```

`python3 /tmp/tameshi-r46-HardReviews/hard.py --selftest` (exit 0):

```
PASS F06_review_non_author got=(['S002'], [])
PASS F07_seat_output_nonempty got=['RevOK']
PASS F08_report_outside_prefix got=(['S002'], [])
PASS F09_report_names_reviewer got=(['S002'], [])
PASS F13_verdict_only_agree got=(['S002'], [])
C1_R45_SELFTEST: cases=24 failed=0
VERDICT: PASS
```

(`cases=24` = the round-45 `len(cases) + 4` = 19, plus my 5.)

`python3 .../hardening/try-mutants.py --group freshness --file /tmp/tameshi-r46-HardReviews/hard.py`:

```
PRISTINE pass VERDICT: PASS
MUTANT F06 mutant killed
MUTANT F07 mutant killed
MUTANT F08 mutant killed
MUTANT F09 mutant killed
MUTANT F13 mutant killed
MUTANT FN1 neutral survived
MUTANT FN2 neutral survived
MUTANT FN3 neutral survived
```

Full group, same command without `--ids` (other ids are outside this seat; F01–F05, F10–F12, F14,
F15 still `survived`, which the manifest allows):

```
MUTANT F01..F05 mutant survived
MUTANT F06,F07,F08,F09 mutant killed
MUTANT F10,F11,F12 mutant survived
MUTANT F13 mutant killed
MUTANT F14,F15 mutant survived
MUTANT FN1,FN2,FN3 neutral survived
```

## Behaviour neutrality

`diff -u /tmp/tameshi-r46-HardReviews/orig.py /tmp/tameshi-r46-HardReviews/hard.py` shows exactly
three changes: the assembler-mandated `SELF_PATH` repoint, the insertion of my additive block before
`def main():`, and the tally line (`extra_cases` accumulation). `measure()` is byte-identical, so no
review-admission rule changes — my cases only call `review_sets()`/`wave_seats()` on in-memory
fixtures.

## Unrun / out of bounds

- Equivalence over the round-45 data revision (`ea25e02...`) was **not** run by this seat: seat
  measurement bounds allow counters only as `--selftest` or against `--rev 745a583.../683eedd...`.
  It belongs to the L1's deciding run of `mutate.py --targets hardened`; behaviour neutrality is
  argued above from the diff instead.
- No fixture repo / `git init` was needed: every case is a pure function call on in-memory data, so
  nothing was committed anywhere.
- No tool installed or upgraded (no pacman; nothing needed).
- No file in the lane was written except this report and
  `.ufo/waves/round-46/w1/HardReviews.addition.py`.

## Risks

- The cases pin the review-admission surface as it is frozen in the round-45 counter; if the hardened
  counter's `SELF_PATH` repoint or the tally rewrite changed, `assemble.py` refuses before my block
  runs (it requires each anchor exactly once), which is the intended failure mode.
- F07 is exercised at `wave_seats()` level rather than through `measure()`; that is the smallest
  input that separates the mutated `.strip()` (a whitespace-only output string).
