# T57W1ScribeItemsR52x1to3 — ledger rows R52.1–R52.3 (round 57, wave 1)

Seat: T57W1ScribeItemsR52x1to3 · axis: calibration · lane base `5e3569969b532310d2b8a3d130901757a3df356b` · spot-check `corpus/lessons/round-52-verifier-spotcheck.md` (added by `c1d49d76be4028df2a68322e7117ff3aafaccd5c`, the `routed_at` for all three items).

## Decisions

| id | status | fixability | commit / reason | evidence (lane file, lines) |
|---|---|---|---|---|
| R52.1 coldread re-key debt | **fixed** | n/a (no patch needed) | `e98044a615bf785ede3a511d506801e55c1828f2` | `.ufo/evidence/round-21/coldread/ledger.json` 42410-42411 (`### The tick, executed`, sha256 `d58978b5…`); 42242-42243 (`### The receipt at this boundary`, sha256 `a44eec94…`) |
| R52.2 LOG.md round-52 entry missing | **fixed** | n/a | `a41195dfc13a73958e4c5228ec196b28d03ded03` | `LOG.md` 2444 (`## 2026-10-27 — round 52 (honest stop, run wrap-up)`) |
| R52.3 over-count review overstated | **open** | **fixable-costly** — uncredits none | none; stays open (see below) | `corpus/lessons/round-52.md` 27 (`Example: Corr12, where the reviewer found 0 of 14 …`) |

Rows: `.ufo/waves/round-57/w1/T57W1ScribeItemsR52x1to3/rows.json` (each row carries `keys`, `verdict_basis`, `note`). Nothing staged under `stage/` (R52.3 is not a cheap patch).

## Verification (commands and outputs in `T57W1ScribeItemsR52x1to3-receipts/`)

1. **Spot-check and base.** `git log --diff-filter=A -- corpus/lessons/round-52-verifier-spotcheck.md` → `c1d49d7`. Base is `5e35699`, which contains `c1d49d7`.
2. **R52.1 monitor.** In a scratch clone at base, `python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev <rev>`:
   - at base `5e35699` → 64 of 64 sections credited (exit 0);
   - at `c1d49d7` → 45 of 64 credited (exit 0), the closure's figure.
   - 19 headings are credited at base and uncredited at `c1d49d7`. They are exactly the R52.1 set: `The tick, executed`, `The receipt at this boundary`, `Using the ledger`, `Six-case confidence statement …`, and the rest.
   - Entry `### The tick, executed` (sha256 `d58978b5…`) is absent at `c1d49d7` (grep count 0) and present at base (2 occurrences). `git log --reverse -S` shows first addition in `e98044a` (round-53 re-key pass 1), then `88afa94`.
   - Restoring commit chosen: `e98044a`, the first re-key commit to bind a lost heading. The full 19-heading credit was reached by `88afa94`, `7fa9a5e` and `c1dd23b`; the note in the row says so.
3. **R52.2.** `git log -S'round 52 (honest stop, run wrap-up)' -- LOG.md` → `a41195d` only. Occurrences of `round 52 (honest stop` at `c1d49d7` are 0; at base 1. `a41195d` touches `LOG.md`.
4. **R52.3 still true at base.** `corpus/lessons/round-52.md:27` retains the "0 of 14" example; `git log c1d49d7..5e35699 -- corpus/lessons/round-52.md` is empty. Corr12's reader `.ufo/evidence/round-51/coldread/reads/T51W2Read12.md` carries two strict `| **drift** |` rows: P2 (line 55) and P10 (line 63). So the "0 of 14" statement is contradicted. The round-53 contract's note claims R52.3 "worked under this round", but no tree change backs that.
5. **Row check through the round-50 counter's own code.** `.ufo/evidence/round-50/c1/measure.py` is imported (not copied) and `measure()` is run over the three rows on a fixture commit in a second scratch clone (`fixture_measure.py`, `regex_check.py`):
   - `fixed=2 open=1`, `R52.1` and `R52.2` pass (resolver, keys, touched-commit freshness, ACK words, ancestry all ok);
   - `R52.3`: `open_unplanned=1` even though the fixture's planned paragraph names `R52.3` (see finding 1);
   - the same run with only the planned-id regex widened to `\bR\d{2}\.\d+\b` gives `total=0`.

## Why R52.3 is open, not fixed, and what it would take

A correct fix re-derives the over-count verdicts for records 01, 02, 06, 09–13 under one written counting rule (the closure proposed "reader-marked drift at CAND; exclude holds-hist"). That means mapping 51 record findings to reader rows. The readers use three formats (markdown tables, JSON blocks, prose), so there is no single mechanical join. I counted strict `| **drift** |` table rows: Corr12 has 2 and the others have 0. That count covers only the table format, so the zeros for the other readers are **not** a count of their qualifying findings. The row is therefore `open`, not `fixed`, and no lesson patch is staged.

Uncredit: `corpus/lessons/round-52.md` is not a pinned input of the round-21 ledger. `grep 'lessons/round-5' ledger.json` finds only round-10…round-51 names, and no `round-52.md` entry. A later correction would not uncredit any cold-read heading.

## Findings for the L1

1. **Round-50 counter cannot pass any open R5x row.** `planned_ids()` in `.ufo/evidence/round-50/c1/measure.py` uses `\bR4\d\.\d+\b`. An `open` row for any R5x id is therefore always `open_unplanned`, however the newest `**Planned (round` paragraph reads. Verified: the fixture's paragraph names `R52.3`, `planned_ids` returns `set()`, and `open_unplanned=1`. Round 57's C1 counter inherits this regex; it must match `R\d{2}\.\d+` or equivalent before any open R5x row can pass.
2. **R52.3 needs the planned line.** Base SCORECARD's newest `**Planned (round` paragraph is round 55 (`SCORECARD.md:2598`) and does not name R52.3. The L1 must add it in round 57's paragraph at the content-final commit if R52.3 stays open.
3. **Reader-format caveat.** Any future re-derivation of R52.3 must start from the reader's own verdict format per file, not from a table grep.

## Tools

None installed or updated. The fixture used `git clone --shared` and `git -c user.name=fixture` in scratch only; no lane or fleet repo was mutated. Scratch clones were removed at the end.

## Out of scope

Did not decide the floors (L1). Did not touch SKILL.md, QUALITY, SOURCES, README, or any ledger-pinned section.
