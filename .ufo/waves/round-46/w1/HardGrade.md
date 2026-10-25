seat: HardGrade
item: selftest addition killing the three declared freshness survivors F01 (snapshot-absent reason), F02 (25-token quote upper bound), F03 (quote present in snapshot) for the round-45 freshness counter, without changing counter behaviour and without killing the neutral mutants.

## Deliverable

`.ufo/waves/round-46/w1/HardGrade.addition.py` (59 lines, sha256
`852f360b8b94bee806abcb268c2cc02f505ecec27b899a77fdeb4ac52f4072fa`):
exactly one top-level `extra_HardGrade()` (verified: `grep -c '^def extra_'` = 1) plus four
helpers named `_xHardGrade_*` (`row`, `page`, `quote26`, `quote10_absent`). It calls the
counter's own `grade()` with in-memory fixture dicts and byte strings only: it never reads
`__file__`, `SELF_PATH` or any source text, so no case can be killed by pinning source bytes.
No imports, no subprocess, no scratch repo: all three rules are `grade()`-level, not
`measure()`-level, so the smallest fixture is a dict + bytes triple.

`extra_HardGrade()` returns `(cases, failed)` = `(3, 0)` on the pristine counter and prints one
`PASS <case>` / `FAIL <case> got=... want=...` line per case. Each case compares the full
`(state, reason)` tuple returned by `grade()`, which is exactly what `measure()` prints as
`INVALID <id> <reason>` / `DRIFTED <id>`.

## Per mutant: case, separating input, helper evidence

| id | case | separating input | pristine | mutant |
|---|---|---|---|---|
| F01 | `F01_snapshot_absent_reason` | valid `drifted` entry (url matches, opened 2026-10-25) with `raw_sha256 = sha256(b'')` and `raw = None` | `('invalid', 'snapshot absent')` | `('drifted', 'ok')` |
| F02 | `F02_quote_upper_bound_25` | 26-token quote that IS verbatim inside the snapshot page, shares 4 content words (flaky, failures, cluster, same) with the row, and is not a substring of the row cells | `('invalid', 'quote length 26')` | `('verified', 'ok')` |
| F03 | `F03_quote_absent_from_snapshot` | 10-token quote absent from the snapshot, shares 4 content words with the row, not copied from the row cells, 6..25 tokens | `('invalid', 'quote absent')` | `('verified', 'ok')` |

Why each fixture is not masked by a sibling rule (the reason the round-45 cases survived):

- F01 — `T9_snapshot_absent` already passes `raw=None` but only asserts the state `invalid`,
  which the mutant also produces (`raw = b''` falls into the hash check). My entry's
  `raw_sha256` is the digest of the empty byte string, which is what an empty snapshot file
  hashes to, so the mutated fall-through matches the hash and reaches the `drifted` return:
  the observable state itself flips (`drifted` vs `invalid`), not only the message. The
  fixture is reachable from `measure()`: `load_snapshot` returns `None` for an absent snapshot
  path and passes it straight to `grade()`.
- F02 — `T5_quote_too_long` uses 26 copies of `mutants`, which is absent from the page, so the
  mutant is masked by `quote absent`. My 26-token quote is present verbatim in the page
  (`<p>Flaky failures cluster inside the same job because the rerun repeats one order of the
  tests only and the second attempt hides the ordering defect entirely from the report.</p>`),
  the entry's `raw_sha256` is `sha256(page)` so the hash rule passes, and the row's `teaches`
  cell (`flaky failures cluster in the same job`) gives 4 shared words, so with the bound
  widened to 26 the mutant reaches `verified` while the pristine rule refuses at 26.
- F03 — `T4_quote_absent` uses `The mutation score is computed by the moon and stars`, which
  shares only 1 content word (`score`) with the row, so the mutant is masked by
  `overlap 1`. My absent quote (`Flaky failures never appear when the same job reruns alone`)
  shares 4 content words, is 10 tokens, is not copied from the row, and its `raw_sha256` is
  `sha256(page)`, so with `if False:` the only remaining rules all pass and the mutant reaches
  `verified`.

## Commands and exact output

Assembly (helper, exact):

```
$ python3 .ufo/evidence/round-46/hardening/assemble.py --group freshness \
    --add .ufo/waves/round-46/w1/HardGrade.addition.py --out /tmp/tameshi-r46-HardGrade/hard.py
wrote /tmp/tameshi-r46-HardGrade/hard.py (1 additions)
```

Pristine selftest of the hardened copy (scratch path, `/tmp/tameshi-r46-HardGrade/hard.py`,
sha256 `ef4f98498d9d18aa93fab26a9f7de70c248fed5ebcb706951ad9a8fcc3e04566`; orig copy
`orig.py` sha256 `ba64041f49ffcf15bb0d881604a5fe3ccf9d24e56f72bef055035fbe3d27c6ed`):

```
$ python3 /tmp/tameshi-r46-HardGrade/hard.py --selftest ; echo EXIT=$?
... (T1..T19 all PASS, as in round 45)
PASS F01_snapshot_absent_reason got=('invalid', 'snapshot absent') want=('invalid', 'snapshot absent')
PASS F02_quote_upper_bound_25 got=('invalid', 'quote length 26') want=('invalid', 'quote length 26')
PASS F03_quote_absent_from_snapshot got=('invalid', 'quote absent') want=('invalid', 'quote absent')
C1_R45_SELFTEST: cases=22 failed=0
VERDICT: PASS
EXIT=0
```

Tally: `cases=22 failed=0`, `VERDICT: PASS`, exit 0 (19 round-45 cases + my 3; the assembler's
`len(cases) + 4 + extra_cases` label is unchanged).

Mutant sweep (helper, exact, full output):

```
$ python3 .ufo/evidence/round-46/hardening/try-mutants.py --group freshness \
    --file /tmp/tameshi-r46-HardGrade/hard.py
PRISTINE pass VERDICT: PASS
MUTANT F01 mutant killed
MUTANT F02 mutant killed
MUTANT F03 mutant killed
MUTANT F04 mutant survived
MUTANT F05 mutant survived
MUTANT F06 mutant survived
MUTANT F07 mutant survived
MUTANT F08 mutant survived
MUTANT F09 mutant survived
MUTANT F10 mutant survived
MUTANT F11 mutant survived
MUTANT F12 mutant survived
MUTANT F13 mutant survived
MUTANT F14 mutant survived
MUTANT F15 mutant survived
MUTANT FN1 neutral survived
MUTANT FN2 neutral survived
MUTANT FN3 neutral survived
```

All three assigned ids `killed`; all three neutral mutants `survived`; pristine `pass`.
F04-F15 are other seats' assigned ids and remain survivors here (untouched by this addition).

Isolation (each mutated copy run separately, showing exactly one failing case per mutant):

```
F01 fail | FAIL F01_snapshot_absent_reason got=('drifted', 'ok') want=('invalid', 'snapshot absent')   C1_R45_SELFTEST: cases=22 failed=1  rc=1
F02 fail | FAIL F02_quote_upper_bound_25 got=('verified', 'ok') want=('invalid', 'quote length 26')     C1_R45_SELFTEST: cases=22 failed=1  rc=1
F03 fail | FAIL F03_quote_absent_from_snapshot got=('verified', 'ok') want=('invalid', 'quote absent') C1_R45_SELFTEST: cases=22 failed=1  rc=1
```

## Behaviour preservation

The addition defines only new names (`extra_HardGrade`, `_xHardGrade_*`) and touches no
round-45 line; `assemble.py` changes only `SELF_PATH` and the selftest tally, both by design.
No counter-mode run was made by me (bounds: seats run counters only as `--selftest` or against
the two named revs into scratch, and equivalence/`measure()` field comparison is the L1's
deciding run). The round-45 data-rev equivalence run was therefore left unrun by this seat.

## Tooling

No tool installed, upgraded or removed. pacman untouched. All scratch under
`/tmp/tameshi-r46-HardGrade/` (`orig.py`, `hard.py`); no fixture git repo was needed.
Lane checkout untouched except this deliverable and this report; no git/jj command run in the
lane.

## Risks / blockers

- None blocking. One judgement call recorded: F01's kill uses `raw_sha256 = sha256(b'')` so the
  mutated fall-through reaches the `drifted` return; the fixture is a legal ledger state (an
  empty snapshot file hashed, then absent) and the flip is in the state, not only in the reason
  string.
