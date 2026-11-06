# Round 90 — frozen plan (tameshi, L1 TameshiR90, attempt 1)

Base `4e1c10e0cfcc1e7533f1fc71a1b3b615aa60a7e0` (round-89 closure spot-check tip). Pre-freeze
commits: `33dd6e47` (C1 spec + pre-registered predictions + expectations, alone), `dd0ddce9`
(expectations amendment 1, alone, before any control receipt), `a90218cc` (instruments),
`3cf905bc` (C1 control receipts; C2 manifest v2, fix generator, controls driver),
then the C2 v2 control receipts in the freeze commit's parent (see § Controls). This file is
the freeze; nothing below changes after any seat scores.

## Fresh-start reads (Amendment 46/47)

Read before declaring: rounds 87, 88, 89 closures (MANIFEST tameshi rows for 87-89) and
`corpus/lessons/round-8{7,8,9}-verifier-spotcheck.md`. One class killed all three: the claim
was that a lane-built instrument certifies something (a counter, a ledger leg, a witness), and
the kill was a counterfeit or a runner the instrument accepted while the work was not done
(r87 `cf-c`/`cf-oid`, r88 `parked`/`stub`, r89 T89E2 alias runners and the T89C1 counterfeit
witness). This round's C1 is chosen so that no lane instrument's printed figure is evidence:
the counter executes the fleet gate itself, from git objects, and the only lane bytes it
compares against are the case note's verdict cells. A counterfeit that passes must contain the
true verdicts, which is the claim.

## Claims (two; causally separable)

### R90-C1 — coverage: a reproducible mutation case on the fleet's own registry gate (sourced)

Surface: `scripts/sources-census.sh` in the fleet repo at `f47ad6ba8d306f8125597401cb2ce45c1297a593`
(blob sha256 `3fb72615…4e30`), measured under its own `selftest` mode. It is the first
fleet-root gate the lane measures; all eleven ledger legs are sibling-lane gates. The gate
is read-only: every mutant is a scratch copy materialized from the fleet's object store.
The case is NOT added to `tools/mutate-and-run.sh` and claims nothing about the ledger.

Spec: `.ufo/evidence/round-90/c1/census-mutants.json` (sha256 `ce8983d5…e290`, committed in
`33dd6e47` before any run), 12 single-edit mutants C01-C12, each with a pre-registered verdict
prediction (`pre-freeze/expected.tsv`) and a witness registry.

Counting command (frozen, sha256 `d7365bbb…b528`):

    python3 -I .ufo/evidence/round-90/c1/measure.py --repo <lane> --rev REV --work <empty dir>

Predicate (the same condition as `measure.py`'s `ok = all(conj.values())` and its receipt label
`C1_R90_PASS=true`): pin, spec, green (pristine selftest exit 0 + `selftest ok`, twice), canary
(pristine + `exit 97` after line 1 exits 97), every mutant valid (old string once, new ≠ old,
`bash -n`), no trivial mutant, no inconclusive or unstable verdict (two runs each), the case note
`corpus/knowledge/mutation-case-fleet-sources-census.md` present with one row per spec id whose
verdict equals the derived verdict, exactly one `measured: K/N killed` line equal to the derived
counts, every SURVIVED row's witness differs between pristine and mutant, the note's `source:`
line cites an S-id > S315 that is `mined` in `corpus/SOURCES.md` with the note in `used-by`, a
`corpus/README.md` table row names the note, and n ≥ 10.

Before (do-nothing): at base `4e1c10e0` → `C1_SETUP spec-absent-at-rev`, exit 2
(`pre-freeze/controls/CTL1-nowork-base.out`); at `33dd6e47` (spec, no note) →
`note=false … C1_R90_PASS=false`, exit 1 (`CTL1b-nowork-A.out`). Target: `C1_R90_PASS=true`,
exit 0, at the landing revision.

Kill rule (any one kills C1):
- (a) any committed state — lane or scratch clone, any seat's — that does not hold the true
  verdicts of these mutants under the gate's own selftest reaches `C1_R90_PASS=true`;
- (b) a non-author execution of the gate's own `selftest` on a spec mutant (the exact edit, a
  scratch copy of the pinned blob and fixtures, an ordinary fleet shell environment) gives a
  verdict different from the note's row (the measurement is not reproducible outside the
  counter's environment);
- (c) the note states a fact about the gate (a line, an arm, a fixture, a figure) that the pinned
  blob or the committed receipts contradict;
- (d) the cited new S-id was not opened this round (no Gate row with URL, access date and a
  located quote of ≤25 words in `corpus/lessons/round-90.md`).

Declared limits (not kills): the canary shows the copy runs but cannot show which selftest arm
executed a mutated line; a SURVIVED witness proves non-equivalence on one registry, not that the
behaviour matters on real registries (the connector seat measures that separately, report only);
the kill-rate 5/12 describes this spec, not the gate's strength against all faults.

### R90-C2 — calibration: the round-89 closure's routed record defects 1-4 closed over committed bytes

Population (frozen): `tools/defect-bind-r90.json` v2 (sha256 `c5287003…9d95`), five rows:
README coverage-map row for `knowledge/kernel-witnessed-ledger.md` (item 1), the entry citing
that row (item 1), the round-89 lesson's appended corrections for the trend count and the
mkcheck2 reason (items 2, 3), the SKILL registry row for `tools/ledger-witness.py` marked
not admitted (item 4), and the `tools/registry.json` row's figure bound to an executed selftest
receipt (item 4). Item 5 (the lane's own routed successors) is carried, not measured.

Counting command (frozen, sha256 `6b0a7070…c8ba6`; also in `pre-freeze/instrument-sha256-v2.txt`):

    bash .ufo/evidence/round-90/c2/measure-c2.sh <lane> REV <empty dir> [MANIFEST_SRC]

Predicate (label `C2_R90_PASS=true`): manifest pinned AND `DEFECT_BIND: rows=5 closed=5 open=0
unexpected=0` with exit 0 AND `registry-check.py --only ledger-witness-selftest` exits 0 with
`REGISTRY_CHECK: held=1/1 superseded=0` (the row executes the real tool's selftest).

Before: base `4e1c10e0` → `rows=fail registry=fail` (defect-bind setup exit 2: the R89-4b
receipt is absent; every doc row `section-absent`), `C2_R90_PASS=false`
(`pre-freeze/controls/C2-nowork-base.out`). Target: `C2_R90_PASS=true` at the landing revision.

Kill rule: (a) a committed state reaches `C2_R90_PASS=true` while a non-author reading finds any
of routed items 1-4 not actually repaired; (b) any standing no-harm sweep regresses between base
and landing: `tools/selfstate-freshness.py` (rows/match/stale/unexpected), its `--pin-audit`,
`tools/registry-figure-bind.py`, `tools/pointer-recheck.py`, and `tools/registry-check.py` over
every pre-existing row.

## Controls (pre-freeze, committed before this file)

C1 (16 states, `pre-freeze/controls/CTL*.out`, summary `C1-summary.txt`): CTL14-pos (honest
fixture note in a scratch clone) → PASS; CTL2-flip → `mismatched0=false`; CTL3-figure →
`figure=false`; CTL4-ids → `ids=false`; CTL10-source → `source=false`; CTL16-oldsource →
`source=false`; CTL15-coverage → `coverage=false`; CTL5-spec → `spec=false`; CTL6-noop →
`invalid0=false`; CTL7-syntax → `invalid0=false`; CTL8-absent → `invalid0=false`; CTL9-equiv →
`witnessed=false`; CTL11-trivial → `trivial0=false`; CTL12-pin → `pin=false`. Spec-edit controls
also fail `spec` (by design: the spec is pinned). CTL13-canary was dropped (amendment 1; disclosed).

C2 (`C2-*.out`): nowork-base and nowork-instr → `rows=fail registry=fail`; C2-pos → PASS;
C2-wrongsection → `rows=fail` (R89-1a `section-absent`); C2-bogus-registry → `registry=fail`
(rows still close: the receipt row alone is forgeable by a receipt written outside the row,
which is why the live registry conjunct exists). Manifest v1 controls are kept under
`controls/superseded-manifest-v1/` (v1 misread the receipt-tokens semantics; repaired before
freeze, see lesson M1).

## Data seen before the freeze (disclosed)

The 33dd6e47 no-work run derived all twelve verdicts (5 KILLED, 7 SURVIVED; 12/12 predictions
held). The predicate fixes no kill-rate target, so the observed data cannot steer it.

## Wave

One v1 wave `r90-w1`, 14 seats (attack seats 6: two reviewers, two critics, one
mutation-tester, one labrat). Items: independent reproduction of every verdict outside the
counter (kill rule b), no-harm sweeps at base, survivor-killing selftest arms drafted for the
fleet (report-only, never pushed), case-note draft, two source scouts, counter review, claim
attacks on C1 and C2, a mutation test of the C1 counter, a fleet impact scan of the survivor
classes, a TZ/locale stability probe, and a scratch-safety audit.

## Assimilation and considerthese

Assimilation: none this round (no staged `merge/tameshi/` theme serves a fleet-gate mutation
case). considerthese: `2026-11-05.md` idea 4 (mutation-survivor table) is the one proposal
mined (`considerthese/2026-11-05.md:73-74`, a standing per-tool survivor table): this round applies it to
one fleet gate — the case note carries a survivor table with a witness and a drafted killing arm per
survivor. The daily standing panel over `tools/*.py` stays unimplemented.
