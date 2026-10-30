# T58W2ScoutCT — considerthese confirmation (round 58 wave 2)

Seat: scout · base `2a32aa8228d5f86a85c81a923a3148bf792a9538` · C0 `8063d0a551fc5b3cb5a2d397da7353af53444534` (verified lane head: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline -3` → `8063d0a5` on top).

## The ONE proposal: `considerthese/2026-10-28.md` proposal 2 — counter-arm liveness check

Verbatim (lines 77–78 at C0, byte-for-byte from `git show 8063d0a5…:considerthese/2026-10-28.md`):

> 2. **Counter-arm liveness check.** For each frozen counter, list its arms and require one committed input per arm that moves
>    that arm's tally away from zero. A passing control set did not reveal that round 53's re-key arm could never fire.

**Unimplemented at C0.** Sweeps (all in a fresh shared clone detached at C0):

1. **No instrument carries it.** `git ls-tree --name-only C0 tools/ | grep -iE 'arm|liveness|fire|burn|assim|pointer|stale|drift'` → no output (exit 1). `scripts/` is empty. No `arm-census` path exists outside retained seat receipts under `.ufo/waves/round-55/w1/T55W1ScribeConsiderthese-receipts/` — the round-55 scribe's draft (`arm-census.py`, census: 63/414 arms live at base `0a2010ac`, 68/428 at freeze `631cd64`) was never landed; `.ufo/evidence/round-56/` holds only the no-harm trio, no `quality/` dir.
2. **No criterion carries it.** `git grep -iE "arm.liveness|away from zero|one committed input per arm" C0 -- ':!considerthese' ':!.ufo/waves'` hits only: the round-57/58 **c1** counter selftest comment (`c1/measure.py:510`/`:514` — "moves its tally away from zero (round-53 lesson: a counter arm that can never fire)"), the round-57/58 **c2** selftest docstring (`c2/measure.py:54`/`:59` — "one fixture per arm moves that arm away from zero"), and the unrelated literal `counter-arm` in `tools/mutate-and-run.sh:1863`. QUALITY **criterion 105** (round 54) is the nearest neighbour and does not cover the proposal: its credit line is `corpus/lessons/round-54.md ## Mistakes`, not considerthese, and it requires positive controls per arm only *within a round's control set* for manifest-reading arms — not a standing census over every frozen counter. 30 frozen `cN/measure.py` files exist at C0 (plus non-`cN` named counters such as `round-23/final-measure.py`, `round-25/c1-measure.py`); nothing enumerates their arms.
3. **Sequencing leaves it as the pick.** Round-56 lesson (`corpus/lessons/round-56.md:28-33`): proposal 1 mined into criterion 107 (revision half landed; the byte-for-byte quote half is declared unmined in the criterion's own scope sentence), "Proposals 2–5 remain unmined (at most one per round)"; round 57 then mined proposal 3 (`tools/cold-read-forecast.py`). Remaining from the latest file at C0: **2, 4, 5**. Round 55's scribe had already picked 2 with the same unimplemented verdict (`.ufo/waves/round-55/w1/T55W1ScribeConsiderthese.json`: `"implemented": false` — "no tool/criterion enumerates a counter's arms and requires a committed input per arm; QUALITY 105 … only proves non-zero passing arms on a positive control"); round 55 was rejected-harmed and nothing landed.
4. **It is this round's failure class.** The decisive wave-1 finding is the bent-runner forgery in `.ufo/waves/round-58/w1/T58W1RevengerC2-receipts/`: `attack.py` Attack B swaps in a claimant-authored `registry-check.py` ("the executed AND mutants arms are then produced by claimant code"); `honest-run.txt` (six `EXPLAIN shortfall …=0` rows from the real executor) versus `attack-out.txt` shows the counter printing `C2_R58_PASS=true` with execution arms that never genuinely fired. That is precisely an arm whose tally moves without a committed input — the dead-arm class the proposal names, and the class of the recarried R53.1 (Planned round 59: "frozen rekey counter's directory discovery is structurally dead; publish a successor").
5. **Alternatives checked and set aside.** Proposal 4 (assimilation backlog burn-down) and proposal 5 (stale-closure-pointer sweep) are also unimplemented at C0 (tree grep: no burn-down/backlog instrument; `tools/pointer-check.py` strips `:N` suffixes and never re-resolves line/page pointers), but nothing round 58 does touches them: C3 adopted exactly one `merge/tameshi` entry with no backlog census, and the only pointer work this round is the single routed R53.5 correction (`new_fixes.R53.5 = 764f87bc…` in `.ufo/waves/round-58/l1/facts.json`), a repair, not a standing sweep.

## Identification caveat

INFERENCE: the L1 names the mined proposal in the round-58 report (`contract.json:122` "considerthese mined separately in the report"), which is not yet written, and wave-1's considerthese seat `T58W1ScoutCT` returned empty output (`w1-results.json` results[36]), so no wave-1 pick exists to confirm. The identification of proposal 2 rests on the evidence above (latest-file preference per the wave-1 spec, r56 ordering, r55 precedent, and the round's counter-integrity substance). If the L1 names 4 or 5 instead, the same sweeps confirm both unimplemented; the JSON records their results.

## Precedent for the report line

Round 57's contract wrote: *"considerthese/2026-10-28.md proposal 3 (cold-read cost forecast at planning time) mined as a lesson + QUALITY criterion + tools/forecast tool if landed"*. A round-58 analogue for proposal 2 could route to a lesson/criterion in the 105 family plus the R53.1 successor already in Planned (round 59); the retained r55 census draft is a starting point that was never committed.

## Hygiene

Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2ScoutCT` (shared C0 clone) created for the sweeps and **removed before yield**. No lane file edited; no tool installed. Machine-readable output: `T58W2ScoutCT.json` beside this report.
