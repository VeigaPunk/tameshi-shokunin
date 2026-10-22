# Round 26 — ninth recorded case and round-25 record repair

author: TameshiR26 (L1, attempt 1)
Date: 2026-10-22. Base `d4140796f4e48e8ec81b793facba73fbd03b4443`.

## Claims

Both frozen in `.ufo/evidence/round-26/contract.json` at `622d31d` before any
mutant ran and before any edit the C2 counter reads.

- **C1 depth (learning claim).** Ninth recorded mutation-ledger leg
  `js-cite-check`: kumitate `scripts/cite-check.mjs` at `1205c66` (blob
  sha256 `40573448…c10c9f`). Counter
  `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE_AT_REV`: before
  `depth_score=8`, exit 1; target `recorded_cases=9 wired_legs=9
  depth_score=9`, exit 0.
- **C2 calibration (record repair).** Round-25 spot-check routed items 1–3.
  Counter `python3 .ufo/evidence/round-26/c2-measure.py --repo CLONE_AT_REV`:
  before `mismatches=3/3`, exit 1; target `0/3`, exit 0.

## Gate

Admit candidates: `corpus/knowledge/mutation-case-kumitate-cite-check.md`;
the ninth leg in `tools/mutate-and-run.sh` (spec, pin, table, replay call,
selftest tuple) and its interop mapping in `tools/mte-interop.py`; the two
counters; QUALITY 51 and 52.

Reject:
- reading 5/10 as five suite holes: `S_EMPTY_GUARD` is an equivalent mutant
  (seat CriticEquivalence: `filesScanned++` always runs before `resolved++`,
  316/316 differential runs identical); four survivors are holes, each with a
  hermetic off-suite witness (seats ProbeSOOREDGE, ProbeSSTRICT, ProbeSUSAGE,
  ProbeSPININCLUDES);
- reading "10/10 predictions held" as ten risky predictions: the equivalent
  mutant's SURVIVED prediction could not fail, and one named witness was wrong
  (`K_FENCE_TILDE`, seat ReviewPredictions);
- reading the ten edits as Stryker mutators: seat OpenStrykerMutators maps 7
  of 10 to a Stryker mutator class and 0 of 10 to a documented operator;
- reading `depth_score=9` as proof that the recorded table is right: the
  counter checks wiring only (seat MutateC1Counter lists eight weakenings it
  cannot see; seat CriticC1 shows a leg copied from leg 8 passes the counter
  and the regression). The regression replay, `match=10/10`, ties the table to
  the pinned bytes;
- reading C2's 0/3 as closure of the class: seat CriticC2 counts 16 round
  counters with verdict exits and no registry row; only item 2 is a SCORECARD
  self-assessment row in the strict sense.

S088 opened 2026-10-22 by the L1 (`git -C kumitate-shokunin show
1205c66:scripts/cite-check.mjs`, sha256 equal to the pin; re-opened by seats
OpenCiteCheckPin and five probe seats). Located quote, `:75-76`: "Never reads
--src or --self; MUST PASS in any repo state. This is the whole of
--selftest."

S089 opened 2026-10-22 by the L1 with an ordinary fetch
(https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/,
html sha256 `bc572676…e04d`; also opened by seat OpenEquivalentSource).
Located quote, the paragraph after the `10 ** 0` example: "There is no
definitive way for Stryker to find and ignore them. There is currently also no
way yet to mark them to be ignored."

Both new rows start mined, tier A, recheck 180d, used by the new entry. S052
(Stryker supported mutators) was re-opened by seat OpenStrykerMutators and
left unchanged; the Madeyski et al. 2014 preprint (tier B) was screened and not
added. No existing row's status, recheck or used-by changes.

Bounded lookup: identified 4, screened 4, included 2, excluded 2.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| a knowledge entry vouching for an earlier tool run | `knowledge/mte-report-interop.md:2` at base named the `09dc114` run (tool `8c24255c…`, selftest 16/16); the measured tool was `8269b82f…` with 17/17 (`round-25-verifier-spotcheck.md:197-199`) | none at the time (QUALITY 10, 24 and 26 do not bind a verified-at line to tool bytes) | QUALITY 51; the line now names tool sha256 `193ea6e3…` at `a08e85c` and two committed receipts. Shown able to fail: C2 item R25-SPOT-3 reads MISMATCH at base (`.ufo/evidence/round-26/c2-before.stdout`). |
| a registry row landed in a shape the registry gate refuses | `tools/registry.json` rows 54–55 at `a08e85c` had a prose `source`; `registry-check.py --rev a08e85c` → `could-not-evaluate (registry invalid …)`, exit 2, no row ran (seat RegistryCheck) | `tools/registry-check.py` `SOURCE_RE` (`:108`) — the gate caught it; the L1 did not run it before landing | Both sources rewritten to `<file>@<rev>:<line>`; QUALITY 52 second sentence. Shown able to fail: the `a08e85c` receipt in `.ufo/waves/round-26/w1/RegistryCheck.md`. |

## Routed items 4–5 (round-25 spot-check)

- Item 4, open and explained: the 17 command-binding weakenings still survive
  at `a08e85c` (seat MtGuardGapsRecheck: 0/17 killed; A13 and D06 are one
  byte-identical edit, so 16 distinct); the 14 re-attack findings, round-24
  spot-check items 2–4 and the unpinned emitted reports are unchanged (seat
  ScoutRoutedOpen). This round worked a different frontier area (depth) and
  did not claim them.
- Item 5, closed in the wave contexts: both round-26 wave contexts forbid any
  `jj` command anywhere (seat ScoutJjBounds; QUALITY 52).

## Wave findings routed forward (not claimed this round)

- Kumitate (owner): four cite-check hermetic-suite holes (n+1 line edge,
  `--strict` threshold, usage exit, interior-slice content pin), and a
  non-equivalent neighbour of the equivalent mutant (drop only the `resolved`
  guard: the `VERDICT:` line flips while the exit stays 2).
- `tools/mte-interop.py`: the leg-set guard compares sets, but a count-only
  weakening survives its 17-case selftest (seat MutateInteropLegSet); emitted
  reports carry no revision pin (seat ReviewMteLeg9).
- `c1-measure.py` cannot see a ledger kill-rate lie, a target path change or
  a stale `@old` (seat MutateC1Counter); `c2-measure.py` can be gamed: seat
  MutateC2Counter builds a combined state that reads `mismatches=0/3` with
  all three defects still present (prose tokens, a stale or unrelated
  receipt, a registry row that only names the path). The C2 after-value is
  therefore read together with the seat reviews of the actual text (wave 2
  ReviewCorrections, RerunC2), not alone.
- `tools/mutate-and-run.sh --regression` (all legs, older than this round):
  dropping a leg's status from the summary loop, or a wrong `nlegs`, still
  prints `REGRESSION: PASS`, because the loop never checks
  `npass + nfail + nsetup == nlegs`; the per-leg spec-file `-s` list is not
  pinned by the selftest (seat MutateRunnerSelftest). Not fixed this round:
  a runner edit would re-drift every runner-keyed cold read.
- Drift sentinel (seat CriticC2): calibration has been claimed five rounds
  running from routed items; round 27 should work a different frontier area.

## After measurement

Wave 2 (39 cold reads plus 16 falsifiers, spec `.ufo/waves/round-26/spec-w2.json`)
was validated but not dispatched: its 55-seat gate request was still waiting at
11:47Z, Main's wave-size steer and the 2 h freeze followed, so the request was
cancelled. The round is one wave of 39 seats.

At `40a12bf` (content landing) and `d2206cd` (SCORECARD results), fresh clones:

- C1: `C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9`, exit 0; command D
  `recorded_cases=9 depth_score=9` (`.ufo/evidence/round-26/after/`).
- C2: `C2_RECORD: mismatches=0/3`, exit 0.
- Regression 9/9 PASS and interop 9/9 PASS at `a08e85c` (L1) and again in seat
  clones (ReplicateSweep, InteropCheck, MutateInteropLegSet).
- Registry at `40a12bf`: `held=48/49 superseded=7`; the one row that differed
  was the new `mte-interop-check`, refused as non-hermetic because its argv
  named the live fleet root (`after/registry-40a12bf.json`). Fixed in
  `2b064cf` (the tool's default fleet root is the clone's own mirror);
  `--only mte-interop-check` then reads `held=1/1`. A full registry run at the
  final revision was not repeated.
- Census end: exit 0, 87 rows, seven pre-existing W04 warnings
  (`after/census-end.stdout`).

**Harmed and not restored (retained, reported).** The strict cold-read monitor
reads 62/62 sections, restraint 8 at base; 32/64, restraint 6 at `a08e85c`;
25/64, restraint 6 at `d2206cd` and `2b064cf`
(`after/monitor-harmed-*.json`). Cause: the runner, registry and corpus edits
drifted the traced inputs of 37 existing sections, and two new headings have
no entry. The planned repair was independent seat cold reads (wave 2); the
round-23 author re-anchor tool refuses sections with no prior entry, and no
other restoration ran. Calibration's numeric score at head therefore reads 6
on this monitor, a harm, not a no-harm. The next round's first move is the
wave-2 spec re-generated at its base.

## Errata

- The frozen contract calls cite-check "a never-measured kumitate gate". It
  was probed once before: the kill-rate ledger records a four-defect probe,
  1/4, and a queue row "probe only" (seat ConnectorOverlap). This round is the
  first full recorded sweep; the contract text is wrong on that word.
- Seats DraftQuality and DraftProvinceReadme were cancelled by the L1 after the
  L1 had landed its own text for their items, to release the wave-1 gate
  reservation; they are cancelled, not dead.
