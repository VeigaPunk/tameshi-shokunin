seat: MutC1Counter-2

# C1 freshness counter — mutation audit of `--selftest`

Ticket path said `.ufo/waves/round-45/w1/MutC1Counter.md`; sibling MutC1Counter-3 was assigned the identical path and seat name (duplicate spawn). Agreed in writing via agent message: -3 keeps `MutC1Counter.md`, this report lands at `MutC1Counter-2.md` to avoid clobbering.

## Scope and method

- Target: `.ufo/evidence/round-45/freshness/measure.py` (437 lines, lane sha256 `ba64041f49ffcf15bb0d881604a5fe3ccf9d24e56f72bef055035fbe3d27c6ed`), copied byte-exact to `/tmp/tameshi-r45-MutC1Counter/measure.py` (hashes equal before work).
- For each declared rule: ONE minimal disabling mutation in the scratch copy only, then `python3 measure.py --selftest`, then restore exact pristine bytes. Killed = selftest `VERDICT: FAIL` rc=1; survived = `VERDICT: PASS` rc=0 (an untested rule).
- Baseline pristine: `C1_R45_SELFTEST: cases=19 failed=0` / `VERDICT: PASS` rc=0 — detector sound, so verdicts are conclusive.
- Lane untouched except this report file; scratch only under `/tmp/tameshi-r45-MutC1Counter/` (`measure.py.orig`, `probe.py`, `probe2.py`, `out-*.txt`). No tool installs (python3/git already present; no pacman transaction).
- Bound compliance: every counter invocation was `--selftest` of the scratch copy. The measure()-level killer fixtures (T23-T25) run measure() only inside one `--selftest` invocation, against throwaway repos built per the fixture rule (`mkdtemp` → `git -C "$D" init -q` → `rev-parse --show-toplevel == $D` asserted → commit; all under `/tmp`), never against the lane or any lane revision.

## Battery: 31 probes — 18 killed, 13 SURVIVED

| Probe | Rule (measure.py site) | Mutation (old → new) | Selftest | Verdict |
|---|---|---|---|---|
| P01 | URL exact match (137-138) | `entry.get('url') != row['url']` → `False` | FAIL rc=1 (T2) | killed |
| P02 | opened >= 2026-10-25 (139-140) | `< MIN_OPENED` → `False` | FAIL rc=1 (T7) | killed |
| P02b | opened boundary | `<` → `<=` | FAIL rc=1 (T1) | killed |
| P03 | sha256 match (143-144) | digest compare → `False` | FAIL rc=1 (T3) | killed |
| P04 | verdict whitelist (147-148) | `verdict != 'holds'` → `False` | FAIL rc=1 (T16) | killed |
| P05a | quote length upper (151) | `or n > 25` → `or False` | PASS rc=0 | **SURVIVED** |
| P05b | quote length lower (151) | `n < 6` → `False` | FAIL rc=1 (T6 verifies) | killed |
| P05c | quote length whole rule | → `if False:` | FAIL rc=1 (T6) | killed |
| P05d | upper off-by-one | `n > 25` → `n > 26` | PASS rc=0 | **SURVIVED** |
| P05e | lower off-by-one | `n < 6` → `n < 5` | PASS rc=0 | **SURVIVED** |
| P06 | quote present (157-158) | `if quote not in text:` → `if False:` | PASS rc=0 | **SURVIVED** |
| P07 | quote-not-copied-from-row (159-161) | → `if False:` | FAIL rc=1 (T19) | killed |
| P08 | content-word overlap >= 2 (162-164) | → `if False:` | FAIL rc=1 (T8) | killed |
| P09 | unreachable needs evidence (136) | conditional → unconditional unreachable | FAIL rc=1 (T11) | killed |
| P10a | population: status mined (96) | `r['status'] == 'mined'` → `True` | FAIL rc=1 (T15) | killed |
| P10b | population: id <= 160 (96) | `<= MAX_ID` → `<= MAX_ID + 1` | FAIL rc=1 (T15 S161) | killed |
| P10c | population: URL present (96) | drop `and r['url']` | PASS rc=0 | **SURVIVED** |
| P10d | population: 0-3 leading spaces (60) | ROW_RE `{0,3}` → `{0,4}` | FAIL rc=1 (T15 S003) | killed |
| P11 | duplicate-entry refusal (241) | `if counts[rid] != 1:` → `if False:` | PASS rc=0 | **SURVIVED** |
| P12 | review: non-author (204) | drop `who == authors.get(rid) or` | PASS rc=0 | **SURVIVED** |
| P13a | wave-seat membership (204) | drop `or who not in seats` | FAIL rc=1 (T17 S008/RevZ) | killed |
| P13b | non-empty output (188-189) | drop output clause | FAIL rc=1 (T17 S008/RevZ) | killed |
| P13c | output `.strip()` boundary (189) | `.strip()` removed | PASS rc=0 | **SURVIVED** |
| P14 | report path prefix (206) | → `if False:` | PASS rc=0 | **SURVIVED** |
| P15a | report names id (209) | drop `re.search(...)` clause | FAIL rc=1 (T17 S006) | killed |
| P15b | report names reviewer (209) | drop `who not in text` | PASS rc=0 | **SURVIVED** |
| P16 | dispute sinks agree (213) | `elif ... 'dispute'` → `elif False:` | FAIL rc=1 (T17 S003) | killed |
| P17 | self_pin (221) | → `self_pin = 1` | PASS rc=0 | **SURVIVED** |
| X1 | pass gate TARGET=50 (60,256) | `TARGET = 50` → `0` | PASS rc=0 | **SURVIVED** |
| X2 | `fresh = agreed - disputed` (254) | → `len(agreed)` | PASS rc=0 | **SURVIVED** |
| X3 | review verdict whitelist (211-213) | `== 'agree'` → `True` | FAIL rc=1 (T17 disputed set) | killed |

## Why each survivor escapes (masking / coverage gap)

1. **measure() is never called by selftest** — every measure()-level predicate is untested: duplicate refusal (P11, :241), self_pin (P17, :221), TARGET gate (X1, :60/:256), `fresh = agreed - disputed` (X2, :254). The review_sets/grade units are tested; the composition is not.
2. **P05a/P05d (upper bound)**: T5's 26-token quote is absent from the fixture page, so any upper-bound relaxation is still rejected — via `quote absent`, not length. The 25/26 boundary is never exercised on a *present* quote.
3. **P05e (lower bound)**: T6 is 4 tokens; acceptance of a 5-token quote is untested.
4. **P06 (quote present)**: T4's absent quote is rejected one check later by `overlap 1`, so removing the presence check changes nothing.
5. **P10c (URL present)**: all four T15 rows carry URLs; a mined, in-range, URL-less row is never excluded.
6. **P12 (non-author)**: the only self-review (S002/ExecA) is rejected by `who not in text` — `ExecA` is absent from the fixture report text — not by authorship. The two rules accidentally cover each other; neither is isolated.
7. **P13c**: no whitespace-only-output seat exists; blank `''` and whitespace `'   '` are indistinguishable to the tests.
8. **P14 (prefix)**: S007's `/tmp/Rev.md` is rejected by missing text (`reports.get` → None), not by the `.ufo/waves/round-45/` prefix; no wrong-wave report with valid text exists.
9. **P15b (reviewer named)**: no case has a seat whose name is missing from its report text.

## Killer validation (proposed augmented selftest — validated, NOT applied to the lane)

One master patch to `selftest()` (`/tmp/tameshi-r45-MutC1Counter/probe2.py`): grade cases T20 (26-token otherwise-valid present quote → invalid), T21 (`score is detected mutants over`, 5 tokens → invalid), T22 (absent quote with overlap 5 → invalid); T15 gains a URL-less mined row S009; T17 gains named-author report text (ExecA), a whitespace-only-output seat RevT, a wrong-wave report `.ufo/waves/round-44/Old.md` with valid text, a reviewer-unnamed review (RevW), and matching verified ids; plus measure()-level T23/T24/T25 on throwaway fixture repos:

- `T23_measure_duplicate_refusal`: 55 valid agreed rows + duplicated S001 → expect `fresh=54 invalid=2 C1_R45_PASS=true` (pristine counts both duplicate entries invalid).
- `T24_measure_self_pin`: committed measure.py differs from running bytes by one byte, fresh=55 → expect `self_pin=0 C1_R45_PASS=false`.
- `T25_measure_dispute_and_target`: S001 agree-only, S002 carrying BOTH an agree and a dispute → expect `fresh=1 disputed=1 C1_R45_PASS=false` (kills both X2 and X1; the agreed/disputed id sets must overlap or `len(agreed)` is indistinguishable — first draft of this killer got that wrong and was corrected).

Results: pristine + killers → `cases=25 failed=0` / `VERDICT: PASS` rc=0 (no false alarm). Each survivor + killers → rc=1, killed by exactly its intended case: P05a/P05d←T20, P05e←T21, P06←T22, P10c←T15, P11←T23, P12/P13c/P14/P15b←T17, P17←T24, X1/X2←T25. 13/13 killed.

## Restoration evidence

- After every probe and killer run, `measure.py` was rewritten from pristine bytes and sha256 re-verified `== ba64041f49ffcf15bb0d881604a5fe3ccf9d24e56f72bef055035fbe3d27c6ed` (asserted in both drivers; a mismatch would have aborted).
- Final restored run: `--selftest` rc=0, `VERDICT: PASS`; restored sha `ba64041f…` (equals lane copy and work-start hash).
- Lane `measure.py` never written; lane checkout untouched except this report file.

## Verdict

The frozen selftest genuinely tests 18 of the 31 probed rule-points but leaves 13 surviving mutants: all four measure()-level predicates, the quote upper-length boundary, quote-presence, population URL-presence, the review non-author/prefix/reviewer-named rules (mutually masked rather than independently tested), and the whitespace-only-output boundary. The proposed augmented selftest above closes all 13 with no false alarms. Coverage finding only — no change made to the contract or the lane counter.
