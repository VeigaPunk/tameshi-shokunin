# T57W1ScribeItemsR50x1to4 — ledger rows R50.1-4 (round 57, wave 1)

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `5e3569969b532310d2b8a3d130901757a3df356b`.
Item: the four routed items of `corpus/lessons/round-50-verifier-spotcheck.md` (`## Routed defects for the lane next round`, lines 98-101; the spot-check was added at `9962033fd7a75aa2f2847e979dd687a5d28505a1`, which is the `routed_at` used by the rule).
Machine-readable output: `T57W1ScribeItemsR50x1to4.json`; rows: `T57W1ScribeItemsR50x1to4/rows.json` (sha256 `69137249c2aa17d6c57c36bc5dc9462f944da77bb6e84b27adc9b2bb3d287da7`); receipts: `T57W1ScribeItemsR50x1to4-receipts/`.
No lane file was edited. Nothing was installed or upgraded. The stage directory `T57W1ScribeItemsR50x1to4/stage/` is empty, because no item was open and cheaply fixable.

## Verdicts

| id | status | commit | basis (short) | fixable (residual) |
|---|---|---|---|---|
| R50.1 | fixed | `6d8c11e378aa90b12650808e1b79270742935f15` | S022 is `mined` at base, with used-by naming `corpus/knowledge/fixture-shrinking-pilot.md`; the excerpt was `queued` at the routing commit | n/a |
| R50.2 | fixed (residual disclosed) | `6d8c11e378aa90b12650808e1b79270742935f15` | the rows for `tools/shrink-case.py` and `tools/pbt-staged-id.py` exist in the round-51 registry block (`SKILL.md:2193`, `:2201`), with exit-2 maps and selftests; absent at routing | fixable-costly: `SKILL.md:1548` still reads "Registry scope is these round-12 instruments" (heading `## Repeated controls and gate registry — round 12`, `SKILL.md:1521-1558`); any SKILL.md byte change re-keys the 92 ledger entries that pin SKILL.md |
| R50.3 | fixed (residual disclosed) | `6d8c11e378aa90b12650808e1b79270742935f15` | the superseding F6/F10 rows at `corpus/README.md:621` and `:625` (held round 50 / held round 49) match the sections at `:608` and `:599`; absent at routing | fixable-costly: the original cells `README:83` and `:87` still read `open`; `corpus/README.md` is pinned by 109 ledger entries (headings in § Costly edits) |
| R50.4 | open | — | the carried seven (R45.1, R45.4, R46.2, R47.5, R48.4, R49.3, R49.5) remain `open` in the base ledger and no lesson 51-56 or SCORECARD section records any closed; the forgery-route successor counters named in the round-51 plan are not in the tree | not-fixable in this seat (the work is the seven rows and the successor counters) |

No row is `declined`. No row is `unresolved`.

## Evidence (every excerpt resolves at base; none is in a spot-check, the ledger or a round-57 C1/control file)

- R50.1: `corpus/SOURCES.md:33` `| mined | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |`; `corpus/lessons/round-51.md:12` `Rows touched: S022 status \`queued\` → \`mined\``.
- R50.2: `SKILL.md:2193` `| pbt staged-id generator | gate | \`python3 tools/pbt-staged-id.py --guard …\``; `SKILL.md:2201` `| shrink-case | probe | \`python3 tools/shrink-case.py --pristine …\``.
- R50.3: `corpus/README.md:621` `| F6 | fixture minimization for survivors | S022, S023, S024, S271 | held (round 50) — README.md:608`; `corpus/README.md:625` `| F10 | PBT generators for gate fixtures | … | held (round 49) — README.md:599`.
- R50.4: `SCORECARD.md:2433` `**Planned (round 51):** the seven routed items the round-50 ledger leaves open` and the same line's `successor C1/C2 counters that close the forgery routes disclosed in round 50`; `corpus/lessons/round-50.md:121` `both round-50 frozen counters admit forgeries a mechanical check cannot see`.

Keys (2-4 per id, all present in at least one excerpt): R50.1 `S022, fixture-shrinking-pilot.md, mined`; R50.2 `shrink-case, pbt-staged-id, Gate/probe registry`; R50.3 `F6, F10, README.md:608, README.md:599`; R50.4 `Planned (round 51), forgery routes, successor C1/C2, R45.1`.

## Checks run (commands and outputs in the receipts directory)

1. `build-rows.stdout` — the four items extracted from the spot-check at base (`ITEM R50.1..4`); every evidence item passes the round-50 resolver `check_evidence` (`EXCERPT … ok` ×9); the staged round-57 `judge()` (imported, not copied) returns no fault for R50.1-3 and for R50.4 with `R50.4` in the planned set.
2. `controls.stdout` — `CONTROLS_OK`. Negative controls, each refused with the named term: N1 fix commit equal to the routing commit (`fixed_bad`); N2 excerpt already present at routing (`fixed_bad`, `fixed-not-new`); N3 wrong keys (`key_miss`); N4 open without planned naming (`open_unplanned`); N6 short decline reason (`declined_bad`); N7 fix commit not touching the evidence path (`fixed_bad`). N5 (open with planned naming) passes. Every evidence excerpt of a fixed row is absent at `9962033` (`ABSENT_AT_ROUTED … present=False`, six rows).
3. `extract-base.json` — the staged round-57 extractor run at base: 51 items total; R50.1-4 keys defaulted to `['queued','used-by','corpus/knowledge/fixture-shrinking-pilot.md','mined','S022']`, `['tools/shrink-case.py','tools/pbt-staged-id.py','### Gate/probe registry',':1499-1509', …]`, `['corpus/README.md:83','open',':599',':608']`, `['## C1','## C2','Planned (round 51)']`. Rows pass with these default keys too (`DEFAULT_KEYS_OK`).
4. `greps.txt`, `successor-forgery.txt` — git-log pickaxes for the fix commit (`6d8c11e` only, for S022, the SKILL rows and the README superseding rows); routing-time absence (`0` for all three); the seven open ids appear in one lane file (SCORECARD:2433) at base; the base ledger status of the seven is `open`; `git ls-tree` finds no forgery-route successor C1/C2 counter (only the round-18 and round-50 successor files and `round-52/control/C2_CTL_FORGE.stdout`, which is a round-52 record-correction control, not a forgery successor).

The round-50 resolver and the round-57 judge were imported with `sys.dont_write_bytecode` set; no lane tree or ledger was written.

## Required L1 actions

1. **R50.4 needs a planned name.** `open` passes only if the id appears in the newest `**Planned (round` paragraph of SCORECARD at REV. The round-57 counter's pattern `\bR5[0-6]\.\d+\b` matches `R50.4`. Control N4 shows the refusal without it. Name R50.4 in `**Planned (round 57)**` at the content commit.
2. **Floors.** R50.1-3 are fixed by `6d8c11e`, which is an ancestor of base, so they count toward `fixed` but not toward `this_round` (the counter counts only commits after BASE). This seat does not decide the floors.
3. **Keys.** The rows' keys and the staged extractor's default keys both pass for these four ids; no manual keys entry is needed for them.
4. **Staged counter.** I verified against the staged round-57 `measure.py` (`T57W1ExecC1Counter`). It is not frozen; if its `judge()` changes before freeze, re-run `T57W1ScribeItemsR50x1to4-receipts/build_rows.py`.

## Costly edits (not proposed as staged patches)

- `corpus/README.md` is an input to 109 ledger entries. Any byte change to it re-keys them, under the round-21 ledger's whole-file inputs. The headings uncredited would be: `# tameshi-shokunin` (14), `### The map — where a reader enters, artifact by artifact` (24), `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (27), `## Restore discipline — before/after identity, not continuous non-write proof` (16), `## Restore discipline — proof the substrate never moved` (5), `## Live-tree re-pin and entry-command monitor — round 17` (6), `### Triggers T1–T3 and the re-pin rule` (5), `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` (4), `## Standing rules` (4), `### Where to enter — four readers` (1), `### Round-20 gate/probe registry — frozen receipt instruments` (1), `## The cadence's first scheduled tick, and the service's limits (round 9, measured)` (1), `## Ninth recorded case — round 26` (1).
- `SKILL.md` is an input to 92 ledger entries, including `## Repeated controls and gate registry — round 12` (the heading that carries the `:1548` sentence). `SKILL.md` line counts are unchanged by a one-line edit, but the input sha changes.

## Not verified

- Semantic support. The counter checks presence and newness of an excerpt, not that the superseding README table is correct. I re-read only the F6/F10 superseding rows against the sections they cite.
- R50.1's freshness-monitor clause ("re-base or supersede that monitor, or record the exception"). I did not check it; the round-51 lesson logs the status change.
- The seven open rows' own defects. I checked only their base ledger status and the absence of a closure claim in lessons 51-56 and SCORECARD; I did not re-derive each one against the tree.
- The round-57 counter was not run as a counter (it is not frozen and the instruction says the L1 scores); `judge()` was run by import only.
