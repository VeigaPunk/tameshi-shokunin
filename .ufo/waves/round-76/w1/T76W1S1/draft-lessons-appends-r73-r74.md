# Append 1 — draft erratum for `plans/round-73.plan.md`

<!-- Target: end of plans/round-73.plan.md (append-only), after the "## Wave"
     section. The r72 plan's erratum ("## Erratum, appended 2026-11-03 (round
     73)") is the format precedent. DRAFT by seat T76W1S1. -->

```markdown
## Erratum, appended 2026-11-04 (round 76)

This plan is frozen text and stands as written; one sentence of the R73-C1
kill rule is contradicted by the round's own receipt, and the mismatch is
recorded here rather than rewritten (round-74 verifier spotcheck §6 item 6 /
round-75 verifier spotcheck §6 item 3: "no erratum was appended to
`plans/round-73.plan.md` for its contradicted kill-rule sentence"; the r72
plan erratum `3e0ef1c8` is the precedent).

- Lines 80–82 declare "**Kill rule.** C1 fails if the selftest is not 12/12,
  if any standing row reads other than its expected status, or if any control
  below reaches `unexpected=0`." The green-rows-only control — a reconciler
  over a manifest carrying only the four green round-72 rows — reads
  `WAVE_RECONCILE: rows=4 met=4 unexpected=0` exit 0 (measured in the round's
  own control receipt `.ufo/evidence/round-73/reh/reh-c1-controls.txt`,
  `--- control: green-only ---` block; the always-meet and echo-printed
  controls correctly read `unexpected=1`/exit 1 over the standing six-row
  manifest). A control that reaches `unexpected=0` by design therefore cannot
  be a failure condition as written. The operative predicate is the frozen
  LINE — `WAVE_RECONCILE: rows=6 met=6 unexpected=0` exit 0 over the
  standing six-row `tools/wave-reconcile.json` — which the green-only
  control cannot print; the wave seat T73W1S07 recorded the contradiction in
  `corpus/lessons/round-73.md` ("[landed] the plan's kill-rule wording is
  wrong"). C1's claim is unaffected: the landed tool reads the six-row line
  at the round tip, and the two genuinely-measuring controls still refuse the
  stubs the clause was written against.
```

# Append 2 — draft `used-by` old→new record for `corpus/lessons/round-74.md`

<!-- Target: end of corpus/lessons/round-74.md (append-only). Pays
     corpus/lessons/round-74-verifier-spotcheck.md defect 5 ("the report says
     the `used-by` change is 'logged in the lesson's Gate'; the lesson records
     only the added path … append it to the lesson (append-only)"). The old
     value is quoted from the SOURCES.md Round 74 note's recorded pair
     (`corpus/lessons/round-63.md` ->
     `corpus/lessons/round-63.md, corpus/lessons/round-74.md`). DRAFT by seat
     T76W1S1. -->

```markdown
## Appended — S294 `used-by` old→new (round 76)

The round-74 verifier spotcheck's defect 5 records that this lesson's Gate
named only the added path; the old→new pair lived in the round's report and
the SOURCES `Round 74` note. Recorded here, append-only, so the lesson
carries its own curation delta:

- S294 (`gitattributes`) `used-by` old → new: `corpus/lessons/round-63.md`
  → `corpus/lessons/round-63.md, corpus/lessons/round-74.md`.
```
