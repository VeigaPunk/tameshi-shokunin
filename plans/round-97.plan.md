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
- **Wording (frozen after A3-A8):** at the records revision R,
  `python3 -I .ufo/evidence/round-97/c1/battery-bind.py --lane . --rev R --driver-sha <64 hex>`
  prints `BATTERY states=50 matched=50 mismatched=0 missing=0` and exits 0; it reads the 50
  receipts as blobs at R (a receipt absent from the tree at R is absent even when the file
  stays on disk; an uncommitted index deletion is not seen) and takes its expectations from
  the committed driver's `states()` and `EXPECT_EXTRA` at R; a receipt removed from the tree
  at R by a commit while the file stays on disk prints a nonzero `missing` count and exits 1;
  a `counter_sha=` edit on a receipt that does **not** carry a `mutant=D<nn>` line, an
  `exit=` edit, and a `C1_R96_PASS=true` payload edit on a `__pass` receipt each print a
  nonzero `mismatched` count and exit 1; a `--driver-sha` that is not 64 hex is refused
  `BATTERY_SETUP driver-sha-invalid` and a 64-hex value unequal to the driver blob's sha256 is
  refused `BATTERY_SETUP driver-sha-mismatch`, each exit 2; at base `07e50d6d`
  `git grep -c 'BATTERY states='` prints nothing and
  `C1-summary.txt` is absent at `8ed9c526` (`git cat-file -e` exit 128).
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
  the state (round-96 F1, unchanged). A receipt carrying a `mutant=D<nn>` line is exempt from
  the digest check by construction (the mutant's digest cannot be pinned before the run), so
  a pure `counter_sha=` edit on such a receipt is not detected (A3: `R97E3-forgeries.txt`
  E2e), and any receipt can opt out of the digest check with one `mutant=D<nn>` line (E2d).
- The reader is new work over data that already existed at the base: run from the worktree
  against `07e50d6d` it prints the predicate (measured 2026-11-08, exit 0, rc 0), so the
  after-state is a committed reader, not new receipts. The base does not carry the tool
  (`git cat-file -e 07e50d6d:.ufo/evidence/round-97/c1/battery-bind.py` exit 128) and no
  committed tool prints the line there.

### C2 — operability: the guard-inertia matrix

- **Axis:** operability (a runnable matrix; it produces its stated per-row outcome).
- **Surface:** `.ufo/evidence/round-97/c2/guard-inertia.py` + the committed manifest
  `.ufo/evidence/round-97/c2/guard-inertia.json`, applied to the round-96 checker blob
  `.ufo/evidence/round-96/conjunct-disposition-v96.py` at `--rev`.
- **Wording (frozen after A9-A11):** at the records revision R,
  `python3 -I .ufo/evidence/round-97/c2/guard-inertia.py --lane . --rev R --checker-sha <64 hex> --manifest-sha <64 hex>`
  prints `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0` and exits 0; for each of
  the 10 manifest rows it applies exactly one exact-string edit to the checker blob at R
  (refusing a no-op with `GUARD_SETUP edit-no-op`, an ambiguous anchor with
  `GUARD_SETUP edit-ambiguous`, an unbuildable state with `GUARD_SETUP state-unbuildable`, a
  `limit` row with no declared mechanism with `GUARD_SETUP limit-mechanism-missing`, a
  manifest blob whose sha256 differs from `--manifest-sha` with `GUARD_SETUP
  manifest-sha-mismatch`, and a manifest with no rows with `GUARD_SETUP manifest-empty`, each
  exit 2), runs the pristine and the mutant checker against the same fresh fixture store and
  the same arguments, and reports `killed` only when the pristine run exits with the row's
  declared exit and prints its declared token and the mutant run's exit differs or loses that
  token, and `limit` only when the two runs are identical in exit and declared token; a row
  whose observed class differs from its frozen `expect` makes `unmet` nonzero and exits 1; at
  base `07e50d6d` `git grep -c 'GUARD_INERTIA'` prints nothing.
- **Counter:** `python3 -I .ufo/evidence/round-97/c2/guard-inertia.py --lane . --rev RECORDS_REV --checker-sha <64 hex> --manifest-sha <64 hex>`
- **Battery:** `python3 -I .ufo/evidence/round-97/c2/guard-inertia.py --selftest`
- **Predicate:** `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0` (exit 0)
- **Before:** at base `07e50d6d` no committed tool prints a `GUARD_INERTIA` line; round 96's
  R96M1 mutation matrix covers the counter (`measure-v96.py`), not the checker's guards; the
  round-96 revenger probe left a late seat report (`.ufo/waves/round-96/w1/R96L1.md`,
  "partly refuted") but no committed runnable matrix, and the round-96 record's own M5
  corrected the spot-check's premature dead-seat call (D-b). C2 is the first committed
  matrix over the checker's guard edits.
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

Pre-data; no claim receipt existed when each row was written (the pre-freeze controls are
controls, not a scored positive; the records run postdates every row here).

| id | artifact | falsified sentence | amendment |
|---|---|---|---|
| A1 | `.ufo/evidence/round-97/pre-freeze/c1-forge-worktree-only.out` (`BATTERY states=50 matched=49 mismatched=0 missing=1`, rc 1) | C1's "the four edits each print a nonzero `mismatched` count" | the de-index case is counted `missing`, not `mismatched`; the sentence names the field per edit. **A8 corrects A1's own claim** that "the plan wording already read 'mismatched or missing'" — it did not; the plan sentence is rewritten at A8. The counter is unchanged. |
| A2 | base-rev run (`BATTERY states=50 matched=50 mismatched=0 missing=0`, rc 0) and `git cat-file -e 07e50d6d:…/battery-bind.py` exit 128 | nothing — disclosure, not a narrowing | C1's declared limits gain the base-rev reachability sentence; the predicate, counter and target are unchanged. |
| A3 | `w1/R97E3-forgeries.txt` E2e (`D01.out` digest → 64 zeros: `matched=50`, rc 0), E2d (`pos-real.out` zero digest + forged `mutant=D99`: `matched=50`); `w1/R97R1.md` cases 06/28 | C1's "a `counter_sha=` edit … prints a nonzero `mismatched` count" | narrowed to a receipt that does **not** carry a `mutant=D<nn>` line; the exemption (and the one-line opt-out) is added to C1's declared limits. Structural: a mutant's digest cannot be pinned before the run. Tool unchanged. |
| A4 | `w1/R97R1.md` F2, case 13 (`--driver-sha ''` → predicate, rc 0) | C1's "a `--driver-sha` value unequal … is refused … exit 2" | tool repaired: a non-64-hex `--driver-sha` (including the empty string) is `BATTERY_SETUP driver-sha-invalid` exit 2; a 64-hex unequal value stays `driver-sha-mismatch`. The sentence now names both refusals. |
| A5 | `w1/R97R1.md` F5, case 30 (`C1_R96_PASS=true` edit on a conjunct-graded receipt ignored) | C1's "a `C1_R96_PASS=true` payload edit … prints a nonzero `mismatched` count" | narrowed to "on a `__pass` receipt" — the payload line is graded only where the driver's expectation is `__pass`. Tool unchanged. |
| A6 | `w1/R97R1.md` F6, case 17 (`git cat-file -e` → rc 128); `.ufo/evidence/round-97/pre-freeze/c1-nowork-summary-absent.out` (`rc=128`) | C1's "(`git cat-file -e` exit 1)" | corrected to "exit 128". |
| A7 | `w1/R97R1.md` F4, case 04 (index-only deletion, uncommitted, run at the base rev → `matched=50`) | C1's "a receipt deleted from the index (but left in the working tree) prints a nonzero `missing` count" | narrowed to a deletion **committed into the tree at R** while the file stays on disk; an uncommitted index deletion is not seen because the reader reads blobs at R. |
| A8 | `w1/R97R1.md` F3 (the plan still read "each print a nonzero `mismatched` count") | A1's plan-sync claim | the plan §C1 sentence is rewritten (this table's A1 is superseded on that point); no target or predicate moved. |
| A9 | `w1/R97L1.md` §5/§9; `w1/R97R2.md` F1; round-96 `.ufo/waves/round-96/w1/R96L1.md` (`partly refuted`) and its M5 correction `d8f135d2` | C2's Before "the revenger probe R96L1 delivered nothing (spot-check D-b)" | replaced by: a late seat report with no committed runnable matrix, and the round-96 M5 correction of the premature dead-seat call; C2 is the first committed matrix. Predicate/counter/target unchanged. |
| A10 | `w1/R97R2.md` F5 (the plan's C2 command omitted `--checker-sha` while `claims.json` carried it) | plan/C2 command-line sync | the plan's C2 wording and counter now name `--checker-sha <64 hex>`. |
| A12 | `w1/R97C1.md` §1 skip 3 and §2 (`05`, `06`): a substituted 10-row non-guard manifest prints the exact predicate, and the manifest was not digest-pinned | C2's "the 10 manifest rows" universal (any coherent manifest at R produced the line) | tool gains `--manifest-sha`: a manifest blob whose sha256 differs is `GUARD_SETUP manifest-sha-mismatch` exit 2, an empty manifest is `GUARD_SETUP manifest-empty` exit 2; the claim's counter and wording now name the pin. Manifest rows and counts unchanged; `verify-quiet`'s mechanism text now states both forms (pristine rc 1, mutant rc 128). |
| A13 | `w1/R97C1.md` §In-flight (`11`): a non-guard manifest still printed the predicate on the repaired bytes | the manifest's rows are a human declaration | added to C2's declared limits (the pin fixes which rows are measured, not whether each edit is a guard). |
| A14 | `w1/R97C1.md` §1/§3 (`02`): `controls97.py` graded the wrapper's rc 0 for the two no-work controls, so their pre-registered inner rc could not fail | the control's own assertion | `c1-nowork-bind-absent` now records the grep rc (1) and `c1-nowork-summary-absent` the `cat-file` rc (128); both are graded against those values. Two new C2 controls added: `c2-forge-manifest-subst` (pinned digest vs substituted manifest → exit 2) and `c2-forge-manifest-empty` (exit 2). Controls 16/16. |
| A15 | `w1/R97S1.md`; `w1/R97R1.md`; `.ufo/evidence/round-97/pre-freeze/c1-forge-{exit,payload}.out` (first version: both print `MISMATCH(counter-sha)`) | nothing — control-fixture repair, not a claim narrowing | each C1 body-edit forgery now resets to the pristine receipt at `a.rev` and edits exactly one field; the refreshed receipts print `MISMATCH(exit=7)` and `MISMATCH(exit=0)`; controls 16/16. The wording already named the three fields separately (A1/A5). |
| A11 | `w1/R97R2.md` F3/F4, `w1/R97E2.md` F2 | nothing — instrument hardening | tool repaired: an unbuildable state is `GUARD_SETUP state-unbuildable` exit 2, a `limit` row with no declared mechanism is `GUARD_SETUP limit-mechanism-missing` exit 2, and both selftests create their scratch root before `mkdtemp`. Selftests still 7/7; the manifest and the 10 rows are unchanged. |

Post-repair instrument digests: C1 `battery-bind.py` and C2 `guard-inertia.py` are re-pinned in
`claims.json` at the commit that carries this table; the checker, manifest, driver and counter
blobs are unchanged.
