# T57W1ScribeItemsR53x4to6 — ledger rows R53.4–6 (round 57, wave 1)

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `5e3569969b532310d2b8a3d130901757a3df356b`.
Spot-check: `corpus/lessons/round-53-verifier-spotcheck.md`, routed items R53.4, R53.5, R53.6 (items 4–6 of `## Routed defects (lane must fix next round)`). Spot-check added at `2ef0a5ad429de7f204b0e8138b2f36dcbb32a626` (`routed_at`).
No lane production file was edited; no mutating git ran in the lane. Fixture and integration commits were made only in a scratch clone (`$HYAKU_SCRATCH/tameshi-r57/T57W1ScribeItemsR53x4to6/clone`, removed at end).
Tools installed: none. No tool installs or upgrades were needed.

## Verdicts

| id | status at base | classification | fix status | commit (fixed only) |
|---|---|---|---|---|
| R53.4 | open | fixable-cheap (staged) | defect still holds | — |
| R53.5 | open | receipt part fixable-cheap (staged); LOG pointer part fixable-costly | defect still holds | — |
| R53.6 | fixed | already fixed, nothing staged | fixed by round-54 C0 | `59c38109bf119d0e9d4f878644a82babc937bc1e` |

### R53.4 — committed C2 receipt unanchored (open)
- Spot-check claim: `.ufo/waves/round-53/w1/T53W1ExecTmpVerify-receipts/c2-counter-repaired.stdout` names rev `9c6ef7bc80c0` and records `cr47=rc=1`.
- Still true at base. `git cat-file -t 9c6ef7bc80c0` → `fatal: Not a valid object name` (rc 128). `git log 2ef0a5a..5e3569969b5 -- <receipt>` is empty; the file at base still reads `C2_R53: rev=9c6ef7bc80c0 … cr47=rc=1 … C2_R53_PASS=true`. Receipts: `T57W1ScribeItemsR53x4to6-receipts/git-sweep-R53.4-R53.6.txt`.
- Staged fix (`fixable-cheap`): `stage/.ufo/waves/round-53/w1/T53W1ExecTmpVerify-receipts/c2-counter-repaired.stdout`. It is the output of the frozen round-53 counter run at base: `python3 .ufo/evidence/round-53/c2/measure.py --lane <clone@base> --rev 5e3569969b532310d2b8a3d130901757a3df356b --work <empty> --explain` → `C2_R53: rev=5e3569969b53 tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=2 docs=ok total=0 C2_R53_PASS=true` (exit 0). The `cr47=rc=2` value also confirms R53.6 at base.
- Cold-read pins: `.ufo/waves/round-53/...` pinned by 0 ledger entries (receipts: `coldread-pin-sweep.txt`). No uncredited heading.

### R53.5 — committed freeze receipt and pointer stale (open)
- Spot-check claim: `.ufo/evidence/round-53/verify-freeze.stdout` reads `amendments=5`; LOG pins `freeze e62d9971 (amendments 1–5)`; `cf872769` is never named.
- Still true at base. `.ufo/evidence/round-53/verify-freeze.stdout` line 1 = `FREEZE e62d99711a0d files=8 amendments=5` (unchanged since 2ef0a5a). `.ufo/evidence/round-53/freeze.json` at base lists seven amendments (`"n": 7` at line 48); `9e09db2` (amendment 7, the freeze of record) is an ancestor of base. LOG.md lines 2468–2469 still read ``freeze `e62d9971` (amendments`` / ``1–5, all disclosed in `freeze.json`).``
- Staged cheap part (`fixable-cheap` on its own): `stage/.ufo/evidence/round-53/verify-freeze.stdout` = `bash .ufo/evidence/round-53/verify-freeze.sh <clone@base> 9e09db2` (rc 0): `FREEZE 9e09db2 files=8 amendments=7`, seven `AMENDMENT` lines, `FREEZE_INTEGRITY: OK`. Pinned by 0 ledger entries.
- Costly part (not staged): the LOG.md pointer. Diff at `costly/LOG-pointer.diff` (checked with `git apply --check` against base: applies). `LOG.md` is pinned as a whole-file input by **10** cold-read ledger entries (strict filter: lane-relative inputs and `tameshi@` external inputs only). Headings they would uncredit at the next monitor run: `## The cadence's first scheduled tick, and the service's limits (round 9, measured)`; `## Final pointers — the standing map at the arc's close (round 11, measured)`; `### The map — where a reader enters, artifact by artifact` (3 entries); `## Standing rules` (2 entries); `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (3 entries). Marginal cost is zero only if this LOG.md edit lands in the same content-final commit that the wave-3 re-key already targets.
- Without the LOG pointer the item is partial: a receipt refresh alone does not fix the stated defect.

### R53.6 — CR47 exit-class mapping incomplete in four tools (fixed)
- Spot-check claim: `bash-witness-study`, `env-diff`, `evidence-disposition`, `pin-disposition` raise an uncaught RuntimeError (rc 1) on a set-but-unusable TMPDIR, instead of exit 2.
- Fixed by `59c38109bf119d0e9d4f878644a82babc937bc1e` (round-54 C0, touches all four tools; not an ancestor of `2ef0a5a`; an ancestor of base). Runtime check, scratch clone, `TMPDIR=/nonexistent-r57-tmpdir`:
  - at base `5e3569969b53`: all four exit **2** with `could-not-evaluate` text (`env-diff`, `evidence-disposition`, `pin-disposition` via `--selftest`; `bash-witness-study` via its `selftest` mode, since `--selftest` is not a flag there and returns 64). Good-TMPDIR control `bash-witness-study selftest` → `WITNESS_SELFTEST: 51/51 pass`, `VERDICT: PASS`.
  - at `2ef0a5a`: all four exit **1** with an uncaught `RuntimeError: cannot create clone scratch … (could-not-evaluate)` traceback.
  - Round-53 counter at base: `cr47=rc=2`, `C2_R53_PASS=true`.
- Receipts: `T57W1ScribeItemsR53x4to6-receipts/*badTMPDIR*`.
- Nothing staged, nothing to uncredit. Note: this fix predates the round-56 base, so it does not count toward the round-57 post-base fix floor (the round-50 counter counts only commits that are not ancestors of base).

## Ledger rows (base state)
Written to `.ufo/waves/round-57/w1/T57W1ScribeItemsR53x4to6/rows.json` (rows with `keys` and `verdict_basis`; strip `keys` and `verdict_basis` before writing to `corpus/routed-defects.json`, the ledger schema has no such fields). Evidence was resolved with `check_evidence` imported from the round-50 counter (`.ufo/evidence/round-50/c1/measure.py`), not copied. Every evidence item resolves at base (3 + 1 + 4 items, all keyed at least once).

Also written: `.ufo/waves/round-57/w1/T57W1ScribeItemsR53x4to6/rows-after-integration.json`, the rows as they would read after integrating the staged patches (commit hashes are simulated and must be replaced).

## Round-50 counter run on the rows
- Fixture commit: the three base-state rows in a scratch clone commit, `routed_at=2ef0a5a`, spot-check hash pinned to base bytes. `measure(…)` → `stat={'fixed': 1, 'open': 2, 'declined': 0, 'fixed_this_round': 1}`, `counts={'open_unplanned': 2}`, `total=2`. R53.6 passes the fixed rule (commit touches keyed paths, excerpts absent at `routed_at`, no ACK words).
- The two open rows fail only `open_unplanned`. The round-50 `planned_ids` regex is `\bR4\d\.\d+\b`, so it cannot see any R5x id; the newest `**Planned (round` paragraph at base is round 55 and names no R53 ids. **The round-57 counter must either extend that regex to R5x or the L1 must plan R53.4/R53.5 in the round-57 SCORECARD Planned paragraph.** I did not change the counter.
- Integration simulation: a scratch clone commit adds the two staged receipts (commit A) and the LOG pointer (commit B), and a ledger commit C with R53.4 and R53.5 as `fixed` and R53.6 as `fixed`. `measure(…)` → `stat={'fixed': 3, 'open': 0, 'declined': 0, 'fixed_this_round': 3}`, `total=0`. That run includes the costly LOG edit; with only commit A, R53.5 cannot honestly be `fixed`.

## Options for the L1 (decisions are the L1's)
1. Integrate the staged receipt refresh (R53.4, cheap) → R53.4 `fixed` with that commit (counts as a post-base fix). Its excerpt is `C2_R53: rev=5e3569969b53 …` (keys `c2-counter-repaired.stdout`, `5e3569969b53`, `cr47=rc=2`).
2. R53.5: `open` and planned, unless the LOG.md pointer edit lands in the round-57 content commit; then `fixed` with both `.ufo/evidence/round-53/verify-freeze.stdout` and the LOG.md line as evidence.
3. R53.6: keep `fixed` at `59c3810…`; pre-base.

## Not verified / limits
- I did not run the round-21 cold-read monitor; the pin counts are from the ledger JSON, not from a monitor run.
- I did not run any round-53 counter other than c2 and the freeze check; C1 round-53 was out of scope.
- The 'open' verdicts rely on the stated defects still being present at base (receipt text and freeze text), not on a semantic judgement of the rev-binding rule.
- `bash-witness-study.py` has no `--selftest` flag (the spot-check's invocation); the mode is `selftest`. Recorded in receipts.

## Sources of receipts
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeItemsR53x4to6-receipts/`: counter output, freeze output, bad-TMPDIR stderr at base and at `2ef0a5a`, git sweep, cold-read pin sweep, round-50 measure runs.
