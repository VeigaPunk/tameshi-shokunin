seat: CritDriftClaim

# Landing-rule attack — round 45

Target: `tameshi-shokunin/.ufo/evidence/round-45/contract.json:46` (`landing_rule`):
"considerthese/2026-10-25.md proposal 1 (measured-to-landing drift): both claim counters
and the round-44 record-agreement counter are re-run at the final landing tip, and the
report cites those landing-tip receipts."

## Verdict: the rule does NOT close the measured-vs-landing gap

Three independent defects. D3 alone makes the rule unsatisfiable: the mandated green
receipt cannot exist at a round-45 final tip. D1+D2 leave the round-43 failure shape
fully executable under the rule as written.

### D1 — fixed point: a receipt cannot be inside the commit it measures

Running a counter at a tree T produces output that is not yet in T. Committing that
output creates T' ≠ T. Therefore, whichever way the order is read:

- receipts generated before the tip → they measure an ancestor; content committed after
  the run is unmeasured (the round-43 gap, unchanged);
- receipts generated at the tip → the commit carrying them moves the tip; the new tip is
  unmeasured, and the run would have to be repeated → infinite regress.

There is no consistent execution of "re-run at the final landing tip, cite landing-tip
receipts". The measured revision is always strictly older than the commit that carries
the receipt; the sentence "the landing tip is itself the commit carrying the receipt"
is not a detail, it is the contradiction.

Round-43 empirical anchor (round `git log 3c4003f6e97e5c787e7538b2eb35d62f49783aaf..718a1e987febd32eb78ebc65adfe939f23b3de63`):
the SINGLE commit between measured `3c4003f` and landing `718a1e9` is
"round-43: deciding-run receipts and verdict records". Its diff:

```
 .ufo/evidence/round-43/after/c1-at-3c4003f6.exit   |  1 +
 .ufo/evidence/round-43/after/c1-at-3c4003f6.stdout |  1 +
 .ufo/evidence/round-43/after/c2-at-3c4003f6.exit   |  1 +
 .ufo/evidence/round-43/after/c2-at-3c4003f6.stdout |  1 +
 .ufo/evidence/round-43/after/c3-at-3c4003f6.exit   |  1 +
 .ufo/evidence/round-43/after/c3-at-3c4003f6.stdout |  1 +
 LOG.md                                             |  3 ++
 SCORECARD.md                                       | 37 ++++++++++++++++++++++
 8 files changed, 46 insertions(+)
```

The receipts name `3c4003f`; at `718a1e9` the same round-43 counter is red:
`m7=1`, `total=1`, `C2_R43_PASS=false` (exit 1), recorded at
`corpus/lessons/round-43-verifier-spotcheck.md:28`. The commit that carried the
receipts is EXACTLY the commit that broke the claim at landing. The landing rule's
premise — that a landing-tip receipt certifies the landing tip — is false in the very
case the rule was written for.

### D2 — no terminality constraint

The rule never forbids content/record edits after the deciding run or inside the receipt
commit. In round 43 the scorecard/LOG edits landed inside the receipt commit itself.
Without a closed content revision C and a mechanical "nothing but receipts between C and
the tip" check, the same shape stays compliant: run at T, batch receipts with the
scorecard edit, call the result "the final landing tip". Round 43 is that shape.

### D3 — the mandated round-44 counter re-run cannot be green at a round-45 final tip

The round-44 record-agreement counter grades the NEWEST SCORECARD block and pins it to
its contract round. Code path `.ufo/evidence/round-44/calibration/measure.py`:

- `newest_round_block` (lines 155-160) returns the last `## Round N` block;
- `main` (lines 486-489): `if round_no != contract.get('round'): m12.append('newest
  block is round %d, the contract round is %s' ...)` — unconditional.

At the round-45 final tip the newest block is Round 45, so m12 >= 1, total >= 1,
`C2_R44_PASS=false`, exit 1, regardless of whether the round-45 block carries a
well-formed `**Planned (round 46):**` field. Faithful extract of the exact code path,
`/tmp/tameshi-r45-CritDriftClaim/m12-sim.py`, with a round-45 block that DOES carry the
planned field:

```
round_no=45 m12_hits=['newest block is round 45, the contract round is 44'] total=1
C2_R44_PASS=false
```

The only revision where this counter passes is one whose newest block is round 44 —
i.e. BEFORE the round-45 scorecard block lands — which cannot be the round-45 final
landing tip. So the rule demands a receipt that is structurally impossible to obtain;
compliance forces either a non-final-tip run (violating the rule) or a false green
citation (violating honesty). Base receipt confirms the pass only holds while round 44
is still newest: `before/c-r44-at-base.stdout` (`rev=5891bdb...`, `m12=0 total=0`,
PASS=true).

## Impacted axes

- C1 freshness (deciding run), C2 coverage (deciding run): the deciding receipts'
  measured revision is not the tree the outside verdict reads; the round-43 class of
  post-measurement record edits remains fully open.
- Calibration no-harm monitor (round-44 counter): the mandated re-run is unsatisfiable
  at the round-45 tip (D3); citing it green would be fabrication.
- Admission decision for the whole round: hinges on receipts that cannot certify the
  tip (D1) and cannot be green (D3).

## Smallest safe correction — proposed QUALITY.md criterion (one paragraph)

Criterion 85 (round 45). A deciding run's verdict binds the revision it ran against,
never the commit that later carries its receipt: a receipt cannot be inside the commit
it measures, so "re-run at the final landing tip" is unexecutable as written. The round
therefore designates its content revision C — the commit containing every change the
round cites (corpus/, SCORECARD.md, LOG.md, tools/, the counters themselves, the
contract, and ledger/review/orchestrator inputs) — runs each deciding counter against C,
and commits the receipts and report only as child commit(s) whose diff relative to C
touches exclusively permitted receipt/report paths; `git diff --name-only C..tip` must
list no content path, and any content change after C voids the deciding runs and forces
re-deciding at a new C containing it. Each no-harm monitor is run at a revision at which
its own frozen grading assumptions hold: the round-44 record-agreement counter's contract
round must equal the newest SCORECARD block at the revision it runs against, so it is run
while round 44 is still the newest block (or later, and reported red), and a green
receipt for it is never cited at a revision whose newest block belongs to a later round.

Falsifier that must fail the criterion (round-43 shape, from the lane):

```
git diff --name-only 3c4003f6e97e5c787e7538b2eb35d62f49783aaf 718a1e987febd32eb78ebc65adfe939f23b3de63
python3 .ufo/evidence/round-43/calibration/measure.py --lane LANE \
  --rev 718a1e987febd32eb78ebc65adfe939f23b3de63 \
  --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685
```

The first command prints `SCORECARD.md` and `LOG.md` among the changed paths (content
between measured revision and tip) → the landing shape violates the criterion. The
second command's output is already recorded at
`corpus/lessons/round-43-verifier-spotcheck.md:28`: `m7=1 total=1 C2_R43_PASS=false`
(exit 1) → the round must not be admitted. The same check passes the compliant shape in
which the tip diff lists only receipt/report files.

## Notes

- `considerthese/2026-10-25.md:66-68` (proposal 1) originally framed the remedy as a
  morning drift report ("list the commits between the measured commit and the landing
  tip ... so it is caught before the closure"). The contract adopted only the re-run
  half, dropping the drift-listing half — which is the half that would actually have
  caught round 43.
- No counter was run outside the permitted revs (`--rev 5891bdb...` / freeze); the
  round-43 re-run result is cited from the committed closure lesson, not re-executed.
- Tools installed/updated: none. Scratch used: `/tmp/tameshi-r45-CritDriftClaim/`.
