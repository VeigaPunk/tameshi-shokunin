# Round-52 wave-1 — recurrence tracker

Classification from the closure spot-checks' explicit status-neutral conformance defects (where present) and routed-defect sections, cross-checked against the routed-defects ledger. Commands below are the source-display commands; line references refer to the lane files named.

| Class | Rounds seen | Fix recorded (where) | Recurred after fix? (pointer) |
|---|---|---|---|
| Selftest receipts absent / not committed as durable L1 evidence | 45, 47 | Round 46 committed `selftest/c*-selftest.stdout` (round-46 spot-check:19; round-47 spot-check:23); round 50 records the round-47 receipts in `.ufo/evidence/round-50/routed/receipts/MANIFEST.md:14-15` (ledger R47.2, `corpus/routed-defects.json:630-647`) | **Yes.** Round 47 explicitly says the round-46 practice was not repeated (`round-47-verifier-spotcheck.md:23`); R47.2 was fixed by round 50 (`routed-defects.json:630-647`). The initial round-45 defect itself was fixed (`routed-defects.json:433-445`). |
| Tool behavior / registered gate or registry statement drift | 47, 51 | Round 48 restated the six-leg row and env-differential row from repeated runs (`routed-defects.json:606-627`; round-47 routed defect 1 at `round-47-verifier-spotcheck.md:103`); round 52 is routed to update the mte row and SKILL statement (`round-51-verifier-spotcheck.md:124-127`) | **Yes.** R47.1 was recorded fixed in round 48, but round 51 found `mte-interop.py`'s ten-leg table versus registry's 9/9 expectation and SKILL's “nine ledger legs” (`round-51-verifier-spotcheck.md:84-88`). This is R51.1 and the analogous row/statement drift. |
| Stale line pointers / claims not kept aligned to changed source | 48, 51 | Round-48 lesson appended its own line-pointer correction (`round-48-verifier-spotcheck.md:30`); round-51 routes corrections to SKILL runner pointers and scope (`round-51-verifier-spotcheck.md:127`) | **Yes.** The round-48 pointer correction did not prevent the distinct stale runner pointers and write-scope statement in round 51 (`round-51-verifier-spotcheck.md:127`). |
| Round lesson/report completeness: rejected candidates and cross-domain findings omitted from required section | 51 | No closure-recorded fix in the specified rounds; round 51 routes both omissions (`round-51-verifier-spotcheck.md:130-131`) | **No recurrence can be established from rounds 45–51:** these are first reported at round 51, with no later closure in this set. |
| Deciding/control workflow and freeze/provenance hygiene | 48, 51 | Round 49 deciding script added gate-0 ancestry/order and receipts discipline; routed ledger records R48.2/R48.3 fixed (`routed-defects.json:752-797`) | **Not the same defect recurring.** Round 48's late controls/undisclosed previews are distinct from round 51's disclosed pre-scoring amendment and freeze change (`round-48-verifier-spotcheck.md:27-29`; `round-51-verifier-spotcheck.md:33`). |
| Wave dispatch / seat-template operational failures | 47, 51 | No durable gate/fix recorded in the cited routed defects for the round-47 below-floor issue (`round-47-verifier-spotcheck.md:21`); round 51 reports placeholder expansion, misrooted copy, dead seats and missed attack (`round-51-verifier-spotcheck.md:34`, routed R51.5 at `:129`) | **Related recurrence, not demonstrated same mechanism:** both impede planned falsification coverage, but round 47 was an undispatched wave; round 51 was a malformed builder/misrooting failure. |
| Other one-off conformance / evidence issues | 45: dead/duplicate seats (45:19); 46: quote punctuation (46:20); 48: salvage attribution, census warning (48:26,31); 49: redundant hidden copy (49:25); 51: R51.2 re-key overstatement (51:89) | As individually noted in the corresponding closure; no cross-round repeated instance established in the requested range | **No recurrence demonstrated** by these spot-checks. |

## R51.1 classification and missing gate

R51.1 belongs to **tool behavior / registered gate drift**: implementation growth changed the tool's observable leg count while its registered expected output remained 9/9. Evidence: the closure establishes the added `bash-drift-pins` leg and ten-leg output at `round-51-verifier-spotcheck.md:84-88`; its routed-defect instruction is at `:126`.

The gate that would have caught it is an **operational registry replay at the candidate revision**, asserting every active row's registered outcome (specifically `registry-check.py --only mte-interop-check`) with a committed green receipt before accepting the tool change. The round-51 closure itself names this exact gate/receipt remedy at `round-51-verifier-spotcheck.md:126`. A note merely saying to remember to update the row would not enforce agreement.

## Sources and commands

- `corpus/lessons/round-45-verifier-spotcheck.md:19,83-86` — `read` the indicated ranges; shows absent selftest receipts and routing.
- `corpus/lessons/round-46-verifier-spotcheck.md:20,95-101` — `read` the indicated ranges; records no material conformance defect and subsequent routing outcomes.
- `corpus/lessons/round-47-verifier-spotcheck.md:20-25,97-104` — `read` the indicated ranges; explicit five defect classes and routed items.
- `corpus/lessons/round-48-verifier-spotcheck.md:25-31,112-115` — `read` the indicated ranges; explicit conformance defects and routed items.
- `corpus/lessons/round-49-verifier-spotcheck.md:25,120-127` — `read` the indicated ranges; no conformance defect, routed defects.
- `corpus/lessons/round-50-verifier-spotcheck.md:25,96-99` — `read` the indicated ranges; no conformance defect, two routed issues.
- `corpus/lessons/round-51-verifier-spotcheck.md:30-34,84-89,124-132` — `read` the indicated ranges; R51.1 and related routed defects.
- `corpus/routed-defects.json:433-445,606-647,728-827,861-951` — `read` the indicated ranges; fix/open history for cited recurrence examples.
- `considerthese/2026-10-26.md:80-82` — `read` the indicated range; proposal's recurrence example and gate-not-note criterion.
- `python3 -c 'import json; d=json.load(open("corpus/routed-defects.json")); print([(x["id"],x["status"]) for x in d["defects"] if x["id"].startswith(("R45.","R46.","R47.","R48.","R49."))])'` — ledger status tally by routed id (the file states its coverage is round 40–49 at `routed-defects.json:4`).

## Summary
- Recurrent after recorded fix: missing durable selftest receipts (45 → fixed 46 → 47 → fixed 50).
- R51.1 is the recurrent tool/registered-gate drift class, analogous to R47.1.
- Operational replay of registry rows at the candidate revision is the catching gate, not a reminder.
- Round-48 stale-pointer/wording correction did not preclude fresh stale pointers in round 51.
