# W2CriticC2Axis — round-36 w2 — C2 axis-name attack, receipt side

Seat: leaf critic, read-only. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Lane tip at review: `fbb01cf` (verifier spot-check commit); measurement commit `b455001e2589b3f4f471d94a3de7e5e549b9f54c`; frozen counter commit `e423c41b`; v2 sha256 `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` (verified at tip via `git show`). No tools installed; no counter runs consumed — the kill rule's one deciding run stands and was not re-executed.

## What I attacked

The receipt-side question: the v2 deciding run re-executes 16 copies and re-confirms the round-35 capability — is the round's real product the **predicate repair** (operability of the audit) rather than depth? And the best axis name per AXES.md's surface naming.

This re-attacks the same surface `w1/CriticC2Scope.md` defended (`AGREE`), from evidence CriticC2Scope did not diff: the two deciding receipts against each other.

## Counterexample — the receipts themselves answer yes

**1. The deciding run carries zero new behavioral information.** The 16 `COPY` rows of
`.ufo/evidence/round-36/after/c1v2-at-b455001e.stdout` are byte-identical to
`.ufo/evidence/round-35/after/c1-at-34fa5b0c…stdout` (verified by `diff` of the grep'd COPY
sets — zero differences). The predicate lines are identical except `rev=` and the label. So the
round's flagship receipt is, for the audit object under test, a *re-attestation*: same tool
bytes (`6188db16…`), same runner (`a7d3f2dd…`), same panel, same verdicts.

**2. The genuinely new information is three constants and one discrimination.** The v2 diff is
confined to the PASS expression: `c1-measure-v2.py:538-544` adds
`pub_kill_slots==6 && pub_accept_slots==3 && pub_distinct==9` (targets frozen at `:68-70`);
v1 at `.ufo/evidence/round-35/c1/c1-measure.py:516-521` required only
`pub_kill == pub_kill_slots` — vacuously satisfied at 0/0. The 6/3/9 values are not new domain
knowledge; they were copied from the round-35 receipt's own printed fields (`pub_kill=6/6
pub_accept=3/3 pub_distinct=9` at `34fa5b0`). The mutant receipts
(`control/v1-at-emptypanel.stdout` `PASS=true` exit 0 vs `control/v2-at-emptypanel.stdout`
`PASS=false` exit 1, same mutant rev `91373d55`) demonstrate the instrument now discriminates a
degenerate input it previously certified. That is a *correctness repair to the verifier*, not a
knowledge gain about the audited artifact.

**3. AXES.md rubric fit.** `depth` = "verifiable technical detail — decision tables with real
thresholds, named error signatures, cited sources"; the signal is "a reader can act on SKILL.md
alone." The counter is evidence apparatus, not reader-facing knowledge; SKILL.md gains nothing
for C2, and the lane's own depth measure (recorded-case ledger, command D) prints
`recorded_cases=9 depth_score=9` — the claim itself discloses no depth-rubric move. The
predicate's 6/3/9 constants are thresholds in code, but applying "decision tables" to the
measurement instrument makes every counter fix a depth claim — the axis stops separating
knowledge from the apparatus that measures it.
`operability` = "runnable artifacts … a checklist item can be run and produces the stated
outcome." The counter *is* the lane's executable gate for "the tally audit holds." On an
emptied panel it emitted the stated outcome `PASS=true` for a condition that did not hold —
exactly the class operability covers (an artifact whose run produces an outcome diverging from
what it states). CriticC2Scope rejected operability because "the v1 counter already ran" — but
operability's rubric is *run-and-produces-the-stated-outcome*, not *runs*; a verdict that is
vacuously true on degenerate input is the artifact failing its stated outcome.

**4. The lane's own surface convention selects operability.** The naming convention ("name the
axis by the surface the round changed, not the number it prints" — coined in the r35 SCORECARD
block, `SCORECARD.md:1684`; note it is **not** a literal AXES.md section — AXES.md has no
section titled "name the surface"; the nearest rubric text is the six-axis definitions table
and §Working the axes) applied to the audit-surface lineage:
r32 `operability` → r33/r34 `operability` → r35 `depth (declared surface), operability
(runnable artifact)` (both surfaces changed: new audit content *and* new runnable tool) → r36
`depth` alone — on the round where the change is **purely** on the artifact side (the audited
content — tool, runner, panel — is byte-identical; only the oracle's verdict completeness
moved). The label migrated toward `depth` exactly as the work became least knowledge-shaped.
Under the lane's own rule the changed surface is the verdict apparatus: the honest name is
**`operability` (surface: the audit counter's non-vacuity gate)**.

**5. Capability framing.** AXES.md §Capabilities: rows enter "through a round that demonstrates
the capability running"; v2 does distinguish what v1 could not (vacuous vs populated panel), so
"successor predicate" could arguably be a row or a re-statement. The lane declined
(`SCORECARD.md:1770` "a successor audit predicate, not a new repertoire capability") — a
defensible call — but that leaves the round's durable product booked only as an axis tag on an
axis it does not numerically or rubrically move.

## Strongest concrete finding (fixable defect): duplicate authority / stale evidence pointer

The `tally-audit-v3 runner audit` capabilities row admitted at round 35
(`SCORECARD.md:1694-1698`) pins evidence "counter `.ufo/evidence/round-35/c1/c1-measure.py` @
`d360a159…`". This very round demonstrated — with committed receipts — that this counter emits
`PASS=true` on a zero-slot panel. The row was **not** updated; the stronger attestation
(`after/c1v2-at-b455001e.stdout` under `c1-measure-v2.py @ 9eb8944c…`) exists but is cited by
no capability row. Two counters now live in-tree both claiming the audit verdict, the
superseded one still carrying the standing table's pointer. This is the same defect class as
r35-closure defect 1 (the dead `ResidualSentinelClosure.md` LOG pointer this round fixed
append-only), weaker degree: the pointer resolves — to an instrument demonstrated defective.
The capabilities table is the lane's *standing* statement (the round-31 re-statement treats row
values as current), so a future reader replaying the row's counter against a degraded panel gets
false assurance the record knows is false.

## What the counterexample does NOT defeat (mitigations, honestly recorded)

- No numeric inflation: `depth 9 → 9` is disclosed (`SCORECARD.md:1754`); no score was borrowed.
- The re-execution was not ceremony: the kill rule required one real default-mode run to populate
  `pub_kill`/`pub_accept` counts — so "re-executes 16 copies" is structurally necessary; its
  epistemic yield is nonetheless re-attestation + non-vacuity demonstration, not new evidence.
- `depth` is defensible under r35 precedent ("declared surface" tag) and no contract rule is
  violated — so the naming is a **tradeoff** the judge may accept, not an automatic reject.
- The verifier spot-check (`corpus/lessons/round-36-verifier-spotcheck.md`) verified C2's
  evidence but only quoted the axis label descriptively; it did not adjudicate the rubric fit.

## Impacted axes

- **calibration** (the wave's judged axis, and the lane's record quality): naming an instrument
  repair `depth` + leaving the capability row pinned to the vacuous counter overstates where the
  work landed — a restraint gap of degree, disclosed in score but not in label.
- **operability**: the true home of the move; unnamed, and its standing row left pointing at the
  superseded instrument.
- **depth**: used as a surface tag with no rubric-conforming detail added; precedent-dilution
  risk (instrument work becomes claimable as depth without reader-actable content).
- No identity change, no premature numeric saturation, no harmed axis score found.

## Smallest safe correction

1. (fixable defect — pointer repair, same discipline as this round's LOG fix): update the
   `tally-audit-v3 runner audit` capabilities row's evidence pointer to name
   `.ufo/evidence/round-36/c1/c1-measure-v2.py @ 9eb8944c…` + receipt
   `after/c1v2-at-b455001e.stdout`, with a supersession note ("v1 counter frozen, retained;
   vacuous on degenerate panels — v2 is authoritative"). Record-level, append-only; no re-run.
2. (tradeoff — naming): for the record, append a note that `operability` was the rubric-closest
   name (changed surface = verdict apparatus); do **not** retro-edit `contract.json`'s frozen
   `claims.C2.axis` — rewriting a frozen contract after data would be a worse defect than the
   label it fixes. Future counter-predicate claims should be named `operability` (or filed as
   capability re-statements) at freeze time.

## Exact commands run (revisions named)

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
diff <(grep '^COPY' .ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout) \
     <(grep '^COPY' .ufo/evidence/round-36/after/c1v2-at-b455001e.stdout)   # → identical
grep -v '^COPY' <both receipts>; cat control/{v1,v2}-at-emptypanel.{stdout,exit}
sed -n '500,532p' .ufo/evidence/round-35/c1/c1-measure.py                  # v1 predicate :516-521
read  .ufo/evidence/round-36/c1/c1-measure-v2.py:419-555                   # v2 predicate :538-544, targets :68-70
read  .ufo/evidence/round-36/contract.json                               # C2 axis string, kill rule, counting command
read  /home/vgpnk/Projects/shokunin/AXES.md                              # six-axis rubric; no "name the surface" section
sed -n '1605,1776p' SCORECARD.md                                         # r32–r36 blocks, capability rows, r35 naming convention
sed -n '1503,1539p' SCORECARD.md                                         # standing capabilities + axes re-statement
read  corpus/lessons/round-36-verifier-spotcheck.md                      # integrator verdict (evidence-verified, label unadjudicated)
git log --oneline -8                                                     # fbb01cf ← d9c496b ← b455001e ← e423c41b ← 796e08b
```

Files read: `AXES.md` (fleet root); `.ufo/evidence/round-36/contract.json`;
`.ufo/evidence/round-36/c1/c1-measure-v2.py`; `.ufo/evidence/round-35/c1/c1-measure.py`;
`.ufo/evidence/round-36/{after,control}/*`; `.ufo/evidence/round-35/after/c1-at-34fa5b0c*.stdout`;
`.ufo/waves/round-36/w1/{ReviewC2Claim,CriticC2Scope}.md`; `SCORECARD.md` (r31–r36);
`corpus/lessons/round-36-verifier-spotcheck.md`; `.ufo/waves/round-36/dispatch-w2.json`.

Tooling: none installed.

**Verdict line: PARTIAL-DISAGREE — the receipt side supports the question's framing: the v2
deciding run's 16 COPY rows are byte-identical to round 35's (verified by diff), so the round's
durable product is the predicate repair plus re-attestation, and the rubric-closest axis name is
`operability` (surface: the audit counter's non-vacuity gate), not `depth`. `depth` remains a
defensible tradeoff under r35 precedent with honest `9→9` disclosure — not judge-must-reject —
but one fixable defect stands: the `tally-audit-v3` capabilities row still pins the v1 counter
`d360a159…` demonstrated vacuous this round, orphaning the stronger v2 receipt; smallest safe
correction is an append-only evidence-pointer supersession on that row, never a retro-edit of
the frozen contract.**
