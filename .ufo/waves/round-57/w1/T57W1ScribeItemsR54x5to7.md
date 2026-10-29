# T57W1ScribeItemsR54x5to7 — ledger rows R54.5–R54.7

Seat: scribe, wave 1 of round 57 (L1 `TameshiR57`). Item: triage routed items R54.5, R54.6, R54.7 from `corpus/lessons/round-54-verifier-spotcheck.md` into ledger rows for `corpus/routed-defects.json`. Lane base `5e3569969b532310d2b8a3d130901757a3df356b`. No lane file was edited; the candidate ledger was committed only in a scratch clone.

## Verdicts

| id | verdict | credited commit | evidence (lane records, not spot-checks) |
|---|---|---|---|
| R54.5 | **fixed** | `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` | `SCORECARD.md:2661-2662`, `corpus/lessons/round-55.md:59` |
| R54.6 | **fixed** | `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` | `SCORECARD.md:2669`, `corpus/lessons/round-55.md:60` |
| R54.7 | **fixed** | `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` | `SCORECARD.md:2674-2675`, `corpus/lessons/round-55.md:61` |

No item is `open` or `declined`. No item is `unresolved`. Nothing was staged under `stage/` because no item is open. Floors are not decided here.

## Basis, per item

**R54.5 (finding counts).** The routed defect is the round-54 report's "25 wave-1 findings" and "22 findings in 9 sections" against the committed readers. Re-derived at base from the 46 committed `T54W{1,2}Read*.json` files (`-receipts/` excluded):

- w1: 23 reports, **28** findings, 15 non-empty.
- w2: 23 reports, **25** findings, **12** non-empty sections.

The correction `w1=28 w2=25 sections=12` is in `SCORECARD.md` ER-R54-5, added by `9cf0146`. The pre-correction text is absent at routed_at `650987a`. Matches the re-derivation. Caveats: the fleet report `.ufo/reports/round-54/tameshi.md` is outside the lane and still carries the old numbers; the "26" in commit subject `99c3bc8` is immutable history and is not named in the correction.

**R54.6 (uncommitted round work).** The three seat deliverables (`T54W2Sent03.md`, `T54W2Sent03-receipts/c1committed-positive.stdout`, `T54W2Sent03-receipts/rejection-attribution.txt`) all exist at base and were first added by `ff2a821`. That repair predates routed_at `650987a`, so the round-50 rule (fixed commit must not be an ancestor of routed_at) cannot credit `ff2a821` directly. The ledger credits `9cf0146`, which post-dates routing and introduces the corrected text ("they are committed; the sweep that committed them is `ff2a821`"). **Flag for L1:** a defect repaired before its spot-check routed it can only be credited through a later record commit. That is a rule consequence, not a lane defect.

**R54.7 (forged-file disposition).** `T54W2Sent01-forged-reader.json` is absent at base; `T54W2Sent01-receipts/forged-reader.json` is present; `7fa9a5e` is an R100 rename with 0 content change. The corrected wording "renamed into … at `7fa9a5e`" is in `SCORECARD.md` ER-R54-7, added by `9cf0146`. Non-credit re-checked: the path does not match `/T54W\d+.*Read.*\.json$`, and its `section_sha256` `b90c1f79…` occurs only in the forged file and in the seat report `T54W2Sent01.md`, never in a committed Read JSON. The fleet report still says "the deletion lands in 7fa9a5e0" (outside lane reach).

## Verification

- Round-50 resolver reused by import (`.ufo/evidence/round-50/c1/measure.py`, `check_evidence` and `measure`), run on a scratch clone at base with the three candidate rows committed there. Output `receipts/measure-fixture.txt`: all six evidence items resolve; `TOTAL 0`; `fixed=3`; no refusals; spot-check bytes unchanged (sha256 of base bytes pinned).
- Negative controls (`receipts/negative-controls.txt`), each caught by the resolver:
  - R54.6 credited to `ff2a821` → `fixed-commit` refused (predates routing).
  - R54.5 excerpt with `w1=29` → `evidence-bad excerpt-not-in-lines`.
  - R54.7 keys matching nothing → `key-miss`.
- Count sweep, ancestry and rename checks: `receipts/sweeps.txt`.
- The round-57 counter itself was not run; it is not this seat's assignment.

## Artifacts

- `.ufo/waves/round-57/w1/T57W1ScribeItemsR54x5to7/rows.json` — three rows with `keys`, `verdict_basis`, `seat`, `note`.
- `.ufo/waves/round-57/w1/T57W1ScribeItemsR54x5to7.json` — machine-readable summary.
- `.ufo/waves/round-57/w1/T57W1ScribeItemsR54x5to7-receipts/` — `measure-fixture.txt`, `negative-controls.txt`, `sweeps.txt`, `build.py`, `negctl.py`.

## Out of scope / not done

- No lane file edited; no fleet file written.
- Cold-read ledger not consulted: no fix was staged, so no pinned input is touched.
- Tooling: none installed or upgraded (standard library and `git` only).
