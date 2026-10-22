# QualityCriterion — draft criterion for routed-item identity (round 25, wave 1)

Seat: `TameshiR25.QualityCriterion` (critic, leaf). Draft only: `corpus/QUALITY.md` is not edited.
Lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`; the checkout HEAD is `5b69fb2`, and `c9ff09f` is an ancestor of it.

## Verdict

1. **Drafted criterion 50 would have refused round 24.** Round 24's contract cites routed provenance. Its 11 predicates and the round-23 closure's 11 routed items have the same count but different identities. Five routed items have no predicate and no frozen disposition, among them the three closure-only items. Criteria 12, 44 and 48 each check something adjacent, but none of them compares a claim's population with the items its cited routing source actually lists.
2. **Round 25's c1-measure population fails the draft at freeze, on one of three items.**
   - **R23-ROUTED-1 and R23-ROUTED-3 pass.** Both need one disclosure sentence each.
   - **R23-ROUTED-2 fails.** It is labelled a "rerun" of the round-23 guard sweep, but `guard-mutants.spec` is a different population:
     - three of the ten round-23 anchors are dropped, although each is still live exactly once at base and at the lane revision;
     - three are re-anchored to different lines;
     - one defect is added.
   - None of this is named. The c1-measure counter cannot see it: it checks only that the spec's own defects are killed.

## What the cited criteria already cover, and the gap

- **QUALITY12** (`corpus/QUALITY.md:39-42`): a frozen declaration reports all declared defects and unresolved denominators. It governs defects the declaration itself names, not items an upstream routing source names that the declaration omits.
- **QUALITY44** (`corpus/QUALITY.md:432-439`): a frozen mutation population never drops a stale anchor; it re-anchors and names the rewrite. This applies inside one population. It does not say that a "rerun" must carry the population it reruns.
- **QUALITY48** (`corpus/QUALITY.md:489-502`) and its execution note (`:506-510`): a routed gap counts as repaired only when a frozen predicate fails at base and holds after. Tool absence is new capability, not repair. Criterion 48 governs each item that has a predicate. It never requires every routed item to get either a predicate or a disposition. That is why round 24 passed its own counter while omitting items.
- **Spot-check** `corpus/lessons/round-24-verifier-spotcheck.md:34`: "Counter population and original routed breadth do not coincide; three closure-routed items remain unrecorded … Unprovable as declared". The routed list itself is at `:37`.

## Evidence for the round-24 counterexample (hand-derived mapping)

The routed source cited by the round-24 contract is `.ufo/evidence/round-24/contract.json` `"sources"`: `fresh-adjudication.json routed_not_executed; MANIFEST rounds[421] closure notes`.

- The fleet `MANIFEST.json` `rounds[421].notes` (read-only JSON parse) lists "Route next round": eight deferred repairs, then "multi-token stdout fixture in the ruler, re-run guard sweep, and dead-falsifier coverage gap". That makes 11 routed items.
- `.ufo/waves/round-23/fresh-adjudication.json` `routed_not_executed` has 8 entries. These are the same eight deferred repairs.
- The round-23 lane SCORECARD successor list (`SCORECARD.md:1118-1125`) names only 7 items. It omits the loose stdout tokens and all three closure items, so those three exist only in fleet prose.

| Routed item (closure) | Round-24 predicate | Frozen round-24 disposition |
|---|---|---|
| argv swap-name / name-insensitive mutant | K1 | — |
| negative-exit mutant | K3 | — |
| bundle_sha256 pins | K5, K6 | — |
| runner held/cleanup/external in projection | K7, K8, K10 | — |
| fleet-root realpath | K11 | — |
| bounded streams | K9 (size only; redaction dropped, `lessons/round-24.md:132`) | — |
| hash clone runner copy | none | none at freeze; "implemented … no predicate" only in post-hoc Erratum I (`lessons/round-24.md:128-136`) |
| loose stdout tokens | none | none at freeze; Erratum I and the residual correction (`lessons/round-24.md:133-134,236-239`) |
| multi-token stdout fixture in the ruler | none (K4 is the selftest any-token control, already red at base: `SCORECARD.md:1145-1146`) | **none anywhere** |
| re-run guard sweep | none | **none anywhere** |
| dead-falsifier coverage gap | none | **none anywhere** |
| — | K2 argv-casefold | author-added (`lessons/round-24.md:73`) |

A count check passes this table: the contract target is `{discriminated:11,total:11}` against 11 routed items. An identity check refuses it, with five routed items unmapped and two predicates that are not routed. The contract wording "eleven named … predicates routed by round23 critics and closure" therefore overstates the coverage. Round 24 conceded this only after the measurement, in Erratum I, and Erratum I still missed the three closure items.

## Draft criterion (proposed text, not appended)

> 50. A claim that cites routed provenance freezes a routed-item ledger with its contract, before any seat. Routed provenance means the claim says "routed by", or cites a closure or spot-check route list, or cites `routed_not_executed`.
> - The ledger has one row per item of every cited routing source. Each row quotes the item with its path:line or JSON pointer.
> - Each row maps the item by identity either to one or more counted predicates or to a non-counted disposition: `deferred` with an owner, `declined` with a reason, or `implemented-unpredicated`.
> - Each counted predicate also gets a row naming its routed item, or a label of `author-added` or `control`.
> - Matching counts never stand in for matching identities. A prose-only source is enumerated into rows; citing it whole does not count.
> - Some routed items name an existing artifact, such as "rerun X" or "in the ruler". Such an item maps to that artifact's exact population. Otherwise each member it drops, re-anchors or re-homes is named, in the manner of QUALITY44.
> - If any routed item is unmapped, the routed qualifier is unprovable. The claim is then worded as covered/total of the source, never as "the routed items".
>
> This narrows QUALITY12 and QUALITY48 and replaces neither.
>
> Captured by: `lessons/round-24-verifier-spotcheck.md:34,37`; `lessons/round-24.md` Erratum I.
>
> Falsifier:
> - The ledger check, applied to the round-24 contract against `MANIFEST rounds[421].notes` and `fresh-adjudication.json routed_not_executed`, must refuse. It names five unmapped routed items (clone-runner hash, loose tokens, multi-token ruler fixture, guard-sweep rerun, dead-falsifier gap), even though 11 predicates equal 11 routed items.
> - Adding those five rows as frozen dispositions, and rewording the claim to 6 of 11 routed items predicated, must pass.
> - Deleting any one row from that passing ledger, or relabelling K2 as routed, must refuse again.

Operational note: the falsifier needs a small checker that compares sets of (source pointer, item) pairs with predicate and disposition labels. No such checker exists in the lane. Until one lands, this criterion is rule text only. It is not failure-backed, the same standing that `QUALITY.md:536-538` records for criterion 49.

## Would the round-25 c1-measure population fail it?

**Claim-scope ledger (what the draft requires).**
- Round 25's C1 cites "round-24 verifier spot-check routing item 1" (`.ufo/evidence/round-25/contract.json:9`). Item 1 asks to adjudicate "the three original closure-routed items" (`round-24-verifier-spotcheck.md:63`).
- The population is R23-ROUTED-1, -2 and -3 (`c1-measure.py:43`), one per item, with no author-added or control members. Labels and count match.
- The identity clause is where it fails.

**R23-ROUTED-2 "re-run guard sweep": fails as frozen.**
- The routed artifact is round 23's ten-anchor sweep. Its anchors are listed at `.ufo/evidence/round-23/mutate.py:12-23`, and `.ufo/evidence/round-23/mutations-A.json` reports `killed 10, survived 0, inconclusive 0` at `496d212`. `SCORECARD.md:1114-1115` records that this sweep was not re-run.
- `.ufo/evidence/round-25/guard-mutants.spec` carries G1 to G8, which compare to round 23 as follows:
  - **Identical edits (4):** argv, cwd, revision and exit (G1 to G4).
  - **Re-anchored to different lines (3):** stdout (G5 drops `findings.add('STDOUT_MISMATCH')`, where round 23 disabled the `any(token …)` condition); membership (G6 drops `findings.add('MEMBERSHIP_MISMATCH')`, where round 23 disabled `if set(receipts) != set(requirements):`); duplicate-command (G7 drops `return 1, ['DUPLICATE_COMMAND']`, where round 23 disabled `if row['name'] in receipts:`).
  - **Added (1):** G8, duplicate-requirement.
  - **Dropped (3):** `bool-exit`, `snapshot-pin` and `empty-requirements`.
- Executed check: I extracted `tools/command-binding.py` with `git show REV:tools/command-binding.py` at REV = `1f73157` and REV = `c9ff09f`, then counted each round-23 `old` anchor and each round-25 `@old` anchor. All ten round-23 anchors occur exactly once at both revisions, and so do G1 to G8. The three dropped anchors are therefore live, not stale.
- The spec's only rationale (`guard-mutants.spec:3`: "G2, G3, G6 and G7 are the four guards round 24 did not re-mutate") neither names the drops nor maps the re-anchors.
- `c1-measure.py:59-69` holds an item when every defect *in the spec* is killed. A narrowed rerun therefore reaches 3/3 unseen.

**R23-ROUTED-1 "multi-token stdout fixture in the ruler": passes, with one disclosure owed.**
- The fixtures are re-homed. They sit in a new round-25 ruler (`c1-suite.py:4`, `multitoken-cases.json` `purpose`), not in round 23's ruler. That ruler stays single-token: `.ufo/evidence/round-23/measure.py:24,26` uses `['PASS']` / `['REJECTED']`. It must stay frozen (`round-24-verifier-spotcheck.md:63`).
- The re-homing is forced and legitimate. The ledger owes one sentence: the old ruler still cannot see the any-of mutant M1, and the fixture now lives in the round-25 ruler.

**R23-ROUTED-3 "dead-falsifier coverage gap": passes.**
- The dead set is the 34 `failed` rows of `.ufo/waves/round-23/original-outcomes2.json`. That file holds 64 rows: 34 failed and 30 completed. This matches the closure's "W2 30/64; 34 aborted" (`MANIFEST rounds[421].verification.wave_accounting`).
- Round 23's one W1 death, `TameshiR23.SourceScope`, was a scribe that got a 429. It is correctly outside a falsifier set. The ledger should say so explicitly.

**Interaction with QUALITY48, outside this item's scope but load-bearing.**
- `c1-before.json` labels the 0/3 baseline "capability-absence". Under the QUALITY48 execution note (`QUALITY.md:506-510`), all three items show new capability or disposition, not repair.
- The contract's `kind: "repair-first"` is fine as a lane label, but the report must not count these items as repairs.

**Round scope (not part of the draft).**
- A stricter round-wide version would require a frozen disposition for every item routed *into* round 25. That covers spot-check items 2 to 5 (`round-24-verifier-spotcheck.md:64-67`) and the "Routed to round25" items (`lessons/round-24.md:151-154,159,169-170,181,201-202,213`).
- That version would refuse round 25 at freeze. The contract carries only C1 (item 1) and C2 (frontier F1), and no ledger. Mapping those items is assigned to in-flight wave seats (`.ufo/waves/round-25/make-spec.py:154,180-182`), after the freeze.
- I kept the draft claim-scoped because round 24's refusal concerned the claim's own cited source. Whether to adopt the round-wide clause is the integrator's decision.

## Smallest safe correction

For round 25's R23-ROUTED-2, choose one:
- **(a) Smallest.** Before any after-measurement, add a contract amendment in the form of `contract-amendment-1.json`. It records a ledger row stating that the R2 sweep is a re-anchored, narrowed rerun covering 7 of round 23's 10 guards. It names `bool-exit`, `snapshot-pin` and `empty-requirements` as dropped with a reason, names the three re-anchored edits, and labels G8 as added. The C1 statement then says "narrowed rerun" instead of "rerun".
- **(b) Stronger.** In an amendment before after-measurement, add the three dropped anchors to the sweep with their round-23 edits. They are live exactly once at `c9ff09f`, so the frozen `specs_sha256.guard` changes in the open.

For R23-ROUTED-1 and R23-ROUTED-3, add the two one-sentence ledger notes above. For round 24, change nothing: its bytes stay immutable, and this is a successor rule.

## Commands run (all read-only; nothing written in the lane except this report)

- `git show {c9ff09f,1f73157}:tools/command-binding.py`, with output sent to two temporary `/tmp/qc-cb-*.py` files that were removed afterwards. A Python anchor count found every round-23 anchor and every G1 to G8 anchor exactly once at both revisions.
- Python JSON reads of fleet `MANIFEST.json` `rounds[421]` and `rounds[435]`, `fresh-adjudication.json` (8 `routed_not_executed` entries), `original-outcomes2.json` (34 failed, 30 completed) and `mutations-A.json` (killed 10).
- `rg` and `grep` over `corpus/QUALITY.md`, `corpus/lessons/round-2{3,4}.md`, `SCORECARD.md`, `.ufo/evidence/round-2{3,4,5}/` and `.ufo/waves/round-25/`.

Read-only git used `GIT_OPTIONAL_LOCKS=0`. No installs or upgrades. Statements marked as mappings are hand-derived from the cited lines. No checker was executed for the draft falsifier, because none exists.
