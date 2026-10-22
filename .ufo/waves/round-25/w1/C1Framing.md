# C1Framing — attack on the framing of round-25 C1

Seat: TameshiR25.C1Framing (critic, leaf). Judged on: calibration.
Frozen contract: `.ufo/evidence/round-25/contract.json` (lane revision c9ff09f, base 1f73157).
Mode: read-only. No commands executed in a clone, no counter/suite/runner executed, no git writes, no installs (tooling directive: nothing installed or updated).

## Verdict

1. **C1 does not count calibration mismatches.** `c1-measure.py` counts a conjunction per item: a SCORECARD table row whose first cell starts with the label, AND an executed check that passes. The SCORECARD test reads only the label and ignores the row's content. An overclaiming row and a missing row both score 0, so overclaim is never reported as its own category. A row saying the item is open still scores 1 if the check passes. So this is a completeness count of "recorded and executed" items. It is not a count of mismatches between what the lane says about itself and repo state.
2. **It is also more than a renamed fixture count, but not by much.** Two of the three checks (R1, R2) are mutation-fixture kill sweeps against `tools/command-binding.py`. That gate is byte-unchanged from base 1f73157 to 5b69fb2. Static tracing predicts both sweeps already pass at the freeze revision 2a97ec1 (`[INFERENCE]`, not executed). If so, the only lane-state change for R1 and R2 between freeze and after is two SCORECARD label rows. R3 is a real record check: a 34-row disposition ledger with fail-capable doctored-copy controls.
3. **0/3 at base reflects missing files only.** The baseline fails by construction: the counter's own files (STAGE list) and the ledger file do not exist at 1f73157. `c1-before.json` says so itself. It is not three behaviors that were failing before.
4. **Narrowing: R1 is faithful, R2 narrows, R3 weakens the meaning of "coverage".**
   - **R2 is narrower than "re-run guard sweep".** Round 23's sweep used ten guard anchors, and all ten still occur exactly once in today's gate. Round 25 re-runs four of them verbatim, re-targets three, adds one new one, and drops bool-exit, snapshot-pin and empty-requirements.
   - **R3's counter accepts a re-attack that died as a disposition.** So "34/34 dispositioned" can hold with almost no restored falsification coverage.

## Evidence

### What the counter actually counts
- Label-only SCORECARD test: `c1-measure.py:144` uses `re.search(r'^\|\s*%s\b' % label, scorecard, re.M)`. Any table row anywhere in `SCORECARD.md` that begins with `R23-ROUTED-n` counts, including a "planned", "open" or "rejected" row.
- Conjunction: `c1-measure.py:146` sets `item['dispositioned'] = bool(item['holds'] and recorded)`. There is no field for "the row claims X but the check says not-X".
- Strongest counterexample: `| R23-ROUTED-2 | open — not re-run |` plus a passing sweep counts as dispositioned. `| R23-ROUTED-2 | done |` plus a failing sweep scores the same 0 as having no row at all.
- The lane's calibration scalar is SHONEN promotion restraint (`SCORECARD.md:67`). C1 correctly keeps it at 8 and is a "calibration; capability" claim like rounds 12–14 (`SCORECARD.md:303,354,415`).

### Baseline is missing files (by construction)
- `c1-measure.py:43-47,128-136`: if any STAGE file is missing, R1 and R2 return `holds: False, reason: absent: …`. Here STAGE includes `c1-suite.py`, `multitoken-cases.json` and both `.spec` files. R3 returns "disposition file absent" (`:102-103`).
- `c1-before.json` "note": "capability-absence baseline: the round-25 ruler files and the disposition file do not exist at base; SCORECARD carries no R23-ROUTED rows."
- `GIT_OPTIONAL_LOCKS=0 git diff --stat 1f73157 5b69fb2 -- tools/command-binding.py tools/mutate-and-run.sh SCORECARD.md .ufo/evidence/round-23 .ufo/evidence/round-24` printed nothing. The full `--stat` lists only round-25 evidence, wave files, `tools/mte-interop.py` and vendor tarballs. The gate under test is untouched.
- Static kill trace for the round-25 R1 fixtures (`multitoken-cases.json`) against the current gate:
  - M1 (any→all) is killed by `mt-missing-first`.
  - M2 (first token only) is killed by `mt-missing-middle`.
  - M3 (last token only) is killed by `mt-missing-first`.
  - M4 (first sorted requirement only) is killed by `mt-offending-sorted-second`.
  - M5 (contiguous, ordered tokens) is killed by `mt-clean-reordered`.
  - M6 (findings reset per row) is killed by `mt-offending-sorted-first`.
- Static kill trace for R2 (selftest cases at `command-binding.py:148-158`):
  - G1 is killed by `source-read-not-command`, G2 by `wrong-cwd`, G3 by `stale-revision`, G4 by `wrong-exit`.
  - G5 is killed by `stderr-cannot-supply-token`, G6 by `missing` and `unknown`.
  - G7 is killed by `duplicate`, G8 by `duplicate-requirement`.
- All 14 kills are therefore expected at the freeze revision on today's gate `[INFERENCE]`.
- The lane's own criterion QUALITY48 (`corpus/QUALITY.md:489-500`) says: "A gap already caught at the base, such as round23's any-token stdout mutant, stays in the denominator as a control. It does not count as a repair."
  - M1 is labelled "(round-23 closure mutant)" in `multitoken-mutants.spec`.
  - Under the lane's own rule, R1 and R2 are controls and evidence repair, not detector repair. The contract's `"kind": "repair-first"` must not be read as a gate repair.

### Routed wording, three sources compared
| Source | Item 1 | Item 2 | Item 3 |
|---|---|---|---|
| MANIFEST `rounds[421].notes` (python json parse) | "multi-token stdout fixture in the ruler" | "re-run guard sweep" | "dead-falsifier coverage gap" |
| Spot-check `round-24-verifier-spotcheck.md:37` | same | "a receipted guard-sweep rerun" | "dead-falsifier coverage disposition" |
| Contract C1 statement | same as spot-check | same as spot-check | same as spot-check |

- Origin of item 1: in the closure rechecks of `rounds[421].verification.rechecks`, "an all-vs-any stdout-token mutant survives the ten-case ruler (single-token fixtures) but is killed by selftest all-of-tokens."
- Origin of item 2: in round 23, `MutationDesign.md:76` notes the sweep ran at intermediate 496d212, not at the delivered revision: "That is not a new execution of the mutation suite."
- Origin of item 3: `rounds[421].verification.wave_accounting` says "W2 30/64; 34 aborted at author death including all 20 reviewers, so falsification coverage was materially thinner than dispatched."
- Spot-check routing item 1 (`:63`): "Adjudicate the three original closure-routed items explicitly, including a retained negative control that can fail. Keep old ruler/target/expected snapshots immutable."
- Population check: the fourth routed-and-unpredicated item, "loose stdout tokens", was recorded by round 24 as "left frozen … open" (`corpus/lessons/round-24.md:133`, `corpus/knowledge/replay-projection-hardening.md:74`). So "the three … left unrecorded" is an accurate population.

### R1 — faithful to the origin; one adjacent gap is out of scope
- The origin was the command-binding gate's ten-case, single-token ruler. R1 adds ruler-owned multi-token fixtures run through the gate's public CLI (`c1-suite.py:43-71`). The fixtures are 2–3 tokens per requirement, including a two-requirement offending-order pair.
- Because the spot-check requires old rulers to stay immutable, a new round-25 ruler is the only legal place for them. "In the ruler" therefore means "in a ruler". The round-23 ruler (`.ufo/evidence/round-23/measure.py`) and the round-24 ruler stay single-token.
- Round-24 `ClosureCarry.md:57-67` (F1) extended the item to a token-dropping projection at `tools/registry-replay.py:101`. R1 does not touch that projection. It is not part of the routed origin, so this is not a narrowing, but C1 must not be read as covering it.

### R2 — narrower than "re-run guard sweep"
- Round-23 anchors: `.ufo/evidence/round-23/mutate.py:13-22` declares ten mutants:
  - argv, cwd, revision, membership, duplicate-command, exit, stdout
  - bool-exit, snapshot-pin, empty-requirements
- Command and observed output (read-only string count with `ast.literal_eval` of `MUTANTS` against `tools/command-binding.py`):
  `argv 1 · cwd 1 · revision 1 · membership 1 · duplicate-command 1 · exit 1 · stdout 1 · bool-exit 1 · snapshot-pin 1 · empty-requirements 1`.
  A literal re-run was therefore mechanically feasible on today's gate.
- How the round-25 `guard-mutants.spec` compares with round 23:
  - **Verbatim (4):** G1 argv, G2 cwd, G3 revision and G4 exit use the same anchors.
  - **Re-targeted (3):** G5, G6 and G7 delete the finding line (`findings.add('STDOUT_MISMATCH')`, `findings.add('MEMBERSHIP_MISMATCH')`) or the return line (`return 1, ['DUPLICATE_COMMAND']`). Round 23 instead disabled the guard condition (`if any(...)`, `if set(receipts) != set(requirements):`, `if row['name'] in receipts:`). Same guards, different mutants.
  - **New (1):** G8 duplicate-requirement.
  - **Dropped (3):** bool-exit (`command-binding.py:90`), empty-requirements (`:70`) and snapshot-pin (`:125`, inside `check()`). Snapshot-pin is the digest guard behind every pinned bundle.
- The spec header says "G2, G3, G6 and G7 are the four guards round 24 did not re-mutate". That repeats an undercount from `ClosureCarry.md:40`. Round-24 K1–K4 (`.ufo/evidence/round-24/measure.py:24-36`) only weakened argv, exit and stdout. So seven round-23 guards went un-re-mutated in round 24, including the three that round 25 also drops.
- No other round-25 seat closes this. `MtGuardGaps` is scoped to "evaluate() (lines 65-113)" (spec.json item prompt), so snapshot-pin in `check()` is outside every round-25 mutation seat.
- On "receipted": the counter re-runs the sweep inside a `TemporaryDirectory` and discards the logs (`c1-measure.py:126`). Its predicate does not require a committed receipt. The receipt is whatever after-record the author commits. That is acceptable, because any verifier can reproduce it by re-executing, but "receipted" is not a counted predicate.

### R3 — a complete ledger, not restored coverage
- Population: `.ufo/waves/round-23/original-outcomes2.json` has 64 rows, `Counter({'failed': 34, 'completed': 30})`. The dead roles are reviewer 20, connector 10, revenger 2 and scout 2, matching the closure's "34 aborted". The round-23 W1 death (SourceScope) is outside it, which is consistent with the closure's wave-2 sentence.
- Dispatch: `.ufo/waves/round-25/spec.json` holds 34 `Re<name>` items, and the set of dead seats with no re-attack item is `[]`. Every dead seat is re-dispatched.
- Weakening: `STATUSES` (`c1-measure.py:48`) counts `reattack-seat-died` with non-empty error text as dispositioned (`:83-86`).
  - The flip control (`:107-111`) only needs one AGREE or FINDING row to flip. So 33 re-deaths plus 1 AGREE gives `holds: true`.
  - All 34 re-deaths fail only because the flip control finds nothing to flip.
  - So R3 measures ledger completeness and checker fail-capability. It does not measure how much falsification actually ran.
- Minor: re-attack prompts require the verdict on the report's LAST line. The counter only requires exactly one `^R23-REATTACK <name>: (AGREE|FINDING)` line anywhere (`:91-94`). This errs conservative: a duplicated line fails.

### The counter does not check its own frozen bytes
- `c1-measure.py` reads REPO's copies of the suite, fixtures and specs (`:128-132`) without comparing them to the contract's `fixtures_sha256`, `specs_sha256` or `suite_sha256`.
- Counterexample: a `guard-mutants.spec` trimmed to G1 alone still gives `holds: true` (`ids == witnessed == ['G1']`, `:68-69`).
- Today's bytes match the frozen pins: `sha256sum` printed `b18460c7…` for measure, `ae33a04b…` for suite, `ea64fca9…` for fixtures, `2a496199…` for multitoken spec and `636909ed…` for guard spec, all equal to `contract.json`. Byte identity at the after revision remains a separate obligation for the judge.

## Impacted axes
- **Calibration (the claimed axis).** The claim words over-reach: "dispositioned" treats a re-death as resolved, "repair-first" can be read as detector repair, and "guard-sweep rerun" implies the round-23 set. The numeric scalar is correctly held at 8. No other axis is moved or harmed by the framing.
- **Depth/coverage.** Not claimed, and they must not be inferred from R1/R2 kills: those are controls under QUALITY48.

## Defect vs tradeoff
- **Fixable defects:**
  - R2 drops three round-23 anchors.
  - The "four guards" undercount.
  - Prose that might say "coverage gap closed" or "three repairs".
- **Tradeoffs the judge can accept if worded honestly:** these are frozen counter semantics.
  - The label-only SCORECARD test.
  - The baseline of missing files.
  - Re-deaths counting toward the ledger.
  - The counter not checking its own bytes.
- **What the judge must reject:** a closure or report that calls the 0→3 movement three previously failing behaviors, a gate repair, a calibration-mismatch count, a full re-run of the round-23 guard sweep, or restored falsification coverage.

## Smallest safe correction (no frozen bytes change)
1. **R2:** retain an uncounted, receipted run of round 23's own `.ufo/evidence/round-23/mutate.py --tool tools/command-binding.py --revision <after REV>` in a clone. That is literally the routed "re-run guard sweep" over all ten original anchors. Alternatively, state in the C1 row and report that bool-exit, snapshot-pin and empty-requirements were not re-run, and route them. Correct the "four guards round 24 did not re-mutate" statement to seven in an erratum. Do not edit the pinned spec.
2. **R3:** print `status_counts` (agree / finding / re-attack died) beside "34/34". Say "every dead seat has a disposition", not "coverage gap closed", unless re-attack deaths are 0.
3. **SCORECARD rows:** each `R23-ROUTED-n` row should state the observed check outcome in words. The integrator or judge should read the row content, because the counter does not.
4. **Judge obligation:** confirm the after revision's `c1-measure.py`, `c1-suite.py`, `multitoken-cases.json` and both specs still match the contract's sha256 pins.

## Strongest honest wording for C1

> C1 (calibration; record repair of round-24 spot-check routing item 1, not a detector repair; calibration ordinal stays 8). The three round-23 closure-routed items that round 24 left unrecorded now each carry a SCORECARD row and a frozen round-25 executed check:
> (1) seven ruler-owned multi-token stdout fixtures, run through `tools/command-binding.py`'s public CLI, kill six single-edit stdout/iteration mutants, each with an explicit `FIXTURE … FAIL` witness;
> (2) a fresh eight-defect guard sweep of the current gate's selftest kills every defect with an explicit `CASE … FAIL` witness — four anchors verbatim from round 23's ten-mutant sweep, three re-targeted to finding/return lines, one new; round 23's bool-exit, snapshot-pin and empty-requirements anchors are not re-run by this check;
> (3) a ledger gives each of the 34 round-23 wave-2 seats that died exactly one disposition — a committed AGREE/FINDING re-attack report or a recorded re-attack death — and two doctored copies of the ledger fail as required.
> The gate is unchanged since base, so the R1/R2 kills are controls under QUALITY48, not repairs. 0/3 at 1f73157 reflects missing files only (the counter's own fixtures and the ledger did not exist), not three failing behaviors. The SCORECARD test checks only that the label is present. Re-attack deaths count as dispositions, not restored coverage. Not a numeric score uplift, not producer authentication, not promotion.
