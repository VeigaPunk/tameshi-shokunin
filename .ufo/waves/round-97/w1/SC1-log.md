# Draft — `LOG.md`, the `## Round 97 (2026-11-08)` entry

Shape follows the round-96 entry. Every revision, receipt path and printed line below was
checked against committed bytes at the lane HEAD (see
`.ufo/waves/round-97/w1/SC1-record-verification.txt`).

---

## Round 97 (2026-11-08) — two claims: the committed battery is re-derivable (calibration) and the guard edits are measured (operability)

- **Shape.** Base `07e50d6d`; instruments `917d7109`; frozen plan and pre-freeze controls
  `997ce0c4`; claims freeze `e72a0c8b`; A1 `136e98a8`; A2 `43acfe81`; wave w1 spec + dispatch
  `f5ace66a`; A3-A11 `6f080522`; A12-A14 `406119cd`; controls 16/16 and records base `35db02e9`;
  records positives `2170db76`. Records revision: `35db02e9`.
- **R97-C1 (calibration).** The round-96 spot-check's D-a: the report cited
  `.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt`, absent at `8ed9c526`
  (`git cat-file -e` exit 128 — `.ufo/evidence/round-97/pre-freeze/c1-nowork-summary-absent.out`
  records `rc=128`). `battery-bind.py` re-grades the 50 committed receipts against the
  committed driver's own `states()`/`EXPECT_EXTRA` (read as blobs at `--rev`, driver pinned
  with `--driver-sha`), and prints `BATTERY states=50 matched=50 mismatched=0 missing=0`, exit 0
  at `35db02e9`, in seconds and without re-running a state
  (`.ufo/evidence/round-97/landing/c1-positive-1.out`; runs 2 and 3 byte-identical). Five
  forgeries each move the line (de-index committed → `missing=1`; `counter_sha=` / `exit=` /
  `__pass` payload edits → `mismatched=1`) and a non-64-hex or unequal driver pin is refused
  at setup. Selftest `7/7`.
- **R97-C2 (operability).** The round-96 spot-check's D-b: the "are the guards inert?" probe
  had no committed measurement. `guard-inertia.py` + `guard-inertia.json` apply ten
  pre-registered exact-string edits to the round-96 checker (uniqueness and no-op refused
  before any run), run pristine and mutant against the same four-file fixture store, and
  classify `killed` only on a measured verdict difference and `limit` only on an identical
  pair. Predicate `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0`, exit 0 at
  `35db02e9` (`.ufo/evidence/round-97/landing/c2-positive-1.out`; runs 2 and 3
  byte-identical); the checker and manifest are digest-pinned, a substituted manifest and an
  empty manifest are refused, and a flipped expectation prints `survived=1`, exit 1. Selftest
  `7/7`.
- **Motivating evidence.** The round's own wave falsified twelve atomic assertions pre-data
  (R97R1 F1-F6: the `mutant=` digest exemption, the empty `--driver-sha`, the `__pass` scope,
  the `cat-file -e` rc, the index-only deletion, the plan sync; R97E3 FW-C1-1; R97C1 §1/§2: the
  substituted non-guard manifest and the unpinned manifest; R97L1 §9 and R97R2 F1: the
  dead-seat provenance). Each became an amendment A3-A14 with its artifact cited in
  `plans/round-97.plan.md` §Amendments; the predicate, counter and target never moved after
  data.
- **Frontier.** S159 and S006 re-opened with located quotes; a duplicate-URL row (S324) was
  withdrawn before the freeze (S160 already holds the URL) and recorded as M3; S009's UCL page
  was a Cloudflare challenge on two fetches, so it was not re-opened. Census exit 0 before and
  after, rows 183, mined 149, queued 23, rejected 11. QUALITY 175-176. Mistakes M1-M3 in
  `corpus/lessons/round-97.md`.
- **Routed to round 98.** The declared limits this round leaves live: a receipt's provenance is
  unbound (a hand-written receipt with the right payload is accepted; `mutant=D<nn>` opts out
  of the digest check), and the guard matrix's manifest is a human declaration that the digest
  pin fixes but does not validate (a coherent non-guard manifest yields the same line when its
  digest is passed). Neither is claimed.

---

## Notes for the integrator

- The entry above is the committed text at `96a24dd3`. Two claims inside it need a decision:
  - **"Five forgeries each move the line"** — the receipts move, but `c1-forge-counter-sha.out`,
    `c1-forge-exit.out`, `c1-forge-payload.out` and `c1-forge-conjunct.out` are the *same
    bytes* (sha256 `1c9754f3…`); the `exit=` and payload edits never reach the grader
    (R97R1 N1, R97C1 §1 item 1). "Each move the line" is true of the receipts, not of the
    suite's discrimination.
  - **"R96L1 delivered nothing"** was already corrected here (A9); QUALITY 176 still carries
    the old attribution — see `SC1-quality.md`.
- The D-a closure's `exit 128` is the measured rc (A6); the LOG entry already carries it.
- The entry's "a non-64-hex or unequal driver pin is refused at setup" is **measured** — I
  ran it against the committed tool at `35db02e9`: empty pin → `BATTERY_SETUP
  driver-sha-invalid` rc 2; 64-hex unequal → `BATTERY_SETUP driver-sha-mismatch` rc 2
  (`.ufo/waves/round-97/w1/SC1-driver-pin-refusals.txt`). The *receipt* for the first refusal
  does not exist in the committed set, and the case-13 receipt the lesson cites
  (`R97R1-repro.txt:444-450`) shows the pre-repair behaviour at rev `5e99c661…`, an object not
  in the store at HEAD — see `SC1-lesson-measurements.md` and `R97SC1.md` F10.
