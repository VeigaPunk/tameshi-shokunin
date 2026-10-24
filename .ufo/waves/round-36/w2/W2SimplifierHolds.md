# W2SimplifierHolds — round-35 Holds × round-36 SCORECARD planned block (read-only mapping)

Seat: `W2SimplifierHolds` (wave-2, falsify, leaf; no subagents; no production edits — this file is
the only lane path created). Attacked: the mapping between every class in the round-35 lesson
`## Holds` + routed-defect set and what round 36 actually addressed, as claimed by the round-36
SCORECARD planned block. No runtime re-measurement was in scope; verification below is receipt
re-read + digest check only.

## Sources read (all read-only, absolute paths under /home/vgpnk/Projects/shokunin/tameshi-shokunin)

- `SCORECARD.md` — round-35 section incl. `**Planned (round 36):**` block and "Disclosed predicate
  defects"; round-36 section incl. its claims table and `**Planned (round 37):**` block.
- `corpus/lessons/round-35.md` — `## Holds (routed to round 36)` (8 classes) + `## Residual
  verification` routed items (cold-read lapse; counter PASS weaker; comment-blinding; stale control
  narration).
- `corpus/lessons/round-36.md` — `## Holds` (code_view deferral reason; refresh-scope honesty).
- `corpus/lessons/round-34.md` `## Holds (routed to round 35)` — upstream naming of the recall classes.
- `LOG.md` round-36 entry (dead-pointer correction; C1/C2 records; waves note).
- `.ufo/evidence/round-36/contract.json` (frozen; `routed_repairs` block).

## Commands run (exact)

- `sha256sum tools/tally-audit-v3.py tools/mutate-and-run.sh .ufo/evidence/round-36/c1/c1-measure-v2.py .ufo/evidence/round-35/c1/c1-measure.py`
  → `6188db16…d354` (matches pin), `a7d3f2dd…2eb9` (matches pin), `9eb8944c…fa53` (matches contract),
  `d360a159…bbe3` (see observation O1).
- Receipt re-reads: `.ufo/evidence/round-36/after/monitor-at-796e08b.stdout` →
  `calibration_restraint_score: 6`; `control/monitor-at-e423c41b.stdout` → `6` (do-nothing control);
  `after/monitor-at-b455001e.stdout` → `8`; `control/v1-at-emptypanel.stdout` →
  `pub_kill=0/0 pub_accept=0/0 … C1_R35_PASS=true` at `rev=91373d5…`; `control/v2-at-emptypanel.stdout`
  → same panel, `C1_R36V2_PASS=false`; `after/c1v2-at-b455001e.stdout` →
  `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 … C1_R36V2_PASS=true` at
  `rev=b455001e2589b3f4f471d94a3de7e5e549b9f54c`; `after/depthD-at-b455001e.stdout` →
  `recorded_cases=9 depth_score=9`, runner `a7d3f2dd…2eb9`.
- Ledger check: grep of `.ufo/evidence/round-21/coldread/ledger.json` for the round-36 refresh
  entries → exactly four new entries (traces `round-36/coldread/traces/L1/source-1..4.json`, seats
  `L1 TameshiR36 author source re-anchor`, reports `round-36/coldread/refresh-receipts.json`).

## Mapping — round-35 Holds / routed defects → round-36 disposition

Round-35 lesson `## Holds (routed to round 36)` classes, with the round-36 SCORECARD planned block
items they map to:

| # | Round-35 item (source) | Round-36 disposition | Where recorded |
|---|---|---|---|
| H1 | Head-side masks outside the block oracle: ANSI-C `$'…'`, nested `"$(…)"`, backslash-newline hide executed code from `code_view`; same weak lexer under-blanks/false-kills (lesson r35 Holds ¶1; r35 residual §4 "comment-blinding not universal"; SCORECARD r35 disclosed defect "code_view") | **EXPLICITLY DEFERRED — NOT taken.** Only planned-block item named not-done | Deferral reason recorded in **four** artifacts: contract `routed_repairs.code_view_ansi_c_quote`; `corpus/lessons/round-36.md` `## Holds` ¶1 (tool sha `6188db16…` pinned by r35 capability row + frozen v1 counter + v2 successor; an edit would void all three and force a full re-audit; planned r37 freeze-before-data with re-pin + re-attest); `SCORECARD.md` r36 intro + `Planned (round 37)`; `LOG.md` r36 bullet |
| H2 | stderr outside the compared tuple (AttackStderrScope, BOUND-1) | Not addressed; carried open | r36 `Planned (round 37)` umbrella: "the open recall classes in the round-35 lesson `## Holds`"; no per-class reason (none owed — still open, not deferred-by-decision) |
| H3 | Removed-workdir side effect not compared (M5) | Not addressed; carried open | same umbrella |
| H4 | Witness-shim config fidelity — **closed at r35** (A4+A7, struck through in Holds); residue: root construction outside the audited block, `HOME`/`TMPDIR`/`PWD`-gated copies | Residue not addressed; carried open | same umbrella |
| H5 | `run_regression` tail region inspected by nothing | Not addressed; carried open | same umbrella |
| H6 | Recall classes: preamble seeding, helper-function scope, name-assembled masks, per-index record parsing (round-34 Holds, measurement-only) | Not addressed; carried open | same umbrella; upstream naming in round-34 `## Holds` |
| H7 | Panel design: public panel small (6 distinct bodies); sealed set is the discriminating surface | Partially touched: v2 freezes public-slot cardinality 6/3 + distinctness 9 as asserted targets, but no new panel bodies; class carried open | addressed-count part: r36 C2 receipts; remainder: same umbrella |
| H8 | C2 counter m1 scope is time-relative (re-derive if baseline moves) | Not addressed; carried open | same umbrella |

Round-35 residual-verification / closure routed items (contract numbering in parentheses):

| Item | Round-36 disposition | Receipts |
|---|---|---|
| Cold-read credit lapse — four drifted headings (recipe, restore discipline, the map, where to enter) routed to r36; SCORECARD planned item 1 | **ADDRESSED — C1.** Monitor command unchanged (`python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev REV`): 6 @ `796e08b` → 8 @ refresh commit `b455001e`, 60/64 → 64/64. Do-nothing control still prints 6 at content commit `e423c41b`. Four new ledger entries + traces under `.ufo/evidence/round-36/coldread/` | `monitor-at-{796e08b,e423c41b,b455001e}.stdout`; `ledger.json` four entries; `refresh-{specs,receipts}.json`, `affected-sections.json` |
| Counter PASS weaker than frozen sentence — no slot-total/distinctness asserts (residual §1; SCORECARD planned item 2; contract defect 2) | **ADDRESSED — C2.** Successor `c1-measure-v2.py` (`9eb8944c…`, frozen pre-data in contract) freezes targets kill=6/accept=3/distinct=9. Vacuous-pass demonstrated: v1 on emptied panel `PASS=true`; v2 on same panel `PASS=false`; v2 deciding at `b455001e` `PASS=true` (6/6, 3/3, slots 9, distinct 9). v1 counter, tool pin, runner bytes all unchanged | `v1-at-emptypanel` (rev `91373d5`), `v2-at-emptypanel`, `c1v2-at-b455001e`; `sha256sum` above; depth D stays 9 |
| LOG r35 dead pointer `ResidualSentinelClosure.md` (contract defect 1) | **ADDRESSED** — append-only r36 LOG correction naming the five real residual reports; `QUALITY.md` criterion 72 added (lesson Mistakes §1) | `LOG.md` round-36 entry; `corpus/lessons/round-36.md` |
| Control narration stale (residual §2, MINOR — superseded by A8 receipt) | No action needed; supersession already recorded in place at r35 | r35 lesson `## Residual verification` |

SCORECARD `**Planned (round 36):**` block, item by item: (1) cold-read refresh — **done** (C1);
(2) successor counter cardinality+distinctness asserts, frozen pre-data then one deciding run —
**done** (C2, kill rule honored: exactly one default-mode v2 run at `b455001e`);
(3) real shell lexer / enumerated supported-form list for `code_view` — **explicitly deferred to
round 37, reason recorded (H1 row above)**; (4) open recall classes in the lesson `## Holds` —
**carried**, now restated verbatim in the r36 `Planned (round 37)` block.

## Observations (flagged, not judged; no edits made)

- **O1 — stale digest in r35 lesson prose:** `corpus/lessons/round-35.md` says the v1 counter's
  "final sha256 `d27e6769…052c2`", but the frozen bytes hash `d360a159…bbe3`, which is what the
  SCORECARD capabilities row (`@ d360a159…`) records. Prose-vs-bytes drift in a historical lesson;
  the counter itself is frozen and matches its SCORECARD pin.
- **O2 — LOG r36 control-receipt filename:** the LOG entry cites
  `control/monitor-at-content-commit.*`; the committed file is
  `control/monitor-at-e423c41b.{exit,stdout,stderr}` (`e423c41b` = the content commit). The
  evidence exists and prints 6; the literal filename in LOG does not resolve. Same reference-drift
  class the round just pinned criterion 72 against.
- **O3 — two numberings of the r35 routed-defect set:** the round-36 contract numbers them
  (1 dead pointer, 2 cardinality, 3 code_view); the r35 SCORECARD section's "Disclosed predicate
  defects" numbers (1 counter-PASS-weaker, 2 code_view). Both artifacts are internally consistent;
  the mapping above uses the contract numbering and names the SCORECARD items explicitly.

## Verdict

Mapping complete and receipt-checked: of the round-35 Holds/routed set, **three items were addressed
this round** (C1 cold-read refresh 6→8 at `b455001e`; C2 cardinality successor with the vacuous-pass
kill demonstrated; the LOG dead-pointer repair), **one item was explicitly deferred with its reason
recorded in four artifacts** (`code_view` ANSI-C `$'…'` class → round 37, pin-voiding rationale), and
**seven classes remain open**, carried only by the round-37 planned umbrella phrase with no new
per-class artifact — plus one new round-36 Holds entry (refresh-scope honesty). Two prose-vs-artifact
drift observations (O1, O2) and one numbering note (O3) are recorded above for a future repair route.
