# Draft — `corpus/QUALITY.md`, criteria 175 and 176

Two criteria in the file's existing voice, each citing `lessons/round-97.md` and each ending
with an `Able to fail:` clause that names a receipt that would fail if the rule were
violated. Both are already committed at `136e98a8` (A1); the text below is the same pair
with the two defects that later amendments (A6, A9) made visible corrected, marked
`⟨CHANGED⟩` where the bytes differ from the committed text.

---

175. A record's verdict is **re-derived from committed bytes by a committed reader**. A summary
    the report cites but the repository does not carry is not evidence, and a reader that
    re-grades the committed receipts with the committed oracle is the minimum that turns an
    attested count into a measurement. Able to fail: the round-96 record cites
    `.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt`, absent at `8ed9c526`
    (`git cat-file -e` exit 128), while round 97's reader prints
    `BATTERY states=50 matched=50 mismatched=0 missing=0` at the records revision, and the
    five forgeries each move the line or the exit
    (`.ufo/evidence/round-97/pre-freeze/c1-forge-*.out`). (`lessons/round-97.md`;
    `corpus/lessons/round-96-verifier-spotcheck.md` D-a.) ⟨CHANGED: the committed text reads
    "exit 1"; the measured rc is 128 — the round's own
    `.ufo/evidence/round-97/pre-freeze/c1-nowork-summary-absent.out` prints `rc=128` and
    `git cat-file -e 8ed9c526:.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt`
    exits 128. A6 already corrected the plan and the claims to 128; this criterion was
    written at A1 and still carries the old number.⟩

176. A guard edit is **killed only when the mutant's verdict differs** from the pristine's in
    the declared direction; an edit whose two runs are identical is a measured `limit` with
    the mechanism named — never `survived`, never presumed observable — and an exact-string
    anchor that is not unique is refused before the edit. Able to fail:
    `guard-inertia.json` row `git-absolute` is measured `limit` (both runs exit 0 under the
    pinned `PATH`), row `verify-quiet` is measured `limit` (both exit 2 with the same token),
    a flipped expectation prints `survived=1` exit 1
    (`.ufo/evidence/round-97/pre-freeze/c2-forge-flipped-expect.out`), and a no-op edit prints
    `GUARD_SETUP edit-no-op` exit 2 (`.ufo/evidence/round-97/pre-freeze/c2-forge-noop.out`);
    the round-96 record had no committed runnable matrix over the checker's guards — the
    revenger seat left a late report (`R96L1.md`, partly refuted) but no measurement.
    (`lessons/round-97.md`; S159, S006.) ⟨CHANGED: the committed text reads "R96L1 delivered
    nothing"; A9 replaced that clause in the claims and the plan after R97R2 F1 showed the
    round-96 revenger seat did land a report, committed at `d8f135d2`. The defect being barred
    — no committed matrix — stands; the attribution did not.⟩

---

## Notes for the integrator

- Both criteria are committed already (`136e98a8`), so these are **corrections**, not
  additions; the numbering 175/176 stays.
- Criterion 175's `Able to fail:` glob `c1-forge-*.out` resolves to **six** committed
  receipts, not the five the clause names. The five C1 forgeries the claim registers are
  `c1-forge-{worktree-only,counter-sha,exit,payload,driver-sha}.out`; the sixth,
  `c1-forge-conjunct.out`, has no plan row and no counterpart in the committed driver's run
  (it is byte-identical to `c1-forge-counter-sha.out`). Narrow the glob to the five, or say
  "the C1 forgeries" — as written, a reader following the glob also lands on the orphan.
- The "five forgeries each move the line or the exit" clause is true of the *receipts* but
  overstated as a *test design*: `c1-forge-counter-sha.out`, `c1-forge-exit.out`,
  `c1-forge-payload.out` and `c1-forge-conjunct.out` are the same bytes
  (sha256 `1c9754f3…`) — the `exit=` and payload edits never reach the grader
  (R97R1 N1, R97C1 §1 item 1). The clause should not imply the suite distinguishes an
  unreached edit from a killed one.
- Criterion 176's "Able to fail:" receipts are all committed and backable:
  `c2-forge-flipped-expect.out` prints `GUARD_INERTIA rows=10 killed=8 limits=1 survived=1
  unmet=1` (rc 1), `c2-forge-noop.out` prints `GUARD_SETUP edit-no-op:rev-hex` (rc 2).
