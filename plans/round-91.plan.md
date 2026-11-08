# Round 91 — frozen plan (tameshi, L1 TameshiR91, attempt 1)

Base `87d1635c8a1a90a405eb348da5ba3e8f93b4ae83` (round-90 verifier-spotcheck tip).
Pre-freeze commits: `ace200b5` (C1 spec copy + pre-registered predictions +
S318 source snapshots, alone), `343b0347` (sealed successor counter + controls
driver), `048c3f30` (C2 successor: manifest r91, fixes-v91, counter, controls
driver), `3d3eee6b` (controls driver repointed to the instrument commit — a
pre-receipt repair, discarded first battery kept under
`controls/superseded-driver-v1/`). This file is the freeze; nothing below
changes after any seat scores.

## Fresh-start reads (Amendment 58 fresh start)

Read before declaring: rounds 88, 89, 90 closures (spot-checks
`corpus/lessons/round-88-verifier-spotcheck.md`, `round-89-verifier-spotcheck.md`,
`round-90-verifier-spotcheck.md`). One class killed all three, in turn: r88's
`parked`/`stub` runner variants that the frozen counter accepted; r89's T89E2
alias runners and T89C1 counterfeit witness; r90's read-path holes V4
(`refs/replace` honoured) and V1 (an ambiguous row skipped) plus the same
token-binding class on the record-repair counter (T90C2). This round's two
claims are the routed successors: a sealed counter (QUALITY 139-140) whose
pre-freeze battery carries V1/V3/V4 and T90M1's four reachable controls, and
the C2 successor binding argv and tool pins (QUALITY 141). Do-nothing control:
at base 87d1635c the C1 spec path does not exist, so the counter refuses at
setup — the claim moves exactly the byte set that must exist.

## Claims (two; causally separable)

### R91-C1 — coverage: the sealed successor counter over the fleet gate (sourced)

Surface: `scripts/sources-census.sh` in the fleet repo at
`f47ad6ba8d306f8125597401cb2ce45c1297a593`, unchanged in round 91 (pin
sha256 `3fb72615…4e30` re-derived at freeze time from the live object store).
The case note `corpus/knowledge/mutation-case-fleet-sources-census.md`
already exists from round 90; the coverage move is that its verdicts now hold
under a sealed counter with the read-path holes closed, not a reopened
measurement.

Sealed successor: `.ufo/evidence/round-91/c1/measure-v91.py` (successor to
round 90's frozen counter, never edited). Sealing: every git read carries
`GIT_NO_REPLACE_OBJECTS=1` with `GIT_CONFIG_NOSYSTEM=1` /
`GIT_CONFIG_GLOBAL=/dev/null`, and the lane and fleet repos are checked for a
non-empty `git replace -l` before any read (QUALITY 139, from
`tools/defect-bind.py` round-82 hardening). The note is read by its
header-named `verdict` column; any ambiguous id-keyed row (duplicate,
missing, or a value outside {KILLED, SURVIVED}) refuses the state rather than
skipping it (QUALITY 140). Spec: `.ufo/evidence/round-91/c1/census-mutants.json`
(bytes identical to round 90's, sha256 `ce8983d5…e290`, copied at
`ace200b5` before the counter).

Counting command (frozen):

    python3 -I .ufo/evidence/round-91/c1/measure-v91.py --repo <lane> --rev REV --work <empty dir>

Predicate (the same condition as the counter's `ok = all(conj.values())` and
its receipt label `C1_R91_PASS=true`): pin, spec, green (pristine selftest
exit 0 + `selftest ok`, twice), canary, every mutant valid (old string once,
new ≠ old, `bash -n`), no trivial mutant, no inconclusive or unstable verdict
(two runs each), the case note present with one row per spec id whose verdict
equals the derived verdict in the header-named column, exactly one `measured:
K/N killed` line equal to the derived counts, every SURVIVED row's witness
differs, the note's `source:` line cites S318 mined with the note in `used-by`,
a `corpus/README.md` table row names the note, and n = 12.

Before (do-nothing): at base → `C1_SETUP spec-absent-at-rev`, exit 2. Target:
`C1_R91_PASS=true`, exit 0, at the landing revision.

Kill rule (any one kills C1):
- (a) any committed state — lane or scratch clone, any seat's — that does not
  hold the true verdicts under the gate's own selftest (or a false witness, or
  a false marker) reaches `C1_R91_PASS=true`;
- (b) a non-author execution of the gate's own `selftest` on a spec mutant (the
  exact edit, a scratch copy of the pinned blob and fixtures, an ordinary
  fleet shell environment) gives a verdict different from the note's row;
- (c) the note states a fact about the gate (a line, an arm, a fixture, a
  figure) that the pinned blob or the committed receipts contradict;
- (d) the cited new S-id (S318) was not opened this round (no Gate row with
  URL, access date and a located quote of ≤25 words in
  `corpus/lessons/round-91.md`).

Declared limits (not kills): the canary shows the copy runs but cannot show
which selftest arm executed a mutated line; a SURVIVED witness proves
non-equivalence on one registry, not that the behaviour matters on real
registries (report-only); S318's quote grounds the `GIT_NO_REPLACE_OBJECTS`
behaviour the sealing relies on, not new gate facts — fleet pinning against
`f47ad6ba` was itself sourced in round 90.

### R91-C2 — calibration: the round-90 closure's routed items 1-2 closed over committed bytes

Population (frozen): `tools/defect-bind-r91.json` (sha256 `cfb58144…61a`),
three rows: the not-admitted marker for the fleet-gate case note (item 1), the
entry's citation of its coverage-map row (item 2), and the round-90 lesson's
receipt-addendum sentence (item 2). Item 3 of the round-90 routed list (the
upstream arms patch) is report-only, never pushed, and carries no claim.

Counting command (frozen):

    bash .ufo/evidence/round-91/c2/measure-c2-v91.sh <lane> REV <empty dir> [MANIFEST_SRC]

Predicate (label `C2_R91_PASS=true`): manifest pinned AND `DEFECT_BIND: rows=3
closed=3 open=0 unexpected=0` with exit 0 AND `ledger-witness-selftest` argv
equals the SKILL entry AND the tool blob hashes to its pin AND the witness
selftest runs from the pinned blob (never the candidate tree) and exits 0.

Before: base → rows open. Target: `C2_R91_PASS=true` at the landing revision.

Kill rule: (a) a committed state reaches `C2_R91_PASS=true` while a
non-author reading finds item 1 or 2 not actually repaired; (b) any standing
no-harm sweep regresses between base and landing: `tools/selfstate-freshness.py`
(rows/match/stale/unexpected), its `--pin-audit`, `tools/registry-figure-bind.py`,
`tools/pointer-recheck.py`, and `tools/registry-check.py` over every
pre-existing row.

## Controls (pre-freeze, committed before this file)

C1 (`pre-freeze/controls/CTL*.out` + `V4-replace.out`, summary `C1-summary.txt`):
CTL14-pos → PASS; CTL2-flip → `mismatched0=false`; CTL3-figure → `figure=false`;
CTL4-ids → `ids=false`; CTL10-source → `source=false`; CTL15-coverage →
`coverage=false`; CTL5-spec → `spec=false`; CTL6-noop → `invalid0=false`;
CTL7-syntax → `invalid0=false`; CTL8-absent → `invalid0=false`; CTL9-equiv →
`witnessed=false`; CTL11-trivial → `trivial0=false`; CTL12-pin → `pin=false`.
V1-dup-row and V3-draft-column (round-90 T90R1 D3): a duplicate or draft-column
note → `ids=false` (refused, not skipped, never a PASS). V4-replace:
`replace-refs-present` or the false note's own mismatched verdict, never a
PASS. Spec-edit controls also fail `spec` (by design: the spec is pinned).

C2 (`C2-*.out`): nowork-base and nowork-instr → rows open; C2-pos → PASS;
C2-wrongcount → rows open (the marker's operative sentence asserting a false
count is not the true sentence, however its rejected quote reads);
C2-keepred → rows open (a marker without the operative sentence is no marker).

## Data seen before the freeze (disclosed)

Round 90's `33dd6e47` no-work run derived all twelve verdicts (5 KILLED, 7
SURVIVED; 12/12 predictions held). The predicate fixes no kill-rate target, so
the observed data cannot steer it. The gate pin was re-derived at freeze time:
`git show f47ad6ba:scripts/sources-census.sh | sha256sum` → `3fb72615…4e30`,
matching the live file hash.

## Wave

One v1 wave `r91-w1`, 14 seats (attack seats 6: two reviewers, two critics, one
mutation-tester, one labrat). Items: independent reproduction of every verdict
outside the counter (kill rule b), no-harm sweeps at base, survivor-killing
selftest arms drafted for the fleet (report-only, never pushed), case-note
amendment draft (S318 `source:` line + not-admitted marker + coverage
back-citation), S318 fetch verification, counter review, claim attacks on C1
and C2, a mutation test of the sealed counter, a fleet impact scan of the
survivor classes, a sealed-environment stability probe, and a scratch-safety
audit.

## Assimilation and considerthese

Assimilation: none this round (no staged `merge/tameshi/` theme serves a
fleet-gate successor case). considerthese: `2026-11-05.md` idea 4 (mutation-
survivor table, round 90's application) stays the standing reading — no new
proposal this round, and this plan names none.

## Amendments (post-wave, pre-file) — the §8 narrowing, applied at the freeze-side check

The frozen text above is not rewritten. Both claims are withdrawn to honest stop by the
artifacts this round's own wave committed; each amendment names the artifact that falsifies
the wording and the property that would remain enforceable.

### A1 — R91-C1 withdrawn (coverage) → honest stop

Falsified by `.ufo/waves/round-91/w1/T91C1.md` §1 (committed scratch state `34a92bbf`
reaches `C1_R91_PASS=true` while the note's presented verdict table is inverted on all
twelve mutants, the true values hidden in a second table under `C001`-`C012` that
`^\|\s*(C\d\d)\s*\|` cannot see) and by `.ufo/waves/round-91/w1/T91R1.md` F1/F2 (the
counter at the frozen rev `50e59d59` reads `cells[vcol + 1]` — one cell past the
header-named `verdict` — and refuses every honest note; the repair landed at `0b63b85e`
after the freeze, so every `CTL*.out` certifies bytes the plan does not name).

What survives as evidence, not as a claim: the twelve verdicts reproduce outside the
counter (`.ufo/waves/round-91/w1/T91E1.md`, `VERDICT: reproducible`), and the seal behaves
as designed when the shipped bytes run (`T91E4.md`, `VERDICT: sealed-holds`).
Enforceable successor property (round 92, QUALITY 143-144, 146): refuse **any**
verdict-shaped row whose id is outside the spec's id set, and pin the counter's own sha256
in the freeze commit and assert it at run time. No score moves; SCORECARD records
`not admitted`.

### A2 — R91-C2 withdrawn (calibration) → honest stop

Falsified by `.ufo/waves/round-91/w1/T91C2.md` (three clone states, three PASSes: the
honest one and two forged — tokens quoted as *rejected* readings, and a false kill reason)
and by `.ufo/waves/round-91/w1/T91R2.md` §2.3 (the `toolpin` conjunct hashes one file
against itself; `toolpin=ok` on every receipt) and `.ufo/waves/round-91/w1/T91SN1.md` F1-F4
(the counter runs the candidate's own checker tool; no seal; abbreviated rev pin).

What stands as upkeep, not as a claim: the two genuinely routed record repairs land
(note admission marker; note's coverage-row citation) and the invented third manifest row
is dropped (`.ufo/waves/round-91/w1/T91R2.md` §3.3 — no routed defect behind it). The
landed state therefore prints `rows=fail` on that dropped row, which is the honest state.
Enforceable successor property (round 92, QUALITY 145, 148): a machine-checkable admission
block whose values are checked, checker run from a pinned blob under the seal.

### Consequence for the round

Both claims `unprovable` / not admitted; no axis harmed (scores unchanged 10/8/9). The
round's deliverable is this narrowing plus QUALITY 143-148, each with a committed state
shown able to fail.
