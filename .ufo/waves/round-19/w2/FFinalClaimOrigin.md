# FFinalClaimOrigin — round-19 w2 falsification

Date: 2026-10-21. Scope: FinalClaimOrigin only; read-only review, no tests or measurement runs.

## Strongest assertion and verdict

**Agree; not falsified.** W1 §2 says the fleet report’s final-revision 60/60-at-`4b7c682` sentence was unsupported by a committed receipt at landing. The primary sentence is fleet `.ufo/reports/round-18/tameshi.md:53` (repeated at `:77`); the routed criterion is `corpus/lessons/round-18-verifier-spotcheck.md:201-204`.

At `4b7c682`, the `.ufo/evidence/round-18/final/` tree lists `measure-final.json` and `measure-final-60.json`, but no receipt for `4b7c682`. The first receipt says revision `a134a09…`, 59/60, restraint 6; the second says `a85f710…`, 60/60, restraint 8, no overrides. Thus the latter does not back a result at the cited tip.

The later replay is properly distinguished from that landing-time gap: `.ufo/evidence/round-19/round18-final-measure.json` names exact argv `python3 .ufo/evidence/round-18/measure.py --repo … --rev 4b7c682… --explain`, revision `4b7c682…`, exit 0, and `recorded_at` 2026-10-21T05:28:25Z. Its bound stdout reports 60/60, restraint 8, overrides false, strict trace gate; the companion pins the receipt and the original tool. SHA-256 of the tool blob at `4b7c682` is `7ca87a7c…26dd37`, matching the companion. This verifies replayed values, not contemporaneous execution. The lane erratum says “repairs missing evidence, not its original timeliness” (`corpus/lessons/round-18.md:148-155`, 2026-10-21) and leaves the fleet report unchanged.

## C1 receipt arithmetic and correction status

Plain JSON rows: `before.json` = corrected 0 + open 5 = total 5, R18-1…R18-5 all open; `after-21e7932.json` = corrected 5 + open 0 = total 5, all five corrected. The after receipt names revision `21e7932…` and ruler SHA `c538c33d…`.

At frozen delivered revision `55e1d312…`, `.ufo/evidence/round-19/measure.py` hashes to `bb651eef…`; the retained after receipt still binds `c538c33d…`, and the frozen evidence inventory has no later after receipt. Therefore the 5/5 arithmetic is real for the initial ruler, but is not a same-ruler final-build result. W1 §4.2 correctly flags this remaining gap; the delivered C1 correction does not make that observation stale. The separate R18-5 replay is not a substitute for this five-defect ruler measurement.

## Concrete falsifier and residual gap

A concrete falsifier of the landing-time assertion would be a receipt present in the `4b7c682` tree (or landed before the fleet report) naming `4b7c682`, the cited argv, and successful bound streams. The historical tree contains no such receipt; the post-freeze replay cannot falsify the temporal claim. The lane erratum exists, while the proposed fleet-side append-only erratum remains unapplied as W1 explicitly states; the fleet report is intentionally not rewritten. Final same-ruler before/after measurement and the public selftest remain for L1; neither was run in this review.