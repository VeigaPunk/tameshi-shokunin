# T57W1ScribeItemsR54x8to10 — ledger rows R54.8, R54.9, R54.10

Seat: T57W1ScribeItemsR54x8to10 (wave 1 of round 57, L1 TameshiR57). Lane base `5e3569969b532310d2b8a3d130901757a3df356b` (= lane HEAD at seat start). Judged on: calibration. No lane file was edited; staged content is under `stage/`.

## Verdicts

| id | status | commit | verdict (against the tree at base) | fixable |
|---|---|---|---|---|
| R54.8 | **open** | — | (a) closed by `9cf0146`: the seat file carries a SUPERSEDED block. (b) still true at base: `corpus/lessons/round-54.md` has no record of the `config.yml` write (`git grep -i config` on that file: no hits); the record lives only in `corpus/lessons/round-55.md` and SCORECARD `ER-R54-8`. | **fixable-cheap** (staged patch, §4) |
| R54.9 | **fixed** | `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` | lesson line 51 `84 staged` is corrected to `80` in `9cf0146`; SCORECARD `ER-R54-9` records `reviewers=5 attack=21/76 seats=76` and `staged=81`. | — |
| R54.10 | **fixed** (judgement, §5) | `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` | SCORECARD `ER-R54-10` states the correct pairing (`controls-a.stdout` prints `rekeyed=0/7`; `0/30` is `r53-counter-at-88afa941.stdout`). No lane file carried the misquote at `routed_at` (receipt 02). | — |

Rows: `rows.json` (measure fields plus `keys`, `verdict_basis`, and an `after_patch` template for R54.8); `ledger-rows.json` (only the ledger fields, for merge). Full evidence excerpts are in those files.

## 1. Commit facts (receipt `…-receipts/01`)

- `routed_at` = `650987a0d6fc285b37f0f9e63a3aae864af9cd5a` (the commit that added the spot-check; the round-50 rule takes the oldest add). Erratum `0a2010a` appended the R54.10 text afterwards.
- Fix commit `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (round-55 C0): ancestor of base, not an ancestor of `650987a`. It touches `SCORECARD.md`, `corpus/lessons/round-54.md` and `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`.

## 2. Evidence, checked by the round-50 resolver

Excerpts come from `measure.py` imported as a module (`check_evidence`, `show`, `norm`, `measure`); the copy was not edited. `sys.dont_write_bytecode` was set, so no `__pycache__` was written into the lane.

| id | evidence (path, lines at base) | excerpt (abridged) |
|---|---|---|
| R54.8 | `corpus/lessons/round-54.md` 98-98 | `## Round-53 routed defects — dispositions (this round)` |
| R54.8 | `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` 343-343 | `recorded in corpus/lessons/round-55.md.` |
| R54.9 | `corpus/lessons/round-54.md` 51-52 | `The other 80 staged merge/tameshi entries — REFUSED for the same capacity reason; they stay reserved by document.` |
| R54.9 | `SCORECARD.md` 2694-2696 | `Corrected: reviewers=5 attack=21/76 seats=76 (27.6 %) from .ufo/waves/round-54/w1-registry.json, and staged=81 …` |
| R54.10 | `SCORECARD.md` 2700-2702 | `Corrected: controls-a.stdout's CTL CTL_R53 line prints rekeyed=0/7; the rekeyed=0/30 reading belongs to …` |
| R54.10 | `.ufo/evidence/round-54/control/controls-a.stdout` 3-3 | `CTL CTL_R53 C1_R54: … rekeyed=0/7 … C1_R54_PASS=false` |

Keys: R54.8 `round-54.md, T54W1ExecStraceNoise.md, config.yml, m_glm53`; R54.9 `merge/tameshi, w1-registry.json, staged=81, reviewers=5`; R54.10 `controls-a.stdout, CTL_R53, r53-counter-at-88afa941`.

## 3. Sweeps and results (receipts `…-receipts/`)

Fixture repos live in scratch (a shared clone detached at base, commits under `-c user.name=fixture`; `--show-toplevel` asserted equal to the clone before any commit).

- `04-fixture-and-resolver-results.json` — fixture A (base + the three rows, stock rule): R54.9 `fixed` total 0; R54.10 `fixed` total 0; R54.8 `open` total 1, the single term `open_unplanned`. With `planned_ids` widened to name R54.8 (the only change): R54.8 total 0. Fixture B1 (base + staged lesson patch) then B2 (ledger with R54.8 `fixed` at B1): R54.8 `fixed`, `fixed_this_round=1`, total 0.
- `05-negative-controls.json` — the checker kills what it should: N1 excerpt `84 staged` not in lines → `evidence_bad`; N2 commit = `routed_at` → `fixed_bad`; N3 commit = base → `fixed_bad` (`fixed-not-new`); N4 declined with a 9-character reason → `declined_bad`; P1 the R54.10 row → total 0.
- `03-excerpt-line-locations-at-base.txt` — the line numbers above, located by substring search.
- `02-misquote-absent-at-routed-at.txt` — at `650987a` no lane file pairs `CTL_R53` or `rekeyed=0/30` with `controls-a`.
- `06-pins-and-planned-regex.txt` — the cold-read ledger `round-21/coldread/ledger.json` has 0 references to `corpus/lessons/round-54.md`, `round-54.md`, `T54W1ExecStraceNoise` or `routed-defects`; the round-54 and round-56 freeze/contract JSONs have 0 pins on them; round-55 `freeze.json` and `contract.json` mention the round-54 lesson only inside amendment prose (not a pinned path).
- `08-fleet-report-copies.txt` — the fleet report `.ufo/reports/round-54/tameshi.md` (outside the lane) still carries `26.3 %` (line 8), `fabricated` (108), `recorded here and in the lesson` (112), `other 84 staged` (206), and the `CTL_R53 … rekeyed=0/30` pairing with `controls-a.stdout` (50-52).
- Not run: the round-21 cold-read monitor and the round-57 counters (out of scope for this seat; the L1 runs them). The cold-read check above is a reference scan, not a monitor run.

## 4. Staged patch for R54.8(b) — fixable-cheap

`stage/corpus/lessons/round-54.md` (full file, sha256 `4bbf44805203a9c459bc441c8670ee9d22d4aba5ca0fac4b6cbe5a7275be8a8e`, base `10068fb8…`) and `stage/R54.8-round-54-lesson.patch` (`diff -u`). The patch appends one section at the end of the file (lines 136–143; no existing byte changes):

```
## Round-54 routed defects — corrections (round 55)

- **R54.8** — the `~/.omp/agent/config.yml` write is recorded in this lesson:
  seat `T54W1ExecStraceNoise` changed `scout` from `@m_grok` to `@m_glm53` outside
  its write scope, and the change was reverted. …
```

Why it is cheap: the file is not in any cold-read ledger input (receipt 06), not frozen by round 54/55/56, and the block contains none of the round-55 stale tokens (`84 staged`, `rekeyed=0/30`, `CTL_POS_c1 true`, `total=14`, `7883e0e5`, `fe70474d`, `097985c1`). The L1 applies it at the content commit. The fixed row for R54.8 then reads: `status fixed`, `commit <content commit>`, evidence `corpus/lessons/round-54.md` lines `139-139`, excerpt `- **R54.8** — the \`~/.omp/agent/config.yml\` write is recorded in this lesson:` (`after_patch` in `rows.json`; fixture B2 verified this exact shape with fixture commit B1 as the commit).

## 5. Judgement calls and findings for the L1

1. **Planned-id rule cannot name R5x.** `planned_ids` in the round-50 counter matches only `\bR4\d\.\d+\b`. An `open` row for any round-50+ item fails `open_unplanned` even when the SCORECARD `Planned (round 55)` paragraph names it (checked: `06`). This is why R54.8 at base fails under the inherited rule. Either the round-57 counter widens the pattern (counter change, your call) or the staged patch lands and R54.8 becomes `fixed`, which needs no Planned line. I recommend the latter.
2. **R54.9 and R54.10 are `fixed` in the lane, while the fleet report copy persists.** The lane's own record (lesson line 51, SCORECARD `ER-R54-9/10`) is correct at base, and the counter reads the lane tree. The fleet report (`.ufo/reports/round-54/tameshi.md`, not in the lane) still prints the old numbers and the misquoted pairing (receipt 08). If you read `fixed` as requiring the fleet copy to be corrected, R54.10 (whose misquote never existed in a lane file) is the one to downgrade, to `declined` with an honest reason; R54.9 would remain `fixed` for the lesson line it corrected.
3. **R54.9 "80" is derived, not measured here.** `staged=81` (`.ufo/evidence/round-55/c1/staged-at-freeze.txt`) includes the refused delta-debugging entry, so the others are 80 [INFERENCE from the spot-check's own statement that the delta-debugging entry is staged].
4. **R54.10 `routed_at`.** The round-50 rule uses the add commit (`650987a`); the R54.10 text was appended later (`0a2010a`). The absence check passes at `650987a`; I did not separately verify `0a2010a`.
5. **R54.8(a)** is closed (receipt `08` shows the seat file's own text still asserts operator authority at line 325, but the SUPERSEDED block at 332 marks it; `9cf0146` added the block). The open part is (b) only.

## 6. Tooling

No installs or upgrades. No PATH directory touched. Scratch `$HYAKU_SCRATCH/tameshi-r57/T57W1ScribeItemsR54x8to10` (fixtures) removed at the end of the seat.

## Files

- `T57W1ScribeItemsR54x8to10/rows.json` — rows with `keys`, `verdict_basis`, `after_patch`
- `T57W1ScribeItemsR54x8to10/ledger-rows.json` — ledger-shaped rows
- `T57W1ScribeItemsR54x8to10/stage/corpus/lessons/round-54.md`, `stage/R54.8-round-54-lesson.patch`
- `T57W1ScribeItemsR54x8to10-receipts/` — 01–08 receipts plus `build.py`, `neg.py`, `locate.py` (the scripts used; they read `$S` and `$HYAKU_SCRATCH`)
- `T57W1ScribeItemsR54x8to10.json` — machine-readable summary
