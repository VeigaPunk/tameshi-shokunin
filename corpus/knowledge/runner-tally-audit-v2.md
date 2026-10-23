# Runner tally audit v2 — the four held-out classes and the counters (round 33)

source: own-work — .ufo/evidence/round-32/heldout/*.json (the sealed set that defeated v1), S097 (bash exit statuses 0..255, pinned bashref.texi), S099 (mutation adequacy, pitest.org)
verified-at: round-33 measurement revision (see SCORECARD.md round-33 row; counter receipts .ufo/evidence/round-33/after/)
recheck: on-runner-change (the audited surface is pinned at sha256 a7d3f2dd...2eb9; any runner edit re-opens every class)

Round 32's `tools/tally-audit.py` met its public panel (18 kill + 8 accept) and failed a sealed
held-out set of runner copies 1/10 kill (`ho_kill=1/10`, `.ufo/evidence/round-32/after/c1v2-at-measurement.stdout`).
This entry records the four classes that defeated it, the counter-design they forced, and what a
third round would have to attack. `tools/tally-audit-v2.py` is the landed answer; the runner stays
byte-identical.

## The four classes (each with its committed seed)

1. **Count-vector blindness.** The v1 runtime oracle swept single statuses and a few two-status
   pairs; no vector ever produced 3-8 failing or setup legs. Surviving seeds: HeldOutPrintf-1/-2
   (printf count fields swapped — visible only when failed>=3), HeldOutGuard-1/-2 (FAIL gated on a
   majority `nsetup <= npass+nfail` — witness `[1,2,2,2,2,2,0,0,0]`), HeldOutTallyArms-01/-02
   (conditional double count of the `1)` arm). Counter-design: one representative vector for every
   (failing, setup) count pair 0..9, oracle compares the exact stdout first line and exit code.
2. **Per-position status blindness.** v1 swept all statuses 0..255 only at position 0; positions
   1..n got {1,2,3,4,126,127,255}. Surviving seeds: HeldOutRefactor-k1 (status 5 at position 3),
   HeldOutLoop-1 (a leg status masked to seven bits inside the block, witness `[0,128,0,...]`).
   Counter-design: every status 0..255 at every position (bash statuses are 0..255 — S097).
3. **Tally-loop misidentification.** v1 picked the FIRST loop whose operands look like leg statuses,
   then stressed that loop — so an auxiliary loop made the audit analyze the wrong code:
   false-rejected accepts HeldOutLoop-3 (single-iteration wrapper around the real loop) and
   HeldOutRefactor-a4 (a pre-count loop before it). Counter-design: identify the tally loop by
   dataflow — the innermost `for` whose body contains the counting `case $st in` arms — and stress
   only that loop.
4. **Extraction-line cardinality.** v1 required exactly one `tblock=$(awk ...)` extraction line in
   the selftest harness and refused (exit 2) a copy with a second equivalent line
   (HeldOutRefactor-a3). Counter-design: accept >=1, splice the injected reference after the LAST.

Two routed tool-review items landed with these: comparisons are stdout-only (stderr captured
separately, never into the compared string), and `--then-regression` runs under a 1200 s timeout.

## What the held-out set is for — and its limits

A public panel is memorizable (round-32 lesson Mistake 4: the v1 counter was met by a 27-line
allowlist). The sealed set is written AFTER the tool freeze by seats who did not write the tool,
each copy carrying exact-string edits plus a witness: a status vector on which the mutated tally
block's (exit, first line) differs from pristine — or `kind=head` for head edits. The counter
re-validates every file (schema, uniqueness, witness) and `ho_invalid` must be 0. What it does NOT
cover: behaviorally equivalent textual mutants (an added comment is `ho_invalid`, by design —
recorded as a calibration item, not a gap), and faults outside run_regression entirely (the audit
surface is the regression tally path, not the whole runner).

## The counter's control gate

Round 32 skipped its declared pre-data control run (lesson Mistake 7). The round-33 counter refuses
to run unless a committed controls receipt names its own sha256 and records every control tool
failing the predicate; controls (do-nothing, always-pass, always-fail, sha-only) are authored by
seats and scored before any held-out authoring. A counter edit therefore invalidates the receipt by
itself.

## Selftest as the replay record

`--selftest` replays every round-32 class as a seeded case (mask, wrapper, pre-count, second
extraction, printf swap, majority guard, double count) plus v1's originals and the new head check
(every leg assigned exactly once as a bare `st_x=$?` before the tally block; no in-block leg
reassignment). 21/21 at the freeze (`.ufo/evidence/round-33/dev/selftest-final.stdout`).

## Measured result

Not measured this round (round 33 honest stop): the sealed held-out set was never authored after
the tool freeze, so the C1 predicate was not run (see SCORECARD.md round-33 row and
corpus/lessons/round-33.md `## Gate`). The tool nonetheless hardened pre-data through five
disclosed amendments driven by nine seat findings; the eight routed residue classes for round 34's
v3 are listed in the lesson's Holds. The coverage lesson that survives regardless of the verdict:
a sweep that never co-occurs a status >= 3 with another non-zero leg, and a driver pinned to one
runtime configuration, jointly blinded nine independent seat batteries — vector design is the
audit, and it must be attacked with the same energy as the code under audit.
