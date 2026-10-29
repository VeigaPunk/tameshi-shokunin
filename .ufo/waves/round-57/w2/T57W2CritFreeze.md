# T57W2CritFreeze: round-57 contract rewritten for amendment 1 (calibration)

Seat: T57W2CritFreeze (critic, leaf, no subagent dispatch). Lane: tameshi. Base `5e3569969b532310d2b8a3d130901757a3df356b`. Lane HEAD at the time of the checks: `06e9849` (C0 `ca75c26` is an ancestor). The lane contract was not edited; the rewrite is staged at `.ufo/waves/round-57/w2/T57W2CritFreeze/stage/.ufo/evidence/round-57/contract.json`. No lane file and no fleet-root file was written. Git work ran in a scratch clone (`git clone --shared`, toplevel asserted, fixture commit with `fixture <fixture@example.invalid>`), removed on exit.

## Verdict

The staged contract is written and parses. Its C1 predicate is one sentence, its clauses map to all 18 counter TERMS, its C2 target is tightened, and it records amendment 1, a panel block and 19 frozen paths. **It is not ready to freeze.** Four findings block the freeze and need an L1 decision or repair:

1. **The amended C1 counter fails its own selftest: `C1_R57_SELFTEST: 11/45 pass`, exit 1.** Measured at this seat (receipt `T57W2CritFreeze-receipts/c1-selftest.txt`). Failures include `good ledger passes`, `defects pin mismatch counted`, `cli good exits 0`, and most refusal cases. The fixtures were not updated for amendment 1. For example, the good ledger's fix commit (`fix`) names neither the item id nor the path in item text, which the amended tie rule now requires, and the selftest defects carry no `text` field. Freeze precondition: selftest 45/45 (or the new count) with exit 0. The counter's docstring still describes the round-50 floors arm and omits the panel arm.
2. **`open` is a free sink under amendment 1, so the predicate passes ledgers that verify little.** The open branch of `judge()` checks only that the id is named in the newest Planned paragraph (`measure.py` lines 272-275). The panel arm compares `status_at_base` with the panel at BASE, so an item that is open at base and fixed after it is accepted as `open`. The only binding work is six this-round fixes (`this_round_short`, floor 6). Arithmetic from the code (not run against the amended counter): 6 real fixes plus 45 open rows named in the Planned paragraph passes every arm when at most 5 panel disagreements occur. The wave-1 do-nothing run showed the same shape under the round-50 open arm (`T57W1CritC1` section 1, S3: 20 fixed + 31 open, total 0). This is the largest calibration hole in the amended design. The contract states it in `claims.C1.cannot_see` (c). Options for the L1 before scoring, each a new amendment: (a) an open cap (critic's suggestion: open <= 17, a judgement); (b) run the blind panel AT REV for open rows (not AT BASE); (c) a mandatory closure sample of open rows with a stated count.
3. **The tightened C2 needle rule (row needles equal a CODES member) is not met by any landed C0 row, and the C2 counter does not implement it.** Receipt `T57W2CritFreeze-receipts/c2-needle-equality.txt`: `receipt-gate-content-drift` has `code=RECEIPT_REV_CONTENT_DRIFT` and `codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED`; `receipt-gate-unresolvable-certified` has `codes=RECEIPT_REV_UNRESOLVABLE`. None equals a CODES member. The C2 counter's `row_named_codes` uses `CODE_RE.findall` on each needle, so it accepts substrings. I followed the critic's "equal" wording, and the C2 counter must change to match before freeze. The L1 must choose: add bare-code needles to the two C0 rows (a registry content change, re-checked with `registry-check --rev`) or relax the sentence to whole-token containment (a further amendment).
4. **Amendment timing is not clean.** The L1 dry run of the amended counter (`.ufo/waves/round-57/dry-c1-explain.txt`, 21:50:18, `total=21` on the working-tree ledger) predates this amendment record. The record says so and does not assert that no row changed in response. The L1 must state that in the round report. No committed REV has been scored.

Smaller items the L1 should fix before freeze (none changes the verdict above):
- `controls.sh` line 18 says CTL_SKIP_c1 "the declined cap must fire"; under amendment 1 the cap is 999, so declined_over is always 0. The control still expects `C1_R57_PASS=false`, so it is not a mismatch, but the comment is false.
- The contract's C1 and C2 `before` pointers to `.ufo/evidence/round-57/before/*.stdout` are dangling: `before/` and `after/` are empty directories. The C1 before-state is now measured (below). The C2 before-state was not re-measured here.
- `panel.json` does not exist; `PANEL_SHA256` is the placeholder. The panel is specified, not run.
- The contract's C1 `before` said "about 52" items; the frozen set has 51.

## What changed in the contract (staged)

- `amendments[0]` (n=1): what (a)-(i), why (T57W1 critic sections, cited), evidence paths (all existence-checked), and `before_scoring`, which discloses the 21:50 dry run.
- `claims.C1`: `before` (measured), `predicate` and `target` (the same single sentence, 1644 characters, checked equal in code), `predicate_terms` (clause to counter TERMS), `verdict_line_tokens`, `terms_line`, `freeze_precondition`, `enumeration` (commands per count), `kill_rule` (names the failing terms), `controls` (unchanged names), `cannot_see` (a)-(g).
- `claims.C2`: `target` tightened per the critic: at least 3 admitted gate rows expecting exits 0, 2 and 3; exit 1 named as usage; equality needles per CODES; the SKILL Verdict-map cell names exits 0/1/2/3 and `RECEIPT_REV_UNRESOLVABLE`; the Standing-rules verdict-receipt cell equals the emitted code; every `RECEIPT_*` token in that section is a CODES member (AST). `enumeration` added. `cannot_see` extended (row 2 not equality-checked; registry-check does literal substring matching).
- `panel`: file, shape, three blind seats (inputs withheld: keys, ledger rows, Planned paragraph, counter), question AT BASE, consolidation (majority of two; no two equal gives `contested`, which counts as one disagreement), budget 5 with the reason, adjudication (the L1 re-checks every disagreement and reports it; adjudication never changes the count; panel.json is not edited after commit), and the ordering (freeze defects and keys, run panel, commit panel.json, pin its sha in measure.py, freeze measure.py and contract, score committed REV only).
- `frozen_paths`: 19 entries (c1 x4 + panel.json, c2 x2, control x2 by name, controls.sh, deciding-run.sh, no-harm.sh, contract.json, tools/receipt-revision-gate.py, tools/registry.json, tools/registry-check.py (added: the C2 counter executes it at REV), three receipt-gate fixtures). `freeze.json` is not listed.
- Unchanged: `no_harm`, `frontier`, `routed_defects_from_round_56`, `lowest_axis`, `shape`, `base_note`.

## Counter TERMS and verdict-line tokens (for the receipt)

| Predicate clause | Counter term(s) |
|---|---|
| (1) 49 BASE rows canonically unchanged | `old49` |
| (1) one row per item, no other row | `missing`, `duplicate`, `extra` |
| (1) frozen set sha256 | `defects_pin` |
| (2) status and status_at_base validity and coherence | `bad_status`, `base_status_bad` |
| (3) evidence resolves; whole-token key | `evidence_bad`, `key_miss` |
| (4) fixed row (commit, ancestry, base coherence, introduction, tie, ack words) | `fixed_bad` (EXPLAIN `fixed-not-new`, `fixed-commit`, `fixed-base-incoherent`) |
| (5) open row named in newest Planned paragraph | `open_unplanned` |
| (6) declined reason >= 40 characters | `declined_bad` |
| (7) seven spot-check files byte-equal | `spotcheck_changed` |
| (8) six fixes carried after BASE | `this_round_short` |
| (9) panel budget and panel pin | `panel_over`, `panel_pin` |
| not binding (always 0) | `fixed_short`, `declined_over` |

All 18 TERMS are mapped (checked). Verdict line tokens: `C1_R57:` `self=` `rev=` `rows=have/51` `agree=n/51` `old49=ok|CHANGED` `fixed=` `declined=` `thisround=` `panel=pin|k/5` `spot=ok|DRIFT` `total=` `C1_R57_PASS=`. The TERMS line adds `fixed= open= declined= fixed_this_round=` and the 18 terms. The contract's `verdict_line_tokens` gives each token's meaning.

## Measurements (commands and outputs)

1. Frozen-set pin: `sha256sum .ufo/evidence/round-57/c1/defects.json` = `bef2293ba3db863b03247e9867b11aa2501aa54af0b098ce0f974817f485dee9` (matches the counter's pin). Count 51, unique ids 51, seven spot files, `per_round` 4/8/6/9/10/7/7.
2. Base ledger: `git show 5e35699…:corpus/routed-defects.json` gives 49 rows (31 fixed, 7 open, 11 declined).
3. Before-state (receipt `before-c1.txt`): the counter run on a scratch commit adding only the frozen set to BASE (the frozen set is untracked in the lane, so the counter cannot run at BASE itself, which is a setup error): `C1_R57: self=63a88c257490 rev=aa691617c08b rows=0/51 agree=0/51 old49=ok fixed=0 declined=0 thisround=0 panel=pin spot=ok total=58 C1_R57_PASS=false`, exit 1. The TERMS line shows `missing=51 this_round_short=6 panel_pin=1`.
4. Counter selftest (receipt `c1-selftest.txt`): `C1_R57_SELFTEST: 11/45 pass`, exit 1 (the earlier shell line `selftest exit=0` was the exit of `tail`, not of the counter; the real exit is 1).
5. CODES: `ast`-parsed from `tools/receipt-revision-gate.py` at HEAD: 11 members. Gate exits, from the source: 0 PASS (`main` returns 0), 1 usage (`SystemExit('usage: ...')` at lines 92, 183, 187), 2 unresolvable (line 194), 3 refused (line 220).
6. Registry at BASE: 22 `gate`-kind rows, none for the gate. At HEAD the admitted gate rows are the three C0 rows (`receipt-gate-accept`, `receipt-gate-content-drift`, `receipt-gate-unresolvable-certified`).
7. Frozen-path existence: 18 of 19 exist; `panel.json` is the only absent path, as planned.
8. Evidence paths named in `amendments[0].evidence` and in `before`: existence-checked; all present except the `before/` pointers, which were replaced.

## Items the counter cannot see (stated in `cannot_see`, not countable here)

- Semantic support of a keyed excerpt; completeness of the 51-item set (extractor recall); whether an open row is still open at REV (finding 2); panel disagreements that are right within the budget of 5; key relevance; that a fixed commit's message reflects the work; that a declined reason is more than its length.
- C2: whether the three mutants are the defects that matter; exits the committed fixtures do not exercise; the row-2 Standing-rules cell (not equality-checked).

## Sentences of the contract I could not make countable

- C1 `cannot_see` (a), (b), (c), (d), (e), (f), (g): these are stated as limits, not as checked predicates. (c) is countable only by a closure sample, which the contract does not yet fix in number.
- The panel blindness condition ("three leaf seats that have not read ... ") is not countable by the counter. It can be attested only by the seats' own receipts, and the contract does not yet require them.
- The panel adjudication line count ("one line per disagreement") is countable by the L1's report, but the contract does not name the report path.
- C2 `cannot_see`: "whether the three mutants are the defects that matter" is a judgement, not a measurement.
- `no_harm.cold_read_floor` (round-21 monitor credited=64/64 score=8 box3=true) and `frontier` items are countable only by running their named tools; they were not run in this item and are unchanged.
- The original C1 target sentence ("every row agrees with the tree") was removed: it cannot be made countable for open rows (finding 2).

## Tools

None installed or updated. Used the host's `git` and `python3` (stdlib: `json`, `ast`, `subprocess`, `hashlib`). No pacman, uv, npm or `~/.local/bin` writes.

## Files written

- `.ufo/waves/round-57/w2/T57W2CritFreeze/stage/.ufo/evidence/round-57/contract.json` (staged contract)
- `.ufo/waves/round-57/w2/T57W2CritFreeze.md` (this report)
- `.ufo/waves/round-57/w2/T57W2CritFreeze.json` (machine-readable summary)
- `.ufo/waves/round-57/w2/T57W2CritFreeze-receipts/before-c1.txt`, `c1-selftest.txt`, `c2-needle-equality.txt`

## Checks the main agent should run

- `python3 .ufo/evidence/round-57/c1/measure.py --selftest` must exit 0 and print `C1_R57_SELFTEST: n/n pass` after repair (finding 1).
- The C1 counter at a committed REV only, after panel.json is committed and its sha is pinned (ordering in `panel.order`).
- `python3 .ufo/evidence/round-57/c2/measure.py --selftest` and the C2 dry run after the needle-equality decision (finding 3).
- `registry-check.py --rev REV` for the three gate rows once any needle edit lands.
