# Draft — `SCORECARD.md`, the round-97 section

Skeleton with the two claim rows and the two capability rows. `measured commits` is left at
`<TO FILL AT RECORDS>` in the shape the spec asks for; the values the lane has actually
reached are given in the note under the table so the integrator can fill them from the
committed records rather than from this draft.

---

## Round 97 — two claims: the committed battery is re-derivable (calibration) and the guard edits are measured (operability)

Base `07e50d6d`; instruments `917d7109`; pre-freeze controls and
frozen plan `997ce0c4`; claims freeze `e72a0c8b` (+ A1 `136e98a8`, A2 `43acfe81`); wave spec and
dispatch `f5ace66a`; A3-A11 `6f080522`; A12-A14 `406119cd`; controls 16/16 and records base
`35db02e9`; records positives `2170db76`.
One v1 wave `w1`, 12 seats (executor 3, scribe 1, scout 1, reviewer 2, critic 1, mutation-tester 1,
sentinel 1, connector 1, revenger 1; attack 4/12 = 33 % by the §6 named set (reviewer×2, critic,
mutation-tester), 7/12 = 58 % including sentinel, connector and revenger).

| Claim | Axis | Before | After (predicate) | Verdict | Counting command | Measured commits |
|---|---|---|---|---|---|---|
| R97-C1 | calibration | at base `07e50d6d` no committed tool prints a `BATTERY states=` line (`git grep -c` empty, rc 1; `.ufo/evidence/round-97/pre-freeze/c1-nowork-bind-absent.out`), the base does not carry the reader (`git cat-file -e` rc 128) and the `C1-summary.txt` the round-96 report cites is absent at `8ed9c526` (`c1-nowork-summary-absent.out`, rc 128) | `BATTERY states=50 matched=50 mismatched=0 missing=0`, exit 0; five refusals rc 1/2; selftest `7/7` | **verified under the amended wording (A1-A8)** | `python3 -I .ufo/evidence/round-97/c1/battery-bind.py --lane . --rev <REV> --driver-sha 88bcca86…` | `<TO FILL AT RECORDS>` |
| R97-C2 | operability | at base no committed tool prints a `GUARD_INERTIA` line (`c2-nowork-absent.out`, rc 1); round 96's R96M1 matrix covers the counter, not the checker's guards; the round-96 revenger probe left a late seat report (`R96L1.md`, partly refuted) but no committed runnable matrix (A9) | `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0`, exit 0; eight killed + two measured limits; flipped expectation `survived=1` rc 1; no-op anchor, substituted manifest, empty manifest rc 2; selftest `7/7` | **verified under the amended wording (A9-A14)** | `python3 -I .ufo/evidence/round-97/c2/guard-inertia.py --lane . --rev <REV> --checker-sha 02a5482a… --manifest-sha 9de0b7e9…` | `<TO FILL AT RECORDS>` |

Scores unchanged: depth 10, calibration 8, freshness 9 (delta 0); the nudge premise holds
(10/8/9 >= 8). Two capability rows enter: `committed-battery binder` (the 50 committed receipts
re-graded by the committed driver's own expectations in seconds; `.ufo/evidence/round-97/landing/
c1-positive-{1,2,3}.out` byte-identical, sha256 `54c6f667…`) and `guard-inertia matrix` (ten checker
edits measured on a four-file fixture store with a digest-pinned checker and manifest;
`.ufo/evidence/round-97/landing/c2-positive-{1,2,3}.out` byte-identical, sha256 `254536aa…`).

**Retired:** none. **Saturation:** unchanged.

---

## Capability rows (the `## Capabilities` table)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| committed-battery binder | re-grade a committed battery's receipts from committed bytes at a named revision, with the oracle pinned by digest, and refuse a receipt that is absent at that revision or whose digest does not match the counter | `python3 -I .ufo/evidence/round-97/c1/battery-bind.py --lane . --rev <REV> --driver-sha 88bcca86…` → `BATTERY states=50 matched=50 mismatched=0 missing=0`, exit 0; `--selftest` → `BATTERY_SELFTEST: 7/7 pass`; `.ufo/evidence/round-97/landing/c1-positive-{1,2,3}.out` (byte-identical, sha256 `54c6f667…`); refusals `.ufo/evidence/round-97/pre-freeze/c1-forge-*.out` | round 97 |
| guard-inertia matrix | measure one declared exact-string edit per guard against the pristine checker on the same fixture store, and classify each row `killed` / `limit` / `survived` from the observed verdicts alone, with the checker and the manifest both digest-pinned | `python3 -I .ufo/evidence/round-97/c2/guard-inertia.py --lane . --rev <REV> --checker-sha 02a5482a… --manifest-sha 9de0b7e9…` → `GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0`, exit 0; `--selftest` → `GUARD_INERTIA_SELFTEST: 7/7 pass`; `.ufo/evidence/round-97/landing/c2-positive-{1,2,3}.out` (byte-identical, sha256 `254536aa…`); `.ufo/evidence/round-97/c2/guard-inertia.json` | round 97 |

---

## Notes for the integrator

- `measured commits` is `<TO FILL AT RECORDS>` in the claim table above, per the spec. The
  lane's own committed value is `35db02e9` (`.ufo/waves/round-97/records-rev.txt`); the
  positives at that revision are `2170db76`. Fill from those bytes, not from this draft.
- The two capability rows are drafted as table rows here; the committed SCORECARD text at
  `96a24dd3` carries them as a prose sentence in the round-97 section instead. Either form
  is consistent with the file's history (the round-93 `conjunct-disposition audit` row and the
  round-96 `revision-identity seal` sentence are both prose in the round section; the
  `## Capabilities` table at the top carries the table form).
- Before/After/Verdict cells above are the committed text at `96a24dd3`, verified:
  `BATTERY states=50 matched=50 mismatched=0 missing=0` and `GUARD_INERTIA rows=10 killed=8
  limits=2 survived=0 unmet=0` are backed by committed receipts; the refusal exits
  (1/2/1/2/2/2) and the two selftest `7/7` lines are backed by the committed pre-freeze set
  (`.ufo/waves/round-97/w1/SC1-record-verification.txt`).
- One wording caveat the SCORECARD inherits from the LOG entry: "five refusals rc 1/2" is true
  of the receipts, but three of the five are the same bytes (sha256 `1c9754f3…`), so the
  suite does not distinguish an unreached edit from a killed one (R97R1 N1, R97C1 §1 item 1).
