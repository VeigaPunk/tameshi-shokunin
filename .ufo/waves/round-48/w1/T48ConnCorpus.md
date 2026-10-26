# T48ConnCorpus — own-corpus grounding of R=3 (C1)

Seat: T48ConnCorpus (connector, Godspeed). Item: connect the round's C1 design (R=3
observation rounds, `stable` / `nondeterministic` value class) to the lane's own corpus on
flakiness; deliver a short grounding note the L1 can put in the lesson.

## Evidence (opened and read)

| Entry | Source rows | Held claims used here |
|---|---|---|
| `corpus/knowledge/repeated-control-precondition.md` | S026 (also S004) | S026's 1.5% run rate, 16% of tests, 84% pass→fail transitions, fail-3-in-a-row verdict, cost; the floor-of-3-is-policy line; the measured in-lane 10%-failure control triples |
| `corpus/knowledge/flaky-aware-verdict-evidence.md` | S261, S262 | S262's rerun-based flaky label, ≤5-reruns ≥82% guidance, 4000-run measurement, ISO/TSO detection gaps, burst lengths, TSR failure-rate mean/range, worked example rates |
| `corpus/knowledge/r8-flakiness-not-static.md` | S263 | 42%/58% split (code+CI log vs execution evidence); protocol-shortcut warning |
| `corpus/knowledge/r8-flaky-cost-baseline.md` | S264 | rerun 0.02 cents vs $5.67 manual investigation; 2.5% developer-time floor; shift toward automatic rerunning |
| `.ufo/evidence/round-48/contract.json` | — | C1 statement (line 26), kill rule (line 29), amendment 3 row grammar (line 11) |
| `.ufo/waves/round-48/w1/T48ExecC1Counter.measure.py` | — | row parsing (`parse_row`, `TAIL_RE`, `MEMBER_RE`, lines 194-230) confirms the evidence cell is fully consumed by the frozen grammar |
| `.ufo/evidence/round-47/coverage/sources/lam-2020-reruns.txt` | S262 snapshot | line numbers below verified directly in the committed text |

## The arithmetic (all independent of any claim)

Model: per statement, each of R=3 rounds yields one P0 `(line, exit)` tuple; V = the set of
distinct P0 tuples over the 3 rounds; |V|=1 → `stable`, 2-3 → `nondeterministic` (contract
line 26, amendment 3). A statement that deviates from its modal tuple with probability p per
P0 run is caught as nondeterministic iff at least one of the 3 P0 runs deviates:

    P(caught) = 1 - (1-p)^3        P(missed, declared stable) = (1-p)^3

| p (per P0 run) | Source of p | P(caught) | P(declared stable despite flakiness) |
|---|---|---|---|
| 0.001 | S262 lower bound: TSR failures <0.1% (`lam-2020-reruns.txt:472`) | 0.30% | 99.70% |
| 0.005 | S262: median failure rate of detected flaky tests below 0.5% (`:292-296`) | 1.49% | 98.51% |
| 0.015 | S026: about 1.5% of all test runs report a flaky result (`S026.html:1130`, via `repeated-control-precondition.md:19`) | 4.43% | 95.57% |
| 0.054 | S262: mean TSR failure rate 5.4% (`lam-2020-reruns.txt:475`) | 15.34% | 84.66% |
| 0.10 | in-lane measured: a control failing 10% of the time (`repeated-control-precondition.md:29`; `waves/round-12/w1/ControlThreats.md:45-56`) | 27.10% (measured 25.67%, 223/300 clean triples) | 72.90% |
| 0.109 | S262 worked example, TSO failure rate 10.9% (`lam-2020-reruns.txt:163`) | 29.27% | 70.73% |
| 0.391 | S262 worked example, ISO failure rate 39.1% (`:162`) | 77.41% | 22.59% |
| 0.50 | S262 upper bound: TSR failures up to 50% (`:473`) | 87.50% | 12.50% |

Complements worth stating in the lesson:

- Expected P0 runs before the first deviation at p=0.054 is 1/p ≈ 18.5, i.e. ≈ 6 rounds; 80%
  catch requires ≈ 29 rounds at p=0.054, ≈ 107 at p=0.015, ≈ 1609 at p=0.001 (ln(0.2)/ln(1-p)).
- Max distinct P0 tuples over 3 rounds = 3, so `oversize` cannot arise from P0 observations alone;
  it can only come from attestation receipts adding a 4th member.
- S262's own detection detector: "after one failure, 87.8% of tests can be found to pass in 5
  reruns" (`lam-2020-reruns.txt:357-360`), on 4000-run measurements; ISO missed 57 of 107 flaky
  tests (`:430-432`), 53% of TSO-detected tests are not detected in ISO (`:446-447`), and TSO
  reaches 82% of tests at burst length 2 while ISO needs 5 (`:433-436`). Note the lane's rule is
  not a consecutive-burst rule: any single deviation flips V to two members, so per-observation it
  is more sensitive than S262's detectors; the limitation is the sample size (3), not the rule.

## Does R=3 + declared nondeterministic class follow from the corpus?

Yes, in shape; no, in guarantee — the note must say both.

- **Yes — the shape.** S262 defines flaky by reruns: "we label tests as flaky if our runs have
  both pass and fail" (`lam-2020-reruns.txt:29`). A single round cannot observe both outcomes, so
  R>1 is the minimal honest shape of a flaky-aware standing row. This is precisely the round-47
  routed defect: the `six-leg regression ledger` row restated a one-shot flaky observation
  (`FAIL (cases=9 passed=7`, exit 1) as a standing value; the round-47 deciding run observed
  `PASS (cases=9 passed=9` and the claim missed (SCORECARD.md:2318; contract line 24). S263's
  thesis — flakiness is not a static property of test code — and its 58% share of cases that
  "required further execution evidence" (r8-flakiness-not-static.md:16,24) support execution
  evidence over static restatement. S264 prices the rerun branch cheap (0.02 cents) against the
  $5.67 manual investigation (`r8-flaky-cost-baseline.md:24`), so paying for R=3 rounds is
  negligible next to the cost of restating a flaky value.
- **No — the guarantee.** At the corpus's own rates, R=3 catches a *typical* flaky statement with
  only ≈15% probability (p=0.054) and a median one (p<0.005) with ≈1.5%. A `stable` row remains a
  finite-sample statement, not a determinism proof — the same boundary the gate already draws:
  `controls_match` "is not a determinism proof and it cures no flakiness" and "the floor of 3 is
  lane policy, not a sourced threshold" (`repeated-control-precondition.md:29`; S026's fail-3-in-
  a-row is "hardly a perfect solution", `S026.html:1136`). S262's own ≤5-reruns ≥82% figure is a
  *classification* result on their Java dataset, not a detection guarantee and not transferable
  here (`flaky-aware-verdict-evidence.md:68`); do not cite it as if it were. The C1 kill rule
  already treats a flaky deciding observation outside V as a mismatch, not a rerun (contract line
  29), which matches the corpus: "retries do not repair" (`repeated-control-precondition.md:27`).

## Should the C1 standing rows cite an entry?

No. The evidence cell is a frozen grammar (contract amendment 3, line 11): `CMD → LINE1, exit N1
[ or LINE2, exit N2 [ or LINE3, exit N3]], tool sha256 `12 hex`, deps `LIST`, runs 3 CLASS`. The
round-48 counter parses that cell with `TAIL_RE`/`MEMBER_RE` and treats a missing/malformed clause
as `unparsed` (a kill) (`T48ExecC1Counter.measure.py:194-230`); a citation appended inside the
cell would be uncharted text whose backtick/`, exit` tokens can be misread as extra members
(`oversize`). The observation *receipts* under `.ufo/evidence/round-48/calibration/observations/`
(not parsed by the row grammar) and the lesson are the right homes for the citation. Precedent:
knowledge entries carry source citations; SCORECARD rows cite evidence paths, not corpus entries.

## Proposed move

Keep the C1 design as frozen. Add to `corpus/lessons/round-48.md` a short "R=3 grounding" note
(§ Grounding note below) stating: R=3 is policy, not a sourced threshold; the detection arithmetic
above; and the residual false-negative risk of a `stable` row. No changes to SCORECARD.md,
SOURCES.md, knowledge entries, or the counter. (Read-only seat: nothing else is edited; this
report is the only deliverable.)

Affected axes: calibration (C1) only. Freshness (C2), depth, no-harm monitors, cold-read sections,
census: untouched.

## Risks

- R=3 materially under-detects rare flakes (≈1.5% catch at the median literature rate; ≈15% at the
  mean). The nondeterministic class is therefore a strong positive finding when it fires, while
  `stable` is weak evidence. Acceptable per the claim's own finite-sample scope; the lesson must
  say so, or a future round repeats the round-47 defect one level up.
- Do not let the corpus's "3" (S026 fail-3-in-a-row; F3 N≥3) be read as sourced endorsement of
  R=3: S026 calls its own rule imperfect and the lane's own entry says no source prescribes a
  repeat count.
- A flake landing only on a variant profile (P2-P5) cannot flip V; it surfaces as an `unstable`
  dependence, which the contract permits to be declared or omitted. That is a designed blind spot
  worth one sentence in the lesson.

## Verification (for the main agent)

- Recompute the table: P = 1-(1-p)^3 for p in {0.001, 0.005, 0.015, 0.054, 0.10, 0.109, 0.391,
  0.50}; expected 0.30/1.49/4.43/15.34/27.10/29.27/77.41/87.50%.
- Spot-check the cited lines in the committed snapshot `lam-2020-reruns.txt` (29, 113-114, 162-163,
  292-296, 357-360, 430-436, 446-447, 472-475) and `repeated-control-precondition.md:19-29`.
- Confirm `T48ExecC1Counter.measure.py` parses rows via `TAIL_RE`/`MEMBER_RE` and would not read a
  citation cell (so the "no citation in rows" recommendation holds).

---

## Grounding note (paste-ready for `corpus/lessons/round-48.md`)

**R=3 is lane policy, not a sourced threshold; here is its detection arithmetic.** The C1 design
runs R=3 observation rounds and declares a statement `nondeterministic` if its P0 (line, exit)
tuples differ across rounds. A statement that deviates with probability p per P0 run is caught
with probability 1-(1-p)^3. At the corpus's rates: p=0.054 (S262 mean TSR failure rate,
`lam-2020-reruns.txt:475`) → 15.3% caught; p<0.005 (S262 median, `:292-296`) → ≈1.5%; p=0.001
(S262 lower bound, `:472`) → 0.3%; p=0.391/0.109 (S262 worked example, `:162-163`) → 77.4%/29.3%;
p=0.015 (S026 run rate, `S026.html:1130`) → 4.4%; in-lane, a 10%-failure control produced three
clean runs in 223/300 triples (≈26% caught; `repeated-control-precondition.md:29`). Expected runs
to first deviation at the mean rate is ≈18.5 (≈6 rounds); 80% catch needs ≈29 rounds. So: a
`nondeterministic` row is a strong positive finding, but a `stable` row is a finite-sample
statement — the same boundary as `controls_match` ("not a determinism proof"; the 3 floor is
policy, S026's fail-3-in-a-row is "hardly a perfect solution", and S262's ≤5-reruns ≥82% does
not transfer). S263: 58% of its flaky cases required execution evidence (code+CI log sufficed for
42%) — supporting execution rounds over static restatement. S264: a rerun costs 0.02 cents vs
$5.67 for a manual investigation, so R=3 is the cheap branch; the expensive failure is restating a
flaky value as standing (round-47's six-leg row). Rare flakes landing only on variant profiles show
up as `unstable` dependences, which the contract permits to declare or omit; a flaky deciding
observation outside V is a mismatch, never a rerun.
