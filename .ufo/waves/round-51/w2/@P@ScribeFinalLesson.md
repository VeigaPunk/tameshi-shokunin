# @P@ScribeFinalLesson — corrections block for `corpus/lessons/round-51.md`

Deliverable of seat `T51W2ScribeFinalLesson` (round 51, wave 2, final lesson fact check). Full evidence, the
audit of `## Gate` and `## Mistakes`, and the confirmed-claims table are in
`.ufo/waves/round-51/w2/T51W2ScribeFinalLesson.md`. Lesson checked at `f133b47` (53 lines; base `9962033f`,
candidate `6d8c11e`, freeze `9d023aed`). No lane file was written; no counter or sweep was re-run.

**Result: 5 corrections required, 1 disclosure addition. Nothing else in the lesson was found false.**

---

## Correction 1 — line 45 (no-harm is not measured at a deciding revision; the 64/64 restoration is a fixture result)

Old (whole bullet):

```
- No-harm at the deciding revision: `.ufo/evidence/round-51/after/no-harm.stdout` (eleven monitors). The round-21 cold-read monitor fell to 44/64 (score 6) after runner and registry changes, then the trace-bound 20-section re-key restored 64/64 (score 8); all readers and traces are listed under `.ufo/evidence/round-51/coldread/`.
```

New:

```
- No-harm is measured at CAND, not at a deciding revision: `.ufo/evidence/round-51/after/` does not exist at `f133b47` (LOG.md:2420 defers the deciding receipts to closure). At `6d8c11e` the eleven-monitor no-harm prints ten `ok` and `NOHARM coldread-floor score=6 credited=44 RED` (`T51W2CritNoHarm.md` F1/F4), and the strict round-21 monitor independently reports 44/64, score 6 — the same 44/64 the base simulation reaches by appending one byte to the runner (`.ufo/waves/round-51/w1/T51CritRekey-sim-receipt.txt`: `covered=44/64`, 20 dropped headings). The trace-bound re-key has not landed on the lane: `.ufo/evidence/round-51/coldread/readers.json` names one reader for each of the 20 lost headings while `coldread/reads/` holds no trace, so 64/64 (score 8) is a fixture result only (`T51ExecRekey.md:74,176,189`, re-key commit `0f28deeb` in a `--shared` clone).
```

Why: `after/` does not exist; `coldread/reads/` has 0 files while `readers.json` maps 20 headings to 20 named
readers; the 44/64, score 6 value is measured at CAND and at the base simulation; 64/64 (score 8) is measured only
in the W1 re-key fixture clone. The `eleven monitors` count itself is right.

## Correction 2 — line 28 (C3's decisive receipt and the report do not exist)

Old:

```
Therefore C3 does not verify: its decisive counter output is `.ufo/evidence/round-51/after/c3.stdout` and is reported verbatim in the report.
```

New:

```
Therefore C3 does not verify. A fresh clone at CAND gives `C3_R51: rev=6d8c11e378aa90b12650808e1b79270742935f15 tools=30 rows=32 covered=29 missing=1 deleted=0 selftest_fail_rows=2 total=1 C3_R51_PASS=false`, the single miss being `tools/round21-measure.py` (`T51W2ExecTool02/c3-counter-full-run.txt`; `T51W2CritC3Truth.md` F1). The deciding-run receipt `.ufo/evidence/round-51/after/c3.stdout` and the round report do not exist at `f133b47`; the line above is the wave-2 CAND measurement.
```

Why: `after/` absent; no round-51 report anywhere in the lane (`reports/` and `.ufo/reports/` contain none; the
only tracked `*round-51*` path outside `.ufo/{waves,evidence}/round-51` is the lesson itself).

## Correction 3 — line 18 (the C1 survivor list names 5 of 7 measured survivors; QUALITY 101 requires all)

Old:

```
remaining weaknesses include duplicate ids, wrong rounds, long pointers, unsupported status phrase and a table header without `ground`.
```

New:

```
remaining weaknesses are duplicate ids (M02), an ignored round value (M03), a pointer span over the counter's six-line limit (M04), a pointer without the expected status phrase (M05), `held` accepted as a substring of `partly held` (M10), a table header without `ground` (M12) and a `mined` row with no used-by path (M15) — every one of the seven has a forge (`T51MutC1Counter.md` §Surviving blind spots; `M10_held_for_partly-forge.txt`, `M15_skip_mined_empty-forge.txt`).
```

Why: `T51MutC1Counter.md` records 7 killed / 7 survived; the lesson omits M10 and M15. `QUALITY.md` criterion 101
says “the round's lesson names the survivors”.

## Correction 4 — line 16 (F11/F12 finding mis-cited to a report that does not contain it)

Old:

```
Two independent wave-1 readers re-derived all ten statuses and agreed with the frozen set; F11/F12 are fixture ids, not frontier rows (`T51CritExpectedA.md`, `T51CritExpectedB.md`).
```

New:

```
Two independent wave-1 readers re-derived all ten statuses and agreed with the frozen set (`T51CritExpectedA.md`, F1-F5; `T51CritExpectedB.md`, F6-F10); F11/F12 are round-43 fixture ids, not frontier rows (`T51CritExpectedB.md:60-63,96`; README:548-555).
```

Why: `grep -c F11` on `T51CritExpectedA.md` = 0; the F11/F12 resolution is `T51CritExpectedB.md:60-63,96`
(`F11_outflag_namespace`, `F12_method_two_returns`, README:548-555).

## Correction 5 — line 10 (S273's quotes have no locations; CORPUS rule 1 requires URL + access date + quote with location)

Old (tail of the S273 bullet):

```
“the exit status of the last command substitution performed” (9). The empirical composition matters
```

New:

```
“the exit status of the last command substitution performed” (9). Quote locations in the stored snapshot: `-e` item lines 6548-6553 and 6554-6560, `pipefail` item lines 6707-6709, §Simple Commands lines 4172-4174 (S273's own copy-line span for the assignment-status rule stops at 4173, one line before the fourth quote's words end). The empirical composition matters
```

Why: `CORPUS.md` §SOURCES.md rule 1 — “the round lesson's `## Gate` records, for every new row, the URL, the
access date, and a ≤25-word quote **with its location** grounding `teaches`.” S272's bullet gives its location
(“pinned lines 6-7”); S273's gives none. Locations verified in
`.ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html` after tag stripping: 6548, 6553, 6554, 6560, 6707,
6709, 4173, 4174. All four quotes are real and within 25 words (9 / 19 / 20 / 9).

## Disclosure addition — line 28 (two of the 30 registry rows misdescribe their tool; not a false lesson sentence, but the C3 paragraph reads as if executor review left the table accurate)

Insert after `the round-51 table rows were reviewed by 30 executors, not admitted solely on the counter's output.`:

```
 Two rows still misdescribe their tool at CAND and the counter's first-token check cannot see it: the `entry-registry walk` row quotes the selftest's last line as `SELFTEST: PASS (51 cases) at 84aa673` where the observed last line is `SELFTEST: PASS (51 cases)` (`T51W2ExecTool02/c3-counter-full-run.txt`, `tools/registry-check.py` line; `T51W2CritC3Truth.md` F2), and the `round-20 receipt-window measure` row glosses exit 2 as usage-only while a non-git `--repo` with no `--rev` also exits 2 with `MEASURE: COULD_NOT_EVALUATE (no revision)` (`@P@ExecTool11/03-exit-code-survey.txt`, cases I-J). Neither affects the frozen verdict: C3 is false for the `round21-measure.py` miss alone.
```

---

## Checked and correct (no change)

Contract/amendment hashes and the “no counter changed after freeze” claim (HEAD digests equal `freeze.json` for
C1/C2/C3 counters, spec, statement sets); selftests 6/6, 11/11, 10/10 and reach `calls_measure=1/1/3`; the base
frontier table at README:76-87 with exactly seven superseded cells and F9's basis at row 86 (the `76-86` note
off-by-one is already disclosed); the ten `FRONTIER Fk: ok` receipt and its negative control; C1's 14-edit / 7-7
mutation probe; the C2 sweep (green control, restore OK, 2/10 `K_MODE_CMP`+`K_COUNT_GE`, 8 SURVIVED, 7/10
predictions), the runner's byte-identical `TABLE_DRIFTPINS`, regression `cases=10 passed=10`, `--selftest 107/107`;
the neutral-name flip of exactly three mutants over three repeats; the five `HOLE` witnesses; C2's counter probe
(15 blind spots / M16 equivalent / M17 killed) and the unbound-suite limitation; the 30-row round-51 registry table,
the `round21-measure.py` blocker (exit 1 in a clone, 13/13 with siblings), the `--help --selftest` forgery, 30 row
seats; the 18/12 tool count and `covered=0` at base; 133 rows, next id S274; census start/end exit 0; the S022-only
status diff; `## Mistakes` row 1 (`:400`, `:403`, `:158`; three path-masked survivors; captured-by `none`; criterion
102 text and the red/green falsifier bytes exit 0/1) and row 2 (`SOURCES.md:33` at base, CTL_0 conflict,
CTL_S022 clears it); no considerthese adoption; no tool installs.

## Notes for the L1, not lesson corrections

1. `T51W2CritQualityMistake.md` cites `corpus/lessons/round-51.md:30-35,64-75` and `:72-75` for text about
   `js-round-gate` / `js-sources-check` / `js-cite-check`; the committed lesson is 53 lines and
   `grep -c js-round-gate` = 0. That critic reviewed the wave-1 draft (`T51ScribeMistakes.md`), not this file.
2. Reason split for the 20 lost sections conflicts between the seat brief (“1 registry section
   `no-ledger-entry`”) and `T51W2CritNoHarm.md` F1 (“the sole `no-ledger-entry` is section 20. The registry section
   (14) is input-drift”). The lesson states neither; the canonical monitor decides.
3. Row-level nit: `corpus/SOURCES.md:148` cell 7 cites “copy lines 4172-4173” while the fourth quote's words end at
   4174 and the zero-status line at 4176.
