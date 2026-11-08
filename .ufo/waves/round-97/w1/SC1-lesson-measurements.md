# Draft — `corpus/lessons/round-97.md` § Measurements

Every number below is a line a committed receipt printed at the revision named. Receipt
paths are relative to the lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; every
path and every quoted line was checked with `git show HEAD:<path>` (receipt inventory and
byte comparison: `.ufo/waves/round-97/w1/SC1-record-verification.txt`).

- **C1 positive at the records revision `35db02e9`.**
  `.ufo/evidence/round-97/landing/c1-positive-1.out` reads
  `BATTERY states=50 matched=50 mismatched=0 missing=0`; runs 2 and 3 are byte-identical
  (all three sha256 `54c6f667…`). `.ufo/evidence/round-97/repeat/c1-run-{1,2,3}.txt` are
  those same bytes.
- **C1 refusals.** `c1-forge-worktree-only.out` (`BATTERY states=50 matched=49
  mismatched=0 missing=1`, rc 1), `c1-forge-counter-sha.out`, `c1-forge-exit.out` and
  `c1-forge-payload.out` (`mismatched=1`, rc 1), `c1-forge-driver-sha.out`
  (`BATTERY_SETUP driver-sha-mismatch`, rc 2). A non-64-hex `--driver-sha` prints
  `BATTERY_SETUP driver-sha-invalid`, rc 2, against the committed tool at the records
  revision (`.ufo/waves/round-97/w1/SC1-driver-pin-refusals.txt`) — **but no committed
  receipt prints that line**: it is in the tool's bytes (`battery-bind.py:127`) only, and the
  case-13 receipt the lesson cites (`R97R1-repro.txt:444-450`) shows the *pre-repair*
  behaviour (`BATTERY states=50 …`, rc 0) at rev `5e99c661…`, which is not in the store at
  HEAD.
  **Disclosed limit:** the three body-edit receipts are the *same bytes*
  (sha256 `1c9754f3…`), because `controls97.py:135,143` resets to the previous attack's
  commit, so the `counter_sha=` edit rides into the `exit=` and payload trees and the reader
  stops at its digest check (`battery-bind.py:154`). Those two edits are exercised by the
  tool's own selftest, not by these receipts (R97R1 N1, R97C1 §1 item 1).
- **C1 selftest.** `c1-selftest.out`: `BATTERY_SELFTEST: 7/7 pass`, rc 0.
- **C2 positive at `35db02e9`.** `.ufo/evidence/round-97/landing/c2-positive-1.out` reads
  `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0`; runs 2 and 3 are
  byte-identical (all three sha256 `254536aa…`). The per-row lines show `rev-hex`,
  `rev-unresolvable` (token-only kill), `replace-refs`, `counter-sha`, `receipt-absent`,
  `no-flip`, `unknown-key`, `min-falsifiable` killed, and `verify-quiet`, `git-absolute` as
  measured limits.
- **C2 refusals.** `c2-forge-flipped-expect.out` (`GUARD_INERTIA rows=10 killed=8
  limits=1 survived=1 unmet=1`, rc 1), `c2-forge-noop.out` (`GUARD_SETUP edit-no-op:rev-hex`,
  rc 2), `c2-forge-manifest-subst.out` (`GUARD_SETUP manifest-sha-mismatch`, rc 2),
  `c2-forge-manifest-empty.out` (`GUARD_SETUP manifest-empty`, rc 2).
- **C2 selftest.** `c2-selftest.out`: `GUARD_INERTIA_SELFTEST: 7/7 pass`, rc 0.
- **Controls.** The committed driver at `35db02e9` re-run from the lane prints
  `CONTROLS97 states=16 matched=16 mismatched=0`, exit 0, and every one of its sixteen
  receipts is byte-identical to the committed set
  (`.ufo/waves/round-97/w1/SC1-controls-rerun.txt`). One committed receipt,
  `c1-forge-conjunct.out`, has no counterpart in the run (a plan row that was never
  registered).
- **Census.** `census-before.txt` and the round-end run both exit 0, rows 183 (A 165 · B 14 ·
  C 4), mined 149 · queued 23 · rejected 11, unchanged.
