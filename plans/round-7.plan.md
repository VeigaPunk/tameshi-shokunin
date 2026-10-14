# WWKD plan — tameshi round 7 (ufo-round-plan-v1)
Axis move: operability (post-service) — ONE move, three ordered legs: the
service's outputs pass to the fleet as instruments.
(1) Leg ledger: `--regression` replays EVERY recorded case at its pinned
    revision (kimi r2, kagi r3, tsukuroi r5, cite-check r6 if landed), and a
    case becomes a CONTRIBUTION — a pinned file set (target sha256 + spec +
    suite command + expected table) — so a fleet lane can add one without a
    tameshi code edit. Today the tool re-runs TWO worked cases (`597e1419…`
    `:66-69`, recorded expectations `:470-472`); round 6 claims the embedding
    of tsukuroi + cite-check (`plans/round-6.plan.md:20-22`).
(2) Leg fleet-run case: mado's round-6 self-service sweep (harness consumed
    read-only; `mado-shokunin/plans/round-6.plan.md:8-26`; declared evidence
    `corpus/knowledge/gate-mutation-proof.md`) is ATTESTED read-only:
    reproduced by tameshi from its pins, or its missing piece named. The lane
    operates; tameshi attests.
(3) Leg queue: the census queue drains at most ONE position and ONLY under a
    fresh round-7 opt-in — a lane naming a pinned target + a hermetic suite;
    the default head is surface-probe (`fleet-suite-census.md:282`). No
    opt-in by the dispatch checkpoint → the no-opt-in line is the record;
    position held; nothing forced (`fleet-suite-census.md:249-291` contract).

Design-time state (frozen 2026-10-14T17:40Z, PREP-T7 lane; this is a design,
every count re-measured at dispatch): HEAD `e0c453e` (14:33), tameshi tree
clean; tool `597e1419…` 1001 L; SKILL `928e073f…` 791 L (the 4th-case list
`:776-792`); round 6 in flight — no round-6 content landed at this read, its
scribe draft appearing (`plans/round-6-record-draft.md`); probe retained:
`/tmp/w5-prept6-cite/work/results.tsv` — K1/K2/K4 SURVIVED, K3 KILLED against
the pinned cite-check bytes (`40573448…`, kumitate HEAD `175de6b`).

Claim: round 7 makes the method's outputs fleet-facing and replayable. The
ledger lands as the receipt tameshi's records cite for every kill-rate claim —
`REGRESSION: PASS (cases=N passed=N)` with per-case pins (target + tool) and
the migration behavior-preserving (`flips=0`, each case's recorded table
intact); N = 4 with round-6's embedding (+1 if the fleet-run case
reproduces). The contribution contract is published (what a case must carry);
the first fleet-contributed case is attested; the queue moves one position iff
an opt-in names a target — else the no-opt-in line stands as the measured
state of the standing offer.

Also: round-6 clauses are the precondition set — checked at dispatch, never
assumed (`plans/round-6.plan.md:30-34`): the cite-check service note with its
kill table (if landed, it is ledger case #4 at the recorded pins), the
`REGRESSION: PASS` embedding, kumitate porcelain-clean, the SKILL opt-in
contract. An unlanded clause is carried as named debt and the ledger carries
what actually landed.

Anti-claim: no opt-in is a complete round outcome (recorded, never hedged
into a claim); a fleet-run case that fails reproduction is a FINDING — the
failing cell named, the sibling's note left read-only, the finding travels as
tameshi's recommendation; the migration is behavior-preserving for recorded
cases or the divergence is the finding (no re-sweep by hand — replay goes
through the ledger); the 4th case only to falsify: a sweep case beyond the
three measured (r2/r3/r5) admits itself only as a falsifier per
`SKILL.md:776-792` (a second JS-family gate as the author-vs-language test, a
coordinated rewrite, a JS unreached arm, a rate outside [50,80],
structural-guard mutants, B7/B8/B9 re-runs) with its hypothesis pre-registered
at dispatch — never another confirming 80 %-shaped sweep (round-6's own
anti-claim carried forward); sibling trees read-only (kumitate, mado
porcelain-clean before/after); hermetic scope — cite-check's integration group
stays a declared skip.

Measure: tool selftest green incl. the contributed-case path; `REGRESSION:
PASS` over all embedded cases, per-case pins + `flips=0` re-verified against
each recorded table; the attestation note (working name
`corpus/knowledge/kill-rate-ledger.md`): the per-defect cross-check table
against mado's note or the named missing piece; the queue record (engagement
#2 pins + kill-rate table + survivor probes + restore proof, or the no-opt-in
line); SKILL append = the contribution + attestation contract; every quoted
count carries its command.

Write scope: this file only (PREP-T7). Round-7 execution scopes assigned at
dispatch; this lane's scratch `/tmp/w6-prept7-*`.