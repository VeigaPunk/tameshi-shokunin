# RevengerContractFreeze — round-36 contract freeze audit (w1)

Seat: revenger (leaf, read-only). Attacked surface: the freeze ordering of
`.ufo/evidence/round-36/contract.json` — (a) commit-order: contract in the content
commit, every data receipt strictly later; (b) the contract's C2 `counter_sha256` vs the
v2 counter bytes at the refresh commit; (c) C1/C2 targets in contract.json vs the
SCORECARD round-36 block, verbatim.

## Axes (godspeed)

- **Order**: contract commit must be an ancestor of every receipt commit; content commit must contain zero receipt bytes.
- **Pin integrity**: v2 sha256 stable content→refresh→receipts→tip and equal to the contract pin.
- **Parity**: contract C1/C2 targets ↔ SCORECARD block ↔ frozen counter constants ↔ receipt outputs.

## Commit chain (evidence)

Lane tip `HEAD = d9c496b19371b779ce0eec6dfee1b049b27a3a2d`. Linear order at tip:

| # | Commit | When (ISO) | Role |
|---|--------|------------|------|
| 0 | `796e08b888849308d0c4d5e932e56833600a139f` | 2026-10-24T02:50:40-03:00 | round-35 verifier spot-check; parent of content commit; == contract `claims.C1.before.rev` |
| 1 | `e423c41ba253357ab8c8513f0376dad9d38ab248` | 2026-10-24T02:50:40-03:00 | **round-36 content commit** — contract.json + v2 counter + SCORECARD block + LOG/lesson/QUALITY/S103 + wave specs/dispatches/validations |
| 2 | `b455001e2589b3f4f471d94a3de7e5e549b9f54c` | 2026-10-24T03:16:09-03:00 | **round-36 refresh commit** — first data receipt: ledger.json + 4 traces (`coldread/traces/L1/source-{1..4}.json`) + refresh-specs/receipts/affected-sections |
| 3 | `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` | 2026-10-24T03:21:45-03:00 | **round-36 receipts commit** — `after/` (monitor×2, c1v2 deciding, census, depthD) + `control/` (monitor at content commit, v1/v2 at empty panel) |

Findings:

- `git merge-base --is-ancestor e423c41b b455001e` → true; `--is-ancestor e423c41b d9c496b1` → true. Contract commit strictly precedes both receipt commits.
- `git log -- .ufo/evidence/round-36/contract.json` → exactly one commit, `e423c41b`. The contract was **committed in the content commit** and never amended after.
- `git show --stat e423c41b` → 16 files, **none** under `.ufo/evidence/round-36/{after,control,coldread}/`, no `ledger.json`, no `.stdout`/`.exit` receipts. All receipts enter at `b455001e` (refresh data) and `d9c496b1` (run receipts). Receipt-before-contract is structurally impossible in this chain.
- `git log -- .ufo/evidence/round-21/coldread/measure.py` → last touched `370f2dff` (2026-10-21, round-21). Monitor unchanged through round-36 → contract `kill_rule` ("no monitor, ledger-algorithm … change after the before run") holds at commit level.
- `git log -- .ufo/evidence/round-36/c1/c1-measure-v2.py .ufo/evidence/round-35/c1/c1-measure.py` → no round-36 commit after `e423c41b` touches either counter (v1 parent frozen since round-35 `5829676d`).

## sha256 pins

`sha256sum` of worktree; `git show <rev>:<path> | sha256sum` for blobs.

| Object | Rev | sha256 |
|---|---|---|
| contract.json | `e423c41b` (blob) | `3aaabcddf27d49d59f1930643fb52b46a55f0eaa16eeabd0e0767211419db4f9` |
| contract.json | tip worktree | `3aaabcdd…` (identical → contract unmodified since content commit) |
| **c1-measure-v2.py** | `e423c41b` (content) | `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` |
| **c1-measure-v2.py** | `b455001e` (**refresh**) | `9eb8944c…` — **equals contract `claims.C2.counter_sha256`** ✓ |
| c1-measure-v2.py | `d9c496b1` (receipts) / tip worktree | `9eb8944c…` (byte-identical across all four points) |
| round-35 c1-measure.py (v1 parent) | worktree | `d360a159a1ad320e8726eed51256146a90025ce5e5fc97840a488f3a2ad4bbe3` (frozen; untouched in r36) |

## Contract ↔ SCORECARD verbatim parity

SCORECARD.md round-36 block (lines 1730–1776, committed in `e423c41b`, same commit as the contract):

**C1** — contract ↔ SCORECARD:
- axis `calibration` ↔ "calibration (lowest axis)" ✓
- before `calibration_restraint_score 6, sections_covered 60/64` @ `796e08b888849308d0c4d5e932e56833600a139f` ↔ "`calibration_restraint_score: 6, sections_covered 60/64` at r35 tip `796e08b`" ✓ (rev abbreviated to 7-hex in prose)
- counting command `python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev REV` — **byte-identical** in both ✓
- after target `8, 64/64 at the round-36 refresh commit` ✓ identical binding; measured commit named via receipt filename → actual receipt `after/monitor-at-b455001e.stdout` names the refresh commit `b455001e` ✓
- do-nothing control = same command at the content commit, must still print 6 ✓ present in both

**C2** — contract ↔ SCORECARD:
- counter `.ufo/evidence/round-36/c1/c1-measure-v2.py` @ `9eb8944c…` recorded in SCORECARD prose ✓ (full hash verified above)
- frozen targets `PUB_KILL_SLOTS_TARGET 6 / PUB_ACCEPT_SLOTS_TARGET 3 / PUB_DISTINCT_TARGET 9` ↔ "pub_kill=6/6 pub_accept=3/3 pub_distinct=9" ✓; the frozen counter itself carries the same constants (lines 68–70) ✓
- before demonstration: v1 on empty panel prints `C1_R35_PASS=true`, exit 0 ✓ both; after: v2 fails empty panel `C1_R36V2_PASS=false` exit 1 and passes deciding run exit 0 ✓ both
- counting command `python3 .ufo/evidence/round-36/c1/c1-measure-v2.py --lane LANE --rev REV --work EMPTY_DIR --sealed .ufo/evidence/round-35/c1/sealed` — **byte-identical** in both ✓
- measured commit = refresh commit via `c1v2-at-<rev>.stdout` → `after/c1v2-at-b455001e.stdout` names `b455001e` ✓

## Receipt cross-checks (corroboration)

- `after/monitor-at-796e08b.stdout`: `"calibration_restraint_score": 6`, `"sections_covered": 60` (before, matches contract expected).
- `control/monitor-at-e423c41b.stdout`: `6`, `60` (control = record edits alone don't restore credit).
- `after/monitor-at-b455001e.stdout`: `8`, `64` (after target met at refresh commit). All `.exit` files `EXIT=0`.
- `control/v1-at-emptypanel.stdout`: `pub_kill=0/0 pub_accept=0/0 pub_distinct=0 C1_R35_PASS=true`, `V1_EXIT=0` (vacuous accept demonstrated).
- `control/v2-at-emptypanel.stdout`: `pub_kill=0/0 … C1_R36V2_PASS=false`, `V2_EXIT=1` (v2 rejects the vacuous panel).
- `after/c1v2-at-b455001e.stdout`: `pub_kill=6/6 pub_accept=3/3 pub_distinct=9 C1_R36V2_PASS=true`, `EXIT=0`.
- Ledger entries at `e423c41b` = 493 → at `b455001e` = 497 (exactly the contract's four appended entries; SCORECARD "four new ledger entries" ✓).

## Divergences

1. **[minor, label-only]** SCORECARD C1 evidence cell cites the control receipt as `control/monitor-at-content-commit.*`; the committed receipts are named `control/monitor-at-e423c41b.{exit,stderr,stdout}`. Same artifact set, same commit; the row's target numbers are unaffected. Cosmetic filename drift between prose and receipt names.
2. **[epistemic limit]** Git proves record/commit order, not wall-clock run order. Corroboration that no data predates the contract: every receipt self-identifies a rev (`796e08b…`, `e423c41b…`, `b455001e…`) and the runs at `e423c41b`/`b455001e` bind outputs to commits that did not exist before `e423c41b`; receipt bytes only enter the history in commits 2–3. That no *uncommitted* run happened earlier is [INFERENCE] from the kill-rule's commit-binding design, not a git-provable fact.

## Verdict

**VERDICT: FREEZE HOLDS** — contract.json committed in content commit `e423c41b` (2026-10-24T02:50:40-03:00) with zero receipt bytes and never amended; all data receipts land strictly later (`b455001e` refresh, `d9c496b1` receipts, both descendants); the contract's v2 pin `9eb8944c…` equals the v2 counter bytes at the refresh commit (and at every later point); C1/C2 targets in the contract match the SCORECARD round-36 block verbatim in values, revs, commands, and measured-commit bindings. One cosmetic label divergence (`monitor-at-content-commit.*` vs `monitor-at-e423c41b.*`), no substantive divergence.

Tooling: none installed (system `git`, `python3`, `sha256sum`, `grep` only; `pacman` untouched per bounds). All git invocations read-only under `--no-optional-locks`.
