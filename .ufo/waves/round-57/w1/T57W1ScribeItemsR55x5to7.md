# T57W1ScribeItemsR55x5to7 — routed items R55.5, R55.6, R55.7 (round-57 wave 1)

Seat: `T57W1ScribeItemsR55x5to7` (leaf scribe). Lane base `5e3569969b532310d2b8a3d130901757a3df356b`.
Source: `corpus/lessons/round-55-verifier-spotcheck.md` items 5-7, routed at `fa48c06c3669355fd80e8722eb733c1d6dfdd2f8` (the only commit that touches the spot-check).

## Verdicts

| id | status | commit / reason | evidence (lane, not spot-check) | keys |
|---|---|---|---|---|
| R55.5 | fixed | `c3e2ca9f020776b3d66c7af854fb82c834674fcf` | `tools/receipt-revision-gate.py` 4-7, 27-28; `.ufo/evidence/round-56/deciding-run.sh` 120-122 | R55.5, receipt-revision-gate.py, deciding-run.sh, RECEIPT_REV_CONTENT_DRIFT |
| R55.6 | fixed | `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` | six round-55 receipts under `.ufo/waves/round-55/` (1-2 each) | base.json, cand.json, rekey.json, coldread-HEAD.json, inputs.json |
| R55.7 | declined | closure-environment contamination; reason stated in rows.json | `corpus/lessons/round-56.md` 60-61, 108 | R55.7, after/c2.stdout, T55W1MutC2-receipts |

Rows: `.ufo/waves/round-57/w1/T57W1ScribeItemsR55x5to7/rows.json` (ledger schema plus `keys` and `verdict_basis` per row).

### R55.5 — fixed by c3e2ca9f (round-56 freeze)
- Defect as routed: `deciding-run.sh` never compares a control `rev=` with the revision under test.
- Tree at base: `tools/receipt-revision-gate.py` exists (added at `c3e2ca9f`, amended at `21eb3c63`); the round-56 `deciding-run.sh` calls it at line 111 and gate 0b runs it on `controls-a/b.stdout` at 120-122.
- Absent at `fa48c06`: `git cat-file -e fa48c06:tools/receipt-revision-gate.py` → `exists on disk, but not in 'fa48c06…'`; `c3e2ca9f` is not an ancestor of `fa48c06`, is an ancestor of base.
- Behaviour at base (clone, receipts saved): the QUALITY 107 command on the real round-54 positive control refuses it, `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED`, exit 3; the same receipt certified at its own revision passes, exit 0.
- Not run: the deciding script itself (round-56 territory); gate 0b is read statically.

### R55.6 — fixed by 981c5e8b (round-56 start)
- Defect as routed: seven round-55 receipts created before the lane tip, never committed.
- `git log --diff-filter=A` for all seven: `981c5e8b` (after `fa48c06`), all absent at `fa48c06`, all present at base. `6efd2a1` re-swept the same set in the same round.
- Cited six (`floor.json` shares rekey.json's byte count, 3022874, and is not cited); each resolves, each path ends with a key (SOFT-path rule).
- Caveat: the excerpts prove the committed content; the commit proof is `git show --stat 981c5e8b` (nine files, all under `.ufo/waves/round-55/`).

### R55.7 — declined (closure-environment)
- The spot-check labels it "closure-environment contamination (not lane debt)". Round 56's lesson records the lane side reverted at `6efd2a1` and the harness side as residual (`## Round-55 routed defects`, row R55.7: PARTIALLY DISPOSED).
- Declined: no lane file change can fence a concurrent non-lane seat's writes; the lane-side symptom is gone at base. Reason is 262 chars, well above the 40-char floor.

## Checks run (commands and results)

1. Ancestry and spot-check commit: `git merge-base --is-ancestor` for `fa48c06`, `c3e2ca9f`, `981c5e8b`, `6efd2a1` against base; `git log -- corpus/lessons/round-55-verifier-spotcheck.md` → only `fa48c06`.
2. Presence at `fa48c06` for the gate, the seven receipts (`git cat-file -e`): all absent at `fa48c06`, all present at base.
3. Resolver (imported by path from the base clone, not copied): `check_evidence` on all 10 evidence items → `None` for each; `has_key` True for each item.
4. Full `measure()` on a fixture ledger (only the three rows, committed in a fixture clone at base): `stat={'fixed': 2, 'open': 0, 'declined': 1}`; counts `missing/extra/duplicate/spotcheck_changed/defects_pin/bad_status/evidence_bad/key_miss/fixed_bad/open_unplanned/declined_bad` all 0. Only `fixed_short=18` and `this_round_short=5` are non-zero, which are the fixture's three-row floors (L1 decides floors). Receipt: `.ufo/waves/round-57/w1/T57W1ScribeItemsR55x5to7-receipts/measure-fixture-3rows.json`.
5. Negative control: the same fixture with R55.5's commit set to base → `counts={'fixed_bad': 1}`, note `fixed-not-new R55.5` (the row can fail). Receipt: `negative-control-r55-5-commit-base.json`.
6. Gate red/green: `gate-r54-ctl-pos-certified-c2108100.stdout` (exit 3, `RECEIPT_REV_CONTENT_DRIFT`), `gate-r54-ctl-pos-certified-own-rev.stdout` (exit 0, `verdict=PASS`).

## Fixability triage

No item is `open`. No patch is staged and no `fixable-cheap`, `fixable-costly` or `not-fixable` label applies. No file outside the seat's own paths was edited; `SKILL.md`, `QUALITY.md`, `SOURCES.md`, `README.md`, knowledge entries, and the ledger itself were not touched (the ledger rows are only in `rows.json` for the L1 to merge).

## Residuals and limits

- Semantic support is not measured by the counter: the R55.5 excerpts show the gate's code paths, not that the gate catches every drift; that rests on the gate's own selftest and the QUALITY 107 falsifier.
- Dropped unverified claims: none. Every `fixed` commit was confirmed by an ancestry check and a per-path presence check; every excerpt was checked by the frozen resolver.
- Not run: the lane's counters, the cold-read monitor (no lane file changed), the deciding script.
- Tools installed or upgraded: none. Writes: staged rows, receipts and this report under `.ufo/waves/round-57/w1/`; clones and fixtures under scratch; no lane or fleet git mutation.
