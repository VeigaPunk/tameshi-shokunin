# T48A2MutFalsifiers — mutation audit of the QUALITY 94-96 falsifier blocks

Seat: T48A2MutFalsifiers (a2w1, godspeed). Item: mutation-audit
`.ufo/evidence/round-48/quality/falsifiers.sh` (the falsifiers of QUALITY criteria 94-96).
Every run below is a scratch probe, never a verdict. The lane checkout was only read; the
only lane write is this report file.

## Method

- Scratch: `/fast/scratch/hyaku/tameshi-r48/T48A2MutFalsifiers` (deleted before finishing;
  nothing under /tmp). Disk-guard before the pass: 602.0G free on `/fast/scratch/hyaku`.
- `S/lane` = `git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin`, then
  `git -C S/lane checkout -q --detach c7586b9a10effc63b4bd327f976edc094c1bdc17`;
  `rev-parse HEAD` returned the content revision and `cat-file -t` returned `commit`.
- Detector: byte copy of `quality/falsifiers.sh` (lane original sha256
  `371c64323b2519a2e3a0cf67ece93afbec520b5fb90265334aeaa1a9ff9de84a`) with ONLY line 4
  edited: `L=/fast/scratch/hyaku/tameshi-r48/T48A2MutFalsifiers/lane`. Invoked as
  `HYAKU_SCRATCH=$S/tmp bash $S/falsifiers.sh` (the script's own `mktemp -p $HYAKU_SCRATCH`
  stays in scratch).
- Script line map (42 lines, counted from the verbatim copy): `reject_check` 9-21 (the
  cite+`Flip:` condition is line 15); block 94 = 22-31 (good-input gate lines 29 and 31);
  block 95 = 32-35 (`R=` 33, the deciding `if` 35); block 96 = 36-42 (`pa`/`pb` 39-40, the
  deciding `if` with the `under_tmp` conjunct 42).
- Mutated inputs restored from saved pristine copies after every run; restoration proven by
  sha256 equality (table below) plus a final fully-restored run. Pristine input hashes:
  lesson `a6d5fd94e0933610…`, `before/c1-at-freeze.stdout` `27ca1e91cc61f08c…`,
  `after/c1.stdout` `b56a8c2a86166404…`, `calibration/measure.py`
  `572a5670deb7edb0…` (equals the freeze-2.json counter sha).

## Baseline (pristine bytes at c7586b9a)

```
WEAK-CITE ### Reject — package entry `r8-predictive-test-selection-cost.md`
rejects=1 weak=1
rejects=2 weak=0
CRITERION-94-FALSIFIER-OK
grep: /fast/scratch/hyaku/tameshi-r48/T48A2MutFalsifiers/lane/.ufo/evidence/round-48/control/c1-controls.stdout: No such file or directory
grep: /fast/scratch/hyaku/tameshi-r48/T48A2MutFalsifiers/lane/.ufo/evidence/round-48/control/c1-controls.stdout: No such file or directory
CRITERION-95-FALSIFIER-VACUOUS
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 9/9 pass|0
CRITERION-96-FALSIFIER-OK
```
(exit 0)

- Block 94 OK: the lesson's two `### Reject` blocks (`corpus/lessons/round-48.md:91-96`,
  cite `CORPUS.md rule 2` + `Flip:` at :96; `:98-102`, cite `QUALITY 10` at :101 + `Flip:`
  at :102) pass `reject_check`.
- Block 95 VACUOUS at this revision: its only input
  `.ufo/evidence/round-48/control/c1-controls.stdout` does not exist at `c7586b9a` — nor at
  the tip `17cc5ce` at any of my four checks (`git -C <lane> ls-tree --name-only HEAD
  .ufo/evidence/round-48/control/` lists only `c2-controls.*` + `run-controls.py`;
  `after/` absent). Disclosed-pending per `LOG.md:2364`. A baseline failure is
  inconclusive, not a killed mutant — see F2 for how M2/M3 were still tested.
- Block 96 OK: `P1=ENVDIFF_SELFTEST: 2/9 pass|1` (`before/c1-at-freeze.stdout:18`) differs
  from `P1=ENVDIFF_SELFTEST: 9/9 pass|0` (`after/c1.stdout:18`), and `under_tmp` is present
  in the counter (4 occurrences: `measure.py:101` def, `:112` scratch_root call, `:395`
  measure work guard, `:836` selftest case name `T63_work_under_tmp_refused`).

## Mutations

| # | Mutant (input mutated) | Attacks | Expected | Observed | Verdict |
|---|---|---|---|---|---|
| M1a | lesson copy: `Flip:` clause deleted from `### Reject — staged copies…` (round-48.md:96) | block 94 good-input gate (falsifiers.sh:29,31) | 94 → VACUOUS | `WEAK-CITE ### Reject — staged copies…`, `rejects=2 weak=1`, `CRITERION-94-FALSIFIER-VACUOUS`; 95/96 unchanged | killed |
| M1b | lesson copy: `; QUALITY 10` deleted from `### Reject (re-stated)…` (round-48.md:101) | block 94 good-input gate | 94 → VACUOUS | `WEAK-CITE ### Reject (re-stated)…`, `weak=1`, `CRITERION-94-FALSIFIER-VACUOUS` | killed |
| M2 | c1-controls.stdout (synthetic fixture): CTL_B `total=1` → `total=0` | block 95 CTL_B conjunct (falsifiers.sh:35, ` total=[1-9]`) | 95 → VACUOUS | `CRITERION-95-FALSIFIER-VACUOUS`; 94/96 unchanged | killed (on fixture; F2) |
| M3 | c1-controls.stdout (synthetic fixture): CTL_E `total=0` → `total=1` | block 95 CTL_E conjunct (falsifiers.sh:35, ` total=0 `) | 95 → VACUOUS | `CRITERION-95-FALSIFIER-VACUOUS` | killed (on fixture; F2) |
| M4 | `after/c1.stdout:18`: `P1=ENVDIFF_SELFTEST: 9/9 pass|0` → `2/9 pass|1` (equalizes pa/pb) | block 96 pa≠pb conjunct (falsifiers.sh:42) | 96 → VACUOUS | `tmp-work`/`var-tmp-work` both `2/9 pass|1`, `CRITERION-96-FALSIFIER-VACUOUS` | killed |
| M5a | counter copy: `under_tmp` guard deleted (def :101-103, scratch_root call :112, measure guard :395-397); selftest case name `T63_work_under_tmp_refused` (:836) left in place | block 96 `under_tmp` conjunct (falsifiers.sh:42) | 96 → VACUOUS | **`CRITERION-96-FALSIFIER-OK`** — `grep -c under_tmp` = 1 (the case name); mutated copy ast-parses | **SURVIVED → F1** |
| M5b | M5a plus case name renamed (`T63_work_tmp_refused`): 0 occurrences left (ast-parse clean) | block 96 `under_tmp` conjunct | 96 → VACUOUS | `CRITERION-96-FALSIFIER-VACUOUS` | killed |

Every mutated run also shows the two non-target blocks unchanged — no cross-talk between
blocks.

## Run outputs (verbatim, decisive lines elided only where marked)

M1a (after the Flip deletion; lesson restored after, hash `a6d5fd94…`):
```
WEAK-CITE ### Reject — package entry `r8-predictive-test-selection-cost.md`
rejects=1 weak=1
WEAK-CITE ### Reject — staged copies of the four C2 documents (`merge/tameshi/SOURCES.append.md`)
rejects=2 weak=1
CRITERION-94-FALSIFIER-VACUOUS
grep: …/lane/.ufo/evidence/round-48/control/c1-controls.stdout: No such file or directory  (x2)
CRITERION-95-FALSIFIER-VACUOUS
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 9/9 pass|0
CRITERION-96-FALSIFIER-OK
```

M1b (after the `; QUALITY 10` deletion; lesson restored after, hash `a6d5fd94…`):
```
WEAK-CITE ### Reject — package entry `r8-predictive-test-selection-cost.md`
rejects=1 weak=1
WEAK-CITE ### Reject (re-stated) — package entry `r8-predictive-test-selection-cost.md`
rejects=2 weak=1
CRITERION-94-FALSIFIER-VACUOUS
grep: …/control/c1-controls.stdout: No such file or directory  (x2)
CRITERION-95-FALSIFIER-VACUOUS
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 9/9 pass|0
CRITERION-96-FALSIFIER-OK
```

M4 (after equalizing B's P1 tuple; receipt restored after, hash `b56a8c2a…`):
```
rejects=1 weak=1 / rejects=2 weak=0
CRITERION-94-FALSIFIER-OK
grep: …/control/c1-controls.stdout: No such file or directory  (x2)
CRITERION-95-FALSIFIER-VACUOUS
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
CRITERION-96-FALSIFIER-VACUOUS
```

M5a (guard deleted, case name left; counter restored after, hash `572a5670…`):
```
parse-ok
1
rejects=1 weak=1 / rejects=2 weak=0
CRITERION-94-FALSIFIER-OK
grep: …/control/c1-controls.stdout: No such file or directory  (x2)
CRITERION-95-FALSIFIER-VACUOUS
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 9/9 pass|0
CRITERION-96-FALSIFIER-OK        ← survivor
```

M5b (all four occurrences gone, `grep -c` = 0, ast-parse clean; counter restored after,
hash `572a5670…`):
```
parse-ok
0
rejects=1 weak=1 / rejects=2 weak=0
CRITERION-94-FALSIFIER-OK
grep: …/control/c1-controls.stdout: No such file or directory  (x2)
CRITERION-95-FALSIFIER-VACUOUS
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 9/9 pass|0
CRITERION-96-FALSIFIER-VACUOUS
```

Fixture baseline (synthetic `c1-controls.stdout` in the clone, sha256
`8a1f5544bbbe9f071c8e69c81d085e74a707d231279736b1d613f2e68ffa4e73`):
```
rejects=1 weak=1 / rejects=2 weak=0
CRITERION-94-FALSIFIER-OK
CTL_B C1_R48: self_pin=1 stmts_pin=1 statements=22 rounds=3 append_only=1 unpinned=0 total=1 mismatches=1 … rev=1111111111111111111111111111111111111111 C1_R48_PASS=false
CRITERION-95-FALSIFIER-OK
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 9/9 pass|0
CRITERION-96-FALSIFIER-OK
```

M2 (CTL_B `total=1` → `total=0`):
```
rejects=1 weak=1 / rejects=2 weak=0
CRITERION-94-FALSIFIER-OK
CTL_B C1_R48: … unpinned=0 total=0 mismatches=1 … C1_R48_PASS=false
CRITERION-95-FALSIFIER-VACUOUS
tmp-work / var-tmp-work unchanged
CRITERION-96-FALSIFIER-OK
```
(Disclosure: the fixture's in-run restore cp failed once — `restore-rc=1` — because the
pristine fixture copy had not been saved yet; the fixture was then restored from the saved
copy and hash-verified `8a1f5544…` before M3.)

M3 (CTL_E `total=0` → `total=1`; fixture restored after, hash `8a1f5544…`):
```
rejects=1 weak=1 / rejects=2 weak=0
CRITERION-94-FALSIFIER-OK
CTL_B C1_R48: … total=1 … C1_R48_PASS=false      (pristine line again)
CRITERION-95-FALSIFIER-VACUOUS
tmp-work / var-tmp-work unchanged
CRITERION-96-FALSIFIER-OK
```

Final restored run (fixture removed; all inputs byte-identical to pristine):
```
rejects=1 weak=1 / rejects=2 weak=0
CRITERION-94-FALSIFIER-OK
grep: …/control/c1-controls.stdout: No such file or directory  (x2)
CRITERION-95-FALSIFIER-VACUOUS
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 9/9 pass|0
CRITERION-96-FALSIFIER-OK
falsifiers-rc=0
git -C S/lane status --porcelain   → empty
```

## Findings

### F1 [medium] — SURVIVOR: block 96's `under_tmp` conjunct is a bare string grep; block 96 stays OK while the counter's /tmp refusal is deleted

`falsifiers.sh:42` ends `… && grep -q 'under_tmp' "$E/calibration/measure.py"` — token
presence anywhere in the file, not the guard's existence. Deleting the guard (`def
under_tmp` at `measure.py:101-103`, the `scratch_root` call at `:112`, the `measure` work
guard at `:395-397`; the mutated copy ast-parses, so it is a plausible defective counter,
not garbage) leaves the selftest case-name string `T63_work_under_tmp_refused` (pristine
`measure.py:836`; line 828 in the mutated copy) — `grep -c under_tmp` → 1 — and block 96
still prints `CRITERION-96-FALSIFIER-OK` (M5a output above).

- Command that shows it: `HYAKU_SCRATCH=$S/tmp bash $S/falsifiers.sh` (M5a output) and
  `grep -c under_tmp <mutated measure.py>` → 1.
- So criterion 96's falsifier sentence ("…and the round-48 counter refuses a `/tmp` work
  dir (`under_tmp`)", `corpus/QUALITY.md` §Criterion 96 falsifier paragraph, round-48
  block at `:1390-1434`) is satisfied by an identifier that merely mentions the token.
- Sharpening option (the L1's call, not applied by me): anchor the conjunct to the guard
  itself (e.g. require `def under_tmp` plus a call site) or assert the behavior through the
  committed selftest case (T63, `.ufo/evidence/round-48/selftest/c1-r48-selftest.stdout:74`
  per T48W2RevQuality).
- The counter copy at `c7586b9a` is the frozen counter (sha256 `572a5670…` = freeze-2.json),
  so this is a falsifier-precision finding, not a counter defect. The full deletion (M5b)
  is killed, so the conjunct is not vacuous — it is merely weaker than it reads.

### F2 [medium] — block 95 had no testable baseline at the pinned revision; M2/M3 verified on a clearly-labeled synthetic fixture; real-receipt confirmation pending on the L1

`control/c1-controls.stdout` is absent at `c7586b9a` (baseline block 95 VACUOUS with the two
grep errors above) and had not landed at tip `17cc5ce` at any of my four checks during the
seat. Per the kill-rule discipline, M2/M3 at that revision would be inconclusive, so I built
a synthetic fixture at `.ufo/evidence/round-48/control/c1-controls.stdout` in the scratch
clone (sha256 `8a1f5544bbbe9f071c8e69c81d085e74a707d231279736b1d613f2e68ffa4e73`), with the
five CTL lines in the counter's exact label format (`measure.py:575-578`:
`C1_R48: self_pin=… total=%d mismatches=… base=… rev=… C1_R48_PASS=…`):

```
CTL_A C1_R48: … total=22 … unparsed=22 … rev=473336d9d789f6081195e7376d17836a24666bc3 C1_R48_PASS=false
CTL_B C1_R48: … total=1 mismatches=1 … rev=1111111111111111111111111111111111111111 C1_R48_PASS=false
CTL_C C1_R48: … unattested=22 total=22 … C1_R48_PASS=false
CTL_D C1_R48: … dep_mismatch=22 total=22 … C1_R48_PASS=false
CTL_E C1_R48: … total=0 … rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C1_R48_PASS=true
```

With the fixture, the baseline is all-three-OK (output above); M2 and M3 each flip block 95
to VACUOUS — the detector's two conjuncts are each necessary, and neither passes vacuously.
The mutants changed only the `total=` value (M2 leaves `mismatches=1`, M3 leaves
`C1_R48_PASS=true` — internally inconsistent lines, disclosed; immaterial because the
detector reads only `total=`). When the L1's receipts commit lands the real
`control/c1-controls.stdout`, re-run `falsifiers.sh`: block 95 should print OK (CTL_B
total≥1, CTL_E total=0; the ` total=0 ` trailing-space match holds because `total=` is
followed by ` mismatches=` on the counter's label line, `measure.py:575`).

### F3 [low] — confirmation: falsifiers.sh exits 0 with a VACUOUS block

My baseline run ended `falsifiers-rc=0` while block 95 printed VACUOUS (the script has no
aggregate status; the last block's `if/echo` decides the exit code). Confirms
T48W2RevQuality F2 from an independent run: a consumer scripting on the exit code sees
success even when a block is vacuous.

### F4 [note] — block 96 context, not re-reported

The two block-96 receipts sit at different revisions (`before/c1-at-freeze.stdout:45`
rev=`9acfbe21…`, the round-47 freeze; `after/c1.stdout:45` rev=`8b0e15d2…`, the round-47
content) — already T48W2RevQuality F3; my equalization mutation (M4) did not need to touch
that. The detector compares only the extracted P1 tokens of the single
`PROFILES hermetic env-differential probe:` line per receipt (verified: exactly one such
line in each, both at `:18`), so any difference in the tuple (line or exit) fires.

## Restoration evidence

| file (scratch-clone path) | pristine sha256 | after restores |
|---|---|---|
| `corpus/lessons/round-48.md` | `a6d5fd94e09336106650756b3b08683eaa7c450c872857ff9eb117818e7086f2` | equal after M1a and M1b |
| `.ufo/evidence/round-47/after/c1.stdout` | `b56a8c2a861664046d6026a95dd452b00ec9331b00e5b523eeb9e0e0b6b37305` | equal after M4 |
| `.ufo/evidence/round-48/calibration/measure.py` | `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` (= freeze-2.json counter sha) | equal after M5a and M5b |
| `.ufo/evidence/round-47/before/c1-at-freeze.stdout` | `27ca1e91cc61f08caacd921636444dab7136b62cada044541ceed6efc38a45e1` | never mutated |
| synthetic `c1-controls.stdout` | `8a1f5544bbbe9f071c8e69c81d085e74a707d231279736b1d613f2e68ffa4e73` | equal after M2 and M3; removed before the final run |
| `falsifiers.sh` (lane original) | `371c64323b2519a2e3a0cf67ece93afbec520b5fb90265334aeaa1a9ff9de84a` | never mutated (the scratch copy differs only at line 4, the `L=` path) |

The final restored run reproduced the baseline exactly (94 OK, 95 VACUOUS with the two
absent-input grep errors, 96 OK, exit 0) and `git -C S/lane status --porcelain` was empty.

## Bounds, tooling, scratch

- Lane: read-only throughout (`git log`/`ls-tree`/`rev-parse`/`cat-file`/file reads). The
  `checkout --detach` ran in the scratch clone only. No git/jj mutating commands anywhere;
  no writes under `corpus/`, `tools/`, `SCORECARD.md`; the only lane write is this report
  file.
- No tools installed or upgraded (git/python3/coreutils only); pacman untouched.
- Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2MutFalsifiers` deleted before finishing.
- Timestamps: every lane-tip check during the seat returned `17cc5ce`; the deciding run was
  in flight throughout. All runs above are probes, not verdicts; I am not an author of what
  I attacked.
