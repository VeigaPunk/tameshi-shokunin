# Round 34 — lesson (tameshi)

Base `66e1fb444615b3afe380e7df0244ef7fae1dd985` (round-32 spot-check head; round-33 carried the
tool/counter freezes). L1 TameshiR34, attempt 1. Round order: amendment 6 (`6aaad5b3`, counter
witness gate set-aware, PRE-AUTHORING per the routed RevengerWitness rule) → controls receipt
minted at the amended rev `6aaad5b3` (`9dd3174c`, receipt-attestation rule) → sealed held-out set
authored after the counter freeze (`c17e593b`, 8 must-kill + 6 must-accept, per-copy authoring
receipts) → deciding run at the measurement revision `c17e593b`:
`C1_R33: … v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0
heldout_after_freeze=1 … C1_R33_PASS=true`, exit 0 — C1 MEASURED TRUE. One v2 wave built and
validated; taskCall returned to the orchestrator (zero dispatches from this session); relays
folded on return.

## Gate

Sources opened this round:

- **S101**: https://mutation-testing.org/, accessed 2026-10-23 UTC, 4,341 bytes, sha256
  `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420` (committed snapshot
  `.ufo/evidence/round-34/src/s101-mutation-testing.html`). Quote (Overview feature list,
  15 words): "exporting source-code mutants; suppressing equivalent mutants; computing the
  mutant-detection rate and the set of live mutants".

Rejections:

- https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html — rejected as a pin/row
  target: unreachable from this host (two timeouts, receipt `.ufo/evidence/round-34/src/
  s101-fetch.exit`), AND its whole scope (bash exit-status range, special statuses 126/127/128+N,
  `case` first-match) is already held at tier A by row S097 (Bash 5.3 `bashref.texi`, whose row
  even records this same timeout) — a TLDP ABS duplicate-topic row was drafted, fetched
  (9,728 bytes, sha256 `60cebcc8…d291`, snapshot `s101b-abs-exit-status.html`) and rejected on
  the duplicate-scope reason, kept as evidence only.
- TLDP ABS exit-status page — see above; duplicate of S097's scope, not rowed.

Row changes, old → new (`corpus/SOURCES.md`, rows 97 → 98): S101 added (mined; used-by
`corpus/knowledge/witness-equivalence-rule.md`). No other cell changed. The knowledge entry
cites S097 (opened in an earlier round; the exit-status/`case` semantics the tuple witness
compares) and S101 (opened this round; equivalent mutants as a first-class framework concern —
the reason accept+vector demands equivalence, not difference). The round's sourced-claim
conjunct rests on S101.

## Mistakes

1. **class:** an authoring prediction validated by assertion instead of execution. **evidence:**
   the `ho-kill-vector-setup-threshold` copy was first authored with witness `[2,2,0,...]`, but
   with `nsetup -gt 1` two setups still trip the guard — pristine and mutated tie (both SETUP),
   the witness returned `(False, 'vector')`, caught by the per-copy authoring receipt before any
   commit. **captured-by:** the pre-data authoring harness (witness gate + real tool per copy);
   the fix (witness `[2,0,...]`, single setup escapes the `-gt 1` guard) was re-verified by
   execution: pristine SETUP(cannot-verify=1) vs mutated PASS(passed=8). **fix:** shown able to
   fail by the caught receipt itself (`.ufo/evidence/round-34/dev/authoring-receipts.json` first
   generation, preserved in the scratch transcript).

## Holds (routed to round 35)

- v3 residue classes NOT adopted pre-data (tool pin frozen at `7b11ba25…8d10`; freeze-before-data
  discipline): Guard-2 divisibility, TallyArms-02 coexistence, quoted case subject,
  helper-function refactors, per-index record parsing, preamble seeding, nonzero-leg stress,
  all-pairs nlegs recompute, whole-stdout comparison already landed as the r33 DevPrintf fix.
- Cold-read re-crediting of the drift monitor sections (SCORECARD/LOG/lessons/SOURCES appends;
  LedgerAudit sized ~19 SOURCES-citing sections + 3 all-four in r33) — carried into the r34 wave;
  if not consumed there, first item of round 35.
- Calibration monitor: the r33 baseline (64/64 restraint 8) was not re-run this round (the
  measurement owned the budget); next round re-baselines.

## Wave

One v2 wave under policy v2 (band 64-128, ≥25% attack): build+attack mixed, post-decision
falsification of the landed artifacts (sealed set, controls receipt, amended counter, tool pin,
panel) plus the routed cold reads and frontier rechecks. Zero dispatches from the L1 session —
the validated taskCall JSON is returned to the orchestrator; seat relays return tagged
`[seat <name>]` and are folded here on arrival (post-data findings cannot amend the frozen rule;
they land as Holds or honest report entries).

## Wave fold (orchestrator-dispatched round-34-w1, 64 seats; author TameshiR34)

Seat outcomes folded here; every artifact attacked stood. C1's deciding receipt stands:
ho_kill=8/8 + ho_accept=6/6 + ho_invalid=0 re-derived by 6+ independent seats; the counting
command re-ran byte-identical at the recorded seed and PASSES at fresh seeds (not seed-fragile);
pins byte-identical at every commit; freeze-before-data order verified. Findings are capability
bounds and hygiene — every attack direction that could matter admits only fail-closed
constructions against the LANDED set (none present in it).

**Corrections to this lesson's earlier bytes (append-only disclosure):**
- The Holds line "whole-stdout comparison already landed as the r33 DevPrintf fix" is WRONG:
  the whole-stdout comparison was ROUTED in r33, never landed — the pinned tool still compares
  first stdout line + rc only (tool.py:44-45, 268-287, 290-302), proven live by four wave seats
  (Mutacceptvectorinertline F5, ResiduePreambleSeeding F5/ctl3, Mutkillvectorarmswap F3-context,
  Mutacceptheadcomment class C). The class stays OPEN; it is the first item in the r35 Holds
  below, with the (0,0)/(1,1) config sweep hole as its highest-priority instance.
- The Gate's "two timeouts" receipt pointer names `.ufo/evidence/round-34/src/s101-fetch.exit`,
  whose committed bytes are `MUT_EXIT=0` (the successful mutation-testing.org fetch overwrote
  the gnu.org attempt log). The gnu.org timeouts are true (session transcript) but are NOT
  receipted in committed bytes; the duplicate-scope rejection ground is independently verified
  via S097. Fix in the r35 append.
- S101 Gate quote word count: labeled 15, wc -w counts 16 — same cosmetic class as the r33
  routed defect 4; contract satisfied.
- ReviewPinChain F1: `contract.json:frozen_artifacts.tool_sha256` still cites 9dbbce62…33a4
  (the f6d8a891 blob); the counter's own TOOL_SHA256 pin (7b11ba25…8d10) governs measurement,
  but a literal contract verifier would score the tree FAIL. r35 housekeeping: amend the
  contract citation or record the rule that contract citations must follow tool re-pins.
- AllFourLog F1 (fixed this fold): the wave validator stdout/exit are now committed as
  `.ufo/waves/round-34/validate.{stdout,stderr,exit}` (exit 0).
- ReviewDevReceipts F2: `dev/tool-selftest.stdout` is a 3-line tail of a 23-line run (captured
  with `tail -3`); the 22/22 verdict is real (re-run by seats). Full captures going forward.
- ReviewDevReceipts F1 (provenance): the authoring receipts landed IN the amendment-6 commit
  (6aaad5b3), so commit order alone cannot demonstrate "amendment before authoring"; the
  real-time order is attested by the probe/panel receipts' content and this lesson's
  pre-authoring disclosure. r35: land dev receipts separately after the amendment.
- ColdReadSourcesRows F1: S100's used-by names corpus/knowledge/executable-self-assessment.md,
  which never cites S100; corrected this fold (old→new logged below) to the lesson that cites it.

**SOURCES.md row change this fold (old → new):** S100 used-by
`corpus/lessons/round-33.md, corpus/knowledge/executable-self-assessment.md` →
`corpus/lessons/round-33.md`. Logged per contract; no other cell changed.

**Dead/incomplete seats:** CriticVoidClaim DEAD on a provider policy refusal (Codex flag on the
seat text; the void-claim critique was covered by ReviewCounterSemantics + 7 converging
mutation seats + RevengerIndependentSet). PanelSeed1's relay arrived truncated but its report
is complete (534 lines, V1-V4 PASS). ReviewDevReceipts relayed content-complete; its .md may
land after this fold. CalibMonitor and PanelSeed4 were still running at fold time — named.

## Holds (round 35) — convergent wave findings, all measurement-only this wave (tool frozen)

Witness-gate bounds (8 seats converged; deciding run stands, all directions fail-closed for
the landed set): the amendment-6 rule (verified = the routed RevengerWitness patch verbatim)
admits future bogus copies — (a) accept+vector = one author-chosen vector: multi-vector +
operand-stress equivalence required; (b) accept+head = behavior-blind and leg-surface-blind:
the landed kill bytes with set flipped kill→accept gate-validate (RevengerSet R1b) — require
per-seal tool-agreement evidence or full-vector+stress equivalence; (c) kill/accept+head scan
the whole-file prefix while the tool audits run_regression's span — span-align; (d) the tail
region (selftest/harness anchors) is inspected by neither head_of nor tally_block_of — include
or bound it. ReviewCounterSemantics F1-F4 is the systematic statement; fix list (a)-(d).
Witness-shim fidelity (6 seats): block_run pins root=r auto=0 KEEP=1 HOME=/w while the tool
audits roots tally-audit and /tmp/tally-audit-work with overridden env — root/HOME/TMPDIR/PWD/
auto/KEEP-keyed constructions evade the tool while the gate validates them (phantom direction,
fail-closed) and mirrors validate real defects as ACCEPTS; TOP PRIORITY = the accept-side
config hole that is NOT fail-closed: the audit sweeps only (auto,KEEP) = (0,1) and (1,0);
(0,0) and (1,1) are real but UNSWEPT (Mutkillvectorarmswap F3: an accept-set swap gated on
(auto=0 && KEEP=0) is witness-valid, tool-ACCEPTED, runner-selftest-passing, LETHAL under
`--regression --workdir DIR`). r35: extend the sweep to all four configs AND pin the witness
shim to the tool's triples + explicit env.
Tool precision (false-kills — 3+ seats; the single most-confirmed target): the twice-only head
rule counts NAME SUBSTRINGS not assignments — an inert comment naming a leg is KILLED
(tool.py:326-334); strip comments before counting. Also: regression_body counts braces
char-wise without skipping comments (a comment '}' closes run_regression early → behaviorally
pristine copy KILLED); comment text seizes the case/for locators ('esac'/'do' in comments →
SETUP refusals).
Tool recall (false-accepts): whole-stdout comparison (DevPrintf class — OPEN, see correction
above); preamble seeding reproduced (head-local `auto` rename → real regression in BOTH runner
configs, workdir leak, tool PASSes — ResiduePreambleSeeding); trailing-comment line swallow
('# inert marker' appended without newline merges with the next line and DESTROYS a head call
— tool ACCEPTs, the first false-accept specimen — Mutacceptheadcomment class C); name-assembled
assignment masks (printf -v "st_$n" 0 — a genuine mask the tool passes, gate validates as
head-leg-assignment — Mutkillheadnonbare); helper-function/scope-boundary faults (top-level
policy helper preserving nlegs — LIVE false pass the gate certifies must-accept —
ResidueHelperRefactor); per-index record parsing (SETUP-CR escape REPRODUCED at the pin: a
parser-crashing kill copy scores a MISS, measurement-conservative — ResiduePerIndexRecord).
Quoted/braced case subjects: the tool REFUSES (SETUP) instead of killing — abstention class,
deciding run silent on it (ResidueQuotedCaseSubject); TallyArms-02 coexistence CLOSED at the
pin (r33 false-pass class fixed — ResidueTallyArmsCoexist); Guard-2 divisibility confirmed
REAL (5/15 guard-predicate survivors, the r32 sealed artifact itself killed —
ResidueGuard2Divisibility); nlegs recomputes 6/14 survivors, all witnesses outside the panel
(ResidueNlegsAllPairs); co-occurrence coverage bounds quantified: 243 of 255 non-zero statuses
never co-occur with a second non-zero leg; 0 vectors pair a non-CO status with another non-zero
leg (ResidueNonzeroLegStress).
Panel design (4 seats): public_panel's 18 must-kill copies carry 13-18 DISTINCT bodies
seed-dependent (deciding seed landed at 14); all nine generated kill stems are clone-capable.
The claim's discriminating power lives in the sealed set (8/8 + 6/6 fully distinct — CLEAN).
r35: assert generated-mutant distinctness (or dedupe), report distinct counts beside copy
counts, note the deciding seed's 14/18 in the corpus.
Dev battery (detector coverage): the 8-probe battery lacks len!=9 (MutCounterrelaxlen9
SURVIVED — behavior-bearing) and zero-diff probes (MutCounterdropequivalencebytes), plus
polarity-closing probes (ConnectorOverlap verified a 3-probe fix kills all four forced-verdict
mutants). r35 pre-data: extend the battery (9-11 probes) and pin the TUPLE-LEVEL battery as the
corpus standard (a boolean-only battery would miss the drop-block-identical mutant's
diagnostic loss — MutCounterdropblockidentical). Counter hardening candidates:
block_run TimeoutExpired is outside main's except tuple (crash risk, unreproduced —
ReviewCounterSemantics residual); the harness check is injection-based (extraction correctness
ignored while ≥1 EXTRACT_RE line exists).
Hygiene: QUALITY.md criterion 72 draft (authored expectations validated by executing
pristine+mutated before commit — QualityGate); SCORECARD r31v2 standing row still says 96 rows
(observed 98 — AllFourScorecard F1); reports/round-1-calibration.md cites PROTOCOL.md paths
absent from this repo (second-hop — ReviewSHONEN); runner :96-99 cites legs 8/9 by spec path
(LedgerDepth note); the six counter-mutation seats each killed/survived-classified their mutant
with the landed counter never touched.
