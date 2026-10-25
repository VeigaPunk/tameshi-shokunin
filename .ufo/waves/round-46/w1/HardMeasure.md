seat: HardMeasure
item: authored `.ufo/waves/round-46/w1/HardMeasure.addition.py` — four measure()-level selftest cases for the round-45 freshness counter that kill declared survivors F05, F10, F11, F12.

# HardMeasure — C2 selftest additions F05,F10,F11,F12 (freshness)

## Deliverable

One file: `.ufo/waves/round-46/w1/HardMeasure.addition.py` (183 lines, sha256
`633ab4569af2da414e5981953e88a3d47a85f45955d66cfa4f15f400c25224af`). It defines exactly one
top-level `extra_HardMeasure()` plus 12 helpers named `_xHardMeasure_*`; nothing else in the lane
was written. No tool was installed or upgraded (no pacman, no uv, no npx).

Each case builds its own scratch git repo (`git init -q -b m` in a `tempfile.TemporaryDirectory`,
`rev-parse --show-toplevel` asserted equal to the scratch dir, one commit with
`-c user.name=t -c user.email=t@t`, `GIT_CONFIG_GLOBAL=GIT_CONFIG_SYSTEM=/dev/null`, every git call
`-C <scratch>`), then runs the counter CLI as
`[sys.executable, os.path.abspath(__file__), '--lane', <scratch>, '--rev', 'm']` and asserts on the
printed `C1_R45:` summary fields plus the exit code. No case asserts on the counter's source bytes:
the three `self_pin=0` fixtures (F05, F10, F11) simply leave `SELF_PATH` uncommitted, and the
`self_pin=1` fixture (F12) commits the running file bytes, which is how the counter itself defines
self_pin.

Fixture (all cases share it, one row per id, `n` rows):
`corpus/SOURCES.md` rows `| S0NN | docN — https://e.org/xNNN | docs | A | mutants detected | alphaNNN | valid | mined | 2026-10-25 | 180d | p |`
(11 pipe cells), one plain-text snapshot `snap/page.txt` whose line *i* is
`qNNN markerNNN mutants detected valid alphaNNN` (a 6-token quote, ≥2 shared content words with the
row's scope+anchor+teaches, not a substring of the row cells), a ledger entry per row with the
snapshot's sha256, reviews, `.ufo/waves/round-45/w2-results.json` seats `RevX`/`RevY`, and
`.ufo/waves/round-45/w2/Rev.md` naming each id and both reviewers.

## Per mutant

### F05 — `if counts[rid] != 1:` → `if False:` (duplicate-entry refusal)

Case: `F05_duplicate_entry_refused`.
Separating input: one population row `S001`, **two** ledger entries for `S001` (both otherwise
gradeable as verified), no reviews, `SELF_PATH` not committed (`self_pin=0`).
Pristine prints `invalid=2 verified=0` (both copies refused, `INVALID S001 duplicate entry` twice);
the mutant grades the id twice and prints `invalid=0 verified=1`.
Asserted: `population=1 entries=2 verified=0 invalid=2 fresh=0 C1_R45_PASS=false`, exit 1.

pristine fixture output:
```
INVALID S001 duplicate entry
INVALID S001 duplicate entry
C1_R45: self_pin=0 population=1 entries=2 verified=0 drifted=0 unreachable=0 invalid=2 unreviewed=0 disputed=0 fresh=0 score=0 target=50 rev=m C1_R45_PASS=false
```
mutant output on the same fixture:
```
C1_R45: self_pin=0 population=1 entries=2 verified=1 drifted=0 unreachable=0 invalid=0 unreviewed=1 disputed=0 fresh=0 score=0 target=50 rev=m C1_R45_PASS=false
```
mutant selftest: `FAIL F05_duplicate_entry_refused verified=1 want=0 invalid=0 want=2`

### F10 — `fresh = len(agreed - disputed)` → `len(agreed)` (dispute sinks agree in measure)

Case: `F10_dispute_sinks_agree`.
Separating input: one verified row `S001` with an `agree` review by `RevX` and a `dispute` review by
`RevY`, both backed by the committed report and both reviewers present with non-empty output;
`self_pin=0`.
Pristine prints `disputed=1 fresh=0 score=0`; the mutant prints `disputed=1 fresh=1 score=10`.

pristine:
```
DISPUTED S001
C1_R45: self_pin=0 population=1 entries=1 verified=1 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=1 fresh=0 score=0 target=50 rev=m C1_R45_PASS=false
```
mutant:
```
C1_R45: self_pin=0 population=1 entries=1 verified=1 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=1 fresh=1 score=10 target=50 rev=m C1_R45_PASS=false
```
mutant selftest: `FAIL F10_dispute_sinks_agree fresh=1 want=0 score=10 want=0`

### F11 — `passed = self_pin == 1 and fresh >= TARGET` → `passed = fresh >= TARGET` (self_pin required)

Case: `F11_self_pin_gates_pass`.
Separating input: `TARGET` (50) verified+agreed rows and **no counter bytes at `SELF_PATH`**, i.e.
the observable `self_pin=0` state. This is the smallest fixture that reaches the real floor with
self_pin unpinned; at any smaller `fresh` the two predicates agree, so no smaller input separates.
Pristine prints `self_pin=0 … fresh=50 score=10 C1_R45_PASS=false` (exit 1); the mutant prints
`C1_R45_PASS=true` and exits 0.

pristine:
```
C1_R45: self_pin=0 population=50 entries=50 verified=50 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=0 fresh=50 score=10 target=50 rev=m C1_R45_PASS=false
```
mutant:
```
C1_R45: self_pin=0 population=50 entries=50 verified=50 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=0 fresh=50 score=10 target=50 rev=m C1_R45_PASS=true
```
mutant selftest: `FAIL F11_self_pin_gates_pass exit=0 want=1 C1_R45_PASS=true want=false`

### F12 — `passed = self_pin == 1 and fresh >= TARGET` → `… fresh >= 0` (TARGET 50 floor)

Case: `F12_target_50_floor`.
Separating input: one verified+agreed row with the running counter bytes committed at `SELF_PATH`
(`self_pin=1`), so `fresh=1` is below `TARGET=50`.
Pristine prints `self_pin=1 … fresh=1 score=10 target=50 C1_R45_PASS=false` (exit 1); the mutant
prints `C1_R45_PASS=true` and exits 0.

pristine:
```
C1_R45: self_pin=1 population=1 entries=1 verified=1 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=0 fresh=1 score=10 target=50 rev=m C1_R45_PASS=false
```
mutant selftest: `FAIL F12_target_50_floor exit=0 want=1 C1_R45_PASS=true want=false`

## Helper output (verbatim)

```
$ python3 .ufo/evidence/round-46/hardening/assemble.py --group freshness \
    --add .ufo/waves/round-46/w1/HardMeasure.addition.py --out /tmp/tameshi-r46-HardMeasure/hard.py
wrote /tmp/tameshi-r46-HardMeasure/hard.py (1 additions)

$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/hardening/try-mutants.py \
    --group freshness --file /tmp/tameshi-r46-HardMeasure/hard.py
PRISTINE pass VERDICT: PASS
MUTANT F01 mutant survived
MUTANT F02 mutant survived
MUTANT F03 mutant survived
MUTANT F04 mutant survived
MUTANT F05 mutant killed
MUTANT F06 mutant survived
MUTANT F07 mutant survived
MUTANT F08 mutant survived
MUTANT F09 mutant survived
MUTANT F10 mutant killed
MUTANT F11 mutant killed
MUTANT F12 mutant killed
MUTANT F13 mutant survived
MUTANT F14 mutant survived
MUTANT F15 mutant survived
MUTANT FN1 neutral survived
MUTANT FN2 neutral survived
MUTANT FN3 neutral survived
```

## Tally (`--selftest` on the assembled hardened file)

```
PASS T1_good_verified … PASS T19_quote_copied_from_row got=invalid (quote copied from row)
PASS F05_duplicate_entry_refused
PASS F10_dispute_sinks_agree
PASS F11_self_pin_gates_pass
PASS F12_target_50_floor
C1_R45_SELFTEST: cases=23 failed=0
VERDICT: PASS
```
exit 0; the 19 round-45 cases plus 4 additions = 23. Three consecutive runs printed the same two
lines (`cases=23 failed=0`, `VERDICT: PASS`); `ls -d /tmp/tameshi-r46-hardmeasure-* | wc -l` = 0
afterwards (no scratch repos left behind).

## Isolation matrix (per-mutant selftest, mutated copy run in /tmp)

```
F01  mutant   rc=0 fails=[]
F02  mutant   rc=0 fails=[]
F03  mutant   rc=0 fails=[]
F04  mutant   rc=0 fails=[]
F05  mutant   rc=1 fails=['FAIL F05_duplicate_entry_refused verified=1']
F06  mutant   rc=0 fails=[]
F07  mutant   rc=0 fails=[]
F08  mutant   rc=0 fails=[]
F09  mutant   rc=0 fails=[]
F10  mutant   rc=1 fails=['FAIL F10_dispute_sinks_agree fresh=1']
F11  mutant   rc=1 fails=['FAIL F11_self_pin_gates_pass exit=0']
F12  mutant   rc=1 fails=['FAIL F12_target_50_floor exit=0']
F13  mutant   rc=0 fails=[]
F14  mutant   rc=0 fails=[]
F15  mutant   rc=0 fails=[]
FN1  neutral  rc=0 fails=[]
FN2  neutral  rc=0 fails=[]
FN3  neutral  rc=0 fails=[]
```
Each of the four assigned mutants fails exactly its own case and no other; every other declared
mutant of the group and all three neutral controls still pass. No case relies on a mutant being
killed by byte pinning.

## Notes / risks

- `F11_self_pin_gates_pass` reads the counter's `TARGET` global (`n = TARGET`) instead of hard-coding
  50, so it stays a floor test if the constant is ever changed; it is the only case with 50 rows and
  it costs ~0.15 s (104 `git show` calls in the counter run). Whole selftest: 0.35 s.
- Cases assert on the counter's printed `C1_R45:` fields (`invalid`, `verified`, `fresh`, `score`,
  `population`, `entries`, `target`, `C1_R45_PASS`) and its exit code, i.e. the same fields the C2
  contract requires the hardened counter to keep printing.
- `git version 2.56.0`, `Python 3.14.8`.
- Unrun (not mine): the deciding `mutate.py --lane … --rev …` run, the C2 equivalence check against
  the round-45 data revision, and every build/lint/test gate — all belong to the L1's deciding run.
