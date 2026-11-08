# tameshi round 97 — frozen declarations (plan)

Lane `tameshi` (verification-fixture craft). Round 97, attempt 1. Base (lane tip at
round start): `07e50d6d0142b21e8443b5417b8edc4d1dd76455`, branch `master`.
Instrument commit (both tools + the C2 manifest): `917d7109c9c4e43dd8fd69e59b147181e2e94d85`.

Round 96 landed admitted but its non-author spot-check left two lane defects:
D-a — the report cites `.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt`, which is
absent from the object store at `8ed9c526`; the 50/50 battery verdict could only be attested
by a seat's re-grade, not re-derived from committed bytes. D-b — the revenger probe
("are the guards inert?") delivered nothing (R96L1 dead), so the round-96 checker's guards
have no measurement. This round closes both with two new instruments and declares **two
claims**, each frozen before any scored record exists.

Axes: depth + calibration (lane axes). C1 moves **calibration** (the lowest non-retired axis,
pinned 8): the round's self-assessment is re-derived from committed bytes instead of being
attested. C2 moves **operability**: a runnable matrix for the checker's guard edits.
The DoD control is the round-96 state at `07e50d6d`; the new revision is the round-97
records revision (`RECORDS_REV`, the commit that carries the tools, the manifest, the
receipts and the claims).

---

## Claims (frozen before data)

### C1 — calibration: the committed battery is re-derivable

- **Axis:** calibration (self-assessment quality: a record's verdict must be a function of
  committed bytes, not of a seat's re-grade).
- **Surface:** `.ufo/evidence/round-97/c1/battery-bind.py` reading, at `--rev`: the
  committed driver `.ufo/evidence/round-96/c1/controls-v96.py` (its `states()` and
  `EXPECT_EXTRA` are the oracle), the frozen counter
  `.ufo/evidence/round-96/c1/measure-v96.py` (its sha256 is the `counter=self` digest) and
  the 50 receipts under `.ufo/evidence/round-96/pre-freeze/controls/`.
- **Wording (frozen):** at the records revision R,
  `python3 -I .ufo/evidence/round-97/c1/battery-bind.py --lane . --rev R` prints
  `BATTERY states=50 matched=50 mismatched=0 missing=0` and exits 0; it reads the 50
  receipts as blobs at R (a receipt present only in the working tree is absent) and takes
  its expectations from the committed driver's `states()` and `EXPECT_EXTRA` at R; a
  receipt deleted from the index (but left in the working tree), a `counter_sha=` edit, an
  `exit=` edit and a `C1_R96_PASS=true` payload edit each print a nonzero `mismatched`
  count and exit 1; a `--driver-sha` value unequal to the driver blob's sha256 is refused
  `BATTERY_SETUP driver-sha-mismatch`, exit 2; at base `07e50d6d`
  `git grep -c 'BATTERY states='` prints nothing and
  `C1-summary.txt` is absent at `8ed9c526` (`git cat-file -e` exit 1).
- **Counter:** `python3 -I .ufo/evidence/round-97/c1/battery-bind.py --lane . --rev RECORDS_REV`
- **Battery:** `python3 -I .ufo/evidence/round-97/c1/battery-bind.py --selftest`
- **Predicate:** `BATTERY states=50 matched=50 mismatched=0 missing=0` (exit 0)
- **Before:** at base `07e50d6d` no committed tool prints a `BATTERY states=` line
  (`git grep -c 'BATTERY states='` empty) and the summary the round-96 report cites is
  absent at `8ed9c526`; the round-96 records carry the 50 receipts but no reader of them.
- **After:** the line above at R, exit 0, plus the five refusals and the selftest.
- **Kill rules:**
  - a: the line is printed while a named receipt is absent at R or its
    `counter_sha=`/`exit=`/payload does not satisfy the committed driver's own `grade()`;
  - b: a receipt that exists only in the working tree is counted `matched`;
  - c: a `--driver-sha` mismatch is graded instead of refused at setup;
  - d: the selftest cannot fail (a cheat case is reintroduced and still passes);
  - e: the driver blob at R is not the oracle the manifest's `states()` names (the reader
    substitutes its own expectations).
- **Declared limits:** the reader trusts the committed driver as the oracle; it verifies
  that the receipts satisfy it, not that the driver's expectations are the right ones. A
  receipt is still a producer's claim: a hand-written receipt carrying the right
  `counter_sha=` and payload cannot be distinguished from a real run without re-executing
  the state (round-96 F1, unchanged).

### C2 — operability: the guard-inertia matrix

- **Axis:** operability (a runnable matrix; it produces its stated per-row outcome).
- **Surface:** `.ufo/evidence/round-97/c2/guard-inertia.py` + the committed manifest
  `.ufo/evidence/round-97/c2/guard-inertia.json`, applied to the round-96 checker blob
  `.ufo/evidence/round-96/conjunct-disposition-v96.py` at `--rev`.
- **Wording (frozen):** at the records revision R,
  `python3 -I .ufo/evidence/round-97/c2/guard-inertia.py --lane . --rev R` prints
  `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0` and exits 0; for each of the
  10 manifest rows it applies exactly one exact-string edit to the checker blob at R
  (refusing a no-op with `GUARD_SETUP edit-no-op` and an ambiguous anchor with
  `GUARD_SETUP edit-ambiguous`, each exit 2), runs the pristine and the mutant checker
  against the same fresh fixture store and the same arguments, and reports `killed` only
  when the pristine run exits with the row's declared exit and prints its declared token
  and the mutant run's exit differs or loses that token, and `limit` only when the two runs
  are identical in exit and declared token; a row whose observed class differs from its
  frozen `expect` makes `unmet` nonzero and exits 1; at base `07e50d6d`
  `git grep -c 'GUARD_INERTIA'` prints nothing.
- **Counter:** `python3 -I .ufo/evidence/round-97/c2/guard-inertia.py --lane . --rev RECORDS_REV`
- **Battery:** `python3 -I .ufo/evidence/round-97/c2/guard-inertia.py --selftest`
- **Predicate:** `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0` (exit 0)
- **Before:** at base no committed tool prints a `GUARD_INERTIA` line; round 96's R96M1
  mutation matrix covers the counter (`measure-v96.py`), not the checker's guards, and the
  revenger probe R96L1 delivered nothing (spot-check D-b).
- **After:** the line above at R, exit 0; the selftest 7/7; a manifest whose killed row is
  declared `limit` prints `survived=1` and exits 1; a no-op edit is refused exit 2.
- **Kill rules:**
  - a: the pristine and the mutant run against different stores, revisions or arguments;
  - b: a no-op or ambiguous edit is applied instead of refused;
  - c: a row whose two runs are identical is counted `killed`;
  - d: a `limit` row names no measured mechanism;
  - e: the checker blob at R is not the one the manifest was measured against (digest pin);
  - f: the tool prints the summary without running every row.
- **Declared limits:** the fixture store is four files (a counter stub, a manifest, a claims
  digest and receipts); a guard whose effect needs the real 50-state receipts is out of
  scope. The matrix measures one exact edit per guard, not two-edit combinations; a guard
  killed only by a combination is not counted (and `git-absolute`/`verify-quiet` are
  measured `limit` for exactly that reason).

## Pre-registered controls (executed and committed before this freeze)

Driver: `.ufo/evidence/round-97/controls97.py` (run with
`--lane . --base 07e50d6d… --rev 917d7109… --work <empty> --outdir .ufo/evidence/round-97/pre-freeze`).
Receipts: `.ufo/evidence/round-97/pre-freeze/*.out`.

| state | attack | expected |
|---|---|---|
| `c1-nowork-bind-absent` | `git grep BATTERY states=` at base | no output, rc 1 |
| `c1-nowork-summary-absent` | `git cat-file -e 8ed9c526:…/C1-summary.txt` | rc 1 |
| `c1-positive` | the binder at the instrument rev | `matched=50`, rc 0 |
| `c1-forge-worktree-only` | receipt dropped from the index, left on disk | `missing=1`, rc 1 |
| `c1-forge-counter-sha` | `counter_sha=` edited | `mismatched=1`, rc 1 |
| `c1-forge-exit` | `exit=` edited | `mismatched=1`, rc 1 |
| `c1-forge-payload` | `C1_R96_PASS=true` flipped | `mismatched=1`, rc 1 |
| `c1-forge-driver-sha` | `--driver-sha 0…0` | `driver-sha-mismatch`, rc 2 |
| `c1-selftest` | the shipped battery | `BATTERY_SELFTEST: 7/7 pass` |
| `c2-nowork-absent` | `git grep GUARD_INERTIA` at base | no output, rc 1 |
| `c2-positive` | the matrix at the instrument rev | `rows=10 killed=8 limits=2 survived=0 unmet=0`, rc 0 |
| `c2-forge-flipped-expect` | a killed row declared `limit` | `survived=1`, rc 1 |
| `c2-forge-noop` | `edit.new == edit.old` | `GUARD_SETUP edit-no-op`, rc 2 |
| `c2-selftest` | the shipped matrix | `GUARD_INERTIA_SELFTEST: 7/7 pass` |

## Kills for the round

- C1 kill rules (a)–(e), C2 kill rules (a)–(f).
- Any `falsifies-wording` artifact of this round's own wave that contradicts a frozen
  sentence is amended **pre-data** in §Amendments (wording narrowed to the enforceable
  property with the artifact cited), never filed as the wider sentence.

## Amendments

(none yet — every pre-data amendment appends a row here with the artifact that falsified
the sentence and the repaired property)
