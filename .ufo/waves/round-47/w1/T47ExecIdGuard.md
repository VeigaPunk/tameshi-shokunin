seat: T47ExecIdGuard
item: prompt section 10 id-collision check + lane guard `tools/staged-id-guard.py`, run in scratch; staged-id guard and renumber map
rev: 9acfbe21435e1976636a276448dee1d5e7155915
base: 0b5b7cd2b2c15d23086e811a0f0348d84261277b
contract: `.ufo/evidence/round-47/contract.json` read; not edited. `tools/` and `corpus/` untouched.
receipts: `.ufo/waves/round-47/w1/T47ExecIdGuard.receipts.md` (both id lists, collisions, renumber map, guard verdict line, can-fail proof, exit-code ledger)

## Axes
Coverage (the adoption half of C3) and calibration (the guard's own honesty surface). This seat is a **receipt** seat: it produced no counter, no registry row, no entry edit and no verdict. The measurement is the collision set, the by-document re-point, and the guard's admissibility of the map the L1 will land.

## Result in one paragraph
The staged package collides with the lane registry on **8 ids, S153–S160**, and the collision is id-only: four of the eight are documents the lane already holds (staged S153→lane S105 POSIX diff, S154→S106 google/golden, S159→lane S155 PIT basic concepts, S160→lane S156 PIT FAQ) and four are new documents. The re-point is by document and matches the frozen contract: **staged S155 (arXiv 2302.09330) → S261, S158 (Lam camera-ready) → S262, S206 (arXiv 2607.09345) → S263, S207 (S2 ICST24 record) → S264**. The guard answers the real pair with `collisions=8 unmapped=0 held=4 cascade=0 next_free=S261 verdict=answered` (exit 0), its `--selftest` passes 24/24, and it can fail: an indented `  | S002 |` registry row against a staged S002 gives `collisions=1 … verdict=refused` (exit 1) while the item's 0-3-space extractor and the guard both see it and a column-zero extractor does not.

## What was run (exact commands)
```
S=/home/vgpnk/Projects/shokuknow; A=/tmp/tameshi-r47-T47ExecIdGuard/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > $A/reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/merge/tameshi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > $A/staged-ids
comm -12 $A/reg-ids $A/staged-ids > $A/collisions
python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py --help
python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py --registry …/corpus/SOURCES.md --staged $S/merge/tameshi/SOURCES.append.md
python3 -I … --registry … --staged … --json
python3 -I … --registry … --staged … --map $A/adoption-map-four.json --json
python3 -I … --registry … --staged … --map $A/adoption-map-r47.json  --json
python3 -I … --registry $A/failreg.md --staged $A/failstaged.md        # indented  | S002 |
python3 -I … --registry $A/failreg-real.md --staged $A/failstaged-real.md --json   # real registry + indented S205
```
Read-only context reads: registry rows S105/S106/S152/S155/S156 and the tail notes at `SOURCES.md:471,474`; round-46 `adoption-map.json`/`guard-map.json`; the three package entries' `source:` lines; every `source:` line in the package's 85 knowledge files.

## Measured facts (all in the receipts file)
- `reg-ids` **120** (S001–S037, S040–S097, S099–S108, S132, S152–S160, S256–S260), `staged-ids` **103** (S153–S255), `collisions` **8**; no duplicate on either side; the registry's id space has **140 gaps**, so S161–S199 and **S200–S255 are absent**.
- Guard admitted-map facts: `safe_floor=S261`, `registry_max=S260`, `staged_max=S255`, `registry_docs=105`, `extractor=0-3space`, `cascade=[]`.
- **S261–S264 are unused as row ids (grep -c → 0, exit 1), absent from all 106 package `source:` lines across 85 files, and absent from every package file.** Denominators recorded.
- Four-entry contract map is **refused** by the guard (`map does not cover every collision: S153,S154,S156,S157,S159,S160`, exit 1). A collision-complete 10-entry map (the four adoptions + four held dedupes + map-only S156→S265, S157→S266) is **admitted** (exit 0, `map_floor=S261`, no clash/staged-clash/below-floor/uncovered). Scratch files kept.

## Findings the L1 owns (details + evidence in the receipts)
1. **Prose conflict on S262–S264.** `corpus/SOURCES.md:471` and `:474` record round-46's map-only reservation “staged S155–S158 to S261–S264”. That map is `S155→S261, S156→S262, S157→S263, S158→S264`; the frozen round-47 contract is `S155→S261, S158→S262, S206→S263, S207→S264`. S261 agrees; **S262, S263, S264 are reassigned**. No landed row is contradicted (round 46 appended none of the four; max row id S260) and the guard reads row ids, not prose, so it admits the contract map — but landing it without amending those two lines leaves the registry stating two documents per id. This seat states the conflict and does not resolve it.
2. **The contract's four-entry map is not guard-admissible on its own.** A `--map` receipt requires every collision decided. Use the admitted 10-entry map (or accept a no-map `answered` run, which is not an adoption map).
3. **Two adopted entries still cite staged ids that have no lane row.** `r8-flakiness-not-static.md:22` cites `S205` (arXiv 1810.05286) and `:34` cites `S208` (tameshi env-diff receipts); `r8-flaky-cost-baseline.md:36` cites `S205`. Lane rows S205/S208 **do not exist** (S200–S255 are gaps), so those ids cannot survive into adopted entries — the sentences need re-grounding to lane-held evidence, or the citation dropped, or two more documents adopted (outside the frozen C3 scope).
4. **`source: S160` in `flaky-aware-verdict-evidence.md` (line 4, plus body lines 26 and 46) must become `S156`**, the lane's PIT FAQ row, not an arithmetic id — the guard's `held` already reports `staged:S160 → S156`. The same entry's S155 (5 occurrences) and S158 (6 occurrences) must become S261 and S262.
5. **Guard diagnostic, one-sided.** `column0_miss` is computed from the **staged** file only, so an indented **registry** row is detected but not reported as a column-zero miss (`column0_miss=[]` on the real-registry probe, while a column-zero registry extractor misses the collision). Detection is correct; only the documented “indented-row proof” field is silent on registry-side indentation. `tools/` was outside my write scope, so it is recorded only (also filed as an observation).

## Files changed
- `.ufo/waves/round-47/w1/T47ExecIdGuard.receipts.md` (new; the named deliverable)
- `.ufo/waves/round-47/w1/T47ExecIdGuard.md` (this report)
No other lane write. No `git`/`jj` mutation, no commit, no sweep of `corpus/` or `tools/`. Scratch confined to `/tmp/tameshi-r47-T47ExecIdGuard/`.

## Tooling
None installed; no pacman transaction. Existing `/usr/bin/python3` and coreutils only.

## Risks
- If the round-47 rows land with the contract ids and lines 471/474 are not amended, a later reader (or the census) sees S262–S264 bound to two documents; the guard will not catch it, because it does not parse prose.
- If an adopting seat applies a naive arithmetic map (the guard prints `S155 naive->S263`), arXiv 2302.09330 would take the id the contract gives arXiv 2607.09345 and the Lam PDF would take an id nothing adopts — an id/document swap that no counter in C3 checks.
- If S205/S208 survive in the adopted entries, the entries cite ids that resolve to nothing in the lane registry; C3's counter would still pass (it counts rows/entries/indexing), so this defect would land silently.

## Blockers
None. The three open items above are L1 decisions, not missing information.
