# T47HardFreshText — selftest addition for the round-46 hardened freshness counter (C2)

Seat: `T47HardFreshText` · group `freshness` · lane `tameshi-shokunin` @ freeze `9acfbe21…`
Deliverable: `.ufo/waves/round-47/w1/T47HardFreshText.addition.py` (one top-level
`extra_T47HardFreshText()`, helpers `_xT47HardFreshText_*`, plus a `--selftest`-only import-time
tripwire for the two mutants whose crash precedes every `extra_*()`).
Counter hardened: `.ufo/evidence/round-46/hardening/freshness-counter.py` (read only, unchanged).

**Result: 10 of 10 owned mutants killed; pristine `VERDICT: PASS` (41 cases, 0 failed);
whole-group sweep: 111 mutants, 68 killed, 41 survived, 2 crashed, 10/10 NEUTRAL `survived`,
zero regressions against `.ufo/evidence/round-47/before/base-freshness.txt`.**

## Cases

Each case is one behavioural input; no case reads the counter's source, hashes it, or pins a
length. Every kill is explained by an input on which the pristine rule and the mutated rule
return different values (the `got=` field of the FAIL line shows the mutated value).

| mutant | case | separating input | pristine vs mutant | FAIL line observed |
|---|---|---|---|---|
| `extract:int:0` (`raw[:4]`→`[:5]`) | `FT01_extract_pdf_branch` | `extract(b'%PDF-1.7…')` with a PATH-first shell stub `pdftotext` that prints one fixed line | pristine: `raw[:4]==b'%PDF'` → stub runs → `'Portable document marker sentence…'`; mutant: `raw[:5]==b'%PDF-'` ≠ `b'%PDF'` → branch skipped, raw bytes decoded, no extracted text and `%PDF` present | `FAIL FT01_extract_pdf_branch text='%PDF-1.7 %���� 1 0 obj << /Type /Catalog /Pages 2 0 R >> end'` |
| `extract:const:0` (`capture_output=True`→`False`) | `FT01_extract_pdf_branch` (same case) | same PDF blob + stub | pristine returns the stub text; mutant leaves `out.stdout` `None`, so `out.stdout.decode` raises — caught by the case and reported as a named FAIL (never a bare traceback) | `FAIL FT01_extract_pdf_branch text='<raised AttributeError>'` |
| `words:bool:0` (`and`→`or`) | `FT02_words_stopword_excluded` | `words('that alpha')` | pristine `{'alpha'}` (stop-word dropped); mutant `{'alpha','that'}` (`len('that')>=4` is true, so the `or` admits it) | `FAIL FT02_words_stopword_excluded ['alpha', 'that']` |
| `words:cmp:0` (`GtE`→`Gt`) | `FT03_words_min_length_four` | `words('quad alpha')` | pristine `{'alpha','quad'}` (4 letters accepted); mutant `{'alpha'}` (`4 > 4` false) | `FAIL FT03_words_min_length_four ['alpha']` |
| `words:int:0` (`4`→`5`) | `FT03_words_min_length_four` (same case) | same | pristine keeps the 4-letter word; mutant `len(w) >= 5` drops it | `FAIL FT03_words_min_length_four ['alpha']` |
| `grade:cmp:9` (`<`→`<=`) | `FT04_grade_overlap_two_admitted` | 11-token quote `Ordering hides flaky runs while the cluster appears only after reruns` present in the page, sharing exactly `{flaky, cluster}` = 2 content words with `_xHardGrade_row()`'s scope+anchor+teaches | pristine `('verified','ok')` (`2 < 2` false); mutant `('invalid','overlap 2')` | `FAIL FT04_grade_overlap_two_admitted ('invalid', 'overlap 2')` |
| `grade:int:0` (`2`→`3`) | `FT04_grade_overlap_two_admitted` (same case) | same | pristine `('verified','ok')`; mutant `2 < 3` → `('invalid','overlap 2')` | `FAIL FT04_grade_overlap_two_admitted ('invalid', 'overlap 2')` |
| `grade:cmp:11` (`Gt`→`GtE`, `n > 25`→`n >= 25`) | `FT05_grade_quote_25_admitted` | the 25-token quote `Flaky failures cluster inside the same job because the rerun repeats one order of the tests only and the second attempt hides the ordering defect`, verbatim in `_xHardGrade_page()`, 3 shared content words, not copied from the row | pristine `('verified','ok')` (`25 > 25` false); mutant `('invalid','quote length 25')` | `FAIL FT05_grade_quote_25_admitted ('invalid', 'quote length 25')` |
| `review_sets:bool:1` (`or`→`and` on line 209) | `FT07_review_report_names_reviewer` (tripwire) | report text `S001 was re-checked against the ledger by an independent seat` — names the id, not the reviewer `RevT47`; plus the control review (report names both id and reviewer) | pristine refuses S001 (`who not in text`), admits S002; mutant `False and False and True` → does not skip → admits S001 | `FAIL FT07_review_report_names_reviewer early agreed=['S001', 'S002']` |
| `review_sets:not:2` (`not text` deleted) | `FT06_review_control_admitted` (tripwire) | same fixture: one refused review and one control that must be admitted | pristine admits S002; mutant `if text or …` short-circuits on every non-empty report, so nothing is admitted | `FAIL FT06_review_control_admitted early agreed=[]` |

### Why FT06/FT07 run at import time (tripwire) and the others do not

The round-46 `selftest()` calls `review_sets()` in its own T17 block, and T17 feeds a review
whose report path is absent, so `read_text` returns `None`. Under both line-209 mutants that
call site raises (`re.search(..., None)`), so the run ends in a traceback with no named `FAIL`
line — exactly the baseline `crashed` state — and the assembler appends every `extra_*()` call
only before the tally print, i.e. after T17. A later case can therefore never report these two.
The tripwire runs the same two fixtures at module import, prints **only** named `FAIL` lines
(nothing when both hold) and returns immediately unless `--selftest` is in `sys.argv`, so the
pristine counter and the `--lane/--rev`, `--check` and `--live` modes emit no additional bytes.
The mutants are not equivalent — direct calls prove a real behavioural difference:

```
pristine             rc=0 agreed=['S002'] disputed=[]
review_sets:bool:1   rc=0 agreed=['S001', 'S002'] disputed=[]   (admits a report that does not name the reviewer)
review_sets:not:2    rc=0 agreed=[] disputed=[]                (drops every non-empty report)
```

`FT01`–`FT05` need no tripwire: none of their mutants raises in an earlier selftest case.

## Sweep evidence

Whole group, no `--ids` (`/tmp/tameshi-r47-T47HardFreshText/sweep.txt`):

```
$ python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardFreshText/h.py --group freshness
101 MUT lines: killed 68, survived 41, crashed 2
10 NEUTRAL lines: git:commute:0, grade:commute:0..4, measure:commute:0..2, live:commute:0 — all survived
diff vs .ufo/evidence/round-47/before/base-freshness.txt (111 ids): REGRESSIONS: none
gained kills (10): extract:int:0, extract:const:0, words:bool:0, words:cmp:0, words:int:0,
                   grade:cmp:9, grade:cmp:11, grade:int:0 (survived → killed)
                   review_sets:bool:1, review_sets:not:2 (crashed → killed)
```

Baseline for this group was 58 killed of 111; with this addition 68 of 111 (the two remaining
`crashed` ids belong to other seats).

## Commands and exit codes

| command | exit |
|---|---|
| `pool.py --enumerate .ufo/evidence/round-46/hardening/freshness-counter.py` (site map) | 0 |
| `assemble.py --group freshness --add …/T47HardFreshText.addition.py --out /tmp/tameshi-r47-T47HardFreshText/h.py` | 0 |
| `python3 /tmp/tameshi-r47-T47HardFreshText/h.py --selftest` (first run: own harness bug — 2-tuple from `_xT47HardFreshText_extract_pdf()` unpacked as 3) | 1 |
| same after fix (first run: stub wrote `%%s` instead of `%s`, so FT01 read `'%s'`) | 1 |
| same, final: `C1_R45_SELFTEST: cases=41 failed=0` / `VERDICT: PASS` | 0 |
| `pool.py --try h.py --group freshness --ids extract:int:0,extract:const:0,words:bool:0,words:cmp:0,words:int:0,grade:cmp:9,grade:cmp:11,grade:int:0,review_sets:bool:1,review_sets:not:2` → `PRISTINE pass`, 10× `killed` | 0 |
| `pool.py --try h.py --group freshness` (whole group, above) | 0 |
| 10× `python3 <mutated counter> --selftest` (per-mutant FAIL capture) | 1 each (the named FAIL line is the kill) |
| 3× direct `review_sets()` probe on pristine / `bool:1` / `not:2` (table above) | 0 |

Scratch only under `/tmp/tameshi-r47-T47HardFreshText/`. Nothing written in the lane except
this report and the one addition file; no git/jj command was run; no tool was installed
(nothing needed — the fake `pdftotext` is a 2-line `/bin/sh` stub under `tempfile`, and
`shutil.rmtree` removes it).

## Risks

- `FT01` prepends its stub directory to `os.environ['PATH']` for the duration of the call and
  restores it in a `finally`; the stub is `/bin/sh`-only, so it needs no PDF toolchain.
- The tripwire's import-time execution is confined to `--selftest`; if a future base counter
  moves the T17 fixture, `FT06/FT07` also run (harmlessly, PASS) from the extra itself, so the
  two kills survive that change.
- `FT04`/`FT05` reuse `_xHardGrade_row()` / `_xHardGrade_page()` read-only; if those round-46
  fixtures change, the shared-word counts (`2` and `3`) must be re-derived.
