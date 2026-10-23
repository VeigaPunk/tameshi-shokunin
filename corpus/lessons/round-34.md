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
